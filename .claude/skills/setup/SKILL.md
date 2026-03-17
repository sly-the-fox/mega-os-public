---
name: setup
description: Interactive onboarding wizard — verify environment, personalize the system, and initialize active state.
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
- **21 slash commands** for daily operations, building, system management, and deployment
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
2. **Agent symlink check** — Count symlinks at `.claude/agents/*.md` (excluding REGISTRY.md, AGENTS.md). Confirm each resolves to an actual file. Report count and any broken links.
3. **Active state check** — Verify these 19 files exist in `active/`:
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

Using the answers from Phase 2, build out the full workspace:

### 3a — Active State

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

### 3b — Business directories (conditional on Phase 2 answers)

- Freelancer: create `business/sales/`, `business/clients/`, `business/finance/revenue-tracker.md` (template)
- Business/Consulting: create full `business/` structure (assets, clients, finance, marketing, operating, sales, strategy), seed `business/operating/recurring-processes.md` (template)
- Product builder only: create `business/marketing/`, `business/strategy/` only
- None/minimal: create `business/` with `.gitkeep` only

### 3c — Engineering directories

- Always create `engineering/scripts/`
- Add `engineering/infra/` if they mention deployment, cloud, or devops
- Add `engineering/automations/`, `engineering/shared-libraries/`, `engineering/troubleshooting/`

### 3d — History initialization

- Write first entry to `core/history/decisions.md` (DEC-001: Initial System Setup)
- Write first entry to `core/history/master-timeline.md`
- Write `core/history/current-state.md` with system snapshot

### 3e — MEMORY.md update

- Add user-specific context: name, domain, stack, projects, business type

Print educational beat: "Your `active/` directory is your daily command center — loaded automatically every session. `core/history/` is your institutional memory — decisions and outcomes are never lost. `business/` tracks revenue, clients, and marketing. Everything persists across sessions because it's all files in a git repo."

Print: "Workspace scaffolded."

If `--minimal` was passed, skip to Phase 10 (Finalization). Otherwise ask: "Continue to Phase 4 (Standards Customization)?"

---

## Phase 4: Standards Customization (interactive)

> **Tip:** If you have strong opinions about coding standards and want to review changes before they're applied, consider switching to **Plan mode** (`/plan`) with **Opus 4.6 (medium)** or equivalent. This lets you approve each standards change before it's written. You can return to setup afterward with `/setup --phase 5`. Otherwise, we'll work through it interactively right here.

1. **Coding standards** — Read `core/standards/coding-standards.md`. Show the user which language sections exist. Ask:
   - Which of these are relevant to your stack?
   - Any languages/frameworks to add?
   - Remove irrelevant sections and add new ones for their stated tech stack with sensible defaults.

2. **Naming conventions** — Read `core/standards/naming.md`. Show current conventions. Ask:
   - Does this match your preferences? Any changes?
   - Apply requested changes.

3. **Writing style** — Check if `core/standards/writing-style.md` exists.
   - If it does NOT exist: copy from `core/standards/writing-style.default.md` to create the user's copy.
   - If it exists and still contains the "Setup required" marker (template version): Ask "Do you have a preferred writing style? (technical/casual/formal/concise)"
   - If they want a personalized style: prompt them to place 3-5 writing samples in `style-samples/`, then analyze the samples and populate `writing-style.md` with a full style profile.
   - If they skip or have no samples: leave the template in place (agents produce neutral content).
   - If already populated (no "Setup required" marker): inform user their style guide is already configured and ask if they want to regenerate it.
   - Note: `writing-style.default.md` ships with the framework and is updated by `/update`. The user's `writing-style.md` is never overwritten by updates.

4. **Review checklist** — Read `core/standards/review-checklist.md`. Show current criteria. Ask:
   - Any criteria to add or remove for your domain?
   - Apply changes.

Print educational beat: "These standards are enforced by the Reviewer agent at the end of every Technical workflow. Customizing now means relevant feedback from day one."

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

**Step 1 — Show the caveat (prominent, before anything else):**

> **Important:** These are **system-level cron jobs** (installed via `crontab`), NOT Claude Code in-session crons. They persist across reboots and sessions — you don't need Claude Code open for them to fire. However, they only run when your computer is powered on and your user session is active. If your laptop is closed or sleeping, scheduled jobs will be skipped — they don't queue up and run later. For critical automations, make sure your machine is awake during the scheduled times. All automations log to `/tmp/mega-os-*.log` so you can check what ran.

**Step 2 — Present the automation menu**, grouped by frequency:

**Daily:**
| # | Name | Time | Description |
|---|------|------|-------------|
| 1 | Daily improvement audit | 7:30 AM | Deep MECE-decomposed system audit with rotating focus: Mon=Governance, Tue=Knowledge, Wed=Technical, Thu=Products, Fri=Business, Sat=Evolution, Sun=Integration. Writes to `active/improvement-audit.md`. |
| 2 | Content generation | 7:03 AM | Generates marketing content per channel schedule |
| 3 | Channel tracker update | 7:27 AM | Updates content pipeline status after generation |
| 4 | PyPI/GitHub metrics | 8:33 AM | Fetches download stats and stars for your published packages |
| 5 | News briefing | 8:45 AM | AI/tech intelligence briefing with optional Telegram delivery |
| 6 | Daily system scan | 9:10 AM | Scans all active state for stale/overdue items, produces `active/daily-digest.md` |
| 7 | Freshstate scan | 9:17 AM | Checks document freshness, alerts on stale docs via Telegram |

**Weekly:**
| # | Name | Schedule | Description |
|---|------|----------|-------------|
| 8 | Content pipeline status | Mon 8:03 AM | Weekly content pipeline check with Telegram summary |
| 9 | Risk staleness alert | Wed 9:07 AM | Flags risks unmaintained >14 days |
| 10 | Weekly review | Sun 10:13 AM | Comprehensive system review + state updates |
| 11 | Revenue check-in | Sun 10:27 AM | Reviews revenue tracker, sends Telegram status |
| 12 | Index maintenance | Sun 10:47 AM | Verifies core/indexes/ consistency with filesystem |

**Monthly:**
| # | Name | Schedule | Description |
|---|------|----------|-------------|
| 13 | System evaluation | 1st & 15th, 11:03 AM | Evaluator assessment of system health |
| 14 | Competitor monitoring | 1st of month, 9:03 AM | Scans for news about competitors |

**Step 3 — Ask the user to pick:**
- Numbers (e.g., "1, 6, 10")
- `all` — install everything
- `recommended` — starter set: **Daily system scan (#6) + Weekly review (#10) + Freshstate scan (#7)**
- `none` — skip this phase

**Step 4 — For each selected automation:**

1. Detect `claude` binary path via `which claude || echo "$HOME/.local/bin/claude"`
2. Detect mega-os repo path from `pwd`
3. Append each cron entry using safe append: `(crontab -l 2>/dev/null; echo "<entry>") | crontab -`
4. Each entry follows the pattern:
   ```
   <schedule> cd <repo-path> && <claude-path> -p "<prompt>" --permission-mode auto > /tmp/mega-os-<name>.log 2>&1
   ```

The exact cron entries per selection:

```bash
# 1. Daily improvement audit (7:30 AM)
30 7 * * * cd <repo> && <claude> -p "/improvement-audit" --permission-mode auto > /tmp/mega-os-improvement-audit.log 2>&1

# 2. Content generation (7:03 AM)
3 7 * * * <claude> -p "Generate today's marketing content per business/marketing/channel-schedule.md" --permission-mode auto >> /tmp/mega-os-content-gen.log 2>&1

# 3. Channel tracker update (7:27 AM)
27 7 * * * cd <repo> && <claude> -p "Read /tmp/mega-os-content-gen.log to see what content was generated today. Update business/marketing/channel-tracker.md with new draft entries, marking their pipeline status as 'drafted' and noting the draft location in drafts/social/." --permission-mode auto > /tmp/mega-os-channel-tracker.log 2>&1

# 4. PyPI/GitHub metrics (8:33 AM)
# Replace <pypi-package> and <github-user/repo> with your published package details
33 8 * * * cd <repo> && <claude> -p "Fetch PyPI download stats for <pypi-package> (use web search or pypistats.org API). Fetch GitHub stars for <github-user/repo> (use GitHub API). Append today's numbers to business/marketing/adoption-metrics.md (create if doesn't exist). If downloads exceed 500 or stars exceed 50, send a milestone alert via Telegram." --permission-mode auto > /tmp/mega-os-metrics.log 2>&1

# 5. News briefing (8:45 AM)
45 8 * * * cd <repo> && <claude> -p "/news-briefing --telegram" --permission-mode auto > /tmp/mega-os-news-briefing.log 2>&1; echo "Exit: $? at $(date)" >> /tmp/mega-os-news-briefing.log

# 6. Daily system scan (9:10 AM)
10 9 * * * cd <repo> && <claude> -p "/daily-scan" --permission-mode auto > /tmp/mega-os-daily-scan.log 2>&1

# 7. Freshstate scan (9:17 AM)
17 9 * * * cd <repo> && <claude> -p "Run freshstate check on this repo. Execute: freshstate check. Save the output to active/freshstate-report.md (replace contents with timestamped report). If any files are stale or cross-references broken, send a summary via Telegram using the bridge at engineering/scripts/telegram-bridge/." --permission-mode auto > /tmp/mega-os-freshstate.log 2>&1

# 8. Content pipeline status (Mon 8:03 AM)
3 8 * * 1 cd <repo> && <claude> -p "Check business/marketing/content-calendar.md for this week's planned article. Check if a draft exists in drafts/. Check business/marketing/channel-tracker.md for overdue content. Send a Telegram summary of content pipeline status: what's due, what's drafted, what's overdue." --permission-mode auto > /tmp/mega-os-content-pipeline.log 2>&1

# 9. Risk staleness alert (Wed 9:07 AM)
7 9 * * 3 cd <repo> && <claude> -p "Check active/risks.md. For each active risk, check if the 'Date Added' is more than 14 days ago and the mitigation status hasn't been updated. Flag stale risks. Send a Telegram alert listing any risks that need mitigation review." --permission-mode auto > /tmp/mega-os-risk-alert.log 2>&1

# 10. Weekly review (Sun 10:13 AM)
13 10 * * 0 cd <repo> && <claude> -p "/weekly-review" --permission-mode auto > /tmp/mega-os-weekly-review.log 2>&1

# 11. Revenue check-in (Sun 10:27 AM)
27 10 * * 0 cd <repo> && <claude> -p "Review business/finance/revenue-tracker.md. Check which streams still show \$0. Check if 30-day or 60-day review dates are approaching. Update the 'Last Checked' date. Send a Telegram summary of revenue status and any action items due this week." --permission-mode auto > /tmp/mega-os-revenue-checkin.log 2>&1

# 12. Index maintenance (Sun 10:47 AM)
47 10 * * 0 cd <repo> && <claude> -p "Verify core/indexes/canonical-files.md, core/indexes/project-map.md, and core/indexes/active-context-map.md are consistent with the actual filesystem. Check for files listed in indexes that don't exist, and important files that exist but aren't indexed. Report any drift found. Update indexes if discrepancies are minor (< 5 items). Flag larger issues for manual review." --permission-mode auto > /tmp/mega-os-index-maintenance.log 2>&1

# 13. System evaluation (1st & 15th, 11:03 AM)
3 11 1,15 * * cd <repo> && <claude> -p "Run a system evaluation as the Evaluator agent. Assess: agent utilization (which agents were used this period), workflow completion rates, document freshness (reference active/freshness-log.md), improvement proposal outcomes (reference active/improvements.md), and revenue progress (reference business/finance/revenue-tracker.md). Write findings to active/coherence-metrics.md. Identify top 3 areas for improvement." --permission-mode auto > /tmp/mega-os-evaluation.log 2>&1

# 14. Competitor monitoring (1st of month, 9:03 AM)
3 9 1 * * cd <repo> && <claude> -p "Search for recent news and announcements about competitors in your domain. Check for new funding rounds, product launches, or feature releases. Update business/strategy/ with any significant findings. Send a Telegram summary." --permission-mode auto > /tmp/mega-os-competitor-monitor.log 2>&1
```

Where `<repo>` and `<claude>` are detected at runtime during setup.

**Step 5 — Confirm:** Print installed jobs via `crontab -l | grep mega-os`

**Step 6 — Show tips:**
- "Check logs anytime: `cat /tmp/mega-os-daily-scan.log`"
- "List your cron jobs: `crontab -l`"
- "Remove a job: `crontab -e` and delete the line"
- "The daily improvement audit runs a different deep scan each day — check `active/improvement-audit.md` for findings"

Ask: "Continue to Phase 8 (Product Scaffolding)?"

---

## Phase 8: First Product Scaffolding (optional, interactive)

Ask: "Do you want to create your first product now?"

If no, skip to Phase 9.

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

Ask: "Continue to Phase 9 (Agent Customization)?"

---

## Phase 9: Agent Customization (optional, interactive)

Print educational beat: "39 agents ship by default across 5 categories (Governance, Knowledge, Technical, Business, Evolution). The system is designed to be extended — custom agents follow the same format and get the same capabilities."

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

**Before creating agents, recommend plan mode:**

Print: "**Recommended:** Before we create agents, switch to **Plan mode** (type `/plan`) and select **Opus 4.6 (medium)** or equivalent as your model. Agent creation involves designing responsibilities, writing definitions, creating symlinks, and updating the registry — Plan mode lets you review and approve each step before it happens.

Once you approve the plan and agents are created, you can jump right back into onboarding where you left off — just run `/setup --phase 10` (or whatever phase is next). The conversation auto-compacts, so your context is preserved even if the conversation gets long."

2. For each requested agent, run `/add-agent` (the add-agent skill) to create it properly.
3. "Want to hide any default agents that aren't relevant? (This removes symlinks but keeps the files.)"
   - If yes, remove the selected symlinks. The agent files remain in their category directories.

Print: "Agent roster customized."

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
