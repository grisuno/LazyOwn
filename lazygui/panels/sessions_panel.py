"""Panel that lists active sessions reported by the backend."""

from __future__ import annotations

from typing import Sequence

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHeaderView,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.services.models import Session
from lazygui.widgets.filter_bar import FilterBar


_SESSION_HEADERS: tuple[str, ...] = (
    "ID",
    "Hostname",
    "OS",
    "User",
    "PID",
    "IP",
    "Last command",
)
_ID_COLUMN: int = 0


class SessionsPanel(PanelBase):
    """Reactive list of :class:`Session` rows."""

    session_selected = Signal(Session)

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Build the layout and subscribe to backend session updates."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier=constants.panel.sessions_id,
            title=constants.panel.sessions_label,
            parent=parent,
        )
        self._sessions: tuple[Session, ...] = ()
        self._filter_text: str = ""
        container = QWidget(self)
        layout = QVBoxLayout(container)
        self._filter_bar = FilterBar(constants=constants, placeholder_text="Filter by hostname, user, IP...", parent=container)
        self._tree = QTreeWidget(container)
        self._tree.setColumnCount(len(_SESSION_HEADERS))
        self._tree.setHeaderLabels(list(_SESSION_HEADERS))
        self._tree.setRootIsDecorated(False)
        self._tree.setAlternatingRowColors(True)
        self._tree.setUniformRowHeights(True)
        self._tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self._tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._tree.header().setStretchLastSection(True)
        layout.addWidget(self._filter_bar)
        layout.addWidget(self._tree)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(container)
        self._filter_bar.filter_changed.connect(self._on_filter_changed)
        self._tree.itemSelectionChanged.connect(self._on_selection_changed)
        backend.sessions_changed.connect(self._on_sessions_changed)
        self._refresh_initial()

    def _refresh_initial(self) -> None:
        """Render any sessions the backend already had at construction time."""
        initial = self._backend.known_sessions()
        if initial:
            self._on_sessions_changed(list(initial))

    def _on_sessions_changed(self, sessions: Sequence[Session]) -> None:
        """Cache the new snapshot and rebuild visible rows."""
        self._sessions = tuple(sessions)
        self._populate_visible()

    def _on_filter_changed(self, text: str) -> None:
        """Persist the current filter text and re-render."""
        self._filter_text = text.lower().strip()
        self._populate_visible()

    def _on_selection_changed(self) -> None:
        """Emit ``session_selected`` for the currently highlighted row."""
        items = self._tree.selectedItems()
        if not items:
            return
        identifier = items[0].text(_ID_COLUMN)
        for session in self._sessions:
            if session.identifier == identifier:
                self.session_selected.emit(session)
                return

    def _populate_visible(self) -> None:
        """Rebuild the tree applying the active filter."""
        self._tree.clear()
        for session in self._sessions:
            if not self._matches_filter(session):
                continue
            item = QTreeWidgetItem(
                [
                    session.identifier,
                    session.hostname,
                    session.operating_system,
                    session.user,
                    session.process_id,
                    session.ip_addresses,
                    session.last_command,
                ]
            )
            item.setTextAlignment(_ID_COLUMN, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self._tree.addTopLevelItem(item)

    def _matches_filter(self, session: Session) -> bool:
        """Return ``True`` if any visible field contains the filter text."""
        if not self._filter_text:
            return True
        haystacks = (
            session.identifier,
            session.hostname,
            session.operating_system,
            session.user,
            session.process_id,
            session.ip_addresses,
            session.last_command,
        )
        return any(self._filter_text in field.lower() for field in haystacks)
