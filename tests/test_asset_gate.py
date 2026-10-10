"""Asset gate + un-nerfed outputs + IntelGraph CSP regression tests."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

import pytest

import modules.lazy_loop as loop
from modules.lazy_loop import AssetGate


@pytest.fixture()
def gate_env(tmp_path, monkeypatch):
    """Isolate the JSON stores so gate tests never touch sessions/."""
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


def test_gate_exact_and_fuzzy_match(gate_env) -> None:
    """Exact hits only on equality; fuzzy hits on substring."""
    gate = AssetGate()
    gate.add("exact_ip", "10.0.0.5", "lab")
    assert gate.evaluate("10.0.0.5")["allowed"] is False
    assert gate.evaluate("10.0.0.6")["allowed"] is True
    gate.add("fuzzy_domain", ".gov", "no gov")
    assert gate.evaluate("target.gov")["allowed"] is False
    assert gate.evaluate("example.com")["allowed"] is True


def test_gate_cidr_match(gate_env) -> None:
    """CIDR rules contain member IPs only."""
    AssetGate().add("cidr", "192.168.1.0/24", "lan")
    assert AssetGate().evaluate("192.168.1.50")["allowed"] is False
    assert AssetGate().evaluate("192.168.2.50")["allowed"] is True


def test_gate_task_allow_is_closed_whitelist(gate_env) -> None:
    """A non-empty task allow-list denies everything outside it."""
    gate = AssetGate("t0001")
    assert gate.evaluate("10.0.0.9")["allowed"] is True
    gate.add("exact_ip", "10.0.0.9", "only this", action="allow")
    from modules.lazy_loop import AssetGate as _G

    task_gate = _G("t0001")
    assert task_gate.evaluate("10.0.0.9")["allowed"] is True
    verdict = task_gate.evaluate("10.0.0.10")
    assert verdict["allowed"] is False
    assert "allow-list" in verdict["reason"]


def test_gate_blocks_asset_insert(gate_env) -> None:
    """Inserting a gated asset raises instead of polluting the graph."""
    AssetGate().add("exact_ip", "10.9.9.9", "blocked")
    assets = loop.AssetGraph()
    with pytest.raises(ValueError):
        assets.insert("ip", "10.9.9.9")
    assert assets.insert("ip", "10.9.9.10").value == "10.9.9.10"


def test_lazy_gate_surface() -> None:
    """The lazy_gate verb exists with block/allow management."""
    import cli.commands.lazyops as lazyops

    assert hasattr(lazyops.LazyCommandSet, "do_lazy_gate")
    assert hasattr(lazyops.LazyCommandSet, "do_lazy_archive")
    assert hasattr(lazyops.LazyCommandSet, "do_lazy_scheduler")


def test_traffic_clear(gate_env) -> None:
    """Clearing drops the stream and reports the discarded count."""
    traffic = loop.TrafficLog("gate-test")
    traffic.record("bash", "nmap 10.0.0.1", "open")
    assert traffic.clear() == 1
    assert traffic.read() == []


def test_intel_template_uses_vendored_libs() -> None:
    """IntelGraph must not depend on CDN scripts (CSP blocks unpkg)."""
    html = (_ROOT / "templates" / "intel.html").read_text()
    assert "unpkg.com" not in html
    assert "cdn.jsdelivr.net" not in html
    assert "force-graph-1.43.5.min.js" in html
    assert "3d-force-graph-1.73.4.min.js" in html
    assert (_ROOT / "static" / "js" / "force-graph-1.43.5.min.js").stat().st_size > 100000
    assert (_ROOT / "static" / "js" / "3d-force-graph-1.73.4.min.js").stat().st_size > 100000


def test_intel_template_embedded_in_lazyown_chrome() -> None:
    """Graph pages live inside the LazyOwn layout, engine untouched by Jinja."""
    for name in ("intel.html", "attack3d.html", "intel_bundle.html", "attack_bundle.html"):
        html = (_ROOT / "templates" / name).read_text()
        assert '{% extends "base.html" %}' in html, name
        assert "{% block content %}" in html, name
        assert 'id="rm-root"' in html, name
        assert "{{" not in html, name
        assert "{#" not in html, name
        assert "|tojson" not in html, name


def test_intel_template_maps_edges_to_links() -> None:
    """force-graph consumes {nodes, links}; raw {nodes, edges} crashes tickFrame."""
    html = (_ROOT / "templates" / "intel.html").read_text()
    assert "links:" in html
    assert "graphData" in html
    assert "/api/intel_graph?layout=force" in html


def test_intel_template_readmenator_grade() -> None:
    """ReadMenator engine: glyphs, labels, halos, communities, drag, fit."""
    html = (_ROOT / "templates" / "intel.html").read_text()
    for token in ("nodeCanvasObject", "graph2ScreenCoords", "enableNodeDrag",
                  "zoomToFit", "Halos", "inspector", "member_of",
                  "data-color", "Top exposed", "Suggested intents",
                  "Confirmed", "funnel:"):
        assert token in html, token
    for emoji in ("🖥", "🔥", "🔌", "⚠", "☠", "🎯", "⚙", "♛", "GLYPH"):
        assert emoji not in html, emoji


def test_intel_nodes_carry_community() -> None:
    """Every fused node joins a community with a stable family color."""
    from modules.intel_fusion import build_intel_graph

    graph = build_intel_graph()
    assert graph["nodes"]
    assert all(n.get("community") and n.get("familyColor") for n in graph["nodes"])
    assert "core" in graph["stats"]["communities"]


def test_intel_payload_readmenator_shape() -> None:
    """Payload mirrors ForceGraphRenderer: type/file/layer/rank + hubs."""
    from modules.intel_fusion import build_analytics, build_intel_graph, page_settings

    graph = build_intel_graph()
    files = [n for n in graph["nodes"] if n.get("type") == "file"]
    assert files
    for node in files:
        assert node.get("family") and node.get("layer")
        assert node.get("rank_pos", 0) >= 0 and node.get("doc")
    assert any(n.get("type") == "community" for n in graph["nodes"])
    assert any(n.get("type") == "layer" for n in graph["nodes"])
    assert any(e.get("type") == "member_of" for e in graph["edges"])
    settings = page_settings(graph)
    assert settings["charge"] == -300 and settings["linkDistance"] == 120
    assert settings["nodeRelSize"] == 4 and settings["cooldownTicks"] == 400
    assert settings["fitMaxZoom"] == 2.5 and settings["fitPad"] == 48
    analytics = build_analytics(graph, {})
    assert "attribution_funnel" in analytics


def test_compact_unfolded_cap_and_flag(gate_env) -> None:
    """Unfolded view caps at 60 and reports truncation honestly."""
    from modules.lazy_loop import ActivityLog, ColdCompactor, ExplorationGraph

    graph = ExplorationGraph("unfold-test")
    for i in range(70):
        node = graph.add_node("fact", f"cold fact {i}", state="done")
        node.meta["cold"] = True
        node.state = "exhausted"
    graph._persist()
    unfolded = ColdCompactor(graph, ActivityLog("unfold-test")).unfolded()
    assert unfolded["total"] == 70
    assert len(unfolded["facts"]) == 60
    assert unfolded["truncated"] is True
    assert ColdCompactor(graph, ActivityLog("unfold-test")).unfolded(limit=500)["truncated"] is False


def test_digest_overview_expandable(gate_env) -> None:
    """Overview indexes expandable digests and covered lineage."""
    from modules.lazy_loop import ActivityLog, ColdCompactor, ExplorationGraph

    graph = ExplorationGraph("overview-test")
    members = [graph.add_node("fact", f"member {i}", state="done").node_id for i in range(3)]
    digest = graph.add_node("fact", "cold digest", state="done",
                            meta={"cold_digest": True, "mode": "minor", "members": members})
    for mid in members:
        node = graph.get(mid)
        node.meta["cold"] = True
        node.state = "exhausted"
    graph._persist()
    view = ColdCompactor(graph, ActivityLog("overview-test")).digest_overview()
    assert view["covered"] == 3
    assert digest.node_id in view["expandable"]
    assert ColdCompactor(graph, ActivityLog("overview-test")).expand(digest.node_id) == members
    assert ColdCompactor(graph, ActivityLog("overview-test")).digest_overview()["expandable"] == []


def test_hot_facts_never_truncated(gate_env) -> None:
    """Hot view returns the full hot set beyond the page cap."""
    from modules.lazy_loop import ExplorationGraph

    graph = ExplorationGraph("hot-test")
    for i in range(65):
        graph.add_node("fact", f"hot fact {i}", state="done")
    assert len(graph.list_facts()) == 50
    assert len(graph.list_facts(hot_full=True)) == 65
