# Getting Started with Mega-OS

This guide walks you through your first session. Read this once, then you can forget about it — the system is self-documenting from here.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) installed (`npm install -g @anthropic-ai/claude-code`)
- A Claude API key or Claude Pro/Max subscription
- Git

---

## 1. Clone and Enter

```bash
git clone https://github.com/YOUR_USERNAME/mega-os.git
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
- Discover all 26 agents via symlinks in `.claude/agents/`
- Enable agent teams via `.claude/settings.json`

You're ready to work.

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

Products live under `products/`. Each product should have its own README.

---

## 5. Customize for Your Domain

### Add a new agent

Create a file at `.claude/agents/<category>/my-agent.md`:

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

See `engineering/scripts/telegram-bridge/README.md` for full details.

---

## 7. Use as an MCP Server / with Other Tools

Mega-OS is tool-agnostic at its core. The agent definitions, standards, and workflows are plain markdown files that any LLM-based tool can consume.

**With Claude Code:** Works out of the box (agents auto-discovered, settings pre-configured).

**With other AI coding tools:** Point the tool at `CLAUDE.md` as a system prompt or project instructions file. The agent definitions in `.claude/agents/` can be adapted as prompt templates.

**As an MCP server:** The file structure (active state, standards, history) can be exposed via an MCP server. Create tools that read/write to `active/`, `core/`, and agent files. The Telegram bridge is a working example of external integration.

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
