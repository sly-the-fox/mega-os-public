#!/bin/bash
#
# sync-to-public.sh — Compare personal mega-os with public repo
# and selectively sync safe files (agents, core, skills, engineering, docs).
#
# Usage:
#   ./sync-to-public.sh          # Show diff only
#   ./sync-to-public.sh --sync   # Sync changed files and commit
#

PRIVATE="/home/abzu/mega-os"
PUBLIC="/home/abzu/mega-os-public"

# Files/dirs safe to sync (no personal data)
SAFE_PATHS=(
  "CLAUDE.md"
  "AGENTS.md"
  "README.md"
  "GETTING_STARTED.md"
  ".gitignore"
  ".claude/agents/"
  ".claude/skills/"
  ".claude/settings.json"
  "core/standards/"
  "core/templates/"
  "core/indexes/canonical-files.md"
  "engineering/scripts/telegram-bridge/telegram_bridge.py"
  "engineering/scripts/telegram-bridge/README.md"
  "engineering/scripts/telegram-bridge/requirements.txt"
  "engineering/scripts/telegram-bridge/.env.example"
  "engineering/scripts/md-to-polished.py"
)

# Files to SKIP during sync (private data)
SKIP_FILES=(
  "core/standards/writing-style.md"
)

# Files/dirs to NEVER sync (personal data)
# products/, business/, active/, core/history/, .env, sessions.json, memory/

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

changed_files=()

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

      if [[ ! -f "$dst_file" ]]; then
        echo -e "${GREEN}  NEW${NC}  ${path}${rel}"
        changed_files+=("${path}${rel}")
      elif ! diff -q "$file" "$dst_file" &>/dev/null; then
        echo -e "${YELLOW}  MOD${NC}  ${path}${rel}"
        changed_files+=("${path}${rel}")
      fi
    done < <(find "$src" -type f -print0 2>/dev/null)
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
    cp "$src" "$dst"
    echo -e "  ${GREEN}copied${NC} ${file}"
  done

  echo ""
  cd "$PUBLIC" || exit 1
  git add -A
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
