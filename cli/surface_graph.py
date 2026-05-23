"""Network surface graph reader for the LazyOwn shell.

Mirrors the ``vis.js`` graph rendered by ``templates/index.html`` (consumed
by ``lazyc2.py``), but works entirely from the filesystem artefacts inside
``sessions/`` so the cmd2 shell can render the same picture without
running the Flask server.

The graph has the same five-node taxonomy as the web UI:

* ``c2``      — the LazyOwn operator station (root).
* ``client``  — an active implant (one ``sessions/<client_id>.log`` file).
* ``host``    — a discovered remote host (from ``hostsdiscovery.txt`` or
                 ``scan_discovery*.csv``, or surfaced via an implant's
                 ``discovered_ips`` column).
* ``port``    — an open TCP/UDP port on a discovered host.
* ``service`` — banner/version metadata attached to a port when known.

Data sources, in priority order:

* ``sessions/hostsdiscovery.txt``        — newline-delimited IPs.
* ``sessions/scan_discovery_*.csv``      — ``;``-quoted IP/PORT/SERVICE.
* ``sessions/<client_id>.log``           — per-implant CSV with the
                                           ``discovered_ips`` and
                                           ``result_portscan`` columns.
* ``payload.json``                       — local C2 host/port (``lhost``,
                                           ``c2_port``) for the root node.
* ``sessions/os.json``                   — current target OS hint.

The module is pure data: it returns plain dataclasses + ``to_dict`` so the
result is equally usable from a Rich/Textual renderer, an MCP response or
a unit test.
"""

from __future__ import annotations

import csv
import glob
import json
import os
import re
import socket
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

HOSTSDISCOVERY_FILENAME: str = "hostsdiscovery.txt"
SCAN_DISCOVERY_GLOB: str = "scan_discovery*.csv"
SCAN_DISCOVERY_DELIMITER: str = ";"
IMPLANT_LOG_SUFFIX: str = ".log"
IMPLANT_HEADER_REQUIRED: frozenset[str] = frozenset({"client_id", "os", "ips", "discovered_ips", "result_portscan"})
LOCAL_IP_FALLBACK: str = "127.0.0.1"
PRIVATE_LOOPBACK: str = "127.0.0.1"
PAYLOAD_FILENAME: str = "payload.json"
OS_HINT_FILENAME: str = "os.json"

NODE_C2: str = "c2"
NODE_KIND_C2: str = "c2"
NODE_KIND_CLIENT: str = "client"
NODE_KIND_HOST: str = "host"
NODE_KIND_PORT: str = "port"
NODE_KIND_SERVICE: str = "service"

EDGE_CONTROLS: str = "controls"
EDGE_DISCOVERED: str = "discovered"
EDGE_OPENS: str = "opens"
EDGE_RUNS: str = "runs"

_IPV4_RE = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def _slug_host(ip: str) -> str:
    """Return the canonical ``host-<dotted-ip>`` id used by the web graph."""
    return "host-" + ip.replace(".", "-")


def _slug_port(host_id: str, port: str, protocol: str) -> str:
    """Return a stable port-node id rooted at ``host_id``."""
    proto = (protocol or "tcp").lower() or "tcp"
    return f"port-{host_id}-{proto}-{port}"


@dataclass(frozen=True)
class SurfaceNode:
    """A node in the network surface graph.

    Args:
        id: Stable string identifier (e.g. ``host-10-0-0-1``).
        kind: One of ``c2``, ``client``, ``host``, ``port``, ``service``.
        label: Human-readable label rendered in the TUI.
        metadata: Free-form structured attributes from the source file.
    """

    id: str
    kind: str
    label: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable view of the node."""
        return {
            "id": self.id,
            "kind": self.kind,
            "label": self.label,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class SurfaceEdge:
    """A directed edge between two surface nodes."""

    source: str
    target: str
    relation: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-serialisable view of the edge."""
        return {"source": self.source, "target": self.target, "relation": self.relation}


@dataclass(frozen=True)
class SurfaceGraph:
    """Aggregate snapshot of nodes + edges discovered on disk."""

    nodes: list[SurfaceNode]
    edges: list[SurfaceEdge]
    local_ips: list[str]
    sessions_dir: str
    payload_path: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable view (mirrors the web UI payload)."""
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "local_ips": list(self.local_ips),
            "sessions_dir": self.sessions_dir,
            "payload_path": self.payload_path,
            "stats": self.stats(),
        }

    def stats(self) -> dict[str, int]:
        """Return per-kind node counts plus edge count."""
        counts: dict[str, int] = {"edges": len(self.edges)}
        for node in self.nodes:
            counts[node.kind] = counts.get(node.kind, 0) + 1
        return counts

    def children_of(self, node_id: str) -> list[SurfaceNode]:
        """Return nodes that ``node_id`` points to via an outgoing edge."""
        by_id = {node.id: node for node in self.nodes}
        children: list[SurfaceNode] = []
        for edge in self.edges:
            if edge.source != node_id:
                continue
            child = by_id.get(edge.target)
            if child is not None:
                children.append(child)
        return children

    def get(self, node_id: str) -> SurfaceNode | None:
        """Return the node with ``node_id`` or ``None``."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None


@dataclass(frozen=True)
class SurfaceGraphConfig:
    """Configuration for :class:`SurfaceGraphBuilder`.

    Args:
        sessions_dir: Path to the ``sessions/`` directory.
        payload_path: Path to ``payload.json`` (read for ``lhost``,
            ``c2_port``).
        include_local_ips_as_hosts: When true, attach each local IP as a
            ``host`` node so the C2 is visible alongside the targets.
        skip_log_basenames: Implant logs that should never be treated as
            beacons (e.g. ``access``).
    """

    sessions_dir: str = "sessions"
    payload_path: str = PAYLOAD_FILENAME
    include_local_ips_as_hosts: bool = False
    skip_log_basenames: tuple[str, ...] = (
        "access",
        "ai_model",
    )


class SurfaceGraphBuilder:
    """Compose a :class:`SurfaceGraph` from on-disk session artefacts."""

    def __init__(self, config: SurfaceGraphConfig | None = None) -> None:
        self._cfg = config or SurfaceGraphConfig()

    def build(self) -> SurfaceGraph:
        """Read every session artefact and return the assembled graph."""
        local_ips = self._discover_local_ips()
        payload = self._load_payload()

        nodes: dict[str, SurfaceNode] = {}
        edges: list[SurfaceEdge] = []

        nodes[NODE_C2] = self._build_c2_node(local_ips, payload)

        for client_id, client_meta in self._read_implants().items():
            client_node_id = client_id
            nodes[client_node_id] = SurfaceNode(
                id=client_node_id,
                kind=NODE_KIND_CLIENT,
                label=self._client_label(client_id, client_meta),
                metadata=client_meta,
            )
            edges.append(SurfaceEdge(NODE_C2, client_node_id, EDGE_CONTROLS))

            for host_ip in client_meta.get("discovered_ip_list", []):
                host_id = _slug_host(host_ip)
                if host_id not in nodes:
                    nodes[host_id] = SurfaceNode(
                        id=host_id,
                        kind=NODE_KIND_HOST,
                        label=host_ip,
                        metadata={"ip": host_ip, "discovered_by": client_id},
                    )
                edges.append(SurfaceEdge(client_node_id, host_id, EDGE_DISCOVERED))

            for host_ip, ports in client_meta.get("port_map", {}).items():
                host_id = _slug_host(host_ip)
                if host_id not in nodes:
                    nodes[host_id] = SurfaceNode(
                        id=host_id,
                        kind=NODE_KIND_HOST,
                        label=host_ip,
                        metadata={"ip": host_ip, "discovered_by": client_id},
                    )
                    edges.append(SurfaceEdge(client_node_id, host_id, EDGE_DISCOVERED))
                for port in ports:
                    port_id = _slug_port(host_id, str(port), "tcp")
                    if port_id in nodes:
                        continue
                    nodes[port_id] = SurfaceNode(
                        id=port_id,
                        kind=NODE_KIND_PORT,
                        label=str(port),
                        metadata={"port": int(port), "protocol": "tcp", "host_ip": host_ip},
                    )
                    edges.append(SurfaceEdge(host_id, port_id, EDGE_OPENS))

        for host_ip in self._read_hostsdiscovery(local_ips):
            host_id = _slug_host(host_ip)
            if host_id in nodes:
                continue
            nodes[host_id] = SurfaceNode(
                id=host_id,
                kind=NODE_KIND_HOST,
                label=host_ip,
                metadata={"ip": host_ip, "source": HOSTSDISCOVERY_FILENAME},
            )
            edges.append(SurfaceEdge(NODE_C2, host_id, EDGE_DISCOVERED))

        for record in self._read_scan_discovery(local_ips):
            host_ip = record["ip"]
            host_id = _slug_host(host_ip)
            if host_id not in nodes:
                nodes[host_id] = SurfaceNode(
                    id=host_id,
                    kind=NODE_KIND_HOST,
                    label=host_ip,
                    metadata={"ip": host_ip, "source": SCAN_DISCOVERY_GLOB},
                )
                edges.append(SurfaceEdge(NODE_C2, host_id, EDGE_DISCOVERED))
            fqdn = record.get("fqdn") or ""
            if fqdn and "fqdn" not in nodes[host_id].metadata:
                merged = dict(nodes[host_id].metadata)
                merged["fqdn"] = fqdn
                nodes[host_id] = SurfaceNode(
                    id=nodes[host_id].id,
                    kind=nodes[host_id].kind,
                    label=f"{host_ip} ({fqdn})",
                    metadata=merged,
                )
            port = record.get("port") or ""
            if not port:
                continue
            protocol = (record.get("protocol") or "tcp").lower()
            port_id = _slug_port(host_id, port, protocol)
            if port_id not in nodes:
                nodes[port_id] = SurfaceNode(
                    id=port_id,
                    kind=NODE_KIND_PORT,
                    label=f"{port}/{protocol}",
                    metadata={
                        "port": int(port) if port.isdigit() else port,
                        "protocol": protocol,
                        "host_ip": host_ip,
                    },
                )
                edges.append(SurfaceEdge(host_id, port_id, EDGE_OPENS))
            service = record.get("service") or ""
            version = record.get("version") or ""
            if service:
                service_id = f"{port_id}-svc"
                if service_id not in nodes:
                    nodes[service_id] = SurfaceNode(
                        id=service_id,
                        kind=NODE_KIND_SERVICE,
                        label=f"{service} {version}".strip(),
                        metadata={"service": service, "version": version, "host_ip": host_ip, "port": port},
                    )
                    edges.append(SurfaceEdge(port_id, service_id, EDGE_RUNS))

        ordered_nodes = sorted(
            nodes.values(),
            key=lambda n: (self._kind_order(n.kind), n.label.lower()),
        )
        return SurfaceGraph(
            nodes=ordered_nodes,
            edges=edges,
            local_ips=list(local_ips),
            sessions_dir=self._cfg.sessions_dir,
            payload_path=self._cfg.payload_path,
        )

    @staticmethod
    def _kind_order(kind: str) -> int:
        order = {
            NODE_KIND_C2: 0,
            NODE_KIND_CLIENT: 1,
            NODE_KIND_HOST: 2,
            NODE_KIND_PORT: 3,
            NODE_KIND_SERVICE: 4,
        }
        return order.get(kind, 9)

    def _build_c2_node(self, local_ips: list[str], payload: dict[str, Any]) -> SurfaceNode:
        label_parts = ["C&C LazyOwn"]
        if local_ips:
            label_parts.append(", ".join(local_ips))
        metadata: dict[str, Any] = {
            "local_ips": list(local_ips),
            "lhost": payload.get("lhost") or "",
            "c2_port": payload.get("c2_port") or "",
            "domain": payload.get("domain") or "",
            "os_target": self._read_os_hint(),
        }
        return SurfaceNode(
            id=NODE_C2,
            kind=NODE_KIND_C2,
            label=" — ".join(label_parts),
            metadata=metadata,
        )

    def _discover_local_ips(self) -> list[str]:
        ips: list[str] = []
        try:
            result = subprocess.run(["ip", "addr"], capture_output=True, text=True, check=True, timeout=5)
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            return self._fallback_local_ips()
        for line in result.stdout.splitlines():
            if "inet " not in line:
                continue
            parts = line.split()
            if len(parts) < 2 or "/" not in parts[1]:
                continue
            ip_address = parts[1].split("/")[0]
            if ip_address == PRIVATE_LOOPBACK:
                continue
            if any(prefix in line for prefix in ("docker", "veth")):
                continue
            ips.append(ip_address)
        return ips or self._fallback_local_ips()

    @staticmethod
    def _fallback_local_ips() -> list[str]:
        try:
            return [socket.gethostbyname(socket.gethostname())]
        except OSError:
            return [LOCAL_IP_FALLBACK]

    def _load_payload(self) -> dict[str, Any]:
        path = Path(self._cfg.payload_path)
        if not path.exists():
            return {}
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return {}
        if isinstance(data, list):
            return data[0] if data and isinstance(data[0], dict) else {}
        return data if isinstance(data, dict) else {}

    def _read_os_hint(self) -> str:
        path = Path(self._cfg.sessions_dir) / OS_HINT_FILENAME
        if not path.exists():
            return ""
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return ""
        if isinstance(data, dict):
            return str(data.get("os") or data.get("name") or "")
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return str(data[0].get("os") or data[0].get("name") or "")
        return ""

    def _read_hostsdiscovery(self, local_ips: list[str]) -> list[str]:
        path = Path(self._cfg.sessions_dir) / HOSTSDISCOVERY_FILENAME
        if not path.exists():
            return []
        out: list[str] = []
        try:
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    ip = line.strip()
                    if not ip or ip in local_ips or not self._is_ipv4(ip):
                        continue
                    if ip not in out:
                        out.append(ip)
        except OSError:
            return []
        return out

    def _read_scan_discovery(self, local_ips: list[str]) -> list[dict[str, str]]:
        pattern = os.path.join(self._cfg.sessions_dir, SCAN_DISCOVERY_GLOB)
        records: list[dict[str, str]] = []
        for csv_path in sorted(glob.glob(pattern)):
            try:
                with open(csv_path, "r", encoding="utf-8", errors="ignore") as fh:
                    reader = csv.reader(fh, delimiter=SCAN_DISCOVERY_DELIMITER, quotechar='"')
                    headers: list[str] = []
                    for row in reader:
                        if not row or all(not col.strip() for col in row):
                            continue
                        if not headers:
                            headers = [col.strip().lower() for col in row]
                            continue
                        record = {
                            headers[i]: row[i].strip() for i in range(min(len(headers), len(row))) if row[i] is not None
                        }
                        ip = record.get("ip", "")
                        if not ip or ip in local_ips or not self._is_ipv4(ip):
                            continue
                        records.append(record)
            except (OSError, csv.Error):
                continue
        return records

    def _read_implants(self) -> dict[str, dict[str, Any]]:
        sessions_dir = Path(self._cfg.sessions_dir)
        if not sessions_dir.exists():
            return {}
        implants: dict[str, dict[str, Any]] = {}
        for log_path in sorted(sessions_dir.glob(f"*{IMPLANT_LOG_SUFFIX}")):
            stem = log_path.stem
            if stem in self._cfg.skip_log_basenames:
                continue
            if "_searchsploit" in stem or stem.startswith("scan_"):
                continue
            last_row = self._read_last_implant_row(log_path)
            if last_row is None:
                continue
            implants[stem] = self._parse_implant_row(last_row)
        return implants

    def _read_last_implant_row(self, path: Path) -> dict[str, str] | None:
        try:
            with path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
                reader = csv.DictReader(fh)
                if reader.fieldnames is None:
                    return None
                header = {name.strip() for name in reader.fieldnames if name}
                if not IMPLANT_HEADER_REQUIRED.issubset(header):
                    return None
                last: dict[str, str] | None = None
                for row in reader:
                    if row:
                        last = row
                return last
        except (OSError, csv.Error, UnicodeError):
            return None

    def _parse_implant_row(self, row: dict[str, str]) -> dict[str, Any]:
        discovered_raw = (row.get("discovered_ips") or "").strip()
        discovered = [
            chunk.strip()
            for chunk in discovered_raw.replace(";", ",").split(",")
            if chunk.strip() and self._is_ipv4(chunk.strip())
        ]
        port_map = self._parse_port_scan(row.get("result_portscan") or "")
        return {
            "client_id": (row.get("client_id") or "").strip(),
            "os": (row.get("os") or "").strip(),
            "pid": (row.get("pid") or "").strip(),
            "hostname": (row.get("hostname") or "").strip(),
            "ips": (row.get("ips") or "").strip(),
            "user": (row.get("user") or "").strip(),
            "discovered_ips_raw": discovered_raw,
            "discovered_ip_list": discovered,
            "port_map": port_map,
            "last_command": (row.get("command") or "").strip(),
        }

    def _parse_port_scan(self, raw: str) -> dict[str, list[int]]:
        if not raw or raw.strip().lower() in {"none", "null", ""}:
            return {}
        candidate = raw.strip()
        try:
            parsed = json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            normalised = candidate.replace("'", '"')
            try:
                parsed = json.loads(normalised)
            except (json.JSONDecodeError, ValueError):
                return {}
        if not isinstance(parsed, dict):
            return {}
        out: dict[str, list[int]] = {}
        for ip, ports in parsed.items():
            if not isinstance(ip, str) or not self._is_ipv4(ip):
                continue
            if not isinstance(ports, (list, tuple)):
                continue
            cleaned: list[int] = []
            seen: set[int] = set()
            for port in ports:
                try:
                    value = int(port)
                except (TypeError, ValueError):
                    continue
                if value in seen:
                    continue
                seen.add(value)
                cleaned.append(value)
            if cleaned:
                out[ip] = cleaned
        return out

    @staticmethod
    def _is_ipv4(value: str) -> bool:
        if not _IPV4_RE.match(value):
            return False
        return all(0 <= int(octet) <= 255 for octet in value.split("."))

    @staticmethod
    def _client_label(client_id: str, meta: dict[str, Any]) -> str:
        bits = [f"Implant {client_id[:10]}"]
        if meta.get("os"):
            bits.append(f"OS/{meta['os']}")
        if meta.get("hostname"):
            bits.append(f"@{meta['hostname']}")
        if meta.get("user"):
            bits.append(f"u={meta['user']}")
        return " ".join(bits)


def build_surface_graph(
    sessions_dir: str = "sessions",
    payload_path: str = PAYLOAD_FILENAME,
) -> SurfaceGraph:
    """Convenience factory: build a graph from on-disk artefacts.

    Args:
        sessions_dir: Path to the LazyOwn sessions directory.
        payload_path: Path to ``payload.json``.

    Returns:
        A populated :class:`SurfaceGraph`.
    """
    cfg = SurfaceGraphConfig(sessions_dir=sessions_dir, payload_path=payload_path)
    return SurfaceGraphBuilder(cfg).build()


def iter_descendants(graph: SurfaceGraph, root_id: str) -> Iterable[SurfaceNode]:
    """Yield every node reachable from ``root_id`` via outgoing edges."""
    visited: set[str] = set()
    queue: list[str] = [root_id]
    while queue:
        current_id = queue.pop(0)
        for child in graph.children_of(current_id):
            if child.id in visited:
                continue
            visited.add(child.id)
            yield child
            queue.append(child.id)


__all__ = [
    "EDGE_CONTROLS",
    "EDGE_DISCOVERED",
    "EDGE_OPENS",
    "EDGE_RUNS",
    "NODE_C2",
    "NODE_KIND_C2",
    "NODE_KIND_CLIENT",
    "NODE_KIND_HOST",
    "NODE_KIND_PORT",
    "NODE_KIND_SERVICE",
    "SurfaceEdge",
    "SurfaceGraph",
    "SurfaceGraphBuilder",
    "SurfaceGraphConfig",
    "SurfaceNode",
    "build_surface_graph",
    "iter_descendants",
]
