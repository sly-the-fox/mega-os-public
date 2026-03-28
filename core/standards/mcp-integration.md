# MCP Integration Standard

Formalizes Model Context Protocol server registration, configuration, and usage patterns for Mega-OS. Documents the existing Playwright MCP as reference implementation and provides a template for future MCP server additions.

**Origin:** OpenJarvis audit IMP-010 (2026-03-27)

---

## What MCP Is

Model Context Protocol (MCP) is Anthropic's standard for connecting AI systems to external tools and data sources. MCP servers expose tools that Claude Code can call directly, without shell wrapping.

Benefits over CLI-based tool integration:
- Structured input/output (JSON schema, not string parsing)
- Persistent server process (connection pooling, state management)
- Standardized discovery (tool listing, capability advertisement)
- Lower token overhead (Mikayla Thompson benchmark: MCP 2x faster, 3x fewer tool calls vs CLI)

---

## Current MCP Servers

| Server | Purpose | Config Location | Status |
|--------|---------|-----------------|--------|
| Playwright | Browser automation (navigation, screenshots, form fill, accessibility) | `.claude/settings.json` → `mcpServers.playwright` | Active |

---

## Adding a New MCP Server

### Step 1: Evaluate Need

Before adding an MCP server, answer:
1. Is there a CLI alternative that works well enough?
2. Will this server be used regularly (not just once)?
3. Is the server maintained and trustworthy?
4. Does it require secrets or credentials? If so, how are they managed?

If the answer to #1 is "yes" and #2 is "no", use the CLI approach instead.

### Step 2: Configure in settings.json

Add the server to `.claude/settings.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/mcp-server"],
      "env": {}
    }
  }
}
```

**Key fields:**
- `command`: The executable to launch the server
- `args`: Command-line arguments
- `env`: Environment variables (use `$ENV_VAR` syntax for secrets)

### Step 3: Register Permissions

Add tool permissions to the `permissions.allow` list in `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__server-name__tool_name"
    ]
  }
}
```

Use wildcards sparingly. Prefer explicit tool names over `mcp__server-name__*`.

### Step 4: Document in This File

Add the server to the "Current MCP Servers" table above with:
- Server name
- Purpose (one line)
- Config location
- Status (Active / Deprecated / Testing)

### Step 5: Test

Verify the server works:
1. Restart Claude Code (MCP servers connect on startup)
2. Call a tool from the new server
3. Verify output matches expected schema
4. Check for error handling (what happens when the server is down?)

---

## Reference Implementation: Playwright MCP

Configuration in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-playwright@latest"]
    }
  }
}
```

Tools exposed: `browser_navigate`, `browser_click`, `browser_fill_form`, `browser_take_screenshot`, `browser_snapshot`, `browser_evaluate`, and more.

Permissions: Each tool is individually allowed in `permissions.allow`.

**Usage pattern:** Tools are called as `mcp__playwright__browser_navigate`, `mcp__playwright__browser_click`, etc. Claude Code handles the MCP protocol — just call the tools by name.

---

## Security Considerations

- Never hardcode credentials in `settings.json`. Use environment variables.
- Review MCP server source before trusting — servers have tool-level access.
- Rate-limit external MCP servers that make network calls.
- MCP servers run as local processes — they have filesystem access. Choose servers from trusted sources.
- Add new MCP tools to permissions explicitly. Avoid blanket wildcards.

---

## When NOT to Use MCP

- One-time operations (use bash/CLI instead)
- Simple file operations (use built-in Read/Write/Edit tools)
- Operations that need audit trail (MCP calls aren't traced by default — add trace lines manually if needed)
- When the equivalent CLI tool is simpler and token-efficient
