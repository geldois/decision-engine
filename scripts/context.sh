#!/usr/bin/env bash
set -euo pipefail

mkdir -p scripts/output

MODE="${1:-all}"

if [ "$MODE" = "all-root" ]; then
  FILES=$(git ls-files '*' ':!*/*' || true)
elif [ "$MODE" = "docs" ]; then
  FILES=$(git ls-files 'docs/**')
elif [ "$MODE" = "scripts" ]; then
  FILES=$(git ls-files 'scripts/**')
elif [ "$MODE" = "app" ]; then
  FILES=$(git ls-files 'src/app/**')
elif [ "$MODE" = "app-root" ]; then
  FILES=$(git ls-files 'src/app/**' ':!src/app/*/*' || true)
elif [ "$MODE" = "app-application" ]; then
  FILES=$(git ls-files 'src/app/application/**')
elif [ "$MODE" = "app-bootstrap" ]; then
  FILES=$(git ls-files 'src/app/bootstrap/**')
elif [ "$MODE" = "app-core" ]; then
  FILES=$(git ls-files 'src/app/core/**')
elif [ "$MODE" = "app-domain" ]; then
  FILES=$(git ls-files 'src/app/domain/**')
elif [ "$MODE" = "app-infrastructure" ]; then
  FILES=$(git ls-files 'src/app/infrastructure/**')
elif [ "$MODE" = "app-interfaces" ]; then
  FILES=$(git ls-files 'src/app/interfaces/**')
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
  echo "PROJECT CONTEXT ($MODE)"
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
