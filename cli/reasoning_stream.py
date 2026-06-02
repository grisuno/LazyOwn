"""Operator-facing view over the autonomous daemon decision log.

The autonomous daemon (``skills/autonomous_daemon.py``) appends structured
events to ``sessions/autonomous_events.jsonl`` through its ``_emit`` helper.
Every event is a JSON object with the shape::

    {"id": "...", "ts": "<iso8601>", "type": "STEP_START",
     "severity": "info", "payload": {...}}

This module turns that raw stream into a compact, human-readable sequence of
:class:`ReasoningEntry` records so the dashboard can render *what the daemon is
thinking* in real time: the command it chose, the phase, the selector that
produced the decision, the rationale and the reinforcement-learning reward.

The module performs no rendering and imports nothing from ``lazyown.py`` or
``lazyc2.py``; it only reads the JSONL log. This keeps it unit-testable and
reusable by the Textual dashboard, the web dashboard or any other consumer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_EVENTS_FILE: str = "sessions/autonomous_events.jsonl"
DEFAULT_LIMIT: int = 12
SUMMARY_MAX_LEN: int = 60
COMMAND_MAX_LEN: int = 28
BYTES_PER_KB: int = 1024
KB_DISPLAY_THRESHOLD: int = 1024
TIME_SLICE_START: int = 11
TIME_SLICE_END: int = 19

_DEFAULT_ICON: str = "·"
_DEFAULT_STYLE: str = "dim white"

_EVENT_STYLES: dict[str, tuple[str, str]] = {
    "OBJECTIVE_START": ("◆", "bold magenta"),
    "OBJECTIVE_DONE": ("◇", "magenta"),
    "ENGAGE_START": ("◆", "bold magenta"),
    "ENGAGE_DONE": ("◇", "magenta"),
    "STEP_START": ("▶", "bold yellow"),
    "STEP_DONE": ("✔", "bold green"),
    "STEP_SKIPPED": ("⊘", "dim yellow"),
    "METRICS_BIAS_SKIP": ("⊘", "dim yellow"),
    "COMMAND_VETOED": ("⛒", "bold red"),
    "APPROVAL_REQUESTED": ("?", "bold cyan"),
    "APPROVAL_DECIDED": ("✓", "cyan"),
    "CREDENTIAL_FOUND": ("✦", "bold green"),
    "HIGH_VALUE": ("★", "bold green"),
    "PHASE_ADVANCE": ("⇒", "bold blue"),
    "PHASE_CHANGE": ("⇒", "bold blue"),
    "OS_DETECTED": ("◉", "blue"),
    "STUCK_LOOP": ("↻", "bold red"),
    "DAEMON_PAUSED": ("‖", "dim white"),
    "DAEMON_RESUMED": ("▷", "green"),
}

_FAILURE_STYLE: str = "bold red"
_FAILURE_ICON: str = "✘"


@dataclass(frozen=True)
class ReasoningEntry:
    """One human-readable line in the daemon reasoning stream.

    Attributes:
        ts: Wall-clock ``HH:MM:SS`` slice of the event timestamp.
        kind: Canonical event type as emitted by the daemon.
        icon: Single-glyph marker used by the renderer.
        style: Rich style string for the marker and command.
        phase: Kill-chain phase the event belongs to, empty if unknown.
        command: Command associated with the event, empty if not applicable.
        summary: Compact rationale or outcome description.
        reward: Reinforcement-learning reward for the step, ``None`` when the
            event carries no reward signal.
    """

    ts: str
    kind: str
    icon: str
    style: str
    phase: str
    command: str
    summary: str
    reward: float | None


def read_raw_events(path: str = DEFAULT_EVENTS_FILE, limit: int = DEFAULT_LIMIT) -> list[dict[str, Any]]:
    """Return the last ``limit`` well-formed events from the JSONL log.

    Malformed lines are skipped silently so a single corrupt write never
    breaks the dashboard. The newest event is last in the returned list.

    Args:
        path: Path to the autonomous events JSONL file.
        limit: Maximum number of events to return from the tail.

    Returns:
        A list of decoded event dictionaries, oldest first.
    """
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []
    events: list[dict[str, Any]] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            decoded = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(decoded, dict):
            events.append(decoded)
    if limit > 0:
        return events[-limit:]
    return events


def _format_time(ts: str) -> str:
    """Extract an ``HH:MM:SS`` slice from an ISO-8601 timestamp."""
    if len(ts) >= TIME_SLICE_END:
        return ts[TIME_SLICE_START:TIME_SLICE_END]
    return ts


def _format_size(num_bytes: int) -> str:
    """Render a byte count as ``B`` or ``KB`` without external deps."""
    if num_bytes >= KB_DISPLAY_THRESHOLD:
        return f"{num_bytes / BYTES_PER_KB:.1f} KB"
    return f"{num_bytes} B"


def _truncate(text: str, limit: int) -> str:
    """Trim ``text`` to ``limit`` characters with an ellipsis marker."""
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "…"


def _summarize(kind: str, payload: dict[str, Any]) -> str:
    """Build a compact rationale string for an event payload."""
    message = str(payload.get("message") or "").strip()
    reason = str(payload.get("reason") or "").strip()
    source = str(payload.get("source") or "").strip()

    if kind == "STEP_START":
        base = reason or message or "decision"
        return _truncate(f"{base} [{source}]" if source else base, SUMMARY_MAX_LEN)
    if kind == "STEP_DONE":
        size = payload.get("output_size")
        findings = payload.get("findings_count")
        parts: list[str] = []
        if isinstance(findings, int) and findings > 0:
            parts.append(f"{findings} finding(s)")
        if isinstance(size, int):
            parts.append(_format_size(size))
        return _truncate(" · ".join(parts) or message or "done", SUMMARY_MAX_LEN)
    if kind == "METRICS_BIAS_SKIP":
        stats = payload.get("stats") or {}
        rate = stats.get("success_rate") if isinstance(stats, dict) else None
        if isinstance(rate, (int, float)):
            return _truncate(f"skipped — success {rate * 100:.0f}%", SUMMARY_MAX_LEN)
        return _truncate(reason or message or "skipped", SUMMARY_MAX_LEN)
    return _truncate(message or reason or source, SUMMARY_MAX_LEN)


def _extract_reward(payload: dict[str, Any]) -> float | None:
    """Return the step reward when present, else ``None``."""
    reward = payload.get("reward")
    if isinstance(reward, (int, float)):
        return float(reward)
    return None


def event_to_entry(event: dict[str, Any]) -> ReasoningEntry:
    """Convert a raw daemon event into a :class:`ReasoningEntry`.

    Args:
        event: A decoded event dictionary from the JSONL log.

    Returns:
        A populated :class:`ReasoningEntry`. Unknown event types fall back to
        a neutral marker so the stream never drops information.
    """
    kind = str(event.get("type") or "")
    payload = event.get("payload")
    if not isinstance(payload, dict):
        payload = {}

    icon, style = _EVENT_STYLES.get(kind, (_DEFAULT_ICON, _DEFAULT_STYLE))
    if kind == "STEP_DONE" and payload.get("success") is False:
        icon, style = _FAILURE_ICON, _FAILURE_STYLE

    command = _truncate(str(payload.get("command") or ""), COMMAND_MAX_LEN)

    return ReasoningEntry(
        ts=_format_time(str(event.get("ts") or "")),
        kind=kind,
        icon=icon,
        style=style,
        phase=str(payload.get("phase") or ""),
        command=command,
        summary=_summarize(kind, payload),
        reward=_extract_reward(payload),
    )


def latest_reasoning(path: str = DEFAULT_EVENTS_FILE, limit: int = DEFAULT_LIMIT) -> list[ReasoningEntry]:
    """Return the most recent daemon decisions as reasoning entries.

    Args:
        path: Path to the autonomous events JSONL file.
        limit: Maximum number of entries to return, newest last.

    Returns:
        A list of :class:`ReasoningEntry`, oldest first.
    """
    return [event_to_entry(event) for event in read_raw_events(path, limit)]
