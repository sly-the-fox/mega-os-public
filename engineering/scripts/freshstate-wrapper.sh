#!/usr/bin/env bash
# freshstate-wrapper.sh — Run freshstate check and save report. Zero API cost.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT"

REPORT="active/freshstate-report.md"

FRESHSTATE="$(command -v freshstate || echo "$HOME/.local/bin/freshstate")"
"$FRESHSTATE" check > "$REPORT" 2>&1 || true

# Notify if stale files found
if grep -qi "stale\|violation\|error" "$REPORT" 2>/dev/null; then
    "$SCRIPT_DIR/notify-telegram.sh" "Freshstate" 0 "$REPORT"
fi
