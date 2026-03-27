---
name: workflow-review
description: Use when analyzing personal workflow patterns and operational friction — reviews priority-execution alignment across active state, business operations, revenue, products, and decisions. Surfaces actionable process improvements.
invocation: /workflow-review
user_invocable: true
arguments: "--focus operations|revenue|products|all --no-coherence"
---

# Workflow Review

Examine personal workflow data — active state, business operations, revenue, products, timeline, and decisions — to surface actionable workflow and process improvements. Complements `/improvement-audit` (which scans system infrastructure) by focusing on **how the user works** rather than how the system is built.

> **Compatibility:** This skill is compatible with headless `claude -p` mode. It uses standalone Agent calls, not TeamCreate.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--focus` | `all` | Limit analysis scope: `operations`, `revenue`, `products`, or `all` |
| `--no-coherence` | false | Skip the Coherence+Parallax reading |

## Phase 0: Parse Arguments

Parse the invocation arguments:

1. **`--focus`**: Determines which exploration areas to dispatch in Phase 1.
   - `operations` → Areas 1, 2, 6, 7
   - `revenue` → Areas 1, 3, 4
   - `products` → Areas 1, 5, 6
   - `all` (default) → All 7 areas
2. **`--no-coherence`**: If set, skip Phase 4 entirely.

Print to console: `"Workflow Review: focus=[focus], coherence=[yes/no]"`

## Phase 1: Parallel Exploration

Dispatch standalone `Agent` calls with `subagent_type: "Explore"` for each area included by the `--focus` filter. **All Agent calls MUST be issued in a single tool-use response** so they execute in parallel.

Do NOT use TeamCreate or SendMessage. Use only the Agent tool.

| # | Area | Key Files | Looking For |
|---|------|-----------|-------------|
| 1 | Active State | `active/now.md`, `active/priorities.md`, `active/blockers.md`, `active/inbox.md` | Stale items (unchecked tasks >7 days), misaligned priorities (P1 items not in now.md Next Steps), recurring blockers, inbox backlog |
| 2 | Business Operations | `business/operating/recurring-processes.md`, `business/operating/sop-*.md` | Processes without SOPs, over-engineered processes, process gaps, missed schedules, automation opportunities |
| 3 | Revenue & Finance | `business/finance/*`, `business/strategy/revenue-top-10.md` | Revenue gaps vs target ($5-8k/mo), underperforming streams, cost creep, streams with no recent activity |
| 4 | Marketing & Growth | `business/marketing/*` | Stale campaigns, channel underutilization, adoption metric stalls, content calendar gaps |
| 5 | Product Progress | `products/*/` (check each product's README, spec, recent git activity) | Stalled features, scope creep, shipping velocity slowdown, products with no commits in 7+ days |
| 6 | Time & Focus | `active/now.md` "What's Done" section, `core/history/master-timeline.md` (last 14 days) | Context switching patterns, unfinished threads, velocity trends (completions per week), ratio of planned vs reactive work |
| 7 | Decision Patterns | `core/history/decisions.md` | Deferred decisions (>7 days pending), decision reversals, decisions missing rationale, decisions not reflected in active state |

### Explorer Prompt Template

Each Explorer receives:
- The area name, scope, and key files from the table above
- Depth target: 5-8 Grep/Glob searches + 3-5 full file reads
- Instruction to produce a structured report

### Explorer Report Format

```markdown
## Area: [Name]

### Key Observations
1. **[Observation]** — Impact: HIGH/MEDIUM/LOW
   - Evidence: [specific data from files — dates, counts, quotes]
   - Pattern: [what this suggests about workflow]

2. **[Observation]** ...

### Metrics (where applicable)
- [Relevant counts, ages, ratios, velocities]

### Friction Points
- [Specific points where workflow slows down or breaks]

### Confidence
- Coverage: HIGH / MEDIUM / LOW
- Gaps: [anything not examined]
```

## Phase 2: Cross-Area Pattern Analysis

After all Explorer agents return, analyze their combined findings for cross-cutting patterns. This is the core analytical step — done in the main context, not delegated.

Look for these specific pattern types:

### 1. Workflow Friction
Where does work stall between stages? Examples:
- Tasks complete but state files not updated
- Decisions made but not reflected in priorities
- Revenue actions planned but not executed

### 2. Execution Gaps
Where is there a gap between intention and action? Examples:
- P1 priorities with no matching Next Steps
- Recurring processes that consistently run late
- Products on the roadmap with no recent commits

### 3. Revenue Alignment
Is time being spent on revenue-generating work? Examples:
- Ratio of revenue-related completions vs system/maintenance work
- Revenue streams with plans but no execution
- Time spent on P3/P4 items while P1 revenue items are stalled

### 4. Decision Debt
Are decisions being deferred or reversed? Examples:
- Pending decisions older than 7 days
- Decisions reversed within 14 days
- Active work that depends on unresolved decisions

### 5. Operational Health
Are operational processes running smoothly? Examples:
- Process completion rates
- Automation coverage gaps
- Manual work that could be automated

## Phase 3: Recommendations

Synthesize cross-area patterns into 5-7 prioritized recommendations.

For each recommendation:
- **ID:** `WR-YYYY-MM-DD-N` (ephemeral, not persistent)
- **Title:** Short descriptive title
- **Observation:** What was found (with evidence from specific files/dates)
- **Pattern:** What workflow dynamic this reveals
- **Suggestion:** Concrete action to improve the workflow
- **Effort:** Quick (< 1 session) / Medium (1-2 sessions) / Large (3+ sessions)
- **Expected Impact:** What improves if this is addressed

Prioritize by: (1) revenue impact, (2) friction reduction, (3) operational health.

## Phase 4: Coherence + Parallax Reading

**Skip if `--no-coherence` flag is set.**

1. **Coherence** reads the full review (exploration findings + cross-area patterns + recommendations) and produces:
   - **Field coherence reading** — what pattern underlies the workflow dynamics?
   - **Unresolved polarity** — what core tension exists between how the user works and what they're trying to achieve?
   - **Blind spot signal** — what might the structured review have missed about workflow patterns?

2. **Parallax** translates Coherence output:
   - **Observation** — what Coherence sees
   - **Dynamic** — the force or tension at play
   - **Implication** — what this means operationally

## Phase 5: Archive Previous Report & Write Output

Before overwriting, preserve the existing report:

1. **Check** if `active/workflow-review.md` exists and has content.
2. **Read** the `Generated:` timestamp from the existing file.
3. **Extract** the date as `YYYY-MM-DD` from the timestamp.
4. **Compute** the ISO week: `YYYY-WNN`.
5. **Build** the archive path: `archive/reports/YYYY-WNN/YYYY-MM-DD-workflow-review.md`
   - If that path already exists (same-day re-run), append `-N` (e.g., `-2`, `-3`).
6. **Copy** the full content of `active/workflow-review.md` to the archive path.
7. **Update** `archive/index.json`:
   - Add the week key if it doesn't exist.
   - Append file metadata (filename, path, date, content_type: `workflow-review`, summary, token_estimate).
8. **Print** to console: `"Archived previous workflow-review (YYYY-MM-DD) to archive/reports/YYYY-WNN/"`
9. If the active file doesn't exist or is empty, skip archival silently.

**Shell shortcut:** `bash engineering/scripts/archive-report.sh workflow-review active/workflow-review.md`

Then write to `active/workflow-review.md` (overwritten each run).

### Output Format

```markdown
# Workflow Review

Generated: YYYY-MM-DD HH:MM
Focus: [focus scope]
Areas Analyzed: [count]
Recommendations: [count]

## Executive Summary

[3-5 sentences: overall workflow health, most significant patterns, top recommendation]

## Area Findings

### Active State
[Key observations, friction points, metrics]

### Business Operations
[Key observations, friction points, metrics]

### Revenue & Finance
[Key observations, friction points, metrics]

### Marketing & Growth
[Key observations, friction points, metrics]

### Product Progress
[Key observations, friction points, metrics]

### Time & Focus
[Key observations, friction points, metrics]

### Decision Patterns
[Key observations, friction points, metrics]

## Cross-Area Patterns

### Workflow Friction
[Where work stalls between stages]

### Execution Gaps
[Gaps between intention and action]

### Revenue Alignment
[Time allocation vs revenue priorities]

### Decision Debt
[Deferred or reversed decisions]

### Operational Health
[Process completion and automation coverage]

## Recommendations

### WR-YYYY-MM-DD-1: [Title]
- **Observation:** [what was found]
- **Pattern:** [what this reveals]
- **Suggestion:** [concrete action]
- **Effort:** Quick | Medium | Large
- **Expected Impact:** [what improves]

### WR-YYYY-MM-DD-2: [Title]
...

## Coherence Reading

### Field Coherence (Coherence)
[Pattern beneath the workflow dynamics]

### Unresolved Polarity (Coherence)
[Core tension between work style and goals]

### Blind Spot Signal (Coherence)
[What structured review may have missed]

### Operational Translation (Parallax)
[Observation -> Dynamic -> Implication]

---
*Generated by mega-os /workflow-review — [focus] scope, [N] areas analyzed*
```

### Console Report

Print:
- Focus scope, area count
- Executive summary
- Top 3 recommendations (title + effort + expected impact)
- Output file path
