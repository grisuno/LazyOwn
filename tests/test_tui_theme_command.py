"""Tests for the cli.tui_theme command logic."""

from __future__ import annotations

import unittest

from cli import tui_theme
from cli.themes import DEFAULT_THEME_NAME, THEMES


class RecordingSave:
    """Minimal stand-in for the payload writer used in tests."""

    def __init__(self) -> None:
        self.calls: list[int] = []

    def __call__(self, payload: dict) -> None:
        self.calls.append(id(payload))


def _payload(**overrides: object) -> dict:
    """Build a fresh payload dict with optional overrides."""
    base: dict = {"tui_theme": DEFAULT_THEME_NAME}
    base.update(overrides)
    return base


class TuiThemeListingTests(unittest.TestCase):
    def test_empty_args_lists_every_registered_theme(self) -> None:
        save = RecordingSave()
        payload = _payload()
        result = tui_theme.run([], payload, save)
        for name in tui_theme.THEME_ORDER:
            with self.subTest(theme=name):
                self.assertIn(name, result)
        self.assertEqual(save.calls, [])

    def test_listing_marks_current_theme(self) -> None:
        save = RecordingSave()
        payload = _payload(tui_theme="gruvbox")
        result = tui_theme.run([], payload, save)
        self.assertIn("* gruvbox", result)
        self.assertIn("current: gruvbox", result)


class TuiThemeSwitchTests(unittest.TestCase):
    def test_known_name_switches_and_persists(self) -> None:
        save = RecordingSave()
        payload = _payload()
        result = tui_theme.run(["monokai"], payload, save)
        self.assertEqual(payload["tui_theme"], "monokai")
        self.assertIn("default -> monokai", result)
        self.assertEqual(len(save.calls), 1)

    def test_unknown_name_does_not_mutate(self) -> None:
        save = RecordingSave()
        payload = _payload(tui_theme="gruvbox")
        result = tui_theme.run(["definitely_not_a_theme"], payload, save)
        self.assertEqual(payload["tui_theme"], "gruvbox")
        self.assertIn("unknown theme", result)
        self.assertEqual(save.calls, [])

    def test_case_insensitive_lookup(self) -> None:
        save = RecordingSave()
        payload = _payload()
        result = tui_theme.run(["Gruvbox"], payload, save)
        self.assertEqual(payload["tui_theme"], "gruvbox")
        self.assertIn("default -> gruvbox", result)

    def test_reset_returns_to_default(self) -> None:
        save = RecordingSave()
        payload = _payload(tui_theme="monokai")
        result = tui_theme.run(["reset"], payload, save)
        self.assertEqual(payload["tui_theme"], DEFAULT_THEME_NAME)
        self.assertIn("monokai -> default", result)


class TuiThemeCycleTests(unittest.TestCase):
    def test_cycle_advances_in_theme_order(self) -> None:
        save = RecordingSave()
        payload = _payload(tui_theme="default")
        result = tui_theme.run(["cycle"], payload, save)
        next_name = tui_theme.THEME_ORDER[1]
        self.assertEqual(payload["tui_theme"], next_name)
        self.assertIn(f"default -> {next_name}", result)

    def test_cycle_wraps_around(self) -> None:
        save = RecordingSave()
        payload = _payload(tui_theme=tui_theme.THEME_ORDER[-1])
        result = tui_theme.run(["cycle"], payload, save)
        self.assertEqual(payload["tui_theme"], tui_theme.THEME_ORDER[0])
        self.assertEqual(len(save.calls), 1)

    def test_prev_walks_backwards_and_wraps(self) -> None:
        save = RecordingSave()
        payload = _payload(tui_theme="default")
        result = tui_theme.run(["prev"], payload, save)
        self.assertEqual(
            payload["tui_theme"],
            tui_theme.THEME_ORDER[-1],
        )
        self.assertIn("default -> ", result)


class TuiThemeRegistrationConsistencyTests(unittest.TestCase):
    def test_theme_order_covers_every_registered_theme(self) -> None:
        self.assertEqual(set(tui_theme.THEME_ORDER), set(THEMES.keys()))

    def test_theme_order_has_no_duplicates(self) -> None:
        self.assertEqual(len(tui_theme.THEME_ORDER), len(set(tui_theme.THEME_ORDER)))


if __name__ == "__main__":
    unittest.main()
