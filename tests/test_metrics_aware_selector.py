"""Tests for ``MetricsAwareSelector`` in ``skills/autonomous_daemon.py``.

The decorator must:

* be a transparent pass-through when the wrapped selector returns
  ``None`` or when there are not enough recorded attempts;
* filter the decision when the recorded ``success_rate`` is below the
  configured threshold and ``count >= min_attempts``;
* leave the :class:`FallbackSelector` unwrapped at chain composition
  time so the cascade always converges;
* respect the env-driven master switch through
  :data:`METRICS_BIAS_ENABLED`;
* cache the summary for the configured TTL to avoid re-reading the
  JSONL log on every step.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "skills"))

from skills.autonomous_daemon import (  # noqa: E402
    CommandDecision,
    FallbackSelector,
    ICommandSelector,
    MetricsAwareSelector,
    ParquetSelector,
    _wrap_chain_with_metrics_bias,
)


class _StubSelector(ICommandSelector):
    """Selector double that returns a hard-coded decision or ``None``."""

    def __init__(self, decision: CommandDecision | None) -> None:
        self._decision = decision
        self.calls: int = 0

    def select(
        self,
        target: str,
        phase: str,
        context: dict[str, Any],
    ) -> CommandDecision | None:
        self.calls += 1
        return self._decision


class _StubMetrics:
    """Stand-in for ``MetricsRecorder`` exposing only ``summarize``."""

    def __init__(self, by_command: dict[str, dict[str, Any]]) -> None:
        self._by_command = by_command
        self.summarize_calls: int = 0
        self.last_window: int | None = None

    def summarize(self, window_seconds: int | None = None) -> dict[str, Any]:
        self.summarize_calls += 1
        self.last_window = window_seconds
        return {
            "total": sum(c.get("count", 0) for c in self._by_command.values()),
            "by_command": self._by_command,
        }


def _decision(command: str) -> CommandDecision:
    return CommandDecision(command=command, source="stub", reason="for test")


def test_passthrough_when_wrapped_returns_none() -> None:
    """A ``None`` from the wrapped selector is forwarded verbatim."""

    metrics = _StubMetrics(by_command={})
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(None), metrics_source=metrics,
    )
    assert decorator.select("t", "recon", {}) is None
    assert metrics.summarize_calls == 0


def test_passthrough_when_insufficient_attempts() -> None:
    """Commands with fewer attempts than ``min_attempts`` are accepted."""

    metrics = _StubMetrics(by_command={
        "nmap": {"count": 1, "success_rate": 0.0, "mean_duration_ms": 100},
    })
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=metrics,
        min_attempts=3,
    )
    decision = decorator.select("t", "recon", {})
    assert decision is not None
    assert decision.command == "nmap"


def test_filters_when_success_rate_below_threshold() -> None:
    """Failing command is filtered out (selector returns ``None``)."""

    metrics = _StubMetrics(by_command={
        "nmap": {"count": 10, "success_rate": 0.1, "mean_duration_ms": 100},
    })
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=metrics,
        min_attempts=3,
        min_success_rate=0.5,
    )
    assert decorator.select("t", "recon", {}) is None


def test_accepts_when_success_rate_at_threshold() -> None:
    """Boundary case: ``success_rate == min_success_rate`` is accepted."""

    metrics = _StubMetrics(by_command={
        "nmap": {"count": 10, "success_rate": 0.5, "mean_duration_ms": 100},
    })
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=metrics,
        min_attempts=3,
        min_success_rate=0.5,
    )
    decision = decorator.select("t", "recon", {})
    assert decision is not None
    assert decision.command == "nmap"


def test_only_filters_named_command_not_whole_decision_object() -> None:
    """The decorator uses the first token of ``decision.command`` only."""

    metrics = _StubMetrics(by_command={
        "lazynmap": {"count": 5, "success_rate": 0.0},
    })
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("lazynmap -sV 10.0.0.1")),
        metrics_source=metrics,
        min_attempts=3,
        min_success_rate=0.5,
    )
    assert decorator.select("t", "recon", {}) is None


def test_summary_is_cached_within_ttl() -> None:
    """Repeated calls within ``cache_ttl_s`` reuse the cached summary."""

    metrics = _StubMetrics(by_command={
        "nmap": {"count": 10, "success_rate": 1.0},
    })

    clock_value = {"now": 100.0}

    def fake_clock() -> float:
        return clock_value["now"]

    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=metrics,
        cache_ttl_s=5.0,
        clock=fake_clock,
    )

    decorator.select("t", "recon", {})
    decorator.select("t", "recon", {})
    assert metrics.summarize_calls == 1

    clock_value["now"] = 200.0
    decorator.select("t", "recon", {})
    assert metrics.summarize_calls == 2


def test_summary_forwards_window_seconds() -> None:
    """The configured window is passed straight through to ``summarize``."""

    metrics = _StubMetrics(by_command={})
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=metrics,
        window_seconds=900,
    )
    decorator.select("t", "recon", {})
    assert metrics.last_window == 900


def test_zero_window_is_treated_as_unbounded() -> None:
    """``window_seconds=0`` translates to ``None`` for the source."""

    metrics = _StubMetrics(by_command={})
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=metrics,
        window_seconds=0,
    )
    decorator.select("t", "recon", {})
    assert metrics.last_window is None


def test_decorator_degrades_when_metrics_source_unavailable() -> None:
    """A ``None`` metrics source disables filtering, never raises."""

    class _BrokenSource:
        def summarize(self, window_seconds: int | None = None) -> dict[str, Any]:
            raise RuntimeError("disk full")

    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=_BrokenSource(),
    )
    decision = decorator.select("t", "recon", {})
    assert decision is not None
    assert decision.command == "nmap"


def test_wrap_chain_leaves_fallback_unwrapped() -> None:
    """``_wrap_chain_with_metrics_bias`` must not decorate the fallback."""

    parquet = ParquetSelector(pdb=None, fail_counts={})
    fallback = FallbackSelector()
    wrapped = _wrap_chain_with_metrics_bias([parquet, fallback])
    assert isinstance(wrapped[0], MetricsAwareSelector)
    assert wrapped[0].wrapped is parquet
    assert wrapped[1] is fallback


def test_wrap_chain_master_switch_off() -> None:
    """When ``enabled`` is False the list is returned unchanged."""

    parquet = ParquetSelector(pdb=None, fail_counts={})
    fallback = FallbackSelector()
    wrapped = _wrap_chain_with_metrics_bias(
        [parquet, fallback], enabled=False,
    )
    assert wrapped == [parquet, fallback]


def test_wrap_chain_is_idempotent() -> None:
    """Re-wrapping an already-wrapped chain does not stack decorators."""

    parquet = ParquetSelector(pdb=None, fail_counts={})
    fallback = FallbackSelector()
    once = _wrap_chain_with_metrics_bias([parquet, fallback])
    twice = _wrap_chain_with_metrics_bias(once)
    assert isinstance(twice[0], MetricsAwareSelector)
    assert twice[0].wrapped is parquet
    assert twice[1] is fallback


def test_filtering_emits_skip_event(tmp_path: Path, monkeypatch) -> None:
    """``METRICS_BIAS_SKIP`` events are appended on filter."""

    from skills import autonomous_daemon as auto

    events_file = tmp_path / "events.jsonl"
    monkeypatch.setattr(auto, "EVENTS_FILE", events_file)
    monkeypatch.setattr(auto, "SESSIONS_DIR", tmp_path)

    metrics = _StubMetrics(by_command={
        "nmap": {"count": 10, "success_rate": 0.0},
    })
    decorator = MetricsAwareSelector(
        wrapped=_StubSelector(_decision("nmap")),
        metrics_source=metrics,
        min_attempts=3,
        min_success_rate=0.5,
    )
    assert decorator.select("t", "recon", {}) is None
    assert events_file.exists()
    import json
    contents = [json.loads(line) for line in events_file.read_text().splitlines()]
    skip_events = [e for e in contents if e["type"] == "METRICS_BIAS_SKIP"]
    assert len(skip_events) == 1
    payload = skip_events[0]["payload"]
    assert payload["command"] == "nmap"
    assert payload["wrapped"] == "_StubSelector"
    assert payload["stats"]["success_rate"] == 0.0


def test_chain_falls_through_to_fallback_when_all_filtered() -> None:
    """When every wrapped selector filters its decision the fallback wins."""

    from skills.autonomous_daemon import CascadeStrategy

    metrics = _StubMetrics(by_command={
        "nmap": {"count": 10, "success_rate": 0.0},
        "lazyburp": {"count": 10, "success_rate": 0.0},
    })

    upstream_a = _StubSelector(_decision("nmap"))
    upstream_b = _StubSelector(_decision("lazyburp"))
    fallback = FallbackSelector()

    wrapped_a = MetricsAwareSelector(
        wrapped=upstream_a, metrics_source=metrics,
        min_attempts=3, min_success_rate=0.5,
    )
    wrapped_b = MetricsAwareSelector(
        wrapped=upstream_b, metrics_source=metrics,
        min_attempts=3, min_success_rate=0.5,
    )

    cascade = CascadeStrategy([wrapped_a, wrapped_b, fallback])
    decision = cascade.next_command(target="10.0.0.1", phase="recon")
    assert decision.source == "fallback"
