"""Terminal-safe Rich console factory.

Colors and unicode glyphs are only safe when the sink interprets them.
This module centralises that decision so no surface ever leaks raw ANSI
codes (``?[32m``) or placeholder boxes (``?`` for ``╭─✔█``) again:

- Rich auto-detection already drops ANSI on non-tty / NO_COLOR /
  TERM=dumb sinks — every console here keeps those defaults.
- When stdout cannot encode UTF-8, panels switch to the ASCII box and
  glyph helpers degrade to ``[x]``/``[>]``/``[ ]``/``#``/``-``.
"""

from __future__ import annotations

import sys

from rich import box
from rich.console import Console

_DONE = "✔"
_ACTIVE = "▶"
_PENDING = "○"
_FILL = "█"
_EMPTY = "░"

_DONE_ASCII = "[x]"
_ACTIVE_ASCII = "[>]"
_PENDING_ASCII = "[ ]"
_FILL_ASCII = "#"
_EMPTY_ASCII = "-"


def supports_unicode() -> bool:
    """Return True when stdout can encode box-drawing glyphs and emoji."""
    try:
        encoding = (getattr(sys.stdout, "encoding", "") or "").lower()
    except Exception:
        return False
    return "utf" in encoding.replace("-", "").replace("_", "")


def get_console(**overrides) -> Console:
    """Build a Rich console with safe color/box defaults.

    Callers may pass Rich ``Console`` options (``width``, ``file``);
    ``color_system``/``force_terminal`` are left on auto so piped or
    crippled sinks never receive raw escape codes.
    """
    return Console(highlight=False, soft_wrap=True, **overrides)


def panel_box():
    """Return the ROUNDED box on UTF-8 sinks, ASCII otherwise."""
    return box.ROUNDED if supports_unicode() else box.ASCII


def milestone_glyph(state: str) -> str:
    """Glyph for a milestone state: done / active / pending (or other)."""
    uni = supports_unicode()
    if state == "done":
        return _DONE if uni else _DONE_ASCII
    if state == "active":
        return _ACTIVE if uni else _ACTIVE_ASCII
    return _PENDING if uni else _PENDING_ASCII


def progress_bar(ratio: float, width: int = 10) -> str:
    """Fixed-width fill bar, unicode blocks or ASCII hashes."""
    uni = supports_unicode()
    clamped = max(0.0, min(1.0, float(ratio or 0.0)))
    filled = int(round(clamped * width))
    fill = _FILL if uni else _FILL_ASCII
    empty = _EMPTY if uni else _EMPTY_ASCII
    return fill * filled + empty * (width - filled)


__all__ = [
    "get_console",
    "milestone_glyph",
    "panel_box",
    "progress_bar",
    "supports_unicode",
]
