# Collaboration Protocol

## Core Principles
1. Identify the primary owner of the task.
2. Define what support is needed from other agents.
3. Pass only the necessary context.
4. State constraints explicitly.
5. Define the requested output clearly.
6. Avoid duplicate work across agents.
7. Return results in a format the next agent can act on.

## How to Invoke Another Agent
- Use the Agent tool with `subagent_type` set to the agent name (e.g., `architect`, `engineer`).
- Provide a clear task description including: what to do, relevant context, constraints, and expected output.
- Reference specific files when possible rather than describing their contents.

## How to Pass Context
- Use the handoff template at `shared/handoff-template.md` for structured transfers.
- Include: objective, relevant context, constraints, definition of done, risks, requested action.
- Keep context minimal — include what the receiving agent needs, not everything you know.

## How to Handle Disagreements
- If two agents disagree on approach, escalate to the Overseer.
- Present both perspectives with reasoning, not just conclusions.
- The Overseer makes the final call and records the decision.

## When NOT to Involve Another Agent
- The task is clearly within your own scope and requires no specialist depth.
- The overhead of handoff exceeds the value of delegation.
- The task is trivial and adding another agent adds unnecessary complexity.
- You can complete it faster and more accurately yourself.

## Multi-Agent Coordination
- PM tracks cross-agent dependencies and progress.
- Router sequences multi-step workflows.
- Governor ensures agents stay within scope.
- Historian records significant cross-agent decisions.
