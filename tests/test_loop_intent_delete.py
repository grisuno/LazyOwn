"""Intent delete modes regression tests (lazy 0.3.12 parity)."""

from __future__ import annotations

import pytest


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_soft_delete_keeps_outputs_and_notifies(tmp_path, monkeypatch):
    """BDD: fake delete keeps node, outputs and lineage with a reason."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    intent = engine.add_intent(task_id, "probe ssh")
    graph = loop.ExplorationGraph(task_id)
    fact = graph.record_fact("ssh open", evidence="nmap", intent_id=intent.node_id)
    result = engine.delete_intent(task_id, intent.node_id, mode="soft", reason="wrong direction")
    assert result["mode"] == "soft"
    kept = loop.ExplorationGraph(task_id)
    assert kept.get(intent.node_id) is not None
    assert kept.get(intent.node_id).state == "deleted"
    assert kept.get(intent.node_id).meta["delete_reason"] == "wrong direction"
    assert kept.get(fact.node_id) is not None
    trail = loop.ActivityLog(task_id).read(50)
    assert any(str(r.get("kind", "")) in ("replan", "cancelled") for r in trail)


def test_soft_delete_requires_reason(tmp_path, monkeypatch):
    """BDD: deletion without a reason is rejected."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    intent = engine.add_intent(task_id, "probe http")
    with pytest.raises(ValueError):
        engine.delete_intent(task_id, intent.node_id, mode="soft", reason="")


def test_hard_delete_removes_exclusive_keeps_shared(tmp_path, monkeypatch):
    """BDD: true delete cascades exclusive descendants, keeps shared/goals."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    goal = loop.ExplorationGraph(task_id).list("goal")
    assert goal, "create_task must seed at least one goal"
    first = engine.add_intent(task_id, "first direction")
    second = engine.add_intent(task_id, "second direction")
    graph = loop.ExplorationGraph(task_id)
    exclusive = graph.record_fact("only first saw this", intent_id=first.node_id)
    shared = graph.record_fact("both saw this", intent_id=first.node_id)
    graph.add_edge(second.node_id, shared.node_id, "yields")
    preview = engine.preview_delete_intent(task_id, first.node_id)
    assert exclusive.node_id in preview["removable"]
    assert shared.node_id not in preview["removable"]
    result = engine.delete_intent(task_id, first.node_id, mode="hard", reason="dead end")
    assert result["mode"] == "hard"
    assert exclusive.node_id in result["removed"]
    assert shared.node_id in result["shared"]
    fresh = loop.ExplorationGraph(task_id)
    assert fresh.get(exclusive.node_id) is None
    assert fresh.get(shared.node_id) is not None
    assert fresh.get(second.node_id) is not None
    for node in fresh.list("goal"):
        assert node is not None
