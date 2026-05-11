"""Tests for cli/reactive_hints.py.

Uses a synthetic GraphAdvisor double so the test suite runs without a real
graphify graph on disk. The double is injected via duck-typing — the module
calls only ``advisor.suggest_next(recent_commands, limit)`` so a minimal
stub suffices.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.reactive_hints import (  # noqa: E402
    SKIP_COMMANDS,
    _extract_labels,
    _first_token,
    _truncate,
    render_inline_hints,
)


class _FakeAdvisor:
    """Minimal advisor double used in tests."""

    def __init__(self, suggestions: list[dict]) -> None:
        self._suggestions = suggestions
        self.called_with: list[tuple] = []

    def suggest_next(self, recent_commands: list[str], limit: int = 3) -> list[dict]:
        self.called_with.append((recent_commands, limit))
        return self._suggestions[:limit]


@pytest.fixture
def advisor_with_three_hints() -> _FakeAdvisor:
    return _FakeAdvisor(
        [
            {"label": "do_lazynmap", "id": "lazyown_do_lazynmap"},
            {"label": "do_gobuster", "id": "lazyown_do_gobuster"},
            {"label": "do_enum4linux", "id": "lazyown_do_enum4linux"},
        ]
    )


@pytest.fixture
def empty_advisor() -> _FakeAdvisor:
    return _FakeAdvisor([])


class TestFirstToken:
    def test_extracts_first_word(self) -> None:
        assert _first_token("lazynmap -sV 10.0.0.1") == "lazynmap"

    def test_single_word(self) -> None:
        assert _first_token("ping") == "ping"

    def test_empty_string(self) -> None:
        assert _first_token("") == ""

    def test_whitespace_only(self) -> None:
        assert _first_token("   ") == ""


class TestTruncate:
    def test_short_string_unchanged(self) -> None:
        assert _truncate("hello", 10) == "hello"

    def test_exact_length_unchanged(self) -> None:
        assert _truncate("1234567890", 10) == "1234567890"

    def test_long_string_truncated(self) -> None:
        result = _truncate("do_very_long_command_name", 10)
        assert len(result) == 10
        assert result.endswith("…")

    def test_truncation_preserves_start(self) -> None:
        result = _truncate("abcdefghij_extra", 10)
        assert result.startswith("abcdefghi")


class TestExtractLabels:
    def test_picks_label_over_id(self) -> None:
        suggestions = [{"label": "do_ping", "id": "lazyown_do_ping"}]
        assert _extract_labels(suggestions, 3) == ["do_ping"]

    def test_falls_back_to_id_when_no_label(self) -> None:
        suggestions = [{"label": "", "id": "lazyown_do_ping"}]
        assert _extract_labels(suggestions, 3) == ["lazyown_do_ping"]

    def test_skips_empty_entries(self) -> None:
        suggestions = [{"label": "", "id": ""}]
        assert _extract_labels(suggestions, 3) == []

    def test_respects_limit(self) -> None:
        suggestions = [{"label": f"cmd_{i}"} for i in range(10)]
        assert len(_extract_labels(suggestions, 3)) == 3

    def test_truncates_long_labels(self) -> None:
        suggestions = [{"label": "x" * 50}]
        labels = _extract_labels(suggestions, 3)
        assert len(labels[0]) <= 25


class TestRenderInlineHints:
    def test_disabled_flag_skips_render(self, advisor_with_three_hints: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE") as mock_console:
            render_inline_hints(advisor_with_three_hints, "lazynmap", enabled=False)
            mock_console.print.assert_not_called()

    def test_skip_command_skips_render(self, advisor_with_three_hints: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE") as mock_console:
            render_inline_hints(advisor_with_three_hints, "help", enabled=True)
            mock_console.print.assert_not_called()

    def test_empty_command_skips_render(self, advisor_with_three_hints: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE") as mock_console:
            render_inline_hints(advisor_with_three_hints, "   ", enabled=True)
            mock_console.print.assert_not_called()

    def test_empty_suggestions_skips_render(self, empty_advisor: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE") as mock_console:
            render_inline_hints(empty_advisor, "lazynmap", enabled=True)
            mock_console.print.assert_not_called()

    def test_normal_command_renders_hint(self, advisor_with_three_hints: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE") as mock_console:
            render_inline_hints(advisor_with_three_hints, "lazynmap", limit=3, enabled=True)
            mock_console.print.assert_called_once()

    def test_advisor_called_with_correct_command(self, advisor_with_three_hints: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE"):
            render_inline_hints(advisor_with_three_hints, "gobuster -w wordlist.txt", limit=2, enabled=True)
        assert advisor_with_three_hints.called_with == [(["gobuster"], 2)]

    def test_exception_in_advisor_does_not_propagate(self) -> None:
        broken_advisor = MagicMock()
        broken_advisor.suggest_next.side_effect = RuntimeError("graph exploded")
        with patch("cli.reactive_hints._HINT_CONSOLE") as mock_console:
            render_inline_hints(broken_advisor, "lazynmap", enabled=True)
            mock_console.print.assert_not_called()

    def test_all_skip_commands_are_skipped(self, advisor_with_three_hints: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE") as mock_console:
            for cmd in SKIP_COMMANDS:
                render_inline_hints(advisor_with_three_hints, cmd, enabled=True)
            mock_console.print.assert_not_called()

    def test_limit_is_passed_to_advisor(self, advisor_with_three_hints: _FakeAdvisor) -> None:
        with patch("cli.reactive_hints._HINT_CONSOLE"):
            render_inline_hints(advisor_with_three_hints, "lazynmap", limit=1, enabled=True)
        _, called_limit = advisor_with_three_hints.called_with[0]
        assert called_limit == 1
