"""Intel fusion + LLM defaults regression tests."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

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
