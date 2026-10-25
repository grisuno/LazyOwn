"""Terminal-safe console: colors and glyphs degrade, never leak."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from core.safe_console import (  # noqa: E402
    get_console,
    milestone_glyph,
    panel_box,
    progress_bar,
    supports_unicode,
)


def test_glyphs_degrade_to_ascii(monkeypatch) -> None:
    """Non-UTF-8 sinks get bracket markers instead of unicode glyphs."""
    import core.safe_console as safe

    monkeypatch.setattr(safe.sys, "stdout", type("S", (), {"encoding": "ascii"})())
    assert not supports_unicode()
    assert milestone_glyph("done") == "[x]"
    assert milestone_glyph("active") == "[>]"
    assert milestone_glyph("pending") == "[ ]"
    assert progress_bar(0.5, width=4) == "##--"


def test_glyphs_unicode_on_utf8(monkeypatch, capsys) -> None:
    """UTF-8 sinks keep the rich glyphs."""
    capsys.readouterr()
    assert milestone_glyph("done") == "✔"
    assert milestone_glyph("other") == "○"
    assert progress_bar(1.0, width=3) == "███"
    assert progress_bar(0.0, width=3) == "░░░"


def test_console_never_forces_color() -> None:
    """Piped sinks receive plain text: no ANSI is ever forced on."""
    import io

    stream = io.StringIO()
    console = get_console(file=stream, width=80)
    console.print("[bold green]hello[/] world")
    assert "\x1b" not in stream.getvalue()
    assert "hello world" in stream.getvalue()


def test_panel_box_ascii_fallback(monkeypatch) -> None:
    """Panels use the ASCII box when unicode is unavailable."""
    from rich import box

    import core.safe_console as safe

    monkeypatch.setattr(safe.sys, "stdout", type("S", (), {"encoding": "latin-1"})())
    assert panel_box() is box.ASCII
