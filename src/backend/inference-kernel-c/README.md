YG# Inference Kernel C - Deterministic Math/Logic Engine

A high-performance C library for symbolic algebra, SAT solving, and deterministic logic operations. Designed for local-first AI systems with auditable, deterministic outputs.

## Overview

This library provides:

1. **Symbolic Algebra Engine** (`symbolic_algebra.c`)
   - Expression expansion, factorization, and simplification
   - Deterministic symbolic manipulation
   - Stubs for expand(), factor(), simplify()

2. **SAT Solver** (`sat_solver.c`)
   - DPLL and CDCL algorithms for satisfiability checking
   - CNF formula parsing (DIMACS format)
   - UNSAT proof generation for auditability

3. **Deterministic Logger** (`deterministic_logger.c`)
   - Text and JSON logging formats
   - Reproducible, auditable output
   - Operation tracing with timestamps

## Architecture

The codebase is designed with multiple optimization paths:

- **Native**: Standard C compilation with `-O3 -march=native`
- **SIMD**: AVX2/AVX-512 vectorization for parallel operations
- **WASM/WASI**: Browser/edge deployment with WebAssembly SIMD
- **GPU**: Placeholders for CUDA, OpenCL, and WebGPU acceleration

### Performance Targets

- **Symbolic algebra**: SIMD coefficient array operations
- **SAT solving**: GPU-parallel clause evaluation and search
- **Logging**: Zero-copy JSON serialization

## Building

### Native Build

```bash
mkdir build && cd build
cmake ..
make
```

### With SIMD Optimizations

```bash
cmake -DENABLE_SIMD=ON ..
make
```

### WASM Build (Emscripten)

```bash
# Install Emscripten SDK first: https://emscripten.org/
emcmake cmake -DBUILD_WASM=ON ..
make
```

This generates `inference_kernel_wasm.wasm` and JS glue code for browser/Node.js.

### WASI Build (WASI-SDK)

```bash
# Install WASI SDK: https://github.com/WebAssembly/wasi-sdk
export CC=/path/to/wasi-sdk/bin/clang
cmake -DBUILD_WASM=ON ..
make
```

## Testing

Each module has a standalone test mode:

```bash
# After native build:
./test_symbolic
./test_sat
./test_logger
```

Or compile individually:

```bash
gcc -DSTANDALONE_TEST -o test_symbolic symbolic_algebra.c
./test_symbolic
```

## Integration

### C/C++ Projects

```c
#include "symbolic_algebra.c"
#include "sat_solver.c"
#include "deterministic_logger.c"

// Initialize logger
logger_init(LOG_INFO, LOG_FORMAT_JSON);

// Create and solve SAT problem
cnf_formula_t *formula = parse_cnf_dimacs(dimacs_string);
sat_solution_t *solution = dpll_solve(formula);

if (solution->result == SAT) {
    logger_log(LOG_INFO, "Formula is satisfiable");
}

free_solution(solution);
free_cnf_formula(formula);
```

### JavaScript/TypeScript (WASM)

```javascript
import InferenceKernel from './inference_kernel_wasm.js';

const module = await InferenceKernel();

// Call exported functions
const expandPtr = module.ccall('expand', 'number', ['number'], [exprPtr]);
const resultPtr = module.ccall('cdcl_solve', 'number', ['number'], [formulaPtr]);
```

## Future Enhancements

### GPU Acceleration

1. **CUDA** (NVIDIA)
   - Add `.cu` kernel files
   - Parallel SAT search branches
   - Symbolic matrix operations with cuBLAS

2. **OpenCL** (Cross-platform)
   - Add `.cl` kernel files
   - Works on AMD, Intel, ARM GPUs

3. **WebGPU** (Browser)
   - Compute shaders for in-browser acceleration
   - Experimental Emscripten support

### Advanced Features

- [ ] Multi-threaded DPLL/CDCL with clause learning
- [ ] Groebner basis computation for symbolic algebra
- [ ] SMT solver integration (theory reasoning)
- [ ] Proof verification and certificate generation
- [ ] Incremental SAT solving

## License

See parent project LICENSE.

## Technical Notes

### Deterministic Execution

All operations are designed to be deterministic:
- Fixed iteration order (no hash table randomness)
- Reproducible floating-point ops (use -ffp-contract=off if needed)
- Timestamp logs use UTC (gmtime)

### Memory Management

Manual memory management for performance:
- Arena allocators for SAT clause storage (TODO)
- Stack-based expression trees where possible
- Explicit free functions for all allocations

### WASM Considerations

- Memory growth enabled (`ALLOW_MEMORY_GROWTH=1`)
- Exported functions use C calling convention
- SIMD support via `-msimd128` (requires recent browsers)
- No threading yet (TODO: pthreads support)

