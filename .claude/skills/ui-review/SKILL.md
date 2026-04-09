---
name: ui-review
description: Use when auditing a product's frontend visuals — reviews CSS, typography, color, spacing, animations, and responsive behavior.
user_invocable: true
invocation: /ui-review
args: "[--product <name>] [--focus <area>] [--live]"
---

# /ui-review

Run a visual craft audit on a product's frontend code. Spawns Visual Designer to review CSS implementation quality and produce actionable findings.

## Usage

```
/ui-review
/ui-review --product tend
/ui-review --product tend --focus typography
```

### Arguments
- `--product <name>` — Target product under `products/`. If omitted, attempts to detect from current context.
- `--focus <area>` — Narrow the review to a specific area: `typography`, `color`, `spacing`, `animations`, `responsive`, or `system` (design tokens/variables). If omitted, reviews all areas.
- `--live` — Navigate to the running site using Playwright and take screenshots at multiple viewports, supplementing code-only review with actual rendered verification.

## What Gets Reviewed

| Area | What Visual Designer Checks |
|------|-----------------------------|
| **Design System** | Token consistency, CSS variable usage, utility class patterns, dark/light support |
| **Typography** | Font selections, type scale, line heights, measure (line length), hierarchy clarity |
| **Color** | Palette consistency, WCAG contrast ratios, semantic color usage, dark/light theme support |
| **Spacing** | Rhythm consistency, vertical baseline, padding/margin patterns, alignment |
| **Animations** | Transition quality, easing curves, micro-interactions, loading states, performance impact |
| **Responsive** | Breakpoint coverage, layout shifts, touch targets (48px min), viewport-specific polish |

## Execution

1. **Detect product.** Read `--product` arg or infer from context. Read the product's `CLAUDE.md` and `README.md` for design system context.

2. **Identify frontend files.** Glob for CSS, SCSS, Tailwind configs, component files (`.tsx`, `.jsx`, `.vue`, `.svelte`), and global style files. If no frontend files found, report and exit.

3. **Spawn Visual Designer review.** Create an agent team with Visual Designer role. Provide:
   - All CSS/style files and key component files
   - Product's design system docs (if any)
   - Focus area filter (if `--focus` specified)

   Visual Designer reviews against these criteria:
   - Are design tokens defined and used consistently?
   - Does the type scale follow a coherent ratio?
   - Do all color combinations meet WCAG AA contrast (4.5:1 for text, 3:1 for large text)?
   - Is spacing rhythm consistent (e.g., 4px/8px base)?
   - Are animations performant (prefer `transform`/`opacity`, avoid layout triggers)?
   - Does every breakpoint look intentional, not just "not broken"?

   If `--live` is set:
   - Navigate to the site URL using `mcp__playwright__browser_navigate`
   - Take screenshots at desktop (1280x800), tablet (768x1024), and mobile (375x812) per `core/standards/visual-preview-protocol.md`
   - Visual Designer reviews screenshots alongside code, producing findings grounded in actual rendered behavior
   - Screenshots are referenced in the report alongside file paths and line numbers

4. **Produce report.** Save findings to `drafts/reviews/ui-review-<product>-<date>.md` with:
   - Summary score (1-5) per area
   - Specific findings with file paths and line numbers
   - Concrete CSS/code suggestions for each finding
   - Priority ranking (fix these first)

5. **Present summary.** Show the user a brief overview of findings and the report location.

## Output

| Artifact | Location |
|----------|----------|
| Review report | `drafts/reviews/ui-review-<product>-<date>.md` |

## Notes

- This is a read-only audit — it produces recommendations but does not modify code.
- For implementation of fixes, route findings to Engineer via the Technical Workflow.
- Can be run repeatedly as a quality gate during frontend development.
- Pairs well with `/simplify` for code quality + visual quality coverage.
- With `--live`, findings are backed by actual browser screenshots. Pairs well with the standard code-only review for comprehensive visual quality assessment.
