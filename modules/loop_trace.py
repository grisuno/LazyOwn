"""Loop trace — standalone interactive HTML for one autonomous run.

Merges the audit trail (commands, judge and opsec verdicts, detection
probabilities), the activity log (worker decisions), the LLM usage log
(member calls and errors) and the token ledger into one self-contained
HTML file with a timeline and expandable event details. No external
assets: the artefact opens offline from ``sessions/traces/``.

>>> from modules.loop_trace import write_trace
>>> path = write_trace("t0001")
>>> path.endswith(".html")
True
"""

from __future__ import annotations

import html
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from modules.report_engagement import (
    LAZY_DIR,
    MAX_OUTPUT_TAIL,
    _read_jsonl,
    aggregate_metrics,
    collect_audit_rows,
    collect_loop_runs,
    iso_from_ts,
)

TRACES_DIRNAME = "sessions"
TRACES_SUBDIR = "traces"
MAX_EVENTS = 400
MAX_DETAIL = 1600

_KIND_CLASS = {
    "command_ok": "ok",
    "command_fail": "fail",
    "command_denied": "deny",
    "llm_ok": "llm",
    "llm_error": "error",
    "round": "round",
    "worker": "worker",
    "finding": "finding",
}

_KIND_LABEL = {
    "command_ok": "command",
    "command_fail": "command",
    "command_denied": "command",
    "llm_ok": "llm",
    "llm_error": "llm",
    "round": "round",
    "worker": "decision",
    "finding": "finding",
}


def build_trace(task_id: str, max_events: int = MAX_EVENTS) -> dict[str, Any]:
    """Merge every signal for one loop task into a trace dictionary.

    Args:
        task_id: Loop task identifier.
        max_events: Maximum timeline events.

    Returns:
        Mapping with ``task_id``, ``summary``, ``metrics``, ``events``
        and ``llm_calls``.
    """
    run = _summary_for(task_id)
    events = _timeline_events(task_id, max_events)
    llm_calls = _llm_calls(task_id)
    metrics = aggregate_metrics([run]) if run.commands else {}
    return {
        "task_id": task_id,
        "summary": run.as_dict(),
        "steps": run.steps,
        "metrics": metrics,
        "events": events,
        "llm_calls": llm_calls,
    }


def _summary_for(task_id: str) -> Any:
    """Find the summary row for one task.

    Args:
        task_id: Loop task identifier.

    Returns:
        LoopRunSummary; an empty summary when the task has no audit trail.
    """
    for run in collect_loop_runs():
        if run.task_id == task_id:
            return run
    return _empty_summary(task_id)


def _empty_summary(task_id: str) -> Any:
    """Build a zeroed summary for tasks without history.

    Args:
        task_id: Loop task identifier.

    Returns:
        LoopRunSummary with default counters.
    """
    from modules.report_engagement import LoopRunSummary

    return LoopRunSummary(task_id=task_id, goal="", status="unknown", target="")


def _event_store_rows(task_id: str) -> list[dict[str, Any]]:
    """Read EventStore rows recorded for one task.

    Args:
        task_id: Loop task identifier.

    Returns:
        Rows mapped into timeline events (findings, captures).
    """
    try:
        from modules.loop.event_store import EventStore

        rows = EventStore().events(task_id=task_id, limit=MAX_EVENTS)
    except Exception:
        return []
    events = []
    for row in rows:
        events.append(
            {
                "ts": float(row.get("ts", 0.0) or 0.0),
                "kind": "finding",
                "title": f"{row.get('kind', '')}: {row.get('title', '')}",
                "detail": str(row.get("payload", ""))[:MAX_DETAIL],
            }
        )
    return events


def _timeline_events(task_id: str, max_events: int) -> list[dict[str, Any]]:
    """Build the merged timeline: commands, rounds, decisions.

    Args:
        task_id: Loop task identifier.
        max_events: Maximum events returned.

    Returns:
        Chronological event list with ``ts``, ``kind``, ``title`` and
        ``detail`` keys.
    """
    events: list[dict[str, Any]] = []
    for row in collect_audit_rows(task_id):
        kind = str(row.get("kind", ""))
        ts = float(row.get("ts", 0.0) or 0.0)
        if kind == "command":
            ok = bool(row.get("ok"))
            denied = str(row.get("judge_action", "")) == "deny" or str(row.get("opsec_gate", "")) == "deny"
            trace_kind = "command_denied" if denied else ("command_ok" if ok else "command_fail")
            detail_lines = [
                f"worker: {row.get('worker', '')}",
                f"step: {row.get('step', '')}",
                f"judge: {row.get('judge_action', '')} ({row.get('judge_source', '')})",
                f"opsec gate: {row.get('opsec_gate', '')}",
                f"detection prob: {row.get('detection_prob', '')}",
                f"duration: {row.get('duration', '')}s",
                "output: " + str(row.get("output_tail", ""))[:MAX_DETAIL],
            ]
            events.append(
                {
                    "ts": ts,
                    "kind": trace_kind,
                    "title": str(row.get("command", "")),
                    "detail": "\n".join(line for line in detail_lines if line.split(": ", 1)[-1]),
                }
            )
        elif kind == "run_start":
            events.append(
                {
                    "ts": ts,
                    "kind": "round",
                    "title": f"run start: {row.get('goal', '')}",
                    "detail": f"rounds={row.get('rounds')} workers={row.get('workers')} mode={row.get('mode')}",
                }
            )
    for row in _read_jsonl(LAZY_DIR / f"activity_{task_id}.jsonl"):
        kind = str(row.get("kind", ""))
        if kind in ("decompose", "plan", "intent", "steer", "pause", "abort", "handover"):
            events.append(
                {
                    "ts": float(row.get("ts", 0.0) or 0.0),
                    "kind": "worker",
                    "title": f"{row.get('worker', '')}: {row.get('kind', '')}",
                    "detail": str(row.get("text", ""))[:MAX_DETAIL],
                }
            )
    events.extend(_event_store_rows(task_id))
    events.sort(key=lambda item: item["ts"])
    return events[:max_events]


def _llm_calls(task_id: str) -> list[dict[str, Any]]:
    """Extract LLM usage rows relevant to one task window.

    Args:
        task_id: Loop task identifier.

    Returns:
        Calls between the task's first and last activity timestamps.
    """
    run = _summary_for(task_id)
    calls = []
    path = LAZY_DIR / "llm_usage.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    for call in data.get("calls") or []:
        ts = float(call.get("ts", 0.0) or 0.0)
        if run.first_ts and (ts < run.first_ts - 1 or ts > run.last_ts + 1):
            continue
        calls.append(
            {
                "ts": ts,
                "member": str(call.get("member", "")),
                "ok": bool(call.get("ok")),
                "text": str(call.get("text", ""))[:MAX_OUTPUT_TAIL],
            }
        )
    return calls


def _token_usage(task_id: str) -> dict[str, int]:
    """Read the persisted token ledger for one task.

    Args:
        task_id: Loop task identifier.

    Returns:
        Mapping with ``prompt_tokens`` and ``completion_tokens``.
    """
    try:
        from modules.loop.tokens import TokenLedger

        usage = TokenLedger().usage(task_id)
    except Exception:
        return {"prompt_tokens": 0, "completion_tokens": 0}
    return usage


def _esc(text: Any) -> str:
    """Escape text for HTML output.

    Args:
        text: Raw value.

    Returns:
        Escaped string.
    """
    return html.escape(str(text or ""))


def render_html(trace: dict[str, Any]) -> str:
    """Render the standalone HTML trace.

    Args:
        trace: Trace built by :func:`build_trace`.

    Returns:
        Complete HTML document string.
    """
    summary = trace["summary"]
    tokens = _token_usage(summary["task_id"])
    event_rows = []
    for event in trace["events"]:
        css = _KIND_CLASS.get(event["kind"], "worker")
        label = _KIND_LABEL.get(event["kind"], event["kind"])
        event_rows.append(
            f"<div class='event {css}'>"
            f"<div class='head'><span class='time'>{_esc(iso_from_ts(event['ts'])[11:19])}</span>"
            f"<span class='badge'>{_esc(label)}</span>"
            f"<span class='title'>{_esc(event['title'][:180])}</span></div>"
            f"<details><summary>detail</summary><pre>{_esc(event['detail'])}</pre></details>"
            "</div>"
        )
    llm_rows = "".join(
        f"<div class='event {'llm' if call['ok'] else 'error'}'>"
        f"<div class='head'><span class='time'>{_esc(iso_from_ts(call['ts'])[11:19])}</span>"
        f"<span class='badge'>{'ok' if call['ok'] else 'error'}</span>"
        f"<span class='title'>{_esc(call['member'])}</span></div>"
        f"<pre>{_esc(call['text'][:400])}</pre>"
        "</div>"
        for call in trace["llm_calls"]
    )
    steps_html = "".join(f"<li>{_esc(step)}</li>" for step in trace["steps"])
    metrics = trace["metrics"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>LazyOwn loop trace {trace["task_id"]}</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 24px; background: #0d1117; color: #c9d1d9; }}
h1 {{ color: #58a6ff; }}
.cards {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0; }}
.card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 18px; }}
.card .n {{ font-size: 22px; font-weight: bold; color: #58a6ff; }}
.card .l {{ font-size: 12px; color: #8b949e; }}
.event {{ border-left: 3px solid #30363d; margin: 6px 0; padding: 6px 12px; background: #161b22; border-radius: 4px; }}
.event.ok {{ border-left-color: #3fb950; }}
.event.fail {{ border-left-color: #f85149; }}
.event.deny {{ border-left-color: #d29922; }}
.event.llm {{ border-left-color: #a371f7; }}
.event.error {{ border-left-color: #f85149; }}
.event.round {{ border-left-color: #58a6ff; }}
.event.worker {{ border-left-color: #39c5cf; }}
.event.finding {{ border-left-color: #e3b341; }}
.head {{ display: flex; gap: 10px; align-items: baseline; }}
.time {{ color: #8b949e; font-size: 12px; min-width: 60px; }}
.badge {{ font-size: 11px; background: #21262d; border: 1px solid #30363d; border-radius: 10px; padding: 1px 8px; }}
.title {{ font-size: 14px; }}
details pre {{ white-space: pre-wrap; font-size: 12px; color: #8b949e; margin: 4px 0 0 70px; }}
details summary {{ cursor: pointer; color: #58a6ff; font-size: 12px; margin-left: 70px; }}
h2 {{ border-bottom: 1px solid #30363d; padding-bottom: 4px; }}
</style>
</head>
<body>
<h1>LazyOwn loop trace — {trace["task_id"]}</h1>
<p>Goal: <b>{_esc(summary["goal"])}</b> &middot; Target: <b>{_esc(summary["target"])}</b> &middot;
Status: <b>{_esc(summary["status"])}</b></p>
<div class="cards">
<div class="card"><div class="n">{summary["rounds"]}</div><div class="l">rounds</div></div>
<div class="card"><div class="n">{summary["commands"]}</div><div class="l">commands</div></div>
<div class="card"><div class="n">{summary["ok_rate"]:.0%}</div><div class="l">success rate</div></div>
<div class="card"><div class="n">{summary["blocked"]}</div><div class="l">blocked by gates</div></div>
<div class="card"><div class="n">{summary["detection_avg"]:.2f}</div><div class="l">avg detection prob</div></div>
<div class="card"><div class="n">{tokens.get("prompt_tokens", 0) + tokens.get("completion_tokens", 0)}</div><div class="l">tokens (ledger)</div></div>
<div class="card"><div class="n">{summary["findings"]}</div><div class="l">findings</div></div>
<div class="card"><div class="n">{metrics.get("detection_avg", 0):.2f}</div><div class="l">engagement det. avg</div></div>
</div>
<h2>Steps covered</h2><ul>{steps_html or "<li>none recorded</li>"}</ul>
<h2>Timeline</h2>
{"".join(event_rows) or "<p>No events recorded.</p>"}
<h2>LLM calls</h2>
{"".join(llm_rows) or "<p>No LLM calls in this window.</p>"}
</body>
</html>
"""


def write_trace(task_id: str, out_path: Path | None = None) -> str:
    """Build and write the trace artefact for one task.

    Args:
        task_id: Loop task identifier.
        out_path: Override for the output path.

    Returns:
        Path to the written HTML file; empty string on failure.
    """
    out_dir = Path(TRACES_DIRNAME) / TRACES_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_path or out_dir / f"trace_{task_id}.html"
    trace = build_trace(task_id)
    target.write_text(render_html(trace), encoding="utf-8")
    return str(target)


def list_tasks_with_traces() -> list[str]:
    """List loop task ids that have an audit trail.

    Returns:
        Sorted task ids.
    """
    return sorted(path.stem.replace("audit_", "", 1) for path in LAZY_DIR.glob("audit_*.jsonl"))


def trace_index_html() -> str:
    """Render the index page linking every task trace.

    Returns:
        HTML document listing tasks with links to their trace files.
    """
    rows = "".join(f"<li><a href='trace_{task_id}.html'>{task_id}</a></li>" for task_id in list_tasks_with_traces())
    generated = datetime.now(UTC).isoformat()
    return (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        f"<title>LazyOwn loop traces</title></head><body>"
        "<h1>LazyOwn loop traces</h1>"
        f"<p>Generated {generated}</p><ul>{rows}</ul></body></html>"
    )


def write_index() -> str:
    """Write the trace index page.

    Returns:
        Path to the written index file.
    """
    out_dir = Path(TRACES_DIRNAME) / TRACES_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "index.html"
    index_path.write_text(trace_index_html(), encoding="utf-8")
    return str(index_path)
