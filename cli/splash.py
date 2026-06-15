"""Animated splash overlay for the LazyOwn first-run experience.

The splash is rendered with Rich on top of the existing ASCII art
banner. Operators keep their original art: this overlay just paints
a typewriter effect around it during the first 1-2 seconds of
startup, then exits cleanly back to the cmd2 prompt. Opt-in via
``payload.json[\"splash\"] = true`` (default false), and auto-on
when ``payload.json`` does not yet exist.

Design notes:

- Single Responsibility: only the overlay animation lives here.
  No payload reading, no shell state, no theme mutation. Callers
  pass the already-resolved theme tokens.
- Open/Closed: new animation kinds (e.g. glitch, fade) extend
  :class:`SplashEffect`; the dispatcher in :func:`render_splash`
  does not change.
- Dependency Inversion: callers depend on :func:`render_splash`
  and the :class:`SplashEffect` protocol, not on Rich directly.
- No magic numbers: timing constants live in :data:`SPLASH_CONFIG`.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Mapping, Protocol

from rich.console import Console
from rich.text import Text

from cli.style import active_tokens


@dataclass(frozen=True)
class SplashConfig:
    """Timing and behaviour knobs for the splash overlay.

    Attributes:
        total_seconds: How long the overlay stays on screen. ``0``
            or negative means render-and-exit immediately. The
            effect never blocks longer than this regardless of the
            typewriter per-character delay.
        per_char_seconds: Delay between consecutive characters in
            the typewriter effect. Lower values feel snappier.
        clear_after: Whether to clear the overlay before returning
            to the caller. When ``False`` the operator sees the
            splash frozen at its final state -- useful for
            screencasts but disruptive in a real shell.
    """

    total_seconds: float = 1.5
    per_char_seconds: float = 0.012
    clear_after: bool = True


SPLASH_CONFIG: SplashConfig = SplashConfig()
"""Default timing for the splash. Tuned for ~1.5s on a modern TTY."""


class SplashEffect(Protocol):
    """Strategy protocol for splash animations.

    A new effect implements ``render`` and is registered in
    :func:`render_splash` dispatch. The effect owns its own
    progress and timing -- the dispatcher only hands it the
    console, the lines to animate, and the resolved tokens.
    """

    def render(
        self,
        console: Console,
        lines: list[str],
        tokens: Mapping[str, str],
        config: SplashConfig,
    ) -> None: ...


class TypewriterEffect:
    """Print each character of each line with a fixed delay.

    A blinking caret is appended to the active line so the
    operator sees the typewriter working. The caret is removed
    before the function returns. The accumulated prefix is
    redrawn on every step so the operator sees the line growing
    left-to-right, not single characters flickering.
    """

    def render(
        self,
        console: Console,
        lines: list[str],
        tokens: Mapping[str, str],
        config: SplashConfig,
    ) -> None:
        accent = tokens.get("accent", "white")
        caret_visible: bool = True
        start = time.monotonic()
        for line_index, line in enumerate(lines):
            accumulated = Text()
            for char_index, char in enumerate(line):
                if time.monotonic() - start > config.total_seconds:
                    accumulated.append(line[char_index:], style=accent)
                    _redraw(console, accumulated, caret=False, tokens=tokens)
                    accumulated = Text()
                    break
                accumulated.append(char, style=accent)
                _redraw(console, accumulated, caret=caret_visible, tokens=tokens)
                if config.per_char_seconds > 0:
                    time.sleep(config.per_char_seconds)
                caret_visible = not caret_visible
            if accumulated.plain:
                console.print(accumulated, end="\n", highlight=False)
            elif line_index < len(lines) - 1:
                console.print("", end="\n", highlight=False)


def _redraw(
    console: Console,
    accumulated: Text,
    caret: bool,
    tokens: Mapping[str, str],
) -> None:
    """Rewrite the current line with ``accumulated`` plus optional caret.

    Args:
        console: Rich console the typewriter writes through.
        accumulated: Text built so far for the current line.
        caret: Whether to append a blinking block character to
            signal ongoing typing.
        tokens: Resolved theme tokens. The caret picks up the
            ``muted`` style.
    """
    snapshot = Text(str(accumulated))
    if caret:
        snapshot.append("\u2588", style=tokens.get("muted", "white"))
    console.print(snapshot, end="\r", highlight=False)


class InstantEffect:
    """Print every line at once with no animation. Used in tests.

    The effect renders and returns immediately so unit tests do
    not have to mock :func:`time.sleep`. ``render_splash`` picks
    this effect whenever ``config.total_seconds <= 0`` or the
    caller asks for it explicitly.
    """

    def render(
        self,
        console: Console,
        lines: list[str],
        tokens: Mapping[str, str],
        config: SplashConfig,
    ) -> None:
        accent = tokens.get("accent", "white")
        for line in lines:
            console.print(Text(line, style=accent), end="\n", highlight=False)


_INSTANT_EFFECT = InstantEffect()
_TYPEWRITER_EFFECT = TypewriterEffect()


def render_splash(
    console: Console,
    lines: list[str],
    payload: Mapping[str, object] | None = None,
    config: SplashConfig | None = None,
    effect_name: str = "typewriter",
) -> None:
    """Render the splash overlay and optionally clear the screen.

    Args:
        console: Rich console the shell already uses. The overlay
            writes through it so colours and terminal width match
            the rest of the operator surface.
        lines: Lines to animate. Each entry is a plain string --
            markup is intentionally NOT parsed, so the operator's
            ASCII art (which often contains brackets) renders
            verbatim.
        payload: Payload mapping for theme resolution. ``None``
            uses the default theme; passing the live payload
            honours the operator's chosen ``tui_theme``.
        config: Override timing/clear behaviour. ``None`` uses
            :data:`SPLASH_CONFIG`.
        effect_name: Which effect to dispatch. ``\"typewriter\"``
            or ``\"instant\"``. Unknown values fall back to
            ``\"instant\"`` so a bad config never crashes startup.

    Returns:
        None. The console is left in a state ready for the next
        prompt line to be printed (or cleared, depending on
        ``config.clear_after``).
    """
    cfg = config if config is not None else SPLASH_CONFIG
    tokens = active_tokens(payload)
    effect = _TYPEWRITER_EFFECT if effect_name == "typewriter" else _INSTANT_EFFECT
    if cfg.total_seconds <= 0 or effect_name == "instant":
        effect = _INSTANT_EFFECT
    effect.render(console, lines, tokens, cfg)
    if cfg.clear_after and lines:
        console.file.write("\x1b[2J\x1b[H")
        console.file.flush()


__all__ = [
    "InstantEffect",
    "SPLASH_CONFIG",
    "SplashConfig",
    "SplashEffect",
    "TypewriterEffect",
    "render_splash",
]
