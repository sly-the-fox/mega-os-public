#!/usr/bin/env python3
"""Build SQLite FTS5 full-text search index over Mega-OS markdown files.

Creates engineering/memory.db indexing markdown across core/history, active,
archive, business, and agent definitions, plus JSONL trace files.

Supports incremental mode: skips rebuild if no files changed since last run.
Full rebuild on Sundays or with --force flag.

Usage:
    python3 engineering/scripts/index-memory.py           # incremental
    python3 engineering/scripts/index-memory.py --force    # full rebuild
"""

import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "engineering" / "memory.db"
MAX_SIZE = 1_000_000

INDEX_DIRS = {
    "core/history": "history",
    "active": "active",
    "archive": "archive",
    "business": "business",
    ".claude/agents": "agents",
}
TRACES_DIR = "core/history/traces"
SKIP_DIRS = {"node_modules", ".git", "__pycache__", "archive"}
EXCLUDE_FILES = {"contacts.md"}
EXCLUDE_EXT = {".env", ".key", ".pem", ".db", ".sqlite", ".png", ".jpg",
               ".jpeg", ".gif", ".svg", ".pdf", ".zip", ".pyc", ".so"}


def should_skip(path):
    if path.name in EXCLUDE_FILES:
        return True
    if path.suffix.lower() in EXCLUDE_EXT:
        return True
    if path.name.startswith(".env"):
        return True
    return False


def extract_title(content, filename):
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else filename


def rel(path):
    return str(path.relative_to(REPO_ROOT))


def modified_iso(path):
    return datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc).strftime("%Y-%m-%d")


def collect_md():
    results = []
    for prefix, category in INDEX_DIRS.items():
        d = REPO_ROOT / prefix
        if not d.is_dir():
            continue
        for f in d.rglob("*.md"):
            if should_skip(f) or not f.is_file() or f.stat().st_size > MAX_SIZE:
                continue
            r = rel(f)
            if r.startswith("core/history/traces/"):
                continue
            results.append((f, category))
    return results


def collect_traces():
    d = REPO_ROOT / TRACES_DIR
    if not d.is_dir():
        return []
    return [f for f in d.rglob("*.jsonl") if f.is_file() and f.stat().st_size <= MAX_SIZE]


def get_last_rebuild(conn):
    """Get timestamp of last successful rebuild."""
    try:
        row = conn.execute("SELECT value FROM index_meta WHERE key='last_rebuild'").fetchone()
        return float(row[0]) if row else 0
    except sqlite3.OperationalError:
        return 0


def set_last_rebuild(conn):
    """Record current time as last rebuild."""
    conn.execute("CREATE TABLE IF NOT EXISTS index_meta (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute("INSERT OR REPLACE INTO index_meta VALUES ('last_rebuild', ?)",
                 (str(time.time()),))
    conn.commit()


def any_file_newer(md_files, trace_files, last_rebuild):
    """Check if any indexed file has been modified since last rebuild."""
    for f, _ in md_files:
        try:
            if f.stat().st_mtime > last_rebuild:
                return True
        except OSError:
            return True
    for f in trace_files:
        try:
            if f.stat().st_mtime > last_rebuild:
                return True
        except OSError:
            return True
    return False


def full_rebuild(conn, md_files, trace_files):
    """Drop and recreate the FTS5 index from scratch."""
    conn.execute("DROP TABLE IF EXISTS documents")
    conn.execute("""CREATE VIRTUAL TABLE documents USING fts5(
        path, title, content, category, modified,
        tokenize='porter unicode61'
    )""")

    md_count = 0
    for f, cat in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        conn.execute("INSERT INTO documents VALUES (?,?,?,?,?)",
                     (rel(f), extract_title(content, f.name), content, cat, modified_iso(f)))
        md_count += 1

    trace_count = 0
    for f in trace_files:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            title = f"{f.name}:{i}"
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    parts = [obj.get("agent", ""), obj.get("action", ""),
                             str(obj.get("detail", ""))[:80]]
                    title = " | ".join(p for p in parts if p)
            except (json.JSONDecodeError, KeyError):
                pass
            conn.execute("INSERT INTO documents VALUES (?,?,?,?,?)",
                         (rel(f), title, line, "traces", modified_iso(f)))
            trace_count += 1

    conn.commit()
    return md_count, trace_count


def main():
    force = "--force" in sys.argv
    is_sunday = datetime.now().weekday() == 6

    md_files = collect_md()
    trace_files = collect_traces()
    print(f"Found {len(md_files)} markdown, {len(trace_files)} trace files")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))

    # Incremental: skip rebuild if no files changed
    if not force and not is_sunday:
        last_rebuild = get_last_rebuild(conn)
        if last_rebuild > 0 and not any_file_newer(md_files, trace_files, last_rebuild):
            try:
                total = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            except sqlite3.OperationalError:
                total = 0
            if total > 0:
                print(f"Index up to date ({total} docs). Skipping rebuild.")
                conn.close()
                return

    reason = "forced" if force else ("weekly full rebuild" if is_sunday else "files changed")
    print(f"Rebuilding FTS5 index ({reason})...")

    md_count, trace_count = full_rebuild(conn, md_files, trace_files)
    set_last_rebuild(conn)

    total = md_count + trace_count
    size = DB_PATH.stat().st_size
    sz = f"{size/1024:.1f} KB" if size < 1_000_000 else f"{size/1_048_576:.1f} MB"

    print(f"\nIndexed: {md_count} markdown + {trace_count} traces = {total} docs ({sz})")
    for cat, cnt in conn.execute(
        "SELECT category, COUNT(*) FROM documents GROUP BY category ORDER BY category"
    ):
        print(f"  {cat}: {cnt}")
    conn.close()


if __name__ == "__main__":
    main()
