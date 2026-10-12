"""Broadcast board timeline regression tests (lazy 0.3.12 parity)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_broadcast_rows_carry_neighbours_and_assets(tmp_path, monkeypatch):
    """BDD: timeline rows expand without extra requests."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    asset = engine.assets.insert("ip", "127.0.0.1")
    intent = engine.add_intent(task_id, "probe ssh on 127.0.0.1")
    graph_module = __import__("modules.lazy_loop", fromlist=["ExplorationGraph"])
    graph = graph_module.ExplorationGraph(task_id)
    fact = graph.record_fact("ssh open on 127.0.0.1", evidence="nmap 22/open",
                             intent_id=intent.node_id, asset_ids=[asset.asset_id])
    result = engine.broadcast(task_id)
    assert result["total"] >= 2
    fact_row = next(i for i in result["items"] if i["id"] == fact.node_id)
    assert fact_row["kind"] == "fact"
    assert any(u["id"] == intent.node_id for u in fact_row["upstream"])
    assert any(a["value"] == "127.0.0.1" for a in fact_row["assets"])
    assert fact_row["day"] != ""
    intent_row = next(i for i in result["items"] if i["id"] == intent.node_id)
    assert any(d["id"] == fact.node_id for d in intent_row["downstream"])


def test_broadcast_search_id_and_kind_filter(tmp_path, monkeypatch):
    """BDD: search supports #id and kind filter."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    intent = engine.add_intent(task_id, "probe http")
    engine.add_hint(task_id, "focus on login forms")
    by_id = engine.broadcast(task_id, query=f"#{intent.node_id}")
    assert by_id["total"] == 1
    assert by_id["items"][0]["id"] == intent.node_id
    by_kind = engine.broadcast(task_id, kinds=["hint"])
    assert by_kind["total"] >= 1
    assert all(i["kind"] == "hint" for i in by_kind["items"])
    page = engine.broadcast(task_id, page=1, per_page=1)
    assert len(page["items"]) == 1
    assert page["has_more"] == (page["total"] > 1)
