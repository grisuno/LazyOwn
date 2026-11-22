"""Tests for the extracted autosuggest wiring mixin."""

from __future__ import annotations

import csv

from cli.autosuggest_shell import AutosuggestMixin


class _StubEngine:
    """Records refresh calls and the enabled flag."""

    def __init__(self):
        self.enabled = None
        self.contexts: list = []

    def set_enabled(self, value):
        self.enabled = value

    def refresh(self, context):
        self.contexts.append(context)


class _StubShell(AutosuggestMixin):
    """Minimal host exposing only what the autosuggest mixin reads."""

    def __init__(self, sessions_dir, params=None, engine=None):
        self.sessions_dir = sessions_dir
        self.params = params or {}
        self._autosuggest = engine


def _write_report(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["command", "tool", "name"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def test_recent_commands_reads_first_tokens_and_limits(tmp_path):
    """Given a transcript, When read, Then last N first-tokens return."""
    report = tmp_path / "LazyOwn_session_report.csv"
    _write_report(
        report,
        [
            {"command": "ping 10.0.0.1", "tool": "", "name": ""},
            {"command": "lazynmap -p-", "tool": "", "name": ""},
            {"command": "", "tool": "gobuster dir", "name": ""},
        ],
    )
    shell = _StubShell(str(tmp_path))
    assert shell._read_recent_commands_for_autosuggest(limit=2) == ["lazynmap", "gobuster"]


def test_recent_commands_missing_file_is_empty(tmp_path):
    """Given no transcript, When read, Then an empty list returns."""
    shell = _StubShell(str(tmp_path))
    assert shell._read_recent_commands_for_autosuggest() == []


def test_refresh_disabled_skips_engine_refresh():
    """Given enable_autosuggest=false, When refreshed, Then no context is built."""
    engine = _StubEngine()
    shell = _StubShell("sessions", {"enable_autosuggest": "false"}, engine)
    shell._refresh_autosuggest("ping")
    assert engine.enabled is False
    assert engine.contexts == []


def test_refresh_enabled_feeds_context(tmp_path):
    """Given an enabled engine, When refreshed, Then shell state reaches the context."""
    report = tmp_path / "LazyOwn_session_report.csv"
    _write_report(report, [{"command": "ping x", "tool": "", "name": ""}])
    engine = _StubEngine()
    shell = _StubShell(
        str(tmp_path),
        {"phase": "recon", "rhost": "10.0.0.5", "os_id": "1"},
        engine,
    )
    shell._refresh_autosuggest("lazynmap")
    assert engine.enabled is True
    assert len(engine.contexts) == 1
    ctx = engine.contexts[0]
    assert ctx.last_command == "lazynmap"
    assert ctx.phase == "recon"
    assert ctx.target == "10.0.0.5"
    assert ctx.os_hint == "1"
    assert ctx.recent_commands == ["ping"]


def test_refresh_without_engine_is_noop():
    """Given no engine, When refreshed, Then nothing raises."""
    shell = _StubShell("sessions", {}, None)
    shell._refresh_autosuggest("ping")
