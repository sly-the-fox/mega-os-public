---
name: publish
description: Sync framework changes to the public Mega-OS repo and push.
invocation: /publish
user_invocable: true
---

# Publish

Syncs framework changes from the private repo to the public distribution repo and optionally pushes.

## Steps

1. **Dry run** — Run `engineering/scripts/sync-to-public.sh` (no flags) to show what changed.

2. **Review** — Show the user the list of NEW and MOD files. If nothing changed, say "Public repo is up to date" and stop.

3. **Confirm** — Ask: "Sync these files to the public repo?"

4. **Sync** — If confirmed, run `engineering/scripts/sync-to-public.sh --sync`. The script copies files, stages, and prompts for a commit message.

   Since the script is interactive (asks for commit message and push confirmation), run it in a way that passes through:
   - Suggest a commit message based on the changes shown (e.g., `sync: update agents and skills`)
   - After the sync completes, `cd ~/mega-os-public && git status` to confirm the state

5. **Push** — Ask: "Push to public remote?" If yes, run `cd ~/mega-os-public && git push`.

6. **Report** — Print summary:
   ```
   Published to mega-os-public:
   - [N] files synced
   - Commit: [message]
   - Pushed: yes/no
   ```

## Notes

- The sync script uses a whitelist (`SAFE_PATHS`) — only framework files are copied. Personal data in `active/`, `business/`, `products/`, `core/history/`, etc. is never synced.
- The public repo has sanitized stubs (generic `active/now.md`, empty `business/`, etc.) so new users get a working skeleton.
- If you need to add a new path to the whitelist, edit `engineering/scripts/sync-to-public.sh`.
