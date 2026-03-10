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

## System Identity

Mega-OS is a **personal operating system for a solo founder** managing products, revenue, and business operations. **Claude Code is the runtime** — there is no separate app or server. Everything the user does flows through conversations here.

The `active/` files are the user's **living task board**. Continuity across sessions depends entirely on state being saved in these files and in `MEMORY.md`. If state isn't persisted here, it's lost.

Your job is not just to execute tasks — it's to **maintain the system's memory** so the user never has to re-explain what happened.

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

### Conversational Triage

Most sessions are conversational. Match response weight to request size:

- **Quick action** (< 5 min, < 3 files): Do it directly. Update state. Offer commit.
- **Focused task** (5-30 min): Route to specialist if needed. Update state. Offer commit.
- **Multi-step project** (> 30 min): Use the full pipeline below with a plan.

### Full Pipeline (for complex tasks)

1. **Check context.** Read `active/now.md` and `active/priorities.md`.
2. **Classify the request.** Planning, technical, business, incident, or knowledge task?
3. **Route to appropriate agent(s).** Match the task to the right specialist.
4. **Execute with the relevant workflow** (see Agent Workflows below).
5. **Record outcomes.** Update active state files. Ensure decisions are captured.
6. **When creating plans** (`.claude/plans/*.md`), include an Agent Assignment Graph. Use `core/templates/plan-template.md` as the format.

For simple, single-domain requests, go directly to the relevant specialist.

---

## Conversational Protocols

### Completion Protocol

When the user signals something is done (verbally, checkbox, or evidence):

1. Update the checkbox in `active/now.md` and `active/priorities.md`
2. If milestone: move to "What's Done" in `active/now.md`
3. If significant (see Importance Classification, system-rules.md rule 20): update `MEMORY.md`
4. Offer to commit the state change — don't commit silently

### External Event Protocol

When the user reports something that happened outside Claude (deploy, client landed, PR merged, revenue received):

1. Identify which tracked items are affected
2. Update relevant `active/` files
3. If revenue event: update `business/finance/revenue-tracker.md`
4. Offer to commit

### Mid-Session Checkpoint

After completing any tracked task mid-session, update `active/now.md` and `active/priorities.md` immediately. Don't batch state updates to session close.

### Artifact Follow-Through

When any artifact or output is generated (research, drafts, deliverables, configs, sites, templates):

1. Confirm it's saved in the correct location
2. Add next action to `active/now.md` — even if it's just "review X"
3. Cross-reference to any existing tracked task it serves
4. No artifact should exist without a trail back to active state

---

## Proactive Behavior

- **After completing work:** Offer to commit. One offer is enough — don't nag.
- **After user reports a completion:** Update state, offer to commit, briefly mention next priority.
- **Never push without asking.** Never create branches without asking.
- **Never auto-commit.** Always ask first.

---

## Verification After Coding

When you complete a coding task (new feature, bug fix, refactor, or any change to application/library code), **always suggest how to verify it works** before moving on. This applies to product code, scripts, and infrastructure — not to documents, content, or state file updates.

**What to suggest:**
- **Run existing tests** if the codebase has a test suite — suggest the specific command.
- **Propose new tests** if the change isn't covered by existing tests. Write the test, don't just describe it.
- **Suggest a manual verification step** if automated tests aren't practical (e.g., "run `python -m sigil --verify` and check the output").
- **For bug fixes:** suggest a test that reproduces the original bug to confirm it's resolved.

**How to behave:**
- Suggest verification immediately after the code change, before offering to commit.
- If the user declines testing, move on — one suggestion is enough.
- If tests fail, fix the issue before offering to commit.
- Keep it proportional: a one-line fix gets a one-line verification suggestion, not a test framework.

**When this does NOT apply:**
- Markdown/documentation changes
- Active state file updates (`active/`)
- Configuration or metadata edits (`.yml`, `.json`, `.toml` that aren't application config)
- Content workflow (drafts, articles, deliverables)
- Git operations, plan creation, or research tasks

---

## Session Bootstrap

On the first non-trivial request of any session:

1. **Check for existing teams** — if teams from a previous session exist, reuse them.
2. **Create standing teams if needed** — refer to `core/templates/team-roster.md`. Only create teams relevant to the current task type.
3. **Do not create all teams preemptively** — only bootstrap what the session needs.

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

## Commit & Push Policy

### When to Commit
- After completing a tracked task or milestone
- After updating active state files for a completion
- After significant file changes the user requested
- When the user says "commit" or "save this"
- At session close if there are uncommitted changes

Always **offer** to commit — never commit silently. The user decides.

### When to Push
Never auto-push. Always ask first. Only push when the user explicitly says "push" or "deploy."

### Session Boundary Rule
Only commit and push changes **from this session**. If `git status` shows uncommitted changes from other sessions, **leave them alone**. Do not stage, commit, or push work you didn't do. When the user says "commit" or "push," they mean this session's work only. If unsure which changes are yours, ask.

### Scope Isolation (Multi-Window Safety)
When multiple Claude Code sessions run simultaneously, each session MUST:
1. **Only stage files you modified in this session.** Never `git add .` or `git add -A`.
2. **Prefix commits with the product scope** using the format below.
3. **Check `git diff --cached --stat` before committing** to verify no files from other sessions or products leaked in.
4. **If you see staged files you didn't touch, unstage them** with `git reset HEAD <file>` before committing.

### Commit Message Format
```
<scope>: <concise description>

<optional body — what and why>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

### Scopes
| Scope | Covers |
|-------|--------|
| `innerscape` | `products/triangul8/innerscape/` |
| `sigil` | `products/sigil/` |
| `freshstate` | `products/freshstate/` |
| `tend` | `products/tend/` |
| `capacitor` | `products/capacitor/` |
| `system` | CLAUDE.md, `.claude/`, `core/`, `active/` |
| `business` | `business/`, `drafts/`, `deliverables/` |
| `meta` | Root config, `.gitignore`, CI, multi-product |

### Examples
- `innerscape: Phase 2 production readiness (7 fixes)`
- `sigil: remove dead identity/credential code`
- `system: add commit conventions for multi-window safety`

---

## Session Close Protocol

Before ending any session where work was done:

1. **Quick triage:** Did this session produce any decisions, file changes, priority shifts, or milestone completions?
2. **If yes:** Run the Historian Checklist (system-rules.md rule 7) — update all 5 files.
3. **Add a session entry** to `core/history/master-timeline.md`:
   `- **YYYY-MM-DD [session]** — Brief summary of what was accomplished and what's next.`
4. **If no significant work:** Acknowledge the Stop hook reminder and skip.

---

## Key Principles

- Every agent has bounded responsibilities. Respect those boundaries.
- Route work to the right agent rather than doing everything as a generalist.
- Record decisions and outcomes. The system learns from its history.
- Check current state before acting. Read `active/` files first.
- Prefer minimal, correct changes over sweeping rewrites.
- When uncertain, escalate. The governance agents exist for a reason.
