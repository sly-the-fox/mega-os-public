---
name: setup
description: Interactive onboarding wizard — verify environment, personalize the system, and initialize active state.
invocation: /setup
user_invocable: true
---

# Setup

Interactive onboarding wizard with 8 phases. Each phase has a natural stopping point where you can continue or stop. Supports arguments: `--phase N` (resume from phase), `--skip-telegram`, `--minimal` (phases 1-3 only).

## Phase 1: Environment Verification (automatic)

Run these checks silently and report a summary:

1. **Settings check** — Read `.claude/settings.json`. Confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set to `1` in the `env` block. If missing, warn.
2. **Agent symlink check** — Count symlinks at `.claude/agents/*.md` (excluding REGISTRY.md, AGENTS.md). Confirm each resolves to an actual file. Report count and any broken links.
3. **Active state check** — Verify these 6 files exist in `active/`:
   - `now.md`, `priorities.md`, `inbox.md`, `blockers.md`, `risks.md`, `improvements.md`
   - Create any missing files with a minimal template:
     ```
     # [Title]

     (No items yet.)
     ```
4. **Core directories check** — Verify `core/standards/`, `core/templates/`, `core/indexes/`, `core/history/` exist. Create any missing directories.
5. **Prior setup check** — Search `core/history/decisions.md` for a decision with "setup" in the title. If found, inform the user that setup was run before and ask whether to re-run or skip completed phases.

Print a status summary table:

```
| Check            | Status | Details          |
|------------------|--------|------------------|
| Agent teams      | OK/WARN| ...              |
| Agent symlinks   | OK/WARN| 30 found, 0 broken |
| Active state     | OK/WARN| 6/6 files        |
| Core directories | OK/WARN| 4/4 present      |
| Prior setup      | New/Re-run | ...           |
```

Ask: "Environment looks good. Continue to Phase 2 (Personalization)?"

---

## Phase 2: Personalization (interactive)

Ask the user these questions one group at a time. Wait for answers before proceeding.

**Identity:**
- What's your name?
- What's your email?
- What's your GitHub username or organization?

**Domain:**
- What domain do you work in? (e.g., web dev, data science, devops, consulting, creative)
- What are you building right now? (1-3 projects or goals)
- What's your primary tech stack? (e.g., Python/FastAPI, TypeScript/Next.js, Go, Rust)

**Workflow:**
- Solo or team?
- How do you prefer to work? (e.g., "plan everything first", "just start building", "iterative sprints")

Store answers in memory for use in subsequent phases. Do not write files yet.

Ask: "Got it. Continue to Phase 3 (Active State Initialization)?"

---

## Phase 3: Active State Initialization (automated)

Using the answers from Phase 2, write these files:

1. **`active/now.md`** — Set the current focus based on stated projects/goals. Use this format:
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
   | [today] | Scaffold first product if not done in Phase 6 | /setup | Needs Review |
   | [today] | Run /weekly-review after first week | /setup | Needs Review |
   ```

4. **Remaining active files** — If `blockers.md`, `risks.md`, or `improvements.md` were created in Phase 1 with minimal templates, leave them as-is (clean slate is correct for new setup).

Print: "Active state initialized. Your priorities and focus are set."

If `--minimal` was passed, skip to Phase 8 (Finalization). Otherwise ask: "Continue to Phase 4 (Standards Customization)?"

---

## Phase 4: Standards Customization (interactive)

1. **Coding standards** — Read `core/standards/coding-standards.md`. Show the user which language sections exist. Ask:
   - Which of these are relevant to your stack?
   - Any languages/frameworks to add?
   - Remove irrelevant sections and add new ones for their stated tech stack with sensible defaults.

2. **Naming conventions** — Read `core/standards/naming.md`. Show current conventions. Ask:
   - Does this match your preferences? Any changes?
   - Apply requested changes.

3. **Writing style** — Ask:
   - Do you have a preferred writing style? (technical/casual/formal/concise)
   - If provided, note it in coding standards or a separate style guide.

4. **Review checklist** — Read `core/standards/review-checklist.md`. Show current criteria. Ask:
   - Any criteria to add or remove for your domain?
   - Apply changes.

Print: "Standards customized for your stack."

Ask: "Continue to Phase 5 (Telegram Bridge)?"

---

## Phase 5: Telegram Bridge Setup (optional, interactive)

If `--skip-telegram` was passed, skip this phase.

Ask: "Do you want to set up the Telegram bridge? This lets you message Claude from your phone."

If no, skip to Phase 6.

If yes, walk through:

1. "Create a bot via @BotFather on Telegram. What's the bot token?"
2. "Send a message to your bot, then check the logs for your chat ID. What's your chat ID?"
3. "Optional: Set a passphrase for authentication (recommended if the bot is public). Enter one or press enter to skip."
4. Create/update `engineering/scripts/telegram-bridge/.env` with their values.
5. Mention: "Install dependencies with `pip install -r engineering/scripts/telegram-bridge/requirements.txt`"
6. Print tips:
   - Sessions persist automatically — conversations continue where you left off
   - 10-minute timeout for Claude responses
   - `/reset` clears context and starts a fresh session
   - `/status` and `/priorities` show current state

Ask: "Continue to Phase 6 (Product Scaffolding)?"

---

## Phase 6: First Product Scaffolding (optional, interactive)

Ask: "Do you want to create your first product now?"

If no, skip to Phase 7.

If yes:

1. "What's the product name?" (validate: kebab-case, no spaces)
2. "What tech stack?" (e.g., Next.js, Python/FastAPI, Go, static site)
3. "One-line description?"

Then:
- Create `products/<name>/` with appropriate structure for the tech stack
- Create `products/<name>/CLAUDE.md` with project context
- Create `products/<name>/README.md` with basic info
- Use `core/templates/spec-template.md` to create `products/<name>/SPEC.md`
- Update `core/indexes/project-map.md` with the new product
- Update `active/priorities.md` if not already listed

Print: "Product scaffolded at `products/<name>/`."

Ask: "Continue to Phase 7 (Agent Customization)?"

---

## Phase 7: Agent Customization (optional, interactive)

Based on the user's domain from Phase 2, suggest relevant custom agents. Examples:

| User Domain | Suggested Agents |
|-------------|-----------------|
| Web dev | api-designer, frontend-specialist, performance-analyst |
| Data science | data-engineer, ml-ops, experiment-tracker |
| DevOps | incident-responder, capacity-planner, sre |
| Consulting | proposal-writer, client-manager, deliverable-tracker |
| Creative | content-strategist, brand-guardian, campaign-manager |

Present suggestions and ask:
1. "Want to create any of these? Or describe a custom agent you need."
2. For each requested agent, run `/add-agent` (the add-agent skill) to create it properly.
3. "Want to hide any default agents that aren't relevant? (This removes symlinks but keeps the files.)"
   - If yes, remove the selected symlinks. The agent files remain in their category directories.

Print: "Agent roster customized."

Ask: "Continue to Phase 8 (Finalization)?"

---

## Phase 8: Finalization (automated)

1. **Update indexes:**
   - Update `core/indexes/project-map.md` to reflect actual `products/` contents
   - Update `core/indexes/canonical-files.md` with any new key files
   - Update `core/indexes/active-context-map.md` with current state

2. **Record setup decision:**
   - Add entry to `core/history/decisions.md`:
     ```
     ## DEC-NNN: Initial System Setup
     - **Date:** [today]
     - **Status:** Accepted
     - **Context:** First-time setup of Mega-OS for [user name]
     - **Decision:** Configured system for [domain], [tech stack], [solo/team]
     - **Products:** [list]
     - **Custom agents:** [list or "none"]
     - **Phases completed:** [1-8 or subset]
     ```
   - Add timeline entry to `core/history/master-timeline.md`

3. **Commit all changes** — Stage and commit with message: "Setup: configure Mega-OS for [user name]"

4. **Print summary:**
   ```
   Setup complete!

   - Environment: verified
   - Identity: [name] <[email]>
   - Domain: [domain]
   - Stack: [tech stack]
   - Products: [list]
   - Custom agents: [list or "defaults only"]

   Suggested next steps:
   - Run /weekly-review at the end of your first week
   - Use /project-kickoff to add more products
   - Use /add-agent to create domain-specific agents
   - Check active/now.md for your current focus
   ```
