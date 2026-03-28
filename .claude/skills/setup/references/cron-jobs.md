# Cron Jobs

> Referenced by: `.claude/skills/setup/SKILL.md` — Phase 7

---

**Step 1 — Show the caveat (prominent, before anything else):**

> **Important:** These are **system-level cron jobs** (installed via `crontab`), NOT Claude Code in-session crons. They persist across reboots and sessions — you don't need Claude Code open for them to fire. However, they only run when your computer is powered on and your user session is active. If your laptop is closed or sleeping, scheduled jobs will be skipped — they don't queue up and run later. For critical automations, make sure your machine is awake during the scheduled times. All automations log to `/tmp/mega-os-*.log` so you can check what ran.

**Step 2 — Present the automation menu**, grouped by frequency:

**Daily:**
| # | Name | Time | Description |
|---|------|------|-------------|
| 1 | Daily improvement audit | 7:30 AM | Deep MECE-decomposed system audit with rotating focus: Mon=Governance, Tue=Knowledge, Wed=Technical, Thu=Products, Fri=Business, Sat=Evolution, Sun=Integration. Writes to `active/improvement-audit.md`. |
| 2 | Content generation | 7:03 AM | Generates marketing content per channel schedule |
| 3 | Channel tracker update | 7:27 AM | Updates content pipeline status after generation |
| 4 | PyPI/GitHub metrics | 8:33 AM | Fetches download stats and stars for your published packages |
| 5 | News briefing | 8:45 AM | AI/tech intelligence briefing with optional Telegram delivery |
| 6 | Daily system scan | 9:10 AM | Scans all active state for stale/overdue items, produces `active/daily-digest.md` |
| 7 | Freshstate scan | 9:17 AM | Checks document freshness, alerts on stale docs via Telegram |
| 8 | Tabular JSON rebuild | 9:23 AM | Rebuilds `contacts.json` + `pipeline.json` from markdown sources (zero cost) |
| 9 | Cross-reference index | 9:24 AM | Rebuilds entity mention index across all files (zero cost) |

**Weekly:**
| # | Name | Schedule | Description |
|---|------|----------|-------------|
| 10 | Content pipeline status | Mon 8:03 AM | Weekly content pipeline check with Telegram summary |
| 11 | Risk staleness alert | Wed 9:07 AM | Flags risks unmaintained >14 days |
| 12 | Weekly review | Sun 10:13 AM | Comprehensive system review + state updates |
| 13 | Revenue check-in | Sun 10:27 AM | Reviews revenue tracker, sends Telegram status |
| 14 | Index maintenance | Sun 10:47 AM | Verifies core/indexes/ consistency with filesystem |

**Monthly:**
| # | Name | Schedule | Description |
|---|------|----------|-------------|
| 15 | System evaluation | 1st & 15th, 11:03 AM | Evaluator assessment of system health |
| 16 | Competitor monitoring | 1st of month, 9:03 AM | Scans for news about competitors |

**Step 3 — Ask the user to pick:**
- Numbers (e.g., "1, 6, 10")
- `all` — install everything
- `recommended` — starter set: **Daily system scan (#6) + Weekly review (#10) + Freshstate scan (#7)**
- `none` — skip this phase

**Step 4 — For each selected automation:**

1. Detect `claude` binary path via `which claude || echo "$HOME/.local/bin/claude"`
2. Detect mega-os repo path from `pwd`
3. Append each cron entry using safe append: `(crontab -l 2>/dev/null; echo "<entry>") | crontab -`
4. Each entry follows the pattern:
   ```
   <schedule> cd <repo-path> && <claude-path> -p "<prompt>" --permission-mode auto > /tmp/mega-os-<name>.log 2>&1
   ```

The exact cron entries per selection:

```bash
# 1. Daily improvement audit (7:30 AM) — requires /improvement-audit skill (create with /add-skill if not present)
30 7 * * * cd <repo> && <claude> -p "/improvement-audit" --permission-mode auto > /tmp/mega-os-improvement-audit.log 2>&1

# 2. Content generation (7:03 AM)
3 7 * * * cd <repo> && <claude> -p "Generate today's marketing content per business/marketing/channel-schedule.md" --permission-mode auto >> /tmp/mega-os-content-gen.log 2>&1

# 3. Channel tracker update (7:27 AM)
27 7 * * * cd <repo> && <claude> -p "Read /tmp/mega-os-content-gen.log to see what content was generated today. Update business/marketing/channel-tracker.md with new draft entries, marking their pipeline status as 'drafted' and noting the draft location in drafts/social/." --permission-mode auto > /tmp/mega-os-channel-tracker.log 2>&1

# 4. PyPI/GitHub metrics (8:33 AM)
# Replace <pypi-package> and <github-user/repo> with your published package details
33 8 * * * cd <repo> && <claude> -p "Fetch PyPI download stats for <pypi-package> (use web search or pypistats.org API). Fetch GitHub stars for <github-user/repo> (use GitHub API). Append today's numbers to business/marketing/adoption-metrics.md (create if doesn't exist). If downloads exceed 500 or stars exceed 50, send a milestone alert via Telegram." --permission-mode auto > /tmp/mega-os-metrics.log 2>&1

# 5. News briefing (8:45 AM)
45 8 * * * cd <repo> && <claude> -p "/news-briefing --telegram" --permission-mode auto > /tmp/mega-os-news-briefing.log 2>&1; echo "Exit: $? at $(date)" >> /tmp/mega-os-news-briefing.log

# 6. Daily system scan (9:10 AM)
10 9 * * * cd <repo> && <claude> -p "/daily-scan" --permission-mode auto > /tmp/mega-os-daily-scan.log 2>&1

# 7. Freshstate scan (9:17 AM)
17 9 * * * cd <repo> && <claude> -p "Run freshstate check on this repo. Execute: freshstate check. Save the output to active/freshstate-report.md (replace contents with timestamped report). If any files are stale or cross-references broken, send a summary via Telegram using the bridge at engineering/scripts/telegram-bridge/." --permission-mode auto > /tmp/mega-os-freshstate.log 2>&1

# 8. Content pipeline status (Mon 8:03 AM)
3 8 * * 1 cd <repo> && <claude> -p "Check business/marketing/content-calendar.md for this week's planned article. Check if a draft exists in drafts/. Check business/marketing/channel-tracker.md for overdue content. Send a Telegram summary of content pipeline status: what's due, what's drafted, what's overdue." --permission-mode auto > /tmp/mega-os-content-pipeline.log 2>&1

# 9. Risk staleness alert (Wed 9:07 AM)
7 9 * * 3 cd <repo> && <claude> -p "Check active/risks.md. For each active risk, check if the 'Date Added' is more than 14 days ago and the mitigation status hasn't been updated. Flag stale risks. Send a Telegram alert listing any risks that need mitigation review." --permission-mode auto > /tmp/mega-os-risk-alert.log 2>&1

# 10. Weekly review (Sun 10:13 AM)
13 10 * * 0 cd <repo> && <claude> -p "/weekly-review" --permission-mode auto > /tmp/mega-os-weekly-review.log 2>&1

# 11. Revenue check-in (Sun 10:27 AM)
27 10 * * 0 cd <repo> && <claude> -p "Review business/finance/revenue-tracker.md. Check which streams still show \$0. Check if 30-day or 60-day review dates are approaching. Update the 'Last Checked' date. Send a Telegram summary of revenue status and any action items due this week." --permission-mode auto > /tmp/mega-os-revenue-checkin.log 2>&1

# 12. Index maintenance (Sun 10:47 AM)
47 10 * * 0 cd <repo> && <claude> -p "Verify core/indexes/canonical-files.md, core/indexes/project-map.md, and core/indexes/active-context-map.md are consistent with the actual filesystem. Check for files listed in indexes that don't exist, and important files that exist but aren't indexed. Report any drift found. Update indexes if discrepancies are minor (< 5 items). Flag larger issues for manual review." --permission-mode auto > /tmp/mega-os-index-maintenance.log 2>&1

# 13. System evaluation (1st & 15th, 11:03 AM)
3 11 1,15 * * cd <repo> && <claude> -p "Run a system evaluation as the Evaluator agent. Assess: agent utilization (which agents were used this period), workflow completion rates, document freshness (reference active/freshness-log.md), improvement proposal outcomes (reference active/improvements.md), and revenue progress (reference business/finance/revenue-tracker.md). Write findings to active/coherence-metrics.md. Identify top 3 areas for improvement." --permission-mode auto > /tmp/mega-os-evaluation.log 2>&1

# 14. Competitor monitoring (1st of month, 9:03 AM)
3 9 1 * * cd <repo> && <claude> -p "Search for recent news and announcements about competitors in your domain. Check for new funding rounds, product launches, or feature releases. Update business/strategy/ with any significant findings. Send a Telegram summary." --permission-mode auto > /tmp/mega-os-competitor-monitor.log 2>&1
```

Where `<repo>` and `<claude>` are detected at runtime during setup.

**Step 5 — Confirm:** Print installed jobs via `crontab -l | grep mega-os`

**Step 6 — Show tips:**
- "Check logs anytime: `cat /tmp/mega-os-daily-scan.log`"
- "List your cron jobs: `crontab -l`"
- "Remove a job: `crontab -e` and delete the line"
- "The daily improvement audit runs a different deep scan each day — check `active/improvement-audit.md` for findings"
