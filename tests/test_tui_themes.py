"""Tests for the four new themes added on top of the original four.

The original theme set (default, dim, bright, colorblind) is covered
by test_tui_style.py. These tests assert the *new* themes (solarized,
monokai, gruvbox, high_contrast) are wired correctly, that their hex
colors parse under Rich's truecolor engine, and that the resolver
returns the right theme for each name.
"""

from __future__ import annotations

import io
import unittest

from rich.console import Console
from rich.text import Text

from cli.themes import DEFAULT_THEME_NAME, THEMES, get_theme, theme_from_payload


NEW_THEME_NAMES: tuple[str, ...] = (
    "solarized",
    "monokai",
    "gruvbox",
    "high_contrast",
)
ALL_TOKEN_KEYS: tuple[str, ...] = (
    "title",
    "subtitle",
    "accent",
    "muted",
    "border",
    "success",
    "warning",
    "danger",
    "hint",
)


class NewThemeRegistrationTests(unittest.TestCase):
    def test_every_new_theme_is_registered(self) -> None:
        for name in NEW_THEME_NAMES:
            with self.subTest(theme=name):
                self.assertIn(name, THEMES)

    def test_original_themes_remain_registered(self) -> None:
        for original in ("default", "dim", "bright", "colorblind"):
            self.assertIn(original, THEMES)
        self.assertEqual(THEMES[DEFAULT_THEME_NAME].name, "default")

    def test_get_theme_resolves_every_new_name(self) -> None:
        for name in NEW_THEME_NAMES:
            with self.subTest(theme=name):
                self.assertIs(get_theme(name), THEMES[name])

    def test_get_theme_uses_case_insensitive_lookup(self) -> None:
        self.assertIs(get_theme("Gruvbox"), THEMES["gruvbox"])
        self.assertIs(get_theme("  SOLARIZED  "), THEMES["solarized"])

    def test_unknown_name_falls_back_to_default(self) -> None:
        self.assertIs(get_theme("not_a_real_theme"), THEMES[DEFAULT_THEME_NAME])
        self.assertIs(get_theme(""), THEMES[DEFAULT_THEME_NAME])
        self.assertIs(get_theme(None), THEMES[DEFAULT_THEME_NAME])

    def test_theme_from_payload_picks_each_new_theme(self) -> None:
        for name in NEW_THEME_NAMES:
            with self.subTest(theme=name):
                self.assertIs(
                    theme_from_payload({"tui_theme": name}),
                    THEMES[name],
                )

    def test_new_themes_have_unique_color_palettes(self) -> None:
        titles = {THEMES[name].title for name in NEW_THEME_NAMES}
        self.assertEqual(len(titles), len(NEW_THEME_NAMES))

    def test_new_themes_have_non_empty_token_values(self) -> None:
        for name in NEW_THEME_NAMES:
            theme = THEMES[name]
            for token in ALL_TOKEN_KEYS:
                with self.subTest(theme=name, token=token):
                    value = getattr(theme, token)
                    self.assertIsInstance(value, str)
                    self.assertGreater(len(value), 0)


class NewThemeRenderTests(unittest.TestCase):
    """Render every token of every new theme through Rich.

    This catches the case where a hex color like ``#b58900`` is set as
    a token style but Rich silently drops it (e.g. when color_system
    is downgraded to ``"standard"``). We force truecolor and assert
    ANSI escapes are emitted.
    """

    def test_every_token_renders_with_ansi_escapes(self) -> None:
        for name in NEW_THEME_NAMES:
            theme = THEMES[name]
            for token in ALL_TOKEN_KEYS:
                buffer = io.StringIO()
                console = Console(
                    file=buffer,
                    force_terminal=True,
                    color_system="truecolor",
                    width=120,
                )
                text = Text("x", style=getattr(theme, token))
                console.print(text, end="")
                rendered = buffer.getvalue()
                with self.subTest(theme=name, token=token):
                    self.assertIn("\x1b[", rendered, msg=f"no ANSI for {name}.{token}")

    def test_every_token_renders_with_ansi_escapes_in_256color(self) -> None:
        for name in NEW_THEME_NAMES:
            theme = THEMES[name]
            for token in ALL_TOKEN_KEYS:
                buffer = io.StringIO()
                console = Console(
                    file=buffer,
                    force_terminal=True,
                    color_system="256",
                    width=120,
                )
                text = Text("x", style=getattr(theme, token))
                console.print(text, end="")
                rendered = buffer.getvalue()
                with self.subTest(theme=name, token=token, color="256"):
                    self.assertIn("\x1b[", rendered)


if __name__ == "__main__":
    unittest.main()
