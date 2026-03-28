#!/usr/bin/env python3
"""Trace utility library for Mega-OS.

Emits structured JSONL traces for workflow steps, events, and timing.
Schema: core/standards/trace-schema.md

Usage:
    from trace_utils import emit_workflow_trace, emit_event, emit_timing
"""

import fcntl
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_TRACE_DIR = _REPO_ROOT / "core" / "history" / "traces"

_WORKFLOW_FILE = _TRACE_DIR / "workflow-traces.jsonl"
_EVENT_FILE = _TRACE_DIR / "event-log.jsonl"
_TIMING_FILE = _TRACE_DIR / "timing.jsonl"


def _utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append_jsonl(filepath, record):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, separators=(",", ":")) + "\n"
    fd = os.open(str(filepath), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        os.write(fd, line.encode("utf-8"))
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def emit_workflow_trace(workflow, step, step_number, action, input_summary,
                        output_summary, status, duration_s=None, error=None,
                        metadata=None):
    record = {
        "ts": _utc_now(),
        "trace_id": str(uuid.uuid4()),
        "workflow": workflow,
        "step": step,
        "step_number": step_number,
        "action": action,
        "input_summary": input_summary[:200],
        "output_summary": output_summary[:200],
        "status": status,
    }
    if duration_s is not None:
        record["duration_s"] = round(duration_s, 3)
    if error is not None:
        record["error"] = error
    if metadata:
        record["metadata"] = metadata
    _append_jsonl(_WORKFLOW_FILE, record)
    return record


def emit_event(event, workflow, detail, severity="info", metadata=None):
    record = {
        "ts": _utc_now(),
        "event_id": str(uuid.uuid4()),
        "event": event,
        "workflow": workflow,
        "detail": detail,
        "severity": severity,
    }
    if metadata:
        record["metadata"] = metadata
    _append_jsonl(_EVENT_FILE, record)
    return record


def emit_timing(skill, duration_s, exit_code=None, source="manual",
                metadata=None):
    record = {
        "ts": _utc_now(),
        "timing_id": str(uuid.uuid4()),
        "skill": skill,
        "duration_s": round(duration_s, 3),
        "source": source,
    }
    if exit_code is not None:
        record["exit_code"] = exit_code
    if metadata:
        record["metadata"] = metadata
    _append_jsonl(_TIMING_FILE, record)
    return record
