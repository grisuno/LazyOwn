"""Frameless palette window invoked by ``Ctrl+K``."""

from __future__ import annotations

from typing import Iterable

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget

from lazygui.config.constants import AppConstants
from lazygui.widgets.command_palette_list import CommandPaletteAction, CommandPaletteList


class CommandPaletteWindow(QWidget):
    """Frameless overlay that fuzzy-filters and dispatches actions."""

    def __init__(
        self,
        constants: AppConstants,
        actions: Iterable[CommandPaletteAction],
        parent: QWidget | None = None,
    ) -> None:
        """Build the search input plus the result list."""
        super().__init__(parent, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self._constants = constants
        self.setFixedSize(
            constants.window.command_palette_width,
            constants.window.command_palette_height,
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._search = QLineEdit(self)
        self._search.setObjectName("CommandPaletteInput")
        self._search.setPlaceholderText(constants.palette.placeholder_text)
        self._list = CommandPaletteList(constants=constants, actions=actions, parent=self)
        layout.addWidget(self._search)
        layout.addWidget(self._list, stretch=1)
        self._search.textChanged.connect(self._list.apply_filter)
        self._list.action_invoked.connect(self._on_action_invoked)

    def set_actions(self, actions: Iterable[CommandPaletteAction]) -> None:
        """Replace the action set on the underlying list."""
        self._list.set_actions(actions)
        self._list.apply_filter(self._search.text())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Intercept Enter and Esc, otherwise delegate to the search box."""
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.hide()
            event.accept()
            return
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._list.invoke_current()
            event.accept()
            return
        if key == Qt.Key.Key_Down:
            self._list.setCurrentIndex(self._list.model().index(min(self._list.currentIndex().row() + 1, self._list.model().rowCount() - 1), 0))
            event.accept()
            return
        if key == Qt.Key.Key_Up:
            self._list.setCurrentIndex(self._list.model().index(max(self._list.currentIndex().row() - 1, 0), 0))
            event.accept()
            return
        super().keyPressEvent(event)

    def showEvent(self, event) -> None:
        """Move keyboard focus into the search box on every open."""
        super().showEvent(event)
        self._search.setFocus()
        self._search.selectAll()

    def _on_action_invoked(self, action: CommandPaletteAction) -> None:
        """Run the selected action and dismiss the palette."""
        self.hide()
        action.invoke()
