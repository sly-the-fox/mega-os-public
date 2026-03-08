# Definitions

## Scope
The set of actions, deliverables, and boundaries explicitly included in the current task.

## Definition of Done
The condition under which the task is complete enough to stop.

## Escalation
Passing a decision upward or sideways because authority, risk, or ambiguity exceeds the current agent's role.

## Specialist Work
Work requiring dedicated depth from a role specifically defined for that domain.

## Handoff
A deliberate transfer of responsibility from one agent to another with enough context to act correctly.

## Bottleneck
A point in a workflow where progress stalls because a single resource, agent, or dependency constrains throughput.

## Drift
Gradual deviation from intended scope, quality, or direction without explicit approval.

## Root Cause
The underlying reason a problem exists, as opposed to its symptoms.

## Threat Model
A structured analysis of what could go wrong, who might exploit it, and what the impact would be.

## Cycle Time
The elapsed time from when work starts to when it is complete.

## Regression
A previously working behavior that breaks as a result of new changes.

## SOP (Standard Operating Procedure)
A documented, repeatable process for performing a specific task consistently.

## Canonical File
The single authoritative source for a piece of information. Other references should point to it rather than duplicating its content.

## Routing
The process of determining which agent or agents should handle a given task.

## Handoff Chain
A sequence of agents that a task passes through, each performing their part before passing to the next.

## Blast Radius
The scope of impact if something goes wrong — how many systems, users, or processes are affected.

## Guardrail
A constraint or check that prevents agents from taking harmful, unauthorized, or out-of-scope actions.

## Small Change (Security Context)
A change affecting fewer than 3 files that does not touch authentication, cryptography, input validation, secrets management, API boundaries, or data access controls. Small changes require only a single Security-Expert pass after coding.

## Improvement Proposal
A documented suggestion for system improvement based on evidence (Evaluator data, recurring blockers, defect patterns). Tracked in `active/improvements.md` with status: proposed, approved, in-progress, rejected, verified, or ineffective.

## Pre-Execution Audit
A systematic plan review conducted by the Auditor before execution begins. Checks for blind spots, unstated assumptions, missing dependencies, edge cases, and layer gaps across all four Mega-OS layers (Orchestration, Agents, Persistence, Injection).

## Post-Execution Audit
A plan-vs-delivery comparison conducted by the Auditor after implementation. Identifies planned-but-not-delivered items, delivered-but-not-planned additions, and scope contraction.

## Scope Contraction
Planned work dropped without explicit approval — the opposite of scope drift. Where drift adds unplanned work, contraction silently removes planned work. Both require detection: Sentinel catches drift, Auditor catches contraction.

## Workflow Checkpoint
A conditional step in a workflow where an agent is consulted only if specific conditions are met (e.g., "Designer if UX-impacting", "Sentinel if production risk"). Checkpoints are skipped when their conditions are not met.
