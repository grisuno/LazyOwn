"""Deterministic attack-path solver over the LazyOwn world model.

Given a world-model snapshot the solver builds a weighted digraph and runs
Dijkstra from a virtual ``operator`` source:

- Anchors (already ``exploited``/``owned`` hosts) cost 0 from the operator.
- Vulnerability edges add remote-exploit hops weighted by severity
  (critical is the cheapest route in).
- Credential edges add login hops for confirmed harvested credentials.
- Network-graph relations (``may_authenticate_to``, ``discovered_by``...)
  add observed lateral hops between hosts.

Output is a ranked path list persisted to ``sessions/attack_paths.json``
and optionally injected into ``sessions/objectives.jsonl``.
"""

from __future__ import annotations

import datetime
import heapq
import json
import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

OPERATOR_SOURCE = "operator"
HOST_PREFIX = "host:"
CRED_PREFIX = "cred:"

ARTIFACT_NAME = "attack_paths.json"

SEVERITY_COST: dict[str, float] = {
    "CRITICAL": 1.0,
    "HIGH": 2.0,
    "MEDIUM": 3.0,
    "LOW": 5.0,
    "INFO": 6.0,
    "UNKNOWN": 4.0,
}

RELATION_COST: dict[str, float] = {
    "has_session": 0.1,
    "compromised_from": 0.1,
    "may_authenticate_to": 0.5,
    "exposes_credential": 0.2,
    "discovered_by": 0.4,
    "shares_network_with": 0.3,
}

DEFAULT_RELATION_COST = 0.6

_SOURCE_STATES = frozenset({"owned", "exploited"})

PRIORITY_BANDS: tuple[tuple[float, str], ...] = (
    (1.5, "critical"),
    (3.0, "high"),
    (6.0, "medium"),
)


def _host_node(ip: str) -> str:
    """Return the graph node id for a host IP.

    Args:
        ip: Host IP or bare identifier.

    Returns:
        Prefixed ``host:<ip>`` node id.
    """
    return ip if ip.startswith(HOST_PREFIX) else f"{HOST_PREFIX}{ip}"


def _bare(node: str) -> str:
    """Return the bare identifier of a host or cred node id.

    Args:
        node: Graph node id such as ``host:10.0.0.5`` or ``cred:abcd``.

    Returns:
        The identifier with the prefix stripped.
    """
    if node.startswith(HOST_PREFIX):
        return node[len(HOST_PREFIX):]
    if node.startswith(CRED_PREFIX):
        return node[len(CRED_PREFIX):]
    return node


_NODE_PREFIXES: tuple[str, ...] = (HOST_PREFIX, CRED_PREFIX, "user:", "shell:", "service:")


def _label(node: str) -> str:
    """Return a readable display label for a graph node id.

    Args:
        node: Graph node id with any known prefix.

    Returns:
        The display text without node-type prefixes.
    """
    text = str(node)
    for prefix in _NODE_PREFIXES:
        if text.startswith(prefix):
            return text[len(prefix):]
    return text


def _action_for(relation: str) -> str:
    """Map a graph relation to a human-readable attack step action.

    Args:
        relation: Typed relation name from the network graph.

    Returns:
        The action label used in path steps.
    """
    if relation == "exploit":
        return "exploit"
    if relation == "anchor":
        return "anchor"
    if relation == "exposes_credential":
        return "harvest"
    if relation == "may_authenticate_to":
        return "login"
    if relation in ("discovered_by", "shares_network_with"):
        return "lateral"
    return "pivot"


def _cost_for_relation(relation: str, weight: Any) -> float:
    """Compute the deterministic hop cost for a graph relation.

    Args:
        relation: Typed relation name.
        weight: Relation weight as stored in the graph (may be None).

    Returns:
        A positive cost for Dijkstra.
    """
    base = RELATION_COST.get(relation, DEFAULT_RELATION_COST)
    try:
        numeric = abs(float(weight))
    except (TypeError, ValueError):
        return base
    if numeric <= 0:
        return base
    return base / min(numeric, 4.0)


def build_edges(snapshot: dict) -> dict[str, dict[str, list[dict]]]:
    """Build the weighted adjacency map from a world-model snapshot.

    Args:
        snapshot: Serialised world model (hosts, credentials,
            vulnerabilities, network_graph relations).

    Returns:
        Adjacency mapping ``node -> {next_node -> [edge_meta]}``.
    """
    adjacency: dict[str, dict[str, list[dict]]] = {}

    def _add(src: str, dst: str, relation: str, weight: Any, evidence: str, cost: float | None = None) -> None:
        adjacency.setdefault(src, {}).setdefault(dst, []).append(
            {
                "relation": relation,
                "cost": cost if cost is not None else _cost_for_relation(relation, weight),
                "evidence": evidence,
            }
        )

    graph = snapshot.get("network_graph") or {}
    for rel in graph.get("relations", []) or []:
        src = str(rel.get("source") or "")
        dst = str(rel.get("target") or "")
        relation = str(rel.get("relation") or "")
        if relation == "runs_service":
            continue
        if not src or not dst:
            continue
        is_cred_edge = relation == "exposes_credential"
        if dst.startswith(CRED_PREFIX) or (src.startswith(CRED_PREFIX) and relation == "may_authenticate_to"):
            if not (is_cred_edge or relation == "may_authenticate_to"):
                continue
        _add(src, dst, relation, rel.get("weight"), str(rel.get("attributes") or ""))

    sources = _source_hosts(snapshot)
    for vuln in snapshot.get("vulnerabilities", []) or []:
        host = _bare(str(vuln.get("host") or ""))
        if not host:
            continue
        severity = str(vuln.get("severity") or "UNKNOWN").upper()
        cve = str(vuln.get("cve") or vuln.get("vuln_id") or "")
        label = f"{cve or severity.lower()} {str(vuln.get('description') or '')[:80]}".strip()
        for src in {OPERATOR_SOURCE, *map(_host_node, sources)}:
            _add(src, _host_node(host), "exploit", None, label, cost=SEVERITY_COST.get(severity, 4.0))

    for cred in snapshot.get("credentials", []) or []:
        host = _bare(str(cred.get("host") or ""))
        if not host:
            continue
        value = str(cred.get("value") or "")
        if not value:
            continue
        confirmed = bool(cred.get("confirmed"))
        evidence = f"credential {value.split(':', 1)[0]}{' (confirmed)' if confirmed else ''}"
        _add(OPERATOR_SOURCE, _host_node(host), "may_authenticate_to", None, evidence, cost=0.6 if confirmed else 1.2)

    seen_anchor: set[str] = set()
    for ip in sources:
        node = _host_node(ip)
        if node in seen_anchor:
            continue
        seen_anchor.add(node)
        _add(OPERATOR_SOURCE, node, "anchor", None, "already held foothold", cost=0.0)

    for ip, host in (snapshot.get("hosts") or {}).items():
        adjacency.setdefault(_host_node(ip), {})
        del host
    return adjacency


def _source_hosts(snapshot: dict) -> list[str]:
    """Return hosts the operator already holds (exploited or owned).

    Args:
        snapshot: Serialised world model.

    Returns:
        Sorted list of bare host identifiers usable as path anchors.
    """
    hosts: list[str] = []
    for ip, host in (snapshot.get("hosts") or {}).items():
        state = str((host or {}).get("state") or "").lower()
        if state in _SOURCE_STATES:
            hosts.append(ip)
    return sorted(hosts)


def _diijkstra(adjacency: dict[str, dict[str, list[dict]]], source: str) -> tuple[dict[str, float], dict[str, tuple[str, dict]]]:
    """Run Dijkstra from *source* with deterministic tie-breaking.

    Args:
        adjacency: Weighted adjacency mapping from :func:`build_edges`.
        source: Start node id (virtual operator or a host).

    Returns:
        ``(dist, prev)`` where ``prev[node]`` is the ``(prev_node, edge)``
        tuple used for reconstruction.
    """
    dist: dict[str, float] = {source: 0.0}
    prev: dict[str, tuple[str, dict]] = {}
    visited: set[str] = set()
    heap: list[tuple[float, str]] = [(0.0, source)]
    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        for nxt, edges in sorted(adjacency.get(node, {}).items()):
            edge = min(edges, key=lambda e: (e["cost"], e["relation"], e["evidence"]))
            new_cost = round(cost + edge["cost"], 4)
            if new_cost < dist.get(nxt, float("inf")) - 1e-9:
                dist[nxt] = new_cost
                prev[nxt] = (node, edge)
                heapq.heappush(heap, (new_cost, nxt))
    return dist, prev


def resolve_paths(
    snapshot: dict,
    top_k: int = 5,
    source: str = OPERATOR_SOURCE,
) -> dict:
    """Solve shortest attack paths toward every reachable host.

    Args:
        snapshot: Serialised world model.
        top_k: Maximum number of paths to return (targets ranked by cost).
        source: Virtual start node; ``operator`` anchors help via
            affected hosts.

    Returns:
        Result dict with ``generated_at``, ``sources``, ``paths``, ``stats``.
    """
    adjacency = build_edges(snapshot)
    dist, prev = _diijkstra(adjacency, source)

    anchoring = _source_hosts(snapshot)
    targets: list[str] = []
    for node in sorted(adjacency, key=_bare):
        if node.startswith(HOST_PREFIX) and node != source:
            targets.append(node)

    results: list[dict] = []
    for node in targets:
        ip = _bare(node)
        if dist.get(node, float("inf")) == float("inf"):
            continue
        if ip in anchoring:
            continue
        steps: list[dict] = []
        cur = node
        while cur != source and cur in prev:
            prev_node, edge = prev[cur]
            steps.append(
                {
                    "from": _label(prev_node),
                    "to": _label(cur),
                    "action": _action_for(edge["relation"]),
                    "relation": edge["relation"],
                    "cost": edge["cost"],
                    "evidence": edge["evidence"],
                }
            )
            cur = prev_node
        steps.reverse()
        cost = round(dist[node], 2)
        summary = " -> ".join(
            (f"{_label(s['to'])}[{s['relation']}]" if s["relation"] != "anchor" else _label(s["to"]))
            for s in steps
        )
        results.append(
            {
                "target": ip,
                "cost": cost,
                "summary": summary,
                "steps": steps,
            }
        )

    results = results[:max(1, top_k)] if results else []
    return {
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "sources": anchoring,
        "paths": results,
        "stats": {
            "hosts": len(snapshot.get("hosts") or {}),
            "graph_relations": len(((snapshot.get("network_graph") or {}).get("relations")) or []),
            "vulnerabilities": len(snapshot.get("vulnerabilities") or []),
            "credentials": len(snapshot.get("credentials") or []),
        },
    }


def build(
    world_model_path: str | Path | None = None,
    top_k: int = 5,
    sessions_dir: str | Path | None = None,
) -> dict:
    """Load the live world model, solve paths, and persist the result.

    Args:
        world_model_path: Optional explicit world-model path; defaults to
            the module default used by :class:`modules.world_model.WorldModel`.
        top_k: Maximum paths to render.
        sessions_dir: Optional sessions directory override used for the
            ``attack_paths.json`` artifact.

    Returns:
        The solved result dict (also written to ``sessions/attack_paths.json``).
    """
    from modules.world_model import WorldModel

    wm = WorldModel(path=world_model_path) if world_model_path else WorldModel()
    snapshot = {
        "hosts": {ip: h.to_dict() for ip, h in wm._hosts.items()},
        "credentials": [vars(c) for c in wm._creds],
        "vulnerabilities": [vars(v) for v in wm._vulns],
        "network_graph": wm.graph_snapshot(),
    }
    result = resolve_paths(snapshot, top_k=top_k)
    _persist(result, sessions_dir)
    return result


def _persist(result: dict, sessions_dir: str | Path | None) -> Path:
    """Write the solver result atomically to sessions.

    Args:
        result: Solved path dict.
        sessions_dir: Directory override; defaults to ``sessions/``.

    Returns:
        The artifact path written.
    """
    base = Path(sessions_dir) if sessions_dir else Path("sessions")
    base.mkdir(parents=True, exist_ok=True)
    artifact = base / ARTIFACT_NAME
    tmp = artifact.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, indent=2), encoding="utf-8")
    tmp.replace(artifact)
    log.info("Golden path artifact written: %s (%d paths)", artifact, len(result.get("paths") or []))
    return artifact


def load_artifact(sessions_dir: str | Path | None = None) -> dict:
    """Read the persisted attack-path artifact.

    Args:
        sessions_dir: Directory override; defaults to ``sessions/``.

    Returns:
        The stored dict, or ``{"paths": []}`` when missing/corrupt.
    """
    base = Path(sessions_dir) if sessions_dir else Path("sessions")
    artifact = base / ARTIFACT_NAME
    try:
        return json.loads(artifact.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"paths": []}


def priority_for(cost: float) -> str:
    """Map a path cost to an objective priority band.

    Args:
        cost: Cumulative path cost.

    Returns:
        ``critical``, ``high``, ``medium``, or ``low``.
    """
    for ceiling, priority in PRIORITY_BANDS:
        if cost <= ceiling:
            return priority
    return "low"


def push_objectives(
    paths: Iterable[dict],
    store_path: Path | None = None,
) -> list:
    """Inject one objective per solved path into the objective store.

    Text uses the stable ``target`` + ``cost`` fingerprint so re-pushes
    deduplicate naturally.

    Args:
        paths: Solved path dicts from :func:`resolve_paths`.
        store_path: Optional objectives file override for tests.

    Returns:
        The list of injected (or existing) Objective objects.
    """
    from skills.lazyown_objective import ObjectiveStore

    store = ObjectiveStore(path=store_path) if store_path else ObjectiveStore()
    injected: list = []
    for path in paths:
        target = str(path.get("target") or "")
        cost = float(path.get("cost") or 0.0)
        if not target:
            continue
        summary = str(path.get("summary") or "")
        text = f"Obtain foothold on {target} via {summary} (cost {cost})"
        objective = store.inject(
            text,
            priority=priority_for(cost),
            source="golden_path",
            context={"target": target, "cost": cost, "steps": path.get("steps") or []},
        )
        injected.append(objective)
    return injected
