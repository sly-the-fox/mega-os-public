#!/usr/bin/env python3
"""Archive aged news briefings into weekly buckets and maintain archive/index.json."""

import json
import os
import re
import shutil
import sys
from datetime import datetime, date, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
NEWS_DIR = ROOT / "deliverables" / "news"
ARCHIVE_DIR = ROOT / "archive" / "news"
ARCHIVE_INDEX = ROOT / "archive" / "index.json"

MAX_AGE_DAYS = 4
BRIEFING_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-briefing\.md$")


def parse_date(filename: str) -> date | None:
    """Extract date from YYYY-MM-DD-briefing.md filename."""
    m = BRIEFING_PATTERN.match(filename)
    if m:
        return date.fromisoformat(m.group(1))
    return None


def iso_week_key(d: date) -> str:
    """Return ISO week string like 2026-W10."""
    iso = d.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def week_date_range(d: date) -> list[str]:
    """Return [monday, sunday] for the ISO week containing d."""
    iso = d.isocalendar()
    monday = date.fromisocalendar(iso.year, iso.week, 1)
    sunday = date.fromisocalendar(iso.year, iso.week, 7)
    return [monday.isoformat(), sunday.isoformat()]


def extract_key_stories(filepath: Path) -> list[str]:
    """Extract HIGH-significance headlines from briefing."""
    stories = []
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return stories

    # Match patterns like: **[Headline]** — [Source] | HIGH
    # or lines containing "| HIGH"
    for line in text.split("\n"):
        if "HIGH" not in line:
            continue
        # Try to extract bold headline
        m = re.search(r"\*\*(.+?)\*\*", line)
        if m:
            stories.append(m.group(1))
    return stories


def extract_topics(filepath: Path) -> list[str]:
    """Extract topic sections from briefing headers."""
    topics = []
    topic_map = {
        "AI": "ai",
        "Big Tech": "ai",
        "UAP": "uaps",
        "Anomalous": "uaps",
        "International": "international",
        "Consciousness": "consciousness",
        "Anthropic": "anthropic",
        "Psychedelic": "psychedelics",
        "Medical": "medical",
        "Psychology": "psychology",
        "Epstein": "epstein",
        "Brand": "brand",
    }
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return topics

    for line in text.split("\n"):
        if line.startswith("## "):
            for keyword, topic in topic_map.items():
                if keyword.lower() in line.lower() and topic not in topics:
                    topics.append(topic)
    return topics


def estimate_tokens(filepath: Path) -> int:
    try:
        text = filepath.read_text(encoding="utf-8")
        return int(len(text.split()) / 0.75)
    except OSError:
        return 0


def load_archive_index() -> dict:
    if ARCHIVE_INDEX.exists():
        try:
            return json.loads(ARCHIVE_INDEX.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "version": 1,
        "generated": "",
        "content_types": ["news-briefing"],
        "weeks": {},
    }


def save_archive_index(index: dict):
    index["generated"] = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    tmp_path = ARCHIVE_INDEX.with_suffix(".json.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
    tmp_path.rename(ARCHIVE_INDEX)


def get_summary(filepath: Path) -> str:
    """Generate summary from briefing metadata line."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return ""

    # Look for the **Generated:** line with story counts
    for line in text.split("\n"):
        if "**Stories:**" in line:
            return line.strip().lstrip("*").rstrip("*").strip()
    return ""


def main():
    today = date.today()
    cutoff = today - timedelta(days=MAX_AGE_DAYS)

    if not NEWS_DIR.exists():
        print("No deliverables/news/ directory found.")
        return

    archived = []
    archive_index = load_archive_index()

    for filepath in sorted(NEWS_DIR.glob("*-briefing.md")):
        file_date = parse_date(filepath.name)
        if file_date is None:
            continue

        if file_date > cutoff:
            continue  # Too recent, skip

        # Calculate target directory
        week = iso_week_key(file_date)
        target_dir = ARCHIVE_DIR / week
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / filepath.name

        # Extract metadata before moving
        key_stories = extract_key_stories(filepath)
        topics = extract_topics(filepath)
        tokens = estimate_tokens(filepath)
        summary = get_summary(filepath)

        # Move file
        shutil.move(str(filepath), str(target_path))

        # Update archive index
        if week not in archive_index["weeks"]:
            archive_index["weeks"][week] = {
                "date_range": week_date_range(file_date),
                "files": [],
            }

        # Avoid duplicate entries
        existing_files = [
            f["filename"] for f in archive_index["weeks"][week]["files"]
        ]
        if filepath.name not in existing_files:
            archive_index["weeks"][week]["files"].append(
                {
                    "filename": filepath.name,
                    "path": f"archive/news/{week}/{filepath.name}",
                    "date": file_date.isoformat(),
                    "content_type": "news-briefing",
                    "topics": topics,
                    "key_stories": key_stories[:10],  # Cap at 10
                    "summary": summary,
                    "token_estimate": tokens,
                }
            )

        archived.append(f"{filepath.name} -> archive/news/{week}/")

    if archived:
        save_archive_index(archive_index)
        print(f"Archived {len(archived)} briefing(s):")
        for item in archived:
            print(f"  {item}")
    else:
        print("No briefings old enough to archive.")


if __name__ == "__main__":
    main()
