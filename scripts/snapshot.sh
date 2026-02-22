#!/usr/bin/env bash
set -euo pipefail

./scripts/build_context.sh
./scripts/build_delta.sh

printf "Snapshots updated: context.txt and delta.txt\n"
