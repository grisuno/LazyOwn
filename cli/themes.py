"""Theme registry for the LazyOwn TUI surfaces.

Every Textual overlay (Cmd-K palette, sessions browser, timeline scrubber,
command form, graph overlay) and the persistent status bar pull their
colour tokens from this module. Themes are pure data: a name plus a
mapping from semantic role to a Rich-compatible style string. Consumers
look up styles by role, never by raw colour, so adding a new theme is
one constant declaration and every surface follows along.

Design notes:

- Single Responsibility: only theme registration and lookup live here.
  No widget, no I/O. The active theme is selected by the operator via
  the ``tui_theme`` payload key; this module never touches
  ``payload.json`` directly.
- Open/Closed: new themes are added to :data:`THEMES`; the resolver does
  not change.
- Dependency Inversion: callers depend on the :class:`Theme` dataclass,
  never on the underlying terminal capabilities.
- No magic numbers/strings: every role and colour lives in one of the
  declared :class:`Theme` constants below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Theme:
    """Immutable mapping from semantic UI role to Rich style string.

    Attributes:
        name: Stable identifier used by ``payload.json["tui_theme"]``.
        title: Style for primary headings (titles, modal headers).
        subtitle: Style for secondary headings and helper text.
        accent: Style for highlighted tokens (matches, focused items).
        muted: Style for inactive entries and field labels.
        border: Style for panel borders and dividers.
        success: Style for positive markers (ok, completed, found).
        warning: Style for cautionary markers.
        danger: Style for destructive or error markers.
        hint: Style for the inline reactive hint footer.
        bar_open: Raw ANSI prefix written by the status bar.
        bar_close: Raw ANSI suffix written by the status bar.
    """

    name: str
    title: str
    subtitle: str
    accent: str
    muted: str
    border: str
    success: str
    warning: str
    danger: str
    hint: str
    bar_open: str
    bar_close: str


DEFAULT_THEME_NAME: str = "default"

_RESET: str = "\033[0m"
_DEFAULT_BAR_OPEN: str = "\033[1;36m"
_DIM_BAR_OPEN: str = "\033[1;90m"
_BRIGHT_BAR_OPEN: str = "\033[1;93;44m"
_COLORBLIND_BAR_OPEN: str = "\033[1;97;45m"


_DEFAULT: Theme = Theme(
    name="default",
    title="bold cyan",
    subtitle="bold white",
    accent="bold yellow",
    muted="dim white",
    border="cyan",
    success="bold green",
    warning="bold yellow",
    danger="bold red",
    hint="dim white italic",
    bar_open=_DEFAULT_BAR_OPEN,
    bar_close=_RESET,
)

_DIM: Theme = Theme(
    name="dim",
    title="dim bold white",
    subtitle="dim white",
    accent="dim cyan",
    muted="dim white",
    border="dim white",
    success="dim green",
    warning="dim yellow",
    danger="dim red",
    hint="dim white",
    bar_open=_DIM_BAR_OPEN,
    bar_close=_RESET,
)

_BRIGHT: Theme = Theme(
    name="bright",
    title="bold bright_cyan",
    subtitle="bold bright_white",
    accent="bold bright_yellow",
    muted="bright_white",
    border="bright_cyan",
    success="bold bright_green",
    warning="bold bright_yellow",
    danger="bold bright_red",
    hint="bright_white italic",
    bar_open=_BRIGHT_BAR_OPEN,
    bar_close=_RESET,
)

_COLORBLIND: Theme = Theme(
    name="colorblind",
    title="bold blue",
    subtitle="bold white",
    accent="bold magenta",
    muted="white",
    border="blue",
    success="bold blue",
    warning="bold magenta",
    danger="bold magenta on white",
    hint="white italic",
    bar_open=_COLORBLIND_BAR_OPEN,
    bar_close=_RESET,
)


THEMES: Mapping[str, Theme] = {
    _DEFAULT.name: _DEFAULT,
    _DIM.name: _DIM,
    _BRIGHT.name: _BRIGHT,
    _COLORBLIND.name: _COLORBLIND,
}


def get_theme(name: str | None) -> Theme:
    """Return the registered :class:`Theme` for ``name`` with safe fallback.

    Args:
        name: Theme identifier as written in ``payload.json["tui_theme"]``.
            ``None`` or unknown names fall back to :data:`DEFAULT_THEME_NAME`.

    Returns:
        The matching :class:`Theme`. Never raises.
    """
    if not isinstance(name, str):
        return THEMES[DEFAULT_THEME_NAME]
    key = name.strip().lower()
    return THEMES.get(key, THEMES[DEFAULT_THEME_NAME])


def theme_from_payload(payload: Mapping[str, object] | None) -> Theme:
    """Return the theme selected by ``payload["tui_theme"]``.

    Args:
        payload: Loaded ``payload.json`` mapping. ``None`` returns the
            default theme.

    Returns:
        The resolved :class:`Theme`.
    """
    if not payload:
        return THEMES[DEFAULT_THEME_NAME]
    raw = payload.get("tui_theme")
    if not isinstance(raw, str):
        return THEMES[DEFAULT_THEME_NAME]
    return get_theme(raw)


__all__ = [
    "DEFAULT_THEME_NAME",
    "THEMES",
    "Theme",
    "get_theme",
    "theme_from_payload",
]
