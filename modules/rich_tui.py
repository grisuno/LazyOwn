"""Rich-based live TUI dashboard for LazyOwn campaign monitoring.

Provides an htop-style real-time dashboard that consumes data from
modules.dashboard_engine.DashboardEngine and renders a terminal UI
using the Python rich library.
"""

from __future__ import annotations

import select
import sys
import termios
import threading
import time
import tty
from typing import Any

from rich.align import Align
from rich.box import HEAVY, MINIMAL, ROUNDED
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

try:
    from modules.dashboard_engine import DashboardEngine
except ImportError:
    from dashboard_engine import DashboardEngine

_SEVERITY_STYLES: dict[str, str] = {
    "CRITICAL": "bold white on red",
    "HIGH": "bold red",
    "MEDIUM": "bold yellow",
    "LOW": "bold blue",
    "NONE": "dim white",
}

_PHASE_STYLES: dict[str, str] = {
    "unscanned": "white",
    "scanned": "blue",
    "enumerated": "cyan",
    "exploited": "yellow",
    "owned": "bold green",
}

_PHASE_ICONS: dict[str, str] = {
    "unscanned": "?",
    "scanned": "S",
    "enumerated": "E",
    "exploited": "X",
    "owned": "*",
}

_SEVERITY_ORDER: dict[str, int] = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
    "NONE": 4,
}


class RichDashboard:
    """Rich-based live TUI dashboard for LazyOwn campaign monitoring.

    Attributes:
        live: When True, operates in non-blocking mode and returns snapshot
              data without running the interactive refresh loop.
    """

    def __init__(
        self,
        dashboard_engine: DashboardEngine | None = None,
        refresh_interval: float = 3.0,
        live: bool = False,
    ) -> None:
        """Initialize the Rich dashboard.

        Args:
            dashboard_engine: DashboardEngine instance for data sourcing.
            refresh_interval: Seconds between refreshes in blocking mode.
            live: Non-blocking mode when True. run() returns snapshot data
                  without entering the interactive loop.
        """
        self._engine = dashboard_engine or DashboardEngine()
        self._refresh_interval = refresh_interval
        self.live = live
        self._running = False
        self._should_stop = False
        self._console = Console()
        self._keyboard_thread: threading.Thread | None = None

    def run(self) -> dict[str, Any] | None:
        """Run the dashboard.

        Returns:
            If live=True, returns the built snapshot dict.
            Otherwise blocks until user quits (q key) and returns None.
        """
        if self.live:
            snapshot = self._engine.build_snapshot()
            self._console.print(self._render_layout(snapshot))
            return snapshot

        self._running = True
        self._should_stop = False

        self._keyboard_thread = threading.Thread(
            target=self._keyboard_listener, daemon=True
        )
        self._keyboard_thread.start()

        snapshot = self._engine.build_snapshot()

        try:
            with Live(
                self._render_layout(snapshot),
                console=self._console,
                auto_refresh=False,
                screen=True,
            ) as live_ctx:
                while self._running and not self._should_stop:
                    time.sleep(self._refresh_interval)
                    snapshot = self._engine.build_snapshot()
                    live_ctx.update(self._render_layout(snapshot))
        finally:
            self.stop()

        return None

    def stop(self) -> None:
        """Gracefully shut down the dashboard and restore terminal state."""
        self._running = False
        self._should_stop = True

    def _render(self) -> Layout:
        """Build a fresh snapshot and return the full frame layout.

        Returns:
            Rich Layout object for the complete dashboard frame.
        """
        snapshot = self._engine.build_snapshot()
        return self._render_layout(snapshot)

    def _keyboard_listener(self) -> None:
        """Thread target that listens for keyboard input in raw terminal mode."""
        fd = sys.stdin.fileno()
        old_settings: list[Any] = []
        try:
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            while self._running:
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                    if ch in ("q", "Q"):
                        self._should_stop = True
                        break
        except (termios.error, OSError, ValueError):
            pass
        finally:
            if old_settings:
                try:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                except (termios.error, OSError):
                    pass

    def _render_layout(self, snapshot: dict[str, Any]) -> Layout:
        """Build a full dashboard Layout from a snapshot dict.

        Args:
            snapshot: Dashboard snapshot from DashboardEngine.build_snapshot().

        Returns:
            Rich Layout ready for rendering.
        """
        layout = Layout()
        layout.split(
            Layout(self._render_header(snapshot), name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=5),
        )
        layout["body"].split_row(
            Layout(self._render_topology(snapshot), name="topology", ratio=2),
            Layout(self._render_recommendations(snapshot), name="recs", ratio=1),
        )
        layout["footer"].split(
            Layout(self._render_pivots_beacons(snapshot), name="pivots_beacons"),
            Layout(self._render_shortcuts(), name="shortcuts", size=3),
        )
        return layout

    def _render_header(self, snapshot: dict[str, Any]) -> Panel:
        """Render the dashboard header bar with campaign statistics.

        Args:
            snapshot: Dashboard snapshot.

        Returns:
            Panel containing the header statistics bar.
        """
        stats = snapshot.get("stats", {})
        timestamp = snapshot.get("timestamp", "")[:19].replace("T", " ")

        text = Text()
        text.append(" LAZYOWN LIVE DASHBOARD", style="bold white on dark_blue")
        text.append(f"  {timestamp}  ", style="dim")
        text.append(" | ", style="dim")
        text.append(
            f"Hosts: {stats.get('total_hosts', 0):>3}", style="bold cyan"
        )
        text.append(" | ", style="dim")
        text.append(
            f"Services: {stats.get('total_services', 0):>3}", style="bold green"
        )
        text.append(" | ", style="dim")
        text.append(
            f"Recs: {stats.get('recommendations', 0):>3}", style="bold yellow"
        )
        text.append(" | ", style="dim")
        text.append(
            f"Pivots: {stats.get('active_pivots', 0):>3}", style="bold magenta"
        )
        text.append(" | ", style="dim")
        text.append(
            f"Beacons: {stats.get('active_profiles', 0):>3}", style="bold red"
        )

        return Panel(text, box=HEAVY)

    def _render_topology(self, snapshot: dict[str, Any]) -> Panel:
        """Render the network topology tree panel.

        Args:
            snapshot: Dashboard snapshot.

        Returns:
            Panel with the network topology tree view.
        """
        nodes = snapshot.get("nodes", [])

        tree = Tree("[bold]Target Network[/bold]", guide_style="dim")
        tree.hide_root = False

        for node in nodes:
            phase = node.get("phase", "?")
            phase_color = _PHASE_STYLES.get(phase, "white")
            phase_icon = _PHASE_ICONS.get(phase, "?")
            ip = node["ip"]
            os_hint = node.get("os_hint", "")
            svc_list = node.get("services", [])

            label = Text()
            label.append(f"[{phase_icon}] ", style=phase_color)
            label.append(ip, style=f"bold {phase_color}")
            label.append(f"  ({phase})", style="dim")
            if os_hint:
                label.append(f"  [{os_hint}]", style="italic dim")

            host_branch = tree.add(label)
            for svc in svc_list[:15]:
                host_branch.add(Text(svc, style="dim"))
            if len(svc_list) > 15:
                host_branch.add(
                    Text(f"... +{len(svc_list) - 15} more", style="dim italic")
                )

        if not nodes:
            tree.add("[dim](no hosts discovered)[/dim]")

        return Panel(tree, title="Network Topology", border_style="blue", box=ROUNDED)

    def _render_recommendations(self, snapshot: dict[str, Any]) -> Panel:
        """Render exploit recommendations panel sorted by severity.

        Args:
            snapshot: Dashboard snapshot.

        Returns:
            Panel with a sorted table of exploit recommendations.
        """
        recs = snapshot.get("recommendations", [])

        if not recs:
            return Panel(
                Align.center("[dim]No recommendations available[/dim]",
                             vertical="middle"),
                title="Exploit Recommendations",
                border_style="yellow",
                box=ROUNDED,
            )

        sorted_recs = sorted(
            recs,
            key=lambda r: _SEVERITY_ORDER.get(
                r.get("severity", "MEDIUM"), 2
            ),
        )

        table = Table(
            box=MINIMAL,
            expand=True,
            show_header=True,
            header_style="bold",
            show_edge=False,
            padding=(0, 1),
        )
        table.add_column("ID", style="bold", width=14, no_wrap=True)
        table.add_column("Sev", width=5)
        table.add_column("Conf", width=5, justify="right")
        table.add_column("Target / Description", max_width=35)

        for r in sorted_recs[:20]:
            sev = str(r.get("severity", "?"))[:8]
            sev_style = _SEVERITY_STYLES.get(sev, "white")
            cve = str(r.get("cve", r.get("id", r.get("name", "?"))))[:14]
            conf = r.get("confidence", 0)
            target = str(r.get("target", r.get("host", "")))[:15]
            desc = str(r.get("description", r.get("rationale", "")))[:40]
            detail = f"{target} {desc}".strip()[:45]

            table.add_row(
                cve,
                f"[{sev_style}]{sev}[/{sev_style}]",
                f"{conf:.0%}",
                detail,
            )

        return Panel(
            table,
            title="Exploit Recommendations",
            border_style="yellow",
            box=ROUNDED,
        )

    def _render_pivots_beacons(self, snapshot: dict[str, Any]) -> Layout:
        """Render bottom panel with active pivots and beacons side by side.

        Args:
            snapshot: Dashboard snapshot.

        Returns:
            Layout with pivot routes and beacon profiles.
        """
        layout = Layout()
        layout.split_row(
            Layout(self._render_pivots(snapshot), name="pivots", ratio=1),
            Layout(self._render_beacons(snapshot), name="beacons", ratio=1),
        )
        return layout

    def _render_pivots(self, snapshot: dict[str, Any]) -> Panel:
        """Render active pivot routes panel.

        Args:
            snapshot: Dashboard snapshot.

        Returns:
            Panel with pivot entries.
        """
        pivots = snapshot.get("pivots", [])

        if not pivots:
            return Panel(
                Align.center("[dim]No active pivots[/dim]", vertical="middle"),
                title="Active Pivots",
                border_style="magenta",
                box=ROUNDED,
            )

        table = Table(box=MINIMAL, expand=True, show_header=False, padding=(0, 1))
        table.add_column("entry", style="dim")

        for p in pivots[:12]:
            ptype = str(p.get("type", "?"))[:8]
            ip = str(p.get("ip", "?"))[:15]
            port = str(p.get("port", "?"))[:6]
            table.add_row(f"[bold magenta]{ptype}[/bold magenta] => {ip}:{port}")

        return Panel(
            table,
            title=f"Active Pivots ({len(pivots)})",
            border_style="magenta",
            box=ROUNDED,
        )

    def _render_beacons(self, snapshot: dict[str, Any]) -> Panel:
        """Render active beacon profiles panel.

        Args:
            snapshot: Dashboard snapshot.

        Returns:
            Panel with beacon entries.
        """
        beacons = snapshot.get("beacons", [])

        if not beacons:
            return Panel(
                Align.center("[dim]No active beacons[/dim]", vertical="middle"),
                title="Active Beacons",
                border_style="red",
                box=ROUNDED,
            )

        table = Table(box=MINIMAL, expand=True, show_header=False, padding=(0, 1))
        table.add_column("entry", style="dim")

        for b in beacons[:12]:
            pid = str(b.get("profile_id", "?"))[:12]
            sleep_s = b.get("sleep_s", 0)
            jitter = b.get("jitter_ms", 0)
            dfront = str(b.get("domain_front", ""))[:20]
            detail_parts: list[str] = []
            if dfront:
                detail_parts.append(f"front={dfront}")
            detail_parts.append(f"sleep={sleep_s}s jitter={jitter}ms")
            detail = " ".join(detail_parts)
            table.add_row(f"[bold red]{pid}[/bold red]  {detail}")

        return Panel(
            table,
            title=f"Active Beacons ({len(beacons)})",
            border_style="red",
            box=ROUNDED,
        )

    def _render_shortcuts(self) -> Panel:
        """Render the keyboard shortcuts footer.

        Returns:
            Panel with keyboard shortcut hints.
        """
        text = Text()
        text.append(" q", style="bold white on red")
        text.append(" quit", style="dim")
        text.append("  ", style="dim")
        text.append(" r", style="bold white on blue")
        text.append(" refresh", style="dim")
        text.append("  ", style="dim")
        text.append(" h", style="bold white on green")
        text.append(" help", style="dim")

        return Panel(
            Align.center(text, vertical="middle"),
            box=HEAVY,
            padding=(0, 2),
        )
