---
name: deep-research
description: MECE deep research — creates an agent team that decomposes a query into mutually exclusive, collectively exhaustive partitions, runs parallel deep-dive explorer agents, and synthesizes findings. Auto-invoked by any workflow step requiring web research.
invocation: /deep-research
user_invocable: true
arguments: "<query> [--depth scan|standard|deep] [--axis topic|source|temporal] [--legs N] [--output path]"
---

# MECE Deep Research

Decompose a research query into mutually exclusive, collectively exhaustive partitions. Spawn parallel explorer agents for deep-dive research on each partition. Synthesize into a unified research document.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `<query>` | (required) | The research question or topic |
| `--depth` | `standard` | Research depth: `scan`, `standard`, or `deep` |
| `--axis` | auto-select | Decomposition axis: `topic`, `source`, or `temporal` |
| `--legs` | auto (3-6) | Number of partitions |
| `--output` | `drafts/research/YYYY-MM-DD-<slug>.md` | Output file path |

## Phase 0: Parse Arguments

Extract query, depth (default: `standard`), axis (default: auto-select based on query type), leg count (default: auto 3-6), output path (default: `drafts/research/YYYY-MM-DD-<slug>.md`).

Generate a slug from the query (lowercase, hyphens, max 40 chars).

## Phase 1: MECE Decomposition (main context, before team creation)

Analyze the query and produce a partition plan. Three decomposition axes:

| Axis | How It Splits | Best For |
|------|--------------|----------|
| `topic` | Subtopic/domain split | Broad conceptual queries ("state of agent trust") |
| `source` | Source-type split (academic, industry, OSS, regulatory) | "State of X" questions ("current AI governance landscape") |
| `temporal` | Time-period split (historical, current, emerging) | Evolution/trend questions ("how has X changed") |

**Auto-selection heuristic:**
- Query contains "state of", "landscape", "ecosystem" → `source`
- Query contains "evolution", "history", "trend", "changed" → `temporal`
- Default → `topic`

For each partition, define:
- **Name** — short label
- **Scope** — what this partition covers
- **Exclusions** — explicit "you cover X but NOT Y" boundaries
- **Suggested queries** — 3-5 WebSearch queries tailored to this partition

**MECE validation rules:**
- **Mutual Exclusion:** each partition's scope must not overlap with any other
- **Collective Exhaustion:** union of all partitions must cover the full query space
- **3-9 partitions.** Fewer than 3 → skip MECE, do direct single-agent research. More than 9 → merge related partitions down to 6-9.
- Print the decomposition plan to console before dispatching

## Phase 2: Create Agent Team

Use TeamCreate:
- **Team name:** `deep-research-<slug>`
- **Lead:** Director agent (`general-purpose`, `mode: "auto"`)
- **Teammates:** N Explorer agents (`general-purpose`, `mode: "auto"`), one per partition

## Phase 3: Director Dispatches to Explorers

Director sends each Explorer their assignment via SendMessage:
- The original query (for context)
- Their specific partition (name, scope, exclusions)
- Depth instructions (see table below)
- Output format specification (see Explorer Report Format below)

All Explorers work in parallel.

### Depth Levels

| Level | WebSearch queries per agent | WebFetch deep reads per agent | Target output per agent |
|-------|---------------------------|------------------------------|------------------------|
| `scan` | 3-5 | 1-2 | 200-400 words |
| `standard` | 5-8 | 3-5 | 400-800 words |
| `deep` | 8-12 | 5-8 | 800-1500 words |

### Explorer Report Format (sent back via SendMessage)

Each Explorer reports findings using this format:

```markdown
## Research Leg: [Partition Name]

### Scope
What was researched and explicit boundaries.

### Key Findings
1. **[Finding]** — [Source] ([URL])
   [2-4 sentence summary with specific data points, numbers, dates]

2. **[Finding]** — [Source] ([URL])
   [2-4 sentence summary]

### Confidence
- Coverage: HIGH / MEDIUM / LOW
- Source Quality: HIGH / MEDIUM / LOW
- Gaps: [anything not found or insufficiently covered]

### Sources
| # | Title | URL | Type | Relevance |
|---|-------|-----|------|-----------|
| 1 | ... | ... | academic/industry/news/OSS/gov | HIGH/MED/LOW |
```

## Phase 4: Director Validates Coverage

Director reviews each Explorer's report:
- Check confidence ratings
- If any Explorer reports LOW coverage → send a follow-up message to that Explorer with focused retry queries
- No recursive MECE — Explorers never decompose further, they just do targeted follow-up searches
- Maximum one retry per Explorer

## Phase 5: Director Synthesizes

Merge all Explorer reports into a unified document:

```markdown
# Deep Research: [Query]

**Generated:** YYYY-MM-DD | **Depth:** scan/standard/deep
**Decomposition:** [N] partitions ([axis] axis) | **Total Sources:** [count]

## Executive Summary
[3-5 sentences synthesizing the most important findings across all partitions]

## Findings by Partition

### [Partition 1 Name]
[Synthesized from Explorer 1's report — key findings with sources inline]

### [Partition 2 Name]
[Synthesized from Explorer 2's report]

...

## Cross-Cutting Themes
[Patterns, connections, or tensions that appear across multiple partitions]

## Gaps and Uncertainties
[What remains unknown, under-covered, or contradictory across sources]

## Source Index
[All sources from all Explorers, deduplicated, sorted by partition]

| # | Title | URL | Partition | Type | Relevance |
|---|-------|-----|-----------|------|-----------|

---
*Generated by mega-os /deep-research — MECE decomposition with [N] parallel explorers*
```

## Phase 6: Write Output + Report

1. Director writes the synthesized document to the output path (default: `drafts/research/YYYY-MM-DD-<slug>.md`)
2. Main context prints a summary to console:
   - Query, depth, axis, partition count
   - Executive summary (from the document)
   - Output file path
3. Suggest next steps (e.g., "Use as source for `/write`", "Deep dive on specific partition")

## Edge Cases

- **Narrow query (< 3 partitions):** Skip MECE. Do direct single-agent deep research using the `deep` depth level. Still write output to `drafts/research/`.
- **Very broad query (> 9 partitions):** Merge related partitions down to 6-9. Prefer fewer, broader partitions over many narrow ones.
- **No web results:** Explorer reports LOW coverage with empty findings. Director notes the gap in synthesis.
- **Duplicate sources across partitions:** Director deduplicates in the Source Index. Findings referencing the same source from different angles are kept (different perspectives are valuable).

## Example Usage

```
/deep-research "Current state of AI agent trust infrastructure"
/deep-research "MCP ecosystem and competing standards" --depth deep --axis source
/deep-research "Evolution of AI governance frameworks" --axis temporal --legs 4
/deep-research "Competitive landscape for cryptographic audit trails" --output drafts/research/competitive-audit-trails.md
```

## Integration

This skill is auto-invoked by system rule 19 whenever any workflow step requires web research. It can also be invoked manually. The `/news-briefing` skill is exempt (it has its own specialized search structure). For follow-up deep dives on high-significance stories from `/news-briefing`, pipe them to `/deep-research`.
