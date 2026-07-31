"""Credentials and loot panel for the operator console.

Displays captured credentials, hashes, and exfiltrated artefacts
from the active backend's session data. Supports filtering and
copy-on-click for credential reuse.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend


class CredentialsPanel(PanelBase):
    """Dock widget displaying captured credentials and loot."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            constants=constants,
            backend=backend,
            identifier=constants.panel.credentials_panel_id,
            title="Credentials",
            parent=parent,
        )
        self._build_ui()
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(constants.timing.panel_refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start()
        self._refresh()

    def _build_ui(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = QHBoxLayout()
        title = QLabel("Credentials & Loot", container)
        title.setObjectName("SubtitleLabel")
        header.addWidget(title)
        header.addStretch()
        copy_btn = QPushButton("Copy Selected", container)
        copy_btn.clicked.connect(self._copy_selected)
        header.addWidget(copy_btn)
        refresh_btn = QPushButton("Refresh", container)
        refresh_btn.clicked.connect(self._refresh)
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        self._creds_label = QLabel("Credentials", container)
        self._creds_label.setObjectName("CaptionLabel")
        layout.addWidget(self._creds_label)

        self._creds_list = QListWidget(container)
        self._creds_list.setAlternatingRowColors(True)
        layout.addWidget(self._creds_list)

        self._hashes_label = QLabel("Hashes", container)
        self._hashes_label.setObjectName("CaptionLabel")
        layout.addWidget(self._hashes_label)

        self._hashes_list = QListWidget(container)
        self._hashes_list.setAlternatingRowColors(True)
        layout.addWidget(self._hashes_list)

        self._loot_label = QLabel("Loot Files", container)
        self._loot_label.setObjectName("CaptionLabel")
        layout.addWidget(self._loot_label)

        self._loot_list = QListWidget(container)
        self._loot_list.setAlternatingRowColors(True)
        layout.addWidget(self._loot_list)

        self.setWidget(container)

    def _refresh(self) -> None:
        try:
            data = self._backend.request_session_state()
        except Exception:
            data = {}
        creds = data.get("credentials", [])
        hashes = data.get("hashes", [])
        loot = data.get("loot", [])

        self._creds_list.clear()
        for c in creds:
            user = c.get("username", "?")
            kind = c.get("type", "password")
            source = c.get("source", "")
            item = QListWidgetItem(f"{user} [{kind}] — {source}")
            item.setData(Qt.ItemDataRole.UserRole, f"{user}")
            self._creds_list.addItem(item)
        self._creds_label.setText(f"Credentials ({len(creds)})")

        self._hashes_list.clear()
        for h in hashes:
            text = h if isinstance(h, str) else h.get("hash", str(h))
            item = QListWidgetItem(text[:120])
            item.setData(Qt.ItemDataRole.UserRole, text)
            self._hashes_list.addItem(item)
        self._hashes_label.setText(f"Hashes ({len(hashes)})")

        self._loot_list.clear()
        for lf in loot:
            name = lf.get("name", lf) if isinstance(lf, dict) else str(lf)
            size = lf.get("size", "") if isinstance(lf, dict) else ""
            item = QListWidgetItem(f"{name} {size}")
            self._loot_list.addItem(item)
        self._loot_label.setText(f"Loot ({len(loot)})")

    def _copy_selected(self) -> None:
        selected = (
            self._creds_list.currentItem()
            or self._hashes_list.currentItem()
        )
        if selected is None:
            return
        value = selected.data(Qt.ItemDataRole.UserRole) or selected.text()
        QApplication.clipboard().setText(str(value))


__all__ = ["CredentialsPanel"]
