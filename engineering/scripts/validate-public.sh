#!/usr/bin/env bash
#
# validate-public.sh — Pre-publish gate for mega-os-public.
# Four checks: coverage, privacy, symlinks, bootstrappability.
# Reads rules from engineering/sync-manifest.json.
#
# Exit 0 = all checks pass, Exit 1 = issues found.
#

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRIVATE="${MEGA_OS_PATH:-$REPO_ROOT}"
PUBLIC="${MEGA_OS_PUBLIC_PATH:-$(dirname "$PRIVATE")/mega-os-public}"
MANIFEST="${PRIVATE}/engineering/sync-manifest.json"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

ERRORS=0

# --- Manifest ---

if [[ ! -f "$MANIFEST" ]]; then
  echo -e "${RED}ERROR: Manifest not found at ${MANIFEST}${NC}" >&2
  exit 1
fi

if ! jq empty "$MANIFEST" 2>/dev/null; then
  echo -e "${RED}ERROR: Invalid JSON in ${MANIFEST}${NC}" >&2
  exit 1
fi

mapfile -t INCLUDE_DIRS < <(jq -r '.include_dirs[]' "$MANIFEST")
mapfile -t INCLUDE_FILES < <(jq -r '.include_files[]' "$MANIFEST")
mapfile -t EXCLUDE < <(jq -r '.exclude[]' "$MANIFEST")
mapfile -t EXCLUDE_PATTERNS < <(jq -r '.exclude_patterns // [] | .[]' "$MANIFEST")
mapfile -t PRIVACY_PATTERNS < <(jq -r '.privacy_patterns[]' "$MANIFEST")

is_excluded() {
  local file="$1"
  for excl in "${EXCLUDE[@]}"; do
    if [[ "$file" == "$excl" ]]; then
      return 0
    fi
  done
  for pat in "${EXCLUDE_PATTERNS[@]}"; do
    if [[ "$pat" == */ ]] && [[ "$file" == *"$pat"* ]]; then
      return 0
    fi
    local basename="${file##*/}"
    if [[ "$basename" == $pat ]]; then
      return 0
    fi
    if [[ "$basename" == "$pat" ]]; then
      return 0
    fi
  done
  return 1
}

# --- Checks ---

echo ""
echo -e "${CYAN}=== Public Repo Validation ===${NC}"
echo -e "Private: ${PRIVATE}"
echo -e "Public:  ${PUBLIC}"
echo ""

if [[ ! -d "$PUBLIC/.git" ]]; then
  echo -e "${RED}ERROR: Public repo not found at ${PUBLIC}${NC}"
  exit 1
fi

# --- Check 1: Coverage ---
echo -e "${CYAN}[1/4] Coverage — framework files present in public${NC}"
COVERAGE_ERRORS=0

# Check include_dirs
for dir in "${INCLUDE_DIRS[@]}"; do
  src_dir="${PRIVATE}/${dir}"
  [[ -d "$src_dir" ]] || continue

  while IFS= read -r -d '' file; do
    rel="${file#$PRIVATE/}"
    is_excluded "$rel" && continue
    dst="${PUBLIC}/${rel}"
    if [[ ! -e "$dst" ]] && [[ ! -L "$dst" ]]; then
      echo -e "  ${RED}MISSING${NC} ${rel}"
      COVERAGE_ERRORS=$((COVERAGE_ERRORS + 1))
    fi
  done < <(find "$src_dir" -type f -print0 2>/dev/null)

  # Symlinks too
  while IFS= read -r -d '' link; do
    rel="${link#$PRIVATE/}"
    is_excluded "$rel" && continue
    dst="${PUBLIC}/${rel}"
    if [[ ! -e "$dst" ]] && [[ ! -L "$dst" ]]; then
      echo -e "  ${RED}MISSING${NC} ${rel} (symlink)"
      COVERAGE_ERRORS=$((COVERAGE_ERRORS + 1))
    fi
  done < <(find "$src_dir" -type l -print0 2>/dev/null)
done

# Check include_files
for f in "${INCLUDE_FILES[@]}"; do
  src="${PRIVATE}/${f}"
  [[ -f "$src" ]] || [[ -L "$src" ]] || continue
  is_excluded "$f" && continue
  dst="${PUBLIC}/${f}"
  if [[ ! -e "$dst" ]]; then
    echo -e "  ${RED}MISSING${NC} ${f}"
    COVERAGE_ERRORS=$((COVERAGE_ERRORS + 1))
  fi
done

if [[ $COVERAGE_ERRORS -eq 0 ]]; then
  echo -e "  ${GREEN}All framework files present${NC}"
else
  ERRORS=$((ERRORS + COVERAGE_ERRORS))
fi

# --- Check 2: Privacy scan ---
echo -e "${CYAN}[2/4] Privacy scan — personal data in public repo${NC}"
PRIV_ERRORS=0

# Build allowlist lookup from manifest
is_privacy_allowed() {
  local pattern="$1"
  local rel_path="$2"
  local allowed
  allowed=$(jq -r --arg pat "$pattern" '.privacy_allowlist[$pat] // [] | .[]' "$MANIFEST" 2>/dev/null)
  while IFS= read -r allowed_path; do
    [[ -z "$allowed_path" ]] && continue
    if [[ "$rel_path" == "$allowed_path" ]]; then
      return 0
    fi
  done <<< "$allowed"
  return 1
}

while IFS= read -r -d '' file; do
  for pattern in "${PRIVACY_PATTERNS[@]}"; do
    matches=$(grep -nP "$pattern" "$file" 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
      rel="${file#$PUBLIC/}"
      # Check allowlist before flagging
      if is_privacy_allowed "$pattern" "$rel"; then
        continue
      fi
      echo -e "  ${RED}MATCH${NC} ${rel} (pattern: ${pattern})"
      echo "$matches" | head -3 | while IFS= read -r line; do
        echo "    $line"
      done
      PRIV_ERRORS=$((PRIV_ERRORS + 1))
    fi
  done
done < <(find "$PUBLIC" -type f -not -path '*/.git/*' -print0 2>/dev/null)

if [[ $PRIV_ERRORS -eq 0 ]]; then
  echo -e "  ${GREEN}No privacy pattern matches${NC}"
else
  ERRORS=$((ERRORS + PRIV_ERRORS))
fi

# --- Check 3: Symlink integrity ---
echo -e "${CYAN}[3/4] Symlink integrity — agent symlinks resolve${NC}"
SYM_ERRORS=0

for link in "$PUBLIC/.claude/agents"/*.md; do
  [[ -L "$link" ]] || continue
  if [[ ! -e "$link" ]]; then
    echo -e "  ${RED}BROKEN${NC} $(basename "$link") -> $(readlink "$link")"
    SYM_ERRORS=$((SYM_ERRORS + 1))
  fi
done

if [[ $SYM_ERRORS -eq 0 ]]; then
  echo -e "  ${GREEN}All agent symlinks resolve${NC}"
else
  ERRORS=$((ERRORS + SYM_ERRORS))
fi

# --- Check 4: Bootstrappability ---
echo -e "${CYAN}[4/4] Bootstrappability — critical files for /setup${NC}"
BOOT_ERRORS=0

BOOTSTRAP_FILES=(
  "CLAUDE.md"
  ".claude/settings.json"
  ".claude/agents/REGISTRY.md"
  ".claude/skills/setup/SKILL.md"
)

for bf in "${BOOTSTRAP_FILES[@]}"; do
  if [[ ! -e "${PUBLIC}/${bf}" ]]; then
    echo -e "  ${RED}MISSING${NC} ${bf}"
    BOOT_ERRORS=$((BOOT_ERRORS + 1))
  fi
done

if [[ $BOOT_ERRORS -eq 0 ]]; then
  echo -e "  ${GREEN}All bootstrap-critical files present${NC}"
else
  ERRORS=$((ERRORS + BOOT_ERRORS))
fi

# --- Summary ---
echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo -e "${GREEN}Validation passed — 0 issues${NC}"
  exit 0
else
  echo -e "${RED}Validation failed — ${ERRORS} issue(s)${NC}"
  exit 1
fi
