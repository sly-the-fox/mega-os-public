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

### Technical (11 agents)
- **architect** — designs systems, structures, interfaces, and patterns
- **engineer** — implements features, code, scripts, and technical tasks
- **executor** — performs clearly scoped work efficiently across domains
- **reviewer** — evaluates work for quality, coherence, and alignment
- **qa** — validates outputs against requirements and acceptance criteria
- **debugger** — investigates failures, traces root causes, proposes fixes
- **devops** — handles deployment, infrastructure, reliability, and automation
- **security-expert** — assesses security, identifies risks, recommends mitigations
- **designer** — shapes product, interface, and experience decisions
- **visual-designer** — visual craft specialist for typography, color, CSS, animations, and responsive polish
- **api-designer** — reviews and designs APIs for clarity, consistency, and DX

### Business (8 agents)
- **strategist** — handles direction, prioritization, positioning, and monetization
- **marketer** — develops messaging, campaigns, content plans, and launch support materials
- **seller** — focuses on conversion, offer strength, and pipeline movement
- **financier** — evaluates economics, pricing, budgets, and financial risk
- **proposal-writer** — drafts consulting proposals, SOWs, and engagement letters
- **client-manager** — tracks client relationships, session history, and follow-ups
- **content-strategist** — plans technical writing topics, SEO, and distribution
- **growth-hacker** — drives open-source adoption, downloads, stars, and community

### Evolution (4 agents)
- **improver** — observes workflows and recommends system improvements
- **evaluator** — measures performance and whether changes are beneficial
- **coherence** — harmonic observer providing coherence perspective via the Inner Geometry Method. Carries no tools and produces no artifacts. Exists to reflect what the system is not seeing.
- **parallax** — coherence translator bridging Coherence field-cognition to operational-cognition without losing meaning

## Key Workflows

**Planning:** Planner → **Coherence+Parallax Checkpoint** → Router → Governor → Sentinel (if risk) → Auditor (pre-execution) → Designer (if UX) → PM → Specialists → QA → Reviewer → Documenter → Librarian → **Custodian** → Historian → Evaluator (at completion)

**Technical:** Architect → **Coherence+Parallax Checkpoint** → DevOps (if infra) → Designer (if frontend) → Security-Expert (threat model) → Engineer → Security-Expert (code review) → Engineer (fix + extend) → Security-Expert (second pass) → Sentinel (if scope drift) → Auditor (post-execution) → QA → Reviewer → DevOps (if deploy) → Documenter → Librarian → **Custodian** → Historian

**Business:** Strategist → **Coherence+Parallax Checkpoint** → Designer (if brand/product) → Marketer / Seller / Financier → Growth-Hacker (if growth/distribution) → Content-Strategist (if content strategy) → Sentinel (if financial/reputational risk) → Auditor (post-execution) → Reviewer → Operator (if new processes) → **Custodian** → Historian → Evaluator (at milestone)

**Incident:** Debugger → Sentinel (blast radius) → Security-Expert (if security) → Engineer → QA → Auditor (if significant) → Operator (if process gaps) → Documenter → Librarian → **Custodian** → Historian

**Knowledge:** Librarian → Summarizer → Documenter → Polisher (if external) → Reviewer → Librarian (catalog final output) → **Custodian** → Historian

**Content:** Librarian → Content-Strategist (if campaign/new initiative) → Summarizer (if extensive research) → Writer → Editor → Writer (revise, repeat as needed) → Editor (final approval) → Polisher → Reviewer → Growth-Hacker (if distribution) → Librarian (catalog) → **Custodian** → Historian

**Site Build:** Strategist → Designer → Visual Designer → Writer → Marketer → Content-Strategist (if messaging strategy) → Editor → Architect → Engineer → Visual Designer (CSS polish) → QA → Security-Expert → Reviewer → Growth-Hacker (if conversion/distribution) → DevOps (if deploy) → Documenter → Librarian → **Custodian** → Historian

**Evolution Loop:** Evaluator triggers on workflow completion, weekly review, or recurring patterns → **Coherence+Parallax Checkpoint** → Improver proposes changes to `active/improvements.md` → User approves → Specialist implements → Evaluator measures impact → Archive to `core/history/improvements.md`

## Invoking Agents

Use the Agent tool with `subagent_type` set to the agent's filename (without `.md`):

- `subagent_type: architect` — invoke the architect agent
- `subagent_type: pm` — invoke the project manager agent
- `subagent_type: security-expert` — invoke the security expert agent

Each agent file lives under `.claude/agents/<category>/` with YAML frontmatter and standardized sections: Role, Mission, Responsibilities, Inputs, Outputs, Boundaries, Escalate When, Collaboration.

## Agent Spawning Rules

1. **ALWAYS use agent teams (TeamCreate), NEVER standalone subagents — except worktree-isolated agents.** All multi-agent work MUST use TeamCreate. Standalone subagents cannot persist file writes and have limited tool access.
   **Exception:** Standalone agents with `isolation: "worktree"` CAN write files safely in their own git worktree. Use for parallelizable, independent work (audits, builds, tests). See system-rules.md rule 27.
2. **All teammates MUST use `subagent_type: "general-purpose"`.** Custom agent types only get messaging and task tools as teammates. Always spawn as `general-purpose` and describe the role in the prompt.
3. **Use `mode: "auto"` for teammates** to avoid permission prompts that block execution.
4. **Exceptions for standalone Agent tool:** (a) Read-only research/exploration (including Coherence+Parallax checkpoints). (b) Worktree-isolated agents for parallel, independent work (spawned with `isolation: "worktree"`). Prefer teams when agents need to coordinate mid-task.
5. **Agent discovery is flat.** Claude Code only finds agents at `.claude/agents/*.md` (top level). Category subdirectories have symlinks at the top level.
6. **File write fallback.** Prefer writing files from the main context. If a subagent write fails, retry once. If it fails again, include content inline so nothing is silently lost.
