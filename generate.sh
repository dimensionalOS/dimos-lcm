#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directories
ROS_MSGS_DIR="$SCRIPT_DIR/sources/ros_msgs"
LCM_TYPES_DIR="$SCRIPT_DIR/lcm_types"

# Generate LCM types from ROS messages
echo "Generating LCM types from ROS messages..."
python3 "$SCRIPT_DIR/sources/ros_to_lcm.py" "$ROS_MSGS_DIR" "$LCM_TYPES_DIR"
echo "Done: $LCM_TYPES_DIR"
