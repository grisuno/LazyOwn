"""Tests for cli/themes.py.

Verifies registry membership, default fallback behaviour and the
``payload.json``-driven selector. No Textual or terminal interaction.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.themes import (  # noqa: E402
    DEFAULT_THEME_NAME,
    THEMES,
    Theme,
    get_theme,
    theme_from_payload,
)


def test_themes_registry_contains_required_entries() -> None:
    """The registry exposes the default plus the three alternates."""
    assert DEFAULT_THEME_NAME in THEMES
    assert {"default", "dim", "bright", "colorblind"} <= set(THEMES.keys())


def test_get_theme_returns_default_for_unknown_name() -> None:
    """Unknown names fall back to the default theme without raising."""
    assert get_theme("does-not-exist") is THEMES[DEFAULT_THEME_NAME]


def test_get_theme_is_case_insensitive() -> None:
    """Theme names are normalised before lookup."""
    assert get_theme("Bright") is THEMES["bright"]


def test_theme_from_payload_none_yields_default() -> None:
    """``None`` payloads return the default theme."""
    assert theme_from_payload(None) is THEMES[DEFAULT_THEME_NAME]


def test_theme_from_payload_picks_named_theme() -> None:
    """A valid payload key swaps the theme."""
    selected = theme_from_payload({"tui_theme": "colorblind"})
    assert selected is THEMES["colorblind"]


def test_theme_dataclass_is_immutable() -> None:
    """Themes are frozen dataclasses to prevent in-place mutation."""
    theme: Theme = THEMES[DEFAULT_THEME_NAME]
    try:
        theme.title = "x"  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("Theme should be immutable")
