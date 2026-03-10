---
name: write-content
description: Write original long-form content using the Content Workflow
user_invocable: true
invocation: /write
arguments: "[topic-or-brief] [--sources file1,file2,...] [--output path]"
---

# Write Content

Produce original long-form content (articles, essays, blog posts, book chapters) using the Content Workflow.

## Critical: Agent Teams Required

Content workflow agents MUST be spawned as an **agent team** using TeamCreate:
- Create a team with Writer, Editor, and Polisher as teammates
- All teammates MUST use `subagent_type: "general-purpose"` (custom types cannot read/write files)
- Use `mode: "auto"` to avoid permission prompts
- **NEVER use standalone subagents** for content work — they cannot persist file writes

## Pipeline (MANDATORY — never skip steps)

Every invocation of `/write` MUST execute the full pipeline. No shortcuts.

### Phase 1: Research
a. **If the topic requires web research** — invoke `/deep-research <topic>` (MECE pattern). This creates an agent team that does parallel deep-dive research. Output at `drafts/research/` becomes source material.
b. **If sources are already provided** (`--sources`) — skip to Phase 2.
c. **Librarian** — locate any additional local source material
d. **Summarizer** — compress research into a working brief (if extensive)

### Phase 2: Draft
c. **Writer** — produce the first draft to `drafts/`, applying `core/standards/writing-style.md`

### Phase 3: Edit (MANDATORY)
d. **Editor** — review draft for structure, citations, fact-checking, voice consistency. Editor makes surgical edits directly to the draft file using the Edit tool.
e. **Writer** — revise based on any editorial feedback that requires substantial changes. Save new version to `drafts/`. Repeat d-e if needed.
f. **Editor** — grant editorial approval.

### Phase 4: Polish (MANDATORY)
g. **Polisher** — format approved draft for publication:
   - Clean markdown artifacts
   - Run `python3 engineering/scripts/md-to-polished.py <file> --format both` to produce DOCX/PDF
   - Output to `deliverables/`
h. **Reviewer** — final quality check on deliverables

### Phase 5: Report
i. Report the output file paths (markdown draft + DOCX/PDF deliverables) and any editorial notes.

## File Locations

| Stage | Location |
|-------|----------|
| Intermediate drafts | `drafts/` (e.g., `drafts/topic-name-v1.md`) |
| Final deliverables | `deliverables/` (DOCX/PDF) |
| Style reference | `core/standards/writing-style.md` |

## Example Usage

```
/write "The architecture of trust in multi-agent systems"
/write "Why agent identity matters" --sources business/strategy/enterprise-ai-context.md
/write "Chapter 3: Signal and Structure" --output drafts/book/chapter-3.md
```
