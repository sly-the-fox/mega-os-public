---
name: daily-scan
description: Use when scanning active state files for stale, unactioned, or overdue items and producing a daily digest.
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

14. **Contact follow-up check** (`business/network/contacts.md`)
    - Parse the People and Businesses tables from `business/network/contacts.md`.
    - For each row, read the `Follow-Up` column.
    - Skip rows where Follow-Up is `—` or empty.
    - Compare the Follow-Up date to today:
      - Due today → **Informational**: "[Platform]: Follow up with [Name] — [Next Action]"
      - 1-2 days overdue → **Needs Review**: "[Name] follow-up overdue by N days — [Next Action]"
      - 3+ days overdue → **Critical**: "[Name] follow-up overdue by N days — [Next Action]"
    - Route overdue items to PM / Seller in the Action Plan.

15. **Outreach staleness check** (`active/now.md`)
    - Scan `active/now.md` for unchecked items (`- [ ]`) in sections containing keywords: "Outreach", "Cold Calls", "DMs", "LinkedIn", "Revenue", "Community", "Reddit".
    - For each unchecked item, check if it has been unchecked for >2 days by comparing the section header date or the file's last-modified date with today.
    - Items unchecked >2 days in outreach/revenue sections → **Critical**: "[item] unchecked for N days — revenue-generating action stalled."
    - This catches manual tasks that aren't tracked by any cron job.

16. **Content draft staleness check** (`business/marketing/channel-tracker.md`)
    - Scan `business/marketing/channel-tracker.md` for entries with pipeline status "drafted".
    - For each "drafted" entry, check the date in the section header.
    - Entries in "drafted" status for >2 days → **Needs Review**: "[channel] [date] content in 'drafted' for N days — needs posting or archiving."
    - This ensures drafted content doesn't sit indefinitely without being posted.

17. **History freshness check** (`core/history/current-state.md`)
    - Check file freshness: `git log -1 --format=%ai core/history/current-state.md`.
    - If file unchanged for 3+ days → **Needs Review**: "current-state.md is N days stale — run Historian Checklist to update."
    - Otherwise → skip (no output).

18. **Agent and doc consistency quick-check**
    - Run `bash engineering/scripts/check-index-integrity.sh` to detect agent/skill index drift.
    - If exit code is 1 (drift detected), include each warning line as a **Critical** item in the digest.
    - If exit code is 0 (clean), log as **Informational**: "Index integrity check passed."
    - This replaces manual counting — the script checks agents, skills, symlinks, and all index files.

19. **Archive previous digest**
    Before overwriting, preserve the existing digest:
    - Run `bash engineering/scripts/archive-report.sh daily-digest active/daily-digest.md`
    - This copies the current `active/daily-digest.md` to `archive/reports/YYYY-WNN/YYYY-MM-DD-daily-digest.md` and updates `archive/index.json`.
    - If the file doesn't exist or is empty, archival is skipped silently.

20. **Write digest**
    - Compile all findings into `active/daily-digest.md` using the template below.
    - Print a console summary: total items by severity, top 3 critical items.

21. **Propose solutions**
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
    | Outreach staleness | PM | Seller | Specific outreach actions + order of priority |
    | Contact follow-ups | PM | Seller | Follow-up action, updated cadence, next date |
    | Content draft staleness | Content-Strategist | PM | Post, revise, or archive decision |

    **How it works at runtime:**
    - For each item, spawn the appropriate research agent (Explore for codebase questions, or the domain specialist for domain questions) to gather context.
    - Then spawn a Plan agent with that context to propose a concrete solution.
    - Agents should run in parallel where items are independent.
    - Write solutions to the digest under a new `## Action Plan` section.
    - Print each item + solution to console.

22. **State sync — route critical findings to active state**
    After writing the digest, check if any Critical items need to be reflected in active state files:

    **Blockers:** If a Critical item represents a new blocker (stalled work, external dependency, access issue):
    - Check if it already exists in `active/blockers.md`
    - If not, add a row: `| [today] | [blocker description] | [owner] | Open | Surfaced by daily scan |`

    **Risks:** If a Critical item represents a new or escalating risk:
    - Check if it already exists in `active/risks.md` (match by description)
    - If new: add a row with severity, likelihood, and initial mitigation
    - If existing: update the mitigation field with new evidence and today's date

    **Rules:**
    - Only route Critical items, not Needs Review or Informational
    - Never duplicate — always check for existing entries first
    - Append `(auto-synced from daily scan YYYY-MM-DD)` to notes for traceability
    - Print synced items to console: `"State sync: added [N] blockers, updated [M] risks"`

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
| Stale current-state.md | 3 days | Needs Review |
| Contact follow-up due today | 0 days | Informational |
| Contact follow-up 1-2 days overdue | 1-2 days | Needs Review |
| Contact follow-up 3+ days overdue | 3 days | Critical |
| Unchecked outreach/revenue items | 2 days | Critical |
| Drafted content not posted | 2 days | Needs Review |

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
| Contacts | | | | |
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
