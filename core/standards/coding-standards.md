# Coding Standards

## General Principles
- Prefer clarity over cleverness
- Keep functions focused and short
- Name things descriptively
- Handle errors at system boundaries
- Write tests for critical paths
- Avoid premature abstraction

## TypeScript / JavaScript
- Use TypeScript with strict mode
- Prefer functional components in React
- Use named exports over default exports
- Handle async errors with try/catch
- Use ESLint + Prettier for formatting
- Prefer const over let, avoid var

## Python
- Target Python 3.10+
- Use type hints for function signatures
- Use virtual environments (.venv)
- Follow PEP 8
- Use f-strings for formatting
- Prefer pathlib over os.path

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
