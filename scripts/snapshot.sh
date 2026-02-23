#!/usr/bin/env bash
set -euo pipefail

./scripts/build_context.sh
./scripts/build_delta.sh

echo "Snapshot generated: context.txt and delta.txt"
