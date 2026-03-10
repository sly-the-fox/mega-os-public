# Mega-OS

Mega-OS is a multi-agent operating system built on Claude Code. It organizes 33 specialized agents into 5 categories, enabling structured collaboration across governance, knowledge management, technical execution, business operations, and system evolution.

Each agent has a defined role, clear boundaries, and explicit handoff protocols. Agents stay in their lane and delegate to specialists when needed.

## Directory Structure

```
mega-os/
  .claude/
    agents/            # 33 agent definitions in category subdirectories
      governance/      # overseer, governor, router, planner, pm, operator, sentinel, auditor, custodian
      knowledge/       # historian, librarian, summarizer, documenter, polisher, writer, editor
      technical/       # architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer
      business/        # strategist, marketer, seller, financier
      evolution/       # improver, evaluator, codex, parallax
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

## Installation

### First install

```bash
git clone https://github.com/sly-the-fox/mega-os-public.git mega-os
cd mega-os
claude
```

Claude Code will auto-load the system. Run `/setup` for guided interactive onboarding (environment check, personalization, cloud backup, automations, and more).

### Cloud backup (recommended)

Mega-OS uses a two-remote model so you can receive framework updates while keeping your personal data private:

```bash
# Inside your mega-os directory after /setup, or manually:
git remote rename origin upstream
git remote add origin git@github.com:YOUR_USERNAME/my-mega-os.git  # private repo
git push -u origin master
```

- **`upstream`** → public Mega-OS repo (framework updates via `/update`)
- **`origin`** → your private repo (cloud backup of everything including personal data)

### Second computer

```bash
git clone git@github.com:YOUR_USERNAME/my-mega-os.git mega-os
cd mega-os
git remote add upstream https://github.com/sly-the-fox/mega-os-public.git
claude  # everything just works
```

### Getting framework updates

```
/update
```

Or manually: `git fetch upstream && git merge upstream/master`

See [GETTING_STARTED.md](GETTING_STARTED.md) for a detailed walkthrough.

## Agent Details

See [AGENTS.md](AGENTS.md) for the full list of agents, design philosophy, and key workflows.

The canonical registry of all agents lives at `.claude/agents/REGISTRY.md`.

## Status

Agent definitions are complete. Core infrastructure and product integrations are in active development.
