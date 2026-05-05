"""Connection dialog for picking a backend.

The dialog lets the operator choose between the local console and a remote
teamserver. Picked values are returned as :class:`ConnectionRequest` so the
caller decides what to do (e.g. instantiate a backend, persist last
selection, hand it off to the main window).
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.config.settings import AppSettings
from lazygui.services.models import BackendKind
from lazygui.services.teamserver_backend import TeamserverCredentials


@dataclass(frozen=True, slots=True)
class ConnectionRequest:
    """Result of a successful :class:`ConnectDialog` interaction."""

    kind: BackendKind
    credentials: TeamserverCredentials | None


_LOCAL_PAGE_INDEX: int = 0
_TEAMSERVER_PAGE_INDEX: int = 1


class ConnectDialog(QDialog):
    """Modal dialog returning a :class:`ConnectionRequest` on accept."""

    def __init__(
        self,
        constants: AppConstants,
        settings: AppSettings,
        parent: QWidget | None = None,
    ) -> None:
        """Build the form and pre-fill from persisted settings."""
        super().__init__(parent)
        self._constants = constants
        self._settings = settings
        self.setWindowTitle("Connect")
        self.setModal(True)
        self.setFixedSize(constants.window.connect_dialog_width, constants.window.connect_dialog_height)
        layout = QVBoxLayout(self)

        title = QLabel("Choose backend", self)
        title.setObjectName("TitleLabel")
        subtitle = QLabel(
            "Local console runs the cmd2 shell in this process. "
            "Teamserver connects to a running lazyc2.py instance.",
            self,
        )
        subtitle.setObjectName("SubtitleLabel")
        subtitle.setWordWrap(True)

        self._kind_combo = QComboBox(self)
        self._kind_combo.addItem("Local console", userData=BackendKind.LOCAL)
        self._kind_combo.addItem("Teamserver", userData=BackendKind.TEAMSERVER)

        self._stacked = QStackedWidget(self)
        self._stacked.addWidget(self._build_local_page())
        self._stacked.addWidget(self._build_teamserver_page())

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self._kind_combo)
        layout.addWidget(self._stacked, stretch=1)
        layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignRight)

        self._kind_combo.currentIndexChanged.connect(self._on_kind_changed)
        self._restore_last_choice()

    # --- API --------------------------------------------------------------

    def request(self) -> ConnectionRequest:
        """Translate current widget state into a :class:`ConnectionRequest`."""
        kind = self._kind_combo.currentData(role=Qt.ItemDataRole.UserRole)
        if kind is BackendKind.LOCAL:
            return ConnectionRequest(kind=kind, credentials=None)
        return ConnectionRequest(
            kind=BackendKind.TEAMSERVER,
            credentials=TeamserverCredentials(
                base_url=self._url_edit.text().strip(),
                username=self._username_edit.text().strip(),
                password=self._password_edit.text(),
                verify_tls=self._verify_check.isChecked(),
            ),
        )

    def persist_choice(self) -> None:
        """Save the picked values back into :class:`AppSettings`."""
        kind = self._kind_combo.currentData(role=Qt.ItemDataRole.UserRole)
        if kind is BackendKind.LOCAL:
            self._settings.last_backend_id = self._constants.backend.local_id
        else:
            self._settings.last_backend_id = self._constants.backend.teamserver_id
            self._settings.last_teamserver_url = self._url_edit.text().strip()
            self._settings.last_operator_name = self._username_edit.text().strip()
        self._settings.save()

    # --- Page builders ----------------------------------------------------

    def _build_local_page(self) -> QWidget:
        """Static description for the local backend page."""
        page = QWidget(self)
        layout = QVBoxLayout(page)
        description = QLabel(
            "The local console will fork the LazyOwn cmd2 shell on a PTY. "
            "All commands run with the privileges of this process.",
            page,
        )
        description.setWordWrap(True)
        description.setObjectName("SubtitleLabel")
        layout.addWidget(description)
        layout.addStretch(stretch=1)
        return page

    def _build_teamserver_page(self) -> QWidget:
        """Form for teamserver URL + credentials."""
        page = QWidget(self)
        form = QFormLayout(page)
        self._url_edit = QLineEdit(page)
        self._url_edit.setPlaceholderText("https://host:port")
        self._username_edit = QLineEdit(page)
        self._password_edit = QLineEdit(page)
        self._password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._verify_check = QCheckBox("Verify TLS certificate", page)
        form.addRow("URL", self._url_edit)
        form.addRow("Operator", self._username_edit)
        form.addRow("Password", self._password_edit)
        form.addRow("", self._verify_check)
        return page

    # --- Internals --------------------------------------------------------

    def _restore_last_choice(self) -> None:
        """Pre-fill the form from persisted settings."""
        last_id = self._settings.last_backend_id
        if last_id == self._constants.backend.teamserver_id:
            self._kind_combo.setCurrentIndex(_TEAMSERVER_PAGE_INDEX)
        else:
            self._kind_combo.setCurrentIndex(_LOCAL_PAGE_INDEX)
        self._url_edit.setText(self._settings.last_teamserver_url)
        self._username_edit.setText(self._settings.last_operator_name)

    def _on_kind_changed(self, index: int) -> None:
        """Switch the stacked widget to match the selected kind."""
        self._stacked.setCurrentIndex(index)
