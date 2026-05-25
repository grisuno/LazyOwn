"""Tests for the operator-presence segment of cli/status_bar.py.

Verifies the new :class:`CollabPresenceSource`, the optional fifth
``operators`` slot of :class:`StatusContext`, the auto-format switch in
the renderer, and the toggle-by-payload behaviour of
:func:`build_default_manager`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.status_bar import (  # noqa: E402
    CollabPresenceSource,
    FileSystemReader,
    StatusBarConfig,
    StatusBarRenderer,
    StatusContext,
    build_default_manager,
)


def _write_operators(tmp_path: Path, records: list[dict]) -> None:
    target = tmp_path / "operators.json"
    target.write_text(json.dumps({"operators": records}), encoding="utf-8")


def test_collab_presence_zero_when_file_missing(tmp_path: Path) -> None:
    """An absent operators file yields the configured fallback string."""
    config = StatusBarConfig(sessions_dir=str(tmp_path))
    reader = FileSystemReader(config, root=tmp_path)
    source = CollabPresenceSource(config, reader, clock=lambda: 1_000_000.0)
    assert source.collect() == config.fallback_operators


def test_collab_presence_counts_active_operators(tmp_path: Path) -> None:
    """Operators marked active and within the stale window are counted."""
    config = StatusBarConfig(sessions_dir=str(tmp_path), operator_stale_seconds=90.0)
    reader = FileSystemReader(config, root=tmp_path)
    now = 1_000_000.0
    _write_operators(
        tmp_path,
        [
            {"name": "alice", "active": True, "last_seen": now - 10.0},
            {"name": "bob", "active": True, "last_seen": now - 1_000.0},
            {"name": "carol", "active": True, "last_seen": now - 5.0},
            {"name": "dave", "active": False, "last_seen": now},
        ],
    )
    source = CollabPresenceSource(config, reader, clock=lambda: now)
    assert source.collect() == "2"


def test_renderer_uses_default_format_when_operators_empty() -> None:
    """An empty ``operators`` segment preserves the historical layout."""
    config = StatusBarConfig()
    renderer = StatusBarRenderer(config)
    line = renderer.render_plain(
        StatusContext(target="10.0.0.1", phase="recon", last_finding="-", next_suggestion="ping")
    )
    assert " ops:" not in line
    assert "10.0.0.1" in line


def test_renderer_switches_to_ops_format_when_present() -> None:
    """A non-empty ``operators`` value triggers the alternate format."""
    config = StatusBarConfig()
    renderer = StatusBarRenderer(config)
    line = renderer.render_plain(
        StatusContext(
            target="10.0.0.1",
            phase="recon",
            last_finding="-",
            next_suggestion="ping",
            operators="3",
        )
    )
    assert "ops: 3" in line


def test_build_default_manager_skips_operators_by_default(tmp_path: Path) -> None:
    """The fifth source is opt-in via ``enable_operator_presence``."""
    manager = build_default_manager(payload=None, sessions_dir=str(tmp_path))
    assert "operators" not in manager._sources  # noqa: SLF001


def test_build_default_manager_wires_operators_when_enabled(tmp_path: Path) -> None:
    """The flag opts into the additional source."""
    payload = {"enable_operator_presence": True}
    manager = build_default_manager(payload=payload, sessions_dir=str(tmp_path))
    assert "operators" in manager._sources  # noqa: SLF001


def test_render_prompt_uses_default_theme_when_unspecified(tmp_path: Path) -> None:
    """Without ``tui_theme`` the prompt carries the default theme colour."""
    payload = {"rhost": "10.0.0.1"}
    manager = build_default_manager(payload=payload, sessions_dir=str(tmp_path))
    rendered = manager.render_prompt("> ")
    assert "\x1b[1;36m" in rendered


def test_render_prompt_switches_colour_with_tui_theme(tmp_path: Path) -> None:
    """Switching ``tui_theme`` changes the ANSI prefix in the next render."""
    payload = {"rhost": "10.0.0.1", "tui_theme": "bright"}
    manager = build_default_manager(payload=payload, sessions_dir=str(tmp_path))
    rendered = manager.render_prompt("> ")
    assert "\x1b[1;93;44m" in rendered
    payload["tui_theme"] = "colorblind"
    rendered = manager.render_prompt("> ")
    assert "\x1b[1;97;45m" in rendered
    payload["tui_theme"] = "dim"
    rendered = manager.render_prompt("> ")
    assert "\x1b[1;90m" in rendered
