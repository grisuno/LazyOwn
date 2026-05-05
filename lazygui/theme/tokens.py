"""Design tokens describing a single theme.

Tokens are immutable. They cover colours, typography sizes and corner radii.
Anything that should differ between themes must be expressed here so the QSS
builder can render it without consulting any other source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ThemeTokens:
    """Atomic design tokens for one theme variant."""

    identifier: str
    display_name: str
    is_dark: bool

    background_base: str
    background_elevated: str
    background_overlay: str
    background_terminal: str

    surface_subtle: str
    surface_strong: str

    border_subtle: str
    border_strong: str
    border_focus: str

    text_primary: str
    text_secondary: str
    text_muted: str
    text_inverse: str
    text_on_accent: str

    accent: str
    accent_hover: str
    accent_pressed: str

    success: str
    warning: str
    danger: str
    info: str

    selection_background: str
    selection_foreground: str

    scrollbar_track: str
    scrollbar_thumb: str
    scrollbar_thumb_hover: str

    radius_small_px: int
    radius_medium_px: int
    radius_large_px: int

    spacing_unit_px: int
