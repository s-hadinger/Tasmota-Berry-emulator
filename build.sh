#!/bin/bash
# build.sh - Simple wrapper script for WASM build

# Compile native
make -C berry-lang clean; make -C berry-lang

# Build WebAssembly
source emsdk/emsdk_env.sh; make -C berry-lang clean BUILD_MODE=emsdk; make -C berry-lang BUILD_MODE=emsdk

echo "Build complete: berry dist/berry.js"
