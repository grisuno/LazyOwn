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
import sys
from pathlib import Path
from typing import Any

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Static

try:
    from cli.ops_commands import PHASES as _PHASES
    from cli.ops_commands import write_phase as _write_phase
except ImportError:
    _PHASES = ("recon", "scan", "enum", "exploit", "privesc", "lateral", "exfil", "report")

    def _write_phase(phase: str) -> bool:  # type: ignore[misc]
        return False


REFRESH_INTERVAL: float = 5.0
SESSIONS_DIR: str = "sessions"
PAYLOAD_PATH: str = "payload.json"
WORLD_MODEL_PATH: str = "sessions/world_model.json"
TASKS_PATH: str = "sessions/tasks.json"
TRANSCRIPT_PATH: str = "sessions/LazyOwn_session_report.csv"
RECENT_CMD_WINDOW: int = 10

KILL_CHAIN_PHASES: list[tuple[str, str]] = [
    ("recon", "Recon"),
    ("scan", "Scan"),
    ("enum", "Enum"),
    ("exploit", "Exploit"),
    ("privesc", "PrivEsc"),
    ("lateral", "Lateral"),
    ("exfil", "Exfil"),
    ("report", "Report"),
]


def _read_json(path: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def _count_lines_in_glob(pattern: str) -> int:
    import glob as _glob

    total = 0
    for fpath in _glob.glob(pattern):
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
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

    def render_content(self, payload: dict, world: dict) -> Text:
        rhost = payload.get("rhost") or "—"
        lhost = payload.get("lhost") or "—"
        domain = payload.get("domain") or "—"
        os_id = payload.get("os_id", 0)
        os_label = "Linux" if str(os_id) == "1" else ("Windows" if str(os_id) == "2" else "?")
        phase = (world.get("phase") or world.get("current_phase") or "unknown").upper()

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
    """Left panel: kill chain phase progress."""

    DEFAULT_CSS = """
    KillChainPanel {
        height: auto;
        border: round $primary;
        padding: 1 2;
        margin: 0 1 1 0;
    }
    """

    def update_data(self, world: dict) -> None:
        completed: list[str] = world.get("completed_phases") or world.get("phases_done") or []
        current: str = (world.get("phase") or world.get("current_phase") or "").lower()
        lines = Text()
        lines.append(" Kill Chain\n", style="bold cyan underline")
        for key, label in KILL_CHAIN_PHASES:
            if key in completed:
                icon, style = "✔", "bold green"
            elif key == current:
                icon, style = "▶", "bold yellow"
            else:
                icon, style = "○", "dim white"
            lines.append(f"  {icon} {label}\n", style=style)
        self.update(lines)


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

        self.update(t)


class HintBar(Static):
    """Bottom bar: graph-driven next-step suggestions."""

    DEFAULT_CSS = """
    HintBar {
        height: 2;
        padding: 0 2;
        background: $panel-darken-1;
        border-top: solid $primary;
    }
    """

    def update_data(self, hints: list[str]) -> None:
        t = Text()
        t.append("  ↳ next: ", style="bold dim cyan")
        t.append(
            " · ".join(h[:22] for h in hints) if hints else "(run /graphify . to enable)", style="dim white italic"
        )
        self.update(t)


class LazyOwnDashboard(App):
    """Full-screen operator dashboard for LazyOwn.

    Reads payload.json, sessions/, and the graphify knowledge graph.
    Auto-refreshes every REFRESH_INTERVAL seconds. Press Q to quit.
    """

    TITLE = "LazyOwn RedTeam Dashboard"
    SUB_TITLE = "press Q to return to shell"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh_data", "Refresh"),
        ("p", "next_phase", "Next phase"),
        ("shift+p", "prev_phase", "Prev phase"),
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
        height: 2;
        dock: bottom;
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

    def compose(self) -> ComposeResult:
        yield Header()
        yield TargetPanel(id="top-bar")
        with Horizontal(id="main-area"):
            with Vertical(id="left-col"):
                yield KillChainPanel(id="kill-chain")
                yield ConfigPanel(id="config-panel")
            with Vertical(id="center-col"):
                yield CommandsPanel(id="commands-panel")
            with Vertical(id="right-col"):
                yield OpsPanel(id="ops-panel")
        yield HintBar(id="hint-bar")
        yield Footer()

    def on_mount(self) -> None:
        self._do_refresh()
        self.set_interval(REFRESH_INTERVAL, self._do_refresh)

    def action_refresh_data(self) -> None:
        self._do_refresh()

    def action_next_phase(self) -> None:
        """Advance to the next kill-chain phase and refresh the display."""
        self._cycle_phase(direction=1)

    def action_prev_phase(self) -> None:
        """Step back to the previous kill-chain phase."""
        self._cycle_phase(direction=-1)

    def _cycle_phase(self, direction: int) -> None:
        world = _read_json(WORLD_MODEL_PATH)
        current = (world.get("phase") or world.get("current_phase") or "recon").lower()
        phases = list(_PHASES)
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
        payload = _read_json(self._payload_path)
        world = _read_json(WORLD_MODEL_PATH)
        tasks_raw = _read_json(TASKS_PATH)
        tasks: list[dict] = tasks_raw if isinstance(tasks_raw, list) else tasks_raw.get("tasks", [])
        commands = _read_recent_commands()
        creds = _count_lines_in_glob(f"{self._sessions_dir}/credentials*.txt")
        hashes = _count_lines_in_glob(f"{self._sessions_dir}/hash*.txt")
        beacons = _beacon_count()
        hints = _graph_hints()

        self.query_one("#top-bar", TargetPanel).update_data(payload, world)
        self.query_one("#kill-chain", KillChainPanel).update_data(world)
        self.query_one("#config-panel", ConfigPanel).update_data(payload)
        self.query_one("#commands-panel", CommandsPanel).update_data(commands)
        self.query_one("#ops-panel", OpsPanel).update_data(world, tasks, creds, hashes, beacons)
        self.query_one("#hint-bar", HintBar).update_data(hints)


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
