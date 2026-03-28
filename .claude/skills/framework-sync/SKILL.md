---
name: framework-sync
description: Use after modifying framework files — reconciles documentation counts, cross-references, index files, and validates sync-manifest integrity. Auto-triggered via PreToolUse hook on git commit.
invocation: /framework-sync
user_invocable: true
arguments: ["--validate-only", "--last-commit", "--files <paths>"]
---

# Framework Sync

Reconciles documentation cross-references after framework files change. Detects which framework files were modified, maps them to dependent documentation, updates counts and listings, validates integrity, and checks sync-manifest compliance.

**When this runs:** Automatically prompted by a PreToolUse hook before `git commit` when staged files include framework paths. Can also be invoked manually.

**When this does NOT run:** Changes to user data files (`active/`, `business/`, `products/`, `drafts/`, `deliverables/`, `archive/`). Edits to root docs (CLAUDE.md, README.md) alone do not trigger — only source file changes do.

## Arguments

- `--validate-only` — Run checks without making changes (used by `/publish` as a pre-gate)
- `--last-commit` — Detect changes from the last git commit instead of staged/unstaged
- `--files <path1> <path2> ...` — Explicitly specify which files changed
- (no args) — Auto-detect from git staged + unstaged changes

## Steps

### Phase 1: Detect Changes

1. **Identify changed framework files.**
   - No args: `git diff --cached --name-only` (staged) + `git diff --name-only` (unstaged modified)
   - `--last-commit`: `git diff --name-only HEAD~1 HEAD`
   - `--files`: use provided list

2. **Filter to framework source files only.** Match against these trigger paths:
   - `.claude/agents/{governance,knowledge,technical,business,evolution}/*.md`
   - `.claude/agents/shared/*.md`
   - `.claude/agents/REGISTRY.md`
   - `.claude/skills/*/SKILL.md` (and new skill directories)
   - `core/standards/*.md`
   - `core/templates/*.md`
   - `engineering/scripts/*`
   - `engineering/sync-manifest.json`
   - `.claude/agents/shared/workflows.md`

   **Exclude (anti-loop targets):** `CLAUDE.md`, `AGENTS.md`, `README.md`, `GETTING_STARTED.md` — these are update targets, not triggers.

3. **If no framework source files changed,** print "No framework changes detected." and stop.

4. **Categorize changes** into groups per `references/cross-reference-map.md`:
   - A: Agent changes
   - B: Shared agent framework changes
   - C: Skill changes
   - D: Standard/template changes
   - E: Script changes
   - F: Workflow changes
   - G: Sync manifest changes

### Phase 2: Map Required Updates

5. **Read actual filesystem state** — these are the sources of truth:
   - Count agent `.md` files per category directory (exclude README.md)
   - Count skill directories with SKILL.md
   - Count standard files, template files, scripts
   - Read current workflow step sequences from workflows.md

6. **Read current documentation values** from each target file listed in the cross-reference map for the detected categories. Extract:
   - Agent counts in REGISTRY.md, AGENTS.md, CLAUDE.md, README.md
   - Skill counts in skills-reference.md, CLAUDE.md, README.md
   - Table entries and listings in index files
   - Workflow summaries in CLAUDE.md

7. **Compute deltas.** For each target, compare actual vs documented. Skip files already correct.

8. **Present update plan to user:**
   ```
   Framework changes detected in [N] files ([categories]).
   Documentation updates needed:
   - REGISTRY.md: agent count 39 -> 40
   - CLAUDE.md: governance count 9 -> 10, skill count 25 -> 26
   - README.md: slash command count 25 -> 26
   - ...

   Proceed with updates? (Y/n)
   ```

   If `--validate-only`, show the plan but do not proceed to Phase 3.

### Phase 3: Apply Updates

9. **Update each target file.** For each file needing changes:
   - Read current content
   - Apply the specific update (count fix, row addition/removal, listing update)
   - Write updated content

   **Idempotency rule:** Always compute counts from the filesystem. Never increment/decrement relative to existing doc values. Running the skill twice produces the same result.

10. **Handle table updates:**
    - For agent tables: use agent filename (minus `.md`) as the unique key
    - For skill tables: use skill directory name as the unique key
    - Check if row already exists before adding; skip if present and correct

11. **Symlink verification** (for agent changes): Ensure `.claude/agents/<name>.md` symlink exists pointing to `<category>/<name>.md`. Create if missing.

### Phase 4: Validate

12. **Run integrity check:**
    ```bash
    bash engineering/scripts/check-index-integrity.sh
    ```
    If mismatches reported, attempt to fix. If unfixable, report to user.

13. **Run sync validation** (if `../mega-os-public/` exists):
    ```bash
    bash engineering/scripts/sync-to-public.sh --validate
    ```
    Report coverage, privacy, symlink, and bootstrappability status.

14. **Privacy scan.** For each changed framework file, scan content against `privacy_patterns` from `engineering/sync-manifest.json`. Report any matches not in the `privacy_allowlist`.

15. **Placeholder check** (if public repo exists). For any private paths referenced by framework files that need representation in the public repo, verify placeholder stubs exist. List any missing. Do NOT create placeholders — flag them for `/publish` to handle.

### Phase 5: Report

16. **Print summary:**
    ```
    Framework sync complete:
    - Changed framework files: [N]
    - Documentation files updated: [N] ([list])
    - Integrity check: PASS / FAIL ([details])
    - Sync validation: PASS / FAIL / SKIPPED (no public repo)
    - Privacy scan: CLEAN / [issues]
    - Missing placeholders: none / [list]
    ```

17. **Offer commit** (if any files were modified and not `--validate-only`):
    ```
    system: sync framework docs after [agent/skill/workflow/standard] changes
    ```

## Integration Points

- **Hook trigger:** PreToolUse on `Bash(git commit*)` runs `detect-framework-changes.sh` as a reminder
- **Workflow insertion:** Conditional step after Reviewer, before Documenter in Technical and Planning workflows
- **Used by `/publish`:** Step 0 runs `/framework-sync --validate-only` as pre-gate
- **Used by `/add-agent` and `/add-skill`:** Final cross-check suggestion

## Cross-Reference Map

See `references/cross-reference-map.md` for the exhaustive mapping of which framework file changes require which documentation updates.
