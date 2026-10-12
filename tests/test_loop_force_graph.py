"""Loop ForceGraph context regression tests (lazy 0.3.12 fidelity)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_loop_graph_is_forcegraph_ready(tmp_path, monkeypatch):
    """BDD: /api/loop_graph payload renders directly in ForceGraph."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    asset = engine.assets.insert("ip", "127.0.0.1")
    intent = engine.add_intent(task_id, "probe ssh on 127.0.0.1")
    graph_module = __import__("modules.lazy_loop", fromlist=["ExplorationGraph"])
    graph = graph_module.ExplorationGraph(task_id)
    graph.anchor(intent.node_id, asset.asset_id)
    payload = engine.loop_graph(task_id)
    ids = {n["id"] for n in payload["nodes"]}
    assert f"e{intent.node_id}" in ids
    assert f"a{asset.asset_id}" in ids
    assert any(link["type"] == "anchors" for link in payload["links"])
    assert all("source" in link and "target" in link for link in payload["links"])


def test_graph_context_surfaces_hubs_and_next(tmp_path, monkeypatch):
    """BDD: planner sees hubs, islands and heat-ordered probes."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    engine.store.add_scope(task_id, "ip", "127.0.0.2", "test surface")
    engine.store.add_scope(task_id, "ip", "127.0.0.3", "test surface")
    lone = engine.assets.insert("ip", "127.0.0.2")
    void = engine.assets.insert("ip", "127.0.0.3")
    assert lone.asset_id and void.asset_id
    intent = engine.add_intent(task_id, "probe ssh on 127.0.0.1")
    graph_module = __import__("modules.lazy_loop", fromlist=["ExplorationGraph"])
    graph = graph_module.ExplorationGraph(task_id)
    linked = engine.assets.insert("ip", "127.0.0.1")
    graph.anchor(intent.node_id, linked.asset_id)
    ctx = engine.graph_context(task_id)
    assert ctx["stats"]["nodes"] >= 2
    assert any(h["id"] == intent.node_id for h in ctx["hubs"])
    assert any(i["value"] == "127.0.0.2" for i in ctx["islands"])
    assert ctx["suggested"], "untested scoped assets must be suggested"


def test_planner_force_ranks_connected_surface(tmp_path, monkeypatch):
    """SDD: candidates on hot graph surface outrank id-order probes."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    modules = __import__("modules.lazy_loop", fromlist=["Planner", "ActivityLog"])
    graph_module = __import__("modules.lazy_loop", fromlist=["ExplorationGraph"])
    graph = graph_module.ExplorationGraph(task_id)
    hot = engine.assets.insert("ip", "127.0.0.9")
    seed = engine.add_intent(task_id, "seed probe for heat")
    graph.anchor(seed.node_id, hot.asset_id)
    planner = modules.Planner(task_id, engine.assets, graph,
                              modules.ActivityLog(task_id), engine.store)
    candidates = planner._candidates()
    assert candidates, "planner must emit candidates on fresh task"
    heats = []
    for _summary, asset_ids, _parents, _priority in candidates:
        heat = max([0] + [3 if a == hot.asset_id else 0 for a in asset_ids])
        heats.append(heat)
    assert heats[0] >= heats[-1], "hot-asset candidates must float first"
