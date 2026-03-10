# Skills Reference

Complete inventory of available skills (slash commands). All skills live under `.claude/skills/`.

| # | Skill | Command | Location | Purpose |
|---|-------|---------|----------|---------|
| 1 | Bug Triage | `/bug-triage` | `.claude/skills/bug-triage/` | Diagnose and triage reported bugs |
| 2 | Weekly Review | `/weekly-review` | `.claude/skills/weekly-review/` | Weekly system review: stale items, progress summary, state updates |
| 3 | Project Kickoff | `/project-kickoff` | `.claude/skills/project-kickoff/` | Initialize a new product under `products/` |
| 4 | Coherence | `/coherence` | `.claude/skills/coherence/` | Invoke Coherence perspective (harmonic observer) |
| 5 | Polish Document | `/polish` | `.claude/skills/polish-document/` | Convert markdown to polished DOCX/PDF |
| 6 | Write Content | `/write` | `.claude/skills/write-content/` | Write original long-form content via Content Workflow |
| 7 | Add Agent | `/add-agent` | `.claude/skills/add-agent/` | Create new agent with file, symlink, registry, and doc updates |
| 8 | Setup | `/setup` | `.claude/skills/setup/` | Interactive onboarding wizard (11 phases) |
| 9 | Daily Scan | `/daily-scan` | `.claude/skills/daily-scan/` | Scan active state for stale/overdue items, produce daily digest |
| 10 | News Briefing | `/news-briefing` | `.claude/skills/news-briefing/` | Daily intelligence briefing covering AI, tech, and monitored topics |
| 11 | Deep Research | `/deep-research` | `.claude/skills/deep-research/` | Tiered MECE-structured research (web, local, or hybrid) |
| 12 | Improvement Audit | `/improvement-audit` | `.claude/skills/improvement-audit/` | Deep system audit with rotating daily focus |
| 13 | Update | `/update` | `.claude/skills/update/` | Pull framework updates from upstream public repo |
| 14 | Publish | `/publish` | `.claude/skills/publish/` | Sync framework changes to public repo (maintainer only) |

## Skill Structure

Each skill directory contains:
- A prompt `.md` file defining the skill's behavior
- Optional supporting files (e.g., Coherence has 4 source files)

## Adding a New Skill

1. Create directory under `.claude/skills/<skill-name>/`
2. Add prompt file defining behavior
3. Register in `.claude/settings.json` (if needed for hooks/triggers)
4. Update this reference
5. Update `core/indexes/project-map.md` skills listing

## Automated Skills

Skills can be run via cron. See `/setup` Phase 7 for the full automation menu.

Common automated skills:
- `/daily-scan` — daily morning digest
- `/weekly-review` — weekly retrospective
- `/improvement-audit` — daily rotating deep audit
- `/news-briefing` — daily intelligence briefing
