#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/context.sh" all
"$SCRIPT_DIR/context.sh" all-root
"$SCRIPT_DIR/context.sh" docs
"$SCRIPT_DIR/context.sh" scripts
"$SCRIPT_DIR/context.sh" app
"$SCRIPT_DIR/context.sh" app-root
"$SCRIPT_DIR/context.sh" app-application
"$SCRIPT_DIR/context.sh" app-bootstrap
"$SCRIPT_DIR/context.sh" app-core
"$SCRIPT_DIR/context.sh" app-domain
"$SCRIPT_DIR/context.sh" app-infrastructure
"$SCRIPT_DIR/context.sh" app-interfaces
"$SCRIPT_DIR/context.sh" tests

"$SCRIPT_DIR/delta.sh" all
"$SCRIPT_DIR/delta.sh" all-root
"$SCRIPT_DIR/delta.sh" docs
"$SCRIPT_DIR/delta.sh" scripts
"$SCRIPT_DIR/delta.sh" app
"$SCRIPT_DIR/delta.sh" app-root
"$SCRIPT_DIR/delta.sh" app-application
"$SCRIPT_DIR/delta.sh" app-bootstrap
"$SCRIPT_DIR/delta.sh" app-core
"$SCRIPT_DIR/delta.sh" app-domain
"$SCRIPT_DIR/delta.sh" app-infrastructure
"$SCRIPT_DIR/delta.sh" app-interfaces
"$SCRIPT_DIR/delta.sh" tests

echo "snapshot generated"
