"""Reusable text-filter bar with debounced ``filter_changed`` signal."""

from __future__ import annotations

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget

from lazygui.config.constants import AppConstants


class FilterBar(QWidget):
    """Single-line text filter that debounces emissions for table views."""

    filter_changed = Signal(str)

    def __init__(
        self,
        constants: AppConstants,
        placeholder_text: str,
        label_text: str = "Filter",
        parent: QWidget | None = None,
    ) -> None:
        """Lay out a label + line edit and wire up debounce timing."""
        super().__init__(parent)
        self._constants = constants
        self._label = QLabel(label_text, self)
        self._label.setObjectName("SubtitleLabel")
        self._line_edit = QLineEdit(self)
        self._line_edit.setPlaceholderText(placeholder_text)
        self._line_edit.setClearButtonEnabled(True)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self._constants.window.dock_min_height // self._constants.font.base_pt)
        layout.addWidget(self._label)
        layout.addWidget(self._line_edit, stretch=1)
        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(self._constants.timing.fuzzy_debounce_ms)
        self._debounce.timeout.connect(self._emit_filter_changed)
        self._line_edit.textChanged.connect(self._on_text_changed)

    def text(self) -> str:
        """Current filter text."""
        return self._line_edit.text()

    def clear(self) -> None:
        """Reset the filter to an empty string."""
        self._line_edit.clear()

    def _on_text_changed(self, _value: str) -> None:
        """Restart the debounce timer on any keystroke."""
        self._debounce.start()

    def _emit_filter_changed(self) -> None:
        """Emit ``filter_changed`` once the user has stopped typing."""
        self.filter_changed.emit(self._line_edit.text())
