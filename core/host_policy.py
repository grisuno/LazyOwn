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
from collections.abc import Sequence

_HOST_RE = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9]([A-Za-z0-9._-]{0,251}[A-Za-z0-9])?)$")
_SHELL_META_CHARS = frozenset(";&|`$(){}!><*?~#\\'\"\n\r")
_FILE_LIKE_SUFFIXES = (
    ".sh",
    ".py",
    ".exe",
    ".dll",
    ".ps1",
    ".bat",
    ".txt",
    ".json",
    ".xml",
    ".html",
    ".php",
    ".jsp",
    ".bin",
    ".elf",
    ".so",
    ".conf",
    ".cfg",
    ".log",
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


def is_world_host(value: object) -> bool:
    """Return True when value may stand as a world-model host key.

    The world-model host surface is stricter than the target grammar: a
    host key must be an IP literal or a dotted hostname. Bare single-label
    slugs (chain names such as ``gym_metasploitable_ms2_nfs_exports``,
    task ids, run ids) match the loose target grammar yet are never
    routable hosts, and letting them into the host map pollutes the
    surface diff and every consumer that reads it.

    Args:
        value: Candidate host key of any type.

    Returns:
        True for IP literals and dotted hostnames; False otherwise.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or "/" in text or not is_valid_host(text):
        return False
    try:
        ipaddress.ip_address(text)
        return True
    except ValueError:
        return "." in text and _HOST_RE.match(text) is not None


def parse_network(value: str) -> ipaddress._BaseNetwork | None:
    """Parse a CIDR-or-IP string into a network object, None on failure.

    Args:
        value: Candidate network in CIDR notation or a bare address.

    Returns:
        The parsed network (host-strictness relaxed), or ``None``.
    """
    try:
        return ipaddress.ip_network(value, strict=False)
    except ValueError:
        return None


def hostname_match(target: str, entry: str) -> bool:
    """Match a hostname target against a scope entry.

    Args:
        target: Candidate hostname.
        entry: Scope entry; a leading ``*.`` wildcards one label and any
            other entry also authorises its subdomains.

    Returns:
        True when the target is the entry or one of its subdomains.
    """
    normalized_target = target.lower().rstrip(".")
    normalized_entry = entry.lower().rstrip(".")
    if normalized_entry.startswith("*."):
        bare = normalized_entry[2:]
        return normalized_target == bare or normalized_target.endswith("." + bare)
    return normalized_target == normalized_entry or normalized_target.endswith("." + normalized_entry)


def target_in_scope(target: str, entries: Sequence[str]) -> bool:
    """Return whether ``target`` falls within any of the scope ``entries``.

    IP targets are matched against CIDR networks and bare IP entries;
    hostname targets are matched against hostname entries (supporting a
    leading ``*.`` wildcard for subdomains). Cross-kind comparisons (IP
    target vs hostname entry, or vice versa) never match because
    resolving them would require DNS, which the guard deliberately
    avoids.

    Args:
        target: The active target (IP address or hostname).
        entries: Authorized scope entries.

    Returns:
        ``True`` when the target is authorized by at least one entry.
    """
    target = (target or "").strip()
    if not target:
        return False
    try:
        parsed_target: ipaddress._BaseAddress | None = ipaddress.ip_address(target)
    except ValueError:
        parsed_target = None
    for raw in entries:
        entry = raw.strip()
        if not entry:
            continue
        if entry == target:
            return True
        network = parse_network(entry)
        if network is not None:
            if parsed_target is not None and parsed_target in network:
                return True
            continue
        if parsed_target is None and hostname_match(target, entry):
            return True
    return False


def network_in_scope(network: str, entries: Sequence[str]) -> bool:
    """Return whether a whole network is authorized by the scope ``entries``.

    A network is authorized only when every address it contains is covered:
    the entry must be a CIDR that is equal to or a supernet of ``network``.
    Bare IPs and hostnames never authorize a network, so a sweep such as
    ``10.0.0.0/16`` cannot slip past a scope that names a single host.

    Args:
        network: The candidate network in CIDR notation.
        entries: Authorized scope entries.

    Returns:
        ``True`` when at least one scope entry covers the whole network.
    """
    parsed = parse_network((network or "").strip())
    if parsed is None:
        return False
    for raw in entries:
        entry = parse_network((raw or "").strip())
        if entry is None or entry.version != parsed.version:
            continue
        if parsed.subnet_of(entry):
            return True
    return False
