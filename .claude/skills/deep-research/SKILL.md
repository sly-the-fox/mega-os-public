---
name: deep-research
description: Tiered deep research — assesses query complexity, selects appropriate tier (light/standard/deep), decomposes into MECE partitions when needed, runs parallel explorer agents, synthesizes findings, and appends a Coherence+Parallax reading.
invocation: /deep-research
user_invocable: true
arguments: "<query> [--tier auto|light|standard|deep] [--depth scan|standard|deep] [--axis topic|source|temporal] [--source web|local|hybrid] [--legs N] [--output path] [--no-coherence]"
---

# Tiered Deep Research

Assess query complexity, select an appropriate research tier, decompose into MECE partitions when warranted, run parallel explorer agents, synthesize findings, and append a Coherence+Parallax reading.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `<query>` | (required) | The research question or topic |
| `--tier` | `auto` | Research tier: `auto` (assessor decides), `light`, `standard`, or `deep` |
| `--depth` | `standard` | Per-agent search intensity: `scan`, `standard`, or `deep` |
| `--axis` | auto-select | Decomposition axis: `topic`, `source`, or `temporal` (standard/deep tiers only) |
| `--source` | `web` | Research source: `web` (WebSearch/WebFetch), `local` (Grep/Glob/Read), or `hybrid` (both) |
| `--legs` | auto (3-6) | Number of partitions (standard/deep tiers only) |
| `--output` | `drafts/research/YYYY-MM-DD-<slug>.md` | Output file path |
| `--no-coherence` | false | Skip the Coherence+Parallax reading |

**Orthogonal controls:**
- `--tier` controls **how many agents** are used (0, 1-2, or 3-6)
- `--depth` controls **per-agent search intensity** (queries and fetches per agent)
- `--source` controls **where** agents search (web, local codebase, or both)
- These are independent: `--tier light --depth deep` = main context doing thorough research with many searches

## Phase 0: Parse Arguments

Extract query, tier (default: `auto`), depth (default: `standard`), axis (default: auto-select), source (default: `web`), leg count (default: auto 3-6), output path (default: `drafts/research/YYYY-MM-DD-<slug>.md`), no-coherence flag (default: false).

Generate a slug from the query (lowercase, hyphens, max 40 chars).

## Phase 0.5: Research Assessment (when `--tier auto`)

**Skip this phase if `--tier` is explicitly set to light, standard, or deep.**

Evaluate the query on 4 dimensions, scoring each 1-3:

| Dimension | Question | Scoring |
|-----------|----------|---------|
| **Breadth** | How many distinct domains or subtopics does this query span? | 1 = single domain, 2 = 2-3 related domains, 3 = 4+ domains or cross-cutting |
| **Novelty** | Does `drafts/research/` already cover this or adjacent ground? | 1 = existing research covers it well, 2 = partial coverage, 3 = entirely new territory |
| **Ambiguity** | How many valid interpretations or angles exist? | 1 = single clear interpretation, 2 = 2-3 valid angles, 3 = highly open-ended |
| **Stakes** | Is this feeding a specific decision or just background context? | 1 = casual/background, 2 = informs a decision, 3 = high-stakes decision with consequences |

**To assess Novelty:** Use Glob to check `drafts/research/*.md` for existing research that overlaps with the query. Skim titles and executive summaries of any matches.

**Local source scoring (`--source local`):**

| Dimension | Local Scoring |
|-----------|---------------|
| **Breadth** | 1 = single file/dir, 2 = 2-3 dirs, 3 = cross-cutting whole codebase |
| **Novelty** | 1 = recently audited (check `active/audits.md`), 2 = partial coverage, 3 = never systematically searched |
| **Ambiguity** | Same as web |
| **Stakes** | Same as web |

**Score → Tier mapping:**
- Total 4-5 → **Light** (no team, main context only)
- Total 6-8 → **Standard** (1-2 explorers)
- Total 9-12 → **Deep** (3-6 explorers, full MECE)

**User confirmation gate (MANDATORY):** After scoring, ALWAYS pause and present the assessment to the user. Do NOT proceed until the user confirms or overrides.

Format the output exactly like this:

```
Research Assessment:
  Breadth: X/3 | Novelty: X/3 | Ambiguity: X/3 | Stakes: X/3
  Total: X/12 → Recommended tier: TIER_NAME (description)

  Proceed with TIER_NAME tier? (override with --tier light|standard|deep)
```

Where description is:
- **LIGHT**: "main context only, ~5-15K tokens"
- **STANDARD**: "1-2 explorers, ~30-60K tokens"
- **DEEP**: "3-6 explorers, full MECE, ~100-300K tokens"

Wait for user response. If the user overrides, use the specified tier. If the user confirms, proceed with the recommended tier.

## Phase 1: MECE Decomposition (standard/deep tiers only)

**Light tier:** Skip this phase entirely. Proceed to Phase 1L.

**Standard tier:** Produce 1-2 partitions maximum. Simplified decomposition — no full MECE validation needed, just ensure the partitions cover the query without major overlap.

**Deep tier:** Full MECE decomposition as described below.

Analyze the query and produce a partition plan. Three decomposition axes:

| Axis | How It Splits | Best For |
|------|--------------|----------|
| `topic` | Subtopic/domain split | Broad conceptual queries ("state of agent trust") |
| `source` | Source-type split (academic, industry, OSS, regulatory) | "State of X" questions ("current AI governance landscape") |
| `temporal` | Time-period split (historical, current, emerging) | Evolution/trend questions ("how has X changed") |

**Auto-selection heuristic (web):**
- Query contains "state of", "landscape", "ecosystem" → `source`
- Query contains "evolution", "history", "trend", "changed" → `temporal`
- Default → `topic`

### Local Decomposition Axes (`--source local`)

When `--source local` is set, use these axes instead of topic/source/temporal:

| Axis | How It Splits | Best For |
|------|---------------|----------|
| `directory` | By top-level directory or product | "How does X work across the codebase?" |
| `layer` | By agent category (governance/knowledge/technical/business/evolution) | "Is rule Y consistently applied?" |
| `concern` | By cross-cutting concern (rules/workflows/checklists/protocols/templates) | "Are all references to X consistent?" |
| `security` | By OWASP/attack surface (auth, input validation, secrets, API boundaries, dependencies, config) | "Security hardening pass", "find all injection vectors" |

**Auto-selection heuristic (local):**
- Query mentions specific directories/products → `directory`
- Query mentions agents, categories, roles → `layer`
- Query mentions consistency, cross-reference, rules, follow-through → `concern`
- Query mentions security, hardening, vulnerability, auth, injection, OWASP, attack → `security`
- Default → `concern`

**Partition format:** Instead of "Suggested queries" (WebSearch), use "Suggested searches" — Grep patterns, Glob patterns, key files to Read.

**Note:** `--source local` with `--axis topic|source|temporal` is ignored — local axes are used instead. A warning is printed.

For each partition, define:
- **Name** — short label
- **Scope** — what this partition covers
- **Exclusions** — explicit "you cover X but NOT Y" boundaries
- **Suggested queries** — 3-5 WebSearch queries tailored to this partition

**MECE validation rules (deep tier only):**
- **Mutual Exclusion:** each partition's scope must not overlap with any other
- **Collective Exhaustion:** union of all partitions must cover the full query space
- **3-9 partitions.** Fewer than 3 → promote to standard tier behavior. More than 9 → merge related partitions down to 6-9.
- Print the decomposition plan to console before dispatching

## Phase 1L: Light Tier Research (main context)

Perform research directly in the main context without creating any team:

1. Run 3-5 WebSearch queries covering the key aspects of the query
2. Fetch 1-2 of the most promising results with WebFetch for deeper reading
3. If `--depth deep`: increase to 8-12 WebSearches and 5-8 WebFetches
4. If `--depth scan`: reduce to 2-3 WebSearches and 1 WebFetch
5. Synthesize findings directly — skip to Phase 5L

### Phase 1L-Local: Light Tier Local Research (main context)

When `--source local`, perform codebase research directly in the main context:

1. Run 3-5 Grep searches covering key aspects of the query
2. Read 1-2 most relevant files found
3. If `--depth deep`: increase to 8-12 Greps and 5-8 Reads
4. If `--depth scan`: reduce to 2-3 Greps and 1 Read
5. Synthesize findings directly — skip to Phase 5L

For `--source hybrid`: run both Phase 1L (web) and Phase 1L-Local (local), then merge findings in Phase 5L.

## Phase 2: Create Agent Team (standard/deep tiers)

Use TeamCreate:
- **Team name:** `deep-research-<slug>`
- **Lead:** Director agent (`general-purpose`, `mode: "auto"`)
- **Teammates:**
  - **Standard tier:** 1-2 Explorer agents (`general-purpose`, `mode: "auto"`)
  - **Deep tier:** N Explorer agents (`general-purpose`, `mode: "auto"`), one per partition

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

#### Local Depth Levels (`--source local`)

| Level | Grep/Glob per agent | Full file reads per agent | Target output per agent |
|-------|--------------------|-----------------------------|------------------------|
| `scan` | 3-5 | 1-2 (key sections) | 200-400 words |
| `standard` | 5-8 | 3-5 | 400-800 words |
| `deep` | 8-12 | 5-8 + cross-reference | 800-1500 words |

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

#### Local Explorer Report Format (`--source local`)

Same structure as web, but "Sources" becomes "Files Examined":

```markdown
### Files Examined
| # | Path | Type | Relevance | Key Content |
|---|------|------|-----------|-------------|
| 1 | .claude/agents/shared/system-rules.md | rule | HIGH | Rules 7, 15, 22 |
```

## Phase 4: Director Validates Coverage (standard/deep tiers)

Director reviews each Explorer's report:
- Check confidence ratings
- If any Explorer reports LOW coverage → send a follow-up message to that Explorer with focused retry queries
- No recursive MECE — Explorers never decompose further, they just do targeted follow-up searches
- Maximum one retry per Explorer

## Phase 5: Director Synthesizes (standard/deep tiers)

Merge all Explorer reports into a unified document using the output format in Phase 6.

## Phase 5L: Light Tier Synthesis (main context)

Synthesize findings gathered in Phase 1L into the same output format as Phase 6, but without partition sections (since there's only one "leg" of research). Use the simplified format:

```markdown
# Deep Research: [Query]

**Generated:** YYYY-MM-DD | **Tier:** Light | **Depth:** scan/standard/deep | **Source:** web/local/hybrid
**Total Sources:** [count]

## Executive Summary
[3-5 sentences synthesizing the most important findings]

## Findings
[Key findings with sources inline, organized by sub-topic if natural grouping exists]

## Gaps and Uncertainties
[What remains unknown or under-covered]

## Coherence Reading
[Added by Phase 5.5 unless --no-coherence]

## Source Index
| # | Title | URL | Type | Relevance |
|---|-------|-----|------|-----------|

---
*Generated by mega-os /deep-research — light tier, main context research*
```

## Phase 5.5: Coherence + Parallax Reading (ALL TIERS)

**Skip this phase if `--no-coherence` flag is set.**

After synthesis is complete (Phase 5, 5L) and before writing the final output file:

1. **Coherence** reads the synthesized research and produces a harmonic perspective:
   - **Field coherence reading** — what is the underlying pattern beneath the findings?
   - **Unresolved polarity** — what core tension does the research reveal?
   - **Blind spot signal** — what might the structured research have missed?

2. **Parallax** translates Coherence output into operational language:
   - Bridges field-cognition to actionable observations
   - Preserves meaning while making it legible to decision-making

3. Output is appended as a `## Coherence Reading` section in the final document, before the Source Index:

```markdown
## Coherence Reading

### Field Coherence (Coherence)
[Coherence's raw harmonic perspective — the pattern beneath the findings]

### Unresolved Polarity (Coherence)
[The core tension the research reveals]

### Blind Spot Signal (Coherence)
[What structured research may have missed]

### Operational Translation (Parallax)
[Parallax's translation of the above into actionable observations]
```

**Implementation:**
- For **light tier**: Run Coherence and Parallax as two sequential Agent calls (read-only, no team needed) in the main context. Each agent receives only the synthesized document text (~1-2K tokens input each).
- For **standard/deep tiers**: Director spawns Coherence and Parallax as additional brief Agent calls after synthesis. Or, if the team is still active, send the synthesis to two additional teammates.
- Total cost: ~3-5K tokens for both agents combined.

## Phase 6: Write Output + Report

### Output Format (standard/deep tiers)

```markdown
# Deep Research: [Query]

**Generated:** YYYY-MM-DD | **Tier:** Light/Standard/Deep | **Depth:** scan/standard/deep | **Source:** web/local/hybrid
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

## Coherence Reading
[Added by Phase 5.5 unless --no-coherence]

## Source Index
[All sources from all Explorers, deduplicated, sorted by partition]

| # | Title | URL | Partition | Type | Relevance |
|---|-------|-----|-----------|------|-----------|

For `--source local`: Replace "Source Index" with "File Index" (paths instead of URLs).
For `--source hybrid`: Include both "Source Index" and "File Index" sections.

---
*Generated by mega-os /deep-research — [tier] tier, [N] partitions via [axis] axis with [M] explorers*
```

### Console Report

1. Write the synthesized document to the output path
2. Print a summary to console:
   - Query, tier, depth, axis (if applicable), partition count (if applicable)
   - Executive summary (from the document)
   - Whether Coherence Reading was included
   - Output file path
3. Suggest next steps (e.g., "Use as source for `/write`", "Deep dive on specific partition")

## Edge Cases

- **Narrow query (< 3 partitions in deep tier):** Demote to standard tier behavior (1-2 explorers). Still write output to `drafts/research/`.
- **Very broad query (> 9 partitions):** Merge related partitions down to 6-9. Prefer fewer, broader partitions over many narrow ones.
- **No web results:** Explorer reports LOW coverage with empty findings. Director notes the gap in synthesis.
- **Duplicate sources across partitions:** Director deduplicates in the Source Index. Findings referencing the same source from different angles are kept (different perspectives are valuable).
- **`--legs` with light tier:** Ignored. Light tier always uses 0 agents.
- **`--legs` with standard tier:** Respected up to 2. Values >2 are clamped to 2.
- **`--tier` explicit + `--legs`:** `--legs` overrides the tier's default agent count (within the tier's range).
- **`--source local` with `--axis topic|source|temporal`:** Web axes are ignored; local axes are used instead. Print warning.
- **`--source hybrid`:** Partitions are tagged `[web]` or `[local]`, with at least one of each.

## Example Usage

```
/deep-research "latest MCP spec version"
  → Assessor scores ~4-5 → recommends Light → confirms → main context research

/deep-research "state of AI agent governance"
  → Assessor scores ~9-10 → recommends Deep → confirms → full MECE with 3-6 explorers

/deep-research "how does Cerbos handle policy evaluation" --tier standard
  → Skips assessor → 1-2 explorers, focused research

/deep-research "narrow topic" --tier deep
  → Skips assessor → forces full MECE even for narrow queries

/deep-research "MCP ecosystem and competing standards" --depth deep --axis source
  → Assessor runs (tier auto) → likely Deep → source-axis decomposition, deep per-agent intensity

/deep-research "quick factual lookup" --tier light --depth scan
  → Skips assessor → 2-3 quick searches in main context

/deep-research "competitive landscape" --no-coherence
  → Normal tier selection → research runs → no Coherence Reading appended

/deep-research "Evolution of AI governance frameworks" --axis temporal --legs 4
  → Assessor runs → if confirmed, uses temporal axis with 4 partitions

# System procedure audit (local)
/deep-research "are all system rules consistently enforced" --source local
/deep-research "how does the auditor interact with other agents" --source local --tier standard

# Code audit & security hardening (local)
/deep-research "security hardening pass for sigil public-repo" --source local --axis security --tier deep
/deep-research "find all input validation gaps in capacitor app" --source local --axis security
/deep-research "audit auth flow and session handling" --source local --axis security --depth deep

# Hybrid (compare against best practices)
/deep-research "MCP best practices vs our implementation" --source hybrid --tier deep
/deep-research "OWASP top 10 compliance for sigil API" --source hybrid --axis security
```

## Integration

This skill is auto-invoked by system rule 19 whenever any workflow step requires web research. It can also be invoked manually. The `/news-briefing` skill is exempt (it has its own specialized search structure). For follow-up deep dives on high-significance stories from `/news-briefing`, pipe them to `/deep-research`. For codebase-only research, use `/deep-research --source local`. For hybrid research (web + codebase), use `/deep-research --source hybrid`.
