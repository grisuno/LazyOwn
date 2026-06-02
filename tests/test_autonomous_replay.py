"""Tests for ``skills/autonomous_replay.py``.

The replay layer must:

* Parse ``autonomous_events.jsonl`` and ignore malformed lines.
* Slice the event stream inclusively by event id.
* Trace a STEP_START sequence without re-executing commands.
* Surface a divergence when the recorded ``decision_seed`` does not
  match the recomputed one (introduced by ``compute_decision_seed``
  in ``skills/autonomous_daemon.py``).
* Execute commands through an injected runner without depending on the
  daemon module.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest


_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "skills"))

from skills.autonomous_replay import (  # noqa: E402
    EventLogReader,
    REPLAY_MODE_EXECUTE,
    REPLAY_MODE_TRACE,
    ReplayDispatcher,
    ReplayReport,
    SUPPORTED_REPLAY_MODES,
    replay,
)
from skills.autonomous_daemon import compute_decision_seed  # noqa: E402


def _event(
    event_id: str,
    objective_id: str,
    step: int,
    command: str,
    source: str = "fallback",
    seed_override: str = None,
) -> Dict[str, Any]:
    seed = (
        seed_override
        if seed_override is not None
        else compute_decision_seed(objective_id, step, source)
    )
    return {
        "id": event_id,
        "ts": "2026-06-01T00:00:00+00:00",
        "type": "STEP_START",
        "severity": "info",
        "payload": {
            "objective_id": objective_id,
            "step": step,
            "command": command,
            "source": source,
            "reason": f"recorded reason for {command}",
            "decision_seed": seed,
        },
    }


def _write_jsonl(path: Path, events: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event) + "\n")


def test_event_log_reader_returns_empty_when_missing(tmp_path: Path) -> None:
    """A missing file must yield an empty list, not raise."""

    reader = EventLogReader(tmp_path / "absent.jsonl")
    assert reader.read() == []


def test_event_log_reader_skips_malformed_lines(tmp_path: Path) -> None:
    """Truncated or invalid JSON lines are skipped silently."""

    path = tmp_path / "events.jsonl"
    path.write_text("\n".join([
        json.dumps(_event("aa", "obj-1", 0, "ping")),
        "{not json",
        json.dumps(_event("bb", "obj-1", 1, "lazynmap")),
    ]) + "\n")
    events = EventLogReader(path).read()
    assert [e["id"] for e in events] == ["aa", "bb"]


def test_slice_is_inclusive_on_both_bounds(tmp_path: Path) -> None:
    """Bounds match recorded ids and are returned inclusively."""

    path = tmp_path / "events.jsonl"
    events = [
        _event("a", "obj", 0, "ping"),
        _event("b", "obj", 1, "lazynmap"),
        _event("c", "obj", 2, "auto_populate"),
    ]
    _write_jsonl(path, events)
    reader = EventLogReader(path)
    raw = reader.read()
    sliced = reader.slice(raw, from_event_id="b", to_event_id="c")
    assert [e["id"] for e in sliced] == ["b", "c"]


def test_trace_returns_one_step_per_event(tmp_path: Path) -> None:
    """Trace mode lists each STEP_START in order with no divergences."""

    path = tmp_path / "events.jsonl"
    _write_jsonl(path, [
        _event("aa", "obj-x", 0, "ping"),
        _event("bb", "obj-x", 1, "lazynmap"),
    ])
    report = ReplayDispatcher(reader=EventLogReader(path)).trace()
    assert isinstance(report, ReplayReport)
    assert report.mode == REPLAY_MODE_TRACE
    assert report.events_seen == 2
    assert [s.command for s in report.steps] == ["ping", "lazynmap"]
    assert report.divergences == []


def test_trace_detects_decision_seed_divergence(tmp_path: Path) -> None:
    """A bad recorded seed produces exactly one divergence entry."""

    path = tmp_path / "events.jsonl"
    _write_jsonl(path, [
        _event("aa", "obj-x", 0, "ping", seed_override="deadbeefdeadbeef"),
    ])
    report = ReplayDispatcher(reader=EventLogReader(path)).trace()
    assert len(report.divergences) == 1
    divergence = report.divergences[0]
    assert divergence.field == "decision_seed"
    assert divergence.recorded == "deadbeefdeadbeef"
    assert (
        divergence.recomputed
        == compute_decision_seed("obj-x", 0, "fallback")
    )


def test_execute_runs_commands_through_injected_runner(tmp_path: Path) -> None:
    """Execute mode delegates to the supplied runner and captures output."""

    path = tmp_path / "events.jsonl"
    _write_jsonl(path, [
        _event("aa", "obj-x", 0, "ping"),
        _event("bb", "obj-x", 1, "lazynmap"),
    ])

    class _Runner:
        def __init__(self) -> None:
            self.calls: List[str] = []

        def run(self, command: str, timeout: int) -> str:
            self.calls.append(command)
            return f"output of {command}"

    runner = _Runner()
    report = ReplayDispatcher(reader=EventLogReader(path)).execute(
        runner=runner,
    )
    assert report.mode == REPLAY_MODE_EXECUTE
    assert runner.calls == ["ping", "lazynmap"]
    assert all(step.replayed_success for step in report.steps)
    assert report.steps[0].replayed_output_snippet == "output of ping"


def test_execute_marks_runner_errors_as_failure(tmp_path: Path) -> None:
    """A runner that returns an error-like string flips success to False."""

    path = tmp_path / "events.jsonl"
    _write_jsonl(path, [_event("aa", "obj-x", 0, "ping")])

    class _Runner:
        def run(self, command: str, timeout: int) -> str:
            return "[timeout] ping exceeded"

    report = ReplayDispatcher(reader=EventLogReader(path)).execute(
        runner=_Runner(),
    )
    assert report.steps[0].replayed_success is False


def test_replay_convenience_returns_dict(tmp_path: Path) -> None:
    """The top-level ``replay`` helper returns a JSON-serialisable dict."""

    path = tmp_path / "events.jsonl"
    _write_jsonl(path, [_event("aa", "obj-x", 0, "ping")])
    report = replay(events_path=path)
    assert report["mode"] == REPLAY_MODE_TRACE
    assert report["events_seen"] == 1
    json.dumps(report)


def test_replay_rejects_unknown_mode(tmp_path: Path) -> None:
    """An unsupported mode raises ``ValueError``."""

    path = tmp_path / "events.jsonl"
    _write_jsonl(path, [_event("aa", "obj-x", 0, "ping")])
    with pytest.raises(ValueError):
        replay(events_path=path, mode="invalid")


def test_supported_modes_constant() -> None:
    """The constant exposes both valid modes for external validators."""

    assert set(SUPPORTED_REPLAY_MODES) == {REPLAY_MODE_TRACE, REPLAY_MODE_EXECUTE}


def test_step_skips_events_without_command(tmp_path: Path) -> None:
    """Events with no ``command`` field are dropped from the trace."""

    path = tmp_path / "events.jsonl"
    bad = {
        "id": "cc",
        "ts": "2026-06-01T00:00:00+00:00",
        "type": "STEP_START",
        "severity": "info",
        "payload": {"objective_id": "obj"},
    }
    _write_jsonl(path, [
        bad,
        _event("aa", "obj", 0, "ping"),
    ])
    report = ReplayDispatcher(reader=EventLogReader(path)).trace()
    assert [s.command for s in report.steps] == ["ping"]
    assert report.events_seen == 2
