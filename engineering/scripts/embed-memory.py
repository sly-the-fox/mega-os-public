#!/usr/bin/env python3
"""Build embedding index over Mega-OS documents for semantic search.

Uses fastembed (ONNX-based, fully local) with BAAI/bge-small-en-v1.5 (384 dims).
Stores embeddings in engineering/memory.db alongside the FTS5 index.
Incremental: skips files whose content hash hasn't changed.

Usage:
    python3 engineering/scripts/embed-memory.py           # incremental
    python3 engineering/scripts/embed-memory.py --force    # full re-embed
"""

import hashlib
import os
import re
import sqlite3
import struct
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "engineering" / "memory.db"
MAX_SIZE = 1_000_000
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
CHUNK_CHAR_THRESHOLD = 8000  # ~2K tokens

INDEX_DIRS = {
    "core/history": "history",
    "active": "active",
    "archive": "archive",
    "business": "business",
    ".claude/agents": "agents",
    ".claude/projects": "memory",
}
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
    if "node_modules" in path.parts or "__pycache__" in path.parts:
        return True
    return False


def rel(path):
    return str(path.relative_to(REPO_ROOT))


def modified_iso(path):
    return datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc).strftime("%Y-%m-%d")


def sha256(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def pack_embedding(vec):
    """Pack float32 vector into bytes."""
    return struct.pack(f"{len(vec)}f", *vec)


def unpack_embedding(blob, dim=EMBEDDING_DIM):
    """Unpack bytes into float32 list."""
    return list(struct.unpack(f"{dim}f", blob))


def chunk_text(content):
    """Split content into chunks. Per-file if small, section-level if large."""
    if len(content) < CHUNK_CHAR_THRESHOLD:
        return [(0, content)]

    sections = []
    current = []
    for line in content.splitlines(True):
        if line.startswith("## ") and current:
            sections.append("".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("".join(current))

    if len(sections) <= 1:
        return [(0, content)]

    return list(enumerate(sections))


def categorize(path_str):
    """Determine category from path."""
    for prefix, cat in INDEX_DIRS.items():
        if path_str.startswith(prefix):
            return cat
    return "other"


def collect_files():
    """Collect all markdown files to embed."""
    results = []
    for prefix in INDEX_DIRS:
        d = REPO_ROOT / prefix
        if not d.is_dir():
            continue
        for f in d.rglob("*.md"):
            if should_skip(f) or not f.is_file() or f.stat().st_size > MAX_SIZE:
                continue
            r = rel(f)
            if r.startswith("core/history/traces/"):
                continue
            results.append(f)
    return results


def init_table(conn):
    """Create the doc_embeddings table if it doesn't exist."""
    conn.execute("""CREATE TABLE IF NOT EXISTS doc_embeddings (
        path TEXT,
        content_hash TEXT,
        embedding BLOB,
        chunk_index INTEGER DEFAULT 0,
        chunk_text TEXT,
        token_count INTEGER,
        category TEXT,
        modified TEXT,
        indexed_at TEXT,
        PRIMARY KEY (path, chunk_index)
    )""")
    conn.commit()


def main():
    force = "--force" in sys.argv
    start = time.time()

    try:
        from fastembed import TextEmbedding
    except ImportError:
        print("ERROR: fastembed not installed. Run: pip install fastembed")
        sys.exit(1)

    print(f"Loading embedding model ({EMBEDDING_MODEL})...")
    model = TextEmbedding(EMBEDDING_MODEL)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    init_table(conn)

    # Load existing hashes for incremental skip
    existing = {}
    if not force:
        try:
            for row in conn.execute("SELECT path, chunk_index, content_hash FROM doc_embeddings"):
                existing[(row[0], row[1])] = row[2]
        except sqlite3.OperationalError:
            pass

    files = collect_files()
    print(f"Found {len(files)} markdown files")

    # Determine what needs embedding
    to_embed = []
    seen_paths = set()
    skipped = 0

    for f in files:
        path = rel(f)
        seen_paths.add(path)
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        content_hash = sha256(content)
        category = categorize(path)
        mod = modified_iso(f)
        chunks = chunk_text(content)

        for chunk_idx, chunk_content in chunks:
            key = (path, chunk_idx)
            if not force and key in existing and existing[key] == content_hash:
                skipped += 1
                continue
            to_embed.append({
                "path": path,
                "chunk_index": chunk_idx,
                "chunk_text": chunk_content[:200],
                "full_text": chunk_content,
                "content_hash": content_hash,
                "token_count": len(chunk_content) // 4,
                "category": category,
                "modified": mod,
            })

    # Delete rows for files that no longer exist
    deleted = 0
    for (path, chunk_idx) in list(existing.keys()):
        if path not in seen_paths:
            conn.execute("DELETE FROM doc_embeddings WHERE path=? AND chunk_index=?",
                         (path, chunk_idx))
            deleted += 1

    if not to_embed and deleted == 0:
        total = conn.execute("SELECT COUNT(*) FROM doc_embeddings").fetchone()[0]
        elapsed = time.time() - start
        print(f"Embeddings up to date ({total} chunks, {skipped} unchanged). "
              f"Took {elapsed:.1f}s")
        conn.close()
        return

    # Batch embed in small groups to limit memory usage
    BATCH_SIZE = 32
    if to_embed:
        total_chunks = len(to_embed)
        print(f"Embedding {total_chunks} chunks in batches of {BATCH_SIZE}...")
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        for batch_start in range(0, total_chunks, BATCH_SIZE):
            batch = to_embed[batch_start:batch_start + BATCH_SIZE]
            texts = [item["full_text"] for item in batch]
            embeddings = list(model.embed(texts))

            for item, emb in zip(batch, embeddings):
                conn.execute(
                    "DELETE FROM doc_embeddings WHERE path=? AND chunk_index=?",
                    (item["path"], item["chunk_index"]),
                )
                conn.execute(
                    "INSERT INTO doc_embeddings VALUES (?,?,?,?,?,?,?,?,?)",
                    (
                        item["path"],
                        item["content_hash"],
                        pack_embedding(emb),
                        item["chunk_index"],
                        item["chunk_text"],
                        item["token_count"],
                        item["category"],
                        item["modified"],
                        now_iso,
                    ),
                )
            conn.commit()
            done = min(batch_start + BATCH_SIZE, total_chunks)
            print(f"  {done}/{total_chunks} chunks embedded")

    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM doc_embeddings").fetchone()[0]
    elapsed = time.time() - start

    print(f"\nEmbedded: {len(to_embed)} new/changed chunks")
    print(f"Deleted: {deleted} stale chunks")
    print(f"Skipped: {skipped} unchanged chunks")
    print(f"Total: {total} chunks in index")
    print(f"Time: {elapsed:.1f}s")

    for cat, cnt in conn.execute(
        "SELECT category, COUNT(*) FROM doc_embeddings GROUP BY category ORDER BY category"
    ):
        print(f"  {cat}: {cnt}")
    conn.close()


if __name__ == "__main__":
    main()
