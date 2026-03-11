# Coding Standards

## General Principles
- Prefer clarity over cleverness
- Keep functions focused and short
- Name things descriptively
- Handle errors at system boundaries
- Write tests for critical paths
- Avoid premature abstraction

## Python (Sigil, Freshstate, scripts)
- Target Python 3.12+
- Use type hints for function signatures
- Use virtual environments (.venv)
- Follow PEP 8
- Use f-strings for formatting
- Prefer pathlib over os.path
- Use `uv` for dependency management where available
- Prefer dataclasses or Pydantic models over raw dicts

### FastAPI (Sigil)
- Use Pydantic models for request/response schemas
- Use dependency injection for shared resources (db sessions, auth)
- Use APIRouter for route organization
- Return explicit status codes
- Use async def for I/O-bound endpoints

### CLI Tools (Freshstate)
- Use Click or Typer for CLI interfaces
- Provide --help for all commands
- Use rich for terminal output where appropriate
- Support both CLI and programmatic usage (importable modules)

## TypeScript / Next.js (Tend, Capacitor)
- Use TypeScript with strict mode
- Prefer functional components in React
- Use named exports over default exports
- Handle async errors with try/catch
- Use ESLint + Prettier for formatting
- Prefer const over let, avoid var

### Prisma (Tend)
- Use migrations for all schema changes
- Keep schema.prisma as single source of truth
- Use explicit relation names for clarity
- Handle Prisma errors with typed catches

## Database
- Use migrations for schema changes
- Name tables as plural nouns (snake_case)
- Include created_at and updated_at timestamps
- Index foreign keys

## Security
- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all external input
- Use parameterized queries
- Follow OWASP top 10 guidelines

## Version Control
- Write clear commit messages (what and why)
- Keep commits focused on one change
- Don't commit generated files or dependencies
