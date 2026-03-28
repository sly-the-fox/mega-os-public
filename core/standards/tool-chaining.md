# Tool Chaining Patterns

Reusable multi-tool chain patterns for common Mega-OS operations. Skills and workflows should reference these patterns rather than reinventing chains.

**Origin:** OpenJarvis audit IMP-011 (2026-03-27)

---

## What This Is

A tool chain is a sequence of tool calls that together accomplish a higher-level operation. Instead of each skill reimplementing common chains (e.g., "read file, validate, transform, write"), this document defines shared patterns.

---

## Chain Catalog

### Chain: Read-Validate-Transform-Write (RVTW)

**Use when:** Processing a file through a transformation pipeline.

```
1. Read source file
2. Validate content (check for error patterns per tool-validation.md)
3. Transform content (parse, restructure, extract)
4. Write output to target location
5. Verify output exists and is non-empty
```

**Used by:** `/polish-document`, `/generate-content`, content workflow

**Key principle:** Always validate between read and transform. Never transform unchecked input.

---

### Chain: Search-Aggregate-Report (SAR)

**Use when:** Scanning multiple files to produce a summary report.

```
1. Glob/Grep to find relevant files
2. Read each file (parallel if independent)
3. Extract relevant data points
4. Aggregate into structured output
5. Write report to target location
6. Archive previous report version (if applicable)
```

**Used by:** `/daily-scan`, `/improvement-audit`, `/metrics-scan`, `/workflow-review`, cron health check

**Key principle:** Archive before overwrite. Use `engineering/scripts/archive-report.sh` for the archival step.

---

### Chain: State-Check-Update-Confirm (SCUC)

**Use when:** Updating active state files (now.md, priorities.md, etc.).

```
1. Read current state file
2. Check what needs to change (compare to new information)
3. Update the specific section (Edit tool, not full rewrite)
4. Confirm the update is correct (re-read and verify)
5. Offer to commit
```

**Used by:** Completion Protocol, External Event Protocol, Contact Follow-Up Protocol

**Key principle:** Use Edit (surgical), not Write (full overwrite), for state files. This prevents clobbering concurrent changes from other sessions.

---

### Chain: Research-Draft-Review-Publish (RDRP)

**Use when:** Creating content that will be published or shared.

```
1. Research: Gather source material (web, codebase, existing docs)
2. Draft: Writer produces content applying writing-style.md
3. Review: Editor checks voice, accuracy, structure
4. Revise: Writer incorporates feedback (repeat 3-4 as needed)
5. Polish: Polisher formats for target platform
6. Publish: Post/schedule to platform
7. Track: Update channel-tracker.md and now.md
```

**Used by:** Content Workflow, `/write-content`, `/generate-content`

**Key principle:** Never skip the Editor step. Even for short content, the Editor checks voice consistency.

---

### Chain: Cron-Execute-Log-Notify (CELN)

**Use when:** Running automated cron jobs.

```
1. Log start time: echo "START $(date)" > /tmp/mega-os-$SKILL.log
2. Execute skill: timeout $LIMIT claude -p "..." --permission-mode auto >> log
3. Capture exit code: EXIT=$?
4. Log end time: echo "Exit: $EXIT at $(date)" >> log
5. Verify output: check target file modification date
6. Emit timing trace: append to timing.jsonl
7. Notify: send Telegram notification with status
```

**Used by:** All 14 cron jobs in crontab

**Key principle:** Every cron job follows this exact pattern. The timing trace (step 6) feeds IMP-008 metrics.

---

### Chain: Audit-Finding-Track-Resolve (AFTR)

**Use when:** An audit (pre- or post-execution) produces findings.

```
1. Auditor produces findings with severity ratings
2. Record each finding in active/audits.md (AUD-P### or AUD-X###)
3. Route findings to responsible agent
4. Responsible agent resolves (or acknowledges with timeline)
5. Update finding status in audits.md
6. If significant: Historian records in decisions.md
```

**Used by:** Auditor Checklist, Planning Workflow step 5, Technical Workflow step 10

**Key principle:** Findings are always recorded before being communicated. No verbal-only findings.

---

### Chain: Git-Stage-Verify-Commit (GSVC)

**Use when:** Committing changes to the repository.

```
1. git status — see all changes
2. git diff — review staged + unstaged
3. Stage specific files (never git add -A)
4. git diff --cached --stat — verify only intended files are staged
5. Compose commit message with scope prefix
6. Commit with Co-Authored-By trailer
7. git status — verify clean state
```

**Used by:** Commit & Push Policy, session close

**Key principle:** Never stage files you didn't modify in this session. Always verify before committing.

---

## How to Reference

In skills and workflow steps, reference chains by name:

> "Apply the CELN chain for cron execution with SKILL=improvement-audit and LIMIT=900"

> "Follow the SCUC chain to update now.md with the new task"

This creates a shared vocabulary and reduces duplication in skill definitions.
