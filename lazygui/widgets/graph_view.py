"""Interactive attack topography graph widget.

Renders the C2 beacon graph using Qt Graphics Framework (QGraphicsView).
Nodes represent servers, beacons and hosts. Edges represent connections.
Supports drag, zoom, selection highlighting and context menus.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.services.models import GraphEdge, GraphNode, Topology

_ICON_CACHE: dict[str, QPixmap] = {}
_ICON_SIZE_C2: int = 64
_ICON_SIZE_BEACON: int = 48
_ICON_SIZE_HOST: int = 32
_ICON_SIZE_PORT: int = 24
_ICON_DIR: str | None = None


def _resolve_icon_dir() -> str:
    global _ICON_DIR
    if _ICON_DIR is not None:
        return _ICON_DIR
    candidates = [
        Path("static"),
        Path(__file__).resolve().parents[3] / "static",
    ]
    for candidate in candidates:
        if candidate.is_dir() and (candidate / "c2.png").is_file():
            _ICON_DIR = str(candidate)
            return _ICON_DIR
    _ICON_DIR = ""
    return _ICON_DIR


def _load_icon(name: str) -> QPixmap | None:
    if not name:
        return None
    if name in _ICON_CACHE:
        return _ICON_CACHE[name]
    icon_dir = _resolve_icon_dir()
    if not icon_dir:
        return None
    path = Path(icon_dir) / name
    if not path.is_file():
        return None
    pixmap = QPixmap(str(path))
    if pixmap.isNull():
        return None
    _ICON_CACHE[name] = pixmap
    return pixmap


def _icon_for_node(node: GraphNode) -> QPixmap | None:
    ntype = node.node_type.lower()
    os_hint = node.metadata.get("os", node.metadata.get("platform", "")).lower()
    if ntype == "c2":
        return _load_icon("c2.png")
    if ntype in ("beacon", "client", "agent", "implant"):
        if "windows" in os_hint:
            return _load_icon("Windows.png")
        if "linux" in os_hint:
            return _load_icon("Linux.png")
        return _load_icon("client.png")
    if ntype in ("host", "computer", "server"):
        return _load_icon("host.png")
    if ntype in ("port", "service"):
        return _load_icon("port.png")
    return _load_icon("client.png")

_NODE_RADIUS_C2: float = 32.0
_NODE_RADIUS_BEACON: float = 24.0
_NODE_RADIUS_HOST: float = 16.0
_NODE_RADIUS_PORT: float = 12.0
_EDGE_PEN_WIDTH: float = 2.0
_Z_VALUE_NODE: float = 2.0
_Z_VALUE_EDGE: float = 1.0
_Z_VALUE_LABEL: float = 3.0
_LAYOUT_FORCE: float = 0.04
_LAYOUT_DAMPING: float = 0.88
_LAYOUT_REPULSION: float = 15000.0
_LAYOUT_ATTRACTION: float = 0.005
_LAYOUT_CENTER_X: float = 400.0
_LAYOUT_CENTER_Y: float = 300.0
_LAYOUT_SPREAD: float = 180.0
_MAX_ITERATIONS: int = 200

_COLOR_MAP: dict[str, QColor] = {
    "c2": QColor("#58a6ff"),
    "beacon": QColor("#3fb950"),
    "host": QColor("#d2991d"),
    "port": QColor("#8b949e"),
    "windows": QColor("#58a6ff"),
    "linux": QColor("#3fb950"),
    "macos": QColor("#a371f7"),
    "default": QColor("#f85149"),
}

NodeCallback = Callable[[str], None]
ContextMenuCallback = Callable[[str, QPointF], None]


@dataclass(slots=True)
class GraphNodeState:
    """Internal state for a graph node being laid out."""

    node: GraphNode
    velocity_x: float = 0.0
    velocity_y: float = 0.0


class GraphNodeItem(QGraphicsEllipseItem):
    """A single node in the graph with label and selection support."""

    def __init__(
        self,
        node: GraphNode,
        radius: float,
        color: QColor,
        pixmap: QPixmap | None = None,
        on_selected: NodeCallback | None = None,
        on_context_menu: ContextMenuCallback | None = None,
        label_visible: bool = True,
        parent: QGraphicsItem | None = None,
    ) -> None:
        super().__init__(-radius, -radius, radius * 2, radius * 2, parent)
        self._node = node
        self._radius = radius
        self._color = color
        self._pixmap = pixmap
        self._on_selected = on_selected
        self._on_context_menu = on_context_menu
        self.setZValue(_Z_VALUE_NODE)
        self.setBrush(QBrush(color))
        self.setPen(QPen(color.darker(120), 1.5))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self._label_item: QGraphicsTextItem | None = None
        if label_visible:
            self._create_label()

    def _create_label(self) -> None:
        label = self._node.label[:20]
        text_item = QGraphicsTextItem(label, self)
        text_item.setDefaultTextColor(QColor("#e6edf3"))
        font = QFont("JetBrains Mono", 8)
        font.setBold(False)
        text_item.setFont(font)
        text_item.setZValue(_Z_VALUE_LABEL)
        text_rect = text_item.boundingRect()
        text_item.setPos(-text_rect.width() / 2, self._radius + 2)
        self._label_item = text_item

    @property
    def node_data(self) -> GraphNode:
        """Return the immutable node data associated with this item."""
        return self._node

    def paint(
        self,
        painter: QPainter,
        option: Any,
        widget: Any = None,
    ) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        rect = self.rect()

        if self._pixmap and not self._pixmap.isNull():
            pixmap_rect = QRectF(
                rect.center().x() - self._radius,
                rect.center().y() - self._radius,
                self._radius * 2,
                self._radius * 2,
            )
            source = QRectF(0, 0, self._pixmap.width(), self._pixmap.height())
            if self.isSelected():
                painter.save()
                glow_pen = QPen(QColor("#58a6ff"), 3.0)
                glow_color = QColor("#58a6ff")
                glow_color.setAlpha(60)
                painter.setPen(glow_pen)
                painter.setBrush(QBrush(glow_color))
                painter.drawEllipse(rect)
                painter.restore()
            painter.drawPixmap(pixmap_rect, self._pixmap, source)
            return

        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0.0, self._color.lighter(130))
        gradient.setColorAt(1.0, self._color.darker(110))
        painter.setBrush(QBrush(gradient))
        if self.isSelected():
            pen = QPen(QColor("#58a6ff"), 3.0)
            glow = QColor("#58a6ff")
            glow.setAlpha(60)
            painter.setBrush(QBrush(glow))
        else:
            pen = QPen(self._color.darker(120), 1.5)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        if not self.isSelected():
            highlight = QColor(255, 255, 255, 40)
            painter.setBrush(QBrush(highlight))
            inner = rect.adjusted(rect.width() * 0.3, rect.height() * 0.3, -rect.width() * 0.3, -rect.height() * 0.3)
            painter.drawEllipse(inner)

        if self._node.icon:
            painter.save()
            icon_font = QFont("DejaVu Sans Mono", 10)
            painter.setFont(icon_font)
            painter.setPen(QPen(QColor("#ffffff")))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self._node.icon[:1].upper())
            painter.restore()

    def mousePressEvent(self, event: Any) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            if self._on_context_menu is not None:
                scene_pos = self.scenePos()
                self._on_context_menu(self._node.identifier, scene_pos)
            event.accept()
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: Any) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            if self._on_selected is not None:
                self._on_selected(self._node.identifier)
        super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event: Any) -> None:
        pen = QPen(QColor("#58a6ff"), 2.5)
        self.setPen(pen)
        if self._label_item:
            self._label_item.setDefaultTextColor(QColor("#58a6ff"))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: Any) -> None:
        self.setPen(QPen(self._color.darker(120), 1.5))
        if self._label_item:
            self._label_item.setDefaultTextColor(QColor("#e6edf3"))
        super().hoverLeaveEvent(event)

    def itemChange(self, change: Any, value: Any) -> Any:
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange and self._label_item:
            self._label_item.setVisible(True)
        return super().itemChange(change, value)


class GraphEdgeItem(QGraphicsLineItem):
    """A line connecting two graph nodes with optional label."""

    def __init__(
        self,
        edge: GraphEdge,
        source_item: QGraphicsItem,
        target_item: QGraphicsItem,
        parent: QGraphicsItem | None = None,
    ) -> None:
        super().__init__(parent)
        self._edge = edge
        self._source = source_item
        self._target = target_item
        self.setZValue(_Z_VALUE_EDGE)
        color = QColor(edge.color) if edge.color else QColor("#30363d")
        pen = QPen(color, _EDGE_PEN_WIDTH, Qt.PenStyle.SolidLine)
        self.setPen(pen)
        self._label_item: QGraphicsTextItem | None = None
        if edge.label:
            text = QGraphicsTextItem(edge.label, self)
            text.setDefaultTextColor(QColor("#8b949e"))
            font = QFont("JetBrains Mono", 7)
            text.setFont(font)
            text.setZValue(_Z_VALUE_LABEL)
            self._label_item = text
        self._update_position()

    def _update_position(self) -> None:
        if not self._source or not self._target:
            return
        start = self._source.scenePos()
        end = self._target.scenePos()
        self.setLine(start.x(), start.y(), end.x(), end.y())
        if self._label_item:
            mid_x = (start.x() + end.x()) / 2
            mid_y = (start.y() + end.y()) / 2
            self._label_item.setPos(mid_x, mid_y)

    def update_position(self) -> None:
        """Recalculate the line endpoints from source and target positions."""
        self._update_position()

    @property
    def edge_data(self) -> GraphEdge:
        """Return the immutable edge data."""
        return self._edge


class GraphScene(QGraphicsScene):
    """Scene managing all graph nodes and edges with physics layout."""

    node_selected = Signal(str)
    node_context_menu = Signal(str, QPointF)

    def __init__(self, constants: AppConstants, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._constants = constants
        self._node_items: dict[str, GraphNodeItem] = {}
        self._edge_items: list[GraphEdgeItem] = []
        self._node_states: dict[str, GraphNodeState] = {}
        self._physics_active: bool = False
        self._iteration: int = 0

    def set_topology(self, topology: Topology) -> None:
        """Replace the current graph with a new topology using force layout."""
        self.clear()
        self._node_items.clear()
        self._edge_items.clear()
        self._node_states.clear()

        if not topology.nodes and not topology.edges:
            return

        for node in topology.nodes:
            self._add_node(node)

        for edge in topology.edges:
            self._add_edge(edge)

        self._apply_force_layout()
        self._physics_active = True
        self._iteration = 0

    def _add_node(self, node: GraphNode) -> None:
        color = _resolve_node_color(node)
        radius = _resolve_node_radius(node)
        pixmap = _icon_for_node(node)

        def _on_selected(nid: str) -> None:
            self.node_selected.emit(nid)

        def _on_context_menu(nid: str, pos: QPointF) -> None:
            self.node_context_menu.emit(nid, pos)

        item = GraphNodeItem(
            node, radius, color, pixmap=pixmap,
            on_selected=_on_selected,
            on_context_menu=_on_context_menu,
            label_visible=True,
        )
        self.addItem(item)
        self._node_items[node.identifier] = item
        self._node_states[node.identifier] = GraphNodeState(node=node)

    def _add_edge(self, edge: GraphEdge) -> None:
        source = self._node_items.get(edge.source_id)
        target = self._node_items.get(edge.target_id)
        if not source or not target:
            return
        edge_item = GraphEdgeItem(edge, source, target)
        self.addItem(edge_item)
        self._edge_items.append(edge_item)

    def _apply_force_layout(self) -> None:
        ids = list(self._node_items.keys())
        count = len(ids)
        if count == 0:
            return
        center_x = self.sceneRect().width() / 2 if self.sceneRect().width() > 0 else _LAYOUT_CENTER_X
        center_y = self.sceneRect().height() / 2 if self.sceneRect().height() > 0 else _LAYOUT_CENTER_Y
        angle_step = 2 * math.pi / count
        for idx, nid in enumerate(ids):
            item = self._node_items[nid]
            angle = idx * angle_step
            rx = _LAYOUT_SPREAD * (1 + 0.3 * math.sin(angle * 3))
            ry = _LAYOUT_SPREAD * (1 + 0.3 * math.cos(angle * 2))
            x = center_x + rx * math.cos(angle)
            y = center_y + ry * math.sin(angle)
            item.setPos(x, y)

    def step_physics(self) -> bool:
        """Run one iteration of force-directed layout. Returns False when stable."""
        if not self._physics_active:
            return False
        ids = list(self._node_states.keys())
        if not ids:
            self._physics_active = False
            return False
        if self._iteration >= _MAX_ITERATIONS:
            self._physics_active = False
            return False
        self._iteration += 1
        center_x = _LAYOUT_CENTER_X
        center_y = _LAYOUT_CENTER_Y
        forces: dict[str, tuple[float, float]] = {nid: (0.0, 0.0) for nid in ids}
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                nid_a = ids[i]
                nid_b = ids[j]
                item_a = self._node_items[nid_a]
                item_b = self._node_items[nid_b]
                dx = item_a.pos().x() - item_b.pos().x()
                dy = item_a.pos().y() - item_b.pos().y()
                dist = math.hypot(dx, dy) or 1.0
                repulsion = _LAYOUT_REPULSION / (dist * dist)
                fx = repulsion * (dx / dist)
                fy = repulsion * (dy / dist)
                fa_x, fa_y = forces[nid_a]
                forces[nid_a] = (fa_x + fx, fa_y + fy)
                fb_x, fb_y = forces[nid_b]
                forces[nid_b] = (fb_x - fx, fb_y - fy)
            for edge_item in self._edge_items:
                e = edge_item.edge_data
                if e.source_id == ids[i]:
                    nid_b = e.target_id
                elif e.target_id == ids[i]:
                    nid_b = e.source_id
                else:
                    continue
                item_a = self._node_items[ids[i]]
                item_b = self._node_items[nid_b]
                dx = item_b.pos().x() - item_a.pos().x()
                dy = item_b.pos().y() - item_a.pos().y()
                dist = math.hypot(dx, dy) or 1.0
                attraction = _LAYOUT_ATTRACTION * dist
                fx = attraction * (dx / dist)
                fy = attraction * (dy / dist)
                fa_x, fa_y = forces[ids[i]]
                forces[ids[i]] = (fa_x + fx, fa_y + fy)
            cx = center_x - self._node_items[ids[i]].pos().x()
            cy = center_y - self._node_items[ids[i]].pos().y()
            gravity = 0.01
            fa_x, fa_y = forces[ids[i]]
            forces[ids[i]] = (fa_x + cx * gravity, fa_y + cy * gravity)

        max_velocity = 0.0
        for nid, (fx, fy) in forces.items():
            state = self._node_states[nid]
            state.velocity_x = (state.velocity_x + fx * _LAYOUT_FORCE) * _LAYOUT_DAMPING
            state.velocity_y = (state.velocity_y + fy * _LAYOUT_FORCE) * _LAYOUT_DAMPING
            vel = math.hypot(state.velocity_x, state.velocity_y)
            if vel > max_velocity:
                max_velocity = vel
            item = self._node_items[nid]
            item.moveBy(state.velocity_x, state.velocity_y)
        for edge_item in self._edge_items:
            edge_item.update_position()
        if max_velocity < 0.1:
            self._physics_active = False
            return False
        return True

    def selected_node_id(self) -> str | None:
        """Return the identifier of the first selected node, or None."""
        for nid, item in self._node_items.items():
            if item.isSelected():
                return nid
        return None


class GraphView(QGraphicsView):
    """Interactive graph view with zoom, pan and physics animation."""

    node_selected = Signal(str)
    node_context_menu = Signal(str, QPointF)

    _ZOOM_FACTOR: float = 1.15
    _MAX_ZOOM: float = 5.0
    _MIN_ZOOM: float = 0.1

    def __init__(self, constants: AppConstants, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._constants = constants
        self._scene = GraphScene(constants, self)
        self._scene.node_selected.connect(self.node_selected.emit)
        self._scene.node_context_menu.connect(self.node_context_menu.emit)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(QColor("#0d1117")))
        self.setMinimumSize(400, 300)
        self._physics_timer: Any = None
        self._install_physics_timer()

    def set_topology(self, topology: Topology) -> None:
        """Render a new graph topology."""
        self._scene.set_topology(topology)
        self.fitInView(self._scene.sceneRect().adjusted(-50, -50, 50, 50), Qt.AspectRatioMode.KeepAspectRatio)

    def _install_physics_timer(self) -> None:
        from PySide6.QtCore import QTimer

        self._physics_timer = QTimer(self)
        self._physics_timer.setInterval(16)
        self._physics_timer.timeout.connect(self._tick_physics)
        self._physics_timer.start()

    def _tick_physics(self) -> None:
        self._scene.step_physics()

    def wheelEvent(self, event: Any) -> None:
        zoom_in = event.angleDelta().y() > 0
        factor = self._ZOOM_FACTOR if zoom_in else 1.0 / self._ZOOM_FACTOR
        current = self.transform().m11()
        if factor > 1.0 and current >= self._MAX_ZOOM:
            return
        if factor < 1.0 and current <= self._MIN_ZOOM:
            return
        self.scale(factor, factor)

    def selected_node_id(self) -> str | None:
        """Return the identifier of the currently selected node."""
        return self._scene.selected_node_id()

    def fit_to_content(self) -> None:
        """Zoom to fit all graph content."""
        self.fitInView(self._scene.sceneRect().adjusted(-30, -30, 30, 30), Qt.AspectRatioMode.KeepAspectRatio)

    @property
    def scene_handle(self) -> GraphScene:
        """Return the underlying graph scene."""
        return self._scene


def _resolve_node_color(node: GraphNode) -> QColor:
    ntype = node.node_type.lower()
    os_hint = node.metadata.get("os", node.metadata.get("platform", "")).lower()
    for keyword in ("windows", "linux", "macos"):
        if keyword in ntype or keyword in os_hint:
            return _COLOR_MAP.get(keyword, _COLOR_MAP["default"])
    return _COLOR_MAP.get(ntype, _COLOR_MAP["default"])


def _resolve_node_radius(node: GraphNode) -> float:
    ntype = node.node_type.lower()
    if ntype == "c2":
        return float(_ICON_SIZE_C2) / 2.0
    if ntype in ("beacon", "client", "agent", "implant"):
        return float(_ICON_SIZE_BEACON) / 2.0
    if ntype in ("host", "computer", "server"):
        return float(_ICON_SIZE_HOST) / 2.0
    if ntype in ("port", "service"):
        return float(_ICON_SIZE_PORT) / 2.0
    return float(_ICON_SIZE_HOST) / 2.0
