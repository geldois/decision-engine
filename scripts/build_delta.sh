#!/usr/bin/env bash
set -euo pipefail

OUTPUT="delta.txt"

print_line() {
  local char="$1"
  printf "%0.s${char}" {1..80}
  printf "\n"
}

{
  echo "PROJECT DELTA"
  echo "Date: $(date)"
  echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
  echo "Last commit: $(git log -1 --pretty=format:'%h - %s')"
  print_line "="
  echo

  echo "STATUS"
  print_line "-"
  git status -s
  echo

  echo "DIFF"
  print_line "-"
  git diff
  echo

} > "$OUTPUT"
