"""Purple Team Dashboard — Textual TUI for engagement monitoring.

Launch from the LazyOwn shell with ``purple_dashboard`` or directly:

    python3 -m cli.purple_tui

Layout:
    ┌─ Header (session / score / detection rate) ────────────────────────┐
    │  Left (Score + Methods)  │  Center (Recent Actions) │ Right (Stats)│
    ├────────────────────────────────────────────────────────────────────┤
    │  Footer ([Q] Quit  [R] Refresh  [E] Exec  [?] Help)              │
    └───────────────────────────────────────────────────────────────────┘
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Static

_SESSIONS_DIR = Path("sessions")
_DATASET_FILE = _SESSIONS_DIR / "purple_dataset.csv"
_AUDIT_FILE = _SESSIONS_DIR / "purple_audit.jsonl"
_SCORE_FILE = _SESSIONS_DIR / "purple_score.json"
_REPORT_FILE = _SESSIONS_DIR / "purple_report.json"


def _load_score() -> dict[str, Any]:
    if _SCORE_FILE.exists():
        try:
            return json.loads(_SCORE_FILE.read_text())
        except Exception:
            pass
    return {"total": 0, "detected": 0, "missed": 0, "score": 0.0,
            "by_category": {}, "by_method": {}}


def _load_recent_results(n: int = 15) -> list[dict[str, Any]]:
    if not _AUDIT_FILE.exists():
        return []
    results = []
    for line in _AUDIT_FILE.read_text().splitlines():
        if not line.strip():
            continue
        try:
            results.append(json.loads(line))
        except Exception:
            continue
    return results[-n:]


def _dataset_stats() -> dict[str, Any]:
    if not _DATASET_FILE.exists():
        return {"rows": 0, "size_kb": 0}
    size = _DATASET_FILE.stat().st_size // 1024
    with open(_DATASET_FILE) as f:
        rows = sum(1 for _ in f) - 1
    return {"rows": max(0, rows), "size_kb": size}


def _make_bar(value: float, width: int = 20) -> str:
    filled = int(value * width)
    return "#" * filled + "." * (width - filled)


def _color_rate(rate: float) -> str:
    if rate <= 0.3:
        return f"[green]{rate:.0%}[/green]"
    elif rate <= 0.6:
        return f"[yellow]{rate:.0%}[/yellow]"
    else:
        return f"[red]{rate:.0%}[/red]"


class PurpleDashboard(App):
    """Textual TUI for purple team engagement monitoring."""

    CSS = """
    Screen { background: $surface }
    #score-panel { height: 8; border: solid $accent; padding: 1 2 }
    #methods-panel { height: auto; border: solid $accent; padding: 1 2 }
    #actions-panel { border: solid $accent; padding: 1 2 }
    #stats-panel { width: 35; border: solid $accent; padding: 1 2 }
    .title { text-style: bold; color: $accent }
    .hit { color: green }
    .miss { color: red }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="left-col"):
                yield Static(id="score-panel")
                yield Static(id="methods-panel")
            yield Static(id="actions-panel")
            yield Static(id="stats-panel")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Purple Team Dashboard"
        self.refresh_data()

    def action_refresh(self) -> None:
        self.refresh_data()

    def refresh_data(self) -> None:
        score = _load_score()
        results = _load_recent_results()
        ds = _dataset_stats()

        self._render_score(score)
        self._render_methods(score)
        self._render_actions(results)
        self._render_stats(score, ds)

    def _render_score(self, score: dict) -> None:
        panel = self.query_one("#score-panel")
        total = score.get("total", 0)
        detected = score.get("detected", 0)
        missed = score.get("missed", 0)
        rate = score.get("score", 0.0)

        if total == 0:
            status = "NO DATA"
            color = "white"
        elif rate <= 0.3:
            status = "STEALTH"
            color = "green"
        elif rate <= 0.6:
            status = "MODERATE"
            color = "yellow"
        elif rate <= 0.8:
            status = "NOISY"
            color = "red"
        else:
            status = "VISIBLE"
            color = "red"

        bar = _make_bar(rate, 30)
        text = Text.from_markup(
            f"[bold]PURPLE TEAM SCORE[/bold]\n\n"
            f"  Detection Rate: [{color}]{rate:.1%}[/{color}]  [{color}]{status}[/{color}]\n"
            f"  [{color}]{bar}[/{color}]\n\n"
            f"  Actions: {total}  |  Detected: {detected}  |  Missed: {missed}"
        )
        panel.update(text)

    def _render_methods(self, score: dict) -> None:
        panel = self.query_one("#methods-panel")
        methods = score.get("by_method", {})
        if not methods:
            panel.update(Text.from_markup("[dim]No detection method data yet[/dim]"))
            return

        lines = ["[bold]DETECTION METHODS[/bold]\n"]
        for method, stats in sorted(methods.items()):
            total = stats.get("total", 0)
            det = stats.get("detected", 0)
            rate = det / total if total > 0 else 0
            bar = _make_bar(rate, 15)
            lines.append(f"  {method:20s} [{bar}] {_color_rate(rate)}")
        panel.update(Text.from_markup("\n".join(lines)))

    def _render_actions(self, results: list) -> None:
        panel = self.query_one("#actions-panel")
        if not results:
            panel.update(Text.from_markup(
                "[bold]RECENT ACTIONS[/bold]\n\n"
                "  [dim]No actions recorded yet.[/dim]\n"
                "  Run 'purple_exec <command>' to start.\n"
            ))
            return

        lines = ["[bold]RECENT ACTIONS[/bold]\n"]
        lines.append(f"  {'Time':8s}  {'Command':35s}  {'Cat':12s}  {'Oracle':7s}  {'BT':6s}")
        lines.append(f"  {'-'*72}")

        for r in reversed(results):
            ts = r.get("timestamp", "")[11:19]
            cmd = r.get("command", "")[:20]
            args = r.get("args", "")[:14]
            full_cmd = f"{cmd} {args}".strip()[:35]
            cat = r.get("category", "")[:12]
            oracle = r.get("oracle_prediction", 0)
            detected = r.get("actually_detected", False)

            bt_label = "[green]HIT[/green]" if detected else "[dim]miss[/dim]"
            oracle_str = f"{oracle:.0%}"

            lines.append(
                f"  {ts:8s}  {full_cmd:35s}  {cat:12s}  {oracle_str:7s}  {bt_label}"
            )

        panel.update(Text.from_markup("\n".join(lines)))

    def _render_stats(self, score: dict, ds: dict) -> None:
        panel = self.query_one("#stats-panel")
        cats = score.get("by_category", {})

        lines = ["[bold]STATISTICS[/bold]\n"]
        lines.append(f"  Dataset rows : {ds.get('rows', 0)}")
        lines.append(f"  Dataset size : {ds.get('size_kb', 0)} KB")
        lines.append("")

        if cats:
            lines.append("[bold]BY CATEGORY[/bold]")
            for cat, stats in sorted(cats.items()):
                total = stats.get("total", 0)
                det = stats.get("detected", 0)
                rate = det / total if total > 0 else 0
                bar = _make_bar(rate, 10)
                lines.append(f"  {cat:15s} [{bar}] {_color_rate(rate)}")

        lines.append("")
        lines.append("[bold]FILES[/bold]")
        lines.append(f"  sessions/purple_dataset.csv")
        lines.append(f"  sessions/purple_audit.jsonl")
        lines.append(f"  sessions/purple_score.json")
        lines.append(f"  sessions/detection_feedback.jsonl")

        panel.update(Text.from_markup("\n".join(lines)))


def launch() -> None:
    """Launch the purple team dashboard TUI."""
    app = PurpleDashboard()
    app.run()


if __name__ == "__main__":
    launch()
