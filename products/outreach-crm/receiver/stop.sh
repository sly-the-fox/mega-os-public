#!/usr/bin/env bash
# Stop the outreach capture receiver.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "Receiver is not running (no PID file)"
  exit 0
fi

PID=$(cat "$PID_FILE")

if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  rm -f "$PID_FILE"
  echo "Receiver stopped (PID $PID)"
else
  rm -f "$PID_FILE"
  echo "Receiver was not running (stale PID file removed)"
fi
