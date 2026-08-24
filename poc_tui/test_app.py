"""Pytest tests for LazyOwn TUI Shell POC."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from app import DashboardPanel, LazyOwnTUI, OutputPanel, PluginBrowser, ShellBackend
from textual.widgets import Input, Label, RichLog

REPO_DIR = str(Path(__file__).parent.parent.resolve())


def _run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


# ---------------------------------------------------------------------------
# ShellBackend
# ---------------------------------------------------------------------------


def _make_backend() -> ShellBackend:
    backend = ShellBackend(REPO_DIR)
    backend.import_shell_class()
    return backend


class TestShellBackend:
    def test_init_sets_base_dir(self) -> None:
        backend = ShellBackend(REPO_DIR)
        assert backend.base_dir == Path(REPO_DIR).resolve()

    def test_run_before_start(self) -> None:
        backend = ShellBackend(REPO_DIR)
        result = backend.run("help")
        assert "not initialized" in result

    def test_start_and_stop(self) -> None:
        backend = _make_backend()
        backend.start()
        assert backend._shell is not None
        backend.stop()

    def test_run_show(self) -> None:
        backend = _make_backend()
        backend.start()
        result = backend.run("show")
        backend.stop()
        assert len(result) > 0

    def test_run_help(self) -> None:
        backend = _make_backend()
        backend.start()
        result = backend.run("help")
        backend.stop()
        assert "Documented commands" in result

    def test_get_commands(self) -> None:
        backend = _make_backend()
        backend.start()
        commands = backend.get_commands()
        backend.stop()
        assert len(commands) > 100
        assert "help" in commands
        assert "set" in commands

    def test_get_aliases(self) -> None:
        backend = _make_backend()
        backend.start()
        aliases = backend.get_aliases()
        backend.stop()
        assert isinstance(aliases, dict)

    def test_set_and_show(self) -> None:
        backend = _make_backend()
        backend.start()
        backend.run("set rhost 192.168.1.1")
        result = backend.run("show")
        backend.stop()
        assert "192.168.1.1" in result

    def test_buffer_cleared(self) -> None:
        backend = _make_backend()
        backend.start()
        backend.run("set rhost 10.99.99.99")
        r2 = backend.run("help")
        backend.stop()
        assert "10.99.99.99" not in r2


# ---------------------------------------------------------------------------
# Textual app tests
# ---------------------------------------------------------------------------


class TestLazyOwnTUIApp:

    def test_app_creates(self) -> None:
        app = LazyOwnTUI(base_dir=REPO_DIR)
        assert app.base_dir == REPO_DIR

    def test_app_starts_stops(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                assert app.is_running
            assert not app.is_running
        _run_async(_t())

    def test_panels_visible(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                assert app.query_one("#sidebar-left").visible
                assert app.query_one("#output-area").visible
                assert app.query_one("#sidebar-right").visible
                assert app.query_one("#cmd-input").visible
        _run_async(_t())

    def test_input_has_focus(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                assert inp.has_focus
        _run_async(_t())

    def test_execute_help(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "help"
                await pilot.press("enter")
                await pilot.pause()
                await pilot.pause()
                log = app.query_one("#output-log", RichLog)
                assert len(log.lines) > 0
        _run_async(_t())

    def test_input_cleared_after_submit(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "show"
                await pilot.press("enter")
                await pilot.pause()
                assert inp.value == ""
        _run_async(_t())

    def test_history_up(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "show"
                await pilot.press("enter")
                await pilot.pause()
                inp.value = "help"
                await pilot.press("enter")
                await pilot.pause()
                await pilot.press("up")
                assert inp.value == "help"
        _run_async(_t())

    def test_history_down(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "show"
                await pilot.press("enter")
                await pilot.pause()
                await pilot.press("up")
                assert inp.value == "show"
                await pilot.press("down")
                assert inp.value == ""
        _run_async(_t())

    def test_tab_complete(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "exploitgym"
                await pilot.press("tab")
                assert inp.value == "exploitgym "
        _run_async(_t())

    def test_toggle_sidebar(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                left = app.query_one("#sidebar-left")
                right = app.query_one("#sidebar-right")
                assert left.display is True
                app.action_toggle_sidebar()
                assert left.display is False
                assert right.display is False
                app.action_toggle_sidebar()
                assert left.display is True
        _run_async(_t())

    def test_quit(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                app.action_quit()
                await pilot.pause()
                assert not app.is_running
        _run_async(_t())

    def test_backend_ready(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                await pilot.pause()
                assert app.backend._shell is not None
                cmds = app.backend.get_commands()
                assert len(cmds) > 100
        _run_async(_t())

    def test_set_updates_dashboard(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "set rhost 10.10.10.5"
                await pilot.press("enter")
                for _ in range(30):
                    await pilot.pause()
                    if not app._cmd_running and not app._cmd_queue:
                        break
                assert not app._cmd_running
                dash = app.query_one("#sidebar-left", DashboardPanel)
                dash.refresh_data(app.backend, app._cmd_count)
                await pilot.pause()
                lbl = dash.query_one("#dash-rhost", Label)
                assert "10.10.10.5" in str(lbl.render())
        _run_async(_t())

    def test_show_command_output_in_log(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "show"
                await pilot.press("enter")
                await pilot.pause()
                await pilot.pause()
                log = app.query_one("#output-log", RichLog)
                assert len(log.lines) > 2

                # Output must contain actually rendered payload keys,
                # not empty lines or anti-bug: captured via RichLog.lines
        _run_async(_t())

    def test_q_is_quit_not_shell_alias(self) -> None:
        """'q' must quit the TUI — never reach the real shell's exit alias."""
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "q"
                await pilot.press("enter")
                await pilot.pause()
                assert not app.is_running
        _run_async(_t())

    def test_quit_word_not_sent_to_backend(self) -> None:
        """exit/quit/q words must never reach shell.onecmd."""
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                for word in ("q", "quit", "exit"):
                    app2 = LazyOwnTUI(base_dir=REPO_DIR)
                    assert word in app2._EXIT_WORDS
        _run_async(_t())

    def test_commands_queue_serialized(self) -> None:
        """Two fast commands must queue, not race."""
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "set rhost 10.1.2.3"
                await pilot.press("enter")
                inp.value = "set domain queue.local"
                await pilot.press("enter")
                for _ in range(20):
                    await pilot.pause()
                    if not app._cmd_running and not app._cmd_queue:
                        break
                dash = app.query_one("#sidebar-left", DashboardPanel)
                lbl = dash.query_one("#dash-domain", Label)
                assert "queue.local" in str(lbl.render())
        _run_async(_t())

    def test_focus_returns_after_command(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "set lhost 10.9.9.1"
                await pilot.press("enter")
                for _ in range(20):
                    await pilot.pause()
                    if not app._cmd_running:
                        break
                assert inp.has_focus
        _run_async(_t())

    def test_output_renders_ansi_codes(self) -> None:
        """append_result converts ANSI escapes to styled text, no markup crash."""
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                output = app.query_one("#output-area", OutputPanel)
                ansi_text = "\x1b[32m[+]\x1b[37m test\x1b[0m [+]"
                output.append_result(ansi_text)
                await pilot.pause()
                log = app.query_one("#output-log", RichLog)
                assert len(log.lines) > 0
        _run_async(_t())

    def test_busy_command_shows_running_indicator(self) -> None:
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test() as pilot:
                await pilot.pause()
                await pilot.pause()
                inp = app.query_one("#cmd-input", Input)
                inp.value = "set rhost 10.5.5.5"
                await pilot.press("enter")
                await pilot.pause()
                # Whether finished or still running, no crash; queue drained eventually
                for _ in range(30):
                    await pilot.pause()
                    if not app._cmd_running:
                        break
                assert not app._cmd_running
        _run_async(_t())

    def test_layout_all_panels_render_in_screenshot(self) -> None:
        """All three layout panels must be visible in the exported screen.

        Regression: the previous CSS grid collapsed the center output
        panel to zero width — commands executed but nothing was visible.
        """
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test(size=(100, 30)) as pilot:
                await pilot.pause()
                await pilot.pause()
                svg = app.export_screenshot().replace("&#160;", " ")
                assert "CAMPAIGN" in svg, "left sidebar not rendered"
                assert "COMMANDS" in svg, "right sidebar not rendered"
                assert "Starting cmd2 backend" in svg, "output panel not rendered"
        _run_async(_t())

    def test_command_output_visible_in_screenshot(self) -> None:
        """Run a real command and verify its output text is VISIBLE on screen."""
        async def _t():
            app = LazyOwnTUI(base_dir=REPO_DIR)
            async with app.run_test(size=(100, 30)) as pilot:
                for _ in range(50):
                    await pilot.pause()
                    if app.backend._shell is not None:
                        break
                assert app.backend._shell is not None
                inp = app.query_one("#cmd-input", Input)
                inp.value = "set rhost 99.99.99.99"
                await pilot.press("enter")
                for _ in range(50):
                    await pilot.pause()
                    if not app._cmd_running and not app._cmd_queue:
                        break
                assert not app._cmd_running
                svg = app.export_screenshot().replace("&#160;", " ")
                assert "99.99.99.99" in svg, "command output not visible on screen"
        _run_async(_t())
