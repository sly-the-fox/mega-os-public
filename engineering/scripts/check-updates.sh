#!/bin/bash
#
# check-updates.sh — Check if a newer version of Mega-OS is available.
#
# For users who downloaded via ZIP (no git). Compares local VERSION
# against the latest VERSION on GitHub.
#
# Usage:
#   ./check-updates.sh
#

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOCAL_VERSION_FILE="${REPO_ROOT}/VERSION"
REMOTE_URL="https://raw.githubusercontent.com/sly-the-fox/mega-os-public/master/VERSION"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Read local version
if [[ ! -f "$LOCAL_VERSION_FILE" ]]; then
  echo -e "${RED}No VERSION file found at ${LOCAL_VERSION_FILE}${NC}"
  echo "Your installation may predate the versioning system."
  echo "Consider re-downloading from https://github.com/sly-the-fox/mega-os-public"
  exit 1
fi

LOCAL_VERSION=$(cat "$LOCAL_VERSION_FILE" | tr -d '[:space:]')
echo -e "${CYAN}Local version:${NC}  ${LOCAL_VERSION}"

# Fetch remote version
REMOTE_VERSION=$(curl -sf "$REMOTE_URL" 2>/dev/null | tr -d '[:space:]')

if [[ -z "$REMOTE_VERSION" ]]; then
  echo -e "${YELLOW}Could not fetch remote version.${NC}"
  echo "Check your internet connection, or visit:"
  echo "  https://github.com/sly-the-fox/mega-os-public/releases"
  exit 1
fi

echo -e "${CYAN}Remote version:${NC} ${REMOTE_VERSION}"
echo ""

if [[ "$LOCAL_VERSION" == "$REMOTE_VERSION" ]]; then
  echo -e "${GREEN}You're up to date.${NC}"
  exit 0
else
  echo -e "${YELLOW}A newer version is available: ${REMOTE_VERSION}${NC}"
  echo ""

  # Check if this is a git repo
  if git -C "$REPO_ROOT" rev-parse --is-inside-work-tree &>/dev/null; then
    echo "You're in a git repo. Run /update in Claude Code or:"
    echo "  git fetch upstream && git merge upstream/master"
  else
    echo "You're using a ZIP download. To update:"
    echo "  1. Download the latest release from https://github.com/sly-the-fox/mega-os-public"
    echo "  2. Run: ./engineering/scripts/apply-update.sh (ships in a future release)"
    echo ""
    echo "For easier updates in the future, consider switching to a git clone:"
    echo "  git clone https://github.com/sly-the-fox/mega-os-public.git mega-os"
  fi
  exit 1
fi
