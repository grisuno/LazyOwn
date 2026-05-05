"""Built-in palette registry.

Each palette module exposes a ``TOKENS`` instance of :class:`ThemeTokens`.
:func:`builtin_palettes` returns them all in declaration order so callers
need not enumerate filenames manually.
"""

from __future__ import annotations

from typing import Mapping

from lazygui.theme.palettes import (
    catppuccin_mocha,
    cobalt_clone,
    gruvbox_dark,
    solarized_light,
    tactical_green,
    tokyo_night,
)
from lazygui.theme.tokens import ThemeTokens


def builtin_palettes() -> Mapping[str, ThemeTokens]:
    """Return the built-in palette registry as ``id -> tokens``."""
    palettes: tuple[ThemeTokens, ...] = (
        tactical_green.TOKENS,
        tokyo_night.TOKENS,
        catppuccin_mocha.TOKENS,
        gruvbox_dark.TOKENS,
        cobalt_clone.TOKENS,
        solarized_light.TOKENS,
    )
    return {tokens.identifier: tokens for tokens in palettes}


__all__ = ["builtin_palettes"]
