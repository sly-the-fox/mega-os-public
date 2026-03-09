---
name: add-agent
description: Create a new agent with file, symlink, and all registry/doc updates in sync.
invocation: /add-agent
user_invocable: true
---

# Add Agent

Create a new agent and update all references so everything stays in sync.

## Steps

1. **Collect info** — Ask the user:
   - Agent name (must be lowercase kebab-case, e.g., `api-designer`)
   - One-line description (when should this agent be used?)
   - Category: governance, knowledge, technical, business, or evolution
   - Tools needed (e.g., read, write, bash, edit, grep, glob)

   **Validate:**
   - Name is kebab-case (lowercase letters, numbers, hyphens only)
   - No existing agent with the same name (check `.claude/agents/REGISTRY.md`)
   - Category is one of the five valid categories

2. **Create agent file** — Write `.claude/agents/<category>/<name>.md` using this template. Read an existing agent in the same category first to match the exact format:

   ```markdown
   ---
   name: <name>
   description: <one-line description>
   tools: <tools>
   ---

   # <Name (Title Case)>

   ## Role
   <What this agent does — 1-2 sentences.>

   ## Mission
   <The agent's core objective.>

   ## Responsibilities
   - <responsibility 1>
   - <responsibility 2>
   - <responsibility 3>

   ## Inputs
   - <What this agent receives (requests, files, data)>

   ## Outputs
   - <What this agent produces (files, decisions, reports)>

   ## Boundaries
   - Does NOT <thing outside scope>
   - Does NOT <another thing outside scope>

   ## Escalate When
   - <condition requiring escalation>

   ## Collaboration
   - **<agent>** — <how they interact>
   ```

   Ask the user to fill in or confirm the Role, Mission, and Responsibilities. Suggest reasonable defaults based on the name and description.

3. **Create symlink** — Run:
   ```bash
   ln -s <category>/<name>.md .claude/agents/<name>.md
   ```
   Verify the symlink resolves correctly.

4. **Update REGISTRY.md** — Read `.claude/agents/REGISTRY.md`. Add the new agent to the correct category table, maintaining alphabetical order within the category.

5. **Update AGENTS.md** — Read `AGENTS.md`:
   - Update the agent count in the category header (e.g., "### Technical (9 agents)" → "### Technical (10 agents)")
   - Add the agent entry in the correct category list, maintaining alphabetical order
   - The format is: `- **<name>** — <description>`

6. **Update README.md** — Read `README.md`:
   - Update the total agent count (e.g., "30 specialized agents" → "31 specialized agents")
   - Update the count comment in the directory structure (e.g., `# 30 agent definitions` → `# 31 agent definitions`)
   - Add the agent name to the correct category line in the directory structure

7. **Update CLAUDE.md** — Read `CLAUDE.md`:
   - Update the count in the "What This Is" paragraph if it mentions a specific number
   - Update the count in the category table row
   - Add the agent name to the Agents column in the correct category row

8. **Update Collaboration sections** — Ask the user:
   - "Which existing agents does this new agent collaborate with?"
   - For each named collaborator, read that agent's file and add a line to its `## Collaboration` section referencing the new agent
   - Add reciprocal entries in the new agent's Collaboration section

9. **Commit** — Stage all changed files and commit:
   ```
   Add <name> agent (<category>)
   ```

Print summary of all files created/modified.
