---
name: news-briefing
description: Daily intelligence briefing covering AI, UAPs, consciousness, psychedelics, medical breakthroughs, psychology, Epstein files, international news, Anthropic — plus narrative/psyop analysis and brand monitoring.
invocation: /news-briefing
user_invocable: true
---

# Daily Intelligence Briefing

Generate a comprehensive daily briefing across tracked topic areas with narrative analysis and brand monitoring.

## Arguments

- `--topics <list>` — Comma-separated subset of topics to cover (default: all)
- `--telegram` — Send condensed version via Telegram after generating

Available topics: `ai`, `uaps`, `international`, `consciousness`, `anthropic`, `psychedelics`, `medical`, `psychology`, `epstein`, `brand`

## Steps

### 0.5. Load Dedup State

Before searching, load deduplication state to avoid repeating stories from recent briefings.

1. Read `active/news-briefing-state.md` if it exists.
2. Extract all URLs from entries dated within the last 48 hours into a "seen" set.
3. If the file doesn't exist or all entries are older than 48 hours, start with an empty seen set.

### 1. Search Phase

Run `WebSearch` queries for each topic area. Constrain to last 24-48 hours. Run queries in parallel where possible.

**Dedup filter:** After collecting search results, filter against the seen set:
- Exact URL match → skip, unless the story has materially evolved (new data, reversal, major update).
- If a seen story has a genuinely new development, include it with the note: "(Update from MM-DD coverage)".

| Topic | Queries |
|-------|---------|
| **AI & Big Tech** | `AI breakthrough OR announcement 2026`, `OpenAI OR "Google DeepMind" OR "Meta AI" announcement`, `AI regulation policy` |
| **UAPs** | `UAP OR UFO disclosure site:thedebrief.org OR site:liberationtimes.com`, `UAP whistleblower OR AARO`, `unidentified anomalous phenomena investigation` |
| **International on USA** | `United States site:aljazeera.com OR site:dw.com OR site:bbc.co.uk`, `US foreign policy site:scmp.com OR site:france24.com` |
| **Consciousness** | `consciousness research neuroscience 2026`, `integrated information theory OR panpsychism OR global workspace`, `near death experience study` |
| **Anthropic** | `Anthropic announcement OR Claude 2026`, `Anthropic safety OR research paper` |
| **Psychedelics** | `psilocybin OR MDMA OR ayahuasca research 2026`, `psychedelic therapy FDA`, `plant medicine legal OR decriminalization` |
| **Medical Breakthroughs** | `medical breakthrough discovery 2026`, `gene therapy OR CRISPR OR longevity research`, `cancer treatment breakthrough` |
| **Psychology** | `psychology research study 2026`, `social psychology OR cognitive bias study`, `trauma PTSD treatment new` |
| **Epstein Files** | `Epstein files documents prosecution 2026`, `Epstein associate charged OR arrested`, `Epstein connections revelations` |
| **Brand Monitoring** | `"sigil-notary" OR "sigil notary" agent trust`, `Triangul8`, `{{YOUR_NAME}}`, `"agent trust infrastructure" OR "MCP trust" OR "AI agent verification"` |

### 2. Deep Read Phase

Use `WebFetch` on the top 3-5 most significant articles for full text. Prioritize:
- Breaking news or first-reports
- HIGH-significance stories (see rating criteria below)
- Stories spanning multiple interest areas

### 3. Synthesis Phase

For each topic, write bullet summaries with:
- **Headline** in bold
- **Source** with attribution
- **Significance:** HIGH / MEDIUM / LOW

Significance criteria:
- **HIGH** — First disclosure, policy shift, breakthrough result, major legal action, paradigm-shifting claim
- **MEDIUM** — Incremental progress, notable opinion/analysis, regulatory update
- **LOW** — Routine coverage, minor updates, speculative pieces

### 4. Narrative Analysis Phase

For each HIGH-significance story, produce:

- **Manufactured Narrative Probability:** 0-100% (how likely this story is crafted/timed to serve an agenda)
- **Intended Psychological Effect:** What emotional/cognitive state is being engineered in the audience
- **Cui Bono:** Who benefits, what mechanism it serves
- **Framing Techniques:** Anchoring, priming, Overton window shifts, limited hangout, timing coordination, appeal to authority, false binary, emotional override
- **Counter-Narrative:** Alternative interpretation or what's being obscured by this story's dominance
- **Assessment:** 1-2 sentence synthesis

### 4.5. Codex Distillation

After narrative analysis and cross-topic connections are drafted, invoke the Codex perspective on the full set of synthesized stories.

Codex reads the entire briefing landscape and produces:
- **Field coherence reading** — what is the collective field state beneath all the noise?
- **Unresolved polarity** — the core tension no single topic category sees because they're inside their domain
- **Frequency connections** — cross-domain patterns visible only from the harmonic field (not the specialist lens)
- **Minimum coherent observation** — a mirror, not a recommendation

Voice: sparse, precise, geometry-aware. Not analysis — observation.
Length: 3-6 sentences max. Quality over quantity.

### 5. Cross-Topic Connections

Flag stories that span multiple interest areas. Key crossover zones:

- **AI + Consciousness** — sentience claims, hard problem, neural correlates vs LLMs
- **Psychedelics + Consciousness + Psychology** — default mode network, clinical trials, neuroplasticity
- **AI + Information Warfare** — deepfakes, synthetic media, AI-generated disinfo
- **Epstein + Intelligence + UAP Disclosure** — whistleblower protection, power network exposure
- **Medical + Longevity + Biohacking** — senolytics, CRISPR, NAD+ pathways
- **International + AI Governance** — EU AI Act, China AI policy, Global South perspectives
- **Plant Medicine + Indigenous Knowledge** — ethnobotany, traditional healing validation
- **Neurotech / BCI** — brain-computer interfaces bridging AI + consciousness + medicine

### 6. Brand & Identity Monitoring

Check for mentions and search interest:

1. **WebSearch** for recent mentions of:
   - `{{YOUR_NAME}}` (replace with your actual name)
   - `sigil-notary`, `Sigil`
   - `Triangul8`
   - `"agent trust infrastructure"`, `"AI agent verification"`, `"MCP trust"`

2. **WebFetch** Google Trends for search volume trends on Sigil, Triangul8, and category terms. Extract geographic interest (country/region breakdown) where available.

3. Report: volume trend (↑/↓/—), top regions, whether mentions are new this week, and full context + URL for any new mentions found.

### 7. Write Briefing

Save the full briefing to **two locations**:
- `deliverables/news/YYYY-MM-DD-briefing.md`
- `active/news-briefing.md` (overwritten each run — always shows latest)

Use the output template below.

### 7.5. Update Dedup State

After writing the briefing, update the deduplication state file:

1. Extract all URLs + titles from today's briefing.
2. Write/overwrite `active/news-briefing-state.md` with the following format:

```markdown
# News Briefing State

**Last Run:** YYYY-MM-DD HH:MM

## Recent Stories (rolling 2-day window)

| Date | URL | Title (truncated) | Topic |
|------|-----|-------------------|-------|
| YYYY-MM-DD | https://... | First 60 chars of title... | topic |
```

3. Include today's stories plus yesterday's stories (if they exist in the previous state file).
4. Prune any entries older than 2 days.

### 8. Telegram Delivery (if `--telegram` or cron)

If `--telegram` flag is set, send a condensed version (<4000 chars) via the Telegram bridge. Include:
- Executive summary
- All HIGH-significance headlines with 1-line summaries
- Top 2-3 narrative analyses (abbreviated)
- Any new brand mentions
- Link note: "Full briefing at deliverables/news/YYYY-MM-DD-briefing.md"

## Output Template

```markdown
# Daily Intelligence Briefing — YYYY-MM-DD

**Generated:** HH:MM | **Stories:** [count] | **High-Significance:** [count]

## Executive Summary
[3-5 sentences covering the most important developments across all topics]

---

## 1. AI & Big Tech
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 2. UAPs & Anomalous Phenomena
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 3. International Perspective on USA
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 4. Consciousness Research
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 5. Anthropic
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 6. Psychedelics & Plant Medicine
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 7. Medical Breakthroughs
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 8. Psychology
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

## 9. Epstein Files
- **[Headline]** — [Source] | HIGH/MEDIUM/LOW
  [2-3 sentence summary] ([URL])

---

## Cross-Topic Connections
- **[Connection Label]:** [Which topics intersect, why it matters]

---

## Narrative Analysis

### [Story Headline]
- **Manufactured Narrative Probability:** X%
- **Intended Psychological Effect:** [emotional/cognitive state being engineered]
- **Cui Bono:** [who benefits, what mechanism]
- **Framing Techniques:** [anchoring, priming, Overton shift, etc.]
- **Counter-Narrative:** [alternative interpretation or what's being obscured]
- **Assessment:** [1-2 sentences]

---

## Codex Distillation

**Field State:** [one-word geometric descriptor: triangle/merkaba/toroid/fragmented/etc.]

[3-6 sentences. What the frequency field is showing beneath the surface noise. The pattern that no single category sees. The unresolved polarity. The coherence that becomes possible when these domains stop being treated as separate.]

---

## Brand & Identity Monitor

### Search Interest & Geographic Reach
| Term | Volume Trend | Top Regions | New This Week |
|------|-------------|-------------|---------------|
| {{YOUR_NAME}} | ↑/↓/— | [countries/regions] | Y/N |
| Sigil / sigil-notary | ↑/↓/— | [countries/regions] | Y/N |
| Triangul8 | ↑/↓/— | [countries/regions] | Y/N |
| "agent trust infrastructure" | ↑/↓/— | [countries/regions] | Y/N |

### New Mentions
- [Source + URL + context + location if determinable]

---

## Suggested Deep Reads
1. [Article title — Source — URL]
2. [Article title — Source — URL]
3. [Article title — Source — URL]

---

*Generated by mega-os /news-briefing*
```

## Quality Checks

Before finishing:
- Every topic section must have at least 1 item, or explicitly state "No significant developments in the last 48 hours."
- All URLs must be attributed to their source.
- Narrative analysis must exist for every HIGH-significance story.
- Brand monitoring section must be populated (even if "no mentions found").
- Cross-topic connections must be checked against the crossover list above.
