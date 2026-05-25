"""Tests for cli/palette_overlay.py.

Exercises the data layer (state, filtering, ranking). The Textual app
itself is not instantiated; the runner argument of ``launch_overlay`` is
used to verify the wiring without rendering.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.palette_overlay import (  # noqa: E402
    PaletteOverlayConfig,
    PaletteOverlayState,
    PaletteRow,
    build_state,
    launch_overlay,
)


def _fake_index() -> dict:
    return {
        "commands": [
            {"name": "do_ping", "phase": "recon", "summary": "ping a host"},
            {"name": "do_lazynmap", "phase": "recon", "summary": "nmap scan"},
            {"name": "do_gobuster", "phase": "enum", "summary": "directory bruteforce"},
            {"name": "do_palette", "phase": "uncategorized", "summary": "open palette"},
        ],
        "phase_to_commands": {"recon": ["do_ping"]},
    }


def test_rows_returns_all_commands_when_query_empty() -> None:
    """No query returns every canonical command, sorted deterministically."""
    state = PaletteOverlayState(config=PaletteOverlayConfig(), index=_fake_index())
    rows = state.rows()
    names = {row.name for row in rows}
    assert names == {"do_ping", "do_lazynmap", "do_gobuster", "do_palette"}


def test_rows_filter_by_substring() -> None:
    """Substring match narrows results."""
    state = PaletteOverlayState(config=PaletteOverlayConfig(), index=_fake_index())
    state.set_query("nmap")
    rows = state.rows()
    assert [row.name for row in rows] == ["do_lazynmap"]


def test_rows_rank_recents_above_substrings() -> None:
    """Recents float to the top when not contradicted by an exact prefix match."""
    state = PaletteOverlayState(
        config=PaletteOverlayConfig(),
        index=_fake_index(),
        recents=("do_gobuster",),
    )
    state.set_query("o")
    rows = state.rows()
    assert rows[0].name == "do_gobuster"
    assert rows[0].is_recent is True


def test_rows_respect_max_rows() -> None:
    """The truncation limit caps the returned list length."""
    config = PaletteOverlayConfig(max_rows=2)
    state = PaletteOverlayState(config=config, index=_fake_index())
    rows = state.rows()
    assert len(rows) == 2


def test_build_state_returns_none_when_index_missing(monkeypatch) -> None:
    """The factory returns ``None`` when the index cannot be loaded."""
    monkeypatch.setattr("cli.palette_overlay._load_index", lambda: None)
    assert build_state() is None


def test_launch_overlay_uses_runner_for_tests() -> None:
    """The runner override lets tests bypass Textual entirely."""
    state = PaletteOverlayState(config=PaletteOverlayConfig(), index=_fake_index())

    def runner(context):
        return "do_ping"

    selected = launch_overlay(state=state, runner=runner)
    assert selected == "do_ping"


def test_truncate_summary_uses_truncation_suffix() -> None:
    """Long summaries get truncated with the configured suffix."""
    config = PaletteOverlayConfig(summary_max_chars=10, truncation_suffix="..")
    state = PaletteOverlayState(
        config=config,
        index={
            "commands": [
                {"name": "do_x", "phase": "p", "summary": "a" * 50},
            ],
        },
    )
    row = state.rows()[0]
    assert row.summary.endswith("..")
    assert len(row.summary) == config.summary_max_chars


def test_set_query_strips_whitespace() -> None:
    """Leading/trailing whitespace is removed before scoring."""
    state = PaletteOverlayState(config=PaletteOverlayConfig(), index=_fake_index())
    state.set_query("  nmap  ")
    rows = state.rows()
    assert [row.name for row in rows] == ["do_lazynmap"]
