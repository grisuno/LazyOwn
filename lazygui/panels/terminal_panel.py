"""Console panel hosting the :class:`TerminalView` with beacon command support."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.widgets.terminal_view import TerminalView


class TerminalPanel(PanelBase):
    """Dock panel wiring :class:`TerminalView` to the active backend with beacon command support."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Compose the terminal view, session selector and command bar."""
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
        layout.setSpacing(0)

        command_bar = QWidget(container)
        command_layout = QHBoxLayout(command_bar)
        command_layout.setContentsMargins(4, 2, 4, 2)
        command_layout.setSpacing(4)

        self._session_label = QLabel("Target:", command_bar)
        command_layout.addWidget(self._session_label)

        self._session_combo = QComboBox(command_bar)
        self._session_combo.addItem("(C2 Server)", userData=None)
        self._session_combo.setMinimumWidth(180)
        self._session_combo.setToolTip("Select a beacon to send commands to, or C2 Server for global commands")
        command_layout.addWidget(self._session_combo)

        self._cmd_input = QLineEdit(command_bar)
        self._cmd_input.setPlaceholderText("type command... (Enter = send)")
        self._cmd_input.returnPressed.connect(self._send_beacon_command)
        command_layout.addWidget(self._cmd_input, stretch=1)

        send_btn = QPushButton("Send", command_bar)
        send_btn.clicked.connect(self._send_beacon_command)
        command_layout.addWidget(send_btn)

        layout.addWidget(command_bar)

        self._terminal = TerminalView(constants=constants, parent=container)
        layout.addWidget(self._terminal)
        self.setWidget(container)

        backend.terminal_output.connect(self._terminal.append_output)
        self._terminal.input_typed.connect(backend.feed_terminal_input)
        backend.sessions_changed.connect(self._update_session_combo)
        backend.beacon_result.connect(self._on_beacon_result)

    def focus_terminal(self) -> None:
        """Move keyboard focus into the terminal text area."""
        self._terminal.setFocus()

    def set_target_session(self, session_id: str) -> None:
        """Select a specific beacon in the dropdown."""
        for i in range(self._session_combo.count()):
            data = self._session_combo.itemData(i, Qt.ItemDataRole.UserRole)
            if data == session_id:
                self._session_combo.setCurrentIndex(i)
                return

    def _send_beacon_command(self) -> None:
        """Send the typed command to the selected beacon or C2 server."""
        command = self._cmd_input.text().strip()
        if not command:
            return
        self._cmd_input.clear()
        target = self._session_combo.currentData(Qt.ItemDataRole.UserRole)
        target_label = self._session_combo.currentText()
        if target is None:
            self._backend.send_command(command, target_session=None)
        else:
            self._backend.send_command(command, target_session=str(target))
        self._terminal.append_output(f"\n[{target_label}] $ {command}\n")

    def _update_session_combo(self, sessions: list) -> None:
        """Update the session dropdown with current beacons."""
        current_selection = self._session_combo.currentData(Qt.ItemDataRole.UserRole)
        self._session_combo.blockSignals(True)
        self._session_combo.clear()
        self._session_combo.addItem("(C2 Server)", userData=None)
        for session in sessions:
            label = f"[{session.operating_system[:3]}] {session.hostname or session.identifier[:8]}"
            self._session_combo.addItem(label, userData=session.identifier)
        for i in range(self._session_combo.count()):
            if self._session_combo.itemData(i, Qt.ItemDataRole.UserRole) == current_selection:
                self._session_combo.setCurrentIndex(i)
                break
        self._session_combo.blockSignals(False)

    def _on_beacon_result(self, result) -> None:
        """Display beacon command results in the terminal."""
        self._terminal.append_output(
            f"\n=== [{result.client_id}] {result.command} ===\n{result.output}\n=== END ===\n"
        )
