#!/bin/bash
#
# sync-to-public.sh — Compare personal mega-os with public repo
# and selectively sync safe files (agents, core, skills, engineering, docs).
#
# Reads include/exclude rules from engineering/sync-manifest.json (single source of truth).
#
# Usage:
#   ./sync-to-public.sh              # Show diff only
#   ./sync-to-public.sh --sync       # Sync changed files and commit
#   ./sync-to-public.sh --validate   # Run all checks, exit 0/1, no sync
#   ./sync-to-public.sh --auto-commit # Sync only files changed in last commit, auto-commit+push
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

# --- Manifest reader ---

if [[ ! -f "$MANIFEST" ]]; then
  echo -e "${RED}ERROR: Manifest not found at ${MANIFEST}${NC}" >&2
  exit 1
fi

if ! jq empty "$MANIFEST" 2>/dev/null; then
  echo -e "${RED}ERROR: Invalid JSON in ${MANIFEST}${NC}" >&2
  exit 1
fi

# Read arrays from manifest
mapfile -t INCLUDE_DIRS < <(jq -r '.include_dirs[]' "$MANIFEST")
mapfile -t INCLUDE_FILES < <(jq -r '.include_files[]' "$MANIFEST")
mapfile -t EXCLUDE < <(jq -r '.exclude[]' "$MANIFEST")
mapfile -t EXCLUDE_PATTERNS < <(jq -r '.exclude_patterns // [] | .[]' "$MANIFEST")
mapfile -t PRIVACY_PATTERNS < <(jq -r '.privacy_patterns[]' "$MANIFEST")

# --- Helper functions ---

is_excluded() {
  local file="$1"
  # Exact path match
  for excl in "${EXCLUDE[@]}"; do
    if [[ "$file" == "$excl" ]]; then
      return 0
    fi
  done
  # Pattern match (glob-style: directory suffixes, basename globs)
  for pat in "${EXCLUDE_PATTERNS[@]}"; do
    # Directory pattern (ends with /): match if path contains it
    if [[ "$pat" == */ ]] && [[ "$file" == *"$pat"* ]]; then
      return 0
    fi
    # Basename glob (e.g. *.pyc): match against filename
    local basename="${file##*/}"
    if [[ "$basename" == $pat ]]; then
      return 0
    fi
    # Exact basename match (e.g. .env, sessions.json)
    if [[ "$basename" == "$pat" ]]; then
      return 0
    fi
  done
  return 1
}

is_in_scope() {
  # Check if a file path matches include_dirs or include_files
  local file="$1"
  for dir in "${INCLUDE_DIRS[@]}"; do
    if [[ "$file" == "$dir"* ]]; then
      return 0
    fi
  done
  for f in "${INCLUDE_FILES[@]}"; do
    if [[ "$file" == "$f" ]]; then
      return 0
    fi
  done
  return 1
}

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

privacy_scan_file() {
  # Scan a single file for privacy patterns. Returns 0 if clean, 1 if matches found.
  local file="$1"
  local rel_path="$2"  # relative path for allowlist lookup
  local found=0
  for pattern in "${PRIVACY_PATTERNS[@]}"; do
    local matches
    matches=$(grep -nP "$pattern" "$file" 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
      # Check allowlist
      if is_privacy_allowed "$pattern" "$rel_path"; then
        continue
      fi
      echo -e "${RED}  PRIVACY${NC} ${file}:"
      echo "$matches" | while IFS= read -r line; do
        echo "    $line"
      done
      found=1
    fi
  done
  return $found
}

build_file_list() {
  # Build the full list of files that should sync, respecting include/exclude rules
  local files=()

  # Walk include_dirs
  for dir in "${INCLUDE_DIRS[@]}"; do
    local src="${PRIVATE}/${dir}"
    if [[ -d "$src" ]]; then
      # Regular files
      while IFS= read -r -d '' file; do
        local rel="${file#$PRIVATE/}"
        if ! is_excluded "$rel"; then
          files+=("$rel")
        fi
      done < <(find "$src" -type f -print0 2>/dev/null)

      # Symlinks
      while IFS= read -r -d '' link; do
        local rel="${link#$PRIVATE/}"
        if ! is_excluded "$rel"; then
          files+=("$rel")
        fi
      done < <(find "$src" -type l -print0 2>/dev/null)
    fi
  done

  # Add include_files
  for f in "${INCLUDE_FILES[@]}"; do
    local src="${PRIVATE}/${f}"
    if [[ -f "$src" ]] || [[ -L "$src" ]]; then
      if ! is_excluded "$f"; then
        files+=("$f")
      fi
    fi
  done

  # Deduplicate and print
  printf '%s\n' "${files[@]}" | sort -u
}

# --- Mode: --validate ---

if [[ "${1:-}" == "--validate" ]]; then
  echo ""
  echo -e "${CYAN}=== Sync Validation ===${NC}"
  echo -e "Private: ${PRIVATE}"
  echo -e "Public:  ${PUBLIC}"
  echo ""

  ERRORS=0

  # Check 1: Coverage — every in-scope file in private must exist in public (or be excluded)
  echo -e "${CYAN}[1/4] Coverage check${NC}"
  while IFS= read -r file; do
    dst="${PUBLIC}/${file}"
    if [[ ! -e "$dst" ]] && [[ ! -L "$dst" ]]; then
      echo -e "  ${RED}MISSING${NC} ${file}"
      ERRORS=$((ERRORS + 1))
    fi
  done < <(build_file_list)

  if [[ $ERRORS -eq 0 ]]; then
    echo -e "  ${GREEN}All framework files present in public repo${NC}"
  fi

  # Check 2: Privacy scan on public repo files
  echo -e "${CYAN}[2/4] Privacy scan${NC}"
  PRIV_ERRORS=0
  if [[ -d "$PUBLIC" ]]; then
    while IFS= read -r -d '' file; do
      rel="${file#$PUBLIC/}"
      if ! privacy_scan_file "$file" "$rel"; then
        PRIV_ERRORS=$((PRIV_ERRORS + 1))
      fi
    done < <(find "$PUBLIC" -type f -not -path '*/.git/*' -print0 2>/dev/null)
  fi
  if [[ $PRIV_ERRORS -eq 0 ]]; then
    echo -e "  ${GREEN}No privacy pattern matches in public repo${NC}"
  else
    ERRORS=$((ERRORS + PRIV_ERRORS))
  fi

  # Check 3: Symlink integrity
  echo -e "${CYAN}[3/4] Symlink integrity${NC}"
  SYM_ERRORS=0
  for link in "$PUBLIC/.claude/agents"/*.md; do
    [[ -L "$link" ]] || continue
    if [[ ! -e "$link" ]]; then
      echo -e "  ${RED}BROKEN${NC} ${link} -> $(readlink "$link")"
      SYM_ERRORS=$((SYM_ERRORS + 1))
    fi
  done
  if [[ $SYM_ERRORS -eq 0 ]]; then
    echo -e "  ${GREEN}All agent symlinks resolve${NC}"
  else
    ERRORS=$((ERRORS + SYM_ERRORS))
  fi

  # Check 4: Bootstrappability — critical files for /setup
  echo -e "${CYAN}[4/4] Bootstrappability${NC}"
  BOOTSTRAP_FILES=(
    "CLAUDE.md"
    ".claude/settings.json"
    ".claude/agents/REGISTRY.md"
    ".claude/skills/setup/SKILL.md"
  )
  for bf in "${BOOTSTRAP_FILES[@]}"; do
    if [[ ! -e "${PUBLIC}/${bf}" ]]; then
      echo -e "  ${RED}MISSING${NC} ${bf} (required for bootstrap)"
      ERRORS=$((ERRORS + 1))
    fi
  done
  if [[ $ERRORS -eq $((SYM_ERRORS + PRIV_ERRORS)) ]] || [[ $ERRORS -eq 0 ]]; then
    echo -e "  ${GREEN}All bootstrap-critical files present${NC}"
  fi

  echo ""
  if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}Validation passed — 0 issues${NC}"
    exit 0
  else
    echo -e "${RED}Validation failed — ${ERRORS} issue(s)${NC}"
    exit 1
  fi
fi

# --- Mode: --auto-commit ---

if [[ "${1:-}" == "--auto-commit" ]]; then
  [[ -d "$PUBLIC/.git" ]] || exit 0

  # Get files changed in the last commit
  committed_files=$(git -C "$PRIVATE" diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null)
  [[ -z "$committed_files" ]] && exit 0

  # Filter to in-scope, non-excluded files
  sync_needed=()
  for file in $committed_files; do
    if is_in_scope "$file" && ! is_excluded "$file"; then
      sync_needed+=("$file")
    fi
  done

  [[ ${#sync_needed[@]} -eq 0 ]] && exit 0

  # Privacy scan on files being synced
  privacy_blocked=false
  for file in "${sync_needed[@]}"; do
    src="${PRIVATE}/${file}"
    if [[ -f "$src" ]]; then
      for pattern in "${PRIVACY_PATTERNS[@]}"; do
        if grep -qP "$pattern" "$src" 2>/dev/null; then
          if ! is_privacy_allowed "$pattern" "$file"; then
            echo "[mega-os] BLOCKED: ${file} contains private data (pattern: ${pattern})" >&2
            privacy_blocked=true
          fi
        fi
      done
    fi
  done
  if [[ "$privacy_blocked" == "true" ]]; then
    echo "[mega-os] Sync aborted due to privacy matches. Review and re-run." >&2
    exit 1
  fi

  # Sync the files
  synced=()
  for file in "${sync_needed[@]}"; do
    src="${PRIVATE}/${file}"
    dst="${PUBLIC}/${file}"

    if [[ -L "$src" ]]; then
      mkdir -p "$(dirname "$dst")"
      rm -f "$dst"
      cp -P "$src" "$dst"
      synced+=("$file")
    elif [[ -f "$src" ]]; then
      mkdir -p "$(dirname "$dst")"
      cp "$src" "$dst"
      synced+=("$file")
    elif [[ ! -e "$src" ]]; then
      # File was deleted — remove from public too
      if [[ -e "$dst" ]] || [[ -L "$dst" ]]; then
        rm -f "$dst"
        synced+=("$file (deleted)")
      fi
    fi
  done

  [[ ${#synced[@]} -eq 0 ]] && exit 0

  # Commit to public repo
  commit_msg=$(git -C "$PRIVATE" log -1 --pretty=format:"%s" HEAD)
  cd "$PUBLIC" || exit 0
  for file in "${synced[@]}"; do
    # Strip " (deleted)" suffix for git add
    clean_file="${file% (deleted)}"
    git add "$clean_file" 2>/dev/null || true
  done
  git commit -m "sync: ${commit_msg}" --no-verify >/dev/null 2>&1 || true

  # Push in background
  git push --quiet &>/dev/null &

  echo "[mega-os] Synced ${#synced[@]} file(s) to public repo"
  exit 0
fi

# --- Mode: diff (default) or --sync ---

changed_files=()
synced_files=()

echo ""
echo -e "${CYAN}=== Mega-OS Sync Check ===${NC}"
echo -e "Private: ${PRIVATE}"
echo -e "Public:  ${PUBLIC}"
echo ""

while IFS= read -r rel; do
  src="${PRIVATE}/${rel}"
  dst="${PUBLIC}/${rel}"

  if [[ -L "$src" ]]; then
    # Symlink handling
    link_target="$(readlink "$src")"
    if [[ ! -L "$dst" ]]; then
      echo -e "${GREEN}  SYM${NC}  ${rel} -> ${link_target}"
      changed_files+=("$rel")
    elif [[ "$(readlink "$dst")" != "$link_target" ]]; then
      echo -e "${YELLOW}  SYM${NC}  ${rel} -> ${link_target}"
      changed_files+=("$rel")
    fi
  elif [[ -f "$src" ]]; then
    if [[ ! -f "$dst" ]]; then
      echo -e "${GREEN}  NEW${NC}  ${rel}"
      changed_files+=("$rel")
    elif ! diff -q "$src" "$dst" &>/dev/null; then
      echo -e "${YELLOW}  MOD${NC}  ${rel}"
      changed_files+=("$rel")
    fi
  fi
done < <(build_file_list)

echo ""

if [[ ${#changed_files[@]} -eq 0 ]]; then
  echo -e "${GREEN}Public repo is up to date. Nothing to sync.${NC}"
  exit 0
fi

echo -e "${CYAN}${#changed_files[@]} file(s) differ.${NC}"
echo ""

# If --sync flag, copy and commit
if [[ "${1:-}" == "--sync" ]]; then
  # Privacy scan before syncing
  echo -e "${CYAN}Running privacy scan...${NC}"
  privacy_blocked=false
  for file in "${changed_files[@]}"; do
    src="${PRIVATE}/${file}"
    if [[ -f "$src" ]] && [[ ! -L "$src" ]]; then
      for pattern in "${PRIVACY_PATTERNS[@]}"; do
        if grep -qP "$pattern" "$src" 2>/dev/null; then
          if ! is_privacy_allowed "$pattern" "$file"; then
            echo -e "${RED}  BLOCKED${NC} ${file} — matches privacy pattern: ${pattern}"
            privacy_blocked=true
          fi
        fi
      done
    fi
  done

  if [[ "$privacy_blocked" == "true" ]]; then
    echo ""
    echo -e "${RED}Sync aborted — privacy patterns detected in files above.${NC}"
    echo -e "Add the file to the 'exclude' list in ${MANIFEST} or remove the personal data."
    exit 1
  fi
  echo -e "${GREEN}Privacy scan clean.${NC}"
  echo ""

  echo -e "${CYAN}Syncing files...${NC}"
  for file in "${changed_files[@]}"; do
    src="${PRIVATE}/${file}"
    dst="${PUBLIC}/${file}"
    mkdir -p "$(dirname "$dst")"

    if [[ -L "$src" ]]; then
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
