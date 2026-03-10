---
name: update
description: Pull framework updates from the upstream Mega-OS public repo.
invocation: /update
user_invocable: true
---

# Update

Pulls framework updates from the upstream Mega-OS repository into your local clone.

## Steps

1. **Check upstream remote** — Run `git remote -v` and look for an `upstream` remote.

   - If `upstream` exists, continue to step 2.
   - If not, ask: "No upstream remote found. Add the Mega-OS public repo as upstream?"
     - If yes: `git remote add upstream https://github.com/sly-the-fox/mega-os-public.git`
     - If no: stop.

2. **Fetch** — Run `git fetch upstream`.

3. **Check for updates** — Run `git log HEAD..upstream/master --oneline`.

   - If no new commits, say "You're up to date with upstream. No changes to pull." and stop.
   - If there are new commits, show them to the user.

4. **Show what changed** — Run `git diff HEAD..upstream/master --stat` to show which files were modified upstream.

5. **Confirm** — Ask: "Merge these upstream updates?"

6. **Merge** — Run `git merge upstream/master`.

   - **If clean merge:** Commit is automatic. Print "Framework updated successfully."
   - **If conflicts:** Run `git diff --name-only --diff-filter=U` to list conflicting files.
     - For each conflicting file, explain what it is and suggest resolution:
       - `CLAUDE.md` — Look for `<!-- USER CONFIG START/END -->` markers. Keep user content between markers, accept upstream changes outside markers.
       - `active/*.md` — Always keep yours (`git checkout --ours <file>`). Your state is more important than upstream stubs.
       - `.claude/settings.json` — Merge carefully. Keep your permissions and hooks, accept new upstream defaults.
       - Agent/skill files — Usually accept upstream (`git checkout --theirs <file>`) unless you've customized them.
       - Standards — Accept upstream, then re-apply your customizations at the bottom.
     - After resolution, stage and commit: `git add . && git commit -m "merge: upstream framework update"`

7. **Verify** — Run Claude Code's SessionStart check (read `active/now.md`) to confirm everything still loads correctly.

8. **Report** — Print summary:
   ```
   Framework updated:
   - [N] new commits from upstream
   - Conflicts: [none / list]
   - Status: clean
   ```

## Notes

- This only pulls framework changes (agents, skills, standards, templates, scripts). Your personal data in `active/`, `business/`, `products/` etc. is never overwritten by upstream — upstream has only empty stubs for those paths.
- If a merge goes wrong, you can always `git merge --abort` to undo.
- Run `/update` periodically (e.g., weekly) to get new agents, skills, and bug fixes.
