#!/usr/bin/env python3
"""Rank context files by relevance to a query for smart context budgeting.

Combines FTS5 BM25 scores and embedding cosine similarity to produce a ranked
list of files with token cost estimates and budget recommendations.

Always-load files (from active/index.json) bypass scoring entirely.

Usage:
    python3 engineering/scripts/rank-context.py "update the sales pipeline"
    python3 engineering/scripts/rank-context.py "agent routing" --budget 20000
    python3 engineering/scripts/rank-context.py "revenue forecasting" --json
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "engineering" / "memory.db"
ACTIVE_INDEX = REPO_ROOT / "active" / "index.json"
DEFAULT_BUDGET = 15000  # tokens
FTS5_WEIGHT = 0.4
EMBED_WEIGHT = 0.6


def load_active_index():
    """Load active/index.json for token estimates and load priorities."""
    try:
        data = json.loads(ACTIVE_INDEX.read_text(encoding="utf-8"))
        return data.get("files", [])
    except (OSError, json.JSONDecodeError):
        return []


def fts5_scores(query, limit=50):
    """Get BM25 scores from FTS5 index. Returns {path: raw_rank}."""
    if not DB_PATH.exists():
        return {}
    conn = sqlite3.connect(str(DB_PATH))
    sql = """SELECT path, rank FROM documents WHERE documents MATCH ?
             ORDER BY rank LIMIT ?"""
    try:
        rows = conn.execute(sql, [query, limit]).fetchall()
    except sqlite3.OperationalError:
        escaped = query.replace('"', '""')
        try:
            rows = conn.execute(sql, [f'"{escaped}"', limit]).fetchall()
        except sqlite3.OperationalError:
            rows = []
    conn.close()
    # FTS5 rank is negative (more negative = better match)
    return {path: rank for path, rank in rows}


def embedding_scores(query, limit=50):
    """Get cosine similarity scores from embedding index. Returns {path: score}."""
    try:
        # Import inline to handle missing fastembed gracefully
        from semantic_search import semantic_search
        results = semantic_search(query, top_k=limit)
        # Deduplicate: keep best chunk score per file
        best = {}
        for r in results:
            path = r["path"]
            if path not in best or r["score"] > best[path]:
                best[path] = r["score"]
        return best
    except (ImportError, Exception):
        return {}


def normalize_scores(scores):
    """Normalize scores to [0, 1] range."""
    if not scores:
        return {}
    vals = list(scores.values())
    min_v, max_v = min(vals), max(vals)
    if max_v == min_v:
        return {k: 1.0 for k in scores}
    return {k: (v - min_v) / (max_v - min_v) for k, v in scores.items()}


def estimate_tokens(path):
    """Estimate token count for a file."""
    full_path = REPO_ROOT / path
    try:
        size = full_path.stat().st_size
        return size // 4  # rough chars/4 estimate
    except OSError:
        return 500  # default


def rank_context(query, budget=DEFAULT_BUDGET, output_json=False):
    """Rank files by relevance and allocate within token budget."""
    # Get always-load files from index
    index_files = load_active_index()
    always_files = {f["path"] for f in index_files if f.get("load_priority") == "always"}
    token_estimates = {f["path"]: f.get("token_estimate", 500) for f in index_files}

    # Score files
    fts5 = fts5_scores(query)
    embeds = embedding_scores(query)

    # FTS5 ranks are negative; invert so higher = better
    if fts5:
        fts5_inverted = {k: -v for k, v in fts5.items()}
        fts5_norm = normalize_scores(fts5_inverted)
    else:
        fts5_norm = {}

    embed_norm = normalize_scores(embeds)

    # Combine all scored paths
    all_paths = set(fts5_norm.keys()) | set(embed_norm.keys())

    # Include always-load files even if they didn't score
    all_paths = set(fts5_norm.keys()) | set(embed_norm.keys()) | always_files

    scored = []
    for path in all_paths:
        f_score = fts5_norm.get(path, 0)
        e_score = embed_norm.get(path, 0)

        # Weighted blend
        if fts5_norm and embed_norm:
            combined = FTS5_WEIGHT * f_score + EMBED_WEIGHT * e_score
        elif embed_norm:
            combined = e_score
        else:
            combined = f_score

        tokens = token_estimates.get(path, estimate_tokens(path))
        scored.append({
            "path": path,
            "relevance_score": round(combined, 4),
            "fts5_score": round(f_score, 4),
            "embed_score": round(e_score, 4),
            "token_cost": tokens,
            "is_always": path in always_files,
        })

    # Always-load files first, then by relevance score
    scored.sort(key=lambda x: (not x["is_always"], -x["relevance_score"]))

    # Budget allocation
    # Always-load files consume budget first
    remaining_budget = budget
    for item in scored:
        if item["is_always"]:
            remaining_budget -= item["token_cost"]
            item["recommended"] = True

    # Greedily fill remaining budget
    for item in scored:
        if item["is_always"]:
            continue
        if item["token_cost"] <= remaining_budget and item["relevance_score"] > 0.1:
            item["recommended"] = True
            remaining_budget -= item["token_cost"]
        else:
            item["recommended"] = False

    return {
        "query": query,
        "budget": budget,
        "budget_used": budget - remaining_budget,
        "files": scored,
    }


def main():
    p = argparse.ArgumentParser(description="Rank context files by relevance")
    p.add_argument("query", help="User message or topic keywords")
    p.add_argument("--budget", type=int, default=DEFAULT_BUDGET,
                   help=f"Token budget (default: {DEFAULT_BUDGET})")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--top", type=int, default=20, help="Max results to show")
    args = p.parse_args()

    result = rank_context(args.query, budget=args.budget)

    if args.json:
        result["files"] = result["files"][:args.top]
        print(json.dumps(result, indent=2))
        return

    files = result["files"][:args.top]
    recommended = [f for f in files if f.get("recommended")]
    print(f"Context ranking for: \"{args.query}\"")
    print(f"Budget: {result['budget']} tokens, used: {result['budget_used']}")
    print(f"Recommended: {len(recommended)} files\n")

    for i, f in enumerate(files, 1):
        tag = " [ALWAYS]" if f["is_always"] else (" [LOAD]" if f.get("recommended") else "")
        scores = f"fts5={f['fts5_score']}, embed={f['embed_score']}"
        print(f"[{i}] {f['path']}{tag}")
        print(f"    score={f['relevance_score']}  tokens={f['token_cost']}  ({scores})")
        print()


if __name__ == "__main__":
    main()
