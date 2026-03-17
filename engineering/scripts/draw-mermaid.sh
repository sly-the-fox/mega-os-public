#!/usr/bin/env bash
# draw-mermaid.sh — Thin wrapper around mmdc (Mermaid CLI)
# Usage: draw-mermaid.sh <input.mmd> <output.svg|png|pdf>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUPPETEER_CONFIG="${SCRIPT_DIR}/puppeteer-config.json"

if ! command -v mmdc &>/dev/null; then
  echo "Error: mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli" >&2
  exit 1
fi

if [[ $# -lt 2 ]]; then
  echo "Usage: draw-mermaid.sh <input.mmd> <output.[svg|png|pdf]>" >&2
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [[ ! -f "$INPUT" ]]; then
  echo "Error: Input file not found: $INPUT" >&2
  exit 1
fi

mmdc -i "$INPUT" -o "$OUTPUT" -t dark --backgroundColor transparent -p "$PUPPETEER_CONFIG"
echo "Rendered: $OUTPUT"
