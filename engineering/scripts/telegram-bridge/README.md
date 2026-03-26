# Telegram Bridge

Lightweight daemon that bridges Telegram messages to Claude Code running in the Mega-OS project.

## How It Works

1. Long-polls the Telegram Bot API for incoming messages
2. Pipes each message to `claude --message "<msg>" --cwd $MEGA_OS_PATH` with JSON output
3. Sends Claude's response back to the Telegram chat
4. Maintains per-chat session persistence for conversational continuity

## Setup

1. Create a Telegram bot via [@BotFather](https://t.me/BotFather) and get the bot token.

2. Copy the env file and fill in your token:
   ```
   cp .env.example .env
   # Edit .env with your TELEGRAM_BOT_TOKEN
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the bridge:
   ```
   python3 telegram_bridge.py
   ```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather | (required) |
| `MEGA_OS_PATH` | Path to mega-os directory | auto-detected |
| `ALLOWED_CHAT_IDS` | Comma-separated chat IDs to allow (empty = all) | (empty) |
| `POLL_TIMEOUT` | Telegram long-poll timeout in seconds | 30 |
| `CLAUDE_TIMEOUT` | Max seconds to wait for Claude response | 600 |
| `BRIDGE_PASSPHRASE` | Passphrase for second-factor auth (optional) | (empty) |
| `RATE_LIMIT_MAX` | Max messages per 60-second window per chat | 10 |
| `LOG_MESSAGES` | Log all messages to `chat-log.jsonl` | `true` |

## Built-in Commands

- `/status` — shows contents of `active/now.md`
- `/priorities` — shows contents of `active/priorities.md`
- `/help` — lists available commands
- `/reset` — clears your session context and starts a fresh conversation
- `/restart` — restart the bridge process (requires re-authentication)

Any other message is forwarded to Claude Code.

## Session Persistence

Each chat maintains its own Claude Code session. Sessions are saved to `sessions.json` and automatically resumed on each message, so conversations continue where you left off. If a stored session becomes stale, the bridge detects this and starts a fresh session automatically.

Use `/reset` to manually clear your session and start fresh.

## Progress Indicator

While Claude is processing your request, the bridge sends a "thinking..." indicator message so you know it's working. This is especially useful for long-running requests (up to the 10-minute timeout).

## Passphrase Auth

Set `BRIDGE_PASSPHRASE` in `.env` to require authentication before a chat can interact with the bot. Users must send the correct passphrase once per session. This is recommended for public-facing bots.

## Message Logging

All messages (incoming and outgoing) are logged to `chat-log.jsonl` in JSONL format (one JSON object per line). Each entry contains a UTC timestamp, chat ID, username, direction (`in`/`out`), and the message text.

Set `LOG_MESSAGES=false` in `.env` to disable. See `chat-log.jsonl.example` for the format.

The log file is gitignored. The example file syncs to the public repo.

## Rate Limiting

Each chat is limited to a configurable number of messages per 60-second window (default: 10). Set `RATE_LIMIT_MAX` in `.env` to adjust. Messages that exceed the limit are rejected with a notification.

## Access Control

Set `ALLOWED_CHAT_IDS` to restrict which Telegram chats can interact with the bot. Find your chat ID by sending a message to the bot and checking the logs.

## Running as a Service (systemd)

The bridge runs as a systemd user service that auto-starts on boot and restarts on crash.

### Setup

```bash
# Enable user services without active login session
loginctl enable-linger abzu

# Reload and enable the service
systemctl --user daemon-reload
systemctl --user enable telegram-bridge
systemctl --user start telegram-bridge
```

The unit file lives at `~/.config/systemd/user/telegram-bridge.service`.

### Management

```bash
# Check status
systemctl --user status telegram-bridge

# View logs (live)
journalctl --user -u telegram-bridge -f

# View recent logs
journalctl --user -u telegram-bridge --since "30 min ago"

# Manual stop/start
systemctl --user stop telegram-bridge
systemctl --user start telegram-bridge
```

### Remote restart from iPhone

Send `/restart` in Telegram. The bridge exits cleanly, systemd restarts it within ~8 seconds (5s restart delay + startup). You'll need to re-authenticate with the passphrase since `authenticated_chats` is in-memory only.

### Crash loop protection

If the bridge crashes 5 times within 5 minutes, systemd stops restarting it to prevent crash loops. To recover:

```bash
systemctl --user reset-failed telegram-bridge
systemctl --user start telegram-bridge
```
