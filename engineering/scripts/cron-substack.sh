#!/usr/bin/env bash
# Weekly Substack article generation (runs Tuesday, posts Thursday)
# Full Writer → Editor → Polisher pipeline via /write-content
set -euo pipefail

REPO="${MEGA_OS_HOME:-$HOME/mega-os}"
cd "$REPO"
LOG=/tmp/mega-os-substack.log

CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 \
  timeout 1200 "$CLAUDE_BIN" -p \
  "Read business/marketing/content-calendar.md and find this week's Substack article. Run /write-content with the title from the calendar. The full Writer → Editor → Polisher pipeline must run. Draft goes to drafts/, PDF and DOCX deliverables go to deliverables/. Update business/marketing/channel-tracker.md with the draft status. Send a Telegram notification with the article title and deliverable paths." \
  --permission-mode auto > "$LOG" 2>&1
SUB_EXIT=$?

echo "Exit: $SUB_EXIT at $(date)" >> "$LOG"

# Staleness check: was a PDF produced today?
LATEST_PDF=$(ls -t deliverables/*.pdf 2>/dev/null | head -1)
if [ -n "$LATEST_PDF" ] && [ "$(date -r "$LATEST_PDF" +%F 2>/dev/null)" = "$(date +%F)" ]; then
  echo "PDF deliverable: UPDATED today ($LATEST_PDF)" >> "$LOG"
else
  echo "PDF deliverable: NOT updated (stale)" >> "$LOG"
fi

"$REPO/engineering/scripts/notify-telegram.sh" "Substack Article" $SUB_EXIT "$LOG"
"$REPO/engineering/scripts/cron-autocommit.sh" --job substack >> /tmp/mega-os-autocommit.log 2>&1
