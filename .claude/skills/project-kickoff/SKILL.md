# Project Kickoff

Initialize a new project with proper structure, documentation, and registration in the Mega-OS system.

## Steps

1. **Create project directory**
   - Create `products/<project-name>/` using kebab-case naming.
   - Create a basic directory structure appropriate for the tech stack.

2. **Create project CLAUDE.md**
   - Write a project-level CLAUDE.md with:
     - What the project is
     - Tech stack
     - How to run/build
     - Key files and directories
     - Project-specific conventions

3. **Create project spec**
   - Use `core/templates/spec-template.md` as the base.
   - Fill in: overview, goals, non-goals, technical approach, dependencies, milestones, risks.

4. **Register in project map**
   - Add the project to `core/indexes/project-map.md`.
   - Add key files to `core/indexes/canonical-files.md` if appropriate.

5. **Add to priorities**
   - Add the project to `active/priorities.md` at the appropriate priority level.
   - Update `active/now.md` if this is the current focus.

6. **Log decision**
   - Create an entry in `core/history/decisions.md` recording:
     - Why this project was started
     - Key technical choices
     - Expected outcomes
   - Add a timeline entry to `core/history/master-timeline.md`.

7. **Initialize version control**
   - If the project has its own repo, initialize git.
   - If part of mega-os, ensure files are tracked.
   - Create an initial commit.
