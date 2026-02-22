#!/usr/bin/env bash
set -euo pipefail

OUTPUT="context.txt"

{
  printf "\nPROJECT CONTEXT SNAPSHOT\n"
  printf "Generated at: %s\n" "$(date)"
  printf "%0.s=" {1..80}
  printf "\n\n"

  printf "FILES:\n"
  printf "%0.s-" {1..80}
  printf "\n"

  git ls-files

  printf "\n\nCONTENT:\n"
  printf "%0.s-" {1..80}
  printf "\n"

  git ls-files | while read -r file; do
    [ -f "$file" ] || continue

    if file "$file" | grep -q text; then
      printf "\n[%s]\n" "$file"
      printf "%0.s." {1..80}
      printf "\n"
      cat "$file"
      printf "\n"
    fi
  done

} > "$OUTPUT"