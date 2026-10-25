"""Estorides OSINT fusion: load, merge, surface readers."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.estorides_fusion import (  # noqa: E402
    community_for,
    find_export,
    load_export,
    merge_estorides,
)
from modules.surface_ops import (  # noqa: E402
    discovery_targets,
    is_ipv4,
    parse_confirm,
    write_world_model_hosts,
)


def _load_surface_graph():
    """Import cli/surface_graph.py by path (no cmd2 package import)."""
    spec = importlib.util.spec_from_file_location("surface_graph_standalone", _ROOT / "cli" / "surface_graph.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _base_nodes() -> dict:
    """One existing host node as built by the graph builders."""
    return {
        "host-10-0-0-5": {
            "id": "host-10-0-0-5",
            "kind": "host",
            "value": "10.0.0.5",
            "label": "10.0.0.5",
            "community": "net:10.0.0.5",
            "sources": ["surface"],
        }
    }


def test_load_lazyown_vocabulary(tmp_path: Path) -> None:
    """The estorides --export lazyown file loads verbatim."""
    payload = {
        "source": "estorides",
        "nodes": [
            {
                "kind": "host",
                "etype": "ipv4",
                "value": "10.0.0.5",
                "label": "10.0.0.5",
                "sources": ["shodan"],
                "attrs": {},
            }
        ],
        "edges": [],
    }
    path = tmp_path / "estorides_lazyown.json"
    path.write_text(json.dumps(payload))
    loaded = load_export(path)
    assert loaded["nodes"][0]["kind"] == "host"
    assert loaded["nodes"][0]["sources"] == ["shodan"]


def test_load_raw_export_translates_types(tmp_path: Path) -> None:
    """Raw export_json documents map to LazyOwn kinds."""
    payload = {
        "name": "estorides",
        "nodes": [
            {"id": "ipv4:10.0.0.9", "type": "ipv4", "value": "10.0.0.9", "sources": ["censys"]},
            {"id": "cve:CVE-2024-1", "type": "cve", "value": "CVE-2024-1", "sources": ["nvd"]},
        ],
        "edges": [{"source": "ipv4:10.0.0.9", "target": "cve:CVE-2024-1", "relation": "affected_by"}],
    }
    path = tmp_path / "estorides_graph.json"
    path.write_text(json.dumps(payload))
    loaded = load_export(path)
    kinds = {n["kind"] for n in loaded["nodes"]}
    assert {"host", "finding"} <= kinds
    assert loaded["edges"][0]["type"] == "observed_in"


def test_merge_fuses_matching_ip() -> None:
    """Same IP fuses records instead of duplicating nodes."""
    nodes = _base_nodes()
    edges: list = []
    est = {
        "nodes": [
            {
                "kind": "host",
                "etype": "ipv4",
                "value": "10.0.0.5",
                "label": "10.0.0.5",
                "sources": ["shodan"],
                "attrs": {"os": "linux"},
            }
        ],
        "edges": [],
    }
    stats = merge_estorides(nodes, edges, est)
    assert stats["fused"] == 1 and stats["added"] == 0
    assert len(nodes) == 1
    node = nodes["host-10-0-0-5"]
    assert "estorides" in node["sources"] and "shodan" in node["sources"]
    assert node["os"] == "linux"


def test_merge_adds_new_entities_capped() -> None:
    """Unknown entities arrive tagged until the cap."""
    nodes = _base_nodes()
    edges: list = []
    est = {
        "nodes": [
            {
                "kind": "domain",
                "etype": "domain",
                "value": "Example.COM ",
                "label": "Example.COM",
                "sources": ["crtsh"],
                "attrs": {},
            }
        ],
        "edges": [],
    }
    stats = merge_estorides(nodes, edges, est, cap=1)
    assert stats["added"] == 1
    added = nodes["est:domain:example.com"]
    assert added["community"] == "intel"
    assert added["familyColor"]
    assert community_for("host", "10.0.0.9") == "net:10.0.0.9"


def test_merge_edges_reanchor(tmp_path: Path) -> None:
    """Estorides relations re-anchor on fused ids, never on ghosts."""
    nodes = _base_nodes()
    edges: list = []
    est = {
        "nodes": [
            {"kind": "host", "etype": "ipv4", "value": "10.0.0.5", "label": "10.0.0.5", "sources": [], "attrs": {}},
            {
                "kind": "finding",
                "etype": "cve",
                "value": "CVE-2024-1",
                "label": "CVE-2024-1",
                "sources": [],
                "attrs": {},
            },
        ],
        "edges": [
            {
                "source_kind": "host",
                "source_value": "10.0.0.5",
                "target_kind": "finding",
                "target_value": "CVE-2024-1",
                "type": "affected_by",
                "evidence": "estorides:x",
            },
            {
                "source_kind": "host",
                "source_value": "ghost",
                "target_kind": "finding",
                "target_value": "CVE-2024-1",
                "type": "affected_by",
                "evidence": "estorides:x",
            },
        ],
    }
    stats = merge_estorides(nodes, edges, est)
    assert stats["edges"] == 1
    assert edges[0]["source"] == "host-10-0-0-5"
    assert edges[0]["type"] == "observed_in"


def test_find_export_prefers_lazyown(tmp_path: Path) -> None:
    """No export anywhere resolves to None instead of raising."""
    assert find_export(tmp_path) is None


def test_parse_confirm() -> None:
    """Only affirmative answers launch scans."""
    assert parse_confirm("y") and parse_confirm("YES")
    assert not parse_confirm("n") and not parse_confirm("")
    assert is_ipv4("10.0.0.5") and not is_ipv4("999.1.1.1")


def test_discovery_targets_reads_all_files(tmp_path: Path) -> None:
    """hostsdiscovery + hosts_*_discovery files all contribute."""
    (tmp_path / "hostsdiscovery.txt").write_text("10.0.0.1\nnot-an-ip\n")
    (tmp_path / "hosts_10.0.0.0_24_discovery.txt").write_text("10.0.0.2\n10.0.0.1\n")
    assert discovery_targets(tmp_path) == ["10.0.0.1", "10.0.0.2"]


def test_write_world_model_hosts(tmp_path: Path) -> None:
    """Unknown estorides IPs append, known ones never duplicate."""
    from modules.world_model import read_state_dict

    world = {"hosts": {"10.0.0.1": {"ip": "10.0.0.1"}}}
    (tmp_path / "world_model.json").write_text(json.dumps(world))
    document = {
        "nodes": [
            {"kind": "host", "value": "10.0.0.2"},
            {"kind": "host", "value": "10.0.0.1"},
            {"kind": "domain", "value": "example.com"},
        ]
    }
    assert write_world_model_hosts(document, tmp_path) == 1
    reread = read_state_dict(tmp_path / "world_model.json")
    assert reread["hosts"]["10.0.0.2"]["state"] == "estorides"


def test_surface_readers_cover_sessions_formats(tmp_path: Path) -> None:
    """CSV scans, nmap normal output and discovery globs all parse."""
    sg = _load_surface_graph()
    (tmp_path / "hosts_net_discovery.txt").write_text("10.9.0.1\n")
    (tmp_path / "scan_x.csv").write_text(
        '"IP";"FQDN";"PORT";"PROTOCOL";"SERVICE";"VERSION"\n"10.9.0.2";"web";"80";"tcp";"http";"nginx"\n'
    )
    (tmp_path / "scan_y.nmap").write_text(
        "Nmap scan report for 10.9.0.3\nPORT     STATE SERVICE\n22/tcp   open  ssh\n80/tcp   closed http\n"
    )
    builder = sg.SurfaceGraphBuilder(sg.SurfaceGraphConfig(sessions_dir=str(tmp_path)))
    graph = builder.build()
    hosts = sorted(n.metadata.get("ip", "") for n in graph.nodes if n.kind == "host")
    assert "10.9.0.1" in hosts and "10.9.0.2" in hosts and "10.9.0.3" in hosts
    ports = sorted(str(n.metadata.get("port")) for n in graph.nodes if n.kind == "port")
    assert "80" in ports and "22" in ports
    assert "443" not in ports
