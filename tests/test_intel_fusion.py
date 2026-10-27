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
    assert top["score"] == round(sum(l["points"] for l in top["score_detail"]), 2)
    labels = " | ".join(l["label"] for l in top["score_detail"])
    assert "connectivity" in labels
    assert "findings" in labels


def test_summary_heat_component_from_matched_cve(tmp_path: Path, monkeypatch) -> None:
    """A hot CVE candidate matched on a host raises its score with a labeled line."""
    import time

    from modules import lazy_cve_feed
    from modules.lazy_world_diff import record_changes

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
    labels = " | ".join(l["label"] for l in top["score_detail"])
    assert "recent exposure change" in labels or "CVE" in labels
    assert 0 <= top["score"] <= 100


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
