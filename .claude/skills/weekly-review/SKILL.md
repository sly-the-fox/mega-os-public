# Weekly Review

Review the current state of the system, summarize progress, identify blockers, and update active state files.

## Steps

1. **Review active state**
   - Read `active/now.md` — is the current focus still accurate?
   - Read `active/priorities.md` — have priorities shifted?
   - Read `active/inbox.md` — are there unprocessed items?
   - Read `active/blockers.md` — are blockers resolved or new ones appeared?

2. **Check products**
   - For each active product in `products/`, check for recent changes.
   - Note any significant progress, regressions, or stalled work.

3. **Review decisions**
   - Read `core/history/decisions.md` — any decisions made this week?
   - Are there pending decisions that need resolution?

4. **Summarize**
   - **Wins:** What was accomplished this week?
   - **Blockers:** What is stalled and why?
   - **Changes:** What shifted in priorities or direction?
   - **Next week:** What should be the focus?

5. **Update active state**
   - Update `active/now.md` with current focus.
   - Reorder `active/priorities.md` if needed.
   - Clear resolved items from `active/blockers.md`.
   - Archive processed items from `active/inbox.md`.

6. **Run Evaluator**
   - Review task completion rates, cycle times, and blocker frequency.
   - Identify recurring blocker patterns (3+ of the same type triggers Improver).
   - Identify recurring defect patterns from QA reports.
   - Record findings to `core/history/evaluations.md` with date, metrics, and recommendations.

7. **Run Improver**
   - Review Evaluator findings from this week.
   - Propose new improvements to `active/improvements.md` based on evidence.
   - Review existing proposals in `active/improvements.md` — update status of any in-progress items.
   - Archive completed improvements (verified/ineffective) to `core/history/improvements.md`.

8. **Update history**
   - Add a timeline entry to `core/history/master-timeline.md`.
   - Update `core/history/current-state.md` if system state changed.
