#!/usr/bin/env bash
# cron-autocommit.sh — Auto-commit and push known cron output files.
#
# Usage:
#   cron-autocommit.sh --daily           # Batch commit all daily cron outputs
#   cron-autocommit.sh --job <job-name>  # Commit outputs for a specific job
#
# Safety: Only stages whitelisted paths. Never runs 'git add .' or 'git add -A'.
# Exit codes: 0 = success or no changes, 1 = error

set -euo pipefail

REPO="/home/abzu/mega-os"
cd "$REPO"

TODAY=$(date +%F)

log() { echo "[autocommit] $(date '+%H:%M:%S') $*"; }

# --- Lock file check with exponential backoff (~61s total) ---
wait_for_lock() {
    local lockfile="$REPO/.git/index.lock"
    local delays=(1 2 4 8 16 30)
    for delay in "${delays[@]}"; do
        [[ ! -f "$lockfile" ]] && return 0
        log "WARN: .git/index.lock exists, waiting ${delay}s..."
        sleep "$delay"
    done
    if [[ -f "$lockfile" ]]; then
        log "ERROR: .git/index.lock still present after ~61s. Aborting."
        return 1
    fi
}

# --- Push any unpushed commits from a previous failed push ---
push_pending() {
    local unpushed
    unpushed=$(git log origin/master..HEAD --oneline 2>/dev/null) || true
    if [[ -n "$unpushed" ]]; then
        log "Found unpushed commits, pushing first..."
        if ! git push origin master 2>&1; then
            log "WARN: Push failed, trying pull --rebase..."
            git pull --rebase origin master 2>&1 || true
            git push origin master 2>&1 || log "WARN: Push still failing. Continuing."
        fi
    fi
}

# --- Gather changed files for a list of paths/dirs ---
# Args: file paths or directory paths (dirs end with /)
# Outputs: deduplicated list of changed files, one per line
gather_changes() {
    for entry in "$@"; do
        if [[ "$entry" == */ ]]; then
            # Directory — check for modified, new, and deleted files
            [[ -d "$entry" ]] || continue
            git diff --name-only HEAD -- "$entry" 2>/dev/null || true
            git ls-files --others --exclude-standard -- "$entry" 2>/dev/null || true
            git diff --name-only --diff-filter=D HEAD -- "$entry" 2>/dev/null || true
        else
            # Single file — check for modification, untracked, or deletion
            git diff --name-only HEAD -- "$entry" 2>/dev/null || true
            git ls-files --others --exclude-standard -- "$entry" 2>/dev/null || true
            git diff --name-only --diff-filter=D HEAD -- "$entry" 2>/dev/null || true
        fi
    done | sort -u | grep -v '^$' || true
}

# --- Daily whitelist ---
daily_whitelist() {
    gather_changes \
        active/dream-report.md \
        active/improvement-audit.md \
        active/news-briefing.md \
        active/news-briefing-state.md \
        active/daily-digest.md \
        active/freshstate-report.md \
        active/index.json \
        active/historian-digest.md \
        active/week-calendar.md \
        active/cron-health.md \
        active/changelog.jsonl \
        business/marketing/channel-tracker.md \
        business/marketing/adoption-metrics.md \
        business/network/contacts.json \
        business/sales/pipeline.json \
        core/indexes/cross-references.json \
        archive/index.json \
        deliverables/news/ \
        drafts/social/ \
        archive/news/ \
        archive/reports/
}

daily_allowed_prefixes() {
    echo "active/ business/marketing/ business/network/contacts.json business/sales/pipeline.json core/indexes/cross-references.json archive/ deliverables/news/ drafts/social/"
}

# --- Per-job whitelists ---
job_whitelist() {
    local job="$1"
    case "$job" in
        substack)
            gather_changes drafts/ deliverables/ business/marketing/channel-tracker.md ;;
        weekly-review)
            gather_changes active/workflow-review.md active/now.md active/priorities.md ;;
        index-maintenance)
            gather_changes core/indexes/ ;;
        workflow-review)
            gather_changes active/workflow-review.md ;;
        revenue-checkin)
            gather_changes business/finance/revenue-tracker.md ;;
        system-evaluation)
            gather_changes active/system-evaluation.md ;;
        competitor-monitor)
            gather_changes business/strategy/ ;;
        *)
            log "ERROR: Unknown job '$job'. Known: substack, weekly-review, index-maintenance, workflow-review, revenue-checkin, system-evaluation, competitor-monitor"
            return 1 ;;
    esac
}

job_allowed_prefixes() {
    local job="$1"
    case "$job" in
        substack)           echo "drafts/ deliverables/ business/marketing/" ;;
        weekly-review)      echo "active/" ;;
        index-maintenance)  echo "core/indexes/" ;;
        workflow-review)    echo "active/" ;;
        revenue-checkin)    echo "business/finance/" ;;
        system-evaluation)  echo "active/" ;;
        competitor-monitor) echo "business/strategy/" ;;
    esac
}

# --- Stage, verify, commit, push ---
do_commit() {
    local mode="$1"
    local job_name="${2:-}"

    # Gather changed files
    local files
    if [[ "$mode" == "daily" ]]; then
        files=$(daily_whitelist)
    else
        files=$(job_whitelist "$job_name")
    fi

    if [[ -z "$files" ]]; then
        log "No changes for $mode${job_name:+ ($job_name)}. Nothing to commit."
        return 0
    fi

    # Stage files individually (never git add . or git add -A)
    local count=0
    local file_list=""
    while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        if [[ -e "$f" ]]; then
            git add -- "$f"
        else
            # File was deleted (e.g., archived briefing moved away)
            git add -u -- "$f" 2>/dev/null || true
        fi
        file_list+="- $f
"
        count=$((count + 1))
    done <<< "$files"

    [[ $count -eq 0 ]] && { log "No files staged."; return 0; }

    # Safety check: verify only allowed prefixes are staged
    local allowed
    if [[ "$mode" == "daily" ]]; then
        allowed=$(daily_allowed_prefixes)
    else
        allowed=$(job_allowed_prefixes "$job_name")
    fi

    while IFS= read -r staged_file; do
        [[ -z "$staged_file" ]] && continue
        local ok=false
        for prefix in $allowed; do
            if [[ "$staged_file" == "$prefix"* ]]; then
                ok=true
                break
            fi
        done
        if [[ "$ok" == false ]]; then
            log "WARN: Unstaging unexpected file: $staged_file"
            git reset HEAD -- "$staged_file" 2>/dev/null || true
            count=$((count - 1))
        fi
    done < <(git diff --cached --name-only)

    [[ $count -le 0 ]] && { log "All files unstaged by safety check."; return 0; }

    # Commit
    local label
    if [[ "$mode" == "daily" ]]; then
        label="daily cron outputs ($TODAY)"
    else
        label="$job_name cron outputs ($TODAY)"
    fi

    git commit -m "$(cat <<EOF
system: $label

Files: $count changed
$file_list
Co-Authored-By: mega-os-cron <noreply@mega-os.local>
EOF
    )"
    log "Committed $count files: $label"

    # Push to origin master
    if git push origin master 2>&1; then
        log "Pushed to origin/master."
    else
        log "WARN: Push failed, trying pull --rebase..."
        if git pull --rebase origin master 2>&1 && git push origin master 2>&1; then
            log "Pushed after rebase."
        else
            log "ERROR: Push failed after rebase. Commit is local only."
            return 1
        fi
    fi
}

# --- Main ---
main() {
    local mode=""
    local job_name=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --daily) mode="daily"; shift ;;
            --job)   mode="job"; job_name="${2:?--job requires a name}"; shift 2 ;;
            *)       log "ERROR: Unknown arg: $1"; exit 1 ;;
        esac
    done

    [[ -z "$mode" ]] && { log "ERROR: Specify --daily or --job <name>"; exit 1; }

    log "Start: mode=$mode${job_name:+, job=$job_name}"

    wait_for_lock
    push_pending
    do_commit "$mode" "$job_name"

    log "Done."
}

main "$@"
