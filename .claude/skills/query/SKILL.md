---
name: query
description: Structured queries over active state, contacts, pipeline, and cross-references
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
| `<any term>` | Falls back to cross-reference mention search |

## Data Sources

- `core/indexes/cross-references.json` — entity mention index (rebuilt daily 9:24 AM)
- `business/network/contacts.json` — structured contact data with computed fields
- `business/sales/pipeline.json` — structured pipeline data
- `active/index.json` — file metadata with last-updated dates
- `active/priorities.md` — priority sections (read directly)
- `core/history/decisions.md` — decision log (read directly)

The query engine auto-regenerates stale JSON when the markdown source is newer.

## Notes

- Zero API cost — pure Python, no LLM calls
- Freshness guard: if JSON is stale vs markdown source, regenerates before querying
- Cross-reference index covers: contacts, products, agents, decisions, risks, improvements, audits
