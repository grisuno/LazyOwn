"""Centralized security hardening utilities for the LazyOwn framework.

Contract: provides safe alternatives to dangerous patterns found across
the codebase. Every function is a single-responsibility security control
that replaces ad-hoc, vulnerable patterns with a tested, auditable path.

The module is a facade over four single-concern siblings; import them
directly for new code:

- :mod:`core.paths` — filesystem containment for untrusted paths.
- :mod:`core.tls` — client TLS contexts and the gated lab fallback.
- :mod:`core.secrets` — owner-only secret storage, sealing, key requirements.
- :mod:`core.text` — HTML escaping, emoji detection, secret redaction.

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

import logging
import os
import re
import subprocess
import warnings
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from core.errors import SecurityViolation
from core.host_policy import is_valid_host as _is_valid_host_policy
from core.paths import (
    DIR_PATH_MAX_LENGTH,
    PATH_SEGMENT_MAX_LENGTH,
    UPSTREAM_PATH_MAX_LENGTH,
    YAML_NAME_MAX_LENGTH,
    is_safe_dir_path,
    is_safe_path_segment,
    is_safe_yaml_name,
    realpath_contained,
    realpath_within_base,
    safe_join_under,
    safe_open_under,
    safe_path_join,
    sanitize_filename,
    validate_upstream_path,
)
from core.safe_exec import safe_run_argv
from core.secrets import (
    MAX_SSH_COMMAND_LENGTH,
    SEALED_SECRET_PREFIX,
    SECRET_DIR_MODE,
    SECRET_FILE_MODE,
    build_sshpass_command,
    require_encryption_key,
    seal_secret,
    set_sshpass_env,
    store_secret_owner_only,
    unseal_secret,
)
from core.text import (
    contains_emoji,
    escape_html_content,
    escape_powershell_single_quoted,
    iter_emoji_spans,
    redact_text,
)
from core.tls import (
    TLS_MINIMUM_VERSION,
    tls_lab_fallback_context,
    tls_lab_unverified_allowed,
    tls_secure_context,
)

log = logging.getLogger("core.hardening")

MAX_CLIPBOARD_CONTENT_LENGTH = 65536
SHELL_OPERATOR_CHARS = frozenset([";", "|", "&", "$", "`", "\n", "\r"])
PROGRAM_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9._/\-][a-zA-Z0-9._/\- ]*$")

_NETWORK_CIDR_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    r"(?:/(?:3[0-2]|[12]?\d))?$"
)
_PORT_PATTERN = re.compile(r"^(?:\d{1,5}(?:,\d{1,5})*(?:-\d{1,5})?)$")


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

    Deprecated:
        Use :func:`core.safe_exec.safe_run_argv` (the single execution
        primitive). This wrapper keeps its stricter validation contract
        and delegates execution; it will be removed after its callers
        migrate.
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
    warnings.warn(
        "core.hardening.safe_subprocess_run is deprecated; use core.safe_exec.safe_run_argv",
        DeprecationWarning,
        stacklevel=2,
    )
    return safe_run_argv(
        list(argv),
        timeout=timeout,
        capture_output=capture_output,
        extra_env=extra_env,
    )


def safe_clipboard_copy(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to system clipboard.

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
        except (subprocess.SubprocessError, OSError):
            continue
    log.debug("clipboard copy failed: no X11 clipboard tool available")
    return False


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
    "realpath_within_base",
    "realpath_contained",
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
