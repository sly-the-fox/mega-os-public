---
name: build-site
description: Use when building a website from concept to deployment — orchestrates strategy, design, content, implementation, and quality phases.
user_invocable: true
invocation: /build-site
args: "<description> [--product <name>] [--deploy]"
---

# /build-site

Build a website or landing page from concept through deployment.

## Usage

```
/build-site <description>
/build-site <description> --product local-sites
/build-site <description> --deploy
```

### Arguments
- `<description>` — What to build (e.g., "landing page for Sigil", "portfolio site", "restaurant site for Joe's Grill")
- `--product <name>` — Target an existing product under `products/`. For `local-sites`, generates a TypeScript config file.
- `--deploy` — Include deployment phase (DevOps) after quality checks.

## Workflow

Execute phases sequentially. Each phase creates an agent team. All teammates use `subagent_type: "general-purpose"`, `mode: "auto"`.

### Phase 1: Strategy + Design Direction

**Team: site-strategy**

| Role | Prompt Focus |
|------|-------------|
| Strategist | Define target audience, value proposition, competitive positioning, conversion goals |
| Designer | Create UX structure — site map, page flow, wireframe descriptions, component hierarchy |
| Visual Designer | Establish visual direction — color palette, typography selections, spacing system, animation approach, art direction |

**Output:** Strategy brief + UX wireframes + visual direction document saved to `drafts/sites/<site-name>/`.

### Phase 2: Content + Architecture (parallel)

**Team: site-content**

Run content and architecture work in parallel within the team.

| Role | Prompt Focus |
|------|-------------|
| Writer | Draft all page copy — headlines, body text, CTAs, meta descriptions. Apply `core/standards/writing-style.md`. |
| Marketer | Review copy for positioning, messaging strength, and conversion optimization |
| Editor | Review copy for voice consistency, clarity, and factual accuracy |
| Architect | Validate component structure against the product's architecture. For `--product local-sites`, confirm config schema compatibility. |

**Output:** Finalized copy + architecture validation saved to `drafts/sites/<site-name>/`.

### Phase 3: Implementation

**Team: site-build**

| Role | Prompt Focus |
|------|-------------|
| Engineer | Build the site — implement pages, components, configuration. For `--product local-sites`, create the TypeScript config at `products/local-sites/src/config/sites/<site-name>.ts`. |
| Visual Designer | CSS review and polish pass — typography, color, spacing, animations, responsive breakpoints. Refine until the site looks incredible. |

**Output:** Working site code.

### Phase 4: Quality

**Team: site-quality**

| Role | Prompt Focus |
|------|-------------|
| QA | Test across breakpoints, validate links, check accessibility (contrast, alt text, ARIA), verify content matches approved copy |
| Security Expert | Review for XSS, injection, CSP headers, dependency vulnerabilities |
| Visual Designer | Browser preview: navigate to built pages in Playwright, take screenshots at desktop (1280x800), tablet (768x1024), and mobile (375x812) viewports per `core/standards/visual-preview-protocol.md`. Review screenshots for visual quality, layout issues, responsive behavior. Flag issues for Engineer to fix before proceeding. |
| Reviewer | Final quality gate — check against `core/standards/review-checklist.md`, verify all phases delivered |

**Output:** Quality report with pass/fail and remediation items.

**If issues found:** Route back to Engineer/Visual Designer for fixes, then re-run quality.

### Phase 5: Deploy (if --deploy)

**Team: site-deploy**

| Role | Prompt Focus |
|------|-------------|
| DevOps | Deploy to target platform (Netlify, Vercel, etc.), configure DNS, verify HTTPS, run smoke tests |

**Output:** Live URL + deployment confirmation.

### Phase 6: Wrap-up

Run directly in main context (no team needed):

1. Update `active/now.md` with the completed site and any follow-up TODOs
2. Output summary: what was built, where files live, quality results, next steps
3. Offer to commit

## File Locations

| Artifact | Location |
|----------|----------|
| Strategy/design drafts | `drafts/sites/<site-name>/` |
| Product configs | `products/<product>/src/config/sites/<site-name>.ts` |
| Site code | `products/<product>/` or standalone location |

## Notes

- For `--product local-sites`: Read `products/local-sites/CLAUDE.md` and an existing site config before implementation to understand the schema.
- Each phase team is created and completed before the next phase starts.
- Visual Designer gets a dedicated polish pass in Phase 3 — this is what makes sites look incredible vs. merely functional.
- Content always goes through Writer → Editor flow, even for short copy.
