---
name: metrics-scan
description: "Run the daily metrics scan — fetches PyPI downloads, GitHub stats, website availability, Dev.to, and GitHub Sponsors. Appends to adoption-metrics.md and optionally sends Telegram notification."
invocation: /metrics-scan
user_invocable: true
arguments: "--telegram (send Telegram notification), --products-only (skip channel metrics), --channels-only (skip product metrics)"
---

# Metrics Scan

Run the automated metrics collection script.

## What It Does

Invokes `engineering/scripts/fetch-metrics.py` which:

1. **PyPI downloads** — sigil-notary, freshstate (via pypistats.org API)
2. **GitHub repos** — stars, forks, open issues, watchers for sigil, freshstate, mega-os-public (via GitHub API)
3. **GitHub traffic** — 14-day clone and view counts (via `gh api`, requires push access)
4. **GitHub Sponsors** — sponsor count (via `gh api graphql`)
5. **Website availability** — HEAD requests to sigil-notary.dev, aequilibris.consulting, and all `.pages.dev` demo sites
6. **Dev.to** — total views, reactions, comments (via Dev.to API)
7. **Auto-discovery** — detects new public repos under the configured GitHub user

Results are appended to `business/marketing/adoption-metrics.md`.

## Steps

### 1. Run the Script

```bash
cd /home/abzu/mega-os && python engineering/scripts/fetch-metrics.py $ARGS
```

Where `$ARGS` are any arguments passed to this skill (e.g., `--telegram`).

### 2. Report Results

Print a summary of what was fetched and any milestones detected.

## Adding New Sources

Edit `engineering/scripts/fetch-metrics.py`:
- Add new packages to `PACKAGES` list
- Add new GitHub repos to `GITHUB_REPOS` list
- Add new websites to `WEBSITES` list
- Add new sections to `adoption-metrics.md` with the standard table format

## Cron

Runs daily at 8:33 AM via cron (Python script invocation, zero Claude API cost). The `/metrics-scan` skill exists for manual invocation during sessions.

## Output

- `business/marketing/adoption-metrics.md` — metrics appended
- Console summary — printed to stdout
- Telegram notification — if `--telegram` flag is passed
