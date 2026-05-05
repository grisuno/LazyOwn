"""Catppuccin Mocha palette - warm pastel dark theme."""

from __future__ import annotations

from lazygui.theme.tokens import ThemeTokens

TOKENS = ThemeTokens(
    identifier="catppuccin_mocha",
    display_name="Catppuccin Mocha",
    is_dark=True,
    background_base="#1e1e2e",
    background_elevated="#181825",
    background_overlay="#11111b",
    background_terminal="#11111b",
    surface_subtle="#313244",
    surface_strong="#45475a",
    border_subtle="#313244",
    border_strong="#585b70",
    border_focus="#cba6f7",
    text_primary="#cdd6f4",
    text_secondary="#bac2de",
    text_muted="#7f849c",
    text_inverse="#1e1e2e",
    text_on_accent="#1e1e2e",
    accent="#cba6f7",
    accent_hover="#dec4ff",
    accent_pressed="#a583e0",
    success="#a6e3a1",
    warning="#f9e2af",
    danger="#f38ba8",
    info="#89dceb",
    selection_background="#45475a",
    selection_foreground="#cdd6f4",
    scrollbar_track="#1e1e2e",
    scrollbar_thumb="#45475a",
    scrollbar_thumb_hover="#585b70",
    radius_small_px=4,
    radius_medium_px=8,
    radius_large_px=12,
    spacing_unit_px=6,
)
