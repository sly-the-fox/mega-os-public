# Review Checklist

Standard checklist for the Reviewer agent when evaluating work.

## Correctness
- [ ] Does the output match the requirements?
- [ ] Are edge cases handled?
- [ ] Is the logic sound?
- [ ] Are there off-by-one errors or boundary issues?

## Completeness
- [ ] Are all requirements addressed?
- [ ] Is anything missing that was requested?
- [ ] Are error cases covered?
- [ ] Is the definition of done met?

## Security
- [ ] No hardcoded secrets or credentials?
- [ ] Input validation at system boundaries?
- [ ] No injection vulnerabilities (SQL, XSS, command)?
- [ ] Appropriate access controls?
- [ ] FastAPI: dependencies validate auth before data access?
- [ ] Prisma: no raw queries unless necessary and parameterized?

## Quality
- [ ] Code is readable and well-named?
- [ ] No unnecessary complexity?
- [ ] Follows project coding standards?
- [ ] No dead code or debugging artifacts?
- [ ] Python: type hints on function signatures?
- [ ] TypeScript: strict mode, no `any` without justification?

## Documentation
- [ ] Changes documented where needed?
- [ ] API changes reflected in docs?
- [ ] Non-obvious decisions explained?

## Testing
- [ ] Tests exist for critical paths?
- [ ] Tests actually test the right thing?
- [ ] Edge cases covered in tests?

## Integration
- [ ] Works with existing system?
- [ ] No breaking changes to interfaces?
- [ ] Dependencies are appropriate?
- [ ] Database migrations included if schema changed?
