"""Tests for cli.splash — the animated first-run overlay."""

from __future__ import annotations

import io
import unittest

from rich.console import Console

from cli.splash import (
    SPLASH_CONFIG,
    InstantEffect,
    SplashConfig,
    TypewriterEffect,
    render_splash,
)


def _console() -> tuple[io.StringIO, Console]:
    """Build a Rich console that writes into an in-memory buffer."""
    buffer = io.StringIO()
    return buffer, Console(
        file=buffer,
        force_terminal=True,
        color_system="truecolor",
        width=120,
    )


class SplashInstantEffectTests(unittest.TestCase):
    def test_instant_renders_every_line(self) -> None:
        buffer, console = _console()
        InstantEffect().render(
            console,
            ["alpha", "beta", "gamma"],
            {"accent": "bold cyan", "muted": "dim white"},
            SplashConfig(total_seconds=0, clear_after=False),
        )
        rendered = buffer.getvalue()
        self.assertIn("alpha", rendered)
        self.assertIn("beta", rendered)
        self.assertIn("gamma", rendered)

    def test_instant_does_not_block(self) -> None:
        _, console = _console()
        start = __import__("time").monotonic()
        InstantEffect().render(
            console,
            ["x" * 200],
            {"accent": "bold cyan", "muted": "dim white"},
            SPLASH_CONFIG,
        )
        elapsed = __import__("time").monotonic() - start
        self.assertLess(elapsed, 0.05)

    def test_instant_emits_ansi_for_known_tokens(self) -> None:
        buffer, console = _console()
        InstantEffect().render(
            console,
            ["hello"],
            {"accent": "bold cyan", "muted": "dim white"},
            SplashConfig(total_seconds=0, clear_after=False),
        )
        self.assertIn("\x1b[", buffer.getvalue())


class SplashTypewriterEffectTests(unittest.TestCase):
    def test_typewriter_renders_all_lines_when_total_seconds_high(self) -> None:
        buffer, console = _console()
        TypewriterEffect().render(
            console,
            ["ab", "cd"],
            {"accent": "bold cyan", "muted": "dim white"},
            SplashConfig(total_seconds=5.0, per_char_seconds=0.0, clear_after=False),
        )
        rendered = buffer.getvalue()
        self.assertIn("ab", rendered)
        self.assertIn("cd", rendered)


class SplashDispatchTests(unittest.TestCase):
    def test_render_splash_dispatches_instant_for_zero_seconds(self) -> None:
        buffer, console = _console()
        render_splash(
            console,
            ["hi"],
            payload=None,
            config=SplashConfig(total_seconds=0, clear_after=False),
        )
        self.assertIn("hi", buffer.getvalue())

    def test_render_splash_dispatches_instant_when_explicit(self) -> None:
        buffer, console = _console()
        render_splash(
            console,
            ["hi"],
            payload=None,
            config=SplashConfig(total_seconds=10.0, per_char_seconds=0.5, clear_after=False),
            effect_name="instant",
        )
        self.assertIn("hi", buffer.getvalue())

    def test_render_splash_unknown_effect_falls_back_to_instant(self) -> None:
        buffer, console = _console()
        render_splash(
            console,
            ["hi"],
            payload=None,
            config=SplashConfig(total_seconds=0, clear_after=False),
            effect_name="definitely_not_a_real_effect",
        )
        self.assertIn("hi", buffer.getvalue())

    def test_render_splash_uses_payload_theme_when_provided(self) -> None:
        buffer, console = _console()
        render_splash(
            console,
            ["styled"],
            payload={"tui_theme": "monokai"},
            config=SplashConfig(total_seconds=0, clear_after=False),
        )
        self.assertIn("\x1b[", buffer.getvalue())

    def test_render_splash_clear_after_emits_clear_escape(self) -> None:
        buffer, console = _console()
        render_splash(
            console,
            ["will-clear"],
            payload=None,
            config=SplashConfig(total_seconds=0, clear_after=True),
        )
        self.assertIn("\x1b[2J", buffer.getvalue())

    def test_render_splash_no_clear_when_disabled(self) -> None:
        buffer, console = _console()
        render_splash(
            console,
            ["stays"],
            payload=None,
            config=SplashConfig(total_seconds=0, clear_after=False),
        )
        self.assertNotIn("\x1b[2J", buffer.getvalue())


class SplashEdgeCaseTests(unittest.TestCase):
    def test_empty_lines_is_noop(self) -> None:
        buffer, console = _console()
        render_splash(
            console,
            [],
            payload=None,
            config=SplashConfig(total_seconds=0, clear_after=True),
        )
        self.assertNotIn("\x1b[2J", buffer.getvalue())

    def test_lines_with_brackets_render_verbatim(self) -> None:
        buffer, console = _console()
        ascii_art = [
            r"  __        __         _  _    ",
            r" / _\ ___  / _\  ___  | || |   ",
            r" \ \ / _ \ \ \ / _ \ | || |_  ",
            r" _\ \ (_) | _\ \ (_) ||__   _| ",
            r" \__/\___/ \__/\___/    |_|    ",
        ]
        render_splash(
            console,
            ascii_art,
            payload=None,
            config=SplashConfig(total_seconds=0, clear_after=False),
        )
        rendered = buffer.getvalue()
        for line in ascii_art:
            self.assertIn(line.strip().split()[0], rendered)


if __name__ == "__main__":
    unittest.main()
