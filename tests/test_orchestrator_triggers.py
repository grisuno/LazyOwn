"""BDD tests for the orchestrator Triggers tab.

Given the scheduler triggers are now configuration plus runtime state,
When the operator opens the Triggers tab,
Then the table lists the persistent store rows, toggling a row persists
into the store, adding via the app method registers a trigger, and
removing removes only from the store.
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Sandbox the lazy store for every test in this module."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


def test_triggers_tab_lists_store_rows(sandbox):
    """Given seeded YAML triggers, the tab table shows every row."""
    import asyncio

    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules.trigger_policy import seed_store

    seed_store(policy=[{"kind": "service", "enabled": True}])

    async def _drive():
        app = LazyOrchestratorApp()
        async with app.run_test() as pilot:
            await pilot.pause(0.3)
            app.query_one("#tabs").active = "tab-triggers"
            await pilot.pause(0.2)
            return app.query_one("#triggers-table").row_count

    assert asyncio.run(_drive()) == 1


def test_triggers_toggle_persists(sandbox):
    """Given a disabled trigger, toggle_trigger flips it in the store."""
    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules.loop_triggers import TriggerStore

    app = LazyOrchestratorApp()
    item = TriggerStore("").add("service")
    assert item["enabled"]
    changed = app.toggle_trigger(int(item["id"]))
    assert changed
    rows = {int(i["id"]): i for i in TriggerStore("").list()}
    assert not rows[int(item["id"])]["enabled"]


def test_triggers_add_and_remove_via_app(sandbox):
    """Given operator input, add_trigger appends and remove_trigger deletes."""
    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules.loop_triggers import TriggerStore

    app = LazyOrchestratorApp()
    item = app.add_trigger("interval", "120")
    assert item["kind"] == "interval"
    removed = app.remove_trigger(int(item["id"]))
    assert removed
    assert TriggerStore("").list() == []


def test_trigger_kind_options_cover_registry(sandbox):
    """Given the add form, the kind picker covers every trigger kind."""
    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules.loop_triggers import TRIGGER_KINDS

    app = LazyOrchestratorApp()
    kinds = [value for value, _ in app.trigger_kind_options()]
    assert set(kinds) == set(TRIGGER_KINDS)
