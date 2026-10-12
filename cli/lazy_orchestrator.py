"""Orchestrator admin console for the autonomous loop.

A Textual TUI in the spirit of the marketplace configurator:

- Now: what the loop is executing right now (task, stages, live activity
  tail, per-worker current command);
- Config: every payload knob the runner reads (rounds, workers,
  heartbeat, verb timeout, agentic flags, NOA, proxy);
- Models: the LLM failover chain (add/remove members);
- Guard: the intercept rules (add/remove).

Edits persist straight to ``payload.json`` (or a sandbox path in tests)
through ``core.config``; nothing else mutates global state.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from modules.jsonl_tail import JsonlTail

POLL_SEC = 0.5
NOW_LINES = 400
STAGE_LABELS = (
    ("lazy_scope", "scope"),
    ("lazy_asset", "assets"),
    ("lazy_enrich", "enrich"),
    ("lazy_planner", "plan"),
    ("lazy_frontier", "queue"),
    ("lazy_worker", "work"),
    ("lazy_guard", "guard"),
    ("lazy_traffic", "traffic"),
    ("lazy_finding", "find"),
    ("lazy_retest", "retest"),
    ("lazy_compact", "compact"),
    ("lazy_trace", "trace"),
)


@dataclass(frozen=True)
class ConfigField:
    """One editable payload knob."""

    key: str
    label: str
    placeholder: str = ""
    kind: str = "text"


CONFIG_FIELDS = (
    ConfigField("plan_heartbeat_seconds", "Heartbeat seconds", "600"),
    ConfigField("verb_timeout", "Verb timeout seconds", "300"),
    ConfigField("agent_tool_calling", "Agentic tool calling", "true"),
    ConfigField("agent_max_iterations", "Agent max iterations", "6"),
    ConfigField("noa_compaction", "NOA raw archiving", "false"),
    ConfigField("max_concurrent", "Max concurrent tasks", "0"),
    ConfigField("proxy_autostart", "Recorder proxy autostart", "true"),
    ConfigField("proxy_port", "Recorder proxy port", "8080"),
    ConfigField("agent_backend", "Main agent backend", "native"),
)


class FormModal(ModalScreen[dict]):
    """Generic key/value modal used for models and guard rules."""

    BINDINGS = [("escape", "dismiss(None)", "cancel")]

    def __init__(self, title: str, fields: list[tuple[str, str, str]]) -> None:
        """Store the title and (id, label, placeholder) field specs."""
        super().__init__()
        self._title = title
        self._fields = fields

    def compose(self) -> ComposeResult:
        """One labeled input per field plus a save button."""
        with Vertical(classes="modal-box"):
            yield Static(self._title, classes="modal-title")
            for field_id, label, placeholder in self._fields:
                yield Static(label, classes="modal-label")
                yield Input(placeholder=placeholder, id=field_id)
            yield Button("Save", id="modal-save", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Collect the values and close the modal."""
        if event.button.id != "modal-save":
            return
        values = {
            field_id: str(self.query_one(f"#{field_id}", Input).value).strip() for field_id, _label, _p in self._fields
        }
        self.dismiss(values)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter commits the form like the save button."""
        values = {
            field_id: str(self.query_one(f"#{field_id}", Input).value).strip() for field_id, _label, _p in self._fields
        }
        self.dismiss(values)


class LazyOrchestratorApp(App[None]):
    """Admin console: Now / Config / Models / Guard."""

    CSS = """
    #now-status { height: 6; border: round $accent; padding: 0 1; }
    #now-log { height: 1fr; border: round $primary; }
    #config-status { height: 3; color: $text-muted; }
    DataTable { height: 1fr; }
    .modal-box { width: 70; height: auto; padding: 1 2; background: $surface;
                 border: round $accent; }
    .modal-title { text-style: bold; padding-bottom: 1; }
    .modal-label { padding-top: 1; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("s", "save_config", "Save config"),
        Binding("space", "toggle_item", "Toggle"),
        Binding("a", "add_item", "Add"),
        Binding("d", "delete_item", "Delete"),
    ]

    def __init__(self, payload_path: str | Path | None = None, task_id: str = "") -> None:
        """Bind the console to a payload file and an optional task."""
        super().__init__()
        self._payload_path = Path(payload_path) if payload_path else None
        self.task_id = task_id
        self._tail: JsonlTail | None = None
        self._tail_task = ""
        self._now_lines: list[str] = []
        self._worker_command: dict[str, str] = {}

    def compose(self) -> ComposeResult:
        """Build the four panes."""
        yield Header(show_clock=True)
        with TabbedContent(id="tabs"):
            with TabPane("Now", id="tab-now"):
                with Vertical():
                    yield Static("waiting for a task...", id="now-status")
                    yield RichLog(markup=False, highlight=False, max_lines=NOW_LINES, id="now-log")
            with TabPane("Config", id="tab-config"):
                with VerticalScroll():
                    for spec in CONFIG_FIELDS:
                        yield Static(spec.label, classes="modal-label")
                        yield Input(placeholder=spec.placeholder, id=f"cfg-{spec.key}")
                    yield Button("Save config", id="config-save", variant="primary")
                    yield Static("", id="config-status")
            with TabPane("Pipeline", id="tab-pipeline"):
                yield DataTable(id="stages-table")
            with TabPane("Verbs", id="tab-verbs"):
                yield DataTable(id="verbs-table")
            with TabPane("Models", id="tab-models"):
                yield DataTable(id="models-table")
            with TabPane("Guard", id="tab-guard"):
                yield DataTable(id="guard-table")
        yield Footer()

    def on_mount(self) -> None:
        """Load the payload into the form and refresh the data tables."""
        self.title = "lazy_orchestrator"
        self._load_payload_into_form()
        self._refresh_stages()
        self._refresh_verbs()
        self._refresh_models()
        self._refresh_guard()
        self.set_interval(POLL_SEC, self._poll_now)

    def toggle_stage(self, name: str) -> bool:
        """Flip one pipeline stage on/off and persist it."""
        from modules.orchestrator_config import set_stage, stage_enabled

        enabled = not stage_enabled(name)
        set_stage(name, enabled)
        self._refresh_stages()
        return enabled

    def toggle_verb(self, name: str) -> bool:
        """Flip one auto verb on/off and persist it."""
        from modules.orchestrator_config import upsert_verb, verb_enabled

        enabled = not verb_enabled(name)
        upsert_verb(name, enabled=enabled)
        self._refresh_verbs()
        return enabled

    def add_auto_verb(self, name: str, keywords: str = "", needs_target: str = "true", description: str = "") -> dict:
        """Register a new operator-defined auto verb."""
        from modules.orchestrator_config import upsert_verb

        entry = upsert_verb(
            name,
            enabled=True,
            keywords=[word.strip() for word in str(keywords).split(",") if word.strip()],
            needs_target=str(needs_target).strip().lower() not in ("false", "no", "0", "off"),
            description=description or f"operator-defined verb {name}",
            custom=True,
        )
        self._refresh_verbs()
        return entry

    def remove_auto_verb(self, name: str) -> bool:
        """Delete a custom verb, or disable a built-in one."""
        from modules.orchestrator_config import remove_verb

        removed = remove_verb(name)
        self._refresh_verbs()
        return bool(removed)

    def _refresh_stages(self) -> None:
        """Render the pipeline stages with their firing condition."""
        try:
            table = self.query_one("#stages-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("stage", "enabled", "fires when", "detail")
        try:
            from modules.orchestrator_config import stages

            for name, stage in stages().items():
                table.add_row(name, "on" if stage["enabled"] else "off", stage["fires_when"], stage["label"], key=name)
        except Exception:
            return

    def _refresh_verbs(self) -> None:
        """Render the auto verbs with source, state and keywords."""
        try:
            table = self.query_one("#verbs-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("verb", "enabled", "target", "keywords", "source", "description")
        try:
            from modules.orchestrator_config import effective_verbs

            for entry in effective_verbs():
                table.add_row(
                    entry["name"],
                    "on" if entry["enabled"] else "off",
                    "yes" if entry["needs_target"] else "no",
                    ",".join(entry["keywords"][:4]),
                    entry["source"],
                    entry["description"][:60],
                    key=entry["name"],
                )
        except Exception:
            return

    def _load_payload(self) -> dict:
        """Load the payload mapping (empty on failure)."""
        try:
            from core.config import load_payload

            payload = load_payload(self._payload_path) if self._payload_path else load_payload()
        except Exception:
            return {}
        return dict(payload or {})

    def _load_payload_into_form(self) -> None:
        """Fill the config inputs with the current payload values."""
        payload = self._load_payload()
        for spec in CONFIG_FIELDS:
            value = payload.get(spec.key, "")
            try:
                widget = self.query_one(f"#cfg-{spec.key}", Input)
                widget.value = "" if value is None else str(value)
            except Exception:
                continue

    def save_config(self, values: dict) -> dict:
        """Merge the given keys into the payload and persist it.

        Args:
            values: Mapping of payload keys to new values (strings).

        Returns:
            The updated payload mapping.
        """
        from core.config import save_payload

        payload = self._load_payload()
        for key, raw in values.items():
            if raw == "":
                continue
            payload[key] = _coerce(raw)
        if self._payload_path:
            save_payload(payload, self._payload_path)
        else:
            save_payload(payload)
        return payload

    def add_model_member(self, name: str, model: str, priority: str = "0") -> str:
        """Append one LLM chain member; returns the stored name."""
        from modules.lazy_engine import LlmPool

        member = LlmPool().add_member(name, model, int(_coerce(priority or 0)))
        self._refresh_models()
        return str(member.get("name", name))

    def remove_model_member(self, name: str) -> bool:
        """Drop one LLM chain member by name."""
        from modules.lazy_engine import LlmPool

        removed = LlmPool().remove_member(name)
        self._refresh_models()
        return bool(removed)

    def add_guard_rule(self, pattern: str, action: str = "ask", reason: str = "") -> bool:
        """Register one guard intercept rule."""
        from modules.lazy_engine import Guard

        Guard().add_rule(pattern, action.lower() or "ask", reason or pattern)
        self._refresh_guard()
        return True

    def remove_guard_rule(self, pattern: str) -> bool:
        """Delete one guard rule by exact pattern."""
        from modules.lazy_engine import Guard

        removed = Guard().remove_rule(pattern)
        self._refresh_guard()
        return bool(removed)

    def _refresh_models(self) -> None:
        """Render the LLM chain into the models table."""
        try:
            table = self.query_one("#models-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("name", "model", "priority")
        try:
            from modules.lazy_engine import LlmPool

            for member in LlmPool().members():
                table.add_row(
                    str(member.get("name", "")),
                    str(member.get("model", "")),
                    str(member.get("priority", 0)),
                    key=str(member.get("name", "")),
                )
        except Exception:
            return

    def _refresh_guard(self) -> None:
        """Render the guard rules into the guard table."""
        try:
            table = self.query_one("#guard-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("pattern", "action", "priority", "reason")
        try:
            from modules.lazy_engine import Guard

            for rule in Guard().rules:
                table.add_row(
                    str(rule.get("pattern", "")),
                    str(rule.get("action", "")),
                    str(rule.get("priority", 0)),
                    str(rule.get("reason", ""))[:60],
                    key=str(rule.get("pattern", "")),
                )
        except Exception:
            return

    def _resolve_task(self) -> str:
        """Pick the requested task or the newest running/running-ish one."""
        if self.task_id:
            return self.task_id
        try:
            from modules.lazy_engine import TaskStore

            tasks = TaskStore().list()
        except Exception:
            return ""
        for record in reversed(tasks):
            if str(record.get("status", "")) in ("running", "queued", "paused"):
                self.task_id = str(record.get("task_id", ""))
                return self.task_id
        if tasks:
            self.task_id = str(tasks[-1].get("task_id", ""))
        return self.task_id

    def _poll_now(self) -> None:
        """Tail the active task's activity into the Now pane."""
        import modules.lazy_loop as _loop

        task_id = self._resolve_task()
        if not task_id:
            return
        if self._tail is None or self._tail_task != task_id:
            self._tail_task = task_id
            self._tail = JsonlTail(_loop._store_path(f"activity_{task_id}.jsonl"))
            self._worker_command = {}
        records = self._tail.read_new(limit=50) if self._tail else []
        try:
            log = self.query_one("#now-log", RichLog)
        except Exception:
            return
        for record in records:
            kind = str(record.get("kind", "event"))
            worker = str(record.get("worker", "engine"))
            text = " ".join(str(record.get("text", "")).split())[:200]
            line = f"[{kind}] {worker}: {text}"
            log.write(Text(line))
            self._now_lines.append(line)
            if kind == "tool":
                self._worker_command[worker] = text
            elif kind in ("finish", "settle"):
                self._worker_command.pop(worker, None)
        try:
            status = self.query_one("#now-status", Static)
        except Exception:
            return
        latest = self._now_lines[-1] if self._now_lines else "no activity yet"
        workers = ", ".join(f"{name}={cmd[:40]}" for name, cmd in list(self._worker_command.items())[:4]) or "idle"
        status.update(Text(f"task {task_id}  lines={len(self._now_lines)}\nworkers: {workers}\nlast: {latest[:160]}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the config save button."""
        if event.button.id != "config-save":
            return
        values = {}
        for spec in CONFIG_FIELDS:
            try:
                values[spec.key] = str(self.query_one(f"#cfg-{spec.key}", Input).value).strip()
            except Exception:
                continue
        self.save_config(values)
        try:
            self.query_one("#config-status", Static).update(
                Text(f"saved {len([v for v in values.values() if v])} key(s) to payload")
            )
        except Exception:
            pass

    def action_refresh(self) -> None:
        """Reload tables and form from disk."""
        self._refresh_stages()
        self._refresh_verbs()
        self._refresh_models()
        self._refresh_guard()
        self._load_payload_into_form()

    def _selected_row(self, table_id: str) -> str:
        """Return the row key of the selected row, or empty string."""
        try:
            table = self.query_one(f"#{table_id}", DataTable)
            key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            return str(key.value or "")
        except Exception:
            return ""

    def action_toggle_item(self) -> None:
        """Toggle the selected stage or auto verb."""
        tab = self._active_tab()
        if tab == "tab-pipeline":
            name = self._selected_row("stages-table")
            if name:
                self.toggle_stage(name)
        elif tab == "tab-verbs":
            name = self._selected_row("verbs-table")
            if name:
                self.toggle_verb(name)

    def action_save_config(self) -> None:
        """Save the form values (keyboard shortcut)."""
        values = {}
        for spec in CONFIG_FIELDS:
            try:
                values[spec.key] = str(self.query_one(f"#cfg-{spec.key}", Input).value).strip()
            except Exception:
                continue
        self.save_config(values)

    def _active_tab(self) -> str:
        """Return the active tab id."""
        try:
            return str(self.query_one("#tabs", TabbedContent).active)
        except Exception:
            return ""

    def action_add_item(self) -> None:
        """Open the add modal for the active tab."""
        tab = self._active_tab()
        if tab == "tab-models":

            def _done(values: dict | None) -> None:
                if values and values.get("name"):
                    self.add_model_member(values["name"], values.get("model", ""), values.get("priority", "0"))

            self.push_screen(
                FormModal(
                    "Add LLM member",
                    [
                        ("name", "Name", "groq-cloud"),
                        ("model", "Model", "groq:llama-3.3-70b-versatile"),
                        ("priority", "Priority", "5"),
                    ],
                ),
                _done,
            )
        elif tab == "tab-guard":

            def _done_rule(values: dict | None) -> None:
                if values and values.get("pattern"):
                    self.add_guard_rule(values["pattern"], values.get("action", "ask"), values.get("reason", ""))

            self.push_screen(
                FormModal(
                    "Add guard rule",
                    [
                        ("pattern", "Regex pattern", r"curl.*\|\s*(sh|bash)"),
                        ("action", "Action (allow|ask|deny)", "ask"),
                        ("reason", "Reason", "remote pipe"),
                    ],
                ),
                _done_rule,
            )
        elif tab == "tab-verbs":

            def _done_verb(values: dict | None) -> None:
                if values and values.get("verb"):
                    self.add_auto_verb(
                        values["verb"],
                        values.get("keywords", ""),
                        values.get("needs_target", "true"),
                        values.get("description", ""),
                    )

            self.push_screen(
                FormModal(
                    "Add auto verb",
                    [
                        ("verb", "Shell command name", "myscan"),
                        ("keywords", "Comma-separated keywords", "myscan, custom scan"),
                        ("needs_target", "Carries target (true|false)", "true"),
                        ("description", "Description", "operator-defined verb"),
                    ],
                ),
                _done_verb,
            )

    def action_delete_item(self) -> None:
        """Delete the selected row in the active tab."""
        tab = self._active_tab()
        if tab == "tab-models":
            try:
                table = self.query_one("#models-table", DataTable)
                row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
                if row_key.value:
                    self.remove_model_member(str(row_key.value))
            except Exception:
                return
        elif tab == "tab-guard":
            try:
                table = self.query_one("#guard-table", DataTable)
                row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
                if row_key.value:
                    self.remove_guard_rule(str(row_key.value))
            except Exception:
                return
        elif tab == "tab-verbs":
            name = self._selected_row("verbs-table")
            if name:
                self.remove_auto_verb(name)


def _coerce(raw) -> object:
    """Coerce a form string into bool/int when it clearly is one."""
    text = str(raw).strip().lower()
    if text in ("true", "yes", "on"):
        return True
    if text in ("false", "no", "off"):
        return False
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return raw


def run_orchestrator_console(task_id: str = "") -> None:
    """Launch the admin console (attach mode)."""
    app = LazyOrchestratorApp(task_id=task_id)
    app.run()


__all__ = ["LazyOrchestratorApp", "FormModal", "run_orchestrator_console"]
