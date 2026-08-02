"""Application bootstrap.

Wires the configuration, theme, services and main window together. The
:class:`Application` class is the only place that knows how to assemble
every subsystem; everything else accepts dependencies through its
constructor and stays testable in isolation.
"""

from __future__ import annotations

import logging
import sys
from collections.abc import Sequence

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from lazygui.config.c2_credentials import C2Credentials, load_c2_credentials
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
        self._c2_credentials: C2Credentials = self._discover_credentials()
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

    # --- Credential discovery ---------------------------------------------

    def _discover_credentials(self) -> C2Credentials:
        """Attempt to load auto-generated credentials from the project root.

        ``lazyc2.py`` writes ``.c2_credentials.txt`` at startup with strong
        auto-generated credentials. When the file exists and the operator
        has not already manually configured teamserver credentials, those
        values are used for the initial connection.
        """
        creds = load_c2_credentials(self._paths.project_root)
        if not creds.loaded:
            return C2Credentials.empty()
        if self._settings.c2_credentials_loaded:
            return C2Credentials.empty()
        _logger.info("Discovered C2 credentials for user %s", creds.username)
        return creds

    def _sync_credentials_to_settings(self, credentials: C2Credentials) -> None:
        """Persist auto-discovered credentials into settings."""
        if not credentials.loaded:
            return
        self._settings.last_operator_name = credentials.username
        self._settings.last_teamserver_password = credentials.password
        self._settings.c2_credentials_loaded = True
        self._settings.save()

    # --- Backend management ----------------------------------------------

    def show_connect_dialog(self) -> None:
        """Open the connection dialog and swap backends if accepted."""
        dialog = ConnectDialog(
            constants=self._constants,
            settings=self._settings,
            paths=self._paths,
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
        """Instantiate the backend remembered in settings or auto-discovered.

        When the last backend is ``teamserver``, credentials are resolved in
        this order:
        1. Auto-generated ``.c2_credentials.txt`` (if present and fresh)
        2. Persisted settings (operator name + password)
        3. Fall back to local backend (never connect with empty credentials)
        """
        identifier = self._settings.last_backend_id
        if identifier != self._constants.backend.teamserver_id:
            return self._backend_factory.create_local()
        try:
            from lazygui.services.teamserver_backend import TeamserverCredentials

            username, password = self._resolve_teamserver_credentials()
            if not username or not password:
                _logger.info("No teamserver credentials available, falling back to local backend")
                return self._backend_factory.create_local()

            credentials = TeamserverCredentials(
                base_url=self._settings.last_teamserver_url,
                username=username,
                password=password,
                verify_tls=False,
            )
            return self._backend_factory.create_teamserver(credentials=credentials)
        except Exception as exc:
            _logger.warning("Falling back to local backend: %s", exc)
        return self._backend_factory.create_local()

    def _resolve_teamserver_credentials(self) -> tuple[str, str]:
        """Return ``(username, password)`` from the best available source.

        Priority:
        1. Auto-discovered ``.c2_credentials.txt`` (fresh, not yet consumed)
        2. Persisted settings (previously used credentials)
        3. Empty tuple (triggers local fallback)
        """
        if self._c2_credentials.loaded:
            self._sync_credentials_to_settings(self._c2_credentials)
            return (self._c2_credentials.username, self._c2_credentials.password)
        stored_username = self._settings.last_operator_name
        stored_password = self._settings.last_teamserver_password
        if stored_username and stored_password:
            return (stored_username, stored_password)
        return ("", "")

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
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s %(name)s: %(message)s"
                )
            )
            logger.addHandler(handler)
