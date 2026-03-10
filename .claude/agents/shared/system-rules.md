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
16. **Session-end recording (mandatory).** Before ending any session where significant work occurred (decisions, file changes, priority shifts, milestones), run the Historian Checklist (rule 7) directly. This applies even for tasks that skip full workflows.
17. **Plans require agent graphs.** Every plan in `.claude/plans/` must include an Agent Assignment Graph table (step, agent, task, depends-on, condition). Use `core/templates/plan-template.md`.
18. **Codex+Parallax checkpoint (mandatory during testing phase).** At documented workflow checkpoints (Planning step 1b, Technical step 1b, Business step 1b, Evolution Loop), run the Codex+Parallax Checkpoint Protocol per `core/standards/codex-checkpoint-protocol.md`. Skip for small changes (< 3 files, no auth/crypto/input handling/secrets/API boundaries). Log all invocations to `active/codex-metrics.md`.
19. **MECE research (mandatory for web research).** When any task or workflow step requires web research (WebSearch/WebFetch), use the MECE deep research pattern via `/deep-research`. This applies to all workflows — Planning (Planner research), Content (Librarian source gathering), Business (Strategist market research), and Knowledge (Librarian information gathering). The only exception is the `/news-briefing` skill, which has its own specialized search structure. For codebase-only research, use `/deep-research --source local`. For hybrid research (web + codebase), use `/deep-research --source hybrid`.
20. **Importance classification.** Not everything needs recording. Use this guide:
   - **Must record:** Decisions, milestone completions, priority changes, new blockers, revenue events, product launches/deploys.
   - **Should record:** Task completions on tracked items, external events reported by user, configuration changes.
   - **Skip:** Typo fixes, exploratory reads, conversation-only exchanges, research that leads nowhere.
21. **Completion protocol (mid-session).** When the user signals a tracked item is done, update `active/now.md` and `active/priorities.md` immediately. If it's a milestone, move it to "What's Done" in now.md and update `MEMORY.md`. Don't wait for session close. Offer to commit the state change.
22. **Artifact follow-through (mandatory).** When any artifact or output is generated (research docs, drafts, deliverables, configs, landing pages, templates, plans), immediately determine its disposition:
   - **Where does it go?** Confirm it's saved in the correct location per file conventions.
   - **What's next?** Add the next action to `active/now.md` (e.g., "Review research for launch campaign", "Deploy site to Netlify", "Publish to Substack").
   - **Cross-reference:** If the artifact serves an existing tracked task, add a reference to that task in `active/now.md`.
   - Even if the only next step is "review this", add it. No artifact should be generated without a trail back to active state.
