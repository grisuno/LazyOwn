"""Scope ownership, port-aware traffic search, role-based evidences (lazy parity)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_scope_covers_by_ownership_not_substring(tmp_path, monkeypatch):
    """BDD: root domain owns subdomains/services, decoys stay out."""
    engine = _patched_engine(tmp_path, monkeypatch)
    sub = engine.assets.insert("subdomain", "app.example.com")
    svc = engine.assets.insert("service", "http://app.example.com:8080/login")
    decoy = engine.assets.insert("subdomain", "notexample.com")
    scope = [{"kind": "root_domain", "value": "example.com"}]
    owned = engine.assets.scoped(scope)
    ids = {n.asset_id for n in owned}
    assert sub.asset_id in ids
    assert svc.asset_id in ids
    assert decoy.asset_id not in ids


def test_scope_cidr_covers_url_embedded_ip(tmp_path, monkeypatch):
    """BDD: CIDR scope hits direct URLs on in-range hosts."""
    engine = _patched_engine(tmp_path, monkeypatch)
    inside = engine.assets.insert("url", "http://10.1.2.3/api")
    outside = engine.assets.insert("url", "http://10.9.9.9/api")
    scope = [{"kind": "cidr", "value": "10.1.2.0/24"}]
    owned = engine.assets.scoped(scope)
    ids = {n.asset_id for n in owned}
    assert inside.asset_id in ids
    assert outside.asset_id not in ids


def test_scope_ip_covers_any_port_url(tmp_path, monkeypatch):
    """BDD: ip scope owns the host on every port."""
    engine = _patched_engine(tmp_path, monkeypatch)
    first = engine.assets.insert("url", "http://10.2.3.4:8080/a")
    second = engine.assets.insert("url", "http://10.2.3.4:9090/b")
    other = engine.assets.insert("url", "http://10.2.3.5:8080/a")
    scope = [{"kind": "ip", "value": "10.2.3.4"}]
    ids = {n.asset_id for n in engine.assets.scoped(scope)}
    assert first.asset_id in ids
    assert second.asset_id in ids
    assert other.asset_id not in ids


def test_worker_scope_enforcement_cidr(tmp_path, monkeypatch):
    """BDD: a CIDR scope admits in-range targets and blocks the rest."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("scope enforcement check")["task_id"]
    engine.store.add_scope(task_id, "cidr", "10.1.2.0/24", "test scope")
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker("worker-1", task_id, engine.assets, graph,
                         loop.ActivityLog(task_id), loop.TrafficLog(task_id),
                         loop.Guard(task_id), engine.store)
    assert worker._scope_allows_target("10.1.2.5") is True
    assert worker._scope_allows_target("http://10.1.2.5:8080/x") is True
    assert worker._scope_allows_target("10.9.9.9") is False
    assert worker._scope_allows_target("evil.example.com") is False


def test_traffic_search_host_port_aware(tmp_path, monkeypatch):
    """BDD: same-host rows on other ports never mix into the result."""
    import modules.lazy_loop as loop

    _patched_engine(tmp_path, monkeypatch)
    traffic = loop.TrafficLog("t1")
    traffic.record("bash", "curl http://10.3.3.3:8080/login", "ok 200")
    traffic.record("bash", "curl http://10.3.3.3:9090/login", "ok 200")
    traffic.record("bash", "curl http://10.3.3.30:8080/login", "ok 200")
    scoped = traffic.search_host("10.3.3.3", port="8080")
    assert len(scoped) == 1
    assert ":8080" in scoped[0]["command"]
    any_port = traffic.search_host("10.3.3.3")
    assert len(any_port) == 2
    assert all("10.3.3.30" not in r["command"] for r in any_port)


def test_finding_evidence_roles_notes_order(tmp_path, monkeypatch):
    """BDD: findings bind many evidences with roles, notes and order."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    traffic = loop.TrafficLog(task_id)
    service = loop.FindingService(task_id, graph, loop.ActivityLog(task_id), engine.store)
    finding = service.report("sqli in login", summary="error-based", severity="high")
    assert traffic.bind(finding.node_id, "aaa111", graph, role="request", note="payload") is True
    assert traffic.bind(finding.node_id, "bbb222", graph, role="response") is True
    rows = traffic.evidence(finding.node_id, graph)
    assert [r["digest"] for r in rows] == ["aaa111", "bbb222"]
    assert rows[0]["role"] == "request"
    assert rows[0]["note"] == "payload"
    assert traffic.reorder_evidence(finding.node_id, ["bbb222", "aaa111"], graph) is True
    assert [r["digest"] for r in traffic.evidence(finding.node_id, graph)] == ["bbb222", "aaa111"]
    legacy = graph.get(finding.node_id)
    legacy.meta["traffic_refs"] = ["ccc333"]
    rows = traffic.evidence(finding.node_id, graph)
    assert rows[-1] == {"digest": "ccc333", "role": "supporting", "note": "", "ts": 0.0}
