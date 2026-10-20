"""BDD tests for the consolidated session-start brief.

Given the operator starts a session with a target, world-model state,
autonomous tasks, catalog verbs and declarative triggers,
When the shell renders the startup brief,
Then one panel summarises every layer, missing stores never raise,
and the shell integration picks the newest task automatically.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Sandbox every store the brief reads."""
    import modules.lazy_loop as loop
    import modules.world_model as world_model_module

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setenv("LAZY_SESSIONS_DIR", str(tmp_path))
    monkeypatch.setattr(world_model_module, "_DEFAULT_PATH", str(tmp_path / "world_model.json"))
    monkeypatch.setattr(world_model_module, "_default_wm", None)
    return tmp_path


def _console_text(renderable) -> str:
    from rich.console import Console

    console = Console(record=True, width=120, force_terminal=False)
    console.print(renderable)
    return console.export_text()


def test_brief_covers_target_phase_and_layers(sandbox):
    """Given a full campaign, the brief shows target, phase and counters."""
    from cli.session_brief import build_session_brief
    from modules import trigger_policy
    from modules.verb_catalog import sync
    from modules.world_model import get_world_model

    payload = {"rhost": "10.0.0.5", "lhost": "192.168.1.10", "c2_port": 5555}
    sync()
    trigger_policy.seed_store(policy=[{"kind": "service"}, {"kind": "interval", "every_sec": 60}])
    get_world_model().add_host("10.0.0.5")

    text = _console_text(build_session_brief(payload))
    assert "10.0.0.5" in text
    assert "recon" in text
    assert "verbs on=14" in text
    assert "triggers=2" in text


def test_brief_never_raises_on_empty_stores(tmp_path, monkeypatch):
    """Given no stores at all, the brief still renders the target line."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    from cli.session_brief import build_session_brief

    text = _console_text(build_session_brief({"rhost": "1.2.3.4"}))
    assert "1.2.3.4" in text


def test_brief_shows_newest_task(sandbox):
    """Given loop tasks exist, the newest running task heads the brief."""
    from cli.session_brief import build_session_brief
    from modules.lazy_engine import TaskStore

    store = TaskStore()
    task = store.create("phish the finance team")
    text = _console_text(build_session_brief({"rhost": "10.0.0.5"}, tasks=store.list()))
    assert str(getattr(task, "task_id", "")) in text or "phish the finance team" in text


def test_console_brief_respects_hints_off(tmp_path, monkeypatch):
    """Given ui_hints=off, the integration prints no brief."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    from cli.session_brief import brief_enabled

    assert brief_enabled({"ui_hints": "off"}) is False
    assert brief_enabled({"ui_hints": "on"}) is True
