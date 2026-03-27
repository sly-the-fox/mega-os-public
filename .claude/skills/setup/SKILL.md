---
name: setup
description: Use when onboarding — interactive wizard to verify environment, personalize the system, and initialize active state.
invocation: /setup
user_invocable: true
---

# Setup

Interactive onboarding wizard with 11 phases (0-10). Each phase has a natural stopping point where you can continue or stop. Supports arguments: `--phase N` (resume from phase), `--skip-telegram`, `--minimal` (phases 0-3 then jump to Phase 10).

---

## Phase 0: Welcome & System Tour (interactive)

Print a welcome message:

"Welcome to **Mega-OS** — a personal operating system for builders, powered by Claude Code.

You have:
- **39 AI agents** organized in 5 categories (Governance, Knowledge, Technical, Business, Evolution)
- **25+ slash commands** for daily operations, building, system management, and deployment
- **8 automated workflows** (Planning, Technical, Business, Incident, Knowledge, Content, Site Build, Evolution)
- **Optional cron automations** for daily scans, news briefings, and system self-improvement
- **A living task board** in `active/` that persists your context across every session

Think of this as your command center. Claude reads your current state at the start of every session and picks up where you left off. Agents are specialists you delegate to. The system learns and improves over time.

One of the first things we'll set up is a **private Git repo**. Every commit backs up your entire operating system — priorities, decisions, context, everything. Your OS lives in the cloud, accessible from any machine."

Then show the commands overview:

"Here are the commands built into your OS:

**Daily Operations:**
| Command | What it does |
|---------|-------------|
| `/goodmorning` | Morning briefing with overnight cron results and suggested plan |
| `/daily-scan` | Morning digest — scans for stale, overdue, or unactioned items |
| `/weekly-review` | End-of-week retrospective with progress summary and priority updates |
| `/news-briefing` | AI-curated intelligence briefing for your domain |
| `/dream` | Generate a reflective prompt from the week's context |

**Building & Creating:**
| Command | What it does |
|---------|-------------|
| `/project-kickoff` | Scaffold a new product under `products/` |
| `/write` | Launch the content pipeline (Writer -> Editor -> Polisher) |
| `/build-site` | Build a website from concept to deployment |
| `/bug-triage` | Diagnose and fix a reported bug |
| `/deep-research` | MECE-structured research (web, local codebase, or hybrid) |
| `/generate-content` | Generate short-form social content per channel schedule |
| `/draw` | Generate visual diagrams and images |

**System Management:**
| Command | What it does |
|---------|-------------|
| `/setup` | This wizard (re-run anytime to reconfigure) |
| `/add-agent` | Create a new custom agent |
| `/improvement-audit` | Deep system audit with rotating daily focus |
| `/coherence` | Invoke the Coherence perspective (harmonic awareness) |
| `/workflow-review` | Analyze workflow patterns and operational friction |
| `/metrics-scan` | Fetch PyPI, GitHub, and website metrics for your packages |
| `/polish` | Convert markdown to polished DOCX/PDF |

**Deployment & Updates:**
| Command | What it does |
|---------|-------------|
| `/update` | Pull framework updates from the upstream public repo |
| `/publish` | Sync your framework changes to the public repo (maintainer only) |

You don't need to memorize these — they'll be in your finalization cheat sheet, and Claude knows them all."

Ask: "Ready to set up? Choose: **full guided setup** (~20 min, 11 phases) or **minimal setup** (~5 min, gets you running fast)?"

If minimal: set `--minimal` flag. If full: continue normally.

---

## Phase 1: Environment Verification (automatic)

Run these checks silently and report a summary:

0. **Merge driver setup** — Run `git config merge.ours.driver true`. This activates the `merge=ours` strategy used by `.gitattributes` to protect personal data directories during upstream merges. This is idempotent and safe to re-run.
1. **Settings check** — Read `.claude/settings.json`. Confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set to `1` in the `env` block. If missing, warn.
2. **Agent symlink check** — Count symlinks at `.claude/agents/*.md` (excluding REGISTRY.md, README.md). Confirm each resolves to an actual file. Report count and any broken links.
3. **Active state check** — Verify at minimum these files exist in `active/` (additional files are fine):
   - `now.md`, `priorities.md`, `inbox.md`, `blockers.md`, `risks.md`, `improvements.md`
   - `audits.md`, `coherence-metrics.md`, `freshness-log.md`, `freshstate-report.md`
   - `daily-digest.md`, `news-briefing.md`, `news-briefing-state.md`
   - `improvement-audit.md`, `workflow-review.md`, `system-evaluation.md`
   - `cron-health.md`, `codex-metrics.md`, `dream-report.md`
   - Also verify `active/index.json` exists (critical — SessionStart hook depends on it)
   - Create any missing files with the placeholder templates from the public repo (empty tables, zero counters, "No items yet" stubs). If `index.json` is missing, create it with the starter manifest listing all 19 active files.
4. **Core directories check** — Verify `core/standards/`, `core/templates/`, `core/indexes/`, `core/history/` exist. Create any missing directories.
5. **Git config check** — Verify `git config user.name` and `git config user.email` are set. If not, warn that git commits will need a name and email.
6. **Prior setup check** — Search `core/history/decisions.md` for a decision with "setup" in the title. If found, inform the user that setup was run before and ask whether to re-run or skip completed phases.

Print educational beat: "The `.claude/settings.json` controls permissions and environment. The `active/` directory is your living task board, read at every session start."

Print a status summary table:

```
| Check            | Status | Details          |
|------------------|--------|------------------|
| Agent teams      | OK/WARN| ...              |
| Agent symlinks   | OK/WARN| 33 found, 0 broken |
| Active state     | OK/WARN| 19/19 files + index.json |
| Core directories | OK/WARN| 4/4 present      |
| Git identity     | OK/WARN| ...              |
| Prior setup      | New/Re-run | ...           |
```

Ask: "Environment looks good. Continue to Phase 2 (Identity & Context)?"

---

## Phase 2: Identity & Context (interactive)

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

**Business Context:**
- Are you freelancing, running a business, building products, consulting, or a mix?
- Do you have revenue goals? (optional — "yes" seeds a revenue tracker in business/finance/)
- Do you have existing clients? (optional — "yes" creates business/clients/)

Store answers in memory for use in subsequent phases. Do not write files yet.

Ask: "Got it. Continue to Phase 3 (Workspace Scaffolding)?"

---

## Phase 3: Workspace Scaffolding (automated)

Using answers from Phase 2, build the full workspace: active state files (now.md, priorities.md, inbox.md), business directories, engineering directories, history initialization, and MEMORY.md.

> See `references/workspace-templates.md` for detailed templates and scaffolding instructions.

Print: "Workspace scaffolded."

If `--minimal` was passed, skip to Phase 10 (Finalization). Otherwise ask: "Continue to Phase 4 (Standards Customization)?"

---

## Phase 4: Standards Customization (interactive)

Customize coding standards, naming conventions, writing style, and review checklist for the user's tech stack and preferences. Each standard is shown, discussed, and updated interactively.

> See `references/standards-customization.md` for the full customization flow and writing style setup instructions.

Print: "Standards customized for your stack."

Ask: "Continue to Phase 5 (Git Repository & Cloud Backup)?"

---

## Phase 5: Git Repository & Cloud Backup (interactive)

Print: "Mega-OS is a living system — your priorities, decisions, and context change every session. Git turns that into **durable cloud storage**. Every commit is a snapshot of your entire operating system. Push to a private repo and your OS is backed up, versioned, and accessible from any machine."

**Step 1 — Check current remotes:**

Run `git remote -v`. Analyze what exists:

- If `origin` points to the public Mega-OS repo (user cloned it directly), it needs renaming to `upstream`.
- If `upstream` already exists, note it.
- If no remotes exist, proceed to setup.

**Step 2 — Ask:**

"Do you want to set up cloud backup with a private GitHub repo?"

If no, skip to Phase 6.

If yes:

1. "Create a **private** repository on GitHub (e.g., `my-mega-os`). Don't initialize it with a README — we already have one. I'll wait for the URL."
2. Once they provide the URL, reconfigure remotes:
   ```bash
   # If origin currently points to the public repo, rename it
   git remote rename origin upstream
   # Add user's private repo as origin
   git remote add origin <user-provided-url>
   ```
3. Stage all setup changes so far and commit: `system: initial Mega-OS setup for [name]`
4. Ask: "Push to your remote now?" If yes: `git push -u origin master`
5. Confirm: `git remote -v` — show the user both remotes.

**Step 3 — Tips:**

- "Commit after each significant session (Claude will remind you at session close)"
- "Push at least daily for cloud backup"
- "Private repo = your data stays private (priorities, decisions, client info)"
- "`git log --oneline` shows your OS evolution over time"
- "If your machine dies, clone the repo on a new one and you're back in business"
- "Setting up on a second computer? Just `git clone <your-private-repo> mega-os && cd mega-os && git remote add upstream https://github.com/sly-the-fox/mega-os-public.git`"

Ask: "Continue to Phase 6 (Telegram Bridge)?"

---

## Phase 6: Telegram Bridge Setup (optional, interactive)

If `--skip-telegram` was passed, skip this phase.

Ask: "Do you want to set up the Telegram bridge? This lets you message Claude from your phone."

If no, skip to Phase 7.

Print educational beat: "The Telegram bridge lets you interact with your OS from your phone — check priorities, triage items, even trigger workflows while you're away from your desk."

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

Ask: "Continue to Phase 7 (Automation Setup)?"

---

## Phase 7: Automation Setup (optional, interactive)

Present 14 available cron automations (7 daily, 5 weekly, 2 monthly) and let the user pick which to install. Options: specific numbers, `all`, `recommended` (daily scan + weekly review + freshstate), or `none`.

> See `references/cron-jobs.md` for the caveat, automation menu tables, selection flow, exact cron entries, and tips.

Ask: "Continue to Phase 8 (Product Scaffolding)?"

---

## Phase 8: First Product Scaffolding (optional, interactive)

Optionally scaffold the user's first product under `products/` with CLAUDE.md, README, SPEC, and index updates.

> See `references/product-scaffolding.md` for the full scaffolding flow and directory structure.

Ask: "Continue to Phase 9 (Agent Customization)?"

---

## Phase 9: Agent Customization (optional, interactive)

Suggest domain-specific custom agents based on Phase 2 answers, offer to create them via `/add-agent`, and optionally hide irrelevant default agents.

> See `references/agent-suggestions.md` for the domain-to-agent suggestion table, Plan mode recommendation, and creation/hiding steps.

Ask: "Continue to Phase 10 (Finalization)?"

---

## Phase 10: Finalization (automated)

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
     - **Phases completed:** [0-10 or subset]
     - **Automations:** [count] cron jobs configured / skipped
     - **Git remote:** [url or "not configured"]
     ```
   - Add timeline entry to `core/history/master-timeline.md`

3. **Commit all changes** — Stage and commit with message: "system: initial Mega-OS setup for [user name]"

4. **Print summary:**
   ```
   Setup complete!

   - Environment: verified
   - Identity: [name] <[email]>
   - Domain: [domain]
   - Stack: [tech stack]
   - Products: [list]
   - Custom agents: [list or "defaults only"]
   - Automations: [count] cron jobs configured / skipped
   - Git remote: [url or "not configured — run /setup --phase 5 to set up"]

   Your Commands:
     /goodmorning       — Morning briefing with overnight cron results
     /daily-scan        — Morning digest of stale/overdue items
     /weekly-review     — End-of-week retrospective
     /news-briefing     — AI-curated domain news
     /dream             — Reflective prompt from the week's context
     /project-kickoff   — Scaffold a new product
     /write             — Launch content pipeline (Writer -> Editor -> Polisher)
     /build-site        — Build a website from concept to deployment
     /bug-triage        — Diagnose and fix a bug
     /deep-research     — MECE-structured research
     /generate-content  — Short-form social content per channel schedule
     /draw              — Generate visual diagrams and images
     /add-agent         — Create a custom agent
     /coherence         — Harmonic consciousness perspective
     /workflow-review   — Analyze workflow patterns and friction
     /metrics-scan      — Fetch PyPI/GitHub/website metrics
     /improvement-audit — Deep system audit (rotating daily focus)
     /polish            — Convert markdown to DOCX/PDF
     /setup             — Re-run this wizard anytime
     /update            — Pull framework updates from upstream
     /publish           — Sync framework changes to public repo (maintainers)

   Suggested next steps:
     - Start working on your first project — Claude picks up context from active/now.md
     - Commit and push after your first real work session (your OS is backed up in the cloud)
     - Run /weekly-review at the end of your first week
     - Use /project-kickoff to add more products
     - Use /add-agent to create domain-specific agents
     - Run /update periodically to get new agents, skills, and bug fixes from the Mega-OS project
     - Check active/now.md for your current focus
   ```
