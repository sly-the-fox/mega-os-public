# Workflows

Standard workflow sequences. Not every task requires all steps — skip stages that don't apply.

## Planning Workflow
1. **Planner** — breaks down request into tasks, milestones, dependencies
2. **Router** — assigns tasks to appropriate specialist agents
3. **Governor** — validates scope and constraints
4. **PM** — tracks progress, dependencies, deadlines
5. **Specialists** — execute assigned tasks
6. **QA** — verifies deliverables meet quality gates
7. **Reviewer** — checks correctness, standards, completeness
8. **Documenter** — writes or updates documentation
9. **Historian** — records decisions, outcomes, lessons

## Technical Workflow
1. **Architect** — defines or validates technical approach
2. **Engineer** — implements changes
3. **QA** — tests and verifies
4. **Security-Expert** — reviews security concerns (if relevant)
5. **Reviewer** — final review
6. **DevOps** — handles deployment (if needed)
7. **Documenter** — updates technical docs

## Business Workflow
1. **Strategist** — defines business objective and approach
2. **Marketer / Seller / Financier** — execute in their domains
3. **Reviewer** — validates alignment with strategy
4. **Historian** — records decision and rationale

## Incident Workflow
1. **Debugger** — diagnoses root cause
2. **Security-Expert** — assesses security implications (if security-related)
3. **Engineer** — implements fix
4. **QA** — verifies fix, checks for regressions
5. **Historian** — records incident, root cause, resolution

## Knowledge Workflow
1. **Librarian** — locates and organizes relevant information
2. **Summarizer** — distills into concise summaries
3. **Documenter** — produces formal documentation
4. **Historian** — archives knowledge artifact and context

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
1. `core/history/improvements.md` — record with evidence, proposal, and status
**An improvement is not tracked until it is recorded.**

---

## When to Use Which Workflow
- **New feature or project:** Planning workflow
- **Code change or bug fix:** Technical workflow (or Incident if production issue)
- **Business decision:** Business workflow
- **Production incident:** Incident workflow
- **Documentation or knowledge task:** Knowledge workflow
- **Simple, bounded task:** Skip directly to the relevant specialist
