# Lane Definitions & Plan Generation

> Referenced by: `.claude/skills/goodmorning/SKILL.md`

## Lane Extraction Rules

### Lane 1: Dream
- Read `active/dream-report.md`.
- Extract the blockquoted question (line starting with `>`).
- Display in a blockquote. If file is stale or missing, note "Dream did not run."

### Lane 2: Action Items (Daily Digest)
- Read `active/daily-digest.md`.
- Extract the Critical and Needs Review sections.
- List items numbered, preserving severity.
- If digest is stale, note "Daily scan has not run yet today."

### Lane 3: Improvement Audit
- Read `active/improvement-audit.md`.
- Extract: Focus area, finding counts (HIGH/MEDIUM/LOW), executive summary.
- List HIGH-severity findings with one-line descriptions.
- IMPORTANT: Never merge this lane with Workflow Review. They are always separate.

### Lane 4: News Intelligence
- Read `active/news-briefing.md`.
- Extract: total story count, HIGH-significance count.
- List top 5 HIGH-significance headlines with one-line summaries.

### Lane 5: System Health
- Read `active/freshstate-report.md` — extract stale count, violation count.
- Read `active/cron-health.md` — extract failure/warning counts.
- Read `business/marketing/adoption-metrics.md` — extract the last row from "Sigil Notary" section.
- Read `active/system-evaluation.md` if it exists — extract latest evaluation summary.
- Combine into a compact health dashboard.

### Lane 6: Content Pipeline
- Read `business/marketing/channel-tracker.md`.
- Extract today's scheduled content (by date in "Upcoming Content" section).
- List items with pipeline status: "drafted", "not started", "posted".
- Flag any items in "drafted" status that are >2 days old as "OVERDUE".

### Lane 7: Workflow Review (conditional)
- Only display this lane on Mondays or if `active/workflow-review.md` was updated today.
- Read `active/workflow-review.md`.
- Extract: focus area, key findings, action items.
- IMPORTANT: This is always a separate lane from the Improvement Audit.

## Suggested Plan Generation

Read `active/now.md` — extract all unchecked items (`- [ ]`).
Read `active/priorities.md` — understand P1/P2/P3 ranking.

Categorize unchecked items into:

### Part 1 — Fix (30 min)
Critical items from daily digest that can be resolved quickly.

### Part 2 — Review (20 min)
Items needing human judgment (needs-review items, improvement proposals).

### Part 3 — Create (flexible)
Scheduled creative/development work from now.md.

### Part 4 — Outreach (flexible)
Revenue-generating actions, contact follow-ups, and content posting.

- From `active/now.md`: extract cold calls, LinkedIn DMs, cold connection requests, community outreach.
- From `business/network/contacts.md`: pull rows where Follow-Up column <= today.
  - Show overdue first (sorted by days overdue descending), then due today.
  - Format: `[Platform]: Follow up with [Name] — [Next Action]`
  - Place after revenue outreach items, before content posting.
- From `business/marketing/channel-tracker.md`: for each platform with today's content in "drafted" or "content ready" status, add: "Post [topic] to [platform] (`draft-path`)"
  - Platforms to check: Twitter/X, TikTok, Dev.to, Reddit, LinkedIn, Discord, Substack, HN
- Order: revenue outreach first (calls, DMs), then contact follow-ups, then content posting by platform.

Prioritize P1 items and revenue-generating tasks.
