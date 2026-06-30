"""Declarative schema and validation for ``payload.json``.

``payload.json`` is the single source of runtime configuration for every
component of LazyOwn (CLI, C2, MCP, autonomous daemon). Historically it has
been a free-form dictionary: any key/value was accepted at load time, and
each consumer rediscovered the right type with ad-hoc casts. Typos in keys
silently degraded features instead of surfacing as errors, and string
values that needed to be integers (``"5555"`` vs ``5555``) caused failures
deep inside subprocess calls.

This module introduces a thin, additive validation layer:

* :class:`FieldSpec` declares the expected type, default, and human-readable
  documentation for every well-known payload key.
* :func:`validate_value` checks a single value against its spec.
* :func:`validate_payload` returns the full list of issues without raising,
  so backwards compatibility is preserved — callers decide whether to warn
  or block.
* :func:`coerce_value` performs safe, well-defined coercions (e.g. parsing
  ``"5555"`` into ``5555`` when the field is declared as an integer port).

The schema is the source of truth for the setup wizard as well — every
prompt label, default, validator and example value comes from here so a
new field is defined in exactly one place.

Design rules:

- Adding a new well-known key means adding a :class:`FieldSpec` here; no
  other module needs to change to surface the documentation.
- Validation is intentionally non-fatal: unknown keys are warnings (so
  operator-private extensions keep working), and bad values are warnings
  by default. Callers that need hard failures (e.g. the wizard) inspect
  :class:`ValidationIssue.severity`.
- No external dependencies. Pydantic et al. would impose an install
  burden that would break ``./run`` on fresh boxes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, Mapping

IPV4_REGEX = re.compile(r"\A((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)\Z")
INTERFACE_REGEX = re.compile(r"\A[A-Za-z0-9._@:-]{1,32}\Z")
HOSTNAME_REGEX = re.compile(
    r"\A(?=.{1,253}\Z)"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*"
    r"\.?\Z"
)
URL_REGEX = re.compile(r"\Ahttps?://[\w\-.:/?#\[\]@!$&'()*+,;=%]+\Z")
HEX_REGEX = re.compile(r"\A[0-9a-fA-F]+\Z")
PORT_MIN = 1
PORT_MAX = 65535


class FieldKind(str, Enum):
    """Categorical type of a payload field used by validators and the wizard."""

    STRING = "string"
    INT = "int"
    PORT = "port"
    BOOL = "bool"
    IP = "ip"
    HOSTNAME = "hostname"
    URL = "url"
    PATH = "path"
    INTERFACE = "interface"
    HEX = "hex"
    OS_ID = "os_id"
    JSON_BLOB = "json_blob"
    OPAQUE = "opaque"


class Severity(str, Enum):
    """Severity of a :class:`ValidationIssue`."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class FieldSpec:
    """Declarative description of a payload field.

    Attributes:
        name: Key as it appears in ``payload.json``.
        kind: Categorical :class:`FieldKind` controlling validation and
            coercion behaviour.
        default: Value used when bootstrapping a brand new payload.
        description: One-line plain-language explanation suitable for
            help text and wizard tooltips.
        long_help: Multi-line explanation used by the wizard's tutorial
            mode. Newlines are preserved verbatim.
        example: Concrete example value shown to novices.
        category: Logical grouping (``network``, ``c2``, ``recon``, ``ai``,
            ``credentials``, ``wordlists``, ``email``, ``misc``).
        sensitive: When ``True`` the wizard masks the value in summaries.
        required: When ``True`` an empty/missing value is reported as an
            error rather than a warning.
        allowed: Optional whitelist of acceptable values for enum-like fields.
        min_value: Optional inclusive lower bound for numeric fields.
        max_value: Optional inclusive upper bound for numeric fields.
        custom_validator: Optional callable returning ``None`` when the
            value is valid or a string message when it is not. Runs after
            the kind-based validator.
    """

    name: str
    kind: FieldKind
    default: Any
    description: str
    long_help: str = ""
    example: str = ""
    category: str = "misc"
    sensitive: bool = False
    required: bool = False
    allowed: tuple[Any, ...] | None = None
    min_value: int | None = None
    max_value: int | None = None
    custom_validator: Callable[[Any], str | None] | None = None


@dataclass(frozen=True)
class ValidationIssue:
    """Structured outcome of a single validation check.

    Issues are returned as a list so consumers can render them as a table,
    emit a single warning, or short-circuit on the first error. The
    :attr:`severity` field makes it explicit which issues are advisory and
    which must be addressed before the value can be used.

    Attributes:
        key: Name of the offending field.
        message: Human-readable explanation of the problem.
        severity: One of :class:`Severity`. Callers should treat warnings
            as advisory and errors as blocking.
        value: The raw value that produced the issue. Sensitive fields are
            masked by :func:`format_issue` so logs do not leak credentials.
    """

    key: str
    message: str
    severity: Severity = Severity.WARNING
    value: Any = None


def _validate_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return f"expected string, got {type(value).__name__}"
    return None


def _validate_int(value: Any) -> str | None:
    if isinstance(value, bool):
        return "expected int, got bool"
    if isinstance(value, int):
        return None
    if isinstance(value, str):
        try:
            int(value, 10)
        except ValueError:
            return f"expected integer, got non-numeric string {value!r}"
        return None
    return f"expected int, got {type(value).__name__}"


def _validate_port(value: Any) -> str | None:
    error = _validate_int(value)
    if error:
        return error
    numeric = int(value)
    if not (PORT_MIN <= numeric <= PORT_MAX):
        return f"port must be between {PORT_MIN} and {PORT_MAX}, got {numeric}"
    return None


def _validate_bool(value: Any) -> str | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, str) and value.strip().lower() in {
        "true",
        "false",
        "yes",
        "no",
        "1",
        "0",
        "on",
        "off",
    }:
        return None
    return f"expected boolean-like value, got {value!r}"


def _validate_ip(value: Any) -> str | None:
    if not isinstance(value, str):
        return f"expected IPv4 string, got {type(value).__name__}"
    if not IPV4_REGEX.match(value):
        return f"{value!r} is not a valid IPv4 address"
    return None


def _validate_hostname(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return f"expected non-empty hostname, got {value!r}"
    if value == "localhost":
        return None
    if IPV4_REGEX.match(value):
        return None
    if not HOSTNAME_REGEX.match(value):
        return f"{value!r} is not a valid hostname"
    return None


def _validate_url(value: Any) -> str | None:
    if not isinstance(value, str):
        return f"expected URL string, got {type(value).__name__}"
    if not URL_REGEX.match(value):
        return f"{value!r} is not a well-formed http(s) URL"
    return None


def _validate_path(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return f"expected non-empty filesystem path, got {value!r}"
    return None


def _validate_interface(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return f"expected non-empty interface name, got {value!r}"
    if not INTERFACE_REGEX.match(value):
        return f"{value!r} is not a valid interface name"
    return None


def _validate_hex(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return f"expected hex string, got {value!r}"
    if not HEX_REGEX.match(value):
        return f"{value!r} is not a hex string"
    return None


def _validate_os_id(value: Any) -> str | None:
    if str(value).strip() in {"1", "2"}:
        return None
    return f"os_id must be '1' (Linux) or '2' (Windows), got {value!r}"


def _validate_json_blob(value: Any) -> str | None:
    import json

    if not isinstance(value, str):
        return f"expected JSON string, got {type(value).__name__}"
    try:
        json.loads(value)
    except json.JSONDecodeError as exc:
        return f"value is not valid JSON: {exc.msg}"
    return None


def _validate_opaque(_value: Any) -> str | None:
    return None


_KIND_VALIDATORS: Mapping[FieldKind, Callable[[Any], str | None]] = {
    FieldKind.STRING: _validate_string,
    FieldKind.INT: _validate_int,
    FieldKind.PORT: _validate_port,
    FieldKind.BOOL: _validate_bool,
    FieldKind.IP: _validate_ip,
    FieldKind.HOSTNAME: _validate_hostname,
    FieldKind.URL: _validate_url,
    FieldKind.PATH: _validate_path,
    FieldKind.INTERFACE: _validate_interface,
    FieldKind.HEX: _validate_hex,
    FieldKind.OS_ID: _validate_os_id,
    FieldKind.JSON_BLOB: _validate_json_blob,
    FieldKind.OPAQUE: _validate_opaque,
}


def _coerce_int(raw: Any) -> Any:
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        stripped = raw.strip()
        if stripped and (stripped[0] in "+-" and stripped[1:].isdigit() or stripped.isdigit()):
            try:
                return int(stripped, 10)
            except ValueError:
                return raw
    return raw


def _coerce_bool(raw: Any) -> Any:
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, str):
        lowered = raw.strip().lower()
        if lowered in {"true", "yes", "on", "1"}:
            return True
        if lowered in {"false", "no", "off", "0"}:
            return False
    return raw


_KIND_COERCERS: Mapping[FieldKind, Callable[[Any], Any]] = {
    FieldKind.INT: _coerce_int,
    FieldKind.PORT: _coerce_int,
    FieldKind.BOOL: _coerce_bool,
}


def _spec(
    name: str,
    kind: FieldKind,
    default: Any,
    description: str,
    *,
    long_help: str = "",
    example: str = "",
    category: str = "misc",
    sensitive: bool = False,
    required: bool = False,
    allowed: Iterable[Any] | None = None,
    min_value: int | None = None,
    max_value: int | None = None,
    custom_validator: Callable[[Any], str | None] | None = None,
) -> FieldSpec:
    return FieldSpec(
        name=name,
        kind=kind,
        default=default,
        description=description,
        long_help=long_help.strip(),
        example=example,
        category=category,
        sensitive=sensitive,
        required=required,
        allowed=tuple(allowed) if allowed is not None else None,
        min_value=min_value,
        max_value=max_value,
        custom_validator=custom_validator,
    )


SCHEMA: dict[str, FieldSpec] = {
    spec.name: spec
    for spec in (
        _spec(
            "rhost",
            FieldKind.IP,
            "10.0.0.1",
            "Target IP address (the machine you are testing).",
            long_help=(
                "Every recon, exploit and credential command reads rhost as the "
                "default target. You can override it per-command with --target, "
                "but setting it here once saves a lot of typing. Examples include "
                "HackTheBox addresses like 10.10.11.5 or a local lab 192.168.56.10."
            ),
            example="10.10.11.5",
            category="network",
            required=True,
        ),
        _spec(
            "lhost",
            FieldKind.IP,
            "127.0.0.1",
            "Your attacker IP on the target network (tun0/eth0).",
            long_help=(
                "Used as the listener address for reverse shells, the C2 server "
                "bind address, and as the source IP for some scans. On a VPN "
                "engagement this is your tun0 address; on a local lab it is the "
                "interface that can reach the target."
            ),
            example="10.10.14.20",
            category="network",
            required=True,
        ),
        _spec(
            "rport",
            FieldKind.PORT,
            5555,
            "Default target port (rare; most commands derive it from scans).",
            category="network",
        ),
        _spec(
            "lport",
            FieldKind.PORT,
            5555,
            "Default listener port for reverse shells.",
            example="9001",
            category="network",
        ),
        _spec(
            "listener", FieldKind.PORT, 7777, "Auxiliary listener port (file delivery, ad-hoc nc).", category="network"
        ),
        _spec(
            "reverse_shell_port",
            FieldKind.PORT,
            6666,
            "Default reverse-shell port for payload generators.",
            category="network",
        ),
        _spec("proxy_port", FieldKind.PORT, 8888, "Local HTTP proxy port (Burp/ZAP integration).", category="network"),
        _spec(
            "device",
            FieldKind.INTERFACE,
            "wlan0",
            "Network interface facing the target.",
            example="tun0",
            category="network",
        ),
        _spec(
            "spoof_ip", FieldKind.IP, "185.199.110.153", "Spoofed source IP for decoy/idle scans.", category="network"
        ),
        _spec(
            "startip",
            FieldKind.IP,
            "10.10.11.1",
            "Inclusive lower bound of the network discovery range.",
            category="network",
        ),
        _spec(
            "endip",
            FieldKind.IP,
            "10.10.11.255",
            "Inclusive upper bound of the network discovery range.",
            category="network",
        ),
        _spec(
            "domain",
            FieldKind.HOSTNAME,
            "localhost",
            "Target virtual host / DNS name.",
            long_help=(
                "Needed when the web application uses Host-header routing, when "
                "you are kerberos-roasting against an Active Directory domain, "
                "and by every command that emits HTTP requests."
            ),
            example="target.htb",
            category="network",
        ),
        _spec(
            "subdomain", FieldKind.STRING, "dc01", "Target subdomain (DC name or web subdomain).", category="network"
        ),
        _spec("url", FieldKind.URL, "http://VariaType.htb", "Base URL for HTTP-centric commands.", category="network"),
        _spec(
            "method",
            FieldKind.STRING,
            "POST",
            "Default HTTP verb for crafted requests.",
            allowed=("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"),
            category="network",
        ),
        _spec(
            "headers",
            FieldKind.JSON_BLOB,
            '{"Content-Type": "application/json"}',
            "Default request headers (JSON string).",
            category="network",
        ),
        _spec(
            "params",
            FieldKind.JSON_BLOB,
            '{"param1": "LAZYFUZZ"}',
            "Default query-string params (JSON string).",
            category="network",
        ),
        _spec(
            "data",
            FieldKind.JSON_BLOB,
            '{"key": "LAZYFUZZ"}',
            "Default form-encoded body (JSON string).",
            category="network",
        ),
        _spec(
            "json_data",
            FieldKind.JSON_BLOB,
            '{"json_key": "json_value"}',
            "Default JSON request body (JSON string).",
            category="network",
        ),
        _spec(
            "headers_file", FieldKind.PATH, "modules/headers.json", "Optional headers payload file.", category="network"
        ),
        _spec("data_file", FieldKind.PATH, "modules/data.json", "Optional body payload file.", category="network"),
        _spec(
            "params_file", FieldKind.PATH, "modules/params.json", "Optional params payload file.", category="network"
        ),
        _spec(
            "json_data_file",
            FieldKind.PATH,
            "modules/json_data.json",
            "Optional JSON body payload file.",
            category="network",
        ),
        _spec(
            "hide_code",
            FieldKind.INT,
            404,
            "HTTP status code to hide in fuzzing output.",
            min_value=100,
            max_value=599,
            category="network",
        ),
        _spec("field", FieldKind.STRING, "page", "Default form field name for fuzzers.", category="network"),
        _spec(
            "os_id",
            FieldKind.OS_ID,
            "1",
            "Target operating system: 1 = Linux, 2 = Windows.",
            long_help=(
                "Drives which post-exploitation tools the framework suggests. "
                "Set automatically by `ping` based on TTL; you only need to set "
                "it manually if you are skipping the ping step."
            ),
            example="1",
            allowed=("1", "2"),
            category="recon",
            required=True,
        ),
        _spec(
            "c2_port",
            FieldKind.PORT,
            4444,
            "TCP port the C2 listener binds to.",
            example="4444",
            category="c2",
        ),
        _spec(
            "c2_user",
            FieldKind.STRING,
            "LazyOwn",
            "C2 operator username (HTTP basic auth).",
            category="c2",
            sensitive=True,
        ),
        _spec(
            "c2_pass",
            FieldKind.STRING,
            "LazyOwn",
            "C2 operator password (HTTP basic auth).",
            category="c2",
            sensitive=True,
        ),
        _spec(
            "c2_maleable_route",
            FieldKind.STRING,
            "/pleasesubscribe/v1/users/",
            "URI prefix used by beacons when polling the C2 server.",
            long_help=(
                "Beacons append a per-host id to this prefix. Change it to "
                "match a malleable profile if you need to blend into a "
                "specific environment's traffic."
            ),
            example="/api/v2/sessions/",
            category="c2",
        ),
        _spec("user_agent_win", FieldKind.STRING, "", "User-Agent string for Windows beacons.", category="c2"),
        _spec("user_agent_lin", FieldKind.STRING, "", "User-Agent string for Linux beacons.", category="c2"),
        _spec("user_agent_1", FieldKind.STRING, "", "Decoy User-Agent slot 1.", category="c2"),
        _spec("user_agent_2", FieldKind.STRING, "", "Decoy User-Agent slot 2.", category="c2"),
        _spec("user_agent_3", FieldKind.STRING, "", "Decoy User-Agent slot 3.", category="c2"),
        _spec("url_trafic_1", FieldKind.URL, "https://www.youtube.com", "Decoy traffic URL slot 1.", category="c2"),
        _spec("url_trafic_2", FieldKind.URL, "https://www.youtube.com", "Decoy traffic URL slot 2.", category="c2"),
        _spec("url_trafic_3", FieldKind.URL, "https://www.youtube.com", "Decoy traffic URL slot 3.", category="c2"),
        _spec(
            "sleep",
            FieldKind.INT,
            6,
            "Seconds between beacon check-ins.",
            min_value=1,
            max_value=3600,
            category="c2",
        ),
        _spec(
            "sleep_start",
            FieldKind.INT,
            333,
            "Seconds the autonomous loop waits before its first action.",
            long_help=(
                "Gives the C2 listener and scanners time to boot before the "
                "autonomous loop fires its first recommendation. Lowering this "
                "below 60 may cause the daemon to act before nmap returns."
            ),
            min_value=10,
            max_value=86400,
            category="c2",
        ),
        _spec(
            "rat_key",
            FieldKind.HEX,
            "82e672ae054aa4de6f042c888111686a",
            "XOR key used by the Go beacon stub.",
            category="c2",
            sensitive=True,
        ),
        _spec("enable_c2_implant_debug", FieldKind.BOOL, "True", "Verbose beacon logging.", category="c2"),
        _spec(
            "enable_cloudflare", FieldKind.BOOL, False, "Route C2 traffic through Cloudflare redirector.", category="c2"
        ),
        _spec("binary_name", FieldKind.STRING, "curl", "Stub binary name produced by build helpers.", category="c2"),
        _spec(
            "aes_key",
            FieldKind.HEX,
            "",
            "AES-256 key used to encrypt C2 traffic and beacon payloads.",
            long_help=(
                "Must be exactly 64 hex characters (32 bytes after decode). "
                "When empty, the framework loads or generates one under "
                "sessions/key.aes. The resolved value is exposed as "
                "self.params['aes_key'] and self.aes_key for use throughout "
                "the framework (CLI, C2, MCP, and lazyaddons via {{aes_key}} "
                "template substitution)."
            ),
            example="82e672ae054aa4de6f042c888111686a82e672ae054aa4de6f042c888111686a",
            category="c2",
            sensitive=True,
            min_value=0,
            max_value=0,
            custom_validator=lambda v: (
                None
                if (
                    isinstance(v, str)
                    and (v == "" or (len(v) == 64 and all(c in "0123456789abcdefABCDEF" for c in v)))
                )
                else "aes_key must be 64 hex characters (32 bytes) or empty"
            ),
        ),
        _spec(
            "c2_allowed_origins",
            FieldKind.STRING,
            "",
            "Comma-separated list of origins allowed to talk to the C2 web layer.",
            long_help=(
                "In PROD, the C2 web layer refuses to start when this is empty. "
                "In DEV, the framework falls back to https://{lhost}. The "
                "wildcard '*' is never accepted; the token is dropped from "
                "any CSV value before resolution."
            ),
            example="https://c2.example,https://ops.example",
            category="c2",
        ),
        _spec(
            "c2_csrf_enabled",
            FieldKind.BOOL,
            "True",
            "Require a CSRF token on every mutating operator request.",
            category="c2",
        ),
        _spec(
            "c2_register_limit",
            FieldKind.STRING,
            "5 per minute",
            "Flask-Limiter rate applied to the /register endpoint.",
            category="c2",
        ),
        _spec(
            "c2_api_command_allowlist",
            FieldKind.STRING,
            "ping,set,show,help,status,sessions,sitrep,gets,get,downloader,getosession,osession,setar,getar,session,clean",
            "Comma-separated first-token allowlist for /api/run.",
            long_help=(
                "Every command reaching the LazyOwn shell through /api/run "
                "must start with one of these tokens; shell metacharacters "
                "are always rejected regardless of the allowlist."
            ),
            example="ping,set,show,status",
            category="c2",
        ),
        _spec(
            "c2_trusted_proxy_count",
            FieldKind.INT,
            0,
            "Number of trusted reverse proxies in front of the C2.",
            long_help=(
                "When greater than zero, the C2 parses X-Forwarded-For "
                "right-to-left and skips this many hops before trusting the "
                "leftmost address. Zero disables header parsing entirely."
            ),
            min_value=0,
            max_value=8,
            category="c2",
        ),
        _spec(
            "c2_operator_ip_allowlist",
            FieldKind.STRING,
            "127.0.0.1",
            "Comma-separated IPs allowed to access operator-only routes.",
            category="c2",
        ),
        _spec(
            "c2_reverse_shell_password",
            FieldKind.STRING,
            "",
            "Password required to trigger the /lazyos reverse shell.",
            long_help=(
                "Must be at least 12 characters when set. When empty, the "
                "framework logs a WARNING and falls back to the legacy "
                "string 'grisiscomebacksayknokknok' for backwards "
                "compatibility. Set this in payload.json to silence the "
                "warning and replace the legacy hardcoded value."
            ),
            example="please-change-me-12+chars",
            category="c2",
            sensitive=True,
        ),
        _spec(
            "c2_max_upload_size_mb",
            FieldKind.INT,
            10,
            "Maximum upload size in megabytes enforced by the C2 web layer.",
            min_value=1,
            max_value=1024,
            category="c2",
        ),
        _spec(
            "c2_https_redirect",
            FieldKind.BOOL,
            "True",
            "Force HTTP -> HTTPS redirect in PROD (no-op in DEV).",
            category="c2",
        ),
        _spec(
            "api_key",
            FieldKind.STRING,
            "your_api_key_here",
            "Groq API key (free tier available at console.groq.com).",
            long_help=(
                "Enables AI-powered command suggestions, the phishing copy "
                "generator, and the vulnerability analyst. The framework "
                "degrades gracefully when missing — only AI features turn off."
            ),
            example="gsk_********************************",
            category="ai",
            sensitive=True,
        ),
        _spec(
            "prompt",
            FieldKind.STRING,
            "Presentate como Lazy OWN OneLiner assistant",
            "Default system prompt for the LLM agents.",
            category="ai",
        ),
        _spec(
            "wordlist",
            FieldKind.PATH,
            "/usr/share/wordlists/rockyou.txt",
            "Primary password wordlist.",
            example="/usr/share/wordlists/rockyou.txt",
            category="wordlists",
        ),
        _spec(
            "dirwordlist",
            FieldKind.PATH,
            "/usr/share/wordlists/SecLists-master/Discovery/Web-Content/directory-list-2.3-medium.txt",
            "Directory brute-force wordlist (gobuster/ffuf/feroxbuster).",
            category="wordlists",
        ),
        _spec(
            "usrwordlist",
            FieldKind.PATH,
            "/usr/share/wordlists/SecLists-master/Usernames/xato-net-10-million-usernames.txt",
            "Username brute-force wordlist.",
            category="wordlists",
        ),
        _spec(
            "dnswordlist",
            FieldKind.PATH,
            "/usr/share/wordlists/SecLists-master/Discovery/DNS/subdomains-top1million-110000.txt",
            "DNS subdomain enumeration wordlist.",
            category="wordlists",
        ),
        _spec("iiswordlist", FieldKind.PATH, "", "IIS-specific content discovery wordlist.", category="wordlists"),
        _spec(
            "exploitdb",
            FieldKind.PATH,
            "/usr/share/exploitdb/exploits/",
            "Local Exploit-DB exploits/ root.",
            category="recon",
        ),
        _spec(
            "start_user",
            FieldKind.STRING,
            "",
            "Initial username discovered against the target.",
            long_help=(
                "Auto-populated by the credentials engine when the first "
                "valid login is found. You can also set it manually if you "
                "already have credentials from the brief."
            ),
            example="alice",
            category="credentials",
            sensitive=True,
        ),
        _spec(
            "start_pass",
            FieldKind.STRING,
            "",
            "Initial password matching start_user.",
            category="credentials",
            sensitive=True,
        ),
        _spec(
            "file",
            FieldKind.STRING,
            "file_to_operate.ext",
            "Default file name used by file-centric commands.",
            category="misc",
        ),
        _spec("path", FieldKind.STRING, "/home/$USER", "Default working path used by some templates.", category="misc"),
        _spec(
            "mode",
            FieldKind.STRING,
            "attack",
            "Framework mode (informational; tools may read this).",
            allowed=("attack", "defense", "audit", "ctf"),
            category="misc",
        ),
        _spec(
            "email_from",
            FieldKind.STRING,
            "",
            "Default From: address for phishing campaigns.",
            category="email",
            sensitive=True,
        ),
        _spec(
            "email_to",
            FieldKind.STRING,
            "",
            "Default recipient for testing phishing campaigns.",
            category="email",
            sensitive=True,
        ),
        _spec("email_username", FieldKind.STRING, "", "SMTP username.", category="email", sensitive=True),
        _spec("email_password", FieldKind.STRING, "", "SMTP password.", category="email", sensitive=True),
        _spec("smtp_server", FieldKind.HOSTNAME, "smtp.gmail.com", "SMTP server hostname.", category="email"),
        _spec("smtp_port", FieldKind.PORT, 587, "SMTP server port.", category="email"),
        _spec(
            "enable_toasts",
            FieldKind.BOOL,
            True,
            "Render unseen events from sessions/*.jsonl as dim toast lines after each command.",
            long_help=(
                "Toasts are non-blocking and replay only events emitted since the previous prompt. "
                "Disable when running scripted batches where additional output noise is unwanted."
            ),
            category="misc",
        ),
        _spec(
            "toast_max_per_tick",
            FieldKind.INT,
            5,
            "Maximum number of toast lines shown per command.",
            min_value=1,
            max_value=50,
            category="misc",
        ),
        _spec(
            "reactive_semantic_enabled",
            FieldKind.BOOL,
            True,
            "Allow reactive_engine to emit semantic suggestions from SessionRAG.",
            long_help=(
                "When enabled, the reactive engine queries the SessionRAG index "
                "(ChromaDB or keyword fallback) for past sessions whose output "
                "resembles the current one and emits a priority-5 suggest_next "
                "decision pointing at the originating command. Regex-based "
                "matchers always outrank these hints; disable to keep the "
                "engine strictly rule-driven."
            ),
            category="misc",
        ),
        _spec(
            "enable_operator_presence",
            FieldKind.BOOL,
            False,
            "Show the count of active collaboration operators in the status bar.",
            long_help=(
                "Reads sessions/operators.json (written by collab_bp) and appends ops:<n> to the status line. "
                "Disabled by default so single-operator sessions keep the current bar format."
            ),
            category="c2",
        ),
        _spec(
            "tui_theme",
            FieldKind.STRING,
            "default",
            "Colour theme for the TUI overlays (default, dim, bright, colorblind).",
            allowed=("default", "dim", "bright", "colorblind"),
            category="misc",
        ),
        _spec(
            "scope",
            FieldKind.OPAQUE,
            [],
            "Authorized engagement scope as a list of CIDR/IP/hostname entries.",
            long_help=(
                "The scope guard blocks (in enforce mode) or warns (in warn mode) "
                "when an offensive command targets a host outside this list. "
                "Entries may be CIDR networks (10.10.11.0/24), bare addresses "
                "(10.10.11.5) or hostnames (corp.local, *.corp.local). An empty "
                "scope disables the guard, so existing campaigns are unaffected "
                "until a scope is defined. Manage it with the scope command."
            ),
            example='["10.10.11.0/24", "dc.corp.local"]',
            category="security",
        ),
        _spec(
            "scope_enforcement",
            FieldKind.STRING,
            "warn",
            "Scope guard posture: off (disabled), warn (annotate), enforce (block).",
            long_help=(
                "off disables the guard entirely. warn allows out-of-scope "
                "offensive commands but prints a warning. enforce blocks them "
                "pending interactive confirmation; in non-interactive sessions "
                "enforce blocks outright. The guard only ever acts when a scope "
                "is defined, so warn is a safe default."
            ),
            allowed=("off", "warn", "enforce"),
            category="security",
        ),
    )
}


def field_for(key: str) -> FieldSpec | None:
    """Return the :class:`FieldSpec` for ``key`` or ``None`` if it is unknown."""
    return SCHEMA.get(key)


def coerce_value(key: str, raw: Any) -> Any:
    """Return ``raw`` coerced to the canonical type declared for ``key``.

    Unknown keys and values that already satisfy the schema are returned
    unchanged. Coercion is intentionally narrow: only ``int``/``port`` and
    boolean-like strings are converted. This keeps the function safe for
    use inside the ``assign`` command without surprising operators.

    Args:
        key: Payload key as written in ``payload.json``.
        raw: Value about to be assigned.

    Returns:
        The coerced value, or ``raw`` unchanged when no coercion is
        defined for the field's kind.
    """
    spec = SCHEMA.get(key)
    if spec is None:
        return raw
    coercer = _KIND_COERCERS.get(spec.kind)
    return coercer(raw) if coercer is not None else raw


def validate_value(key: str, value: Any) -> ValidationIssue | None:
    """Validate ``value`` against the schema entry for ``key``.

    Returns:
        ``None`` when the value is acceptable; otherwise a
        :class:`ValidationIssue` whose severity is ``ERROR`` when the
        field is declared as required and either missing or invalid, and
        ``WARNING`` for soft constraints (out-of-range integers, bad
        format on optional fields). Unknown keys produce a warning so the
        caller knows the value will not be type-checked.
    """
    spec = SCHEMA.get(key)
    if spec is None:
        return ValidationIssue(
            key=key,
            message=f"{key!r} is not a known payload key; value will not be validated",
            severity=Severity.INFO,
            value=value,
        )

    if value is None or (isinstance(value, str) and value == ""):
        if spec.required:
            return ValidationIssue(
                key=key,
                message=f"{key!r} is required (example: {spec.example or spec.default!r})",
                severity=Severity.ERROR,
                value=value,
            )
        return None

    coerced = coerce_value(key, value)
    validator = _KIND_VALIDATORS.get(spec.kind, _validate_opaque)
    message = validator(coerced)
    if message is not None:
        severity = Severity.ERROR if spec.required else Severity.WARNING
        return ValidationIssue(key=key, message=message, severity=severity, value=value)

    if (
        spec.allowed is not None
        and coerced not in spec.allowed
        and str(coerced) not in {str(item) for item in spec.allowed}
    ):
        return ValidationIssue(
            key=key,
            message=f"{key!r} must be one of {list(spec.allowed)}, got {value!r}",
            severity=Severity.WARNING,
            value=value,
        )

    if isinstance(coerced, int) and not isinstance(coerced, bool):
        if spec.min_value is not None and coerced < spec.min_value:
            return ValidationIssue(
                key=key,
                message=f"{key!r} must be >= {spec.min_value}, got {coerced}",
                severity=Severity.WARNING,
                value=value,
            )
        if spec.max_value is not None and coerced > spec.max_value:
            return ValidationIssue(
                key=key,
                message=f"{key!r} must be <= {spec.max_value}, got {coerced}",
                severity=Severity.WARNING,
                value=value,
            )

    if spec.custom_validator is not None:
        message = spec.custom_validator(coerced)
        if message:
            severity = Severity.ERROR if spec.required else Severity.WARNING
            return ValidationIssue(key=key, message=message, severity=severity, value=value)

    return None


def validate_payload(payload: Mapping[str, Any]) -> list[ValidationIssue]:
    """Validate an entire payload dictionary and return all issues found.

    The check is intentionally exhaustive — it returns issues for every
    key, including unknown ones, so callers can decide which severity
    levels to surface. No exception is ever raised, which preserves the
    historical contract that loading ``payload.json`` must never crash
    the framework just because a field is malformed.

    Args:
        payload: Dictionary loaded from ``payload.json``.

    Returns:
        Possibly empty list of :class:`ValidationIssue`. Required fields
        that are missing from the payload entirely are reported with
        :class:`Severity.ERROR`.
    """
    issues: list[ValidationIssue] = []
    for spec in SCHEMA.values():
        if spec.required and spec.name not in payload:
            issues.append(
                ValidationIssue(
                    key=spec.name,
                    message=f"{spec.name!r} is required but missing from payload",
                    severity=Severity.ERROR,
                    value=None,
                )
            )
    for key, value in payload.items():
        issue = validate_value(key, value)
        if issue is not None:
            issues.append(issue)
    return issues


def format_issue(issue: ValidationIssue) -> str:
    """Render a :class:`ValidationIssue` as a single human-readable line.

    Sensitive fields have their value redacted so log scrapers do not
    expose credentials. The format intentionally mirrors GCC-style
    diagnostics (``key: severity: message``) so it grep-friendly.
    """
    spec = SCHEMA.get(issue.key)
    display: str
    if spec is not None and spec.sensitive:
        display = "<redacted>"
    else:
        raw = "" if issue.value is None else str(issue.value)
        display = raw if len(raw) <= 64 else raw[:61] + "..."
    suffix = f" (value={display!r})" if display else ""
    return f"{issue.key}: {issue.severity.value}: {issue.message}{suffix}"


def default_payload() -> dict[str, Any]:
    """Return a freshly built payload dict populated from the schema defaults.

    Useful for tests and for the wizard when no ``payload.json`` exists.
    """
    return {spec.name: spec.default for spec in SCHEMA.values()}


def categories() -> dict[str, list[FieldSpec]]:
    """Return schema entries grouped by :attr:`FieldSpec.category`.

    Used by the wizard to render category-aware tables and by future
    documentation generators.
    """
    grouped: dict[str, list[FieldSpec]] = {}
    for spec in SCHEMA.values():
        grouped.setdefault(spec.category, []).append(spec)
    return grouped


__all__ = [
    "FieldKind",
    "FieldSpec",
    "Severity",
    "SCHEMA",
    "ValidationIssue",
    "categories",
    "coerce_value",
    "default_payload",
    "field_for",
    "format_issue",
    "validate_payload",
    "validate_value",
]
