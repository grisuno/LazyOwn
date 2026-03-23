#!/usr/bin/env python3
"""
modules/world_model.py
=======================
Unified engagement world model for LazyOwn autonomous operations.

Tracks the state of every discovered host through a formal state machine,
aggregates credentials and vulnerabilities, derives the current engagement
phase, and produces a compact context string for LLM consumption.

Design principles
-----------------
- Single Responsibility : each class owns exactly one domain concept
- Open/Closed           : new host states or finding types via extension only
- Dependency Inversion  : depends on Finding abstraction, not ObsParser directly
- Thread-safe           : RLock guards all mutations; safe for Flask + MCP threads
- Persistent            : auto-saves to sessions/world_model.json on every mutation

Usage
-----
    from modules.world_model import WorldModel, HostState

    wm = WorldModel()
    wm.add_host("10.10.11.78")
    wm.advance_host(  "10.10.11.78", HostState.SCANNED)
    wm.add_service(   "10.10.11.78", port=80, name="http", version="Apache 2.4.49")
    wm.add_credential("administrator:P@ssw0rd!", host="10.10.11.78")

    print(wm.get_phase().value)       # -> "exploitation"
    print(wm.to_context_string())     # compact summary for LLM prompt

    # Called automatically after ObsParser runs:
    wm.update_from_findings(obs.findings)
"""
from __future__ import annotations

import json
import logging
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger("world_model")

_BASE_DIR     = Path(__file__).parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"
_DEFAULT_PATH = _SESSIONS_DIR / "world_model.json"


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

class HostState(str, Enum):
    """Ordered engagement states for a single host."""
    UNSCANNED   = "unscanned"
    SCANNED     = "scanned"       # nmap completed
    ENUMERATED  = "enumerated"    # services enumerated (gobuster, smb, ldap…)
    EXPLOITED   = "exploited"     # initial foothold obtained
    OWNED       = "owned"         # privilege escalation successful

    def rank(self) -> int:
        return list(HostState).index(self)

    def can_advance_to(self, next_state: "HostState") -> bool:
        return next_state.rank() == self.rank() + 1


class EngagementPhase(str, Enum):
    """Derived from the aggregate host state across all targets."""
    RECON            = "recon"
    SCANNING         = "scanning"
    ENUMERATION      = "enumeration"
    EXPLOITATION     = "exploitation"
    POST_EXPLOITATION = "post_exploitation"
    COMPLETE         = "complete"


@dataclass
class ServiceInfo:
    port:     int
    protocol: str  = "tcp"
    name:     str  = ""
    version:  str  = ""
    state:    str  = "open"


@dataclass
class CredentialEntry:
    value:     str                     # "user:pass" or hash
    host:      str  = ""
    service:   str  = ""
    confirmed: bool = False
    found_at:  str  = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class VulnerabilityEntry:
    description: str
    host:        str  = ""
    cve:         str  = ""
    severity:    str  = "UNKNOWN"
    found_at:    str  = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class NetworkRelation:
    """A directed, typed relationship between two network nodes.

    Node naming convention:
        host:<ip>          — a discovered host
        user:<username>    — a user account
        service:<name>     — a running service (e.g. service:smb)
        cred:<hash>        — a captured credential (first 12 chars)
    """
    source:     str
    target:     str
    relation:   str             # e.g. has_session, runs_service, shares_cred_with
    weight:     float = 1.0
    attributes: Dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Network graph (Graph-based reasoning layer)
# ---------------------------------------------------------------------------


class NetworkGraph:
    """
    Lightweight directed graph for network topology and lateral movement reasoning.

    Tracks typed relationships between hosts, users, services, and credentials
    and exposes degree-centrality analysis to identify pivot points without
    requiring an external graph library.

    Design
    ------
    - Single Responsibility : graph structure + centrality only; no I/O
    - Open/Closed           : new relation types added as data, not code
    - Thread-safe           : caller (WorldModel) holds its own RLock

    Centrality algorithm
    --------------------
    Normalized degree centrality:
        C(v) = (in_degree(v) + out_degree(v)) / (2 * (N - 1))

    A node with high centrality is reachable by and can reach many others —
    an ideal pivot candidate for lateral movement.
    """

    def __init__(self) -> None:
        # adjacency[source][target] = [NetworkRelation, ...]
        self._adjacency: Dict[str, Dict[str, List[NetworkRelation]]] = {}
        self._nodes: set = set()

    # ── Mutations ─────────────────────────────────────────────────────────────

    def add_relation(self, relation: NetworkRelation) -> None:
        """Add a directed edge. Duplicate edges accumulate (multi-graph)."""
        self._nodes.add(relation.source)
        self._nodes.add(relation.target)
        self._adjacency \
            .setdefault(relation.source, {}) \
            .setdefault(relation.target, []) \
            .append(relation)

    # ── Queries ───────────────────────────────────────────────────────────────

    def neighbors(self, node: str) -> List[str]:
        """Return nodes reachable from *node* in one outbound hop."""
        return list(self._adjacency.get(node, {}).keys())

    def in_degree(self, node: str) -> int:
        """Count edges pointing INTO *node*."""
        return sum(
            1 for targets in self._adjacency.values() if node in targets
        )

    def out_degree(self, node: str) -> int:
        """Count edges leaving *node*."""
        return len(self._adjacency.get(node, {}))

    def degree_centrality(self) -> List[tuple]:
        """
        Return (node, centrality_score) pairs sorted descending by score.
        Score is normalized to [0.0, 1.0] over all discovered nodes.
        """
        n = len(self._nodes)
        if n <= 1:
            return [(node, 0.0) for node in self._nodes]
        denominator = 2.0 * (n - 1)
        scores: Dict[str, float] = {}
        for node in self._nodes:
            total = self.in_degree(node) + self.out_degree(node)
            scores[node] = round(total / denominator, 4)
        return sorted(scores.items(), key=lambda kv: -kv[1])

    def pivot_candidates(self, top_k: int = 5) -> List[Dict]:
        """
        Return the *top_k* highest-centrality nodes as pivot candidates.
        The returned list is suitable for injection into an LLM prompt as
        strategic network context.
        """
        centrality = dict(self.degree_centrality())
        candidates: List[Dict] = []
        for node, score in sorted(
            centrality.items(), key=lambda kv: -kv[1]
        )[:top_k]:
            candidates.append({
                "node":       node,
                "centrality": score,
                "out_degree": self.out_degree(node),
                "in_degree":  self.in_degree(node),
                "neighbors":  self.neighbors(node)[:8],
            })
        return candidates

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        relations: List[dict] = []
        for src, targets in self._adjacency.items():
            for tgt, rels in targets.items():
                for r in rels:
                    relations.append({
                        "source":     r.source,
                        "target":     r.target,
                        "relation":   r.relation,
                        "weight":     r.weight,
                        "attributes": r.attributes,
                    })
        return {"nodes": list(self._nodes), "relations": relations}

    @classmethod
    def from_dict(cls, data: dict) -> "NetworkGraph":
        g = cls()
        for r in data.get("relations", []):
            g.add_relation(NetworkRelation(
                source=r["source"],
                target=r["target"],
                relation=r["relation"],
                weight=r.get("weight", 1.0),
                attributes=r.get("attributes", {}),
            ))
        return g


@dataclass
class HostEntry:
    ip:              str
    state:           HostState              = HostState.UNSCANNED
    os_hint:         str                    = ""
    services:        Dict[int, ServiceInfo] = field(default_factory=dict)
    notes:           List[str]              = field(default_factory=list)
    last_updated:    str                    = field(default_factory=lambda: datetime.now().isoformat())

    def add_service(self, svc: ServiceInfo) -> None:
        self.services[svc.port] = svc
        self.last_updated = datetime.now().isoformat()

    def advance(self, new_state: HostState) -> bool:
        """Advance state only if new_state is the next valid step. Returns True if changed."""
        if new_state.rank() > self.state.rank():
            self.state        = new_state
            self.last_updated = datetime.now().isoformat()
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "ip":           self.ip,
            "state":        self.state.value,
            "os_hint":      self.os_hint,
            "services":     {str(p): vars(s) for p, s in self.services.items()},
            "notes":        self.notes,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "HostEntry":
        h = cls(
            ip       = d["ip"],
            state    = HostState(d.get("state", HostState.UNSCANNED.value)),
            os_hint  = d.get("os_hint", ""),
            notes    = d.get("notes", []),
            last_updated = d.get("last_updated", ""),
        )
        for port_str, svc in d.get("services", {}).items():
            h.services[int(port_str)] = ServiceInfo(**svc)
        return h


# ---------------------------------------------------------------------------
# Phase derivation
# ---------------------------------------------------------------------------

class _PhaseDeriver:
    """
    Derives the current EngagementPhase from the aggregate host states.
    Keeps the derivation logic isolated so it can be swapped or extended.
    """

    _STATE_TO_PHASE: Dict[str, EngagementPhase] = {
        HostState.UNSCANNED.value:  EngagementPhase.RECON,
        HostState.SCANNED.value:    EngagementPhase.SCANNING,
        HostState.ENUMERATED.value: EngagementPhase.ENUMERATION,
        HostState.EXPLOITED.value:  EngagementPhase.EXPLOITATION,
        HostState.OWNED.value:      EngagementPhase.POST_EXPLOITATION,
    }

    def derive(self, hosts: Dict[str, HostEntry]) -> EngagementPhase:
        if not hosts:
            return EngagementPhase.RECON
        if all(h.state == HostState.OWNED for h in hosts.values()):
            return EngagementPhase.COMPLETE
        max_state = max(hosts.values(), key=lambda h: h.state.rank()).state
        return self._STATE_TO_PHASE.get(max_state.value, EngagementPhase.RECON)


# ---------------------------------------------------------------------------
# MITRE tactic → phase mapping
# ---------------------------------------------------------------------------

PHASE_TO_MITRE_TACTICS: Dict[EngagementPhase, List[str]] = {
    EngagementPhase.RECON:             ["TA0043 - Reconnaissance"],
    EngagementPhase.SCANNING:          ["TA0007 - Discovery"],
    EngagementPhase.ENUMERATION:       ["TA0007 - Discovery", "TA0006 - Credential Access"],
    EngagementPhase.EXPLOITATION:      ["TA0001 - Initial Access", "TA0002 - Execution"],
    EngagementPhase.POST_EXPLOITATION: ["TA0004 - Privilege Escalation", "TA0008 - Lateral Movement",
                                        "TA0010 - Exfiltration"],
    EngagementPhase.COMPLETE:          ["TA0040 - Impact"],
}

# Phase → MCP tool names that are most relevant
PHASE_TO_TOOLS: Dict[EngagementPhase, List[str]] = {
    EngagementPhase.RECON: [
        "lazyown_tool_dig_any", "lazyown_tool_dig_reverse",
        "lazyown_tool_gobuster_dns", "lazyown_tool_dnsrecon_axfr",
    ],
    EngagementPhase.SCANNING: [
        "lazyown_tool_enum_smb", "lazyown_tool_enum4linux_tool",
        "lazyown_tool_ffuf_tool", "lazyown_tool_nikto_host",
        "lazyown_tool_showmount_tool", "lazyown_tool_enum_rpcbind",
    ],
    EngagementPhase.ENUMERATION: [
        "lazyown_tool_ldapsearch_tool", "lazyown_tool_smbclient_list",
        "lazyown_tool_kerbrute_tool_user", "lazyown_tool_nxc_ldap",
        "lazyown_tool_gobuster_web",
    ],
    EngagementPhase.EXPLOITATION: [
        "lazyown_tool_evil_winrm_tool", "lazyown_tool_hydrardp_tool",
        "lazyown_tool_kerberoasting_tool", "lazyown_tool_asrep_roast",
        "lazyown_plugin_generate_reverse_shell",
    ],
    EngagementPhase.POST_EXPLOITATION: [
        "lazyown_c2_command", "lazyown_c2_adversary",
        "lazyown_tool_bloodhound-python", "lazyown_tool_crackmapexec_smb",
    ],
}


# ---------------------------------------------------------------------------
# WorldModel
# ---------------------------------------------------------------------------

class WorldModel:
    """
    Thread-safe, persistent engagement world model.

    Maintains hosts, credentials, vulnerabilities, and the derived phase.
    Persists state to sessions/world_model.json on every mutation.
    """

    def __init__(self, path: str | Path = _DEFAULT_PATH) -> None:
        self._path:    Path                       = Path(path)
        self._lock:    threading.RLock             = threading.RLock()
        self._hosts:   Dict[str, HostEntry]       = {}
        self._creds:   List[CredentialEntry]      = []
        self._vulns:   List[VulnerabilityEntry]   = []
        self._graph:   NetworkGraph               = NetworkGraph()
        self._deriver: _PhaseDeriver              = _PhaseDeriver()
        self._load()

    # ── Host management ───────────────────────────────────────────────────────

    def add_host(self, ip: str) -> HostEntry:
        with self._lock:
            if ip not in self._hosts:
                self._hosts[ip] = HostEntry(ip=ip)
                log.debug("WorldModel: new host %s", ip)
                self._save()
            return self._hosts[ip]

    def advance_host(self, ip: str, new_state: HostState) -> bool:
        with self._lock:
            host = self._hosts.get(ip) or self.add_host(ip)
            changed = host.advance(new_state)
            if changed:
                log.info("WorldModel: %s -> %s", ip, new_state.value)
                self._save()
            return changed

    def add_service(self, ip: str, port: int, name: str = "", version: str = "",
                    protocol: str = "tcp") -> None:
        with self._lock:
            host = self._hosts.get(ip) or self.add_host(ip)
            host.add_service(ServiceInfo(port=port, name=name, version=version, protocol=protocol))
            if host.state == HostState.UNSCANNED:
                host.advance(HostState.SCANNED)
            if name:
                self._graph.add_relation(NetworkRelation(
                    source=f"host:{ip}",
                    target=f"service:{name}",
                    relation="runs_service",
                    attributes={"port": str(port), "version": version},
                ))
            self._save()

    def add_note(self, ip: str, note: str) -> None:
        with self._lock:
            host = self._hosts.get(ip) or self.add_host(ip)
            if note not in host.notes:
                host.notes.append(note)
                self._save()

    # ── Credential / vulnerability tracking ───────────────────────────────────

    def add_credential(self, value: str, host: str = "", service: str = "") -> None:
        with self._lock:
            if not any(c.value == value for c in self._creds):
                self._creds.append(CredentialEntry(value=value, host=host, service=service))
                log.info("WorldModel: credential captured for %s", host or "unknown")
                cred_node = f"cred:{value[:12]}"
                if host:
                    self._graph.add_relation(NetworkRelation(
                        source=f"host:{host}",
                        target=cred_node,
                        relation="exposes_credential",
                        attributes={"service": service},
                    ))
                    # Credential potentially grants access to other hosts
                    for other_ip in self._hosts:
                        if other_ip != host:
                            self._graph.add_relation(NetworkRelation(
                                source=cred_node,
                                target=f"host:{other_ip}",
                                relation="may_authenticate_to",
                                weight=0.5,
                            ))
                self._save()

    def add_vulnerability(self, description: str, host: str = "",
                           cve: str = "", severity: str = "UNKNOWN") -> None:
        with self._lock:
            entry = VulnerabilityEntry(description=description, host=host, cve=cve, severity=severity)
            self._vulns.append(entry)
            self._save()

    # ── Finding integration ───────────────────────────────────────────────────

    def update_from_findings(self, findings: list) -> None:
        """
        Integrate a list of Finding objects (from obs_parser.ObsParser).
        Each finding updates the relevant part of the world model.
        """
        for f in findings:
            ftype = getattr(f, "type", "")
            value = getattr(f, "value", "")
            host  = getattr(f, "host",  "")
            if not value:
                continue
            try:
                if ftype == "ip":
                    self.add_host(value)
                elif ftype == "credential":
                    self.add_credential(value, host=host)
                elif ftype == "service_version":
                    if host:
                        parts = value.split(" ", 1)
                        name    = parts[0]
                        version = parts[1] if len(parts) > 1 else ""
                        self.add_note(host, f"service: {value}")
                elif ftype == "cve":
                    self.add_vulnerability(value, host=host, cve=value)
                elif ftype == "hash":
                    self.add_credential(value, host=host, service="hash")
                elif ftype == "path":
                    if host:
                        self.add_note(host, f"path: {value}")
                elif ftype == "username":
                    if host:
                        self.add_note(host, f"user: {value}")
            except Exception as exc:
                log.debug("WorldModel.update_from_findings: %s", exc)

    # ── Network graph ─────────────────────────────────────────────────────────

    def add_relation(
        self,
        source: str,
        target: str,
        relation: str,
        weight: float = 1.0,
        **attributes: str,
    ) -> None:
        """Add an arbitrary directed relationship to the network graph."""
        with self._lock:
            self._graph.add_relation(NetworkRelation(
                source=source,
                target=target,
                relation=relation,
                weight=weight,
                attributes=dict(attributes),
            ))
            self._save()

    def pivot_candidates(self, top_k: int = 5) -> List[Dict]:
        """
        Return the top_k highest-centrality nodes as pivot candidates.
        Uses normalized degree centrality over the full network graph.
        """
        with self._lock:
            return self._graph.pivot_candidates(top_k=top_k)

    def graph_snapshot(self) -> dict:
        """Return the full network graph as a serialisable dict."""
        with self._lock:
            return self._graph.to_dict()

    # ── Phase and context ─────────────────────────────────────────────────────

    def get_phase(self) -> EngagementPhase:
        with self._lock:
            return self._deriver.derive(self._hosts)

    def get_suggested_tools(self) -> List[str]:
        return PHASE_TO_TOOLS.get(self.get_phase(), [])

    def to_context_string(self) -> str:
        """
        Compact, LLM-readable summary of the current engagement state.
        Designed to fit in a prompt without consuming excessive tokens.
        """
        with self._lock:
            phase = self._deriver.derive(self._hosts)
            lines: List[str] = [
                f"Phase: {phase.value}",
                f"Hosts: {len(self._hosts)}  "
                f"Credentials: {len(self._creds)}  "
                f"Vulnerabilities: {len(self._vulns)}",
                "",
            ]
            for ip, host in self._hosts.items():
                svc_summary = ", ".join(
                    f"{p}/{s.name}" for p, s in sorted(host.services.items())
                ) or "no services"
                lines.append(f"  [{host.state.value:11s}] {ip}  {host.os_hint or ''}  | {svc_summary}")
                for note in host.notes[-3:]:          # last 3 notes per host
                    lines.append(f"             note: {note}")

            if self._creds:
                lines.append("\nCredentials (latest 5):")
                for c in self._creds[-5:]:
                    lines.append(f"  {c.host or 'unknown'}: {c.value[:60]}")

            if self._vulns:
                lines.append("\nVulnerabilities (latest 5):")
                for v in self._vulns[-5:]:
                    sev = f"[{v.severity}]" if v.severity != "UNKNOWN" else ""
                    lines.append(f"  {v.host or 'unknown'} {sev} {v.cve or ''} {v.description[:80]}")

            lines.append(f"\nSuggested tools for {phase.value}: "
                         + ", ".join(self.get_suggested_tools()[:5] or ["(any)"]))

            pivots = self._graph.pivot_candidates(top_k=3)
            if pivots:
                lines.append("\nTop pivot candidates (by network centrality):")
                for p in pivots:
                    lines.append(
                        f"  {p['node']}  centrality={p['centrality']:.3f}  "
                        f"out={p['out_degree']} in={p['in_degree']}"
                    )

            return "\n".join(lines)

    # ── Serialization ─────────────────────────────────────────────────────────

    def _save(self) -> None:
        """Write state to disk. Caller must hold _lock."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".json.tmp")
        try:
            data = {
                "hosts":           {ip: h.to_dict() for ip, h in self._hosts.items()},
                "credentials":     [vars(c) for c in self._creds],
                "vulnerabilities": [vars(v) for v in self._vulns],
                "network_graph":   self._graph.to_dict(),
                "saved_at":        datetime.now().isoformat(),
            }
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            tmp.replace(self._path)
        except Exception as exc:
            log.warning("WorldModel._save failed: %s", exc)
            if tmp.exists():
                tmp.unlink(missing_ok=True)

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            self._hosts = {ip: HostEntry.from_dict(h) for ip, h in data.get("hosts", {}).items()}
            self._creds = [CredentialEntry(**c) for c in data.get("credentials", [])]
            self._vulns = [VulnerabilityEntry(**v) for v in data.get("vulnerabilities", [])]
            if "network_graph" in data:
                self._graph = NetworkGraph.from_dict(data["network_graph"])
            log.info("WorldModel: loaded %d hosts, %d creds from %s",
                     len(self._hosts), len(self._creds), self._path)
        except Exception as exc:
            log.warning("WorldModel._load failed: %s — starting fresh", exc)

    # ── Convenience ───────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Clear all state and delete the persisted file."""
        with self._lock:
            self._hosts.clear()
            self._creds.clear()
            self._vulns.clear()
            if self._path.exists():
                self._path.unlink()

    def snapshot(self) -> dict:
        """Return a plain-dict snapshot (for JSON serialisation)."""
        with self._lock:
            return {
                "phase":           self.get_phase().value,
                "hosts":           {ip: h.to_dict() for ip, h in self._hosts.items()},
                "credentials":     [vars(c) for c in self._creds],
                "vulnerabilities": [vars(v) for v in self._vulns],
                "pivot_candidates": self._graph.pivot_candidates(top_k=5),
            }


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_wm: Optional[WorldModel] = None


def get_world_model(path: str | Path = _DEFAULT_PATH) -> WorldModel:
    """Return (or create) the module-level singleton WorldModel."""
    global _default_wm
    if _default_wm is None:
        _default_wm = WorldModel(path=path)
    return _default_wm


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse, sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    p = argparse.ArgumentParser(description="LazyOwn World Model CLI")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("show",  help="Print current world model context")
    sub.add_parser("reset", help="Clear world model")
    add_p = sub.add_parser("add-host", help="Add a host")
    add_p.add_argument("ip")
    add_p.add_argument("--state", default="scanned")

    args = p.parse_args()
    wm = WorldModel()

    if args.cmd == "show" or args.cmd is None:
        print(wm.to_context_string())
        print(f"\nPhase: {wm.get_phase().value}")
    elif args.cmd == "reset":
        wm.reset()
        print("World model reset.")
    elif args.cmd == "add-host":
        wm.add_host(args.ip)
        wm.advance_host(args.ip, HostState(args.state))
        print(wm.to_context_string())
