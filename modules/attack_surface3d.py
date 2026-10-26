"""Attack-surface 3D intel module: C2-centred campaign graph.

Fuses the live attack surface (``cli.surface_graph``: C2 root, implants,
discovered hosts, open ports, services) with the campaign intel fusion
(``modules.intel_fusion``: objectives, findings, loop tasks, session-log
mentions) into ONE heterogeneous graph rendered with the ReadMenator
node engine (force 2D/3D, circular bundles, spherical view).

Inspiration mapping (kept, not copied):
- estorides entity resolution -> hosts merged by IP across surface scans,
  world model and logs; corroborating artefacts tagged per node.
- CAIRN explorer (Cisco-Talos) toggles/hulls/analytics -> type pills,
  community halos, top-exposed ranking feeding ``intel_summary.json``.
- ReadMenator force/bundle explorers -> verbatim node engine, physics
  sizes, glyphs, legend and inspector; only the data adapters differ.

The reverse leg closes the loop: :func:`refresh_summary` scores host
exposure into ``sessions/intel_summary.json``, which the autonomous
planner consumes, turning session data into information and information
into intelligence on every request.
"""

from __future__ import annotations

import time
from pathlib import Path

try:
    from cli.surface_graph import (
        NODE_C2,
        SurfaceGraphBuilder,
        SurfaceGraphConfig,
    )
except ImportError:  # minimal envs without the cmd2-based cli package
    import importlib.util as _ilu
    import sys as _sys

    _SPEC = _ilu.spec_from_file_location(
        "surface_graph_standalone",
        Path(__file__).resolve().parent.parent / "cli" / "surface_graph.py")
    _MOD = _ilu.module_from_spec(_SPEC)
    _sys.modules[_SPEC.name] = _MOD
    _SPEC.loader.exec_module(_MOD)
    NODE_C2 = _MOD.NODE_C2
    SurfaceGraphBuilder = _MOD.SurfaceGraphBuilder
    SurfaceGraphConfig = _MOD.SurfaceGraphConfig
from modules.intel_fusion import (
    DOC_MAX_CHARS,
    SYMBOLS_PER_NODE,
    TYPE_COLORS,
    build_intel_graph,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

KIND_TO_LAYER = {
    "c2": "infrastructure",
    "client": "utility",
    "host": "presentation",
    "host-owned": "data_access",
    "port": "presentation",
    "service": "business_logic",
    "domain": "presentation",
    "url": "presentation",
    "asn": "infrastructure",
    "email": "utility",
    "mac": "utility",
    "intel": "unknown",
    "finding": "testing",
    "finding-critical": "testing",
    "cve": "testing",
    "objective": "utility",
    "task": "utility",
}

LAYER_COLORS = {
    "presentation": "#22d3ee",
    "business_logic": "#34d399",
    "data_access": "#a78bfa",
    "infrastructure": "#fbbf24",
    "utility": "#94a3b8",
    "testing": "#fb923c",
    "unknown": "#64748b",
}

EDGE_COLORS = {
    "controls": "rgba(245,179,1,.5)",
    "discovered": "rgba(77,163,255,.5)",
    "opens": "rgba(61,220,132,.4)",
    "runs": "rgba(179,136,255,.45)",
    "owns": "rgba(255,77,77,.55)",
    "has_finding": "rgba(255,159,28,.45)",
    "targets": "rgba(179,136,255,.45)",
    "observed_in": "rgba(128,128,128,.4)",
    "member_of": "rgba(167,139,250,.22)",
    "layered_as": "rgba(52,211,153,.16)",
}


def _family_color(name: str) -> str:
    """Stable dusty HSL color from a community name (djb2, ReadMenator)."""
    digest = 5381
    for char in name or "?":
        digest = ((digest << 5) + digest + ord(char)) & 0xFFFFFFFF
    hue = digest % 360
    sat = 55 + ((digest >> 8) % 12)
    lit = 58 + ((digest >> 16) % 10)
    return f"hsl({hue}, {sat}%, {lit}%)"


def _pagerank(ids: list[str], pairs: list[tuple[str, str]],
              alpha: float = 0.85, max_iter: int = 100,
              tol: float = 1e-6) -> dict[str, float]:
    """PageRank over node ids (same contract as ReadMenator rank)."""
    n = len(ids)
    if not n:
        return {}
    index = {nid: i for i, nid in enumerate(ids)}
    out_links: dict[int, list[int]] = {i: [] for i in range(n)}
    for src, dst in pairs:
        if src in index and dst in index and src != dst:
            out_links[index[src]].append(index[dst])
    rank = [1.0 / n] * n
    for _ in range(max_iter):
        nxt = [(1.0 - alpha) / n] * n
        dangling = sum(rank[i] for i in range(n) if not out_links[i])
        for i in range(n):
            nxt[i] += alpha * dangling / n
        for i in range(n):
            if out_links[i]:
                share = alpha * rank[i] / len(out_links[i])
                for j in out_links[i]:
                    nxt[j] += share
        if sum(abs(nxt[i] - rank[i]) for i in range(n)) < tol:
            rank = nxt
            break
        rank = nxt
    return {nid: rank[index[nid]] for nid in ids}


def _host_of(node: dict) -> str:
    """Return the dotted IP a surface node belongs to, or ""."""
    meta = node.get("meta", {})
    return str(meta.get("ip") or meta.get("host_ip") or "")


def build_attack_graph(sessions_dir: str | Path = SESSIONS_DIR,
                       payload_path: str = "payload.json",
                       est_cap: int = 300) -> dict:
    """Fuse surface scans with campaign intel into one C2-centred graph."""
    root = Path(str(sessions_dir))
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_edge(src: str, dst: str, kind: str, evidence: str = "",
                 weight: float = 1.0) -> None:
        """Append one provenance-tagged relation between known nodes."""
        if src in nodes and dst in nodes and src != dst:
            if not any(e["source"] == src and e["target"] == dst
                       and e["type"] == kind for e in edges):
                edges.append({"source": src, "target": dst, "type": kind,
                              "evidence": (evidence or "")[:200],
                              "color": EDGE_COLORS.get(kind, "#808080"),
                              "weight": weight})

    def tag(nid: str, source: str) -> None:
        """Record a corroborating artefact on a node, deduped."""
        if nid in nodes and source not in nodes[nid]["sources"]:
            nodes[nid]["sources"].append(source)

    surface = SurfaceGraphBuilder(SurfaceGraphConfig(
        sessions_dir=str(root), payload_path=payload_path)).build()
    for node in surface.nodes:
        meta = dict(node.metadata)
        kind = node.kind
        value = meta.get("ip", "")
        if kind == "c2":
            value = "lazyown"
        elif kind == "client":
            value = node.id
        elif kind == "port":
            value = f"{meta.get('host_ip', '')}:{meta.get('port', '')}"
        elif kind == "service":
            value = f"{meta.get('host_ip', '')}:{meta.get('port', '')}:{meta.get('service', '')}"
        elif kind == "host":
            value = meta.get("ip", node.label)
        community = "core" if kind in ("c2", "client") else f"net:{_host_of({'meta': meta}) or value}"
        nodes[node.id] = {"id": node.id, "kind": kind, "value": value,
                           "label": node.label, "meta": meta,
                           "color": "#e0e0e0", "community": community,
                           "sources": ["surface"]}
    for edge in surface.edges:
        add_edge(edge.source, edge.target, edge.relation, evidence="surface")

    intel = build_intel_graph(root)
    by_host: dict[str, str] = {}
    for nid, node in nodes.items():
        if node["kind"] == "host":
            by_host[str(node["value"]).lower()] = nid
    key_to_id: dict[tuple[str, str], str] = {}
    for nid, node in nodes.items():
        key_to_id[(node["kind"], str(node["value"]).lower())] = nid
    intel_service_ports: list[dict] = []
    for inode in intel.get("nodes", []):
        if inode.get("type") in ("community", "layer"):
            continue
        ikind = str(inode.get("kind", "intel"))
        ivalue = str(inode.get("value", ""))
        if ikind in ("host", "host-owned") and ivalue.lower() in by_host:
            nid = by_host[ivalue.lower()]
            node = nodes[nid]
            for field in ("os", "state", "log_hits"):
                if inode.get(field) and not node.get(field):
                    node[field] = inode[field]
            if ikind == "host-owned":
                node["owned"] = True
                node["color"] = "#ff4d4d"
            for src in inode.get("sources", []):
                tag(nid, src)
            key_to_id[(ikind, ivalue.lower())] = nid
            key_to_id[("host", ivalue.lower())] = nid
            key_to_id[("host-owned", ivalue.lower())] = nid
        elif ikind == "service":
            intel_service_ports.append(inode)
        elif ikind == "c2":
            if NODE_C2 in nodes:
                for src in inode.get("sources", []):
                    tag(NODE_C2, src)
                key_to_id[("c2", ivalue.lower())] = NODE_C2
        else:
            nid = inode["id"]
            if nid not in nodes:
                nodes[nid] = {"id": nid, "kind": ikind, "value": ivalue,
                              "label": str(inode.get("label", ivalue)),
                              "meta": {}, "color": inode.get("color", "#e0e0e0"),
                              "community": str(inode.get("community_label")
                                               or inode.get("community") or "misc"),
                              "sources": list(inode.get("sources", []))}
                for field in ("severity", "status", "goal", "port", "service",
                              "version", "os", "log_hits", "log_only"):
                    if inode.get(field) is not None:
                        nodes[nid][field] = inode[field]
            key_to_id[(ikind, ivalue.lower())] = nid
    for inode in intel_service_ports:
        host_ip = str(inode.get("community_label", "")).removeprefix("net:")
        merged = False
        for nid, node in nodes.items():
            if node["kind"] == "port" and node["meta"].get("host_ip") == host_ip:
                want = str(inode.get("port", inode.get("value", "").split(":")[-1]))
                if str(node["meta"].get("port")) == want:
                    for src in inode.get("sources", []):
                        tag(nid, src)
                    merged = True
                    break
        if not merged and host_ip:
            hid = by_host.get(host_ip.lower())
            if hid:
                sid = f"svc-{inode['id']}"
                nodes[sid] = {"id": sid, "kind": "service",
                              "value": str(inode.get("value", sid)),
                              "label": str(inode.get("label", sid)), "meta": {},
                              "color": "#3ddc84", "community": f"net:{host_ip}",
                              "sources": list(inode.get("sources", []))}
                key_to_id[("service", str(inode.get("value", "")).lower())] = sid
                add_edge(hid, sid, "serves", evidence="world_model services")
    smap = _intel_id_map(intel, key_to_id)
    for edge in intel.get("edges", []):
        if edge.get("type") in ("member_of", "layered_as"):
            continue
        src = smap.get(edge["source"])
        dst = smap.get(edge["target"])
        if src and dst:
            add_edge(src, dst, str(edge.get("type", "observed_in")),
                     evidence=str(edge.get("evidence", "")),
                     weight=float(edge.get("weight", 1.0)))

    try:
        from modules.estorides_fusion import find_export as _est_find
        from modules.estorides_fusion import load_export as _est_load
        from modules.estorides_fusion import merge_estorides as _est_merge
        est_path = _est_find(root)
        if est_path is not None:
            _est_merge(nodes, edges, _est_load(est_path), cap=est_cap)
    except Exception:
        pass

    try:
        from modules import lazy_surface_diff

        diff = lazy_surface_diff.refresh(None, root)
        if diff.get("changes"):
            touched: dict[str, set] = {}
            for change in diff["changes"][:200]:
                host = str(change.get("host", ""))
                if not host:
                    continue
                touched.setdefault(host, set()).add(str(change.get("kind", "")))
            for host, kinds in touched.items():
                nid = by_host.get(host.lower())
                if nid and nid in nodes:
                    nodes[nid]["changed"] = sorted(kinds)
                    nodes[nid]["changed_at"] = diff.get("ts", 0)
    except Exception:
        pass

    for node in nodes.values():
        node["degree"] = sum(1 for e in edges
                             if e["source"] == node["id"] or e["target"] == node["id"])
    try:
        from modules.finding_lifecycle import apply_confirmation as _apply_conf
        _apply_conf(nodes, root)
    except Exception:
        pass
    _enrich(nodes, edges)
    communities: dict[str, int] = {}
    for node in nodes.values():
        if node.get("type") == "file":
            community = str(node.get("community_label", "misc"))
        else:
            community = str(node.get("community", "misc"))
        communities[community] = communities.get(community, 0) + 1
    stats = {"nodes": len(nodes), "edges": len(edges),
             "hosts": sum(1 for n in nodes.values()
                          if n.get("kind") in ("host", "host-owned")),
             "clients": sum(1 for n in nodes.values() if n.get("kind") == "client"),
             "ports": sum(1 for n in nodes.values() if n.get("kind") == "port"),
             "services": sum(1 for n in nodes.values() if n.get("kind") == "service"),
             "findings": sum(1 for n in nodes.values()
                             if str(n.get("kind", "")).startswith("finding")),
             "communities": communities, "generated": time.time()}
    return {"nodes": list(nodes.values()), "edges": edges, "stats": stats}


def _intel_id_map(intel: dict, key_to_id: dict) -> dict[str, str]:
    """Map every intel node id to its merged attack-graph id."""
    mapping: dict[str, str] = {}
    for node in intel.get("nodes", []):
        if node.get("type") in ("community", "layer"):
            continue
        key = (str(node.get("kind", "intel")), str(node.get("value", "")).lower())
        if key in key_to_id:
            mapping[node["id"]] = key_to_id[key]
    return mapping


def _doc(node: dict) -> str:
    """Bounded purpose string for the inspector."""
    bits = [str(node.get("label", node.get("id", "")))]
    meta = node.get("meta", {})
    for field in ("os", "user", "hostname", "service", "version", "protocol",
                  "severity", "status", "state"):
        val = node.get(field, meta.get(field))
        if val:
            bits.append(f"{field} {val}")
        if field == "service" and node.get("version"):
            break
    if node.get("goal"):
        bits.append(str(node["goal"])[:120])
    sources = node.get("sources") or []
    if sources:
        bits.append("sources: " + ", ".join(sources[:4]))
    return " · ".join(b for b in bits if b)[:DOC_MAX_CHARS]


def _symbols(node: dict) -> list[dict]:
    """Compact symbol records for the inspector (max 40)."""
    out: list[dict] = []
    for idx, src in enumerate(node.get("sources", [])[:8]):
        out.append({"n": str(src)[:60], "k": "source", "l": idx + 1})
    meta = node.get("meta", {})
    if node.get("kind") == "host":
        for port in sorted(meta.get("open_ports", [])):
            out.append({"n": f"{port}/{meta.get('protocol', 'tcp')}", "k": "port",
                        "l": int(port) if str(port).isdigit() else 0})
    if meta.get("service") or node.get("service"):
        out.append({"n": str(meta.get("service") or node.get("service"))[:60],
                    "k": "service", "l": 1})
    if meta.get("user") or node.get("user"):
        out.append({"n": str(meta.get("user") or node.get("user"))[:60],
                    "k": "user", "l": 2})
    return out[:SYMBOLS_PER_NODE]


def _enrich(nodes: dict[str, dict], edges: list[dict]) -> None:
    """Add ReadMenator explorer fields in place (type/layer/rank/doc)."""
    pairs = [(e["source"], e["target"]) for e in edges
             if e["source"] in nodes and e["target"] in nodes]
    rank = _pagerank(sorted(nodes), pairs)
    ordered = sorted(rank.values(), reverse=True)
    port_counts: dict[str, int] = {}
    finding_targets: dict[str, int] = {}
    for edge in edges:
        if edge.get("type") == "opens":
            port_counts[edge["source"]] = port_counts.get(edge["source"], 0) + 1
        if edge.get("type") == "has_finding":
            finding_targets[edge["source"]] = finding_targets.get(edge["source"], 0) + 1
    for nid, node in nodes.items():
        kind = str(node.get("kind", "intel"))
        if kind == "host" and node.get("owned"):
            kind = "host-owned"
            node["kind"] = kind
        community = str(node.get("community", "misc"))
        layer = KIND_TO_LAYER.get(kind, "unknown")
        meta = node.get("meta", {})
        language = str(node.get("os") or meta.get("os") or node.get("service")
                       or meta.get("service") or node.get("severity")
                       or meta.get("protocol") or kind)
        node["type"] = "file"
        node["file"] = str(node.get("value", nid))
        node["language"] = language
        node["symbols"] = max(1, len(node.get("sources", [])) + node.get("degree", 0) // 2)
        node["findings"] = finding_targets.get(nid, 1 if kind.startswith("finding") else 0)
        node["community_label"] = community
        node["family"] = community
        node["layer"] = layer
        node["rank"] = round(rank.get(nid, 0.0), 6)
        node["rank_pos"] = (ordered.index(rank[nid]) + 1) if nid in rank else 0
        node["doc"] = _doc(node)
        node["symbol_list"] = _symbols(node)
        if node.get("kind") == "host":
            node["ports"] = port_counts.get(nid, 0)
        node["familyColor"] = _family_color(community)
        if community and community != "unknown":
            node["color"] = _family_color(community)
            node["familyColor"] = node["color"]
    community_ids: dict[str, int] = {}
    for node in list(nodes.values()):
        label = str(node.get("community", "misc"))
        if label not in community_ids:
            community_ids[label] = len(community_ids)
    counts: dict[str, int] = {}
    for node in nodes.values():
        if node.get("type") != "file":
            continue
        counts[node["community_label"]] = counts.get(node["community_label"], 0) + 1
    for label, cid in community_ids.items():
        hub_id = f"community:{cid}"
        if hub_id not in nodes:
            nodes[hub_id] = {"id": hub_id, "kind": "community", "type": "community",
                             "label": label, "value": label, "community": label,
                             "community_label": label, "family": label,
                             "language": "community", "layer": "unknown",
                             "symbols": counts.get(label, 0), "degree": counts.get(label, 0),
                             "findings": 0, "rank": 0.0, "rank_pos": 0,
                             "doc": f"Community {label} · {counts.get(label, 0)} nodes",
                             "symbol_list": [], "sources": [],
                             "color": TYPE_COLORS["community"],
                             "community_id": cid, "size": counts.get(label, 0),
                             "familyColor": TYPE_COLORS["community"]}
        else:
            nodes[hub_id]["size"] = counts.get(label, 0)
    for node in list(nodes.values()):
        if node.get("type") != "file":
            continue
        cid = community_ids[str(node.get("community", "misc"))]
        hub_id = f"community:{cid}"
        node["community_id"] = cid
        edges.append({"source": node["id"], "target": hub_id,
                      "type": "member_of", "weight": 1,
                      "color": EDGE_COLORS["member_of"], "evidence": "community"})
        layer = str(node.get("layer", "unknown"))
        layer_id = f"layer:{layer}"
        if layer_id not in nodes:
            nodes[layer_id] = {"id": layer_id, "kind": "layer", "type": "layer",
                               "label": layer, "value": layer, "community": "misc",
                               "community_label": "", "family": layer,
                               "language": "layer", "layer": layer,
                               "symbols": 0, "degree": 0, "findings": 0,
                               "rank": 0.0, "rank_pos": 0,
                               "doc": f"Layer {layer}",
                               "symbol_list": [], "sources": [],
                               "color": TYPE_COLORS["layer"],
                               "familyColor": TYPE_COLORS["layer"]}
        edges.append({"source": node["id"], "target": layer_id,
                      "type": "layered_as", "weight": 1,
                      "color": EDGE_COLORS["layered_as"], "evidence": "layer"})


def refresh_summary(graph: dict, sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Score exposure into intel_summary.json for the autonomous loop."""
    from modules.intel_fusion import write_summary

    return write_summary(graph, sessions_dir)


__all__ = ["build_attack_graph", "refresh_summary",
           "NODE_C2", "EDGE_COLORS", "KIND_TO_LAYER"]
