# Secrets Management

## Inventory

| Secret | Used By | Location | Rotation Policy |
|--------|---------|----------|-----------------|
| TELEGRAM_BOT_TOKEN | notify-telegram.sh, send-telegram.py, telegram-bridge | `.env` (project root), `engineering/scripts/telegram-bridge/.env` | Quarterly |
| NOTIFY_CHAT_ID / ALLOWED_CHAT_IDS | notify-telegram.sh, send-telegram.py, telegram-bridge | `.env` (project root) | Static (chat ID) |
| GITHUB_TOKEN | fetch-metrics.py | Environment variable | Per GitHub expiry |
| CLOUDFLARE_API_TOKEN | deploy-sigil-site.sh (via wrangler) | Environment variable | Quarterly |
| ANTHROPIC_API_KEY | Claude Code runtime | Environment variable | Per Anthropic policy |

## Committed Secret Alert

**`engineering/scripts/telegram-bridge/.env`** contains an actual bot token committed to git. This file should be gitignored and the token rotated. The `.env.example` file in the same directory is the correct pattern.

**Remediation:** Rotate the Telegram bot token via BotFather, update `.env`, and add `engineering/scripts/telegram-bridge/.env` to `.gitignore` if not already covered.

## Policy

- **Never commit secrets.** Use `.env` files (gitignored) or environment variables.
- **Gitignore patterns:** `.env*`, `*.pem`, `*.key`, `sessions.json` — already in `.gitignore`
- **Rotation:** API keys quarterly. Rotate immediately if exposed.
- **Storage:** Environment variables for runtime. `.env` files for local dev (never committed).
- **New secrets:** Add to this inventory table when created.
- **Decommissioned secrets:** Remove from environment and note here with date.

## Gitignore Coverage

The root `.gitignore` covers:
- `.env*` — all env files at any directory level
- `*.pem`, `*.key` — certificate and key files
- `sessions.json` — session tokens

*Last audited: 2026-03-27*
