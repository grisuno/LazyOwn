"""Solarized Light palette - low-contrast daylight option."""

from __future__ import annotations

from lazygui.theme.tokens import ThemeTokens

TOKENS = ThemeTokens(
    identifier="solarized_light",
    display_name="Solarized Light",
    is_dark=False,
    background_base="#fdf6e3",
    background_elevated="#eee8d5",
    background_overlay="#f5efdc",
    background_terminal="#fdf6e3",
    surface_subtle="#eee8d5",
    surface_strong="#dcd6c2",
    border_subtle="#dcd6c2",
    border_strong="#93a1a1",
    border_focus="#268bd2",
    text_primary="#073642",
    text_secondary="#586e75",
    text_muted="#93a1a1",
    text_inverse="#fdf6e3",
    text_on_accent="#fdf6e3",
    accent="#268bd2",
    accent_hover="#3aa0e6",
    accent_pressed="#1f6f9f",
    success="#859900",
    warning="#b58900",
    danger="#dc322f",
    info="#2aa198",
    selection_background="#eee8d5",
    selection_foreground="#073642",
    scrollbar_track="#eee8d5",
    scrollbar_thumb="#93a1a1",
    scrollbar_thumb_hover="#586e75",
    radius_small_px=3,
    radius_medium_px=6,
    radius_large_px=10,
    spacing_unit_px=6,
)
