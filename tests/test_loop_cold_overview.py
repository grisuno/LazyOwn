"""Cold debounce + planner overview parity (lazy 0.3.8 coldgraph)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def _old_facts(graph, count, prefix="stale fact"):
    import modules.lazy_loop as loop

    parent = graph.add_node("intent", f"{prefix} parent direction", state="done")
    nodes = [graph.add_node("fact", f"{prefix} body text for grouping {i // 3}",
                            state="done") for i in range(count)]
    for node in nodes:
        node.updated = loop._now() - 1000.0
        graph.add_edge(parent.node_id, node.node_id, "yields")
    graph._persist()
    return nodes


def test_compact_debounce_keeps_fresh_hot(tmp_path, monkeypatch):
    """BDD: fresh facts survive the anti-flap window."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    for i in range(55):
        graph.add_node("fact", f"fresh fact body grouping {i // 3}", state="done")
    out = loop.ColdCompactor(graph, loop.ActivityLog(task_id)).compact()
    assert out["compacted"] == 0


def test_compact_folds_stale_facts(tmp_path, monkeypatch):
    """BDD: untouched facts fold into digests after the window."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    _old_facts(graph, 55)
    out = loop.ColdCompactor(graph, loop.ActivityLog(task_id)).compact()
    assert out["compacted"] > 0
    assert out["digest_id"] > 0
    revived = loop.ColdCompactor(graph, loop.ActivityLog(task_id)).expand(out["digest_id"])
    assert revived


def test_planner_round_folds_minor_window(tmp_path, monkeypatch):
    """BDD: 20-50 uncovered cold nodes fold on a round, no no-op window."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    _old_facts(graph, 25)
    compactor = loop.ColdCompactor(graph, loop.ActivityLog(task_id))
    cold = compactor._load_cold()
    struct = compactor.structural_cold(compactor.hot_set())
    cold["round_no"] = loop.COLD_R_ROUNDS
    cold["cold_since"] = {str(i): 0 for i in struct}
    compactor._save_cold(cold)
    out = compactor.on_planner_round()
    assert out["triggered"] == "minor"
    digests = [n for n in graph.list("fact") if n.meta.get("cold_digest")]
    assert digests
    assert sum(len(n.meta.get("members", [])) for n in digests) >= loop.COLD_K_MIN


def test_graph_overview_carries_findings_and_done_totals(tmp_path, monkeypatch):
    """BDD: planner sees every finding plus done-intent totals inline."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    service = loop.FindingService(task_id, graph, loop.ActivityLog(task_id), engine.store)
    critical = service.report("rce in upload", summary="unauthenticated", severity="critical")
    service.report("weak cipher", summary="tls 1.0", severity="low")
    intent = engine.add_intent(task_id, "probe upload")
    loop.ExplorationGraph(task_id).set_state(intent.node_id, "done")
    view = engine.graph_overview(task_id)
    assert [f["id"] for f in view["finding_list"]] == [critical.node_id] + [
        f["id"] for f in view["finding_list"][1:]]
    assert view["finding_list"][0]["severity"] == "critical"
    assert view["done_intents_total"] == 1
    assert len(view["recent_done_intents"]) == 1
    assert view["recent_done_intents"][0]["id"] == intent.node_id
