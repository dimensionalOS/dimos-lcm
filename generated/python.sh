#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

LCM_TYPES_DIR="$ROOT_DIR/lcm_types"
PYTHON_OUT_DIR="$SCRIPT_DIR/python_lcm_msgs/lcm_msgs"

rm -rf "$PYTHON_OUT_DIR"
"$ROOT_DIR/lcm_batch_processor.sh" -v -p "$LCM_TYPES_DIR" -o "$PYTHON_OUT_DIR" > /dev/null 2>&1
python3 "$SCRIPT_DIR/python_lcm_msgs/fix_imports.py" > /dev/null 2>&1
git checkout "$PYTHON_OUT_DIR/__init__.py" > /dev/null 2>&1 || true
echo "Regenerated python lcm messages"
ruff format $PYTHON_OUT_DIR
