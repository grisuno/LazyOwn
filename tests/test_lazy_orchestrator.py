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
