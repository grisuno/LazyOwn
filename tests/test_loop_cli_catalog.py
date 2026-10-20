"""BDD tests for planner prompt visibility into routable CLI verbs.

Given the autonomous loop plans a round,
When the planner prompt context assembles,
Then it carries an ``Allowed commands:`` line built from the operator's
enabled verb catalog for the current kill-chain phase, disabled
commands never appear, and a missing catalog view leaves the prompt
without the line (fail closed, never wider).
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Sandbox loop stores, world model and verb catalog."""
    import modules.lazy_loop as loop
    import modules.world_model as world_model_module
    from modules import killchain

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(world_model_module, "_DEFAULT_PATH", str(tmp_path / "world_model.json"))
    monkeypatch.setattr(world_model_module, "_default_wm", None)
    monkeypatch.setattr(killchain, "_DEFAULT_CONFIG", killchain.KillChainConfig(sessions_dir=tmp_path))

    from modules import verb_catalog
    from modules.verb_catalog import VerbCatalogConfig

    catalog_path = tmp_path / "verbs.yaml"
    catalog_path.write_text(
        "version: 1\nverbs:\n  lazynmap:\n    enabled: true\n  ping:\n    enabled: false\n"
        "  pyautomate:\n    enabled: true\n",
        encoding="utf-8",
    )
    index_path = tmp_path / "index.json"
    index_path.write_text(
        '{"commands": ['
        '{"name": "do_lazynmap", "phase": "recon"}, '
        '{"name": "do_ping", "phase": "recon"}, '
        '{"name": "do_pyautomate", "phase": "exploit"}]}',
        encoding="utf-8",
    )

    def _default(cfg: VerbCatalogConfig | None = None) -> VerbCatalogConfig:

        return VerbCatalogConfig(catalog_path=catalog_path, index_path=index_path)

    monkeypatch.setattr(verb_catalog, "_default_config", _default)
    del verb_catalog
    return tmp_path


def test_catalog_cli_for_phase_lists_enabled_only(sandbox):
    """Given a mixed catalog, only enabled commands reach the planner text."""
    from modules.lazy_cli_bridge import catalog_cli_for_phase

    text = catalog_cli_for_phase()
    assert "lazynmap" in text
    assert "ping" not in text
    assert "pyautomate" not in text


def test_prompt_context_carries_allowed_commands(sandbox):
    """Given a recon world model, the prompt context carries allowed verbs."""
    from modules.lazy_loop import AssetGraph, ExplorationGraph, TaskStore, build_prompt_context
    from modules.world_model import get_world_model

    task_id = TaskStore().create("probe the target").task_id
    graph = ExplorationGraph(task_id)
    get_world_model().add_host("10.0.0.9")
    context = build_prompt_context(task_id, graph, AssetGraph(), TaskStore())
    assert "Allowed commands" in context
    assert "lazynmap" in context


def test_missing_catalog_view_adds_nothing(tmp_path, monkeypatch):
    """Given no catalog view, the prompt gains no verbs line."""
    import modules.lazy_loop as loop
    import modules.world_model as world_model_module

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(world_model_module, "_DEFAULT_PATH", str(tmp_path / "world_model.json"))
    monkeypatch.setattr(world_model_module, "_default_wm", None)
    from modules import verb_catalog

    def _broken():
        raise RuntimeError("no catalog")

    monkeypatch.setattr(verb_catalog, "_default_config", _broken)
    from modules.lazy_loop import AssetGraph, ExplorationGraph, TaskStore, build_prompt_context

    task_id = TaskStore().create("probe").task_id
    context = build_prompt_context(task_id, ExplorationGraph(task_id), AssetGraph(), TaskStore())
    assert "Allowed commands" not in context
