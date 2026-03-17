#!/bin/bash
#
# apply-update.sh — Selective framework updater for ZIP-based installations.
#
# Downloads the latest Mega-OS release, diffs framework files only
# (using sync-manifest.json include list), and copies only framework files
# while preserving user-data directories.
#
# Usage:
#   ./apply-update.sh
#

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MANIFEST="${REPO_ROOT}/engineering/sync-manifest.json"
LOCAL_VERSION_FILE="${REPO_ROOT}/VERSION"
RELEASE_URL="https://github.com/sly-the-fox/mega-os-public/archive/refs/heads/master.zip"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# User-data directories that must NEVER be overwritten
NEVER_OVERWRITE=("active/" "business/" "products/" "drafts/" "deliverables/" "archive/" "core/history/" "core/indexes/" "style-samples/" ".claude/CLAUDE.local.md" ".claude/projects/")

is_user_data() {
  local file="$1"
  for deny in "${NEVER_OVERWRITE[@]}"; do
    if [[ "$deny" == */ ]] && [[ "$file" == "$deny"* ]]; then
      return 0
    fi
    if [[ "$file" == "$deny" ]]; then
      return 0
    fi
  done
  return 1
}

# Check prerequisites
if ! command -v curl &>/dev/null; then
  echo -e "${RED}curl is required but not installed.${NC}"
  exit 1
fi

if ! command -v unzip &>/dev/null; then
  echo -e "${RED}unzip is required but not installed.${NC}"
  exit 1
fi

if ! command -v jq &>/dev/null; then
  echo -e "${RED}jq is required but not installed.${NC}"
  exit 1
fi

# Read local version
LOCAL_VERSION="unknown"
if [[ -f "$LOCAL_VERSION_FILE" ]]; then
  LOCAL_VERSION=$(cat "$LOCAL_VERSION_FILE" | tr -d '[:space:]')
fi
echo -e "${CYAN}Current version:${NC} ${LOCAL_VERSION}"

# Download latest release
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo -e "${CYAN}Downloading latest Mega-OS release...${NC}"
if ! curl -sfL "$RELEASE_URL" -o "$TMPDIR/release.zip"; then
  echo -e "${RED}Failed to download. Check your internet connection.${NC}"
  exit 1
fi

echo -e "${CYAN}Extracting...${NC}"
unzip -q "$TMPDIR/release.zip" -d "$TMPDIR"

# Find the extracted directory (GitHub adds a suffix)
EXTRACTED=$(find "$TMPDIR" -maxdepth 1 -type d -name "mega-os-public-*" | head -1)
if [[ -z "$EXTRACTED" ]]; then
  echo -e "${RED}Could not find extracted directory.${NC}"
  exit 1
fi

# Check remote version
REMOTE_VERSION="unknown"
if [[ -f "$EXTRACTED/VERSION" ]]; then
  REMOTE_VERSION=$(cat "$EXTRACTED/VERSION" | tr -d '[:space:]')
fi
echo -e "${CYAN}Latest version:${NC}  ${REMOTE_VERSION}"

if [[ "$LOCAL_VERSION" == "$REMOTE_VERSION" ]]; then
  echo -e "${GREEN}You're already up to date.${NC}"
  exit 0
fi

echo ""

# Read manifest include lists
if [[ ! -f "$MANIFEST" ]]; then
  echo -e "${YELLOW}No sync-manifest.json found. Using remote manifest.${NC}"
  MANIFEST="$EXTRACTED/engineering/sync-manifest.json"
fi

mapfile -t INCLUDE_DIRS < <(jq -r '.include_dirs[]' "$MANIFEST")
mapfile -t INCLUDE_FILES < <(jq -r '.include_files[]' "$MANIFEST")

# Build list of framework files from the downloaded release
echo -e "${CYAN}Comparing framework files...${NC}"
CHANGES=()
NEW=()

for dir in "${INCLUDE_DIRS[@]}"; do
  src_dir="${EXTRACTED}/${dir}"
  [[ -d "$src_dir" ]] || continue
  while IFS= read -r -d '' file; do
    rel="${file#$EXTRACTED/}"
    is_user_data "$rel" && continue
    local_file="${REPO_ROOT}/${rel}"
    if [[ ! -f "$local_file" ]]; then
      NEW+=("$rel")
    elif ! diff -q "$file" "$local_file" &>/dev/null; then
      CHANGES+=("$rel")
    fi
  done < <(find "$src_dir" -type f -print0 2>/dev/null)
done

for f in "${INCLUDE_FILES[@]}"; do
  is_user_data "$f" && continue
  src_file="${EXTRACTED}/${f}"
  local_file="${REPO_ROOT}/${f}"
  [[ -f "$src_file" ]] || continue
  if [[ ! -f "$local_file" ]]; then
    NEW+=("$f")
  elif ! diff -q "$src_file" "$local_file" &>/dev/null; then
    CHANGES+=("$f")
  fi
done

if [[ ${#CHANGES[@]} -eq 0 ]] && [[ ${#NEW[@]} -eq 0 ]]; then
  echo -e "${GREEN}No framework file changes detected.${NC}"
  # Still update VERSION
  cp "$EXTRACTED/VERSION" "$LOCAL_VERSION_FILE" 2>/dev/null
  exit 0
fi

echo ""
if [[ ${#NEW[@]} -gt 0 ]]; then
  echo -e "${GREEN}New files:${NC}"
  for f in "${NEW[@]}"; do
    echo "  + $f"
  done
fi
if [[ ${#CHANGES[@]} -gt 0 ]]; then
  echo -e "${YELLOW}Modified files:${NC}"
  for f in "${CHANGES[@]}"; do
    echo "  ~ $f"
  done
fi
echo ""
echo -e "Total: ${GREEN}${#NEW[@]} new${NC}, ${YELLOW}${#CHANGES[@]} modified${NC}"
echo ""

read -p "Apply these updates? [y/N]: " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Update cancelled."
  exit 0
fi

# Apply changes
echo -e "${CYAN}Applying updates...${NC}"
APPLIED=0

for f in "${NEW[@]}" "${CHANGES[@]}"; do
  src="${EXTRACTED}/${f}"
  dst="${REPO_ROOT}/${f}"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo -e "  ${GREEN}updated${NC} $f"
  APPLIED=$((APPLIED + 1))
done

# Update VERSION
cp "$EXTRACTED/VERSION" "$LOCAL_VERSION_FILE" 2>/dev/null

echo ""
echo -e "${GREEN}Applied ${APPLIED} file(s). Version updated to ${REMOTE_VERSION}.${NC}"
echo ""
echo "Your personal data (active/, business/, products/, etc.) was not touched."
echo "Review the changes and commit when ready."
