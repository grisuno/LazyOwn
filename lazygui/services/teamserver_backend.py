"""Teamserver backend with Socket.IO real-time and full HTTP API coverage.

Connects to ``lazyc2.py`` via HTTP REST + Socket.IO WebSocket. The backend
provides bidirectional terminal access, beacon command/result flow, graph
topology streaming, dashboard aggregation, listener management and campaign
tracking. Fault-tolerant with automatic reconnection and graceful degradation.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QObject, QTimer

from lazygui.config.constants import AppConstants
from lazygui.services.backend import Backend, BackendDescriptor, BackendStatus
from lazygui.services.models import (
    BeaconResult,
    CampaignSummary,
    DashboardPayload,
    EventLevel,
    EventRecord,
    GraphEdge,
    GraphNode,
    Listener,
    Operator,
    Session,
    Topology,
)

_logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class TeamserverCredentials:
    """Connection parameters for :class:`TeamserverBackend`."""

    base_url: str
    username: str
    password: str
    verify_tls: bool = False


class TeamserverBackend(Backend):
    """Real-time backend communicating with ``lazyc2.py`` over HTTP + Socket.IO."""

    def __init__(
        self,
        constants: AppConstants,
        credentials: TeamserverCredentials,
        parent: QObject | None = None,
    ) -> None:
        """Store ``credentials`` and prepare polling timers and Socket.IO client."""
        descriptor = BackendDescriptor(
            identifier=constants.backend.teamserver_id,
            display_name="Teamserver",
            summary=f"HTTP + Socket.IO to {credentials.base_url}",
        )
        super().__init__(descriptor=descriptor, parent=parent)
        self._constants = constants
        self._credentials = credentials
        self._http = self._build_http_session()
        self._sio_client: Any = None
        self._sio_thread: threading.Thread | None = None
        self._poll_timer: QTimer | None = None
        self._graph_timer: QTimer | None = None
        self._sessions: tuple[Session, ...] = ()
        self._listeners: tuple[Listener, ...] = ()
        self._topology: Topology = Topology.empty()
        self._campaigns: tuple[CampaignSummary, ...] = ()
        self._last_payload: dict[str, Any] = {}
        self._busy_lock = threading.Lock()

    def start(self) -> None:
        """Begin polling and establish Socket.IO connection.

        First authenticates via the C2 login form to obtain a Flask session
        cookie. Then starts HTTP polling and Socket.IO after authentication
        completes, so the WebSocket upgrade carries the session cookie.
        """
        if self._poll_timer is not None:
            return
        self._set_status(BackendStatus.CONNECTING)
        self._establish_flask_session()
        self._install_http_polling()
        self._start_socketio()
        self.refresh()
        self._refresh_topology()
        self._refresh_dashboard()

    def stop(self) -> None:
        """Tear down all timers and Socket.IO connection."""
        for attr in ("_poll_timer", "_graph_timer"):
            timer: QTimer | None = getattr(self, attr, None)
            if timer is not None:
                timer.stop()
                timer.deleteLater()
                setattr(self, attr, None)
        self._stop_socketio()
        self._sessions = ()
        self._listeners = ()
        self._topology = Topology.empty()
        self._campaigns = ()
        self._set_status(BackendStatus.DISCONNECTED)

    def send_command(self, command: str, target_session: str | None = None) -> None:
        """Submit ``command`` via Socket.IO PTY (global) or ``/issue_command`` (beacon).

        Global commands go through Socket.IO ``/pty`` to reach the PTY
        directly and bypass CSRF. Beacon commands POST to ``/issue_command``
        which the implant polls.
        """
        if target_session is None:
            self._send_command_via_pty(command)
        else:
            self._post_session_command(command=command, client_id=target_session)

    def refresh(self) -> None:
        """Pull consolidated state JSON and emit derived signals."""
        try:
            payload = self._http_get_json(self._constants.network.api_data_path)
        except Exception as exc:
            status_code = getattr(exc, 'response', None)
            status_text = f"HTTP {status_code.status_code}" if status_code is not None else str(exc)
            self._emit_event(EventLevel.WARNING, f"Teamserver poll failed: {status_text}")
            self._set_status(BackendStatus.DEGRADED)
            return
        self._last_payload = payload if isinstance(payload, Mapping) else {}
        self._update_from_payload(self._last_payload)
        self._build_topology_from_payload(self._last_payload)
        self._set_status(BackendStatus.CONNECTED)

    def resize_terminal(self, columns: int, rows: int) -> None:
        """Forward resize to Socket.IO PTY namespace when connected."""
        if self._sio_client is not None:
            try:
                self._sio_client.emit(
                    self._constants.network.socketio_event_resize,
                    {"cols": columns, "rows": rows},
                    namespace=self._constants.network.socketio_namespace_pty,
                )
            except Exception:
                pass

    def feed_terminal_input(self, data: str) -> None:
        """Feed keystrokes to the PTY via Socket.IO, falling back to HTTP commands.

        Socket.IO ``/pty`` namespace sends raw input directly to the PTY
        and bypasses CSRF checks, so it is preferred when available.
        """
        if self._sio_client is not None:
            try:
                self._sio_client.emit(
                    self._constants.network.socketio_event_pty_input,
                    {"input": data},
                    namespace=self._constants.network.socketio_namespace_pty,
                )
                return
            except Exception:
                pass
        self._dispatch_terminal_lines(data)

    def known_sessions(self) -> Sequence[Session]:
        """Most recent snapshot delivered by the last poll."""
        return self._sessions

    def known_listeners(self) -> Sequence[Listener]:
        """Most recent snapshot delivered by the last poll."""
        return self._listeners

    def known_topology(self) -> Topology:
        """Most recent graph topology snapshot."""
        return self._topology

    def known_campaigns(self) -> Sequence[CampaignSummary]:
        """Most recent campaign snapshot."""
        return self._campaigns

    def request_beacon_results(self, client_id: str) -> None:
        """Fetch stored command results for a specific beacon."""
        try:
            payload = self._http_get_json(self._constants.network.get_results_path)
            if isinstance(payload, Mapping) and client_id in payload:
                result_data = payload[client_id]
                if isinstance(result_data, Mapping):
                    self.beacon_result.emit(
                        BeaconResult(
                            client_id=str(client_id),
                            output=str(result_data.get("output", "")),
                            command=str(result_data.get("command", "")),
                            operating_system=str(result_data.get("client", "")),
                            hostname=str(result_data.get("hostname", "")),
                            user=str(result_data.get("user", "")),
                            ips=str(result_data.get("ips", "")),
                            pid=str(result_data.get("pid", "")),
                            discovered_ips=str(result_data.get("discovered_ips", "")),
                            result_portscan=str(result_data.get("result_portscan", "")),
                            result_pwd=str(result_data.get("result_pwd", "")),
                        )
                    )
        except Exception as exc:
            self._emit_event(EventLevel.WARNING, f"Results fetch failed for {client_id}: {exc}")

    # --- HTTP plumbing -----------------------------------------------------

    def _establish_flask_session(self) -> None:
        """Authenticate with the C2 via the login form to obtain a session cookie.

        Flask-Login requires a session cookie for Socket.IO namespace access.
        A form POST to ``/login`` authenticates the operator and sets the
        session cookie on the ``requests.Session``, which is then forwarded
        to the Socket.IO upgrade request.
        """
        try:
            self._http_post_form(
                "/login",
                {"username": self._credentials.username, "password": self._credentials.password},
            )
            self._emit_event(EventLevel.DEBUG, "Flask session established via /login")
        except Exception as exc:
            self._emit_event(EventLevel.WARNING, f"Flask session login failed: {exc}; Socket.IO may not connect")

    def _build_http_session(self) -> Any:
        import requests
        from requests.auth import HTTPBasicAuth

        http = requests.Session()
        http.auth = HTTPBasicAuth(self._credentials.username, self._credentials.password)
        http.headers.update({"User-Agent": self._constants.network.http_user_agent})
        http.verify = self._credentials.verify_tls
        return http

    def _build_url(self, path: str) -> str:
        base = self._credentials.base_url.rstrip("/")
        if not path.startswith("/"):
            path = "/" + path
        return base + path

    def _http_get_json(self, path: str) -> Any:
        response = self._http.get(
            self._build_url(path),
            timeout=(
                self._constants.network.http_connect_timeout_seconds,
                self._constants.network.http_read_timeout_seconds,
            ),
        )
        if not response.ok:
            body = response.text[:500] if response.text else ""
            _logger.debug("HTTP %s %s response body: %s", response.status_code, path, body)
        response.raise_for_status()
        return response.json()

    def _http_post_form(self, path: str, payload: Mapping[str, Any]) -> Any:
        response = self._http.post(
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

    def _http_post_json(self, path: str, payload: Mapping[str, Any]) -> Any:
        response = self._http.post(
            self._build_url(path),
            json=payload,
            timeout=(
                self._constants.network.http_connect_timeout_seconds,
                self._constants.network.http_read_timeout_seconds,
            ),
        )
        response.raise_for_status()
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {}

    def _post_global_command(self, command: str) -> None:
        """Send a command via Socket.IO PTY instead of ``/api/run``.

        ``/api/run`` requires CSRF which is not available to the desktop
        GUI. Socket.IO ``/pty`` bypasses CSRF entirely because auth is
        handled at connection time.
        """
        self._send_command_via_pty(command)

    def _post_session_command(self, command: str, client_id: str) -> None:
        try:
            self._http_post_form(
                self._constants.network.api_issue_command_path,
                {"command": command, "client_id": client_id},
            )
        except Exception as exc:
            self._emit_event(EventLevel.ERROR, f"issue_command failed: {exc}")
            return
        self._emit_event(EventLevel.INFO, f"[{client_id}] $ {command}")

    def _send_command_via_pty(self, command: str) -> None:
        """Send a command through the Socket.IO ``/pty`` namespace.

        Bypasses CSRF entirely because Socket.IO authentication is handled
        at connection time. Falls back to emitting the command attempt as an
        event when the Socket.IO client is not connected.
        """
        if self._sio_client is not None:
            try:
                self._sio_client.emit(
                    self._constants.network.socketio_event_pty_input,
                    {"input": command + "\n"},
                    namespace=self._constants.network.socketio_namespace_pty,
                )
                self._emit_event(EventLevel.INFO, f"$ {command}")
                return
            except Exception as exc:
                self._emit_event(EventLevel.ERROR, f"PTY command failed: {exc}")
                return
        self._emit_event(EventLevel.WARNING, f"Socket.IO not connected; cannot run: {command}")

    def _dispatch_terminal_lines(self, data: str) -> None:
        if "\n" not in data:
            return
        for line in data.splitlines():
            stripped = line.strip()
            if stripped:
                self._send_command_via_pty(stripped)

    def _poll_command_output(self) -> None:
        try:
            payload = self._http_get_json(self._constants.network.api_output_path)
        except Exception:
            return
        output = payload.get("output", "") if isinstance(payload, Mapping) else ""
        if output:
            self.terminal_output.emit(output)

    def _refresh_topology(self) -> None:
        """Rebuild topology from the last known payload.

        The graph is built from ``/api/data`` fields: ``connected_clients``,
        ``connected_hosts``, ``discovered_ips``, ``result_portscan``,
        ``os_data``, ``hostname``, ``ips``, and ``local_ips``.
        """
        if self._last_payload:
            self._build_topology_from_payload(self._last_payload)

    def _refresh_dashboard(self) -> None:
        try:
            payload = self._http_get_json(self._constants.network.api_dashboard_path)
        except Exception:
            return
        events: list[EventRecord] = []
        raw_events = payload.get("events", []) or []
        for evt in raw_events if isinstance(raw_events, list) else []:
            if isinstance(evt, Mapping):
                events.append(
                    EventRecord.now(
                        level=EventLevel.INFO,
                        source="teamserver",
                        message=str(evt.get("message", evt.get("summary", str(evt)))),
                    )
                )
        dashboard = DashboardPayload(
            connected_clients=tuple(payload.get("connected_clients", []) or []),
            beacon_count=int(payload.get("beacon_count", 0) or 0),
            events=tuple(events),
            campaign_state=payload.get("campaign", {}) or {},
            facts_count=int(payload.get("facts_count", 0) or 0),
            last_update=str(payload.get("last_update", "")),
        )
        self.dashboard_updated.emit(dashboard)

    # --- Polling timers setup ------------------------------------------------

    def _install_http_polling(self) -> None:
        interval = self._constants.timing.teamserver_poll_interval_ms
        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(interval)
        self._poll_timer.timeout.connect(self.refresh)
        self._poll_timer.start()
        self._graph_timer = QTimer(self)
        self._graph_timer.setInterval(interval)
        self._graph_timer.timeout.connect(self._refresh_topology)
        self._graph_timer.start()

    # --- Socket.IO client ----------------------------------------------------

    def _start_socketio(self) -> None:
        def _connect_sio() -> None:
            import socketio

            client = socketio.Client(
                reconnection=True,
                reconnection_attempts=self._constants.network.socketio_reconnect_max_attempts,
                reconnection_delay=self._constants.timing.websocket_reconnect_delay_ms / 1000.0,
                reconnection_delay_max=30.0,
                ssl_verify=False,
                logger=False,
                engineio_logger=False,
            )
            ns_pty = self._constants.network.socketio_namespace_pty
            ns_terminal = self._constants.network.socketio_namespace_terminal
            ns_default = self._constants.network.socketio_namespace_default

            @client.on("connect", namespace=ns_pty)
            def _on_pty_connect() -> None:
                self._emit_event(EventLevel.DEBUG, "Socket.IO /pty connected")

            @client.on(self._constants.network.socketio_event_pty_output, namespace=ns_pty)
            def _on_pty_output(data: dict) -> None:
                output = (data or {}).get("output", "")
                if output:
                    self.terminal_output.emit(str(output))

            @client.on("connect", namespace=ns_terminal)
            def _on_terminal_connect() -> None:
                self._emit_event(EventLevel.DEBUG, "Socket.IO /terminal connected")

            @client.on(self._constants.network.socketio_event_response, namespace=ns_terminal)
            def _on_terminal_response(data: dict) -> None:
                output = (data or {}).get("output", "")
                if output:
                    self.terminal_output.emit(str(output))

            @client.on(self._constants.network.socketio_event_output, namespace=ns_default)
            def _on_output(data: dict) -> None:
                output = (data or {}).get("data", (data or {}).get("output", ""))
                if output:
                    self.terminal_output.emit(str(output))

            @client.on("connect")
            def _on_connect() -> None:
                self._emit_event(EventLevel.DEBUG, "Socket.IO default namespace connected")

            @client.on("disconnect")
            def _on_disconnect() -> None:
                self._emit_event(EventLevel.DEBUG, "Socket.IO disconnected")

            try:
                import base64
                auth_b64 = base64.b64encode(
                    f"{self._credentials.username}:{self._credentials.password}".encode()
                ).decode()
                auth_header = f"Basic {auth_b64}"
                cookie_header = "; ".join(
                    f"{key}={value}"
                    for key, value in self._http.cookies.get_dict().items()
                )
                connect_headers = {"Authorization": auth_header}
                if cookie_header:
                    connect_headers["Cookie"] = cookie_header
                client.connect(
                    self._build_url("/"),
                    transports=["websocket"],
                    namespaces=[ns_pty, ns_terminal, ns_default],
                    headers=connect_headers,
                    wait_timeout=10.0,
                )
                self._sio_client = client
                self._emit_event(EventLevel.INFO, "Socket.IO connected successfully")
            except Exception as exc:
                self._emit_event(EventLevel.WARNING, f"Socket.IO connection failed: {exc} (HTTP polling still active)")

        self._sio_thread = threading.Thread(target=_connect_sio, daemon=True, name="sio-client")
        self._sio_thread.start()

    def _stop_socketio(self) -> None:
        if self._sio_client is not None:
            try:
                self._sio_client.disconnect()
            except Exception:
                pass
            self._sio_client = None

    # --- Payload normalisation --------------------------------------------

    def _update_from_payload(self, payload: Any) -> None:
        if not isinstance(payload, Mapping):
            return
        self._update_sessions(payload)
        self._update_listeners(payload)
        self._update_operator(payload)

    def _update_sessions(self, payload: Mapping[str, Any]) -> None:
        connected = payload.get("connected_clients", []) or []
        os_data: Mapping[str, str] = payload.get("os_data", {}) or {}
        hostnames: Mapping[str, str] = payload.get("hostname", {}) or {}
        pids: Mapping[str, str] = payload.get("pid", {}) or {}
        users: Mapping[str, str] = payload.get("user", {}) or {}
        ips: Mapping[str, str] = payload.get("ips", {}) or {}
        discovered: Mapping[str, str] = payload.get("discovered_ips", {}) or {}
        history: Mapping[str, list[Mapping[str, str]]] = payload.get("commands_history", {}) or {}
        results: Mapping[str, Mapping[str, Any]] = payload.get("results", {}) or {}

        new_sessions: list[Session] = []
        for client_id in connected:
            cid = str(client_id)
            last_command = ""
            entries = history.get(cid, [])
            if entries:
                entry = entries[-1]
                if isinstance(entry, dict):
                    last_command = str(entry.get("command", ""))
                else:
                    last_command = str(entry)
            beacon_data = results.get(cid, {}) if isinstance(results, Mapping) else {}
            new_sessions.append(
                Session(
                    identifier=cid,
                    hostname=str(hostnames.get(cid, beacon_data.get("hostname", ""))),
                    operating_system=str(os_data.get(cid, beacon_data.get("client", ""))),
                    process_id=str(pids.get(cid, beacon_data.get("pid", ""))),
                    user=str(users.get(cid, beacon_data.get("user", ""))),
                    ip_addresses=str(ips.get(cid, beacon_data.get("ips", ""))),
                    discovered_ips=str(discovered.get(cid, beacon_data.get("discovered_ips", ""))),
                    last_command=last_command or str(beacon_data.get("command", "")),
                )
            )
        sessions_tuple = tuple(new_sessions)
        if sessions_tuple != self._sessions:
            self._sessions = sessions_tuple
            self.sessions_changed.emit(list(sessions_tuple))

    def _update_listeners(self, payload: Mapping[str, Any]) -> None:
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
        listeners_tuple = tuple(listeners)
        if listeners_tuple != self._listeners:
            self._listeners = listeners_tuple
            self.listeners_changed.emit(list(listeners_tuple))

    def _update_operator(self, payload: Mapping[str, Any]) -> None:
        username = payload.get("current_user_username")
        if not username:
            return
        operator = Operator(
            name=str(username),
            role="teamserver",
            is_authenticated=bool(payload.get("is_authenticated", False)),
            karma_name=str(payload.get("karma_name", "")),
            elo=int(payload.get("elo", 0) or 0),
        )
        self.operator_changed.emit(operator)

    def _parse_graph_nodes(self, payload: Any) -> list[GraphNode]:
        nodes: list[GraphNode] = []
        if not isinstance(payload, Mapping):
            return nodes
        raw_nodes = payload.get("nodes", [])
        for n in raw_nodes if isinstance(raw_nodes, list) else []:
            if not isinstance(n, Mapping):
                continue
            nid = str(n.get("id", ""))
            nlabel = str(n.get("label", nid))
            ntype = str(n.get("group", n.get("type", "host")))
            nodes.append(
                GraphNode(
                    identifier=nid,
                    label=nlabel,
                    node_type=ntype,
                    shape=str(n.get("shape", "dot")),
                    color=str(n.get("color", "#58a6ff")),
                    icon=str(n.get("image", n.get("icon", ""))),
                    metadata=n.get("metadata", {}) or {},
                )
            )
        return nodes

    def _parse_graph_edges(self, payload: Any) -> list[GraphEdge]:
        edges: list[GraphEdge] = []
        if not isinstance(payload, Mapping):
            return edges
        raw_edges = payload.get("edges", [])
        for e in raw_edges if isinstance(raw_edges, list) else []:
            if not isinstance(e, Mapping):
                continue
            edges.append(
                GraphEdge(
                    source_id=str(e.get("from", e.get("source", ""))),
                    target_id=str(e.get("to", e.get("target", ""))),
                    label=str(e.get("label", "")),
                    edge_type=str(e.get("type", "default")),
                    color=str(e.get("color", "#30363d")),
                )
            )
        return edges

    def _build_topology_from_payload(self, payload: Mapping[str, Any]) -> None:
        """Build the graph topology from ``/api/data`` fields.

        Uses the same data the web GUI's ``generateGraph()`` function reads:
        ``connected_clients`` (beacons), ``connected_hosts`` (discovered
        hosts), ``discovered_ips`` per client, ``result_portscan`` per
        client, ``os_data``, ``hostname``, ``ips``, and ``local_ips`` for
        the C2 label.
        """
        nodes: list[GraphNode] = []
        edges: list[GraphEdge] = []

        local_ips = payload.get("local_ips", []) or []
        c2_label = "C2 LazyOwn"
        if local_ips:
            c2_label = "C2 " + ", ".join(str(ip) for ip in local_ips)
        nodes.append(GraphNode(identifier="c2", label=c2_label, node_type="c2", color="#58a6ff"))

        connected_clients: list[str] = list(payload.get("connected_clients", []) or [])
        os_data: dict[str, str] = dict(payload.get("os_data", {}) or {})
        hostnames: dict[str, str] = dict(payload.get("hostname", {}) or {})
        ips_dict: dict[str, str] = dict(payload.get("ips", {}) or {})
        users: dict[str, str] = dict(payload.get("user", {}) or {})
        discovered_ips_dict: dict[str, str] = dict(payload.get("discovered_ips", {}) or {})
        portscan_dict: dict[str, str] = dict(payload.get("result_portscan", {}) or {})

        host_seen: set[str] = set()

        for client_id in connected_clients:
            cid = str(client_id)
            client_os = str(os_data.get(cid, "")).lower()
            client_hostname = str(hostnames.get(cid, cid[:8]))
            client_ips = str(ips_dict.get(cid, ""))
            client_user = str(users.get(cid, ""))
            client_discovered = str(discovered_ips_dict.get(cid, ""))
            client_ports = str(portscan_dict.get(cid, ""))

            if "windows" in client_os:
                os_label = "WIN"
                node_color = "#58a6ff"
            elif "linux" in client_os:
                os_label = "LNX"
                node_color = "#3fb950"
            else:
                os_label = "UNK"
                node_color = "#f85149"

            label_parts = [f"[{os_label}]"]
            if client_hostname:
                label_parts.append(client_hostname)
            else:
                label_parts.append(cid[:8])
            if client_user:
                label_parts.append(f"@{client_user}")

            nodes.append(GraphNode(
                identifier=cid,
                label=" ".join(label_parts),
                node_type="beacon",
                color=node_color,
                metadata={"os": client_os, "hostname": client_hostname, "ips": client_ips, "user": client_user},
            ))
            edges.append(GraphEdge(source_id="c2", target_id=cid, label="HTTPS", edge_type="c2"))

            for dip in client_discovered.split(","):
                dip = dip.strip()
                if not dip:
                    continue
                host_id = f"host-{dip.replace('.', '-')}"
                if host_id not in host_seen:
                    host_seen.add(host_id)
                    nodes.append(GraphNode(identifier=host_id, label=dip, node_type="host", color="#d2991d"))
                edges.append(GraphEdge(source_id=cid, target_id=host_id, label="discovered", edge_type="host", color="#d2991d"))

            port_to_host: dict[str, list[str]] = {}
            for port_str in client_ports.split(","):
                port_str = port_str.strip()
                if not port_str:
                    continue
                for dip in client_discovered.split(","):
                    dip = dip.strip()
                    if not dip:
                        continue
                    host_id = f"host-{dip.replace('.', '-')}"
                    port_to_host.setdefault(host_id, []).append(port_str)

            for host_id, ports in port_to_host.items():
                for port in ports:
                    port_id = f"port-{host_id}-{port}"
                    nodes.append(GraphNode(identifier=port_id, label=port, node_type="port", color="#8b949e"))
                    edges.append(GraphEdge(source_id=host_id, target_id=port_id, label=port, edge_type="port", color="#8b949e"))

        connected_hosts: list[str] = list(payload.get("connected_hosts", []) or [])
        for host_ip in connected_hosts:
            host_ip = str(host_ip).strip()
            if not host_ip:
                continue
            host_id = f"host-{host_ip.replace('.', '-')}"
            if host_id not in host_seen:
                host_seen.add(host_id)
                nodes.append(GraphNode(identifier=host_id, label=host_ip, node_type="host", color="#d2991d"))
                edges.append(GraphEdge(source_id="c2", target_id=host_id, label="known", edge_type="host", color="#484f58"))

        new_topology = Topology(nodes=tuple(nodes), edges=tuple(edges))
        if new_topology != self._topology:
            self._topology = new_topology
            self.topology_changed.emit(new_topology)

    def _emit_event(self, level: EventLevel, message: str) -> None:
        record = EventRecord.now(level=level, source="teamserver", message=message)
        self.event_logged.emit(record)
        if level in (EventLevel.ERROR, EventLevel.CRITICAL):
            _logger.error(message)
        elif level is EventLevel.WARNING:
            _logger.warning(message)
        else:
            _logger.debug(message)
