#!/usr/bin/env bash
# Archive an active report file before it gets overwritten.
# Usage: archive-report.sh <report-type> <active-file-path>
# Example: archive-report.sh improvement-audit active/improvement-audit.md
#
# Reads the Generated: timestamp from the file, copies it to
# archive/reports/YYYY-WNN/YYYY-MM-DD-<report-type>.md, and
# updates archive/index.json.

set -euo pipefail

REPORT_TYPE="${1:?Usage: archive-report.sh <report-type> <active-file-path>}"
ACTIVE_FILE="${2:?Usage: archive-report.sh <report-type> <active-file-path>}"

# Resolve paths relative to repo root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ACTIVE_PATH="$ROOT/$ACTIVE_FILE"
ARCHIVE_INDEX="$ROOT/archive/index.json"

# --- Guard: file must exist and have content ---
if [[ ! -s "$ACTIVE_PATH" ]]; then
  exit 0  # Skip silently
fi

# --- Extract Generated: date ---
# Handles formats like "Generated: 2026-03-15 09:10" or "**Generated:** 2026-03-15T15:30:00Z"
GENERATED_LINE=$(grep -m1 -oP '(?:Generated:?\s*\**\s*)(\d{4}-\d{2}-\d{2})' "$ACTIVE_PATH" || true)
FILE_DATE=$(echo "$GENERATED_LINE" | grep -oP '\d{4}-\d{2}-\d{2}' || true)

if [[ -z "$FILE_DATE" ]]; then
  # Fallback: use file modification date
  FILE_DATE=$(date -r "$ACTIVE_PATH" +%Y-%m-%d)
fi

# --- Compute ISO week ---
ISO_WEEK=$(date -d "$FILE_DATE" +%G-W%V)

# --- Build archive path ---
ARCHIVE_DIR="$ROOT/archive/reports/$ISO_WEEK"
mkdir -p "$ARCHIVE_DIR"

ARCHIVE_FILE="$ARCHIVE_DIR/${FILE_DATE}-${REPORT_TYPE}.md"

# Handle collision: same report type, same day
if [[ -f "$ARCHIVE_FILE" ]]; then
  N=2
  while [[ -f "$ARCHIVE_DIR/${FILE_DATE}-${REPORT_TYPE}-${N}.md" ]]; do
    ((N++))
  done
  ARCHIVE_FILE="$ARCHIVE_DIR/${FILE_DATE}-${REPORT_TYPE}-${N}.md"
fi

# --- Copy the file ---
cp "$ACTIVE_PATH" "$ARCHIVE_FILE"

RELATIVE_PATH="archive/reports/$ISO_WEEK/$(basename "$ARCHIVE_FILE")"
echo "Archived previous $REPORT_TYPE ($FILE_DATE) to $RELATIVE_PATH"

# --- Update archive/index.json ---
if command -v python3 &>/dev/null; then
  python3 - "$ARCHIVE_INDEX" "$REPORT_TYPE" "$FILE_DATE" "$ISO_WEEK" "$RELATIVE_PATH" "$(basename "$ARCHIVE_FILE")" "$ACTIVE_PATH" <<'PYEOF'
import json, sys, os
from datetime import date, datetime, timezone

index_path, report_type, file_date, iso_week, rel_path, filename, active_path = sys.argv[1:]

# Load or init index
if os.path.exists(index_path):
    with open(index_path) as f:
        index = json.load(f)
else:
    index = {"version": 1, "generated": "", "content_types": [], "weeks": {}}

# Ensure content type is registered
if report_type not in index.get("content_types", []):
    index.setdefault("content_types", []).append(report_type)

# Compute week date range
d = date.fromisoformat(file_date)
iso = d.isocalendar()
monday = date.fromisocalendar(iso.year, iso.week, 1)
sunday = date.fromisocalendar(iso.year, iso.week, 7)

if iso_week not in index["weeks"]:
    index["weeks"][iso_week] = {
        "date_range": [monday.isoformat(), sunday.isoformat()],
        "files": []
    }

# Estimate tokens
try:
    with open(active_path) as f:
        text = f.read()
    token_est = int(len(text.split()) / 0.75)
    # Extract first meaningful line as summary (skip frontmatter/headers)
    summary = ""
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("---") and not stripped.startswith("Generated") and not stripped.startswith("**Generated"):
            summary = stripped[:120]
            break
except Exception:
    token_est = 0
    summary = ""

# Avoid duplicates
existing = [f["filename"] for f in index["weeks"][iso_week]["files"]]
if filename not in existing:
    index["weeks"][iso_week]["files"].append({
        "filename": filename,
        "path": rel_path,
        "date": file_date,
        "content_type": report_type,
        "summary": summary,
        "token_estimate": token_est
    })

index["generated"] = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

tmp = index_path + ".tmp"
with open(tmp, "w") as f:
    json.dump(index, f, indent=2)
    f.write("\n")
os.rename(tmp, index_path)
PYEOF
fi
