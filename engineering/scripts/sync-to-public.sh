#!/bin/bash
#
# sync-to-public.sh — Compare personal mega-os with public repo
# and selectively sync safe files (agents, core, skills, engineering, docs).
#
# Usage:
#   ./sync-to-public.sh          # Show diff only
#   ./sync-to-public.sh --sync   # Sync changed files and commit
#

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRIVATE="${MEGA_OS_PATH:-$REPO_ROOT}"
PUBLIC="${MEGA_OS_PUBLIC_PATH:-$(dirname "$PRIVATE")/mega-os-public}"

# Files/dirs safe to sync (no personal data)
SAFE_PATHS=(
  "CLAUDE.md"
  "AGENTS.md"
  "README.md"
  "GETTING_STARTED.md"
  # LICENSE is intentionally excluded — private has personal copyright,
  # public has corporate (AEQUILIBRIS GROUP Limited). Do not sync.
  ".gitignore"
  ".freshstate.yml"
  ".claude/agents/"
  ".claude/skills/"
  ".claude/hooks/"
  ".claude/settings.json"
  "core/standards/"
  "core/templates/"
  "engineering/scripts/sync-to-public.sh"
  "engineering/scripts/archive-report.sh"
  "engineering/scripts/archive-briefings.py"
  "engineering/scripts/build-active-index.py"
  "engineering/scripts/check-index-integrity.sh"
  "engineering/scripts/cron-health-check.py"
  "engineering/scripts/draw-mermaid.sh"
  "engineering/scripts/fetch-metrics.py"
  "engineering/scripts/freshstate-wrapper.sh"
  "engineering/scripts/notify-telegram.sh"
  "engineering/scripts/puppeteer-config.json"
  "engineering/scripts/md-to-polished.py"
  "engineering/scripts/telegram-bridge/telegram_bridge.py"
  "engineering/scripts/telegram-bridge/README.md"
  "engineering/scripts/telegram-bridge/requirements.txt"
  "engineering/scripts/telegram-bridge/.env.example"
  "engineering/scripts/telegram-bridge/chat-log.jsonl.example"
)

# Files to SKIP during sync (contain personal data or private customization)
SKIP_FILES=(
  "core/standards/writing-style.md"
  ".claude/skills/news-briefing/SKILL.md"
  ".claude/skills/improvement-audit/SKILL.md"
  ".claude/skills/reddit-comments/reddit-comments.md"
)

# Files/dirs to NEVER sync (personal data)
# products/, business/, active/, core/history/, .env, sessions.json, memory/

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

changed_files=()
synced_files=()

echo ""
echo -e "${CYAN}=== Mega-OS Sync Check ===${NC}"
echo -e "Private: ${PRIVATE}"
echo -e "Public:  ${PUBLIC}"
echo ""

for path in "${SAFE_PATHS[@]}"; do
  src="${PRIVATE}/${path}"
  dst="${PUBLIC}/${path}"

  # Handle directories
  if [[ -d "$src" ]]; then
    # Use -follow to traverse symlinks, but track symlinks separately
    while IFS= read -r -d '' file; do
      rel="${file#$src}"
      dst_file="${dst}${rel}"

      # Skip private files
      skip=false
      for skip_file in "${SKIP_FILES[@]}"; do
        if [[ "${path}${rel}" == "$skip_file" ]]; then
          skip=true
          break
        fi
      done
      [[ "$skip" == "true" ]] && continue

      if [[ ! -f "$dst_file" ]] && [[ ! -L "$dst_file" ]]; then
        echo -e "${GREEN}  NEW${NC}  ${path}${rel}"
        changed_files+=("${path}${rel}")
      elif ! diff -q "$file" "$dst_file" &>/dev/null; then
        echo -e "${YELLOW}  MOD${NC}  ${path}${rel}"
        changed_files+=("${path}${rel}")
      fi
    done < <(find "$src" -type f -print0 2>/dev/null)

    # Also find symlinks in the source directory
    while IFS= read -r -d '' link; do
      rel="${link#$src}"
      dst_link="${dst}${rel}"
      link_target="$(readlink "$link")"

      # Skip private files
      skip=false
      for skip_file in "${SKIP_FILES[@]}"; do
        if [[ "${path}${rel}" == "$skip_file" ]]; then
          skip=true
          break
        fi
      done
      [[ "$skip" == "true" ]] && continue

      if [[ ! -L "$dst_link" ]]; then
        # Destination is not a symlink (either missing or a regular file)
        echo -e "${GREEN}  SYM${NC}  ${path}${rel} -> ${link_target}"
        changed_files+=("${path}${rel}")
      elif [[ "$(readlink "$dst_link")" != "$link_target" ]]; then
        echo -e "${YELLOW}  SYM${NC}  ${path}${rel} -> ${link_target}"
        changed_files+=("${path}${rel}")
      fi
    done < <(find "$src" -type l -print0 2>/dev/null)
  # Handle single files
  elif [[ -f "$src" ]]; then
    if [[ ! -f "$dst" ]]; then
      echo -e "${GREEN}  NEW${NC}  ${path}"
      changed_files+=("$path")
    elif ! diff -q "$src" "$dst" &>/dev/null; then
      echo -e "${YELLOW}  MOD${NC}  ${path}"
      changed_files+=("$path")
    fi
  fi
done

echo ""

if [[ ${#changed_files[@]} -eq 0 ]]; then
  echo -e "${GREEN}Public repo is up to date. Nothing to sync.${NC}"
  exit 0
fi

echo -e "${CYAN}${#changed_files[@]} file(s) differ.${NC}"
echo ""

# If --sync flag, copy and commit
if [[ "$1" == "--sync" ]]; then
  echo -e "${CYAN}Syncing files...${NC}"
  for file in "${changed_files[@]}"; do
    src="${PRIVATE}/${file}"
    dst="${PUBLIC}/${file}"
    mkdir -p "$(dirname "$dst")"

    if [[ -L "$src" ]]; then
      # Preserve symlinks
      link_target="$(readlink "$src")"
      rm -f "$dst"
      ln -s "$link_target" "$dst"
      echo -e "  ${GREEN}linked${NC} ${file} -> ${link_target}"
    else
      cp "$src" "$dst"
      echo -e "  ${GREEN}copied${NC} ${file}"
    fi
    synced_files+=("$file")
  done

  echo ""
  cd "$PUBLIC" || exit 1
  # Stage only the files we synced, not everything in the repo
  for file in "${synced_files[@]}"; do
    git add "$file"
  done
  echo -e "${CYAN}Staged changes:${NC}"
  git status -s
  echo ""
  read -p "Commit message (or empty to skip): " msg
  if [[ -n "$msg" ]]; then
    git commit -m "$msg"
    read -p "Push to remote? [y/N]: " push
    if [[ "$push" =~ ^[Yy]$ ]]; then
      git push
    fi
  fi
else
  echo -e "Run ${CYAN}./sync-to-public.sh --sync${NC} to copy these files and commit."
fi
