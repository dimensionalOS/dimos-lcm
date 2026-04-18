#!/usr/bin/env bash
# Builds the C++ echo binary against the LCM runtime found via pkg-config
# and the generated headers in ../../../generated/cpp_lcm_msgs.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../.." && pwd)"
BUILD_DIR="$HERE/build"
mkdir -p "$BUILD_DIR"

LCM_FLAGS="$(pkg-config --cflags --libs lcm)"

CXX="${CXX:-c++}"
CXX_STD="-std=c++17"
OPT_FLAGS="${BENCH_CXX_FLAGS:--O3 -DNDEBUG}"
INCLUDES=(
    "-I$REPO_ROOT/generated/cpp_lcm_msgs"
)

set -x
$CXX $CXX_STD $OPT_FLAGS "${INCLUDES[@]}" \
    "$HERE/echo.cpp" -o "$BUILD_DIR/echo" \
    $LCM_FLAGS
{ set +x; } 2>/dev/null
echo "built $BUILD_DIR/echo"
