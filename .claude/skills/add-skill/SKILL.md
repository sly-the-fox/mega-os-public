---
name: add-skill
description: Use when creating a new skill — handles directory, SKILL.md, and all index/doc updates in sync.
invocation: /add-skill
user_invocable: true
---

# Add Skill

Create a new skill and update all references so everything stays in sync.

## Steps

1. **Collect info** — Ask the user:
   - Skill name (must be lowercase kebab-case, e.g., `my-skill`)
   - One-line description (what does this skill do?)
   - Invocation command (e.g., `/my-skill`)
   - User-invocable? (yes/no — can users call it directly?)
   - Arguments (optional — what arguments does it accept?)

   **Validate:**
   - Name is kebab-case (lowercase letters, numbers, hyphens only)
   - No existing directory at `.claude/skills/<name>/`
   - Invocation starts with `/`

2. **Create skill directory and file** — Write `.claude/skills/<name>/SKILL.md` with this structure:

   ```markdown
   ---
   name: <name>
   description: <one-line description>
   invocation: /<name>
   user_invocable: <true/false>
   ---

   # <Name (Title Case)>

   <Description of what this skill does.>

   ## Steps

   1. **Step one** — ...
   2. **Step two** — ...

   ## Output

   <What this skill produces.>
   ```

   Ask the user to provide or confirm the steps. Suggest reasonable defaults based on the name and description.

3. **Update skills-reference.md** — Read `core/standards/skills-reference.md`. Add the new skill as a new row in the table, using the next sequential number. Maintain the existing table format:
   ```
   | # | Skill | Command | Location | Purpose |
   ```

4. **Update canonical-files.md** — Read `core/indexes/canonical-files.md`:
   - Add `.claude/skills/<name>/SKILL.md` to the Skills section (maintain alphabetical order)
   - Increment the skills count in the section header (e.g., `## Skills (22)` → `## Skills (23)`)

5. **Update project-map.md** — Read `core/indexes/project-map.md`:
   - Add the skill name to the `skills/` line in the directory tree (maintain alphabetical order within the comma-separated list)

6. **Update README.md** — Read `README.md`:
   - Increment the slash command count (e.g., "22 slash commands" → "23 slash commands")
   - Add the skill to the appropriate Commands table section (Daily Operations, Building & Creating, System Management, or Deployment & Updates)

7. **Update MEMORY.md** — Read the memory file at the path shown in the project memory index:
   - Update the skills count and add the new skill name to the skills list

8. **Verify** — Run the integrity check script if it exists:
   ```bash
   bash engineering/scripts/check-index-integrity.sh
   ```
   If it reports mismatches, fix them before proceeding.

9. **Cross-check** — Suggest running `/framework-sync --validate-only` to verify all cross-references are consistent after the skill addition.

10. **Commit** — Stage all changed files and offer to commit:
   ```
   system: add /<name> skill for <description>
   ```

Print summary of all files created/modified.
