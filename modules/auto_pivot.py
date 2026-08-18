"""Auto-Pivoting Engine for LazyOwn.

Automated lateral movement through compromised hosts:
- Multi-hop SOCKS proxy chaining
- Subnet discovery via compromised host perspective
- Route maintenance with health checks
- Automatic credential re-use across hops
"""

from __future__ import annotations

import json
import socket
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


@dataclass
class PivotNode:
    ip: str
    hostname: str
    access_level: str
    credential_id: str
    pivot_port: int
    socket_type: str  # "socks4", "socks5", "http", "chisel", "ligolo"
    status: str  # "active", "stale", "dead"
    discovered_subnets: list[str] = field(default_factory=list)
    reachable_hosts: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    last_seen: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    route_priority: int = 50


@dataclass
class PivotChain:
    chain_id: str
    nodes: list[PivotNode] = field(default_factory=list)
    entry_point: str = ""
    target_subnet: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class AutoPivotEngine:
    """Manages automated pivoting through compromised hosts.

    Attributes:
        config: Reference to payload.json configuration.
        sessions_dir: Directory for persisting pivot state.
    """

    __slots__ = (
        "_config",
        "_sessions_dir",
        "_pivot_nodes",
        "_active_chains",
        "_port_counter",
        "_socks_base_port",
    )

    _SOCKS_BASE_PORT = 1080
    _MAX_PORTS = 20
    _HEALTH_CHECK_INTERVAL = 30
    _SUBNET_PATTERNS = [
        "192.168.0.0/16",
        "172.16.0.0/12",
        "10.0.0.0/8",
    ]

    def __init__(self, config: Any = None) -> None:
        self._config = config
        self._sessions_dir = SESSIONS_DIR
        self._pivot_nodes: dict[str, PivotNode] = {}
        self._active_chains: dict[str, PivotChain] = {}
        self._port_counter = 0
        self._socks_base_port = self._SOCKS_BASE_PORT
        self._load_state()

    def set_config(self, config: Any) -> None:
        self._config = config

    def _next_port(self) -> int:
        port = self._socks_base_port + self._port_counter
        self._port_counter = (self._port_counter + 1) % self._MAX_PORTS
        return port

    def add_pivot_node(
        self,
        ip: str,
        access_type: str = "ssh",
        credential_id: str = "",
        hostname: str = "",
    ) -> PivotNode:
        socket_type = "socks5"
        if access_type in ("ssh",):
            socket_type = "socks5"
        elif access_type in ("winrm", "psexec"):
            socket_type = "http"
        elif access_type in ("chisel",):
            socket_type = "chisel"
        elif access_type in ("ligolo",):
            socket_type = "ligolo"

        node = PivotNode(
            ip=ip,
            hostname=hostname or ip,
            access_level=access_type,
            credential_id=credential_id,
            pivot_port=self._next_port(),
            socket_type=socket_type,
            status="active",
        )
        self._pivot_nodes[ip] = node
        self._persist_state()
        return node

    def remove_pivot_node(self, ip: str) -> None:
        self._pivot_nodes.pop(ip, None)
        for chain in list(self._active_chains.values()):
            chain.nodes = [n for n in chain.nodes if n.ip != ip]
            if not chain.nodes:
                del self._active_chains[chain.chain_id]
        self._persist_state()

    def discover_subnets(self, node_ip: str, command_output: str) -> list[str]:
        discovered: list[str] = []
        for pattern in self._SUBNET_PATTERNS:
            if pattern.split("/")[0].replace(".0", "") in command_output:
                discovered.append(pattern)
        import re as _re
        ip_pattern = _re.compile(r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b")
        private_ips = set(ip_pattern.findall(command_output))
        for ip_addr in private_ips:
            if ip_addr != node_ip:
                discovered.append(f"{ip_addr}/32")

        if node_ip in self._pivot_nodes:
            self._pivot_nodes[node_ip].discovered_subnets = list(set(discovered))
        self._persist_state()
        return discovered

    def build_chain(
        self,
        target_ip: str,
        via_nodes: list[str] | None = None,
        subnet: str = "",
    ) -> PivotChain | None:
        if via_nodes:
            nodes = [self._pivot_nodes[n] for n in via_nodes if n in self._pivot_nodes]
        else:
            candidates = sorted(
                self._pivot_nodes.values(),
                key=lambda n: n.route_priority,
                reverse=True,
            )
            nodes = [candidates[0]] if candidates else []

        if not nodes:
            return None

        import secrets as _secrets
        chain = PivotChain(
            chain_id=_secrets.token_hex(8),
            nodes=nodes,
            entry_point=nodes[0].ip,
            target_subnet=subnet,
        )
        self._active_chains[chain.chain_id] = chain
        self._persist_state()
        return chain

    def generate_proxychains_config(
        self, chain_id: str | None = None
    ) -> str:
        nodes: list[PivotNode] = []
        if chain_id and chain_id in self._active_chains:
            nodes = self._active_chains[chain_id].nodes
        else:
            active = [n for n in self._pivot_nodes.values() if n.status == "active"]
            nodes = sorted(active, key=lambda n: n.pivot_port)

        if not nodes:
            return ""

        lines = [
            "[ProxyList]",
            "strict_chain",
            "tcp_read_time_out 15000",
            "tcp_connect_time_out 8000",
        ]
        for node in nodes:
            if node.socket_type == "socks5":
                lines.append(f"socks5 {node.ip} {node.pivot_port}")
            elif node.socket_type == "socks4":
                lines.append(f"socks4 {node.ip} {node.pivot_port}")
            elif node.socket_type == "http":
                lines.append(f"http {node.ip} {node.pivot_port}")
        return "\n".join(lines)

    def generate_sshuttle_command(self, node_ip: str, subnet: str) -> str:
        return f"sshuttle -r {node_ip} {subnet}"

    def generate_chisel_command(
        self, target_ip: str, local_port: int | None = None
    ) -> tuple[str, str]:
        lp = local_port or self._next_port()
        server_cmd = f"chisel server -p {lp} --reverse"
        client_cmd = f"chisel client {target_ip}:{lp} R:socks"
        return server_cmd, client_cmd

    def generate_ssh_socks_command(self, node_ip: str, local_port: int | None = None) -> str:
        lp = local_port or self._next_port()
        return f"ssh -D {lp} -N -f {node_ip}"

    def health_check(self, node_ip: str) -> str:
        node = self._pivot_nodes.get(node_ip)
        if not node:
            return "unknown"

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((node.ip, node.pivot_port))
            sock.close()
            if result == 0:
                node.status = "active"
                node.last_seen = datetime.now(UTC).isoformat()
            else:
                node.status = "stale"
        except (TimeoutError, socket.gaierror, ConnectionRefusedError, OSError):
            node.status = "dead"

        self._persist_state()
        return node.status

    def health_check_all(self) -> dict[str, str]:
        results: dict[str, str] = {}
        for ip in list(self._pivot_nodes.keys()):
            results[ip] = self.health_check(ip)
        return results

    def get_active_routes(self) -> list[dict[str, Any]]:
        routes: list[dict[str, Any]] = []
        for node in self._pivot_nodes.values():
            if node.status == "active":
                routes.append({
                    "ip": node.ip,
                    "port": node.pivot_port,
                    "type": node.socket_type,
                    "access": node.access_level,
                    "subnets": node.discovered_subnets,
                    "route_priority": node.route_priority,
                })
        return sorted(routes, key=lambda r: r["route_priority"], reverse=True)

    def get_reachable_hosts(self, node_ip: str | None = None) -> list[str]:
        if node_ip and node_ip in self._pivot_nodes:
            return self._pivot_nodes[node_ip].reachable_hosts
        all_hosts: set[str] = set()
        for node in self._pivot_nodes.values():
            all_hosts.update(node.reachable_hosts)
        return sorted(all_hosts)

    def set_reachable_hosts(self, node_ip: str, hosts: list[str]) -> None:
        if node_ip in self._pivot_nodes:
            self._pivot_nodes[node_ip].reachable_hosts = hosts
            self._persist_state()

    def set_route_priority(self, node_ip: str, priority: int) -> None:
        if node_ip in self._pivot_nodes:
            self._pivot_nodes[node_ip].route_priority = max(0, min(100, priority))
            self._persist_state()

    def _persist_state(self) -> Path:
        self._sessions_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "updated_at": datetime.now(UTC).isoformat(),
            "nodes": {
                ip: {
                    "ip": n.ip,
                    "hostname": n.hostname,
                    "access_level": n.access_level,
                    "credential_id": n.credential_id,
                    "pivot_port": n.pivot_port,
                    "socket_type": n.socket_type,
                    "status": n.status,
                    "discovered_subnets": n.discovered_subnets,
                    "reachable_hosts": n.reachable_hosts,
                    "route_priority": n.route_priority,
                    "created_at": n.created_at,
                    "last_seen": n.last_seen,
                }
                for ip, n in self._pivot_nodes.items()
            },
            "chains": {
                cid: {
                    "chain_id": c.chain_id,
                    "entry_point": c.entry_point,
                    "target_subnet": c.target_subnet,
                    "node_ips": [n.ip for n in c.nodes],
                    "created_at": c.created_at,
                }
                for cid, c in self._active_chains.items()
            },
        }
        target = self._sessions_dir / "pivot_state.json"
        with target.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
        return target

    def _load_state(self) -> None:
        state_path = self._sessions_dir / "pivot_state.json"
        if not state_path.exists():
            return
        try:
            with state_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            for ip, node_data in data.get("nodes", {}).items():
                self._pivot_nodes[ip] = PivotNode(
                    ip=node_data["ip"],
                    hostname=node_data.get("hostname", ip),
                    access_level=node_data.get("access_level", "ssh"),
                    credential_id=node_data.get("credential_id", ""),
                    pivot_port=node_data.get("pivot_port", self._next_port()),
                    socket_type=node_data.get("socket_type", "socks5"),
                    status=node_data.get("status", "stale"),
                    discovered_subnets=node_data.get("discovered_subnets", []),
                    reachable_hosts=node_data.get("reachable_hosts", []),
                    route_priority=node_data.get("route_priority", 50),
                    created_at=node_data.get("created_at", ""),
                    last_seen=node_data.get("last_seen", ""),
                )
                self._port_counter = max(
                    self._port_counter,
                    (self._pivot_nodes[ip].pivot_port - self._socks_base_port + 1)
                    % self._MAX_PORTS,
                )
            for chain_data in data.get("chains", {}).values():
                nodes = [
                    self._pivot_nodes[nip]
                    for nip in chain_data.get("node_ips", [])
                    if nip in self._pivot_nodes
                ]
                self._active_chains[chain_data["chain_id"]] = PivotChain(
                    chain_id=chain_data["chain_id"],
                    nodes=nodes,
                    entry_point=chain_data.get("entry_point", ""),
                    target_subnet=chain_data.get("target_subnet", ""),
                    created_at=chain_data.get("created_at", ""),
                )
        except (json.JSONDecodeError, KeyError):
            pass

    def suggest_next_pivot(self) -> dict[str, Any] | None:
        all_subnets: set[str] = set()
        for node in self._pivot_nodes.values():
            all_subnets.update(node.discovered_subnets)

        if not all_subnets:
            return None

        suggestions: list[dict[str, Any]] = []
        for subnet in all_subnets:
            gateway_ip = subnet.split("/")[0]
            if gateway_ip not in self._pivot_nodes:
                suggestions.append({
                    "target_subnet": subnet,
                    "via": max(
                        self._pivot_nodes.values(),
                        key=lambda n: n.route_priority,
                        default=None,
                    ),
                    "action": "scan_subnet",
                    "command": f"nmap -sn {subnet}",
                })

        return suggestions[0] if suggestions else None
