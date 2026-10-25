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

from cli.themes import THEMES  # noqa: E402
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
    events_path.write_text('not-json\n{"type":"ok"}\n', encoding="utf-8")
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
    records = [{"type": "ev", "severity": "info", "summary": f"line-{i}"} for i in range(5)]
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


def _toast_event(kind: str, severity: str, summary: str) -> ToastEvent:
    """Build one toast event for formatter tests."""
    return ToastEvent(
        source="events.jsonl",
        offset=0,
        event_type=kind,
        severity=severity,
        summary=summary,
        timestamp="2026-10-10T00:00:00Z",
    )


def test_prominent_completion_renders_full_text() -> None:
    """ENGAGE_DONE keeps its complete message instead of a truncated line."""
    config = ToastConfig()
    formatter = ToastFormatter(config, THEMES["default"])
    long_summary = "engagement dcbb4fa4 finished — 6 steps (5 ran, 1 skipped), shell=False skipped=[recon:lazynmap (scan_already_held)]"
    assert len(long_summary) > config.max_line_chars
    event = _toast_event("ENGAGE_DONE", "info", long_summary)
    assert formatter.is_prominent(event) is True
    rendered = formatter.format_many([event], width=100)
    captured = Console(file=io.StringIO(), width=100, record=True, highlight=False)
    captured.print(rendered)
    flat = " ".join(captured.export_text().split())
    condensed = flat.replace("│", "").replace(" ", "")
    assert "engagement dcbb4fa4 finished" in flat
    assert "skipped=[recon:lazynmap(scan_already_held)]" in condensed
    assert "..." not in flat


def test_prominent_severity_renders_panel() -> None:
    """Error events render as toastr panels with full text."""
    config = ToastConfig()
    formatter = ToastFormatter(config, THEMES["default"])
    event = _toast_event("STEP_DENIED", "error", "rm -rf / blocked — destructive")
    assert formatter.is_prominent(event) is True
    assert formatter.is_prominent(_toast_event("STEP_DONE", "info", "ok")) is False
    rendered = formatter.format_many([event], width=100)
    captured = Console(file=io.StringIO(), width=100, record=True, highlight=False)
    captured.print(rendered)
    assert "rm -rf / blocked — destructive" in captured.export_text()


def test_over_budget_events_collapse_into_digest() -> None:
    """Events beyond the tick budget surface as a digest, never silently."""
    config = ToastConfig(max_per_tick_default=2)
    formatter = ToastFormatter(config, THEMES["default"])
    events = [_toast_event("STEP_DONE", "info", f"line-{i}") for i in range(5)]
    rendered = formatter.format_many(events, width=100)
    captured = Console(file=io.StringIO(), width=100, record=True, highlight=False)
    captured.print(rendered)
    text = captured.export_text()
    assert "line-3" in text and "line-4" in text
    assert "+3 more" in text and "STEP_DONE" in text


def _cli_record(event_type: str, payload: dict, target: str = "10.0.0.5") -> dict:
    return {
        "id": "x",
        "ts": "21:14:02",
        "event_type": event_type,
        "source": "cli",
        "severity": "info",
        "payload": payload,
        "session_id": "",
        "target": target,
        "operator": "autonomous_loop",
    }


def test_summary_prefers_title_then_description() -> None:
    reader = ToastReader(ToastConfig())
    record = _cli_record(
        "exploit",
        {"title": "DVWA SQL injection", "description": "confidence=50%", "cve": "", "mitre_id": "T1190"},
    )
    event = reader._build_event(json.dumps(record), "events.jsonl", 0)
    assert event.summary == "DVWA SQL injection — confidence=50%"


def test_summary_falls_back_to_capture_metadata() -> None:
    reader = ToastReader(ToastConfig())
    record = _cli_record(
        "ctf_capture",
        {
            "title": "",
            "description": "",
            "artifacts": [],
            "metadata": {"vuln_id": "vsftpd_backdoor", "cve": "CVE-2011-2523", "artifacts": ["ctf/vsftpd_backdoor/record.json"]},
        },
    )
    event = reader._build_event(json.dumps(record), "events.jsonl", 0)
    assert "vsftpd_backdoor" in event.summary
    assert "CVE-2011-2523" in event.summary
    assert "record.json" in event.summary


def test_summary_deduplicates_command_args_tail() -> None:
    reader = ToastReader(ToastConfig())
    record = _cli_record(
        "echo",
        {"command": "tmux kill-session -t lab 2>/dev/null", "args": "kill-session -t lab 2>/dev/null"},
    )
    event = reader._build_event(json.dumps(record), "events.jsonl", 0)
    assert event.summary == "tmux kill-session -t lab 2>/dev/null"


def test_activity_trigger_sources_expand_and_render() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        _write_jsonl(
            Path(tmp) / "activity_t0001.jsonl",
            [{"ts": "2026-10-21T22:11:54", "task": "t0001", "worker": "scheduler", "kind": "fire", "text": "trigger #1 kind=service addons=hellbird:lazyaddon"}],
        )
        reader = ToastReader(ToastConfig(), root=Path(tmp))
        sources, _ = reader.resolve_sources(ToastConfig().event_files)
        assert "activity_t0001.jsonl" in sources
        all_events: list = []
        for name in sources:
            events, end = reader.read_unseen(name, 0)
            all_events.extend(events)
            if name == "activity_t0001.jsonl":
                assert end > 0
        trigger_events = [e for e in all_events if e.event_type == "scheduler"]
        assert len(trigger_events) == 1
        assert "trigger #1 kind=service addons=hellbird:lazyaddon" in trigger_events[0].summary


def test_collect_includes_activity_sources() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        _write_jsonl(
            Path(tmp) / "activity_t0002.jsonl",
            [{"ts": "21:14:02", "task": "t0002", "worker": "scheduler", "kind": "fire", "text": "trigger #2 kind=service"}],
        )
        bus = build_default_bus({"enable_toasts": True}, sessions_dir=tmp)
        events = bus.collect()
        assert any(e.event_type == "scheduler" and "trigger #2" in e.summary for e in events)
