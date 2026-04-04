#!/usr/bin/env bash
set -euo pipefail

mkdir -p scripts/output

MODE="${1:-all}"

if [ "$MODE" = "all-root" ]; then
  PATHS=$(git ls-files '*' ':!*/*' || true)
elif [ "$MODE" = "docs" ]; then
  PATHS="docs"
elif [ "$MODE" = "scripts" ]; then
  PATHS="scripts"
elif [ "$MODE" = "app" ]; then
  PATHS="src/app"
elif [ "$MODE" = "app-root" ]; then
  PATHS=$(git ls-files 'src/app/**' ':!src/app/*/*' || true)
elif [ "$MODE" = "app-api" ]; then
  PATHS="src/app/api"
elif [ "$MODE" = "app-application" ]; then
  PATHS="src/app/application"
elif [ "$MODE" = "app-bootstrap" ]; then
  PATHS="src/app/bootstrap"
elif [ "$MODE" = "app-domain" ]; then
  PATHS="src/app/domain"
elif [ "$MODE" = "app-domain-value_objects" ]; then
  PATHS="src/app/domain/value_objects"
elif [ "$MODE" = "app-infrastructure" ]; then
  PATHS="src/app/infrastructure"
elif [ "$MODE" = "tests" ]; then
  PATHS="tests"
else
  PATHS=""
fi

OUTPUT="scripts/output/delta-$MODE.txt"
MAX_SIZE=20000

print_line() {
  local char="$1"
  printf "%*s\n" 80 "" | tr " " "$char"
  printf "\n"
}

{
  echo "PROJECT DELTA ($MODE)"
  echo "Date: $(date)"
  echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
  echo "Last commit: $(git log -1 --pretty=format:'%h - %s')"
  print_line "="

  echo "STATUS"
  print_line "-"
  if [ -z "$PATHS" ]; then
    git status -s
  else
    git status -s -- $PATHS
  fi
  echo

  echo "STAGED DIFF"
  print_line "-"
  git diff --cached --name-only -- $PATHS | while read -r file; do
    [ -f "$file" ] || continue
    echo
    echo "[$file]"
    print_line "."
    git diff --cached --unified=5 -- "$file"
    echo
  done

  echo "WORKING TREE DIFF"
  print_line "-"
  git diff --name-only -- $PATHS | while read -r file; do
    [ -f "$file" ] || continue

    echo
    echo "[$file]"
    print_line "."

    git diff --unified=5 -- "$file"
    echo
  done

  echo "UNTRACKED FILES"
  print_line "-"
  git ls-files --others --exclude-standard | while read -r file; do
    if [ -n "$PATHS" ]; then
      if echo "$PATHS" | grep -qx "$file"; then
        match=true
      else
        match=false
        for path in $PATHS; do
          if [[ "$file" == $path* ]]; then
            match=true
            break
          fi
        done
      fi
      [ "$match" = false ] && continue
    fi

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
