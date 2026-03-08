# Mega-OS — Master Instructions

This file is read on every session start. Follow these instructions.

---

## What This Is

Mega-OS is a multi-agent operating system with 26 specialized agents organized into 5 categories. Each agent has a defined role, bounded responsibilities, and explicit collaboration interfaces.

| Category   | Count | Agents |
|------------|-------|--------|
| Governance | 7     | overseer, governor, router, planner, pm, operator, sentinel |
| Knowledge  | 4     | historian, librarian, summarizer, documenter |
| Technical  | 9     | architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer |
| Business   | 4     | strategist, marketer, seller, financier |
| Evolution  | 2     | improver, evaluator |

Agent definitions live under `.claude/agents/` in category subdirectories.

---

## Quick Orientation

- **Agent Registry:** `.claude/agents/REGISTRY.md` — canonical directory of all agents
- **Shared Rules:** `.claude/agents/shared/system-rules.md`
- **Active State:** `active/` — now.md, priorities.md, inbox.md, blockers.md
- **Indexes:** `core/indexes/` — project map, canonical files, context map
- **Standards:** `core/standards/` — naming, documentation, coding, review checklist
- **History:** `core/history/` — decisions, current state, timeline
- **Templates:** `core/templates/` — decision, spec, SOP, handoff

---

## Products

All products live under `products/`. Add your own projects here. Check for a README at the product root before making changes.

---

## How to Work

On receiving any request:

1. **Check context.** Read `active/now.md` and `active/priorities.md`.
2. **Classify the request.** Planning, technical, business, incident, or knowledge task?
3. **Route to appropriate agent(s).** Match the task to the right specialist.
4. **For complex tasks, follow the full pipeline:**
   - Plan (scope and approach)
   - Route (assign to specialists)
   - Execute (do the work)
   - QA (verify quality)
   - Review (check correctness and standards)
5. **Record outcomes.** Update active state files. Ensure decisions are captured.

For simple, single-domain requests, go directly to the relevant specialist.

---

## Agent Workflows

### Planning
Planner → Router → Governor validates → PM tracks → Specialists → QA → Reviewer → Documenter → Historian

### Technical
Architect → Engineer → QA → Security-Expert (if relevant) → Reviewer → DevOps (if deploy) → Documenter

### Business
Strategist → Marketer / Seller / Financier → Reviewer → Historian

### Incident
Debugger → Security-Expert (if security) → Engineer → QA → Historian

### Knowledge Management
Librarian → Summarizer → Documenter → Historian

---

## Coordination Rules

- **Overseer** resolves conflicts between agents or workflows.
- **Governor** enforces scope boundaries. No agent exceeds its role without Governor approval.
- **Sentinel** monitors for risk — security, process violations, technical debt. Can halt workflows.
- **PM** tracks progress across all active work. Task state changes go in `active/`.
- **Historian** records all significant decisions and outcomes.
- **Evaluator** periodically assesses system performance.
- **Improver** proposes changes based on evidence from Evaluator.

When in doubt about authority, consult `.claude/agents/REGISTRY.md`.

---

## File Conventions

| Purpose            | Location                     |
|--------------------|------------------------------|
| Current work state | `active/`                    |
| Standards          | `core/standards/`            |
| Indexes            | `core/indexes/`              |
| History            | `core/history/`              |
| Templates          | `core/templates/`            |
| Agent definitions  | `.claude/agents/<category>/` |
| Shared protocols   | `.claude/agents/shared/`     |
| Skills             | `.claude/skills/`            |
| Products           | `products/<name>/`           |
| Business           | `business/`                  |

All filenames use lowercase kebab-case. Uppercase only for system-level docs (CLAUDE.md, README.md, AGENTS.md, REGISTRY.md).

---

## System Rules

All agents follow the rules in `.claude/agents/shared/system-rules.md`. Read and follow them.

---

## Registry Reference

Use `.claude/agents/REGISTRY.md` as the canonical directory of agent roles. Do not invent, rename, or reassign agent responsibilities without updating the registry.

---

## Agent Teams — Required Patterns

When spawning agents, follow these rules strictly:

1. **Teammates that need file access MUST use `subagent_type: "general-purpose"`.**
   Custom agent types (debugger, qa, reviewer, architect, etc.) only get messaging and task tools as teammates — they cannot read, write, or edit files. Always spawn teammates as `general-purpose` and describe their role in the prompt instead.

2. **Use `mode: "auto"` for teammates** to avoid permission prompts that block execution.

3. **Use subagents for research/planning only.** Non-team subagents (via the Agent tool without a team) may not persist file writes. If you need files changed, either:
   - Use an agent team (teammates get full write access)
   - Use `isolation: "worktree"` for isolated file changes
   - Do the writes yourself from the main context after the subagent returns

4. **Agent discovery is flat.** Claude Code only finds agents at `.claude/agents/*.md` (top level). The category subdirectories have symlinks at the top level — do not remove them.

---

## Key Principles

- Every agent has bounded responsibilities. Respect those boundaries.
- Route work to the right agent rather than doing everything as a generalist.
- Record decisions and outcomes. The system learns from its history.
- Check current state before acting. Read `active/` files first.
- Prefer minimal, correct changes over sweeping rewrites.
- When uncertain, escalate. The governance agents exist for a reason.
