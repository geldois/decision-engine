#!/usr/bin/env bash
set -euo pipefail

FAIL=0

print_line() {
  local char="$1"
  printf "%0.s${char}" {1..80}
  printf "\n"
}

print_header() {
  echo "ARCHITECTURE VALIDATION"
  echo "Date: $(date)"
  print_line "="
  echo
}

print_section() {
  echo "$1"
  print_line "-"
}

check_violation() {
  local description="$1"
  local command="$2"

  if eval "$command" >/dev/null 2>&1; then
    echo "FAIL - $description"
    FAIL=1
  else
    echo "OK   - $description"
  fi
}

print_header

print_section "LAYER DEPENDENCY RULES"

check_violation \
  "Domain must not depend on application layer" \
  "grep -R 'from app.application' src/app/domain"

check_violation \
  "Domain must not depend on infrastructure layer" \
  "grep -R 'from app.infrastructure' src/app/domain"

check_violation \
  "Application must not depend on infrastructure layer" \
  "grep -R 'from app.infrastructure' src/app/application"

check_violation \
  "Services must not depend on infrastructure layer" \
  "grep -R 'from app.infrastructure' src/app/services"

echo
print_line "="

if [ "$FAIL" -eq 0 ]; then
  echo "RESULT: ARCHITECTURE CLEAN"
  print_line "="
  exit 0
else
  echo "RESULT: ARCHITECTURE VIOLATIONS DETECTED"
  print_line "="
  exit 1
fi
