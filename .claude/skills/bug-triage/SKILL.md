---
name: bug-triage
description: Use when triaging a bug — systematically gather information, classify severity, identify root cause, and route to the appropriate specialist.
user_invocable: true
---

# Bug Triage

Systematically gather information, classify severity, identify root cause, and route to the appropriate specialist.

## Steps

1. **Gather information**
   - What is the reported behavior?
   - What is the expected behavior?
   - What environment/context does it occur in?
   - Read relevant error logs, stack traces, or screenshots if provided.

2. **Reproduce (if possible)**
   - Attempt to reproduce the issue based on the report.
   - Note reproduction steps, frequency, and conditions.
   - If not reproducible, document what was tried.

3. **Classify severity**
   - **P0 — Critical:** System down, data loss, security breach. Immediate action required.
   - **P1 — High:** Major feature broken, no workaround. Address within current session.
   - **P2 — Medium:** Feature degraded, workaround exists. Schedule for near-term fix.
   - **P3 — Low:** Minor issue, cosmetic, or edge case. Add to backlog.

4. **Root cause hypothesis**
   - Based on available evidence, identify the most likely area of the codebase.
   - Distinguish symptom from cause.
   - Note confidence level (confirmed, likely, speculative).

5. **Route to specialist**
   - P0/P1: Invoke the Debugger agent immediately.
   - Security-related: Route to Security-Expert.
   - Infrastructure/deployment: Route to DevOps.
   - General code: Route to Engineer.

6. **Document**
   - Log the bug in `active/inbox.md` with date, description, severity, and owner.
   - For P0/P1, also note in `active/blockers.md`.
   - Update `active/now.md` if this changes current focus.
