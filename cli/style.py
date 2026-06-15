"""Centralised TUI style tokens for the LazyOwn operator surface.

This module is a thin semantic layer over :mod:`cli.themes`. It exposes a
small, stable set of tokens (``title``, ``accent``, ``hint``...) so that
callers -- the cmd2 prompt, the post-command hint line, the daily tip,
the splash overlay -- never reference raw ANSI escape codes or theme
names directly. Switching the active theme re-paints every surface that
imports from this module without any change in call sites.

Design notes:

- Single Responsibility: only token -> style resolution lives here.
  No I/O, no payload reading, no printing. Callers pass the payload
  mapping in when they need theme resolution.
- Open/Closed: new tokens are added by extending :data:`TOKEN_KEYS`;
  the resolver does not change.
- Dependency Inversion: callers depend on the :func:`style` /
  :func:`paint` functions, never on :mod:`cli.themes` directly. The
  underlying theme module can be swapped without touching consumers.
- No magic strings: every token key is declared in :data:`TOKEN_KEYS`.
"""

from __future__ import annotations

from typing import Mapping

from rich.text import Text

from cli.themes import Theme, get_theme, theme_from_payload

TOKEN_KEYS: tuple[str, ...] = (
    "title",
    "subtitle",
    "accent",
    "muted",
    "border",
    "success",
    "warning",
    "danger",
    "hint",
)
"""Semantic style tokens every TUI surface should reference.

Adding a new role here is the only edit required to expose it
across the whole operator surface.
"""


def style(token: str, theme: Theme | None = None) -> str:
    """Return the Rich style string for a semantic token.

    Args:
        token: One of :data:`TOKEN_KEYS`. Unknown tokens fall back to
            ``"white"`` rather than raising -- callers may pass
            user-influenced keys without crashing the prompt.
        theme: Optional pre-resolved :class:`cli.themes.Theme`. When
            ``None`` the default theme is used.

    Returns:
        A Rich-compatible style string (e.g. ``"bold cyan"``).
    """
    chosen = theme if theme is not None else get_theme(None)
    if not hasattr(chosen, token):
        return "white"
    return str(getattr(chosen, token))


def active_tokens(payload: Mapping[str, object] | None) -> dict[str, str]:
    """Resolve every :data:`TOKEN_KEYS` entry for the payload's theme.

    Args:
        payload: Loaded ``payload.json`` mapping. ``None`` returns
            the default theme tokens.

    Returns:
        Dict mapping each token key to a Rich style string. Useful
        when a surface wants to render multiple tokens without
        re-resolving the theme per call.
    """
    theme = theme_from_payload(payload)
    return {key: style(key, theme) for key in TOKEN_KEYS}


def paint(text: str, token: str, payload: Mapping[str, object] | None = None) -> Text:
    """Render ``text`` with the style of ``token`` for the active theme.

    Args:
        text: Raw text to render. No markup parsing.
        token: Semantic token from :data:`TOKEN_KEYS`.
        payload: Optional payload mapping; ``None`` uses defaults.

    Returns:
        A :class:`rich.text.Text` instance ready to print or compose.
    """
    return Text(text, style=style(token, theme_from_payload(payload)))


def render_prompt(console, segments: list[tuple[str, str]], payload: Mapping[str, object] | None = None) -> None:
    """Print a themed prompt line composed of ``(text, token)`` pairs.

    The function does not terminate with a newline; cmd2's prompt
    machinery appends the trailing space. Each segment is coloured
    using the resolved theme, and segments are joined with a dim
    separator so the prompt reads as a single visual unit.

    Args:
        console: A :class:`rich.console.Console` the shell already
            uses for output.
        segments: Ordered list of ``(text, token)`` pairs. Tokens come
            from :data:`TOKEN_KEYS`. An empty list is a no-op.
        payload: Optional payload mapping. When ``None`` the default
            theme is used; passing a payload lets the call site pick
            the operator's chosen theme.

    Returns:
        None. The result is written to ``console`` directly.
    """
    if not segments:
        return
    theme = theme_from_payload(payload)
    composed = Text()
    for index, (raw, token) in enumerate(segments):
        if index > 0:
            composed.append(" \u2502 ", style=style("muted", theme))
        composed.append(raw, style=style(token, theme))
    console.print(composed, end="")


__all__ = [
    "TOKEN_KEYS",
    "active_tokens",
    "paint",
    "render_prompt",
    "style",
]
