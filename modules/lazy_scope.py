"""Lab-only default scope for autonomous loop targets.

When no explicit task scope is configured the autonomous loop must never
touch public infrastructure. This module decides whether a target is a
local lab address: loopback, RFC1918 IPv4, link-local, unique-local or
loopback IPv6, or a hostname whose every resolved address is lab-local.
Operators can extend the lab set with an explicit allowlist file.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

from __future__ import annotations

import ipaddress
import re
import socket
from dataclasses import dataclass, field
from pathlib import Path

LAB_DEFAULT_ENABLED = True
LAB_RESOLVE_TIMEOUT_SEC = 2.0
LAB_RESOLVE_TTL_SEC = 300.0
MAX_HOST_EXTRACT = 64
ALLOWLIST_FILENAME = "scope_allow.txt"
DENYLIST_FILENAME = "scope_deny.txt"
_HOSTNAME_PATTERN = re.compile(
    r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\b",
    re.IGNORECASE,
)
_IPV4_PATTERN = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)
_IPV6_PATTERN = re.compile(r"(?<![\w:])(?:[0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}(?![\w:])")
_FILE_SUFFIXES = frozenset(
    {
        "py", "sh", "js", "json", "yaml", "yml", "md", "txt", "xml", "html",
        "csv", "log", "conf", "cfg", "ini", "bak", "zip", "tar", "gz", "pcap",
    }
)


@dataclass(frozen=True)
class ScopeVerdict:
    """Outcome of a lab-scope check for one target.

    Attributes:
        allowed: True when the target may be touched.
        reason: Machine-readable denial kind or "" when allowed.
        detail: Human-readable explanation for the audit trail.
    """

    allowed: bool
    reason: str = ""
    detail: str = ""


@dataclass
class _ResolveCache:
    """Tiny TTL cache for hostname resolution results."""

    entries: dict[str, tuple[float, tuple[str, ...]]] = field(default_factory=dict)

    def get(self, name: str, now: float) -> tuple[str, ...] | None:
        """Return cached addresses when fresh.

        Args:
            name: Hostname previously resolved.
            now: Current monotonic timestamp.

        Returns:
            Cached address tuple or None on miss/expiry.
        """
        hit = self.entries.get(name)
        if hit is None:
            return None
        stamp, values = hit
        if now - stamp > LAB_RESOLVE_TTL_SEC:
            self.entries.pop(name, None)
            return None
        return values

    def put(self, name: str, values: tuple[str, ...], now: float) -> None:
        """Store resolution results.

        Args:
            name: Hostname resolved.
            values: Resolved address strings.
            now: Current monotonic timestamp.
        """
        if len(self.entries) > 256:
            self.entries.clear()
        self.entries[name] = (now, values)


_CACHE = _ResolveCache()


def is_lab_address(address: str) -> bool:
    """Classify one address as lab-local.

    Args:
        address: IPv4 or IPv6 literal.

    Returns:
        True for loopback, RFC1918, link-local or unique-local addresses.
    """
    text = str(address or "").strip().strip("[]")
    if not text:
        return False
    try:
        parsed = ipaddress.ip_address(text)
    except ValueError:
        return False
    if isinstance(parsed, ipaddress.IPv6Address) and parsed.ipv4_mapped:
        parsed = parsed.ipv4_mapped
    return (
        parsed.is_loopback
        or parsed.is_private
        or parsed.is_link_local
    )


def extract_hosts(text: str) -> list[str]:
    """Pull IP literals and plausible hostnames out of free text.

    Args:
        text: Command line, intent text or tool arguments.

    Returns:
        Unique candidate hosts in first-seen order, capped.
    """
    sample = str(text or "")
    candidates: list[tuple[int, str]] = []
    seen: set[str] = set()

    def _keep(start: int, value: str) -> None:
        lowered = value.lower().rstrip(".")
        if lowered and lowered not in seen:
            seen.add(lowered)
            candidates.append((start, lowered))

    for match in _IPV4_PATTERN.finditer(sample):
        _keep(match.start(), match.group(0))
    for match in _IPV6_PATTERN.finditer(sample):
        candidate = match.group(0)
        if ":" in candidate and not candidate.endswith(":"):
            _keep(match.start(), candidate)
    for match in _HOSTNAME_PATTERN.finditer(sample):
        name = match.group(0).lower()
        tail = name.rsplit(".", 1)[-1]
        if tail in _FILE_SUFFIXES:
            continue
        _keep(match.start(), name)
    return [value for _, value in sorted(candidates, key=lambda item: item[0])][:MAX_HOST_EXTRACT]


def resolve_addresses(name: str, now: float | None = None) -> tuple[str, ...]:
    """Resolve a hostname to all of its addresses.

    Args:
        name: Hostname to resolve.
        now: Optional monotonic timestamp override (tests).

    Returns:
        Tuple of address strings; empty when resolution fails or the
        name is an address literal already.
    """
    import time

    moment = time.monotonic() if now is None else now
    text = str(name or "").strip().strip("[]")
    if not text or _looks_like_address(text):
        return ()
    cached = _CACHE.get(text.lower(), moment)
    if cached is not None:
        return cached
    try:
        rows = socket.getaddrinfo(text, None)
    except OSError:
        rows = []
    values = tuple(dict.fromkeys(str(row[4][0]) for row in rows))
    _CACHE.put(text.lower(), values, moment)
    return values


def _looks_like_address(text: str) -> bool:
    """Return True when the text is already an IP literal.

    Args:
        text: Candidate host string.

    Returns:
        True for IPv4/IPv6 literals.
    """
    try:
        ipaddress.ip_address(text.strip("[]"))
    except ValueError:
        return False
    return True


def read_scope_file(name: str, sessions_dir: str | Path = "sessions") -> frozenset[str]:
    """Load operator entries from a scope list file.

    Args:
        name: File name inside ``sessions_dir`` covering the entries.
        sessions_dir: Directory holding the scope files.

    Returns:
        Frozenset of lowercase entries; comments and blanks skipped.
    """
    path = Path(sessions_dir) / name
    if not path.is_file():
        return frozenset()
    entries: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        entry = line.strip().lower()
        if not entry or entry.startswith("#"):
            continue
        entries.add(entry.rstrip("."))
    return frozenset(entries)


def read_allowlist(sessions_dir: str | Path = "sessions") -> frozenset[str]:
    """Load operator-approved extra lab hosts.

    Args:
        sessions_dir: Directory holding ``scope_allow.txt``.

    Returns:
        Frozenset of lowercase host entries; comments and blanks skipped.
    """
    return read_scope_file(ALLOWLIST_FILENAME, sessions_dir)


def read_denylist(sessions_dir: str | Path = "sessions") -> frozenset[str]:
    """Load explicitly denied hosts and networks.

    Args:
        sessions_dir: Directory holding ``scope_deny.txt``.

    Returns:
        Frozenset of lowercase deny entries: hostnames, IPs or CIDR blocks.
    """
    return read_scope_file(DENYLIST_FILENAME, sessions_dir)


def scope_verdict(
    target: str,
    resolver=resolve_addresses,
    allowlist: frozenset[str] | None = None,
    denylist: frozenset[str] | None = None,
) -> ScopeVerdict:
    """Decide whether one target is inside the default lab scope.

    Deny entries have priority: a deny hit blocks before any allow path is
    considered. Denied entries may be hostnames, IP literals or CIDR
    blocks; CIDR deny covers every address inside the block. Address
    literals are classified directly; hostnames must resolve and every
    answer must be lab-local. Unresolvable names are denied.

    Args:
        target: Host or IP the loop wants to touch.
        resolver: Address resolver (injectable for tests).
        allowlist: Extra operator-approved lab hosts.
        denylist: Operator-denied hosts, IPs or CIDR blocks.

    Returns:
        ScopeVerdict with allowed flag, denial kind and detail.
    """
    text = str(target or "").strip().strip("[]")
    if not text:
        return ScopeVerdict(False, "empty", "no target to authorize")
    lowered = text.lower().rstrip(".")
    if denylist and _entry_denied(text, lowered, denylist):
        return ScopeVerdict(False, "denylist", f"{text} is explicitly denied by operator denylist")
    if allowlist and lowered in allowlist:
        return ScopeVerdict(True, "", "operator allowlist")
    if _looks_like_address(text):
        if is_lab_address(text):
            return ScopeVerdict(True, "", "lab address literal")
        return ScopeVerdict(False, "public-ip", f"{text} is not a lab address")
    addresses = resolver(text)
    if not addresses:
        return ScopeVerdict(False, "unresolved", f"{text} does not resolve")
    if denylist:
        denied_addresses = [addr for addr in addresses if _address_denied(addr, denylist)]
        if denied_addresses:
            return ScopeVerdict(False, "denylist", f"{text} resolves to a denied address: {denied_addresses[0]}")
    public = [addr for addr in addresses if not is_lab_address(addr)]
    if public:
        return ScopeVerdict(
            False,
            "public-resolve",
            f"{text} resolves outside the lab: {', '.join(public[:3])}",
        )
    return ScopeVerdict(True, "", f"{text} resolves inside the lab")


def _networks_of(entries: frozenset[str]) -> list[ipaddress._BaseNetwork]:
    """Return parsed CIDR networks from a scope entry set."""
    networks: list[ipaddress._BaseNetwork] = []
    for entry in entries:
        try:
            parsed = ipaddress.ip_network(entry.rstrip("."), strict=False)
        except ValueError:
            continue
        networks.append(parsed)
    return networks


def _address_denied(address: str, denylist: frozenset[str]) -> bool:
    """Return True when one address falls inside a deny CIDR or literal."""
    text = str(address or "").strip("[]")
    try:
        parsed = ipaddress.ip_address(text)
    except ValueError:
        return False
    for network in _networks_of(denylist):
        if parsed in network:
            return True
    return text in denylist


def _entry_denied(text: str, lowered: str, denylist: frozenset[str]) -> bool:
    """Return True when a target matches or resolves into the denylist.

    Args:
        text: Original target token.
        lowered: Lowercased target without the trailing dot.
        denylist: Operator deny entries.

    Returns:
        True when the target is denied.
    """
    if lowered in denylist or text in denylist:
        return True
    if _looks_like_address(text):
        return _address_denied(text, denylist)
    addresses = resolve_addresses(lowered)
    return any(_address_denied(addr, denylist) for addr in addresses)


def command_scope_verdict(
    command: str,
    resolver=resolve_addresses,
    allowlist: frozenset[str] | None = None,
    denylist: frozenset[str] | None = None,
) -> ScopeVerdict:
    """Check every host mentioned in a command line.

    Args:
        command: Full command string about to execute.
        resolver: Address resolver (injectable for tests).
        allowlist: Extra operator-approved lab hosts.
        denylist: Operator-denied hosts, IPs or CIDR blocks.

    Returns:
        Verdict for the first offending host, or an allowed verdict when
        every extracted host passes.
    """
    for host in extract_hosts(command):
        verdict = scope_verdict(host, resolver=resolver, allowlist=allowlist, denylist=denylist)
        if not verdict.allowed:
            return verdict
    return ScopeVerdict(True, "", "all hosts inside lab scope")


__all__ = [
    "ALLOWLIST_FILENAME",
    "DENYLIST_FILENAME",
    "LAB_DEFAULT_ENABLED",
    "LAB_RESOLVE_TIMEOUT_SEC",
    "LAB_RESOLVE_TTL_SEC",
    "ScopeVerdict",
    "command_scope_verdict",
    "extract_hosts",
    "is_lab_address",
    "read_allowlist",
    "read_denylist",
    "read_scope_file",
    "resolve_addresses",
    "scope_verdict",
]
