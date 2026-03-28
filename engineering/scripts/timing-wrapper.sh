#!/usr/bin/env bash
# timing-wrapper.sh — Time any command and emit a timing trace.
# Usage: timing-wrapper.sh <skill-name> <source> <command...>
# Example: timing-wrapper.sh improvement-audit cron timeout 900 claude -p "/improvement-audit"
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: timing-wrapper.sh <skill-name> <source> <command...>" >&2
  exit 1
fi

SKILL="$1"; shift
SOURCE="$1"; shift

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TRACE_DIR="$REPO_ROOT/core/history/traces"
TIMING_FILE="$TRACE_DIR/timing.jsonl"
mkdir -p "$TRACE_DIR"

START_EPOCH=$(date +%s%N)
START_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

set +e
"$@"
CMD_EXIT=$?
set -e

END_EPOCH=$(date +%s%N)
DURATION_NS=$(( END_EPOCH - START_EPOCH ))
DURATION_S=$(awk "BEGIN {printf \"%.3f\", $DURATION_NS / 1000000000}")

if [[ -r /proc/sys/kernel/random/uuid ]]; then
  TID=$(cat /proc/sys/kernel/random/uuid)
elif command -v uuidgen &>/dev/null; then
  TID=$(uuidgen)
else
  TID="no-uuid"
fi

JSON=$(printf '{"ts":"%s","timing_id":"%s","skill":"%s","duration_s":%s,"exit_code":%d,"source":"%s"}\n' \
  "$START_ISO" "$TID" "$SKILL" "$DURATION_S" "$CMD_EXIT" "$SOURCE")

(
  flock 200
  printf '%s' "$JSON" >> "$TIMING_FILE"
) 200>"$TIMING_FILE.lock"
rm -f "$TIMING_FILE.lock"

exit "$CMD_EXIT"
