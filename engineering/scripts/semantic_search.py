#!/usr/bin/env python3
"""Semantic search over Mega-OS document embeddings.

Uses locally-stored embeddings (BAAI/bge-small-en-v1.5 via fastembed) and
numpy cosine similarity. Zero API cost, runs entirely on CPU.

Usage:
    python3 engineering/scripts/semantic_search.py "how does work get assigned"
    python3 engineering/scripts/semantic_search.py "revenue model" --top 5
    python3 engineering/scripts/semantic_search.py "agent routing" --cat agents
"""

import argparse
import sqlite3
import struct
import sys
from pathlib import Path

EMBEDDING_DIM = 384
DB_PATH = Path(__file__).resolve().parent.parent / "memory.db"


def unpack_embedding(blob):
    """Unpack bytes into float32 numpy array."""
    import numpy as np
    return np.array(struct.unpack(f"{EMBEDDING_DIM}f", blob), dtype=np.float32)


def semantic_search(query, top_k=10, category=None, db_path=None):
    """Search documents by semantic similarity.

    Returns list of {path, score, chunk_text, category, modified, chunk_index}.
    """
    import numpy as np

    db = Path(db_path) if db_path else DB_PATH
    if not db.exists():
        return []

    conn = sqlite3.connect(str(db))
    try:
        count = conn.execute("SELECT COUNT(*) FROM doc_embeddings").fetchone()[0]
    except sqlite3.OperationalError:
        conn.close()
        return []

    if count == 0:
        conn.close()
        return []

    # Load model and embed query
    try:
        from fastembed import TextEmbedding
    except ImportError:
        print("ERROR: fastembed not installed. Run: pip install fastembed", file=sys.stderr)
        conn.close()
        return []

    model = TextEmbedding("BAAI/bge-small-en-v1.5")
    query_emb = list(model.embed([query]))[0]
    query_vec = np.array(query_emb, dtype=np.float32)

    # Load all embeddings
    sql = "SELECT path, embedding, chunk_text, category, modified, chunk_index FROM doc_embeddings"
    params = []
    if category:
        sql += " WHERE category = ?"
        params.append(category)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    if not rows:
        return []

    # Compute cosine similarity
    paths = []
    snippets = []
    categories = []
    modifieds = []
    chunk_indices = []
    embeddings = []

    for path, emb_blob, snippet, cat, mod, cidx in rows:
        paths.append(path)
        snippets.append(snippet)
        categories.append(cat)
        modifieds.append(mod)
        chunk_indices.append(cidx)
        embeddings.append(unpack_embedding(emb_blob))

    doc_matrix = np.vstack(embeddings)

    # Cosine similarity: dot(q, d) / (|q| * |d|)
    query_norm = np.linalg.norm(query_vec)
    doc_norms = np.linalg.norm(doc_matrix, axis=1)
    # Avoid division by zero
    doc_norms = np.where(doc_norms == 0, 1e-10, doc_norms)
    similarities = doc_matrix @ query_vec / (doc_norms * query_norm)

    # Rank by similarity
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        score = float(similarities[idx])
        if score <= 0:
            continue
        results.append({
            "path": paths[idx],
            "score": round(score, 4),
            "chunk_text": snippets[idx],
            "category": categories[idx],
            "modified": modifieds[idx],
            "chunk_index": chunk_indices[idx],
        })

    return results


def main():
    p = argparse.ArgumentParser(description="Semantic search over Mega-OS documents")
    p.add_argument("query", help="Natural language search query")
    p.add_argument("--top", type=int, default=10, help="Number of results")
    p.add_argument("--cat", "--category", dest="category",
                   choices=["history", "active", "archive", "business", "agents", "memory"])
    p.add_argument("--db", default=str(DB_PATH))
    args = p.parse_args()

    results = semantic_search(args.query, top_k=args.top, category=args.category,
                              db_path=args.db)

    if not results:
        print(f"No semantic results for: {args.query}")
        return

    print(f"Semantic search: \"{args.query}\" ({len(results)} results)\n")
    for i, r in enumerate(results, 1):
        snippet = r["chunk_text"].strip().replace("\n", " ")[:160]
        chunk_tag = f" [chunk {r['chunk_index']}]" if r["chunk_index"] > 0 else ""
        print(f"[{i}] {r['path']}{chunk_tag} (score: {r['score']}, {r['modified']}, {r['category']})")
        print(f"    {snippet}\n")
    print(f"--- {len(results)} result(s) ---")


if __name__ == "__main__":
    main()
