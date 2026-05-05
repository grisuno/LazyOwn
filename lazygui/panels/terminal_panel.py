"""Console panel hosting the :class:`TerminalView`."""

from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.widgets.terminal_view import TerminalView


class TerminalPanel(PanelBase):
    """Dock panel wiring :class:`TerminalView` to the active backend."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Compose the terminal view and connect bidirectional streams."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier=constants.panel.terminal_id,
            title=constants.panel.terminal_label,
            parent=parent,
        )
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        self._terminal = TerminalView(constants=constants, parent=container)
        layout.addWidget(self._terminal)
        self.setWidget(container)
        backend.terminal_output.connect(self._terminal.append_output)
        self._terminal.input_typed.connect(backend.feed_terminal_input)

    def focus_terminal(self) -> None:
        """Move keyboard focus into the terminal text area."""
        self._terminal.setFocus()
