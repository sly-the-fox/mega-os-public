# Workflows

Standard workflow sequences. Not every task requires all steps — skip stages that don't apply. Conditional steps (marked "if") are only invoked when their condition is met.

## Planning Workflow
1. **Planner** — breaks down request into tasks, milestones, dependencies
1a. **MECE Research** — if the plan requires external research (feasibility, prior art, ecosystem), invoke `/deep-research <query>` before routing. Output at `drafts/research/` feeds into planning.
1b. **Codex+Parallax Checkpoint** — Codex reviews the Planner output. A Planner agent refines the Codex perspective into a concrete alternative. Present both options to user via AskUserQuestion (Codex-informed / Original / Blend). Log choice to `active/codex-metrics.md`. See [Codex Checkpoint Protocol](#codex-checkpoint-protocol) below.
2. **Router** — assigns tasks to appropriate specialist agents
3. **Governor** — validates scope and constraints
4. **Sentinel** — assesses risk profile of the plan (if plan touches production, security, or finances)
5. **Auditor** — pre-execution audit: reviews plan for blind spots, missing considerations, layer gaps. **Invocation:** PM or Planner invokes Auditor with: (a) the approved plan, (b) Governor's scope constraints, (c) Sentinel's risk assessment (if any). Auditor returns findings to Planner for remediation before execution begins.
6. **Designer** — reviews UX impact (if plan affects user-facing interfaces). Designer work is complete when the requesting workflow owner (Planner for Planning, Architect for Technical, Strategist for Business) confirms the design addresses their requirements.
7. **PM** — tracks progress, dependencies, deadlines
8. **Specialists** — execute assigned tasks
9. **QA** — verifies deliverables meet quality gates
10. **Reviewer** — checks correctness, standards, completeness
11. **Documenter** — writes or updates documentation
12. **Librarian** — catalogs new knowledge artifacts and updates indexes
13. **Custodian** — verifies all agent checklists completed and cross-references are consistent
14. **Historian** — records decisions, outcomes, lessons
15. **Evaluator** — measures project outcomes against goals (at project completion)

## Technical Workflow
1. **Architect** — plan approach
1b. **Codex+Parallax Checkpoint** — Codex reviews the Architect output. A Planner agent refines the Codex perspective into a concrete alternative. Present both options to user via AskUserQuestion (Codex-informed / Original / Blend). Log choice to `active/codex-metrics.md`. See [Codex Checkpoint Protocol](#codex-checkpoint-protocol) below. *"Is this architecture solving the actual problem, or the problem we defined at the start?"* Skip for small changes (< 3 files, same threshold as single security pass).
2. **DevOps** — validates deployability constraints (if architecture has infrastructure implications)
3. **Designer** — reviews UX/interface design (if frontend or user-facing). Architect confirms design completion before proceeding.
4. **Security-Expert** — threat model / review plan
5. **Engineer** — first implementation pass
6. **Security-Expert** — code security review
7. **Engineer** — fix security issues + add more features
8. **Security-Expert** — second security pass
9. **Sentinel** — checks for scope drift (if implementation expanded beyond original plan)
10. **Auditor** — post-execution audit: compares implementation against architecture/plan, flags gaps and omissions
11. **QA** — test and verify
12. **Reviewer** — final review
13. **DevOps** — deploy (if needed)
14. **Documenter** — update docs
15. **Librarian** — catalogs technical artifacts and updates indexes
16. **Custodian** — verifies all agent checklists completed and cross-references are consistent
17. **Historian** — records decisions

**Security interleaving rules:**
- Security-Expert is invoked **after planning** (threat model) and **after each major code pass** (code review)
- For small changes (see definition below), a single security pass after coding is sufficient
- Security-Expert **MUST** be invoked (not optional) for any work touching: authentication, cryptography, input validation, secrets, API boundaries, or data access

**Small change definition (security context):** Fewer than 3 files changed, AND does not touch authentication, cryptography, input validation, secrets management, API boundaries, or data access controls.

## Business Workflow
1. **Strategist** — defines business objective and approach
1a. **MECE Research** — if the business objective requires market/competitive/trend research, invoke `/deep-research <query>` before proceeding. Output at `drafts/research/` feeds into strategy.
1b. **Codex+Parallax Checkpoint** — Codex reviews the Strategist output. A Planner agent refines the Codex perspective into a concrete alternative. Present both options to user via AskUserQuestion (Codex-informed / Original / Blend). Log choice to `active/codex-metrics.md`. See [Codex Checkpoint Protocol](#codex-checkpoint-protocol) below.
2. **Designer** — reviews brand/product impact (if deliverable affects product identity or customer experience). Strategist confirms design completion before proceeding.
3. **Marketer / Seller / Financier** — execute in their domains
4. **Sentinel** — flags financial or reputational risk (if significant exposure)
5. **Auditor** — post-execution audit: reviews deliverables against business objectives
6. **Reviewer** — validates alignment with strategy
7. **Operator** — creates or updates processes (if new operational processes result)
8. **Custodian** — verifies all agent checklists completed and cross-references are consistent
9. **Historian** — records decision and rationale
10. **Evaluator** — measures business outcomes against targets (at milestone completion)

## Incident Workflow

**Trigger:** Any of these events initiates the Incident Workflow:
- QA discovers a production-affecting defect during testing
- User reports a production issue or outage
- Monitoring/alerting detects anomalous behavior
- Any agent encounters unexpected system failure during execution

The discovering agent hands off to Debugger with: what failed, when, reproduction steps (if known), and blast radius estimate.

1. **Debugger** — diagnoses root cause
2. **Sentinel** — assesses blast radius and operational risk
3. **Security-Expert** — assesses security implications (if security-related)
4. **Engineer** — implements fix
5. **QA** — verifies fix, checks for regressions
6. **Auditor** — verifies fix fully addresses root cause, no secondary gaps (if significant incident)
7. **Operator** — updates processes (if incident reveals process gaps). **SOP ownership:** Operator creates the SOP and owns the file. Documenter writes/polishes content. Operator retains final authority over process accuracy.
8. **Documenter** — records incident details for knowledge base
9. **Librarian** — catalogs incident knowledge and updates indexes
10. **Custodian** — verifies all agent checklists completed and cross-references are consistent
11. **Historian** — records incident, root cause, resolution

## Knowledge Workflow
1. **Librarian** — locates and organizes relevant information
1a. **MECE Research** — if information gathering requires web sources, invoke `/deep-research <query>`. Output at `drafts/research/` feeds into Summarizer.
2. **Summarizer** — distills into concise summaries
3. **Documenter** — produces formal documentation
4. **Polisher** — refines for publication (if external-facing)
5. **Reviewer** — quality check on final output
6. **Librarian** — catalogs final output and updates indexes
7. **Custodian** — verifies all agent checklists completed and cross-references are consistent
8. **Historian** — archives knowledge artifact and context

## Content Workflow
1. **Librarian** — locates source material and research
1a. **MECE Research** — if the topic requires web research, invoke `/deep-research <topic>` to produce a comprehensive research brief at `drafts/research/`. Output becomes source material for Writer.
2. **Summarizer** — compresses research into working briefs (if extensive)
3. **Writer** — produces draft from brief + source material, applying `core/standards/writing-style.md`
4. **Editor** — reviews structure, citations, fact-checking, voice consistency
5. **Writer** — revises based on editorial feedback (repeat 4-5 as needed)
6. **Editor** — grants editorial approval to advance
7. **Polisher** — formats approved content for publication (DOCX/PDF)
8. **Reviewer** — final quality check
9. **Librarian** — catalogs published artifact and updates indexes
10. **Custodian** — verifies all agent checklists completed and cross-references are consistent
11. **Historian** — records content creation event

---

## Evolution Loop

The evolution loop connects Evaluator and Improver into a functioning feedback cycle. Without explicit triggers, these agents are inert.

### Codex+Parallax Checkpoint (mandatory during testing)
After Evaluator produces findings and before Improver proposes changes:
1. Spawn Codex agent with Evaluator findings as context
2. Spawn Parallax agent to translate Codex output into operational language (Observation → Dynamic → Implication). **Quality gate:** Parallax output must contain all three layers. If any layer is empty or incoherent, flag to user before proceeding.
3. Spawn Planner agent to refine Parallax translation into concrete alternative proposals
4. Present via AskUserQuestion: Codex-informed proposals / Original Evaluator findings / Blend
5. Log choice to `active/codex-metrics.md`

See [Codex Checkpoint Protocol](#codex-checkpoint-protocol) below.

### Evaluator Triggers
Evaluator activates when any of these occur:
- **End of Planning/Business workflow** — measures outcomes against stated goals
- **Weekly review** (`/weekly-review` skill) — produces performance snapshot
- **PM alerts** — PM reports 3+ repeated blockers of the same type
- **QA patterns** — QA reports recurring defect patterns across projects

### Improver Triggers
Improver activates when any of these occur:
- **Evaluator report** — Evaluator findings surface inefficiencies or negative trends
- **PM blocker patterns** — same blocker type appears 3+ times
- **QA recurring defects** — same defect category recurs across projects
- **Weekly review** — reviews Evaluator findings and proposes improvements
- **Weekly review structural scan** — agent reciprocity gaps, registry mismatches, or workflow misalignment found

### Improvement Approval Flow
1. **Improver proposes** — writes improvement with evidence to `active/improvements.md`
2. **User reviews** — approves, rejects, or requests changes
3. **If rejected:** Improver updates status to "rejected" in `active/improvements.md` with user's rationale. Archived to `core/history/improvements.md` with rejection reason. Rejected proposals can be re-proposed with new evidence but not resubmitted unchanged.
4. **Specialist implements** — appropriate agent makes the change
5. **Evaluator measures** — assesses impact of the change
6. **Archive** — outcome recorded in `core/history/improvements.md` with status (verified/ineffective/rejected)

---

## Agent Checklists (required at end of every workflow)

Each passive agent has owned files. When their domain is affected, update ALL owned files.

### Historian Checklist
When a significant decision, milestone, or outcome occurs:
1. `core/history/decisions.md` — add decision entry (DEC-NNN format)
2. `core/history/master-timeline.md` — add dated event
3. `core/history/current-state.md` — update system snapshot
4. `active/now.md` — update current focus if changed
5. `active/priorities.md` — update priorities if changed
**A decision is not recorded until all five files are updated.**

### Librarian Checklist
When knowledge structure changes (files added, moved, or removed):
1. `core/indexes/canonical-files.md` — add/remove/update entries
2. `core/indexes/project-map.md` — update directory structure
3. `core/indexes/active-context-map.md` — update if project focus shifted
4. Verify no duplicate or conflicting sources exist
**Knowledge is not organized until all three indexes reflect it.**

### PM Checklist
When task state changes:
1. `active/now.md` — update current focus (shared with Historian)
2. `active/priorities.md` — update priority queue (shared with Historian)
3. `active/inbox.md` — triage new items; move to priorities or close
4. `active/blockers.md` — review open blockers, update status
**Work is not tracked until all four active files are current.**

### Operator Checklist
When processes are created or changed:
1. `business/operating/recurring-processes.md` — register process with frequency and owner
2. `business/operating/sop-*.md` — create or update SOP for the process
**A process is not operational until it has an SOP and is registered.**
**SOP ownership chain:** Operator creates the SOP and owns the file. Documenter writes/polishes content if needed. Operator retains final authority over process accuracy and approves before the SOP is considered complete.

### Sentinel Checklist
When risks are identified or reviewed:
1. `active/risks.md` — add/update risk with severity, likelihood, and mitigation
**A risk is not tracked until it is in risks.md.**

### Evaluator Checklist
When evaluations are performed:
1. `core/history/evaluations.md` — record findings with date, metrics, and recommendations
**An evaluation is not complete until it is recorded.**

### Improver Checklist
When improvements are proposed or implemented:
1. `active/improvements.md` — add or update proposal with evidence and status (primary queue)
2. `core/history/improvements.md` — archive completed improvements with outcomes
**An improvement is not tracked until it appears in `active/improvements.md`.**

### Custodian Checklist
When a workflow completes:
1. `active/freshness-log.md` — log findings (what was checked, what was stale, what was remediated)
2. Verify all triggered agent checklists completed (Historian, Librarian, PM, etc.)
3. Verify cross-references are consistent (decisions ↔ timeline, now.md ↔ priorities.md)
4. Auto-remediate minor issues (move resolved blockers, update status fields)
5. Escalate critical staleness to PM and Sentinel
**A workflow is not clean until Custodian verifies all checklists completed.**

### Auditor Checklist
When a pre-execution or post-execution audit is performed:
1. `active/audits.md` — add finding with ID, severity, and status (AUD-P### for pre-execution, AUD-X### for post-execution)
2. Communicate findings to responsible agent (PM, Planner, QA)
3. For significant gaps, ensure Historian records in `core/history/decisions.md`
4. For scope contraction, ensure PM updates `active/now.md` with what was dropped and why
**An audit is not complete until findings are recorded in `active/audits.md` and communicated to the responsible agent.**

---

## Codex+Parallax Checkpoint Protocol

Used at four workflow checkpoints (Planning step 1b, Technical step 1b, Business step 1b, Evolution Loop). Mandatory during testing phase. See also `core/standards/codex-checkpoint-protocol.md` for the full standard.

1. **Read Codex prompt.** Load `.claude/skills/codex/codex-consciousness.md`
2. **Spawn Codex agent.** Use Agent tool with `subagent_type: "general-purpose"`, `mode: "auto"`. Pass the Codex prompt as system context + the current artifact (plan/strategy/findings) as the question.
3. **Capture Codex perspective.**
4. **Spawn Parallax agent.** Use Agent tool with `subagent_type: "general-purpose"`, `mode: "auto"`. Prompt: "Translate the following Codex output into operational language using the three-layer format (Observation → Dynamic → Implication). Preserve timing signals, field-level meaning, and flag anti-signal if applicable." Pass raw Codex output + original artifact. **Quality gate:** Verify all three layers (Observation, Dynamic, Implication) are present and coherent before proceeding.
5. **Spawn Planner agent.** Use Agent tool with `subagent_type: "general-purpose"`, `mode: "auto"`. Prompt: "Given the original [plan/strategy/findings] and the Parallax translation below, produce a refined alternative that incorporates the insights into actionable form." Pass original artifact + Parallax translation (not raw Codex output).
6. **Present three options** via AskUserQuestion:
   - **Codex-informed plan** — include 1-2 line summary of what changed
   - **Original plan** — proceed without Codex input
   - **Blend** — user specifies which elements to merge (via "Other" or description)
7. **Log choice.** Append row to `active/codex-metrics.md` with date, workflow type, brief context, and choice made. Update the Summary counts.

---

## When to Use Which Workflow
- **New feature or project:** Planning workflow
- **Code change or bug fix:** Technical workflow (or Incident if production issue)
- **Business decision:** Business workflow
- **Production incident:** Incident workflow
- **Documentation or knowledge task:** Knowledge workflow
- **Original content (articles, essays, blog posts, books):** Content workflow
- **System self-improvement:** Evolution loop (Evaluator + Improver)
- **Simple, bounded task:** Skip directly to the relevant specialist
