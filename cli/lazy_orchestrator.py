"""Orchestrator admin console for the autonomous loop.

A Textual TUI in the spirit of the marketplace configurator:

- Now: what the loop is executing right now (task, stages, live activity
  tail, per-worker current command);
- Config: every payload knob the runner reads (rounds, workers,
  heartbeat, verb timeout, agentic flags, NOA, proxy);
- Verbs: auto-verb registry with a searchable command picker;
- Playbooks/Gyms/Chains/Profiles: YAML asset tabs managed by the ``OrchestratorAssetsMixin``; the Models and Guard rules live here.
- Models: the LLM failover chain (add/remove members);
- Guard: the intercept rules (add/remove).

Edits persist straight to ``payload.json`` (or a sandbox path in tests)
through ``core.config``; playbook changes are confined to the playbooks
directory and written atomically.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
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

from cli.orchestrator_assets_tabs import CONFIG_FIELDS, OrchestratorAssetsMixin
from cli.tui_forms import (
    ConfirmModal,
    FormModal,
    SearchSelectModal,
    YamlEditorModal,
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


def discover_shell_commands() -> list[str]:
    """Return every routable shell command name.

    The pre-built ``cli/command_index.json`` catalogue is authoritative
    when present. When it is stale or missing the source tree is scanned
    with the same ``do_*`` method convention cmd2 uses.

    Returns:
        Sorted unique command names without the ``do_`` prefix.
    """
    names: set[str] = set()
    try:
        from cli.palette import all_commands

        for row in all_commands():
            name = str(row.get("name", ""))
            if name.startswith("do_") and len(name) > 3:
                names.add(name[3:])
    except Exception:
        names.clear()
    if not names:
        root = Path(__file__).resolve().parent.parent
        sources = [root / "lazyown.py", *(root / "cli" / "commands").glob("*.py")]
        pattern = re.compile(r"^\s*def do_([A-Za-z][A-Za-z0-9_]*)\s*\(", re.MULTILINE)
        for source in sources:
            try:
                text = source.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            names.update(pattern.findall(text))
    return sorted(names)


def command_descriptions() -> dict[str, str]:
    """Return ``{command: summary}`` from the palette index when available."""
    try:
        from cli.palette import all_commands

        return {
            str(row["name"])[3:]: str(row.get("summary") or "")
            for row in all_commands()
            if str(row.get("name", "")).startswith("do_") and len(str(row["name"])) > 3
        }
    except Exception:
        return {}


def verb_candidates() -> list[tuple[str, str]]:
    """Return searchable ``(verb, description)`` pairs for the picker.

    Built-in and operator-defined auto verbs come first because they are
    the primary loop surface; every remaining shell command follows.
    """
    from modules.orchestrator_config import effective_verbs

    descriptions = command_descriptions()
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    try:
        entries = effective_verbs()
    except Exception:
        entries = []
    for entry in entries:
        name = str(entry.get("name", "")).strip()
        if not name or name in seen:
            continue
        source = "custom verb" if entry.get("source") == "custom" else "auto verb"
        detail = str(entry.get("description") or "").strip() or descriptions.get(name, "")
        pairs.append((name, f"[{source}] {detail}".strip()))
        seen.add(name)
    for name in discover_shell_commands():
        if name in seen:
            continue
        pairs.append((name, descriptions.get(name, "shell command")))
        seen.add(name)
    return pairs


class LazyOrchestratorApp(OrchestratorAssetsMixin, App[None]):
    """Admin console: Now / Config / Verbs / Chains / Models / Guard."""

    CSS = """
    #now-status { height: 6; border: round $accent; padding: 0 1; }
    #now-log { height: 1fr; border: round $primary; }
    #config-status { height: 3; color: $text-muted; }
    #chains-detail, #profiles-detail, #playbooks-detail, #gyms-detail { height: 10;
        border: round $secondary; padding: 0 1; }
    DataTable { height: 1fr; }
    .modal-box { width: 70; height: auto; padding: 1 2; background: $surface;
                 border: round $accent; }
    .modal-box-wide { width: 100; height: 38; padding: 1 2; background: $surface;
                      border: round $accent; }
    .modal-title { text-style: bold; padding-bottom: 1; }
    .modal-label { padding-top: 1; }
    .modal-hint { color: $text-muted; padding-top: 1; }
    .modal-error { color: $error; padding-top: 1; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("s", "save_config", "Save config"),
        Binding("space", "toggle_item", "Toggle"),
        Binding("a", "add_item", "Add"),
        Binding("e", "edit_item", "Edit"),
        Binding("d", "delete_item", "Delete"),
    ]

    def __init__(self, payload_path: str | Path | None = None, task_id: str = "") -> None:
        """Bind the console to a payload file and an optional task."""
        super().__init__()
        self._payload_path = Path(payload_path) if payload_path else None
        self._chains_dir_override: Path | None = None
        self._playbooks_dir_override: Path | None = None
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
            with TabPane("Triggers", id="tab-triggers"):
                with Vertical():
                    yield DataTable(id="triggers-table")
                    yield Static("seeded YAML triggers refresh the table", id="triggers-detail")
            with TabPane("Playbooks", id="tab-playbooks"):
                with Vertical():
                    yield DataTable(id="playbooks-table")
                    yield Static("select a playbook to preview it", id="playbooks-detail")
            with TabPane("Gyms", id="tab-gyms"):
                with Vertical():
                    yield DataTable(id="gyms-table")
                    yield Static("select a gym to preview its state", id="gyms-detail")
            with TabPane("Chains", id="tab-chains"):
                with Vertical():
                    yield DataTable(id="chains-table")
                    yield Static("select a chain to preview its steps", id="chains-detail")
            with TabPane("Profiles", id="tab-profiles"):
                with Vertical():
                    yield DataTable(id="profiles-table")
                    yield Static("select a profile to activate it", id="profiles-detail")
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
        self._refresh_triggers()
        self._refresh_playbooks()
        self._refresh_gyms()
        self._refresh_chains()
        self._refresh_profiles()
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
        """Flip one auto verb on/off and persist it in its owning layer."""
        from modules.orchestrator_config import upsert_verb, verb_enabled
        from modules.verb_catalog import catalog_enabled, catalog_source, set_enabled

        source = catalog_source(name)
        if source is not None:
            enabled = not bool(catalog_enabled(name))
            set_enabled(name, enabled)
            self._refresh_verbs()
            return enabled
        enabled = not verb_enabled(name)
        upsert_verb(name, enabled=enabled)
        self._refresh_verbs()
        return enabled

    def add_auto_verb(
        self,
        name: str,
        keywords: str = "",
        needs_target: str = "true",
        description: str = "",
        phases: str = "",
    ) -> dict:
        """Register a new operator-defined auto verb."""
        from modules.orchestrator_config import upsert_verb

        entry = upsert_verb(
            name,
            enabled=True,
            keywords=[word.strip() for word in str(keywords).split(",") if word.strip()],
            phases=[phase.strip() for phase in str(phases).split(",") if phase.strip()],
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
        self._refresh_triggers()
        self._refresh_playbooks()
        self._refresh_gyms()
        self._refresh_chains()
        self._refresh_profiles()
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
        """Toggle the selected stage, auto verb, or chain."""
        tab = self._active_tab()
        if tab == "tab-pipeline":
            name = self._selected_row("stages-table")
            if name:
                self.toggle_stage(name)
        elif tab == "tab-verbs":
            name = self._selected_row("verbs-table")
            if name:
                self.toggle_verb(name)
        elif tab == "tab-triggers":
            try:
                trigger_id = int(self._selected_row("triggers-table"))
            except ValueError:
                return
            self.toggle_trigger(trigger_id)
        elif tab == "tab-chains":
            name = self._selected_row("chains-table")
            if name:
                self.toggle_chain(name)
        elif tab == "tab-gyms":
            name = self._selected_row("gyms-table")
            if name:
                self.toggle_gym(name)
        elif tab == "tab-profiles":
            name = self._selected_row("profiles-table")
            if name:
                self.activate_profile(name)

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
        if tab == "tab-triggers":

            def _picked_kind(value: str | None) -> None:
                if not value:
                    return

                def _done_trigger(values: dict | None) -> None:
                    if values is None:
                        return
                    self.add_trigger(value, values.get("every_sec", "0"), values.get("arg", ""))

                defaults = {"every_sec": "0", "arg": ""}
                self.push_screen(
                    FormModal(
                        f"Configure trigger {value}",
                        [("every_sec", "Interval seconds (0 = event)", "0"), ("arg", "Argument", "")],
                        defaults=defaults,
                    ),
                    _done_trigger,
                )

            self.push_screen(
                SearchSelectModal(
                    "Add trigger - choose a kind",
                    self.trigger_kind_options(),
                    placeholder="search trigger kind",
                ),
                _picked_kind,
            )
        elif tab == "tab-models":

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

            def _picked(value: str | None) -> None:
                if not value:
                    return

                def _done_verb(values: dict | None) -> None:
                    if values and values.get("verb"):
                        self.add_auto_verb(
                            values["verb"],
                            values.get("keywords", ""),
                            values.get("needs_target", "true"),
                            values.get("description", ""),
                            values.get("phases", ""),
                        )

                defaults = {
                    "verb": value,
                    "keywords": value.replace("_", " "),
                    "needs_target": "true",
                    "phases": "",
                    "description": "",
                }
                self.push_screen(
                    FormModal(
                        f"Configure verb {value}",
                        [
                            ("verb", "Shell command name", "myscan"),
                            ("keywords", "Comma-separated keywords", "myscan, custom scan"),
                            ("phases", "Comma-separated kill-chain phases", "recon, exploit"),
                            ("needs_target", "Carries target (true|false)", "true"),
                            ("description", "Description", "operator-defined verb"),
                        ],
                        defaults=defaults,
                    ),
                    _done_verb,
                )

            self.push_screen(
                SearchSelectModal(
                    "Add auto verb - choose a command or verb",
                    verb_candidates(),
                    placeholder="search command or auto verb",
                ),
                _picked,
            )
        elif tab == "tab-playbooks":

            def _done_new(values: dict | None) -> None:
                if not (values and values.get("filename")):
                    return
                try:
                    self.create_playbook_file(
                        values["filename"],
                        values.get("name", ""),
                        values.get("description", ""),
                        values.get("platforms", "linux"),
                    )
                except (FileExistsError, ValueError) as exc:
                    self.notify(f"playbook not created: {exc}", severity="error")

            self.push_screen(
                FormModal(
                    "New playbook",
                    [
                        ("filename", "File name (e.g. apt_demo)", "apt_demo"),
                        ("name", "APT name", "Demo APT"),
                        ("description", "Description", "adversary emulation plan"),
                        ("platforms", "Comma-separated platforms", "linux, windows"),
                    ],
                    defaults={"platforms": "linux"},
                ),
                _done_new,
            )
        elif tab == "tab-gyms":

            def _done_new_gym(values: dict | None) -> None:
                if not (values and values.get("id")):
                    return
                from modules.redteam_gym import create_gym

                phases = [part.strip() for part in str(values.get("phases", "")).split(",") if part.strip()]
                try:
                    result = create_gym(
                        values["id"],
                        name=values.get("name", ""),
                        scenario=values.get("scenario", "metasploitable"),
                        objective=values.get("objective", ""),
                        description=values.get("description", ""),
                        difficulty=values.get("difficulty", "easy"),
                        chain=values.get("chain", ""),
                        phases=phases or None,
                        max_points=int(values.get("max_points", "1000") or 1000),
                        elo_bonus=int(values.get("elo_bonus", "100") or 100),
                    )
                except ValueError as exc:
                    self.notify(f"gym not created: {exc}", severity="error")
                    return
                if not result.get("success"):
                    self.notify(f"gym not created: {result.get('error', '')}", severity="error")
                    return
                self._refresh_gyms()

            self.push_screen(
                FormModal(
                    "New gym definition",
                    [
                        ("id", "Gym ID (file stem)", "my_gym"),
                        ("name", "Display name", "My Gym"),
                        ("scenario", "Lab scenario or range", "metasploitable"),
                        ("objective", "Objective", "Root the target"),
                        ("difficulty", "Difficulty (easy|medium|hard)", "easy"),
                        ("chain", "Optional APT chain", ""),
                        ("phases", "Comma-separated phases", "enum, exploit"),
                        ("max_points", "Max points", "1000"),
                        ("elo_bonus", "ELO bonus", "100"),
                    ],
                    defaults={"difficulty": "easy", "phases": "enum, exploit"},
                ),
                _done_new_gym,
            )
        elif tab == "tab-chains":

            def _done_chain(playbook: str | None) -> None:
                if playbook:
                    self.generate_chain(playbook)

            self.push_screen(
                SearchSelectModal(
                    "Generate chain from playbook",
                    self.playbook_candidates(),
                    placeholder="search playbook engine key",
                ),
                _done_chain,
            )

    def action_edit_item(self) -> None:
        """Edit the selected playbook YAML or LLM member priority."""
        tab = self._active_tab()
        if tab == "tab-playbooks":
            filename = self._selected_row("playbooks-table")
            if filename:
                self._edit_playbook(filename)
            return
        if tab == "tab-gyms":
            gym_id = self._selected_row("gyms-table")
            if gym_id:
                self._edit_gym(gym_id)
            return
        if tab != "tab-models":
            return
        try:
            table = self.query_one("#models-table", DataTable)
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            name = str(row_key.value or "")
        except Exception:
            return
        if not name:
            return

        def _done(values: dict | None) -> None:
            if values and values.get("priority") is not None:
                self.set_model_priority(name, values.get("priority", "0"))

        current = ""
        try:
            from modules.lazy_engine import LlmPool

            for member in LlmPool().members():
                if str(member.get("name", "")) == name:
                    current = str(member.get("priority", 0))
        except Exception:
            pass
        self.push_screen(
            FormModal(
                f"Priority for {name}",
                [("priority", "Priority (higher runs first)", current or "0")],
            ),
            _done,
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
        elif tab == "tab-playbooks":
            filename = self._selected_row("playbooks-table")
            if not filename:
                return

            def _confirmed(answer: bool | None) -> None:
                if answer:
                    self.delete_playbook_file(filename)

            self.push_screen(
                ConfirmModal(f"Delete {filename}?", "The YAML file is removed from playbooks/."),
                _confirmed,
            )
        elif tab == "tab-gyms":
            gym_id = self._selected_row("gyms-table")
            if not gym_id:
                return

            def _confirmed_gym(answer: bool | None) -> None:
                if not answer:
                    return
                from modules.redteam_gym import delete_gym

                result = delete_gym(gym_id)
                if not result.get("success"):
                    self.notify(f"gym not deleted: {result.get('error', '')}", severity="error")
                    return
                self._refresh_gyms()

            self.push_screen(
                ConfirmModal(f"Delete gym {gym_id}?", "The YAML definition is removed from gyms/."),
                _confirmed_gym,
            )
        elif tab == "tab-chains":
            name = self._selected_row("chains-table")
            if name:
                self.remove_chain(name)
        elif tab == "tab-triggers":
            try:
                trigger_id = int(self._selected_row("triggers-table"))
            except ValueError:
                return

            def _confirmed_trigger(answer: bool | None) -> None:
                if answer:
                    self.remove_trigger(trigger_id)

            self.push_screen(
                ConfirmModal(f"Delete trigger {trigger_id}?", "The store row (and any YAML seed) stays for next sync."),
                _confirmed_trigger,
            )


def run_orchestrator_console(task_id: str = "") -> None:
    """Launch the admin console (attach mode)."""
    app = LazyOrchestratorApp(task_id=task_id)
    app.run()


__all__ = ["LazyOrchestratorApp", "FormModal", "run_orchestrator_console"]
