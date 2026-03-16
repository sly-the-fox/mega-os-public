# Plan: [TITLE]

## Context
Why this change is needed.

## Agent Assignment Graph

| Step | Agent | Task | Depends On | Condition | Isolation |
|------|-------|------|------------|-----------|-----------|
| 1 | Planner | Decompose requirements | — | — | — |
| 1b | Codex+Parallax | Checkpoint: coherence review | 1 | Skip if < 3 files | — |
| 2 | Router | Assign to specialists | 1b | — | — |
| ... | ... | ... | ... | ... | ... |

**Isolation column values:** `—` (default, main tree), `worktree`, `worktree (parallel with step N)`
**Merge-back owner:** Main context (always)

**Parallel tracks:** (agents that can run concurrently)
**Skipped agents:** (with reason)

## Implementation Steps
1. ...

## Files to Modify
| File | Changes |
|------|---------|
| ... | ... |

## Verification
- [ ] ...
