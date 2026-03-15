# Reddit Comments

Generate authentic Reddit comments in Chadd's voice.

## Usage
```
/reddit-comments <thread-url-or-context>
```

## Inputs
- Thread title and context (URL or pasted text)
- Subreddit
- Optional: desired stance (agree / disagree / question / reaction / experience)

## Process

1. **Read the calibration sample** at `style-samples/reddit-casual.md` — this is the voice anchor.
2. **Read the subreddit adaptation rules** in `core/standards/writing-style.md` under "Platform-Specific Adaptations > Reddit."
3. **Draft the comment** following these rules:

### Voice Rules
- Lead with a direct opinion or reaction, not a meta-observation
- Commas where periods would go, occasional run-ons
- Reference things you've seen, built, or experienced — not abstract analysis
- Slight imperfection is good. Don't over-polish.
- No frameworks, no "the interesting part is," no "curious whether"
- Personality and color over analytical precision

### Length Distribution (across a batch)
- 60% — 1-3 sentences
- 30% — short paragraph (4-6 sentences)
- 10% — longer response (2 short paragraphs max)

### Subreddit Culture
- **r/ExperiencedDevs** — dry, jaded, practical. Short and opinionated. No enthusiasm.
- **r/LocalLLaMA** — enthusiastic, technical, benchmarks matter. Can geek out.
- **r/MachineLearning** — academic-adjacent, skeptical, values rigor. Don't hand-wave.
- **r/ClaudeAI** — casual, experience-sharing, product-focused.
- **r/artificial** — general audience, mix of informed and surface-level. Keep it accessible.
- **r/devops** — battle-scarred, practical, loves war stories. No theory without practice.
- **r/softwarearchitecture** — thoughtful, tolerates longer responses if they're good.
- **r/ChatGPTCoding** — casual, practical, "did this work for you?" energy.

### Hard Rules
- Never mention own projects unless directly relevant AND it's < 20% of comments in a batch
- Never generate more than 3 comments in one invocation
- Each comment must have a different structure from the others
- Disagree with something sometimes. Questions are more authentic than always adding value.
- If generating multiple comments, explicitly vary: length, opener style, tone, and whether it ends with a question

4. **Run through Editor agent** with explicit instruction: "Break any uniformity between these comments. They should not look like they came from the same session."
5. **Save to** `drafts/social/YYYY-MM-DD-reddit-comments.md` with status tracking per comment.

## Status Tracking
Each comment gets a status field:
```
**Status:** drafted / reviewed / posted / skipped
```

## Anti-Patterns (Will Get Flagged)
- All comments same length
- All comments same structure (opener → expansion → experience → question)
- "The X is the most interesting part..."
- "Curious whether..."
- "From an architecture perspective..."
- Starting with a meta-observation about the thread
- Ending every comment with a question
- 180+ words when 40 would do
