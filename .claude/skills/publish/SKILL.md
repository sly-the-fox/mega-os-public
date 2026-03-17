---
name: publish
description: Sync framework changes to the public Mega-OS repo and push.
invocation: /publish
user_invocable: true
---

# Publish

Syncs framework changes from the private repo to the public distribution repo and optionally pushes.

## Steps

1. **Validate** — Run `engineering/scripts/validate-public.sh` to check coverage, privacy, symlinks, and bootstrappability.
   - If validation **fails**: show the report and **stop**. Do not proceed to sync. Tell the user what needs to be fixed.
   - If validation **passes**: continue to step 2.

2. **Dry run** — Run `engineering/scripts/sync-to-public.sh` (no flags) to show what changed.

3. **Review** — Show the user the list of NEW and MOD files. If nothing changed, say "Public repo is up to date" and stop.

4. **Confirm** — Ask: "Sync these files to the public repo?"

5. **Sync** — If confirmed, run `engineering/scripts/sync-to-public.sh --sync`. The script copies files, stages, and prompts for a commit message.

   Since the script is interactive (asks for commit message and push confirmation), run it in a way that passes through:
   - Suggest a commit message based on the changes shown (e.g., `sync: update agents and skills`)
   - After the sync completes, `cd ~/mega-os-public && git status` to confirm the state

6. **Push** — Ask: "Push to public remote?" If yes, run `cd ~/mega-os-public && git push`.

7. **Report** — Print summary:
   ```
   Published to mega-os-public:
   - [N] files synced
   - Commit: [message]
   - Pushed: yes/no
   ```

## Notes

- The sync system reads `engineering/sync-manifest.json` — directory-based rules mean new files in framework directories sync automatically. No manual registration needed.
- Privacy patterns in the manifest are checked before every sync. If a file matches, sync is blocked.
- The public repo has sanitized stubs (generic `active/now.md`, empty `business/`, etc.) so new users get a working skeleton.
- To exclude a new file from syncing, add it to the `exclude` array in `engineering/sync-manifest.json`.
