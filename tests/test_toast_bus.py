"""Tests for cli/toast_bus.py.

Covers offset persistence, JSONL parsing, severity-to-role mapping,
budget enforcement and the toggle-by-payload behaviour. The Textual app
is never instantiated — the tests use the Rich console capture mode.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

from rich.console import Console

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.toast_bus import (  # noqa: E402
    ToastBus,
    ToastConfig,
    ToastEvent,
    ToastFormatter,
    ToastReader,
    ToastState,
    build_default_bus,
    render_toasts,
    toasts_enabled,
)
from cli.themes import THEMES  # noqa: E402


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record))
            handle.write("\n")


def _append_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record))
            handle.write("\n")


def test_state_round_trip(tmp_path: Path) -> None:
    """Offsets persist across :class:`ToastState` instances."""
    config = ToastConfig(sessions_dir=str(tmp_path))
    first = ToastState(config, root=tmp_path)
    first.set("events.jsonl", 4096)
    assert first.flush() is True
    second = ToastState(config, root=tmp_path)
    assert second.get("events.jsonl") == 4096


def test_state_clamps_negative_offsets(tmp_path: Path) -> None:
    """Negative offsets are coerced to zero."""
    config = ToastConfig(sessions_dir=str(tmp_path))
    state = ToastState(config, root=tmp_path)
    state.set("events.jsonl", -10)
    assert state.get("events.jsonl") == 0


def test_reader_returns_unseen_events_only(tmp_path: Path) -> None:
    """A second read returns no events when the offset is current."""
    config = ToastConfig(sessions_dir=str(tmp_path))
    events_path = tmp_path / "events.jsonl"
    _write_jsonl(events_path, [{"type": "test", "severity": "info", "summary": "hello"}])
    reader = ToastReader(config, root=tmp_path)
    events, end_offset = reader.read_unseen("events.jsonl", 0)
    assert len(events) == 1
    assert events[0].summary == "hello"
    again, _ = reader.read_unseen("events.jsonl", end_offset)
    assert again == []


def test_reader_handles_malformed_lines(tmp_path: Path) -> None:
    """Non-JSON lines are skipped without raising."""
    config = ToastConfig(sessions_dir=str(tmp_path))
    events_path = tmp_path / "events.jsonl"
    events_path.write_text("not-json\n{\"type\":\"ok\"}\n", encoding="utf-8")
    reader = ToastReader(config, root=tmp_path)
    events, _ = reader.read_unseen("events.jsonl", 0)
    assert len(events) == 1
    assert events[0].event_type == "ok"


def test_formatter_uses_theme_role_for_severity() -> None:
    """Severity strings map to theme roles via the configured table."""
    config = ToastConfig()
    formatter = ToastFormatter(config, THEMES["default"])
    event = ToastEvent(
        source="events.jsonl",
        offset=10,
        event_type="WARN",
        severity="warning",
        summary="something happened",
        timestamp="2026-05-24T00:00:00Z",
    )
    rendered = formatter.format(event)
    plain = rendered.plain
    assert "WARN" in plain
    assert "something happened" in plain


def test_bus_render_respects_per_tick_budget(tmp_path: Path) -> None:
    """At most ``max_per_tick_default`` events are printed in one call."""
    config = ToastConfig(sessions_dir=str(tmp_path), max_per_tick_default=2)
    events_path = tmp_path / "events.jsonl"
    records = [
        {"type": "ev", "severity": "info", "summary": f"line-{i}"}
        for i in range(5)
    ]
    _write_jsonl(events_path, records)
    captured = Console(file=io.StringIO(), record=True, highlight=False)
    bus = ToastBus(
        config=config,
        state=ToastState(config, root=tmp_path),
        reader=ToastReader(config, root=tmp_path),
        formatter=ToastFormatter(config, THEMES["default"]),
        console=captured,
    )
    printed = bus.render(enabled=True)
    assert printed == 2


def test_bus_render_disabled_returns_zero(tmp_path: Path) -> None:
    """The bus is a no-op when ``enabled`` is False."""
    config = ToastConfig(sessions_dir=str(tmp_path))
    bus = ToastBus(
        config=config,
        state=ToastState(config, root=tmp_path),
        reader=ToastReader(config, root=tmp_path),
        formatter=ToastFormatter(config, THEMES["default"]),
        console=Console(file=io.StringIO()),
    )
    assert bus.render(enabled=False) == 0


def test_bus_mark_all_seen_consumes_pending(tmp_path: Path) -> None:
    """``mark_all_seen`` advances the offset for every configured file."""
    config = ToastConfig(sessions_dir=str(tmp_path))
    events_path = tmp_path / "events.jsonl"
    _write_jsonl(events_path, [{"type": "ev"}])
    bus = ToastBus(
        config=config,
        state=ToastState(config, root=tmp_path),
        reader=ToastReader(config, root=tmp_path),
        formatter=ToastFormatter(config, THEMES["default"]),
        console=Console(file=io.StringIO()),
    )
    bus.mark_all_seen()
    again = bus.render(enabled=True)
    assert again == 0


def test_toasts_enabled_default_true() -> None:
    """Missing payload flag yields True so first runs see notifications."""
    assert toasts_enabled(None) is True
    assert toasts_enabled({}) is True
    assert toasts_enabled({"enable_toasts": False}) is False
    assert toasts_enabled({"enable_toasts": "no"}) is False


def test_render_toasts_returns_count(tmp_path: Path) -> None:
    """The one-shot helper returns the number of toast lines printed."""
    events_path = tmp_path / "events.jsonl"
    _write_jsonl(events_path, [{"type": "ev"}])
    payload = {"enable_toasts": True}
    captured = Console(file=io.StringIO())
    count = render_toasts(payload=payload, sessions_dir=str(tmp_path), console=captured)
    assert count == 1


def test_build_default_bus_honours_budget(tmp_path: Path) -> None:
    """The factory propagates ``toast_max_per_tick`` into the config."""
    payload = {"toast_max_per_tick": 1}
    bus = build_default_bus(payload=payload, sessions_dir=str(tmp_path))
    events_path = tmp_path / "events.jsonl"
    _write_jsonl(events_path, [{"type": "a"}, {"type": "b"}])
    captured_console = Console(file=io.StringIO())
    bus._console = captured_console
    printed = bus.render(enabled=True)
    assert printed == 1


def test_reader_picks_up_new_events_after_offset(tmp_path: Path) -> None:
    """Appended events past the previous offset are surfaced on next read."""
    config = ToastConfig(sessions_dir=str(tmp_path))
    events_path = tmp_path / "events.jsonl"
    _write_jsonl(events_path, [{"type": "a"}])
    reader = ToastReader(config, root=tmp_path)
    _, offset_after_first = reader.read_unseen("events.jsonl", 0)
    _append_jsonl(events_path, [{"type": "b"}])
    events, _ = reader.read_unseen("events.jsonl", offset_after_first)
    assert [event.event_type for event in events] == ["b"]
