"""Live attack-surface graph derived from the world model.

The static ``templates/graph.html`` is a one-off pyvis export with hardcoded
nodes; it cannot reflect an engagement in progress. This module builds a
*live* graph instead, straight from ``sessions/world_model.json`` (the
authoritative campaign state written by the autonomous daemon and the CLI).

The output is a vis-network-friendly payload — ``nodes``, ``edges`` and a
``stats`` block — that the ``/surface_live`` page polls on an interval so the
topology updates as hosts move from *unscanned* to *owned*. Compromised hosts
and high-centrality pivot points are flagged with ``pulse`` so the front end
can animate them.

Centrality is computed with the existing :class:`modules.world_model.NetworkGraph`
(normalized degree centrality), so this module adds presentation only and never
re-implements graph reasoning. It imports nothing from ``lazyc2.py`` and is a
pure transformation, which keeps it unit-testable.
"""

from __future__ import annotations

from typing import Any

try:
    from modules.world_model import NetworkGraph
except ImportError:
    from world_model import NetworkGraph

HOST_PREFIX: str = "host:"
SERVICE_PREFIX: str = "service:"

GROUP_HOST: str = "host"
GROUP_SERVICE: str = "service"
GROUP_OTHER: str = "node"

COMPROMISED_STATES: frozenset[str] = frozenset({"exploited", "owned"})

NODE_VALUE_BASE: int = 4
NODE_VALUE_CENTRALITY_SCALE: int = 20
PULSE_CENTRALITY_THRESHOLD: float = 0.25
PIVOT_TOP_K: int = 5
RUNS_SERVICE_RELATION: str = "runs_service"


def _is_compromised(state: str) -> bool:
    """Return ``True`` when a host state means a foothold was obtained."""
    return state.lower() in COMPROMISED_STATES


def _node_value(centrality: float) -> int:
    """Map a centrality score to a vis-network node size."""
    return NODE_VALUE_BASE + int(round(centrality * NODE_VALUE_CENTRALITY_SCALE))


def _group_for(node_id: str) -> str:
    """Classify a graph node id into a vis-network group."""
    if node_id.startswith(HOST_PREFIX):
        return GROUP_HOST
    if node_id.startswith(SERVICE_PREFIX):
        return GROUP_SERVICE
    return GROUP_OTHER


def _label_for(node_id: str) -> str:
    """Strip the typed prefix from a node id for display."""
    for prefix in (HOST_PREFIX, SERVICE_PREFIX):
        if node_id.startswith(prefix):
            return node_id[len(prefix) :]
    return node_id


def build_live_graph(world: dict[str, Any]) -> dict[str, Any]:
    """Build a live vis-network payload from a world-model snapshot.

    Args:
        world: Parsed ``world_model.json`` content. Missing or malformed
            sections degrade gracefully to an empty graph.

    Returns:
        A dictionary with ``nodes``, ``edges`` and ``stats`` keys. Each node
        carries ``id``, ``label``, ``group``, ``state``, ``centrality``,
        ``value``, ``pulse`` and ``title``. Each edge carries ``from``, ``to``,
        ``relation`` and ``value``.
    """
    world = world or {}
    hosts = world.get("hosts") or {}
    credentials = world.get("credentials") or []
    network_graph = world.get("network_graph") or {}

    graph = NetworkGraph.from_dict(network_graph if isinstance(network_graph, dict) else {})
    centrality = dict(graph.degree_centrality())

    hosts_with_creds: set[str] = set()
    for cred in credentials:
        if isinstance(cred, dict) and cred.get("host"):
            hosts_with_creds.add(f"{HOST_PREFIX}{cred['host']}")

    nodes: list[dict[str, Any]] = []
    seen_nodes: set[str] = set()
    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str]] = set()

    compromised_count = 0
    service_count = 0

    def _emit_node(node_id: str, state: str, title: str) -> None:
        if node_id in seen_nodes:
            return
        seen_nodes.add(node_id)
        score = centrality.get(node_id, 0.0)
        compromised = _is_compromised(state)
        pulse = compromised or score >= PULSE_CENTRALITY_THRESHOLD or node_id in hosts_with_creds
        nodes.append(
            {
                "id": node_id,
                "label": _label_for(node_id),
                "group": _group_for(node_id),
                "state": state,
                "centrality": score,
                "value": _node_value(score),
                "pulse": pulse,
                "title": title,
            }
        )

    def _emit_edge(source: str, target: str, relation: str, weight: float) -> None:
        key = (source, target, relation)
        if key in seen_edges:
            return
        seen_edges.add(key)
        edges.append({"from": source, "to": target, "relation": relation, "value": weight})

    for ip, host in hosts.items():
        if not isinstance(host, dict):
            continue
        state = str(host.get("state") or "unscanned")
        services = host.get("services") or {}
        host_id = f"{HOST_PREFIX}{ip}"
        title = f"{ip} — {state} — {len(services)} service(s)"
        _emit_node(host_id, state, title)
        if _is_compromised(state):
            compromised_count += 1
        for svc in services.values():
            if not isinstance(svc, dict):
                continue
            name = str(svc.get("name") or "unknown")
            service_id = f"{SERVICE_PREFIX}{name}"
            version = str(svc.get("version") or "")
            _emit_node(service_id, "service", f"{name} {version}".strip())
            _emit_edge(host_id, service_id, RUNS_SERVICE_RELATION, 1.0)
            service_count += 1

    for relation in network_graph.get("relations", []) if isinstance(network_graph, dict) else []:
        if not isinstance(relation, dict):
            continue
        source = str(relation.get("source") or "")
        target = str(relation.get("target") or "")
        if not source or not target:
            continue
        _emit_node(source, _group_for(source), source)
        _emit_node(target, _group_for(target), target)
        _emit_edge(
            source,
            target,
            str(relation.get("relation") or "related"),
            float(relation.get("weight") or 1.0),
        )

    stats = {
        "hosts": len(hosts),
        "compromised": compromised_count,
        "services": service_count,
        "credentials": len(credentials),
        "pivots": graph.pivot_candidates(PIVOT_TOP_K),
    }
    return {"nodes": nodes, "edges": edges, "stats": stats}
