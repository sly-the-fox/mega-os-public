# Cross-Reference Map

Exhaustive mapping of framework file changes to documentation updates. Used by `/framework-sync` to determine what needs reconciling.

---

## Category A: Agent Changes

**Trigger:** Files added/removed/renamed under `.claude/agents/{governance,knowledge,technical,business,evolution}/*.md`

| Target File | What to Update |
|---|---|
| `.claude/agents/REGISTRY.md` | Add/remove row in category table, update total agent count |
| `AGENTS.md` | Update category count in header, add/remove agent description |
| `CLAUDE.md` | Update count in "What This Is" table (governance, knowledge, technical, business, evolution columns) |
| `README.md` | Update "N AI agents" count, update agent listing if present |
| `core/indexes/canonical-files.md` | Add/remove agent file entry in Agents section, update section count |
| `core/indexes/project-map.md` | Add/remove agent name in category listing |
| `.claude/agents/shared/agent-capabilities.md` | Add/remove capability profile entry (if file exists) |

**Symlink check:** If agent added/removed, verify symlink exists at `.claude/agents/<name>.md` pointing to `<category>/<name>.md`.

---

## Category B: Shared Agent Framework Changes

**Trigger:** Files modified under `.claude/agents/shared/*.md` (system-rules.md, workflows.md, etc.)

| Target File | What to Update |
|---|---|
| `CLAUDE.md` | Update workflow summaries (if workflows.md changed), update rule references |
| `AGENTS.md` | Update workflow descriptions (if workflows.md changed) |

Note: Only workflows.md changes require cross-reference updates. Other shared files (system-rules.md, definitions.md) are self-contained.

---

## Category C: Skill Changes

**Trigger:** Directories/files added/removed under `.claude/skills/*/SKILL.md`

| Target File | What to Update |
|---|---|
| `core/standards/skills-reference.md` | Add/remove row in skill table |
| `CLAUDE.md` | Update skill count (e.g., "Skills (25)" in Configuration comment or MEMORY reference) |
| `README.md` | Update slash command count, add/remove from Commands table |
| `core/indexes/canonical-files.md` | Add/remove skill file entry, update Skills section count |
| `core/indexes/project-map.md` | Add/remove skill name in skills listing |
| `GETTING_STARTED.md` | Only if skill is onboarding-relevant (manual judgment) |
| `.claude/skills/setup/SKILL.md` | Only if skill changes Phase 0 commands overview |
| `.claude/skills/setup/references/cron-jobs.md` | Only if skill is automatable via cron |

---

## Category D: Standard/Template Changes

**Trigger:** Files added/removed under `core/standards/*.md` or `core/templates/*.md`

| Target File | What to Update |
|---|---|
| `core/indexes/canonical-files.md` | Add/remove file entry in Standards or Templates section, update section count |
| `core/indexes/project-map.md` | Update standards or templates listing |
| `CLAUDE.md` | Only if standard is directly referenced in Quick Orientation section |

---

## Category E: Script Changes

**Trigger:** Files added/removed under `engineering/scripts/*`

| Target File | What to Update |
|---|---|
| `core/indexes/project-map.md` | Update scripts listing |
| `.claude/skills/setup/references/cron-jobs.md` | Only if script is a new cron job |
| `core/standards/skills-reference.md` | Only if script backs a skill |

---

## Category F: Workflow Changes

**Trigger:** `.claude/agents/shared/workflows.md` modified

| Target File | What to Update |
|---|---|
| `CLAUDE.md` | Update "Agent Workflows" section — workflow step sequences and summaries |
| `AGENTS.md` | Update "Key Workflows" section |
| `README.md` | Update workflow count if a new workflow type was added |

---

## Category G: Sync Manifest Changes

**Trigger:** `engineering/sync-manifest.json` modified

| Target File | What to Update |
|---|---|
| `CLAUDE.md` | Update Data Classification table (if new include/exclude category) |
| Run privacy scan | Validate no privacy leaks with new patterns |

---

## Anti-Loop Rule

Root docs (`CLAUDE.md`, `AGENTS.md`, `README.md`, `GETTING_STARTED.md`) are **targets** of cross-reference updates, never **triggers**. Editing them directly does NOT re-invoke framework-sync. Only changes to source files (Categories A-G triggers) cause updates to flow to targets.

---

## Count Sources of Truth

When updating counts, always compute from the filesystem:

| Count | How to Compute |
|---|---|
| Agent count per category | `ls .claude/agents/<category>/*.md \| wc -l` (exclude README.md if present) |
| Total agent count | Sum of all category counts |
| Skill count | `ls -d .claude/skills/*/SKILL.md \| wc -l` |
| Standard count | `ls core/standards/*.md \| wc -l` |
| Template count | `ls core/templates/*.md \| wc -l` |
| Script count | `ls engineering/scripts/* \| wc -l` |

Never increment/decrement existing values. Always recount from disk. This ensures idempotency.
