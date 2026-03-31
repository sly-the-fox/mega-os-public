---
name: connect
description: Find relevant connections in your network, surface non-obvious matches, and draft introduction messages.
user_invocable: true
arguments:
  - name: subcommand
    description: "Action: who, intro, refresh, profiles. Default: who."
    required: false
  - name: name
    description: "Contact name(s) — for who and intro subcommands."
    required: false
---

# /connect

Network connection matcher — surfaces relevant connections between contacts, explains why they should know each other, and drafts double-opt-in introductions.

## Subcommand Routing

Parse the user's input to determine which subcommand to run:

- `/connect who <name>` -> **Who**
- `/connect intro <A> <B>` -> **Intro**
- `/connect refresh` -> **Refresh**
- `/connect profiles` -> **Profiles**
- `/connect` (no args) -> prompt: "Who do you want to find connections for?"

---

## Who

**Find the top 5 contacts most relevant to a given person.**

### Steps

1. Run `python3 engineering/scripts/match-contacts.py --who "<name>"` to generate matches
   - If the script errors (contact not found, fastembed missing), report the error clearly
   - If results are cached and fresh (OUTPUT_JSON mtime < 1 hour, same target), read cached results instead of re-running

2. Read `business/network/connection-matches.json` for the results

3. For each match in the top 5, generate a one-sentence explanation:
   - Ground it in the `shared_tags` and `explanation_hints` from the JSON
   - Reference specific details from `business/network/contacts.md` for both the target and the match
   - Keep it conversational: "Ken and Casey both work in AI consulting and are Colorado-based. Casey has deep enterprise connections that could complement Ken's SMB focus."

4. For each match, suggest an action based on relationship strength of BOTH parties:
   - Both >= 0.7: "Introduce directly — you know both well"
   - Both >= 0.5: "Mention in your next follow-up with [name]"
   - One < 0.5: "Build the relationship with [weaker contact] first"

5. If the target contact was captured within the last 48 hours (check `Last Contact` date), flag: "Post-event follow-up opportunity — [name] is a fresh connection"

6. Present the ranked list with:
   - Match rank and name
   - Similarity score and relationship strength
   - One-sentence explanation
   - Suggested action

---

## Intro

**Draft double-opt-in introduction messages between two contacts.**

### Prerequisite Check

1. Check relationship strength for BOTH contacts (from connection-matches.json or compute via `--profiles`)
2. If either contact has relationship_strength < 0.5:
   - Warn: "You may not know [name] well enough to introduce them (strength: X). Proceed anyway?"
   - If user declines, stop
3. If both contacts are below 0.3, refuse: "Build stronger relationships with both before introducing them."

### Context Loading

Before generating any message:
1. Read `core/standards/writing-style.md` — **MANDATORY** (User-Voice Content Gate)
2. Read `business/network/outreach-config.json` for sender identity
3. Read both contacts' full entries from `business/network/contacts.md`
4. Check `business/network/event-debriefs/` for shared events between the two contacts
5. Read the match data from `connection-matches.json` (shared tags, explanation hints)

### Message Generation

Generate three pieces:

**1. Heads-up to A:**
```
Hey [A first name], I know someone working on [relevant thing from B's profile].
[One sentence on why they'd benefit from connecting — grounded in shared tags/context].
Would you be open to an intro?
```

**2. Heads-up to B:**
Same structure, personalized for B's perspective.

**3. Combined intro (sent after both opt in):**
```
[A first name], meet [B first name]. [One sentence on B's work relevant to A].
[B first name], [A first name] [one sentence on A's work relevant to B].
I think you two would have a great conversation about [shared topic].
```

### Rules
- All messages MUST follow `core/standards/writing-style.md` — no em dashes, no generic AI voice
- Reference actual shared context, not invented connections
- Keep each message to 3-5 sentences max
- Sign the combined intro with the sender's name from outreach-config.json

### On Approve

1. Log to `business/network/outreach-log.md`:
   - Two rows: one for A (heads-up), one for B (heads-up)
   - Approach: `introduction`
   - Intent: `introduction`
2. Update `active/now.md` with next action: "Wait for [A] and [B] to confirm intro"
3. Offer to commit

---

## Refresh

**Re-run the matching engine and report profile stats.**

1. Run `python3 engineering/scripts/match-contacts.py --profiles`
2. Report:
   - Total contacts parsed
   - Contacts with sufficient data
   - Contacts skipped (insufficient data) — list names
   - Contacts with LinkedIn captures
   - Unmatched captures (captured but not in contacts.md)
3. If the user wants to run a full match afterward, suggest `/connect who <name>`

---

## Profiles

**Show all contacts with tags and relationship strength.**

1. Run `python3 engineering/scripts/match-contacts.py --profiles`
2. Format output as a table:

```
| Contact | Tags | Strength | Capture? |
|---------|------|----------|----------|
| Ken Clark | domain:ai, domain:consulting, geo:colorado, role:executive | 0.5 | Yes |
| Casey Lembke | domain:ai, domain:consulting, geo:colorado | 0.7 | No |
...
```

3. Highlight contacts with strength < 0.3 (below introduction threshold)
4. Note any contacts with no tags (composite text may be too sparse)

---

## Data Sources

| Source | What It Provides |
|--------|-----------------|
| `business/network/contacts.md` | Names, context, notes, relationship status |
| `business/network/captures/*.json` | LinkedIn profile full text |
| `business/network/captures/processed/*.json` | Previously processed LinkedIn captures |
| `business/network/connection-matches.json` | Generated output (gitignored, regenerable) |
| `business/network/outreach-config.json` | Sender identity for intro messages |
| `business/network/event-debriefs/*.md` | Event conversation notes |
| `core/standards/writing-style.md` | Voice enforcement for generated messages |
