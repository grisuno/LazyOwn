"""Network scope contracts: a CIDR sweep needs whole-block authorization."""

from __future__ import annotations

from cli.scope_guard import network_denied, network_in_scope
from modules import lazy_scope
from modules.lazy_loop import scope_allows_network


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(loop, "_payload_scope_items", lambda: [])
    return LazyEngine()


def test_network_in_scope_requires_covering_cidr():
    """Given scope entries, When a sweep is wider, Then only a covering CIDR passes."""
    assert network_in_scope("10.1.2.0/24", ["10.1.0.0/16"]) is True
    assert network_in_scope("10.1.0.0/16", ["10.1.2.0/24"]) is False
    assert network_in_scope("10.1.2.0/24", ["10.1.2.5"]) is False
    assert network_in_scope("10.1.2.0/24", ["10.1.2.0/24"]) is True
    assert network_in_scope("2001:db8::/32", ["2001:db8::/16"]) is True
    assert network_in_scope("10.1.2.0/24", ["2001:db8::/16"]) is False


def test_network_denied_uses_overlap():
    """Given a deny range, When a sweep touches it, Then the whole sweep is denied."""
    assert network_denied("10.1.2.0/24", ["10.1.2.128/25"]) is True
    assert network_denied("10.1.2.0/24", ["10.1.3.0/24"]) is False
    assert network_denied("10.1.2.0/24", ["10.1.0.0/16"]) is True


def test_network_verdict_lab_and_public():
    """Given the lab default, When a block is private, Then it passes."""
    assert lazy_scope.network_verdict("10.0.0.0/24").allowed
    assert lazy_scope.network_verdict("127.0.0.0/8").allowed
    assert not lazy_scope.network_verdict("8.8.8.0/24").allowed
    assert not lazy_scope.network_verdict("0.0.0.0/0").allowed
    assert not lazy_scope.network_verdict("not-a-network").allowed


def test_network_verdict_denylist_overlap():
    """Given a deny sub-range, When a sweep overlaps it, Then it is denied."""
    verdict = lazy_scope.network_verdict("10.0.0.0/24", denylist=frozenset({"10.0.0.128/25"}))
    assert not verdict.allowed
    assert verdict.reason == "denylist"


def test_network_verdict_allowlist_must_cover():
    """Given an allowlist, When it covers the block, Then it is allowed."""
    allowed = lazy_scope.network_verdict("8.8.8.0/24", allowlist=frozenset({"8.8.0.0/16"}))
    assert allowed.allowed
    assert allowed.detail == "operator allowlist network"
    narrower = lazy_scope.network_verdict("8.8.8.0/24", allowlist=frozenset({"8.8.4.0/24"}))
    assert not narrower.allowed
    assert narrower.reason == "public-network"


def test_scope_allows_network_uses_task_scope(tmp_path, monkeypatch):
    """Given a task CIDR scope, When the sweep fits, Then it is allowed."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("network scope check")["task_id"]
    engine.store.add_scope(task_id, "cidr", "10.1.2.0/24", "test")
    allowed, _reason = scope_allows_network(task_id, engine.store, "10.1.2.0/24")
    assert allowed is True
    denied, reason = scope_allows_network(task_id, engine.store, "10.1.3.0/24")
    assert denied is False
    assert "outside task scope" in reason


def test_scope_allows_network_lab_default(tmp_path, monkeypatch):
    """Given no task scope, When the sweep is public, Then the lab default denies it."""
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("network lab default check")["task_id"]
    allowed, _reason = scope_allows_network(task_id, engine.store, "10.9.0.0/16")
    assert allowed is True
    denied, reason = scope_allows_network(task_id, engine.store, "8.8.8.0/24")
    assert denied is False
    assert "scope-lab-default" in reason


def test_worker_command_in_scope_checks_cidr(tmp_path, monkeypatch):
    """Given a CIDR scope, When a command sweeps outside it, Then the worker blocks."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("worker cidr check")["task_id"]
    engine.store.add_scope(task_id, "cidr", "10.1.2.0/24", "test")
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    assert worker._command_in_scope("nmap -sT -Pn 10.1.2.0/24") is True
    assert worker._command_in_scope("nmap -sT -Pn 10.1.3.0/24") is False
    assert worker._command_in_scope("nmap -sT -Pn 10.1.2.5") is True


def test_worker_command_in_scope_without_hosts(tmp_path, monkeypatch):
    """Given a command with no host, When checked, Then it passes untouched."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("worker no host check")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    assert worker._command_in_scope("id") is True
