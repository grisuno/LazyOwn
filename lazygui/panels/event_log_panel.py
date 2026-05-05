"""Panel hosting the application-wide event log."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.services.event_log import EventLog
from lazygui.services.models import EventLevel
from lazygui.widgets.event_log_view import EventLogView


_LEVEL_LABELS: dict[EventLevel, str] = {
    EventLevel.DEBUG: "Debug",
    EventLevel.INFO: "Info",
    EventLevel.WARNING: "Warning",
    EventLevel.ERROR: "Error",
    EventLevel.CRITICAL: "Critical",
}


class EventLogPanel(PanelBase):
    """Dock panel wrapping :class:`EventLogView` plus a level filter."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        event_log: EventLog,
        parent: QWidget | None = None,
    ) -> None:
        """Compose the toolbar (level filter + clear) and the log view."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier=constants.panel.event_log_id,
            title=constants.panel.event_log_label,
            parent=parent,
        )
        self._event_log = event_log
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        toolbar = QWidget(container)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self._level_label = QLabel("Min level", toolbar)
        self._level_label.setObjectName("SubtitleLabel")
        self._level_combo = QComboBox(toolbar)
        for level in constants.event_log.levels:
            event_level = EventLevel(level)
            self._level_combo.addItem(_LEVEL_LABELS[event_level], userData=event_level)
        self._level_combo.setCurrentText(_LEVEL_LABELS[EventLevel(constants.event_log.default_level_filter)])
        self._clear_button = QPushButton("Clear", toolbar)
        toolbar_layout.addWidget(self._level_label)
        toolbar_layout.addWidget(self._level_combo)
        toolbar_layout.addStretch(stretch=1)
        toolbar_layout.addWidget(self._clear_button)
        self._view = EventLogView(constants=constants, event_log=event_log, parent=container)
        layout.addWidget(toolbar)
        layout.addWidget(self._view)
        self.setWidget(container)
        self._level_combo.currentIndexChanged.connect(self._on_level_changed)
        self._clear_button.clicked.connect(self._event_log.clear)
        backend.event_logged.connect(event_log.append)

    def _on_level_changed(self, _index: int) -> None:
        """Forward the new minimum level to the underlying view."""
        level = self._level_combo.currentData(role=Qt.ItemDataRole.UserRole)
        if isinstance(level, EventLevel):
            self._view.set_minimum_level(level)
