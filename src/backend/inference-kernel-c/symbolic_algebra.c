// symbolic_algebra.c
// High-performance symbolic algebra core with SIMD optimizations, GPU stubs, and pattern matching

#include <immintrin.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

// Basic expression kinds
typedef enum {
    EXPR_CONST,
    EXPR_VAR,
    EXPR_ADD,
    EXPR_MUL,
    EXPR_POW
} ExprKind;

// Small-string variable names for locality
#define VAR_NAME_MAX 32

typedef struct Expr Expr;

typedef struct {
    double value;
} EConst;

typedef struct {
    char name[VAR_NAME_MAX];
} EVar;

typedef struct {
    Expr** items;
    size_t len;
} EList;

typedef struct {
    Expr* base;
    Expr* exp;
} EPow;

struct Expr {
    ExprKind kind;
    union {
        EConst c;
        EVar v;
        EList list;   // for ADD or MUL n-ary nodes
        EPow powv;
    } as;
};

// Memory helpers
static inline Expr* expr_new(ExprKind k) {
    Expr* e = (Expr*)calloc(1, sizeof(Expr));
    if (!e) abort();
    e->kind = k;
    return e;
}

static inline Expr* expr_const(double v) {
    Expr* e = expr_new(EXPR_CONST);
    e->as.c.value = v;
    return e;
}

static inline Expr* expr_var(const char* n) {
    Expr* e = expr_new(EXPR_VAR);
    strncpy(e->as.v.name, n, VAR_NAME_MAX - 1);
    e->as.v.name[VAR_NAME_MAX-1] = '\0';
    return e;
}

static inline Expr* expr_nary(ExprKind k, size_t n) {
    Expr* e = expr_new(k);
    e->as.list.items = (Expr**)calloc(n, sizeof(Expr*));
    if (!e->as.list.items) abort();
    e->as.list.len = n;
    return e;
}

static inline Expr* expr_pow(Expr* base, Expr* exp) {
    Expr* e = expr_new(EXPR_POW);
    e->as.powv.base = base;
    e->as.powv.exp = exp;
    return e;
}

// SIMD-accelerated numeric vector ops to speed numeric constant folding
// Processes up to 4 doubles at once via AVX2 where available, falling back to scalar otherwise.
static inline void simd_add4(const double* a, const double* b, double* out, size_t n) {
#if defined(__AVX2__)
    size_t i = 0;
    for (; i + 4 <= n; i += 4) {
        __m256d va = _mm256_loadu_pd(a + i);
        __m256d vb = _mm256_loadu_pd(b + i);
        __m256d vc = _mm256_add_pd(va, vb);
        _mm256_storeu_pd(out + i, vc);
    }
    for (; i < n; ++i) out[i] = a[i] + b[i];
#else
    for (size_t i = 0; i < n; ++i) out[i] = a[i] + b[i];
#endif
}

static inline void simd_mul4(const double* a, const double* b, double* out, size_t n) {
#if defined(__AVX2__)
    size_t i = 0;
    for (; i + 4 <= n; i += 4) {
        __m256d va = _mm256_loadu_pd(a + i);
        __m256d vb = _mm256_loadu_pd(b + i);
        __m256d vc = _mm256_mul_pd(va, vb);
        _mm256_storeu_pd(out + i, vc);
    }
    for (; i < n; ++i) out[i] = a[i] * b[i];
#else
    for (size_t i = 0; i < n; ++i) out[i] = a[i] * b[i];
#endif
}

// Flatten and fold n-ary ADD/MUL nodes with SIMD where applicable
static inline void fold_constants_add(double* buf, size_t n, double* out_sum) {
    if (n == 0) { *out_sum = 0.0; return; }
    if (n == 1) { *out_sum = buf[0]; return; }
    // pairwise add using SIMD buffer
    size_t half = n / 2;
    double* tmp = (double*)malloc(sizeof(double) * half);
    for (size_t i = 0; i < half; ++i) tmp[i] = 0.0;
    simd_add4(buf, buf + half, tmp, half);
    double s = 0.0;
    for (size_t i = 0; i < half; ++i) s += tmp[i];
    if (n % 2) s += buf[n - 1];
    free(tmp);
    *out_sum = s;
}

static inline void fold_constants_mul(double* buf, size_t n, double* out_prod) {
    if (n == 0) { *out_prod = 1.0; return; }
    if (n == 1) { *out_prod = buf[0]; return; }
    size_t half = n / 2;
    double* tmp = (double*)malloc(sizeof(double) * half);
    for (size_t i = 0; i < half; ++i) tmp[i] = 1.0;
    simd_mul4(buf, buf + half, tmp, half);
    double p = 1.0;
    for (size_t i = 0; i < half; ++i) p *= tmp[i];
    if (n % 2) p *= buf[n - 1];
    free(tmp);
    *out_prod = p;
}

// Pattern matching engine (simple tree pattern with wildcards)
// Wildcards: "_" matches any node; "?name" captures a node into an environment

typedef struct {
    const char* key;
    const Expr* val;
} Binding;

typedef struct {
    Binding* items;
    size_t len;
    size_t cap;
} Bindings;

static inline void bind_push(Bindings* b, const char* k, const Expr* v) {
    if (b->len == b->cap) {
        b->cap = b->cap ? b->cap * 2 : 8;
        b->items = (Binding*)realloc(b->items, b->cap * sizeof(Binding));
        if (!b->items) abort();
    }
    b->items[b->len].key = k;
    b->items[b->len].val = v;
    b->len++;
}

static bool bind_get(const Bindings* b, const char* k, const Expr** out) {
    for (size_t i = 0; i < b->len; ++i) {
        if (strcmp(b->items[i].key, k) == 0) { *out = b->items[i].val; return true; }
    }
    return false;
}

static bool expr_equal(const Expr* a, const Expr* b);

static bool match_expr(const Expr* pattern, const Expr* term, Bindings* env) {
    if (!pattern || !term) return false;
    if (pattern->kind == EXPR_VAR) {
        const char* n = pattern->as.v.name;
        if (strcmp(n, "_") == 0) return true; // wildcard
        if (n[0] == '?' ) { // capture
            const Expr* existing = NULL;
            if (bind_get(env, n+1, &existing)) {
                return expr_equal(existing, term);
            }
            bind_push(env, n+1, term);
            return true;
        }
    }
    if (pattern->kind != term->kind) return false;
    switch (pattern->kind) {
        case EXPR_CONST:
            return pattern->as.c.value == term->as.c.value;
        case EXPR_VAR:
            return strcmp(pattern->as.v.name, term->as.v.name) == 0;
        case EXPR_POW:
            return match_expr(pattern->as.powv.base, term->as.powv.base, env) &&
                   match_expr(pattern->as.powv.exp, term->as.powv.exp, env);
        case EXPR_ADD:
        case EXPR_MUL: {
            if (pattern->as.list.len != term->as.list.len) return false;
            for (size_t i = 0; i < pattern->as.list.len; ++i) {
                if (!match_expr(pattern->as.list.items[i], term->as.list.items[i], env)) return false;
            }
            return true;
        }
    }
    return false;
}

static bool expr_equal(const Expr* a, const Expr* b) {
    if (a == b) return true;
    if (!a || !b) return false;
    if (a->kind != b->kind) return false;
    switch (a->kind) {
        case EXPR_CONST: return a->as.c.value == b->as.c.value;
        case EXPR_VAR:   return strcmp(a->as.v.name, b->as.v.name) == 0;
        case EXPR_POW:   return expr_equal(a->as.powv.base, b->as.powv.base) && expr_equal(a->as.powv.exp, b->as.powv.exp);
        case EXPR_ADD:
        case EXPR_MUL:
            if (a->as.list.len != b->as.list.len) return false;
            for (size_t i = 0; i < a->as.list.len; ++i) if (!expr_equal(a->as.list.items[i], b->as.list.items[i])) return false;
            return true;
    }
    return false;
}

// Simplification using constant folding with SIMD-accelerated helpers for bulk constants
static Expr* simplify(Expr* e) {
    if (!e) return NULL;
    switch (e->kind) {
        case EXPR_CONST:
        case EXPR_VAR:
            return e;
        case EXPR_POW:
            e->as.powv.base = simplify(e->as.powv.base);
            e->as.powv.exp  = simplify(e->as.powv.exp);
            return e;
        case EXPR_ADD:
        case EXPR_MUL: {
            for (size_t i = 0; i < e->as.list.len; ++i) e->as.list.items[i] = simplify(e->as.list.items[i]);
            double* buf = (double*)malloc(sizeof(double) * e->as.list.len);
            size_t cnt = 0; size_t nonc = 0;
            for (size_t i = 0; i < e->as.list.len; ++i) {
                if (e->as.list.items[i]->kind == EXPR_CONST) {
                    buf[cnt++] = e->as.list.items[i]->as.c.value;
                } else {
                    e->as.list.items[nonc++] = e->as.list.items[i];
                }
            }
            if (cnt > 0) {
                double out = 0.0;
                if (e->kind == EXPR_ADD) {
                    fold_constants_add(buf, cnt, &out);
                    if (nonc == 0) { e->kind = EXPR_CONST; e->as.c.value = out; free(buf); return e; }
                    Expr* c = expr_const(out);
                    e->as.list.items[nonc++] = c;
                } else {
                    out = 1.0;
                    fold_constants_mul(buf, cnt, &out);
                    if (nonc == 0) { e->kind = EXPR_CONST; e->as.c.value = out; free(buf); return e; }
                    Expr* c = expr_const(out);
                    e->as.list.items[nonc++] = c;
                }
            }
            free(buf);
            e->as.list.len = nonc;
            return e;
        }
    }
    return e;
}

// GPU acceleration stubs (optional backend hooks). These compile even without CUDA/OpenCL.
typedef int (*gpu_add_vec_fn)(const double* a, const double* b, double* out, size_t n);
typedef int (*gpu_mul_vec_fn)(const double* a, const double* b, double* out, size_t n);

static gpu_add_vec_fn GPU_ADD_VEC = NULL;
static gpu_mul_vec_fn GPU_MUL_VEC = NULL;

int register_gpu_add(gpu_add_vec_fn fn) { GPU_ADD_VEC = fn; return 0; }
int register_gpu_mul(gpu_mul_vec_fn fn) { GPU_MUL_VEC = fn; return 0; }

int gpu_add_vec(const double* a, const double* b, double* out, size_t n) {
    if (GPU_ADD_VEC) return GPU_ADD_VEC(a, b, out, n);
    simd_add4(a, b, out, n);
    return 0;
}

int gpu_mul_vec(const double* a, const double* b, double* out, size_t n) {
    if (GPU_MUL_VEC) return GPU_MUL_VEC(a, b, out, n);
    simd_mul4(a, b, out, n);
    return 0;
}

// Public API
Expr* sa_const(double v) { return expr_const(v); }
Expr* sa_var(const char* n) { return expr_var(n); }
Expr* sa_addn(size_t n) { return expr_nary(EXPR_ADD, n); }
Expr* sa_muln(size_t n) { return expr_nary(EXPR_MUL, n); }
Expr* sa_pow(Expr* base, Expr* exp) { return expr_pow(base, exp); }
Expr* sa_simplify(Expr* e) { return simplify(e); }

// Pattern compile helpers
Expr* sa_pat_any(void) { return expr_var("_"); }
Expr* sa_pat_capture(const char* name) {
    char buf[VAR_NAME_MAX];
    buf[0] = '?';
    strncpy(buf+1, name, VAR_NAME_MAX-2);
    buf[VAR_NAME_MAX-1] = '\0';
    return expr_var(buf);
}

bool sa_match(const Expr* pattern, const Expr* term, Bindings* env) { env->len = 0; return match_expr(pattern, term, env); }

void sa_print(const Expr* e) {
    if (!e) { printf("<null>"); return; }
    switch (e->kind) {
        case EXPR_CONST: printf("%g", e->as.c.value); break;
        case EXPR_VAR:   printf("%s", e->as.v.name); break;
        case EXPR_ADD:   printf("("); for (size_t i=0;i<e->as.list.len;i++){ if(i) printf(" + "); sa_print(e->as.list.items[i]); } printf(")"); break;
        case EXPR_MUL:   printf("("); for (size_t i=0;i<e->as.list.len;i++){ if(i) printf(" * "); sa_print(e->as.list.items[i]); } printf(")"); break;
        case EXPR_POW:   sa_print(e->as.powv.base); printf("^"); sa_print(e->as.powv.exp); break;
    }
}

#ifdef __cplusplus
}
#endif
