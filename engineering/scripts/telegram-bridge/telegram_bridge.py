#!/usr/bin/env python3
"""
Telegram Bridge for Mega-OS

Polls Telegram Bot API for messages, pipes them to Claude Code via CLI,
and sends responses back to the Telegram chat.

Prerequisites:
    - Create a bot via @BotFather on Telegram
    - Set TELEGRAM_BOT_TOKEN in .env
    - Ensure `claude` CLI is available on PATH

Usage:
    python3 telegram_bridge.py
"""

import datetime
import json
import logging
import os
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# --- Rate Limiting ---

RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "10"))  # max messages per window
_rate_tracker: dict[int, list[float]] = defaultdict(list)


def is_rate_limited(chat_id: int) -> bool:
    """Check if a chat has exceeded the rate limit."""
    now = time.time()
    timestamps = _rate_tracker[chat_id]
    # Prune old entries
    _rate_tracker[chat_id] = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
    if len(_rate_tracker[chat_id]) >= RATE_LIMIT_MAX:
        return True
    _rate_tracker[chat_id].append(now)
    return False

# --- Configuration ---

SCRIPT_DIR = Path(__file__).parent
ENV_FILE = SCRIPT_DIR / ".env"
MEGA_OS_PATH = os.getenv("MEGA_OS_PATH", str(SCRIPT_DIR.parent.parent.parent))

# Load .env file
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_CHAT_IDS = os.getenv("ALLOWED_CHAT_IDS", "")  # comma-separated, empty = allow all
BRIDGE_PASSPHRASE = os.getenv("BRIDGE_PASSPHRASE", "")  # second-factor auth
POLL_TIMEOUT = int(os.getenv("POLL_TIMEOUT", "30"))
CLAUDE_TIMEOUT = int(os.getenv("CLAUDE_TIMEOUT", "600"))

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Track which chats have authenticated (passphrase verified)
authenticated_chats: set[int] = set()

# --- Message Logging ---

CHAT_LOG_FILE = SCRIPT_DIR / "chat-log.jsonl"
LOG_MESSAGES = os.getenv("LOG_MESSAGES", "true").lower() in ("true", "1", "yes")


def log_message(chat_id: int, username: str, direction: str, text: str):
    """Append a message record to the chat log (JSONL format)."""
    if not LOG_MESSAGES:
        return
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "chat_id": chat_id,
        "username": username,
        "direction": direction,
        "text": text,
    }
    try:
        with open(CHAT_LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        logger.warning(f"Failed to write chat log: {e}")


# --- Session Persistence ---

SESSIONS_FILE = SCRIPT_DIR / "sessions.json"


def load_sessions() -> dict[str, str]:
    """Load chat_id -> session_id mapping from disk."""
    if SESSIONS_FILE.exists():
        try:
            return json.loads(SESSIONS_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_sessions(sessions: dict[str, str]):
    """Save chat_id -> session_id mapping to disk."""
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))


# Global session map (str keys because JSON keys are strings)
chat_sessions: dict[str, str] = load_sessions()


def validate_config():
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not ALLOWED_CHAT_IDS:
        missing.append("ALLOWED_CHAT_IDS")
    if missing:
        logger.error(f"Required env vars not set: {', '.join(missing)}. Create a .env file or set them.")
        sys.exit(1)
    if not BRIDGE_PASSPHRASE:
        logger.warning("BRIDGE_PASSPHRASE not set — second-factor auth disabled.")
    if not Path(MEGA_OS_PATH).is_dir():
        logger.error("MEGA_OS_PATH directory not found.")
        sys.exit(1)


def get_allowed_chat_ids() -> set[int]:
    if not ALLOWED_CHAT_IDS:
        return set()
    return {int(cid.strip()) for cid in ALLOWED_CHAT_IDS.split(",") if cid.strip()}


def telegram_request(method: str, params: dict | None = None) -> dict:
    """Make a request to the Telegram Bot API."""
    url = f"{TELEGRAM_API}/{method}"
    with httpx.Client(timeout=POLL_TIMEOUT + 10) as client:
        response = client.post(url, json=params or {})
        response.raise_for_status()
        return response.json()


def get_updates(offset: int | None = None) -> list[dict]:
    """Long-poll for new messages."""
    params = {"timeout": POLL_TIMEOUT, "allowed_updates": ["message"]}
    if offset is not None:
        params["offset"] = offset
    result = telegram_request("getUpdates", params)
    return result.get("result", [])


def send_message(chat_id: int, text: str, reply_to: int | None = None):
    """Send a message to a Telegram chat, splitting if too long."""
    max_len = 4000  # Telegram limit is 4096, leave margin
    chunks = [text[i : i + max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        params = {"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"}
        if reply_to:
            params["reply_to_message_id"] = reply_to
        try:
            telegram_request("sendMessage", params)
        except httpx.HTTPStatusError:
            # Retry without markdown if parsing fails
            params.pop("parse_mode", None)
            telegram_request("sendMessage", params)


def handle_builtin_command(chat_id: int, command: str) -> bool:
    """Handle built-in commands. Returns True if handled."""
    if command == "/status":
        now_file = Path(MEGA_OS_PATH) / "active" / "now.md"
        text = now_file.read_text() if now_file.exists() else "No active/now.md found."
        send_message(chat_id, text)
        return True

    if command == "/priorities":
        prio_file = Path(MEGA_OS_PATH) / "active" / "priorities.md"
        text = prio_file.read_text() if prio_file.exists() else "No active/priorities.md found."
        send_message(chat_id, text)
        return True

    if command == "/reset":
        # Clear stored session for this chat
        key = str(chat_id)
        if key in chat_sessions:
            del chat_sessions[key]
            save_sessions(chat_sessions)
        send_message(chat_id, "Session cleared. Next message starts a fresh conversation.")
        return True

    if command == "/help":
        send_message(
            chat_id,
            "Commands:\n"
            "/status — Show current focus\n"
            "/priorities — Show priority list\n"
            "/reset — Clear context and start fresh\n"
            "/help — Show this help\n\n"
            "Sessions persist automatically — follow-up messages continue the conversation.\n"
            "Timeout: 10 minutes per request.",
        )
        return True

    return False


def invoke_claude(message: str, chat_id: int, use_session: bool = False) -> str:
    """Send a message to Claude Code and return the response.

    Resumes the stored session for this chat_id (or starts a new one).
    Session IDs are persisted to disk so they survive bridge restarts.
    """
    try:
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)  # Allow running from inside a Claude session

        cmd = [
            "claude",
            "-p",
            "--output-format", "json",
        ]

        # Resume existing session if in chat mode and we have a stored session
        key = str(chat_id)
        if use_session and key in chat_sessions:
            cmd.extend(["--resume", chat_sessions[key]])

        # "--" prevents message text from being parsed as flags
        cmd.append("--")
        cmd.append(message)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=CLAUDE_TIMEOUT,
            env=env,
            cwd=MEGA_OS_PATH,
        )
        if result.returncode != 0:
            logger.error(f"Claude exit {result.returncode}: {result.stderr[:200]}")
            # If resume failed (stale session), clear it and retry fresh
            if use_session and key in chat_sessions:
                logger.info(f"Clearing stale session for chat {chat_id}, retrying fresh")
                del chat_sessions[key]
                save_sessions(chat_sessions)
                return invoke_claude(message, chat_id, use_session=False)
            return "Claude encountered an error processing your request."

        # Parse JSON response to extract session_id and result text
        response_text = result.stdout.strip()
        try:
            data = json.loads(response_text)
            # Save session ID for conversational continuity
            session_id = data.get("session_id", "")
            if session_id:
                chat_sessions[key] = session_id
                save_sessions(chat_sessions)
                logger.info(f"Stored session {session_id[:12]}... for chat {chat_id}")

            # Extract the actual response text
            return data.get("result", response_text) or "(empty response)"
        except json.JSONDecodeError:
            # If not valid JSON, return raw output
            return response_text or "(empty response)"

    except subprocess.TimeoutExpired:
        return "Claude timed out (10 min limit). For complex tasks, try running directly in the terminal."
    except FileNotFoundError:
        return "Service temporarily unavailable."


def main():
    validate_config()
    allowed = get_allowed_chat_ids()

    logger.info("Telegram bridge starting...")
    logger.info(f"Mega-OS path: {MEGA_OS_PATH}")
    logger.info(f"Allowed chat IDs: {allowed or 'all'}")

    # Verify bot connection
    try:
        me = telegram_request("getMe")
        bot_name = me.get("result", {}).get("username", "unknown")
        logger.info(f"Connected as @{bot_name}")
    except Exception as e:
        logger.error(f"Failed to connect to Telegram: {e}")
        sys.exit(1)

    offset = None

    while True:
        try:
            updates = get_updates(offset)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)
            continue

        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            text = message["text"].strip()
            msg_id = message["message_id"]
            user = message.get("from", {}).get("username", "unknown")

            # Access control — chat ID allowlist
            if allowed and chat_id not in allowed:
                logger.warning(f"Rejected message from unauthorized chat {chat_id}")
                continue

            # Second-factor auth — passphrase required once per session
            if BRIDGE_PASSPHRASE and chat_id not in authenticated_chats:
                if text == BRIDGE_PASSPHRASE:
                    authenticated_chats.add(chat_id)
                    send_message(chat_id, "Authenticated. You may now send commands.")
                    logger.info(f"Chat {chat_id} authenticated (user: {user})")
                else:
                    send_message(chat_id, "Please authenticate with the passphrase.")
                continue

            logger.info(f"Message from {user} (chat {chat_id}): {text[:80]}")
            log_message(chat_id, user, "in", text)

            # Rate limiting
            if is_rate_limited(chat_id):
                send_message(chat_id, "Rate limit exceeded. Please wait before sending more messages.")
                logger.warning(f"Rate limited chat {chat_id}")
                continue

            # Built-in commands
            if text.startswith("/") and handle_builtin_command(chat_id, text.split()[0]):
                continue

            # Send "thinking" indicator
            try:
                telegram_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})
                send_message(chat_id, "Thinking...")
            except Exception:
                pass

            # Invoke Claude (always resumes session for conversational continuity)
            response = invoke_claude(text, chat_id, use_session=True)
            send_message(chat_id, response, reply_to=msg_id)
            log_message(chat_id, "bot", "out", response)
            logger.info(f"Response sent to chat {chat_id} ({len(response)} chars)")


if __name__ == "__main__":
    main()
