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

## Handoff Validation

Before accepting a handoff, the receiving agent must confirm:
1. **Objective is clear** — the goal of the work is unambiguous
2. **Inputs are present** — all referenced files, data, and context are accessible
3. **Definition of Done is testable** — completion criteria can be objectively verified

If any of these are missing, the receiving agent **rejects the handoff** back to the sender with a specific list of what is missing. The sender must address the gaps before re-sending.

## Conflict Resolution

When agents disagree on approach:
1. Each agent states their position with **evidence** (not just opinion)
2. **Single-domain conflict:** the domain specialist decides (e.g., Architect for architecture, Security-Expert for security)
3. **Cross-domain conflict:** escalate to Overseer with both positions documented
4. Overseer makes the final decision
5. Historian records the decision, the chosen position, and the rejected position with rationale
6. The losing position is preserved in the record — it may become relevant later

## QA vs Reviewer Classification

When both QA and Reviewer could be involved, use this rubric:

| Criterion | QA | Reviewer |
|-----------|-----|----------|
| **Focus** | Does it work? (functional correctness) | Is it good? (quality, standards, maintainability) |
| **Method** | Tests, verification, acceptance criteria | Code review, standards compliance, architectural fit |
| **Blocks on** | Failing tests, broken functionality, unmet requirements | Style violations, missed edge cases, unclear logic |
| **Output** | Pass/fail with evidence | Approve/request changes with reasoning |

**Rule:** QA runs first (does it work?), then Reviewer (is it good?). If QA fails, fix before Reviewer sees it.

## Multi-Agent Coordination
- PM tracks cross-agent dependencies and progress.
- Router sequences multi-step workflows.
- Governor ensures agents stay within scope.
- Historian records significant cross-agent decisions.
