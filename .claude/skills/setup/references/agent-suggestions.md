# Agent Suggestions

> Referenced by: `.claude/skills/setup/SKILL.md` — Phase 9

---

Print educational beat: "39 agents ship by default across 5 categories (Governance, Knowledge, Technical, Business, Evolution). The system is designed to be extended — custom agents follow the same format and get the same capabilities."

Based on the user's domain from Phase 2, suggest relevant custom agents. Examples:

| User Domain | Suggested Agents |
|-------------|-----------------|
| Web dev | api-designer, frontend-specialist, performance-analyst |
| Data science | data-engineer, ml-ops, experiment-tracker |
| DevOps | incident-responder, capacity-planner, sre |
| Consulting | proposal-writer, client-manager, deliverable-tracker |
| Creative | content-strategist, brand-guardian, campaign-manager |

Present suggestions and ask:
1. "Want to create any of these? Or describe a custom agent you need."

**Before creating agents, recommend plan mode:**

Print: "**Recommended:** Before we create agents, switch to **Plan mode** (type `/plan`) and select **Opus 4.6 (medium)** or equivalent as your model. Agent creation involves designing responsibilities, writing definitions, creating symlinks, and updating the registry — Plan mode lets you review and approve each step before it happens.

Once you approve the plan and agents are created, you can jump right back into onboarding where you left off — just run `/setup --phase 10` (or whatever phase is next). The conversation auto-compacts, so your context is preserved even if the conversation gets long."

2. For each requested agent, run `/add-agent` (the add-agent skill) to create it properly.
3. "Want to hide any default agents that aren't relevant? (This removes symlinks but keeps the files.)"
   - If yes, remove the selected symlinks. The agent files remain in their category directories.

Print: "Agent roster customized."
