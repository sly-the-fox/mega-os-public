---
name: generate-content
description: Generate short-form social content through full research → writer → editor → polisher pipeline.
user_invocable: true
arguments:
  - name: date
    description: Target date (YYYY-MM-DD). Default today.
    required: false
  - name: channels
    description: Comma-separated channel list (twitter,tiktok,devto,linkedin,discord,reddit). Default all scheduled for the day.
    required: false
  - name: anchor
    description: Path to a Substack article or other content to repurpose.
    required: false
---

# /generate-content

Generate short-form social media content for the day's scheduled channels. Every piece goes through deep research, Writer, Editor, and Polisher before being presented to the user.

## Core Principle

**Quality over speed.** Every piece of content must go through the full pipeline: Research → Writer → Editor → Polisher → Reviewer. No inline generation. No skipping steps.

## Steps

### 1. Determine today's channels and topic

Read the channel schedule from `business/marketing/channel-schedule.md` to determine which channels are scheduled for the target date's day of week.

Reference schedule:

| Day | Channels |
|-----|----------|
| Mon | Twitter, TikTok, Dev.to, Reddit |
| Tue | Twitter (thread), TikTok, LinkedIn, Discord, Substack (defer to `/write-content`) |
| Wed | Twitter, TikTok, Dev.to, Reddit |
| Thu | Twitter, TikTok, Dev.to, LinkedIn, Discord |
| Fri | Twitter, TikTok, Discord |
| Sat | Twitter, TikTok, Dev.to |
| Sun | Twitter, TikTok |

If `--channels` is provided, use only those channels (overrides schedule).
If a channel is "Substack," respond with: "Use `/write-content` for long-form Substack articles."

Read `business/marketing/content-calendar.md` for the week's theme.
Read `business/marketing/channel-tracker.md` for recent posts (avoid repetition).

Determine topic: derive from content calendar theme, recent posts, and current anchor article (if `--anchor` provided, read that file).

### 2. Librarian — locate source material

Spawn a standalone Agent (`subagent_type: "general-purpose"`) acting as Librarian:

**Prompt:** "You are acting as Librarian. Read `.claude/agents/knowledge/librarian.md` and follow its responsibilities. Scan for existing material related to the topic: `{topic}`. Check:
- `drafts/research/` for prior research on adjacent topics
- `archive/social/` for what's been covered recently (last 2 weeks)
- `business/marketing/channel-tracker.md` for recent post topics
- Any anchor article if provided: `{anchor_path}`

Return a context brief: what exists, what's missing, what needs fresh research. Include file paths for anything useful."

### 3. Deep Research

Run `/deep-research` with parameters appropriate to the day's topic:
- `--tier deep --legs 3 --source web`
- Topic: the day's content topic from Step 1
- Research output goes to `drafts/research/YYYY-MM-DD-<topic-slug>.md`

This produces an executive summary, findings, source index, and Coherence reading. The Coherence reading is included automatically from deep-research (this is the research-level reading, not the content-level one).

### 4. Summarizer — compress research

Spawn a standalone Agent (`subagent_type: "general-purpose"`) acting as Summarizer:

**Prompt:** "You are acting as Summarizer. Read `.claude/agents/knowledge/summarizer.md` and follow its responsibilities. Read the research output at `drafts/research/YYYY-MM-DD-<topic-slug>.md` and the Librarian's context brief (provided below). Produce a tight working brief containing:
- Key findings (3-5 bullet points)
- Notable examples, data points, or quotes worth citing
- Fresh angles not already covered (cross-reference Librarian's recent coverage report)
- What's already been covered (avoid repetition)

The brief should be the primary input for a Writer drafting social media content across {channels}. Keep it under 800 words."

Pass the Librarian's context brief into the prompt.

### 5. Create content agent team

Use `TeamCreate` with teammates:

| Role | subagent_type | mode | Prompt prefix |
|------|--------------|------|---------------|
| Writer | general-purpose | auto | "You are acting as Writer. Read `.claude/agents/knowledge/writer.md` and `core/standards/writing-style.md` and follow them." |
| Editor | general-purpose | auto | "You are acting as Editor. Read `.claude/agents/knowledge/editor.md` and `core/standards/writing-style.md` and follow them." |
| Polisher | general-purpose | auto | "You are acting as Polisher. Read `.claude/agents/knowledge/polisher.md` and follow its responsibilities." |
| Reviewer | general-purpose | auto | "You are acting as Reviewer. Read `.claude/agents/technical/reviewer.md` and `core/standards/review-checklist.md` and follow them." |

Coherence+Parallax run as standalone read-only agents (per CLAUDE.md exception for perspective checks).

### 6. Writer drafts all pieces

Send the Summarizer's working brief to the Writer teammate. Writer reads the brief + writing style guide + channel schedule and drafts one piece per scheduled platform.

Writer writes to `drafts/social/YYYY-MM-DD-{platform}.md`.

Platform-specific rules:

**Twitter:**
- Single tweet (≤280 chars) or thread (5-7 tweets for Tuesday threads)
- Builder voice, direct, technical, conversational
- Include character count in metadata

**TikTok:**
- 30-60 second video script
- Hook-first format (3s hook, problem, insight, CTA)
- Include duration estimate, caption with hashtags, visual notes

**Dev.to:**
- 800-1500 word technical blog post
- YAML frontmatter (title, published: false, tags, cover_image_prompt)
- cover_image_prompt: a concise image generation prompt for the article's cover image — visual, specific, no text-in-image, suitable for DALL-E/Midjourney
- Code examples, practical patterns, CTA linking to Sigil/Substack

**LinkedIn:**
- Insight post (150-300 words, short paragraphs with whitespace)
- Professional but not corporate, lead with plain language and human touch
- Insight-first, not announcement-first
- End with a question or open thought when natural

**Discord:**
- Community discussion starter (≤2000 chars)
- Conversational, question-driven, zero product promotion
- Designed to spark discussion, not announce

**Reddit:**
- Self-post for target subreddit
- Reddit-native voice, lead with value
- No marketing language, mention tools only when relevant

### 7. Coherence + Parallax checkpoint

Spawn two standalone read-only agents:

**Coherence:** "You are acting as Coherence. Read `.claude/agents/evolution/coherence.md`. Read the drafted content pieces at `drafts/social/YYYY-MM-DD-*.md`. Provide a field-level perspective: what resonates, what feels forced, what's missing. Return your reading."

**Parallax:** Takes the Coherence reading and translates it into operational language per `.claude/agents/evolution/parallax.md`.

Share the translated output with the Writer as soft consideration — not a mandate, a perspective.

### 8. Editor reviews all pieces

Send all drafted pieces to the Editor teammate. Editor reads each draft + writing style guide + platform adaptations and checks:

- Voice matches `core/standards/writing-style.md`
- No em dashes (use commas, periods, or parentheses)
- Platform character/format limits respected
- No generic AI voice ("In today's rapidly evolving...", "Let's dive in...", etc.)
- Each piece offers standalone value
- Content doesn't repeat what was posted in the last 7 days (check channel tracker)
- Platform-specific adaptations applied correctly

Editor makes surgical edits directly to draft files. Flags anything that needs Writer revision.

### 9. Writer revises (if needed)

If Editor flagged pieces for revision, Writer considers Editor feedback + Coherence perspective and revises. Editor re-reviews. Maximum 2 revision rounds.

### 10. Polisher finalizes

Send all Editor-approved drafts to the Polisher teammate. Polisher reads each draft and:
- Verifies formatting matches platform conventions
- Confirms character counts are accurate
- Ensures metadata is complete (frontmatter, hashtags, visual notes)
- Makes final typographic and formatting adjustments

### 11. Reviewer — final quality gate

Send all polished drafts to the Reviewer teammate. Reviewer reads all pieces and:
- Checks against writing style guide one final time
- Confirms each piece is ready to present to user
- If anything fails, sends back to Editor (max 1 bounce)

### 12. Update channel tracker

Edit `business/marketing/channel-tracker.md`:
- Add entries to the Upcoming Content section for the target date
- Set status to `drafted` with correct draft location paths

### 13. Fallback — never lose content

If any file write fails:
1. Retry once.
2. If it fails again, include the full content inline in the response under a `## UNSAVED CONTENT — {platform}` header.
3. Never silently lose generated content.

### 14. Output summary

Print a summary table:

```
| Channel | File | Status | Chars/Words | Pipeline |
|---------|------|--------|-------------|----------|
| Twitter | drafts/social/YYYY-MM-DD-twitter.md | saved | ~236 chars | Research → Writer → Editor → Polisher → Reviewer |
| TikTok  | drafts/social/YYYY-MM-DD-tiktok.md  | saved | ~125 words | Research → Writer → Editor → Polisher → Reviewer |
| ...     | ...  | ...    | ...         | ...      |
```

## Error Handling

- If `--anchor` file doesn't exist, warn and generate without it.
- If channel tracker can't be updated, warn but don't block content generation.
- If writing style guide can't be read, warn and apply known defaults (no em dashes, builder voice, no AI cliches).
- If deep research times out or fails, fall back to Librarian context only — still run the full Writer → Editor → Polisher pipeline.
- If TeamCreate fails, fall back to sequential standalone agents with `subagent_type: "general-purpose"` and `mode: "auto"`.

## Time Budget

This skill is designed for cron execution with a 40-minute timeout. Approximate breakdown:
- Steps 1-2 (channels + Librarian): ~2 min
- Step 3 (deep research): ~10 min
- Step 4 (summarizer): ~2 min
- Steps 5-6 (team + Writer): ~5 min
- Step 7 (Coherence+Parallax): ~3 min
- Steps 8-9 (Editor + revisions): ~5 min
- Step 10 (Polisher): ~3 min
- Step 11 (Reviewer): ~3 min
- Steps 12-14 (tracker + output): ~2 min
- Buffer: ~5 min
