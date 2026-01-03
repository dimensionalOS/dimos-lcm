#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

LCM_TYPES_DIR="$ROOT_DIR/lcm_types"
PYTHON_OUT_DIR="$SCRIPT_DIR/python_lcm_msgs/lcm_msgs"

rm -rf "$PYTHON_OUT_DIR"
"$ROOT_DIR/sources/lcm_to_generated.sh" -p "$LCM_TYPES_DIR" -o "$PYTHON_OUT_DIR"
python3 "$SCRIPT_DIR/python_lcm_msgs/fix_imports.py"  >/dev/null
git checkout "$PYTHON_OUT_DIR/__init__.py" 2>/dev/null || true
echo "Regenerated python lcm messages"
ruff format $PYTHON_OUT_DIR
