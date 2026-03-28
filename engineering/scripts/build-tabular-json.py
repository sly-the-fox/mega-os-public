#!/usr/bin/env python3
"""Build machine-queryable JSON companions for contacts.md and pipeline.md.

Parses markdown tables into structured JSON with computed fields
(overdue status, days until follow-up, stats). Zero API cost.
"""

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TODAY = date.today()

CONTACTS_MD = ROOT / "business" / "network" / "contacts.md"
CONTACTS_JSON = ROOT / "business" / "network" / "contacts.json"

PIPELINE_MD = ROOT / "business" / "sales" / "pipeline.md"
PIPELINE_JSON = ROOT / "business" / "sales" / "pipeline.json"


def parse_markdown_table(text: str, section_header: str = None) -> list[dict]:
    """Parse a markdown table into a list of dicts.

    If section_header is given, only parse the table under that ## heading.
    Handles escaped pipes within cells.
    """
    lines = text.splitlines()
    rows = []
    headers = None
    in_section = section_header is None
    past_separator = False

    for line in lines:
        stripped = line.strip()

        # Track section headers
        if stripped.startswith("## "):
            if section_header and section_header in stripped:
                in_section = True
                headers = None
                past_separator = False
                continue
            elif in_section and section_header:
                # Hit next section — stop
                break

        if not in_section:
            continue

        if not stripped.startswith("|"):
            if headers and past_separator:
                # End of table (non-table line after data rows)
                break
            continue

        # Parse table row
        # Handle escaped pipes by temporarily replacing them
        cleaned = stripped.replace("\\|", "\x00")
        cols = [c.strip().replace("\x00", "|") for c in cleaned.split("|")]
        # Remove empty strings from leading/trailing |
        cols = [c for c in cols if c or cols.index(c) not in (0, len(cols) - 1)]
        # Actually, split on | gives empty first/last, so filter properly
        cols = [c.strip() for c in cleaned.split("|")]
        if cols and cols[0] == "":
            cols = cols[1:]
        if cols and cols[-1] == "":
            cols = cols[:-1]

        if not cols:
            continue

        # Detect separator row
        if all(re.match(r"^[-:]+$", c.strip()) for c in cols):
            past_separator = True
            continue

        # Detect header row
        if headers is None:
            headers = [h.strip() for h in cols]
            continue

        if not past_separator:
            continue

        # Data row
        row = {}
        for i, h in enumerate(headers):
            row[h] = cols[i].strip() if i < len(cols) else ""
        rows.append(row)

    return rows


def parse_date(s: str) -> date | None:
    """Parse a date string, returning None for empty/dash values."""
    s = s.strip()
    if not s or s in ("—", "--", "-", "N/A", "TBD", "Ongoing", "ongoing"):
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_cadence(s: str) -> int | None:
    """Parse cadence as integer days."""
    s = s.strip()
    if not s or s in ("—", "--", "-"):
        return None
    try:
        return int(s)
    except ValueError:
        return None


def build_contacts_json() -> dict:
    """Build contacts.json from contacts.md."""
    if not CONTACTS_MD.exists():
        return {"version": 1, "error": "contacts.md not found"}

    text = CONTACTS_MD.read_text(encoding="utf-8")
    source_mtime = datetime.fromtimestamp(
        CONTACTS_MD.stat().st_mtime, tz=timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%S")

    # Parse People table
    people_rows = parse_markdown_table(text, "People")
    people = []
    overdue_count = 0
    due_today_count = 0
    due_this_week = 0

    for row in people_rows:
        name = row.get("Name", "").strip()
        if not name or name == "—":
            continue

        follow_up = parse_date(row.get("Follow-Up", ""))
        cadence = parse_cadence(row.get("Cadence", ""))

        overdue = False
        days_until = None
        if follow_up:
            delta = (follow_up - TODAY).days
            days_until = delta
            overdue = delta < 0
            if delta == 0:
                due_today_count += 1
            if 0 <= delta <= 7:
                due_this_week += 1
            if overdue:
                overdue_count += 1

        people.append({
            "name": name,
            "platform": row.get("Platform", "").strip(),
            "context": row.get("Context", "").strip()[:200],
            "last_contact": row.get("Last Contact", "").strip(),
            "follow_up": row.get("Follow-Up", "").strip(),
            "cadence": cadence,
            "next_action": row.get("Next Action", "").strip(),
            "notes": row.get("Notes", "").strip()[:300],
            "overdue": overdue,
            "days_until_followup": days_until,
        })

    # Parse Declined table
    declined_rows = parse_markdown_table(text, "Declined")
    declined = []
    for row in declined_rows:
        name = row.get("Name", row.get("Business", "")).strip()
        if name and name != "—":
            declined.append({
                "name": name,
                "reason": row.get("Reason", row.get("Notes", "")).strip(),
                "date": row.get("Date", "").strip(),
            })

    return {
        "version": 1,
        "generated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "business/network/contacts.md",
        "source_mtime": source_mtime,
        "people": people,
        "declined": declined,
        "stats": {
            "total_active": len(people),
            "total_declined": len(declined),
            "overdue_followups": overdue_count,
            "due_today": due_today_count,
            "due_this_week": due_this_week,
        },
    }


def build_pipeline_json() -> dict:
    """Build pipeline.json from pipeline.md."""
    if not PIPELINE_MD.exists():
        return {"version": 1, "error": "pipeline.md not found"}

    text = PIPELINE_MD.read_text(encoding="utf-8")
    source_mtime = datetime.fromtimestamp(
        PIPELINE_MD.stat().st_mtime, tz=timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%S")

    # Parse Active Pipeline table
    active_rows = parse_markdown_table(text, "Active Pipeline")
    active = []
    overdue_count = 0

    for row in active_rows:
        contact = row.get("Contact", "").strip()
        if not contact or contact == "—":
            continue

        due = parse_date(row.get("Due", ""))
        overdue = due is not None and (due - TODAY).days < 0

        if overdue:
            overdue_count += 1

        active.append({
            "contact": contact,
            "company": row.get("Company", "").strip(),
            "source": row.get("Source", "").strip(),
            "stage": row.get("Stage", "").strip(),
            "service_interest": row.get("Service Interest", "").strip(),
            "est_value": row.get("Est. Value", "").strip(),
            "next_action": row.get("Next Action", "").strip(),
            "due": row.get("Due", "").strip(),
            "overdue": overdue,
        })

    # Parse Warm section (bullet list, not table)
    warm = []
    in_warm = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Warm"):
            in_warm = True
            continue
        if in_warm and stripped.startswith("## "):
            in_warm = False
            continue
        if in_warm and stripped.startswith("- **"):
            # Extract name from **Name**
            match = re.match(r"- \*\*(.+?)\*\*", stripped)
            if match:
                warm.append(match.group(1))

    # Parse Won/Lost table
    won_lost_rows = parse_markdown_table(text, "Won / Lost")
    won_lost = []
    for row in won_lost_rows:
        contact = row.get("Contact", "").strip()
        if contact and contact != "—":
            won_lost.append({
                "contact": contact,
                "company": row.get("Company", "").strip(),
                "stage": row.get("Stage", "").strip(),
                "service": row.get("Service", "").strip(),
                "value": row.get("Value", "").strip(),
                "date": row.get("Date", "").strip(),
                "notes": row.get("Notes", "").strip(),
            })

    return {
        "version": 1,
        "generated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "business/sales/pipeline.md",
        "source_mtime": source_mtime,
        "active": active,
        "warm": warm,
        "won_lost": won_lost,
        "stats": {
            "active_deals": len(active),
            "warm_contacts": len(warm),
            "overdue_actions": overdue_count,
            "won": len([w for w in won_lost if w.get("stage") == "Won"]),
            "lost": len([w for w in won_lost if w.get("stage") == "Lost"]),
        },
    }


def atomic_write(data: dict, path: Path):
    """Write JSON atomically via temp file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    tmp.rename(path)


def main():
    contacts = build_contacts_json()
    atomic_write(contacts, CONTACTS_JSON)
    stats = contacts.get("stats", {})
    print(
        f"Built contacts.json: {stats.get('total_active', 0)} active, "
        f"{stats.get('overdue_followups', 0)} overdue, "
        f"{stats.get('due_this_week', 0)} due this week"
    )

    pipeline = build_pipeline_json()
    atomic_write(pipeline, PIPELINE_JSON)
    stats = pipeline.get("stats", {})
    print(
        f"Built pipeline.json: {stats.get('active_deals', 0)} active deals, "
        f"{stats.get('warm_contacts', 0)} warm, "
        f"{stats.get('overdue_actions', 0)} overdue actions"
    )


if __name__ == "__main__":
    main()
