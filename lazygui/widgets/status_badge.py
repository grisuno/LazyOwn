"""Compact label that reflects a :class:`BackendStatus` value."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QWidget

from lazygui.services.backend import BackendStatus

_STATUS_TO_OBJECT_NAME: dict[BackendStatus, str] = {
    BackendStatus.DISCONNECTED: "InfoLabel",
    BackendStatus.CONNECTING: "WarningLabel",
    BackendStatus.CONNECTED: "SuccessLabel",
    BackendStatus.DEGRADED: "WarningLabel",
    BackendStatus.ERROR: "DangerLabel",
}


class StatusBadge(QLabel):
    """Status label whose ``objectName`` reflects severity for QSS styling."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create the badge in the disconnected state."""
        super().__init__(parent)
        self.setObjectName(_STATUS_TO_OBJECT_NAME[BackendStatus.DISCONNECTED])
        self.set_status(BackendStatus.DISCONNECTED)

    def set_status(self, status: BackendStatus) -> None:
        """Update label text and the object name driving QSS colour."""
        self.setText(status.value.capitalize())
        self.setObjectName(_STATUS_TO_OBJECT_NAME[status])
        style = self.style()
        if style is not None:
            style.unpolish(self)
            style.polish(self)
