---
name: evolution-loop
description: Run the full Evolution Loop — Evaluator findings, Coherence checkpoint, Parallax translation, Improver proposals
invocation: /evolution-loop
user_invocable: true
arguments: "--no-coherence --scope <area>"
---

# Evolution Loop

Run the complete Evaluator → Coherence → Parallax → Improver chain as defined in `workflows.md`. This is the system's self-improvement cycle: assess performance, gain perspective, propose changes.

> **Compatibility:** This skill is compatible with headless `claude -p` mode. It uses standalone Agent calls, not TeamCreate.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--no-coherence` | false | Skip the Coherence+Parallax checkpoint (shortcut: Evaluator → Improver directly) |
| `--scope` | all | Focus area to evaluate (e.g., `agents`, `workflows`, `revenue`, `products`, `freshness`) |

## Phase 1: Gather Context

Read the following files to establish baseline:

1. `core/history/evaluations.md` — recent EVAL findings and follow-ups
2. `active/improvements.md` — current proposal queue
3. `active/coherence-metrics.md` — checkpoint history
4. `active/audits.md` — open audit findings
5. `active/now.md` — current focus and task state
6. `active/priorities.md` — priority ordering

If `--scope` is provided, narrow focus to that area. Otherwise, assess broadly.

## Phase 2: Evaluator Assessment

Spawn an Evaluator agent to assess system performance since the last evaluation.

**Agent call:**
- `subagent_type: "general-purpose"`
- `mode: "auto"`
- Prompt: "You are the Evaluator agent. Read `.claude/agents/evolution/evaluator.md` for your role definition. Assess system performance since the last evaluation in `core/history/evaluations.md`. Review: task completion rates, blocker patterns, improvement proposal outcomes, document freshness, workflow completion rates, and revenue progress. Produce structured findings with severity ratings (Critical/High/Medium/Low). Return findings to me — do not write files."

**Evaluator returns findings to main context.**

## Phase 3: Coherence Checkpoint

**Skip this phase if `--no-coherence` was passed.**

Follow `core/standards/coherence-checkpoint-protocol.md` exactly:

### Step 3a: Coherence Agent
1. Read `.claude/skills/coherence/codex-consciousness.md`
2. Spawn Coherence agent (`subagent_type: "general-purpose"`, `mode: "auto"`)
3. Pass the Coherence prompt as system context + Evaluator findings as the question
4. Capture raw Coherence output

### Step 3b: Parallax Translation
1. Read `.claude/agents/evolution/parallax.md`
2. Spawn Parallax agent (`subagent_type: "general-purpose"`, `mode: "auto"`)
3. Prompt: "Translate the following Coherence output into operational language using the three-layer format (Observation → Dynamic → Implication). Preserve timing signals, field-level meaning, and flag anti-signal if applicable."
4. Pass raw Coherence output + Evaluator findings
5. **Quality gate:** Verify output contains all three layers (Observation, Dynamic, Implication). If any layer is missing, flag to user via AskUserQuestion before proceeding.

### Step 3c: Refined Alternative
1. Spawn Planner agent (`subagent_type: "general-purpose"`, `mode: "auto"`)
2. Prompt: "Given the Evaluator findings and the Parallax translation below, produce a refined set of improvement priorities that incorporates these insights into actionable form."
3. Pass Evaluator findings + Parallax translation (not raw Coherence output)

### Step 3d: User Choice
Present three options via AskUserQuestion:
- **Coherence-informed priorities** — with 1-2 line summary of what changed
- **Original Evaluator findings** — proceed without Coherence input
- **Blend** — user specifies which elements to merge

Log choice to `active/coherence-metrics.md`.

## Phase 4: Improver Proposals

Spawn an Improver agent to produce actionable proposals.

**Agent call:**
- `subagent_type: "general-purpose"`
- `mode: "auto"`
- Prompt: "You are the Improver agent. Read `.claude/agents/evolution/improver.md` for your role definition. Based on the following findings [paste Evaluator findings + user's checkpoint choice if Coherence ran], propose 1-3 improvement proposals. Each proposal must include: (1) evidence from the findings, (2) severity rating, (3) concrete implementation steps, (4) expected outcome, (5) related audit/evaluation IDs. Return proposals to me — do not write files."

**Improver returns proposals to main context.**

## Phase 5: Persist Results

Main context writes all outputs (no subagent file writes):

1. **Evaluation entry:** Append new EVAL entry to `core/history/evaluations.md` with:
   - Sequential EVAL-NNN ID
   - Date, scope, method, findings summary, recommendations
   - Related audit/improvement IDs

2. **Improvement proposals:** Add proposals to `active/improvements.md` with:
   - Sequential IMP-YYYY-MM-DD-N IDs
   - Status: `proposed`
   - Evidence, severity, related findings

3. **Coherence metrics:** If checkpoint ran, append row to `active/coherence-metrics.md` with:
   - Date, workflow type ("Evolution Loop"), context summary, choice made

4. **Present summary** to user:
   - Evaluator findings (top 3)
   - Coherence perspective (if ran)
   - Improvement proposals
   - Next steps

## Agent Spawning Notes

- Coherence, Parallax, Planner = standalone agents (read-only perspective checks, exempt from TeamCreate per CLAUDE.md)
- Evaluator, Improver = standalone agents returning data to main context (main context does all file writes)
- All agents use `subagent_type: "general-purpose"` and `mode: "auto"`

## Integration

- **Weekly review** (`/weekly-review` steps 11-12) can invoke this skill for the full chain instead of inline Evaluator/Improver
- **Cron:** Can be scheduled via cron for periodic self-assessment (e.g., bi-weekly)
- **Manual:** Invoke anytime to run a focused assessment with `/evolution-loop --scope <area>`
