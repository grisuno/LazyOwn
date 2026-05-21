"""Multi-listener manager for LazyOwn C2.

Allows the C2 to listen on multiple ports simultaneously, each serving the
same Flask application.  Beacons/implants can connect to any listener and
share the same global state (commands, results, connected_clients).

Persistence: ``sessions/listeners.json`` stores the listener configuration.

Bind address: never hardcoded. The address comes from ``payload.json``
via ``c2_bind_address`` or ``lhost``. Wildcard literals (``""``,
``"0.0.0.0"``, ``"::"``) are rejected at the bind site; if the operator
wants to expose the listener on a network interface they must put that
interface's specific IP in ``payload.json``.
"""

from __future__ import annotations

import errno
import ipaddress
import json
import os
import socket
import ssl as _ssl
import threading
import time
from dataclasses import dataclass, field
from typing import Any

from utils import print_error, print_msg, print_warn


_LOOPBACK_BIND_ADDRESS = "127.0.0.1"
_WILDCARD_BIND_LITERALS = frozenset({"", "0.0.0.0", "::"})
_BIND_PROBE_TIMEOUT_SECONDS = 0.5


def _collect_listener_bind_candidates(payload: dict[str, Any] | None) -> list[str]:
    """Return the ordered list of specific IP candidates from payload.json.

    The list contains operator-controlled candidates first
    (``c2_bind_address`` then ``lhost``) and always ends with the
    loopback fallback. Wildcard literals are filtered out because the
    framework must never bind to every interface implicitly.

    Args:
        payload: Parsed ``payload.json`` mapping or ``None``.

    Returns:
        A deduplicated list of bindable IPv4/IPv6 literal candidates.
    """
    candidates: list[str] = []
    seen: set[str] = set()
    if isinstance(payload, dict):
        for key in ("c2_bind_address", "lhost"):
            raw = payload.get(key)
            if not isinstance(raw, str):
                continue
            stripped = raw.strip()
            if stripped == "" or stripped == "0.0.0.0" or stripped == "::":
                continue
            try:
                ipaddress.ip_address(stripped)
            except ValueError:
                continue
            if stripped in seen:
                continue
            candidates.append(stripped)
            seen.add(stripped)
    if _LOOPBACK_BIND_ADDRESS not in seen:
        candidates.append(_LOOPBACK_BIND_ADDRESS)
    return candidates


def _probe_listener_bind(address: str, port: int) -> tuple[bool, int | None]:
    """Probe whether ``(address, port)`` can be bound for TCP.

    Wildcard literals are rejected inline so the helper doubles as a
    sanitiser. The probe uses ``SO_REUSEADDR`` and an ephemeral
    timeout to avoid spurious ``EADDRINUSE`` after a recent close.

    Args:
        address: IPv4/IPv6 literal candidate.
        port: Port number to test.

    Returns:
        ``(True, None)`` when the bind succeeds; otherwise
        ``(False, errno_value)``.
    """
    if not isinstance(address, str):
        return False, errno.EINVAL
    safe_address = address.strip()
    if safe_address == "" or safe_address == "0.0.0.0" or safe_address == "::":
        return False, errno.EACCES
    family = socket.AF_INET6 if ":" in safe_address else socket.AF_INET
    probe = None
    try:
        probe = socket.socket(family, socket.SOCK_STREAM)
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        probe.settimeout(_BIND_PROBE_TIMEOUT_SECONDS)
        probe.bind((safe_address, port))
        return True, None
    except OSError as exc:
        return False, exc.errno
    finally:
        if probe is not None:
            try:
                probe.close()
            except OSError:
                pass


def _resolve_listener_bind_address(payload: dict[str, Any] | None, port: int | None = None) -> str:
    """Return the specific IP literal listeners must bind to.

    Candidates are taken exclusively from ``payload.json``
    (``c2_bind_address`` then ``lhost``) with loopback as the final
    fallback. When ``port`` is supplied each candidate is probed and
    the first bindable address wins, so a stale VPN IP does not
    prevent the C2 from starting; the loopback fallback is always
    bindable.

    Args:
        payload: Parsed ``payload.json`` mapping or ``None``.
        port: Optional port for the bind probe. When omitted the
            first valid candidate is returned without probing.

    Returns:
        A specific IPv4/IPv6 literal safe to pass to ``make_server``.
    """
    candidates = _collect_listener_bind_candidates(payload)
    if not candidates:
        return _LOOPBACK_BIND_ADDRESS
    if port is None:
        return candidates[0]
    for candidate in candidates:
        bindable, _ = _probe_listener_bind(candidate, int(port))
        if bindable:
            return candidate
    return _LOOPBACK_BIND_ADDRESS


@dataclass
class Listener:
    """A single C2 listener endpoint."""

    id: str
    port: int
    ssl: bool = False
    active: bool = True
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))
    _server: Any = field(default=None, repr=False)
    _thread: threading.Thread | None = field(default=None, repr=False)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "port": self.port,
            "ssl": self.ssl,
            "active": self.active,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Listener":
        return cls(
            id=data["id"],
            port=data["port"],
            ssl=data.get("ssl", False),
            active=data.get("active", True),
            created_at=data.get("created_at", time.strftime("%Y-%m-%dT%H:%M:%S")),
        )


class ListenerManager:
    """Manage multiple C2 listener ports.

    ``app`` may be ``None`` when used from the CLI for config-only operations
    (add, remove, list).  Start/stop require a live Flask application instance.
    """

    def __init__(self, app: Any = None, sessions_dir: str = "sessions", payload: dict[str, Any] | None = None):
        self.app = app
        self.sessions_dir = sessions_dir
        self.listeners: dict[str, Listener] = {}
        self._lock = threading.Lock()
        self._payload = payload if isinstance(payload, dict) else None
        self._load()

    def set_payload(self, payload: dict[str, Any] | None) -> None:
        """Update the payload mapping used to resolve the bind address."""
        self._payload = payload if isinstance(payload, dict) else None

    def _bind_address(self, port: int | None = None) -> str:
        """Return the specific bind address derived from payload.json.

        When ``port`` is supplied the candidates are probed and the
        first bindable one is returned, so a payload-configured IP
        belonging to a downed interface does not stop the listener
        from starting on the loopback fallback.
        """
        return _resolve_listener_bind_address(self._payload, port=port)

    def _listeners_path(self) -> str:
        return os.path.join(self.sessions_dir, "listeners.json")

    def _load(self) -> None:
        path = self._listeners_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            for item in data.get("listeners", []):
                listener = Listener.from_dict(item)
                self.listeners[listener.id] = listener
        except Exception as e:
            print_warn(f"[listener] Failed to load listeners.json: {e}")

    def _save(self) -> None:
        path = self._listeners_path()
        try:
            os.makedirs(self.sessions_dir, exist_ok=True)
            data = {
                "listeners": [lst.to_dict() for lst in self.listeners.values()],
            }
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print_warn(f"[listener] Failed to save listeners.json: {e}")

    def add(self, port: int, ssl: bool = False, listener_id: str | None = None) -> Listener:
        """Register a new listener configuration (does not start it)."""
        if listener_id is None:
            listener_id = f"listener-{port}"
        with self._lock:
            if listener_id in self.listeners:
                print_warn(f"[listener] {listener_id} already exists, overwriting.")
            listener = Listener(id=listener_id, port=port, ssl=ssl)
            self.listeners[listener_id] = listener
            self._save()
        print_msg(f"[listener] Registered {listener_id} on port {port} (ssl={ssl})")
        return listener

    def remove(self, listener_id: str) -> bool:
        """Remove a listener configuration."""
        with self._lock:
            listener = self.listeners.pop(listener_id, None)
            if listener is None:
                print_error(f"[listener] {listener_id} not found.")
                return False
            if listener._server is not None:
                self._stop(listener)
            self._save()
        print_msg(f"[listener] Removed {listener_id}")
        return True

    def start(self, listener_id: str) -> bool:
        """Start a single listener.

        Requires a live Flask ``app`` instance.  Returns ``False`` immediately
        when called without one (CLI config-only mode).
        """
        if self.app is None:
            print_warn("[listener] No Flask app — start via the C2 API or restart lazyc2.")
            return False
        listener = self.listeners.get(listener_id)
        if listener is None:
            print_error(f"[listener] {listener_id} not found.")
            return False
        if listener._server is not None:
            print_warn(f"[listener] {listener_id} is already running.")
            return True

        try:
            ssl_context = None
            if listener.ssl:
                cert_path = "cert.pem"
                key_path = "key.pem"
                if os.path.exists(cert_path) and os.path.exists(key_path):
                    ssl_context = (cert_path, key_path)
                else:
                    print_warn(
                        f"[listener] SSL requested but cert.pem/key.pem not found. "
                        f"Starting {listener_id} without SSL."
                    )

            from werkzeug.serving import make_server

            bind_address = self._bind_address(port=listener.port)
            if bind_address in _WILDCARD_BIND_LITERALS:
                print_error(
                    f"[listener] {listener_id} refused wildcard bind address; "
                    f"set c2_bind_address or lhost in payload.json"
                )
                return False

            if bind_address == _LOOPBACK_BIND_ADDRESS:
                configured = _collect_listener_bind_candidates(self._payload)
                if configured != [_LOOPBACK_BIND_ADDRESS]:
                    print_warn(
                        f"[listener] {listener_id} falling back to {_LOOPBACK_BIND_ADDRESS}: "
                        f"configured addresses {configured!r} were not bindable on this host"
                    )

            server = make_server(
                bind_address,
                listener.port,
                self.app,
                threaded=True,
                ssl_context=ssl_context,
            )
            listener._server = server
            thread = threading.Thread(
                target=server.serve_forever,
                daemon=True,
                name=f"listener-{listener.port}",
            )
            listener._thread = thread
            thread.start()
            print_msg(
                f"[listener] {listener_id} started on {bind_address}:{listener.port} "
                f"(ssl={listener.ssl})"
            )
            return True
        except Exception as e:
            print_error(f"[listener] Failed to start {listener_id}: {e}")
            return False

    def stop(self, listener_id: str) -> bool:
        """Stop a single listener."""
        listener = self.listeners.get(listener_id)
        if listener is None:
            print_error(f"[listener] {listener_id} not found.")
            return False
        return self._stop(listener)

    def _stop(self, listener: Listener) -> bool:
        if listener._server is None:
            return True
        try:
            listener._server.shutdown()
            listener._server = None
            listener._thread = None
            print_msg(f"[listener] {listener.id} stopped.")
            return True
        except Exception as e:
            print_error(f"[listener] Failed to stop {listener.id}: {e}")
            return False

    def start_all(self) -> None:
        """Start every listener marked as active."""
        for listener_id, listener in self.listeners.items():
            if listener.active:
                self.start(listener_id)

    def stop_all(self) -> None:
        """Stop every running listener."""
        for listener_id, listener in list(self.listeners.items()):
            self.stop(listener_id)

    def status(self) -> list[dict[str, Any]]:
        """Return status of all listeners."""
        result = []
        for listener in self.listeners.values():
            result.append({
                **listener.to_dict(),
                "running": listener._server is not None,
            })
        return result

    def get_default_port(self, fallback: int = 4444) -> int:
        """Return the port of the first active listener, or fallback."""
        for listener in self.listeners.values():
            if listener.active:
                return listener.port
        return fallback
