---
name: dream
description: "Overnight dreaming -- generates One Question to Sit With based on the week's context, plus optional connection discovery and memory consolidation."
invocation: /dream
user_invocable: true
arguments: "--full (run all 4 dream processes, not just the question)"
---

# Dream

Generate a contemplative question from the week's context. Not a task. Not a status update. A question worth carrying in the back of your mind.

## Steps

### 1. Gather Context (last 7 days)

Read the following files. Extract decisions, completions, blockers, shifts, and tensions from the past 7 days:

- `active/now.md` -- current focus, what's done, what's next
- `active/priorities.md` -- what matters and in what order
- `active/blockers.md` -- what's stuck
- `core/history/decisions.md` -- decisions made in the last 7 days (filter by date column)
- `core/history/master-timeline.md` -- session entries from the last 7 days
- `active/signals.md` -- if it exists, lightweight agent observations
- `active/improvements.md` -- what the system is trying to become
- `active/risks.md` -- what threatens the work

Also check git log for the last 7 days:
```bash
git log --since="7 days ago" --format="%ai %s" --no-merges
```

### 2. Synthesize Patterns

From the gathered context, identify:
- **Tensions** -- where priorities pull in different directions
- **Recurring themes** -- what keeps showing up across different files
- **Gaps** -- what's conspicuously absent from the week's activity vs. stated priorities
- **Momentum** -- what's building energy, what's losing it
- **Emerging realities** -- what's becoming true that wasn't true 7 days ago

### 3. Generate the One Question

Craft a single question that:
- The context is asking but nobody has voiced
- Is about direction, identity, or what's forming -- not about tasks
- Cannot be answered with a checklist or a yes/no
- Would be worth carrying in the back of your mind for the day
- Is specific enough to be useful (not generic philosophy)
- References the actual state of the work, not abstract principles

**Bad examples** (too generic):
- "What really matters to you?"
- "Are you building what you want?"
- "What would happen if you slowed down?"

**Good examples** (grounded in context):
- "You shipped Sigil's landing page and Substack in the same week but haven't touched consulting outreach -- is consulting still the first revenue path, or has writing already taken that spot?"
- "Three of your four revenue streams require an audience you don't have yet. Which one builds the audience the others need?"
- "The system now has 38 agents and 14 cron jobs. At what point does maintaining the system become the work?"

### 4. Write Output

**Default mode (lite):** Write to `active/dream-report.md`:

```markdown
# One Question to Sit With

Generated: YYYY-MM-DD

> [The question]

**Context:** [1-2 sentences on what surfaced this question from the week's data]
```

**Full mode (`--full`):** Write to `active/dream-report.md`:

```markdown
# Dream Report

Generated: YYYY-MM-DD

## One Question to Sit With

> [The question]

**Context:** [1-2 sentences on what surfaced this question]

## What Crystallized

[Compressed patterns from the week's decisions and events. Not a summary -- a distillation. What themes emerged when you look at the week as a whole rather than day by day?]

## Connections Noticed

[Non-obvious cross-domain links. Things that aren't filed together but are actually about the same underlying dynamic. 2-4 bullet points max.]

## What's Forming

[What might be true in 30 days that isn't true today? Based on current trajectories, not wishes. 2-3 sentences.]
```

### 5. Console Output

Print the One Question to console so it appears in cron logs and Telegram notifications:

```
Dream complete.

> [The question]
```

## Mode Detection

Check if the user's prompt contains `--full`. If yes, run full mode. Otherwise, run lite mode (just the question).

## Quality Criteria

The question is good if:
- Reading it produces a slight pause -- a "huh" moment
- It connects two things the founder hasn't explicitly connected
- It's uncomfortable in a productive way, not in a judgmental way
- It would still be relevant 3 days from now
- It couldn't have been generated without reading the actual context
