"""Tests for lazygui domain models.

Covers GraphNode, GraphEdge, Topology, BeaconResult, DashboardPayload,
CampaignSummary, EventRecord, Session, Listener, Operator, and their
behavioural contracts.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

pytest.importorskip("PySide6")

from lazygui.services.models import (
    BackendKind,
    BeaconResult,
    CampaignSummary,
    DashboardPayload,
    EventLevel,
    EventRecord,
    GraphEdge,
    GraphNode,
    Session,
    Topology,
)


class TestGraphNode:
    """GraphNode contract: identifier, label, type, colour and metadata."""

    def test_minimal_construction(self) -> None:
        node = GraphNode(identifier="c2", label="C2", node_type="c2")
        assert node.identifier == "c2"
        assert node.label == "C2"
        assert node.node_type == "c2"
        assert node.shape == "dot"
        assert node.color == "#58a6ff"

    def test_full_construction(self) -> None:
        node = GraphNode(
            identifier="beacon1",
            label="WIN-DC01",
            node_type="beacon",
            shape="circle",
            color="#3fb950",
            icon="/icons/win.png",
            metadata={"os": "windows", "version": "10.0.19041"},
        )
        assert node.shape == "circle"
        assert node.color == "#3fb950"
        assert node.icon == "/icons/win.png"
        assert node.metadata["os"] == "windows"

    def test_default_metadata(self) -> None:
        node = GraphNode(identifier="h", label="h", node_type="host")
        assert isinstance(node.metadata, dict)
        assert len(node.metadata) == 0

    def test_equality(self) -> None:
        a = GraphNode(identifier="a", label="a", node_type="host")
        b = GraphNode(identifier="a", label="a", node_type="host")
        c = GraphNode(identifier="a", label="a", node_type="beacon")
        assert a == b
        assert a != c

    def test_immutable(self) -> None:
        node = GraphNode(identifier="n", label="n", node_type="host")
        with pytest.raises(Exception):
            node.identifier = "x"  # type: ignore[misc]


class TestGraphEdge:
    """GraphEdge contract: source, target, label, type and colour."""

    def test_construction(self) -> None:
        edge = GraphEdge(
            source_id="c2",
            target_id="beacon1",
            label="HTTPS",
            edge_type="c2",
            color="#ff9e3b",
        )
        assert edge.source_id == "c2"
        assert edge.target_id == "beacon1"
        assert edge.label == "HTTPS"
        assert edge.edge_type == "c2"
        assert edge.color == "#ff9e3b"

    def test_defaults(self) -> None:
        edge = GraphEdge(source_id="a", target_id="b")
        assert edge.label == ""
        assert edge.edge_type == "default"
        assert edge.color == "#30363d"

    def test_equality(self) -> None:
        a = GraphEdge(source_id="x", target_id="y")
        b = GraphEdge(source_id="x", target_id="y")
        c = GraphEdge(source_id="x", target_id="z")
        assert a == b
        assert a != c


class TestTopology:
    """Topology contract: collection of nodes and edges."""

    def test_empty_topology(self) -> None:
        t = Topology()
        assert isinstance(t.nodes, tuple)
        assert isinstance(t.edges, tuple)
        assert len(t.nodes) == 0
        assert len(t.edges) == 0

    def test_empty_classmethod(self) -> None:
        t = Topology.empty()
        assert len(t.nodes) == 0
        assert len(t.edges) == 0

    def test_populated_topology(self) -> None:
        nodes = (
            GraphNode(identifier="c2", label="C2", node_type="c2"),
            GraphNode(identifier="b1", label="Beacon1", node_type="beacon"),
        )
        edges = (GraphEdge(source_id="c2", target_id="b1"),)
        t = Topology(nodes=nodes, edges=edges)
        assert len(t.nodes) == 2
        assert len(t.edges) == 1

    def test_equality(self) -> None:
        a = Topology()
        b = Topology.empty()
        c = Topology(nodes=(GraphNode(identifier="x", label="x", node_type="host"),))
        assert a == b
        assert a != c

    def test_empty_list_keywords(self) -> None:
        t = Topology(nodes=[], edges=[])
        assert len(t.nodes) == 0
        assert len(t.edges) == 0


class TestBeaconResult:
    """BeaconResult contract: command execution result from a beacon."""

    def test_minimal_construction(self) -> None:
        result = BeaconResult(client_id="abc", output="whoami\nroot", command="whoami")
        assert result.client_id == "abc"
        assert result.output == "whoami\nroot"
        assert result.command == "whoami"
        assert result.operating_system == ""
        assert result.hostname == ""

    def test_full_construction(self) -> None:
        result = BeaconResult(
            client_id="x",
            output="ls\ntmp",
            command="ls",
            operating_system="linux",
            hostname="web01",
            user="root",
            ips="10.0.0.5",
            pid="1234",
            discovered_ips="10.0.0.6",
            result_portscan="22,80,443",
            result_pwd="/etc/shadow",
        )
        assert result.operating_system == "linux"
        assert result.hostname == "web01"
        assert result.user == "root"
        assert result.pid == "1234"
        assert result.discovered_ips == "10.0.0.6"

    def test_equality(self) -> None:
        a = BeaconResult(client_id="1", output="a", command="a")
        b = BeaconResult(client_id="1", output="a", command="a")
        c = BeaconResult(client_id="2", output="a", command="a")
        assert a == b
        assert a != c

    def test_empty_fields_default_to_empty_string(self) -> None:
        result = BeaconResult(client_id="c", output="o", command="c")
        for attr in ("operating_system", "hostname", "user", "ips", "pid", "discovered_ips", "result_portscan", "result_pwd"):
            assert getattr(result, attr) == ""


class TestDashboardPayload:
    """DashboardPayload contract: aggregated dashboard snapshot."""

    def test_defaults(self) -> None:
        d = DashboardPayload()
        assert d.connected_clients == ()
        assert d.beacon_count == 0
        assert d.events == ()
        assert d.facts_count == 0

    def test_populated(self) -> None:
        events = (EventRecord.now(EventLevel.INFO, "test", "msg"),)
        d = DashboardPayload(beacon_count=5, events=events, facts_count=12)
        assert d.beacon_count == 5
        assert len(d.events) == 1
        assert d.facts_count == 12

    def test_equality(self) -> None:
        a = DashboardPayload()
        b = DashboardPayload()
        c = DashboardPayload(beacon_count=3)
        assert a == b
        assert a != c


class TestCampaignSummary:
    """CampaignSummary contract: campaign status from backend."""

    def test_defaults(self) -> None:
        c = CampaignSummary(identifier="c1", name="Test", status="active", playbook="apt29")
        assert c.identifier == "c1"
        assert c.name == "Test"
        assert c.status == "active"
        assert c.playbook == "apt29"
        assert c.objectives_total == 0
        assert c.objectives_completed == 0
        assert c.target_count == 0

    def test_with_counts(self) -> None:
        c = CampaignSummary(
            identifier="c2", name="Op Alpha", status="running", playbook="apt29",
            objectives_total=10, objectives_completed=3, target_count=5,
        )
        assert c.objectives_total == 10
        assert c.objectives_completed == 3
        assert c.target_count == 5

    def test_equality(self) -> None:
        a = CampaignSummary(identifier="c", name="n", status="s", playbook="p")
        b = CampaignSummary(identifier="c", name="n", status="s", playbook="p")
        c = CampaignSummary(identifier="d", name="n", status="s", playbook="p")
        assert a == b
        assert a != c


class TestEventRecord:
    """EventRecord contract: timestamped log entry."""

    def test_now_uses_utc(self) -> None:
        record = EventRecord.now(EventLevel.INFO, "src", "msg")
        assert record.timestamp.tzinfo == UTC

    def test_fields(self) -> None:
        ts = datetime(2026, 1, 1, tzinfo=UTC)
        record = EventRecord(timestamp=ts, level=EventLevel.ERROR, source="beacon", message="fail")
        assert record.timestamp == ts
        assert record.level == EventLevel.ERROR
        assert record.source == "beacon"
        assert record.message == "fail"

    def test_numeric_levels(self) -> None:
        assert EventLevel.DEBUG.numeric == 0
        assert EventLevel.INFO.numeric == 1
        assert EventLevel.WARNING.numeric == 2
        assert EventLevel.ERROR.numeric == 3
        assert EventLevel.CRITICAL.numeric == 4
        assert EventLevel.ERROR.numeric > EventLevel.INFO.numeric


class TestSessionModel:
    """Session model contract."""

    def test_construction(self) -> None:
        s = Session(
            identifier="abc", hostname="web01", operating_system="linux",
            process_id="1234", user="root", ip_addresses="10.0.0.5",
            discovered_ips="10.0.0.6", last_command="whoami",
        )
        assert s.identifier == "abc"
        assert s.hostname == "web01"
        assert s.operating_system == "linux"

    def test_metadata_default(self) -> None:
        s = Session("id", "h", "os", "1", "u", "1.1.1.1", "2.2.2.2", "")
        assert isinstance(s.metadata, dict)


class TestBackendKind:
    """BackendKind enum contract."""

    def test_values(self) -> None:
        assert BackendKind.LOCAL == "local"
        assert BackendKind.TEAMSERVER == "teamserver"

    def test_str_compat(self) -> None:
        assert str(BackendKind.LOCAL) == "local"


class TestEventLevel:
    """EventLevel enum contract."""

    def test_order(self) -> None:
        levels = list(EventLevel)
        numeric = [lvl.numeric for lvl in levels]
        assert numeric == sorted(numeric)

    def test_compare(self) -> None:
        assert EventLevel.DEBUG.numeric < EventLevel.CRITICAL.numeric
        assert EventLevel.ERROR.numeric > EventLevel.WARNING.numeric
