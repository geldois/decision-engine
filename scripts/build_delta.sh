#!/usr/bin/env bash
set -euo pipefail

OUTPUT="delta.txt"

{
  printf "PROJECT DELTA\n"
  printf "Date: %s\n" "$(date)"
  printf "Branch: %s\n" "$(git rev-parse --abbrev-ref HEAD)"
  printf "Last commit: %s\n" "$(git log -1 --pretty=format:'%h - %s')"
  printf "%0.s=" {1..80}
  printf "\n\n"

  printf "STATUS:\n"
  printf "%0.s-" {1..80}
  printf "\n"
  git status -s

  printf "\n\nDIFF:\n"
  printf "%0.s-" {1..80}
  printf "\n"
  git diff

} > "$OUTPUT"
