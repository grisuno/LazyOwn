"""Application bootstrap.

Wires the configuration, theme, services and main window together. The
:class:`Application` class is the only place that knows how to assemble
every subsystem; everything else accepts dependencies through its
constructor and stays testable in isolation.
"""

from __future__ import annotations

import logging
import sys
from typing import Sequence

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from lazygui.config.constants import AppConstants
from lazygui.config.paths import AppPaths
from lazygui.config.settings import AppSettings
from lazygui.services.backend import Backend, BackendStatus
from lazygui.services.event_log import EventLog
from lazygui.services.factory import BackendFactory
from lazygui.services.models import BackendKind, EventLevel, EventRecord
from lazygui.theme.manager import ThemeManager
from lazygui.windows.connect_dialog import ConnectDialog, ConnectionRequest
from lazygui.windows.main_window import MainWindow

_logger = logging.getLogger(__name__)


class Application:
    """Owns the QApplication instance and the lifetime of every subsystem."""

    def __init__(self, argv: Sequence[str] | None = None) -> None:
        """Build constants/settings/theme/backend/main-window."""
        self._constants = AppConstants()
        self._paths = AppPaths(constants=self._constants)
        self._paths.ensure_config_dir()
        self._settings = AppSettings.load(constants=self._constants, paths=self._paths)
        self._configure_logging()
        self._configure_qt_attributes()
        self._qt_app = QApplication(list(argv or sys.argv))
        self._configure_qt_application_metadata()
        self._theme_manager = ThemeManager(
            constants=self._constants,
            settings=self._settings,
            application=self._qt_app,
        )
        self._theme_manager.apply_initial()
        self._backend_factory = BackendFactory(constants=self._constants, paths=self._paths)
        self._event_log = EventLog(constants=self._constants)
        self._backend: Backend = self._build_initial_backend()
        self._main_window = MainWindow(
            constants=self._constants,
            settings=self._settings,
            theme_manager=self._theme_manager,
            backend=self._backend,
            event_log=self._event_log,
        )
        self._main_window.window_requests_connect = self.show_connect_dialog  # type: ignore[assignment]

    def run(self) -> int:
        """Show the main window, start the backend, and run the event loop."""
        self._main_window.show()
        self._start_backend(self._backend)
        return self._qt_app.exec()

    # --- Backend management ----------------------------------------------

    def show_connect_dialog(self) -> None:
        """Open the connection dialog and swap backends if accepted."""
        dialog = ConnectDialog(
            constants=self._constants,
            settings=self._settings,
            parent=self._main_window,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        request = dialog.request()
        dialog.persist_choice()
        try:
            new_backend = self._build_backend_from_request(request)
        except Exception as exc:
            QMessageBox.critical(self._main_window, "Connection error", str(exc))
            return
        self._swap_backend(new_backend)

    def _build_initial_backend(self) -> Backend:
        """Instantiate the backend remembered in settings (or local default)."""
        identifier = self._settings.last_backend_id
        if identifier == self._constants.backend.teamserver_id:
            try:
                from lazygui.services.teamserver_backend import TeamserverCredentials

                credentials = TeamserverCredentials(
                    base_url=self._settings.last_teamserver_url,
                    username=self._settings.last_operator_name,
                    password="",
                    verify_tls=False,
                )
                return self._backend_factory.create_teamserver(credentials=credentials)
            except Exception as exc:
                _logger.warning("Falling back to local backend: %s", exc)
        return self._backend_factory.create_local()

    def _build_backend_from_request(self, request: ConnectionRequest) -> Backend:
        """Instantiate a backend based on the dialog return value."""
        if request.kind is BackendKind.LOCAL:
            return self._backend_factory.create_local()
        if request.credentials is None:
            raise ValueError("Teamserver credentials missing.")
        return self._backend_factory.create_teamserver(credentials=request.credentials)

    def _swap_backend(self, new_backend: Backend) -> None:
        """Tear down the previous backend and rebuild the panels around the new one."""
        try:
            self._backend.stop()
        except Exception:
            pass
        self._backend = new_backend
        self._main_window.close()
        self._main_window = MainWindow(
            constants=self._constants,
            settings=self._settings,
            theme_manager=self._theme_manager,
            backend=self._backend,
            event_log=self._event_log,
        )
        self._main_window.window_requests_connect = self.show_connect_dialog  # type: ignore[assignment]
        self._main_window.show()
        self._start_backend(self._backend)

    def _start_backend(self, backend: Backend) -> None:
        """Connect signal handlers and call ``start()`` on the backend."""
        backend.event_logged.connect(self._event_log.append)
        try:
            backend.start()
        except Exception as exc:
            self._event_log.append(
                EventRecord.now(
                    level=EventLevel.ERROR,
                    source="application",
                    message=f"Backend failed to start: {exc}",
                )
            )
            backend._set_status(BackendStatus.ERROR)  # noqa: SLF001 — bootstrap-only fallback
        if hasattr(backend, "announce_local_operator"):
            backend.announce_local_operator()  # type: ignore[attr-defined]

    # --- Qt setup ---------------------------------------------------------

    def _configure_qt_attributes(self) -> None:
        """Set high-DPI policy before instantiating QApplication."""
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    def _configure_qt_application_metadata(self) -> None:
        """Populate organization/application metadata used by ``QSettings``."""
        QCoreApplication.setOrganizationName(self._constants.ids.organization_name)
        QCoreApplication.setOrganizationDomain(self._constants.ids.organization_domain)
        QCoreApplication.setApplicationName(self._constants.ids.application_name)

    def _configure_logging(self) -> None:
        """Install a basic log configuration directing INFO+ to stderr."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
