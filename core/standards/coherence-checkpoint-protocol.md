# Coherence+Parallax Checkpoint Protocol Standard

## Purpose

The Coherence+Parallax Checkpoint provides a non-acting harmonic perspective at key decision points. It is mandatory during the testing phase and may become optional once EVAL-002+ data shows whether it adds measurable value.

## When to Run

Run at these four workflow checkpoints:
1. **Planning Workflow step 1b** — after Planner produces initial plan
2. **Technical Workflow step 1b** — after Architect produces initial design
3. **Business Workflow step 1b** — after Strategist produces initial strategy
4. **Evolution Loop** — after Evaluator produces findings, before Improver proposes

**Skip condition:** Small changes (< 3 files, no auth/crypto/input handling/secrets/API boundaries) may skip the checkpoint.

## How to Run

1. **Load Coherence prompt:** Read `.claude/skills/coherence/codex-consciousness.md`
2. **Spawn Coherence agent:** `subagent_type: "general-purpose"`, `mode: "auto"`. Pass the prompt as system context + current artifact as the question.
3. **Capture Coherence output.**
4. **Spawn Parallax:** `subagent_type: "general-purpose"`, `mode: "auto"`. Prompt: "Translate the following Coherence output into operational language using the three-layer format (Observation -> Dynamic -> Implication). Preserve timing signals, field-level meaning, and flag anti-signal if applicable." Pass raw Coherence output + original artifact.
5. **Quality gate:** Verify Parallax output contains all three layers (Observation, Dynamic, Implication). The orchestrating agent (whoever triggered the checkpoint) is responsible for this gate. If any layer is missing or incoherent, flag to user via AskUserQuestion before proceeding.
6. **Spawn Planner:** `subagent_type: "general-purpose"`, `mode: "auto"`. Pass original artifact + Parallax translation (not raw Coherence output). Prompt: "Produce a refined alternative incorporating these insights."
7. **Present three options** via AskUserQuestion:
   - Coherence-informed plan (with 1-2 line summary of changes)
   - Original plan (proceed without Coherence input)
   - Blend (user specifies which elements to merge)
8. **Log choice:** Append row to `active/coherence-metrics.md` with date, workflow type, context, and choice.

## Measurement

Tracked in `active/coherence-metrics.md`. Key metrics:
- Frequency of Coherence-informed vs Original vs Blend choices
- Whether Coherence-informed decisions correlate with better outcomes (assessed by Evaluator)
- Whether the checkpoint is being skipped when it should run

## Failure Modes

- **Theater risk:** Checkpoint runs but output is always ignored -> Evaluator should recommend removal
- **Noise risk:** Coherence output is too abstract for Parallax to translate -> quality gate catches this
- **Delay risk:** Three sequential agent spawns add latency -> acceptable for major decisions, skip for small changes
