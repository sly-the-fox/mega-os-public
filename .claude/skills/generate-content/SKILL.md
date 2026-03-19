---
name: generate-content
description: Generate short-form social content for scheduled channels. Main context writes all files — no subagent delegation.
user_invocable: true
arguments:
  - name: date
    description: Target date (YYYY-MM-DD). Default today.
    required: false
  - name: channels
    description: Comma-separated channel list (twitter,tiktok,devto,discord,reddit). Default all scheduled for the day.
    required: false
  - name: anchor
    description: Path to a Substack article or other content to repurpose.
    required: false
---

# /generate-content

Generate short-form social media content for the day's scheduled channels. All file writes happen in the main context — never delegate writes to subagents.

## Core Principle

**Main context writes all files.** No subagent file write delegation. This prevents content loss when running headless or via bridges.

## Steps

### 1. Determine today's channels

Read the channel schedule from `business/marketing/channel-schedule.md` to determine which channels are scheduled for the target date's day of week.

Reference schedule:

| Day | Channels |
|-----|----------|
| Mon | Twitter, TikTok, Dev.to, Reddit |
| Tue | Twitter (thread), TikTok, Discord, Substack (defer to `/write-content`) |
| Wed | Twitter, TikTok, Dev.to, Reddit |
| Thu | Twitter, TikTok, Dev.to, Discord |
| Fri | Twitter, TikTok, Discord |
| Sat | Twitter, TikTok, Dev.to |
| Sun | Twitter, TikTok |

If `--channels` is provided, use only those channels (overrides schedule).
If a channel is "Substack," respond with: "Use `/write-content` for long-form Substack articles."

### 2. Gather context

Read these files for voice and context:
- `core/standards/writing-style.md` — voice, tone, style rules
- `business/marketing/channel-tracker.md` — recent posts, what's been covered
- `business/marketing/content-calendar.md` — current theme/anchor article

If `--anchor` is provided, read that file for repurposing.

### 3. Generate content inline

Generate all content pieces directly in the main context. For each channel:

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

**Discord:**
- Community discussion starter (≤2000 chars)
- Conversational, question-driven, zero product promotion
- Designed to spark discussion, not announce

**Reddit:**
- Self-post for target subreddit
- Reddit-native voice, lead with value
- No marketing language, mention tools only when relevant

### 4. Inline editor pass

Before writing files, review each piece for:
- [ ] Voice matches `core/standards/writing-style.md`
- [ ] No em dashes (use commas, periods, or parentheses)
- [ ] Platform character/format limits respected
- [ ] No generic AI voice ("In today's rapidly evolving...", "Let's dive in...", etc.)
- [ ] Each piece offers standalone value
- [ ] Content doesn't repeat what was posted in the last 3 days (check channel tracker)

### 5. Write draft files

Write each piece to `drafts/social/{date}-{platform}.md` using the standard draft format.

Match the template format from existing drafts:
- **Twitter:** Header with type/post time/repurposes, content between `---` dividers, character count + notes
- **TikTok:** Header, Script section with [HOOK], [PROBLEM], [INSIGHT], [CTA] blocks, duration/caption/visual/notes
- **Dev.to:** YAML frontmatter (including cover_image_prompt after tags), article body, footer with Sigil/Substack links

### 6. Fallback — never lose content

If any file write fails:
1. Retry once.
2. If it fails again, include the full content inline in the response under a `## UNSAVED CONTENT — {platform}` header.
3. Never silently lose generated content.

### 7. Update channel tracker

Edit `business/marketing/channel-tracker.md`:
- Add entries to the Upcoming Content section for the target date
- Set status to `drafted` with correct draft location paths

### 8. Output summary

Print a summary table:

```
| Channel | File | Status | Chars/Words |
|---------|------|--------|-------------|
| Twitter | drafts/social/YYYY-MM-DD-twitter.md | saved | ~236 chars |
| TikTok  | drafts/social/YYYY-MM-DD-tiktok.md  | saved | ~125 words |
| ...     | ...  | ...    | ...         |
```

## Error Handling

- If `--anchor` file doesn't exist, warn and generate without it.
- If channel tracker can't be updated, warn but don't block content generation.
- If writing style guide can't be read, warn and apply known defaults (no em dashes, builder voice, no AI clichés).
