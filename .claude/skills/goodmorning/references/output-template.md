# Output Template

> Referenced by: `.claude/skills/goodmorning/SKILL.md`

Use this format for the morning briefing. Each lane is its own `###` section with a `---` separator. Do NOT combine lanes. Do NOT skip lanes that have data. If a lane has no data (file missing or stale), show the lane header with a note.

```markdown
## Good Morning — YYYY-MM-DD (Day of Week)

### What Ran Today
✓ Dream (5:30 AM) ✓ Improvement Audit (7:30 AM) ✓ News Briefing (8:45 AM)
✓ Daily Scan (9:10 AM) ✓ Freshstate (9:17 AM) ✗ Content Gen (FAILED)

---

### Lane 1: Dream
> [The question]

---

### Lane 2: Action Items
**Critical (N)**
1. [item — source file, age]
2. ...

**Needs Review (N)**
3. [item — source file, age]
...

---

### Lane 3: Improvement Audit
Focus: [area] ([day] rotation)
Findings: N HIGH / N MEDIUM / N LOW
Theme: [executive summary one-liner]

HIGH findings:
- [finding 1]
- [finding 2]
...

---

### Lane 4: News Intelligence
Stories: N total, N HIGH significance
- [headline 1]
- [headline 2]
- [headline 3]
- [headline 4]
- [headline 5]

---

### Lane 5: System Health
- Freshstate: N files checked, N stale, N violations
- Cron Health: N failures, N warnings
- Sigil: ~N downloads, N stars

---

### Lane 6: Content Pipeline
Today's schedule: [channels]
Drafted: [list]
Overdue (>2 days in drafted): [list or "none"]

---

### Lane 7: Workflow Review (if applicable)
[findings and action items]

---

### Suggested Plan

**Part 1 — Fix (30 min)**
- [ ] [critical item 1]
- [ ] [critical item 2]

**Part 2 — Review (20 min)**
- [ ] [review item 1]
- [ ] [review item 2]

**Part 3 — Create (flexible)**
- [ ] [development/content task]

**Part 4 — Outreach (flexible)**
- [ ] [cold call / DM / connection request]
- [ ] [Platform]: Follow up with [Name] — [next action]
- [ ] Post [topic] to Twitter/X (`drafts/social/...`)
- [ ] Post [topic] to Dev.to (`drafts/social/...`)
- [ ] Post [topic] to Reddit (`drafts/social/...`)
```
