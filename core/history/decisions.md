# Decision Log

## DEC-001: 26-Agent Architecture
- **Date:** 2026-03-06
- **Decision:** Adopt a 26-agent system organized into 5 categories
- **Rationale:** Covers governance, knowledge, technical, business, and evolution needs without role overlap
- **Status:** Implemented

## DEC-002: Category Subdirectories
- **Date:** 2026-03-06
- **Decision:** Organize agents into category subdirectories under .claude/agents/
- **Rationale:** Better organization and discoverability than a flat list of 26 files
- **Status:** Implemented, discovery verification pending

## DEC-003: Kebab-Case Naming
- **Date:** 2026-03-06
- **Decision:** Use lowercase kebab-case for all filenames
- **Rationale:** Consistency, URL-safe, readable
- **Status:** Implemented

## DEC-004: Git Repository
- **Date:** 2026-03-07
- **Decision:** Initialize as git repo (private)
- **Rationale:** Version control, worktree isolation, change tracking
- **Status:** Implemented

## DEC-005: Telegram CLI Wrapper
- **Date:** 2026-03-07
- **Decision:** Use lightweight Python daemon polling Telegram, piping to claude --message
- **Rationale:** Simpler than MCP, avoids complex server setup
- **Status:** Planned

## DEC-006: Skip MCP Servers Initially
- **Date:** 2026-03-07
- **Decision:** No MCP servers configured at launch
- **Rationale:** Configure as specific needs arise rather than preemptively
- **Status:** Active

## DEC-007: Telegram Bridge Security Hardening
- **Date:** 2026-03-07
- **Decision:** Add multi-layer security to Telegram bridge — CLI argument injection fix, passphrase-based second-factor auth, per-chat rate limiting, generic error messages, pinned dependencies
- **Rationale:** Security audit identified 9 findings (1 critical, 2 high, 3 medium, 2 low, 1 info). Applied fixes for all actionable items.
- **Status:** Implemented
