#!/usr/bin/env python3
"""Query the Mega-OS FTS5 full-text search index.

Usage:
    python3 engineering/scripts/query_memory.py "rejected improvements"
    python3 engineering/scripts/query_memory.py "revenue" --category active --limit 5
"""

import argparse
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "memory.db"


def main():
    p = argparse.ArgumentParser(description="Search Mega-OS memory index")
    p.add_argument("query", help="FTS5 search query")
    p.add_argument("--category", choices=["history", "active", "archive", "traces", "business", "agents"])
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--db", default=str(DEFAULT_DB))
    args = p.parse_args()

    if not Path(args.db).is_file():
        print("Index not built. Run: python3 engineering/scripts/index-memory.py")
        sys.exit(1)

    conn = sqlite3.connect(args.db)
    sql = """SELECT path, title, snippet(documents, 2, '>>', '<<', '...', 40),
             category, modified, rank
             FROM documents WHERE documents MATCH ?"""
    params = [args.query]
    if args.category:
        sql += " AND category = ?"
        params.append(args.category)
    sql += " ORDER BY rank LIMIT ?"
    params.append(args.limit)

    try:
        rows = conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        escaped = args.query.replace('"', '""')
        params[0] = f'"{escaped}"'
        rows = conn.execute(sql, params).fetchall()

    if not rows:
        print(f"No results for: {args.query}")
        return

    for i, (path, title, snip, cat, mod, rank) in enumerate(rows, 1):
        snip_clean = snip.strip().replace("\n", " ")[:200]
        print(f"[{i}] {path} ({mod}, {cat})")
        print(f"    {snip_clean}\n")
    print(f"--- {len(rows)} result(s) ---")
    conn.close()


if __name__ == "__main__":
    main()
