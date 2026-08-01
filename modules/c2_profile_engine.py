"""Extended malleable C2 profile engine with TLS, DNS, SMB, and WebSocket transports.

Complements ``modules/c2_profile.py`` by adding transport-layer profile types and
profile rotation. The base module handles HTTP profiles; this module extends to
the full transport stack required by modern C2 frameworks.

Contracts:
    - C2TransportProfile: base dataclass for transport profiles
    - TlsProfile: TLS 1.2/1.3 cipher suites, JA3/JA4 fingerprinting config
    - DnsProfile: DNS beacon configuration (A/AAAA/TXT, encoding, jitter)
    - SmbProfile: SMB peer-to-peer named pipe beacon config
    - WebSocketProfile: WebSocket transport with compression and masking
    - ProfileRotator: round-robin profile rotation with cooldown windows
    - ProfileEngine: composition root combining HTTP profiles from c2_profile.py
      with transport profiles defined here

Design (SOLID):
    - Single Responsibility: each class handles one transport concern
    - Open/Closed: new transports registered via dataclass without modifying engine
    - Liskov: all transport profiles are safely substitutable dataclasses
    - Interface Segregation: each profile exposes only its own config surface
    - Dependency Inversion: engine depends on abstract profile dicts, not on Flask

Usage:
    from modules.c2_profile_engine import (
        ProfileEngine,
        TlsProfile,
        DnsProfile,
        SmbProfile,
        WebSocketProfile,
    )

    engine = ProfileEngine.from_payload(payload)
    tls_profile = engine.tls_profile
    dns_profile = engine.dns_profile
    engine.rotate()  # advance to next profile in rotation queue
"""

from __future__ import annotations

import hashlib
import logging
import random
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from core.config import Config

log = logging.getLogger("c2_profile_engine")

TLS_VERSION_MIN = "1.2"
TLS_VERSION_MAX = "1.3"
DNS_QUERY_TYPES = ("A", "AAAA", "TXT", "MX", "CNAME")
DNS_ENCODINGS = ("base32", "base64", "hex", "raw")
SMB_DEFAULT_PIPE_PREFIX = "\\\\"
SMB_NAMED_PIPE_MAX_LENGTH = 256
WEBSOCKET_PROTOCOLS = ("ws", "wss")
DEFAULT_ROTATION_COOLDOWN_S = 600

JA3_GREASE_CANDIDATES = [
    0x0A0A, 0x1A1A, 0x2A2A, 0x3A3A, 0x4A4A, 0x5A5A,
    0x6A6A, 0x7A7A, 0x8A8A, 0x9A9A, 0xAAAA, 0xBABA,
    0xCACA, 0xDADA, 0xEAEA, 0xFAFA,
]

LIBRARY_CIPHER_SUITES = {
    "chrome_120": [
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
    ],
    "firefox_120": [
        "TLS_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_256_GCM_SHA384",
    ],
    "safari_17": [
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
    ],
    "edge_120": [
        "TLS_AES_256_GCM_SHA384",
        "TLS_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256",
    ],
    "generic_tls": [
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    ],
}


@dataclass
class TlsProfile:
    """TLS transport configuration for HTTPS and WSS C2 channels.

    Attributes:
        enabled: Whether TLS is active for this transport.
        min_version: Minimum TLS version string ('1.2' or '1.3').
        max_version: Maximum TLS version string.
        cipher_suites: Ordered list of cipher suite names.
        sni_hostname: Server Name Indication value (domain fronting).
        certificate_path: Path to custom TLS certificate PEM file.
        key_path: Path to custom TLS private key PEM file.
        ja3_fingerprint_library: Browser library to emulate for JA3.
        grease_extensions: Whether to include GREASE TLS extensions.
        alpn_protocols: Application-Layer Protocol Negotiation values.
    """

    enabled: bool = True
    min_version: str = TLS_VERSION_MIN
    max_version: str = TLS_VERSION_MAX
    cipher_suites: list[str] = field(default_factory=list)
    sni_hostname: str = ""
    certificate_path: str = ""
    key_path: str = ""
    ja3_fingerprint_library: str = "chrome_120"
    grease_extensions: bool = True
    alpn_protocols: list[str] = field(default_factory=lambda: ["h2", "http/1.1"])

    def get_cipher_suites(self) -> list[str]:
        """Return cipher suites, resolving library alias if set."""
        if self.cipher_suites:
            return list(self.cipher_suites)
        return list(
            LIBRARY_CIPHER_SUITES.get(
                self.ja3_fingerprint_library,
                LIBRARY_CIPHER_SUITES["generic_tls"],
            )
        )

    def get_ja3_hash(self) -> str:
        """Compute a JA3 fingerprint hash from the current profile.

        Returns an MD5 hex digest simulating what a JA3 fingerprint
        would look like for this profile's TLS client hello.
        """
        version = "771" if self.min_version == "1.2" else "772"
        ciphers = ",".join(sorted(self.get_cipher_suites()))
        extensions = "0-5-10-11-13-16-23-43-45-51"
        if self.grease_extensions:
            grease_id = random.choice(JA3_GREASE_CANDIDATES)
            extensions += f"-{grease_id}"
        ec_curves = "29-23-24-25"
        ec_formats = "0"
        ja3_raw = f"{version},{ciphers},{extensions},{ec_curves},{ec_formats}"
        return hashlib.md5(ja3_raw.encode()).hexdigest()

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> TlsProfile:
        """Build a TlsProfile from a configuration dictionary."""
        return TlsProfile(
            enabled=bool(raw.get("enabled", True)),
            min_version=str(raw.get("min_version", TLS_VERSION_MIN)),
            max_version=str(raw.get("max_version", TLS_VERSION_MAX)),
            cipher_suites=list(raw.get("cipher_suites", [])),
            sni_hostname=str(raw.get("sni_hostname", "")),
            certificate_path=str(raw.get("certificate_path", "")),
            key_path=str(raw.get("key_path", "")),
            ja3_fingerprint_library=str(
                raw.get("ja3_fingerprint_library", "chrome_120")
            ),
            grease_extensions=bool(raw.get("grease_extensions", True)),
            alpn_protocols=list(raw.get("alpn_protocols", ["h2", "http/1.1"])),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize this profile to a plain dictionary."""
        return {
            "enabled": self.enabled,
            "min_version": self.min_version,
            "max_version": self.max_version,
            "cipher_suites": self.cipher_suites,
            "sni_hostname": self.sni_hostname,
            "certificate_path": self.certificate_path,
            "key_path": self.key_path,
            "ja3_fingerprint_library": self.ja3_fingerprint_library,
            "grease_extensions": self.grease_extensions,
            "alpn_protocols": self.alpn_protocols,
        }


@dataclass
class DnsProfile:
    """DNS tunneling beacon configuration.

    Controls how the DNS beacon encodes commands and results in DNS
    queries, including encoding scheme, domain structure, and timing.

    Attributes:
        enabled: Whether DNS transport is active.
        domain: Parent domain for DNS queries (sub.<domain>).
        query_types: Allowed DNS query types.
        encoding: Data encoding scheme (base32, base64, hex, raw).
        max_query_length: Maximum length of a single DNS query label.
        idle_jitter_ms: Jitter in milliseconds between idle queries.
        poll_interval_ms: Polling interval in milliseconds.
        ttl_cache_bypass: Use unique subdomains to bypass DNS caching.
    """

    enabled: bool = False
    domain: str = ""
    query_types: list[str] = field(default_factory=lambda: ["A", "TXT"])
    encoding: str = "base64"
    max_query_length: int = 63
    idle_jitter_ms: int = 2000
    poll_interval_ms: int = 10000
    ttl_cache_bypass: bool = True

    def build_query_subdomain(self, data: bytes, packet_id: int = 0) -> str:
        """Build a DNS query subdomain from encoded data and a packet ID.

        Args:
            data: Raw bytes to encode in the subdomain.
            packet_id: Sequence number for TTL cache bypass.

        Returns:
            A subdomain string like 'abc123.sessions.mydomain.com'.
        """
        if self.ttl_cache_bypass:
            prefix = f"p{packet_id}"
        else:
            prefix = "c"
        if self.encoding == "base32":
            import base64 as _b64
            encoded = _b64.b32encode(data).decode().rstrip("=").lower()
        elif self.encoding == "base64":
            import base64 as _b64
            encoded = (
                _b64.urlsafe_b64encode(data).decode().rstrip("=").replace("+", "-").replace("/", "_")
            )
        elif self.encoding == "hex":
            encoded = data.hex()
        else:
            encoded = data.decode(errors="replace")
        encoded = encoded[:self.max_query_length]
        return f"{prefix}{encoded}.{self.domain.lstrip('.')}"

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> DnsProfile:
        """Build a DnsProfile from a configuration dictionary."""
        return DnsProfile(
            enabled=bool(raw.get("enabled", False)),
            domain=str(raw.get("domain", "")),
            query_types=list(raw.get("query_types", ["A", "TXT"])),
            encoding=str(raw.get("encoding", "base64")),
            max_query_length=int(raw.get("max_query_length", 63)),
            idle_jitter_ms=int(raw.get("idle_jitter_ms", 2000)),
            poll_interval_ms=int(raw.get("poll_interval_ms", 10000)),
            ttl_cache_bypass=bool(raw.get("ttl_cache_bypass", True)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize this profile to a plain dictionary."""
        return {
            "enabled": self.enabled,
            "domain": self.domain,
            "query_types": self.query_types,
            "encoding": self.encoding,
            "max_query_length": self.max_query_length,
            "idle_jitter_ms": self.idle_jitter_ms,
            "poll_interval_ms": self.poll_interval_ms,
            "ttl_cache_bypass": self.ttl_cache_bypass,
        }


@dataclass
class SmbProfile:
    """SMB peer-to-peer named pipe beacon configuration.

    Controls the named pipe path, authentication mechanism, and
    retransmission settings for chained beacon communication over
    SMB named pipes within an internal network.

    Attributes:
        enabled: Whether SMB transport is active.
        pipe_name: Named pipe path (e.g., '\\\\\\.\\pipe\\MyPipe').
        domain: Windows domain for authentication.
        username: SMB authentication username.
        ntlm_hash: NTLM hash for pass-the-hash authentication.
        retry_count: Maximum retransmission attempts.
        retry_interval_ms: Delay between retries in milliseconds.
        timeout_ms: I/O operation timeout in milliseconds.
        encrypt_traffic: Whether to request SMB encryption (3.x+).
    """

    enabled: bool = False
    pipe_name: str = ""
    domain: str = ""
    username: str = ""
    ntlm_hash: str = ""
    retry_count: int = 3
    retry_interval_ms: int = 5000
    timeout_ms: int = 30000
    encrypt_traffic: bool = True

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> SmbProfile:
        """Build an SmbProfile from a configuration dictionary."""
        return SmbProfile(
            enabled=bool(raw.get("enabled", False)),
            pipe_name=str(raw.get("pipe_name", "")),
            domain=str(raw.get("domain", "")),
            username=str(raw.get("username", "")),
            ntlm_hash=str(raw.get("ntlm_hash", "")),
            retry_count=int(raw.get("retry_count", 3)),
            retry_interval_ms=int(raw.get("retry_interval_ms", 5000)),
            timeout_ms=int(raw.get("timeout_ms", 30000)),
            encrypt_traffic=bool(raw.get("encrypt_traffic", True)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize this profile to a plain dictionary."""
        return {
            "enabled": self.enabled,
            "pipe_name": self.pipe_name,
            "domain": self.domain,
            "username": self.username,
            "ntlm_hash": self.ntlm_hash,
            "retry_count": self.retry_count,
            "retry_interval_ms": self.retry_interval_ms,
            "timeout_ms": self.timeout_ms,
            "encrypt_traffic": self.encrypt_traffic,
        }


@dataclass
class WebSocketProfile:
    """WebSocket transport configuration for beacon channels.

    Attributes:
        enabled: Whether WebSocket transport is active.
        protocol: 'ws' or 'wss'.
        path: URI path for the WebSocket endpoint.
        origin: Origin header value for the handshake.
        subprotocols: WebSocket subprotocol list.
        use_compression: Enable per-message deflate extension.
        use_masking: Apply client-to-server masking (RFC 6455).
        heartbeat_interval_ms: Ping/pong heartbeat interval.
        max_message_size_kb: Maximum inbound message size in KB.
    """

    enabled: bool = False
    protocol: str = "wss"
    path: str = "/ws/connect"
    origin: str = ""
    subprotocols: list[str] = field(default_factory=list)
    use_compression: bool = True
    use_masking: bool = True
    heartbeat_interval_ms: int = 30000
    max_message_size_kb: int = 1024

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> WebSocketProfile:
        """Build a WebSocketProfile from a configuration dictionary."""
        return WebSocketProfile(
            enabled=bool(raw.get("enabled", False)),
            protocol=str(raw.get("protocol", "wss")),
            path=str(raw.get("path", "/ws/connect")),
            origin=str(raw.get("origin", "")),
            subprotocols=list(raw.get("subprotocols", [])),
            use_compression=bool(raw.get("use_compression", True)),
            use_masking=bool(raw.get("use_masking", True)),
            heartbeat_interval_ms=int(raw.get("heartbeat_interval_ms", 30000)),
            max_message_size_kb=int(raw.get("max_message_size_kb", 1024)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize this profile to a plain dictionary."""
        return {
            "enabled": self.enabled,
            "protocol": self.protocol,
            "path": self.path,
            "origin": self.origin,
            "subprotocols": self.subprotocols,
            "use_compression": self.use_compression,
            "use_masking": self.use_masking,
            "heartbeat_interval_ms": self.heartbeat_interval_ms,
            "max_message_size_kb": self.max_message_size_kb,
        }


class TransportType(Enum):
    """Enumeration of supported C2 transport types."""

    HTTP = "http"
    DNS = "dns"
    SMB = "smb"
    WEBSOCKET = "websocket"


@dataclass
class RotationSlot:
    """Tracks a profile slot in the rotation queue.

    Attributes:
        name: Human-readable slot name.
        transport: Transport type this slot activates.
        last_used_at: Unix timestamp of last activation.
        cooldown_s: Minimum seconds between activations.
    """

    name: str
    transport: TransportType
    last_used_at: float = 0.0
    cooldown_s: int = DEFAULT_ROTATION_COOLDOWN_S

    def is_available(self) -> bool:
        """Return True if the cooldown window has elapsed."""
        if self.last_used_at == 0.0:
            return True
        elapsed = time.monotonic() - self.last_used_at
        return elapsed >= self.cooldown_s

    def touch(self) -> None:
        """Mark this slot as just used."""
        self.last_used_at = time.monotonic()


class ProfileRotator:
    """Round-robin profile rotation with cooldown windows.

    Maintains a queue of RotationSlot objects and advances the active
    slot on each call to ``rotate()``. Slots that are within their
    cooldown window are skipped automatically.

    Attributes:
        slots: Ordered list of rotation slots.
        current_index: Index of the currently active slot.
    """

    def __init__(self, slots: list[RotationSlot]) -> None:
        if not slots:
            raise ValueError("ProfileRotator requires at least one rotation slot")
        self._slots = list(slots)
        self._current_index = 0

    @property
    def current_slot(self) -> RotationSlot:
        """Return the currently active rotation slot."""
        return self._slots[self._current_index]

    @property
    def transport(self) -> TransportType:
        """Return the transport type of the current slot."""
        return self.current_slot.transport

    def rotate(self) -> RotationSlot:
        """Advance to the next available slot and return it.

        Skips slots still in their cooldown window. If all slots are
        on cooldown, the cooldowns are reset and rotation starts fresh.
        """
        self.current_slot.touch()
        attempts = len(self._slots)
        for _ in range(attempts):
            self._current_index = (self._current_index + 1) % len(self._slots)
            if self.current_slot.is_available():
                return self.current_slot
        for slot in self._slots:
            slot.last_used_at = 0.0
        self._current_index = 0
        self.current_slot.touch()
        return self.current_slot

    def list_slots(self) -> list[dict[str, Any]]:
        """Return a list of slot states for inspection."""
        result = []
        for i, slot in enumerate(self._slots):
            result.append({
                "name": slot.name,
                "transport": slot.transport.value,
                "active": i == self._current_index,
                "available": slot.is_available(),
                "cooldown_s": slot.cooldown_s,
            })
        return result


class ProfileValidator:
    """Validates transport profile configurations.

    Checks for logical inconsistencies such as enabled profiles
    missing required fields (domain for DNS, pipe name for SMB).
    """

    @staticmethod
    def validate_tls(profile: TlsProfile) -> list[str]:
        """Validate a TlsProfile and return error messages."""
        errors: list[str] = []
        if not profile.enabled:
            return errors
        if profile.min_version not in ("1.2", "1.3"):
            errors.append("tls.min_version must be '1.2' or '1.3'")
        if profile.max_version not in ("1.2", "1.3"):
            errors.append("tls.max_version must be '1.2' or '1.3'")
        cert = Path(profile.certificate_path)
        key = Path(profile.key_path)
        if profile.certificate_path and not cert.is_file():
            errors.append(f"tls.certificate_path does not exist: {profile.certificate_path}")
        if profile.key_path and not key.is_file():
            errors.append(f"tls.key_path does not exist: {profile.key_path}")
        if profile.certificate_path and not profile.key_path:
            errors.append("tls.key_path is required when certificate_path is set")
        if profile.ja3_fingerprint_library not in LIBRARY_CIPHER_SUITES:
            errors.append(
                f"tls.ja3_fingerprint_library '{profile.ja3_fingerprint_library}' "
                f"not in known libraries: {', '.join(sorted(LIBRARY_CIPHER_SUITES))}"
            )
        return errors

    @staticmethod
    def validate_dns(profile: DnsProfile) -> list[str]:
        """Validate a DnsProfile and return error messages."""
        errors: list[str] = []
        if not profile.enabled:
            return errors
        if not profile.domain:
            errors.append("dns.domain is required when DNS transport is enabled")
        elif not re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}$", profile.domain):
            errors.append(f"dns.domain '{profile.domain}' is not a valid domain name")
        if profile.encoding not in DNS_ENCODINGS:
            errors.append(f"dns.encoding must be one of {DNS_ENCODINGS}, got '{profile.encoding}'")
        if profile.max_query_length < 1 or profile.max_query_length > 253:
            errors.append("dns.max_query_length must be between 1 and 253")
        if profile.poll_interval_ms < 1000:
            errors.append("dns.poll_interval_ms must be >= 1000 ms")
        if profile.idle_jitter_ms < 0:
            errors.append("dns.idle_jitter_ms must be >= 0")
        return errors

    @staticmethod
    def validate_smb(profile: SmbProfile) -> list[str]:
        """Validate an SmbProfile and return error messages."""
        errors: list[str] = []
        if not profile.enabled:
            return errors
        if not profile.pipe_name:
            errors.append("smb.pipe_name is required when SMB transport is enabled")
        elif len(profile.pipe_name) > SMB_NAMED_PIPE_MAX_LENGTH:
            errors.append(
                f"smb.pipe_name exceeds {SMB_NAMED_PIPE_MAX_LENGTH} characters"
            )
        if profile.retry_count < 1:
            errors.append("smb.retry_count must be >= 1")
        if profile.retry_interval_ms < 100:
            errors.append("smb.retry_interval_ms must be >= 100 ms")
        if profile.timeout_ms < 1000:
            errors.append("smb.timeout_ms must be >= 1000 ms")
        if profile.username and not profile.domain:
            errors.append("smb.domain is required when username is set")
        return errors

    @staticmethod
    def validate_websocket(profile: WebSocketProfile) -> list[str]:
        """Validate a WebSocketProfile and return error messages."""
        errors: list[str] = []
        if not profile.enabled:
            return errors
        if profile.protocol not in WEBSOCKET_PROTOCOLS:
            errors.append(f"websocket.protocol must be one of {WEBSOCKET_PROTOCOLS}")
        if not profile.path.startswith("/"):
            errors.append("websocket.path must start with '/'")
        if profile.heartbeat_interval_ms < 5000:
            errors.append("websocket.heartbeat_interval_ms must be >= 5000 ms")
        if profile.max_message_size_kb < 1:
            errors.append("websocket.max_message_size_kb must be >= 1")
        return errors

    def validate_all(
        self,
        tls: TlsProfile | None = None,
        dns: DnsProfile | None = None,
        smb: SmbProfile | None = None,
        websocket: WebSocketProfile | None = None,
    ) -> dict[str, list[str]]:
        """Validate all provided profiles and return a dict of transport -> errors."""
        result: dict[str, list[str]] = {}
        if tls is not None:
            result["tls"] = self.validate_tls(tls)
        if dns is not None:
            result["dns"] = self.validate_dns(dns)
        if smb is not None:
            result["smb"] = self.validate_smb(smb)
        if websocket is not None:
            result["websocket"] = self.validate_websocket(websocket)
        return result


class ProfileEngine:
    """Composition root for the extended C2 profile system.

    Combines HTTP profiles from ``modules.c2_profile.py`` with transport
    profiles (TLS, DNS, SMB, WebSocket) defined in this module. Provides
    profile rotation and validation across all transport layers.

    Attributes:
        tls_profile: Active TLS configuration.
        dns_profile: Active DNS beacon configuration.
        smb_profile: Active SMB peer-to-peer configuration.
        websocket_profile: Active WebSocket configuration.
        rotator: ProfileRotator instance for auto-rotation.
        validator: ProfileValidator for transport-level validation.
    """

    def __init__(
        self,
        tls_profile: TlsProfile | None = None,
        dns_profile: DnsProfile | None = None,
        smb_profile: SmbProfile | None = None,
        websocket_profile: WebSocketProfile | None = None,
        rotation_slots: list[RotationSlot] | None = None,
    ) -> None:
        self._tls = tls_profile or TlsProfile()
        self._dns = dns_profile or DnsProfile()
        self._smb = smb_profile or SmbProfile()
        self._websocket = websocket_profile or WebSocketProfile()
        self._rotator = ProfileRotator(rotation_slots or self._default_slots())
        self._validator = ProfileValidator()

    @property
    def tls_profile(self) -> TlsProfile:
        """Return the current TLS profile."""
        return self._tls

    @property
    def dns_profile(self) -> DnsProfile:
        """Return the current DNS profile."""
        return self._dns

    @property
    def smb_profile(self) -> SmbProfile:
        """Return the current SMB profile."""
        return self._smb

    @property
    def websocket_profile(self) -> WebSocketProfile:
        """Return the current WebSocket profile."""
        return self._websocket

    @property
    def rotator(self) -> ProfileRotator:
        """Return the profile rotator."""
        return self._rotator

    @property
    def active_transport(self) -> TransportType:
        """Return the currently active transport type."""
        return self._rotator.transport

    def rotate(self) -> RotationSlot:
        """Advance to the next transport in the rotation queue."""
        return self._rotator.rotate()

    def validate(self) -> dict[str, list[str]]:
        """Validate all transport profiles and return error dict."""
        return self._validator.validate_all(
            tls=self._tls,
            dns=self._dns,
            smb=self._smb,
            websocket=self._websocket,
        )

    def get_active_profile_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict of the active transport config."""
        transport = self._rotator.transport
        profiles: dict[TransportType, Any] = {
            TransportType.HTTP: {},
            TransportType.DNS: self._dns.to_dict(),
            TransportType.SMB: self._smb.to_dict(),
            TransportType.WEBSOCKET: self._websocket.to_dict(),
        }
        result = profiles.get(transport, {})
        result["transport"] = transport.value
        result["tls"] = self._tls.to_dict()
        return result

    def get_all_profiles_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict of all profiles."""
        return {
            "tls": self._tls.to_dict(),
            "dns": self._dns.to_dict(),
            "smb": self._smb.to_dict(),
            "websocket": self._websocket.to_dict(),
            "rotation": self._rotator.list_slots(),
        }

    def _default_slots(self) -> list[RotationSlot]:
        """Build default rotation slots from enabled transports."""
        slots: list[RotationSlot] = []
        if self._tls.enabled:
            slots.append(
                RotationSlot(
                    name="http-tls",
                    transport=TransportType.HTTP,
                )
            )
        if self._dns.enabled:
            slots.append(
                RotationSlot(
                    name="dns-tunnel",
                    transport=TransportType.DNS,
                    cooldown_s=1200,
                )
            )
        if self._smb.enabled:
            slots.append(
                RotationSlot(
                    name="smb-peer",
                    transport=TransportType.SMB,
                    cooldown_s=300,
                )
            )
        if self._websocket.enabled:
            slots.append(
                RotationSlot(
                    name="websocket-stream",
                    transport=TransportType.WEBSOCKET,
                )
            )
        if not slots:
            slots.append(
                RotationSlot(name="http-default", transport=TransportType.HTTP)
            )
        return slots

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ProfileEngine:
        """Build a ProfileEngine from a configuration dictionary.

        Expected structure:
            {
                "c2_tls": {...},
                "c2_dns": {...},
                "c2_smb": {...},
                "c2_websocket": {...}
            }
        """
        return cls(
            tls_profile=TlsProfile.from_dict(raw.get("c2_tls", {})),
            dns_profile=DnsProfile.from_dict(raw.get("c2_dns", {})),
            smb_profile=SmbProfile.from_dict(raw.get("c2_smb", {})),
            websocket_profile=WebSocketProfile.from_dict(raw.get("c2_websocket", {})),
        )

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> ProfileEngine:
        """Build a ProfileEngine from a LazyOwn payload configuration dict."""
        return cls.from_dict(payload)

    @classmethod
    def from_config(cls, config: Config) -> ProfileEngine:
        """Build a ProfileEngine from a LazyOwn Config object."""
        raw: dict[str, Any] = {
            "c2_tls": config.get("c2_tls", {}),
            "c2_dns": config.get("c2_dns", {}),
            "c2_smb": config.get("c2_smb", {}),
            "c2_websocket": config.get("c2_websocket", {}),
        }
        return cls.from_dict(raw)


__all__ = [
    "ProfileEngine",
    "ProfileRotator",
    "ProfileValidator",
    "RotationSlot",
    "TransportType",
    "TlsProfile",
    "DnsProfile",
    "SmbProfile",
    "WebSocketProfile",
    "LIBRARY_CIPHER_SUITES",
    "JA3_GREASE_CANDIDATES",
]
