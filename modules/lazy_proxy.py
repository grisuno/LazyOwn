"""Recording HTTP/HTTPS proxy for the autonomous loop.

Every exchange a worker (or any tool the operator routes) sends through
this proxy is persisted with the existing
:class:`modules.traffic_recorder.TrafficRecorder`: file-tree bodies plus
SQLite index. HTTPS is terminated with a locally generated CA so
request and response bodies are captured for findings/evidence; the CA
certificate path is exported so curl/requests/python trust it.

Automation contract:
    ``LazyLoopEngine.proxy_start()`` starts one shared recorder
    instance; ``auto_loop`` starts it when ``proxy_autostart`` is on and
    points the worker environment at it; every round ingests new
    exchanges into the task traffic log so ``lazy_traffic`` and finding
    evidence see proxy traffic like any bash execution.

Fail-open policy: recorder or TLS problems never kill the operator's
traffic; the proxy answers 502 and keeps serving.
"""

from __future__ import annotations

import http.client
import ipaddress
import logging
import os
import re
import select
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from datetime import UTC
from pathlib import Path
from urllib.parse import urlsplit

from core.hardening import (
    tls_lab_fallback_context as _hardened_lab_fallback_context,
)
from core.hardening import (
    tls_lab_unverified_allowed as _hardened_lab_unverified_allowed,
)
from core.hardening import (
    tls_secure_context as _hardened_tls_secure_context,
)
from core.hardening import (
    validate_upstream_path as _hardened_validate_upstream_path,
)
from modules.traffic_recorder import TrafficRecorder

DEFAULT_PROXY_HOST = "127.0.0.1"
DEFAULT_PROXY_PORT = 8899
DEFAULT_TRAFFIC_DIR_NAME = "traffic"
CA_CERT_NAME = "ca.pem"
CA_KEY_NAME = "ca.key"
CA_COMMON_NAME = "LazyOwn Recorder CA"
CA_VALID_DAYS = 3650
LEAF_VALID_DAYS = 825
UPSTREAM_TIMEOUT_SEC = 30.0
MAX_BODY_BYTES = 2_000_000
MAX_TUNNEL_REQUESTS = 200
TRUST_ANCHOR_NAME = "lazyown-recorder-ca.crt"
NSS_NICKNAME = "LazyOwn Recorder CA"
TRUST_TARGETS = (
    ("/usr/local/share/ca-certificates", ("update-ca-certificates",)),
    ("/etc/pki/ca-trust/source/anchors", ("update-ca-trust", "extract")),
    ("/etc/ca-certificates/trust-source/anchors", ("trust", "extract-compat")),
)
HOP_BY_HOP = frozenset(
    {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "proxy-connection",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
    }
)

log = logging.getLogger("modules.lazy_proxy")

_METADATA_IPV4 = frozenset({"169.254.169.254", "169.254.169.253", "100.100.100.200"})
_METADATA_IPV6 = frozenset({"fd00:ec2::254"})
_METADATA_HOSTNAMES = frozenset(
    {
        "metadata.google.internal",
        "metadata.goog",
        "metadata.azure.internal",
        "instance-data",
        "instance-data-compute",
    }
)
_MAX_HOST_LEN = 253
_HOST_LABEL_RE = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")
_INSECURE_TLS_WARNED = False


def _proxy_allow_private() -> bool:
    """Return True when private/loopback targets stay reachable.

    The recorder proxy is a pentest tool: lab targets live on
    RFC1918/loopback. Blocking them by default would break the core
    workflow, so they stay allowed unless the operator sets
    ``LAZY_PROXY_ALLOW_PRIVATE=0``. Cloud metadata endpoints are
    always denied regardless of this flag.
    """
    return os.environ.get("LAZY_PROXY_ALLOW_PRIVATE", "1") != "0"


def _proxy_insecure_tls() -> bool:
    """Return True only when the operator explicitly opts into no-verify TLS."""
    return os.environ.get("LAZY_PROXY_INSECURE_TLS", "") == "1"


def _proxy_trust_ca() -> str:
    """Return an extra CA bundle path for upstream verification, if configured."""
    return str(os.environ.get("LAZY_PROXY_TRUST_CA", "") or "").strip()


def _is_metadata_ip(value: str) -> bool:
    """Return True for known cloud instance-metadata service addresses."""
    text = (value or "").strip().strip("[]").lower()
    if text in _METADATA_IPV4 or text in _METADATA_IPV6:
        return True
    try:
        addr = ipaddress.ip_address(text)
    except ValueError:
        return False
    if str(addr) in _METADATA_IPV4 or str(addr.compressed).lower() in _METADATA_IPV6:
        return True
    return False


def _is_metadata_hostname(host: str) -> bool:
    """Return True for well-known cloud metadata DNS names."""
    name = (host or "").strip().lower().rstrip(".")
    if not name:
        return False
    if name in _METADATA_HOSTNAMES or name in _METADATA_IPV4:
        return True
    if name.endswith(".metadata.google.internal"):
        return True
    return False


def _host_syntax_valid(host: str) -> bool:
    """Validate host syntax without trusting its value for routing."""
    if not host or len(host) > _MAX_HOST_LEN or "\x00" in host:
        return False
    if any(ch.isspace() for ch in host) or "@" in host or "/" in host:
        return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        pass
    if ".." in host or host.startswith(("-", ".")) or host.endswith(("-", ".")):
        return False
    return all(_HOST_LABEL_RE.match(label) for label in host.split("."))


def _resolved_ips(host: str) -> list[str]:
    """Resolve host to literal IPs; empty list when DNS is unavailable."""
    try:
        infos = socket.getaddrinfo(host, None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
    except OSError:
        return []
    out: list[str] = []
    for info in infos:
        sockaddr = info[4] if len(info) > 4 else ()
        if sockaddr:
            out.append(str(sockaddr[0]))
    return out


def _validate_proxy_target(host: str, port: int, scheme: str) -> tuple[str, int]:
    """Validate a proxy target derived from client-controlled data.

    Raises:
        ValueError: When the target is malformed or denied by SSRF policy.

    Policy: scheme must be http/https, port 1-65535, host syntax valid,
    ``0.0.0.0``/unspecified rejected, cloud metadata hosts/IPs always
    rejected (including DNS-resolved addresses), private/loopback allowed
    only when ``LAZY_PROXY_ALLOW_PRIVATE`` is on.
    """
    if scheme not in ("http", "https"):
        raise ValueError(f"unsupported scheme: {scheme!r}")
    candidate = (host or "").strip().strip("[]")
    if not candidate or not _host_syntax_valid(candidate):
        raise ValueError("invalid proxy host")
    try:
        port_num = int(port)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid proxy port") from exc
    if not 1 <= port_num <= 65535:
        raise ValueError("proxy port out of range")
    if _is_metadata_hostname(candidate) or _is_metadata_ip(candidate):
        raise ValueError("proxy target denied (metadata service)")
    try:
        addr = ipaddress.ip_address(candidate)
        if addr.is_unspecified:
            raise ValueError("proxy target denied (unspecified address)")
        if addr.is_multicast:
            raise ValueError("proxy target denied (multicast)")
        if (addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved) and not (
            _is_metadata_ip(candidate)
        ):
            pass
    except ValueError as exc:
        if "proxy target denied" in str(exc):
            raise
    for resolved in _resolved_ips(candidate):
        if _is_metadata_ip(resolved):
            raise ValueError("proxy target denied (metadata service)")
        try:
            raddr = ipaddress.ip_address(resolved)
        except ValueError:
            continue
        if raddr.is_unspecified or raddr.is_multicast:
            raise ValueError("proxy target denied (resolved restricted address)")
        if not _proxy_allow_private() and (
            raddr.is_private or raddr.is_loopback or raddr.is_link_local or raddr.is_reserved
        ):
            raise ValueError("proxy target denied (private address)")
    return candidate, port_num


def _upstream_tls_context(server_hostname: str) -> ssl.SSLContext:
    """Build a verifying client TLS context for upstream connections.

    Hostname checking stays on with ``CERT_REQUIRED`` and TLS 1.2 floor.
    An operator bundle from ``LAZY_PROXY_TRUST_CA`` is loaded when set.
    An explicit ``LAZY_PROXY_INSECURE_TLS=1`` opt-in returns an
    unverified context (logged once); request data can never enable it.
    """
    global _INSECURE_TLS_WARNED
    if _proxy_insecure_tls():
        if not _INSECURE_TLS_WARNED:
            _INSECURE_TLS_WARNED = True
            log.warning("LAZY_PROXY_INSECURE_TLS=1: upstream TLS verification disabled by operator")
        return _hardened_lab_fallback_context()
    return _hardened_tls_secure_context(_proxy_trust_ca())


def tls_lab_unverified_allowed(host: str) -> bool:
    """Return True only when a lab host has explicit self-signed opt-in.

    Args:
        host: Target hostname or IP literal.

    Returns:
        True when ``LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1`` covers this host.
    """
    return bool(_hardened_lab_unverified_allowed(host))


def _validate_upstream_path(path: str) -> str:
    """Validate origin-form path before any upstream request.

    Args:
        path: Upstream request path.

    Returns:
        The validated path unchanged.

    Raises:
        ValueError: When the path is not safe origin-form.
    """
    if not _hardened_validate_upstream_path(path or "/"):
        raise ValueError("invalid upstream path")
    return path


def resolve_validated_target(host: str, port: int, scheme: str) -> tuple[str, list[str]]:
    """Validate a target and return its pinned IP literals.

    The returned IPs already passed the metadata/private policy, so
    callers must dial one of them instead of re-resolving the hostname
    (DNS-rebinding TOCTOU guard) while keeping SNI/host header as the
    original validated hostname.

    Args:
        host: Client-supplied target host.
        port: Client-supplied target port.
        scheme: ``http`` or ``https``.

    Returns:
        Tuple of validated hostname and pinned IP list (possibly empty
        for IP literals, in which case the literal itself is the pin).

    Raises:
        ValueError: When the target is denied by SSRF policy.
    """
    candidate, port_num = _validate_proxy_target(host, port, scheme)
    try:
        literal = ipaddress.ip_address(candidate)
    except ValueError:
        literal = None
    if literal is not None:
        return candidate, [str(literal)]
    pinned: list[str] = []
    for resolved in _resolved_ips(candidate):
        if _is_metadata_ip(resolved):
            raise ValueError("proxy target denied (metadata service)")
        try:
            addr = ipaddress.ip_address(resolved)
        except ValueError:
            continue
        if addr.is_unspecified or addr.is_multicast:
            raise ValueError("proxy target denied (resolved restricted address)")
        if not _proxy_allow_private() and (
            addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
        ):
            raise ValueError("proxy target denied (private address)")
        pinned.append(str(addr))
    if not pinned:
        raise ValueError("proxy target denied (unresolvable host)")
    return candidate, pinned


def _dial_pinned(ips: list[str], port: int, *, timeout: float):
    """Dial each pinned IP in order, returning the first connected socket.

    Args:
        ips: Validated IP literals from :func:`resolve_validated_target`.
        port: Validated port.
        timeout: Connection timeout in seconds.

    Returns:
        Connected socket.

    Raises:
        ValueError: When no pinned address exists.
        OSError: When every pinned address refuses the connection.
    """
    if not ips:
        raise ValueError("no pinned address for proxy target")
    errors: list[OSError] = []
    for literal in ips:
        try:
            return socket.create_connection((literal, int(port)), timeout=timeout)
        except OSError as exc:
            errors.append(exc)
    raise errors[-1]


def connect_pinned(host: str, ips: list[str], port: int, scheme: str, *, timeout: float):
    """Open a socket to a pinned validated IP, wrapping TLS for https.

    Args:
        host: Validated hostname for SNI and certificate verification.
        ips: Pinned IP literals from :func:`resolve_validated_target`.
        port: Validated port.
        scheme: ``http`` or ``https``.
        timeout: Connection timeout in seconds.

    Returns:
        Connected (optionally TLS-wrapped) socket.
    """
    raw = _dial_pinned(ips, port, timeout=timeout)
    if scheme != "https":
        return raw
    try:
        return _upstream_tls_context(host).wrap_socket(raw, server_hostname=host)
    except ssl.SSLCertVerificationError:
        try:
            raw.close()
        except OSError:
            pass
        raise


class _PinnedHTTPConnection(http.client.HTTPConnection):
    """HTTP connection dialling a validated IP instead of the hostname."""

    def __init__(self, host: str, port: int, *, pinned_ips: list[str], timeout: float) -> None:
        """Store pinned IPs; hostname is kept for headers only."""
        super().__init__(host, port, timeout=timeout)
        self._pinned_ips = list(pinned_ips or [])

    def connect(self) -> None:
        """Dial the pinned IP so DNS cannot re-resolve to another host."""
        self.sock = _dial_pinned(self._pinned_ips, self.port, timeout=self.timeout)


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS connection dialling a validated IP with SNI preserved."""

    def __init__(
        self,
        host: str,
        port: int,
        *,
        pinned_ips: list[str],
        timeout: float,
        context: ssl.SSLContext,
    ) -> None:
        """Store pinned IPs and the verifying TLS context."""
        super().__init__(host, port, timeout=timeout, context=context)
        self._pinned_ips = list(pinned_ips or [])

    def connect(self) -> None:
        """Dial the pinned IP and verify the cert against the hostname."""
        raw = _dial_pinned(self._pinned_ips, self.port, timeout=self.timeout)
        self.sock = self._context.wrap_socket(raw, server_hostname=self.host)


def _is_lab_host(host: str) -> bool:
    """Return True for loopback/private literals or localhost."""
    name = (host or "").strip().strip("[]").lower()
    if name == "localhost":
        return True
    try:
        addr = ipaddress.ip_address(name)
        return bool(addr.is_loopback or addr.is_private or addr.is_link_local)
    except ValueError:
        return False


def _https_connection(host: str, port: int, *, timeout: float) -> http.client.HTTPSConnection:
    """Return an HTTPS connection, verifying by default.

    Public targets always verify. Lab (loopback/private) targets with
    self-signed certs fall back to unverified only to preserve the
    recorder workflow, with a one-time warning; the fallback is gated
    by operator policy, never by request data.
    """
    return http.client.HTTPSConnection(host, port, timeout=timeout, context=_upstream_tls_context(host))


def _default_traffic_dir() -> Path:
    """Return the shared recorder directory under the repository."""
    return Path(__file__).resolve().parent.parent / "sessions" / DEFAULT_TRAFFIC_DIR_NAME


def _parse_upstream(spec: str) -> dict:
    """Parse ``[user:pass@]host:port`` into an upstream proxy spec.

    The operator-supplied hop is syntax-validated here (metadata hops
    rejected); per-request targets are still validated and pinned at
    relay time.
    """
    text = (spec or "").strip()
    if not text:
        return {}
    auth = ""
    if "@" in text:
        auth, _, text = text.rpartition("@")
    host, _, port_text = text.rpartition(":")
    if not host:
        host, port_text = "127.0.0.1", text
    try:
        port = int(port_text or 8080)
    except ValueError:
        port = 8080
    candidate = host.strip().strip("[]")
    if not candidate or not _host_syntax_valid(candidate):
        return {}
    if _is_metadata_hostname(candidate) or _is_metadata_ip(candidate):
        log.warning("upstream proxy to metadata service denied")
        return {}
    if not 1 <= port <= 65535:
        return {}
    return {"host": candidate, "port": port, "auth": auth}


def _upstream_auth_header(auth: str) -> dict:
    """Build a Proxy-Authorization header from ``user:pass``."""
    if not auth:
        return {}
    import base64

    token = base64.b64encode(auth.encode()).decode()
    return {"Proxy-Authorization": f"Basic {token}"}


def _cert_stem(host: str) -> str:
    """Normalize a host into a filesystem-safe certificate name."""
    return re.sub(r"[^A-Za-z0-9._-]", "_", host or "unknown")[:80] or "unknown"


def detect_trust_target() -> tuple[str, tuple[str, ...]]:
    """Return the first existing system trust anchor directory and refresh command."""
    for anchor_dir, command in TRUST_TARGETS:
        if Path(anchor_dir).is_dir():
            return anchor_dir, command
    return "", ()


def ca_trusted(ca_path: str | Path) -> bool:
    """Return True when the system anchor already holds this CA."""
    anchor_dir, _ = detect_trust_target()
    if not anchor_dir:
        return False
    anchor = Path(anchor_dir) / TRUST_ANCHOR_NAME
    try:
        return anchor.exists() and anchor.read_bytes() == Path(ca_path).read_bytes()
    except OSError:
        return False


def _run_root(argv: list[str]) -> subprocess.CompletedProcess:
    """Run a privileged command, prompting for sudo only when needed."""
    if os.geteuid() == 0:
        return subprocess.run(argv, check=False, timeout=180)
    return subprocess.run(["sudo", *argv], check=False, timeout=300)


def detect_nss_profiles() -> list[str]:
    """Return user NSS database directories (Firefox profiles + Chrome)."""
    home = Path.home()
    profiles: list[str] = []
    try:
        for cert_db in sorted(home.glob(".mozilla/firefox/*/cert9.db")):
            profiles.append(str(cert_db.parent))
    except OSError:
        pass
    chrome_db = home / ".pki" / "nssdb"
    if chrome_db.is_dir():
        profiles.append(str(chrome_db))
    return profiles


def install_ca_nss(ca_path: str | Path, runner=None, profiles: list[str] | None = None) -> dict:
    """Install the recorder CA into user NSS databases via certutil.

    NSS stores are user-owned, so no sudo is required; the command is a
    no-op when certutil or the profiles are missing.

    Args:
        ca_path: CA certificate PEM path.
        runner: Injection point for certutil execution (tests).
        profiles: Explicit NSS directories (defaults to auto-discovery).

    Returns:
        Dict with installed/profiles counts and reason; never raises.
    """
    ca_file = Path(ca_path)
    if not ca_file.exists():
        return {"installed": 0, "profiles": 0, "reason": "ca certificate not found"}
    certutil = shutil.which("certutil")
    if not certutil:
        return {"installed": 0, "profiles": 0, "reason": "certutil not installed"}
    directories = list(profiles) if profiles is not None else detect_nss_profiles()
    if not directories:
        return {"installed": 0, "profiles": 0, "reason": "no NSS profiles"}
    run = runner or (lambda argv: subprocess.run(argv, check=False, timeout=60))
    installed = 0
    failed = 0
    for directory in directories:
        database = f"sql:{directory}"
        check = run([certutil, "-L", "-d", database, "-n", NSS_NICKNAME])
        if getattr(check, "returncode", 1) == 0:
            installed += 1
            continue
        add = run([certutil, "-A", "-d", database, "-n", NSS_NICKNAME, "-t", "C,,", "-i", str(ca_file)])
        if getattr(add, "returncode", 1) == 0:
            installed += 1
        else:
            failed += 1
    return {"installed": installed, "profiles": len(directories), "failed": failed, "reason": "ok"}


def install_ca_trust(ca_path: str | Path, runner=None) -> dict:
    """Install the recorder CA into the system trust store.

    The anchor is only written when the CA is missing or stale; sudo is
    invoked then and prompts on the operator terminal. Non-interactive
    callers (MCP) fail soft with a reason instead of hanging.

    Args:
        ca_path: CA certificate PEM path.
        runner: Injection point for privileged execution (tests).

    Returns:
        Dict with installed flag, anchor path and reason; never raises.
    """
    ca_file = Path(ca_path)
    if not ca_file.exists():
        return {"installed": False, "reason": "ca certificate not found", "anchor": ""}
    anchor_dir, refresh = detect_trust_target()
    if not anchor_dir:
        return {"installed": False, "reason": "unsupported trust layout", "anchor": ""}
    anchor = Path(anchor_dir) / TRUST_ANCHOR_NAME
    if ca_trusted(ca_file):
        return {"installed": True, "reason": "already trusted", "anchor": str(anchor)}
    run = runner or _run_root
    staged = ""
    try:
        with tempfile.NamedTemporaryFile("wb", suffix=".crt", delete=False) as handle:
            handle.write(ca_file.read_bytes())
            staged = handle.name
        install_bin = shutil.which("install")
        copy_argv = (
            [install_bin, "-D", "-m", "0644", staged, str(anchor)] if install_bin else ["cp", staged, str(anchor)]
        )
        copied = run(copy_argv)
        if getattr(copied, "returncode", 1) != 0:
            return {"installed": False, "reason": "copy failed (sudo cancelled?)", "anchor": str(anchor)}
        if refresh and shutil.which(refresh[0]):
            refreshed = run(list(refresh))
            if getattr(refreshed, "returncode", 1) != 0:
                return {"installed": False, "reason": "trust refresh failed", "anchor": str(anchor)}
    except Exception as exc:
        return {"installed": False, "reason": str(exc)[:200], "anchor": str(anchor)}
    finally:
        if staged:
            try:
                Path(staged).unlink()
            except OSError:
                pass
    return {"installed": True, "reason": "installed", "anchor": str(anchor)}


class CertificateAuthority:
    """On-disk CA plus cached per-host leaf certificates for MITM."""

    def __init__(self, pki_dir: str | Path) -> None:
        """Load or create the CA under ``pki_dir``."""
        self.pki_dir = Path(pki_dir)
        self.pki_dir.mkdir(parents=True, exist_ok=True)
        self.cert_path = self.pki_dir / CA_CERT_NAME
        self.key_path = self.pki_dir / CA_KEY_NAME
        self.leaf_dir = self.pki_dir / "certs"
        self.leaf_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._contexts: dict[str, ssl.SSLContext] = {}
        self._ensure_ca()

    def _ensure_ca(self) -> None:
        """Create the CA key/cert once and load them into memory."""
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.x509.oid import NameOID

        if self.cert_path.exists() and self.key_path.exists():
            self._ca_key = serialization.load_pem_private_key(self.key_path.read_bytes(), password=None)
            self._ca_cert = x509.load_pem_x509_certificate(self.cert_path.read_bytes())
            return
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, CA_COMMON_NAME)])
        now = time.time()
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(subject)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(_utc(now - 3600))
            .not_valid_after(_utc(now + CA_VALID_DAYS * 86400))
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    content_commitment=False,
                    key_encipherment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    key_cert_sign=True,
                    crl_sign=True,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
            .sign(key, _sha256())
        )
        self.key_path.write_bytes(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        self.cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        try:
            os.chmod(self.key_path, 0o600)
        except OSError:
            pass
        self._ca_key = key
        self._ca_cert = cert

    def _write_leaf(self, host: str, cert_path: Path, key_path: Path) -> None:
        """Generate and persist one leaf certificate for ``host``."""
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.x509.oid import NameOID

        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        try:
            san = x509.IPAddress(__import__("ipaddress").ip_address(host))
        except ValueError:
            san = x509.DNSName(host)
        now = time.time()
        cert = (
            x509.CertificateBuilder()
            .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, host[:64])]))
            .issuer_name(self._ca_cert.subject)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(_utc(now - 3600))
            .not_valid_after(_utc(now + LEAF_VALID_DAYS * 86400))
            .add_extension(x509.SubjectAlternativeName([san]), critical=False)
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
            .add_extension(
                x509.AuthorityKeyIdentifier.from_issuer_public_key(self._ca_key.public_key()), critical=False
            )
            .sign(self._ca_key, _sha256())
        )
        cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        key_path.write_bytes(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        try:
            os.chmod(key_path, 0o600)
        except OSError:
            pass

    def context_for(self, host: str) -> ssl.SSLContext:
        """Return the server TLS context for one host, generating on miss."""
        with self._lock:
            cached = self._contexts.get(host)
            if cached is not None:
                return cached
            stem = _cert_stem(host)
            cert_path = self.leaf_dir / f"{stem}.pem"
            key_path = self.leaf_dir / f"{stem}.key"
            if not cert_path.exists() or not key_path.exists():
                self._write_leaf(host, cert_path, key_path)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            try:
                context.minimum_version = ssl.TLSVersion.TLSv1_2
            except (AttributeError, ValueError):
                pass
            context.load_cert_chain(certfile=str(cert_path), keyfile=str(key_path))
            self._contexts[host] = context
            return context


def _utc(timestamp: float):
    """Return a naive UTC datetime for x509 builders."""
    from datetime import datetime

    return datetime.fromtimestamp(timestamp, tz=UTC)


def _sha256():
    """Return the SHA-256 hasher used for certificate signatures."""
    from cryptography.hazmat.primitives import hashes

    return hashes.SHA256()


def _server_class():
    """Build the ThreadingHTTPServer subclass with recorder attachments."""
    from http.server import ThreadingHTTPServer

    class RecorderServer(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

        def __init__(self, address, handler, *, recorder, authority, task="", upstream=None):
            super().__init__(address, handler)
            self.recorder = recorder
            self.authority = authority
            self.task = task
            self.upstream = dict(upstream or {})

        def handle_error(self, request, client_address) -> None:
            """Silence client-side connection noise instead of tracebacks.

            A browsing target that drops the connection while the proxy
            writes a 502 must not dump a BrokenPipeError traceback per
            request; real server faults still go to the default handler.
            """
            exc = sys.exc_info()[1]
            if isinstance(
                exc, (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, TimeoutError, socket.timeout)
            ):
                return
            ThreadingHTTPServer.handle_error(self, request, client_address)

    return RecorderServer


class ProxyController:
    """Owns the single shared recorder proxy instance."""

    def __init__(self) -> None:
        """Prepare state; nothing binds until :meth:`start`."""
        self._lock = threading.Lock()
        self._server = None
        self._thread: threading.Thread | None = None
        self._authority: CertificateAuthority | None = None
        self._recorder: TrafficRecorder | None = None
        self.host = DEFAULT_PROXY_HOST
        self.port = 0
        self.task = ""
        self.upstream = ""
        self.traffic_dir = _default_traffic_dir()

    def start(
        self,
        host: str = DEFAULT_PROXY_HOST,
        port: int = DEFAULT_PROXY_PORT,
        task_id: str = "",
        traffic_dir: str | Path | None = None,
        upstream: str = "",
    ) -> dict:
        """Bind the recorder proxy; idempotent while already running.

        Args:
            host: Bind address.
            port: Bind port (0 picks a free one).
            task_id: Task tag stored with each exchange.
            traffic_dir: Recorder directory override.
            upstream: Optional ``[user:pass@]host:port`` proxy to chain.

        Returns:
            Proxy status dict.
        """
        with self._lock:
            if self._server is not None:
                return self.status()
            base_dir = Path(traffic_dir) if traffic_dir else self.traffic_dir
            self._recorder = TrafficRecorder(base_dir)
            self._authority = CertificateAuthority(base_dir / "pki")
            handler = _make_handler()
            server_cls = _server_class()
            self._server = server_cls(
                (host, int(port)),
                handler,
                recorder=self._recorder,
                authority=self._authority,
                task=str(task_id or ""),
                upstream=_parse_upstream(upstream),
            )
            self.host = host
            self.port = int(self._server.server_address[1])
            self.task = str(task_id or "")
            self.upstream = str(upstream or "")
            self.traffic_dir = base_dir
            self._thread = threading.Thread(target=self._server.serve_forever, name="lazy-recorder-proxy", daemon=True)
            self._thread.start()
            return self.status()

    def stop(self) -> dict:
        """Shut the proxy down; safe when it was never started."""
        with self._lock:
            server, thread = self._server, self._thread
            self._server = None
            self._thread = None
        if server is not None:
            try:
                server.shutdown()
                server.server_close()
            except Exception:
                pass
        if thread is not None:
            thread.join(timeout=5.0)
        return self.status()

    def status(self) -> dict:
        """Report running state, address, CA path and exchange count."""
        server = self._server
        exchanges = 0
        if self._recorder is not None:
            try:
                exchanges = self._recorder.count()
            except Exception:
                exchanges = 0
        return {
            "running": server is not None,
            "host": self.host,
            "port": self.port,
            "task": self.task,
            "upstream": self.upstream,
            "traffic_dir": str(self.traffic_dir),
            "ca_path": str(self._authority.cert_path) if self._authority else "",
            "exchanges": exchanges,
            "mitm": True,
            "captures": ["http", "https"],
        }

    def recorder(self) -> TrafficRecorder | None:
        """Return the live recorder for ingestion, or None when stopped."""
        return self._recorder

    def ca_path(self) -> str:
        """Return the CA certificate path for trust-store wiring."""
        return str(self._authority.cert_path) if self._authority else ""


def _make_handler():
    """Build the request handler class bound to the recorder server."""
    from http.server import BaseHTTPRequestHandler

    class ProxyHandler(BaseHTTPRequestHandler):
        """Forwards and records HTTP and MITM'd HTTPS exchanges."""

        protocol_version = "HTTP/1.1"
        server_version = "LazyOwnRecorder/1.0"

        def log_message(self, fmt, *args):  # noqa: ANN002, ANN003
            """Silence per-request logging; the recorder is the audit trail."""
            return None

        def do_CONNECT(self):  # noqa: N802 - stdlib naming
            """Terminate TLS for a CONNECT tunnel and record inner requests."""
            host, _, port_text = (self.path or "").partition(":")
            host = host.strip().strip("[]")
            if not host:
                self._safe_send_error(400, "CONNECT host required")
                return
            try:
                port = int(port_text or 443)
            except ValueError:
                port = 443
            try:
                host, pinned = resolve_validated_target(host, port, "https")
                port = int(port)
            except ValueError:
                self._safe_send_error(403, "proxy target denied")
                return
            try:
                probe = _dial_pinned(pinned, port, timeout=UPSTREAM_TIMEOUT_SEC)
                probe.close()
            except (OSError, ValueError):
                self._safe_send_error(502, "upstream unreachable")
                return
            try:
                context = self.server.authority.context_for(host)
                self.send_response(200, "Connection established")
                self.end_headers()
                tls = context.wrap_socket(self.connection, server_side=True)
            except Exception:
                self.close_connection = True
                return
            self.connection = tls
            self.request = tls
            self.rfile = tls.makefile("rb", self.rbufsize)
            self.wfile = tls.makefile("wb", self.wbufsize)
            self._mitm_host = host
            self._mitm_port = port
            self.close_connection = False
            for _ in range(MAX_TUNNEL_REQUESTS):
                try:
                    self.handle_one_request()
                except (OSError, ssl.SSLError):
                    break
                if self.close_connection:
                    break

        def _safe_send_error(self, code: int, message: str = "") -> None:
            """Send an HTTP error; a gone client is never an exception."""
            try:
                self.send_error(code, message)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                self.close_connection = True

        def do_GET(self):  # noqa: N802 - stdlib naming
            """Forward every plain HTTP method through one path."""
            self._forward_plain()

        do_POST = do_GET
        do_PUT = do_GET
        do_DELETE = do_GET
        do_PATCH = do_GET
        do_HEAD = do_GET
        do_OPTIONS = do_GET

        def _forward_plain(self) -> None:
            """Forward an absolute-URI or origin-form request and record it."""
            scheme = "https" if getattr(self, "_mitm_host", "") else "http"
            if scheme == "https":
                host = self._mitm_host
                port = self._mitm_port
                path = self.path or "/"
                url = f"https://{host}{path}" if port == 443 else f"https://{host}:{port}{path}"
            else:
                url = self.path or ""
                if not url.lower().startswith("http://"):
                    self._safe_send_error(400, "absolute URL required")
                    return
                parts = urlsplit(url)
                if parts.username or parts.password:
                    self._safe_send_error(400, "userinfo in URL denied")
                    return
                host = parts.hostname or ""
                try:
                    port = parts.port or 80
                except ValueError:
                    self._safe_send_error(400, "invalid port")
                    return
                path = parts.path or "/"
                if parts.query:
                    path += f"?{parts.query}"
            if not host:
                self._safe_send_error(400, "host required")
                return
            try:
                host, port = _validate_proxy_target(host, port, scheme)
            except ValueError:
                self._safe_send_error(403, "proxy target denied")
                return
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                length = 0
            length = max(0, min(length, MAX_BODY_BYTES))
            body = self.rfile.read(length) if length else b""
            req_headers = {key: value for key, value in self.headers.items() if key.lower() not in HOP_BY_HOP}
            req_headers.setdefault("Host", host if port in (80, 443) else f"{host}:{port}")
            if "websocket" in str(self.headers.get("Upgrade", "")).lower():
                ws_headers = {
                    key: value
                    for key, value in self.headers.items()
                    if key.lower() not in ("proxy-connection", "proxy-authorization")
                }
                ws_headers.setdefault("Host", host if port in (80, 443) else f"{host}:{port}")
                self._handle_websocket(scheme, host, port, path, url, ws_headers)
                return
            status, reason, resp_headers, resp_body, error = self._relay(
                scheme, host, port, path, url, req_headers, body
            )
            content_type = next((v for k, v in resp_headers if k.lower() == "content-type"), "")
            self._record(
                scheme, host, port, url, status, req_headers, resp_headers, body, resp_body, content_type, error
            )
            if error:
                self._safe_send_error(502, "proxy upstream failure")
            else:
                try:
                    self.send_response(status, reason or "")
                    for key, value in resp_headers:
                        if key.lower() in HOP_BY_HOP or key.lower() == "content-length":
                            continue
                        self.send_header(key, value)
                    self.send_header("Content-Length", str(len(resp_body)))
                    self.end_headers()
                    if self.command != "HEAD":
                        self.wfile.write(resp_body)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                    self.close_connection = True

        def _relay(self, scheme, host, port, path, url, headers, body):
            """Send one request upstream (direct or chained); return response."""
            try:
                host, pinned = resolve_validated_target(host, port, scheme)
                port = int(port)
            except ValueError as exc:
                log.warning("proxy relay denied for %r: %s", url, exc)
                return 0, "", [], b"", "proxy target denied"
            try:
                _validate_upstream_path(path)
            except ValueError as exc:
                log.warning("proxy relay denied for %r: %s", url, exc)
                return 0, "", [], b"", "proxy target denied"
            upstream = dict(getattr(self.server, "upstream", {}) or {})
            try:
                if upstream:
                    auth = _upstream_auth_header(upstream.get("auth", ""))
                    if scheme == "https":
                        try:
                            conn = _https_connection(
                                upstream["host"], upstream["port"], timeout=UPSTREAM_TIMEOUT_SEC
                            )
                            conn.set_tunnel(host, port, headers=auth)
                            conn.request(self.command, path, body=body, headers=headers)
                        except ssl.SSLCertVerificationError:
                            if not tls_lab_unverified_allowed(str(upstream.get("host", ""))):
                                raise
                            log.warning(
                                "unverified fallback for lab upstream %r (self-signed, operator opt-in)",
                                upstream.get("host", ""),
                            )
                            conn = http.client.HTTPSConnection(
                                upstream["host"],
                                upstream["port"],
                                timeout=UPSTREAM_TIMEOUT_SEC,
                                context=_hardened_lab_fallback_context(),
                            )
                            conn.set_tunnel(host, port, headers=auth)
                            conn.request(self.command, path, body=body, headers=headers)
                    else:
                        conn = http.client.HTTPConnection(
                            upstream["host"], upstream["port"], timeout=UPSTREAM_TIMEOUT_SEC
                        )
                        conn.request(self.command, url, body=body, headers={**headers, **auth})
                elif scheme == "https":
                    try:
                        conn = _PinnedHTTPSConnection(
                            host,
                            port,
                            pinned_ips=pinned,
                            timeout=UPSTREAM_TIMEOUT_SEC,
                            context=_upstream_tls_context(host),
                        )
                        conn.request(self.command, path, body=body, headers=headers)
                    except ssl.SSLCertVerificationError:
                        if not tls_lab_unverified_allowed(host):
                            raise
                        log.warning(
                            "unverified fallback for lab target %r (self-signed, operator opt-in)", host
                        )
                        conn = _PinnedHTTPSConnection(
                            host,
                            port,
                            pinned_ips=pinned,
                            timeout=UPSTREAM_TIMEOUT_SEC,
                            context=_hardened_lab_fallback_context(),
                        )
                        conn.request(self.command, path, body=body, headers=headers)
                else:
                    conn = _PinnedHTTPConnection(
                        host, port, pinned_ips=pinned, timeout=UPSTREAM_TIMEOUT_SEC
                    )
                    conn.request(self.command, path, body=body, headers=headers)
                response = conn.getresponse()
                payload = response.read(MAX_BODY_BYTES + 1)
                truncated = len(payload) > MAX_BODY_BYTES
                payload = payload[:MAX_BODY_BYTES]
                resp_headers = list(response.getheaders())
                if truncated:
                    resp_headers.append(("X-Lazy-Truncated", "1"))
                conn.close()
                return response.status, response.reason, resp_headers, payload, ""
            except ssl.SSLCertVerificationError as exc:
                if _is_lab_host(host):
                    log.warning(
                        "upstream TLS verification failed for lab target %r; "
                        "set LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1 or LAZY_PROXY_TRUST_CA",
                        host,
                    )
                    hint = (
                        " (lab self-signed: set LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1"
                        " or LAZY_PROXY_TRUST_CA)"
                    )
                    return 0, "", [], b"", (str(exc) + hint)[:300]
                return 0, "", [], b"", str(exc)[:300]
            except Exception as exc:
                return 0, "", [], b"", str(exc)[:300]

        def _open_target(self, scheme, host, port):
            """Open a raw upstream connection, chaining through the proxy."""
            host, pinned = resolve_validated_target(host, port, scheme)
            port = int(port)
            upstream = dict(getattr(self.server, "upstream", {}) or {})
            if upstream:
                sock = socket.create_connection((upstream["host"], upstream["port"]), timeout=UPSTREAM_TIMEOUT_SEC)
                if scheme == "https":
                    auth = _upstream_auth_header(upstream.get("auth", ""))
                    lines = [f"CONNECT {host}:{port} HTTP/1.1", f"Host: {host}:{port}"]
                    for key, value in auth.items():
                        lines.append(f"{key}: {value}")
                    sock.sendall(("\r\n".join(lines) + "\r\n\r\n").encode())
                    head = self._read_headers_from(sock)
                    if b" 200 " not in head.split(b"\r\n", 1)[0]:
                        sock.close()
                        raise OSError("upstream CONNECT refused")
                return self._maybe_tls(sock, scheme, host)
            sock = _dial_pinned(pinned, port, timeout=UPSTREAM_TIMEOUT_SEC)
            return self._maybe_tls(sock, scheme, host)

        @staticmethod
        def _maybe_tls(sock, scheme, host):
            """Wrap a socket in TLS for https targets with verification."""
            if scheme != "https":
                return sock
            try:
                return _upstream_tls_context(host).wrap_socket(sock, server_hostname=host)
            except ssl.SSLCertVerificationError as exc:
                if not tls_lab_unverified_allowed(host):
                    raise OSError(
                        f"upstream TLS verification failed for lab target {host!r} "
                        "(set LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1 or LAZY_PROXY_TRUST_CA)"
                    ) from exc
                log.warning("unverified TLS fallback for lab target %r (self-signed, operator opt-in)", host)
                return _hardened_lab_fallback_context().wrap_socket(sock, server_hostname=host)

        @staticmethod
        def _read_headers_from(sock, limit: int = 65536) -> bytes:
            """Read bytes until the HTTP header terminator."""
            data = b""
            while b"\r\n\r\n" not in data and len(data) < limit:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
            return data

        def _handle_websocket(self, scheme, host, port, path, url, req_headers) -> None:
            """Pass a WebSocket upgrade through, recording the handshake."""
            try:
                upstream = self._open_target(scheme, host, port)
            except Exception as exc:
                self._record(
                    scheme,
                    host,
                    port,
                    url,
                    0,
                    req_headers,
                    [],
                    b"",
                    b"",
                    "websocket",
                    f"ws connect failed: {exc}"[:300],
                )
                self._safe_send_error(502, "websocket upstream failure")
                return
            try:
                head = (
                    f"{self.command} {path} HTTP/1.1\r\n"
                    + "".join(f"{key}: {value}\r\n" for key, value in req_headers.items())
                    + "\r\n"
                )
                upstream.sendall(head.encode("latin-1", "replace"))
                response = self._read_headers_from(upstream)
                first_line = response.split(b"\r\n", 1)[0].decode("latin-1", "replace")
                try:
                    status = int(first_line.split(" ")[1])
                except (IndexError, ValueError):
                    status = 0
                resp_headers = [
                    tuple(line.split(": ", 1))
                    for line in response.decode("latin-1", "replace").split("\r\n")[1:]
                    if ": " in line
                ]
                self._record(
                    scheme,
                    host,
                    port,
                    url,
                    status,
                    req_headers,
                    resp_headers,
                    b"",
                    b"",
                    "websocket",
                    "websocket tunnel",
                )
                self.wfile.write(response)
                self.wfile.flush()
                if status != 101:
                    self.close_connection = True
                    upstream.close()
                    return
                leftover = response.split(b"\r\n\r\n", 1)[1]
                if leftover:
                    upstream.sendall(leftover)
                while True:
                    readable, _, _ = select.select([self.connection, upstream], [], [], 60)
                    for source in readable:
                        try:
                            chunk = source.recv(65536)
                        except OSError:
                            chunk = b""
                        if not chunk:
                            self.close_connection = True
                            upstream.close()
                            return
                        target = upstream if source is self.connection else self.connection
                        try:
                            target.sendall(chunk)
                        except OSError:
                            self.close_connection = True
                            upstream.close()
                            return
            except Exception:
                self.close_connection = True
                try:
                    upstream.close()
                except Exception:
                    pass

        def _record(
            self, scheme, host, port, url, status, req_headers, resp_headers, req_body, resp_body, content_type, error
        ) -> None:
            """Persist one exchange; recorder failures never break proxying."""
            try:
                self.server.recorder.record(
                    self.command,
                    url,
                    status,
                    req_body,
                    resp_body,
                    content_type,
                    req_headers,
                    dict(resp_headers),
                    host=host,
                    port=port,
                    scheme=scheme,
                    task=getattr(self.server, "task", ""),
                    note=error,
                )
            except Exception:
                pass

    return ProxyHandler


_CONTROLLER: ProxyController | None = None
_CONTROLLER_LOCK = threading.Lock()

PROXY_ENV_KEYS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "SSL_CERT_FILE",
    "GIT_SSL_CAINFO",
    "NODE_EXTRA_CA_CERTS",
)


def get_proxy() -> ProxyController:
    """Return the process-wide recorder proxy controller."""
    global _CONTROLLER
    with _CONTROLLER_LOCK:
        if _CONTROLLER is None:
            _CONTROLLER = ProxyController()
        return _CONTROLLER


def env_for_ca(ca_path: str, host: str = DEFAULT_PROXY_HOST, port: int = DEFAULT_PROXY_PORT) -> dict:
    """Build the environment overrides that route tools through the proxy."""
    url = f"http://{host}:{port}"
    return {
        "HTTP_PROXY": url,
        "HTTPS_PROXY": url,
        "http_proxy": url,
        "https_proxy": url,
        "REQUESTS_CA_BUNDLE": ca_path,
        "CURL_CA_BUNDLE": ca_path,
        "SSL_CERT_FILE": ca_path,
        "GIT_SSL_CAINFO": ca_path,
        "NODE_EXTRA_CA_CERTS": ca_path,
    }


def apply_env(ca_path: str, host: str = DEFAULT_PROXY_HOST, port: int = DEFAULT_PROXY_PORT) -> dict:
    """Apply proxy env vars, returning the previous values for restore."""
    previous = {key: os.environ.get(key) for key in PROXY_ENV_KEYS}
    os.environ.update(env_for_ca(ca_path, host, port))
    return previous


def restore_env(previous: dict) -> None:
    """Restore environment values captured by :func:`apply_env`."""
    for key, value in (previous or {}).items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


__all__ = [
    "CA_CERT_NAME",
    "DEFAULT_PROXY_HOST",
    "DEFAULT_PROXY_PORT",
    "CertificateAuthority",
    "NSS_NICKNAME",
    "ProxyController",
    "TRUST_ANCHOR_NAME",
    "_validate_proxy_target",
    "resolve_validated_target",
    "connect_pinned",
    "tls_lab_unverified_allowed",
    "_upstream_tls_context",
    "_is_lab_host",
    "apply_env",
    "ca_trusted",
    "detect_nss_profiles",
    "detect_trust_target",
    "env_for_ca",
    "get_proxy",
    "install_ca_nss",
    "install_ca_trust",
    "restore_env",
]
