"""Live Network Map Dashboard for LazyOwn.

Provides a curses-based real-time visualization of:
- Discovered hosts with service status
- Kill-chain phase progression per host
- Active exploit recommendations
- Pivot chain topology
- Beacon health indicators

Consumes data from WorldModel, ExploitRecommender, AutoPivotEngine, and EvasionEngine.
"""

from __future__ import annotations

import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"

_NMAP_PORT_PRIORITY: dict[str, int] = {
    "http": 1, "https": 2, "ssh": 3, "smb": 4, "rdp": 5,
    "winrm": 6, "mysql": 7, "ftp": 8, "telnet": 9, "dns": 10,
}


def _parse_nmap_xml_services(sessions_dir: Path) -> dict[str, list[dict]]:
    """Parse all scan_*.nmap.xml files and return {ip: [svc_dicts]}."""
    results: dict[str, list[dict]] = {}
    try:
        import xml.etree.ElementTree as _ET
    except ImportError:
        return results

    for xml_file in sorted(sessions_dir.glob("scan_*.nmap.xml")):
        try:
            tree = _ET.parse(str(xml_file))
            root = tree.getroot()
            for addr_el in root.iter("address"):
                if addr_el.get("addrtype") == "ipv4":
                    ip = addr_el.get("addr", "")
                    if ip and ip not in results:
                        results[ip] = []
                    for port_el in root.iter("port"):
                        state_el = port_el.find("state")
                        if state_el is not None and state_el.get("state") == "open":
                            pid = port_el.get("portid", "0")
                            svc_el = port_el.find("service")
                            name = svc_el.get("name", "?") if svc_el is not None else "?"
                            prod = svc_el.get("product", "") if svc_el is not None else ""
                            ver = svc_el.get("version", "") if svc_el is not None else ""
                            vstr = f"{prod} {ver}".strip() if prod or ver else ""
                            results[ip].append({"port": int(pid), "name": name, "version": vstr})
                    break
        except Exception:
            continue

    for ip in results:
        results[ip].sort(key=lambda s: _NMAP_PORT_PRIORITY.get(s["name"], 99))
    return results

_PHASE_COLORS: dict[str, str] = {
    "unscanned": "white",
    "scanned": "blue",
    "enumerated": "cyan",
    "exploited": "yellow",
    "owned": "green",
}

_SEVERITY_COLORS: dict[str, str] = {
    "CRITICAL": "red",
    "HIGH": "magenta",
    "MEDIUM": "yellow",
    "LOW": "blue",
    "NONE": "white",
}

_EDGE_SYMBOLS: dict[str, str] = {
    "direct": "---",
    "pivot": "-=-",
    "c2": "~~~",
}


@dataclass
class DashboardNode:
    label: str
    ip: str
    phase: str
    services: list[str] = field(default_factory=list)
    vuln_count: int = 0
    is_beacon: bool = False
    is_pivot: bool = False
    children: list[DashboardNode] = field(default_factory=list)


@dataclass
class DashboardEdge:
    source: str
    target: str
    relation: str  # "direct", "pivot", "c2"
    active: bool = True


class DashboardEngine:
    """Builds a live dashboard data model from campaign state.

    Does NOT depend on curses directly — produces structured data suitable
    for text-based rendering, JSON export, or TUI consumption.

    Attributes:
        world_model: Optional reference to the campaign WorldModel.
        sessions_dir: Path to the sessions directory.
    """

    __slots__ = (
        "_world_model",
        "_exploit_recommender",
        "_auto_pivot",
        "_evasion_engine",
        "_sessions_dir",
        "_refresh_interval",
        "_last_refresh",
    )

    def __init__(self, world_model: Any = None) -> None:
        self._world_model = world_model
        self._exploit_recommender: Any = None
        self._auto_pivot: Any = None
        self._evasion_engine: Any = None
        self._sessions_dir = SESSIONS_DIR
        self._refresh_interval = 5.0
        self._last_refresh = 0.0

    def set_world_model(self, model: Any) -> None:
        self._world_model = model

    def set_exploit_recommender(self, recommender: Any) -> None:
        self._exploit_recommender = recommender

    def set_auto_pivot(self, pivot: Any) -> None:
        self._auto_pivot = pivot

    def set_evasion_engine(self, evasion: Any) -> None:
        self._evasion_engine = evasion

    def build_snapshot(self) -> dict[str, Any]:
        """Build a complete dashboard snapshot from all data sources.

        Returns:
            Dict with keys: nodes, edges, stats, recommendations, pivots, beacons.
        """
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []
        stats: dict[str, int] = defaultdict(int)
        recommendations: list[dict[str, Any]] = []
        pivots: list[dict[str, Any]] = []
        beacons: list[dict[str, Any]] = []

        if self._world_model is not None:
            wm = self._world_model
            for host_ip, host in wm._hosts.items():
                phase = host.state.value if hasattr(host.state, "value") else str(host.state)
                stats[f"hosts_{phase}"] = stats.get(f"hosts_{phase}", 0) + 1
                svc_list = [
                    f"{s.port}/{s.name}" for s in host.services.values() if s.state == "open"
                ]

                node = {
                    "ip": host_ip,
                    "label": host_ip,
                    "phase": phase,
                    "phase_color": _PHASE_COLORS.get(phase, "white"),
                    "services": svc_list,
                    "os_hint": host.os_hint or "",
                    "service_count": len(svc_list),
                }
                nodes.append(node)
                edges.append({
                    "source": "attacker",
                    "target": host_ip,
                    "relation": "direct",
                    "active": True,
                })

        nmap_services = _parse_nmap_xml_services(self._sessions_dir)
        known_ips = {n["ip"] for n in nodes}
        for ip, svcs in nmap_services.items():
            svc_list = [f"{s['port']}/{s['name']}" for s in svcs]
            if ip in known_ips:
                for n in nodes:
                    if n["ip"] == ip and not n["services"]:
                        n["services"] = svc_list
                        n["service_count"] = len(svc_list)
            else:
                nodes.append({
                    "ip": ip,
                    "label": ip,
                    "phase": "scanned",
                    "phase_color": _PHASE_COLORS.get("scanned", "blue"),
                    "services": svc_list,
                    "os_hint": "",
                    "service_count": len(svc_list),
                })
                edges.append({
                    "source": "attacker",
                    "target": ip,
                    "relation": "direct",
                    "active": True,
                })
                stats["hosts_scanned"] = stats.get("hosts_scanned", 0) + 1

        if self._exploit_recommender is not None:
            try:
                recs = self._exploit_recommender.recommend(top_n=10)
                recommendations = recs
                stats["recommendations"] = len(recs)
            except Exception:
                pass

        if self._auto_pivot is not None:
            try:
                pivots = self._auto_pivot.get_active_routes()
                stats["active_pivots"] = len(pivots)
            except Exception:
                pass

        if self._evasion_engine is not None:
            try:
                profile = self._evasion_engine.get_active_profile()
                if profile:
                    beacons.append({
                        "profile_id": profile.profile_id,
                        "user_agent": profile.user_agent[:50],
                        "sleep_s": profile.sleep_s,
                        "jitter_ms": profile.jitter_ms,
                        "domain_front": profile.domain_front,
                    })
                stats["active_profiles"] = 1 if profile else 0
            except Exception:
                pass

        stats["total_hosts"] = len(nodes)
        stats["total_services"] = sum(n.get("service_count", 0) for n in nodes)
        self._last_refresh = time.time()

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": dict(stats),
            "recommendations": recommendations,
            "pivots": pivots,
            "beacons": beacons,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def render_text_map(self, snapshot: dict[str, Any] | None = None) -> str:
        """Render a text-based network map from a dashboard snapshot.

        Args:
            snapshot: Dashboard snapshot dict from build_snapshot().
                      Builds a fresh snapshot if None.

        Returns:
            A multi-line ASCII-art network topology string.
        """
        if snapshot is None:
            snapshot = self.build_snapshot()

        lines: list[str] = []
        lines.append("=" * 72)
        lines.append("  LAZYOWN LIVE NETWORK MAP")
        lines.append("=" * 72)
        lines.append("")

        stats = snapshot.get("stats", {})
        lines.append(
            f"  Hosts: {stats.get('total_hosts', 0)} | "
            f"Services: {stats.get('total_services', 0)} | "
            f"Recommendations: {stats.get('recommendations', 0)} | "
            f"Pivots: {stats.get('active_pivots', 0)}"
        )
        lines.append("")

        for i, node in enumerate(snapshot.get("nodes", [])):
            phase_icon = self._phase_icon(node.get("phase", "unscanned"))
            color = node.get("phase_color", "white")
            lines.append(
                f"  [{phase_icon}] {node['ip']:<16} | "
                f"Phase: {node['phase']:<12} | "
                f"OS: {node.get('os_hint', '?')[:15]:<15} | "
                f"Services: {', '.join(node.get('services', [])[:5])}"
            )

        recs = snapshot.get("recommendations", [])
        if recs:
            lines.append("")
            lines.append("-" * 72)
            lines.append("  [EXPLOIT RECOMMENDATIONS]")
            lines.append("-" * 72)
            for r in recs[:5]:
                sev_color = _SEVERITY_COLORS.get(r.get("severity", "MEDIUM"), "white")
                lines.append(
                    f"  [{sev_color}] {r.get('cve', '?')} "
                    f"| {r.get('severity', '?'):<8} "
                    f"| conf={r.get('confidence', 0):.0%} "
                    f"| {r.get('description', '')[:50]}"
                )

        pivots = snapshot.get("pivots", [])
        if pivots:
            lines.append("")
            lines.append("-" * 72)
            lines.append("  [ACTIVE PIVOTS]")
            lines.append("-" * 72)
            for p in pivots:
                lines.append(
                    f"  {p.get('type', '?'):<8} -> {p['ip']}:{p.get('port', '?')} "
                    f"| subnets: {', '.join(p.get('subnets', [])[:3])}"
                )

        beacons = snapshot.get("beacons", [])
        if beacons:
            lines.append("")
            lines.append("-" * 72)
            lines.append("  [ACTIVE BEACONS]")
            lines.append("-" * 72)
            for b in beacons:
                lines.append(
                    f"  Profile: {b.get('profile_id', '?')} "
                    f"| Sleep: {b.get('sleep_s', 0)}s "
                    f"| Front: {b.get('domain_front', '?')}"
                )

        lines.append("")
        lines.append("=" * 72)
        return "\n".join(lines)

    def render_ascii_topology(self, snapshot: dict[str, Any] | None = None) -> str:
        """Render an ASCII-art topology tree from a snapshot.

        Args:
            snapshot: Dashboard snapshot dict from build_snapshot().

        Returns:
            Multi-line ASCII topology string.
        """
        if snapshot is None:
            snapshot = self.build_snapshot()

        lines: list[str] = []
        lines.append("         [Attacker]")
        lines.append("             |")
        lines.append("    +--------+--------+")

        nodes = snapshot.get("nodes", [])
        if not nodes:
            lines.append("    (no hosts discovered)")
        else:
            for i, node in enumerate(nodes):
                connector = "    |" if i == 0 else "    +"
                prefix = "    +--" if i == len(nodes) - 1 else "    |--"
                phase_icon = self._phase_icon(node.get("phase", "unscanned"))
                lines.append(
                    f"{prefix} [{phase_icon}] {node['ip']} "
                    f"({node.get('os_hint', '?')}) [{node.get('phase', '?')}]"
                )
                for svc in node.get("services", [])[:3]:
                    lines.append(f"    |    |-- {svc}")
                if len(node.get("services", [])) > 3:
                    lines.append(f"    |    |-- ... +{len(node['services']) - 3} more")

        pivots = snapshot.get("pivots", [])
        for p in pivots:
            lines.append(f"    +====[{p.get('type', '?')}]====> {p['ip']}:{p.get('port', '?')}")

        return "\n".join(lines)

    @staticmethod
    def _phase_icon(phase: str) -> str:
        icons = {
            "unscanned": "?",
            "scanned": "S",
            "enumerated": "E",
            "exploited": "X",
            "owned": "*",
        }
        return icons.get(phase, "?")

    def export_json(self, snapshot: dict[str, Any] | None = None) -> str:
        """Export dashboard snapshot as JSON string.

        Args:
            snapshot: Dashboard snapshot dict from build_snapshot().

        Returns:
            JSON string.
        """
        if snapshot is None:
            snapshot = self.build_snapshot()
        return json.dumps(snapshot, indent=2, ensure_ascii=False)

    def persist_snapshot(self, snapshot: dict[str, Any] | None = None) -> Path:
        """Persist dashboard snapshot to sessions/dashboard_snapshot.json.

        Args:
            snapshot: Dashboard snapshot dict from build_snapshot().

        Returns:
            Path to the written file.
        """
        if snapshot is None:
            snapshot = self.build_snapshot()
        self._sessions_dir.mkdir(parents=True, exist_ok=True)
        target = self._sessions_dir / "dashboard_snapshot.json"
        with target.open("w", encoding="utf-8") as fh:
            json.dump(snapshot, fh, indent=2, ensure_ascii=False)
        return target

    def format_for_cli(self, snapshot: dict[str, Any] | None = None) -> str:
        """Compact single-line status for CLI prompt integration.

        Args:
            snapshot: Dashboard snapshot dict from build_snapshot().

        Returns:
            Short status string: "[H:3 S:12 R:5 P:2 B:1]"
        """
        if snapshot is None:
            snapshot = self.build_snapshot()
        stats = snapshot.get("stats", {})
        return (
            f"[H:{stats.get('total_hosts', 0)} "
            f"S:{stats.get('total_services', 0)} "
            f"R:{stats.get('recommendations', 0)} "
            f"P:{stats.get('active_pivots', 0)} "
            f"B:{stats.get('active_profiles', 0)}]"
        )
