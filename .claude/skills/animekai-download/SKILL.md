---
name: animekai-download
description: Download anime episodes from animekai.to using Playwright MCP browser automation.
invocation: /animekai-download
user_invocable: true
---

# Anime Download — animekai.to via Playwright MCP

Download anime episodes from animekai.to using Playwright MCP browser automation.

## Invocation
```
/animekai-download <show-url> [--start N] [--end N] [--audio dub|sub] [--resolution 1080|720|360]
```

## Parameters
| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `show-url` | Yes | — | animekai.to watch page URL for the season |
| `--start` | No | 1 | First episode to download |
| `--end` | No | last | Last episode to download |
| `--audio` | No | `dub` | `dub` or `sub` |
| `--resolution` | No | `1080` | `1080`, `720`, or `360` |

## Examples
```
/animekai-download https://animekai.to/watch/my-little-pony-friendship-is-magic-season-1-dub-2kpr
/animekai-download https://animekai.to/watch/naruto-shippuden-dub-xyz --start 15 --end 26
/animekai-download https://animekai.to/watch/some-show --audio sub --resolution 720
```

## Defaults
- **Audio**: Dub (override with `--audio sub`)
- **Resolution**: 1920x1080
- **Download destination**: `/home/abzu/Video Media/` — files accumulate here, user moves them to final location
- **File naming**: Whatever megaup provides (e.g. `YP-1R-01x17-1080.mp4`)

## Prerequisites
- Playwright MCP server running (configured in `.mcp.json`)
- Anti-detection init script: `engineering/scripts/playwright-adblock.js`
- Do NOT modify `playwright-adblock.js` or `.mcp.json`

---

## Workflow

### Step 1: Setup

1. Parse arguments — extract show URL, start/end episode numbers, audio preference, resolution
2. Navigate to the show URL using `mcp__playwright__browser_navigate`
3. Take a snapshot to confirm page loaded
4. Read the episode list to determine total episode count
5. Validate `--start` and `--end` against available episodes
6. Report to user: "Downloading episodes X-Y of Z, audio: {dub|sub}, resolution: {1080|720|360}p"

### Step 2: Per-Episode Loop

For each episode N from `--start` to `--end`:

#### 2a. Select Episode
- Click episode N in the episode list

#### 2b. Select Audio Track
- Click "Dub" button (or "Hard Sub" for `--audio sub`)
- **CRITICAL — Known bug after MCP restart**: The first click may not actually switch the audio track. Always verify by checking that:
  - The comments section says "Episode N dub" (or "Episode N sub")
  - Duration matches expectations (~22:00 for dub, ~23:30 for sub)
- If verification fails, click the audio button again and re-verify

#### 2c. Wait for Player
- Wait ~5 seconds for JWPlayer iframe to load inside the megaup.nl embed

#### 2d. Pause Video
- Target the iframe containing the video player
- Execute: `frame.evaluate(() => document.querySelector('video').pause())`
- This reduces bandwidth competition during download

#### 2e. Extract Download URL
- Intercept `window.open` to capture the megaup download URL:
```js
frame.evaluate(() => new Promise(resolve => {
  const orig = window.open;
  window.open = function(url) { resolve(url); window.open = orig; return null; };
  document.querySelector('.jw-tooltip-download').parentElement.click();
  setTimeout(() => resolve('timeout'), 5000);
}));
```
- If result is `'timeout'`, retry once. If still timeout, log failure and skip to next episode.

#### 2f. Open megaup.cc
- Open a new tab
- Navigate to the extracted megaup.cc URL

#### 2g. Verify Episode
- Confirm the filename displayed on megaup contains the correct episode number
- If wrong episode, close tab and retry from step 2a

#### 2h. Select Resolution
- Click the matching resolution option (1080/720/360)

#### 2i. Wait for Countdown
- If a countdown timer appears, wait until the Download button becomes enabled
- Some episodes have no countdown, some have ~30s

#### 2j. Click Download
- **MUST use evaluate(), NEVER Playwright `.click()`**:
```js
page.evaluate(() => document.querySelector('button.btn').click());
```

#### 2k. Monitor Download
- Switch to the download history tab (chrome://downloads/ or equivalent)
- Check progress every 2 minutes until the file shows as complete
- Files download to `/home/abzu/Video Media/` or Playwright's temp directory

#### 2l. Cleanup
- Close the megaup.cc tab
- Return to the animekai.to tab
- Proceed to next episode

### Step 3: Post-Download Report

After all episodes are attempted:
1. List completed episodes with file paths
2. List any failed episodes with failure reason
3. Suggest retry command for failed episodes if any

---

## Key Rules

These rules are **non-negotiable**. They exist because violating them causes real failures.

1. **NEVER double-click** the download button — triggers duplicate downloads or blocks
2. **NEVER use Playwright `.click()`** for the download button — only `page.evaluate(() => ...)`. Playwright's click intercepts navigation and breaks the download
3. **NEVER interact with ad/popup tabs** — close them by checking hostname. Flixzone URLs contain "animekai.to" in query params; close any tab whose URL doesn't match expected domains (animekai.to, megaup.cc, megaup.nl)
4. **Pause video before extracting URL** — reduces bandwidth competition during download
5. **After MCP restart**: audio selection state resets. Must click the audio button and verify via comments section. First click may not register — always verify, click again if needed
6. **MCP crashes during lag spikes are expected** — when this happens:
   - Check `/home/abzu/Video Media/` and `/tmp/playwright-*` for completed files
   - Resume from the next incomplete episode
   - Do not re-download episodes that completed before the crash
7. **Don't modify** `playwright-adblock.js` or `.mcp.json` — they are tuned and working
8. **Dub is default** — only use sub when explicitly requested via `--audio sub`
9. **One episode at a time** — do not attempt parallel downloads
10. **Close megaup tab after each download** — leaving them open accumulates memory and causes MCP instability
