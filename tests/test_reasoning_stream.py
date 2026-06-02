"""Tests for cli/reasoning_stream.py.

The suite drives the parser with synthetic JSONL fixtures so it runs
deterministically without a live autonomous daemon. It pins the event-type to
icon/style mapping, reward extraction, malformed-line tolerance and the
tail-window behaviour the dashboard relies on.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.reasoning_stream import (  # noqa: E402
    ReasoningEntry,
    _format_size,
    _truncate,
    event_to_entry,
    latest_reasoning,
    read_raw_events,
)


def _write_events(path: Path, events: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")


def test_read_raw_events_missing_file_returns_empty(tmp_path):
    assert read_raw_events(str(tmp_path / "nope.jsonl")) == []


def test_read_raw_events_skips_malformed_lines(tmp_path):
    target = tmp_path / "events.jsonl"
    target.write_text(
        '{"type": "STEP_START", "payload": {}}\nthis is not json\n\n{"type": "STEP_DONE", "payload": {}}\n',
        encoding="utf-8",
    )
    events = read_raw_events(str(target))
    assert [e["type"] for e in events] == ["STEP_START", "STEP_DONE"]


def test_read_raw_events_honours_limit_tail(tmp_path):
    target = tmp_path / "events.jsonl"
    _write_events(target, [{"type": "STEP_DONE", "payload": {"step": i}} for i in range(10)])
    events = read_raw_events(str(target), limit=3)
    assert [e["payload"]["step"] for e in events] == [7, 8, 9]


def test_event_to_entry_step_start_uses_reason_and_source():
    event = {
        "ts": "2026-06-02T01:29:03.056945+00:00",
        "type": "STEP_START",
        "payload": {
            "command": "lazynmap",
            "phase": "recon",
            "reason": "nmap full scan",
            "source": "bridge",
        },
    }
    entry = event_to_entry(event)
    assert isinstance(entry, ReasoningEntry)
    assert entry.icon == "▶"
    assert entry.ts == "01:29:03"
    assert entry.phase == "recon"
    assert entry.command == "lazynmap"
    assert "nmap full scan" in entry.summary
    assert "[bridge]" in entry.summary
    assert entry.reward is None


def test_event_to_entry_step_done_failure_flips_icon_and_style():
    event = {
        "type": "STEP_DONE",
        "payload": {"command": "x", "success": False, "phase": "enum"},
    }
    entry = event_to_entry(event)
    assert entry.icon == "✘"
    assert entry.style == "bold red"


def test_event_to_entry_extracts_reward():
    event = {
        "type": "STEP_DONE",
        "payload": {"command": "x", "success": True, "reward": 0.821, "output_size": 2048},
    }
    entry = event_to_entry(event)
    assert entry.reward == 0.821
    assert "2.0 KB" in entry.summary


def test_event_to_entry_metrics_skip_renders_success_rate():
    event = {
        "type": "METRICS_BIAS_SKIP",
        "payload": {"command": "lazyburp", "stats": {"success_rate": 0.0}},
    }
    entry = event_to_entry(event)
    assert entry.icon == "⊘"
    assert "success 0%" in entry.summary


def test_event_to_entry_unknown_type_falls_back():
    entry = event_to_entry({"type": "WHATEVER", "payload": {"message": "hello"}})
    assert entry.icon == "·"
    assert entry.summary == "hello"


def test_event_to_entry_handles_non_dict_payload():
    entry = event_to_entry({"type": "STEP_START", "payload": None})
    assert entry.command == ""
    assert entry.phase == ""


def test_format_size_threshold():
    assert _format_size(512) == "512 B"
    assert _format_size(2048) == "2.0 KB"


def test_truncate_adds_ellipsis():
    assert _truncate("abcdef", 4) == "abc…"
    assert _truncate("abc", 4) == "abc"


def test_latest_reasoning_end_to_end(tmp_path):
    target = tmp_path / "events.jsonl"
    _write_events(
        target,
        [
            {"type": "STEP_START", "payload": {"command": "ping", "phase": "recon", "reason": "go"}},
            {"type": "STEP_DONE", "payload": {"command": "ping", "success": True, "reward": 0.5}},
        ],
    )
    entries = latest_reasoning(str(target))
    assert [e.kind for e in entries] == ["STEP_START", "STEP_DONE"]
    assert entries[-1].reward == 0.5
