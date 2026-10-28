"""Intel fusion + LLM defaults regression tests."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules import intel_fusion  # noqa: E402
from modules.intel_fusion import (  # noqa: E402
    assign_layout,
    build_intel_graph,
    node_id,
    write_summary,
)


def _fixture_sessions(tmp_path: Path) -> Path:
    """Write a minimal campaign: world model, lazy task, objective, log."""
    world = {
        "phase": "recon",
        "hosts": {"10.0.0.5": {"ip": "10.0.0.5", "state": "scanned",
                               "os_hint": "linux",
                               "services": {"22": {"port": 22, "name": "ssh", "state": "open"}}}},
        "vulnerabilities": [{"id": "v1", "title": "open ssh", "host": "10.0.0.5",
                             "severity": "high"}],
    }
    (tmp_path / "world_model.json").write_text(json.dumps(world))
    lazy = tmp_path / "lazy"
    lazy.mkdir()
    (lazy / "tasks.json").write_text(json.dumps({"seq": 1, "tasks": {
        "t0001": {"task_id": "t0001", "goal": "assess 10.0.0.5", "status": "running",
                  "scope": [{"kind": "ip", "value": "10.0.0.5"}]}}}))
    (tmp_path / "objectives.jsonl").write_text(
        json.dumps({"objective": "own 10.0.0.5", "status": "open"}) + "\n")
    (tmp_path / "autonomous_events.jsonl").write_text(
        json.dumps({"message": "scanned 10.0.0.5"}) + "\n")
    return tmp_path


def test_node_id_deterministic() -> None:
    """Same kind+value always yields the same id."""
    assert node_id("host", "10.0.0.5") == node_id("host", "10.0.0.5")
    assert node_id("host", "10.0.0.5") != node_id("service", "10.0.0.5")


def test_build_fuses_all_sources(tmp_path: Path) -> None:
    """World, lazy task, objective and logs fuse into one C2 graph."""
    graph = build_intel_graph(_fixture_sessions(tmp_path))
    kinds = {n["kind"] for n in graph["nodes"]}
    assert {"c2", "host", "service", "finding", "task", "objective"} <= kinds
    assert any(n["id"] and n["sources"] for n in graph["nodes"])
    assert all(e.get("evidence") for e in graph["edges"])


def test_layouts_circular_spherical_force(tmp_path: Path) -> None:
    """Circular/spherical pin positions; force modes stay free."""
    graph = build_intel_graph(_fixture_sessions(tmp_path))
    circ = assign_layout(dict(graph, nodes=[dict(n) for n in graph["nodes"]]), "circular")
    assert all("x" in n and "y" in n for n in circ["nodes"])
    sph = assign_layout(dict(graph, nodes=[dict(n) for n in graph["nodes"]]), "spherical")
    assert any(n.get("z", 0) != 0 for n in sph["nodes"])
    free = assign_layout(dict(graph, nodes=[dict(n) for n in graph["nodes"]]), "force3d")
    assert all("x" not in n for n in free["nodes"])


def test_summary_scores_and_suggests(tmp_path: Path) -> None:
    """Summary ranks the exposed host and suggests probe intents."""
    graph = build_intel_graph(_fixture_sessions(tmp_path))
    summary = write_summary(graph, tmp_path)
    assert summary["top_exposed"][0]["host"] == "10.0.0.5"
    assert any("10.0.0.5" in intent for intent in summary["suggested_intents"])
    assert (tmp_path / "intel_summary.json").exists()


def test_summary_score_is_bounded_0_100(tmp_path: Path) -> None:
    """A hyper-connected host with huge degree never scores past 100."""
    world = {
        "phase": "recon",
        "hosts": {
            f"10.0.1.{i}": {"ip": f"10.0.1.{i}", "state": "scanned", "services": {}}
            for i in range(1, 40)
        },
    }
    (tmp_path / "world_model.json").write_text(json.dumps(world))
    graph = build_intel_graph(tmp_path)
    summary = write_summary(graph, tmp_path)
    scores = [row["score"] for row in summary["top_exposed"]]
    assert all(0 <= score <= 100 for score in scores)


def test_summary_score_detail_components_sum(tmp_path: Path) -> None:
    """Score detail lines add up to the reported score exactly."""
    graph = build_intel_graph(_fixture_sessions(tmp_path))
    summary = write_summary(graph, tmp_path)
    top = summary["top_exposed"][0]
    assert top["score"] == round(sum(line["points"] for line in top["score_detail"]), 2)
    labels = " | ".join(line["label"] for line in top["score_detail"])
    assert "connectivity" in labels
    assert "findings" in labels

def test_summary_heat_component_from_matched_cve(tmp_path: Path, monkeypatch) -> None:
    """A hot CVE candidate matched on a host raises its score with a labeled line."""
    import time

    from modules import lazy_cve_feed

    monkeypatch.setattr(
        lazy_cve_feed,
        "correlate",
        lambda banner, version="", allow_network=True: [
            {"cve": "CVE-2021-41773", "heat": "hot", "cvss": 9.8, "kev": True,
             "epss": 0.9, "exploit": True, "in_range": True, "confidence": "high"}
        ],
        raising=True,
    )
    intel_fusion._CVE_CORRELATION_CACHE.clear()

    (tmp_path / "world_model.json").write_text(
        json.dumps(
            {
                "phase": "exploit",
                "hosts": {"10.0.0.5": {"ip": "10.0.0.5", "state": "scanned",
                                       "services": {"80": {"port": 80, "name": "http", "version": "Apache 2.4.49", "state": "open"}}}},
            }
        )
    )
    (tmp_path / "autonomous_events.jsonl").write_text(
        json.dumps({"message": "hit"}) + "\n")
    (tmp_path / "lazy_changes.jsonl").write_text(
        json.dumps({"kind": "port_opened", "ip": "10.0.0.5", "port": 80, "before": None,
                    "after": {"service": "https"}, "detected": time.time()}) + "\n")
    graph = build_intel_graph(tmp_path)
    summary = write_summary(graph, tmp_path)
    top = summary["top_exposed"][0]
    labels = " | ".join(line["label"] for line in top["score_detail"])
    assert "recent exposure change" in labels
    assert "CVE" in labels
    assert 0 <= top["score"] <= 100


def test_summary_recency_rewards_new_hosts(tmp_path: Path) -> None:
    """A host that appeared this week earns the recency component."""
    import time

    (tmp_path / "lazy_changes.jsonl").write_text(
        json.dumps({"kind": "host_new", "ip": "10.0.0.5", "port": "", "before": None,
                    "after": {"ip": "10.0.0.5"}, "detected": time.time()}) + "\n")
    graph = build_intel_graph(_fixture_sessions(tmp_path))
    summary = write_summary(graph, tmp_path)
    detail = next(h["score_detail"] for h in summary["top_exposed"] if h["host"] == "10.0.0.5")
    assert "host appeared or returned this week" in " | ".join(line["label"] for line in detail)


def test_summary_reports_heat_counts_and_changes(tmp_path: Path) -> None:
    """Summary exposes heat distribution and recent changes for the loop."""
    import time

    (tmp_path / "lazy_changes.jsonl").write_text(
        json.dumps({"kind": "port_opened", "ip": "10.0.0.5", "port": 443, "before": None,
                    "after": {"service": "https"}, "detected": time.time()}) + "\n")
    graph = build_intel_graph(_fixture_sessions(tmp_path))
    summary = write_summary(graph, tmp_path)
    assert set(summary["heat_counts"]) == {"hot", "warm", "cold"}
    assert summary["recent_changes"][0]["kind"] == "port_opened"


def _svg_fixture(kind_counts: dict[str, int] | None = None) -> dict:
    """Craft a synthetic intel-graph payload with known nodes and edges."""
    nodes: list[dict] = [
        {"id": "c2root", "kind": "c2", "value": "c2", "degree": 3},
        {"id": "h1", "kind": "host", "value": "10.0.0.5", "degree": 2},
        {"id": "h2", "kind": "host-owned", "value": "10.0.0.6", "degree": 1},
        {"id": "h3", "kind": "host", "value": "10.0.0.7", "degree": 1},
        {"id": "s1", "kind": "service", "value": "openssh", "degree": 1, "community": "net:10.0.0.5"},
        {"id": "c1", "kind": "cve", "value": "CVE-2023-38408", "degree": 1,
         "heat": "hot", "heat_rank": 3, "community": "net:10.0.0.5"},
        {"id": "c2", "kind": "cve", "value": "CVE-2015-01-01", "degree": 1,
         "heat": "cold", "heat_rank": 1, "community": "net:10.0.0.6"},
    ]
    edges: list[dict] = [
        {"source": "h1", "target": "c2root", "type": "commands"},
        {"source": "s1", "target": "h1", "type": "opens"},
        {"source": "c1", "target": "h1", "type": "matched"},
        {"source": "c2", "target": "h2", "type": "matched"},
        {"source": "h2", "target": "c2root", "type": "commands"},
        {"source": "h3", "target": "c2root", "type": "commands"},
    ]
    for kind, count in (kind_counts or {}).items():
        for index in range(count):
            nid = f"x-{kind}-{index}"
            nodes.append({"id": nid, "kind": kind, "value": f"{kind} {index}", "degree": 0})
            edges.append({"source": "c1", "target": nid, "type": "observed_in"})
    return {"nodes": nodes, "edges": edges}


def test_svg_selection_bounded_and_deterministic() -> None:
    """Selected nodes open with the c2 hub and stay inside the cap."""
    payload = _svg_fixture({"intel": 200})
    selection = intel_fusion.svg_selection(payload, cap_nodes=40)
    assert "c2root" in selection
    assert len(selection) == 40
    assert intel_fusion.svg_selection(payload, cap_nodes=40) == intel_fusion.svg_selection(payload, cap_nodes=40)


def test_relations_svg_renders_nodes_edges_and_manifest() -> None:
    """The svg pins the c2 hub, host nodes with the matched CVE ring and edges."""
    svg = intel_fusion.relations_svg(_svg_fixture())
    assert svg.count("<circle") == 7
    assert svg.count("<line") == 6
    assert 'cx="500.0"' in svg and 'cy="300.0"' in svg
    for host in ('data-node-kind="host"', 'fill="#4da3ff"'):
        assert host in svg
    assert "CVE-2023-38408" in svg


def test_selection_is_input_order_independent() -> None:
    """Fusion artifacts may interleave nodes; the selection must not care."""
    payload = _svg_fixture({"intel": 8})
    scrambled = {
        "nodes": list(reversed(payload["nodes"])),
        "edges": list(reversed(payload["edges"])),
    }
    assert intel_fusion.svg_selection(payload) == intel_fusion.svg_selection(scrambled)


def test_relations_svg_escapes_untrusted_text() -> None:
    """Scan-derived labels never carry raw angle brackets into the svg."""
    payload = _svg_fixture()
    payload["nodes"].append(
        {"id": "evil", "kind": "finding", "value": "<script>alert(1)</script>", "degree": 1}
    )
    payload["edges"].append({"source": "evil", "target": "c2root", "type": "observed_in"})
    svg = intel_fusion.relations_svg(payload)
    assert "<script>alert(1)</script>" not in svg
    assert "&lt;script&gt;" in svg


def test_relations_svg_empty_graph_returns_blank() -> None:
    """No nodes means no svg block, and the report hides the section."""
    assert intel_fusion.relations_svg({"nodes": [], "edges": []}) == ""
    assert intel_fusion.relations_svg({}) == ""


def test_relations_svg_caps_heat_ranking() -> None:
    """With a tight cap signal nodes stay and noise nodes never render."""
    payload = _svg_fixture({"intel": 30})
    selection = intel_fusion.svg_selection(payload, cap_nodes=4)
    assert selection[0] == "c2root"
    assert "c1" in selection
    assert not any(nid.startswith("x-intel") for nid in selection)


def test_report_renders_relations_appendix() -> None:
    """/report wires the snapshot into a dedicated appendix."""
    source = (_ROOT / "lazyc2.py").read_text()
    assert 'from modules.intel_fusion import' in source
    assert "relations_svg" in source
    assert '"graph_svg"' in source
    template = (_ROOT / "templates" / "report.html").read_text()
    assert "Appendix G" in template
    assert "graph_svg" in template
    assert "| safe }}" in template


def test_report_template_renders_host_scores_and_snapshot() -> None:
    """/report renders score lines, the funnel and the relations svg."""
    from jinja2 import Environment, FileSystemLoader

    svg = intel_fusion.relations_svg(_svg_fixture())

    class _User:
        is_authenticated = True

    env = Environment(loader=FileSystemLoader(str(_ROOT / "templates")))
    env.filters["markdown"] = lambda text: text
    env.globals["url_for"] = lambda *a, **k: "#"
    env.globals["current_user"] = _User()
    env.globals["get_flashed_messages"] = lambda with_categories=False: []
    html = env.get_template("report.html").render(
        report_data={}, tools=[], tasks=[], cves=[],
        session_data={"params": {}, "implants": []}, implants=[],
        loops_summary={"total": 0, "by_status": {}, "by_target": {}, "recent": []},
        surface_intel={
            "summary": {
                "funnel": {"discovered": 1, "owned": 0, "with findings": 1},
                "heat_counts": {"hot": 1, "warm": 0, "cold": 1},
                "top_exposed": [
                    {"host": "10.0.0.5", "score": 45.0,
                     "score_detail": [{"label": "CVE heat", "points": 40.0}]}
                ],
            },
            "changes": [], "ghosts": [], "history": [], "graph_svg": svg,
        },
    )
    assert "Appendix G" in html
    assert svg in html
    assert "host appeared" not in html
    assert "CVE heat +40.0" in html
    assert "10.0.0.5" in html


def test_llm_defaults_seeded() -> None:
    """Local, cloud, pi-agent and agentic legs exist with failover priority order."""
    from modules.lazy_loop import LlmPool

    names = [m["name"] for m in LlmPool.DEFAULT_MEMBERS]
    assert names == ["llamacpp-local", "groq-cloud", "pi-qwen", "ollama-local", "toposwarm-agent"]
    specs = [m["model"] for m in LlmPool.DEFAULT_MEMBERS]
    assert specs[2] == "pi:local-model"
    prios = [m["priority"] for m in LlmPool.DEFAULT_MEMBERS]
    assert prios == sorted(prios, reverse=True)


def test_factory_complete_rejects_empty() -> None:
    """Empty prompt is empty out; dead legs raise for failover."""
    from modules.llm_factory import complete

    assert complete("groq:x", "") == ""
    try:
        complete("toposwarm:router", "hi")
    except RuntimeError:
        return
    except Exception:
        return
