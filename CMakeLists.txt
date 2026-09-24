cmake_minimum_required(VERSION 3.12)
project(QuantumEtherTapestry LANGUAGES CXX)

# ==============================================================================
# 🌐 COMPILER CONFIGURATION & OPTIMIZATION SETTINGS
# ==============================================================================

# Force modern C++17 standards for optimization stability
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Apply hyper-optimized compiler flags across platform binaries
if(MSVC)
    # Windows-specific optimization flags
    target_compile_options(LatticeRoutingEngine PRIVATE /O2 /W4)
else()
    # Linux (g++) and macOS (Clang) production optimization optimization flags (-O3)
    add_compile_options(-O3 -Wall -Wextra -Wpedantic)
endif()

# ==============================================================================
# ⚙️ [E] EMPIRICAL REGISTER / EXECUTABLE TARGETS
# ==============================================================================

# Define the production binary target path rules
add_executable(LatticeRoutingEngine 
    src/lattice_routing.cpp
)

# Ensure the header file directory layout resolves correctly during compilation passes
target_include_directories(LatticeRoutingEngine PRIVATE src)

# Set the output destination directory for the final native executable
set_target_properties(LatticeRoutingEngine PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
