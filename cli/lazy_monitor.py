"""Live worker-visibility monitor for the autonomous loop.

The loop is never a black box: every worker's tool calls, results,
guard decisions, approvals, traffic and findings stream into a
multi-pane Textual view. Two modes share the same rendering:

- attach (``lazy_view [task]``): tails the task's store files, so it
  works from a second terminal while ``lazy_loop`` runs elsewhere and
  keeps working after the run for audit;
- embedded (``lazy_loop --view``): the runner starts the engine inside
  this app and also streams the executor's raw output live.

Keys: ``q`` quit, ``p``/``r`` pause/resume, ``a``/``d`` approve/deny
first pending intercept, ``h`` hint, ``s`` steer, ``k`` kill, ``f``
findings, ``g`` guard, ``t`` traffic, ``1``..``5`` focus a worker.
"""

from __future__ import annotations

import threading
from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Input, RichLog, Static, TabbedContent, TabPane

from modules.jsonl_tail import JsonlTail
from modules.lazy_engine import ExplorationGraph, InterceptQueue, TaskStore
from modules.loop_progress import CHAIN_STAGES, snap_to_states, snapshot_from_overview

POLL_SEC = 0.5
FINDINGS_EVERY_TICKS = 8
TRAFFIC_LINES = 400
ACTIVITY_LINES = 1200
MAX_WORKER_PANES = 6
STORE_DIR = Path("sessions") / "lazy"

_KIND_STYLE = {
    "tool": "bold cyan",
    "result": "white",
    "block": "bold red",
    "deny": "bold red",
    "intercept": "bold yellow",
    "kill": "bold red",
    "steer": "bold magenta",
    "settle": "yellow",
    "settlement": "yellow",
    "finding": "bold green",
    "verdict": "green",
    "enriched": "blue",
    "round": "dim",
    "retry": "yellow",
    "capability": "yellow",
    "pause": "yellow",
}


class PromptModal(ModalScreen[str]):
    """One-line modal used for hints and steering messages."""

    BINDINGS = [("escape", "dismiss('')", "cancel")]

    def __init__(self, title: str, placeholder: str = "") -> None:
        """Store the modal labels."""
        super().__init__()
        self._title = title
        self._placeholder = placeholder

    def compose(self) -> ComposeResult:
        """Title plus a single input line."""
        yield Vertical(
            Static(self._title, classes="modal-title"),
            Input(placeholder=self._placeholder, id="modal-input"),
            classes="modal-box",
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Dismiss with the typed value."""
        self.dismiss(str(event.value))

    def action_dismiss(self, value: str = "") -> None:
        """Escape closes with an empty value."""
        self.dismiss("")


class LazyMonitorApp(App[dict]):
    """Multi-pane loop monitor with operator controls."""

    CSS = """
    #body { height: 1fr; }
    #left { width: 38; border: round $accent; padding: 0 1; }
    #workers-grid { width: 1fr; }
    .worker-pane { border: round $primary; height: 1fr; }
    .worker-title { background: $boost; }
    #bottom { height: 14; border: round $secondary; }
    .modal-box { width: 70; height: auto; padding: 1 2; background: $surface;
                 border: round $accent; }
    .modal-title { text-style: bold; padding-bottom: 1; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("n", "next_task", "Next task"),
        Binding("p", "pause", "Pause"),
        Binding("r", "resume", "Resume"),
        Binding("a", "approve", "Approve"),
        Binding("d", "deny", "Deny"),
        Binding("h", "hint", "Hint"),
        Binding("s", "steer", "Steer"),
        Binding("k", "kill", "Kill"),
        Binding("f", "tab_findings", "Findings"),
        Binding("g", "tab_guard", "Guard"),
        Binding("t", "tab_traffic", "Traffic"),
        Binding("1", "focus_worker(1)", "W1", show=False),
        Binding("2", "focus_worker(2)", "W2", show=False),
        Binding("3", "focus_worker(3)", "W3", show=False),
        Binding("4", "focus_worker(4)", "W4", show=False),
        Binding("5", "focus_worker(5)", "W5", show=False),
    ]

    def __init__(self, task_id: str = "", engine=None, config=None, params: dict | None = None) -> None:
        """Bind the monitor to a task and optionally embed a live engine."""
        super().__init__()
        self.task_id = task_id
        self.engine = engine
        self.config = config
        self.params = dict(params or {})
        self.result: dict = {}
        self._ticks = 0
        self._panes: dict[str, RichLog] = {}
        self._pane_titles: dict[str, Static] = {}
        self._tails: dict[str, JsonlTail] = {}
        self._seen_findings: set = set()
        self._cancelled = {"flag": False}
        self._engine_thread: threading.Thread | None = None

    def compose(self) -> ComposeResult:
        """Build the split view: stages, worker panes, audit tabs."""
        yield Header(show_clock=True)
        with Horizontal(id="body"):
            with Vertical(id="left"):
                yield Static("chain", classes="worker-title")
                yield Static(id="stages")
                yield Static(id="stats")
                yield Static(id="approvals")
            with VerticalScroll(id="workers-grid"):
                for index in range(1, MAX_WORKER_PANES + 1):
                    name = f"worker-{index}"
                    with Vertical(classes="worker-pane", id=f"pane-{name}"):
                        yield Static(name, classes="worker-title", id=f"title-{name}")
                        yield RichLog(
                            markup=False, wrap=True, highlight=False, max_lines=TRAFFIC_LINES, id=f"log-{name}"
                        )
        with TabbedContent(id="bottom"):
            with TabPane("Activity", id="tab-activity"):
                yield RichLog(markup=False, wrap=True, highlight=False, max_lines=ACTIVITY_LINES, id="log-activity")
            with TabPane("Guard", id="tab-guard"):
                yield RichLog(markup=False, wrap=True, highlight=False, max_lines=TRAFFIC_LINES, id="log-guard")
            with TabPane("Traffic", id="tab-traffic"):
                yield RichLog(markup=False, wrap=True, highlight=False, max_lines=TRAFFIC_LINES, id="log-traffic")
            with TabPane("Findings", id="tab-findings"):
                yield RichLog(markup=False, wrap=True, highlight=False, max_lines=TRAFFIC_LINES, id="log-findings")
        yield Footer()

    def on_mount(self) -> None:
        """Resolve the task, wire pane logs and start polling."""
        self._resolve_task()
        for index in range(1, MAX_WORKER_PANES + 1):
            name = f"worker-{index}"
            try:
                self._panes[name] = self.query_one(f"#log-{name}", RichLog)
                self._pane_titles[name] = self.query_one(f"#title-{name}", Static)
            except Exception:
                continue
        self._activity = self.query_one("#log-activity", RichLog)
        self._guard = self.query_one("#log-guard", RichLog)
        self._traffic = self.query_one("#log-traffic", RichLog)
        self._findings = self.query_one("#log-findings", RichLog)
        self._stages = self.query_one("#stages", Static)
        self._stats = self.query_one("#stats", Static)
        self._approvals = self.query_one("#approvals", Static)
        self._init_tails()
        self._render_stages({})
        self.set_interval(POLL_SEC, self._poll)
        if self.engine is not None:
            self._start_engine()
        self.title = f"lazy_view :: {self.task_id or 'no task'}"

    def _resolve_task(self) -> None:
        """Pick the newest task when none was given."""
        if self.task_id:
            return
        try:
            tasks = TaskStore().list()
            if tasks:
                self.task_id = str(tasks[-1].get("task_id", ""))
        except Exception:
            self.task_id = ""

    def _init_tails(self) -> None:
        """Create one incremental reader per audited stream."""
        names = {
            "activity": f"activity_{self.task_id}.jsonl",
            "guard": f"guard_audit_{self.task_id}.jsonl",
            "traffic": f"traffic_{self.task_id}.jsonl",
        }
        for key, filename in names.items():
            self._tails[key] = JsonlTail(STORE_DIR / filename)

    def _start_engine(self) -> None:
        """Run the embedded orchestration in a background thread."""
        from modules.lazy_runner import build_executor

        def _stream(line: str) -> None:
            try:
                self.call_from_thread(self._append_activity, str(line), "dim")
            except Exception:
                pass

        executor = build_executor(getattr(self.engine, "shell", None), self.config, _stream, self._cancelled)

        def _run() -> None:
            try:
                result = self.engine.orchestrate(
                    goal=self.config.goal,
                    task_id=self.config.task_id,
                    target=self.config.target,
                    max_rounds=self.config.rounds,
                    workers=self.config.workers,
                    timeout_sec=self.config.timeout,
                    executor=executor,
                )
            except BaseException as exc:  # noqa: BLE001 - surfaced in the UI
                result = {"error": str(exc), "task_id": self.config.task_id}
            try:
                self.call_from_thread(self._finish, result)
            except Exception:
                pass

        self._engine_thread = threading.Thread(target=_run, daemon=True)
        self._engine_thread.start()

    def _finish(self, result: dict) -> None:
        """Store the engine summary and announce completion."""
        self.result = dict(result or {})
        status = self.result.get("status", self.result.get("error", "done"))
        self._append_activity(f"=== loop finished: {status} (q to quit, state is saved) ===", "bold green")

    def _poll(self) -> None:
        """Tail every store, update panes, stages and approvals."""
        self._ticks += 1
        self._drain_activity()
        self._drain_guard()
        self._drain_traffic()
        self._render_approvals()
        if self._ticks % FINDINGS_EVERY_TICKS == 0:
            self._render_findings()
            self._render_stages(self._overview())

    def _overview(self) -> dict:
        """Current graph overview (never raises)."""
        try:
            return ExplorationGraph(self.task_id).overview()
        except Exception:
            return {}

    def _drain_activity(self) -> None:
        """Route new activity rows to the worker panes and activity tab."""
        for record in self._tails["activity"].read_new():
            worker = str(record.get("worker", ""))
            kind = str(record.get("kind", ""))
            text = str(record.get("text", ""))
            line = Text()
            line.append(f"[{kind}] ", style=_KIND_STYLE.get(kind, "dim"))
            line.append(text[:400], style=_KIND_STYLE.get(kind, ""))
            if worker.startswith("worker-") and worker in self._panes:
                line = Text()
                line.append(f"[{kind}] ", style=_KIND_STYLE.get(kind, "dim"))
                line.append(text[:400])
                self._panes[worker].write(line)
                if kind == "tool":
                    self._pane_titles[worker].update(f"{worker} :: {text[:70]}")
                elif kind in ("result", "block", "kill", "settle"):
                    self._pane_titles[worker].update(f"{worker} :: {kind}")
            self._append_activity_text(line)

    def _drain_guard(self) -> None:
        """Render new guard audit rows."""
        for record in self._tails["guard"].read_new():
            action = str(record.get("action", ""))
            style = {"deny": "bold red", "ask": "bold yellow"}.get(action, "green")
            line = Text()
            line.append(f"{action.upper():5} ", style=style)
            line.append(
                f"{record.get('tool_use_id', '')} "
                f"{str(record.get('reason', ''))[:80]} :: "
                f"{str(record.get('command', ''))[:160]}"
            )
            self._guard.write(line)

    def _drain_traffic(self) -> None:
        """Render new traffic records."""
        for record in self._tails["traffic"].read_new():
            line = Text()
            line.append(f"{str(record.get('kind', '')):6} ", style="cyan")
            line.append(f"{str(record.get('command', ''))[:120]}  ")
            line.append(str(record.get("digest", ""))[:12], style="dim")
            self._traffic.write(line)

    def _render_approvals(self) -> None:
        """Show the pending approval queue with its decision keys."""
        try:
            pending = InterceptQueue(self.task_id).pending()
        except Exception:
            pending = []
        text = Text()
        text.append(f"approvals pending: {len(pending)}\n", style="bold")
        for item in pending[:6]:
            text.append(f"#{item.get('id')} ", style="bold yellow")
            text.append(f"{str(item.get('reason', ''))[:40]}\n")
            text.append(f"   {str(item.get('command', ''))[:70]}\n", style="dim")
        if pending:
            text.append("[a] approve first  [d] deny first", style="green")
        try:
            self._approvals.update(text)
        except Exception:
            pass

    def _render_findings(self) -> None:
        """Refresh the findings tab from the exploration graph."""
        try:
            findings = ExplorationGraph(self.task_id).list("finding")
        except Exception:
            return
        for node in findings:
            signature = str(node.meta.get("sig", node.node_id))
            if signature in getattr(self, "_seen_findings", set()):
                continue
            seen = getattr(self, "_seen_findings", set())
            seen.add(signature)
            self._seen_findings = seen
            line = Text()
            line.append(f"#{node.node_id} ", style="bold green")
            line.append(f"[{node.meta.get('severity', '')}] ", style="green")
            line.append(str(node.text)[:200])
            self._findings.write(line)

    def _render_stages(self, overview: dict) -> None:
        """Render the orchestrator chain milestones plus counters."""
        record = {}
        try:
            record = self.engine.store.get(self.task_id) if self.engine else {}
            record = record or TaskStore().get(self.task_id) or {}
        except Exception:
            record = {}
        snapshot = snapshot_from_overview(overview, record)
        states = snap_to_states(snapshot)
        text = Text()
        for stage in CHAIN_STAGES:
            state = states.get(stage, "pending")
            mark = {"done": "[x]", "pending": "[ ]"}.get(state, "[>]")
            style = {"done": "green", "pending": "red"}.get(state, "bold blue")
            text.append(f"{mark} {stage}\n", style=style)
        try:
            self._stages.update(text)
        except Exception:
            pass
        stats = Text()
        stats.append(f"status  {snapshot.status}\n")
        stats.append(f"goals   {snapshot.goals_done}/{snapshot.goals_total}\n")
        stats.append(
            f"intents {snapshot.intents_done} done / "
            f"{snapshot.intents_open} open / {snapshot.intents_pending} pending\n"
        )
        stats.append(f"facts   {snapshot.facts}\n")
        stats.append(f"tools   {snapshot.tool_calls}\n")
        stats.append(f"findings {snapshot.findings}\n")
        stats.append(f"scope   {snapshot.scope}\n")
        try:
            self._stats.update(stats)
        except Exception:
            pass

    def _append_activity(self, text: str, style: str = "") -> None:
        """Append a raw line to the activity transcript."""
        line = Text(text) if not style else Text(text, style=style)
        self._append_activity_text(line)

    def _append_activity_text(self, line: Text) -> None:
        """Safe write to the activity log."""
        try:
            self._activity.write(line)
        except Exception:
            pass

    def _running_intent(self):
        """Return the newest running/open intent for steer/kill actions."""
        try:
            intents = [n for n in ExplorationGraph(self.task_id).list("intent") if n.state in ("open", "running")]
            if intents:
                return intents[-1]
        except Exception:
            pass
        return None

    def action_pause(self) -> None:
        """Pause the task between worker steps."""
        try:
            TaskStore().pause(self.task_id)
            self._append_activity("task paused", "yellow")
        except Exception:
            pass

    def action_resume(self) -> None:
        """Resume a paused task."""
        try:
            TaskStore().resume(self.task_id)
            self._append_activity("task resumed", "green")
        except Exception:
            pass

    def action_approve(self) -> None:
        """Approve the first pending intercept."""
        self._decide("approved")

    def action_deny(self) -> None:
        """Deny the first pending intercept."""
        self._decide("denied")

    def _decide(self, verdict: str) -> None:
        """Decide the first pending approval."""
        try:
            pending = InterceptQueue(self.task_id).pending()
            if not pending:
                return
            item_id = int(pending[0].get("id", 0))
            if InterceptQueue(self.task_id).decide(item_id, verdict):
                self._append_activity(f"intercept #{item_id} {verdict}", "green" if verdict == "approved" else "red")
        except Exception:
            pass

    def action_hint(self) -> None:
        """Inject an operator hint for the next planner round."""

        def _done(text: str) -> None:
            if text.strip():
                try:
                    self.engine.add_hint(self.task_id, text.strip()) if self.engine else _hint_via_graph(
                        self.task_id, text.strip()
                    )
                    self._append_activity(f"hint: {text.strip()[:120]}", "magenta")
                except Exception:
                    pass

        self.push_screen(PromptModal("Planner hint"), _done)

    def action_steer(self) -> None:
        """Send a mid-run correction to the newest running intent."""
        intent = self._running_intent()
        if intent is None:
            self._append_activity("no running intent to steer", "yellow")
            return

        def _done(text: str) -> None:
            if text.strip():
                try:
                    TaskStore().steer(self.task_id, intent.node_id, text.strip())
                    self._append_activity(f"steer intent #{intent.node_id}: {text.strip()[:120]}", "magenta")
                except Exception:
                    pass

        self.push_screen(PromptModal(f"Steer intent #{intent.node_id}"), _done)

    def action_kill(self) -> None:
        """Kill the newest running intent."""
        intent = self._running_intent()
        if intent is None:
            self._append_activity("no running intent to kill", "yellow")
            return
        try:
            TaskStore().kill(self.task_id, intent.node_id)
            self._append_activity(f"kill intent #{intent.node_id}", "red")
        except Exception:
            pass

    def action_tab_findings(self) -> None:
        """Focus the findings tab."""
        self._focus_tab("tab-findings")

    def action_tab_guard(self) -> None:
        """Focus the guard tab."""
        self._focus_tab("tab-guard")

    def action_tab_traffic(self) -> None:
        """Focus the traffic tab."""
        self._focus_tab("tab-traffic")

    def _focus_tab(self, tab_id: str) -> None:
        """Activate one bottom tab by id."""
        try:
            self.query_one("#bottom", TabbedContent).active = tab_id
        except Exception:
            pass

    def action_focus_worker(self, index: int) -> None:
        """Scroll the matching worker pane into view."""
        name = f"worker-{int(index)}"
        pane = self._panes.get(name)
        if pane is not None:
            try:
                pane.scroll_end(animate=False)
            except Exception:
                pass

    def action_next_task(self) -> None:
        """Switch the monitor to the next task in the store."""
        try:
            tasks = [str(task.get("task_id", "")) for task in TaskStore().list()]
        except Exception:
            return
        tasks = [task for task in tasks if task]
        if len(tasks) < 2:
            self._append_activity("only one task in the store", "yellow")
            return
        try:
            index = (tasks.index(self.task_id) + 1) % len(tasks)
        except ValueError:
            index = 0
        self.task_id = tasks[index]
        self._reset_view()
        self._append_activity(f"switched to task {self.task_id}", "green")
        self.title = f"lazy_view :: {self.task_id}"

    def _reset_view(self) -> None:
        """Drop tails, panes and caches so the next poll reloads cleanly."""
        self._seen_findings = set()
        self._ticks = 0
        for pane in self._panes.values():
            try:
                pane.clear()
            except Exception:
                pass
        for name, title in self._pane_titles.items():
            try:
                title.update(name)
            except Exception:
                pass
        for log in (
            getattr(self, "_activity", None),
            getattr(self, "_guard", None),
            getattr(self, "_traffic", None),
            getattr(self, "_findings", None),
        ):
            if log is not None:
                try:
                    log.clear()
                except Exception:
                    pass
        self._init_tails()
        self._render_stages(self._overview())


def _hint_via_graph(task_id: str, text: str) -> None:
    """Inject a hint without a live engine instance (attach mode)."""
    from modules.lazy_engine import ActivityLog, ExplorationGraph

    graph = ExplorationGraph(task_id)
    node = graph.add_node("hint", text)
    ActivityLog(task_id).emit("human", "hint", f"hint #{node.node_id}: {text[:200]}")


def run_monitor_command(task_id: str = "") -> dict:
    """Attach the monitor to an existing task (never blocks the loop).

    Args:
        task_id: Task to inspect (empty picks the newest task).

    Returns:
        App exit payload (unused by attach mode, kept for symmetry).
    """
    app = LazyMonitorApp(task_id=task_id)
    app.run()
    return dict(app.result or {})


def run_monitor_session(engine, config, params: dict | None = None) -> dict:
    """Run the loop inside the monitor (``lazy_loop --view``).

    Args:
        engine: Bound :class:`LazyEngine`.
        config: :class:`modules.lazy_runner.LoopRunConfig`.
        params: Payload mapping (kept for signature parity).

    Returns:
        Orchestrator summary produced by the embedded run.
    """
    if not config.task_id:
        created = engine.create_task(config.goal or f"engage {config.target or 'target'}")
        config.task_id = str(created.get("task_id", ""))
    app = LazyMonitorApp(task_id=config.task_id, engine=engine, config=config, params=params)
    app.run()
    result = dict(app.result or {})
    if not result:
        result = {"task_id": config.task_id, "status": "cancelled", "overview": {}}
    return result


__all__ = ["LazyMonitorApp", "run_monitor_command", "run_monitor_session"]
