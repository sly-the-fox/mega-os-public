# Workspace Templates

> Referenced by: `.claude/skills/setup/SKILL.md` — Phase 3

---

Using the answers from Phase 2, build out the full workspace:

## 3a — Active State

1. **`active/now.md`** — Remove the `MEGA-OS:UNCONFIGURED` marker. Set the current focus based on stated projects/goals. Use this format:
   ```markdown
   # Current Focus

   ## Active Work
   **[Project name]** — [one-line description from their answer]

   ## Key Context
   - Tech stack: [from Phase 2]
   - Working style: [from Phase 2]

   ## Next Steps
   - [ ] Complete setup (Phase 4+)
   - [ ] [First actionable step for their project]
   - [ ] [Second actionable step]
   ```

2. **`active/priorities.md`** — Populate from their projects/goals:
   ```markdown
   # Priorities

   ## P1 — Critical
   - [Their primary project/goal]

   ## P2 — High
   - [Their secondary project/goal, if any]

   ## P3 — Medium
   - System customization (standards, agents)

   ## P4 — Low
   - [Anything else mentioned]
   ```

3. **`active/inbox.md`** — Seed with 2-3 actionable items:
   ```markdown
   # Inbox

   | Date | Item | Source | Status |
   |------|------|--------|--------|
   | [today] | Review coding standards for [their stack] | /setup | Needs Review |
   | [today] | Scaffold first product if not done in Phase 8 | /setup | Needs Review |
   | [today] | Run /weekly-review after first week | /setup | Needs Review |
   ```

4. **Remaining active files** — If `blockers.md`, `risks.md`, or `improvements.md` were created in Phase 1 with minimal templates, leave them as-is (clean slate is correct for new setup).

## 3b — Business directories (conditional on Phase 2 answers)

- Freelancer: create `business/sales/`, `business/clients/`, `business/finance/revenue-tracker.md` (template)
- Business/Consulting: create full `business/` structure (assets, clients, finance, marketing, operating, sales, strategy), seed `business/operating/recurring-processes.md` (template)
- Product builder only: create `business/marketing/`, `business/strategy/` only
- None/minimal: create `business/` with `.gitkeep` only

## 3c — Engineering directories

- Always create `engineering/scripts/`
- Add `engineering/infra/` if they mention deployment, cloud, or devops
- Add `engineering/automations/`, `engineering/shared-libraries/`, `engineering/troubleshooting/`

## 3d — History initialization

- Write first entry to `core/history/decisions.md` (DEC-001: Initial System Setup)
- Write first entry to `core/history/master-timeline.md`
- Write `core/history/current-state.md` with system snapshot

## 3e — MEMORY.md update

- Add user-specific context: name, domain, stack, projects, business type

Print educational beat: "Your `active/` directory is your daily command center — loaded automatically every session. `core/history/` is your institutional memory — decisions and outcomes are never lost. `business/` tracks revenue, clients, and marketing. Everything persists across sessions because it's all files in a git repo."
