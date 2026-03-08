---
name: polish-document
description: Convert a markdown document to polished DOCX/PDF output
user_invocable: true
invocation: /polish
arguments: "[file-path] [--format docx|pdf|both]"
---

# Polish Document

Convert a markdown document into a polished, professionally formatted DOCX and/or PDF.

## Instructions

1. If a file path argument is provided, use it. Otherwise, ask which markdown file to polish.
2. Verify the file exists and is a markdown file.
3. Run the conversion script:
   ```
   python engineering/scripts/md-to-polished.py <file-path> --format both
   ```
4. Report the output file paths and sizes.
5. If `core/standards/writing-style.md` has content beyond the skeleton, optionally review the source markdown for style adherence before conversion, noting any em dashes or style mismatches found.

## Example Usage

```
/polish business/strategy/enterprise-ai-context-publishable.md
/polish business/strategy/enterprise-ai-context-deep-dive.md --format pdf
```
