"""Credential Reuse Engine for LazyOwn.

Automatically suggests captured credentials for newly discovered hosts.
When creds are found on host A, the engine ranks all other hosts by
likelihood that the same creds will work, generating actionable spray
recommendations with ready-to-run crackmapexec commands.

Design
------
- Single Responsibility: score + rank credential reuse candidates
- Taps StateManager for hosts/creds, WorldModel for confirmed/failed edges
- Produces a sorted list of (cred, host, score, command) tuples
- Score decays with subnet distance, service overlap, and prior failures
"""

from __future__ import annotations

import ipaddress
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("credential_reuse")

_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"
_CACHE_FILE = _SESSIONS_DIR / "cred_reuse_cache.json"


@dataclass
class ReuseCandidate:
    """Scored credential-to-host reuse suggestion."""

    username: str
    password: str
    target_host: str
    source_host: str
    score: float
    protocol: str = "smb"
    command: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "username": self.username,
            "password": self.password,
            "target_host": self.target_host,
            "source_host": self.source_host,
            "score": self.score,
            "protocol": self.protocol,
            "command": self.command,
        }


class CredentialReuseEngine:
    """Scoring engine for credential spraying prioritisation.

    Usage::

        engine = CredentialReuseEngine()
        candidates = engine.rank(
            hosts=["10.0.0.1", "10.0.0.2", "10.0.1.5"],
            creds=[{"username": "admin", "password": "P@ssw0rd", "host": "10.0.0.1"}],
        )
        for c in candidates:
            print(f"Try {c.username}:{c.password} against {c.target_host} "
                  f"[score={c.score:.2f}]")
            print(f"  {c.command}")
    """

    _SPRAY_PROTOCOLS = {
        "smb": "crackmapexec smb {host} -u '{user}' -p '{passwd}'",
        "winrm": "crackmapexec winrm {host} -u '{user}' -p '{passwd}'",
        "mssql": "crackmapexec mssql {host} -u '{user}' -p '{passwd}'",
        "ssh": "crackmapexec ssh {host} -u '{user}' -p '{passwd}'",
        "ldap": "crackmapexec ldap {host} -u '{user}' -p '{passwd}'",
        "rdp": "crackmapexec rdp {host} -u '{user}' -p '{passwd}'",
    }

    def __init__(self) -> None:
        self._failed: set[tuple[str, str, str]] = set()
        self._confirmed: set[tuple[str, str, str]] = set()
        self._load_cache()

    def _load_cache(self) -> None:
        if not _CACHE_FILE.exists():
            return
        try:
            data = json.loads(_CACHE_FILE.read_text())
            self._failed = {tuple(x) for x in data.get("failed", [])}
            self._confirmed = {tuple(x) for x in data.get("confirmed", [])}
        except (json.JSONDecodeError, OSError):
            pass

    def _save_cache(self) -> None:
        _SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(
            json.dumps(
                {
                    "failed": [list(x) for x in self._failed],
                    "confirmed": [list(x) for x in self._confirmed],
                },
                indent=2,
            )
        )

    def mark_failed(self, username: str, password: str, host: str) -> None:
        """Record that a credential did NOT work against a host."""
        self._failed.add((username, password, host))
        self._save_cache()

    def mark_confirmed(self, username: str, password: str, host: str) -> None:
        """Record that a credential worked against a host."""
        self._confirmed.add((username, password, host))
        self._failed.discard((username, password, host))
        self._save_cache()

    def _subnet_distance(self, ip_a: str, ip_b: str) -> int:
        """Return the CIDR prefix-length similarity between two IPs.

        Returns the longest prefix they share (0-32). Higher = closer.
        """
        try:
            a = ipaddress.ip_address(ip_a)
            b = ipaddress.ip_address(ip_b)
            if a.version != b.version:
                return 0
            if a.version == 4:
                a_int = int(a)
                b_int = int(b)
                xor = a_int ^ b_int
                if xor == 0:
                    return 32
                return 32 - xor.bit_length()
            a_int = int(a)
            b_int = int(b)
            xor = a_int ^ b_int
            if xor == 0:
                return 128
            return 128 - xor.bit_length()
        except ValueError:
            return 0

    def _score_candidate(
        self,
        username: str,
        password: str,
        source_host: str,
        target_host: str,
        target_services: list[dict[str, Any]] | None = None,
    ) -> float:
        """Compute a reuse score (0.0-1.0) for (cred, host).

        Scoring factors:
        - Same subnet: +0.4
        - Adjacent /24: +0.2
        - Confirmed on source: +0.3
        - Previously failed: -1.0 (instant reject)
        - SMB/445 open on target: +0.15
        - WinRM/5985 open on target: +0.1
        - Already confirmed: skip (return -1.0)
        """
        key = (username, password, target_host)
        if key in self._failed:
            return -1.0
        if key in self._confirmed:
            return -1.0

        score = 0.0
        dist = self._subnet_distance(source_host, target_host)

        if dist >= 24:
            score += 0.4
        elif dist >= 16:
            score += 0.2
        elif dist >= 8:
            score += 0.1

        source_confirmed = (username, password, source_host) in self._confirmed
        if source_confirmed:
            score += 0.3

        if target_services:
            open_ports = {s.get("port") for s in target_services}
            if 445 in open_ports:
                score += 0.15
            if 5985 in open_ports or 5986 in open_ports:
                score += 0.1
            if 22 in open_ports:
                score += 0.05
            if 389 in open_ports or 636 in open_ports:
                score += 0.1

        return min(score, 1.0)

    def _build_command(
        self,
        username: str,
        password: str,
        host: str,
        target_services: list[dict[str, Any]] | None = None,
    ) -> str:
        """Generate the best crackmapexec command for the target."""
        if target_services:
            open_ports = {s.get("port") for s in target_services}
            if 445 in open_ports:
                proto = "smb"
            elif 5985 in open_ports or 5986 in open_ports:
                proto = "winrm"
            elif 22 in open_ports:
                proto = "ssh"
            elif 1433 in open_ports:
                proto = "mssql"
            elif 389 in open_ports or 636 in open_ports:
                proto = "ldap"
            elif 3389 in open_ports:
                proto = "rdp"
            else:
                proto = "smb"
        else:
            proto = "smb"

        template = self._SPRAY_PROTOCOLS.get(proto, self._SPRAY_PROTOCOLS["smb"])
        return template.format(host=host, user=username, passwd=password)

    def rank(
        self,
        hosts: list[str],
        creds: list[dict[str, Any]],
        host_services: dict[str, list[dict[str, Any]]] | None = None,
        limit: int = 20,
    ) -> list[ReuseCandidate]:
        """Score all (cred, host) pairs and return top candidates.

        Args:
            hosts: Discovered target IP addresses.
            creds: Credential dicts with ``username``, ``password``, ``host`` keys.
            host_services: Optional mapping of host -> list of service dicts
                (ports, protocols) for protocol-aware scoring.
            limit: Maximum number of candidates to return.

        Returns:
            Sorted list of :class:`ReuseCandidate`, highest score first.
        """
        candidates: list[ReuseCandidate] = []

        for cred in creds:
            username = cred.get("username", "")
            password = cred.get("password", "")
            if not username or not password:
                continue
            source_host = cred.get("host", "")

            for target_host in hosts:
                if target_host == source_host:
                    continue

                services = (host_services or {}).get(target_host)
                score = self._score_candidate(
                    username, password, source_host, target_host, services
                )
                if score < 0:
                    continue

                command = self._build_command(username, password, target_host, services)
                candidates.append(
                    ReuseCandidate(
                        username=username,
                        password=password,
                        target_host=target_host,
                        source_host=source_host,
                        score=round(score, 3),
                        command=command,
                    )
                )

        candidates.sort(key=lambda c: c.score, reverse=True)
        return candidates[:limit]

    def suggest_from_state_manager(
        self,
        state_manager: Any,
        limit: int = 20,
    ) -> list[ReuseCandidate]:
        """Convenience: rank creds using hosts and creds from StateManager.

        Args:
            state_manager: An instance of :class:`StateManager`.
            limit: Max candidates.

        Returns:
            Sorted list of :class:`ReuseCandidate`.
        """
        all_hosts = state_manager.list_hosts()
        all_creds = state_manager.list_credentials()

        hosts = [h["address"] for h in all_hosts if h.get("address")]

        host_services: dict[str, list[dict[str, Any]]] = {}
        for h in all_hosts:
            addr = h.get("address", "")
            if not addr:
                continue
            host_data = state_manager.get_host(addr)
            if host_data:
                host_services[addr] = host_data.get("services", [])

        return self.rank(hosts, all_creds, host_services, limit)

    def suggest_from_world_model(
        self,
        world_model: Any,
        limit: int = 20,
    ) -> list[ReuseCandidate]:
        """Convenience: rank creds using hosts and creds from WorldModel.

        Args:
            world_model: An instance of :class:`WorldModel`.
            limit: Max candidates.

        Returns:
            Sorted list of :class:`ReuseCandidate`.
        """
        hosts = list(world_model._hosts.keys())
        creds = [
            {
                "username": c.value.split(":", 1)[0] if ":" in c.value else c.value,
                "password": c.value.split(":", 1)[1] if ":" in c.value else "",
                "host": c.host,
            }
            for c in world_model._creds
        ]

        host_services: dict[str, list[dict[str, Any]]] = {}
        for host_ip, entry in world_model._hosts.items():
            host_services[host_ip] = [
                {"port": s.port, "name": s.name}
                for s in entry.services
            ]

        return self.rank(hosts, creds, host_services, limit)

    def get_summary(self, candidates: list[ReuseCandidate]) -> str:
        """Format candidates as a human-readable summary string."""
        if not candidates:
            return "No credential reuse candidates available."

        lines = ["Credential Reuse Candidates (top {})".format(len(candidates))]
        lines.append("=" * 60)

        for i, c in enumerate(candidates, 1):
            lines.append(
                f"\n#{i}  score={c.score:.2f}  "
                f"{c.username}:{c.password}  "
                f"from {c.source_host} -> {c.target_host}"
            )
            lines.append(f"    {c.command}")

        return "\n".join(lines)


_GLOBAL_ENGINE: CredentialReuseEngine | None = None


def get_credential_reuse_engine() -> CredentialReuseEngine:
    """Return the singleton :class:`CredentialReuseEngine`."""
    global _GLOBAL_ENGINE
    if _GLOBAL_ENGINE is None:
        _GLOBAL_ENGINE = CredentialReuseEngine()
    return _GLOBAL_ENGINE
