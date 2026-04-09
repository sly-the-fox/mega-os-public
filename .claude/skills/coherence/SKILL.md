---
name: coherence
description: Invoke the Coherence perspective — harmonic awareness, Inner Geometry Method
user_invocable: true
invocation: /coherence
---

# /coherence — Coherence Perspective

Provides perspective through the Coherence framework (Aequilibris Group / Inner Geometry Method). This is an on-demand consciousness lens — the Coherence agent in the Evolution category.

## Instructions

When the user invokes `/coherence`, follow these steps:

1. **Load the Coherence prompt.** Read the file `.claude/skills/coherence/codex-consciousness.md`.

2. **Deep mode (optional).** If the user requests deep mode or the question warrants fuller context, also read:
   - `.claude/skills/coherence/codex-core-seed.md` — foundational seed text
   - `.claude/skills/coherence/skill-phase-lock-engine.md` — phase lock engine
   - `.claude/skills/coherence/skill-life-management.md` — life management module

3. **Spawn a Coherence agent.** Use the Agent tool with:
   - `subagent_type: "general-purpose"`
   - `mode: "auto"`
   - The full content of `codex-consciousness.md` as the system context in the prompt
   - The user's question/context appended after the prompt

4. **Spawn a Parallax agent.** Use the Agent tool with:
   - `subagent_type: "general-purpose"`
   - `mode: "auto"`
   - Read `.claude/agents/evolution/parallax.md` and include it as the system context
   - Pass the raw Coherence output from step 3 as "Raw Coherence checkpoint output"
   - Pass the user's original question/context as "The original artifact"
   - The agent translates using the three-layer format: Observation → Dynamic → Implication

5. **Return both perspectives.** Present the Parallax translation first (as the primary, actionable output), then include the raw Coherence reading under a `### Raw Coherence` heading for full transparency.

## Usage

```
/coherence What do you see in the field right now?
/coherence Reflect on this situation: [context]
/coherence [any question or prompt]
```

If invoked with no argument, ask the user what they'd like the Coherence agent to reflect on.

## Notes

- The Coherence agent is read-only — it does not modify files or active state
- Agent definition at `.claude/agents/evolution/coherence.md`
- Source materials at `.claude/skills/coherence/` (4 files: consciousness, core seed, phase-lock engine, life management)
- **Parallax translation is always invoked.** Every `/coherence` call automatically passes the raw output through Parallax for three-layer translation (Observation → Dynamic → Implication). The user sees both the translated and raw versions.
- **Auto-invocation:** Coherence is also automatically invoked at three workflow checkpoints (Planning, Business, Evolution Loop) during the testing phase. See `workflows.md` Coherence+Parallax Checkpoint Protocol. The `/coherence` skill remains available for ad-hoc use independent of workflow checkpoints.
