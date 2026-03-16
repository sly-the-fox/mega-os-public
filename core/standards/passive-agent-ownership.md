# Passive Agent File Ownership Standard

Passive agents are agents whose primary function is maintaining system state files rather than producing deliverables. They must follow the checklist pattern to ensure consistency.

## Passive Agents and Their Owned Files

| Agent | Owned Files | Checklist Location |
|-------|-------------|-------------------|
| Historian | `core/history/decisions.md`, `core/history/master-timeline.md`, `core/history/current-state.md`, `active/now.md`*, `active/priorities.md`* | `shared/workflows.md` → Historian Checklist |
| Librarian | `core/indexes/canonical-files.md`, `core/indexes/project-map.md`, `core/indexes/active-context-map.md` | `shared/workflows.md` → Librarian Checklist |
| PM | `active/now.md`*, `active/priorities.md`*, `active/inbox.md`, `active/blockers.md` | `shared/workflows.md` → PM Checklist |
| Operator | `business/operating/recurring-processes.md`, `business/operating/sop-*.md` | `shared/workflows.md` → Operator Checklist |
| Sentinel | `active/risks.md` | `shared/workflows.md` → Sentinel Checklist |
| Evaluator | `core/history/evaluations.md` | `shared/workflows.md` → Evaluator Checklist |
| Improver | `active/improvements.md`, `core/history/improvements.md` | `shared/workflows.md` → Improver Checklist |
| Auditor | `active/audits.md` | `shared/workflows.md` → Auditor Checklist |
| Custodian | `active/freshness-log.md` | `shared/workflows.md` → Custodian Checklist |
| Evaluator | `active/system-evaluation.md` | `shared/workflows.md` → Evaluator Checklist |

*Shared ownership between Historian and PM. PM updates first, then Historian records in history.

## Checklist Requirements

Every passive agent file ownership entry must specify:
1. **Which files** — exact paths, not categories
2. **Completeness rule** — "X is not Y until all Z files are updated"
3. **Trigger** — when the checklist is invoked (e.g., "when a decision is made")

## Adding a New Passive Agent

When adding an agent with file ownership responsibilities:
1. Define owned files in the agent's `.md` file under Responsibilities
2. Add a checklist section to `shared/workflows.md` under "Agent Checklists"
3. Update this standard with the new agent's row
4. Update `core/indexes/canonical-files.md` if new files are created
