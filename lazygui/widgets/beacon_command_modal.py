"""Beacon command modal — send commands to beacons and view results."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from lazygui.services.backend import Backend
from lazygui.services.models import BeaconResult


class BeaconCommandModal(QDialog):
    """Modal dialog for executing commands on a beacon and viewing results.

    Signals:
        command_sent: Emitted when a command is dispatched.
    """

    command_sent = Signal(str, str)

    def __init__(
        self,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Initialise the modal with a backend reference.

        Args:
            backend: The active backend for dispatching commands.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._backend = backend
        self._command_history: dict[str, list[str]] = {}
        self.setWindowTitle("Beacon Command")
        self.setMinimumSize(800, 600)
        self.setModal(True)
        self._build_ui()
        backend.beacon_result.connect(self._on_beacon_result)
        backend.sessions_changed.connect(self._on_sessions_changed)

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)

        target_row = QHBoxLayout()
        target_row.addWidget(QLabel("Target:", self))
        self._target_combo = QLineEdit(self)
        self._target_combo.setPlaceholderText("Beacon ID (or leave empty for C2)")
        target_row.addWidget(self._target_combo, stretch=1)
        main_layout.addLayout(target_row)

        cmd_row = QHBoxLayout()
        self._cmd_input = QLineEdit(self)
        self._cmd_input.setPlaceholderText("Command... (Enter = send)")
        self._cmd_input.returnPressed.connect(self._send_command)
        cmd_row.addWidget(self._cmd_input, stretch=1)
        send_btn = QPushButton("Send", self)
        send_btn.clicked.connect(self._send_command)
        cmd_row.addWidget(send_btn)
        main_layout.addLayout(cmd_row)

        body = QHBoxLayout()

        left_col = QVBoxLayout()
        left_col.addWidget(QLabel("History", self))
        self._history_list = QListWidget(self)
        self._history_list.itemClicked.connect(self._on_history_clicked)
        left_col.addWidget(self._history_list)
        body.addLayout(left_col, stretch=1)

        right_col = QVBoxLayout()
        right_col.addWidget(QLabel("Output", self))
        self._output_view = QPlainTextEdit(self)
        self._output_view.setReadOnly(True)
        self._output_view.setStyleSheet("font-family: monospace; font-size: 11px;")
        right_col.addWidget(self._output_view)
        body.addLayout(right_col, stretch=3)

        main_layout.addLayout(body)

    def _send_command(self) -> None:
        """Dispatch the typed command to the selected beacon."""
        command = self._cmd_input.text().strip()
        if not command:
            return
        self._cmd_input.clear()
        target_id = self._target_combo.text().strip() or None
        if target_id:
            self._backend.send_command(command, target_session=target_id)
        else:
            self._backend.send_command(command, target_session=None)

        cid = target_id or "(C2)"
        self._add_history_entry(cid, command)

    def _add_history_entry(self, client_id: str, command: str) -> None:
        if client_id not in self._command_history:
            self._command_history[client_id] = []
        self._command_history[client_id].append(command)
        item = QListWidgetItem(f"[{client_id}] {command}")
        item.setData(Qt.ItemDataRole.UserRole, (client_id, command))
        self._history_list.insertItem(0, item)

    def _on_history_clicked(self, item: QListWidgetItem) -> None:
        data = item.data(Qt.ItemDataRole.UserRole)
        if data and isinstance(data, tuple):
            client_id, command = data
            self._target_combo.setText(client_id if client_id != "(C2)" else "")
            self._cmd_input.setText(command)
            self._cmd_input.setFocus()

    def _on_beacon_result(self, result: BeaconResult) -> None:
        """Display beacon command result in the output view."""
        self._output_view.appendPlainText(
            f"\n=== [{result.client_id}] {result.command} ===\n{result.output}\n=== END ===\n"
        )

    def _on_sessions_changed(self, sessions: list) -> None:
        """Update when sessions change (no-op: kept for future use)."""
        pass

    def focus_input(self) -> None:
        """Move keyboard focus to the command input."""
        self._cmd_input.setFocus()
