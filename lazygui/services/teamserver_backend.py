"""Teamserver backend.

Talks to ``lazyc2.py`` over HTTPS using the documented JSON endpoints. A
single :class:`QTimer` polls ``/api/data`` for state, and ``/api/run`` plus
``/api/output`` are used to stream commands and their stdout/stderr.

The backend is designed to be fault-tolerant: a transient network blip
flips the status to ``DEGRADED`` and the next successful poll restores it,
without disturbing the rest of the GUI.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping, Sequence

from PySide6.QtCore import QObject, QTimer

from lazygui.config.constants import AppConstants
from lazygui.services.backend import Backend, BackendDescriptor, BackendStatus
from lazygui.services.models import EventLevel, EventRecord, Listener, Operator, Session

if TYPE_CHECKING:  # pragma: no cover
    pass


_logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class TeamserverCredentials:
    """Connection parameters for :class:`TeamserverBackend`."""

    base_url: str
    username: str
    password: str
    verify_tls: bool = False


class TeamserverBackend(Backend):
    """Polls ``lazyc2.py`` and dispatches commands via its REST endpoints."""

    def __init__(
        self,
        constants: AppConstants,
        credentials: TeamserverCredentials,
        parent: QObject | None = None,
    ) -> None:
        """Store ``credentials`` and prepare the polling timers."""
        descriptor = BackendDescriptor(
            identifier=constants.backend.teamserver_id,
            display_name="Teamserver",
            summary=f"HTTP/JSON to {credentials.base_url}",
        )
        super().__init__(descriptor=descriptor, parent=parent)
        self._constants = constants
        self._credentials = credentials
        self._session = self._build_http_session()
        self._poll_timer: QTimer | None = None
        self._output_timer: QTimer | None = None
        self._sessions: tuple[Session, ...] = ()
        self._listeners: tuple[Listener, ...] = ()
        self._busy_lock = threading.Lock()

    # --- Backend lifecycle -------------------------------------------------

    def start(self) -> None:
        """Begin polling the teamserver for state and command output."""
        if self._poll_timer is not None:
            return
        self._set_status(BackendStatus.CONNECTING)
        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(self._constants.timing.teamserver_poll_interval_ms)
        self._poll_timer.timeout.connect(self.refresh)
        self._poll_timer.start()
        self._output_timer = QTimer(self)
        self._output_timer.setInterval(self._constants.timing.teamserver_poll_interval_ms)
        self._output_timer.timeout.connect(self._poll_command_output)
        self._output_timer.start()
        self.refresh()

    def stop(self) -> None:
        """Stop polling and reset internal caches."""
        for timer_attribute in ("_poll_timer", "_output_timer"):
            timer = getattr(self, timer_attribute)
            if timer is not None:
                timer.stop()
                timer.deleteLater()
                setattr(self, timer_attribute, None)
        self._sessions = ()
        self._listeners = ()
        self._set_status(BackendStatus.DISCONNECTED)

    def send_command(self, command: str, target_session: str | None = None) -> None:
        """POST a command either to ``/api/run`` (global) or ``/issue_command``."""
        if target_session is None:
            self._post_global_command(command)
        else:
            self._post_session_command(command=command, client_id=target_session)

    def refresh(self) -> None:
        """Pull the consolidated state JSON and emit derived signals."""
        try:
            payload = self._http_get_json(self._constants.network.api_data_path)
        except Exception as exc:
            self._emit_event(EventLevel.WARNING, f"Teamserver poll failed: {exc}")
            self._set_status(BackendStatus.DEGRADED)
            return
        self._update_from_payload(payload)
        self._set_status(BackendStatus.CONNECTED)

    def resize_terminal(self, columns: int, rows: int) -> None:
        """Teamserver has no PTY; the resize signal is informational only."""
        del columns, rows

    def feed_terminal_input(self, data: str) -> None:
        """Buffer keystrokes and dispatch on newline as a global command."""
        if "\n" not in data:
            return
        for line in data.splitlines():
            stripped = line.strip()
            if stripped:
                self.send_command(stripped, target_session=None)

    def known_sessions(self) -> Sequence[Session]:
        """Most recent snapshot delivered by the last poll."""
        return self._sessions

    def known_listeners(self) -> Sequence[Listener]:
        """Most recent snapshot delivered by the last poll."""
        return self._listeners

    # --- HTTP plumbing -----------------------------------------------------

    def _build_http_session(self) -> Any:
        """Configure the ``requests.Session`` used for every call.

        Imports ``requests`` lazily so the local backend remains usable even if
        ``requests`` is not installed in the active environment.
        """
        import requests
        from requests.auth import HTTPBasicAuth

        http = requests.Session()
        http.auth = HTTPBasicAuth(self._credentials.username, self._credentials.password)
        http.headers.update({"User-Agent": self._constants.network.http_user_agent})
        http.verify = self._credentials.verify_tls
        return http

    def _http_get_json(self, path: str) -> Mapping[str, Any]:
        """Issue a GET and decode the JSON body."""
        response = self._session.get(
            self._build_url(path),
            timeout=(
                self._constants.network.http_connect_timeout_seconds,
                self._constants.network.http_read_timeout_seconds,
            ),
        )
        response.raise_for_status()
        return response.json()

    def _http_post_form(self, path: str, payload: Mapping[str, str]) -> Mapping[str, Any]:
        """Issue a form POST and decode the JSON body when present."""
        response = self._session.post(
            self._build_url(path),
            data=payload,
            timeout=(
                self._constants.network.http_connect_timeout_seconds,
                self._constants.network.http_read_timeout_seconds,
            ),
        )
        response.raise_for_status()
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {}

    def _build_url(self, path: str) -> str:
        """Compose ``base_url + path`` accounting for trailing slashes."""
        base = self._credentials.base_url.rstrip("/")
        if not path.startswith("/"):
            path = "/" + path
        return base + path

    def _post_global_command(self, command: str) -> None:
        """Run an arbitrary shell command on the teamserver via ``/api/run``."""
        try:
            payload = self._http_post_form(self._constants.network.api_run_path, {"command": command})
        except Exception as exc:
            self._emit_event(EventLevel.ERROR, f"send_command failed: {exc}")
            return
        message = payload.get("message", "command queued")
        self._emit_event(EventLevel.INFO, f"$ {command} -> {message}")

    def _post_session_command(self, command: str, client_id: str) -> None:
        """Queue a command for a specific implant via ``/issue_command``."""
        try:
            self._http_post_form(
                self._constants.network.api_issue_command_path,
                {"command": command, "client_id": client_id},
            )
        except Exception as exc:
            self._emit_event(EventLevel.ERROR, f"issue_command failed: {exc}")
            return
        self._emit_event(EventLevel.INFO, f"[{client_id}] $ {command}")

    def _poll_command_output(self) -> None:
        """Pull the global command stdout buffer and stream it to the terminal."""
        try:
            payload = self._http_get_json(self._constants.network.api_output_path)
        except Exception:
            return
        output = payload.get("output", "")
        if output:
            self.terminal_output.emit(output)

    # --- Payload normalisation --------------------------------------------

    def _update_from_payload(self, payload: Mapping[str, Any]) -> None:
        """Parse the consolidated payload and emit derived domain signals."""
        connected = payload.get("connected_clients", []) or []
        os_data: Mapping[str, str] = payload.get("os_data", {}) or {}
        hostnames: Mapping[str, str] = payload.get("hostname", {}) or {}
        pids: Mapping[str, str] = payload.get("pid", {}) or {}
        users: Mapping[str, str] = payload.get("user", {}) or {}
        ips: Mapping[str, str] = payload.get("ips", {}) or {}
        discovered: Mapping[str, str] = payload.get("discovered_ips", {}) or {}
        history: Mapping[str, list[Mapping[str, str]]] = payload.get("commands_history", {}) or {}

        new_sessions: list[Session] = []
        for client_id in connected:
            last_command = ""
            entries = history.get(client_id, [])
            if entries:
                last_command = entries[-1].get("command", "")
            new_sessions.append(
                Session(
                    identifier=str(client_id),
                    hostname=str(hostnames.get(client_id, "")),
                    operating_system=str(os_data.get(client_id, "")),
                    process_id=str(pids.get(client_id, "")),
                    user=str(users.get(client_id, "")),
                    ip_addresses=str(ips.get(client_id, "")),
                    discovered_ips=str(discovered.get(client_id, "")),
                    last_command=last_command,
                )
            )
        sessions_tuple = tuple(new_sessions)
        if sessions_tuple != self._sessions:
            self._sessions = sessions_tuple
            self.sessions_changed.emit(list(sessions_tuple))

        listeners_tuple = self._derive_listeners(payload)
        if listeners_tuple != self._listeners:
            self._listeners = listeners_tuple
            self.listeners_changed.emit(list(listeners_tuple))

        operator = self._derive_operator(payload)
        if operator is not None:
            self.operator_changed.emit(operator)

    def _derive_listeners(self, payload: Mapping[str, Any]) -> tuple[Listener, ...]:
        """Derive listener tuples from the implants/route metadata."""
        port = int(payload.get("c2_port") or self._constants.network.default_teamserver_port)
        scheme = self._constants.network.default_teamserver_scheme
        listeners: list[Listener] = []
        primary = Listener(
            identifier="primary",
            kind=scheme.upper(),
            address=self._credentials.base_url,
            port=port,
            is_secure=scheme == "https",
            description=str(payload.get("c2_route", "")),
        )
        listeners.append(primary)
        for implant in payload.get("implants", []) or []:
            if not isinstance(implant, Mapping):
                continue
            listeners.append(
                Listener(
                    identifier=str(implant.get("name", "implant")),
                    kind="IMPLANT",
                    address=str(implant.get("os", "")),
                    port=port,
                    is_secure=False,
                    description=str(implant.get("date", "")),
                )
            )
        return tuple(listeners)

    def _derive_operator(self, payload: Mapping[str, Any]) -> Operator | None:
        """Synthesise an :class:`Operator` from the auth fields in the payload."""
        username = payload.get("current_user_username")
        if not username:
            return None
        return Operator(
            name=str(username),
            role="teamserver",
            is_authenticated=bool(payload.get("is_authenticated", False)),
            karma_name=str(payload.get("karma_name", "")),
            elo=int(payload.get("elo", 0) or 0),
        )

    def _emit_event(self, level: EventLevel, message: str) -> None:
        """Forward a structured event record to the GUI."""
        record = EventRecord.now(level=level, source="teamserver", message=message)
        self.event_logged.emit(record)
        if level in (EventLevel.ERROR, EventLevel.CRITICAL):
            _logger.error(message)
