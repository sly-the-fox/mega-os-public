# Standards Customization

> Referenced by: `.claude/skills/setup/SKILL.md` — Phase 4

---

> **Tip:** If you have strong opinions about coding standards and want to review changes before they're applied, consider switching to **Plan mode** (`/plan`) with **Opus 4.6 (medium)** or equivalent. This lets you approve each standards change before it's written. You can return to setup afterward with `/setup --phase 5`. Otherwise, we'll work through it interactively right here.

1. **Coding standards** — Read `core/standards/coding-standards.md`. Show the user which language sections exist. Ask:
   - Which of these are relevant to your stack?
   - Any languages/frameworks to add?
   - Remove irrelevant sections and add new ones for their stated tech stack with sensible defaults.

2. **Naming conventions** — Read `core/standards/naming.md`. Show current conventions. Ask:
   - Does this match your preferences? Any changes?
   - Apply requested changes.

3. **Writing style** — Check if `core/standards/writing-style.md` exists.
   - If it does NOT exist: copy from `core/standards/writing-style.default.md` to create the user's copy.
   - If it exists and still contains the "Setup required" marker (template version): Ask "Do you have a preferred writing style? (technical/casual/formal/concise)"
   - If they want a personalized style: prompt them to place 3-5 writing samples in `style-samples/`, then analyze the samples and populate `writing-style.md` with a full style profile.
   - If they skip or have no samples: leave the template in place (agents produce neutral content).
   - If already populated (no "Setup required" marker): inform user their style guide is already configured and ask if they want to regenerate it.
   - Note: `writing-style.default.md` ships with the framework and is updated by `/update`. The user's `writing-style.md` is never overwritten by updates.

4. **Review checklist** — Read `core/standards/review-checklist.md`. Show current criteria. Ask:
   - Any criteria to add or remove for your domain?
   - Apply changes.

Print educational beat: "These standards are enforced by the Reviewer agent at the end of every Technical workflow. Customizing now means relevant feedback from day one."
