"""BDD for the cve_hot trigger hint fingerprints.

Given a hot CVE matched on a discovered service, When the loop trigger
fires, Then the verification hint is proposed once per evidence
signature: the same (cve, product, banner) never queues a second
pending hint until the evidence changes or the repeat window expires,
so the pending backlog cannot fill with duplicate asks.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

CANNED_MATCH = {
    "cve": "CVE-2021-44228",
    "heat": "hot",
    "cvss": 10.0,
    "product": "log4j-core",
    "version": "2.14.1",
    "host": "10.0.0.5",
    "port": "8080",
    "confidence": 0.8,
}


class _Graph:
    """Recording ExplorationGraph double for trigger evaluation."""

    def __init__(self) -> None:
        self.nodes: list[dict] = []

    def add_node(self, kind: str, text: str, state: str = "pending", priority: int = 3, meta: dict | None = None):
        self.nodes.append({"kind": kind, "text": text, "meta": dict(meta or {})})

    def list(self, *args, **kwargs) -> list:
        return []


class _Assets:
    """Listable asset store emitting one fresh service asset per round."""

    def __init__(self, value: str = "log4j-core 2.14.1") -> None:
        self.value = value
        self._next_id = 1

    def list(self, kind: str) -> list:
        asset = SimpleNamespace(asset_id=self._next_id, kind=kind, value=self.value)
        self._next_id += 1
        return [asset]


@pytest.fixture()
def trigger_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Trigger store, graph and assets isolated under tmp_path with canned matches."""
    import modules.lazy_loop as loop
    import modules.loop_triggers as triggers
    import modules.world_model as world_module

    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(world_module, "get_world_model", lambda: {"hosts": {}})

    def fake_hot_matches(services, allow_network=False):
        rows = []
        for svc in services:
            version = str(svc.get("version", "") or "")
            rows.append(dict(CANNED_MATCH, version=version or CANNED_MATCH["version"]))
        return rows

    monkeypatch.setattr("modules.lazy_cve_feed.hot_matches", fake_hot_matches)
    store = triggers.TriggerStore("")
    store.add("cve_hot", every_sec=0.0)
    return triggers, store, _Graph(), _Assets()


def test_cve_hot_hint_proposed_once_per_signature(trigger_env) -> None:
    """First round queues the verification hint; the same evidence never re-queues."""
    triggers, store, graph, assets = trigger_env
    first = store.due("", graph, None, assets=assets)
    assert any(hit["kind"] == "cve_hot" for hit in first)
    assert len(graph.nodes) == 1
    assert "CVE-2021-44228" in graph.nodes[0]["text"]
    second = store.due("", graph, None, assets=assets)
    assert any(hit["kind"] == "cve_hot" for hit in second)
    assert len(graph.nodes) == 1


def test_changed_banner_refires_the_hint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A new version banner is new evidence: the hint queues again."""
    import modules.lazy_loop as loop
    import modules.loop_triggers as triggers
    import modules.world_model as world_module

    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(world_module, "get_world_model", lambda: {"hosts": {}})
    state = {"version": CANNED_MATCH["version"]}

    def fake_hot_matches(services, allow_network=False):
        return [dict(CANNED_MATCH, version=state["version"])]

    monkeypatch.setattr("modules.lazy_cve_feed.hot_matches", fake_hot_matches)
    store = triggers.TriggerStore("")
    store.add("cve_hot", every_sec=0.0)
    graph = _Graph()
    assets = _Assets()
    store.due("", graph, None, assets=assets)
    assert len(graph.nodes) == 1
    assert triggers.hint_fingerprint(CANNED_MATCH) != triggers.hint_fingerprint(
        {**CANNED_MATCH, "version": "2.15.0"}
    )
    state["version"] = "2.15.0"
    store.due("", graph, None, assets=assets)
    assert len(graph.nodes) == 2


def test_hint_fingerprint_normalizes_product_and_version() -> None:
    """Product tokens normalize case and spacing; banner or cve changes differ."""
    import modules.loop_triggers as triggers

    base = triggers.hint_fingerprint({"cve": "CVE-1", "product": "Apache Httpd", "version": "2.4.49"})
    assert triggers.hint_fingerprint({"cve": "CVE-1", "product": "apache httpd", "version": "2.4.49"}) == base
    assert triggers.hint_fingerprint({"cve": "CVE-1", "product": "Apache Httpd", "version": "2.4.50"}) != base
    assert triggers.hint_fingerprint({"cve": "CVE-2", "product": "Apache Httpd", "version": "2.4.49"}) != base


def test_prune_drops_expired_fingerprints() -> None:
    """Expired signatures leave the store; fresh ones survive pruning."""
    import modules.loop_triggers as triggers

    store = {"fp-old": 100.0, "fp-new": 10_000.0}
    pruned = triggers.prune_hint_fingerprints(store, now=10_500.0, ttl=600.0)
    assert pruned == {"fp-new": 10_000.0}


def test_hint_ttl_expires_and_refires(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """After the repeat window the same candidate is proposed again."""
    import modules.lazy_loop as loop
    import modules.loop_triggers as triggers
    import modules.world_model as world_module

    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(world_module, "get_world_model", lambda: {"hosts": {}})
    monkeypatch.setattr(
        "modules.lazy_cve_feed.hot_matches", lambda services, allow_network=False: [dict(CANNED_MATCH)]
    )
    monkeypatch.setattr(triggers, "HINT_REPEAT_TTL_SEC", 0.0)
    store = triggers.TriggerStore("")
    store.add("cve_hot", every_sec=0.0)
    graph = _Graph()
    assets = _Assets()
    store.due("", graph, None, assets=assets)
    store.due("", graph, None, assets=assets)
    assert len(graph.nodes) == 2


def test_hint_store_written_under_loop_stores(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Fingerprints persist beside the loop stores and dedupe across calls."""
    import json

    import modules.lazy_loop as loop
    import modules.loop_triggers as triggers
    import modules.world_model as world_module

    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(world_module, "get_world_model", lambda: {"hosts": {}})
    monkeypatch.setattr(
        "modules.lazy_cve_feed.hot_matches", lambda services, allow_network=False: [dict(CANNED_MATCH)]
    )
    store = triggers.TriggerStore("")
    store.add("cve_hot", every_sec=0.0)
    graph = _Graph()
    store.due("", graph, None, assets=_Assets())
    path = tmp_path / triggers.HINT_FINGERPRINT_STORE
    assert path.exists()
    payload = json.loads(path.read_text())
    assert payload and all(isinstance(v, float) for v in payload.values())
