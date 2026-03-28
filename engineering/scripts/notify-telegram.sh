#!/usr/bin/env bash
# notify-telegram.sh — Send a Telegram notification after a cron job completes.
#
# Usage:
#   notify-telegram.sh <job-name> <exit-code> [log-file]
#
# Examples:
#   # Inline after a cron command:
#   3 7 * * * cd ~/mega-os && claude -p "..." > /tmp/job.log 2>&1; /home/abzu/mega-os/engineering/scripts/notify-telegram.sh "Content Gen" $? /tmp/job.log
#
#   # Or wrap a command:
#   notify-telegram.sh "Daily Scan" 0
#
# Reads TELEGRAM_BOT_TOKEN and NOTIFY_CHAT_ID from the .env file
# in engineering/scripts/telegram-bridge/.env

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/telegram-bridge/.env"

# Load .env
if [[ -f "$ENV_FILE" ]]; then
    # shellcheck disable=SC1090
    set -a
    while IFS='=' read -r key value; do
        [[ -z "$key" || "$key" == \#* ]] && continue
        key="${key// /}"
        value="${value// /}"
        export "$key"="$value"
    done < "$ENV_FILE"
    set +a
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="${NOTIFY_CHAT_ID:-${ALLOWED_CHAT_IDS%%,*}}"  # Use first allowed chat ID as default

if [[ -z "$BOT_TOKEN" || -z "$CHAT_ID" ]]; then
    echo "SKIP: TELEGRAM_BOT_TOKEN or NOTIFY_CHAT_ID/ALLOWED_CHAT_IDS not set" >&2
    exit 2  # Exit 2 = skipped (not configured), distinct from exit 1 (failed)
fi

JOB_NAME="${1:?Usage: notify-telegram.sh <job-name> <exit-code> [log-file]}"
EXIT_CODE="${2:?Usage: notify-telegram.sh <job-name> <exit-code> [log-file]}"
LOG_FILE="${3:-}"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"

# Build message
if [[ "$EXIT_CODE" -eq 0 ]]; then
    STATUS="completed"
    ICON="[OK]"
else
    STATUS="FAILED (exit $EXIT_CODE)"
    ICON="[FAIL]"
fi

MSG="$ICON Cron: $JOB_NAME
Status: $STATUS
Time: $TIMESTAMP"

# Append log tail if log file provided and exists
if [[ -n "$LOG_FILE" && -f "$LOG_FILE" ]]; then
    LOG_SIZE=$(wc -c < "$LOG_FILE")
    if [[ "$LOG_SIZE" -gt 0 ]]; then
        # Get last 20 lines, trim to keep message under Telegram's 4096 limit
        LOG_TAIL=$(tail -20 "$LOG_FILE" | head -c 3000)
        MSG="$MSG

--- Log tail ---
$LOG_TAIL"
    fi
fi

# Send via Telegram Bot API (with single retry on failure)
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HEALTH_FILE="$REPO_ROOT/active/cron-health.md"

send_telegram() {
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MSG" \
        -d parse_mode="" \
        > /dev/null 2>&1
}

if ! send_telegram; then
    echo "WARN: Telegram notification failed, retrying in 30s..." >&2
    sleep 30
    if ! send_telegram; then
        echo "ERROR: Telegram notification failed after retry" >&2
        # Fallback: log to persistent cron-health file (survives reboots, read by /goodmorning)
        echo "| $(date '+%Y-%m-%d %H:%M') | NOTIFICATION_FAILED | $JOB_NAME (exit: $EXIT_CODE) | Telegram unreachable after retry |" >> "$HEALTH_FILE" 2>/dev/null
        exit 1
    fi
fi
