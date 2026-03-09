---
name: daily-scan
description: Scan all active state files for stale, unactioned, or overdue items and produce a daily digest.
invocation: /daily-scan
user_invocable: true
---

# Daily Scan

Scan all passive agent outputs and active state files for items needing attention. Produce a prioritized digest at `active/daily-digest.md`.

## Steps

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

8. **Scan decisions** (`core/history/decisions.md`)
   - Find pending decisions (Status = Pending or TBD).
   - Pending longer than 7 days → **Needs Review**.
   - Others → **Informational**.

9. **Scan focus** (`active/now.md`)
   - Count unchecked Next Steps (`- [ ]`).
   - Check file freshness: `git log -1 --format=%ai active/now.md`.
   - If file unchanged for 7+ days → **Needs Review** (focus may be stale).
   - Otherwise → **Informational** (list unchecked count).

10. **Agent structure quick-check**
    - Count agent files in `.claude/agents/` subdirectories (governance/, knowledge/, technical/, business/, evolution/) vs count in REGISTRY.md. Flag if counts differ.
    - Count symlinks at `.claude/agents/*.md` (top level) vs agent files in subdirectories. Flag if mismatched.
    - This is a fast count-only check. Full integrity analysis runs in weekly review.

11. **Write digest**
    - Compile all findings into `active/daily-digest.md` using the template below.
    - Print a console summary: total items by severity, top 3 critical items.

12. **Propose solutions**
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
| Agent count mismatch | 0 tolerance | Critical |

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
