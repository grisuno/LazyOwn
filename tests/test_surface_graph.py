"""Tests for the network surface graph reader.

The reader composes the same picture that ``templates/index.html`` renders
with ``vis.js`` but works from the on-disk session artefacts so it can be
exercised in isolation without booting the C2 Flask server.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cli.surface_graph import (  # noqa: E402
    EDGE_CONTROLS,
    EDGE_DISCOVERED,
    EDGE_OPENS,
    EDGE_RUNS,
    NODE_C2,
    NODE_KIND_CLIENT,
    NODE_KIND_HOST,
    NODE_KIND_PORT,
    NODE_KIND_SERVICE,
    SurfaceGraphBuilder,
    SurfaceGraphConfig,
    build_surface_graph,
    iter_descendants,
)


IMPLANT_COLUMNS = (
    "client_id",
    "os",
    "pid",
    "hostname",
    "ips",
    "user",
    "discovered_ips",
    "result_portscan",
    "result_pwd",
    "command",
    "output",
)


def _write_implant_log(path: Path, **fields: str) -> None:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(IMPLANT_COLUMNS))
    writer.writeheader()
    row = {col: fields.get(col, "") for col in IMPLANT_COLUMNS}
    writer.writerow(row)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def _write_payload(tmp_path: Path, **overrides) -> Path:
    payload = {
        "lhost": "10.10.10.10",
        "c2_port": 4443,
        "domain": "lab.local",
    }
    payload.update(overrides)
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")
    return payload_path


def _build(tmp_path: Path, sessions: Path) -> SurfaceGraphConfig:
    payload_path = _write_payload(tmp_path)
    return SurfaceGraphConfig(sessions_dir=str(sessions), payload_path=str(payload_path))


@pytest.fixture()
def sessions_dir(tmp_path: Path) -> Path:
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    return sessions


def test_empty_sessions_still_produce_c2_root(tmp_path: Path, sessions_dir: Path) -> None:
    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()

    assert any(node.id == NODE_C2 for node in graph.nodes)
    assert graph.get(NODE_C2).kind == "c2"
    assert graph.stats().get("edges") == 0


def test_hostsdiscovery_populates_host_nodes(tmp_path: Path, sessions_dir: Path) -> None:
    (sessions_dir / "hostsdiscovery.txt").write_text(
        "10.0.0.1\n10.0.0.2\n\nnot-an-ip\n10.0.0.1\n",
        encoding="utf-8",
    )
    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()

    host_ids = {node.id for node in graph.nodes if node.kind == NODE_KIND_HOST}
    assert host_ids == {"host-10-0-0-1", "host-10-0-0-2"}
    assert all(
        edge.source == NODE_C2 and edge.relation == EDGE_DISCOVERED
        for edge in graph.edges
        if edge.target.startswith("host-")
    )


def test_scan_discovery_csv_adds_ports_and_services(tmp_path: Path, sessions_dir: Path) -> None:
    (sessions_dir / "scan_discovery_lab.csv").write_text(
        '"IP";"FQDN";"PORT";"PROTOCOL";"SERVICE";"VERSION"\n'
        '"10.0.0.5";"dc01.lab";"445";"tcp";"microsoft-ds";"Samba 4.15"\n'
        '"10.0.0.5";"dc01.lab";"88";"tcp";"kerberos-sec";""\n'
        '"10.0.0.6";"";"";"";"";""\n',
        encoding="utf-8",
    )
    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()

    host_dc = graph.get("host-10-0-0-5")
    assert host_dc is not None
    assert host_dc.metadata.get("fqdn") == "dc01.lab"

    port_ids = {node.id for node in graph.nodes if node.kind == NODE_KIND_PORT}
    assert "port-host-10-0-0-5-tcp-445" in port_ids
    assert "port-host-10-0-0-5-tcp-88" in port_ids

    service_nodes = [node for node in graph.nodes if node.kind == NODE_KIND_SERVICE]
    assert any(node.metadata["service"] == "microsoft-ds" for node in service_nodes)
    assert any(edge.relation == EDGE_OPENS for edge in graph.edges)
    assert any(edge.relation == EDGE_RUNS for edge in graph.edges)


def test_implant_log_creates_client_and_links_hosts(tmp_path: Path, sessions_dir: Path) -> None:
    client_id = "beacon-7f3a"
    log_path = sessions_dir / f"{client_id}.log"
    portscan = json.dumps({"10.0.0.5": [22, 80, 22], "10.0.0.6": [3389]})
    _write_implant_log(
        log_path,
        client_id=client_id,
        os="linux",
        pid="1234",
        hostname="box01",
        ips="10.0.0.99",
        user="root",
        discovered_ips="10.0.0.5,10.0.0.6",
        result_portscan=portscan,
        command="whoami",
        output="root",
    )

    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()

    client_node = graph.get(client_id)
    assert client_node is not None
    assert client_node.kind == NODE_KIND_CLIENT
    assert client_node.metadata["hostname"] == "box01"
    assert client_node.metadata["user"] == "root"
    assert sorted(client_node.metadata["discovered_ip_list"]) == ["10.0.0.5", "10.0.0.6"]
    assert client_node.metadata["port_map"] == {"10.0.0.5": [22, 80], "10.0.0.6": [3389]}

    assert any(
        edge.source == NODE_C2 and edge.target == client_id and edge.relation == EDGE_CONTROLS
        for edge in graph.edges
    )
    assert any(
        edge.source == client_id and edge.target == "host-10-0-0-5" and edge.relation == EDGE_DISCOVERED
        for edge in graph.edges
    )

    port_ids = {node.id for node in graph.nodes if node.kind == NODE_KIND_PORT}
    assert "port-host-10-0-0-5-tcp-22" in port_ids
    assert "port-host-10-0-0-5-tcp-80" in port_ids
    assert "port-host-10-0-0-6-tcp-3389" in port_ids


def test_non_implant_logs_are_ignored(tmp_path: Path, sessions_dir: Path) -> None:
    (sessions_dir / "access.log").write_text("not csv at all\n", encoding="utf-8")
    (sessions_dir / "scan_192.168.1.1.nmap.xml_searchsploit.log").write_text(
        "ssploit data\n", encoding="utf-8"
    )
    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()

    assert not any(node.kind == NODE_KIND_CLIENT for node in graph.nodes)


def test_to_dict_round_trips_through_json(tmp_path: Path, sessions_dir: Path) -> None:
    (sessions_dir / "hostsdiscovery.txt").write_text("10.0.0.1\n", encoding="utf-8")
    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()
    encoded = json.dumps(graph.to_dict())
    decoded = json.loads(encoded)

    assert {"nodes", "edges", "local_ips", "sessions_dir", "stats"}.issubset(decoded)
    assert any(n["id"] == "host-10-0-0-1" for n in decoded["nodes"])


def test_iter_descendants_walks_only_outgoing_edges(tmp_path: Path, sessions_dir: Path) -> None:
    (sessions_dir / "hostsdiscovery.txt").write_text("10.0.0.1\n", encoding="utf-8")
    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()

    reachable = {node.id for node in iter_descendants(graph, NODE_C2)}
    assert "host-10-0-0-1" in reachable
    assert NODE_C2 not in reachable


def test_build_surface_graph_factory_works_without_payload_file(tmp_path: Path, sessions_dir: Path) -> None:
    graph = build_surface_graph(
        sessions_dir=str(sessions_dir),
        payload_path=str(tmp_path / "missing.json"),
    )
    assert graph.get(NODE_C2) is not None


def test_invalid_portscan_blob_does_not_crash(tmp_path: Path, sessions_dir: Path) -> None:
    client_id = "beacon-bad"
    log_path = sessions_dir / f"{client_id}.log"
    _write_implant_log(
        log_path,
        client_id=client_id,
        os="linux",
        pid="1",
        hostname="h",
        ips="1.1.1.1",
        user="r",
        discovered_ips="1.1.1.2",
        result_portscan="not json at all",
        command="id",
        output="uid=0",
    )
    cfg = _build(tmp_path, sessions_dir)
    graph = SurfaceGraphBuilder(cfg).build()
    client = graph.get(client_id)
    assert client is not None
    assert client.metadata["port_map"] == {}
