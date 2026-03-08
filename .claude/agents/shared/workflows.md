# Workflows

Standard workflow sequences. Not every task requires all steps — skip stages that don't apply. Conditional steps (marked "if") are only invoked when their condition is met.

## Planning Workflow
1. **Planner** — breaks down request into tasks, milestones, dependencies
2. **Router** — assigns tasks to appropriate specialist agents
3. **Governor** — validates scope and constraints
4. **Sentinel** — assesses risk profile of the plan (if plan touches production, security, or finances)
5. **Auditor** — pre-execution audit: reviews plan for blind spots, missing considerations, layer gaps
6. **Designer** — reviews UX impact (if plan affects user-facing interfaces)
7. **PM** — tracks progress, dependencies, deadlines
8. **Specialists** — execute assigned tasks
9. **QA** — verifies deliverables meet quality gates
10. **Reviewer** — checks correctness, standards, completeness
11. **Documenter** — writes or updates documentation
12. **Librarian** — catalogs new knowledge artifacts and updates indexes
13. **Historian** — records decisions, outcomes, lessons
14. **Evaluator** — measures project outcomes against goals (at project completion)

## Technical Workflow
1. **Architect** — plan approach
2. **DevOps** — validates deployability constraints (if architecture has infrastructure implications)
3. **Designer** — reviews UX/interface design (if frontend or user-facing)
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
16. **Historian** — records decisions

**Security interleaving rules:**
- Security-Expert is invoked **after planning** (threat model) and **after each major code pass** (code review)
- For small changes (see definition below), a single security pass after coding is sufficient
- Security-Expert **MUST** be invoked (not optional) for any work touching: authentication, cryptography, input validation, secrets, API boundaries, or data access

**Small change definition (security context):** Fewer than 3 files changed, AND does not touch authentication, cryptography, input validation, secrets management, API boundaries, or data access controls.

## Business Workflow
1. **Strategist** — defines business objective and approach
2. **Designer** — reviews brand/product impact (if deliverable affects product identity or customer experience)
3. **Marketer / Seller / Financier** — execute in their domains
4. **Sentinel** — flags financial or reputational risk (if significant exposure)
5. **Auditor** — post-execution audit: reviews deliverables against business objectives
6. **Reviewer** — validates alignment with strategy
7. **Operator** — creates or updates processes (if new operational processes result)
8. **Historian** — records decision and rationale
9. **Evaluator** — measures business outcomes against targets (at milestone completion)

## Incident Workflow
1. **Debugger** — diagnoses root cause
2. **Sentinel** — assesses blast radius and operational risk
3. **Security-Expert** — assesses security implications (if security-related)
4. **Engineer** — implements fix
5. **QA** — verifies fix, checks for regressions
6. **Auditor** — verifies fix fully addresses root cause, no secondary gaps (if significant incident)
7. **Operator** — updates processes (if incident reveals process gaps)
8. **Documenter** — records incident details for knowledge base
9. **Librarian** — catalogs incident knowledge and updates indexes
10. **Historian** — records incident, root cause, resolution

## Knowledge Workflow
1. **Librarian** — locates and organizes relevant information
2. **Summarizer** — distills into concise summaries
3. **Documenter** — produces formal documentation
4. **Polisher** — refines for publication (if external-facing)
5. **Reviewer** — quality check on final output
6. **Librarian** — catalogs final output and updates indexes
7. **Historian** — archives knowledge artifact and context

---

## Evolution Loop

The evolution loop connects Evaluator and Improver into a functioning feedback cycle. Without explicit triggers, these agents are inert.

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

### Improvement Approval Flow
1. **Improver proposes** — writes improvement with evidence to `active/improvements.md`
2. **User reviews** — approves, rejects, or requests changes
3. **Specialist implements** — appropriate agent makes the change
4. **Evaluator measures** — assesses impact of the change
5. **Archive** — outcome recorded in `core/history/improvements.md` with status (verified/ineffective)

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

### Auditor Checklist
When a pre-execution or post-execution audit is performed:
1. Record findings in the handoff to the next workflow step (PM, QA, or Planner)
2. For significant gaps, ensure Historian records the finding in `core/history/decisions.md`
3. For scope contraction, ensure PM updates `active/now.md` with what was dropped and why
**An audit is not complete until findings are communicated to the responsible agent.**

---

## When to Use Which Workflow
- **New feature or project:** Planning workflow
- **Code change or bug fix:** Technical workflow (or Incident if production issue)
- **Business decision:** Business workflow
- **Production incident:** Incident workflow
- **Documentation or knowledge task:** Knowledge workflow
- **System self-improvement:** Evolution loop (Evaluator + Improver)
- **Simple, bounded task:** Skip directly to the relevant specialist
