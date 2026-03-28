#!/usr/bin/env python3
"""Query engine for Mega-OS structured data.

Reads pre-built indexes (cross-references, contacts, pipeline, active index)
and answers structured queries. Zero API cost.

Usage:
    python3 query-engine.py "what mentions Jeff Toffoli"
    python3 query-engine.py "overdue follow-ups"
    python3 query-engine.py "pipeline at Discovery"
    python3 query-engine.py "stale files"
    python3 query-engine.py "stale files 3"       # files not updated in 3+ days
    python3 query-engine.py "P1 priorities"
    python3 query-engine.py "pending decisions"
"""

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TODAY = date.today()

XREF_PATH = ROOT / "core" / "indexes" / "cross-references.json"
CONTACTS_JSON = ROOT / "business" / "network" / "contacts.json"
CONTACTS_MD = ROOT / "business" / "network" / "contacts.md"
PIPELINE_JSON = ROOT / "business" / "sales" / "pipeline.json"
PIPELINE_MD = ROOT / "business" / "sales" / "pipeline.md"
ACTIVE_INDEX = ROOT / "active" / "index.json"
PRIORITIES_MD = ROOT / "active" / "priorities.md"
DECISIONS_MD = ROOT / "core" / "history" / "decisions.md"


def ensure_fresh(json_path: Path, md_source: Path, builder_script: str):
    """Regenerate JSON if the markdown source is newer."""
    if not json_path.exists():
        subprocess.run(
            ["python3", str(ROOT / "engineering" / "scripts" / builder_script)],
            capture_output=True, cwd=ROOT,
        )
        return
    if not md_source.exists():
        return
    if md_source.stat().st_mtime > json_path.stat().st_mtime:
        subprocess.run(
            ["python3", str(ROOT / "engineering" / "scripts" / builder_script)],
            capture_output=True, cwd=ROOT,
        )


def load_json(path: Path) -> dict:
    """Load JSON file, returning empty dict on error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def query_mentions(query: str) -> str:
    """Handle 'what mentions X' queries using cross-references."""
    # Ensure fresh
    ensure_fresh(XREF_PATH, ROOT / "active" / "now.md", "build-cross-references.py")
    xref = load_json(XREF_PATH)
    entities = xref.get("entities", {})

    # Extract entity name from query
    # Patterns: "what mentions X", "mentions X", "references X", "X references"
    term = query
    for prefix in ["what mentions ", "mentions ", "who mentions ", "references ", "what references "]:
        if term.lower().startswith(prefix):
            term = term[len(prefix):]
            break

    term = term.strip().rstrip("?")

    # Search entities by name (case-insensitive partial match)
    matches = []
    for key, entity in entities.items():
        if term.lower() in entity["name"].lower():
            matches.append(entity)

    if not matches:
        return f"No entities matching '{term}' found in cross-reference index."

    lines = []
    for m in matches:
        lines.append(f"## {m['type'].title()}: {m['name']}")
        lines.append(f"Canonical: `{m['canonical_file']}`")
        lines.append(f"Mentions: {m['mention_count']} across {len(m['referenced_in'])} files")
        lines.append("")
        for ref in m["referenced_in"]:
            lines.append(f"  - `{ref}`")
        lines.append("")

    return "\n".join(lines)


def query_overdue() -> str:
    """Handle 'overdue follow-ups' queries."""
    ensure_fresh(CONTACTS_JSON, CONTACTS_MD, "build-tabular-json.py")
    contacts = load_json(CONTACTS_JSON)
    people = contacts.get("people", [])

    overdue = [p for p in people if p.get("overdue")]
    if not overdue:
        return "No overdue follow-ups."

    lines = [f"## Overdue Follow-Ups ({len(overdue)})", ""]
    for p in sorted(overdue, key=lambda x: x.get("days_until_followup", 0)):
        days = abs(p.get("days_until_followup", 0))
        lines.append(
            f"- **{p['name']}** — {days}d overdue (was due {p['follow_up']}). "
            f"Next action: {p.get('next_action', 'N/A')}"
        )

    # Also show due today / this week
    due_today = [p for p in people if p.get("days_until_followup") == 0]
    due_week = [p for p in people if 0 < (p.get("days_until_followup") or 999) <= 7]

    if due_today:
        lines.extend(["", f"## Due Today ({len(due_today)})", ""])
        for p in due_today:
            lines.append(f"- **{p['name']}** — {p.get('next_action', 'N/A')}")

    if due_week:
        lines.extend(["", f"## Due This Week ({len(due_week)})", ""])
        for p in sorted(due_week, key=lambda x: x.get("days_until_followup", 0)):
            lines.append(
                f"- **{p['name']}** — due in {p['days_until_followup']}d ({p['follow_up']}). "
                f"{p.get('next_action', 'N/A')}"
            )

    stats = contacts.get("stats", {})
    lines.extend([
        "",
        f"**Totals:** {stats.get('total_active', 0)} active contacts, "
        f"{stats.get('overdue_followups', 0)} overdue, "
        f"{stats.get('due_this_week', 0)} due this week",
    ])

    return "\n".join(lines)


def query_pipeline(stage: str = None) -> str:
    """Handle 'pipeline at X' queries."""
    ensure_fresh(PIPELINE_JSON, PIPELINE_MD, "build-tabular-json.py")
    pipeline = load_json(PIPELINE_JSON)

    active = pipeline.get("active", [])
    if stage:
        active = [d for d in active if stage.lower() in d.get("stage", "").lower()]

    if not active:
        return f"No pipeline entries{' at stage ' + stage if stage else ''}."

    title = f"Pipeline — {stage}" if stage else "Full Pipeline"
    lines = [f"## {title} ({len(active)} deals)", ""]

    for d in active:
        overdue_tag = " [OVERDUE]" if d.get("overdue") else ""
        lines.append(
            f"- **{d['contact']}** ({d['company']}) — {d['stage']}{overdue_tag}\n"
            f"  Service: {d['service_interest']}\n"
            f"  Next: {d['next_action']} (due: {d['due']})"
        )
        lines.append("")

    warm = pipeline.get("warm", [])
    if warm and not stage:
        lines.extend([f"## Warm ({len(warm)})", ""])
        for name in warm:
            lines.append(f"- {name}")

    stats = pipeline.get("stats", {})
    lines.extend([
        "",
        f"**Totals:** {stats.get('active_deals', 0)} active, "
        f"{stats.get('warm_contacts', 0)} warm, "
        f"{stats.get('overdue_actions', 0)} overdue",
    ])

    return "\n".join(lines)


def query_stale(days: int = 7) -> str:
    """Handle 'stale files' queries — files not updated in N+ days."""
    index = load_json(ACTIVE_INDEX)
    files = index.get("files", [])

    stale = []
    for f in files:
        last = f.get("last_updated", "")
        if not last:
            continue
        try:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
            age = (TODAY - last_date).days
            if age >= days:
                stale.append({**f, "age_days": age})
        except ValueError:
            continue

    if not stale:
        return f"No files stale (>{days} days) in active/."

    stale.sort(key=lambda x: x["age_days"], reverse=True)

    lines = [f"## Stale Active Files (>{days} days, {len(stale)} files)", ""]
    for f in stale:
        lines.append(
            f"- **{f['filename']}** — {f['age_days']}d old "
            f"(last: {f['last_updated']}, priority: {f['load_priority']})"
        )

    return "\n".join(lines)


def query_priorities(level: str = "P1") -> str:
    """Handle 'P1 priorities' queries — extract priority section from priorities.md."""
    if not PRIORITIES_MD.exists():
        return "priorities.md not found."

    text = PRIORITIES_MD.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find the section matching the priority level
    in_section = False
    section_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"## {level}"):
            in_section = True
            section_lines.append(stripped)
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section:
            section_lines.append(line)

    if not section_lines:
        return f"No {level} section found in priorities.md."

    return "\n".join(section_lines)


def query_decisions() -> str:
    """Handle 'pending decisions' queries."""
    if not DECISIONS_MD.exists():
        return "decisions.md not found."

    text = DECISIONS_MD.read_text(encoding="utf-8")

    # Find all decision entries that aren't resolved
    lines = ["## Pending Decisions", ""]
    in_table = False
    headers = None
    pending = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table and headers:
                in_table = False
            continue

        cols = [c.strip() for c in stripped.split("|")]
        cols = [c for i, c in enumerate(cols) if c or i not in (0, len(cols) - 1)]
        if cols and cols[0] == "":
            cols = cols[1:]
        if cols and cols[-1] == "":
            cols = cols[:-1]

        if any(re.match(r"^[-:]+$", c) for c in cols):
            in_table = True
            continue

        if not in_table and "ID" in stripped:
            headers = cols
            in_table = False  # Next line is separator
            continue

        if headers and in_table:
            row = {}
            for i, h in enumerate(headers):
                row[h] = cols[i] if i < len(cols) else ""

            status = row.get("Status", "").lower()
            if "resolved" not in status and "closed" not in status:
                pending.append(row)

    if not pending:
        return "No pending decisions."

    for row in pending:
        dec_id = row.get("ID", "?")
        title = row.get("Decision", row.get("Title", "?"))
        date_val = row.get("Date", "")
        status = row.get("Status", "")
        lines.append(f"- **{dec_id}** — {title} ({date_val}, status: {status})")

    return "\n".join(lines)


def route_query(query: str) -> str:
    """Route a query string to the appropriate handler."""
    q = query.lower().strip()

    # Overdue / follow-ups
    if any(kw in q for kw in ["overdue", "follow-up", "followup", "due today", "due this week"]):
        return query_overdue()

    # Pipeline
    if "pipeline" in q:
        # Extract stage if present
        for stage in ["interested", "discovery", "proposal", "booked", "active", "won", "lost"]:
            if stage in q:
                return query_pipeline(stage.title())
        return query_pipeline()

    # Stale files
    if "stale" in q:
        # Check for custom day count
        match = re.search(r"(\d+)\s*d", q)
        days = int(match.group(1)) if match else 7
        return query_stale(days)

    # Priorities
    for level in ["P1", "P2", "P3", "P4"]:
        if level.lower() in q or f"priority {level[-1]}" in q:
            return query_priorities(level)
    if "priorities" in q or "priority" in q:
        return query_priorities("P1")

    # Pending decisions
    if "decision" in q or "pending" in q:
        return query_decisions()

    # Mentions / cross-references (default for anything else)
    if any(kw in q for kw in ["mention", "reference", "who", "what"]):
        return query_mentions(query)

    # If nothing matched, try as a mention search
    return query_mentions(query)


def main():
    if len(sys.argv) < 2:
        print("Usage: query-engine.py <query>")
        print()
        print("Examples:")
        print('  "what mentions Jeff Toffoli"')
        print('  "overdue follow-ups"')
        print('  "pipeline at Discovery"')
        print('  "stale files"')
        print('  "P1 priorities"')
        print('  "pending decisions"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    result = route_query(query)
    print(result)


if __name__ == "__main__":
    main()
