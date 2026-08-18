"""Beacon command modal — send commands to beacons and inspect full history.

The modal is the primary operator surface for issuing commands to a beacon
implant and reviewing both real-time results and the persisted command
history served by the teamserver. History is loaded from the backend
(request_beacon_history) so prior engagements survive restarts; live results
stream in through the ``beacon_result`` signal.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import (
    QComboBox,
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


@dataclass(frozen=True, slots=True)
class _HistoryEntry:
    """A single command/result entry shown in the modal history list."""

    client_id: str
    command: str
    timestamp: str = ""
    output: str = ""


class BeaconCommandModal(QDialog):
    """Modal dialog for executing commands on a beacon and viewing results.

    Signals:
        command_sent: Emitted with the target and command when dispatched.
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
        self._entries: list[_HistoryEntry] = []
        self._history: list[_HistoryEntry] = []
        self.setWindowTitle("Beacon Command")
        self.setMinimumSize(860, 640)
        self.setModal(True)
        self._build_ui()
        backend.beacon_result.connect(self._on_beacon_result)
        backend.sessions_changed.connect(self._on_sessions_changed)

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)

        target_row = QHBoxLayout()
        target_row.addWidget(QLabel("Target:", self))
        self._target_combo = QComboBox(self)
        self._target_combo.setEditable(True)
        self._target_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self._target_combo.setPlaceholderText("Select (C2) or enter a beacon id")
        self._target_combo.addItem("(C2)")
        self._target_combo.currentTextChanged.connect(self._on_target_changed)
        target_row.addWidget(self._target_combo, stretch=1)
        self._load_btn = QPushButton("Load History", self)
        self._load_btn.clicked.connect(self._reload_history)
        target_row.addWidget(self._load_btn)
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
        self._output_view.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        right_col.addWidget(self._output_view)
        body.addLayout(right_col, stretch=3)

        main_layout.addLayout(body)

    def _selected_target(self) -> str:
        """Return the current target id, or empty string for the C2 global."""
        text = self._target_combo.currentText().strip()
        return "" if text == "(C2)" or not text else text

    def _on_target_changed(self, _text: str) -> None:
        self._output_view.clear()
        self._reload_history()

    def _reload_history(self) -> None:
        """Load and render the persisted history for the selected target."""
        self._history_list.clear()
        target = self._selected_target()
        if not target:
            return
        records: list[dict] = []
        try:
            records = self._backend.request_beacon_history(target)
        except Exception:
            records = []
        if not records:
            for session in self._backend.known_sessions():
                if str(getattr(session, "identifier", "")) == target:
                    last = getattr(session, "last_command", "")
                    if last:
                        records = [{"client_id": target, "command": last, "output": ""}]
                    break
        self._history = []
        for record in records:
            entry = _HistoryEntry(
                client_id=str(record.get("client_id", target)),
                command=str(record.get("command", "")),
                timestamp=str(record.get("timestamp", "")),
                output=str(record.get("output", "")),
            )
            self._history.append(entry)
            label = f"[{entry.client_id}] {entry.command}"
            if entry.timestamp:
                label = f"{entry.timestamp[:19]}  {label}"
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, len(self._history) - 1)
            self._history_list.addItem(item)
        if self._history:
            self._history_list.setCurrentRow(0)
            self._render_entry(0)

    def _on_sessions_changed(self, sessions: list) -> None:
        """Refresh the target selector from the backend session list."""
        current = self._selected_target()
        self._target_combo.blockSignals(True)
        for session in sessions:
            cid = str(getattr(session, "identifier", ""))
            if cid and self._target_combo.findText(cid) == -1:
                self._target_combo.addItem(cid)
        if current:
            idx = self._target_combo.findText(current)
            if idx >= 0:
                self._target_combo.setCurrentIndex(idx)
        self._target_combo.blockSignals(False)

    def _send_command(self) -> None:
        """Dispatch the typed command to the selected beacon."""
        command = self._cmd_input.text().strip()
        if not command:
            return
        self._cmd_input.clear()
        target = self._selected_target()
        self._backend.send_command(command, target_session=target or None)
        entry = _HistoryEntry(client_id=target or "(C2)", command=command)
        self._history.append(entry)
        self._history_list.insertItem(0, QListWidgetItem(f"[{entry.client_id}] {command}"))
        self._output_view.appendPlainText(f"\n$ {command}\n")
        self.command_sent.emit(target or "", command)

    def _on_history_clicked(self, item: QListWidgetItem) -> None:
        data = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(data, int) and 0 <= data < len(self._history):
            self._last_entry(data)

    def _last_entry(self, index: int) -> None:
        entry = self._history[index]
        self._output_view.clear()
        header = f"=== [{entry.client_id}] {entry.command} ==="
        if entry.timestamp:
            header += f"  ({entry.timestamp})"
        self._output_view.appendPlainText(f"{header}\n{entry.output}\n=== END ===\n")

    def _on_beacon_result(self, result: BeaconResult) -> None:
        """Append a live beacon result to the output view and history."""
        cmd = str(result.command or "")
        text = f"\n=== [{result.client_id}] {cmd} ===\n{result.output}\n=== END ===\n"
        self._output_view.appendPlainText(text)
        self._history.append(
            _HistoryEntry(client_id=result.client_id, command=cmd, output=result.output)
        )

    def open(self) -> None:  # noqa: A003 - Qt API override
        """Populate sessions before showing."""
        try:
            sessions = list(self._backend.known_sessions())
            if sessions:
                self._on_sessions_changed(sessions)
            self._reload_history()
        except Exception:
            pass
        super().open()

    def focus_input(self) -> None:
        """Move keyboard focus to the command input."""
        self._cmd_input.setFocus()
