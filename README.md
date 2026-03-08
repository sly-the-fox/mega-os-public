# Mega-OS

Mega-OS is a multi-agent operating system built on [Claude Code](https://claude.ai/code). It organizes 26 specialized agents into 5 categories, enabling structured collaboration across governance, knowledge management, technical execution, business operations, and system evolution.

Each agent has a defined role, clear boundaries, and explicit handoff protocols. Agents stay in their lane and delegate to specialists when needed.

## Directory Structure

```
mega-os/
  .claude/
    agents/            # 26 agent definitions in category subdirectories
      governance/      # overseer, governor, router, planner, pm, operator, sentinel
      knowledge/       # historian, librarian, summarizer, documenter
      technical/       # architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer
      business/        # strategist, marketer, seller, financier
      evolution/       # improver, evaluator
      shared/          # system rules, collaboration protocol, templates
    skills/            # reusable skills (bug-triage, weekly-review, project-kickoff)
  active/              # current state files
    now.md             # what is happening right now
    priorities.md      # ordered priority list
    inbox.md           # incoming items awaiting triage
    blockers.md        # active blockers
  core/                # standards, templates, indexes, project history
  products/            # your product codebases (add your own here)
  engineering/         # scripts, automations, infrastructure
  business/            # assets, clients, finance, marketing, operations
```

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/mega-os.git
cd mega-os
claude
```

That's it. Claude Code reads `CLAUDE.md` on startup, discovers all 26 agents, and is ready to work.

**New here?** Read [GETTING_STARTED.md](GETTING_STARTED.md) for a full walkthrough — first task, adding products, customizing agents, Telegram bridge setup, and MCP server usage.

## Agent Teams

Mega-OS supports multi-agent collaboration via Claude Code's agent teams feature. See the **Agent Teams** section in `CLAUDE.md` for important usage patterns and known workarounds.

Key points:
- Teammates that need file access must use `subagent_type: "general-purpose"` with role described in the prompt
- Use `mode: "auto"` for teammates to avoid permission blocking
- Agent discovery is flat — symlinks at `.claude/agents/*.md` point to category subdirectories

## Agent Details

See [AGENTS.md](AGENTS.md) for the full list of agents, design philosophy, and key workflows.

The canonical registry of all agents lives at `.claude/agents/REGISTRY.md`.

## Telegram Bridge

A lightweight daemon for sending messages to Claude Code via Telegram. See `engineering/scripts/telegram-bridge/README.md` for setup instructions.

## License

MIT
