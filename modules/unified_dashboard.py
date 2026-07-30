"""Unified campaign dashboard — combines all state sources into one view.

The existing :class:`modules.dashboard_engine.DashboardEngine` builds a
snapshot from the world model, exploit recommender, auto-pivot, and evasion
engine.  However, it does NOT include:

- Hive Mind status (active drones, memory vectors)
- Policy Engine status (active rules, last decision)
- Autonomous Daemon status (pending objectives, current phase)
- Live Surface graph (real-time network topology)
- GraphAdvisor pivot candidates

This module fills that gap by composing all data sources into a single
unified snapshot suitable for CLI rendering, JSON export, or TUI consumption.

Design (SOLID)
--------------
- Single Responsibility : aggregate + render campaign state only.
- Open/Closed           : new data sources added as ``_collect_*`` methods.
- Dependency Inversion  : depends on ``DashboardEngine`` interface, not
  concrete implementations of hive/policy/daemon.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


class UnifiedDashboard:
    """Aggregates world model, hive, policy, daemon, and graph state.

    Attributes:
        sessions_dir: Path to the sessions directory.
    """

    def __init__(self, sessions_dir: Path | None = None) -> None:
        self._sessions_dir = sessions_dir or _SESSIONS_DIR
        self._dashboard: Any = None
        self._graph: Any = None

    def _get_dashboard(self) -> Any:
        if self._dashboard is None:
            try:
                from modules.dashboard_engine import DashboardEngine
                from modules.exploit_recommender import ExploitRecommender
                from modules.world_model import WorldModel
                wm = WorldModel(self._sessions_dir / "world_model.json")
                self._dashboard = DashboardEngine(wm)
                er = ExploitRecommender(wm)
                self._dashboard.set_exploit_recommender(er)
            except Exception as exc:
                log.debug("UnifiedDashboard: dashboard engine unavailable: %s", exc)
                self._dashboard = False
        return self._dashboard if self._dashboard is not False else None

    def _get_graph(self) -> Any:
        if self._graph is None:
            try:
                from cli.graph_advisor import GraphAdvisor
                self._graph = GraphAdvisor.from_path()
            except Exception as exc:
                log.debug("UnifiedDashboard: graph advisor unavailable: %s", exc)
                self._graph = False
        return self._graph if self._graph is not False else None

    def build_unified_snapshot(self) -> dict[str, Any]:
        """Build a complete dashboard snapshot from all data sources.

        Returns:
            Dict with keys: world_model, hive_status, policy_status,
            daemon_status, live_graph, graph_advice, dashboard, timestamp.
        """
        snapshot: dict[str, Any] = {
            "world_model": self._collect_world_model(),
            "hive_status": self._collect_hive_status(),
            "policy_status": self._collect_policy_status(),
            "daemon_status": self._collect_daemon_status(),
            "live_graph": self._collect_live_graph(),
            "graph_advice": self._collect_graph_advice(),
            "dashboard": self._collect_dashboard(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return snapshot

    def _collect_world_model(self) -> dict:
        wm_file = self._sessions_dir / "world_model.json"
        if wm_file.exists():
            try:
                return json.loads(wm_file.read_text())
            except Exception:
                return {}
        return {}

    def _collect_hive_status(self) -> dict:
        try:
            from hive_mind import get_hive
            hive = get_hive()
            return hive.status()
        except Exception as exc:
            log.debug("UnifiedDashboard: hive unavailable: %s", exc)
            return {"error": "hive unavailable"}

    def _collect_policy_status(self) -> dict:
        try:
            from skills.lazyown_policy import get_policy
            policy = get_policy()
            return policy.status_report()
        except Exception as exc:
            log.debug("UnifiedDashboard: policy unavailable: %s", exc)
            return {"error": "policy unavailable"}

    def _collect_daemon_status(self) -> dict:
        status_file = self._sessions_dir / "autonomous_status.json"
        if status_file.exists():
            try:
                return json.loads(status_file.read_text())
            except Exception:
                return {}
        return {}

    def _collect_live_graph(self) -> dict:
        wm = self._collect_world_model()
        if not wm:
            return {}
        try:
            from modules.live_surface import build_live_graph
            return build_live_graph(wm)
        except Exception as exc:
            log.debug("UnifiedDashboard: live surface unavailable: %s", exc)
            return {"error": str(exc)}

    def _collect_graph_advice(self) -> dict:
        graph = self._get_graph()
        if graph is None:
            return {"error": "graph unavailable"}
        try:
            if not graph.is_available():
                return {"available": False, "reason": "graph not loaded"}
            summary = graph.summary()
            return {
                "available": summary.get("available", True),
                "nodes": summary.get("nodes", 0),
                "edges": summary.get("edges", 0),
                "communities": summary.get("communities", 0),
            }
        except Exception as exc:
            log.debug("UnifiedDashboard: graph advice unavailable: %s", exc)
            return {"error": str(exc)}

    def _collect_dashboard(self) -> dict:
        dashboard = self._get_dashboard()
        if dashboard is None:
            return {"error": "dashboard unavailable"}
        try:
            return dashboard.build_snapshot()
        except Exception as exc:
            log.debug("UnifiedDashboard: dashboard snapshot failed: %s", exc)
            return {"error": str(exc)}

    def render_unified(self) -> str:
        """Render the unified dashboard as a text string for CLI/TUI.

        Returns:
            A multi-line ASCII dashboard string.
        """
        snap = self.build_unified_snapshot()
        lines: list[str] = []
        lines.append("=" * 72)
        lines.append("  LAZYOWN UNIFIED CAMPAIGN DASHBOARD")
        lines.append("=" * 72)

        # World Model
        wm = snap.get("world_model", {})
        hosts = wm.get("hosts", {})
        phase_counts: dict[str, int] = {}
        for h in hosts.values():
            phase = h.get("state", "unknown") if isinstance(h, dict) else "unknown"
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        lines.append(f"\n  [World Model] {len(hosts)} hosts | Phases: {phase_counts}")

        # Hive Mind
        hive = snap.get("hive_status", {})
        if "error" not in hive:
            drones = hive.get("drones_active", 0)
            mem_stats = hive.get("memory_stats", {})
            vectors = mem_stats.get("semantic_count", 0) if isinstance(mem_stats, dict) else 0
            lines.append(f"  [Hive Mind] {drones} drones | Memory: {vectors} vectors")
        else:
            lines.append(f"  [Hive Mind] {hive.get('error', 'unavailable')}")

        # Daemon
        daemon = snap.get("daemon_status", {})
        if daemon:
            phase = daemon.get("current_phase", "?")
            pending = daemon.get("pending_objectives", [])
            lines.append(f"  [Daemon] Phase: {phase} | Objectives: {len(pending)}")
        else:
            lines.append("  [Daemon] Not running")

        # Policy
        policy = snap.get("policy_status", {})
        if "error" not in policy:
            rules = policy.get("active_rules", 0)
            last = policy.get("last_decision", "?")
            lines.append(f"  [Policy] Rules: {rules} | Last decision: {last}")
        else:
            lines.append(f"  [Policy] {policy.get('error', 'unavailable')}")

        # Graph Advisor
        graph = snap.get("graph_advice", {})
        if "error" not in graph:
            nodes = graph.get("nodes", 0)
            pivots = len(graph.get("top_pivot_candidates", []))
            lines.append(f"  [GraphAdvisor] {nodes} nodes | Pivot candidates: {pivots}")
        else:
            lines.append(f"  [GraphAdvisor] {graph.get('error', 'unavailable')}")

        # Dashboard
        dash = snap.get("dashboard", {})
        if "error" not in dash:
            stats = dash.get("stats", {})
            lines.append(
                f"  [Dashboard] Hosts: {stats.get('total_hosts', 0)} | "
                f"Services: {stats.get('total_services', 0)} | "
                f"Pivots: {stats.get('active_pivots', 0)}"
            )
        else:
            lines.append(f"  [Dashboard] {dash.get('error', 'unavailable')}")

        # Live Graph
        live = snap.get("live_graph", {})
        if live and "error" not in live:
            nodes = len(live.get("nodes", []))
            edges = len(live.get("edges", []))
            lines.append(f"  [LiveSurface] {nodes} nodes | {edges} edges")

        lines.append(f"\n  Updated: {snap.get('timestamp', '?')}")
        lines.append("=" * 72)
        return "\n".join(lines)

    def export_json(self) -> str:
        """Export the unified snapshot as a JSON string."""
        return json.dumps(self.build_unified_snapshot(), indent=2, default=str)


def get_unified_dashboard(sessions_dir: Path | None = None) -> UnifiedDashboard:
    """Return a module-level :class:`UnifiedDashboard` singleton."""
    global _dashboard
    if _dashboard is None:
        _dashboard = UnifiedDashboard(sessions_dir=sessions_dir)
    return _dashboard


_dashboard: UnifiedDashboard | None = None


__all__ = [
    "UnifiedDashboard",
    "get_unified_dashboard",
]
