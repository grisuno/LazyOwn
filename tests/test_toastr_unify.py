"""BDD tests for the unified toastr presentation layer.

Given three surfaces (cmd2 shell, yara sentinel popup, C2 builder)
raise operator-facing toastr boxes,
When they render,
Then every severity resolves through the single toast-bus style table,
the shell panel wraps long messages and falls back on empty input,
and the sentinel popup keeps its field layout without local style
dictionaries drifting from the theme.
"""

from __future__ import annotations

from cli.toast_bus import (
    rich_toastr_panel,
    sentinel_toast_panel,
    shell_hint_bypass,
    toastr_severity_style,
)


def test_severity_table_covers_every_surface_level():
    """Given shell and sentinel severities, the table resolves all of them."""
    for level in ("success", "error", "warning", "info", "low", "medium", "high", "critical"):
        style = toastr_severity_style(level)
        assert style["border_style"], level
        assert style["text_style"], level


def test_unknown_severity_falls_back_to_info():
    """Given an unmapped severity string, the info style is used."""
    assert toastr_severity_style("does-not-exist") == toastr_severity_style("info")


def test_plain_text_message_wraps_and_adapts():
    """Given a long worded message, the panel wraps inside its width."""
    message = " ".join(["lorem"] * 60)
    panel = rich_toastr_panel(message, "info", terminal_width=100)
    plain = getattr(panel.renderable, "plain", "")
    assert "\n" in plain
    for line in plain.splitlines():
        assert len(line) <= 100


def test_empty_message_falls_back_like_legacy():
    """Given an empty message, the legacy Empty-message fallback applies."""
    panel = rich_toastr_panel("", "info", terminal_width=80)
    assert getattr(panel.renderable, "plain", "") == "Empty message"


def test_markup_is_escaped_for_plain_text():
    """Given a message with markup characters, the renderable stays plain."""
    panel = rich_toastr_panel("[bold]boom[/bold]", "info", terminal_width=80)
    assert getattr(panel.renderable, "plain", "") == "[bold]boom[/bold]"


def test_sentinel_panel_keeps_field_layout():
    """Given sentinel fields, the popup panel keeps the documented layout."""
    panel = sentinel_toast_panel(
        "report.yaml", "suspicious decode", "lazy enc", "entropy 7.9", severity="critical"
    )
    plain = panel.renderable.plain
    for marker in ("File:", "Info:", "Commands:", "Details:"):
        assert marker in plain


def test_sentinel_severity_selects_border():
    """Given a sentinel severity, the border follows the unified table."""
    assert str(sentinel_toast_panel("a", "b", "c", "d", "high").border_style) == "red"
    assert str(sentinel_toast_panel("a", "b", "c", "d", "critical").border_style) == "magenta"


class _SpyConsole:
    """Console double that records bypass output without styling."""

    def __init__(self) -> None:
        self.bypassed: list[tuple[str, str]] = []

    def print(self, message: str, style: str = "", **_unused) -> None:
        """Record the flat bypass line."""
        self.bypassed.append((message, style))


def test_shell_hint_bypass_prints_flat_line():
    """Given hints off, the shell prints a flat styled line instead of a panel."""
    console = _SpyConsole()
    assert shell_hint_bypass(console, "down", "warning") is True
    assert console.bypassed == [("[WARNING] down", "bold yellow")]


def test_shell_hint_bypass_keeps_empty_fallback():
    """Given an empty message with hints off, the same fallback text is printed."""
    console = _SpyConsole()
    assert shell_hint_bypass(console, "", "info") is True
    assert console.bypassed == [("[INFO] Empty message", "bold blue")]
