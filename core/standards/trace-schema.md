# Trace Schema Standard

Defines the JSONL trace format for capturing workflow execution data. Traces are append-only, machine-readable records that enable data-driven evaluation and routing optimization.

**Origin:** OpenJarvis audit IMP-004 (2026-03-27)

---

## Trace File Locations

| File | Purpose | Retention |
|------|---------|-----------|
| `core/history/traces/workflow-traces.jsonl` | Workflow-level execution traces | 30 days rolling |
| `core/history/traces/event-log.jsonl` | System events (IMP-009) | 30 days rolling |
| `core/history/traces/timing.jsonl` | Skill/workflow execution timing (IMP-008) | 30 days rolling |
| `core/history/traces/archive/` | Archived traces older than 30 days | Summary stats only |

All trace files are gitignored (ephemeral operational data, not framework or user content).

---

## Workflow Trace Schema

Each line in `workflow-traces.jsonl` is a JSON object:

```json
{
  "ts": "2026-03-27T14:30:00Z",
  "workflow": "technical",
  "step": "engineer",
  "step_number": 5,
  "action": "implement",
  "input_summary": "Add capability profiles to agent definitions",
  "output_summary": "39 agent files updated with capabilities field",
  "status": "success",
  "files_changed": 39,
  "duration_ms": 45000,
  "session_id": "abc123",
  "notes": ""
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ts` | ISO 8601 | Yes | Timestamp when step completed |
| `workflow` | string | Yes | Workflow type: planning, technical, business, incident, knowledge, content, site-build, evolution |
| `step` | string | Yes | Agent name that executed the step |
| `step_number` | int | Yes | Position in workflow sequence (1-indexed) |
| `action` | string | Yes | What the agent did: plan, design, implement, review, test, document, evaluate, route, audit |
| `input_summary` | string | Yes | Brief description of what was handed to this step (max 200 chars) |
| `output_summary` | string | Yes | Brief description of what this step produced (max 200 chars) |
| `status` | string | Yes | success, failure, skipped, escalated |
| `files_changed` | int | No | Number of files modified (0 for read-only steps) |
| `duration_ms` | int | No | Wall-clock time in milliseconds (when timing available) |
| `session_id` | string | No | Claude Code session identifier (if available) |
| `notes` | string | No | Free-form notes (errors, escalation reasons, etc.) |

---

## Event Log Schema

Each line in `event-log.jsonl` is a JSON object:

```json
{
  "ts": "2026-03-27T14:30:00Z",
  "event": "workflow_start",
  "workflow": "technical",
  "detail": "OpenJarvis adoption Pass 4",
  "severity": "info"
}
```

### Event Types

| Event | When | Severity |
|-------|------|----------|
| `workflow_start` | Workflow begins | info |
| `workflow_end` | Workflow completes | info |
| `workflow_fail` | Workflow fails | warning |
| `agent_escalation` | Agent escalates to another | warning |
| `gate_pass` | Quality gate passed (QA, Reviewer, Security) | info |
| `gate_fail` | Quality gate failed | warning |
| `state_update` | Active state file modified | info |
| `decision` | Significant decision recorded | info |
| `cron_run` | Cron job executed | info |
| `cron_fail` | Cron job failed | error |

---

## Timing Schema

Each line in `timing.jsonl` is a JSON object:

```json
{
  "ts": "2026-03-27T14:30:00Z",
  "skill": "improvement-audit",
  "duration_s": 142.5,
  "exit_code": 0,
  "source": "cron"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ts` | ISO 8601 | Yes | When execution started |
| `skill` | string | Yes | Skill or workflow name |
| `duration_s` | float | Yes | Wall-clock seconds |
| `exit_code` | int | No | Process exit code (for cron/scripted runs) |
| `source` | string | Yes | How it was triggered: cron, manual, workflow |

---

## Retention Policy

- **Active window:** 30 days of raw JSONL traces
- **Archival:** Cron runs weekly, computes summary statistics for traces older than 30 days, writes to `core/history/traces/archive/YYYY-WNN-summary.json`
- **Summary format:** Aggregated counts by workflow type, success rates, average durations, top failure reasons
- **Raw traces older than 30 days:** Deleted after archival

---

## What to Trace

Trace **workflow-level steps** (agent handoffs, routing decisions, quality gate outcomes). Do NOT trace:
- Individual tool calls within a step
- File reads/writes (too noisy)
- Intermediate reasoning

The goal is a clean signal about workflow health, not a replay log.

---

## How to Emit Traces

### From Python scripts (cron, engineering tools)

```python
import json, datetime, pathlib

TRACE_FILE = pathlib.Path("core/history/traces/workflow-traces.jsonl")

def emit_trace(workflow, step, step_number, action, input_summary, output_summary, status, **kwargs):
    entry = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "workflow": workflow,
        "step": step,
        "step_number": step_number,
        "action": action,
        "input_summary": input_summary[:200],
        "output_summary": output_summary[:200],
        "status": status,
        **{k: v for k, v in kwargs.items() if v is not None}
    }
    with TRACE_FILE.open("a") as f:
        f.write(json.dumps(entry) + "\n")
```

### From bash (cron wrappers, timing hooks)

```bash
echo '{"ts":"'"$(date -u +%FT%TZ)"'","skill":"'"$SKILL"'","duration_s":'"$DURATION"',"exit_code":'"$EXIT"',"source":"cron"}' >> core/history/traces/timing.jsonl
```

### From workflow orchestration (Claude sessions)

Agents append traces at the end of their step in the workflow. The orchestrating context (main session or team coordinator) is responsible for ensuring traces are emitted. This is voluntary — if a session doesn't emit traces, the system still functions. Traces are additive value, not a hard dependency.

---

## Querying Traces

For ad-hoc analysis: `grep` or `jq` over JSONL files.

For structured queries: `engineering/scripts/index-memory.py` indexes traces into the SQLite FTS5 database (IMP-005), enabling full-text search across trace data.

Example: `jq 'select(.status == "failure")' core/history/traces/workflow-traces.jsonl`
