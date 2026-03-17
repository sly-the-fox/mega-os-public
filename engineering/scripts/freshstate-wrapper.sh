#!/usr/bin/env bash
# freshstate-wrapper.sh — Run freshstate check and save report. Zero API cost.
set -euo pipefail

cd /home/abzu/mega-os
REPORT="active/freshstate-report.md"

/home/abzu/.local/bin/freshstate check > "$REPORT" 2>&1 || true

# Notify if stale files found
if grep -qi "stale\|violation\|error" "$REPORT" 2>/dev/null; then
    /home/abzu/mega-os/engineering/scripts/notify-telegram.sh "Freshstate" 0 "$REPORT"
fi
