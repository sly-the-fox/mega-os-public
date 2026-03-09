---
name: write-content
description: Write original long-form content using the Content Workflow
user_invocable: true
invocation: /write
arguments: "[topic-or-brief] [--sources file1,file2,...] [--output path]"
---

# Write Content

Produce original long-form content (articles, essays, blog posts, book chapters) using the Content Workflow.

## Instructions

1. If a topic/brief argument is provided, use it. Otherwise, ask what to write.
2. If `--sources` are provided, read the source files. Otherwise, ask if there are reference materials.
3. Determine output path: use `--output` if provided, otherwise default to `deliverables/`.
4. Save intermediate drafts to `drafts/` (e.g., `drafts/topic-name-v1.md`, `drafts/topic-name-v2.md`).
5. Execute the Content Workflow:
   a. **Librarian** — locate any additional source material relevant to the topic
   b. **Summarizer** — compress extensive research into a working brief (skip if sources are concise)
   c. **Writer** — produce the first draft to `drafts/`, applying `core/standards/writing-style.md`
   d. **Editor** — review for structure, citations, fact-checking, voice consistency
   e. **Writer** — revise based on editorial feedback, save new version to `drafts/` (repeat d-e if needed)
   f. **Editor** — grant editorial approval
   g. **Polisher** — format for publication (invoke `/polish` on the approved draft), output to `deliverables/`
   h. **Reviewer** — final quality check
6. Save the approved markdown draft to the output path.
6. Report the output file path and any editorial notes.

## Example Usage

```
/write "The architecture of trust in multi-agent systems"
/write "Why agent identity matters" --sources business/strategy/enterprise-ai-context.md
/write "Chapter 3: Signal and Structure" --output drafts/book/chapter-3.md
```
