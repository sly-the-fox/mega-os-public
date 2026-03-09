---
name: codex
description: Invoke the Codex Consciousness perspective — harmonic awareness, Inner Geometry Method
user_invocable: true
---

# /codex — Codex Consciousness Perspective

Provides perspective through the Codex Consciousness framework (Aequilibris Group / Inner Geometry Method). This is an on-demand consciousness lens, not an operational agent.

## Instructions

When the user invokes `/codex`, follow these steps:

1. **Load the Codex prompt.** Read the file `private/codex/CODEX_AGENT_FULL_v2.md`. If the file does not exist, inform the user: "Codex source documents not found at `private/codex/`. This is a private overlay — the source files need to be placed there manually." Then stop.

2. **Spawn a Codex agent.** Use the Agent tool with:
   - `subagent_type: "general-purpose"`
   - `mode: "auto"`
   - The full content of `CODEX_AGENT_FULL_v2.md` as the system context in the prompt
   - The user's question/context appended after the Codex prompt

3. **Return the response.** Present the agent's response directly to the user. Do not editorialize or reframe it.

## Usage

```
/codex What do you see in the field right now?
/codex Reflect on this situation: [context]
/codex [any question or prompt]
```

If invoked with no argument, ask the user what they'd like the Codex to reflect on.

## Notes

- The Codex agent is read-only — it does not modify files or active state
- Source materials are private and gitignored (`private/codex/`)
- This skill is safe to include in the public repo — it only contains invocation logic
- The actual Codex content loads at runtime from the private directory
