"""Orchestrator admin console: headless smoke and real persistence.

The app is driven through Textual's ``run_test`` pilot; configuration,
LLM chain and guard edits use sandboxed stores so nothing touches the
real sessions or payload.
"""

from __future__ import annotations

import json

import pytest


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Sandbox the lazy store for every test in this module."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


def test_orchestrator_config_saves_to_payload(sandbox):
    """Config tab edits merge into the payload file without dropping keys."""
    import asyncio

    from textual.widgets import Input

    from cli.lazy_orchestrator import LazyOrchestratorApp

    payload_path = sandbox / "payload.json"
    payload_path.write_text('{"rhost": "127.0.0.1"}')

    async def _drive() -> LazyOrchestratorApp:
        app = LazyOrchestratorApp(payload_path=payload_path)
        async with app.run_test() as pilot:
            await pilot.pause(0.4)
            app.query_one("#cfg-plan_heartbeat_seconds", Input).value = "45"
            app.save_config({"plan_heartbeat_seconds": "45", "agent_tool_calling": "false"})
        return app

    asyncio.run(_drive())
    data = json.loads(payload_path.read_text(encoding="utf-8"))
    assert data["plan_heartbeat_seconds"] == 45
    assert data["agent_tool_calling"] is False
    assert data["rhost"] == "127.0.0.1"


def test_orchestrator_models_and_guard_actions(sandbox):
    """Add/remove helpers round-trip through the real stores."""
    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules.lazy_engine import Guard, LlmPool

    app = LazyOrchestratorApp()
    app.add_model_member("stub-member", "groq:stub-model", "7")
    names = [member["name"] for member in LlmPool().members()]
    assert "stub-member" in names
    assert app.remove_model_member("stub-member") is True
    assert "stub-member" not in [m["name"] for m in LlmPool().members()]

    assert app.add_guard_rule(r"forbidden-xyz", "deny", "test rule") is True
    assert any(rule.get("pattern") == r"forbidden-xyz" for rule in Guard().rules)
    assert app.remove_guard_rule(r"forbidden-xyz") is True
    assert not any(rule.get("pattern") == r"forbidden-xyz" for rule in Guard().rules)


def test_orchestrator_now_shows_activity(sandbox):
    """The Now pane tails the active task's activity stream."""
    import asyncio

    import modules.lazy_loop as loop
    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("probe surface")["task_id"]
    loop.ActivityLog(task_id).emit("worker-1", "tool", "[allow] nmap -sV 127.0.0.1")

    async def _drive() -> LazyOrchestratorApp:
        app = LazyOrchestratorApp(task_id=task_id)
        async with app.run_test() as pilot:
            await pilot.pause(0.9)
        return app

    app = asyncio.run(_drive())
    assert any("nmap -sV 127.0.0.1" in line for line in app._now_lines)
    assert app._worker_command.get("worker-1", "").endswith("nmap -sV 127.0.0.1")


def test_orchestrator_command_registered():
    from cli.commands.lazyloop import LazyQueueCommandSet

    assert hasattr(LazyQueueCommandSet, "do_lazy_orchestrator")


@pytest.fixture()
def payload_store(monkeypatch):
    """In-memory payload so orchestrator config writes stay sandboxed."""
    store = {"payload": {"rhost": "127.0.0.1"}}

    def _load(target=None):
        return dict(store["payload"])

    def _save(data, target=None):
        store["payload"] = dict(data)

    import core.config

    monkeypatch.setattr(core.config, "load_payload", _load)
    monkeypatch.setattr(core.config, "save_payload", _save)
    import modules.orchestrator_config as config_module

    config_module._invalidate()
    yield store
    config_module._invalidate()


def test_stage_toggles_persist(payload_store):
    """Stage enable/disable flags persist under orchestrator.stages."""
    from modules import orchestrator_config as config

    assert config.stage_enabled("retest") is True
    config.set_stage("retest", False)
    assert config.stage_enabled("retest") is False
    section = payload_store["payload"]["orchestrator"]["stages"]["retest"]
    assert section["enabled"] is False
    config.set_stage("retest", True)
    assert config.stage_enabled("retest") is True
    config.reset()
    assert "orchestrator" not in payload_store["payload"]


def test_auto_verb_enable_disable_and_custom(payload_store):
    """Disabled verbs leave planning and execution; custom verbs join both."""
    from modules import auto_registry as registry
    from modules import orchestrator_config as config

    assert registry.propose_intents("exploit and pwn the host", "127.0.0.1")
    config.upsert_verb("auto_pwn", enabled=False)
    proposed = registry.propose_intents("exploit and pwn the host", "127.0.0.1")
    assert not any("auto_pwn" in line for line in proposed)
    assert registry.steps_for("auto auto_pwn 127.0.0.1", "") is None
    assert registry.is_shell_verb("auto_pwn 127.0.0.1") is True
    assert "auto_pwn" in registry.verbs()

    config.upsert_verb(
        "myscan", enabled=True, keywords=["myscan"], needs_target=True, description="custom", custom=True
    )
    assert registry.propose_intents("please myscan now", "127.0.0.1") == ["auto myscan 127.0.0.1"]
    assert registry.steps_for("auto myscan 127.0.0.1", "") == ["myscan 127.0.0.1"]
    assert config.remove_verb("myscan") is True
    assert config.verb_config("myscan") is None


def test_engine_respects_disabled_workers(payload_store, tmp_path, monkeypatch):
    """Disabling the workers stage pauses frontier execution."""
    import modules.lazy_loop as loop
    from modules import orchestrator_config as config
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    engine.add_intent(task_id, "probe 127.0.0.1")
    config.set_stage("workers", False)
    summary = engine.run_round(task_id, workers=1, executor=lambda command: "22/tcp open ssh")
    assert summary["executed"] == 0
    config.set_stage("workers", True)
    summary = engine.run_round(task_id, workers=1, executor=lambda command: "22/tcp open ssh")
    assert summary["executed"] >= 1


def test_orchestrator_tables_render(payload_store):
    """Pipeline and Verbs tabs render one row per entry."""
    import asyncio

    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules import orchestrator_config as config

    async def _drive():
        app = LazyOrchestratorApp()
        async with app.run_test() as pilot:
            await pilot.pause(0.4)
            stages_table = app.query_one("#stages-table")
            verbs_table = app.query_one("#verbs-table")
        return app, stages_table.row_count, verbs_table.row_count

    _app, stage_rows, verb_rows = asyncio.run(_drive())
    assert stage_rows == len(config.stages())
    assert verb_rows == len(config.effective_verbs())


def test_orchestrator_chains_tab_lists_and_toggles(sandbox, monkeypatch, tmp_path):
    """Chains tab: rows render, toggle flips YAML, preview shows steps."""
    import asyncio

    import yaml as _yaml

    from cli.lazy_orchestrator import LazyOrchestratorApp

    chains_dir = tmp_path / "chains"
    chains_dir.mkdir()
    (chains_dir / "apt_chain.yaml").write_text(
        _yaml.dump(
            {
                "name": "apt_chain",
                "description": "base",
                "enabled": True,
                "defaults": {"playbook": "rocke"},
                "steps": [{"run": "echo {playbook} {target}"}],
            }
        ),
        encoding="utf-8",
    )
    (chains_dir / "apt_demo.yaml").write_text(
        _yaml.dump(
            {
                "name": "apt_demo",
                "description": "child",
                "enabled": True,
                "extends": "apt_chain",
                "defaults": {"playbook": "demo"},
            }
        ),
        encoding="utf-8",
    )
    probe = LazyOrchestratorApp()
    probe._chains_dir_override = chains_dir
    rows = probe.chain_rows()
    assert {r["name"] for r in rows} == {"apt_chain", "apt_demo"}
    preview = probe.chain_steps_preview("apt_demo")
    assert "echo demo" in preview or "echo {playbook}" in preview

    async def _drive() -> None:
        app = LazyOrchestratorApp()
        app._chains_dir_override = chains_dir
        async with app.run_test() as pilot:
            await pilot.pause(0.4)
            assert app.toggle_chain("apt_demo") is True
            assert app.toggle_chain("apt_demo") is True
            assert app.generate_chain("nope-missing-playbook") == ""
            assert app.remove_chain("apt_chain") is False
            assert app.remove_chain("apt_demo") is True

    asyncio.run(_drive())
    remaining = [r["name"] for r in probe.chain_rows()]
    assert "apt_demo" not in remaining


def test_orchestrator_generate_chain_uses_playbooks(sandbox, monkeypatch, tmp_path):
    """Generate action pins the playbook engine key, not a guess."""
    from cli.lazy_orchestrator import LazyOrchestratorApp

    app = LazyOrchestratorApp()
    app._chains_dir_override = tmp_path / "chains"
    path = app.generate_chain("rocke")
    assert path.endswith("apt_rocke.yaml")
    import yaml as _yaml

    raw = _yaml.safe_load((tmp_path / "chains" / "apt_rocke.yaml").read_text(encoding="utf-8"))
    assert raw["defaults"] == {"playbook": "rocke"} and raw["extends"] == "apt_chain"


def test_orchestrator_playbooks_crud(tmp_path):
    """Playbooks tab methods create, preview, update and delete YAML."""
    import yaml as _yaml

    from cli.lazy_orchestrator import LazyOrchestratorApp

    app = LazyOrchestratorApp()
    app._playbooks_dir_override = tmp_path
    created = app.create_playbook_file("demo", "Demo APT", "demo plan", "linux, windows")
    assert created.endswith("demo.yaml")

    rows = app.playbook_rows()
    assert len(rows) == 1
    assert rows[0]["file"] == "demo.yaml"
    assert rows[0]["kind"] == "apt"
    assert "apt_name: Demo APT" in app.playbook_preview("demo.yaml")

    updated = _yaml.safe_dump(
        {
            "apt_name": "Demo APT",
            "description": "updated",
            "platforms": ["linux"],
            "phases": [
                {"name": "execution", "technique_id": "T1059", "atomic_tests": [{"atomic_id": "T1059"}]}
            ],
        },
        sort_keys=False,
    )
    assert app.save_playbook_text("demo.yaml", updated) is True
    assert app.playbook_rows()[0]["steps"] == 1

    assert app.save_playbook_text("demo.yaml", "not: [valid") is False
    assert app.delete_playbook_file("demo.yaml") is True
    assert app.playbook_rows() == []


def test_orchestrator_verb_candidates_cover_commands_and_verbs():
    """The verb picker sees built-in verbs plus real shell commands."""
    from cli.lazy_orchestrator import command_descriptions, discover_shell_commands, verb_candidates

    commands = discover_shell_commands()
    assert "lazynmap" in commands
    assert "auto_loop" in commands
    pairs = dict(verb_candidates())
    assert "auto_pwn" in pairs
    assert "lazynmap" in pairs
    assert command_descriptions().get("lazynmap")


def test_search_select_filter_ranks_prefix_first():
    """Searchable select ranks prefixes, then substrings, then descriptions."""
    from cli.tui_forms import filter_candidates

    options = [("nmap", "scanner"), ("lazynmap", "wrapper"), ("pwn", "exploit nmap")]
    assert [value for value, _ in filter_candidates("nmap", options)] == ["nmap", "lazynmap", "pwn"]
    assert filter_candidates("zzz", options) == []


def test_orchestrator_playbooks_tab_renders(tmp_path):
    """The Playbooks tab shows one row per file and a YAML preview."""
    import asyncio

    import yaml as _yaml

    from cli.lazy_orchestrator import LazyOrchestratorApp

    (tmp_path / "apt_demo.yaml").write_text(
        _yaml.safe_dump({"apt_name": "Demo", "description": "demo", "phases": []}), encoding="utf-8"
    )

    async def _drive():
        app = LazyOrchestratorApp()
        app._playbooks_dir_override = tmp_path
        async with app.run_test() as pilot:
            await pilot.pause(0.3)
            app.query_one("#tabs").active = "tab-playbooks"
            await pilot.pause(0.2)
            return app.query_one("#playbooks-table").row_count, str(app.query_one("#playbooks-detail").content)

    rows, detail = asyncio.run(_drive())
    assert rows == 1
    assert "apt_name: Demo" in detail or "Demo" in detail


def test_verb_add_opens_searchable_picker(payload_store):
    """Pressing add on Verbs opens the search picker with a prefilled form."""
    import asyncio

    from textual.widgets import Input

    from cli.lazy_orchestrator import LazyOrchestratorApp

    async def _drive():
        app = LazyOrchestratorApp()
        async with app.run_test() as pilot:
            await pilot.pause(0.3)
            app.query_one("#tabs").active = "tab-verbs"
            await pilot.pause(0.2)
            await pilot.press("a")
            await pilot.pause(0.2)
            search = app.screen.query_one("#select-search", Input)
            search.value = "lazynmap"
            await pilot.pause(0.2)
            await pilot.press("enter")
            await pilot.pause(0.2)
            return app.screen.query_one("#verb", Input).value

    assert asyncio.run(_drive()) == "lazynmap"


def test_orchestrator_gyms_tab_starts_and_stops(tmp_path, monkeypatch):
    """The Gyms tab reads YAML definitions and toggles persistent runs."""
    import shutil

    import modules.gym_registry as registry
    import modules.outcome_bus as outcome_bus
    import modules.redteam_gym as gym
    import modules.world_model as world_model
    from cli.lazy_orchestrator import LazyOrchestratorApp

    shutil.copytree(registry.GYMS_DIR, tmp_path / "gyms")
    monkeypatch.setattr(world_model, "_DEFAULT_PATH", tmp_path / "world_model.json")
    monkeypatch.setattr(world_model, "_default_wm", None)
    monkeypatch.setattr(registry, "GYMS_DIR", tmp_path / "gyms")
    monkeypatch.setattr(registry, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(gym, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(gym, "GYM_LEADERBOARD", tmp_path / "sessions" / "gym" / "leaderboard.json")
    monkeypatch.setattr(gym, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(outcome_bus, "record_event", lambda **kwargs: {})

    app = LazyOrchestratorApp()
    rows = {row["id"]: row for row in app.gym_rows()}
    assert "first_blood_web" in rows
    assert rows["first_blood_web"]["active"] == 0
    assert "apt_name" not in app.gym_preview("first_blood_web").lower()

    started = app.start_gym("first_blood_web", target="172.17.0.2")
    assert started["success"] is True
    assert app.gym_rows()  # table refresh does not raise outside a running app
    assert next(row for row in app.gym_rows() if row["id"] == "first_blood_web")["active"] == 1

    stopped = app.stop_gym("first_blood_web")
    assert stopped["count"] == 1
    assert next(row for row in app.gym_rows() if row["id"] == "first_blood_web")["active"] == 0


def test_orchestrator_params_tab_renders_and_creates(sandbox, tmp_path):
    """Params tab: rows render, a parameter is declared and published."""
    import asyncio

    from cli.lazy_orchestrator import LazyOrchestratorApp

    class _Shell:
        def __init__(self):
            self.params = {}

    shell = _Shell()

    async def _drive():
        app = LazyOrchestratorApp(shell=shell, param_root=tmp_path)
        async with app.run_test() as pilot:
            await pilot.pause(0.4)
            table = app.query_one("#params-table")
            rows = table.row_count
            created = app.create_param("tui_shared_param", "string", "v", "shared demo")
        return rows, created

    rows, created = asyncio.run(_drive())
    assert rows > 0, "the params table must list the catalog"
    assert created["name"] == "tui_shared_param"
    assert shell.params["tui_shared_param"] == "v"

    from core.param_registry import load_entries

    assert "tui_shared_param" in load_entries(tmp_path)
