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
import re
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

# --- Persistent HTTP Client ---
_http_client: httpx.Client | None = None
_consecutive_failures: int = 0
_cooldown_until: float = 0.0

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
    """Save chat_id -> session_id mapping to disk (atomic write)."""
    try:
        tmp_path = SESSIONS_FILE.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(sessions, indent=2))
        os.replace(tmp_path, SESSIONS_FILE)
    except OSError as e:
        logger.warning(f"Failed to save sessions: {e}")


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


def _init_client():
    """Create (or replace) the persistent httpx client."""
    global _http_client
    _http_client = httpx.Client(timeout=httpx.Timeout(POLL_TIMEOUT + 10, connect=10.0))


def _recreate_client():
    """Close and recreate the HTTP client after sustained failures."""
    global _http_client
    if _http_client is not None:
        try:
            _http_client.close()
        except Exception:
            pass
    _init_client()
    logger.info("HTTP client recreated after sustained failures")


def telegram_request(method: str, params: dict | None = None) -> dict:
    """Make a request to the Telegram Bot API with retry logic."""
    global _consecutive_failures, _cooldown_until

    # Cooldown: skip sends (not polls) during sustained outage
    if _consecutive_failures >= 5 and method != "getUpdates":
        now = time.time()
        if now < _cooldown_until:
            raise httpx.TransportError(
                f"Cooldown active ({int(_cooldown_until - now)}s remaining)"
            )
        logger.info("Cooldown expired, retrying")

    url = f"{TELEGRAM_API}/{method}"
    last_exc: Exception | None = None

    for attempt in range(3):
        try:
            response = _http_client.post(url, json=params or {})
            # Handle 429 rate limit
            if response.status_code == 429:
                retry_after = min(int(response.headers.get("Retry-After", "5")), 30)
                logger.warning(f"Telegram 429 — backing off {retry_after}s")
                time.sleep(retry_after)
                continue
            response.raise_for_status()
            _consecutive_failures = 0
            return response.json()
        except httpx.TransportError as e:
            last_exc = e
            _consecutive_failures += 1
            if attempt < 2:
                delay = 2 ** attempt  # 1s, 2s
                logger.warning(
                    f"Transport error (attempt {attempt + 1}/3): {e} — retrying in {delay}s"
                )
                time.sleep(delay)
            else:
                logger.error(f"Transport error (attempt 3/3): {e} — exhausted retries")
                if _consecutive_failures >= 5:
                    _cooldown_until = time.time() + 30
                    logger.warning("5+ consecutive failures — entering 30s cooldown")
                _recreate_client()
        except httpx.HTTPStatusError:
            raise  # Don't retry client errors (400, 403, etc.)

    raise last_exc or httpx.TransportError("Request failed after 3 attempts")


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
            try:
                params.pop("parse_mode", None)
                telegram_request("sendMessage", params)
            except (httpx.TransportError, httpx.HTTPStatusError) as e:
                logger.error(f"Fallback send failed: {e}")
                raise


def send_photo(chat_id: int, photo_path: str, caption: str = "", reply_to: int | None = None):
    """Send a photo to a Telegram chat via multipart upload."""
    url = f"{TELEGRAM_API}/sendPhoto"
    try:
        with open(photo_path, "rb") as f:
            data = {"chat_id": str(chat_id)}
            if caption:
                data["caption"] = caption[:1024]
            if reply_to:
                data["reply_to_message_id"] = str(reply_to)
            response = _http_client.post(url, data=data, files={"photo": f})
            response.raise_for_status()
            logger.info(f"Photo sent to chat {chat_id}: {photo_path}")
    except Exception as e:
        logger.error(f"Failed to send photo {photo_path}: {e}")


def send_document(chat_id: int, doc_path: str, caption: str = "", reply_to: int | None = None):
    """Send a document to a Telegram chat via multipart upload."""
    url = f"{TELEGRAM_API}/sendDocument"
    try:
        with open(doc_path, "rb") as f:
            data = {"chat_id": str(chat_id)}
            if caption:
                data["caption"] = caption[:1024]
            if reply_to:
                data["reply_to_message_id"] = str(reply_to)
            response = _http_client.post(url, data=data, files={"document": f})
            response.raise_for_status()
            logger.info(f"Document sent to chat {chat_id}: {doc_path}")
    except Exception as e:
        logger.error(f"Failed to send document {doc_path}: {e}")


# File extensions that can be sent as photos vs documents
_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
_DOC_EXTS = {".pdf", ".html", ".csv", ".txt", ".json"}
_ALL_FILE_EXTS = _IMAGE_EXTS | _DOC_EXTS

# Regex to find absolute file paths in response text
_FILE_PATH_RE = re.compile(
    r"(/(?:tmp|home)[^\s\"'`\])\*]+\.(?:png|jpg|jpeg|gif|webp|pdf|html|csv))"
)


def extract_and_send_files(chat_id: int, text: str, reply_to: int | None = None) -> list[str]:
    """Scan response text for file paths, send matching files via Telegram.

    Returns list of file paths that were successfully sent.
    """
    sent = []
    matches = _FILE_PATH_RE.findall(text)
    for path_str in dict.fromkeys(matches):  # deduplicate, preserve order
        path = Path(path_str)
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext in _IMAGE_EXTS:
            send_photo(chat_id, str(path), caption=path.name, reply_to=reply_to)
            sent.append(path_str)
        elif ext in _DOC_EXTS:
            send_document(chat_id, str(path), caption=path.name, reply_to=reply_to)
            sent.append(path_str)
    return sent


# --- Inbound File Handling ---

INBOUND_DIR = Path("/tmp/telegram-inbound")


def download_telegram_file(file_id: str, suffix: str = ".jpg") -> str | None:
    """Download a file from Telegram servers and return the local path."""
    try:
        INBOUND_DIR.mkdir(parents=True, exist_ok=True)
        result = telegram_request("getFile", {"file_id": file_id})
        file_path = result.get("result", {}).get("file_path", "")
        if not file_path:
            return None
        download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        response = _http_client.get(download_url)
        response.raise_for_status()
        # Use original extension if available, fall back to suffix
        ext = Path(file_path).suffix or suffix
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        local_path = INBOUND_DIR / f"telegram-{ts}{ext}"
        local_path.write_bytes(response.content)
        logger.info(f"Downloaded inbound file: {local_path} ({len(response.content)} bytes)")
        return str(local_path)
    except Exception as e:
        logger.error(f"Failed to download telegram file {file_id}: {e}")
        return None


def extract_inbound_files(message: dict) -> tuple[list[str], str]:
    """Extract files from a Telegram message. Returns (file_paths, caption)."""
    file_paths = []
    caption = message.get("caption", "").strip()

    # Photos — Telegram sends multiple sizes, grab the largest (last)
    if "photo" in message:
        photos = message["photo"]
        if photos:
            largest = photos[-1]
            path = download_telegram_file(largest["file_id"], ".jpg")
            if path:
                file_paths.append(path)

    # Documents (PDFs, images sent as files, etc.)
    if "document" in message:
        doc = message["document"]
        file_name = doc.get("file_name", "file")
        ext = Path(file_name).suffix or ".bin"
        path = download_telegram_file(doc["file_id"], ext)
        if path:
            file_paths.append(path)

    return file_paths, caption


def handle_builtin_command(chat_id: int, command: str) -> bool | str:
    """Handle built-in commands. Returns True if handled, 'restart' to signal restart."""
    if command == "/status":
        try:
            now_file = Path(MEGA_OS_PATH) / "active" / "now.md"
            text = now_file.read_text() if now_file.exists() else "No active/now.md found."
        except OSError as e:
            text = f"Error reading status: {e}"
        try:
            send_message(chat_id, text)
        except Exception as e:
            logger.error(f"Failed to send /status response: {e}")
        return True

    if command == "/priorities":
        try:
            prio_file = Path(MEGA_OS_PATH) / "active" / "priorities.md"
            text = prio_file.read_text() if prio_file.exists() else "No active/priorities.md found."
        except OSError as e:
            text = f"Error reading priorities: {e}"
        try:
            send_message(chat_id, text)
        except Exception as e:
            logger.error(f"Failed to send /priorities response: {e}")
        return True

    if command == "/reset":
        key = str(chat_id)
        if key in chat_sessions:
            del chat_sessions[key]
            try:
                save_sessions(chat_sessions)
            except Exception as e:
                logger.error(f"Failed to save sessions on reset: {e}")
        try:
            send_message(chat_id, "Session cleared. Next message starts a fresh conversation.")
        except Exception as e:
            logger.error(f"Failed to send /reset response: {e}")
        return True

    if command == "/restart":
        try:
            send_message(chat_id, "Restarting bridge... (you'll need to re-authenticate)")
        except Exception:
            pass
        logger.info(f"Restart requested by chat {chat_id}")
        return "restart"  # Signal main loop to exit after acknowledging offset

    if command == "/help":
        try:
            send_message(
                chat_id,
                "Commands:\n"
                "/status — Show current focus\n"
                "/priorities — Show priority list\n"
                "/reset — Clear context and start fresh\n"
                "/restart — Restart the bridge (requires re-auth)\n"
                "/help — Show this help\n\n"
                "Sessions persist automatically — follow-up messages continue the conversation.\n"
                "You can send photos and documents — they'll be downloaded and passed to Claude.\n"
                "Timeout: 10 minutes per request.",
            )
        except Exception as e:
            logger.error(f"Failed to send /help response: {e}")
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
        # Prepend file-saving instruction so screenshots/PDFs land on disk
        # and the bridge can detect paths and send files via Telegram
        prefixed = (
            "[System: When using browser_take_screenshot, ALWAYS provide a "
            "filename parameter (e.g. screenshot-{timestamp}.png). Save to "
            "/tmp/playwright-screenshots/. Include the full file path in your "
            "response so it can be delivered. Same for playwright_save_as_pdf.]\n\n"
            + message
        )
        cmd.append(prefixed)

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
    _init_client()
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
    poll_backoff = 5  # seconds, doubles on failure, caps at 120

    while True:
        try:
            updates = get_updates(offset)
            poll_backoff = 5
        except Exception as e:
            logger.error(f"Polling error: {e} — retrying in {poll_backoff}s")
            time.sleep(poll_backoff)
            poll_backoff = min(poll_backoff * 2, 120)
            continue

        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue

            # Determine if this message has content we can process
            has_text = "text" in message
            has_files = "photo" in message or "document" in message
            if not has_text and not has_files:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "").strip()
            msg_id = message["message_id"]
            user = message.get("from", {}).get("username", "unknown")

            # Handle inbound files (photos, documents)
            inbound_paths = []
            if has_files:
                inbound_paths, caption = extract_inbound_files(message)
                if not text and caption:
                    text = caption
                if inbound_paths:
                    file_refs = "\n".join(
                        f"[Attached file: {p}]" for p in inbound_paths
                    )
                    if text:
                        text = f"{text}\n\n{file_refs}"
                    else:
                        text = f"The user sent these files. Please view and acknowledge them.\n\n{file_refs}"

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
            if text.startswith("/"):
                result = handle_builtin_command(chat_id, text.split()[0])
                if result == "restart":
                    # Acknowledge offset so /restart doesn't replay after restart
                    try:
                        telegram_request("getUpdates", {"offset": offset, "timeout": 0})
                    except Exception:
                        pass
                    sys.exit(0)  # systemd restarts the process
                if result:
                    continue

            # Send "thinking" indicator
            try:
                telegram_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})
                send_message(chat_id, "Thinking...")
            except Exception:
                pass

            # Invoke Claude (always resumes session for conversational continuity)
            response = invoke_claude(text, chat_id, use_session=True)
            try:
                # Send any files (screenshots, PDFs) referenced in the response
                sent_files = extract_and_send_files(chat_id, response, reply_to=msg_id)
                if sent_files:
                    logger.info(f"Sent {len(sent_files)} file(s) to chat {chat_id}")

                send_message(chat_id, response, reply_to=msg_id)
                log_message(chat_id, "bot", "out", response)
                logger.info(f"Response sent to chat {chat_id} ({len(response)} chars)")
            except Exception as e:
                logger.error(f"Failed to deliver response to chat {chat_id}: {e}")
                log_message(chat_id, "bot", "out_failed", response)


if __name__ == "__main__":
    main()
