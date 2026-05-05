"""Tokyo Night palette - balanced dark blue theme."""

from __future__ import annotations

from lazygui.theme.tokens import ThemeTokens

TOKENS = ThemeTokens(
    identifier="tokyo_night",
    display_name="Tokyo Night",
    is_dark=True,
    background_base="#1a1b26",
    background_elevated="#1f2335",
    background_overlay="#16161e",
    background_terminal="#15151f",
    surface_subtle="#24283b",
    surface_strong="#2a2f45",
    border_subtle="#2a2f45",
    border_strong="#414868",
    border_focus="#7aa2f7",
    text_primary="#c0caf5",
    text_secondary="#a9b1d6",
    text_muted="#565f89",
    text_inverse="#1a1b26",
    text_on_accent="#1a1b26",
    accent="#7aa2f7",
    accent_hover="#9ab8ff",
    accent_pressed="#5d83d8",
    success="#9ece6a",
    warning="#e0af68",
    danger="#f7768e",
    info="#7dcfff",
    selection_background="#283457",
    selection_foreground="#c0caf5",
    scrollbar_track="#1a1b26",
    scrollbar_thumb="#414868",
    scrollbar_thumb_hover="#565f89",
    radius_small_px=3,
    radius_medium_px=6,
    radius_large_px=10,
    spacing_unit_px=6,
)
