#!/usr/bin/env bash
set -euo pipefail

OUTPUT="context.txt"

print_line() {
  local char="$1"
  printf "%0.s${char}" {1..80}
  printf "\n"
}

{
  echo "PROJECT CONTEXT SNAPSHOT"
  echo "Date: $(date)"
  print_line "="
  echo

  echo "FILES"
  print_line "-"
  git ls-files
  echo

  echo "CONTENT"
  print_line "-"

  git ls-files | while read -r file; do
    [ -f "$file" ] || continue

    if file "$file" | grep -q text; then
      echo
      echo "[$file]"
      print_line "."
      cat "$file"
      echo
    fi
  done

} > "$OUTPUT"
