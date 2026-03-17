#!/bin/bash
#
# test-merge-safety.sh — Verify that merge=ours protects user-data directories.
#
# Creates a temporary git repo simulating user + upstream, modifies user-data
# files on both sides, merges, and confirms user modifications are preserved.
#
# Usage:
#   ./test-merge-safety.sh
#
# Exit codes:
#   0 — All tests passed
#   1 — One or more tests failed
#

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

PASS=0
FAIL=0

report() {
  local status="$1"
  local test_name="$2"
  if [[ "$status" == "PASS" ]]; then
    echo -e "  ${GREEN}PASS${NC} ${test_name}"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}FAIL${NC} ${test_name}"
    FAIL=$((FAIL + 1))
  fi
}

echo -e "${CYAN}=== Merge Safety Tests ===${NC}"
echo ""

# --- Setup: create "upstream" repo ---
UPSTREAM="$TMPDIR/upstream"
mkdir -p "$UPSTREAM"
cd "$UPSTREAM"
git init -q
git config user.name "test" && git config user.email "test@test.com"

# Create protected directories with .gitattributes
PROTECTED_DIRS=("active" "business" "products" "drafts" "deliverables" "archive" "core/history" "core/indexes" "style-samples")

for dir in "${PROTECTED_DIRS[@]}"; do
  mkdir -p "$dir"
  echo "* merge=ours" > "$dir/.gitattributes"
  echo "upstream stub content" > "$dir/test-file.md"
done

# Create root .gitattributes
cat > .gitattributes << 'ATTR'
core/standards/writing-style.md    merge=ours
.claude/CLAUDE.local.md            merge=ours
ATTR

# Create a framework file (should update normally)
mkdir -p .claude/agents
echo "framework v1" > .claude/agents/test-agent.md

# Create VERSION
echo "2026.03.1" > VERSION

git add -A && git commit -q -m "initial"

# --- Setup: clone as "user" repo ---
USER_REPO="$TMPDIR/user"
git clone -q "$UPSTREAM" "$USER_REPO"
cd "$USER_REPO"
git config user.name "test" && git config user.email "test@test.com"

# Configure merge driver (critical — without this, merge=ours is ignored)
git config merge.ours.driver true

# User customizes their files
for dir in "${PROTECTED_DIRS[@]}"; do
  echo "user's important data for $dir" > "$dir/test-file.md"
done
git add -A && git commit -q -m "user customizations"

# --- Upstream makes changes to same files ---
cd "$UPSTREAM"
for dir in "${PROTECTED_DIRS[@]}"; do
  echo "upstream changed this in $dir" > "$dir/test-file.md"
done
echo "framework v2" > .claude/agents/test-agent.md
echo "2026.03.2" > VERSION
git add -A && git commit -q -m "upstream update"

# --- User pulls upstream ---
cd "$USER_REPO"
git fetch -q origin
git merge -q origin/master --no-edit 2>/dev/null

# --- Verify: protected files kept user's version ---
echo -e "${CYAN}Protected directory tests:${NC}"
for dir in "${PROTECTED_DIRS[@]}"; do
  content=$(cat "$dir/test-file.md")
  if [[ "$content" == "user's important data for $dir" ]]; then
    report "PASS" "$dir/test-file.md preserved"
  else
    report "FAIL" "$dir/test-file.md was overwritten (got: $content)"
  fi
done

# --- Verify: framework file WAS updated ---
echo ""
echo -e "${CYAN}Framework file tests:${NC}"
framework_content=$(cat .claude/agents/test-agent.md)
if [[ "$framework_content" == "framework v2" ]]; then
  report "PASS" "framework file updated from upstream"
else
  report "FAIL" "framework file NOT updated (got: $framework_content)"
fi

version_content=$(cat VERSION)
if [[ "$version_content" == "2026.03.2" ]]; then
  report "PASS" "VERSION updated from upstream"
else
  report "FAIL" "VERSION NOT updated (got: $version_content)"
fi

# --- Verify: merge driver not configured = no protection ---
echo ""
echo -e "${CYAN}Missing merge driver test:${NC}"
UNPROTECTED="$TMPDIR/unprotected"
git clone -q "$UPSTREAM" "$UNPROTECTED"
cd "$UNPROTECTED"
git config user.name "test" && git config user.email "test@test.com"
# Deliberately NOT setting merge.ours.driver
echo "user data that should be protected" > active/test-file.md
git add -A && git commit -q -m "user data"

# Reset upstream to make a new change
cd "$UPSTREAM"
echo "upstream overwrites without driver" > active/test-file.md
git add -A && git commit -q -m "upstream change 2"

cd "$UNPROTECTED"
git fetch -q origin
git merge -q origin/master --no-edit 2>/dev/null || true
unprotected_content=$(cat active/test-file.md 2>/dev/null)
if [[ "$unprotected_content" != "user data that should be protected" ]]; then
  report "PASS" "without merge driver, user data is NOT protected (expected)"
else
  report "FAIL" "without merge driver, user data was still protected (unexpected)"
fi

# --- Summary ---
echo ""
TOTAL=$((PASS + FAIL))
echo -e "${CYAN}Results: ${PASS}/${TOTAL} passed${NC}"
if [[ $FAIL -gt 0 ]]; then
  echo -e "${RED}${FAIL} test(s) failed${NC}"
  exit 1
else
  echo -e "${GREEN}All tests passed${NC}"
  exit 0
fi
