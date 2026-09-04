"""Session resumer for the LazyOwn shell.

Scans ``sessions/`` for previous engagement data (IP directories, scan files,
credentials) and presents a resume panel at shell startup so the operator
can quickly pick up where they left off.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py``.
    - All output through ``rich.console.Console``.
    - ``SessionResumer`` receives a sessions dir path; no hardcoded paths.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console(highlight=False, soft_wrap=True)


@dataclass(frozen=True)
class SessionSummary:
    """One previous engagement discovered in sessions/."""

    target: str
    phase: str
    scan_exists: bool
    creds_exist: bool
    last_modified: float
    file_count: int


@dataclass
class SessionResumerConfig:
    """Centralised constants for the session resumer."""

    sessions_dir: str = "sessions"
    max_targets: int = 10
    scan_pattern: str = "scan_*.nmap"
    creds_pattern: str = "credentials*.txt"
    world_model_file: str = "world_model.json"


class SessionResumer:
    """Scan sessions/ and present a resume panel.

    Args:
        config: Optional config override.
    """

    def __init__(self, config: SessionResumerConfig | None = None) -> None:
        self._config = config or SessionResumerConfig()
        self._root = Path(self._config.sessions_dir)

    def _discover_targets(self) -> list[SessionSummary]:
        """Discover IP-named subdirectories and top-level scan files."""
        summaries: list[SessionSummary] = []
        if not self._root.is_dir():
            return summaries

        seen: set[str] = set()

        for entry in sorted(self._root.iterdir()):
            if not entry.is_dir():
                continue
            name = entry.name
            if name.startswith(".") or name.startswith("__"):
                continue
            if name in (
                "captured_images",
                "c2_profiles",
                "db",
                "ai_model",
                "bofs",
                "cve_cache",
                "chromadb",
                "delivery",
                "detection_cache",
                "default_engagement",
                "sessions",
            ):
                continue

            scan_files = list(entry.glob(self._config.scan_pattern))
            creds_files = list(entry.glob(self._config.creds_pattern))
            world_model = entry / self._config.world_model_file

            phase = "unknown"
            if world_model.exists():
                try:
                    wm_data = json.loads(world_model.read_text())
                    phase = wm_data.get("phase", "unknown")
                except Exception:
                    pass

            try:
                mtime = max(
                    (f.stat().st_mtime for f in entry.iterdir() if f.is_file()),
                    default=0.0,
                )
            except OSError:
                mtime = 0.0

            file_count = sum(1 for _ in entry.iterdir())

            if name not in seen and (scan_files or creds_files or file_count > 2):
                seen.add(name)
                summaries.append(
                    SessionSummary(
                        target=name,
                        phase=phase,
                        scan_exists=bool(scan_files),
                        creds_exist=bool(creds_files),
                        last_modified=mtime,
                        file_count=file_count,
                    )
                )

        summaries.sort(key=lambda s: s.last_modified, reverse=True)
        return summaries[: self._config.max_targets]

    def render_startup_panel(self) -> str | None:
        """Render the resume panel and return the selected target IP, or None."""
        summaries = self._discover_targets()
        if not summaries:
            return None

        import time

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=3)
        table.add_column("Target", style="green")
        table.add_column("Phase")
        table.add_column("Scans", justify="center")
        table.add_column("Creds", justify="center")
        table.add_column("Files", justify="right")
        table.add_column("Last active", style="dim")

        for idx, s in enumerate(summaries, 1):
            age = time.time() - s.last_modified
            if age < 3600:
                age_str = f"{int(age / 60)}m ago"
            elif age < 86400:
                age_str = f"{int(age / 3600)}h ago"
            else:
                age_str = f"{int(age / 86400)}d ago"

            table.add_row(
                str(idx),
                s.target,
                s.phase,
                "[green]yes[/]" if s.scan_exists else "[dim]no[/]",
                "[green]yes[/]" if s.creds_exist else "[dim]no[/]",
                str(s.file_count),
                age_str,
            )

        _console.print()
        _console.print(
            Panel(
                table,
                title="[bold]Previous sessions found[/]",
                subtitle="[dim]Type a number to resume, or press Enter to start fresh[/]",
                border_style="cyan",
            )
        )

        try:
            choice = input("  Resume which session? [number/Enter]: ").strip()
        except (EOFError, KeyboardInterrupt):
            return None

        if not choice:
            return None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(summaries):
                return summaries[idx].target
        except ValueError:
            pass

        return None
