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
