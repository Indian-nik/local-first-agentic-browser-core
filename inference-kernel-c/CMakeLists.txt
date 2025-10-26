cmake_minimum_required(VERSION 3.15)
project(InferenceKernel C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Compiler warnings and optimization flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -pedantic")
set(CMAKE_C_FLAGS_DEBUG "-g -O0")
set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")

# Source files
set(KERNEL_SOURCES
    deterministic_logger.c
    sat_solver.c
    symbolic_algebra.c
)

# Create main library
add_library(inference_kernel STATIC ${KERNEL_SOURCES})

# Include directories
target_include_directories(inference_kernel PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Link against math library
target_link_libraries(inference_kernel PRIVATE m)

#############################################################################
# GPU/ACCELERATOR SUPPORT SECTION
# 
# This section contains infrastructure for GPU and hardware accelerator
# support using CUDA and OpenCL. Uncomment and configure as needed.
#############################################################################

# Option to enable GPU support
option(ENABLE_GPU_SUPPORT "Enable GPU acceleration support" OFF)
option(ENABLE_CUDA "Enable CUDA support" OFF)
option(ENABLE_OPENCL "Enable OpenCL support" OFF)

if(ENABLE_GPU_SUPPORT)
    message(STATUS "GPU support enabled")
    
    # CUDA Support
    if(ENABLE_CUDA)
        find_package(CUDAToolkit)
        if(CUDAToolkit_FOUND)
            message(STATUS "CUDA found: ${CUDAToolkit_VERSION}")
            
            # Add CUDA kernel source files
            # set(CUDA_KERNEL_SOURCES
            #     kernels/inference_cuda_kernels.cu
            #     kernels/matrix_ops_cuda.cu
            # )
            
            # Enable CUDA language support
            enable_language(CUDA)
            
            # Set CUDA architecture(s)
            set(CMAKE_CUDA_ARCHITECTURES "75;80;86" CACHE STRING "CUDA architectures")
            
            # Create CUDA kernel library
            # add_library(inference_cuda_kernels ${CUDA_KERNEL_SOURCES})
            # target_include_directories(inference_cuda_kernels PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
            # target_link_libraries(inference_cuda_kernels PUBLIC CUDA::cudart CUDA::cublas)
            
            # Link main library with CUDA kernels
            # target_link_libraries(inference_kernel PUBLIC inference_cuda_kernels)
            target_compile_definitions(inference_kernel PUBLIC ENABLE_CUDA)
            
        else()
            message(WARNING "CUDA requested but not found")
        endif()
    endif()
    
    # OpenCL Support
    if(ENABLE_OPENCL)
        find_package(OpenCL)
        if(OpenCL_FOUND)
            message(STATUS "OpenCL found: ${OpenCL_VERSION_STRING}")
            
            # Add OpenCL kernel source files
            # set(OPENCL_KERNEL_SOURCES
            #     kernels/inference_opencl_kernels.c
            #     kernels/matrix_ops_opencl.c
            # )
            
            # Add kernel files as resources or compile them
            # file(GLOB OPENCL_KERNEL_FILES "${CMAKE_CURRENT_SOURCE_DIR}/kernels/*.cl")
            
            # Create OpenCL kernel library
            # add_library(inference_opencl_kernels ${OPENCL_KERNEL_SOURCES})
            # target_include_directories(inference_opencl_kernels PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
            # target_link_libraries(inference_opencl_kernels PUBLIC OpenCL::OpenCL)
            
            # Link main library with OpenCL kernels
            # target_link_libraries(inference_kernel PUBLIC inference_opencl_kernels)
            target_compile_definitions(inference_kernel PUBLIC ENABLE_OPENCL)
            
        else()
            message(WARNING "OpenCL requested but not found")
        endif()
    endif()
    
    # Additional GPU runtime libraries
    # Uncomment and add other accelerator runtime libraries as needed:
    # - ROCm/HIP for AMD GPUs
    # - SYCL for Intel GPUs
    # - Metal for Apple Silicon
    
    # Example ROCm/HIP support:
    # if(ENABLE_ROCM)
    #     find_package(hip)
    #     if(hip_FOUND)
    #         target_link_libraries(inference_kernel PUBLIC hip::host)
    #         target_compile_definitions(inference_kernel PUBLIC ENABLE_ROCM)
    #     endif()
    # endif()
    
endif()

# Installation rules
install(TARGETS inference_kernel
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
    DESTINATION include/inference_kernel
    FILES_MATCHING PATTERN "*.h"
)

# Testing support
option(BUILD_TESTS "Build unit tests" OFF)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Print configuration summary
message(STATUS "=== Inference Kernel Configuration ===")
message(STATUS "C Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "GPU Support: ${ENABLE_GPU_SUPPORT}")
if(ENABLE_GPU_SUPPORT)
    message(STATUS "  CUDA: ${ENABLE_CUDA}")
    message(STATUS "  OpenCL: ${ENABLE_OPENCL}")
endif()
message(STATUS "======================================")