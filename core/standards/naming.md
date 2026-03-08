# Naming Standards

## Files and Directories
- Use lowercase kebab-case for all filenames: `security-expert.md`, `project-map.md`
- Directories are also lowercase kebab-case: `shared-libraries/`, `example-api/`
- No spaces, no camelCase, no underscores in filenames

## Agent Files
- Named after the role: `engineer.md`, `overseer.md`, `qa.md`
- Shared resources in `shared/` subdirectory
- Registry at `REGISTRY.md` (uppercase for system-level files)

## Code Conventions
- **TypeScript/JavaScript**: camelCase for variables/functions, PascalCase for components/classes
- **Python**: snake_case for variables/functions, PascalCase for classes
- **Environment variables:** UPPER_SNAKE_CASE
- **Database columns:** snake_case
- **API endpoints:** kebab-case paths, camelCase JSON fields

## Documentation
- Uppercase for system-level docs: CLAUDE.md, README.md, AGENTS.md, REGISTRY.md
- Lowercase kebab-case for everything else
- Use `.md` extension for all documentation

## Branches
- feature/description, fix/description, chore/description
