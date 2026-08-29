"""Tests for the cli/style semantic token layer."""

from __future__ import annotations

import io
import unittest

from rich.console import Console

from cli import style
from cli.themes import DEFAULT_THEME_NAME, THEMES


class StyleTokenTests(unittest.TestCase):
    def test_known_token_returns_theme_attribute(self) -> None:
        for name, theme in THEMES.items():
            with self.subTest(theme=name):
                self.assertEqual(style.style("title", theme), theme.title)
                self.assertEqual(style.style("accent", theme), theme.accent)

    def test_unknown_token_falls_back_to_white(self) -> None:
        self.assertEqual(style.style("not_a_token"), "white")
        self.assertEqual(style.style("not_a_token", THEMES[DEFAULT_THEME_NAME]), "white")

    def test_active_tokens_covers_every_key(self) -> None:
        tokens = style.active_tokens(None)
        self.assertEqual(set(tokens), set(style.TOKEN_KEYS))
        for value in tokens.values():
            self.assertIsInstance(value, str)
            self.assertGreater(len(value), 0)

    def test_active_tokens_honours_payload(self) -> None:
        bright = style.active_tokens({"tui_theme": "bright"})
        default = style.active_tokens({"tui_theme": "default"})
        self.assertEqual(bright["title"], THEMES["bright"].title)
        self.assertEqual(default["title"], THEMES["default"].title)
        self.assertNotEqual(bright["title"], default["title"])

    def test_paint_returns_rich_text_with_style(self) -> None:
        painted = style.paint("hello", "accent", {"tui_theme": "colorblind"})
        self.assertEqual(painted.plain, "hello")
        self.assertEqual(painted.style, THEMES["colorblind"].accent)

    def test_render_prompt_emits_segments_separated_by_bar(self) -> None:
        buffer = io.StringIO()
        console = Console(file=buffer, force_terminal=True, color_system="truecolor", width=120)
        style.render_prompt(
            console,
            [("lazyown", "accent"), ("10.10.11.5", "title"), ("recon", "hint")],
        )
        rendered = buffer.getvalue()
        self.assertIn("lazyown", rendered)
        self.assertIn("10.10.11.5", rendered)
        self.assertIn("recon", rendered)
        self.assertIn("\u2502", rendered)
        self.assertNotIn("\n", rendered.rstrip(""))
        self.assertIn("\x1b[", rendered)

    def test_render_prompt_empty_is_noop(self) -> None:
        buffer = io.StringIO()
        console = Console(file=buffer, force_terminal=True, color_system="truecolor", width=120)
        style.render_prompt(console, [])
        self.assertEqual(buffer.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
