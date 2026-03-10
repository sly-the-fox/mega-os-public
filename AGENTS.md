# Mega-OS Agent System

Canonical source: [.claude/agents/REGISTRY.md](.claude/agents/REGISTRY.md)

## Design Philosophy

- **Stay in role.** Each agent has a defined scope. It does not drift into another agent's territory.
- **Handoff to specialists.** When a task falls outside scope, delegate rather than improvise.
- **Preserve rationale.** Decisions, tradeoffs, and context are recorded so future agents and humans understand why.
- **Prefer practical over theoretical.** Working solutions beat abstract frameworks.
- **Minimal viable action.** Do the smallest effective thing rather than broad rewrites.

## Agent Categories

### Governance (9 agents)
- **overseer** — routes work, chooses specialists, keeps execution aligned with priorities
- **governor** — enforces task boundaries, permissions, and execution limits
- **router** — determines which agents handle each request and sequences workflow
- **planner** — converts goals into phased plans, tasks, and dependencies
- **pm** — manages progress, coordination, and accountability
- **operator** — maintains SOPs, process clarity, and operational consistency
- **sentinel** — watches for risk, governance, safety, and permission issues
- **auditor** — reviews plans for blind spots and audits delivery against plans
- **custodian** — verifies document freshness and checklist completion at workflow end

### Knowledge (7 agents)
- **historian** — maintains timelines, decisions, and institutional memory
- **librarian** — organizes knowledge, identifies canonical files, reduces duplication
- **summarizer** — compresses context into concise briefs without losing meaning
- **documenter** — turns work into clear, durable documentation
- **polisher** — polishes raw documents into publication-ready deliverables
- **writer** — writes original long-form content (articles, essays, books) in the user's voice
- **editor** — editorial specialist for structure, citations, fact-checking, and voice consistency

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
- **marketer** — develops messaging, campaigns, content plans, and launch support materials
- **seller** — focuses on conversion, offer strength, and pipeline movement
- **financier** — evaluates economics, pricing, budgets, and financial risk

### Evolution (4 agents)
- **improver** — observes workflows and recommends system improvements
- **evaluator** — measures performance and whether changes are beneficial
- **codex** — harmonic observer providing coherence perspective via the Inner Geometry Method. Carries no tools and produces no artifacts. Exists to reflect what the system is not seeing.
- **parallax** — coherence translator bridging Codex field-cognition to operational-cognition without losing meaning

## Key Workflows

**Planning:** Planner → **Codex+Parallax Checkpoint** → Router → Governor → Sentinel (if risk) → Auditor (pre-execution) → Designer (if UX) → PM → Specialists → QA → Reviewer → Documenter → Librarian → **Custodian** → Historian → Evaluator (at completion)

**Technical:** Architect → **Codex+Parallax Checkpoint** → DevOps (if infra) → Designer (if frontend) → Security-Expert (threat model) → Engineer → Security-Expert (code review) → Engineer (fix + extend) → Security-Expert (second pass) → Sentinel (if scope drift) → Auditor (post-execution) → QA → Reviewer → DevOps (if deploy) → Documenter → Librarian → **Custodian** → Historian

**Business:** Strategist → **Codex+Parallax Checkpoint** → Designer (if brand/product) → Marketer / Seller / Financier → Sentinel (if financial/reputational risk) → Auditor (post-execution) → Reviewer → Operator (if new processes) → **Custodian** → Historian → Evaluator (at milestone)

**Incident:** Debugger → Sentinel (blast radius) → Security-Expert (if security) → Engineer → QA → Auditor (if significant) → Operator (if process gaps) → Documenter → Librarian → **Custodian** → Historian

**Knowledge:** Librarian → Summarizer → Documenter → Polisher (if external) → Reviewer → Librarian (catalog final output) → **Custodian** → Historian

**Content:** Librarian → Summarizer (if extensive research) → Writer → Editor → Writer (revise, repeat as needed) → Editor (final approval) → Polisher → Reviewer → Librarian (catalog) → **Custodian** → Historian

**Evolution Loop:** Evaluator triggers on workflow completion, weekly review, or recurring patterns → **Codex+Parallax Checkpoint** → Improver proposes changes to `active/improvements.md` → User approves → Specialist implements → Evaluator measures impact → Archive to `core/history/improvements.md`

## Invoking Agents

Use the Agent tool with `subagent_type` set to the agent's filename (without `.md`):

- `subagent_type: architect` — invoke the architect agent
- `subagent_type: pm` — invoke the project manager agent
- `subagent_type: security-expert` — invoke the security expert agent

Each agent file lives under `.claude/agents/<category>/` with YAML frontmatter and standardized sections: Role, Mission, Responsibilities, Inputs, Outputs, Boundaries, Escalate When, Collaboration.
