"""Integration tests: exploration graph claims ride on SQLite leases."""

from __future__ import annotations

import pytest

import modules.lazy_loop as loop


@pytest.fixture()
def graph(tmp_path, monkeypatch):
    """Exploration graph over a throwaway sessions dir with fresh leases."""
    from modules.loop import state_db

    store_dir = tmp_path / "lazy"
    monkeypatch.setattr(loop, "STORE_DIR", store_dir)
    monkeypatch.setattr(loop, "_LEASE_STORE", None)
    monkeypatch.setattr(state_db, "default_db_path", lambda: tmp_path / "loop_state.db")
    store = loop._lease_store()
    graph = loop.ExplorationGraph("task-leases")
    yield graph, store
    monkeypatch.setattr(loop, "_LEASE_STORE", None)


def test_claim_acquires_lease(graph):
    graph, store = graph
    node = graph.add_node("intent", "scan target", priority=1)
    assert graph.compare_and_claim(node.node_id) is True
    assert store.active("task-leases", node.node_id) is True
    assert graph.get(node.node_id).state == "running"


def test_second_claim_blocked_by_lease(graph):
    graph, store = graph
    node = graph.add_node("intent", "scan target", priority=1)
    assert graph.compare_and_claim(node.node_id) is True
    assert graph.compare_and_claim(node.node_id) is False


def test_settle_on_exhausted_blocks_reclaim(graph):
    graph, store = graph
    node = graph.add_node("intent", "scan target", priority=1)
    graph.compare_and_claim(node.node_id)
    graph.set_state(node.node_id, "exhausted")
    assert store.active("task-leases", node.node_id) is False
    assert graph.compare_and_claim(node.node_id) is False


def test_requeue_releases_lease(graph):
    graph, store = graph
    node = graph.add_node("intent", "scan target", priority=1)
    graph.compare_and_claim(node.node_id)
    graph.set_state(node.node_id, "pending")
    assert store.active("task-leases", node.node_id) is False
    assert graph.compare_and_claim(node.node_id) is True


def test_budget_check_includes_token_verdict(tmp_path, monkeypatch):
    store_dir = tmp_path / "lazy"
    monkeypatch.setattr(loop, "STORE_DIR", store_dir)
    budget = loop.Budget()
    verdict = budget.check("no-such-task")
    assert verdict["ok"] is True
    assert "token" in verdict


def test_token_guard_fail_soft(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "TokenLedger", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    verdict = loop.token_guard("t1")
    assert verdict["ok"] is True
    assert verdict["action"] == "continue"


def test_lease_store_disabled(monkeypatch):
    from modules import orchestrator_config as oc

    monkeypatch.setattr(oc, "leases_config", lambda: {"enabled": False})
    monkeypatch.setattr(loop, "_LEASE_STORE", None)
    assert loop._lease_store() is None
    graph = loop.ExplorationGraph("task-nolease")
    node = graph.add_node("intent", "scan target", priority=1)
    assert graph.compare_and_claim(node.node_id) is True
