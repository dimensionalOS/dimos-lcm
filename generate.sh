#!/usr/bin/env bash
set -euo pipefail


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/sources/ros_to_lcm.py"

echo -e "\033[32mRos -> LCM done\033[0m"

# Generate Python bindings
"$SCRIPT_DIR/generated/generate_python.sh"
echo -e "\033[32mLCM -> Python done\033[0m"

# Generate C++ bindings
rm -rf "$SCRIPT_DIR/generated/cpp_lcm_msgs"
"$SCRIPT_DIR/lcm_batch_processor.sh" -cpp "$SCRIPT_DIR/lcm_types" -o "$SCRIPT_DIR/generated/cpp_lcm_msgs"
echo -e "\033[32mLCM -> C++ done\033[0m"

# Generate C# bindings
rm -rf "$SCRIPT_DIR/generated/cs_lcm_msgs"
"$SCRIPT_DIR/lcm_batch_processor.sh" -cs "$SCRIPT_DIR/lcm_types" -o "$SCRIPT_DIR/generated/cs_lcm_msgs"
echo -e "\033[32mLCM -> C# done\033[0m"

# Generate Java bindings
rm -rf "$SCRIPT_DIR/generated/java_lcm_msgs"
"$SCRIPT_DIR/lcm_batch_processor.sh" -j "$SCRIPT_DIR/lcm_types" -o "$SCRIPT_DIR/generated/java_lcm_msgs"
echo -e "\033[32mLCM -> Java done\033[0m"
