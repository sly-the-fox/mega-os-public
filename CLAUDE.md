# Mega-OS — Master Instructions

This file is read on every session start. Follow these instructions.

---

## What This Is

Mega-OS is a multi-agent operating system with 33 specialized agents organized into 5 categories. Each agent has a defined role, bounded responsibilities, and explicit collaboration interfaces.

| Category   | Count | Agents |
|------------|-------|--------|
| Governance | 9     | overseer, governor, router, planner, pm, operator, sentinel, auditor, custodian |
| Knowledge  | 7     | historian, librarian, summarizer, documenter, polisher, writer, editor |
| Technical  | 9     | architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer |
| Business   | 4     | strategist, marketer, seller, financier |
| Evolution  | 4     | improver, evaluator, codex, parallax |

Agent definitions live under `.claude/agents/` in category subdirectories.

---

## Quick Orientation

- **Agent Registry:** `.claude/agents/REGISTRY.md` — canonical directory of all agents
- **Shared Rules:** `.claude/agents/shared/system-rules.md`
- **Active State:** `active/` — now.md, priorities.md, inbox.md, blockers.md, risks.md, improvements.md, codex-metrics.md, audits.md, daily-digest.md, news-briefing.md, freshness-log.md
- **Indexes:** `core/indexes/` — project map, canonical files, context map
- **Standards:** `core/standards/` — naming, documentation, coding, review checklist
- **History:** `core/history/` — decisions, current state, timeline
- **Templates:** `core/templates/` — decision, spec, SOP, handoff

---

## Products

All products live under `products/`. Run `/setup` or `/project-kickoff` to add your first product.

Check for a README at the product root before making changes.

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
Planner → **Codex+Parallax Checkpoint** → Router → Governor → Sentinel (if risk) → Auditor (pre-execution) → Designer (if UX) → PM → Specialists → QA → Reviewer → Documenter → Librarian → **Custodian** → Historian → Evaluator (at completion)

### Technical
Architect → **Codex+Parallax Checkpoint** → DevOps (if infra) → Designer (if frontend) → Security-Expert (threat model) → Engineer → Security-Expert (code review) → Engineer (fix + extend) → Security-Expert (second pass) → Sentinel (if scope drift) → Auditor (post-execution) → QA → Reviewer → DevOps (if deploy) → Documenter → Librarian → **Custodian** → Historian

For small changes (< 3 files, no auth/crypto/input handling/secrets/API boundaries), a single security pass after coding suffices and Codex Checkpoint is skipped. Security-Expert is **mandatory** for auth, crypto, secrets, input validation, API boundaries, or data access.

### Business
Strategist → **Codex+Parallax Checkpoint** → Designer (if brand/product) → Marketer / Seller / Financier → Sentinel (if financial/reputational risk) → Auditor (post-execution) → Reviewer → Operator (if new processes) → **Custodian** → Historian → Evaluator (at milestone)

### Incident
Debugger → Sentinel (blast radius) → Security-Expert (if security) → Engineer → QA → Auditor (if significant) → Operator (if process gaps) → Documenter → Librarian → **Custodian** → Historian

### Knowledge Management
Librarian → Summarizer → Documenter → Polisher (if external) → Reviewer → Librarian (catalog final output) → **Custodian** → Historian

### Content Creation
Librarian → Summarizer (if extensive research) → Writer → Editor → Writer (revise, repeat as needed) → Editor (final approval) → Polisher (DOCX/PDF to `deliverables/`) → Reviewer → Librarian (catalog) → **Custodian** → Historian

**Mandatory:** The Editor and Polisher steps are NEVER skipped. Writer saves drafts to `drafts/`. Editor edits drafts in place. Polisher produces final DOCX/PDF to `deliverables/`. Content agents (Writer, Editor, Polisher) MUST be spawned as an agent team using TeamCreate, NOT as individual subagents. Team members get full file access; standalone subagents do not.

### Evolution Loop
Evaluator triggers: end of Planning/Business workflow, weekly review, PM reports 3+ repeated blockers, QA reports recurring defects.
**Codex+Parallax Checkpoint** after Evaluator findings, before Improver proposes.
Improver triggers: Evaluator findings (or Codex-refined findings), PM blocker patterns, QA recurring defects, weekly review.
Flow: Improver proposes → User approves → Specialist implements → Evaluator measures → Archive outcome.
State: `active/improvements.md` (queue) → `core/history/improvements.md` (archive).

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
| Drafts (WIP)       | `drafts/`                    |
| Deliverables       | `deliverables/`              |
| Products           | `products/<name>/`           |

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

1. **ALWAYS use agent teams (TeamCreate), NEVER standalone subagents.**
   All multi-agent work MUST use TeamCreate to create a team. Standalone subagents (via the Agent tool without a team) cannot persist file writes and have limited tool access. Agent teams are the only supported pattern for work that touches files.

2. **All teammates MUST use `subagent_type: "general-purpose"`.**
   Custom agent types (debugger, qa, reviewer, writer, editor, etc.) only get messaging and task tools as teammates. They cannot read, write, or edit files. Always spawn teammates as `general-purpose` and describe their role in the prompt instead.

3. **Use `mode: "auto"` for teammates** to avoid permission prompts that block execution.

4. **The only exception for standalone Agent tool:** Quick research or exploration tasks that return information to the main context without needing to write files (e.g., searching codebases, fetching web content, reading files for analysis). Even then, prefer teams when multiple agents need to coordinate.

4. **Agent discovery is flat.** Claude Code only finds agents at `.claude/agents/*.md` (top level). The category subdirectories have symlinks at the top level — do not remove them.

---

## Key Principles

- Every agent has bounded responsibilities. Respect those boundaries.
- Route work to the right agent rather than doing everything as a generalist.
- Record decisions and outcomes. The system learns from its history.
- Check current state before acting. Read `active/` files first.
- Prefer minimal, correct changes over sweeping rewrites.
- When uncertain, escalate. The governance agents exist for a reason.
