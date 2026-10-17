"""Orchestrator admin console for the autonomous loop.

A Textual TUI in the spirit of the marketplace configurator:

- Now: what the loop is executing right now (task, stages, live activity
  tail, per-worker current command);
- Config: every payload knob the runner reads (rounds, workers,
  heartbeat, verb timeout, agentic flags, NOA, proxy);
- Verbs: auto-verb registry with a searchable command picker;
- Playbooks: full CRUD over the YAML playbooks under ``playbooks/``;
- Gyms: YAML gym catalogue with persistent runs from the world model;
- Chains: APT chain YAML administration;
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


class LazyOrchestratorApp(App[None]):
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
        """Flip one auto verb on/off and persist it."""
        from modules.orchestrator_config import upsert_verb, verb_enabled

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

    def _playbooks_dir(self) -> Path:
        """Playbook file root (overrideable for sandboxed tests)."""
        if self._playbooks_dir_override is not None:
            return self._playbooks_dir_override
        from modules.playbook_admin import PLAYBOOKS_DIR

        return PLAYBOOKS_DIR

    def playbook_rows(self) -> list[dict]:
        """Return one row per playbook file, including invalid ones."""
        from modules.playbook_admin import scan_playbooks

        try:
            entries = scan_playbooks(self._playbooks_dir())
        except Exception:
            return []
        return [
            {
                "file": entry.file,
                "path": entry.path,
                "name": entry.name,
                "kind": entry.kind,
                "steps": entry.steps,
                "phases": entry.phases,
                "platforms": ",".join(entry.platforms),
                "description": entry.description,
                "valid": entry.valid,
                "error": entry.error,
            }
            for entry in entries
        ]

    def playbook_preview(self, filename: str, limit: int = 18) -> str:
        """Return a bounded YAML preview for one playbook file."""
        from modules.playbook_admin import preview_playbook

        row = next((item for item in self.playbook_rows() if item["file"] == filename), None)
        if row is None:
            return "playbook not found"
        return preview_playbook(row["path"], limit=limit)

    def create_playbook_file(
        self,
        filename: str,
        name: str = "",
        description: str = "",
        platforms: str = "linux",
    ) -> str:
        """Create one playbook YAML and repaint the table."""
        from modules.playbook_admin import create_playbook

        platform_list = [part.strip() for part in str(platforms).split(",") if part.strip()]
        path = create_playbook(
            filename,
            name=name,
            description=description,
            platforms=platform_list or ["linux"],
            directory=self._playbooks_dir(),
        )
        self._refresh_playbooks()
        return str(path)

    def save_playbook_text(self, filename: str, text: str) -> bool:
        """Validate and persist raw YAML edited by the operator."""
        from modules.playbook_admin import save_playbook_yaml

        try:
            save_playbook_yaml(filename, text, directory=self._playbooks_dir())
        except (OSError, ValueError) as exc:
            self.notify(f"playbook not saved: {exc}", severity="error")
            return False
        self._refresh_playbooks()
        return True

    def delete_playbook_file(self, filename: str) -> bool:
        """Delete one playbook YAML after the operator confirms."""
        from modules.playbook_admin import delete_playbook

        removed = delete_playbook(filename, directory=self._playbooks_dir())
        self._refresh_playbooks()
        return bool(removed)

    def playbook_candidates(self) -> list[tuple[str, str]]:
        """Return ``(engine_key, summary)`` pairs for chain generation."""
        from modules.apt_playbooks import AptPlaybookEngine

        try:
            engine = AptPlaybookEngine(playbook_dir=str(self._playbooks_dir()))
            entries = engine.list_playbooks()
        except Exception:
            return []
        return [
            (
                str(entry.get("apt_name", "")).lower().replace(" ", "_"),
                f"{entry.get('phases', 0)} phases, {entry.get('atomic_tests', 0)} tests",
            )
            for entry in entries
            if entry.get("apt_name")
        ]

    def _refresh_playbooks(self) -> None:
        """Render the playbook table with per-file state."""
        try:
            table = self.query_one("#playbooks-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("file", "name", "kind", "steps", "phases", "platforms", "status")
        for row in self.playbook_rows():
            state = "ok" if row["valid"] else f"invalid ({row['error'][:40]})"
            table.add_row(
                row["file"],
                row["name"],
                row["kind"],
                str(row["steps"]),
                str(row["phases"]),
                row["platforms"],
                state,
                key=row["file"],
            )
        self._update_playbooks_detail(self._selected_row("playbooks-table"))

    def _update_playbooks_detail(self, filename: str) -> None:
        """Show the selected playbook YAML in the detail pane."""
        try:
            panel = self.query_one("#playbooks-detail", Static)
        except Exception:
            return
        if not filename:
            panel.update("select a playbook to preview it")
            return
        row = next((item for item in self.playbook_rows() if item["file"] == filename), None)
        header = f"{filename}  [{row['kind']}]  {row['steps']} step(s)" if row else filename
        panel.update(Text(f"{header}\n{self.playbook_preview(filename)}"))

    def _edit_playbook(self, filename: str) -> None:
        """Open the raw YAML editor for one playbook file."""
        from modules.playbook_admin import validate_playbook

        row = next((item for item in self.playbook_rows() if item["file"] == filename), None)
        if row is None:
            return
        try:
            text = Path(row["path"]).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            self.notify(f"playbook unreadable: {exc}", severity="error")
            return

        def _validate(raw: str) -> None:
            import yaml as _yaml

            try:
                data = _yaml.safe_load(raw)
            except Exception as exc:
                raise ValueError(f"invalid YAML: {exc}") from exc
            errors = validate_playbook(data)
            if errors:
                raise ValueError("; ".join(errors))

        def _saved(raw: str | None) -> None:
            if raw is not None:
                self.save_playbook_text(filename, raw)

        self.push_screen(YamlEditorModal(f"Edit {filename}", text, validator=_validate), _saved)

    def gym_rows(self) -> list[dict]:
        """Return one row per gym definition with its active-run count."""
        from modules.gym_registry import scan_definitions
        from modules.redteam_gym import get_active_challenges

        try:
            definitions = scan_definitions()
            active = get_active_challenges()
        except Exception:
            return []
        by_gym: dict[str, list[dict]] = {}
        for run in active:
            by_gym.setdefault(str(run.get("challenge_id", "")), []).append(run)
        rows: list[dict] = []
        for entry in definitions:
            gym_id = str(entry.get("id", ""))
            runs = by_gym.get(gym_id, [])
            rows.append(
                {
                    "id": gym_id,
                    "file": entry.get("file", ""),
                    "path": entry.get("path", ""),
                    "name": entry.get("name", gym_id),
                    "difficulty": entry.get("difficulty", ""),
                    "scenario": entry.get("scenario", ""),
                    "chain": entry.get("chain", ""),
                    "max_points": entry.get("max_points", 0),
                    "phases": entry.get("phases", []),
                    "objective": entry.get("objective", ""),
                    "valid": entry.get("valid", True),
                    "error": entry.get("error", ""),
                    "runs": runs,
                    "active": len(runs),
                }
            )
        return rows

    def gym_preview(self, gym_id: str, limit: int = 16) -> str:
        """Return a bounded YAML preview for one gym definition."""
        from modules.gym_registry import definition_path

        try:
            path = definition_path(gym_id)
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except (OSError, ValueError) as exc:
            return f"unreadable: {exc}"
        shown = lines[: max(0, limit)]
        if len(lines) > len(shown):
            shown.append(f"... +{len(lines) - len(shown)} more line(s)")
        return "\n".join(shown)

    def _refresh_gyms(self) -> None:
        """Render the gym catalogue and its persistent active runs."""
        try:
            table = self.query_one("#gyms-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("gym", "name", "difficulty", "scenario", "active", "max points", "status")
        for row in self.gym_rows():
            state = "ok" if row["valid"] else f"invalid ({row['error'][:36]})"
            table.add_row(
                row["id"],
                row["name"],
                row["difficulty"],
                row["scenario"],
                str(row["active"]),
                str(row["max_points"]),
                state,
                key=row["id"],
            )
        self._update_gyms_detail(self._selected_row("gyms-table"))

    def _update_gyms_detail(self, gym_id: str) -> None:
        """Show definition metadata and every active run for one gym."""
        try:
            panel = self.query_one("#gyms-detail", Static)
        except Exception:
            return
        if not gym_id:
            panel.update("select a gym to preview its state")
            return
        row = next((item for item in self.gym_rows() if item["id"] == gym_id), None)
        if row is None:
            panel.update("gym not found")
            return
        lines = [
            f"{row['id']}  [{row['difficulty']}]  scenario={row['scenario']}  max={row['max_points']}",
            f"objective: {row['objective']}",
            f"phases: {', '.join(row['phases'])}  chain: {row['chain'] or '-'}",
        ]
        if row["active"]:
            lines.append(f"active runs ({row['active']}):")
            for run in row["runs"]:
                lines.append(
                    f"  {run.get('run_id', '')}  operator={run.get('operator', '')}  "
                    f"elapsed={run.get('elapsed_seconds', 0)}s  target={run.get('target', '') or '-'}"
                )
        else:
            lines.append("active runs: none (space starts this gym)")
        if not row["valid"]:
            lines.append(f"invalid: {row['error']}")
        lines.extend(["---", self.gym_preview(gym_id)])
        panel.update("\n".join(lines))

    def start_gym(self, gym_id: str, target: str = "") -> dict:
        """Start one gym and repaint the table."""
        from modules.redteam_gym import start_challenge

        result = start_challenge(gym_id, target=target)
        self._refresh_gyms()
        return result

    def stop_gym(self, selector: str = "") -> dict:
        """Stop one gym (or every gym when selector is empty) and repaint."""
        from modules.redteam_gym import stop_challenges

        result = stop_challenges(selector)
        self._refresh_gyms()
        return result

    def toggle_gym(self, gym_id: str) -> dict:
        """Start the selected gym, or stop its active runs when already active."""
        runs = [run for run in self.gym_rows() if run["id"] == gym_id]
        if runs and runs[0]["active"]:
            return self.stop_gym(gym_id)
        target = str(self._load_payload().get("rhost", "") or "")
        return self.start_gym(gym_id, target=target)

    def _edit_gym(self, gym_id: str) -> None:
        """Open the raw YAML editor for one gym definition."""
        from modules.gym_registry import definition_path, validate_definition

        try:
            text = definition_path(gym_id).read_text(encoding="utf-8", errors="replace")
        except (OSError, ValueError) as exc:
            self.notify(f"gym unreadable: {exc}", severity="error")
            return

        def _validate(raw: str) -> None:
            import yaml as _yaml

            try:
                data = _yaml.safe_load(raw)
            except Exception as exc:
                raise ValueError(f"invalid YAML: {exc}") from exc
            errors = validate_definition(data, filename=gym_id)
            if errors:
                raise ValueError("; ".join(errors))

        def _saved(raw: str | None) -> None:
            if raw is None:
                return
            from modules.redteam_gym import save_gym_yaml

            result = save_gym_yaml(gym_id, raw)
            if not result.get("success"):
                self.notify(f"gym not saved: {result.get('error', '')}", severity="error")
                return
            self._refresh_gyms()

        self.push_screen(YamlEditorModal(f"Edit {gym_id}.yaml", text, validator=_validate), _saved)

    def profile_rows(self) -> list[dict]:
        """Return one row per orchestrator profile with the active marker."""
        from modules import orchestrator_config as config

        try:
            available = config.profiles()
            active = config.active_profile()
        except Exception:
            return []
        rows: list[dict] = []
        for name, data in available.items():
            limits = dict(data.get("limits") or {})
            rows.append(
                {
                    "name": name,
                    "active": name == active,
                    "chain": str(data.get("chain", "")),
                    "playbook": str(data.get("playbook", "")),
                    "rounds": limits.get("rounds", ""),
                    "workers": limits.get("workers", ""),
                    "description": str(data.get("description", "")),
                }
            )
        return sorted(rows, key=lambda row: (not row["active"], row["name"]))

    def activate_profile(self, name: str) -> bool:
        """Persist one profile as active and repaint the profile table."""
        from modules import orchestrator_config as config

        try:
            config.set_profile(name)
        except KeyError:
            return False
        self._refresh_profiles()
        return True

    def _refresh_profiles(self) -> None:
        """Render every profile and highlight the active one."""
        try:
            table = self.query_one("#profiles-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("profile", "active", "chain", "playbook", "rounds", "workers", "description")
        for row in self.profile_rows():
            table.add_row(
                row["name"],
                "yes" if row["active"] else "",
                row["chain"],
                row["playbook"],
                str(row["rounds"]),
                str(row["workers"]),
                row["description"][:60],
                key=row["name"],
            )
        self._update_profile_detail(self._selected_row("profiles-table"))

    def _update_profile_detail(self, name: str) -> None:
        """Show limits and budgets for the selected profile."""
        try:
            panel = self.query_one("#profiles-detail", Static)
        except Exception:
            return
        if not name:
            panel.update("select a profile to activate it")
            return
        from modules import orchestrator_config as config

        try:
            profile = config.profile_config(name)
        except Exception:
            panel.update("profile unavailable")
            return
        limits = ", ".join(f"{key}={value}" for key, value in sorted((profile.get("limits") or {}).items()))
        budget = ", ".join(f"{key}={value}" for key, value in sorted((profile.get("budget") or {}).items()))
        panel.update(Text(f"{name}\nlimits: {limits}\nbudget: {budget}"))

    def _chains_dir(self):
        """Chain file root (overrideable for sandboxed tests)."""
        if self._chains_dir_override is not None:
            return self._chains_dir_override
        from modules.chain_registry import CHAINS_DIR

        return CHAINS_DIR

    def chain_rows(self) -> list[dict]:
        """Return one row per chain file, including disabled ones."""
        from modules.chain_registry import scan_all

        try:
            return scan_all(self._chains_dir())
        except Exception:
            return []

    def chain_steps_preview(self, name: str, limit: int = 10) -> str:
        """Return the resolved step lines of a chain for the detail pane."""
        from modules.chain_registry import get

        try:
            chain = get(name, self._chains_dir())
        except Exception:
            return "chain registry unavailable"
        if chain is None:
            return "chain not found or disabled"
        lines = [f"{i}. {step.run}" for i, step in enumerate(chain.steps[:limit], 1)]
        if len(chain.steps) > limit:
            lines.append(f"... +{len(chain.steps) - limit} more")
        lines.append("")
        lines.append(f"run: apt_chain {chain.name} <target>")
        return "\n".join(lines)

    def toggle_chain(self, name: str) -> bool:
        """Flip a chain's enabled flag in its YAML file."""
        from modules.chain_registry import scan_all, set_enabled

        current = next((row for row in scan_all(self._chains_dir()) if row["name"] == name), None)
        if current is None:
            return False
        ok = set_enabled(name, not current["enabled"], self._chains_dir())
        self._refresh_chains()
        return bool(ok)

    def generate_chain(self, playbook_key: str) -> str:
        """Generate chains/apt_<slug>.yaml from a playbook engine key."""
        from modules.apt_playbooks import AptPlaybookEngine
        from modules.chain_registry import generate_for_playbook

        key = (playbook_key or "").strip()
        engine = AptPlaybookEngine(playbook_dir=str(self._playbooks_dir()))
        playbook = engine.get(key)
        if playbook is None:
            return ""
        path = generate_for_playbook(key, apt_display=playbook.apt_name, chains_dir=self._chains_dir())
        self._refresh_chains()
        return str(path)

    def remove_chain(self, name: str) -> bool:
        """Delete a chain file unless others extend it or it is the base.

        Returns False (refusing loudly) for the base ``apt_chain`` and
        for any parent with children — edit or disable those instead.
        """
        from modules.chain_registry import scan_all

        if name == "apt_chain":
            return False
        try:
            rows = scan_all(self._chains_dir())
        except Exception:
            return False
        if any(row.get("extends") == name for row in rows):
            return False
        target = next((row for row in rows if row["name"] == name), None)
        if target is None:
            return False
        try:
            Path(target["source"]).unlink()
        except OSError:
            return False
        self._refresh_chains()
        return True

    def _refresh_chains(self) -> None:
        """Render the chains table with per-file state."""
        try:
            table = self.query_one("#chains-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("chain", "enabled", "steps", "playbook", "extends", "description")
        for row in self.chain_rows():
            state = "on" if row["enabled"] else "off"
            if not row.get("valid", True):
                state = f"off ({row.get('error', 'invalid')[:40]})"
            table.add_row(
                row["name"],
                state,
                str(row.get("steps", "")),
                str(row.get("playbook", "")),
                str(row.get("extends", "")),
                str(row.get("description", ""))[:60],
                key=row["name"],
            )
        self._update_chains_detail(self._selected_row("chains-table"))

    def _update_chains_detail(self, name: str) -> None:
        """Show the selected chain's steps in the detail pane."""
        try:
            self.query_one("#chains-detail", Static).update(self.chain_steps_preview(name) if name else "")
        except Exception:
            pass

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Refresh the detail pane when the cursor moves."""
        try:
            control_id = event.control.id
        except Exception:
            return
        try:
            key = event.row_key
            value = str(key.value or "")
        except Exception:
            return
        if control_id == "chains-table":
            self._update_chains_detail(value)
        elif control_id == "profiles-table":
            self._update_profile_detail(value)
        elif control_id == "playbooks-table":
            self._update_playbooks_detail(value)
        elif control_id == "gyms-table":
            self._update_gyms_detail(value)

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

    def set_model_priority(self, name: str, priority: str = "0") -> bool:
        """Change one LLM member's failover rank and repaint the table."""
        from modules.lazy_engine import LlmPool

        try:
            rank = int(str(priority).strip())
        except (TypeError, ValueError):
            return False
        touched = LlmPool().set_priority(name, rank)
        self._refresh_models()
        return bool(touched)

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
