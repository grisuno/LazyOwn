"""Operator-facing ``tui_theme`` command logic.

The cmd2 ``do_tui_theme`` method in ``lazyown.py`` delegates to
:func:`run` here. Keeping the logic out of the shell makes it
trivially testable: pass a payload dict, a payload-saver callable,
and a sys.argv-style argument list, get back a human-readable
result string and a side effect on the payload.

Usage from the shell:

    tui_theme                    # list all themes, mark current
    tui_theme gruvbox            # switch active theme
    tui_theme cycle              # next theme in deterministic order
    tui_theme prev               # previous theme
    tui_theme reset              # fall back to default

The command is intentionally idempotent and never raises -- any
invalid input is reported to the operator without mutating state.
"""

from __future__ import annotations

from typing import Callable, MutableMapping, Sequence

from cli.themes import DEFAULT_THEME_NAME, THEMES, get_theme

THEME_ORDER: tuple[str, ...] = (
    "default",
    "dim",
    "bright",
    "colorblind",
    "solarized",
    "monokai",
    "gruvbox",
    "high_contrast",
)
"""Deterministic ordering for ``cycle`` / ``prev`` / listing.

Order roughly follows contrast and popularity: the four original
themes first (default/dim/bright/colorblind), then the four
additions (solarized/monokai/gruvbox/high_contrast). Operators who
bind ``tui_theme cycle`` to a hotkey get a predictable sequence.
"""


def _set_theme(payload: MutableMapping[str, object], name: str) -> None:
    """Persist ``name`` into ``payload[\"tui_theme\"]`` after validation.

    Args:
        payload: Mapping mutated in place. The ``tui_theme`` key is
            set to the canonical lowercase theme name.
        name: Requested theme name. Unknown names are silently
            coerced to :data:`cli.themes.DEFAULT_THEME_NAME` so
            ``tui_theme bogus`` cannot leave the operator without a
            usable theme.
    """
    resolved = get_theme(name)
    payload["tui_theme"] = resolved.name


def _format_listing(current: str) -> str:
    """Render the theme table shown by ``tui_theme`` with no args.

    Args:
        current: Name of the active theme. The matching row is
            flagged with a marker so the operator knows the state.

    Returns:
        Multi-line text block ready to print.
    """
    lines = ["available TUI themes:"]
    width = max(len(name) for name in THEME_ORDER)
    for name in THEME_ORDER:
        marker = "*" if name == current else " "
        theme = THEMES[name]
        lines.append(f"  {marker} {name.ljust(width)}  {theme.title} / {theme.accent}")
    lines.append(f"current: {current}  (use 'tui_theme <name>' to switch)")
    return "\n".join(lines)


def _cycle(payload: MutableMapping[str, object], direction: int) -> str:
    """Advance the active theme by one slot in :data:`THEME_ORDER`.

    Args:
        payload: Mapping mutated in place with the new theme name.
        direction: ``+1`` for next, ``-1`` for previous. Any other
            value is treated as ``+1``.

    Returns:
        Single-line confirmation of the new active theme.
    """
    current = str(payload.get("tui_theme", DEFAULT_THEME_NAME))
    try:
        index = THEME_ORDER.index(current)
    except ValueError:
        index = 0
    step = 1 if direction >= 0 else -1
    new_name = THEME_ORDER[(index + step) % len(THEME_ORDER)]
    _set_theme(payload, new_name)
    return f"theme: {current} -> {new_name}"


def run(
    args: Sequence[str],
    payload: MutableMapping[str, object],
    save: Callable[[MutableMapping[str, object]], None],
) -> str:
    """Execute the ``tui_theme`` command.

    Args:
        args: Argument list (excluding the verb itself). Empty list
            lists themes; one positional argument switches or moves
            the active theme; ``reset`` clears back to default.
        payload: Live payload mapping. Mutated in place on theme
            changes; the operator's selection persists across shell
            restarts because :func:`save` writes the JSON.
        save: Callable invoked after every mutation so the on-disk
            ``payload.json`` matches the in-memory state. The shell
            binds this to the existing payload writer; tests pass a
            no-op recorder.

    Returns:
        Human-readable result string. Always a single block of text
        suitable for direct printing.
    """
    current = str(payload.get("tui_theme", DEFAULT_THEME_NAME))
    if not args:
        return _format_listing(current)

    verb = args[0].strip().lower()
    if verb in ("reset", "default"):
        _set_theme(payload, DEFAULT_THEME_NAME)
        save(payload)
        return f"theme: {current} -> {DEFAULT_THEME_NAME}"
    if verb == "cycle":
        message = _cycle(payload, 1)
        save(payload)
        return message
    if verb == "prev":
        message = _cycle(payload, -1)
        save(payload)
        return message
    if verb in THEMES:
        _set_theme(payload, verb)
        save(payload)
        return f"theme: {current} -> {verb}"
    return f"unknown theme: {verb!r}. available: {', '.join(THEME_ORDER)}. current: {current}"


__all__ = ["THEME_ORDER", "run"]
