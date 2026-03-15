---
name: daily-scan
description: Scan all active state files for stale, unactioned, or overdue items and produce a daily digest.
invocation: /daily-scan
user_invocable: true
---

# Daily Scan

Scan all passive agent outputs and active state files for items needing attention. Produce a prioritized digest at `active/daily-digest.md`.

## Steps

**Scope:** Only scan `active/` state files. Never scan `archive/` — archived content is frozen.

1. **Scan inbox** (`active/inbox.md`)
   - Find items not marked Routed or Closed.
   - Items older than 2 days → **Critical**.
   - Others → **Needs Review**.

2. **Scan blockers** (`active/blockers.md`)
   - Find items with Status = Open.
   - Items older than 5 days → **Critical**.
   - Others → **Needs Review**.

3. **Scan risks** (`active/risks.md`)
   - Find risks with Status = Open.
   - Risks older than 7 days with no mitigation update → **Needs Review**.
   - Others → **Informational**.

4. **Scan improvements** (`active/improvements.md`)
   - Find items with status "proposed" or "approved".
   - Items older than 14 days → **Needs Review**.
   - Others → **Informational**.

5. **Scan evaluations** (`core/history/evaluations.md`)
   - Find recommendations not yet acted on.
   - Recommendations older than 14 days → **Needs Review**.
   - Others → **Informational**.

6. **Scan audits** (`active/audits.md`)
   - Find findings with Status = Open.
   - Critical/High severity older than 7 days → **Critical**.
   - Medium/Low severity older than 7 days → **Needs Review**.
   - Others → **Informational**.

7. **Scan processes** (`business/operating/recurring-processes.md`)
   - Check "Next Due" column against today's date.
   - Overdue (Next Due < today) → **Critical**.
   - Due today → **Needs Review**.

8. **Auto-sync process registry** (`business/operating/recurring-processes.md`)
   - For each process in the registry, check for evidence that it ran:
     - Check cron log output via `cron list` for matching skill invocations.
     - Check output file timestamps (e.g., `active/daily-digest.md`, `active/news-briefing.md`, `active/freshstate-report.md`, `active/improvement-audit.md`).
     - Check `git log --since="yesterday" --format="%ai %s"` for commits referencing the process.
   - If evidence found and Last Run is stale, update Last Run to the detected timestamp.
   - Recalculate Next Due based on the process frequency and updated Last Run.
   - Log any auto-corrections as **Informational** in the digest: "Auto-synced [process] Last Run to [date]."

9. **Scan decisions** (`core/history/decisions.md`)
   - Find pending decisions (Status = Pending or TBD).
   - Pending longer than 7 days → **Needs Review**.
   - Others → **Informational**.

10. **Recent decisions (24h)** (`core/history/decisions.md`)
    - Find decisions accepted or resolved in the last 24 hours (compare date column to today/yesterday).
    - For each recent decision, surface as **Informational**: "DEC-XXX: [title] — accepted [date]."
    - This keeps the daily digest aware of recent direction changes without requiring manual cross-referencing.

11. **Scan focus** (`active/now.md`)
   - Count unchecked Next Steps (`- [ ]`).
   - Check file freshness: `git log -1 --format=%ai active/now.md`.
   - If file unchanged for 7+ days → **Needs Review** (focus may be stale).
   - Otherwise → **Informational** (list unchecked count).

12. **Incorporate improvement audit** (`active/improvement-audit.md`)
    - Check if file exists and was generated today (compare `Generated:` date).
    - If today's audit exists:
      - Read the Executive Summary and Improvement Proposals sections.
      - Count proposals by severity (High, Medium, Low).
      - High-severity proposals -> **Critical** (promote to Action Plan with concrete next steps).
      - Medium-severity proposals -> **Needs Review**.
      - Low-severity proposals -> **Informational**.
      - Include the focus area name and executive summary in the digest.
    - If file is missing or stale (not today's date):
      - Log as **Informational**: "No improvement audit available for today."
    - Do NOT modify `active/improvement-audit.md` — read-only input.
    - Do NOT auto-promote IA- items to `active/improvements.md` — requires user review.

13. **Workflow review staleness check** (`active/workflow-review.md`)
    - Only check on Mondays (detect day of week).
    - If it's Monday:
      - Check if file exists and read the `Generated:` date.
      - If file is missing or >7 days old → **Needs Review**: "Workflow review is stale — run `/workflow-review` before next weekly review."
      - Otherwise → skip (no output).
    - If not Monday → skip entirely.

14. **Agent and doc consistency quick-check**
    - Count agent files in `.claude/agents/` subdirectories (governance/, knowledge/, technical/, business/, evolution/) vs count in REGISTRY.md. Flag if counts differ.
    - Count symlinks at `.claude/agents/*.md` (top level) vs agent files in subdirectories. Flag if mismatched.
    - Count agents referenced in README.md, AGENTS.md, CLAUDE.md. Flag if any differ from actual count.
    - Count skills listed in README.md vs actual `.claude/skills/` directories. Flag mismatches.
    - This is a fast count-only check. Full integrity analysis runs in weekly review.

15. **Archive previous digest**
    Before overwriting, preserve the existing digest:
    - Run `bash engineering/scripts/archive-report.sh daily-digest active/daily-digest.md`
    - This copies the current `active/daily-digest.md` to `archive/reports/YYYY-WNN/YYYY-MM-DD-daily-digest.md` and updates `archive/index.json`.
    - If the file doesn't exist or is empty, archival is skipped silently.

16. **Write digest**
    - Compile all findings into `active/daily-digest.md` using the template below.
    - Print a console summary: total items by severity, top 3 critical items.

17. **Propose solutions**
    For each item surfaced in the digest (Critical, Needs Review, and Informational), propose a concrete next action. Use the agent routing table below to determine which agent(s) should research and plan the solution:

    | Item Source | Research Agent | Planning Agent | What to Propose |
    |-------------|---------------|----------------|-----------------|
    | Inbox (unrouted) | Router | Planner | Route destination + first action |
    | Blockers | Explore (codebase context) | Planner | Resolution steps, owner, timeline |
    | Risks | Sentinel | Strategist | Updated mitigation or escalation path |
    | Improvements | Improver | Planner | Implementation steps or rejection rationale |
    | Evaluations | Evaluator | Planner | Follow-up action to address recommendation |
    | Audits | Auditor | Planner | Remediation steps, assigned specialist |
    | Processes | Operator | PM | Schedule fix or SOP creation |
    | Decisions | Explore (context) | Planner | Decision path: what info is needed, who decides |
    | Focus | PM | Planner | Priority sequencing of unchecked items |
    | Improvement audit | Auditor | Improver | Verify finding, propose implementation |
| Agent structure | Improver | Planner | Remediation steps for structural fixes |

    **How it works at runtime:**
    - For each item, spawn the appropriate research agent (Explore for codebase questions, or the domain specialist for domain questions) to gather context.
    - Then spawn a Plan agent with that context to propose a concrete solution.
    - Agents should run in parallel where items are independent.
    - Write solutions to the digest under a new `## Action Plan` section.
    - Print each item + solution to console.

## Staleness Thresholds

| Item | Threshold | Severity |
|------|-----------|----------|
| Unrouted inbox | 2 days | Critical |
| Open blockers | 5 days | Critical |
| Open risks (no progress) | 7 days | Needs Review |
| Stale improvements | 14 days | Needs Review |
| Unacted evaluator recs | 14 days | Needs Review |
| Open audit findings (High+) | 7 days | Critical |
| Overdue processes | 1 day past due | Critical |
| Pending decisions | 7 days | Needs Review |
| Stale now.md focus | 7 days | Needs Review |
| Missing improvement audit | 0 tolerance | Informational |
| Agent count mismatch | 0 tolerance | Critical |
| Stale workflow review (Mon only) | 7 days | Needs Review |

## Output Template

Write the following to `active/daily-digest.md`:

```markdown
# Daily Digest

Generated: YYYY-MM-DD HH:MM

## Action Required

### Critical
(items needing same-day action — list each with source file and age)

### Needs Review
(items needing action this week — list each with source file and age)

### Informational
(awareness only — counts and brief notes)

## Summary

| Source | Total | Critical | Review | Info |
|--------|-------|----------|--------|------|
| Inbox | | | | |
| Blockers | | | | |
| Risks | | | | |
| Improvements | | | | |
| Evaluations | | | | |
| Audits | | | | |
| Processes | | | | |
| Decisions | | | | |
| Focus | | | | |
| Improvement Audit | | | | |
| **Total** | | | | |

## Action Plan

### 1. [Item title from scan]
- **Source:** `active/file.md`
- **Severity:** Critical / Needs Review / Informational
- **Assigned:** [Agent name(s)]
- **Proposed Solution:** [Concrete next steps]
- **Effort:** Quick (< 1 session) / Medium (1-2 sessions) / Large (3+ sessions)

### 2. [Next item...]
...
```
