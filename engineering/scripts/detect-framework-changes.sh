#!/usr/bin/env bash
# detect-framework-changes.sh
# Checks if staged git files include framework files (per sync-manifest).
# Used by PreToolUse hook on git commit — silent when no framework files staged.

set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0

# Get staged files (exit silently if not in a git repo or nothing staged)
STAGED=$(git diff --cached --name-only 2>/dev/null) || exit 0
[ -z "$STAGED" ] && exit 0

# Framework source paths (triggers for /framework-sync)
# These are files whose changes require cross-reference updates.
# Root docs (CLAUDE.md, README.md, etc.) are TARGETS, not triggers — excluded to prevent loops.
FRAMEWORK_PATTERNS=(
  ".claude/agents/governance/"
  ".claude/agents/knowledge/"
  ".claude/agents/technical/"
  ".claude/agents/business/"
  ".claude/agents/evolution/"
  ".claude/agents/shared/"
  ".claude/agents/REGISTRY.md"
  ".claude/agents/README.md"
  ".claude/skills/"
  ".claude/hooks/"
  "core/standards/"
  "core/templates/"
  "engineering/scripts/"
  "engineering/sync-manifest.json"
)

# Collect matching framework files
MATCHES=()
while IFS= read -r file; do
  for pattern in "${FRAMEWORK_PATTERNS[@]}"; do
    if [[ "$file" == "$pattern"* ]]; then
      MATCHES+=("$file")
      break
    fi
  done
done <<< "$STAGED"

# Output only if framework files found
if [ ${#MATCHES[@]} -gt 0 ]; then
  echo ""
  echo "FRAMEWORK FILES CHANGED (${#MATCHES[@]}):"
  for f in "${MATCHES[@]}"; do
    echo "  - $f"
  done
  echo ""
  echo "Cross-references may need updating. Run /framework-sync after committing."
  echo ""
fi
