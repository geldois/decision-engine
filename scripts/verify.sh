#!/usr/bin/env bash
set -euo pipefail

print_line() {
  local char="$1"
  printf "%0.s${char}" {1..80}
  printf "\n"
}

echo "PROJECT VERIFICATION"
echo "Date: $(date)"
print_line "="
echo

echo "Running tests"
print_line "-"
pytest
echo

echo "Running architecture checks"
print_line "-"
./scripts/check_architecture.sh
echo

echo "Verification completed successfully."
