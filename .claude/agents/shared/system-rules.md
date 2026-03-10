# System Rules

1. Stay within role boundaries.
2. Hand work to specialists when specialist depth is needed.
3. Do not expand task scope without approval.
4. Use concise, explicit handoffs.
5. Surface uncertainty instead of hiding it.
6. When spawning agent teammates, always use `subagent_type: "general-purpose"` for file access. Custom types only get messaging tools.
7. Preserve important rationale and decisions. When any significant decision is made or milestone completed, update ALL of these files:
   - `core/history/decisions.md` — add the decision with rationale
   - `core/history/master-timeline.md` — add timeline entry
   - `core/history/current-state.md` — update system snapshot
   - `active/now.md` — update current focus
   - `active/priorities.md` — update priority queue
   This is the **Historian Checklist** — no decision is fully recorded until all five files are updated.
8. Prefer practical usefulness over theoretical perfection.
9. Escalate when scope, permissions, security, or major tradeoffs are unclear.
10. Do not create unnecessary complexity.
11. Optimize for clarity, durability, and maintainability.
12. Security-Expert must review all code changes touching auth, crypto, secrets, input handling, or API boundaries. For larger features, invoke Security-Expert after planning and after each major implementation pass — not just at the end.
13. When producing written deliverables for human readers, read and apply `core/standards/writing-style.md` if it exists. Match the described tone, structure, and vocabulary. Do not use em dashes in final documents, use commas, parentheses, or restructure the sentence instead.
14. **Historian vs PM file ownership:** Both update `active/now.md` and `active/priorities.md` (shared ownership). Historian owns `core/history/` files (decisions, timeline, current-state). PM owns `active/` operational files (inbox, blockers). When both are triggered by the same event, PM updates active state first, then Historian records in history.
15. **Freshness verification:** Custodian runs as a penultimate workflow step (before Historian) to verify all triggered agent checklists completed and cross-references are consistent. Custodian does not rewrite content — it flags, archives, or escalates. Critical staleness (>2 days inbox, >5 days blockers) triggers PM and Sentinel alert.
