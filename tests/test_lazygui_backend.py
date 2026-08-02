"""Tests for lazygui backend services.

Covers Backend, TeamserverBackend, TeamserverCredentials, BackendStatus,
BackendDescriptor, and backend signal contracts.
"""

from __future__ import annotations

import pytest

from PySide6.QtCore import QObject

from lazygui.config.constants import AppConstants
from lazygui.services.backend import Backend, BackendDescriptor, BackendStatus
from lazygui.services.models import (
    BeaconResult,
    CampaignSummary,
    DashboardPayload,
    EventLevel,
    EventRecord,
    GraphEdge,
    GraphNode,
    Operator,
    Session,
    Topology,
)
from lazygui.services.teamserver_backend import TeamserverCredentials, TeamserverBackend
from lazygui.services.models import Listener as ListenerModel


class TestBackendDescriptor:
    """BackendDescriptor is a read-only identifier for backends."""

    def test_construction(self) -> None:
        d = BackendDescriptor(identifier="local", display_name="Local", summary="PTY console")
        assert d.identifier == "local"
        assert d.display_name == "Local"
        assert d.summary == "PTY console"

    def test_immutable(self) -> None:
        d = BackendDescriptor(identifier="x", display_name="y", summary="z")
        with pytest.raises(Exception):
            d.identifier = "new"  # type: ignore[misc]


class TestBackendStatus:
    """BackendStatus enum lifecycle states."""

    def test_values(self) -> None:
        assert BackendStatus.DISCONNECTED == "disconnected"
        assert BackendStatus.CONNECTING == "connecting"
        assert BackendStatus.CONNECTED == "connected"
        assert BackendStatus.DEGRADED == "degraded"
        assert BackendStatus.ERROR == "error"


class TestTeamserverCredentials:
    """TeamserverCredentials immutable connection params."""

    def test_construction(self) -> None:
        creds = TeamserverCredentials(
            base_url="https://127.0.0.1:4444",
            username="op",
            password="secret",
            verify_tls=False,
        )
        assert creds.base_url == "https://127.0.0.1:4444"
        assert creds.username == "op"
        assert creds.password == "secret"
        assert creds.verify_tls is False

    def test_default_tls(self) -> None:
        creds = TeamserverCredentials(base_url="http://x", username="u", password="p")
        assert creds.verify_tls is False

    def test_immutable(self) -> None:
        creds = TeamserverCredentials(base_url="a", username="b", password="c")
        with pytest.raises(Exception):
            creds.password = "new"  # type: ignore[misc]


class TestBackendSignals:
    """Backend emits Qt signals with correct types."""

    def test_signals_exist(self) -> None:
        b = self._make_backend()
        assert hasattr(b, "status_changed")
        assert hasattr(b, "terminal_output")
        assert hasattr(b, "sessions_changed")
        assert hasattr(b, "listeners_changed")
        assert hasattr(b, "operator_changed")
        assert hasattr(b, "event_logged")
        assert hasattr(b, "topology_changed")
        assert hasattr(b, "dashboard_updated")
        assert hasattr(b, "beacon_result")
        assert hasattr(b, "campaign_changed")

    def test_initial_status_is_disconnected(self) -> None:
        b = self._make_backend()
        assert b.status == BackendStatus.DISCONNECTED

    def test_status_transition(self) -> None:
        b = self._make_backend()
        b._set_status(BackendStatus.CONNECTING)
        assert b.status == BackendStatus.CONNECTING
        b._set_status(BackendStatus.CONNECTED)
        assert b.status == BackendStatus.CONNECTED

    def test_status_no_duplicate_emit(self) -> None:
        b = self._make_backend()
        emitted: list[BackendStatus] = []
        b.status_changed.connect(emitted.append)
        b._set_status(BackendStatus.CONNECTING)
        b._set_status(BackendStatus.CONNECTING)
        b._set_status(BackendStatus.CONNECTED)
        assert emitted == [BackendStatus.CONNECTING, BackendStatus.CONNECTED]

    def test_descriptor_read_only(self) -> None:
        b = self._make_backend()
        assert b.descriptor.identifier == "test"
        assert b.descriptor.display_name == "Test"

    def test_known_sessions_defaults(self) -> None:
        b = self._make_backend()
        assert b.known_sessions() == ()
        assert b.known_listeners() == ()

    def test_known_topology_default(self) -> None:
        b = self._make_backend()
        t = b.known_topology()
        assert len(t.nodes) == 0
        assert len(t.edges) == 0

    def test_known_campaigns_default(self) -> None:
        b = self._make_backend()
        assert b.known_campaigns() == ()

    def test_world_model_default(self) -> None:
        b = self._make_backend()
        wm = b.request_world_model()
        assert isinstance(wm, dict)

    def test_session_state_default(self) -> None:
        b = self._make_backend()
        state = b.request_session_state()
        assert "credentials" in state
        assert "hashes" in state
        assert "loot" in state

    @staticmethod
    def _make_backend() -> "ConcreteBackend":
        desc = BackendDescriptor(identifier="test", display_name="Test", summary="...")
        return ConcreteBackend(desc)


class ConcreteBackend(Backend):
    """Minimal concrete backend for testing the abstract contract."""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def send_command(self, command: str, target_session: str | None = None) -> None:
        pass

    def refresh(self) -> None:
        pass

    def resize_terminal(self, columns: int, rows: int) -> None:
        pass

    def feed_terminal_input(self, data: str) -> None:
        pass


class TestTeamserverBackendConstruction:
    """TeamserverBackend can be constructed with valid credentials."""

    def test_construction(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://127.0.0.1:4444", username="op", password="pw")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        assert backend.status == BackendStatus.DISCONNECTED
        assert backend.descriptor.identifier == constants.backend.teamserver_id
        assert backend.known_sessions() == ()

    def test_construction_with_parent(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        parent = QObject()
        backend = TeamserverBackend(constants=constants, credentials=creds, parent=parent)
        assert backend.parent() is parent

    def test_build_url(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://10.0.0.1:4444/", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        url = backend._build_url("/api/data")
        assert url == "https://10.0.0.1:4444/api/data"

    def test_build_url_no_trailing_slash(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://10.0.0.1:4444", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        url = backend._build_url("api/run")
        assert url == "https://10.0.0.1:4444/api/run"


class TestTeamserverPayloadParsing:
    """TeamserverBackend correctly parses API payloads."""

    def test_update_from_empty_payload(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        backend._update_from_payload({"not_a_valid": "payload"})
        assert backend.known_sessions() == ()

    def test_non_mapping_payload(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        backend._update_from_payload("string_payload")
        assert backend.known_sessions() == ()

    def test_parse_graph_nodes_from_valid_payload(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        payload = {
            "nodes": [
                {"id": "c2", "label": "C2", "group": "c2", "color": "#58a6ff"},
                {"id": "b1", "label": "WIN-PC", "group": "beacon", "color": "#3fb950"},
            ],
            "edges": [
                {"from": "c2", "to": "b1", "label": "HTTPS"},
            ],
        }
        nodes = backend._parse_graph_nodes(payload)
        assert len(nodes) == 2
        assert nodes[0].identifier == "c2"
        assert nodes[0].node_type == "c2"
        assert nodes[1].node_type == "beacon"

    def test_parse_graph_edges_from_valid_payload(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        payload = {
            "nodes": [],
            "edges": [
                {"from": "c2", "to": "b1", "label": "HTTPS", "type": "c2", "color": "#ff9e3b"},
            ],
        }
        edges = backend._parse_graph_edges(payload)
        assert len(edges) == 1
        assert edges[0].source_id == "c2"
        assert edges[0].target_id == "b1"
        assert edges[0].label == "HTTPS"
        assert edges[0].edge_type == "c2"

    def test_parse_empty_graph_payload(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        assert backend._parse_graph_nodes("not_a_mapping") == []
        assert backend._parse_graph_edges(None) == []
        assert backend._parse_graph_edges({}) == []

    def test_update_operator(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        emitted: list[Operator] = []
        backend.operator_changed.connect(emitted.append)
        backend._update_operator({
            "current_user_username": "op1",
            "is_authenticated": True,
            "karma_name": "elite",
            "elo": 2500,
        })
        assert len(emitted) == 1
        assert emitted[0].name == "op1"
        assert emitted[0].elo == 2500

    def test_update_operator_no_username(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        emitted: list[Operator] = []
        backend.operator_changed.connect(emitted.append)
        backend._update_operator({"is_authenticated": True})
        assert len(emitted) == 0

    def test_update_sessions_empty(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        backend._update_sessions({})
        assert backend.known_sessions() == ()


class TestTeamserverBackendLifecycle:
    """TeamserverBackend start/stop contract."""

    def test_stop_without_start(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        backend.stop()
        assert backend.status == BackendStatus.DISCONNECTED

    def test_stop_sets_disconnected(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        backend.stop()
        assert backend.status == BackendStatus.DISCONNECTED
        assert backend.known_sessions() == ()
        assert backend.known_listeners() == ()

    def test_send_command_does_not_raise(self) -> None:
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        backend = TeamserverBackend(constants=constants, credentials=creds)
        backend.send_command("help")


class TestTopologyDataContract:
    """Topology construction and comparison."""

    def test_construct_and_compare(self) -> None:
        nodes = (GraphNode(identifier="a", label="A", node_type="c2"),)
        edges = (GraphEdge(source_id="a", target_id="a"),)
        t1 = Topology(nodes=nodes, edges=edges)
        t2 = Topology(nodes=nodes, edges=edges)
        assert t1 == t2

    def test_none_converted(self) -> None:
        t = Topology(nodes=(), edges=())
        assert t.nodes == ()
        assert t.edges == ()


class TestTopologyBuilderFromPayload:
    """Graph topology is built from /api/data payload fields."""

    def make_backend(self):
        from lazygui.config.constants import AppConstants
        constants = AppConstants()
        creds = TeamserverCredentials(base_url="https://x", username="u", password="p")
        return TeamserverBackend(constants=constants, credentials=creds)

    def test_builds_c2_node(self) -> None:
        backend = self.make_backend()
        backend._build_topology_from_payload({})
        topo = backend.known_topology()
        c2_nodes = [n for n in topo.nodes if n.node_type == "c2"]
        assert len(c2_nodes) == 1
        assert c2_nodes[0].identifier == "c2"

    def test_builds_beacon_nodes(self) -> None:
        backend = self.make_backend()
        payload = {
            "connected_clients": ["beacon1", "beacon2"],
            "os_data": {"beacon1": "linux", "beacon2": "windows"},
            "hostname": {"beacon1": "web01", "beacon2": "DC01"},
            "ips": {"beacon1": "10.0.0.5", "beacon2": "10.0.0.6"},
            "user": {"beacon1": "root", "beacon2": "admin"},
            "discovered_ips": {},
            "result_portscan": {},
        }
        backend._build_topology_from_payload(payload)
        topo = backend.known_topology()
        beacon_nodes = [n for n in topo.nodes if n.node_type == "beacon"]
        assert len(beacon_nodes) == 2
        assert {n.identifier for n in beacon_nodes} == {"beacon1", "beacon2"}

    def test_builds_edges_c2_to_beacon(self) -> None:
        backend = self.make_backend()
        payload = {
            "connected_clients": ["bx"],
            "os_data": {"bx": "linux"},
            "hostname": {"bx": "h"},
            "ips": {"bx": "10.0.0.1"},
            "user": {"bx": "u"},
            "discovered_ips": {},
            "result_portscan": {},
        }
        backend._build_topology_from_payload(payload)
        topo = backend.known_topology()
        c2_edges = [e for e in topo.edges if e.source_id == "c2" and e.edge_type == "c2"]
        assert len(c2_edges) == 1
        assert c2_edges[0].target_id == "bx"

    def test_builds_host_nodes_from_discovered(self) -> None:
        backend = self.make_backend()
        payload = {
            "connected_clients": ["bx"],
            "os_data": {"bx": "linux"},
            "hostname": {"bx": "h"},
            "ips": {"bx": "10.0.0.1"},
            "user": {"bx": "u"},
            "discovered_ips": {"bx": "10.0.0.5,10.0.0.6"},
            "result_portscan": {},
        }
        backend._build_topology_from_payload(payload)
        topo = backend.known_topology()
        host_nodes = [n for n in topo.nodes if n.node_type == "host"]
        assert len(host_nodes) == 2

    def test_builds_port_nodes(self) -> None:
        backend = self.make_backend()
        payload = {
            "connected_clients": ["bx"],
            "os_data": {"bx": "linux"},
            "hostname": {"bx": "h"},
            "ips": {"bx": "10.0.0.1"},
            "user": {"bx": "u"},
            "discovered_ips": {"bx": "10.0.0.5"},
            "result_portscan": {"bx": "22,80"},
        }
        backend._build_topology_from_payload(payload)
        topo = backend.known_topology()
        port_nodes = [n for n in topo.nodes if n.node_type == "port"]
        assert len(port_nodes) == 2

    def test_builds_connected_hosts(self) -> None:
        backend = self.make_backend()
        payload = {
            "connected_clients": [],
            "connected_hosts": ["10.0.0.99", "10.0.0.100"],
        }
        backend._build_topology_from_payload(payload)
        topo = backend.known_topology()
        host_nodes = [n for n in topo.nodes if n.node_type == "host"]
        assert len(host_nodes) == 2

    def test_topology_emitted_on_change(self) -> None:
        backend = self.make_backend()
        emitted: list[Topology] = []
        backend.topology_changed.connect(emitted.append)
        payload = {
            "connected_clients": ["bx"],
            "os_data": {"bx": "linux"},
            "hostname": {"bx": "h"},
            "ips": {"bx": "10.0.0.1"},
            "user": {"bx": "u"},
            "discovered_ips": {},
            "result_portscan": {},
        }
        backend._build_topology_from_payload(payload)
        assert len(emitted) == 1

    def test_topology_not_emitted_on_no_change(self) -> None:
        backend = self.make_backend()
        emitted: list[Topology] = []
        backend.topology_changed.connect(emitted.append)
        payload = {
            "connected_clients": ["bx"],
            "os_data": {"bx": "linux"},
            "hostname": {"bx": "h"},
            "ips": {"bx": "10.0.0.1"},
            "user": {"bx": "u"},
            "discovered_ips": {},
            "result_portscan": {},
        }
        backend._build_topology_from_payload(payload)
        assert len(emitted) == 1
        backend._build_topology_from_payload(payload)
        assert len(emitted) == 1
