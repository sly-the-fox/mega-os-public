#!/usr/bin/env bash
# check-index-integrity.sh — Detect drift between skill/agent directories and index files.
# Exit 0 = clean, Exit 1 = drift detected.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ERRORS=0

red()   { printf '\033[0;31m%s\033[0m\n' "$1"; }
green() { printf '\033[0;32m%s\033[0m\n' "$1"; }
warn()  { printf '\033[0;33m⚠ %s\033[0m\n' "$1"; ERRORS=$((ERRORS + 1)); }

# --- Skills ---

# Actual skill directories
ACTUAL_SKILLS=$(find "$REPO_ROOT/.claude/skills" -mindepth 1 -maxdepth 1 -type d | wc -l)

# skills-reference.md entries (count table rows with a pipe-delimited number)
SKILLS_REF="$REPO_ROOT/core/standards/skills-reference.md"
if [[ -f "$SKILLS_REF" ]]; then
    REF_SKILLS=$(grep -cE '^\| [0-9]+ \|' "$SKILLS_REF" || true)
    if [[ "$ACTUAL_SKILLS" -ne "$REF_SKILLS" ]]; then
        warn "skills-reference.md: $REF_SKILLS entries vs $ACTUAL_SKILLS skill directories"
    fi
else
    warn "skills-reference.md not found"
fi

# canonical-files.md skill count
CANONICAL="$REPO_ROOT/core/indexes/canonical-files.md"
if [[ -f "$CANONICAL" ]]; then
    CANON_COUNT=$(grep -oP '## Skills \(\K[0-9]+' "$CANONICAL" || echo "0")
    if [[ "$ACTUAL_SKILLS" -ne "$CANON_COUNT" ]]; then
        warn "canonical-files.md: Skills count ($CANON_COUNT) vs actual ($ACTUAL_SKILLS)"
    fi
    # Check each skill directory has an entry
    for dir in "$REPO_ROOT/.claude/skills"/*/; do
        skill_name=$(basename "$dir")
        if ! grep -q "skills/$skill_name/" "$CANONICAL"; then
            warn "canonical-files.md: missing entry for skill '$skill_name'"
        fi
    done
fi

# project-map.md skill listing
PROJMAP="$REPO_ROOT/core/indexes/project-map.md"
if [[ -f "$PROJMAP" ]]; then
    for dir in "$REPO_ROOT/.claude/skills"/*/; do
        skill_name=$(basename "$dir")
        if ! grep -q "$skill_name" "$PROJMAP"; then
            warn "project-map.md: missing skill '$skill_name'"
        fi
    done
fi

# README.md slash command count
README="$REPO_ROOT/README.md"
if [[ -f "$README" ]]; then
    README_SKILLS=$(grep -oP '\*\*[0-9]+ slash commands\*\*' "$README" | grep -oP '[0-9]+' || echo "0")
    if [[ -n "$README_SKILLS" && "$ACTUAL_SKILLS" -ne "$README_SKILLS" ]]; then
        warn "README.md: says $README_SKILLS slash commands vs $ACTUAL_SKILLS skill directories"
    fi
fi

# --- Agents ---

# Count agent .md files in subdirectories (excluding shared/, REGISTRY.md, README.md)
ACTUAL_AGENTS=0
for category in governance knowledge technical business evolution; do
    dir="$REPO_ROOT/.claude/agents/$category"
    if [[ -d "$dir" ]]; then
        count=$(find "$dir" -maxdepth 1 -name '*.md' -type f | wc -l)
        ACTUAL_AGENTS=$((ACTUAL_AGENTS + count))
    fi
done

# REGISTRY.md agent count
REGISTRY="$REPO_ROOT/.claude/agents/REGISTRY.md"
if [[ -f "$REGISTRY" ]]; then
    # Count rows in agent tables (lines with | Name | `path.md` | ..., excluding headers/separators)
    REG_AGENTS=$(grep -cE '^\| .+ \| `' "$REGISTRY" || true)
    if [[ "$ACTUAL_AGENTS" -ne "$REG_AGENTS" ]]; then
        warn "REGISTRY.md: $REG_AGENTS entries vs $ACTUAL_AGENTS agent files"
    fi
fi

# Symlink validation
for link in "$REPO_ROOT/.claude/agents"/*.md; do
    [[ -L "$link" ]] || continue
    if [[ ! -e "$link" ]]; then
        warn "Broken symlink: $link -> $(readlink "$link")"
    fi
done

# Symlink count vs agent files
SYMLINK_COUNT=$(find "$REPO_ROOT/.claude/agents" -maxdepth 1 -name '*.md' -type l | wc -l)
if [[ "$ACTUAL_AGENTS" -ne "$SYMLINK_COUNT" ]]; then
    warn "Symlinks ($SYMLINK_COUNT) vs agent files ($ACTUAL_AGENTS) mismatch"
fi

# README.md agent count
if [[ -f "$README" ]]; then
    README_AGENTS=$(grep -oP '\*\*[0-9]+ (specialized )?AI agents\*\*' "$README" | grep -oP '[0-9]+' | head -1 || echo "0")
    if [[ -n "$README_AGENTS" && "$ACTUAL_AGENTS" -ne "$README_AGENTS" ]]; then
        warn "README.md: says $README_AGENTS agents vs $ACTUAL_AGENTS agent files"
    fi
fi

# CLAUDE.md agent count
CLAUDEMD="$REPO_ROOT/CLAUDE.md"
if [[ -f "$CLAUDEMD" ]]; then
    CLAUDE_AGENTS=$(grep -oP '[0-9]+ specialized agents' "$CLAUDEMD" | grep -oP '[0-9]+' | head -1 || echo "0")
    if [[ -n "$CLAUDE_AGENTS" && "$ACTUAL_AGENTS" -ne "$CLAUDE_AGENTS" ]]; then
        warn "CLAUDE.md: says $CLAUDE_AGENTS agents vs $ACTUAL_AGENTS agent files"
    fi
fi

# --- Sync Manifest ---

MANIFEST="$REPO_ROOT/engineering/sync-manifest.json"
if [[ -f "$MANIFEST" ]]; then
    # Validate JSON
    if ! jq empty "$MANIFEST" 2>/dev/null; then
        warn "sync-manifest.json: invalid JSON"
    fi

    # Verify all include_dirs exist
    while IFS= read -r dir; do
        if [[ ! -d "$REPO_ROOT/$dir" ]]; then
            warn "sync-manifest.json: include_dir '$dir' does not exist"
        fi
    done < <(jq -r '.include_dirs[]' "$MANIFEST" 2>/dev/null)

    # Verify all include_files exist
    while IFS= read -r f; do
        if [[ ! -f "$REPO_ROOT/$f" ]] && [[ ! -L "$REPO_ROOT/$f" ]]; then
            warn "sync-manifest.json: include_file '$f' does not exist"
        fi
    done < <(jq -r '.include_files[]' "$MANIFEST" 2>/dev/null)

    # Verify all exclude paths are within include scope
    while IFS= read -r excl; do
        in_scope=false
        while IFS= read -r dir; do
            if [[ "$excl" == "$dir"* ]]; then
                in_scope=true
                break
            fi
        done < <(jq -r '.include_dirs[]' "$MANIFEST" 2>/dev/null)
        if [[ "$in_scope" == "false" ]]; then
            # Check include_files too
            while IFS= read -r f; do
                if [[ "$excl" == "$f" ]]; then
                    in_scope=true
                    break
                fi
            done < <(jq -r '.include_files[]' "$MANIFEST" 2>/dev/null)
        fi
        if [[ "$in_scope" == "false" ]]; then
            warn "sync-manifest.json: exclude '$excl' is not within any include scope"
        fi
    done < <(jq -r '.exclude[]' "$MANIFEST" 2>/dev/null)
else
    warn "sync-manifest.json not found"
fi

# --- Summary ---
echo ""
if [[ "$ERRORS" -eq 0 ]]; then
    green "✓ Index integrity check passed — no drift detected"
    echo "  Skills: $ACTUAL_SKILLS | Agents: $ACTUAL_AGENTS | Symlinks: $SYMLINK_COUNT"
    exit 0
else
    red "✗ Index integrity check failed — $ERRORS issue(s) found"
    echo "  Skills: $ACTUAL_SKILLS | Agents: $ACTUAL_AGENTS | Symlinks: $SYMLINK_COUNT"
    exit 1
fi
