#!/usr/bin/env bash
set -euo pipefail


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SCRIPT_DIR/generated"

python3 "$SCRIPT_DIR/sources/ros_to_lcm.py"

echo -e "\033[32mRos -> LCM done\033[0m"

# Generate Python bindings
"$SCRIPT_DIR/tools/generate_python.sh"
echo -e "\033[32mLCM -> Python done\033[0m"

# Generate C++ bindings
rm -rf "$SCRIPT_DIR/generated/cpp_lcm_msgs"
"$SCRIPT_DIR/sources/lcm_to_generated.sh" -cpp "$SCRIPT_DIR/lcm_types" -o "$SCRIPT_DIR/generated/cpp_lcm_msgs"
echo -e "\033[32mLCM -> C++ done\033[0m"

# Generate C# bindings
rm -rf "$SCRIPT_DIR/generated/cs_lcm_msgs"
"$SCRIPT_DIR/sources/lcm_to_generated.sh" -cs "$SCRIPT_DIR/lcm_types" -o "$SCRIPT_DIR/generated/cs_lcm_msgs"
echo -e "\033[32mLCM -> C# done\033[0m"

# Generate Java bindings
rm -rf "$SCRIPT_DIR/generated/java_lcm_msgs"
"$SCRIPT_DIR/sources/lcm_to_generated.sh" -j "$SCRIPT_DIR/lcm_types" -o "$SCRIPT_DIR/generated/java_lcm_msgs"
echo -e "\033[32mLCM -> Java done\033[0m"

# Generate TypeScript bindings
rm -rf "$SCRIPT_DIR/generated/ts_lcm_msgs"
deno run --allow-read --allow-write "$SCRIPT_DIR/tools/ts/gen/mod.ts" -q -o "$SCRIPT_DIR/generated/ts_lcm_msgs" "$SCRIPT_DIR/lcm_types"/*.lcm
# Copy to msgs package (for JSR publishing - symlinks not supported)
rm -rf "$SCRIPT_DIR/tools/ts/msgs/generated"
cp -r "$SCRIPT_DIR/generated/ts_lcm_msgs" "$SCRIPT_DIR/tools/ts/msgs/generated"
echo -e "\033[32mLCM -> TypeScript done\033[0m"
