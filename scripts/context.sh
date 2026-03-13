#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-all}"

if [ "$MODE" = "core" ]; then
  FILES=$(git ls-files ':!tests')
elif [ "$MODE" = "tests" ]; then
  FILES=$(git ls-files 'tests/**')
else
  FILES=$(git ls-files)
fi

OUTPUT="scripts/output/context-$MODE.txt"
MAX_SIZE=20000

print_line() {
  local char="$1"
  printf "%*s\n" 80 "" | tr " " "$char"
  printf "\n"
}

{
  echo "PROJECT CONTEXT"
  echo "Date: $(date)"
  print_line "="

  echo "PROJECT TREE"
  print_line "-"
  echo "$FILES"
  echo

  echo "FILE CONTENT"
  print_line "-"
  echo "$FILES" | while read -r file; do
    [ -f "$file" ] || continue
    if ! file "$file" | grep -q text; then
      continue
    fi
    size=$(wc -c <"$file")
    echo
    echo "[$file]"
    print_line "."

    if [ "$size" -lt "$MAX_SIZE" ]; then
      cat "$file"
    else
      echo "[FILE TOO LARGE - SHOWING STRUCTURE]"

      if [[ "$file" == *.py ]]; then
        grep -E "^(class |def )" "$file" || true
      else
        head -n 40 "$file"
        echo "... (truncated)"
      fi
    fi
    echo
  done
} >"$OUTPUT"
