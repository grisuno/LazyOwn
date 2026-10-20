"""Asset administration tabs for the orchestrator console.

Mixin holding the tab controllers that edit YAML-run assets: Playbooks,
Gyms, Chains and Profiles. Split out of ``cli/lazy_orchestrator.py`` to
keep the Textual app module under the size ceiling while per-tab state
and persistence helpers stay single-responsibility here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rich.text import Text
from textual.widgets import DataTable, Input, Static


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


class OrchestratorAssetsMixin:
    """Tab controllers for Playbooks, Gyms, Chains and Profiles tabs."""

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

    def _refresh_triggers(self) -> None:
        """Render scheduler triggers from the persistent store."""
        from modules.trigger_policy import export_store

        try:
            table = self.query_one("#triggers-table", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("id", "kind", "every_sec", "enabled", "arg")
        for item in export_store():
            table.add_row(
                str(item.get("id", "")),
                str(item.get("kind", "")),
                str(item.get("every_sec", 0)),
                "on" if item.get("enabled") else "off",
                str(item.get("arg", "")),
                key=str(item.get("id", "")),
            )
        self._update_trigger_detail()

    def _update_trigger_detail(self) -> None:
        """Show a summary of the declarative seed policy."""
        from modules.trigger_policy import read_policy

        try:
            panel = self.query_one("#triggers-detail", Static)
        except Exception:
            return
        policy = read_policy()
        seeds = policy.get("seeds") or []
        on = sum(1 for item in seeds if item["enabled"])
        panel.update(Text(f"YAML seeds: {len(seeds)} ({on} on)"))

    def toggle_trigger(self, trigger_id: int) -> bool:
        """Flip one trigger's enabled flag in the store."""
        from modules.loop_triggers import TriggerStore
        from modules.trigger_policy import export_store

        enabled = any(
            int(item.get("id", 0)) == int(trigger_id) and item.get("enabled")
            for item in export_store()
        )
        changed = TriggerStore("").set_enabled(trigger_id, not enabled)
        self._refresh_triggers()
        return changed

    def remove_trigger(self, trigger_id: int) -> bool:
        """Delete one trigger from the store."""
        from modules.loop_triggers import TriggerStore

        removed = TriggerStore("").remove(trigger_id)
        self._refresh_triggers()
        return removed

    def add_trigger(self, kind: str, every_sec: str = "", arg: str = "") -> dict:
        """Add a scheduler trigger entered from the picker form."""
        from modules.loop_triggers import TriggerStore

        try:
            every = float(every_sec)
        except (TypeError, ValueError):
            every = 0.0
        item = TriggerStore("").add(kind, arg=(arg or "")[:300], every_sec=every)
        self._refresh_triggers()
        return item

    def trigger_kind_options(self) -> list[tuple[str, str]]:
        """Return selectable trigger kinds for the add form."""
        from modules.loop_triggers import TRIGGER_KINDS

        return [(kind, kind) for kind in TRIGGER_KINDS]

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

