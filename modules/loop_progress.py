"""Rich Live milestone panel for the autonomous loop.

Renders the orchestrator chain as persistent milestones — green done,
blue in-progress (spinner), red still pending — plus intent/fact/finding
counts, elapsed time and the latest activity line. The panel stays on
screen when the run finishes.

Robustness rules (learned the hard way):

- No markup strings anywhere: every cell is a ``Text`` object with an
  explicit style, so literal ``[green]`` tags can never leak and foreign
  ``[brackets]`` in activity lines can never crash rendering.
- Fixed panel width (100 cols) with non-wrapping cells: narrow sinks
  cannot corrupt the live region by wrapping.
- Non-terminal sinks never use ``Live`` (Rich would degrade to printing
  every refresh as a full new panel): they get one compact milestone
  line per stage change plus the final table at stop.
- All output goes through :mod:`core.safe_console`: no ANSI codes on
  non-tty sinks, ASCII box and markers when stdout cannot encode UTF-8.
- Stage states are inferred from the task overview, never asserted.
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field

from rich.text import Text

from core.safe_console import (
    get_console,
    milestone_glyph,
    panel_box,
    supports_unicode,
)

CHAIN_STAGES: tuple[str, ...] = (
    "lazy_task", "lazy_scope", "lazy_asset", "lazy_enrich",
    "lazy_planner", "lazy_frontier", "lazy_worker", "lazy_guard",
    "lazy_traffic", "lazy_finding", "lazy_retest", "lazy_compact",
    "lazy_trace", "lazy_report",
)

PANEL_WIDTH = 100

_STAGE_SHORT = {
    "lazy_task": "task",
    "lazy_scope": "scope",
    "lazy_asset": "assets",
    "lazy_enrich": "enrich",
    "lazy_planner": "plan",
    "lazy_frontier": "queue",
    "lazy_worker": "work",
    "lazy_guard": "guard",
    "lazy_traffic": "traffic",
    "lazy_finding": "find",
    "lazy_retest": "retest",
    "lazy_compact": "compact",
    "lazy_trace": "trace",
    "lazy_report": "report",
}

_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


@dataclass
class LoopSnapshot:
    """Point-in-time task state polled from the session stores."""

    status: str = "running"
    goals_total: int = 0
    goals_done: int = 0
    intents_pending: int = 0
    intents_open: int = 0
    intents_done: int = 0
    facts: int = 0
    findings: int = 0
    anchors: int = 0
    scope: int = 0
    tool_calls: int = 0
    results: int = 0
    last_line: str = ""
    elapsed_sec: float = 0.0


def snapshot_from_overview(overview: dict, record: dict | None = None,
                           activity_tail: str = "",
                           elapsed_sec: float = 0.0) -> LoopSnapshot:
    """Build a snapshot from a graph overview dict plus task record."""
    record = record or {}
    intents = overview.get("intents", []) or []
    goals = overview.get("goals", []) or []
    states = [str(i.get("state", "")) for i in intents]
    return LoopSnapshot(
        status=str(record.get("status", "running") or "running"),
        goals_total=len(goals),
        goals_done=sum(1 for g in goals if g.get("state") == "done"),
        intents_pending=sum(1 for s in states if s == "pending"),
        intents_open=sum(1 for s in states if s in ("open", "running")),
        intents_done=sum(1 for s in states if s == "done"),
        facts=int(overview.get("facts", 0) or 0),
        findings=int(overview.get("findings", 0) or 0),
        anchors=int(overview.get("anchors", 0) or 0),
        scope=len(record.get("scope", []) or []),
        last_line=str(activity_tail or "")[:160],
        elapsed_sec=float(elapsed_sec or 0.0),
    )


def snap_to_states(snapshot: LoopSnapshot) -> dict[str, str]:
    """Infer done/active/pending per chain stage from a snapshot."""
    worked = snapshot.facts + snapshot.findings > 0 or snapshot.results > 0
    states: dict[str, str] = {
        "lazy_task": "done",
        "lazy_scope": "done" if snapshot.scope > 0 else "pending",
        "lazy_asset": "done" if snapshot.anchors > 0 or worked else "pending",
        "lazy_enrich": "done" if worked else "pending",
        "lazy_planner": "done" if (snapshot.intents_pending
                                   + snapshot.intents_open
                                   + snapshot.intents_done) > 0 else "pending",
        "lazy_frontier": "done" if (snapshot.intents_pending == 0
                                    and (snapshot.intents_open
                                         + snapshot.intents_done) > 0) else "pending",
        "lazy_worker": "done" if (snapshot.intents_done > 0 or worked) else "pending",
        "lazy_guard": "done" if snapshot.tool_calls > 0 or worked else "pending",
        "lazy_traffic": "done" if snapshot.results > 0 or worked else "pending",
        "lazy_finding": "done" if snapshot.findings > 0 else "pending",
        "lazy_retest": "done" if snapshot.findings > 0 and (
            snapshot.intents_done > 0 or snapshot.intents_pending == 0) else "pending",
        "lazy_compact": "done" if snapshot.status in ("done", "exhausted",
                                                      "timeout") else "pending",
        "lazy_trace": "done" if snapshot.anchors > 0 else "pending",
        "lazy_report": "done" if snapshot.status == "done" else "pending",
    }
    return states


def sanitize_line(line: str) -> str:
    """Strip ANSI codes and carriage returns from a transcript line."""
    text = _ANSI_RE.sub("", line or "")
    return text.replace("\r", "").rstrip("\n")


@dataclass
class LoopProgress:
    """Live milestone panel; call :meth:`refresh` from the poll loop."""

    goal: str = ""
    target: str = ""
    chain: tuple[str, ...] = CHAIN_STAGES
    _live: object = field(default=None, repr=False)
    _console: object = field(default=None, repr=False)
    _started_at: float = field(default=0.0, repr=False)
    _lock: object = field(default_factory=threading.Lock, repr=False)
    _last_stage: object = field(default=None, repr=False)
    _final: object = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Create the safe console used for every render."""
        self._console = get_console()

    @property
    def live_mode(self) -> bool:
        """True only when the sink supports a real live region."""
        try:
            return bool(self._console.is_terminal)
        except Exception:
            return False

    def start(self) -> None:
        """Open the Live display, or print the header in line mode."""
        with self._lock:
            if self._live is not None:
                return
            from rich.live import Live
            self._started_at = time.monotonic()
            if not self.live_mode:
                self._live = False
                try:
                    self._console.print(self._header(), markup=False,
                                        highlight=False)
                except Exception:
                    pass
                return
            self._live = Live(self._render(LoopSnapshot()),
                              console=self._console, transient=False,
                              auto_refresh=True, refresh_per_second=4)
            try:
                self._live.start()
            except Exception:
                self._live = False

    def stop(self) -> None:
        """Freeze the final panel on screen (both modes)."""
        with self._lock:
            live, self._live = self._live, None
            final = self._final
        if live is None or live is False:
            if final is not None and live is False:
                try:
                    self._console.print(final, markup=False, highlight=False)
                except Exception:
                    pass
            return
        try:
            live.stop()
        except Exception:
            pass

    def refresh(self, snapshot: LoopSnapshot) -> None:
        """Re-render milestones from a fresh snapshot (thread-safe)."""
        with self._lock:
            live = self._live
        if live is None:
            return
        if live is False:
            states = snap_to_states(snapshot)
            current = next((s for s in self.chain if states.get(s) != "done"), None)
            if current != self._last_stage:
                self._last_stage = current
                try:
                    self._console.print(self._milestone_line(snapshot, states, current),
                                        markup=False, highlight=False)
                except Exception:
                    pass
            self._final = self._render(snapshot)
            return
        try:
            live.update(self._render(snapshot))
        except Exception:
            pass

    def emit(self, line: str) -> None:
        """Print a transcript line above the live panel, colors kept safe."""
        cleaned = sanitize_line(line)
        if not cleaned.strip():
            return
        try:
            text = Text.from_ansi(cleaned)
            self._console.print(text, end="\n", markup=False, highlight=False)
        except Exception:
            try:
                self._console.print(Text(cleaned), markup=False, highlight=False)
            except Exception:
                pass

    def _header(self):
        """Plain-text header for line mode."""
        title = f"auto_loop :: {self.goal[:80]}"
        if self.target:
            title += f"  ->  {self.target}"
        return Text(title, style="bold")

    def _milestone_line(self, snapshot: LoopSnapshot, states: dict,
                        current: str | None):
        """One compact line per stage change for line mode."""
        done = sum(1 for s in self.chain if states.get(s) == "done")
        text = Text()
        text.append(f"[{done}/{len(self.chain)}] ", style="dim")
        if current is None:
            text.append("all milestones done", style="green")
        else:
            text.append(f"now: {_STAGE_SHORT.get(current, current)}", style="blue")
        text.append(f"  intents {snapshot.intents_done}/{snapshot.intents_pending} "
                    f"facts {snapshot.facts} findings {snapshot.findings} "
                    f"{snapshot.status} {snapshot.elapsed_sec:.0f}s", style="dim")
        return text

    def _footer(self, snapshot: LoopSnapshot, elapsed: float):
        """Plain-text footer (never parses activity content as markup)."""
        footer = Text()
        footer.append(f"goals {snapshot.goals_done}/{snapshot.goals_total}  ", style="dim")
        footer.append(f"intents {snapshot.intents_done} done / "
                      f"{snapshot.intents_open} open / "
                      f"{snapshot.intents_pending} pending  ", style="dim")
        footer.append(f"facts {snapshot.facts}  findings {snapshot.findings}  "
                      f"{snapshot.status}  {elapsed:.0f}s", style="dim")
        if snapshot.last_line:
            footer.append("\n[last] ", style="dim")
            footer.append(snapshot.last_line[:120])
        return footer

    def _render(self, snapshot: LoopSnapshot):
        """Build the milestone panel for a snapshot (Text cells only)."""
        from rich.panel import Panel
        from rich.spinner import Spinner
        from rich.table import Table
        states = snap_to_states(snapshot)
        current = next((s for s in self.chain if states.get(s) != "done"), None)
        table = Table(show_header=False, box=None, padding=(0, 1), expand=False)
        table.add_column("mark", width=4, no_wrap=True)
        table.add_column("stage", no_wrap=True)
        table.add_column("detail", no_wrap=True)
        for stage in self.chain:
            state = states.get(stage, "pending")
            short = _STAGE_SHORT.get(stage, stage)
            if state == "done":
                table.add_row(Text(milestone_glyph("done"), style="green"),
                              Text(short, style="green"), Text(""))
            elif stage == current:
                spinner = Spinner("dots" if supports_unicode() else "line",
                                  style="blue", text=Text(""))
                table.add_row(spinner, Text(short, style="bold blue"),
                              Text("running", style="blue"))
            else:
                table.add_row(Text(milestone_glyph("pending"), style="red"),
                              Text(short, style="red"), Text(""))
        elapsed = time.monotonic() - (self._started_at or time.monotonic())
        title = Text(f"auto_loop :: {self.goal[:60]}", style="bold")
        if self.target:
            title.append(f"  ->  {self.target}", style="dim")
        return Panel(table, title=title,
                     subtitle=self._footer(snapshot, elapsed),
                     box=panel_box(), border_style="cyan", padding=(0, 1),
                     width=min(PANEL_WIDTH, self._console.width or PANEL_WIDTH))


__all__ = [
    "CHAIN_STAGES",
    "LoopProgress",
    "LoopSnapshot",
    "sanitize_line",
    "snap_to_states",
    "snapshot_from_overview",
]
