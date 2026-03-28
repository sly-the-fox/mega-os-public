#!/usr/bin/env python3
"""Archive trace entries older than 30 days and produce weekly summaries.

Usage: python3 archive-traces.py
Designed for cron. Safe when trace files are empty or missing.
"""

import fcntl
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_TRACE_DIR = _REPO_ROOT / "core" / "history" / "traces"
_ARCHIVE_DIR = _TRACE_DIR / "archive"
_CUTOFF_DAYS = 30

_FILES = {
    "workflow": _TRACE_DIR / "workflow-traces.jsonl",
    "event": _TRACE_DIR / "event-log.jsonl",
    "timing": _TRACE_DIR / "timing.jsonl",
}


def _parse_ts(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _read_jsonl(path):
    if not path.exists() or path.stat().st_size == 0:
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"Warning: skipping malformed line in {path.name}", file=sys.stderr)
    return entries


def _write_jsonl_locked(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        for e in entries:
            os.write(fd, (json.dumps(e, separators=(",", ":")) + "\n").encode())
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _partition(entries, cutoff):
    old, recent = [], []
    for e in entries:
        ts_str = e.get("ts", e.get("timestamp", ""))
        if not ts_str:
            recent.append(e)
            continue
        try:
            if _parse_ts(ts_str) < cutoff:
                old.append(e)
            else:
                recent.append(e)
        except (ValueError, TypeError):
            recent.append(e)
    return old, recent


def _workflow_stats(entries):
    by_wf = defaultdict(list)
    for e in entries:
        by_wf[e.get("workflow", "unknown")].append(e)
    stats = {}
    for wf, items in by_wf.items():
        total = len(items)
        ok = sum(1 for i in items if i.get("status") == "success")
        durations = [i["duration_s"] for i in items if "duration_s" in i]
        stats[wf] = {
            "total": total, "successes": ok, "failures": total - ok,
            "success_rate": round(ok / total, 3) if total else 0,
            "avg_duration_s": round(sum(durations) / len(durations), 3) if durations else None,
        }
    return stats


def _timing_stats(entries):
    by_skill = defaultdict(list)
    for e in entries:
        by_skill[e.get("skill", "unknown")].append(e)
    stats = {}
    for skill, items in by_skill.items():
        durations = [i["duration_s"] for i in items if "duration_s" in i]
        stats[skill] = {
            "runs": len(items),
            "avg_s": round(sum(durations) / len(durations), 3) if durations else None,
            "max_s": round(max(durations), 3) if durations else None,
            "failures": sum(1 for i in items if i.get("exit_code", 0) != 0),
        }
    return stats


def main():
    cutoff = datetime.now(timezone.utc) - timedelta(days=_CUTOFF_DAYS)
    now = datetime.now(timezone.utc)
    iso_year, iso_week, _ = now.isocalendar()
    week_label = f"{iso_year}-W{iso_week:02d}"

    all_old = {}
    all_recent = {}
    for key, path in _FILES.items():
        entries = _read_jsonl(path)
        old, recent = _partition(entries, cutoff)
        all_old[key] = old
        all_recent[key] = recent

    total = sum(len(v) for v in all_old.values())
    if total == 0:
        print("No entries older than 30 days. Nothing to archive.")
        return

    summary = {
        "archived_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cutoff": cutoff.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "week": week_label,
        "counts": {k: len(v) for k, v in all_old.items()},
        "workflow_stats": _workflow_stats(all_old["workflow"]),
        "timing_stats": _timing_stats(all_old["timing"]),
    }

    _ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = _ARCHIVE_DIR / f"{week_label}-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Summary: {summary_path}")

    for key, path in _FILES.items():
        if all_old[key]:
            _write_jsonl_locked(path, all_recent[key])
            print(f"  {key}: archived {len(all_old[key])}, {len(all_recent[key])} remain")

    print(f"Total archived: {total}")


if __name__ == "__main__":
    main()
