"""Gruvbox Dark palette - retro warm contrast theme."""

from __future__ import annotations

from lazygui.theme.tokens import ThemeTokens

TOKENS = ThemeTokens(
    identifier="gruvbox_dark",
    display_name="Gruvbox Dark",
    is_dark=True,
    background_base="#282828",
    background_elevated="#32302f",
    background_overlay="#1d2021",
    background_terminal="#1d2021",
    surface_subtle="#3c3836",
    surface_strong="#504945",
    border_subtle="#3c3836",
    border_strong="#665c54",
    border_focus="#fabd2f",
    text_primary="#ebdbb2",
    text_secondary="#d5c4a1",
    text_muted="#928374",
    text_inverse="#282828",
    text_on_accent="#282828",
    accent="#fabd2f",
    accent_hover="#fdd35a",
    accent_pressed="#d79921",
    success="#b8bb26",
    warning="#fe8019",
    danger="#fb4934",
    info="#83a598",
    selection_background="#504945",
    selection_foreground="#fbf1c7",
    scrollbar_track="#282828",
    scrollbar_thumb="#504945",
    scrollbar_thumb_hover="#665c54",
    radius_small_px=2,
    radius_medium_px=4,
    radius_large_px=6,
    spacing_unit_px=6,
)
