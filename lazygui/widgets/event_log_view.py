"""Read-only viewer for :class:`EventLog` records."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem, QWidget

from lazygui.config.constants import AppConstants
from lazygui.services.event_log import EventLog
from lazygui.services.models import EventLevel, EventRecord


_LEVEL_COLUMN: int = 0
_TIME_COLUMN: int = 1
_SOURCE_COLUMN: int = 2
_MESSAGE_COLUMN: int = 3
_COLUMN_HEADERS: tuple[str, str, str, str] = ("Level", "Time", "Source", "Message")


class EventLogView(QTreeWidget):
    """Tree-style log viewer wired to an :class:`EventLog` instance."""

    def __init__(
        self,
        constants: AppConstants,
        event_log: EventLog,
        parent: QWidget | None = None,
    ) -> None:
        """Bind the view to ``event_log`` and configure columns/headers."""
        super().__init__(parent)
        self._constants = constants
        self._event_log = event_log
        self._minimum_level = EventLevel(constants.event_log.default_level_filter)
        self.setColumnCount(len(_COLUMN_HEADERS))
        self.setHeaderLabels(list(_COLUMN_HEADERS))
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(False)
        self.header().setStretchLastSection(True)
        self.header().setSectionResizeMode(_MESSAGE_COLUMN, QHeaderView.ResizeMode.Stretch)
        font = QFont(self._constants.font.monospace_stack[0])
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(self._constants.font.monospace_pt)
        self.setFont(font)
        event_log.record_appended.connect(self._on_record_appended)
        event_log.cleared.connect(self.clear)
        for record in event_log.snapshot():
            self._append_record(record)

    def set_minimum_level(self, level: EventLevel) -> None:
        """Filter view to records of severity >= ``level`` and reload."""
        if level == self._minimum_level:
            return
        self._minimum_level = level
        self.clear()
        for record in self._event_log.snapshot(minimum_level=level):
            self._append_record(record)

    @property
    def minimum_level(self) -> EventLevel:
        """Currently active severity filter."""
        return self._minimum_level

    def _on_record_appended(self, record: EventRecord) -> None:
        """Append the record only if it passes the severity filter."""
        if record.level.numeric < self._minimum_level.numeric:
            return
        self._append_record(record)

    def _append_record(self, record: EventRecord) -> None:
        """Render a single record as a top-level item."""
        item = QTreeWidgetItem(self)
        item.setText(_LEVEL_COLUMN, record.level.value.upper())
        item.setText(_TIME_COLUMN, record.timestamp.astimezone().strftime("%H:%M:%S"))
        item.setText(_SOURCE_COLUMN, record.source)
        item.setText(_MESSAGE_COLUMN, record.message)
        item.setTextAlignment(_LEVEL_COLUMN, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.scrollToBottom()
