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
13. When producing text that will be published or sent as the user's voice — including social media replies, comments, bios, DMs, emails, and any content the user might post — read and apply `core/standards/writing-style.md` including platform-specific adaptations. This applies regardless of whether the task was classified as a "quick action." Do not use em dashes in any user-voice content; use commas, parentheses, or restructure instead.
14. **Historian vs PM file ownership:** Both update `active/now.md` and `active/priorities.md` (shared ownership). Historian owns `core/history/` files (decisions, timeline, current-state). PM owns `active/` operational files (inbox, blockers). When both are triggered by the same event, PM updates active state first, then Historian records in history.
15. **Freshness verification:** Custodian runs as a penultimate workflow step (before Historian) to verify all triggered agent checklists completed and cross-references are consistent. Custodian does not rewrite content — it flags, archives, or escalates. Critical staleness (>2 days inbox, >5 days blockers) triggers PM and Sentinel alert.
16. **Session-end recording (mandatory).** Before ending any session where significant work occurred (decisions, file changes, priority shifts, milestones), run the Historian Checklist (rule 7) directly. This applies even for tasks that skip full workflows.
17. **Plans require agent graphs.** Every plan in `.claude/plans/` must include an Agent Assignment Graph table (step, agent, task, depends-on, condition). Use `core/templates/plan-template.md`.
18. **Coherence+Parallax checkpoint (mandatory during testing phase).** At documented workflow checkpoints (Planning step 1b, Technical step 1b, Business step 1b, Evolution Loop), run the Coherence+Parallax Checkpoint Protocol per `core/standards/coherence-checkpoint-protocol.md`. Skip for small changes (< 3 files, no auth/crypto/input handling/secrets/API boundaries). Log all invocations to `active/coherence-metrics.md`.
19. **MECE research (mandatory for web research).** When any task or workflow step requires web research (WebSearch/WebFetch), use the MECE deep research pattern via `/deep-research`. This applies to all workflows — Planning (Planner research), Content (Librarian source gathering), Business (Strategist market research), and Knowledge (Librarian information gathering). The only exception is the `/news-briefing` skill, which has its own specialized search structure. For codebase-only research, use `/deep-research --source local`. For hybrid research (web + codebase), use `/deep-research --source hybrid`.
20. **Importance classification.** Not everything needs recording. Use this guide:
   - **Must record:** Decisions, milestone completions, priority changes, new blockers, revenue events, product launches/deploys.
   - **Should record:** Task completions on tracked items, external events reported by user, configuration changes, deferred decisions with rationale, exploration outcomes that inform future work, user preferences/corrections discovered mid-session.
   - **Context journal candidates:** Reasoning behind non-obvious choices, exploration paths tried and abandoned, deferred work with enough context to resume, session-specific context that future sessions might need.
   - **Skip:** Typo fixes, exploratory reads that lead nowhere, conversation-only exchanges, information already captured in code comments or commit messages.
21. **Completion protocol (mid-session).** When the user signals a tracked item is done, update `active/now.md` and `active/priorities.md` immediately. If it's a milestone, move it to "What's Done" in now.md and update `MEMORY.md`. Don't wait for session close. Offer to commit the state change.
22. **Artifact follow-through (mandatory).** When any artifact or output is generated (research docs, drafts, deliverables, configs, landing pages, templates, plans), immediately determine its disposition:
   - **Where does it go?** Confirm it's saved in the correct location per file conventions.
   - **What's next?** Add the next action to `active/now.md` (e.g., "Review research for launch campaign", "Deploy site to Netlify", "Publish to Substack").
   - **Cross-reference:** If the artifact serves an existing tracked task, add a reference to that task in `active/now.md`.
   - Even if the only next step is "review this", add it. No artifact should be generated without a trail back to active state.
23. **Archive search protocol.** When a user asks about past events or information not in active state:
    1. Read `archive/index.json` and identify the relevant week bucket.
    2. If user specifies a time frame, go directly to that bucket.
    3. If no time frame, search the 2-3 most recent week buckets.
    4. Read the specific archived file(s).
    5. Never preload archive content.
25. **Uncertainty Escalation Protocol.** When an agent team member encounters genuine uncertainty that could lead to materially wrong output, they must escalate rather than guess.

    **Escalate when:**
    - Requirements are ambiguous and different interpretations lead to materially different outputs
    - Multiple valid approaches exist with tradeoffs only the user can weigh
    - The agent is about to make an assumption that, if wrong, requires significant rework
    - Context is missing that only the user can provide (not derivable from project files)
    - The action is irreversible or high-impact (deploys, deletes, external communication, financial)

    **Do NOT escalate when:**
    - The action is easily reversible (file edits, drafts)
    - Standards or conventions already answer the question
    - The uncertainty is cosmetic (formatting, naming, ordering)
    - A reasonable default exists and the downside of being wrong is minimal

    **How to escalate (team members):**
    Send a structured message to the team lead via `SendMessage`:
    ```
    UNCERTAIN: [one-line summary of what's unclear]
    OPTIONS: [2-3 possible paths the agent sees]
    DEFAULT: [what the agent would do if forced to choose]
    RISK: [what goes wrong if the default is wrong]
    ```

    **How the team lead handles it:**
    - If resolvable from project context, respond directly to the team member
    - If it requires user judgment, surface via `AskUserQuestion` immediately
    - Do not batch uncertainty questions — surface them as they arrive
    - After receiving the answer, relay it back to the team member via `SendMessage`
26. **Team usage enforcement.** Before executing any multi-step task:
   1. Classify: quick-action (< 5 min, < 3 files) / focused (single specialist) / multi-step (2+ agents).
   2. Multi-step tasks MUST use TeamCreate with appropriate specialists.
   3. Focused tasks SHOULD use TeamCreate unless single-agent, single-file.
   4. Quick actions proceed directly.
   5. Standalone Agent tool is permitted for: (a) read-only research/exploration (including Coherence+Parallax checkpoints), and (b) parallelizable file-writing work when spawned with `isolation: "worktree"`. Worktree-isolated agents get their own git worktree and cannot interfere with the main working tree. See rule 27 for the required protocol.
   6. Governor validates team usage at workflow boundaries.
27. **Worktree isolation protocol.** Governs the worktree exception in rule 26.5. When spawning standalone agents with `isolation: "worktree"`:

    **Use when ALL of these apply:**
    - The task produces file changes (not read-only)
    - The work is independent (no mid-task dependency on other agents' output)
    - Parallel execution saves meaningful time (2+ agents can run concurrently)

    **Do NOT use when:**
    - Work is sequential and depends on prior agent output
    - The task modifies active state files (`active/`, `core/history/`, `core/indexes/`)
    - The task is trivial (single file, < 5 min)
    - Agents need to coordinate mid-task via SendMessage
    - The workflow is Content, Knowledge, or Business (sequential by nature)

    **Governance gate:** Before spawning worktree-isolated agents, confirm:
    1. Tasks are truly independent (no shared file modifications)
    2. Workflow type is eligible (Technical, Incident, or Planning only)
    3. Concurrency limit: max 3 simultaneous worktrees

    **Merge-back rules:**
    - Main context is ALWAYS the merge-back owner. Agents never merge their own work.
    - After a worktree agent completes, review its diff before merging.
    - Merge ordering: Security-Expert merges first (security takes priority). Then other agents alphabetically.
    - Use `git merge --no-ff <worktree-branch>` to preserve isolation boundary in history.
    - If the second merge conflicts with the first, the relevant specialist reviews the resolution.
    - If conflicts are non-trivial, abandon parallel results and re-run the task sequentially.
    - If the agent made no changes, cleanup is automatic.
    - After merge, run relevant tests/verification. If tests fail, `git merge --abort` or `git reset --hard HEAD~1` to pre-merge state and re-run sequentially.

    **Failure and cleanup:**
    - If a worktree agent crashes or times out, its worktree is abandoned (no merge).
    - Orphaned worktrees are cleaned periodically with `git worktree prune`.
    - After merge, verify no `active/`, `core/history/`, or `core/indexes/` files were modified. If they were, revert those specific files with `git checkout HEAD~1 -- <path>`.

    **State files:** Worktree agents must NOT modify `active/`, `core/history/`, or `core/indexes/`. If a worktree agent needs to record findings, it writes to a scratch file in its worktree and the main context triages after merge.

28. **Date integrity.** When writing any day+date combination (e.g., "Wed Mar 25", "Thu 2026-03-26"):
    - NEVER calculate day-of-week mentally. Run `date -d "YYYY-MM-DD" +%A` to get the authoritative day name.
    - When adding events, deadlines, or follow-ups with day names, validate EVERY instance before writing.
    - If a date already exists in another file (contacts.md, prep docs), verify it against `date` before copying — don't assume the source is correct.
    - Preferred format for events: `Day YYYY-MM-DD` (e.g., "Thu 2026-03-26") — unambiguous, machine-parseable.
    - Reference `active/week-calendar.md` for a quick day+date lookup when available.
