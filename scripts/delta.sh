#!/usr/bin/env bash
set -euo pipefail

OUTPUT="scripts/output/delta.txt"
MAX_SIZE=20000

print_line() {
  local char="$1"
  printf "%*s\n" 80 "" | tr " " "$char"
  printf "\n"
}

{
  echo "PROJECT DELTA"
  echo "Date: $(date)"
  echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
  echo "Last commit: $(git log -1 --pretty=format:'%h - %s')"
  print_line "="

  echo "STATUS"
  print_line "-"
  git status -s
  echo

  echo "FILES CHANGED (SUMMARY)"
  print_line "-"
  echo "Python:   $(git diff --name-only | grep -c '\.py$' || true)"
  echo "Shell:    $(git diff --name-only | grep -c '\.sh$' || true)"
  echo "Markdown: $(git diff --name-only | grep -c '\.md$' || true)"
  echo "Other:    $(git diff --name-only | grep -vE '\.(py|sh|md)$' | wc -l)"
  echo

  echo "STAGED DIFF"
  print_line "-"
  git diff --cached --unified=5
  echo

  echo "WORKING TREE DIFF"
  print_line "-"
  git diff --unified=5
  echo
  
  echo "UNTRACKED FILES"
  print_line "-"
  git ls-files --others --exclude-standard | while read -r file; do
    size=$(wc -c <"$file")
    echo "[$file]"
    print_line "."
    if [ "$size" -lt "$MAX_SIZE" ]; then
      cat "$file"
    else
      echo "[FILE TOO LARGE - CONTENT OMITTED]"
      echo "Size: $size bytes"
    fi
    echo
  done
} >"$OUTPUT"
