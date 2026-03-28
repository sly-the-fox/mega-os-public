# Product Scaffolding

> Referenced by: `.claude/skills/setup/SKILL.md` — Phase 8

---

Ask: "Do you want to create your first product now?"

If no, skip to Phase 9.

If yes:

1. "What's the product name?" (validate: kebab-case, no spaces)
2. "What tech stack?" (e.g., Next.js, Python/FastAPI, Go, static site)
3. "One-line description?"

Then:
- Create `products/<name>/` with appropriate structure for the tech stack
- Create `products/<name>/CLAUDE.md` with project context
- Create `products/<name>/README.md` with basic info
- Use `core/templates/spec-template.md` to create `products/<name>/SPEC.md`
- Update `core/indexes/project-map.md` with the new product
- Update `active/priorities.md` if not already listed

Print: "Product scaffolded at `products/<name>/`."
