# Mega-OS

A personal operating system for builders, powered by Claude Code. Mega-OS organizes 38 specialized AI agents into 5 categories, giving you a structured command center for managing products, business operations, and knowledge across every session.

## What You Get

- **38 AI agents** in 5 categories (Governance, Knowledge, Technical, Business, Evolution) with defined roles and handoff protocols
- **14 slash commands** for daily operations, building, system management, and deployment
- **7 automated workflows** (Planning, Technical, Business, Incident, Knowledge, Content, Evolution)
- **Optional cron automations** for daily scans, news briefings, and system self-improvement
- **A living task board** in `active/` that persists your context across every session
- **Git-as-cloud-backup** — every commit preserves your entire OS state

## Getting Started

### First install

```bash
git clone https://github.com/sly-the-fox/mega-os.git mega-os
cd mega-os
claude
```

Claude Code auto-loads the system. On first run, it detects an unconfigured system and prompts you to run `/setup` for guided interactive onboarding.

### The `/setup` wizard

```
/setup           # Full guided setup (~20 min, 11 phases)
/setup --minimal # Quick setup (~5 min, gets you running fast)
```

Setup walks you through: environment verification, personalization, workspace scaffolding, standards customization, git cloud backup, Telegram bridge (optional), cron automations (optional), product scaffolding, and agent customization.

### Cloud backup (recommended)

Mega-OS uses a two-remote model so you can receive framework updates while keeping your personal data private:

```bash
# Inside your mega-os directory after /setup, or manually:
git remote rename origin upstream
git remote add origin git@github.com:YOUR_USERNAME/my-mega-os.git  # private repo
git push -u origin master
```

- **`upstream`** — public Mega-OS repo (framework updates via `/update`)
- **`origin`** — your private repo (cloud backup of everything including personal data)

Every commit is a snapshot of your entire operating system. Push regularly and your OS is backed up, versioned, and accessible from any machine.

### Second computer

```bash
git clone git@github.com:YOUR_USERNAME/my-mega-os.git mega-os
cd mega-os
git remote add upstream https://github.com/sly-the-fox/mega-os.git
claude  # everything just works
```

### Getting framework updates

```
/update
```

Or manually: `git fetch upstream && git merge upstream/master`

## Commands

**Daily Operations:**

| Command | What it does |
|---------|-------------|
| `/daily-scan` | Morning digest — scans for stale, overdue, or unactioned items |
| `/weekly-review` | End-of-week retrospective with progress summary and priority updates |
| `/news-briefing` | AI-curated intelligence briefing for your domain |

**Building & Creating:**

| Command | What it does |
|---------|-------------|
| `/project-kickoff` | Scaffold a new product under `products/` |
| `/write` | Launch the content pipeline (Writer -> Editor -> Polisher) |
| `/bug-triage` | Diagnose and fix a reported bug |
| `/deep-research` | MECE-structured research (web, local codebase, or hybrid) |

**System Management:**

| Command | What it does |
|---------|-------------|
| `/setup` | Guided onboarding wizard (re-run anytime to reconfigure) |
| `/add-agent` | Create a new custom agent |
| `/improvement-audit` | Deep system audit with rotating daily focus |
| `/coherence` | Invoke the Coherence perspective (harmonic awareness) |
| `/polish` | Convert markdown to polished DOCX/PDF |

**Deployment & Updates:**

| Command | What it does |
|---------|-------------|
| `/update` | Pull framework updates from the upstream public repo |
| `/publish` | Sync your framework changes to the public repo (maintainer only) |

## Directory Structure

```
mega-os/
  .claude/
    agents/            # 38 agent definitions in category subdirectories
      governance/      # overseer, governor, router, planner, pm, operator, sentinel, auditor, custodian
      knowledge/       # historian, librarian, summarizer, documenter, polisher, writer, editor
      technical/       # architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer, api-designer
      business/        # strategist, marketer, seller, financier, proposal-writer, client-manager, content-strategist, growth-hacker
      evolution/       # improver, evaluator, coherence, parallax
      shared/          # system rules, collaboration protocol, templates
    skills/            # slash commands (setup, add-agent, project-kickoff, bug-triage, daily-scan, etc.)
  active/              # living task board (loaded every session)
    now.md             # current focus and active work
    priorities.md      # ordered priority list
    inbox.md           # incoming items awaiting triage
    blockers.md        # active blockers
    risks.md           # risk register
    improvements.md    # improvement proposals
  core/                # standards, templates, indexes, project history
  products/            # product codebases
  engineering/         # scripts, automations, infrastructure
  business/            # assets, clients, finance, marketing, operations
```

## Agent Details

See [AGENTS.md](AGENTS.md) for the full list of agents, design philosophy, and key workflows.

The canonical registry of all agents lives at `.claude/agents/REGISTRY.md`.

## How It Works

1. **Session start:** Claude reads your `active/` files and picks up where you left off
2. **During work:** Agents handle specialized tasks (security reviews, content creation, business strategy, etc.)
3. **Session end:** State updates are committed to git — nothing is lost between sessions
4. **Over time:** The Evolution agents (Evaluator, Improver) propose system improvements based on usage patterns

Your OS learns and adapts. Decisions are recorded in `core/history/`. Improvements flow through a proposal/approval cycle. The system gets better as you use it.

## License

MIT
