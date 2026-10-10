"""LazyOwn operator dashboard — a full-screen Textual TUI.

Launch from the LazyOwn shell with ``dashboard`` or directly:

    python3 -m cli.dashboard_tui [--payload PATH] [--sessions PATH]

The dashboard auto-refreshes every REFRESH_INTERVAL seconds. Press Q or
Ctrl-C to close and return to the cmd2 shell.

Layout:
    ┌─ Header (target / domain / phase / OS) ─────────────────────────────┐
    │  Left (Kill Chain + Config)  │  Center (Commands) │ Right (Ops)      │
    ├──────────────────────────────────────────────────────────────────────┤
    │  Hint bar (graph suggestions)                                        │
    └─ Footer ([Q] Quit  [R] Refresh  [?] Help) ──────────────────────────┘
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, Footer, Header, Input, Log, Static

from cli.killchain import PhaseProgress
from cli.reasoning_stream import ReasoningEntry, latest_reasoning
from modules.killchain import KillChain as _KC

try:
    from cli.ops_commands import write_phase as _write_phase
except ImportError:

    def _write_phase(phase: str) -> bool:  # type: ignore[misc]
        return False


_PHASES: tuple[str, ...] = _KC.phases()
KILL_CHAIN_PHASES: tuple[tuple[str, str], ...] = tuple((p[0], p[1]) for p in _KC.phases_for_display())

STATE_DONE: str = "done"
STATE_ACTIVE: str = "active"
STATE_PENDING: str = "pending"


def _get_killchain_for_tui() -> list:
    """Return kill-chain progress as :class:`PhaseProgress`-compatible list.

    Derives state exclusively from ``KillChain.get_progress`` (world model)
    so the dashboard TUI, Flask `/killchain`, and CLI agree on every phase.
    """
    progress = _KC.get_progress()
    result = []
    for ps in progress:
        result.append(
            PhaseProgress(
                key=ps.key,
                label=ps.label,
                state=ps.status,
                activity=0,
                reward=0.0,
            )
        )
    return result


__all__ = ["KILL_CHAIN_PHASES", "LazyOwnDashboard", "launch"]

REFRESH_INTERVAL: float = 5.0
SESSIONS_DIR: str = "sessions"
PAYLOAD_PATH: str = "payload.json"
WORLD_MODEL_PATH: str = "sessions/world_model.json"
TASKS_PATH: str = "sessions/tasks.json"
TRANSCRIPT_PATH: str = "sessions/LazyOwn_session_report.csv"
EVENTS_PATH: str = "sessions/autonomous_events.jsonl"
RECENT_CMD_WINDOW: int = 10
REASONING_WINDOW: int = 12
KILLCHAIN_EVENT_WINDOW: int = 400
REASONING_MAX_HEIGHT: int = 12
HINT_BUTTON_MAX_LABEL: int = 18
HINT_BUTTON_MAX_COUNT: int = 5
KILLCHAIN_HEADER_ROWS: int = 1
DISPATCH_TIMEOUT: int = 900
REPO_ROOT: str = str(Path(__file__).resolve().parent.parent)
TOAST_PANEL_LIMIT: int = 4


class CommandRequested(Message):
    """Posted when the operator submits a command or clicks a hint button."""

    def __init__(self, command: str) -> None:
        super().__init__()
        self.command = command


class PhaseSelected(Message):
    """Posted when the operator clicks a kill-chain phase row."""

    def __init__(self, phase: str) -> None:
        super().__init__()
        self.phase = phase


def dispatch_command(command: str, timeout: int = DISPATCH_TIMEOUT) -> tuple[bool, str]:
    """Run one LazyOwn command headlessly and capture its output.

    Uses the supported ``lazyown.py --headless --command`` entry point with
    list-form argv so the operator input never reaches a shell. A crashing or
    hanging command cannot take the dashboard down with it.

    Args:
        command: Command line typed by the operator.
        timeout: Seconds before the child process is killed.

    Returns:
        Tuple of (success, output). Output is stdout, or stderr when the
        process failed without producing stdout.
    """
    argv = [sys.executable, "lazyown.py", "--headless", "--json-output", "--command", command]
    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    try:
        proc = subprocess.run(
            argv,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s"
    except OSError as exc:
        return False, f"dispatch failed: {exc}"
    output = (proc.stdout or "").strip()
    if proc.returncode != 0 and not output:
        output = (proc.stderr or "").strip() or f"exit code {proc.returncode}"
    return proc.returncode == 0, output


def _read_json(path: str) -> dict[str, Any]:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def _engagement_to_cli_phase(engagement_phase: str) -> str:
    """Map a WorldModel EngagementPhase value to a CLI phase name.

    Delegates to the single source of truth in :class:`modules.killchain.KillChain`.
    """
    from modules.killchain import KillChain

    return KillChain.engagement_phase_to_cli(engagement_phase)


def _count_lines_in_glob(pattern: str) -> int:
    import glob as _glob

    total = 0
    for fpath in _glob.glob(pattern):
        try:
            with open(fpath, encoding="utf-8", errors="ignore") as fh:
                total += sum(1 for line in fh if line.strip())
        except OSError:
            pass
    return total


def _read_recent_commands(limit: int = RECENT_CMD_WINDOW) -> list[dict[str, str]]:
    path = Path(TRANSCRIPT_PATH)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
    except (OSError, csv.Error):
        return []
    columns = ("tool", "command", "name")
    if not rows:
        return []
    cmd_col = next((c for c in columns if c in rows[0]), None)
    if cmd_col is None:
        return []
    recent = rows[-limit:]
    out: list[dict[str, str]] = []
    for row in recent:
        cmd = (row.get(cmd_col) or "").strip()
        status = (row.get("status") or row.get("result") or "").strip()
        ts = (row.get("timestamp") or row.get("date") or "").strip()
        if cmd:
            out.append({"cmd": cmd, "status": status[:20], "ts": ts[:16]})
    return out


def _graph_hints(limit: int = 5) -> list[str]:
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from cli.graph_advisor import GraphAdvisor

        advisor = GraphAdvisor.from_path()
        if not advisor.is_available():
            return []
        suggs = advisor.suggest_next(limit=limit)
        return [s.get("label") or s.get("id") or "" for s in suggs if s.get("label") or s.get("id")]
    except Exception:
        return []


def _fallback_hints(last_command: str = "", limit: int = HINT_BUTTON_MAX_COUNT) -> list[str]:
    """Suggest next steps from the static kill-chain tables.

    The graph advisor needs a built ``graphify-out/`` graph. Without one the
    hint bar used to render an empty placeholder, which made the whole
    feature invisible. The adjacency and phase-priority tables in
    :mod:`cli.reactive_hints` are always present, so they act as the
    baseline and the graph only refines it.

    Args:
        last_command: Most recent command line, used for adjacency lookup.
        limit: Maximum suggestions to return.

    Returns:
        Suggested command verbs, possibly empty when every candidate has
        already run this session.
    """
    try:
        from cli.reactive_hints import command_hints

        return command_hints(last_command, limit=limit)
    except Exception:
        return []


def _resolve_hints(recent: list[dict], limit: int = HINT_BUTTON_MAX_COUNT) -> list[str]:
    """Return actionable hints, preferring the graph over the static tables.

    Args:
        recent: Recent command entries from the transcript.
        limit: Maximum suggestions to return.

    Returns:
        Non-empty hint list when any source can produce one.
    """
    last = str(recent[0].get("cmd", "")) if recent else ""
    hints = _graph_hints(limit=limit)
    if hints:
        return hints
    return _fallback_hints(last, limit=limit)


def _beacon_count() -> int:
    beacons_file = Path(SESSIONS_DIR) / "beacons.json"
    if not beacons_file.exists():
        return 0
    try:
        data = json.loads(beacons_file.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict):
            return len(data)
    except (OSError, json.JSONDecodeError):
        pass
    return 0


def _read_credential_lines(pattern: str) -> list[str]:
    """Read actual credential lines from credential files."""
    import glob as _glob

    lines: list[str] = []
    for fpath in sorted(_glob.glob(pattern)):
        try:
            with open(fpath, encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#"):
                        lines.append(stripped[:50])
        except OSError:
            pass
    return lines


def _get_recommendations() -> list[dict]:
    """Get next-step recommendations from the recommendation engine."""
    try:
        from cli.recommendation_signals import recommend_with_evidence

        payload = _read_json(PAYLOAD_PATH)
        world = _read_json(WORLD_MODEL_PATH)
        recs = recommend_with_evidence(
            payload,
            sessions_dir=SESSIONS_DIR,
            phase=str(world.get("phase", "recon")),
            limit=5,
        )
        return [
            {
                "command": rec.command_preview or rec.action,
                "confidence": int(rec.score * 100),
                "reason": "; ".join(rec.reasons) if rec.reasons else rec.action,
            }
            for rec in recs
        ]
    except Exception:
        return []


class TargetPanel(Static):
    """Top info bar: target, domain, phase, OS."""

    DEFAULT_CSS = """
    TargetPanel {
        height: 3;
        padding: 0 2;
        background: $panel;
        border-bottom: solid $primary;
        color: $text;
    }
    """

    def get_selection(self, selection: Any) -> list[str] | None:
        """Override to prevent IndexError when selection offsets exceed text length.

        Rich ``Text`` objects may produce ``Content`` whose plain-text length is
        shorter than the character offsets derived by the framework, leading to
        a crash in ``Selection.extract``. This override safely returns ``None``
        when the selection is invalid.
        """
        try:
            return super().get_selection(selection)
        except IndexError:
            return None

    def render_content(self, payload: dict, world: dict) -> Text:
        rhost = payload.get("rhost") or "—"
        lhost = payload.get("lhost") or "—"
        domain = payload.get("domain") or "—"
        os_id = payload.get("os_id", 0)
        os_label = "Linux" if str(os_id) == "1" else ("Windows" if str(os_id) == "2" else "?")
        try:
            from modules.killchain import KillChain

            phase = KillChain.current_phase().upper()
        except Exception:
            phase = "RECON"

        t = Text()
        t.append(" TARGET ", style="bold white on dark_red")
        t.append(f" {rhost} ", style="bold cyan")
        t.append("  ATTACKER ", style="bold white on dark_green")
        t.append(f" {lhost} ", style="bold green")
        t.append("  DOMAIN ", style="bold white on dark_blue")
        t.append(f" {domain} ", style="bold blue")
        t.append("  PHASE ", style="bold white on dark_orange3")
        t.append(f" {phase} ", style="bold yellow")
        t.append("  OS ", style="dim white")
        t.append(f" {os_label} ", style="bold magenta")
        return t

    def update_data(self, payload: dict, world: dict) -> None:
        self.update(self.render_content(payload, world))


class KillChainPanel(Static):
    """Left panel: kill chain phase progress — single source of truth via KillChain."""

    DEFAULT_CSS = """
    KillChainPanel {
        height: auto;
        border: round $primary;
        padding: 1 2;
        margin: 0 1 1 0;
    }
    KillChainPanel:hover {
        border: round $accent;
    }
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._phase_keys: list[str] = []

    def update_data(self, progress: list[PhaseProgress]) -> None:
        """Render kill-chain progress. ``progress`` comes from KillChain.get_progress()."""
        lines = Text()
        lines.append(" Kill Chain\n", style="bold cyan underline")
        self._phase_keys = []
        for phase in progress:
            if phase.state == STATE_DONE:
                icon, style = "✔", "bold green"
            elif phase.state == STATE_ACTIVE:
                icon, style = "▶", "bold yellow"
            else:
                icon, style = "○", "dim white"
            lines.append(f"  {icon} {phase.label}", style=style)
            if phase.activity:
                lines.append(f"  ×{phase.activity}", style="dim cyan")
                if phase.reward:
                    lines.append(f" r={phase.reward:.2f}", style="dim green")
            lines.append("\n")
            self._phase_keys.append(phase.key)
        self.update(lines)

    def on_click(self, event: Any) -> None:
        """Select the phase whose row was clicked.

        Args:
            event: Textual click event carrying a widget-relative offset.
        """
        index = int(getattr(event, "offset", None).y if getattr(event, "offset", None) else 0)
        index -= KILLCHAIN_HEADER_ROWS
        if 0 <= index < len(self._phase_keys):
            self.post_message(PhaseSelected(self._phase_keys[index]))


class ConfigPanel(Static):
    """Left panel: key payload.json values."""

    DEFAULT_CSS = """
    ConfigPanel {
        height: auto;
        border: round $accent;
        padding: 1 2;
        margin: 0 1 0 0;
    }
    """

    def update_data(self, payload: dict) -> None:
        t = Text()
        t.append(" Config\n", style="bold cyan underline")
        keys = [
            ("rhost", "Target"),
            ("lhost", "Attacker"),
            ("rport", "Port"),
            ("domain", "Domain"),
            ("wordlist", "Wordlist"),
            ("c2_port", "C2 Port"),
        ]
        for key, label in keys:
            val = str(payload.get(key) or "—")
            t.append(f"  {label}: ", style="dim white")
            t.append(val[:28] + "\n", style="bold white")
        self.update(t)


class CommandsPanel(Static):
    """Center panel: recent executed commands."""

    DEFAULT_CSS = """
    CommandsPanel {
        height: 1fr;
        border: round $primary;
        padding: 1 2;
        margin: 0 1 1 0;
    }
    """

    def update_data(self, commands: list[dict]) -> None:
        t = Text()
        t.append(" Recent Commands\n", style="bold cyan underline")
        if not commands:
            t.append("  (no commands yet)\n", style="dim italic")
        for entry in commands:
            cmd = entry.get("cmd") or ""
            status = entry.get("status") or ""
            ts = entry.get("ts") or ""
            if status:
                status_style = "bold green" if "ok" in status.lower() else "dim yellow"
            else:
                status_style = "dim white"
            t.append("  ● ", style="dim cyan")
            t.append(f"{cmd[:28]:<28}", style="bold white")
            if ts:
                t.append(f"  {ts[:16]}", style="dim white")
            if status:
                t.append(f"  {status[:18]}", style=status_style)
            t.append("\n")
        self.update(t)


class ReasoningPanel(Static):
    """Center panel: live autonomous-daemon reasoning stream."""

    DEFAULT_CSS = """
    ReasoningPanel {
        height: 1fr;
        border: round $warning;
        padding: 1 2;
        margin: 0 1 1 0;
    }
    """

    def update_data(self, entries: list[ReasoningEntry]) -> None:
        """Render the most recent daemon decisions, newest first."""
        t = Text()
        t.append(" Daemon Reasoning\n", style="bold cyan underline")
        if not entries:
            t.append("  (daemon idle — start with autonomous_start)\n", style="dim italic")
            self.update(t)
            return
        for entry in reversed(entries):
            t.append(f"  {entry.icon} ", style=entry.style)
            if entry.ts:
                t.append(f"{entry.ts} ", style="dim white")
            if entry.phase:
                t.append(f"{entry.phase[:8]:<8} ", style="dim cyan")
            if entry.command:
                t.append(f"{entry.command} ", style=entry.style)
            if entry.reward is not None:
                reward_style = "bold green" if entry.reward > 0 else "dim white"
                t.append(f"r={entry.reward:.2f} ", style=reward_style)
            if entry.summary:
                t.append(f"{entry.summary}", style="dim white")
            t.append("\n")
        self.update(t)


class OpsPanel(Static):
    """Right panel: objectives, credentials, beacons."""

    DEFAULT_CSS = """
    OpsPanel {
        height: 1fr;
        border: round $success;
        padding: 1 2;
        margin: 0 0 1 0;
    }
    """

    def update_data(
        self,
        world: dict,
        tasks: list,
        creds: int,
        hashes: int,
        beacons: int,
        cred_lines: list[str] | None = None,
    ) -> None:
        t = Text()
        t.append(" Ops\n", style="bold cyan underline")

        objective = (
            world.get("current_objective")
            or world.get("objective")
            or (tasks[0].get("name") or tasks[0].get("title") if tasks else None)
            or "—"
        )
        t.append("  Objective:\n", style="dim white")
        t.append(f"  {str(objective)[:36]}\n\n", style="bold yellow")

        t.append("  Tasks: ", style="dim white")
        t.append(f"{len(tasks)}\n", style="bold white")

        t.append("  Credentials: ", style="dim white")
        t.append(f"{creds}\n", style="bold green" if creds else "dim white")

        t.append("  Hashes: ", style="dim white")
        t.append(f"{hashes}\n", style="bold red" if hashes else "dim white")

        t.append("  Beacons: ", style="dim white")
        t.append(f"{beacons}\n", style="bold magenta" if beacons else "dim white")

        if cred_lines:
            t.append("\n  Found credentials:\n", style="bold green")
            for line in cred_lines[:5]:
                t.append(f"    {line[:36]}\n", style="dim green")
            if len(cred_lines) > 5:
                t.append(f"    ... and {len(cred_lines) - 5} more\n", style="dim")

        self.update(t)


class HintBar(Horizontal):
    """Bottom bar: graph-driven next steps rendered as one-click buttons."""

    DEFAULT_CSS = """
    HintBar {
        height: auto;
        padding: 0 1;
        background: $panel-darken-1;
        border-top: solid $primary;
    }
    HintBar Button {
        margin: 0 1 0 0;
        min-width: 10;
        border: none;
        height: 1;
    }
    HintBar .hint-label {
        width: 8;
        content-align: left middle;
        color: $text-muted;
    }
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._hints: list[str] = []
        self._label: Static | None = None

    def compose(self) -> ComposeResult:
        self._label = Static("next:", classes="hint-label")
        yield self._label

    def update_data(self, hints: list[str]) -> None:
        """Replace the hint buttons with one button per suggestion.

        Only buttons are recreated. The label is mounted once in
        :meth:`compose` and reused, so a five-second refresh with no hints
        cannot accumulate placeholder widgets. Buttons carry no id because
        Textual removal is deferred: reusing ``hint-<name>`` ids would
        collide with the previous, not-yet-removed button.

        Args:
            hints: Suggested command names, best first.
        """
        self._hints = list(hints)
        for child in list(self.children):
            if isinstance(child, Button):
                child.remove()
        if self._label is None:
            return
        if not self._hints:
            self._label.update("(run graph to enable)")
            return
        self._label.update("next:")
        for hint in self._hints[:HINT_BUTTON_MAX_COUNT]:
            self.mount(Button(hint[:HINT_BUTTON_MAX_LABEL]))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Run the clicked suggestion as if it had been typed.

        Args:
            event: Button press event.
        """
        self.post_message(CommandRequested(str(event.button.label)))


class ToastPanel(Static):
    """Notification panel rendering the cmd2 toast stream unchanged.

    Uses :func:`cli.toast_bus.read_recent_toasts` and
    :func:`cli.toast_bus.build_toast_renderable`, so the dashboard shows the
    same themed ``notifications`` panel the shell prints. It tails the event
    file instead of consuming it, so raising a toast in one surface never
    hides it from the other.
    """

    DEFAULT_CSS = """
    ToastPanel {
        height: auto;
        max-height: 10;
        margin: 0 0 1 0;
    }
    """

    def update_data(self, payload: dict, sessions_dir: str, width: int = 0) -> None:
        """Render the latest notifications for the active theme.

        Args:
            payload: Loaded payload used to resolve the theme.
            sessions_dir: Sessions root holding the event files.
            width: Panel width. ``0`` lets the formatter auto-clamp.
        """
        from cli.toast_bus import build_toast_renderable, read_recent_toasts

        try:
            events = read_recent_toasts(sessions_dir=sessions_dir, limit=TOAST_PANEL_LIMIT)
        except Exception:
            events = []
        renderable = build_toast_renderable(events, payload=payload, width=width)
        if renderable is None:
            self.display = False
            return
        self.display = True
        self.update(renderable)


class OutputPanel(Log):
    """Center panel: scrollable output of commands run from the dashboard."""

    DEFAULT_CSS = """
    OutputPanel {
        height: 1fr;
        border: round $primary;
        padding: 0 1;
        margin: 0 1 1 0;
    }
    """


class NextStepsPanel(Static):
    """Right panel: AI-ranked next-step recommendations."""

    DEFAULT_CSS = """
    NextStepsPanel {
        height: auto;
        border: round $warning;
        padding: 1 2;
        margin: 0 0 1 0;
    }
    """

    def update_data(self, recommendations: list[dict]) -> None:
        t = Text()
        t.append(" Next Steps\n", style="bold yellow underline")
        if not recommendations:
            t.append("  (no recommendations available)\n", style="dim italic")
            t.append("  Run 'recommend_next' to generate\n", style="dim")
        else:
            for rec in recommendations[:5]:
                cmd = rec.get("command", "?")
                confidence = rec.get("confidence", 0)
                reason = rec.get("reason", "")
                conf_style = "bold green" if confidence >= 70 else ("yellow" if confidence >= 40 else "dim")
                t.append(f"  {cmd:<20}", style="bold cyan")
                t.append(f"{confidence:>3}%", style=conf_style)
                if reason:
                    t.append(f"  {reason[:28]}", style="dim white")
                t.append("\n")
        self.update(t)


class LazyOwnDashboard(App):
    """Full-screen operator dashboard for LazyOwn.

    Reads payload.json, sessions/, and the graphify knowledge graph.
    Auto-refreshes every REFRESH_INTERVAL seconds. Press Q to quit.
    """

    TITLE = "LazyOwn RedTeam Dashboard"
    SUB_TITLE = "type a command below · click a phase or a hint · F compact · S shot · E export · Q quit"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh_data", "Refresh"),
        ("p", "next_phase", "Next phase"),
        ("shift+p", "prev_phase", "Prev phase"),
        ("f", "toggle_compact", "Compact"),
        ("s", "screenshot", "Screenshot"),
        ("e", "export_snapshot", "Export"),
        ("?", "help", "Help"),
    ]
    DEFAULT_CSS = """
    Screen {
        layout: vertical;
    }
    #top-bar {
        height: 3;
        dock: top;
    }
    #main-area {
        layout: horizontal;
        height: 1fr;
    }
    #left-col {
        layout: vertical;
        width: 28;
        min-width: 22;
    }
    #center-col {
        layout: vertical;
        width: 1fr;
    }
    #right-col {
        layout: vertical;
        width: 30;
        min-width: 24;
    }
    #hint-bar {
        height: auto;
    }
    #cmd-input {
        height: 3;
        margin: 0 1;
    }
    #output-panel {
        height: 1fr;
    }
    #main-area.compact {
        layout: vertical;
    }
    #right-col.compact {
        display: none;
    }
    #reasoning-panel.compact {
        display: none;
    }
    """

    _payload_path: str = PAYLOAD_PATH
    _sessions_dir: str = SESSIONS_DIR

    def __init__(
        self,
        payload_path: str = PAYLOAD_PATH,
        sessions_dir: str = SESSIONS_DIR,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._payload_path = payload_path
        self._sessions_dir = sessions_dir
        self._compact_override: bool = False
        self._phase_filter: str = ""

    def _apply_layout(self, mode: str, hidden_fn: Any = None) -> None:
        """Toggle compact CSS classes from a layout mode name.

        Args:
            mode: One of wide, narrow or compact.
            hidden_fn: Callable mapping mode to hidden widget ids.
        """
        from cli.dashboard_layout import hidden_panels as _hidden

        hidden = set((hidden_fn or _hidden)(mode))
        try:
            self.query_one("#main-area").set_class(mode == "compact", "compact")
            self.query_one("#right-col").set_class("right-col" in hidden, "compact")
            self.query_one("#reasoning-panel").set_class("reasoning-panel" in hidden, "compact")
        except Exception:
            pass

    def compose(self) -> ComposeResult:
        yield Header()
        yield TargetPanel(id="top-bar")
        with Horizontal(id="main-area"):
            with Vertical(id="left-col"):
                yield KillChainPanel(id="kill-chain")
                yield ConfigPanel(id="config-panel")
            with Vertical(id="center-col"):
                yield CommandsPanel(id="commands-panel")
                yield OutputPanel(id="output-panel")
                yield ReasoningPanel(id="reasoning-panel")
            with Vertical(id="right-col"):
                yield NextStepsPanel(id="next-steps")
                yield ToastPanel(id="toast-panel")
                yield OpsPanel(id="ops-panel")
        yield HintBar(id="hint-bar")
        yield Input(placeholder="type a LazyOwn command and press enter", id="cmd-input")
        yield Footer()

    def on_mount(self) -> None:
        self._do_refresh()
        self.set_interval(REFRESH_INTERVAL, self._do_refresh)
        self.query_one("#cmd-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Run the typed command and clear the input.

        Args:
            event: Input submission event.
        """
        command = str(event.value or "").strip()
        event.input.value = ""
        if command:
            self.notify(f"running: {command}", title="command", timeout=2)
            self.post_message(CommandRequested(command))

    def on_command_requested(self, event: CommandRequested) -> None:
        """Dispatch a command in a worker so the UI never blocks.

        Args:
            event: Request posted by the input or a hint button.
        """
        self._execute(event.command)

    @work(thread=True, exclusive=True)
    def _execute(self, command: str) -> None:
        """Run one command off the event loop and hand the result back.

        Widgets may only be touched from the event loop, so the worker
        performs the subprocess call and then marshals the result through
        ``call_from_thread``.

        Args:
            command: Command line to run.
        """
        success, output = dispatch_command(command)
        self.call_from_thread(self._apply_command_result, command, success, output)

    def _apply_command_result(self, command: str, success: bool, output: str) -> None:
        """Log a finished command and refresh the panels on the event loop.

        Args:
            command: Command that was run.
            success: Whether the dispatcher reported success.
            output: Captured stdout, or stderr on failure.
        """
        panel = self.query_one("#output-panel", Log)
        panel.write_line(f"$ {command}")
        for chunk in output.splitlines():
            panel.write_line(chunk)
        if success:
            self.notify(f"done: {command}", title="command", timeout=2)
        else:
            self.notify(f"failed: {command}", title="command", timeout=4)
        self._do_refresh()

    def on_phase_selected(self, event: PhaseSelected) -> None:
        """Filter the center panel to a phase chosen by clicking the kill chain.

        Args:
            event: Phase selection posted by the kill-chain panel.
        """
        self._phase_filter = event.phase if self._phase_filter != event.phase else ""
        label = self._phase_filter or "all phases"
        self.notify(f"filter: {label}", title="kill chain", timeout=2)
        self._do_refresh()

    def action_refresh_data(self) -> None:
        self._do_refresh()

    def action_toggle_compact(self) -> None:
        """Toggle the compact single-column layout for narrow terminals."""
        from cli.dashboard_layout import hidden_panels, layout_mode

        try:
            width = self.size.width
        except Exception:
            width = 0
        forced = not self._compact_override
        self._compact_override = forced
        self._apply_layout(layout_mode(width) if not forced else "compact", hidden_panels)

    def _raise_toast(self, message: str, severity: str = "info", event_type: str = "dashboard") -> None:
        """Publish a dashboard event into the shared toast stream.

        The cmd2 shell renders these on its next command, so both surfaces
        stay in sync instead of the dashboard owning a private channel.

        Args:
            message: Human-readable one-liner.
            severity: Theme severity key.
            event_type: Short label rendered before the message.
        """
        try:
            from cli.toast_bus import emit_toast

            emit_toast(message, severity=severity, event_type=event_type, sessions_dir=self._sessions_dir)
        except Exception:
            pass

    def action_screenshot(self) -> None:
        """Save an SVG screenshot next to the sessions directory."""
        try:
            path = str(Path(self._sessions_dir) / "dashboard.svg")
            self.save_screenshot(path)
            self.notify(f"Saved {path}", title="Screenshot", timeout=2)
            self._raise_toast(f"screenshot saved: {path}", severity="success", event_type="export")
        except Exception as exc:
            self.notify(f"Screenshot failed: {exc}", title="Screenshot", timeout=3)
            self._raise_toast(f"screenshot failed: {exc}", severity="error", event_type="export")

    def action_export_snapshot(self) -> None:
        """Export the current dashboard data as JSON for automation."""
        import datetime as _dt

        try:
            payload = _read_json(self._payload_path)
            data = {
                "exported_at": _dt.datetime.now(_dt.UTC).isoformat(),
                "payload": {k: payload.get(k) for k in ("rhost", "lhost", "domain")},
                "recent_commands": _read_recent_commands(),
                "hints": _graph_hints(),
            }
            out = Path(self._sessions_dir) / "dashboard_snapshot.json"
            out.write_text(json.dumps(data, indent=2), encoding="utf-8")
            self.notify(f"Saved {out}", title="Export", timeout=2)
            self._raise_toast(f"dashboard snapshot exported: {out}", severity="success", event_type="export")
        except Exception as exc:
            self.notify(f"Export failed: {exc}", title="Export", timeout=3)
            self._raise_toast(f"export failed: {exc}", severity="error", event_type="export")

    def action_next_phase(self) -> None:
        """Advance to the next kill-chain phase and refresh the display."""
        self._cycle_phase(direction=1)

    def action_prev_phase(self) -> None:
        """Step back to the previous kill-chain phase."""
        self._cycle_phase(direction=-1)

    def _cycle_phase(self, direction: int) -> None:
        from modules.killchain import KillChain

        phases = list(KillChain.phases())
        current = KillChain.current_phase()
        try:
            idx = phases.index(current)
        except ValueError:
            idx = 0
        new_idx = max(0, min(len(phases) - 1, idx + direction))
        new_phase = phases[new_idx]
        if new_phase != current:
            _write_phase(new_phase)
            self._do_refresh()
            self.notify(f"Phase: {new_phase.upper()}", title="Kill chain", timeout=2)

    def _do_refresh(self) -> None:
        if not self._compact_override:
            try:
                from cli.dashboard_layout import layout_mode as _layout_mode

                self._apply_layout(_layout_mode(self.size.width))
            except Exception:
                pass
        payload = _read_json(self._payload_path)
        world = _read_json(WORLD_MODEL_PATH)
        tasks_raw = _read_json(TASKS_PATH)
        tasks: list[dict] = tasks_raw if isinstance(tasks_raw, list) else tasks_raw.get("tasks", [])
        commands = _read_recent_commands()
        creds = _count_lines_in_glob(f"{self._sessions_dir}/credentials*.txt")
        hashes = _count_lines_in_glob(f"{self._sessions_dir}/hash*.txt")
        beacons = _beacon_count()
        hints = _resolve_hints(commands)
        reasoning = latest_reasoning(EVENTS_PATH, REASONING_WINDOW)
        killchain = _get_killchain_for_tui()

        cred_lines = _read_credential_lines(f"{self._sessions_dir}/credentials*.txt")
        recommendations = _get_recommendations()

        self.query_one("#top-bar", TargetPanel).update_data(payload, world)
        self.query_one("#kill-chain", KillChainPanel).update_data(killchain)
        self.query_one("#config-panel", ConfigPanel).update_data(payload)
        self.query_one("#commands-panel", CommandsPanel).update_data(self._filter_commands(commands))
        self.query_one("#reasoning-panel", ReasoningPanel).update_data(reasoning)
        self.query_one("#next-steps", NextStepsPanel).update_data(recommendations)
        try:
            width = self.query_one("#toast-panel").size.width or 0
        except Exception:
            width = 0
        self.query_one("#toast-panel", ToastPanel).update_data(payload, self._sessions_dir, width)
        self.query_one("#ops-panel", OpsPanel).update_data(world, tasks, creds, hashes, beacons, cred_lines)
        self.query_one("#hint-bar", HintBar).update_data(hints)

    def _filter_commands(self, commands: list[dict]) -> list[dict]:
        """Keep only commands belonging to the phase selected by click.

        Args:
            commands: Recent command entries from the transcript.

        Returns:
            Entries matching the active phase, or all of them when no
            phase filter is active.
        """
        if not self._phase_filter:
            return commands
        needle = self._phase_filter.lower()
        return [c for c in commands if needle in str(c.get("cmd", "")).lower()]


def launch(payload_path: str = PAYLOAD_PATH, sessions_dir: str = SESSIONS_DIR) -> None:
    """Launch the dashboard and block until the user quits.

    Args:
        payload_path: Path to payload.json.
        sessions_dir: Path to the sessions directory.
    """
    app = LazyOwnDashboard(payload_path=payload_path, sessions_dir=sessions_dir)
    app.run()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LazyOwn operator dashboard")
    parser.add_argument("--payload", default=PAYLOAD_PATH, help="Path to payload.json")
    parser.add_argument("--sessions", default=SESSIONS_DIR, help="Path to sessions dir")
    args = parser.parse_args()
    launch(payload_path=args.payload, sessions_dir=args.sessions)
