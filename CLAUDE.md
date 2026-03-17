# Mega-OS — Master Instructions

This file is read on every session start. Follow these instructions.

---

## What This Is

Mega-OS is a multi-agent operating system with 39 specialized agents organized into 5 categories. Each agent has a defined role, bounded responsibilities, and explicit collaboration interfaces.

| Category   | Count | Agents |
|------------|-------|--------|
| Governance | 9     | overseer, governor, router, planner, pm, operator, sentinel, auditor, custodian |
| Knowledge  | 7     | historian, librarian, summarizer, documenter, polisher, writer, editor |
| Technical  | 11    | architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer, visual-designer, api-designer |
| Business   | 8     | strategist, marketer, seller, financier, proposal-writer, client-manager, content-strategist, growth-hacker |
| Evolution  | 4     | improver, evaluator, coherence, parallax |

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
- **Active State:** `active/` — now.md, priorities.md, inbox.md, blockers.md, risks.md, improvements.md, coherence-metrics.md, audits.md, daily-digest.md, news-briefing.md, freshness-log.md
- **Active Index:** `active/index.json` — machine-readable manifest with load priorities
- **Indexes:** `core/indexes/` — project map, canonical files, context map
- **Archive:** `archive/` — aged content organized by type and ISO week (`archive/index.json` is the manifest)
- **Standards:** `core/standards/` — naming, documentation, coding, review checklist
- **History:** `core/history/` — decisions, current state, timeline
- **Templates:** `core/templates/` — decision, spec, SOP, handoff

---

## Products

<!-- USER CONFIG START: products -->
All products live under `products/`. Run `/setup` or `/project-kickoff` to add your first product.

Check for a README and CLAUDE.md at the product root before making changes. Product-level CLAUDE.md files override general standards for that product.
<!-- USER CONFIG END: products -->

---

## How to Work

### Conversational Triage

Most sessions are conversational. Match response weight to request size:

- **Quick action** (< 5 min, < 3 files modified): Do it directly. Update state. Offer commit.
- **Focused task** (5-30 min): Route to specialist if needed. Update state. Offer commit.
- **Multi-step project** (> 30 min): Use the full pipeline below with a plan.

### User-Voice Content Gate

Before generating ANY text the user might post, publish, or send as their own:

1. Read `core/standards/writing-style.md` (including platform-specific adaptations)
2. Apply the style guide to your output
3. For Reddit: also read `style-samples/reddit-casual.md`
4. No em dashes. No generic AI voice. Must sound like the user.

This applies even for "quick action" responses. A suggested reply IS user-voice content. A code review comment is not. The test: "Will this text be published or sent as if written by the user?" If yes, apply the gate.

This does NOT require spawning Writer/Editor agents for short-form content. Apply the style guide directly in your response. The full Content Workflow (Writer → Editor → Polisher) is for long-form content (articles, essays, newsletters).

### Full Pipeline (for complex tasks)

1. **Check context.** Read `active/now.md` and `active/priorities.md`.
2. **Classify the request.** Planning, technical, business, incident, or knowledge task?
3. **Route to appropriate agent(s).** Match the task to the right specialist.
4. **Execute with the relevant workflow** (see Agent Workflows below).
5. **Record outcomes.** Update active state files. Ensure decisions are captured.
6. **When creating plans** (`.claude/plans/*.md`), include an Agent Assignment Graph. Use `core/templates/plan-template.md` as the format.

For simple, single-domain requests, use a lightweight team — see the Lightweight Team Protocol in `workflows.md`. This ensures quality gates (security review, editor pass, Coherence checkpoint) still apply even for small tasks, while skipping heavy governance overhead.

### Selective Loading

The SessionStart hook loads `active/index.json` plus "always" priority files. Use the index to decide what else to load:

- **`on_request`:** Load when the user's request touches the file's topics.
- **`on_demand`:** Load only when explicitly needed.
- **Archive recall:** When information isn't in active state, check `archive/index.json` by time scope first. See memory/archive_recall.md for the full protocol.

### When Something Fails

If a workflow step fails (command error, test failure, build break, agent error):

1. **Diagnose** the root cause — don't blindly retry.
2. **Fix and retry once.** If it fails again, try an alternative approach.
3. **Escalate** to Debugger (for technical) or Overseer (for workflow/coordination) if still blocked.
4. **Never silently skip a failed step** — it will cascade downstream.

---

## Conversational Protocols

### Completion Protocol

When the user signals something is done (verbally, checkbox, or evidence):

1. Update the checkbox in `active/now.md` and `active/priorities.md`
2. If milestone: move to "What's Done" in `active/now.md`
3. If significant — impacts architecture, revenue, or product direction (see system-rules.md rule 20): update `MEMORY.md`
4. Offer to commit the state change — don't commit silently

### External Event Protocol

When the user reports something that happened outside Claude (deploy, client landed, PR merged, revenue received):

1. Identify which tracked items are affected
2. Update relevant `active/` files
3. If revenue event: update `business/finance/revenue-tracker.md`
4. Offer to commit

### Mid-Session Checkpoint

After completing any tracked task mid-session, update `active/now.md` and `active/priorities.md` immediately. Don't batch state updates to session close.

### Contact Follow-Up Completion

When the user reports a contact touch (called, emailed, messaged, met):

1. Update `Last Contact` to today in `business/network/contacts.md`
2. Calculate next `Follow-Up`: today + Cadence (or platform default if Cadence is blank — see comment block in `core/templates/network-contacts-template.md`)
3. Update `Next Action` based on outcome
4. If declined: move to the Declined / Do Not Contact table, clear Follow-Up
5. If parking: set Follow-Up to `—`
6. Confirm the next follow-up date. Let user override. Offer to commit.

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

1. **Create standing teams as needed** — refer to `core/templates/team-roster.md`. Only create teams relevant to the current task type.
2. **Do not create all teams preemptively** — only bootstrap what the session needs.

---

## Agent Workflows

Workflow summaries are below. Full definitions with triggers, severity classification, and detailed steps are in `.claude/agents/shared/workflows.md`.

### Planning
Planner → MECE Research (if needed) → **Coherence+Parallax Checkpoint** → Router → Governor → Sentinel (if risk) → Auditor (pre-execution) → Designer (if UX) → Visual Designer (if frontend/UI) → PM → Specialists → QA → Reviewer → Documenter → Librarian → **Custodian** → Historian → Evaluator (at completion)

### Technical
Architect → API-Designer (if API) → **Coherence+Parallax Checkpoint** → DevOps (if infra) → Designer (if frontend) → Security-Expert (threat model) → Engineer → Security-Expert (code review) → Engineer (fix + extend) → Visual Designer (if frontend/UI) → Security-Expert (second pass) → Sentinel (if scope drift) → Auditor (post-execution) → QA → Reviewer → DevOps (if deploy) → Documenter → Librarian → **Custodian** → Historian

For small changes (< 3 files modified, no auth/crypto/input handling/secrets/API boundaries), a single security pass after coding suffices and Coherence Checkpoint is skipped. Security-Expert is **mandatory** for auth, crypto, secrets, input validation, API boundaries, or data access. Parallelizable steps (Security+Engineer, Auditor+QA) may use worktree isolation — see workflows.md.

For all technical work, follow `core/standards/coding-standards.md`. Reviewer uses `core/standards/review-checklist.md` as the gate checklist.

### Business
Strategist → MECE Research (if needed) → **Coherence+Parallax Checkpoint** → Designer (if brand/product) → Marketer / Seller / Financier → Sentinel (if financial/reputational risk) → Auditor (post-execution) → Reviewer → Operator (if new processes) → **Custodian** → Historian → Evaluator (at milestone)

### Incident
Debugger → Sentinel (blast radius) → Security-Expert (if security) → Engineer → QA → Auditor (if significant) → Operator (if process gaps) → Documenter → Librarian → **Custodian** → Historian

### Knowledge Management
Librarian → MECE Research (if needed) → Summarizer → Documenter → Polisher (if external) → Reviewer → Librarian (catalog final output) → **Custodian** → Historian

### Content Creation
Librarian → Summarizer (if extensive research) → Writer → Editor → Writer (revise, repeat as needed) → Editor (final approval) → Polisher (DOCX/PDF to `deliverables/`) → Reviewer → Librarian (catalog) → **Custodian** → Historian

**Mandatory:** The Editor and Polisher steps are NEVER skipped. Writer saves drafts to `drafts/`. Editor edits drafts in place. Polisher produces final DOCX/PDF to `deliverables/`. Content agents (Writer, Editor, Polisher) MUST be spawned as an agent team using TeamCreate, NOT as individual subagents. Team members get full file access; standalone subagents do not.

### All Generated Content — Style Enforcement

**Any text generated for the user's voice** — regardless of length or format — MUST follow `core/standards/writing-style.md`. This includes but is not limited to:

- Social media posts (Twitter/X, LinkedIn, Discord, TikTok, Reddit, HN)
- Comment replies and responses
- Bios, taglines, and profile copy
- Email drafts
- Short-form marketing copy
- Any text that will be published or sent as if written by the user

**For short-form content** (social posts, comment replies, bios, short copy): Apply the writing style guide directly. At minimum, the Writer agent drafts and the Editor agent reviews before presenting to the user. No em dashes. No generic AI voice. Must sound like the user.

**For long-form content** (articles, blog posts, essays, newsletters): Use the full Content Creation workflow above (Writer → Editor → Polisher).

**If in doubt, run it through the flow.** Never generate publishable text in a raw response without applying the style guide.

**Trigger:** See "User-Voice Content Gate" in the Conversational Triage section above. That gate ensures style enforcement fires BEFORE generation, not as a post-hoc check.

### Evolution Loop
Evaluator triggers: end of Planning/Business workflow, weekly review, PM reports 3+ repeated blockers, QA reports recurring defects.
**Coherence+Parallax Checkpoint** after Evaluator findings, before Improver proposes.
Improver triggers: Evaluator findings (or Coherence-refined findings), PM blocker patterns, QA recurring defects, weekly review.
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

## Data Classification

Mega-OS has a public distribution (framework) and private user data. This classification governs what syncs to the public repo via `engineering/scripts/sync-to-public.sh`.

| Category | Paths | Syncs to public? |
|----------|-------|------------------|
| Framework | `.claude/agents/`, `.claude/skills/`, `.claude/hooks/`, `.claude/settings.json`, `core/standards/`, `core/templates/`, `engineering/scripts/`, `CLAUDE.md`, `AGENTS.md`, `README.md`, `GETTING_STARTED.md`, `.gitignore`, `LICENSE` | YES |
| User data | `active/`, `business/`, `products/`, `drafts/`, `deliverables/`, `archive/`, `core/history/`, `core/indexes/`, `style-samples/`, `.claude/projects/*/memory/` | NEVER |
| Sensitive | `.env*`, `*.pem`, `*.key`, `sessions.json` | NEVER (gitignored) |

**Rule:** When creating a new file, if it contains personal data (names, emails, revenue, client info, project-specific state), it belongs in user data paths. If it's a reusable system component (agent, skill, standard, template), it belongs in framework paths. When uncertain, default to user data.

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
| Archived reports   | `archive/reports/YYYY-WNN/`  |

All filenames use lowercase kebab-case. Uppercase only for system-level docs (CLAUDE.md, README.md, AGENTS.md, REGISTRY.md).

**Report archival:** Skills that overwrite `active/` report files (improvement-audit, daily-digest, workflow-review, news-briefing) auto-archive the previous version to `archive/reports/YYYY-WNN/YYYY-MM-DD-<type>.md` before writing. Use `engineering/scripts/archive-report.sh` for the archival step.

---

## System Rules

All agents follow the rules in `.claude/agents/shared/system-rules.md`. Read and follow them.

---

## Registry Reference

Use `.claude/agents/REGISTRY.md` as the canonical directory of agent roles. Do not invent, rename, or reassign agent responsibilities without updating the registry.

---

## Agent Teams — Required Patterns

When spawning agents, follow these rules strictly:

1. **ALWAYS use agent teams (TeamCreate), NEVER standalone subagents — except worktree-isolated agents.**
   All multi-agent work MUST use TeamCreate to create a team. Standalone subagents (via the Agent tool without a team) cannot persist file writes and have limited tool access. Agent teams are the only supported pattern for work that touches files.
   **Exception:** Standalone agents with `isolation: "worktree"` CAN write files safely in their own git worktree. Use for parallelizable, independent work (audits, builds, tests). See system-rules.md rule 27.

2. **All teammates MUST use `subagent_type: "general-purpose"`.**
   Custom agent types (debugger, qa, reviewer, writer, editor, etc.) only get messaging and task tools as teammates. They cannot read, write, or edit files. Always spawn teammates as `general-purpose` and describe their role in the prompt instead.

3. **Use `mode: "auto"` for teammates** to avoid permission prompts that block execution.

4. **Exceptions for standalone Agent tool:** (a) Quick research or exploration tasks that return information to the main context without needing to write files (e.g., searching codebases, fetching web content, reading files for analysis). This includes Coherence and Parallax checkpoint calls, which are read-only perspective checks. (b) Worktree-isolated agents for parallel, independent work (spawned with `isolation: "worktree"`). Even then, prefer teams when agents need to coordinate mid-task.

5. **Agent discovery is flat.** Claude Code only finds agents at `.claude/agents/*.md` (top level). The category subdirectories have symlinks at the top level — do not remove them.

6. **File write fallback for content generation.** When generating content that must be saved to files, prefer writing files directly from the main context rather than delegating writes to subagents. If using subagents for research or drafting, collect their output and perform all Write calls in the main context. If a file write fails, retry once. If it fails again, include the full content inline in the response so nothing is silently lost.

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
Only commit and push changes **from this session**. If `git status` shows uncommitted changes from other sessions, **leave them alone**. Do not stage, commit, or push work you didn't do. When the user says "commit" or "push," they mean this session's work only. If unsure which changes are yours, ask. Changes merged back from worktree agents spawned in this session are considered this session's work and are eligible for commit.

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
<!-- USER CONFIG START: commit-scopes -->
| Scope | Covers |
|-------|--------|
| `<product-name>` | `products/<product-name>/` |
| `system` | CLAUDE.md, `.claude/`, `core/`, `active/` |
| `business` | `business/`, `drafts/`, `deliverables/` |
| `meta` | Root config, `.gitignore`, CI, multi-product |
<!-- USER CONFIG END: commit-scopes -->

### Examples
- `myapp: add user authentication flow`
- `system: add commit conventions for multi-window safety`
- `business: update revenue tracker with Q1 numbers`

---

## Session Close Protocol

Before ending any session where work was done:

1. **Quick triage:** Did this session produce any decisions, file changes, priority shifts, or milestone completions?
2. **If yes:** Run the Historian Checklist (system-rules.md rule 7) — update all 5 files.
3. **Add a session entry** to `core/history/master-timeline.md`:
   `- **YYYY-MM-DD [session]** — Brief summary of what was accomplished and what's next.`
4. **Memory curation:** Before closing, scan the session for:
   - **New decisions or architecture choices** → add to `context-journal.md` (or MEMORY.md if cross-session relevant)
   - **User preferences or corrections** → save as user/feedback memory in MEMORY.md
   - **Lessons learned or deferred work** → add to `context-journal.md` with enough context to be useful next session
5. **If no significant work:** Acknowledge the Stop hook reminder and skip.

---

## Key Principles

- Every agent has bounded responsibilities. Respect those boundaries.
- Route work to the right agent rather than doing everything as a generalist.
- Record decisions and outcomes. The system learns from its history.
- Check current state before acting. Read `active/` files first.
- Prefer minimal, correct changes over sweeping rewrites.
- When uncertain, escalate. The governance agents exist for a reason.
