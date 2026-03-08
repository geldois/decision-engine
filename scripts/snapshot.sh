#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/context.sh"
"$SCRIPT_DIR/delta.sh"

echo "snapshot generated"
