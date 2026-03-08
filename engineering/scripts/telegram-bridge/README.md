# Telegram Bridge

Lightweight daemon that bridges Telegram messages to Claude Code running in the Mega-OS project.

## How It Works

1. Long-polls the Telegram Bot API for incoming messages
2. Pipes each message to `claude -p "<msg>"` from the project directory
3. Sends Claude's response back to the Telegram chat

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
| `CLAUDE_TIMEOUT` | Max seconds to wait for Claude response | 300 |

## Built-in Commands

- `/status` — shows contents of `active/now.md`
- `/priorities` — shows contents of `active/priorities.md`
- `/help` — lists available commands

Any other message is forwarded to Claude Code.

## Access Control

Set `ALLOWED_CHAT_IDS` to restrict which Telegram chats can interact with the bot. Find your chat ID by sending a message to the bot and checking the logs.

## Running as a Service

To run persistently, use systemd, tmux, or screen:
```
# tmux
tmux new -s telegram-bridge
python3 telegram_bridge.py

# or systemd (create a unit file)
```
