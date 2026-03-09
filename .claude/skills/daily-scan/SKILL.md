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

10. **Write digest**
    - Compile all findings into `active/daily-digest.md` using the template below.
    - Print a console summary: total items by severity, top 3 critical items.

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
```
