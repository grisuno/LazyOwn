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
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Any

log = logging.getLogger("core.hardening")

MAX_SSH_COMMAND_LENGTH = 4096
MAX_CLIPBOARD_CONTENT_LENGTH = 65536
_SAFE_PATH_PATTERN = re.compile(r"^[a-zA-Z0-9._/\-]+$")
_NETWORK_CIDR_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    r"(?:/(?:3[0-2]|[12]?\d))?$"
)
_PORT_PATTERN = re.compile(r"^(?:\d{1,5}(?:,\d{1,5})*(?:-\d{1,5})?)$")


class SecurityViolation(PermissionError):
    """Raised when a security invariant is violated."""


def safe_subprocess_run(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
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

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


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


__all__ = [
    "SecurityViolation",
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
    "MAX_SSH_COMMAND_LENGTH",
    "MAX_CLIPBOARD_CONTENT_LENGTH",
]
