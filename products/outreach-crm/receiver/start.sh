#!/usr/bin/env bash
# Start the outreach capture receiver in the background.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/.pid"
RECEIVER="$SCRIPT_DIR/receiver.py"

if ! command -v python3 &>/dev/null; then
  echo "Error: python3 not found" >&2
  exit 1
fi

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Receiver already running (PID $(cat "$PID_FILE"))"
  exit 0
fi

# Ensure captures directory exists
CAPTURES_DIR="${OUTREACH_CAPTURES_DIR:-$(cd "$SCRIPT_DIR/../../.." && pwd)/business/network/captures}"
mkdir -p "$CAPTURES_DIR" "$CAPTURES_DIR/processed"

export OUTREACH_CAPTURES_DIR="$CAPTURES_DIR"

nohup python3 "$RECEIVER" > "$SCRIPT_DIR/receiver.log" 2>&1 &
echo $! > "$PID_FILE"

echo "Receiver started (PID $(cat "$PID_FILE"))"
echo "  Port: ${OUTREACH_PORT:-7799}"
echo "  Captures: $CAPTURES_DIR"
echo "  Log: $SCRIPT_DIR/receiver.log"
