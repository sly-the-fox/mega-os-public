---
name: query
description: Structured queries over active state, contacts, pipeline, cross-references, full-text search, semantic search, and context ranking
invocation: /query
user_invocable: true
arguments: "<query string>"
---

# /query — Structured Data Query

Run structured queries over Mega-OS indexes without manual file reading.

## Usage

```
/query what mentions Jeff Toffoli
/query overdue follow-ups
/query pipeline at Discovery
/query stale files
/query stale files 3
/query P1 priorities
/query pending decisions
/query sigil
/query search revenue tracker
/query search revenue --cat active
/query semantic how does agent routing work
/query semantic networking event --cat business
/query context revenue forecasting
/query context update the sales pipeline --budget 20000
```

## How It Works

1. Run the query engine:
   ```bash
   python3 engineering/scripts/query-engine.py "<query>"
   ```

2. Present the results to the user.

3. If the query returns no results, suggest alternative queries from the list above.

## Query Types

| Query Pattern | What It Does |
|---------------|-------------|
| `what mentions <entity>` | Cross-reference lookup — shows every file that mentions the entity |
| `overdue follow-ups` | Contacts with past-due follow-up dates, plus due-today and due-this-week |
| `pipeline` / `pipeline at <stage>` | Sales pipeline filtered by stage (Interested, Discovery, Proposal, etc.) |
| `stale files` / `stale files <N>` | Active state files not updated in N+ days (default: 7) |
| `P1 priorities` / `P2 priorities` | Extract priority section from priorities.md |
| `pending decisions` | Unresolved decisions from core/history/decisions.md |
| `search <query>` | FTS5 full-text keyword search across all indexed documents |
| `search <query> --cat <category>` | FTS5 search filtered by category (history, active, archive, business, agents) |
| `semantic <query>` | Embedding-based semantic similarity search — finds conceptually related content even without exact keyword matches |
| `semantic <query> --cat <category>` | Semantic search filtered by category |
| `context <query>` | Ranks all indexed files by relevance to the query, with token budget allocation — recommends which files to load |
| `context <query> --budget <N>` | Context ranking with custom token budget (default: 15000) |
| `<any term>` | Falls back to cross-reference mention search |

## Fallback Chain

When a query doesn't match a specific handler, the engine tries in order:
1. **Exact pattern match** (overdue, pipeline, stale, priorities, decisions)
2. **Cross-reference mention search** (entity lookup)
3. For explicit `search` / `semantic` / `context` prefixes, the appropriate engine is invoked directly

## Search Types Compared

| Type | How It Works | Best For |
|------|-------------|----------|
| `search` (FTS5) | BM25 keyword matching with Porter stemming | "Find files containing this term" |
| `semantic` (Embeddings) | Cosine similarity on BAAI/bge-small-en-v1.5 vectors | "Find files about this concept" (no exact keyword needed) |
| `context` (Hybrid) | 0.4 * FTS5 + 0.6 * semantic, with token budget | "What should I load for this topic?" |

## Data Sources

- `core/indexes/cross-references.json` — entity mention index (rebuilt daily 9:24 AM)
- `business/network/contacts.json` — structured contact data with computed fields
- `business/sales/pipeline.json` — structured pipeline data
- `active/index.json` — file metadata with last-updated dates and token estimates
- `active/priorities.md` — priority sections (read directly)
- `core/history/decisions.md` — decision log (read directly)
- `engineering/memory.db` — FTS5 full-text index (rebuilt daily 1:45 AM)
- `engineering/memory.db` — embedding vectors (rebuilt daily 2:03 AM)

The query engine auto-regenerates stale JSON when the markdown source is newer.

## Notes

- Zero API cost — pure Python, no LLM calls
- FTS5 and embedding indexes live in the same SQLite database (`engineering/memory.db`)
- Semantic search requires `fastembed` (`pip install fastembed`) — gracefully degrades if not installed
- Embedding model (BAAI/bge-small-en-v1.5) runs locally on CPU, ~33MB cached in `~/.cache/fastembed/`
- Freshness guard: if JSON is stale vs markdown source, regenerates before querying
- Cross-reference index covers: contacts, products, agents, decisions, risks, improvements, audits
