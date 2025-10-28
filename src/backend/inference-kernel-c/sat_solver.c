#include <immintrin.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// sat_solver.c - SIMD-optimized SAT solver core with GPU/WebGPU hooks

// Types
typedef int32_t lit_t;
typedef uint32_t var_t;

typedef struct { uint32_t size; lit_t* lits; uint16_t w0, w1; float activity; } clause_t;
typedef struct { uint32_t n_vars, n_clauses; clause_t* clauses; } cnf_formula_t;

typedef struct { int8_t* assign; int8_t* polarity; } assignment_t;

typedef struct { uint32_t* clause_idx; uint16_t* watch_pos; uint32_t size, capacity; } watch_list_t;

typedef struct {
    cnf_formula_t* f; assignment_t asg;
    watch_list_t* watches_pos; watch_list_t* watches_neg;
    lit_t* trail; uint32_t trail_sz, trail_cap;
    uint32_t* dl_stack; uint32_t dl_top;
    float* var_act; float var_decay; float cls_decay; uint32_t restart_interval;
} solver_t;

static inline var_t lit_var(lit_t l){ return (var_t) (l>0? l : -l); }
static inline lit_t lit_neg(lit_t l){ return -l; }
static inline int8_t lit_value(const assignment_t* a, lit_t l){ int8_t v=a->assign[lit_var(l)]; return l>0? v : (int8_t)-v; }

// SIMD helpers
static inline __m256i mm256_abs_epi32(__m256i v){ __m256i m=_mm256_srai_epi32(v,31); __m256i x=_mm256_xor_si256(v,m); return _mm256_sub_epi32(x,m);} 

static int clause_eval_simd(const clause_t* c, const assignment_t* a){
    int n=(int)c->size, i=0;
    __m256i any_true=_mm256_setzero_si256(), any_unk=_mm256_setzero_si256();
    while(i+8<=n){
        __m256i lits=_mm256_loadu_si256((const __m256i*)(c->lits+i));
        __m256i vabs=mm256_abs_epi32(lits);
        const int8_t* base=a->assign;
        __m256i asg32=_mm256_i32gather_epi32((const int*)base, vabs, 1);
        __m256i zero=_mm256_setzero_si256();
        __m256i signmask=_mm256_cmpgt_epi32(zero, lits);
        __m256i low8=_mm256_slli_epi32(asg32,24);
        __m256i val=_mm256_srai_epi32(low8,24);
        __m256i nval=_mm256_sub_epi32(zero,val);
        __m256i litval=_mm256_blendv_epi8(val,nval,signmask);
        __m256i is_true=_mm256_cmpeq_epi32(litval,_mm256_set1_epi32(1)); any_true=_mm256_or_si256(any_true,is_true);
        __m256i is_unk=_mm256_cmpeq_epi32(litval,zero); any_unk=_mm256_or_si256(any_unk,is_unk);
        i+=8;
    }
    if(!_mm256_testz_si256(any_true,_mm256_set1_epi32(-1))) return 1;
    bool tail_true=false, tail_unk=false; for(;i<n;++i){ int8_t v=a->assign[abs(c->lits[i])]; int8_t lv=(c->lits[i]>0)?v:(int8_t)-v; if(lv==1){tail_true=true;break;} if(lv==0) tail_unk=true; }
    if(tail_true) return 1;
    if(!_mm256_testz_si256(any_unk,_mm256_set1_epi32(-1))||tail_unk) return 0;
    return -1;
}

static bool enqueue_lit(solver_t* s, lit_t l){ var_t v=lit_var(l); int8_t val=(l>0)?1:-1; int8_t cur=s->asg.assign[v]; if(cur!=0) return cur==val; if(s->trail_sz==s->trail_cap){ s->trail_cap=s->trail_cap? s->trail_cap*2:1024; s->trail=(lit_t*)realloc(s->trail,sizeof(lit_t)*s->trail_cap);} s->asg.assign[v]=val; s->trail[s->trail_sz++]=l; return true; }

static bool watch_scan_update_simd(solver_t* s, lit_t assigned){
    var_t v=lit_var(assigned); bool neg=assigned<0; watch_list_t* wl=neg? &s->watches_neg[v] : &s->watches_pos[v];
    uint32_t N=wl->size, i=0; const uint32_t stride=8;
    while(i+stride<=N){ __m256i idx=_mm256_loadu_si256((const __m256i*)(wl->clause_idx+i)); __m256i wpos=_mm256_loadu_si256((const __m256i*)(wl->watch_pos+i)); uint32_t lanes[8]; uint16_t wps[8]; _mm256_storeu_si256((__m256i*)lanes,idx); _mm256_storeu_si256((__m256i*)wps,wpos); for(int k=0;k<8;++k){ clause_t* c=&s->f->clauses[lanes[k]]; uint16_t wp=wps[k]; uint16_t other=(wp==c->w0)?c->w1:c->w0; int8_t vwatch=lit_value(&s->asg,c->lits[wp]); if(vwatch==1) continue; bool moved=false; for(uint16_t j=0;j<c->size;++j){ if(j==c->w0||j==c->w1) continue; int8_t vj=lit_value(&s->asg,c->lits[j]); if(vj!=-1){ if(wp==c->w0) c->w0=j; else c->w1=j; moved=true; break; } } if(!moved){ int8_t vother=lit_value(&s->asg,c->lits[other]); if(vother==-1) return false; if(vother==0){ if(!enqueue_lit(s,c->lits[other])) return false; } } } i+=stride; }
    for(;i<N;++i){ uint32_t ci=wl->clause_idx[i]; uint16_t wp=wl->watch_pos[i]; clause_t* c=&s->f->clauses[ci]; uint16_t other=(wp==c->w0)?c->w1:c->w0; int8_t vwatch=lit_value(&s->asg,c->lits[wp]); if(vwatch==1) continue; bool moved=false; for(uint16_t j=0;j<c->size;++j){ if(j==c->w0||j==c->w1) continue; int8_t vj=lit_value(&s->asg,c->lits[j]); if(vj!=-1){ if(wp==c->w0) c->w0=j; else c->w1=j; moved=true; break; } } if(!moved){ int8_t vother=lit_value(&s->asg,c->lits[other]); if(vother==-1) return false; if(vother==0){ if(!enqueue_lit(s,c->lits[other])) return false; } } }
    return true;
}

static bool unit_propagation_simd(solver_t* s){ uint32_t head=0; while(head<s->trail_sz){ lit_t l=s->trail[head++]; if(!watch_scan_update_simd(s,l)) return false; } return true; }

static var_t pick_branch_var(const solver_t* s){ var_t best=0; float ba=-1.0f; for(var_t v=1; v<=s->f->n_vars; ++v){ if(s->asg.assign[v]==0 && s->var_act[v]>ba){ ba=s->var_act[v]; best=v; } } return best; }

static bool cdcl_solve(solver_t* s){ if(!unit_propagation_simd(s)) return false; for(;;){ var_t v=pick_branch_var(s); if(v==0) return true; lit_t l = s->asg.polarity[v]>=0 ? (lit_t)v : (lit_t)(-((int32_t)v)); s->dl_stack[s->dl_top++]=s->trail_sz; if(!enqueue_lit(s,l)) return false; if(!unit_propagation_simd(s)){ if(s->dl_top==0) return false; uint32_t back=s->dl_stack[--s->dl_top]; while(s->trail_sz>back){ var_t rv=lit_var(s->trail[--s->trail_sz]); s->asg.assign[rv]=0; } lit_t alt=-l; if(!enqueue_lit(s,alt)) return false; if(!unit_propagation_simd(s)) return false; } } }

static bool dpll_solve(solver_t* s){ if(!unit_propagation_simd(s)) return false; var_t v=pick_branch_var(s); if(v==0) return true; lit_t l = s->asg.polarity[v]>=0 ? (lit_t)v : (lit_t)(-((int32_t)v)); uint32_t save=s->trail_sz; if(enqueue_lit(s,l) && unit_propagation_simd(s) && dpll_solve(s)) return true; while(s->trail_sz>save){ var_t rv=lit_var(s->trail[--s->trail_sz]); s->asg.assign[rv]=0; } if(enqueue_lit(s,-l) && unit_propagation_simd(s) && dpll_solve(s)) return true; while(s->trail_sz>save){ var_t rv=lit_var(s->trail[--s->trail_sz]); s->asg.assign[rv]=0; } return false; }

// DIMACS parser
static cnf_formula_t* parse_dimacs(FILE* fp){ char line[4096]; uint32_t nvars=0,nclauses=0; while(fgets(line,sizeof(line),fp)){ if(line[0]=='c') continue; if(line[0]=='p'){ sscanf(line,"p cnf %u %u",&nvars,&nclauses); break; } }
    cnf_formula_t* f=(cnf_formula_t*)calloc(1,sizeof(cnf_formula_t)); f->n_vars=nvars; f->n_clauses=nclauses; f->clauses=(clause_t*)calloc(nclauses,sizeof(clause_t));
    uint32_t ci=0; uint32_t cap=16; lit_t* buf=(lit_t*)malloc(cap*sizeof(lit_t));
    while(ci<nclauses && fgets(line,sizeof(line),fp)){
        if(line[0]=='c' || line[0]=='p' || line[0]=='\n') continue; char* tok=strtok(line," \t\r\n"); uint32_t sz=0; while(tok){ int v=atoi(tok); if(v==0){ clause_t* c=&f->clauses[ci++]; c->size=sz; c->lits=(lit_t*)malloc(sizeof(lit_t)*sz); memcpy(c->lits,buf,sizeof(lit_t)*sz); c->w0=0; c->w1=sz>1?1:0; c->activity=0.0f; sz=0; break; } else { if(sz==cap){ cap*=2; buf=(lit_t*)realloc(buf,sizeof(lit_t)*cap);} buf[sz++]=v; } tok=strtok(NULL," \t\r\n"); }
    }
    free(buf); return f;
}

// Proof logging (DRAT-like minimal stubs)
typedef struct { FILE* fp; } proof_t; static proof_t proof_open(const char* path){ proof_t p; p.fp = path? fopen(path,"wb"):NULL; return p;} static void proof_add_clause(proof_t* p, const clause_t* c){ if(!p->fp) return; for(uint32_t i=0;i<c->size;++i){ fprintf(p->fp, "%d ", c->lits[i]); } fputs("0\n", p->fp);} static void proof_close(proof_t* p){ if(p->fp) fclose(p->fp); }

// GPU acceleration hooks (stubs) for parallel search
typedef struct { void* cuda_ctx; void* hip_ctx; void* vk_ctx; } gpu_ctx_t;
static gpu_ctx_t* gpu_init(){ gpu_ctx_t* g=(gpu_ctx_t*)calloc(1,sizeof(gpu_ctx_t)); return g; }
static void gpu_release(gpu_ctx_t* g){ free(g); }
static void gpu_parallel_branch_eval(gpu_ctx_t* g, const cnf_formula_t* f, const assignment_t* a, const lit_t* branch_lits, uint32_t count){ (void)g;(void)f;(void)a;(void)branch_lits;(void)count; }

// WebGPU compute shader integration stubs
typedef struct { void* device; void* queue; void* pipeline; } webgpu_ctx_t;
static webgpu_ctx_t* webgpu_init(){ webgpu_ctx_t* w=(webgpu_ctx_t*)calloc(1,sizeof(webgpu_ctx_t)); return w; }
static void webgpu_release(webgpu_ctx_t* w){ free(w); }
static void webgpu_clause_eval(webgpu_ctx_t* w, const cnf_formula_t* f, const assignment_t* a){ (void)w;(void)f;(void)a; }

// Public solve entry
bool solve_cnf_dimacs(FILE* fp){ cnf_formula_t* f=parse_dimacs(fp); if(!f) return false; solver_t s={0}; s.f=f; s.asg.assign=(int8_t*)calloc(f->n_vars+1,sizeof(int8_t)); s.asg.polarity=(int8_t*)calloc(f->n_vars+1,sizeof(int8_t)); memset(s.asg.polarity,1,f->n_vars+1);
    s.watches_pos=(watch_list_t*)calloc(f->n_vars+1,sizeof(watch_list_t)); s.watches_neg=(watch_list_t*)calloc(f->n_vars+1,sizeof(watch_list_t));
    s.var_act=(float*)calloc(f->n_vars+1,sizeof(float)); s.var_decay=0.95f; s.cls_decay=0.999f; s.restart_interval=256; s.dl_stack=(uint32_t*)calloc(1<<12,sizeof(uint32_t)); s.dl_top=0;
    s.trail=NULL; s.trail_sz=0; s.trail_cap=0;
    // Initialize simple watch lists: every literal watches its clauses at positions 0/1
    for(uint32_t ci=0; ci<f->n_clauses; ++ci){ clause_t* c=&f->clauses[ci]; if(c->size==0){ return false; } if(c->size==1){ if(!enqueue_lit(&s, c->lits[0])) return false; }
        for(int wi=0; wi<(c->size<2? (int)c->size:2); ++wi){ lit_t l=c->lits[wi]; var_t v=lit_var(l); watch_list_t* wl = (l>0)? &s.watches_pos[v] : &s.watches_neg[v]; if(wl->size==wl->capacity){ wl->capacity = wl->capacity? wl->capacity*2 : 4; wl->clause_idx=(uint32_t*)realloc(wl->clause_idx,sizeof(uint32_t)*wl->capacity); wl->watch_pos=(uint16_t*)realloc(wl->watch_pos,sizeof(uint16_t)*wl->capacity);} wl->clause_idx[wl->size]=ci; wl->watch_pos[wl->size]=wi; wl->size++; }
    }
    bool sat = cdcl_solve(&s);
    // Cleanup minimal
    for(uint32_t ci=0;ci<f->n_clauses;++ci) free(f->clauses[ci].lits); free(f->clauses); free(f);
    free(s.asg.assign); free(s.asg.polarity); for(var_t v=1; v<=s.f->n_vars; ++v){ (void)v; } free(s.watches_pos); free(s.watches_neg); free(s.var_act); free(s.dl_stack); free(s.trail);
    return sat;
}
