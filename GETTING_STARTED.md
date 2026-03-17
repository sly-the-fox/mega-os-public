# Getting Started with Mega-OS

This guide walks you through your first session. Read this once, then you can forget about it — the system is self-documenting from here.

**Recommended:** Run `/setup` after launching Claude Code for a guided interactive onboarding that handles everything below automatically.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) installed (`npm install -g @anthropic-ai/claude-code`)
- A Claude API key or Claude Pro/Max subscription
- Git

---

## 1. Clone and Enter

```bash
git clone https://github.com/sly-the-fox/mega-os-public.git mega-os
cd mega-os
```

---

## 2. Launch Claude Code

```bash
claude
```

That's it. On startup, Claude Code will:
- Read `CLAUDE.md` (master instructions for every session)
- Run the SessionStart hook (loads `active/now.md` and `active/priorities.md`)
- Discover all 39 agents via symlinks in `.claude/agents/`
- Enable agent teams via `.claude/settings.json`

You're ready to work.

---

## 2.5. Set Up Cloud Backup (Recommended)

Your Mega-OS clone will contain personal data (priorities, business info, products). Back it up to a private repo:

1. Create a **private** repository on GitHub (e.g., `my-mega-os`)
2. Reconfigure remotes:
   ```bash
   git remote rename origin upstream    # public repo becomes "upstream"
   git remote add origin git@github.com:YOUR_USERNAME/my-mega-os.git
   git push -u origin master
   ```

Now you have two remotes:
- **`origin`** → your private repo (push here for backup)
- **`upstream`** → public Mega-OS repo (pull framework updates from here)

The `/setup` wizard (Phase 9) walks you through this interactively.

### Setting up on a second computer

```bash
git clone git@github.com:YOUR_USERNAME/my-mega-os.git mega-os
cd mega-os
git remote add upstream https://github.com/sly-the-fox/mega-os-public.git
claude  # SessionStart hook loads your state, everything works
```

### Getting framework updates

Run `/update` in Claude Code, or manually:

```bash
git config merge.ours.driver true   # Required once — activates data protection
git fetch upstream
git merge upstream/master
```

The `merge=ours` driver ensures your personal data (`active/`, `business/`, `products/`, etc.) is never overwritten by upstream changes. The `.gitattributes` files in each data directory declare this protection, but git requires the driver to be configured locally for it to take effect.

If you skip the `git config` step, git silently ignores the merge protection and may overwrite your files during merge conflicts.

Framework updates (agents, skills, standards) merge cleanly because upstream has only empty stubs for personal data paths.

---

## 3. Try Your First Multi-Agent Task

Ask Claude to use the agent system:

```
Use the planner agent to break down this task: build a REST API for a todo app
```

Or spawn a team:

```
Create a team to design and build a landing page. Use an architect for design and an engineer for implementation.
```

### Important: Agent Teams Workaround

When spawning teammates that need to read/write files, always use `subagent_type: "general-purpose"` and describe the role in the prompt. Custom agent types (debugger, qa, etc.) only get messaging tools as teammates.

This is documented in `CLAUDE.md` under "Agent Teams — Required Patterns" and will be followed automatically.

---

## 4. Add Your First Product

```
Create a new Next.js project under products/my-app and set it up with TypeScript and Tailwind.
```

Products live under `products/`. Each product should have its own README. You can also use `/project-kickoff` for guided scaffolding.

---

## 5. Customize for Your Domain

### Add a new agent

Use `/add-agent` for a guided flow that creates the file, symlink, and updates all references automatically.

Or do it manually — create a file at `.claude/agents/<category>/my-agent.md`:

```markdown
---
name: my-agent
description: One line explaining when to use this agent.
tools: read, write, bash
---

# My Agent

## Role
What this agent does.

## Responsibilities
- Thing 1
- Thing 2

## Boundaries
- What it does NOT do
```

Then add a symlink so Claude Code discovers it:

```bash
cd .claude/agents
ln -s <category>/my-agent.md my-agent.md
```

### Add a new skill

Create `.claude/skills/my-skill/SKILL.md` with a prompt template. Skills are invoked with `/my-skill` in Claude Code.

### Modify standards

Edit files in `core/standards/` to match your team's conventions for naming, coding style, documentation, and review checklists.

---

## 6. Use the Telegram Bridge (Optional)

Send messages to Claude Code from your phone via Telegram.

1. Create a bot via [@BotFather](https://t.me/BotFather)
2. Set up the bridge:
   ```bash
   cd engineering/scripts/telegram-bridge
   cp .env.example .env
   # Edit .env with your bot token and chat ID
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   .venv/bin/python3 telegram_bridge.py
   ```

### Key features

- **Session persistence:** Conversations continue where you left off. Each chat maintains its own session automatically, saved to `sessions.json`.
- **10-minute timeout:** Claude has up to 10 minutes (600s) to respond to complex requests.
- **Thinking indicator:** A "thinking..." message appears while Claude processes your request.
- **Passphrase auth:** Set `BRIDGE_PASSPHRASE` in `.env` for second-factor authentication (recommended for public bots). Authenticate once per session.
- **Rate limiting:** Configurable per-chat rate limit (default: 10 messages per 60 seconds).
- **`/reset`:** Clears your session context and starts fresh.
- **`/status`** and **`/priorities`:** Quick views of your current state.

See `engineering/scripts/telegram-bridge/README.md` for full details.

---

## 7. Use as an MCP Server / with Other Tools

Mega-OS is tool-agnostic at its core. The agent definitions, standards, and workflows are plain markdown files that any LLM-based tool can consume.

**With Claude Code:** Works out of the box (agents auto-discovered, settings pre-configured).

**With other AI coding tools:** Point the tool at `CLAUDE.md` as a system prompt or project instructions file. The agent definitions in `.claude/agents/` can be adapted as prompt templates.

**As an MCP server:** The file structure (active state, standards, history) can be exposed via an MCP server. Create tools that read/write to `active/`, `core/`, and agent files. The Telegram bridge is a working example of external integration.

---

## Available Skills

**Daily Operations:**

| Skill | Description |
|-------|-------------|
| `/goodmorning` | Morning briefing with overnight cron results and suggested plan |
| `/daily-scan` | Scan active state for stale or overdue items |
| `/weekly-review` | Full system review with cross-referencing |
| `/news-briefing` | AI-curated intelligence briefing |
| `/dream` | Generate a reflective prompt from the week's context |

**Building & Creating:**

| Skill | Description |
|-------|-------------|
| `/project-kickoff` | Scaffold a new product with docs and registration |
| `/write` | Write original long-form content (Writer → Editor → Polisher) |
| `/build-site` | Build a website from concept to deployment |
| `/bug-triage` | Triage and investigate a bug report |
| `/deep-research` | Tiered research with MECE decomposition |
| `/generate-content` | Generate short-form social content per channel schedule |
| `/draw` | Generate visual diagrams and images |

**System Management:**

| Skill | Description |
|-------|-------------|
| `/setup` | Interactive onboarding wizard (recommended first step) |
| `/add-agent` | Create a new agent with all references in sync |
| `/improvement-audit` | Deep system audit with rotating daily focus |
| `/coherence` | Invoke the Coherence perspective |
| `/workflow-review` | Analyze workflow patterns and operational friction |
| `/metrics-scan` | Fetch PyPI, GitHub, and website metrics for your packages |
| `/polish` | Convert markdown to polished DOCX/PDF |

**Deployment & Updates:**

| Skill | Description |
|-------|-------------|
| `/update` | Pull framework updates from upstream |
| `/publish` | Sync framework changes to the public repo (maintainer only) |

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Master instructions (read every session) |
| `AGENTS.md` | Agent philosophy, categories, workflows |
| `active/now.md` | Current focus and next steps |
| `active/priorities.md` | Ordered priority list |
| `.claude/agents/REGISTRY.md` | Canonical agent directory |
| `.claude/settings.json` | Permissions, agent teams, hooks |
| `core/standards/` | Naming, coding, docs, review standards |
| `core/templates/` | Decision, spec, SOP, handoff templates |

---

## How the System Learns

1. **Historian** records decisions and outcomes in `core/history/`
2. **Evaluator** periodically assesses what's working and what isn't
3. **Improver** proposes changes based on evidence
4. You approve or reject — the system adapts over time

This is not a static template. It's a living system that gets better the more you use it.
