"""Tests for ``modules/metrics.py``.

Covers the durable telemetry recorder added to surface command duration,
success rate, p95 and top failures. The in-memory
:class:`MetricsRegistry` used by the C2 stack is also exercised so any
future refactor that breaks the existing Prometheus path is caught here.
"""

from __future__ import annotations

import json
import sys
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.metrics import (  # noqa: E402
    MetricRecord,
    MetricsAggregator,
    MetricsRecorder,
    MetricsRegistry,
    MetricsWriter,
    P95_PERCENTILE,
    REGISTRY,
    get_recorder,
    reset_recorder_for_tests,
)


def _build_recorder(tmp_path: Path) -> MetricsRecorder:
    """Return a recorder writing to *tmp_path* / metrics.jsonl."""

    writer = MetricsWriter(path=tmp_path / "metrics.jsonl")
    return reset_recorder_for_tests(writer=writer)


def test_legacy_registry_inc_and_render() -> None:
    """The legacy in-memory counter registry keeps its contract."""

    local = MetricsRegistry()
    local.inc("foo", {"phase": "recon"})
    local.inc("foo", {"phase": "recon"}, value=2)
    assert local.get("foo", {"phase": "recon"}) == 3

    text = local.prometheus_text()
    assert "# TYPE foo counter" in text
    assert 'foo{phase="recon"} 3' in text

    assert isinstance(REGISTRY, MetricsRegistry)


def test_recorder_appends_record_line(tmp_path: Path) -> None:
    """A single ``record`` call writes one JSONL entry with the duration."""

    recorder = _build_recorder(tmp_path)
    recorder.record(
        command="lazynmap",
        args="-sV 10.0.0.1",
        duration_ms=1234,
        success=True,
        exit_code=0,
        source="cli",
    )

    lines = (tmp_path / "metrics.jsonl").read_text().splitlines()
    assert len(lines) == 1

    payload = json.loads(lines[0])
    assert payload["command"] == "lazynmap"
    assert payload["args"] == "-sV 10.0.0.1"
    assert payload["duration_ms"] == 1234
    assert payload["success"] is True
    assert payload["exit_code"] == 0
    assert payload["source"] == "cli"
    assert payload["ts"].endswith("+00:00")


def test_recorder_clamps_negative_duration(tmp_path: Path) -> None:
    """A negative ``duration_ms`` is clamped to zero."""

    recorder = _build_recorder(tmp_path)
    recorder.record(command="ping", duration_ms=-50, success=False, exit_code=1)
    payload = json.loads((tmp_path / "metrics.jsonl").read_text().splitlines()[0])
    assert payload["duration_ms"] == 0


def test_summarize_aggregates_by_command(tmp_path: Path) -> None:
    """``summarize`` produces success rate, mean and p95 per command."""

    recorder = _build_recorder(tmp_path)
    for i in range(10):
        recorder.record(
            command="nmap",
            duration_ms=100 + i * 10,
            success=i != 9,
            exit_code=0 if i != 9 else 1,
        )
    for i in range(3):
        recorder.record(
            command="ping",
            duration_ms=50,
            success=False,
            exit_code=2,
        )

    summary = recorder.summarize()
    assert summary["total"] == 13
    nmap = summary["by_command"]["nmap"]
    assert nmap["count"] == 10
    assert nmap["success_rate"] == pytest.approx(9 / 10)
    assert nmap["mean_duration_ms"] == pytest.approx(145)
    assert nmap["p95_duration_ms"] == 190

    failures = {entry["command"]: entry["failures"] for entry in summary["top_failures"]}
    assert failures.get("ping") == 3
    assert failures.get("nmap") == 1


def test_summarize_window_filters_old_records(tmp_path: Path) -> None:
    """Window in seconds drops events older than the cutoff."""

    now = datetime.now(timezone.utc)
    fresh = now - timedelta(seconds=30)
    old = now - timedelta(hours=2)

    path = tmp_path / "metrics.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "ts": fresh.isoformat(),
            "command": "nmap",
            "duration_ms": 200,
            "success": True,
        }) + "\n")
        handle.write(json.dumps({
            "ts": old.isoformat(),
            "command": "ping",
            "duration_ms": 80,
            "success": True,
        }) + "\n")

    recorder = reset_recorder_for_tests(writer=MetricsWriter(path=path))
    summary = recorder.summarize(window_seconds=300)
    assert summary["total"] == 1
    assert "nmap" in summary["by_command"]
    assert "ping" not in summary["by_command"]


def test_tail_returns_newest_first(tmp_path: Path) -> None:
    """``tail(n)`` returns the *n* most recent records in reverse order."""

    recorder = _build_recorder(tmp_path)
    for i in range(5):
        recorder.record(command=f"cmd{i}", duration_ms=10 * i, success=True, exit_code=0)
    last_three = recorder.tail(3)
    assert [r["command"] for r in last_three] == ["cmd4", "cmd3", "cmd2"]


def test_concurrent_writes_do_not_corrupt(tmp_path: Path) -> None:
    """Threaded recorders produce decodable lines without truncation."""

    recorder = _build_recorder(tmp_path)
    writers = 8
    per_writer = 25

    def worker(tag: str) -> None:
        for i in range(per_writer):
            recorder.record(
                command=tag,
                args=f"i={i}",
                duration_ms=i,
                success=True,
                exit_code=0,
            )

    threads = [
        threading.Thread(target=worker, args=(f"t{i}",))
        for i in range(writers)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    lines = (tmp_path / "metrics.jsonl").read_text().splitlines()
    assert len(lines) == writers * per_writer
    for line in lines:
        assert json.loads(line)["command"].startswith("t")


def test_get_recorder_is_singleton(tmp_path: Path) -> None:
    """``get_recorder`` returns the same instance for repeated calls."""

    reset_recorder_for_tests(writer=MetricsWriter(path=tmp_path / "m.jsonl"))
    first = get_recorder()
    second = get_recorder()
    assert first is second


def test_aggregator_handles_empty_iterable() -> None:
    """``MetricsAggregator.summarize`` is well-defined on no records."""

    summary = MetricsAggregator.summarize(records=[])
    assert summary["total"] == 0
    assert summary["by_command"] == {}
    assert summary["top_failures"] == []


def test_aggregator_skips_malformed_records() -> None:
    """Non-dict records are silently ignored."""

    summary = MetricsAggregator.summarize(records=[None, 42, "x", {}])
    assert summary["total"] == 1


def test_p95_uses_nearest_rank() -> None:
    """Internal percentile helper matches the documented rank rule."""

    values = sorted([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    assert MetricsAggregator._percentile(values, P95_PERCENTILE) == 100


def test_metric_record_to_dict_roundtrip() -> None:
    """``MetricRecord.to_dict`` produces a JSON-friendly payload."""

    record = MetricRecord(
        ts="2026-06-01T00:00:00+00:00",
        command="ls",
        args="-l",
        duration_ms=42,
        success=True,
        exit_code=0,
        source="cli",
    )
    payload = record.to_dict()
    assert payload["command"] == "ls"
    json.dumps(payload)
