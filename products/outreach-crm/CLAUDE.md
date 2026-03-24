# Outreach CRM

LinkedIn outreach CRM for Mega-OS. Captures profiles via Chrome extension, generates personalized messages via Claude, tracks the full pipeline from capture to reply.

## Architecture

```
Chrome Extension -> Python Receiver (port 7799) -> JSON captures
                                                       |
                                        /outreach skill (Claude Code)
```

- **Extension** (`extension/`): Manifest V3 Chrome extension. Captures LinkedIn profile text and sends to local receiver.
- **Receiver** (`receiver/receiver.py`): Minimal Python HTTP server (~80 lines, stdlib only). Saves JSON files to `business/network/captures/`. No LLM, no processing.
- **Skill** (`.claude/skills/outreach/SKILL.md`): `/outreach` skill processes captures, generates messages, tracks pipeline. Claude Code is the LLM.

## Data Model

### Contact Statuses
| Status | Meaning |
|--------|---------|
| `captured` | Profile captured, awaiting processing |
| `generated` | Message drafted, awaiting review |
| `sent` | Message sent, awaiting reply |
| `replied` | Contact responded |
| `interested` | Expressed interest |
| `not_interested` | Declined |

### Approach Types
`intro`, `follow_up`, `value_prop`, `event_invite`, `mutual_connection`

### Sentiment Values
`positive`, `neutral`, `negative`, `no_reply`

## Data Locations

| File | Purpose |
|------|---------|
| `business/network/captures/*.json` | Raw captures from extension |
| `business/network/captures/processed/` | Archived after processing |
| `business/network/outreach-config.json` | User config (sender identity, org, style) |
| `business/network/outreach-queue.md` | Pipeline view (active contacts) |
| `business/network/outreach-log.md` | Full message history + sentiment |
| `business/network/contacts.md` | Relationship tracker (updated on send) |

## Receiver

- Binds: `127.0.0.1:7799` (configurable via `OUTREACH_PORT` env var)
- `POST /capture` — saves JSON capture file
- `GET /health` — returns status + pending count
- CORS enabled (required for extension)
- Start: `bash receiver/start.sh`
- Stop: `bash receiver/stop.sh`

## Extension

- Manifest V3, runs on `linkedin.com/in/*`
- Clicks "see more" buttons to expand profile sections
- Extracts profile text from `<main>`, truncates at noise markers (8K char limit)
- Gets name from `h1` or URL slug fallback
- Sends `{name, url, text}` to receiver via service worker (CSP bypass)
