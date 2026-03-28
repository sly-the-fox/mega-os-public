# Tool Result Validation Standard

Defines expected output patterns for critical tools and quality gates for detecting bad outputs before they propagate downstream.

**Origin:** OpenJarvis audit IMP-006 (2026-03-27)

---

## Purpose

When a tool or skill produces output, the next agent in the workflow should validate that the output is usable before building on it. This prevents garbage propagation — where a failed tool output silently corrupts downstream work.

This is a **standard** (documentation + behavior guidance), not a runtime enforcement layer. Agents apply these checks as part of their handoff protocol.

---

## Validation Levels

| Level | When | What |
|-------|------|------|
| **Basic** | Every handoff | Output exists, is non-empty, and is the expected type (file, text, data) |
| **Structural** | Handoffs involving structured data | Output matches expected schema (JSON valid, required fields present, correct types) |
| **Semantic** | Quality gates (QA, Reviewer) | Output content makes sense in context (not truncated, not error messages, not placeholder text) |

---

## Common Failure Patterns

These are the patterns that indicate a tool produced bad output. Agents should check for these before accepting handoff input:

### 1. Error-as-Output
The tool returned an error message instead of the expected output. Look for:
- Python tracebacks in text output
- `Error:`, `Failed:`, `Exception:` prefixes
- HTTP status codes (4xx, 5xx) in API responses
- Empty files where content was expected

### 2. Truncated Output
The tool was interrupted mid-execution. Look for:
- Incomplete JSON (missing closing braces/brackets)
- Markdown files ending mid-sentence
- Code files with unclosed blocks

### 3. Placeholder Content
The tool produced template/placeholder text. Look for:
- `TODO`, `FIXME`, `PLACEHOLDER` in output
- Lorem ipsum text
- `[INSERT X HERE]` patterns
- Repeated boilerplate that doesn't address the actual input

### 4. Wrong Target
The tool wrote to the wrong file or produced the wrong type of output. Look for:
- Output filename doesn't match expected pattern
- Content type mismatch (expected JSON, got markdown)
- Content references wrong subject

---

## Validation by Workflow Step

### Engineer -> QA Handoff
- [ ] All files mentioned in the implementation plan exist
- [ ] No syntax errors in code files (if applicable, run linter)
- [ ] No error-as-output in generated files
- [ ] Changes are in the correct scope (no unrelated files modified)

### Writer -> Editor Handoff
- [ ] Draft file exists at expected path in `drafts/`
- [ ] Content is non-empty and addresses the assigned topic
- [ ] No placeholder text
- [ ] Writing style guide was applied (no em dashes, no generic AI voice)

### Skill Output Validation (cron context)
- [ ] Target file was modified (check `date -r` vs today)
- [ ] File size is reasonable (not 0 bytes, not suspiciously small)
- [ ] Exit code is 0
- [ ] No error patterns in log output

### State File Updates
- [ ] File was actually modified (git diff shows changes)
- [ ] Markdown structure is intact (headers, tables not broken)
- [ ] Dates are valid and not in the past (for forward-looking items)

---

## How to Apply

This standard is advisory. Agents apply these checks during handoffs as part of existing workflow protocols. The key behavioral change:

**Before (current):** Accept handoff input without checking.
**After:** Spot-check handoff input for the failure patterns above before building on it.

If a validation check fails:
1. Report the failure to the upstream agent
2. Request correction
3. If correction fails, escalate per error handling protocol (system-rules.md rule 29)

---

## Tracking

QA agents should note validation catches in their output. Over time, these catches feed into the Evaluator's quantitative metrics (IMP-012) to measure tool reliability.
