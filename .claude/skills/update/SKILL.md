---
name: update
description: Pull framework updates from the upstream Mega-OS public repo.
invocation: /update
user_invocable: true
---

# Update

Pulls framework updates from the upstream Mega-OS repository into your local clone.

## Steps

0. **Configure merge driver** — Run `git config merge.ours.driver true`. This activates the `merge=ours` strategy used by `.gitattributes` to protect your personal data directories during merges. Without this, the merge directives are silently ignored.

1. **Check upstream remote** — Run `git remote -v` and look for an `upstream` remote.

   - If `upstream` exists, continue to step 2.
   - If not, ask: "No upstream remote found. Add the Mega-OS public repo as upstream?"
     - If yes: `git remote add upstream https://github.com/sly-the-fox/mega-os-public.git`
     - If no: stop.

2. **Stash uncommitted work** — Run `git stash` to save any uncommitted changes. Print: "Your uncommitted changes have been stashed for safety."

3. **Fetch** — Run `git fetch upstream`.

4. **Check for updates** — Run `git log HEAD..upstream/master --oneline`.

   - If no new commits, say "You're up to date with upstream. No changes to pull." and stop. If work was stashed in step 2, run `git stash pop`.
   - If there are new commits, show them to the user.

5. **Show what changed** — Run `git diff HEAD..upstream/master --stat` to show which files were modified upstream.

6. **Confirm** — Ask: "Merge these upstream updates?"

7. **Merge** — Run `git merge upstream/master`.

   - **If clean merge:** Commit is automatic. Print "Framework updated successfully."
   - **If conflicts:** Run `git diff --name-only --diff-filter=U` to list conflicting files.
     - For each conflicting file, explain what it is and suggest resolution:
       - `CLAUDE.md` — Look for `<!-- USER CONFIG START/END -->` markers. Keep user content between markers, accept upstream changes outside markers.
       - `active/*.md` — Always keep yours (`git checkout --ours <file>`). Your state is more important than upstream stubs. (The `merge=ours` driver should handle this automatically.)
       - `.claude/settings.json` — Merge carefully. Keep your permissions and hooks, accept new upstream defaults.
       - Agent/skill files — Usually accept upstream (`git checkout --theirs <file>`) unless you've customized them.
       - Standards — Accept upstream, then re-apply your customizations at the bottom.
     - After resolution, stage and commit: `git add . && git commit -m "merge: upstream framework update"`

8. **Restore stashed work** — If work was stashed in step 2, run `git stash pop` to restore it.

9. **Verify** — Run Claude Code's SessionStart check (read `active/now.md`) to confirm everything still loads correctly.

10. **Report** — Print summary and safety notice:
   ```
   Framework updated:
   - [N] new commits from upstream
   - Conflicts: [none / list]
   - Status: clean

   Your personal data (active/, business/, products/, etc.) is protected
   by merge=ours rules and was not modified by this update.

   If something looks wrong:
   - During merge: git merge --abort
   - After merge committed: git reset --hard HEAD~1
   - Your pre-update uncommitted work was stashed and has been restored.
   ```

## Notes

- This only pulls framework changes (agents, skills, standards, templates, scripts). Your personal data in `active/`, `business/`, `products/` etc. is never overwritten by upstream — `.gitattributes` with `merge=ours` protects these directories automatically.
- Step 0 configures the merge driver that activates this protection. Without it, the `.gitattributes` directives are silently ignored by git.
- If a merge goes wrong: `git merge --abort` (during merge) or `git reset --hard HEAD~1` (after merge committed).
- Run `/update` periodically (e.g., weekly) to get new agents, skills, and bug fixes.
