#!/usr/bin/env python3
"""Check health of all mega-os cron jobs by inspecting log files.

Writes a health report to active/cron-health.md and sends a single Telegram
alert if any jobs failed or didn't run.

Zero API cost — pure filesystem checks.
"""

import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HEALTH_FILE = ROOT / "active" / "cron-health.md"
NOTIFY_SCRIPT = ROOT / "engineering" / "scripts" / "notify-telegram.sh"

# Define expected cron jobs: (name, log_file, min_bytes, expected_schedule, target_file, scheduled_hour)
# expected_schedule: "daily", "monday", "sunday", "1st", "1st,15th", "wednesday"
# target_file: the file the job is expected to update (None if no specific output file)
# scheduled_hour: hour the job is scheduled to run (used to avoid false STALE for not-yet-run jobs)
CRON_JOBS = [
    ("Dream", "/tmp/mega-os-dream.log", 10, "daily", "active/dream-report.md", 5),
    ("Content Gen", "/tmp/mega-os-content-gen.log", 50, "daily", "business/marketing/channel-tracker.md", 7),
    ("Improvement Audit", "/tmp/mega-os-improvement-audit.log", 100, "daily", "active/improvement-audit.md", 7),
    ("News Briefing", "/tmp/mega-os-news-briefing.log", 100, "daily", "active/news-briefing.md", 8),
    ("Daily Scan", "/tmp/mega-os-daily-scan.log", 100, "daily", "active/daily-digest.md", 9),
    ("Freshstate", "/tmp/mega-os-freshstate.log", 20, "daily", "active/freshstate-report.md", 9),
    ("Metrics", "/tmp/mega-os-metrics.log", 20, "daily", None, 8),
    ("Index Rebuild", "/tmp/mega-os-index.log", 10, "daily", None, 9),
    ("Briefing Archive", "/tmp/mega-os-archive.log", 10, "daily", None, 9),
    ("Historian Digest", "/tmp/mega-os-historian-digest.log", 10, "daily", "active/historian-digest.md", 9),
    ("Cron Health", "/tmp/mega-os-cron-health.log", 0, "daily", None, 9),  # Self — may not exist yet
    ("Content Pipeline", "/tmp/mega-os-content-pipeline.log", 50, "monday", None, 8),
    ("Weekly Review", "/tmp/mega-os-weekly-review.log", 100, "sunday", None, 10),
    ("Revenue Check-in", "/tmp/mega-os-revenue-checkin.log", 50, "1st", None, 10),
    ("Risk Alert", "/tmp/mega-os-risk-alert.log", 50, "wednesday", None, 9),
    ("Index Maintenance", "/tmp/mega-os-index-maintenance.log", 50, "sunday", None, 10),
    ("System Evaluation", "/tmp/mega-os-evaluation.log", 50, "1st,15th", None, 11),
    ("Competitor Monitor", "/tmp/mega-os-competitor-monitor.log", 50, "quarterly", None, 9),
]

DAY_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def should_have_run_today(schedule: str, today: date) -> bool:
    """Determine if a job should have run today based on its schedule."""
    if schedule == "daily":
        return True
    if schedule in DAY_MAP:
        return today.weekday() == DAY_MAP[schedule]
    if schedule == "1st":
        return today.day == 1
    if schedule == "1st,15th":
        return today.day in (1, 15)
    if schedule == "quarterly":
        return today.day == 1 and today.month in (1, 4, 7, 10)
    return False


def check_log(log_path: str, min_bytes: int, today: date) -> dict:
    """Check a log file for health indicators."""
    p = Path(log_path)
    result = {
        "exists": False,
        "modified_today": False,
        "size_ok": False,
        "exit_ok": False,
        "exit_code": None,
        "timed_out": False,
    }

    if not p.exists():
        return result

    result["exists"] = True
    stat = p.stat()
    mod_date = date.fromtimestamp(stat.st_mtime)
    result["modified_today"] = mod_date == today
    result["size_ok"] = stat.st_size >= min_bytes

    # Check for exit code in log
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
        # Look for "Exit: <code>" pattern, scanning from end of file
        for line in reversed(text.split("\n")):
            if line.startswith("Exit: ") or line.startswith("Exit:"):
                # Extract numeric exit code
                match = re.search(r"Exit:\s*(\d+)", line)
                if match:
                    code = int(match.group(1))
                    result["exit_code"] = code
                    result["exit_ok"] = code == 0
                    result["timed_out"] = code == 124
                break
        # If no explicit exit line, check if content exists and is recent
        if result["exit_code"] is None and result["modified_today"] and result["size_ok"]:
            result["exit_ok"] = True  # Assume OK if log is fresh and has content
    except OSError:
        pass

    return result


def check_target(target_file: str | None, today: date) -> bool | None:
    """Check if a job's target output file was updated today. Returns None if no target."""
    if target_file is None:
        return None
    p = ROOT / target_file
    if not p.exists():
        return False
    mod_date = date.fromtimestamp(p.stat().st_mtime)
    return mod_date == today


def main():
    today = date.today()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    day_name = today.strftime("%A")

    lines = [
        "# Cron Health Report",
        "",
        f"**Generated:** {now} ({day_name})",
        "",
        "| Job | Schedule | Should Run | Log Exists | Modified Today | Size OK | Exit OK | Target OK | Status |",
        "|-----|----------|------------|------------|----------------|---------|---------|-----------|--------|",
    ]

    failures = []
    warnings = []
    current_hour = datetime.now().hour

    for name, log_path, min_bytes, schedule, target_file, scheduled_hour in CRON_JOBS:
        should_run = should_have_run_today(schedule, today)
        health = check_log(log_path, min_bytes, today)
        target_ok = check_target(target_file, today)

        if should_run:
            if health["modified_today"] and health["exit_ok"] and health["size_ok"]:
                if target_ok is False:
                    status = "OUTPUT STALE"
                    warnings.append(f"{name}: ran OK but target file not updated today")
                else:
                    status = "OK"
            elif not health["modified_today"] and scheduled_hour > current_hour:
                # Job hasn't run yet but its scheduled time is still ahead
                status = "PENDING"
            elif not health["exists"]:
                status = "MISSING"
                failures.append(f"{name}: log file missing")
            elif not health["modified_today"]:
                status = "STALE"
                failures.append(f"{name}: log not updated today")
            elif health["timed_out"]:
                status = "TIMEOUT"
                failures.append(f"{name}: timed out (exit 124)")
            elif not health["exit_ok"] and health["exit_code"] is not None:
                status = "FAILED"
                failures.append(f"{name}: exit code {health['exit_code']}")
            elif not health["size_ok"]:
                status = "EMPTY"
                warnings.append(f"{name}: log suspiciously small (<{min_bytes}b)")
            else:
                status = "WARN"
                warnings.append(f"{name}: partial issues")
        else:
            status = "N/A"

        target_str = {True: "Yes", False: "No", None: "—"}.get(target_ok, "—")
        lines.append(
            f"| {name} | {schedule} | {'Yes' if should_run else 'No'} "
            f"| {'Yes' if health['exists'] else 'No'} "
            f"| {'Yes' if health['modified_today'] else 'No'} "
            f"| {'Yes' if health['size_ok'] else 'No'} "
            f"| {'Yes' if health['exit_ok'] else 'No'} "
            f"| {target_str} "
            f"| {status} |"
        )

    # Summary
    lines.extend([
        "",
        "## Summary",
        "",
        f"- **Failures:** {len(failures)}",
        f"- **Warnings:** {len(warnings)}",
    ])

    if failures:
        lines.append("")
        lines.append("### Failures")
        for f in failures:
            lines.append(f"- {f}")

    if warnings:
        lines.append("")
        lines.append("### Warnings")
        for w in warnings:
            lines.append(f"- {w}")

    report = "\n".join(lines) + "\n"
    HEALTH_FILE.write_text(report, encoding="utf-8")
    print(f"Wrote {HEALTH_FILE}")

    # Send Telegram alert only if there are failures
    if failures and NOTIFY_SCRIPT.exists():
        import tempfile

        alert = f"Cron Health Alert ({now})\n\nFailures ({len(failures)}):\n"
        alert += "\n".join(f"  - {f}" for f in failures)
        if warnings:
            alert += f"\n\nWarnings ({len(warnings)}):\n"
            alert += "\n".join(f"  - {w}" for w in warnings)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as tf:
            tf.write(alert)
            tmp = tf.name
        try:
            subprocess.run(
                [str(NOTIFY_SCRIPT), "Cron Health", "1" if failures else "0", tmp],
                check=False,
                timeout=10,
            )
        finally:
            os.unlink(tmp)
    elif not failures:
        print("All expected jobs healthy. No Telegram alert needed.")


if __name__ == "__main__":
    main()
