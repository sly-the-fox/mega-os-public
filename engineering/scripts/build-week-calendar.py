#!/usr/bin/env python3
"""Build a rolling 2-week calendar with events extracted from active state files.

Generates active/week-calendar.md with date→day-of-week mapping and scheduled events.
Designed to run daily via cron (after active-index-rebuild, ~9:25 AM).

Zero API cost — pure Python, no LLM calls.
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

MEGA_OS = Path(__file__).resolve().parent.parent.parent
OUTPUT = MEGA_OS / "active" / "week-calendar.md"

# Files to scan for date references
SCAN_FILES = [
    MEGA_OS / "active" / "now.md",
    MEGA_OS / "business" / "network" / "contacts.md",
    MEGA_OS / "core" / "indexes" / "active-context-map.md",
]

# Patterns that indicate an event with a date
# Match ISO dates (2026-03-25) and short dates (Mar 25, 3/25)
ISO_DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
SHORT_DATE_RE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{1,2})\b",
    re.IGNORECASE,
)
SLASH_DATE_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})\b")

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def extract_events(today: datetime) -> dict[str, list[str]]:
    """Extract date→event snippets from scan files. Returns {ISO_date: [snippet, ...]}."""
    events: dict[str, list[str]] = {}
    year = today.year
    window_start = today - timedelta(days=1)
    window_end = today + timedelta(days=15)

    for fpath in SCAN_FILES:
        if not fpath.exists():
            continue
        text = fpath.read_text()
        for line in text.splitlines():
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith("#"):
                continue

            dates_found: list[str] = []

            # ISO dates
            for m in ISO_DATE_RE.finditer(line):
                dates_found.append(m.group(1))

            # Short dates (Mar 25)
            for m in SHORT_DATE_RE.finditer(line):
                month_num = MONTH_MAP.get(m.group(1)[:3].lower())
                if month_num:
                    day_num = int(m.group(2))
                    try:
                        d = datetime(year, month_num, day_num)
                        dates_found.append(d.strftime("%Y-%m-%d"))
                    except ValueError:
                        pass

            # Slash dates (3/25)
            for m in SLASH_DATE_RE.finditer(line):
                month_num = int(m.group(1))
                day_num = int(m.group(2))
                if 1 <= month_num <= 12 and 1 <= day_num <= 31:
                    try:
                        d = datetime(year, month_num, day_num)
                        dates_found.append(d.strftime("%Y-%m-%d"))
                    except ValueError:
                        pass

            for date_str in dates_found:
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue
                if window_start <= dt <= window_end:
                    # Extract a useful snippet from the line
                    snippet = line_stripped
                    # Clean up markdown formatting
                    snippet = re.sub(r"^[-*\[\]x~\s]+", "", snippet)
                    snippet = snippet[:120]
                    if snippet and date_str not in events.get(date_str, []):
                        events.setdefault(date_str, [])
                        # Avoid duplicate snippets
                        if snippet not in events[date_str]:
                            events[date_str].append(snippet)

    return events


def build_calendar(today: datetime, events: dict[str, list[str]]) -> str:
    """Build the markdown calendar content."""
    lines = [
        "---",
        "title: Week Calendar",
        "owner: week-calendar",
        "topics: [week calendar]",
        "load_priority: on_demand",
        "---",
        "",
        "# Week Calendar",
        "",
        f"Generated: {today.strftime('%Y-%m-%d')} ({today.strftime('%A')})",
        "",
    ]

    # Find the Monday of this week
    monday = today - timedelta(days=today.weekday())
    week_num = today.isocalendar()[1]

    for week_offset, label in [(0, "This Week"), (1, "Next Week")]:
        wk = week_num + week_offset
        week_start = monday + timedelta(weeks=week_offset)
        lines.append(f"## {label} (W{wk})")
        lines.append("")
        lines.append("| Date | Day | Events |")
        lines.append("|------|-----|--------|")

        for day_offset in range(7):
            d = week_start + timedelta(days=day_offset)
            date_str = d.strftime("%Y-%m-%d")
            day_name = d.strftime("%a")
            day_events = events.get(date_str, [])

            if day_events:
                # Take up to 3 most relevant events, truncate
                event_text = "; ".join(e[:80] for e in day_events[:3])
                if len(day_events) > 3:
                    event_text += f" (+{len(day_events) - 3} more)"
            else:
                event_text = "—"

            # Highlight today
            if d.date() == today.date():
                lines.append(f"| **{date_str}** | **{day_name}** | **{event_text}** |")
            else:
                lines.append(f"| {date_str} | {day_name} | {event_text} |")

        lines.append("")

    return "\n".join(lines)


def main():
    today = datetime.now()
    events = extract_events(today)
    calendar_md = build_calendar(today, events)
    OUTPUT.write_text(calendar_md)
    print(f"Written: {OUTPUT} ({len(events)} dates with events)")


if __name__ == "__main__":
    main()
