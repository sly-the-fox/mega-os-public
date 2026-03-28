#!/usr/bin/env python3
"""Build active/historian-digest.md from git log.

Reads recent git commits, groups by day and scope, detects timeline gaps
vs core/history/master-timeline.md. Zero API cost — pure git + filesystem.
"""

import re
import subprocess
import sys
from datetime import datetime, date, timedelta
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DIGEST_FILE = ROOT / "active" / "historian-digest.md"
TIMELINE_FILE = ROOT / "core" / "history" / "master-timeline.md"


def get_commits(since_days: int) -> list[dict]:
    """Get commits from the last N days."""
    result = subprocess.run(
        ["git", "log", f"--since={since_days} days ago", "--format=%H|%ai|%s"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"git log failed: {result.stderr}", file=sys.stderr)
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        sha, date_str, subject = parts
        # Parse date (format: 2026-03-17 15:20:01 -0600)
        commit_date = date_str.strip().split(" ")[0]
        commits.append({
            "sha": sha[:8],
            "date": commit_date,
            "subject": subject.strip(),
        })
    return commits


def parse_scope(subject: str) -> tuple[str, str]:
    """Extract scope and description from 'scope: description' format."""
    match = re.match(r"^(\w[\w-]*):\s+(.+)$", subject)
    if match:
        return match.group(1), match.group(2)
    return "unscoped", subject


def get_last_timeline_date() -> str | None:
    """Find the date of the most recent entry in master-timeline.md."""
    if not TIMELINE_FILE.exists():
        return None
    try:
        text = TIMELINE_FILE.read_text(encoding="utf-8")
    except OSError:
        return None

    last_date = None
    for line in text.split("\n"):
        match = re.match(r"^-\s+\*\*(\d{4}-\d{2}-\d{2})", line)
        if match:
            last_date = match.group(1)
    return last_date


def count_commits_since(commits: list[dict], since_date: str) -> int:
    """Count commits after the given date."""
    return sum(1 for c in commits if c["date"] > since_date)


def group_by_day_and_scope(commits: list[dict]) -> dict[str, dict[str, list[str]]]:
    """Group commits into {date: {scope: [descriptions]}}."""
    grouped = defaultdict(lambda: defaultdict(list))
    for c in commits:
        scope, desc = parse_scope(c["subject"])
        grouped[c["date"]][scope].append(desc)
    return grouped


def format_scope_summary(scope_groups: dict[str, list[str]], max_items: int = 5) -> list[str]:
    """Format scope groups as bullet points."""
    lines = []
    for scope in sorted(scope_groups):
        descs = scope_groups[scope]
        count = len(descs)
        # Show up to max_items descriptions, truncate rest
        shown = descs[:max_items]
        summary = "; ".join(shown)
        if count > max_items:
            summary += f" (+{count - max_items} more)"
        lines.append(f"- **{scope}** ({count}): {summary}")
    return lines


def build_digest() -> str:
    """Build the full digest markdown."""
    now = datetime.now()
    all_commits = get_commits(7)

    # Split into 48h and 7d
    cutoff_48h = (date.today() - timedelta(days=2)).isoformat()
    recent = [c for c in all_commits if c["date"] >= cutoff_48h]
    recent_grouped = group_by_day_and_scope(recent)
    all_grouped = group_by_day_and_scope(all_commits)

    # Timeline gap
    last_timeline = get_last_timeline_date()

    lines = [
        "---",
        "title: Recent Activity Digest",
        "owner: historian-digest",
        "topics: [history, recent-activity, commits, continuity]",
        "load_priority: always",
        "---",
        "",
        "# Recent Activity Digest",
        "",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    # Last 48 hours
    lines.append(f"## Last 48 Hours ({len(recent)} commits)")
    lines.append("")
    if recent:
        lines.append("### By Scope")
        # Merge all recent into one scope view
        merged_scopes = defaultdict(list)
        for day_scopes in recent_grouped.values():
            for scope, descs in day_scopes.items():
                merged_scopes[scope].extend(descs)
        lines.extend(format_scope_summary(merged_scopes))
    else:
        lines.append("*No commits in the last 48 hours.*")
    lines.append("")

    # Last 7 days
    lines.append(f"## Last 7 Days ({len(all_commits)} commits)")
    lines.append("")
    if all_commits:
        lines.append("### By Scope")
        merged_scopes = defaultdict(list)
        for day_scopes in all_grouped.values():
            for scope, descs in day_scopes.items():
                merged_scopes[scope].extend(descs)
        lines.extend(format_scope_summary(merged_scopes))
        lines.append("")

        lines.append("### By Day")
        for day in sorted(all_grouped.keys(), reverse=True):
            day_commits = sum(len(v) for v in all_grouped[day].values())
            lines.append(f"- **{day}** ({day_commits} commits)")
    else:
        lines.append("*No commits in the last 7 days.*")
    lines.append("")

    # Timeline gap
    lines.append("## Timeline Gap")
    lines.append("")
    if last_timeline:
        gap_count = count_commits_since(all_commits, last_timeline)
        lines.append(f"- Last timeline entry: {last_timeline}")
        lines.append(f"- Commits since then: {gap_count}")
        if gap_count > 0:
            lines.append(f"- ⚠ ACTION: Run Historian Checklist to backfill")
        else:
            lines.append("- Timeline is up to date")
    else:
        lines.append("- No timeline entries found in master-timeline.md")
        lines.append(f"- Total commits in last 7 days: {len(all_commits)}")
        lines.append("- ⚠ ACTION: Initialize master timeline")
    lines.append("")

    return "\n".join(lines)


def main():
    digest = build_digest()

    # Atomic write
    tmp_path = DIGEST_FILE.with_suffix(".md.tmp")
    tmp_path.write_text(digest, encoding="utf-8")
    tmp_path.rename(DIGEST_FILE)

    print(f"Wrote {DIGEST_FILE}")
    # Print summary to stdout for cron log
    lines = digest.split("\n")
    for line in lines:
        if line.startswith("##") or line.startswith("- ⚠"):
            print(f"  {line}")


if __name__ == "__main__":
    main()
