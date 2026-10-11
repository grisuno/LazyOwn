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
