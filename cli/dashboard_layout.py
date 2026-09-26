"""Responsive layout decisions for the Textual operator dashboard.

Small terminals crush the fixed three-column layout. This module keeps
the width thresholds and panel visibility rules in one testable place;
the dashboard app only toggles CSS classes based on these answers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardLayoutConfig:
    """Centralized knobs for responsive breakpoints."""

    narrow_width: int = 120
    compact_width: int = 80


DEFAULT_LAYOUT_CONFIG = DashboardLayoutConfig()

LAYOUT_WIDE = "wide"
LAYOUT_NARROW = "narrow"
LAYOUT_COMPACT = "compact"


def layout_mode(width: int, config: DashboardLayoutConfig = DEFAULT_LAYOUT_CONFIG) -> str:
    """Return the layout bucket for a terminal width.

    Args:
        width: Terminal width in columns.
        config: Breakpoint configuration.

    Returns:
        wide, narrow or compact.
    """
    if width < config.compact_width:
        return LAYOUT_COMPACT
    if width < config.narrow_width:
        return LAYOUT_NARROW
    return LAYOUT_WIDE


def hidden_panels(mode: str) -> tuple[str, ...]:
    """Return panel ids hidden in the given layout mode.

    Args:
        mode: One of wide, narrow or compact.

    Returns:
        Tuple of widget ids to hide. Wide hides nothing, narrow hides
        the reasoning panel, compact additionally hides the right column.
    """
    if mode == LAYOUT_COMPACT:
        return ("reasoning-panel", "right-col")
    if mode == LAYOUT_NARROW:
        return ("reasoning-panel",)
    return ()


__all__ = [
    "DashboardLayoutConfig",
    "DEFAULT_LAYOUT_CONFIG",
    "LAYOUT_WIDE",
    "LAYOUT_NARROW",
    "LAYOUT_COMPACT",
    "layout_mode",
    "hidden_panels",
]
