# Mega-OS Project Map

Last updated: 2026-03-28

```
mega-os/
├── .claude/
│   ├── agents/                         — 39 agent definitions
│   │   ├── governance/                 — overseer, governor, router, planner, pm, operator, sentinel, auditor, custodian
│   │   ├── knowledge/                  — historian, librarian, summarizer, documenter, editor, polisher, writer
│   │   ├── technical/                  — architect, engineer, executor, reviewer, qa, debugger, devops, security-expert, designer, visual-designer, api-designer
│   │   ├── business/                   — strategist, marketer, seller, financier, proposal-writer, client-manager, content-strategist, growth-hacker
│   │   ├── evolution/                  — improver, evaluator, coherence, parallax
│   │   ├── shared/                     — system-rules, workflows, collaboration-protocol, definitions, escalation-rules, handoff-template, output-template
│   │   ├── REGISTRY.md                 — canonical agent directory
│   │   └── *.md symlinks               — flat discovery (39 symlinks → category subdirs)
│   ├── hooks/                          — session lifecycle hooks (SessionStart, Stop)
│   ├── skills/                         — 24 slash commands
│   │   ├── setup/                      — onboarding wizard (11 phases)
│   │   │   └── references/             — phase reference docs (workspace, standards, products, agents, crons)
│   │   ├── goodmorning/                — morning briefing
│   │   │   └── references/             — lane definitions, output template
│   │   ├── daily-scan/                 — stale/overdue item scan
│   │   ├── weekly-review/              — end-of-week retrospective
│   │   ├── news-briefing/              — intelligence briefing
│   │   ├── dream/                      — reflective prompt
│   │   ├── project-kickoff/            — product scaffolding
│   │   ├── write-content/              — full content pipeline (Writer → Editor → Polisher)
│   │   ├── build-site/                 — website from concept to deployment
│   │   ├── bug-triage/                 — bug diagnosis
│   │   ├── deep-research/              — MECE-structured research
│   │   ├── generate-content/           — short-form social content
│   │   ├── draw/                       — visual generation
│   │   ├── add-agent/                  — create new agent
│   │   ├── add-skill/                  — create new skill
│   │   ├── evolution-loop/             — Evaluator + Improver feedback cycle
│   │   ├── coherence/                  — harmonic awareness, Inner Geometry Method
│   │   ├── workflow-review/            — workflow pattern analysis
│   │   ├── outreach/                   — LinkedIn outreach management
│   │   ├── polish-document/            — markdown to DOCX/PDF
│   │   ├── reddit-comments/            — Reddit comment generation
│   │   ├── ui-review/                  — frontend visual audit
│   │   ├── update/                     — pull upstream framework updates
│   │   └── publish/                    — sync to public repo
│   ├── settings.json                   — permissions and env config
│   └── CLAUDE.local.example.md         — customization template
├── active/                             — current operational state (merge=ours protected)
│   ├── now.md                          — current focus and task board
│   ├── priorities.md                   — priority queue
│   ├── inbox.md                        — incoming items
│   ├── blockers.md                     — active blockers
│   ├── risks.md                        — risk register
│   ├── improvements.md                 — improvement proposals
│   ├── audits.md                       — audit findings
│   ├── index.json                      — manifest with load priorities
│   ├── daily-digest.md                 — daily scan output
│   ├── dream-report.md                 — dream output
│   ├── news-briefing.md                — briefing output
│   ├── news-briefing-state.md          — briefing dedup state
│   ├── historian-digest.md             — recent activity digest
│   ├── improvement-audit.md            — audit output (rotating focus)
│   ├── workflow-review.md              — workflow review output
│   ├── system-evaluation.md            — system evaluation output
│   ├── cron-health.md                  — cron health output
│   ├── coherence-metrics.md            — coherence tracking
│   ├── freshness-log.md                — freshness log
│   └── freshstate-report.md            — freshstate output
├── core/
│   ├── standards/                      — naming, documentation, coding, review, writing style, deployment, secrets
│   ├── templates/                      — decision, spec, SOP, handoff, plan templates
│   ├── indexes/                        — project map, canonical files, context map
│   └── history/                        — current state, decisions, timeline
│       ├── handoffs/                   — handoff records
│       └── weekly-summaries/           — weekly summaries
├── products/                           — product directories (merge=ours protected)
├── business/                           — business operations (merge=ours protected)
│   ├── clients/
│   ├── finance/                        — revenue tracker
│   ├── marketing/
│   ├── operating/                      — recurring processes
│   ├── sales/
│   └── strategy/
├── engineering/
│   ├── automations/
│   ├── infra/
│   ├── scripts/                        — sync, archive, cron, build, telegram-bridge
│   ├── shared-libraries/
│   └── troubleshooting/
├── archive/                            — aged content (merge=ours protected)
│   ├── news/                           — archived briefings
│   └── reports/                        — archived reports
├── drafts/                             — work in progress (merge=ours protected)
├── deliverables/                       — polished output (merge=ours protected)
├── style-samples/                      — writing style samples (merge=ours protected)
├── CLAUDE.md                           — master system instructions
├── AGENTS.md                           — agent philosophy and usage
├── GETTING_STARTED.md                  — new user guide
├── README.md                           — overview
├── VERSION                             — framework version
├── .freshstate.yml                     — freshstate config
└── .gitignore                          — git exclusions
```
