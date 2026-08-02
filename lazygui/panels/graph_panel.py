"""Graph panel for Cobalt Strike-style attack topography visualization.

Renders the C2 beacon graph with interactive nodes, force-directed layout
and context menus for beacon interaction: spawn shell, port scan,
screenshot, keylog, migrate, download/upload.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QMenu, QVBoxLayout, QWidget

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.services.models import Topology
from lazygui.widgets.graph_view import GraphView


class GraphPanel(PanelBase):
    """Dock panel wrapping the interactive graph view."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Build the graph view and connect to backend topology updates."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier=constants.panel.graph_panel_id,
            title=constants.panel.graph_label,
            parent=parent,
        )
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        self._graph_view = GraphView(constants=constants, parent=container)
        layout.addWidget(self._graph_view)
        self.setWidget(container)
        backend.topology_changed.connect(self._on_topology_changed)
        self._graph_view.node_context_menu.connect(self._on_node_context_menu)
        self._graph_view.node_selected.connect(self._on_node_selected)
        initial = backend.known_topology()
        if initial.nodes or initial.edges:
            self._on_topology_changed(initial)

    def _on_topology_changed(self, topology: Topology) -> None:
        """Render the new topology in the graph view."""
        self._graph_view.set_topology(topology)

    def _on_node_context_menu(self, node_id: str, position: QPointF) -> None:
        """Show a Cobalt Strike-style context menu for the selected node."""
        node_info = self._find_node_info(node_id)
        menu = QMenu(self)
        info = menu.addAction(f"Node: {node_info}")
        info.setEnabled(False)
        menu.addSeparator()

        interact = menu.addAction("Interact (Shell)")
        interact.triggered.connect(lambda: self._backend.send_command("shell", target_session=node_id))

        portscan = menu.addAction("Port Scan")
        portscan.triggered.connect(lambda: self._backend.send_command(f"lazynmap", target_session=node_id))

        menu.addSeparator()

        screenshot = menu.addAction("Screenshot")
        screenshot.triggered.connect(lambda: self._backend.send_command("screenshot", target_session=node_id))

        keylog = menu.addAction("Start Keylog")
        keylog.triggered.connect(lambda: self._backend.send_command("keylog", target_session=node_id))

        menu.addSeparator()

        migrate = menu.addAction("Migrate Process")
        migrate.triggered.connect(lambda: self._backend.send_command("migrate", target_session=node_id))

        download = menu.addAction("Download File")
        download.triggered.connect(lambda: self._backend.send_command("download", target_session=node_id))

        upload = menu.addAction("Upload File")
        upload.triggered.connect(lambda: self._backend.send_command("upload", target_session=node_id))

        menu.addSeparator()

        sleep = menu.addAction("Set Sleep")
        sleep.triggered.connect(lambda: self._backend.send_command("sleep", target_session=node_id))

        kill = menu.addAction("Kill Beacon")
        kill.triggered.connect(lambda: self._backend.send_command("kill", target_session=node_id))

        menu.addSeparator()

        refresh = menu.addAction("Refresh Topology")
        refresh.triggered.connect(self._backend.refresh)

        fit_action = menu.addAction("Fit Graph")
        fit_action.triggered.connect(self._graph_view.fit_to_content)

        menu.exec_(self._graph_view.mapToGlobal(position.toPoint()))

    def _on_node_selected(self, node_id: str) -> None:
        """Handle node selection in the graph."""
        pass

    def _find_node_info(self, node_id: str) -> str:
        """Return human-readable info for a node by its identifier."""
        topology = self._backend.known_topology()
        for node in topology.nodes:
            if node.identifier == node_id:
                return f"{node.label} ({node.node_type})"
        return node_id

    @property
    def graph_view(self) -> GraphView:
        """Return the underlying graph view for layout management."""
        return self._graph_view
