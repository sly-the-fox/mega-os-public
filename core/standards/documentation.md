# Documentation Standards

## When to Document
- Architectural decisions: always, in core/history/decisions.md
- New features: README or inline docs as appropriate
- Processes: SOPs in relevant location
- API changes: update API docs immediately
- Configuration: document in context (README or setup guide)

## How to Document
- Lead with purpose: what does this do and why
- Include setup/usage instructions where applicable
- Keep documentation close to what it describes
- Update docs when the thing they describe changes
- Remove stale documentation rather than leaving it to mislead

## Decision Records
- Use core/templates/decision-template.md format
- Log in core/history/decisions.md
- Include: date, decision, rationale, status, consequences

## Implementation Notes
- Keep in the relevant project directory
- Focus on "why" over "what" (code shows what)
- Document non-obvious tradeoffs and constraints

## Polished Deliverables
- Use `engineering/scripts/md-to-polished.py` to convert markdown to DOCX/PDF
- Output goes to `deliverables/` with date-prefixed filenames
- Invoke via `/polish <file-path>` skill
- Polisher agent handles end-to-end document polishing
- All final deliverables must follow `core/standards/writing-style.md` if populated
- No em dashes in final output

## Review Documentation
- Reviewer agent checks for doc completeness
- Documenter agent creates/updates docs
- Librarian agent ensures organization and discoverability
