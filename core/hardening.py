"""Centralized security hardening utilities for the LazyOwn framework.

Contract: provides safe alternatives to dangerous patterns found across
the codebase. Every function is a single-responsibility security control
that replaces ad-hoc, vulnerable patterns with a tested, auditable path.

Invariants:

1. ``safe_subprocess_run`` never invokes a shell unless explicitly allowed
   and audited.
2. ``safe_clipboard_copy`` uses subprocess list-form, never os.system.
3. ``validate_sshpass_env`` sets SSHPASS env var and uses sshpass -e,
   never sshpass -p.
4. ``escape_html`` sanitizes all user-controlled data before HTML insertion.
5. ``safe_path_join`` prevents path traversal via os.path.realpath prefix
   check.
6. ``require_encryption_key`` refuses to operate with a static fallback key.
7. ``defused_xml_parse`` wraps defusedxml for safe XML parsing.
"""

from __future__ import annotations

import html
import logging
import os
import re
import ssl
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from core.host_policy import is_valid_host as _is_valid_host_policy

log = logging.getLogger("core.hardening")

MAX_SSH_COMMAND_LENGTH = 4096
MAX_CLIPBOARD_CONTENT_LENGTH = 65536
SHELL_OPERATOR_CHARS = frozenset([";", "|", "&", "$", "`", "\n", "\r"])
PROGRAM_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9._/\-][a-zA-Z0-9._/\- ]*$")

TLS_MINIMUM_VERSION = ssl.TLSVersion.TLSv1_2
UPSTREAM_PATH_MAX_LENGTH = 8192
DIR_PATH_MAX_LENGTH = 256
PATH_SEGMENT_MAX_LENGTH = 64
YAML_NAME_MAX_LENGTH = 128
YAML_SUFFIX = ".yaml"
SECRET_FILE_MODE = 0o600
SECRET_DIR_MODE = 0o700
ENV_ALLOW_SELF_SIGNED_LAB = "LAZY_PROXY_ALLOW_SELF_SIGNED_LAB"
ENV_ALLOW_PRIVATE = "LAZY_PROXY_ALLOW_PRIVATE"
ENV_INSECURE_TLS = "LAZY_PROXY_INSECURE_TLS"
ENV_TRUST_CA = "LAZY_PROXY_TRUST_CA"

_SAFE_SEGMENT_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")

_EMOJI_RANGES: tuple[tuple[int, int], ...] = (
    (0x1F600, 0x1F64F),
    (0x1F300, 0x1F5FF),
    (0x1F680, 0x1F6FF),
    (0x1F700, 0x1F77F),
    (0x1F780, 0x1F7FF),
    (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF),
    (0x1FA70, 0x1FAFF),
    (0x2600, 0x26FF),
    (0x2700, 0x27BF),
    (0x2B00, 0x2BFF),
    (0xFE00, 0xFE0F),
    (0x200D, 0x200D),
)

_REDACT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)(smbpass\s+)([^\s;]{1,128})"),
    re.compile(r"(?i)(password\s*[=:]\s*['\"]?)([^'\"\s;]{1,128})"),
    re.compile(r"(?i)(passwd\s*[=:]\s*['\"]?)([^'\"\s;]{1,128})"),
    re.compile(r"(?i)(pwd\s*[=:]\s*['\"]?)([^'\"\s;]{1,128})"),
    re.compile(r"(?i)(api[_-]?key\s*[=:]\s*['\"]?)([\w\-.]{8,})(['\"]?)"),
    re.compile(r"(?i)(bearer\s+)([A-Za-z0-9\-._~+/]{8,})"),
    re.compile(r"https?://[^/\s]*:[^@/\s]+@[^\s]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def reject_option_injection(argv: Sequence[str], *, allow_options: bool = True) -> None:
    """Reject argument-injection payloads in argv.

    Args:
        argv: Program and arguments as a sequence.
        allow_options: When False, reject any argument starting with dash.

    Raises:
        SecurityViolation: If an injection pattern is detected.
    """
    for arg in list(argv)[1:]:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
        if "\n" in arg or "\r" in arg:
            raise SecurityViolation("Control character in argument rejected")
        if not allow_options and arg.startswith("-") and arg != "-":
            raise SecurityViolation("Leading-dash argument rejected")


def escape_powershell_single_quoted(value: str) -> str:
    """Escape a value for embedding in a PowerShell single-quoted string.

    Args:
        value: Raw value that may contain quotes or metacharacters.

    Returns:
        Value safe to embed between single quotes in PowerShell.
    """
    return str(value).replace("'", "''")


_SAFE_PATH_PATTERN = re.compile(r"^[a-zA-Z0-9._/\-]+$")
_NETWORK_CIDR_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    r"(?:/(?:3[0-2]|[12]?\d))?$"
)
_PORT_PATTERN = re.compile(r"^(?:\d{1,5}(?:,\d{1,5})*(?:-\d{1,5})?)$")


class SecurityViolation(PermissionError):
    """Raised when a security invariant is violated."""


def terminal_env(base: Mapping[str, str] | None = None) -> dict[str, str]:
    """Return a child environment that keeps ANSI colors on a pipe.

    Tools built on termenv or rich (gum, the LazyNmap script) disable color
    when their stdout is not a terminal. The framework pipes output so it can
    tee it to a log, so the child would otherwise lose its colors. Forcing
    CLICOLOR_FORCE and FORCE_COLOR restores them. An explicit NO_COLOR wins
    over the forced values.

    Args:
        base: Base environment. Defaults to ``os.environ``.
    Returns:
        A new mapping safe to pass as the ``env`` argument of subprocess.
    """
    env = dict(os.environ if base is None else base)
    if "NO_COLOR" not in env:
        env.setdefault("CLICOLOR_FORCE", "1")
        env.setdefault("FORCE_COLOR", "1")
    return env


def safe_subprocess_run(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
    extra_env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.
        extra_env: Optional environment additions merged over the parent
            environment (values are verbatim overrides, never trimmed).

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    program = str(argv[0])
    if "\0" in program:
        raise SecurityViolation("Null byte in program name rejected")
    if "\n" in program or "\r" in program:
        raise SecurityViolation("Control character in program name rejected")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
        if "\n" in arg or "\r" in arg:
            raise SecurityViolation("Control character in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    env: dict[str, str] | None = None
    if extra_env:
        env = dict(os.environ)
        env.update({str(key): str(value) for key, value in extra_env.items()})
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
        env=env,
    )


def safe_clipboard_copy(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes")
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def build_sshpass_command(
    password: str,
    ssh_args: list[str],
    *,
    max_password_length: int = 256,
) -> list[str]:
    """Build an sshpass command using SSHPASS env var (sshpass -e).

    Never uses sshpass -p which exposes passwords in process listings.

    Args:
        password: The SSH password to use.
        ssh_args: Arguments to pass to ssh/scp after sshpass.
        max_password_length: Maximum allowed password length.

    Returns:
        List of command arguments suitable for subprocess.run.

    Raises:
        SecurityViolation: If password exceeds max_password_length or
            contains characters that could break the env var.
    """
    if len(password) > max_password_length:
        raise SecurityViolation("Password exceeds maximum allowed length")
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def set_sshpass_env(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def escape_html_content(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(value), quote=True)


def safe_path_join(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(f"Path traversal blocked: {user_path} resolves outside {base_dir}")
    return candidate


def validate_network_cidr(cidr: str) -> bool:
    """Validate a network CIDR notation string.

    Args:
        cidr: Network address in CIDR notation (e.g. "192.168.1.0/24").

    Returns:
        True if valid CIDR, False otherwise.
    """
    return bool(_NETWORK_CIDR_PATTERN.match(cidr.strip()))


def validate_port_spec(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports or not ports.strip():
        return False
    return bool(_PORT_PATTERN.match(ports.strip()))


def validate_host(host: str) -> bool:
    """Validate a hostname or IP address.

    Single policy shared with the CLI gates: plain IPs, CIDR blocks
    and hostnames pass, shell metacharacters fail. CIDR-only strings
    are additionally accepted by the network pattern below.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    return _is_valid_host_policy(host)


def require_encryption_key(
    env_key: str = "LAZYOWN_SECRET_KEY",
    secret_file: Path | None = None,
) -> str:
    """Require a proper encryption key; never fall back to a static default.

    Args:
        env_key: Environment variable name for the secret key.
        secret_file: Optional path to a file containing the key.

    Returns:
        The encryption key string.

    Raises:
        SecurityViolation: If no key is configured.
    """
    secret = os.environ.get(env_key, "")
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def defused_xml_parse(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError("defusedxml is required for safe XML parsing. Install with: pip install defusedxml")
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def tls_secure_context(extra_ca: str = "") -> ssl.SSLContext:
    """Build a verifying client TLS context with a TLS 1.2 floor.

    Args:
        extra_ca: Optional extra CA bundle path loaded for verification.

    Returns:
        Verifying SSLContext with hostname checking enabled.
    """
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    try:
        context.minimum_version = TLS_MINIMUM_VERSION
    except (AttributeError, ValueError):
        pass
    bundle = (extra_ca or os.environ.get(ENV_TRUST_CA, "") or "").strip()
    if bundle:
        try:
            context.load_verify_locations(cafile=bundle)
        except OSError as exc:
            log.warning("trust bundle unreadable %r: %s", bundle, exc)
    return context


def tls_lab_unverified_allowed(host: str) -> bool:
    """Return True only when unverified lab TLS is explicitly opted in.

    Both conditions must hold: the host is a loopback/private literal (or
    localhost) and the operator set ``LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1``.
    Request data can never enable it alone.

    Args:
        host: Target hostname or IP literal.

    Returns:
        True when the operator opt-in covers this lab host.
    """
    import ipaddress as _ipaddress

    if os.environ.get(ENV_ALLOW_SELF_SIGNED_LAB, "") != "1":
        return False
    name = (host or "").strip().strip("[]").lower()
    if name == "localhost":
        return True
    try:
        addr = _ipaddress.ip_address(name)
    except ValueError:
        return False
    return bool(addr.is_loopback or addr.is_private or addr.is_link_local)


def tls_lab_fallback_context() -> ssl.SSLContext:
    """Build the gated unverified context for lab self-signed hosts.

    This is the single audited location allowed to disable verification.
    Callers must check :func:`tls_lab_unverified_allowed` first; the TLS
    1.2 floor still applies so only verification (not protocol version)
    is relaxed.

    Returns:
        Unverified SSLContext with TLS 1.2 floor.
    """
    log.warning("unverified TLS fallback engaged for lab target (self-signed)")
    fallback = ssl.create_default_context()
    fallback.check_hostname = False
    fallback.verify_mode = ssl.CERT_NONE
    try:
        fallback.minimum_version = TLS_MINIMUM_VERSION
    except (AttributeError, ValueError):
        pass
    return fallback


def validate_upstream_path(path: str) -> bool:
    """Validate an origin-form upstream path without regular expressions.

    Only ``/absolute-path[?query]`` is accepted: absolute URLs, control
    characters, NUL/CR/LF and overlong values are rejected in linear time.

    Args:
        path: Upstream path or target string.

    Returns:
        True when the path is safe to send upstream.
    """
    text = path or ""
    if not text or len(text) > UPSTREAM_PATH_MAX_LENGTH:
        return False
    if not text.startswith("/"):
        return False
    lowered = text.lower()
    if "://" in lowered:
        return False
    for char in text:
        code = ord(char)
        if code < 32 or code == 127:
            return False
    if "\x00" in text:
        return False
    return True


def is_safe_path_segment(segment: str) -> bool:
    """Validate one path segment with a linear charset scan (no regex).

    Args:
        segment: Single directory or filename stem segment.

    Returns:
        True when the segment uses only safe characters.
    """
    if not segment or len(segment) > PATH_SEGMENT_MAX_LENGTH:
        return False
    if segment in (".", ".."):
        return False
    if segment.startswith("."):
        return False
    for char in segment:
        if char not in _SAFE_SEGMENT_CHARS:
            return False
    return True


def is_safe_dir_path(raw: str) -> bool:
    """Validate a relative directory path with linear scans (no regex).

    Args:
        raw: Untrusted relative directory path.

    Returns:
        True when every segment is safe and no traversal is present.
    """
    if not raw or len(raw) > DIR_PATH_MAX_LENGTH:
        return False
    if "\x00" in raw or "\\" in raw:
        return False
    if raw.startswith("/") or raw.endswith("/"):
        return False
    parts = raw.split("/")
    if len(parts) > 8:
        return False
    if not parts:
        return False
    for part in parts:
        if not is_safe_path_segment(part):
            return False
    return True


def is_safe_yaml_name(name: str) -> bool:
    """Validate a YAML filename with linear scans (no regex).

    Args:
        name: Untrusted filename.

    Returns:
        True when the name is a safe ``*.yaml`` file.
    """
    if not name or len(name) > YAML_NAME_MAX_LENGTH:
        return False
    if "\x00" in name or "/" in name or "\\" in name:
        return False
    if not name.endswith(YAML_SUFFIX):
        return False
    stem = name[: -len(YAML_SUFFIX)]
    return is_safe_path_segment(stem)


def safe_join_under(base_dir: str, user_path: str) -> str:
    """Join and resolve ``user_path`` under ``base_dir`` (symlink-safe).

    Uses realpath on both sides plus a commonpath prefix check so
    ``..`` segments and symlink escapes are rejected.

    Args:
        base_dir: Allowed root directory.
        user_path: Untrusted relative path.

    Returns:
        Resolved absolute path within ``base_dir``.

    Raises:
        SecurityViolation: If the resolved path escapes ``base_dir``.
        ValueError: If ``user_path`` is empty.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    try:
        if os.path.commonpath([allowed, candidate]) != allowed:
            raise SecurityViolation(f"Path traversal blocked: {user_path!r} escapes base")
    except ValueError as exc:
        raise SecurityViolation(f"Path traversal blocked: {exc}") from exc
    return candidate


def safe_open_under(base_dir: str, user_path: str, mode: str = "r", **kwargs: Any) -> Any:
    """Open a file under ``base_dir`` after traversal validation.

    Args:
        base_dir: Allowed root directory.
        user_path: Untrusted relative path.
        mode: Open mode (binary-safe modes rejected for writes of text secrets).

    Returns:
        Open file handle. Caller must close it.
    """
    resolved = safe_join_under(base_dir, user_path)
    flags = os.O_RDONLY | os.O_NOFOLLOW
    if "w" in mode or "a" in mode or "+" in mode:
        flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW
        if "a" in mode:
            flags |= os.O_APPEND
        else:
            flags |= os.O_TRUNC
    fd = os.open(resolved, flags, SECRET_FILE_MODE)
    try:
        os.chmod(resolved, SECRET_FILE_MODE)
    except OSError:
        pass
    return os.fdopen(fd, mode, **kwargs)


def store_secret_owner_only(path: str | Path, text: str) -> str:
    """Atomically store a secret owner-only (0600, dir 0700).

    Args:
        path: Destination file path.
        text: Secret text to persist.

    Returns:
        Resolved absolute path as string.
    """
    target = Path(path)
    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(parent, SECRET_DIR_MODE)
    except OSError:
        pass
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW
    fd = os.open(str(target), flags, SECRET_FILE_MODE)
    try:
        payload = str(text or "").encode("utf-8")
        view = memoryview(payload)
        while view:
            written = os.write(fd, view)
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    try:
        os.chmod(target, SECRET_FILE_MODE)
    except OSError:
        pass
    return str(target)


def _is_emoji_codepoint(code: int) -> bool:
    """Return True when ``code`` falls in a known emoji interval."""
    for start, end in _EMOJI_RANGES:
        if start <= code <= end:
            return True
    return False


def contains_emoji(text: str) -> bool:
    """Return True when ``text`` carries any emoji codepoint.

    Args:
        text: Text to inspect.

    Returns:
        True on first emoji hit; linear scan, no regex.
    """
    for char in text or "":
        if _is_emoji_codepoint(ord(char)):
            return True
    return False


def iter_emoji_spans(text: str) -> list[tuple[int, str]]:
    """Return ``(offset, char)`` for every emoji char in ``text``.

    Args:
        text: Text to inspect.

    Returns:
        List of offset/character pairs in encounter order.
    """
    spans: list[tuple[int, str]] = []
    for offset, char in enumerate(text or ""):
        if _is_emoji_codepoint(ord(char)):
            spans.append((offset, char))
    return spans


SEALED_SECRET_PREFIX = "enc:v2:"


def _seal_key(sessions_dir: str | Path = "sessions") -> bytes:
    """Resolve the 32-byte sealing key via the shared AES resolver.

    Args:
        sessions_dir: Directory holding the ``key.aes`` key file.

    Returns:
        Raw 32-byte key material.
    """
    from core.config import resolve_aes_key

    return resolve_aes_key({}, sessions_dir=sessions_dir)


def seal_secret(plaintext: str, *, sessions_dir: str | Path = "sessions") -> str:
    """Seal a secret with Fernet (AES-128-CBC + HMAC) for storage.

    The key comes from the shared ``key.aes`` resolver so sealed values
    round-trip across restarts without new configuration. Failures fall
    back to plaintext so loot/operator flows never break; callers keep
    owner-only file modes regardless.

    Args:
        plaintext: Secret to protect.
        sessions_dir: Key directory override (tests).

    Returns:
        ``enc:v2:`` sealed value, or plaintext when sealing is unavailable.
    """
    text = str(plaintext or "")
    if not text or text.startswith(SEALED_SECRET_PREFIX):
        return text
    try:
        import base64 as _b64

        from cryptography.fernet import Fernet

        raw = _seal_key(sessions_dir)
        token = Fernet(_b64.urlsafe_b64encode(raw)).encrypt(text.encode("utf-8"))
        return SEALED_SECRET_PREFIX + token.decode("ascii")
    except Exception as exc:
        log.warning("secret sealing unavailable, storing with file modes only: %s", type(exc).__name__)
        return text


def unseal_secret(stored: str, *, sessions_dir: str | Path = "sessions") -> str:
    """Reveal a secret stored by :func:`seal_secret` (legacy-compatible).

    Legacy ``enc:v1:`` vault values and plaintext fall back to the
    credential vault / passthrough so existing stores keep working.

    Args:
        stored: Sealed or plaintext value.
        sessions_dir: Key directory override (tests).

    Returns:
        Plaintext secret, or empty string when undecryptable.
    """
    text = str(stored or "")
    if not text:
        return ""
    if text.startswith(SEALED_SECRET_PREFIX):
        try:
            import base64 as _b64

            from cryptography.fernet import Fernet

            raw = _seal_key(sessions_dir)
            return (
                Fernet(_b64.urlsafe_b64encode(raw))
                .decrypt(text[len(SEALED_SECRET_PREFIX) :].encode("ascii"))
                .decode("utf-8")
            )
        except Exception:
            return ""
    try:
        from core.credential_vault import unseal_value as _vault_unseal

        revealed = _vault_unseal(text)
        if revealed:
            return str(revealed)
    except Exception:
        pass
    return text


def redact_text(text: str) -> str:
    """Mask credential-like patterns before persistence or display.

    Args:
        text: Raw text that may embed secrets.

    Returns:
        Text with secrets replaced by ``***`` markers.
    """
    cleaned = str(text or "")

    def _mask(match: re.Match) -> str:
        groups = match.groups()
        if len(groups) >= 2 and groups[0] and groups[-1] is not None:
            return f"{groups[0]}***{groups[-1] if len(groups) > 2 else ''}"
        return "***"

    for pattern in _REDACT_PATTERNS:
        cleaned = pattern.sub("***" if pattern.groups == 0 else _mask, cleaned)
    return cleaned


__all__ = [
    "SecurityViolation",
    "SHELL_OPERATOR_CHARS",
    "PROGRAM_NAME_PATTERN",
    "reject_option_injection",
    "escape_powershell_single_quoted",
    "safe_subprocess_run",
    "safe_clipboard_copy",
    "build_sshpass_command",
    "set_sshpass_env",
    "escape_html_content",
    "safe_path_join",
    "validate_network_cidr",
    "validate_port_spec",
    "validate_host",
    "require_encryption_key",
    "defused_xml_parse",
    "sanitize_filename",
    "tls_secure_context",
    "tls_lab_unverified_allowed",
    "tls_lab_fallback_context",
    "validate_upstream_path",
    "is_safe_path_segment",
    "is_safe_dir_path",
    "is_safe_yaml_name",
    "safe_join_under",
    "safe_open_under",
    "store_secret_owner_only",
    "seal_secret",
    "unseal_secret",
    "SEALED_SECRET_PREFIX",
    "contains_emoji",
    "iter_emoji_spans",
    "redact_text",
    "TLS_MINIMUM_VERSION",
    "UPSTREAM_PATH_MAX_LENGTH",
    "DIR_PATH_MAX_LENGTH",
    "PATH_SEGMENT_MAX_LENGTH",
    "YAML_NAME_MAX_LENGTH",
    "SECRET_FILE_MODE",
    "SECRET_DIR_MODE",
    "MAX_SSH_COMMAND_LENGTH",
    "MAX_CLIPBOARD_CONTENT_LENGTH",
]
