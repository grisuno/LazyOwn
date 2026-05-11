"""Panel that lists the listeners advertised by the backend."""

from __future__ import annotations

from typing import Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.services.models import Listener
from lazygui.widgets.filter_bar import FilterBar

_LISTENER_HEADERS: tuple[str, ...] = ("ID", "Kind", "Address", "Port", "Secure", "Description")
_PORT_COLUMN: int = 3
_SECURE_COLUMN: int = 4


class ListenersPanel(PanelBase):
    """Reactive list of :class:`Listener` rows."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Build the layout and subscribe to backend listener updates."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier=constants.panel.listeners_id,
            title=constants.panel.listeners_label,
            parent=parent,
        )
        self._listeners: tuple[Listener, ...] = ()
        self._filter_text: str = ""
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        self._filter_bar = FilterBar(
            constants=constants,
            placeholder_text="Filter by id, kind, address...",
            parent=container,
        )
        self._tree = QTreeWidget(container)
        self._tree.setColumnCount(len(_LISTENER_HEADERS))
        self._tree.setHeaderLabels(list(_LISTENER_HEADERS))
        self._tree.setRootIsDecorated(False)
        self._tree.setAlternatingRowColors(True)
        self._tree.setUniformRowHeights(True)
        self._tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._tree.header().setStretchLastSection(True)
        layout.addWidget(self._filter_bar)
        layout.addWidget(self._tree)
        self.setWidget(container)
        self._filter_bar.filter_changed.connect(self._on_filter_changed)
        backend.listeners_changed.connect(self._on_listeners_changed)
        initial = backend.known_listeners()
        if initial:
            self._on_listeners_changed(list(initial))

    def _on_listeners_changed(self, listeners: Sequence[Listener]) -> None:
        """Cache and rebuild rows."""
        self._listeners = tuple(listeners)
        self._populate_visible()

    def _on_filter_changed(self, text: str) -> None:
        """Persist filter and re-render."""
        self._filter_text = text.lower().strip()
        self._populate_visible()

    def _populate_visible(self) -> None:
        """Rebuild the tree honouring the active filter."""
        self._tree.clear()
        for listener in self._listeners:
            if not self._matches_filter(listener):
                continue
            item = QTreeWidgetItem(
                [
                    listener.identifier,
                    listener.kind,
                    listener.address,
                    str(listener.port),
                    "yes" if listener.is_secure else "no",
                    listener.description,
                ]
            )
            item.setTextAlignment(_PORT_COLUMN, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            item.setTextAlignment(_SECURE_COLUMN, Qt.AlignmentFlag.AlignCenter)
            self._tree.addTopLevelItem(item)

    def _matches_filter(self, listener: Listener) -> bool:
        """Return ``True`` if the listener fields contain the filter text."""
        if not self._filter_text:
            return True
        haystacks = (
            listener.identifier,
            listener.kind,
            listener.address,
            str(listener.port),
            listener.description,
        )
        return any(self._filter_text in field.lower() for field in haystacks)
