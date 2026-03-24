---
name: outreach
description: LinkedIn outreach CRM — capture profiles, generate messages, track pipeline, manage follow-ups.
user_invocable: true
arguments:
  - name: subcommand
    description: "Action: setup, process, send, reply, status, import, remind, delete. Default: dashboard view."
    required: false
  - name: name
    description: "Contact name (for send, reply, delete)."
    required: false
---

# /outreach

LinkedIn outreach CRM integrated with Mega-OS. Captures profiles via Chrome extension, generates personalized messages, tracks the full pipeline from capture to reply.

## Product Reference

Read `products/outreach-crm/CLAUDE.md` for architecture, data model, and data locations.

## Subcommand Routing

Parse the user's input to determine which subcommand to run:

- `/outreach` (no args) -> **Dashboard**
- `/outreach setup` -> **Setup**
- `/outreach process` -> **Process**
- `/outreach send <name>` -> **Send**
- `/outreach reply <name>` -> **Reply**
- `/outreach status` -> **Status**
- `/outreach import` -> **Import**
- `/outreach remind` -> **Remind**
- `/outreach delete <name>` -> **Delete**

---

## Dashboard (default)

Show a quick overview of the outreach pipeline:

1. Count unprocessed captures: scan `business/network/captures/` for `.json` files where `"processed": false`
2. Read `business/network/outreach-queue.md` and count contacts by status:
   - Captured | Generated | Sent | Replied | Interested | Not Interested
3. Check `business/network/contacts.md` for follow-ups due (Follow-Up date <= today)
4. Present summary with suggested next action:
   - If pending captures: "N profiles waiting. Run `/outreach process` to generate messages."
   - If generated messages: "N messages ready for review."
   - If follow-ups due: "N follow-ups overdue."

---

## Setup

First-time setup for a new Mega-OS user:

1. Create directories (if they don't exist):
   - `business/network/captures/`
   - `business/network/captures/processed/`
2. Copy templates (if files don't exist):
   - `products/outreach-crm/templates/outreach-queue-template.md` -> `business/network/outreach-queue.md`
   - `products/outreach-crm/templates/outreach-log-template.md` -> `business/network/outreach-log.md`
3. If `business/network/outreach-config.json` doesn't exist:
   - Copy `products/outreach-crm/templates/outreach-config-template.json` -> `business/network/outreach-config.json`
   - Ask the user for: sender_name, sender_title, organization, what_you_do, who_you_want_to_reach
   - Write their answers to the config file
4. Test receiver: run `curl -s http://127.0.0.1:7799/health` and report result
5. Confirm extension is installed (just remind the user to load it in Chrome)

---

## Process

Process pending profile captures and generate outreach messages.

### Context Loading

Before generating any message, load these files (skip gracefully if they don't exist):

1. **`business/network/outreach-config.json`** — sender identity, org, target audience, message style, phrases to avoid. **REQUIRED** — if missing, tell user to run `/outreach setup`.
2. **`core/standards/writing-style.md`** — voice enforcement. Apply the User-Voice Content Gate: no em dashes, no generic AI voice, must sound like the user.
3. **`business/sales/icp.md`** — ideal customer profile (who sender wants to reach)
4. **`business/sales/linkedin-profile.md`** — sender's own LinkedIn profile (for self-intro context)
5. **`drafts/outreach/linkedin-warm-dms.md`** — voice anchor (example messages in the user's style)
6. **`drafts/outreach/linkedin-cold-outreach.md`** — voice anchor (cold outreach templates)
7. **`business/network/contacts.md`** — existing relationships
8. **`business/network/outreach-queue.md`** — current pipeline
9. **`business/network/outreach-log.md`** — message history

### Per-Capture Processing

For each unprocessed `.json` file in `business/network/captures/`:

1. Read the JSON: `{name, url, text, captured_at, processed}`
2. Skip if `processed` is `true`

3. **Check for existing contact:**
   - Search `business/network/contacts.md` for a name match
   - Search `business/network/outreach-queue.md` for a name match
   - Search `business/network/outreach-log.md` for previous messages

4. **Extract contact info from profile text:**
   Parse the captured profile text directly to identify:
   - Title (current job title)
   - Company (current employer)
   - Key details worth mentioning (projects, skills, shared interests)
   Do NOT use regex — read the text and extract naturally. This replaces the dashboard's 100-line `extract_contact_info_from_text()` regex parser.

5. **Generate message:**

   **If NEW contact (no match in contacts.md or queue):**
   - Approach type: `intro`
   - Generate a personalized cold outreach message:
     - 3-5 sentences (or per `outreach-config.json` preferred_message_length)
     - Opens with ONE specific observation from their profile (work, specialty, project)
     - Briefly introduces the sender and their org in one sentence
     - Low-friction ask: a yes/no question, coffee invite, or "would you be open to..."
     - NOT salesy, NOT claiming same industry unless true
     - Avoid phrases listed in config's `phrases_to_avoid`
     - Sign with sender_name + organization (from config)
   - If config has event fields filled in: optionally mention the event as part of the invite

   **If EXISTING contact (found in contacts.md, queue, or log):**
   - Approach type: `follow_up`
   - Read their message history from outreach-log.md
   - Generate a follow-up message:
     - References the original outreach naturally
     - Adds a NEW angle or piece of value (don't repeat what was said)
     - 2-3 sentences max
     - Simple, low-friction CTA
     - Feels human, not automated

6. **Present to user with options:**
   - Show the generated message with contact context (name, title, company, LinkedIn URL)
   - **Approve**: save to outreach-queue.md with status "generated", approach type noted
   - **Edit**: user modifies the message directly, then approve
   - **Regenerate**: generate a different version
     - Pass the old message as context ("do NOT repeat this")
     - Accept optional feedback from the user ("too formal", "don't mention X", "more casual")
     - Generate with a different angle
   - **Skip**: mark the capture as processed but don't add to queue

7. **On approve:**
   - Update the JSON capture file: set `"processed": true`
   - Move the file to `business/network/captures/processed/`
   - Add a row to `business/network/outreach-queue.md`:
     `| Name | Company | Title | linkedin_url | generated | approach_type | message_text | captured_date | notes |`
   - Update the "Last updated" date in outreach-queue.md

---

## Send

Mark a message as sent and update the relationship tracker.

1. Find the contact in `business/network/outreach-queue.md` by name (case-insensitive match)
2. If not found, report error
3. Confirm the approach type (default from queue, or ask user):
   - `intro`, `follow_up`, `value_prop`, `event_invite`, `mutual_connection`
4. Add entry to `business/network/outreach-log.md`:
   `| Name | today's date | message_text | approach_type | | | | |`
5. Update `business/network/outreach-queue.md`: change status from "generated" to "sent"
6. Update `business/network/contacts.md` using the Contact Follow-Up Completion protocol from CLAUDE.md:
   - If contact doesn't exist in contacts.md: add new row
   - Set `Platform` = "LinkedIn"
   - Set `Last Contact` = today
   - Set `Cadence` based on relationship: 7 (new/prospect) or 21 (established)
   - Calculate `Follow-Up` = today + Cadence
   - Set `Next Action` = "Wait for reply, follow up if no response"
   - Set `Context` = title, company, how connected
   - Update `Notes` with outreach context
7. Offer to commit

---

## Reply

Log a response from a contact.

1. Find the contact in `business/network/outreach-queue.md` by name
2. Ask the user:
   - What did they say? (response text — can be a summary)
   - Sentiment: `positive`, `neutral`, `negative`
3. Update `business/network/outreach-log.md`:
   - Find the most recent entry for this contact
   - Fill in the Response, Sentiment, and Response Date columns
4. Update `business/network/outreach-queue.md`: change status to "replied"
5. Update `business/network/contacts.md`:
   - Set `Last Contact` = today
   - Recalculate `Follow-Up` = today + Cadence
   - Update `Next Action` based on sentiment:
     - Positive: "Schedule call/meeting" or "Send follow-up resource"
     - Neutral: "Follow up with value add"
     - Negative: "Respect boundary, no further outreach"
6. If positive: suggest changing queue status to "interested"
7. Offer to commit

---

## Status

Compute analytics from the pipeline data.

Read `business/network/outreach-queue.md` and `business/network/outreach-log.md`, then report:

- **Pipeline:** total contacts, breakdown by status (captured/generated/sent/replied/interested/not_interested)
- **Activity:** messages sent today, messages sent this week
- **Response:** awaiting reply count, positive reply rate (positive / total replied)
- **Follow-ups:** overdue count (from contacts.md where Follow-Up <= today and Next Action isn't "no further outreach")
- **Approach effectiveness:** for each approach type with 3+ messages, show positive response rate
- **Message depth:** average messages per contact

Present as a clean summary.

---

## Import

Bulk import contacts from CSV.

1. Ask the user for a file path or accept inline CSV data
2. Parse columns (flexible matching):
   - name / Name (required)
   - company / Company
   - title / Title / job_title / Job Title
   - linkedin_url / LinkedIn URL / linkedin
   - notes / Notes
3. For each row with a non-empty name:
   - Add to `business/network/outreach-queue.md` with status "captured"
4. Skip rows with no name
5. Report: "Imported N contacts, skipped M rows"
6. Offer to commit

---

## Remind

Generate follow-up drafts for contacts that need attention.

1. Read `business/network/outreach-queue.md` and `business/network/contacts.md`
2. Find contacts that need follow-up:
   - Status "interested" — draft event reminder or next-step message
   - Status "replied" with last contact > 7 days ago — draft follow-up
   - Status "sent" with last contact > follow_up_days (from config, default 7) — draft check-in
3. For each, generate a short follow-up message:
   - If event fields are filled in config: mention the event
   - Reference previous interaction
   - Keep it warm and brief (2-3 sentences)
4. Present all drafts for batch review (approve/edit/regenerate/skip each)
5. Approved messages go to outreach-queue.md with updated status

---

## Delete

Remove a contact from the pipeline.

1. Find the contact in `business/network/outreach-queue.md` by name
2. Remove their row from outreach-queue.md
3. Ask: "Also remove from contacts.md?" (default: no)
4. Do NOT delete capture files (kept in `captures/processed/` for reference)
5. Offer to commit
