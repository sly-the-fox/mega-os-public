# User Customizations
#
# This file is yours. It is never overwritten by framework updates.
# Rename this file to CLAUDE.local.md and add your customizations below.
#
# CLAUDE.md imports this file via @./.claude/CLAUDE.local.md
# so anything you write here is loaded every session.
#
# Examples of what to put here:
# - Product-specific instructions
# - Custom commit scopes
# - Personal workflow rules
# - Domain-specific agent guidance
# - Agent behavior overrides (see "Customizing Agents" in GETTING_STARTED.md)

---

## Products

All products live under `products/`. Run `/setup` or `/project-kickoff` to add your first product.

Check for a README and CLAUDE.md at the product root before making changes. Product-level CLAUDE.md files override general standards for that product.

---

## Commit Scopes

| Scope | Covers |
|-------|--------|
| `<product-name>` | `products/<product-name>/` |
| `system` | CLAUDE.md, `.claude/`, `core/`, `active/` |
| `business` | `business/`, `drafts/`, `deliverables/` |
| `meta` | Root config, `.gitignore`, CI, multi-product |
