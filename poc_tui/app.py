"""LazyOwn TUI Shell — Proof of Concept.

cmd2 as backend, Textual as frontend. Zero migration needed.
All 724+ commands, plugins, aliases, hooks — everything works.

Run from LazyOwn root:
    python3 poc_tui/app.py
"""

from __future__ import annotations

import io
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import (
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    RichLog,
    Static,
)


# ---------------------------------------------------------------------------
# Shell backend — wraps the real LazyOwnShell
# ---------------------------------------------------------------------------

class ShellBackend:
    """Run the real cmd2 LazyOwnShell in-process, capture all output."""

    def __init__(self, base_dir: str = ".") -> None:
        self.base_dir = Path(base_dir).resolve()
        self._shell: Any = None
        self._output_buffer = io.StringIO()
        self._lock = threading.Lock()

    def import_shell_class(self) -> None:
        """Import LazyOwnShell in the main thread (required for signal handlers)."""
        os.chdir(self.base_dir)
        if str(self.base_dir) not in sys.path:
            sys.path.insert(0, str(self.base_dir))
        saved_argv = sys.argv[:]
        sys.argv = [str(Path(self.base_dir) / "lazyown.py")]
        try:
            from lazyown import LazyOwnShell
            self._shell_class = LazyOwnShell
        except SystemExit:
            from lazyown import LazyOwnShell
            self._shell_class = LazyOwnShell
        finally:
            sys.argv = saved_argv

    def start(self) -> None:
        """Instantiate LazyOwnShell (must be called from main thread)."""
        saved_argv = sys.argv[:]
        sys.argv = [str(Path(self.base_dir) / "lazyown.py")]
        try:
            self._shell = self._shell_class()
            self._shell.preloop()
        except SystemExit:
            pass
        finally:
            sys.argv = saved_argv

    def run(self, cmd: str) -> str:
        """Execute a command and return its captured output."""
        if self._shell is None:
            return "[shell not initialized]"

        with self._lock:
            self._output_buffer.truncate(0)
            self._output_buffer.seek(0)
            old_shell_stdout = self._shell.stdout
            old_sys_stdout = sys.stdout
            try:
                self._shell.stdout = self._output_buffer
                sys.stdout = self._output_buffer
                self._shell.onecmd(cmd)
            except SystemExit:
                pass
            except Exception as e:
                self._output_buffer.write(f"\n[shell error] {e}\n")
            finally:
                self._shell.stdout = old_shell_stdout
                sys.stdout = old_sys_stdout

            output = self._output_buffer.getvalue()
            return output

    def get_commands(self) -> dict[str, str]:
        """Return {command_name: help_text} from the live shell."""
        if self._shell is None:
            return {}
        commands = {}
        for name in sorted(self._shell.get_all_commands()):
            try:
                doc = self._shell.get_command_help(name) or ""
            except Exception:
                doc = ""
            commands[name] = doc.strip()
        return commands

    def get_aliases(self) -> dict[str, str]:
        if self._shell is None:
            return {}
        return dict(getattr(self._shell, "aliases", {}))

    def stop(self) -> None:
        if self._shell is not None:
            try:
                self._shell.postloop()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Custom widgets
# ---------------------------------------------------------------------------

class DashboardPanel(Static):
    """Left sidebar: live campaign state from payload.json."""

    def __init__(self, base_dir: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.base_dir = base_dir

    def compose(self) -> ComposeResult:
        with Vertical(id="dash-inner"):
            yield Label(" CAMPAIGN ", id="dash-title")
            yield Label("─" * 20, id="dash-sep1")
            yield Label("Target", id="dash-rhost-label")
            yield Label("—", id="dash-rhost")
            yield Label("Local", id="dash-lhost-label")
            yield Label("—", id="dash-lhost")
            yield Label("Domain", id="dash-domain-label")
            yield Label("—", id="dash-domain")
            yield Label("─" * 20, id="dash-sep2")
            yield Label(" Phase ", id="dash-phase-label")
            yield Label("—", id="dash-phase")
            yield Label("─" * 20, id="dash-sep3")
            yield Label(" Aliases ", id="dash-aliases-label")
            yield Label("0 loaded", id="dash-aliases-count")
            yield Label("─" * 20, id="dash-sep4")
            yield Label(" Session ", id="dash-session-label")
            yield Label(datetime.now().strftime("%H:%M:%S"), id="dash-time")
            yield Label("0 cmds", id="dash-cmd-count")

    def refresh_data(self, backend: ShellBackend, cmd_count: int = 0) -> None:
        """Pull latest state from the LIVE shell params (not stale disk file)."""
        payload: dict = {}
        if backend._shell is not None:
            try:
                payload = dict(getattr(backend._shell, "params", {}) or {})
            except Exception:
                payload = {}
        if not payload:
            payload_path = Path(self.base_dir) / "payload.json"
            try:
                import json
                payload = json.loads(payload_path.read_text())
            except Exception:
                payload = {}

        rhost = payload.get("rhost", "—") or "—"
        lhost = payload.get("lhost", "—") or "—"
        domain = payload.get("domain", "—") or "—"
        aliases = backend.get_aliases()

        self.query_one("#dash-rhost", Label).update(f"  {rhost}")
        self.query_one("#dash-lhost", Label).update(f"  {lhost}")
        self.query_one("#dash-domain", Label).update(f"  {domain}")
        self.query_one("#dash-aliases-count", Label).update(f"  {len(aliases)} loaded")
        self.query_one("#dash-cmd-count", Label).update(f"  {cmd_count} cmds")
        self.query_one("#dash-time", Label).update(
            datetime.now().strftime("%H:%M:%S")
        )


class PluginBrowser(Static):
    """Right sidebar: command list from the real cmd2 shell."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Vertical(id="plugin-inner"):
            yield Label(" COMMANDS ", id="plugin-title")
            yield Label("─" * 20, id="plugin-sep")
            yield ListView(id="plugin-list")

    def update_commands(self, commands: dict[str, str]) -> None:
        list_view = self.query_one("#plugin-list", ListView)
        list_view.clear()
        by_cat: dict[str, list[tuple[str, str]]] = {}
        for name, help_text in sorted(commands.items()):
            cat = self._guess_category(name, help_text)
            by_cat.setdefault(cat, []).append((name, help_text))
        for cat, cmds in sorted(by_cat.items()):
            list_view.append(
                ListItem(Label(f"── {cat} ──"), classes="plugin-category")
            )
            for name, help_text in cmds[:20]:
                desc = help_text[:50] + "..." if len(help_text) > 50 else help_text
                list_view.append(
                    ListItem(Label(f"  {name:28s} {desc}"), classes="plugin-item")
                )
            if len(cmds) > 20:
                list_view.append(
                    ListItem(Label(f"  ... +{len(cmds)-20} more"), classes="plugin-item")
                )

    @staticmethod
    def _guess_category(name: str, help_text: str) -> str:
        h = help_text.lower()
        if any(w in h for w in ["scan", "nmap", "recon", "enum"]):
            return "01. Recon"
        if any(w in h for w in ["exploit", "vuln", "cve"]):
            return "02. Exploit"
        if any(w in h for w in ["cred", "pass", "hash", "crack"]):
            return "03. Credentials"
        if any(w in h for w in ["shell", "payload", "reverse", "stager"]):
            return "04. Payloads"
        if any(w in h for w in ["persist", "backdoor", "tunnel"]):
            return "05. Persistence"
        if any(w in h for w in ["report", "loot", "note"]):
            return "06. Reporting"
        return "07. Other"


class OutputPanel(VerticalScroll):
    """Center: accumulative scrollable output log.

    Command output arrives with raw ANSI escape codes from the real shell.
    It is converted via Text.from_ansi (never parsed as Rich markup, which
    would break on sequences like '[+]').
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._cmd_count = 0

    def compose(self) -> ComposeResult:
        yield RichLog(id="output-log", highlight=False, markup=True, wrap=True)

    def _log(self) -> RichLog:
        return self.query_one("#output-log", RichLog)

    def write_renderable(self, renderable: Any) -> None:
        """Write a Rich renderable (no markup parsing applied)."""
        self._log().write(renderable)
        self.scroll_end(animate=False)

    def write_markup(self, text: str) -> None:
        """Write a trusted internal string with Rich markup."""
        self._log().write(text)
        self.scroll_end(animate=False)

    def append_command(self, cmd: str) -> None:
        self._cmd_count += 1
        ts = datetime.now().strftime("%H:%M:%S")
        self.write_markup(f"[dim]{ts}[/dim] [bold cyan]> {cmd}[/bold cyan]")

    def append_result(self, text: str, success: bool = True) -> None:
        """Write real shell output, converting ANSI — never markup-parsed."""
        if not text or not text.strip():
            self.write_markup("[dim](no output)[/dim]")
            self.write_markup("")
            return
        self._log().write(Text.from_ansi(text.rstrip("\n")))
        self._log().write("")
        self.scroll_end(animate=False)

    def append_error(self, text: str) -> None:
        """Write a TUI-side error message (plain, no markup from unsafe text)."""
        self.write_renderable(Text(f"ERROR: {text}", style="bold red"))

    def append_system(self, text: str) -> None:
        """Write a TUI-side status message."""
        self.write_renderable(Text(text, style="dim italic"))


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------

class LazyOwnTUI(App):
    """Textual frontend for the real LazyOwn cmd2 shell."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #main {
        height: 1fr;
    }

    #sidebar-left {
        width: 32;
        border-right: solid $border;
        background: $surface;
    }

    #output-area {
        width: 1fr;
    }

    #output-log {
        height: 100%;
    }

    #sidebar-right {
        width: 30;
        border-left: solid $border;
        background: $surface;
    }

    #cmd-area {
        height: 3;
        border-top: solid $accent;
        padding: 0 1;
    }

    #cmd-input {
        width: 100%;
    }

    DashboardPanel { height: 100%; }
    PluginBrowser { height: 100%; }
    OutputPanel { height: 100%; }

    #dash-title, #plugin-title {
        text-style: bold;
        color: $accent;
        text-align: center;
    }

    #dash-rhost-label, #dash-lhost-label, #dash-domain-label,
    #dash-phase-label, #dash-aliases-label, #dash-session-label {
        text-style: bold;
        color: $text-muted;
        margin-top: 1;
    }

    #dash-rhost, #dash-lhost, #dash-domain {
        color: $success;
        text-align: center;
    }

    #dash-phase {
        color: $warning;
        text-style: bold;
        text-align: center;
    }

    #dash-aliases-count, #dash-cmd-count, #dash-time {
        color: $text;
        text-align: center;
    }

    #plugin-list { height: 1fr; }

    .plugin-category { text-style: bold; color: $accent; }
    .plugin-item { color: $text; }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+l", "clear_output", "Clear Output"),
        Binding("ctrl+h", "toggle_sidebar", "Toggle Sidebar"),
        Binding("f5", "refresh_dashboard", "Refresh"),
        Binding("tab", "tab_complete", "Tab Complete", show=False, priority=True),
    ]

    TITLE = "LazyOwn TUI Shell"
    SUB_TITLE = "cmd2 backend + Textual frontend"

    _EXIT_WORDS = frozenset({"exit", "quit", "q", "logout", "salir", "EOF"})

    cmd_history_index: reactive[int] = reactive(-1)

    def __init__(self, base_dir: str = ".", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.base_dir = str(Path(base_dir).resolve())
        self.backend = ShellBackend(self.base_dir)
        self._cmd_history: list[str] = []
        self._cmd_queue: list[str] = []
        self._cmd_running = False
        self._dash_timer: Timer | None = None
        self._cmd_count = 0
        self.backend.import_shell_class()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            yield DashboardPanel(self.base_dir, id="sidebar-left")
            yield OutputPanel(id="output-area")
            yield PluginBrowser(id="sidebar-right")
        with Horizontal(id="cmd-area"):
            yield Input(
                placeholder="Type a LazyOwn command... (Tab=complete, Up/Down=history)",
                id="cmd-input",
            )
        yield Footer()

    def on_mount(self) -> None:
        """Start the real cmd2 shell backend."""
        self.title = "LazyOwn TUI Shell"
        self.sub_title = f"base: {self.base_dir}"

        inp = self.query_one("#cmd-input", Input)
        inp.focus()

        output = self.query_one("#output-area", OutputPanel)
        output.append_system("Starting cmd2 backend...")

        def _init_backend():
            try:
                self.backend.start()
                self.call_from_thread(self._on_backend_ready)
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                try:
                    self.call_from_thread(
                        lambda: output.append_error(f"Backend init failed: {e}\n{tb}")
                    )
                except Exception:
                    pass

        threading.Thread(target=_init_backend, daemon=True).start()

    def _on_backend_ready(self) -> None:
        """Called on main thread after backend is initialized."""
        output = self.query_one("#output-area", OutputPanel)
        commands = self.backend.get_commands()
        aliases = self.backend.get_aliases()

        output.append_system(
            f"cmd2 backend ready — {len(commands)} commands, "
            f"{len(aliases)} aliases loaded"
        )

        plugin_browser = self.query_one("#sidebar-right", PluginBrowser)
        plugin_browser.update_commands(commands)

        dash = self.query_one("#sidebar-left", DashboardPanel)
        dash.refresh_data(self.backend, self._cmd_count)

        self._dash_timer = self.set_interval(5.0, self._auto_refresh_dashboard)
        output.append_system("Ready. Type 'help' for all commands.")

        inp = self.query_one("#cmd-input", Input)
        inp.focus()

    def _auto_refresh_dashboard(self) -> None:
        dash = self.query_one("#sidebar-left", DashboardPanel)
        dash.refresh_data(self.backend, self._cmd_count)

    # -- Command dispatch via cmd2 backend ------------------------------------

    def execute_command(self, cmd_str: str) -> None:
        """Send command to real cmd2 shell, display captured output.

        Commands are queued so only one runs at a time. Words that would
        exit the inner shell (q/quit/exit ...) close the TUI cleanly instead
        of triggering LazyOwn's real do_exit mid-render.
        """
        output = self.query_one("#output-area", OutputPanel)
        output.append_command(cmd_str)

        verb = cmd_str.strip().split(None, 1)[0].lower() if cmd_str.strip() else ""

        if verb in self._EXIT_WORDS:
            self.action_quit()
            return

        if verb == "clear":
            log = output.query_one("#output-log", RichLog)
            log.clear()
            output.append_system("Output cleared.")
            return

        self._cmd_queue.append(cmd_str)
        self._drain_queue()

    def _drain_queue(self) -> None:
        """Start the next queued command if nothing is running."""
        if self._cmd_running or not self._cmd_queue:
            return
        if self.backend._shell is None:
            output = self.query_one("#output-area", OutputPanel)
            output.append_error("Backend not ready — wait for init.")
            self._cmd_queue.clear()
            return
        cmd = self._cmd_queue.pop(0)
        self._cmd_running = True

        output = self.query_one("#output-area", OutputPanel)
        output.append_system(f"[running] {cmd}")

        def _work() -> None:
            try:
                result = self.backend.run(cmd)
            except Exception as backend_err:
                import traceback as _tb
                result = f"[backend crash] {backend_err}\n{_tb.format_exc()}"
            try:
                self.call_from_thread(self._show_result, result)
            except Exception:
                # App shutting down or loop gone — never leave UI stuck busy.
                self._cmd_running = False

        threading.Thread(target=_work, daemon=True).start()

    def _show_result(self, result: str) -> None:
        """Render command output on the main thread, then refocus input."""
        self._cmd_running = False
        output = self.query_one("#output-area", OutputPanel)
        output.append_result(result)
        self._cmd_count += 1
        dash = self.query_one("#sidebar-left", DashboardPanel)
        dash.refresh_data(self.backend, self._cmd_count)
        inp = self.query_one("#cmd-input", Input)
        inp.focus()
        self._drain_queue()

    # -- Actions ---------------------------------------------------------------

    def action_clear_output(self) -> None:
        output = self.query_one("#output-area", OutputPanel)
        log = output.query_one("#output-log", RichLog)
        log.clear()

    def action_tab_complete(self) -> None:
        inp = self.query_one("#cmd-input", Input)
        if inp.has_focus:
            self._tab_complete(inp)

    def action_toggle_sidebar(self) -> None:
        left = self.query_one("#sidebar-left")
        right = self.query_one("#sidebar-right")
        left.display = not left.display
        right.display = not right.display

    def action_refresh_dashboard(self) -> None:
        dash = self.query_one("#sidebar-left", DashboardPanel)
        dash.refresh_data(self.backend, self._cmd_count)
        output = self.query_one("#output-area", OutputPanel)
        output.append_system("Dashboard refreshed.")

    def action_quit(self) -> None:
        """Clean shutdown: drop the queue, stop the shell, exit the app."""
        self._cmd_queue.clear()
        if self._dash_timer is not None:
            self._dash_timer.stop()
        try:
            quiet = io.StringIO()
            old_out = sys.stdout
            sys.stdout = quiet
            try:
                self.backend.stop()
            finally:
                sys.stdout = old_out
        except Exception:
            pass
        self.exit()

    # -- Input handling --------------------------------------------------------

    @on(Input.Submitted, "#cmd-input")
    def on_command_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value.strip()
        if not cmd:
            return
        self._cmd_history.append(cmd)
        self.cmd_history_index = len(self._cmd_history)
        event.input.value = ""
        self.execute_command(cmd)

    def on_key(self, event: Any) -> None:
        inp = self.query_one("#cmd-input", Input)
        if not inp.has_focus:
            return
        if event.key == "up":
            if self._cmd_history and self.cmd_history_index > 0:
                self.cmd_history_index -= 1
                inp.value = self._cmd_history[self.cmd_history_index]
                event.stop()
        elif event.key == "down":
            if self.cmd_history_index < len(self._cmd_history) - 1:
                self.cmd_history_index += 1
                inp.value = self._cmd_history[self.cmd_history_index]
                event.stop()
            else:
                self.cmd_history_index = len(self._cmd_history)
                inp.value = ""
                event.stop()

    def _tab_complete(self, inp: Input) -> None:
        partial = inp.value.strip().split()[0] if inp.value.strip() else ""
        if not partial:
            return
        commands = self.backend.get_commands()
        aliases = self.backend.get_aliases()
        all_names = list(commands.keys()) + list(aliases.keys())
        matches = [n for n in all_names if n.startswith(partial)]
        if len(matches) == 1:
            rest = inp.value.split(None, 1)
            if len(rest) > 1:
                inp.value = f"{matches[0]} {rest[1]}"
            else:
                inp.value = matches[0] + " "
        elif len(matches) > 1:
            output = self.query_one("#output-area", OutputPanel)
            output.append_system(f"Matches: {', '.join(sorted(matches)[:20])}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="LazyOwn TUI Shell")
    parser.add_argument(
        "--base-dir",
        default=".",
        help="LazyOwn repo root (default: cwd)",
    )
    args = parser.parse_args()

    app = LazyOwnTUI(base_dir=args.base_dir)
    app.run()


if __name__ == "__main__":
    main()
