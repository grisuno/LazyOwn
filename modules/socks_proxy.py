"""SOCKS5 proxy engine for tunneling traffic through LazyOwn beacons.

Provides a configuration-driven SOCKS5 proxy that allows operators to
route external tools through a compromised beacon's network. Supports
authentication, activity logging, connection limits, and bandwidth
throttling.

The engine is designed as a specification-only module: it defines the
protocol, configuration, and validation contracts without coupling to
any specific transport implementation. Concrete transport adapters
(e.g., WebSocket, HTTP long-poll) inject their own I/O layer.

Contracts:
    - SocksProxyConfig: immutable configuration for a SOCKS proxy instance
    - SocksAuthMethod: enumeration of supported authentication methods
    - SocksCommand: SOCKS5 command types (CONNECT, BIND, UDP)
    - SocksProxyEngine: validates config, builds proxy specs, tracks sessions
    - SocksSession: represents an active proxied connection
    - SocksValidator: validates config, client requests, and protocol states

Design (SOLID):
    - Single Responsibility: config, session, engine, validator are separate
    - Open/Closed: new auth methods added via enum without modifying engine
    - Liskov: session and config are safely substitutable dataclasses
    - Interface Segregation: engine exposes only spec/validation, not I/O
    - Dependency Inversion: depends on abstract config dict, not on sockets

Usage:
    from modules.socks_proxy import SocksProxyEngine

    engine = SocksProxyEngine(
        SocksProxyConfig(
            bind_address="127.0.0.1",
            bind_port=1080,
            auth_methods=[SocksAuthMethod.NO_AUTH],
        )
    )
    spec = engine.build_spec()
    errors = engine.validate()
"""

from __future__ import annotations

import ipaddress
import logging
import socket
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

log = logging.getLogger("socks_proxy")

SOCKS_VERSION = 0x05
SOCKS_RESERVED = 0x00
SOCKS_MAX_ADDR_LEN = 255
SOCKS_MIN_PORT = 1
SOCKS_MAX_PORT = 65535
SOCKS_DEFAULT_BIND_PORT = 1080
SOCKS_DEFAULT_BIND_ADDRESS = "127.0.0.1"
SOCKS_DEFAULT_MAX_CONNECTIONS = 32
SOCKS_DEFAULT_SESSION_TIMEOUT_S = 300
SOCKS_DEFAULT_BANDWIDTH_LIMIT_BPS = 0


class SocksAuthMethod(IntEnum):
    """SOCKS5 authentication methods per RFC 1928."""

    NO_AUTH = 0x00
    GSSAPI = 0x01
    USERNAME_PASSWORD = 0x02
    NO_ACCEPTABLE = 0xFF


class SocksCommand(IntEnum):
    """SOCKS5 command types per RFC 1928."""

    CONNECT = 0x01
    BIND = 0x02
    UDP_ASSOCIATE = 0x03


class SocksAddressType(IntEnum):
    """SOCKS5 address types per RFC 1928."""

    IPV4 = 0x01
    DOMAIN = 0x03
    IPV6 = 0x04


class SocksReply(IntEnum):
    """SOCKS5 reply codes per RFC 1928."""

    SUCCEEDED = 0x00
    GENERAL_FAILURE = 0x01
    CONNECTION_NOT_ALLOWED = 0x02
    NETWORK_UNREACHABLE = 0x03
    HOST_UNREACHABLE = 0x04
    CONNECTION_REFUSED = 0x05
    TTL_EXPIRED = 0x06
    COMMAND_NOT_SUPPORTED = 0x07
    ADDRESS_TYPE_NOT_SUPPORTED = 0x08

    def message(self) -> str:
        """Return a human-readable message for this reply code."""
        messages = {
            0x00: "request granted",
            0x01: "general SOCKS server failure",
            0x02: "connection not allowed by ruleset",
            0x03: "network unreachable",
            0x04: "host unreachable",
            0x05: "connection refused",
            0x06: "TTL expired",
            0x07: "command not supported",
            0x08: "address type not supported",
        }
        return messages.get(self.value, f"unknown reply code {self.value}")


@dataclass
class SocksSession:
    """Represents a single active proxied connection.

    Attributes:
        session_id: Unique identifier for this session.
        target_host: Destination hostname or IP address.
        target_port: Destination TCP port.
        beacon_client_id: Client ID of the beacon handling this session.
        bytes_sent: Total bytes sent to target.
        bytes_received: Total bytes received from target.
        created_at: Unix timestamp of session creation.
        last_activity: Unix timestamp of last data transfer.
    """

    session_id: str
    target_host: str
    target_port: int
    beacon_client_id: str
    bytes_sent: int = 0
    bytes_received: int = 0
    created_at: float = 0.0
    last_activity: float = 0.0

    @property
    def elapsed_seconds(self) -> float:
        """Return seconds since session creation."""
        import time
        return time.monotonic() - self.created_at if self.created_at > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize session to dictionary."""
        return {
            "session_id": self.session_id,
            "target_host": self.target_host,
            "target_port": self.target_port,
            "beacon_client_id": self.beacon_client_id,
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "created_at": self.created_at,
            "last_activity": self.last_activity,
            "elapsed_seconds": self.elapsed_seconds,
        }


@dataclass
class SocksProxyConfig:
    """Configuration for a SOCKS5 proxy instance.

    Attributes:
        bind_address: IP address to bind the proxy listener.
        bind_port: TCP port to bind.
        auth_methods: Ordered list of supported authentication methods.
        username: Username for USERNAME_PASSWORD auth.
        password: Password for USERNAME_PASSWORD auth.
        max_connections: Maximum concurrent proxied connections.
        session_timeout_seconds: Idle session timeout in seconds.
        bandwidth_limit_bps: Maximum bandwidth in bytes per second (0 = unlimited).
        allow_localhost: Allow connections to loopback addresses.
        allow_private_ranges: Allow connections to RFC 1918 addresses.
        allowed_ports: List of allowed destination ports (empty = all allowed).
        denied_ports: List of denied destination ports.
        log_connections: Enable connection logging.
    """

    bind_address: str = SOCKS_DEFAULT_BIND_ADDRESS
    bind_port: int = SOCKS_DEFAULT_BIND_PORT
    auth_methods: list[SocksAuthMethod] = field(
        default_factory=lambda: [SocksAuthMethod.NO_AUTH]
    )
    username: str = ""
    password: str = ""
    max_connections: int = SOCKS_DEFAULT_MAX_CONNECTIONS
    session_timeout_seconds: int = SOCKS_DEFAULT_SESSION_TIMEOUT_S
    bandwidth_limit_bps: int = SOCKS_DEFAULT_BANDWIDTH_LIMIT_BPS
    allow_localhost: bool = False
    allow_private_ranges: bool = True
    allowed_ports: list[int] = field(default_factory=list)
    denied_ports: list[int] = field(default_factory=lambda: [22, 3389])
    log_connections: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize config to dictionary."""
        return {
            "bind_address": self.bind_address,
            "bind_port": self.bind_port,
            "auth_methods": [m.name for m in self.auth_methods],
            "username": self.username,
            "password": self.password,
            "max_connections": self.max_connections,
            "session_timeout_seconds": self.session_timeout_seconds,
            "bandwidth_limit_bps": self.bandwidth_limit_bps,
            "allow_localhost": self.allow_localhost,
            "allow_private_ranges": self.allow_private_ranges,
            "allowed_ports": self.allowed_ports,
            "denied_ports": self.denied_ports,
            "log_connections": self.log_connections,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> SocksProxyConfig:
        """Build config from dictionary."""
        auth_methods_raw = raw.get("auth_methods", ["NO_AUTH"])
        auth_methods = []
        for name in auth_methods_raw:
            try:
                auth_methods.append(SocksAuthMethod[name])
            except KeyError:
                log.warning("Unknown SOCKS auth method: %s", name)
        return cls(
            bind_address=str(raw.get("bind_address", SOCKS_DEFAULT_BIND_ADDRESS)),
            bind_port=int(raw.get("bind_port", SOCKS_DEFAULT_BIND_PORT)),
            auth_methods=auth_methods or [SocksAuthMethod.NO_AUTH],
            username=str(raw.get("username", "")),
            password=str(raw.get("password", "")),
            max_connections=int(raw.get("max_connections", SOCKS_DEFAULT_MAX_CONNECTIONS)),
            session_timeout_seconds=int(raw.get("session_timeout_seconds", SOCKS_DEFAULT_SESSION_TIMEOUT_S)),
            bandwidth_limit_bps=int(raw.get("bandwidth_limit_bps", SOCKS_DEFAULT_BANDWIDTH_LIMIT_BPS)),
            allow_localhost=bool(raw.get("allow_localhost", False)),
            allow_private_ranges=bool(raw.get("allow_private_ranges", True)),
            allowed_ports=list(raw.get("allowed_ports", [])),
            denied_ports=list(raw.get("denied_ports", [22, 3389])),
            log_connections=bool(raw.get("log_connections", True)),
        )


class SocksValidator:
    """Validates SOCKS5 proxy configuration and request parameters.

    Ensures bind addresses are valid IPs, ports are in range,
    authentication settings are consistent, and access control
    rules are well-formed.
    """

    @staticmethod
    def validate_config(config: SocksProxyConfig) -> list[str]:
        """Validate a SocksProxyConfig and return error messages.

        Returns an empty list if the config is valid.
        """
        errors: list[str] = []

        try:
            ipaddress.ip_address(config.bind_address)
        except ValueError:
            errors.append(
                f"bind_address '{config.bind_address}' is not a valid IP address"
            )

        if not (SOCKS_MIN_PORT <= config.bind_port <= SOCKS_MAX_PORT):
            errors.append(
                f"bind_port {config.bind_port} is outside valid range "
                f"({SOCKS_MIN_PORT}-{SOCKS_MAX_PORT})"
            )

        if config.max_connections < 1:
            errors.append("max_connections must be >= 1")
        if config.max_connections > 65535:
            errors.append("max_connections must be <= 65535")

        if config.session_timeout_seconds < 5:
            errors.append("session_timeout_seconds must be >= 5")
        if config.session_timeout_seconds > 86400:
            errors.append("session_timeout_seconds must be <= 86400 (24 hours)")

        if config.bandwidth_limit_bps < 0:
            errors.append("bandwidth_limit_bps must be >= 0")

        has_userpass = SocksAuthMethod.USERNAME_PASSWORD in config.auth_methods
        if has_userpass and (not config.username or not config.password):
            errors.append(
                "username and password are required when USERNAME_PASSWORD "
                "authentication is enabled"
            )

        if not config.auth_methods:
            errors.append("at least one auth_method is required")

        for port in config.allowed_ports:
            if not (SOCKS_MIN_PORT <= port <= SOCKS_MAX_PORT):
                errors.append(f"allowed_ports contains invalid port: {port}")
        for port in config.denied_ports:
            if not (SOCKS_MIN_PORT <= port <= SOCKS_MAX_PORT):
                errors.append(f"denied_ports contains invalid port: {port}")
            if port in config.allowed_ports:
                errors.append(
                    f"port {port} appears in both allowed_ports and denied_ports"
                )

        return errors

    @staticmethod
    def validate_request(
        command: int,
        address_type: int,
        host: str,
        port: int,
        config: SocksProxyConfig | None = None,
    ) -> tuple[bool, int, str]:
        """Validate a SOCKS5 request against the proxy configuration.

        Args:
            command: SOCKS command byte (CONNECT, BIND, UDP_ASSOCIATE).
            address_type: Address type byte (IPV4, DOMAIN, IPV6).
            host: Target hostname or IP address.
            port: Target port.
            config: Optional proxy config for access control checks.

        Returns:
            Tuple of (is_valid, reply_code, message).
        """
        if command not in (SocksCommand.CONNECT, SocksCommand.BIND, SocksCommand.UDP_ASSOCIATE):
            return False, SocksReply.COMMAND_NOT_SUPPORTED, "command not supported"

        if address_type not in (SocksAddressType.IPV4, SocksAddressType.DOMAIN, SocksAddressType.IPV6):
            return False, SocksReply.ADDRESS_TYPE_NOT_SUPPORTED, "address type not supported"

        if not host:
            return False, SocksReply.GENERAL_FAILURE, "host is required"

        if len(host) > SOCKS_MAX_ADDR_LEN:
            return False, SocksReply.GENERAL_FAILURE, f"host exceeds {SOCKS_MAX_ADDR_LEN} characters"

        if not (SOCKS_MIN_PORT <= port <= SOCKS_MAX_PORT):
            return False, SocksReply.GENERAL_FAILURE, f"port {port} is invalid"

        if config is not None:
            return SocksValidator._check_access_control(host, port, config)

        return True, SocksReply.SUCCEEDED, "request valid"

    @staticmethod
    def _check_access_control(
        host: str,
        port: int,
        config: SocksProxyConfig,
    ) -> tuple[bool, int, str]:
        """Apply access control rules from proxy config."""
        if config.denied_ports and port in config.denied_ports:
            return False, SocksReply.CONNECTION_NOT_ALLOWED, f"port {port} is denied"
        if config.allowed_ports and port not in config.allowed_ports:
            return False, SocksReply.CONNECTION_NOT_ALLOWED, f"port {port} is not in allowed list"

        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            try:
                ip = socket.getaddrinfo(host, None)[0][4][0]
                ip = ipaddress.ip_address(ip)
            except (socket.gaierror, OSError, IndexError):
                return True, SocksReply.SUCCEEDED, "hostname resolution deferred"

        if ip.is_loopback and not config.allow_localhost:
            return False, SocksReply.CONNECTION_NOT_ALLOWED, "localhost connections not allowed"
        if ip.is_private and not config.allow_private_ranges:
            return False, SocksReply.CONNECTION_NOT_ALLOWED, "private range connections not allowed"

        return True, SocksReply.SUCCEEDED, "access granted"


class SocksProxyEngine:
    """SOCKS5 proxy specification engine.

    Provides configuration, validation, and session management
    for a SOCKS5 proxy tunneled through a LazyOwn beacon. Does
    not handle I/O; concrete adapters inject their transport.

    Attributes:
        config: The SOCKS proxy configuration.
        validator: The configuration and request validator.
        sessions: Active proxied sessions keyed by session_id.
    """

    def __init__(self, config: SocksProxyConfig | None = None) -> None:
        self._config = config or SocksProxyConfig()
        self._validator = SocksValidator()
        self._sessions: dict[str, SocksSession] = {}

    @property
    def config(self) -> SocksProxyConfig:
        """Return the current proxy configuration."""
        return self._config

    @property
    def sessions(self) -> dict[str, SocksSession]:
        """Return active proxied sessions."""
        return dict(self._sessions)

    @property
    def session_count(self) -> int:
        """Return the number of active sessions."""
        return len(self._sessions)

    def validate(self, config: SocksProxyConfig | None = None) -> list[str]:
        """Validate the configuration.

        Args:
            config: Optional config to validate. Uses self.config if None.

        Returns:
            List of error strings (empty = valid).
        """
        cfg = config or self._config
        return self._validator.validate_config(cfg)

    def build_spec(self) -> dict[str, Any]:
        """Build a JSON-serializable proxy specification for beacon delivery.

        The spec contains everything a beacon needs to set up a
        SOCKS5 proxy listener and relay traffic through its C2.
        """
        return {
            "version": SOCKS_VERSION,
            "bind_address": self._config.bind_address,
            "bind_port": self._config.bind_port,
            "auth_methods": [int(m) for m in self._config.auth_methods],
            "username": self._config.username,
            "password": self._config.password,
            "max_connections": self._config.max_connections,
            "session_timeout_seconds": self._config.session_timeout_seconds,
            "bandwidth_limit_bps": self._config.bandwidth_limit_bps,
            "allow_localhost": self._config.allow_localhost,
            "allow_private_ranges": self._config.allow_private_ranges,
            "allowed_ports": self._config.allowed_ports,
            "denied_ports": self._config.denied_ports,
            "log_connections": self._config.log_connections,
        }

    def create_session(
        self,
        session_id: str,
        target_host: str,
        target_port: int,
        beacon_client_id: str,
    ) -> SocksSession | None:
        """Create and track a new proxied session.

        Returns None if max_connections is reached.
        """
        if len(self._sessions) >= self._config.max_connections:
            oldest = self._find_oldest_session()
            if oldest:
                self.remove_session(oldest)
            else:
                return None
        import time
        now = time.monotonic()
        session = SocksSession(
            session_id=session_id,
            target_host=target_host,
            target_port=target_port,
            beacon_client_id=beacon_client_id,
            created_at=now,
            last_activity=now,
        )
        self._sessions[session_id] = session
        if self._config.log_connections:
            log.info(
                "SOCKS session %s -> %s:%d via %s",
                session_id, target_host, target_port, beacon_client_id,
            )
        return session

    def remove_session(self, session_id: str) -> bool:
        """Remove a session by ID. Returns True if it existed."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def get_session(self, session_id: str) -> SocksSession | None:
        """Return a session by ID, or None."""
        return self._sessions.get(session_id)

    def add_bytes(self, session_id: str, sent: int = 0, received: int = 0) -> None:
        """Update byte counters for a session."""
        session = self._sessions.get(session_id)
        if session is None:
            return
        import time
        session.bytes_sent += sent
        session.bytes_received += received
        session.last_activity = time.monotonic()

    def cleanup_expired(self) -> int:
        """Remove sessions that have exceeded the timeout. Returns count removed."""
        import time
        now = time.monotonic()
        expired_ids = [
            sid for sid, s in self._sessions.items()
            if (now - s.last_activity) > self._config.session_timeout_seconds
        ]
        for sid in expired_ids:
            del self._sessions[sid]
        if expired_ids and self._config.log_connections:
            log.info("SOCKS cleaned up %d expired sessions", len(expired_ids))
        return len(expired_ids)

    def list_sessions(self) -> list[dict[str, Any]]:
        """Return a list of all active sessions as dictionaries."""
        return [s.to_dict() for s in self._sessions.values()]

    def _find_oldest_session(self) -> str | None:
        """Return the session_id of the least recently active session."""
        if not self._sessions:
            return None
        return min(self._sessions, key=lambda k: self._sessions[k].last_activity)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> SocksProxyEngine:
        """Build a SocksProxyEngine from a configuration dictionary."""
        config = SocksProxyConfig.from_dict(raw)
        return cls(config=config)

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> SocksProxyEngine:
        """Build a SocksProxyEngine from a LazyOwn payload configuration."""
        socks_raw = payload.get("socks_proxy", {})
        return cls.from_dict(socks_raw)


__all__ = [
    "SocksProxyEngine",
    "SocksProxyConfig",
    "SocksSession",
    "SocksValidator",
    "SocksAuthMethod",
    "SocksCommand",
    "SocksAddressType",
    "SocksReply",
    "SOCKS_VERSION",
]
