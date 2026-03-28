# Search Topics & Source Lanes

> Referenced by: `.claude/skills/news-briefing/SKILL.md` — Phase 1

Customize the topics and queries below to match your interests. Each topic should have queries spanning at least 2 of the 3 source lanes.

## Source Lane Diversification

Each topic's queries must span at least 2 of 3 source lanes:

| Lane | Purpose | Examples |
|------|---------|---------|
| **Breaking/News** | Mainstream coverage, first reports | Default queries (no suffix needed) |
| **Domain-Specific** | Expert/specialist sources | `site:arxiv.org`, `site:substack.com`, industry blogs, specialized outlets |
| **Community/Social** | Practitioner reactions, ground truth | `site:reddit.com`, `site:news.ycombinator.com`, Discord, forums |

## Topic Query Table

Replace these example topics with your own areas of interest:

| Topic | Queries |
|-------|---------|
| **Technology & AI** | `AI breakthrough OR announcement <year>`, `OpenAI OR "Google DeepMind" OR "Meta AI" announcement`, `AI regulation policy`, `AI agent OR MCP OR tool use site:reddit.com OR site:news.ycombinator.com` |
| **Science & Research** | `scientific breakthrough discovery <year>`, `research study published nature OR science`, `climate change research new findings`, `science breakthrough site:arxiv.org OR site:biorxiv.org` |
| **Business & Economy** | `startup funding OR acquisition <year>`, `market trend economic indicator`, `tech industry layoffs OR hiring`, `business strategy site:hbr.org OR site:stratechery.com` |
| **Politics & Policy** | `policy announcement government <year>`, `regulation technology OR privacy`, `geopolitics international relations`, `policy analysis site:foreignaffairs.com OR site:lawfaremedia.org` |
| **Culture & Society** | `social trend cultural shift <year>`, `education technology research`, `mental health study findings`, `culture OR society site:theatlantic.com OR site:aeon.co` |

## Coverage Validation

After search and dedup filtering, check each topic:
- If a topic returns **< 2 results**, run 1-2 **fallback queries** with broader terms or alternative source lanes.
- If a topic returns **0 results** after fallback, explicitly note "No significant developments" with validated confidence.
