---
name: metrics-scan
description: "Use when running the daily metrics scan — fetches PyPI downloads, GitHub stats, website availability, Dev.to, and GitHub Sponsors. Appends to adoption-metrics.md and optionally sends a notification."
invocation: /metrics-scan
user_invocable: true
arguments: "--notify (send notification), --products-only (skip channel metrics), --channels-only (skip product metrics)"
---

# Metrics Scan

Run the automated metrics collection script.

## What It Does

Invokes `engineering/scripts/fetch-metrics.py` which:

1. **PyPI downloads** — your packages (via pypistats.org API)
2. **GitHub repos** — stars, forks, open issues, watchers (via GitHub API)
3. **GitHub traffic** — 14-day clone and view counts (via `gh api`, requires push access)
4. **GitHub Sponsors** — sponsor count (via `gh api graphql`)
5. **Website availability** — HEAD requests to your configured sites
6. **Dev.to** — total views, reactions, comments (via Dev.to API)
7. **Auto-discovery** — detects new public repos under the configured GitHub user

Results are appended to `business/marketing/adoption-metrics.md`.

## Steps

### 1. Run the Script

```bash
python engineering/scripts/fetch-metrics.py $ARGS
```

Where `$ARGS` are any arguments passed to this skill (e.g., `--notify`).

### 2. Report Results

Print a summary of what was fetched and any milestones detected.

## Adding New Sources

Edit `engineering/scripts/fetch-metrics.py`:
- Add new packages to `PACKAGES` list
- Add new GitHub repos to `GITHUB_REPOS` list
- Add new websites to `WEBSITES` list
- Add new sections to `adoption-metrics.md` with the standard table format

## Cron

Can be run daily via cron (Python script invocation, zero Claude API cost). The `/metrics-scan` skill exists for manual invocation during sessions.

## Output

- `business/marketing/adoption-metrics.md` — metrics appended
- Console summary — printed to stdout
- Notification — if `--notify` flag is passed (configure webhook in script)
