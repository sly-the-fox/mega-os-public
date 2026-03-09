---
name: weekly-review
description: Weekly system review — scan for stale items, summarize progress, cross-reference findings, and update active state.
invocation: /weekly-review
user_invocable: true
---

# Weekly Review

Review the current state of the system, scan for stale items, cross-reference passive agent outputs, summarize progress, identify blockers, and update active state files.

## Steps

1. **Run daily scan**
   - Execute all `/daily-scan` steps to populate `active/daily-digest.md`.
   - Read the resulting digest. This is your starting point for the review.

2. **Review active state**
   - Read `active/now.md` — is the current focus still accurate?
   - Read `active/priorities.md` — have priorities shifted?
   - Interpret findings from the daily digest rather than re-reading raw files (the scan already did that).

3. **Check products**
   - For each active product in `products/`, check for recent changes.
   - Note any significant progress, regressions, or stalled work.

4. **Review decisions**
   - Read `core/history/decisions.md` — any decisions made this week?
   - Are there pending decisions that need resolution?

5. **Cross-reference analysis**
   - Compare evaluator recommendations (`core/history/evaluations.md`) against improver proposals (`active/improvements.md`) — are recommendations becoming proposals? Flag any recommendation older than 14 days with no matching proposal.
   - Check if audit findings (`active/audits.md`) overlap with risks (`active/risks.md`) — same issue tracked in both places should be consolidated.
   - Check if blockers (`active/blockers.md`) correlate with known risks — a blocker that matches a risk suggests the risk has materialized.
   - Flag patterns appearing 3+ times across sources (e.g., same topic in risks, audits, and blockers).

6. **Staleness check on indexes**
   - Verify all entries in `core/indexes/canonical-files.md` against the actual filesystem. Flag any entries pointing to files that no longer exist or missing entries for files that should be tracked.
   - Verify `core/indexes/project-map.md` matches actual directory structure.
   - Verify `core/indexes/active-context-map.md` is current.
   - Flag stale entries for Librarian to update.

7. **Agent structure integrity check**
   - **Reciprocity scan:** For each agent file in `.claude/agents/`, read its Collaboration section. For every agent Y referenced, verify Y's Collaboration section references back. Flag any one-way references.
   - **Registry consistency:** Compare each agent's frontmatter `description` against its entry in `.claude/agents/REGISTRY.md` and `AGENTS.md`. Flag mismatches.
   - **Workflow alignment:** For each workflow in `.claude/agents/shared/workflows.md`, verify every agent listed appears in the correct position and that agent's Collaboration section reflects the workflow adjacency.
   - **Checklist compliance:** For each passive agent checklist in workflows.md, verify the corresponding agent file contains matching owned-file references.
   - Report findings as part of the Improver step (step 12).

8. **Summarize**
   - **Wins:** What was accomplished this week?
   - **Blockers:** What is stalled and why?
   - **Changes:** What shifted in priorities or direction?
   - **Trends:** Patterns from cross-reference analysis (step 5).
   - **Next week:** What should be the focus?

9. **Update active state**
   - Update `active/now.md` with current focus.
   - Reorder `active/priorities.md` if needed.
   - Clear resolved items from `active/blockers.md`.
   - Archive processed items from `active/inbox.md`.

10. **Run Evaluator**
    - Review task completion rates, cycle times, and blocker frequency.
    - Identify recurring blocker patterns (3+ of the same type triggers Improver).
    - Identify recurring defect patterns from QA reports.
    - Record findings to `core/history/evaluations.md` with date, metrics, and recommendations.

11. **Run Improver**
    - Review Evaluator findings from this week.
    - Review agent structure integrity findings from step 7.
    - Propose new improvements to `active/improvements.md` based on evidence.
    - Review existing proposals in `active/improvements.md` — update status of any in-progress items.
    - Archive completed improvements (verified/ineffective) to `core/history/improvements.md`.

12. **Update history**
    - Add a timeline entry to `core/history/master-timeline.md`.
    - Update `core/history/current-state.md` if system state changed.
