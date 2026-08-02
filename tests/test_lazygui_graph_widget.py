"""Tests for lazygui graph widget contracts.

Covers GraphNodeItem, GraphEdgeItem, GraphScene, GraphView, topology
rendering and force layout behaviour.
"""

from __future__ import annotations

import pytest

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication

from lazygui.config.constants import AppConstants
from lazygui.services.models import GraphEdge, GraphNode, Topology
from lazygui.widgets.graph_view import (
    _COLOR_MAP,
    _NODE_RADIUS_BEACON,
    _NODE_RADIUS_C2,
    _NODE_RADIUS_HOST,
    _NODE_RADIUS_PORT,
    GraphEdgeItem,
    GraphNodeItem,
    GraphScene,
    GraphView,
    _resolve_node_color,
    _resolve_node_radius,
)


_QAPP: QApplication | None = None


def _get_qapp() -> QApplication:
    global _QAPP
    if _QAPP is None:
        _QAPP = QApplication.instance() or QApplication([])
    return _QAPP


class TestColorResolution:
    """Node colour resolution rules."""

    def test_c2_color(self) -> None:
        node = GraphNode(identifier="c2", label="C2", node_type="c2")
        assert _resolve_node_color(node) == QColor("#58a6ff")

    def test_beacon_color(self) -> None:
        node = GraphNode(identifier="b", label="B", node_type="beacon")
        assert _resolve_node_color(node) == QColor("#3fb950")

    def test_host_color(self) -> None:
        node = GraphNode(identifier="h", label="H", node_type="host")
        assert _resolve_node_color(node) == QColor("#d2991d")

    def test_port_color(self) -> None:
        node = GraphNode(identifier="p", label="P", node_type="port")
        assert _resolve_node_color(node) == QColor("#8b949e")

    def test_windows_os_hint(self) -> None:
        node = GraphNode(identifier="w", label="W", node_type="beacon", metadata={"os": "windows"})
        assert _resolve_node_color(node) == QColor("#58a6ff")

    def test_linux_os_hint(self) -> None:
        node = GraphNode(identifier="l", label="L", node_type="beacon", metadata={"platform": "linux"})
        assert _resolve_node_color(node) == QColor("#3fb950")

    def test_macos_os_hint(self) -> None:
        node = GraphNode(identifier="m", label="M", node_type="beacon", metadata={"os": "macos"})
        assert _resolve_node_color(node) == QColor("#a371f7")

    def test_unknown_default(self) -> None:
        node = GraphNode(identifier="x", label="X", node_type="unknown_type")
        assert _resolve_node_color(node) == QColor("#f85149")


class TestRadiusResolution:
    """Node radius resolution rules."""

    def test_c2_radius(self) -> None:
        node = GraphNode(identifier="c2", label="C2", node_type="c2")
        assert _resolve_node_radius(node) == _NODE_RADIUS_C2

    def test_beacon_radius(self) -> None:
        for ntype in ("beacon", "client", "agent", "implant"):
            node = GraphNode(identifier=ntype, label=ntype, node_type=ntype)
            assert _resolve_node_radius(node) == _NODE_RADIUS_BEACON

    def test_host_radius(self) -> None:
        for ntype in ("host", "computer", "server"):
            node = GraphNode(identifier=ntype, label=ntype, node_type=ntype)
            assert _resolve_node_radius(node) == _NODE_RADIUS_HOST

    def test_port_radius(self) -> None:
        for ntype in ("port", "service"):
            node = GraphNode(identifier=ntype, label=ntype, node_type=ntype)
            assert _resolve_node_radius(node) == _NODE_RADIUS_PORT

    def test_default_radius(self) -> None:
        node = GraphNode(identifier="x", label="X", node_type="unknown_type")
        assert _resolve_node_radius(node) == _NODE_RADIUS_HOST


class TestColorMap:
    """Color map contains all required node type colours."""

    def test_all_keys_present(self) -> None:
        required = {"c2", "beacon", "host", "port", "windows", "linux", "macos", "default"}
        assert set(_COLOR_MAP.keys()) == required


class TestGraphNodeItem:
    """GraphNodeItem renders a graph node with label and callbacks."""

    def test_construction(self) -> None:
        _get_qapp()
        node = GraphNode(identifier="test_node", label="Test", node_type="host")
        color = _resolve_node_color(node)
        radius = _resolve_node_radius(node)
        item = GraphNodeItem(node, radius, color)
        assert item.node_data.identifier == "test_node"
        assert item.node_data.label == "Test"
        assert item.isVisible()

    def test_identifiers(self) -> None:
        _get_qapp()
        for nid in ("c2", "beacon_001", "host_192_168_1_1"):
            node = GraphNode(identifier=nid, label=nid, node_type="host")
            item = GraphNodeItem(node, _NODE_RADIUS_HOST, QColor("#fff"))
            assert item.node_data.identifier == nid

    def test_selection_behaviour(self) -> None:
        _get_qapp()
        node = GraphNode(identifier="s", label="S", node_type="host")
        item = GraphNodeItem(node, _NODE_RADIUS_HOST, QColor("#fff"))
        assert not item.isSelected()
        item.setSelected(True)
        assert item.isSelected()
        item.setSelected(False)
        assert not item.isSelected()

    def test_callback_on_selected(self) -> None:
        _get_qapp()
        called: list[str] = []
        node = GraphNode(identifier="callback_test", label="CB", node_type="host")

        def _cb(nid: str) -> None:
            called.append(nid)

        item = GraphNodeItem(node, _NODE_RADIUS_HOST, QColor("#fff"), on_selected=_cb)
        assert item.node_data.identifier == "callback_test"
        item._on_selected("callback_test")  # type: ignore[union-attr]
        assert called == ["callback_test"]

    def test_callback_on_context_menu(self) -> None:
        _get_qapp()
        called_ids: list[str] = []
        called_pos: list[QPointF] = []
        node = GraphNode(identifier="ctx_test", label="CTX", node_type="host")

        def _cb(nid: str, pos: QPointF) -> None:
            called_ids.append(nid)
            called_pos.append(pos)

        item = GraphNodeItem(node, _NODE_RADIUS_HOST, QColor("#fff"), on_context_menu=_cb)
        pos = QPointF(10.0, 20.0)
        item._on_context_menu("ctx_test", pos)  # type: ignore[union-attr]
        assert called_ids == ["ctx_test"]
        assert called_pos[0] == pos

    def test_node_without_callbacks_does_not_raise(self) -> None:
        _get_qapp()
        node = GraphNode(identifier="nc", label="NC", node_type="host")
        item = GraphNodeItem(node, _NODE_RADIUS_HOST, QColor("#fff"))
        assert item._on_selected is None
        assert item._on_context_menu is None


class TestGraphEdgeItem:
    """GraphEdgeItem connects two node items."""

    def test_construction_with_nodes(self) -> None:
        _get_qapp()
        src_node = GraphNode(identifier="a", label="A", node_type="c2")
        tgt_node = GraphNode(identifier="b", label="B", node_type="beacon")
        src = GraphNodeItem(src_node, _NODE_RADIUS_C2, QColor("#58a6ff"))
        src.setPos(0.0, 0.0)
        tgt = GraphNodeItem(tgt_node, _NODE_RADIUS_BEACON, QColor("#3fb950"))
        tgt.setPos(100.0, 100.0)
        edge = GraphEdge(source_id="a", target_id="b", label="test_edge")
        item = GraphEdgeItem(edge, src, tgt)
        assert item.edge_data.source_id == "a"
        assert item.edge_data.target_id == "b"
        assert item.edge_data.label == "test_edge"

    def test_update_position(self) -> None:
        _get_qapp()
        src_node = GraphNode(identifier="a", label="A", node_type="c2")
        tgt_node = GraphNode(identifier="b", label="B", node_type="host")
        src = GraphNodeItem(src_node, _NODE_RADIUS_C2, QColor("#58a6ff"))
        src.setPos(0.0, 0.0)
        tgt = GraphNodeItem(tgt_node, _NODE_RADIUS_HOST, QColor("#d2991d"))
        tgt.setPos(50.0, 50.0)
        edge = GraphEdge(source_id="a", target_id="b")
        item = GraphEdgeItem(edge, src, tgt)
        item.update_position()
        assert item.line().length() > 1.0


class TestGraphScene:
    """GraphScene manages nodes, edges and force layout."""

    def test_construction(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        assert scene.selected_node_id() is None

    def test_set_topology_with_data(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        nodes = (
            GraphNode(identifier="c2", label="C2", node_type="c2"),
            GraphNode(identifier="b1", label="Beacon1", node_type="beacon"),
        )
        edges = (GraphEdge(source_id="c2", target_id="b1"),)
        topology = Topology(nodes=nodes, edges=edges)
        scene.set_topology(topology)
        assert len(scene._node_items) == 2
        assert len(scene._edge_items) == 1

    def test_set_empty_topology(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        scene.set_topology(Topology.empty())
        assert len(scene._node_items) == 0
        assert len(scene._edge_items) == 0

    def test_force_layout_single_node(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        nodes = (GraphNode(identifier="c2", label="C2", node_type="c2"),)
        topology = Topology(nodes=nodes, edges=())
        scene.set_topology(topology)
        assert "c2" in scene._node_items

    def test_selected_node_id_none_when_empty(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        assert scene.selected_node_id() is None

    def test_physics_completion(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        nodes = (
            GraphNode(identifier="c2", label="C2", node_type="c2"),
            GraphNode(identifier="b1", label="B1", node_type="beacon"),
        )
        edges = (GraphEdge(source_id="c2", target_id="b1"),)
        scene.set_topology(Topology(nodes=nodes, edges=edges))
        for _ in range(210):
            if not scene.step_physics():
                break
        assert not scene._physics_active or scene._iteration >= 200

    def test_physics_stops_without_nodes(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        scene.set_topology(Topology.empty())
        assert not scene.step_physics()

    def test_node_selected_signal(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        emitted: list[str] = []
        scene.node_selected.connect(emitted.append)
        scene.node_selected.emit("n1")
        assert emitted == ["n1"]

    def test_node_context_menu_signal(self) -> None:
        _get_qapp()
        constants = AppConstants()
        scene = GraphScene(constants)
        emitted_ids: list[str] = []
        emitted_pos: list[QPointF] = []

        def _capture(nid: str, pos: QPointF) -> None:
            emitted_ids.append(nid)
            emitted_pos.append(pos)

        scene.node_context_menu.connect(_capture)
        pos = QPointF(100.0, 200.0)
        scene.node_context_menu.emit("ctx_node", pos)
        assert emitted_ids == ["ctx_node"]
        assert emitted_pos[0] == pos


class TestGraphView:
    """GraphView wraps scene with zoom, pan and physics."""

    def test_construction(self) -> None:
        _get_qapp()
        constants = AppConstants()
        view = GraphView(constants)
        assert view.selected_node_id() is None

    def test_set_topology(self) -> None:
        _get_qapp()
        constants = AppConstants()
        view = GraphView(constants)
        nodes = (GraphNode(identifier="a", label="A", node_type="host"),)
        topology = Topology(nodes=nodes, edges=())
        view.set_topology(topology)
        assert view.selected_node_id() is None

    def test_fit_to_content(self) -> None:
        _get_qapp()
        constants = AppConstants()
        view = GraphView(constants)
        view.set_topology(Topology.empty())
        view.fit_to_content()


class TestGraphViewWithDatabaseFixture:
    """Full integration: topology -> view -> scene."""

    def test_full_pipeline(self) -> None:
        _get_qapp()
        constants = AppConstants()
        view = GraphView(constants)
        nodes = (
            GraphNode(identifier="c2", label="C2 Server", node_type="c2"),
            GraphNode(identifier="win01", label="WIN-DC01", node_type="beacon", metadata={"os": "windows"}),
            GraphNode(identifier="lin01", label="WEB-01", node_type="beacon", metadata={"platform": "linux"}),
            GraphNode(identifier="host1", label="10.0.0.5", node_type="host"),
            GraphNode(identifier="port22", label="22/tcp", node_type="port"),
        )
        edges = (
            GraphEdge(source_id="c2", target_id="win01", label="HTTPS"),
            GraphEdge(source_id="c2", target_id="lin01", label="HTTPS"),
            GraphEdge(source_id="win01", target_id="host1", label="discovered"),
            GraphEdge(source_id="host1", target_id="port22", label="SSH"),
        )
        topology = Topology(nodes=nodes, edges=edges)
        view.set_topology(topology)
        scene = view.scene_handle
        assert len(scene._node_items) == 5
        assert len(scene._edge_items) == 4


class TestGraphNodeItemWithIcon:
    """GraphNodeItem renders icons correctly."""

    def test_node_with_icon(self) -> None:
        _get_qapp()
        node = GraphNode(identifier="c2", label="C2", node_type="c2", icon="/static/c2.png")
        item = GraphNodeItem(node, _NODE_RADIUS_C2, QColor("#58a6ff"))
        assert item.node_data.icon == "/static/c2.png"

    def test_hover_behavior(self) -> None:
        _get_qapp()
        node = GraphNode(identifier="h", label="H", node_type="host")
        item = GraphNodeItem(node, _NODE_RADIUS_HOST, QColor("#d2991d"))
        assert item.acceptHoverEvents()

    def test_movable_flag(self) -> None:
        _get_qapp()
        node = GraphNode(identifier="m", label="M", node_type="host")
        item = GraphNodeItem(node, _NODE_RADIUS_HOST, QColor("#fff"))
        assert item.flags() & item.GraphicsItemFlag.ItemIsMovable
