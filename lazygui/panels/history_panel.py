"""Command history panel showing beacon command logs.

Reads ``sessions/<client_id>.log`` CSV files and displays command entries
with output. Supports filtering by client and auto-refresh.
"""

from __future__ import annotations

import csv
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend


class HistoryPanel(PanelBase):
    """Dock panel showing beacon command history from CSV log files."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Build the history viewer UI."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier="panel.history",
            title="History",
            parent=parent,
        )
        self._sessions_dir: Path = Path("sessions")
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = QHBoxLayout()
        title = QLabel("Command History", container)
        title.setObjectName("SubtitleLabel")
        header.addWidget(title)
        header.addStretch()
        self._client_combo = QComboBox(container)
        self._client_combo.setMinimumWidth(150)
        self._client_combo.currentTextChanged.connect(self._populate)
        header.addWidget(self._client_combo)
        refresh_btn = QPushButton("Refresh", container)
        refresh_btn.clicked.connect(self._refresh)
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        self._tree = QTreeWidget(container)
        self._tree.setColumnCount(3)
        self._tree.setHeaderLabels(["Command", "Output", "When"])
        self._tree.setRootIsDecorated(False)
        self._tree.setAlternatingRowColors(True)
        self._tree.setUniformRowHeights(True)
        self._tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self._tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._tree.header().setStretchLastSection(True)
        layout.addWidget(self._tree)

        self.setWidget(container)

        backend.sessions_changed.connect(lambda _: self._refresh())
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(constants.timing.panel_refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start()
        self._refresh()

    def _refresh(self) -> None:
        current = self._client_combo.currentText()
        entries: list[str] = []
        if self._sessions_dir.is_dir():
            for log_file in sorted(self._sessions_dir.glob("*.log"), reverse=True):
                name = log_file.stem
                if name not in entries:
                    entries.append(name)
        self._client_combo.blockSignals(True)
        self._client_combo.clear()
        self._client_combo.addItem("(select client)")
        for entry in entries:
            self._client_combo.addItem(entry)
        idx = self._client_combo.findText(current)
        if idx >= 0:
            self._client_combo.setCurrentIndex(idx)
        self._client_combo.blockSignals(False)
        self._populate()

    def _populate(self) -> None:
        self._tree.clear()
        client = self._client_combo.currentText()
        if client == "(select client)" or not client:
            return
        log_path = self._sessions_dir / f"{client}.log"
        if not log_path.is_file():
            return
        try:
            with open(log_path, "r", newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cmd = row.get("command", "")
                    out = row.get("output", "")
                    ts = row.get("timestamp", row.get("when", ""))
                    item = QTreeWidgetItem([cmd, out[:200], ts])
                    item.setToolTip(1, out)
                    self._tree.addTopLevelItem(item)
        except Exception:
            pass
