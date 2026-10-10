"""Attack-surface 3D module: surface+intel fusion + embedded pages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.attack_surface3d import (  # noqa: E402
    build_attack_graph,
    refresh_summary,
)
from modules.intel_fusion import (  # noqa: E402
    build_analytics,
    build_bundle_payload,
    bundle_settings,
    page_settings,
)


def _fixture_sessions(tmp_path: Path) -> Path:
    """Minimal campaign: world model, implant log, objective, log mention."""
    world = {
        "phase": "enum",
        "hosts": {"10.0.0.5": {"ip": "10.0.0.5", "state": "scanned",
                               "os_hint": "linux",
                               "services": {"22": {"port": 22, "name": "ssh",
                                                   "state": "open"}}}},
        "vulnerabilities": [{"id": "v1", "title": "open ssh", "host": "10.0.0.5",
                             "severity": "critical"}],
    }
    (tmp_path / "world_model.json").write_text(json.dumps(world))
    header = "client_id,os,pid,hostname,ips,user,discovered_ips,result_portscan,command"
    row = ("beacon01,linux,1234,web01,10.0.0.9,root,\"10.0.0.5\","
           "\"{}\",whoami".format(json.dumps({"10.0.0.5": [22]}).replace('"', '""')))
    (tmp_path / "beacon01.log").write_text(header + "\n" + row + "\n")
    (tmp_path / "objectives.jsonl").write_text(
        json.dumps({"objective": "own 10.0.0.5", "status": "open"}) + "\n")
    (tmp_path / "autonomous_events.jsonl").write_text(
        json.dumps({"message": "scanned 10.0.0.5"}) + "\n")
    return tmp_path


def test_attack_fuses_surface_and_intel(tmp_path: Path) -> None:
    """C2, implant, host, service, finding, objective in one graph."""
    graph = build_attack_graph(_fixture_sessions(tmp_path))
    kinds = {n["kind"] for n in graph["nodes"] if n.get("type") == "file"}
    assert {"c2", "client", "host", "port", "objective"} <= kinds
    assert any(k.startswith("finding") for k in kinds)
    assert any(n.get("type") == "community" for n in graph["nodes"])
    assert any(n.get("type") == "layer" for n in graph["nodes"])
    assert all(e.get("evidence") and e.get("color") for e in graph["edges"])
    assert all(n.get("community") and n.get("familyColor") for n in graph["nodes"])


def test_attack_payload_readmenator_shape(tmp_path: Path) -> None:
    """Every file node carries family/layer/rank/doc for the engine."""
    graph = build_attack_graph(_fixture_sessions(tmp_path))
    files = [n for n in graph["nodes"] if n.get("type") == "file"]
    assert files
    for node in files:
        assert node.get("family") and node.get("layer") and node.get("language")
        assert node.get("rank_pos", 0) >= 0 and node.get("doc")
        assert isinstance(node.get("symbol_list"), list)
    assert any(e.get("type") == "member_of" for e in graph["edges"])
    assert any(e.get("type") == "layered_as" for e in graph["edges"])


def test_attack_bundle_payload(tmp_path: Path) -> None:
    """Bundle covers every file with circle angles and sphere points."""
    graph = build_attack_graph(_fixture_sessions(tmp_path))
    bundle = build_bundle_payload(graph)
    files = [n for n in graph["nodes"] if n.get("type") == "file"]
    assert len(bundle["nodes"]) == len(files)
    assert bundle["groups"]
    assert sum(g["n"] for g in bundle["groups"]) == len(files)
    for node in bundle["nodes"]:
        assert set(node) >= {"id", "f", "l", "g", "c", "ly", "lg", "r",
                             "rp", "fd", "d", "a", "p"}
        assert len(node["p"]) == 3
    for edge in bundle["edges"]:
        assert len(edge) == 2 and edge[0] != edge[1]
    settings = bundle_settings(graph)
    assert settings["beta"] == 0.85 and settings["explorerHref"] == "/intel"
    page = page_settings(graph)
    assert page["charge"] == -300 and page["cooldownTicks"] == 400
    assert "attribution_funnel" in build_analytics(graph, {})


def test_attack_summary_feeds_loop(tmp_path: Path) -> None:
    """Exposure summary scores the host for the autonomous planner."""
    sessions = _fixture_sessions(tmp_path)
    graph = build_attack_graph(sessions)
    summary = refresh_summary(graph, sessions)
    assert summary["top_exposed"][0]["host"] == "10.0.0.5"
    assert (sessions / "intel_summary.json").exists()
    stages = [s["stage"] for s in summary["funnel"]]
    assert stages == ["discovered", "with services", "with findings",
                      "confirmed", "owned"]
    counts = [s["hosts"] for s in summary["funnel"]]
    assert counts[0] >= counts[1] >= counts[2] >= counts[3] >= counts[4]
    assert counts[0] >= 1
    assert summary["source_yield"]


def test_attack_pages_embedded_and_wired() -> None:
    """Attack pages live in LazyOwn chrome with fetch data + engine intact."""
    force = (_ROOT / "templates" / "attack3d.html").read_text()
    assert '{% extends "base.html" %}' in force
    assert "/api/attack_graph?layout=force" in force
    assert 'location.href="/attack_bundle"' in force
    for token in ("nodeCanvasObject", "enableNodeDrag(true)", "zoomToFit",
                  "member_of", "Upstream", "Downstream", "Ports", "Confirmed",
                  "document.getElementById(\"rm-root\")"):
        assert token in force, token
    bundle = (_ROOT / "templates" / "attack_bundle.html").read_text()
    for token in ("Circle 2D", "Sphere 3D", "/api/attack_bundle", 'href="/attack3d"'):
        assert token in bundle, token
    for name in ("attack3d.html", "attack_bundle.html"):
        html = (_ROOT / "templates" / name).read_text()
        assert "{{" not in html and "{#" not in html, name
        for emoji in ("🖥", "🔥", "🔌", "⚠", "☠", "🎯", "⚙", "♛", "GLYPH"):
            assert emoji not in html, (name, emoji)


def test_attack_menu_entry_and_routes() -> None:
    """Intel dropdown links the new module; lazyc2 serves its routes."""
    base = (_ROOT / "templates" / "base.html").read_text()
    for token in ("attack3d_view", "AttackGraph 3D", "intel_bundle_view",
                  "IntelGraph Bundles", "attack_bundle_view", "AttackGraph Bundles"):
        assert token in base, token
    source = (_ROOT / "lazyc2.py").read_text()
    for token in ('"/attack3d"', '"/attack_bundle"', '"/api/attack_graph"',
                  '"/api/attack_bundle"', '"/intel_bundle"', '"/api/intel_bundle"',
                  "attack3d.html", "attack_bundle.html"):
        assert token in source, token
    assert 'render_template("surface.html")' in source
    assert 'render_template("graph.html")' in source


def test_new_endpoints_require_login_and_decoy() -> None:
    """Every new route sits behind the WEB session login + operator decoy.

    Session login (flask_login), never bare HTTP Basic: the browser shows
    the login page and logout actually revokes access.
    """
    source = (_ROOT / "lazyc2.py").read_text()
    lines = source.splitlines()
    for view in ("intel_view", "intel_bundle_view", "attack3d_view",
                 "attack_bundle_view", "api_intel_graph", "api_intel_bundle",
                 "api_attack_graph", "api_attack_bundle"):
        idx = next(i for i, line in enumerate(lines) if line.startswith(f"def {view}("))
        preceding = "\n".join(lines[max(0, idx - 4):idx])
        assert "@login_required" in preceding, view
        assert "requires_auth_or_session" not in preceding, view
        body = "\n".join(lines[idx:idx + 25])
        assert "response = decoy()" in body, view
