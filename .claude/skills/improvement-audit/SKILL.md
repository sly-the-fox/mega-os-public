---
name: improvement-audit
description: Deep daily improvement audit — MECE-decomposed local codebase scan through auditor four-layer lens, improver distillation, and Coherence reading. Auto-rotates focus area by day of week.
invocation: /improvement-audit
user_invocable: true
arguments: "[--day mon|tue|wed|thu|fri|sat|sun] [--no-coherence]"
---

# Daily Improvement Audit

Deep MECE-decomposed audit of one system section per day, rotating through all 7 areas weekly. Uses parallel standalone Agent calls for codebase exploration, applies the Auditor's four-layer analysis, distills findings via the Improver, and appends a Coherence+Parallax reading.

> **Compatibility:** This skill is compatible with headless `claude -p` mode. It uses standalone Agent calls, not TeamCreate.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--day` | auto (system day) | Override which day's focus area to audit |
| `--no-coherence` | false | Skip the Coherence+Parallax reading |

## Phase 0: Determine Focus Area

**Exclusions:** Never scan `archive/` — archived content is frozen and not subject to improvement proposals.

Detect the current day of week (or use `--day` override). Select the focus area and MECE partitions from the rotation table:

| Day | Focus Area | Axis | Partitions |
|-----|-----------|------|------------|
| Mon | Governance & Operations | layer | 5 |
| Tue | Knowledge & Memory | concern | 5 |
| Wed | Technical Infrastructure | layer | 6 |
| Thu | Products & Revenue | directory | 6 |
| Fri | Business Operations | concern | 5 |
| Sat | Evolution & Improvement | concern | 5 |
| Sun | Integration & Health | concern | 5 |

Print to console: "Improvement Audit: [Day] — [Focus Area] ([N] partitions, [axis] axis)"

### Partition Definitions

#### Monday: Governance & Operations (`layer` axis)

| # | Partition | Scope | Key Files |
|---|-----------|-------|-----------|
| 1 | Orchestration Layer | Overseer, Governor, Router — routing, authority, conflict resolution | `.claude/agents/governance/{overseer,governor,router}.md` |
| 2 | Execution Management | Planner, PM, Operator — planning, tracking, process management | `.claude/agents/governance/{planner,pm,operator}.md` |
| 3 | Verification Layer | Sentinel, Auditor, Custodian — risk, completeness, freshness | `.claude/agents/governance/{sentinel,auditor,custodian}.md` |
| 4 | Shared Protocols | System rules, workflows, collaboration, escalation, handoff | `.claude/agents/shared/` (all 7 files) |
| 5 | Standards & SOPs | Coding, naming, documentation, review checklist, SOPs | `core/standards/`, `business/operating/sop-*.md` |

#### Tuesday: Knowledge & Memory (`concern` axis)

| # | Partition | Scope | Key Files |
|---|-----------|-------|-----------|
| 1 | Agent Definitions | 7 knowledge agents — roles, boundaries, collaboration links | `.claude/agents/knowledge/` |
| 2 | History & Decisions | Decision log, timeline, current-state, evaluations archive | `core/history/` |
| 3 | Indexes & Maps | Project map, canonical files, context map — accuracy and freshness | `core/indexes/` |
| 4 | Living Memory | MEMORY.md accuracy, freshness tracking, session injection | `MEMORY.md`, `active/freshness-log.md`, `active/freshstate-report.md` |
| 5 | Documentation Standards | Are knowledge agents producing docs per standards? Cross-refs valid? | `core/standards/documentation-standards.md`, templates |

#### Wednesday: Technical Infrastructure (`layer` axis)

| # | Partition | Scope | Key Files |
|---|-----------|-------|-----------|
| 1 | Architecture & Design | Architect, Designer agents — structural decisions, UX patterns | `.claude/agents/technical/{architect,designer}.md` |
| 2 | Build & Deploy | Engineer, Executor, DevOps — implementation, deployment, infra | `.claude/agents/technical/{engineer,executor,devops}.md` |
| 3 | Quality & Debug | QA, Reviewer, Debugger — testing, review gates, incident response | `.claude/agents/technical/{qa,reviewer,debugger}.md` |
| 4 | Security Posture | Security-Expert agent, security standards, threat model coverage | `.claude/agents/technical/security-expert.md`, security-related standards |
| 5 | Engineering Scripts | Automation scripts, shared libraries, tooling | `engineering/` |
| 6 | Code Standards Compliance | Coding standards, review checklist — are they current and enforced? | `core/standards/coding-standards.md`, `core/standards/review-checklist.md` |

#### Thursday: Products & Revenue (`directory` axis)

| # | Partition | Scope | Key Files |
|---|-----------|-------|-----------|
| 1 | Sigil | Spec, public repo, SDK, MCP server, tests, marketing, adoption | `products/sigil/` |
| 2 | freshstate | Spec, CLI, MCP server, registry submissions, CI | `products/freshstate/` |
| 3 | Capacitor | Spec, app code, landing page, deployment status | `products/capacitor/` |
| 4 | Consulting & Templates | Aequilibris site, service docs, template packages | `products/aequilibris-group/`, `products/templates/` |
| 5 | Revenue & Finance | Revenue tracker, financial records, pricing rationale | `business/finance/`, `business/strategy/revenue-top-10.md` |
| 6 | Marketing & Adoption | Content calendar, adoption metrics, launch materials | `business/marketing/` |

#### Friday: Business Operations (`concern` axis)

| # | Partition | Scope | Key Files |
|---|-----------|-------|-----------|
| 1 | Business Agents | 4 agents — strategist, marketer, seller, financier roles and boundaries | `.claude/agents/business/` |
| 2 | Strategy Alignment | Are strategy docs current? Do they align with active priorities? | `business/strategy/` |
| 3 | Sales & Pipeline | Freelance profile, LinkedIn, Gumroad, client pipeline | `business/sales/`, `business/clients/` |
| 4 | Active State Health | now.md, priorities.md, blockers.md, risks.md — freshness and accuracy | `active/now.md`, `active/priorities.md`, `active/blockers.md`, `active/risks.md` |
| 5 | Operational Processes | SOPs current? Recurring processes tracked? Cron automation aligned? | `business/operating/` |

#### Saturday: Evolution & Improvement (`concern` axis)

| # | Partition | Scope | Key Files |
|---|-----------|-------|-----------|
| 1 | Evolution Agents | 4 agents — improver, evaluator, coherence, parallax definitions and boundaries | `.claude/agents/evolution/` |
| 2 | Improvement Pipeline | Active queue, approval flow, staleness, archive completeness | `active/improvements.md`, `core/history/improvements.md` |
| 3 | Evaluation History | Are evaluations being tracked? Recommendations acted on? | `core/history/evaluations.md` |
| 4 | Coherence Integration | Metrics tracking, checkpoint invocations, anti-signal detection | `active/coherence-metrics.md`, `core/standards/coherence-checkpoint-protocol.md` |
| 5 | Audit Findings | Open findings, remediation tracking, severity trends | `active/audits.md` |

#### Sunday: Integration & Health (`concern` axis)

| # | Partition | Scope | Key Files |
|---|-----------|-------|-----------|
| 1 | Configuration & Permissions | Settings, hooks, env vars, permission consistency | `.claude/settings.json`, `.claude/hooks/` |
| 2 | Skills Inventory | All skills current? Invocation works? Arguments documented? | `.claude/skills/` |
| 3 | Templates & Scaffolding | Templates current? Used consistently? Missing templates for common patterns? | `core/templates/` |
| 4 | Cron & Automation | All cron jobs documented? Timing conflicts? Logs checked? | `business/operating/recurring-processes.md`, crontab |
| 5 | System Docs Consistency | CLAUDE.md, AGENTS.md, README.md — agent counts, features, workflows match reality? | `CLAUDE.md`, `AGENTS.md`, `README.md` |

## Phase 1: Parallel Exploration

For each partition, dispatch a standalone `Agent` tool call with `subagent_type: "Explore"` and `mode: "auto"`. **All Agent calls MUST be issued in a single tool-use response** so they execute in parallel.

Do NOT use TeamCreate or SendMessage. Use only the Agent tool.

Each Agent receives in its prompt:
- The focus area context (what we're auditing and why)
- Their specific partition (name, scope, key files)
- The Explorer Search Instructions and Explorer Report Format below
- Depth target: 8-12 Grep/Glob searches + 5-8 full file reads (deep depth)

### Explorer Search Instructions

Each Explorer should:
1. **Inventory:** Glob all files in their partition scope. Count and list them.
2. **Read key files:** Read the most important files fully (agent definitions, standards, configs).
3. **Cross-reference:** Grep for references to their partition's files from OTHER parts of the codebase. Check that references are accurate and current.
4. **Staleness check:** For each key file, check git log for last modification date.
5. **Gap detection:** Look for:
   - Missing documentation or incomplete sections
   - Stale references to moved/deleted files
   - Inconsistencies between related files (e.g., agent definition vs REGISTRY entry)
   - Missing collaboration links (agent A references B, but B doesn't reference A)
   - Standards not being followed
   - Dead code or orphaned files
   - Missing cross-references that should exist

### Explorer Report Format

```markdown
## Partition: [Name]

### Files Inventoried
[count] files examined

### Findings
1. **[Finding title]** — Severity: HIGH/MEDIUM/LOW
   - Location: [file path(s)]
   - Evidence: [what was found]
   - Impact: [why it matters]

2. **[Finding title]** ...

### Cross-Reference Issues
- [file A references file B, but B doesn't exist / is stale / has moved]

### Files Examined
| # | Path | Last Modified | Relevance | Key Finding |
|---|------|--------------|-----------|-------------|

### Confidence
- Coverage: HIGH / MEDIUM / LOW
- Gaps: [anything not examined or insufficiently covered]
```

## Phase 2: Coverage Validation

After all Agent calls return, review each report in the main context:
- If any partition report shows LOW coverage or fewer than 3 findings, dispatch **one** follow-up `Agent` call (`subagent_type: "Explore"`) targeting the thin partition with specific files to examine.
- Maximum one retry per partition.
- Concatenate all reports (initial + any follow-ups) for Phase 3.

## Phase 3: Auditor Four-Layer Analysis

Apply the Auditor's four-layer check to ALL Explorer findings combined:

### Orchestration
- Are the right workflow steps in place for this area?
- Are steps ordered correctly? Any missing handoffs?
- Do workflows reference current agent roles?

### Agents
- Are the right specialists assigned to work in this area?
- Any role gaps (work happening that no agent owns)?
- Boundary violations (agents doing work outside their defined scope)?
- Missing collaboration links between agents?

### Persistence
- Will changes in this area be properly captured in state files?
- Are active/ files up to date for this area?
- Any orphaned artifacts (files with no active state tracking)?

### Injection
- Will future sessions have visibility into this area's current state?
- Does MEMORY.md accurately reflect this area?
- Are hooks and session bootstrap capturing what's needed?

## Phase 4: Improver Distillation

Take the four-layer analysis and distill into 1-5 concrete improvement proposals:

For each proposal:
- **ID:** IA-YYYY-MM-DD-N (ephemeral, not persistent IMP- IDs)
- **Title:** Short descriptive title
- **Layer:** Which of the 4 layers this affects
- **Severity:** High (system gap, broken reference, security issue) / Medium (inconsistency, staleness, drift) / Low (minor improvement, nice-to-have)
- **Evidence:** What was found and where (file paths, line numbers if relevant)
- **Proposal:** Concrete action — what to change, which files, which agent should do it
- **Effort:** Quick (< 1 session) / Medium (1-2 sessions) / Large (3+ sessions)
- **Affected Files:** List of files that would change

Prioritize: High-severity proposals first. Maximum 5 proposals per day — focus on the most impactful findings.

## Phase 5: Coherence + Parallax Reading

**Skip if `--no-coherence` flag is set.**

After the Improver distillation:

1. **Coherence** reads the full audit (Explorer findings + four-layer analysis + proposals) and produces:
   - **Field coherence reading** — what pattern underlies the findings across partitions?
   - **Unresolved polarity** — what core tension does this area hold?
   - **Blind spot signal** — what might the structured audit have missed?

2. **Parallax** translates Coherence output:
   - **Observation** — what Coherence sees
   - **Dynamic** — the force or tension at play
   - **Implication** — what this means operationally

## Phase 6: Write Output

Write to `active/improvement-audit.md` (overwritten each day).

### Output Format

```markdown
# Improvement Audit

Generated: YYYY-MM-DD HH:MM
Focus: [Day] — [Focus Area Name]
Axis: [axis]
Partitions: [count]
Files Examined: [total across all explorers]
Findings: [total count] (H: [high] / M: [medium] / L: [low])

## Executive Summary

[3-5 sentences: what was audited, overall health, most significant findings]

## Findings by Partition

### [Partition 1 Name]
[Synthesized from Explorer 1 — key findings with file paths and evidence]

### [Partition 2 Name]
...

## Four-Layer Analysis

### Orchestration
[Findings about workflow correctness, step ordering, missing steps]

### Agents
[Findings about role gaps, boundary violations, missing collaboration links]

### Persistence
[Findings about state staleness, orphaned artifacts, missing updates]

### Injection
[Findings about session visibility gaps, memory accuracy, hook coverage]

## Improvement Proposals

### IA-YYYY-MM-DD-1: [Title]
- **Layer:** Orchestration | Agents | Persistence | Injection
- **Severity:** High | Medium | Low
- **Evidence:** [what, where]
- **Proposal:** [concrete action]
- **Effort:** Quick | Medium | Large
- **Affected Files:** [list]

### IA-YYYY-MM-DD-2: [Title]
...

## Coherence Reading

### Field Coherence (Coherence)
[Pattern beneath the findings]

### Unresolved Polarity (Coherence)
[Core tension this area holds]

### Blind Spot Signal (Coherence)
[What structured audit may have missed]

### Operational Translation (Parallax)
[Observation -> Dynamic -> Implication]

## File Index
| # | Path | Partition | Last Modified | Relevance | Key Finding |
|---|------|-----------|--------------|-----------|-------------|

---
*Generated by mega-os /improvement-audit — [day] focus, [N] partitions, deep local MECE scan*
```

### Console Report

Print:
- Focus area, partition count, total files examined
- Findings count by severity
- Executive summary
- Top 3 proposals (title + severity + effort)
- Output file path
