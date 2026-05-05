"""Cobalt Clone palette - homage to the classic command-and-control look."""

from __future__ import annotations

from lazygui.theme.tokens import ThemeTokens

TOKENS = ThemeTokens(
    identifier="cobalt_clone",
    display_name="Cobalt Clone",
    is_dark=True,
    background_base="#10171f",
    background_elevated="#162130",
    background_overlay="#0a0f15",
    background_terminal="#000814",
    surface_subtle="#1b2a3a",
    surface_strong="#243a52",
    border_subtle="#1b2a3a",
    border_strong="#2f4d6e",
    border_focus="#ff9e3b",
    text_primary="#e6edf3",
    text_secondary="#9fb3c8",
    text_muted="#5b738a",
    text_inverse="#10171f",
    text_on_accent="#10171f",
    accent="#ff9e3b",
    accent_hover="#ffb866",
    accent_pressed="#d97f1c",
    success="#56d364",
    warning="#f2cc60",
    danger="#ff6b6b",
    info="#4dabf7",
    selection_background="#1f3a5f",
    selection_foreground="#ffffff",
    scrollbar_track="#10171f",
    scrollbar_thumb="#2f4d6e",
    scrollbar_thumb_hover="#3f6991",
    radius_small_px=1,
    radius_medium_px=2,
    radius_large_px=4,
    spacing_unit_px=5,
)
