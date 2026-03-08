# Mega-OS Agent System

Canonical source: [.claude/agents/REGISTRY.md](.claude/agents/REGISTRY.md)

## Design Philosophy

- **Stay in role.** Each agent has a defined scope. It does not drift into another agent's territory.
- **Handoff to specialists.** When a task falls outside scope, delegate rather than improvise.
- **Preserve rationale.** Decisions, tradeoffs, and context are recorded so future agents and humans understand why.
- **Prefer practical over theoretical.** Working solutions beat abstract frameworks.
- **Minimal viable action.** Do the smallest effective thing rather than broad rewrites.

## Agent Categories

### Governance (7 agents)
- **overseer** — routes work, chooses specialists, keeps execution aligned with priorities
- **governor** — enforces task boundaries, permissions, and execution limits
- **router** — determines which agents handle each request and sequences workflow
- **planner** — converts goals into phased plans, tasks, and dependencies
- **pm** — manages progress, coordination, and accountability
- **operator** — maintains SOPs, process clarity, and operational consistency
- **sentinel** — watches for risk, governance, safety, and permission issues

### Knowledge (4 agents)
- **historian** — maintains timelines, decisions, and institutional memory
- **librarian** — organizes knowledge, identifies canonical files, reduces duplication
- **summarizer** — compresses context into concise briefs without losing meaning
- **documenter** — turns work into clear, durable documentation

### Technical (9 agents)
- **architect** — designs systems, structures, interfaces, and patterns
- **engineer** — implements features, code, scripts, and technical tasks
- **executor** — performs clearly scoped work efficiently across domains
- **reviewer** — evaluates work for quality, coherence, and alignment
- **qa** — validates outputs against requirements and acceptance criteria
- **debugger** — investigates failures, traces root causes, proposes fixes
- **devops** — handles deployment, infrastructure, reliability, and automation
- **security-expert** — assesses security, identifies risks, recommends mitigations
- **designer** — shapes product, interface, and experience decisions

### Business (4 agents)
- **strategist** — handles direction, prioritization, positioning, and monetization
- **marketer** — develops messaging, campaigns, and content plans
- **seller** — focuses on conversion, offer strength, and pipeline movement
- **financier** — evaluates economics, pricing, budgets, and financial risk

### Evolution (2 agents)
- **improver** — observes workflows and recommends system improvements
- **evaluator** — measures performance and whether changes are beneficial

## Key Workflows

**Planning:** Planner -> Router -> Governor validates -> PM tracks -> Specialists -> QA -> Reviewer -> Documenter -> Historian

**Technical:** Architect -> Engineer -> QA -> Security-Expert (if relevant) -> Reviewer -> DevOps (if deploy) -> Documenter

**Business:** Strategist -> Marketer / Seller / Financier -> Reviewer -> Historian

**Incident:** Debugger -> Security-Expert (if security) -> Engineer -> QA -> Historian

**Knowledge:** Librarian -> Summarizer -> Documenter -> Historian

## Invoking Agents

Use the Agent tool with `subagent_type` set to the agent's filename (without `.md`):

- `subagent_type: architect` — invoke the architect agent
- `subagent_type: pm` — invoke the project manager agent
- `subagent_type: security-expert` — invoke the security expert agent

Each agent file lives under `.claude/agents/<category>/` with YAML frontmatter and standardized sections: Role, Mission, Responsibilities, Inputs, Outputs, Boundaries, Escalate When, Collaboration.
