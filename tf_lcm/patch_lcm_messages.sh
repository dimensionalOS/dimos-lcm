#!/bin/bash
# Script to patch LCM message files to fix function pointer conversion issues
# This will work on both macOS and Linux systems

# Don't exit on error to handle issues gracefully
set +e

# Use environment variable or relative path
if [ -z "$CPP_MSGS_DIR" ]; then
    # Default to relative path from tf_lcm directory
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    CPP_MSGS_DIR="$SCRIPT_DIR/../cpp_lcm_msgs"
fi

echo "Scanning for LCM message files with potential function pointer conversion issues..."

# Find all .hpp files in the cpp_lcm_msgs directory
CPP_FILES=$(find "$CPP_MSGS_DIR" -type f -name "*.hpp")

# Counter for the number of files patched
FILES_PATCHED=0
FILES_WITH_PATTERN=0

for file in $CPP_FILES; do
  # Check if the file contains the _computeHash function
  if grep -q "_computeHash" "$file"; then
    # Further check if it has the problematic pattern without explicit cast
    if grep -q "const __lcm_hash_ptr cp = { p," "$file" && ! grep -q "const __lcm_hash_ptr cp = { p, (void\*)" "$file"; then
      ((FILES_WITH_PATTERN++))
      echo "Processing $file"
      
      # Make a backup of the original file
      cp "$file" "${file}.bak"
      
      # Use sed to replace the problematic line with a properly casted version
      # For Linux compatibility: Add explicit (void*) cast to getHash function pointer
      # Pattern matches: (int64_t(*)())ClassName::getHash and replaces with (void*)(int64_t(*)())ClassName::getHash
      sed -i 's/(int64_t(\*)())\([A-Za-z_:]*\)::getHash/(void*)(int64_t(*)())\1::getHash/g' "$file"
      
      # Check if the file was actually changed
      if ! cmp -s "$file" "${file}.bak"; then
        ((FILES_PATCHED++))
        echo "✅ Patched: $file"
      else
        echo "⚠️ No changes made to: $file"
        # Restore the original file if no changes were made
        mv "${file}.bak" "$file"
      fi
    fi
  fi
done

# Remove any remaining backup files
find "$CPP_MSGS_DIR" -name "*.hpp.bak" -delete 2>/dev/null

echo ""
# Output a summary
echo "Patching summary:"
echo "- Found $FILES_WITH_PATTERN files with potential issues"
echo "- Successfully patched $FILES_PATCHED files"
echo ""

if [ $FILES_PATCHED -gt 0 ]; then
  echo "✅ Patching complete! The files have been modified with proper function pointer casts."
  echo "   These changes are compatible with both macOS and Linux."
else
  echo "ℹ️ No files were modified. Either they were already patched or no issues were found."
fi
