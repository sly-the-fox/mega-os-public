# Mega-OS

Mega-OS is a multi-agent operating system built on Claude Code. It organizes 31 specialized agents into 5 categories, enabling structured collaboration across governance, knowledge management, technical execution, business operations, and system evolution.

Each agent has a defined role, clear boundaries, and explicit handoff protocols. Agents stay in their lane and delegate to specialists when needed.

## Directory Structure

```
mega-os/
  .claude/
    agents/            # 31 agent definitions in category subdirectories
      governance/      # overseer, governor, router, planner, pm, operator, sentinel, auditor
      knowledge/       # historian, librarian, summarizer, documenter, polisher, writer, editor
      technical/       # architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer
      business/        # strategist, marketer, seller, financier
      evolution/       # improver, evaluator, codex
      shared/          # system rules, collaboration protocol, templates
    skills/            # reusable skills (setup, add-agent, project-kickoff, bug-triage, daily-scan, weekly-review, polish-document, write-content)
  active/              # current state files
    now.md             # what is happening right now
    priorities.md      # ordered priority list
    inbox.md           # incoming items awaiting triage
    blockers.md        # active blockers
  core/                # standards, templates, indexes, project history
  products/            # product codebases
  engineering/         # scripts, automations, infrastructure
  business/            # assets, clients, finance, marketing, operations
```

## Setup

1. Clone the repository:
   ```
   git clone <repo-url> mega-os
   cd mega-os
   ```

2. Ensure Claude Code is installed.

3. Enable agent teams:
   ```
   export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   ```

4. Launch Claude Code and run `/setup` for guided interactive onboarding. Or jump straight in — agents are available via the Agent tool with `subagent_type` matching the agent filename (e.g., `architect`, `engineer`, `pm`).

See [GETTING_STARTED.md](GETTING_STARTED.md) for a detailed walkthrough.

## Agent Details

See [AGENTS.md](AGENTS.md) for the full list of agents, design philosophy, and key workflows.

The canonical registry of all agents lives at `.claude/agents/REGISTRY.md`.

## Status

Agent definitions are complete. Core infrastructure and product integrations are in active development.
