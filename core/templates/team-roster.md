# Standing Team Roster

Declarative team definitions for session bootstrap. Create teams relevant to the current task — do not create all teams preemptively.

---

## Core Operations Team

**When:** Planning, Technical, or Incident tasks.

| Role | Agent Definition | subagent_type | mode |
|------|-----------------|---------------|------|
| Planner | `.claude/agents/governance/planner.md` | general-purpose | auto |
| Engineer | `.claude/agents/technical/engineer.md` | general-purpose | auto |
| QA | `.claude/agents/technical/qa.md` | general-purpose | auto |
| Reviewer | `.claude/agents/technical/reviewer.md` | general-purpose | auto |

**Prompt prefix:** "You are acting as [Role]. Read your agent definition at [path] and follow its responsibilities."

---

## Content Team

**When:** Content creation pipeline (articles, docs, deliverables).

| Role | Agent Definition | subagent_type | mode |
|------|-----------------|---------------|------|
| Writer | `.claude/agents/knowledge/writer.md` | general-purpose | auto |
| Editor | `.claude/agents/knowledge/editor.md` | general-purpose | auto |
| Polisher | `.claude/agents/knowledge/polisher.md` | general-purpose | auto |

**Prompt prefix:** "You are acting as [Role]. Read your agent definition at [path] and follow its responsibilities."

---

## Governance Team

**When:** Workflow-end verification, audits, risk assessment.

| Role | Agent Definition | subagent_type | mode |
|------|-----------------|---------------|------|
| Auditor | `.claude/agents/governance/auditor.md` | general-purpose | auto |
| Sentinel | `.claude/agents/governance/sentinel.md` | general-purpose | auto |
| Custodian | `.claude/agents/governance/custodian.md` | general-purpose | auto |
| Historian | `.claude/agents/knowledge/historian.md` | general-purpose | auto |

**Prompt prefix:** "You are acting as [Role]. Read your agent definition at [path] and follow its responsibilities."
