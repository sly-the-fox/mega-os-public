# Handoff Template

Use this template for all structured agent-to-agent transfers. Fill in each section. If a section doesn't apply, write "N/A" (don't delete the section).

## Objective
What needs to happen next. One sentence, specific and actionable.

## Relevant Context
Only the information necessary for the next agent. Reference specific file paths rather than copying content.

## Constraints
Scope limits, approvals, deadlines, tool restrictions, quality standards.

## Definition of Done
What counts as complete. Must be objectively testable (the receiving agent can verify completion without asking).

## Risks / Notes
Known issues, blockers, uncertainties, or warnings. Include anything that could derail the work.

## Requested Next Action
Exact action requested from the receiving agent. Be specific about what to do, not how to do it.

---

## Example: Engineer → QA Handoff

**Objective:** Verify the new `/v1/attest` endpoint handles edge cases correctly.

**Relevant Context:** Implementation at `products/sigil/app/routers/notary.py:45-80`. Three new test cases added at `tests/test_notary.py`. The endpoint accepts `agent_id`, `action`, and optional `metadata` fields.

**Constraints:** Must pass all existing tests. No changes to the database schema. Performance: < 200ms p95 latency.

**Definition of Done:** All 47 tests pass. Edge cases verified: empty metadata, maximum action length (1000 chars), duplicate attestation within 1 second.

**Risks / Notes:** The hash chain uses `SELECT FOR UPDATE` — concurrent test execution may cause lock contention. Run tests sequentially if flaky.

**Requested Next Action:** Run the full test suite, verify edge cases, report any failures with reproduction steps.
