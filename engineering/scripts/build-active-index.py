#!/usr/bin/env python3
"""Build active/index.json from active/*.md file metadata."""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ACTIVE_DIR = Path(__file__).resolve().parent.parent.parent / "active"

# Hardcoded topic + priority mappings (these files are stable)
FILE_META = {
    "now.md": {
        "topics": ["focus", "tasks", "milestones"],
        "load_priority": "always",
    },
    "priorities.md": {
        "topics": ["priorities", "ranking", "urgency"],
        "load_priority": "always",
    },
    "blockers.md": {
        "topics": ["blockers", "obstacles", "stalled"],
        "load_priority": "always",
    },
    "risks.md": {
        "topics": ["risks", "threats", "mitigation"],
        "load_priority": "always",
    },
    "improvements.md": {
        "topics": ["improvements", "proposals", "evolution"],
        "load_priority": "always",
    },
    "daily-digest.md": {
        "topics": ["digest", "scan", "action-items"],
        "load_priority": "on_request",
    },
    "coherence-metrics.md": {
        "topics": ["coherence", "field-readings", "checkpoints"],
        "load_priority": "on_request",
    },
    "audits.md": {
        "topics": ["audits", "findings", "remediation"],
        "load_priority": "on_request",
    },
    "inbox.md": {
        "topics": ["inbox", "incoming", "unrouted"],
        "load_priority": "on_request",
    },
    "news-briefing.md": {
        "topics": ["news", "intelligence", "briefing"],
        "load_priority": "on_demand",
    },
    "news-briefing-state.md": {
        "topics": ["dedup", "news-state", "seen-urls"],
        "load_priority": "on_demand",
    },
    "freshstate-report.md": {
        "topics": ["freshness", "staleness", "document-health"],
        "load_priority": "on_demand",
    },
    "improvement-audit.md": {
        "topics": ["audit", "improvement-audit", "mece-scan"],
        "load_priority": "on_demand",
    },
    "freshness-log.md": {
        "topics": ["freshness-log", "custodian", "workflow-freshness"],
        "load_priority": "on_demand",
    },
    "workflow-review.md": {
        "topics": ["workflow", "operations", "process-improvement", "personal-effectiveness"],
        "load_priority": "on_demand",
    },
    "cron-health.md": {
        "topics": ["cron", "health", "monitoring", "automation"],
        "load_priority": "on_demand",
    },
    "codex-metrics.md": {
        "topics": ["evaluation", "metrics", "system-performance"],
        "load_priority": "on_demand",
    },
    "historian-digest.md": {
        "topics": ["history", "recent-activity", "commits", "continuity"],
        "load_priority": "always",
    },
}


def get_summary(filepath: Path) -> str:
    """Extract summary from first 3 non-empty, non-heading lines."""
    lines = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith("#"):
                    continue
                if stripped.startswith("---"):
                    continue
                lines.append(stripped)
                if len(lines) >= 3:
                    break
    except OSError:
        return ""
    return " ".join(lines)[:200]


def estimate_tokens(filepath: Path) -> int:
    """Estimate tokens as word_count / 0.75."""
    try:
        text = filepath.read_text(encoding="utf-8")
        word_count = len(text.split())
        return int(word_count / 0.75)
    except OSError:
        return 0


def build_index() -> dict:
    files = []
    for md_file in sorted(ACTIVE_DIR.glob("*.md")):
        filename = md_file.name
        meta = FILE_META.get(filename)
        if meta is None:
            # Unknown file — index it as on_demand
            meta = {
                "topics": [filename.replace(".md", "").replace("-", " ")],
                "load_priority": "on_demand",
            }

        stat = md_file.stat()
        last_updated = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime(
            "%Y-%m-%d"
        )

        files.append(
            {
                "filename": filename,
                "path": f"active/{filename}",
                "topics": meta["topics"],
                "last_updated": last_updated,
                "summary": get_summary(md_file),
                "token_estimate": estimate_tokens(md_file),
                "load_priority": meta["load_priority"],
            }
        )

    return {
        "version": 1,
        "generated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "files": files,
    }


def main():
    index = build_index()
    index_path = ACTIVE_DIR / "index.json"
    tmp_path = ACTIVE_DIR / "index.json.tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        f.write("\n")

    tmp_path.rename(index_path)

    print(f"Built active/index.json: {len(index['files'])} files indexed")
    for entry in index["files"]:
        print(
            f"  {entry['filename']:30s} priority={entry['load_priority']:12s} tokens={entry['token_estimate']}"
        )


if __name__ == "__main__":
    main()
