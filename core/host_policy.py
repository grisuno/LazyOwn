"""Single source of truth for host and network shape validation.

Both the CLI UX gates (``core.validators.check_*``) and the security
predicates (``core.hardening.validate_*``) used to embed their own
host-matching logic, which drifted apart. Every predicate here is
pure (no I/O, no console output) so presentation and security layers
share one fail-closed policy: plain IPs, CIDR blocks and hostnames
pass, anything with shell metacharacters fails.
"""

from __future__ import annotations

import ipaddress
import re

_HOST_RE = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9]([A-Za-z0-9._-]{0,251}[A-Za-z0-9])?)$")
_SHELL_META_CHARS = frozenset(";&|`$(){}!><*?~#\\'\"\n\r")
_FILE_LIKE_SUFFIXES = (
    ".sh", ".py", ".exe", ".dll", ".ps1", ".bat", ".txt", ".json", ".xml",
    ".html", ".php", ".jsp", ".bin", ".elf", ".so", ".conf", ".cfg", ".log",
)


def rejects_shell_meta(value: str) -> bool:
    """Return True when value contains characters usable for shell injection.

    Args:
        value: Raw host string to inspect.

    Returns:
        True when any shell metacharacter is present.
    """
    return any(ch in _SHELL_META_CHARS for ch in value)


def is_valid_cidr(value: str) -> bool:
    """Check value is a valid CIDR block.

    Args:
        value: Candidate CIDR string.

    Returns:
        True when ``ipaddress`` accepts it as a network.
    """
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def is_valid_host(value: object) -> bool:
    """Check value is a plain IP, CIDR, or hostname without shell metacharacters.

    Args:
        value: Candidate host value of any type.

    Returns:
        True for IPs, CIDR blocks and hostnames up to 253 chars.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or len(text) > 253 or rejects_shell_meta(text):
        return False
    candidate = text.split("/")[0] if "/" in text else text
    try:
        ipaddress.ip_address(candidate)
        return "/" not in text or is_valid_cidr(text)
    except ValueError:
        pass
    if "/" in text:
        return is_valid_cidr(text)
    return _HOST_RE.match(text) is not None


def is_file_like(value: object) -> bool:
    """Return True when value names a local artefact by extension, not a host.

    A tool name such as ``linpeas.sh`` superficially matches the hostname
    grammar yet is never an engagement target. Scope and target selection use
    this to keep local files out of host handling.

    Args:
        value: Candidate value of any type.

    Returns:
        True when the value ends with a known non-host file extension.
    """
    if not isinstance(value, str):
        return False
    return value.strip().lower().endswith(_FILE_LIKE_SUFFIXES)


def is_engagement_target(value: object, *, allow_cidr: bool = True) -> bool:
    """Return True when value is a routable engagement target, not a local file.

    A thin policy layer over :func:`is_valid_host`: file-like names are never
    targets, and CIDR blocks are rejected when the caller only accepts a
    single host (``allow_cidr=False``).

    Args:
        value: Candidate target value of any type.
        allow_cidr: When False, reject CIDR blocks (single-host call sites).

    Returns:
        True when the value is a usable host or (optionally) CIDR target.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or is_file_like(text):
        return False
    if not allow_cidr and "/" in text:
        return False
    return is_valid_host(text)
