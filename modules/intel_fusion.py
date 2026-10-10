"""Sessions attack-intel fusion: data -> information -> intelligence.

Reads every campaign artefact under ``sessions/`` (world model, lazy loop
graphs, objectives, scans, event logs) and fuses them into ONE heterogeneous
graph centred on the LazyOwn C2: hosts, ports/services, findings, loop
tasks and objectives. Every node carries a deterministic id
(``sha1(kind:value)``) and every edge an ``evidence`` string naming the
source artefact, so each relation is traceable like a provenance-tracked
research graph.

Payload shape mirrors ReadMenator ``ForceGraphRenderer.build_payload`` so
``templates/intel.html`` (a clone of ReadMenator ``_forcegraph_page``) can
reuse the exact same engine, physics sizes, glyphs, colors, legend and
inspector: file nodes carry ``family``/``layer``/``language``/``rank``/
``doc``/``symbol_list``; community and layer hub nodes plus ``member_of`` /
``layered_as`` structural edges are appended automatically.
"""

from __future__ import annotations

import glob
import hashlib
import json
import math
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

NODE_COLORS = {
    "c2": "#f5b301",
    "host": "#4da3ff",
    "host-owned": "#ff4d4d",
    "service": "#3ddc84",
    "finding": "#ff9f1c",
    "finding-critical": "#ff2d55",
    "objective": "#b388ff",
    "task": "#4dd0e1",
    "intel": "#e0e0e0",
}

EDGE_COLORS = {
    "commands": "rgba(77,163,255,.5)",
    "serves": "rgba(61,220,132,.4)",
    "has_finding": "rgba(255,159,28,.45)",
    "targets": "rgba(179,136,255,.45)",
    "runs": "rgba(77,208,225,.4)",
    "observed_in": "rgba(128,128,128,.4)",
    "owns": "rgba(255,77,77,.55)",
    "member_of": "rgba(167,139,250,.22)",
    "layered_as": "rgba(52,211,153,.16)",
}

SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}

KIND_TO_LAYER = {
    "c2": "infrastructure",
    "host": "presentation",
    "host-owned": "data_access",
    "service": "business_logic",
    "domain": "presentation",
    "url": "presentation",
    "asn": "infrastructure",
    "email": "utility",
    "mac": "utility",
    "finding": "testing",
    "finding-critical": "testing",
    "objective": "utility",
    "task": "utility",
    "intel": "unknown",
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

TYPE_COLORS = {
    "file": "#4f8ef7",
    "community": "#7c5aef",
    "layer": "#4fef8e",
    "external": "#efb84f",
}

DOC_MAX_CHARS = 280
SYMBOLS_PER_NODE = 40


def _family_color(name: str) -> str:
    """Stable dusty HSL color from a community name (djb2, full hue wheel)."""
    digest = 5381
    for char in name or "?":
        digest = ((digest << 5) + digest + ord(char)) & 0xFFFFFFFF
    hue = digest % 360
    sat = 55 + ((digest >> 8) % 12)
    lit = 58 + ((digest >> 16) % 10)
    return f"hsl({hue}, {sat}%, {lit}%)"


def node_id(kind: str, value: str) -> str:
    """Deterministic node id from kind + normalized value."""
    norm = f"{kind}:{(value or '').strip().lower()}"
    return hashlib.sha1(norm.encode()).hexdigest()[:12]


def _load_json(path: Path, default):
    """Load JSON or return default on any failure."""
    try:
        if path.exists():
            return json.loads(path.read_text())
    except (OSError, ValueError):
        pass
    return default


def _read_lines(path: Path, limit: int = 500) -> list[dict]:
    """Read tail JSONL rows, skipping malformed lines."""
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return []
    out = []
    for line in lines[-max(1, limit):]:
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                out.append(item)
        except ValueError:
            continue
    return out


def _host_mentions(text: str) -> list[str]:
    """Extract IPv4 literals from a blob of log text."""
    import re

    return re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text or "")


def _file_pagerank(ids: list[str], pairs: list[tuple[str, str]],
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


def build_intel_graph(sessions_dir: str | Path = SESSIONS_DIR,
                      est_cap: int = 300) -> dict:
    """Fuse all session artefacts into one C2-centred intel graph."""
    root = Path(str(sessions_dir))
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(kind: str, value: str, label: str = "", **extra) -> str:
        """Insert node or merge extra fields into the existing one."""
        nid = node_id(kind, value)
        if nid not in nodes:
            nodes[nid] = {"id": nid, "kind": kind, "value": value,
                          "label": label or value,
                          "color": NODE_COLORS.get(kind, "#e0e0e0"),
                          "community": "misc",
                          "sources": []}
        nodes[nid].update(extra)
        community = nodes[nid].get("community", "misc")
        nodes[nid]["familyColor"] = _family_color(str(community))
        return nid

    def add_edge(src: str, dst: str, kind: str, evidence: str = "", weight: float = 1.0) -> None:
        """Append one provenance-tagged relation."""
        if src in nodes and dst in nodes:
            edges.append({"source": src, "target": dst, "type": kind,
                          "evidence": (evidence or "")[:200],
                          "color": EDGE_COLORS.get(kind, "#808080"),
                          "weight": weight})

    def tag_source(nid: str, source: str) -> None:
        """Record a corroborating artefact on a node, deduped."""
        if nid in nodes and source not in nodes[nid]["sources"]:
            nodes[nid]["sources"].append(source)

    c2_id = add_node("c2", "lazyown", label="LazyOwn C2", degree_hint=0,
                     community="core")

    world = _load_json(root / "world_model.json", {})
    hosts = world.get("hosts", {}) or {}
    if isinstance(hosts, list):
        hosts = {str(h.get("ip", i)): h for i, h in enumerate(hosts) if isinstance(h, dict)}
    owned = set()
    try:
        for row in _read_lines(root / "api_command_audit.jsonl", 2000):
            if str(row.get("result", "")).lower() in ("owned", "root", "system"):
                for ip in _host_mentions(json.dumps(row)):
                    owned.add(ip)
    except Exception:
        pass
    for ip, host in hosts.items():
        if not isinstance(host, dict):
            continue
        kind = "host-owned" if ip in owned else "host"
        hid = add_node(kind, ip, label=ip,
                       os=str(host.get("os_hint", "") or "")[:80],
                       state=str(host.get("state", "")),
                       community=f"net:{ip}")
        tag_source(hid, "world_model.json")
        add_edge(c2_id, hid, "owns" if ip in owned else "commands",
                 evidence=f"world_model phase={world.get('phase', '')}")
        services = host.get("services", {}) or {}
        items = services.items() if isinstance(services, dict) else []
        for port, svc in items:
            svc = svc if isinstance(svc, dict) else {"name": str(svc)}
            name = str(svc.get("name", "unknown"))
            sid = add_node("service", f"{ip}:{port}",
                           label=f"{ip}:{port} {name}",
                           port=str(port), service=name,
                           version=str(svc.get("version", "") or "")[:60],
                           community=f"net:{ip}")
            tag_source(sid, "world_model.json")
            add_edge(hid, sid, "serves", evidence=f"world_model services[{port}]={name}")
    for vuln in world.get("vulnerabilities", []) or []:
        if not isinstance(vuln, dict):
            continue
        host_ip = str(vuln.get("host", "") or vuln.get("ip", "") or "")
        sev = str(vuln.get("severity", "info")).lower()
        fid = add_node("finding-critical" if sev == "critical" else "finding",
                       str(vuln.get("id", vuln.get("title", "")))[:120],
                       label=str(vuln.get("title", "finding"))[:120],
                       severity=sev,
                       community=f"net:{host_ip}" if host_ip else "intel")
        tag_source(fid, "world_model.json")
        if host_ip and node_id("host", host_ip) in nodes:
            add_edge(node_id("host", host_ip), fid, "has_finding",
                     evidence="world_model vulnerabilities")
        elif host_ip and node_id("host-owned", host_ip) in nodes:
            add_edge(node_id("host-owned", host_ip), fid, "has_finding",
                     evidence="world_model vulnerabilities")

    lazy_dir = root / "lazy"
    tasks = {}
    try:
        tasks = _load_json(lazy_dir / "tasks.json", {}).get("tasks", {}) or {}
    except Exception:
        tasks = {}
    for task_id, record in tasks.items():
        if not isinstance(record, dict):
            continue
        scoped = [str(s.get("value", "")) for s in record.get("scope", []) or []
                  if s.get("value")]
        task_community = f"net:{scoped[0]}" if scoped else "loop"
        tid = add_node("task", task_id, label=f"{task_id}: {str(record.get('goal', ''))[:60]}",
                       status=str(record.get("status", "")),
                       goal=str(record.get("goal", ""))[:200],
                       community=task_community)
        tag_source(tid, "sessions/lazy/tasks.json")
        add_edge(c2_id, tid, "runs", evidence="lazy task registry")
        for scope in record.get("scope", []) or []:
            val = str(scope.get("value", ""))
            for kind in ("host", "host-owned"):
                if node_id(kind, val) in nodes:
                    add_edge(tid, node_id(kind, val), "targets",
                             evidence=f"lazy scope {scope.get('kind')}:{val}")
        try:
            exp = _load_json(lazy_dir / f"exp_{task_id}.json", {})
            for node in exp.get("nodes", []) or []:
                if not isinstance(node, dict) or node.get("kind") != "finding":
                    continue
                meta = node.get("meta", {}) or {}
                sev = str(meta.get("severity", "info")).lower()
                fid = add_node("finding-critical" if sev == "critical" else "finding",
                               f"{task_id}#{node.get('node_id')}",
                               label=str(node.get("text", ""))[:120],
                               severity=sev, status=str(meta.get("status", "")),
                               community=task_community)
                tag_source(fid, f"sessions/lazy/exp_{task_id}.json")
                add_edge(tid, fid, "has_finding",
                         evidence=f"lazy {task_id} finding #{node.get('node_id')}")
        except Exception:
            continue

    for row in _read_lines(root / "objectives.jsonl", 200):
        text = str(row.get("objective", "") or row.get("text", "") or "")[:160]
        if not text:
            continue
        oid = add_node("objective", text, label=text,
                       status=str(row.get("status", "")),
                       community="mission")
        tag_source(oid, "objectives.jsonl")
        add_edge(c2_id, oid, "targets", evidence="objectives queue")
        for ip in _host_mentions(text):
            for kind in ("host", "host-owned"):
                if node_id(kind, ip) in nodes:
                    add_edge(oid, node_id(kind, ip), "targets",
                             evidence="objective mentions host")

    log_hits: dict[str, int] = {}
    for name in ("autonomous_events.jsonl", "access.log", "api_command_audit.jsonl"):
        for row in _read_lines(root / name, 500):
            for ip in _host_mentions(json.dumps(row)):
                log_hits[ip] = log_hits.get(ip, 0) + 1
    for ip, count in sorted(log_hits.items(), key=lambda kv: -kv[1])[:60]:
        for kind in ("host", "host-owned"):
            nid = node_id(kind, ip)
            if nid in nodes:
                nodes[nid]["log_hits"] = count
                tag_source(nid, "session logs")
                break
        else:
            lid = add_node("host", ip, label=f"{ip} (log-only)", log_only=True,
                           community=f"net:{ip}")
            nodes[lid]["log_hits"] = count
            tag_source(lid, "session logs")
            add_edge(c2_id, lid, "observed_in", evidence="mentioned in session logs",
                     weight=min(3.0, 0.5 + count / 20.0))

    for path in sorted(glob.glob(str(root / "scan_*.nmap*")))[:20]:
        tag = Path(path).name
        try:
            blob = Path(path).read_text()[:20000]
        except OSError:
            continue
        for ip in set(_host_mentions(blob)):
            for kind in ("host", "host-owned"):
                nid = node_id(kind, ip)
                if nid in nodes:
                    tag_source(nid, tag)
                    break

    try:
        from modules.estorides_fusion import find_export as _est_find
        from modules.estorides_fusion import load_export as _est_load
        from modules.estorides_fusion import merge_estorides as _est_merge
        est_path = _est_find(root)
        if est_path is not None:
            _est_merge(nodes, edges, _est_load(est_path), cap=est_cap)
    except Exception:
        pass

    for node in nodes.values():
        node["degree"] = sum(1 for e in edges if e["source"] == node["id"] or e["target"] == node["id"])
        node["value_rank"] = round(math.log2(2 + node["degree"]), 2)
    try:
        from modules.finding_lifecycle import apply_confirmation as _apply_conf
        _apply_conf(nodes, root)
    except Exception:
        pass
    _enrich_readmenator_fields(nodes, edges)
    communities: dict[str, int] = {}
    for node in nodes.values():
        if node.get("type") == "file":
            community = str(node.get("community_label", node.get("community", "misc")))
        else:
            community = str(node.get("community", "misc"))
        communities[community] = communities.get(community, 0) + 1
    return {"nodes": list(nodes.values()), "edges": edges,
            "stats": {"nodes": len(nodes), "edges": len(edges),
                      "hosts": sum(1 for n in nodes.values() if n["kind"] in ("host", "host-owned")),
                      "findings": sum(1 for n in nodes.values() if n["kind"].startswith("finding")),
                      "communities": communities,
                      "generated": time.time()}}


def _node_doc(node: dict) -> str:
    """Bounded purpose string for the inspector (ReadMenator contract)."""
    bits = [str(node.get("label", node.get("id", "")))]
    if node.get("os"):
        bits.append(f"os {node['os']}")
    if node.get("service"):
        extra = str(node["service"])
        if node.get("version"):
            extra += f" {node['version']}"
        bits.append(extra)
    if node.get("severity"):
        bits.append(f"severity {node['severity']}")
    if node.get("status"):
        bits.append(f"status {node['status']}")
    if node.get("goal"):
        bits.append(str(node["goal"])[:120])
    sources = node.get("sources") or []
    if sources:
        bits.append("sources: " + ", ".join(sources[:4]))
    text = " · ".join(b for b in bits if b)[:DOC_MAX_CHARS]
    return text


def _symbol_list(node: dict) -> list[dict]:
    """Compact symbol records for the inspector (max 40)."""
    out: list[dict] = []
    sources = node.get("sources") or []
    for idx, src in enumerate(sources[:8]):
        out.append({"n": str(src)[:60], "k": "source", "l": idx + 1})
    if node.get("service"):
        out.append({"n": str(node["service"])[:60], "k": "service", "l": 1})
    if node.get("os"):
        out.append({"n": str(node["os"])[:60], "k": "platform", "l": 2})
    if node.get("goal"):
        out.append({"n": str(node["goal"])[:80], "k": "intent", "l": 3})
    return out[:SYMBOLS_PER_NODE]


def _enrich_readmenator_fields(nodes: dict[str, dict], edges: list[dict]) -> None:
    """Add ReadMenator explorer fields in place (type/file/layer/rank/doc)."""
    pairs = [(e["source"], e["target"]) for e in edges
             if e["source"] in nodes and e["target"] in nodes]
    rank = _file_pagerank(sorted(nodes), pairs)
    ordered = sorted(rank.values(), reverse=True)
    finding_targets: dict[str, int] = {}
    for edge in edges:
        if edge.get("type") == "has_finding":
            finding_targets[edge["source"]] = finding_targets.get(edge["source"], 0) + 1
    for nid, node in nodes.items():
        kind = str(node.get("kind", "intel"))
        community = str(node.get("community", "misc"))
        layer = KIND_TO_LAYER.get(kind, "unknown")
        language = str(node.get("os") or node.get("service")
                       or node.get("severity") or node.get("status") or kind)
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
        node["doc"] = _node_doc(node)
        node["symbol_list"] = _symbol_list(node)
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
        edges.append({"source": f"file:{node['id']}" if False else node["id"],
                      "target": hub_id, "type": "member_of", "weight": 1,
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


def group_colors(graph: dict) -> dict:
    """Stable colors for layer/language groupings (ReadMenator contract)."""
    layers: dict[str, str] = {}
    languages: dict[str, str] = {}
    for node in graph.get("nodes", []):
        if node.get("type") != "file":
            continue
        layer = str(node.get("layer") or "unknown")
        language = str(node.get("language") or "unknown")
        if layer not in layers:
            layers[layer] = LAYER_COLORS.get(layer) or _family_color(layer)
        if language not in languages:
            languages[language] = _family_color(language)
    return {"layer": layers, "language": languages}


def page_settings(graph: dict | None = None) -> dict:
    """Explorer page settings with ReadMenator physics sizes (exact values)."""
    return {
        "charge": -300,
        "linkDistance": 120,
        "linkStrength": 0.3,
        "nodeRelSize": 4,
        "hulls": True,
        "hullFill": 0.07,
        "hullStroke": 0.5,
        "hullPad": 18,
        "particles": 4,
        "dimNode": "rgba(80,85,110,.4)",
        "dimLink": "rgba(255,255,255,.04)",
        "mode": "2d",
        "labelTopN": 30,
        "labelZoom": 1.6,
        "labelMax": 28,
        "labelHighlightMax": 60,
        "clusterStrength": 0.6,
        "collidePad": 4,
        "collideMaxNodes": 1500,
        "dagLevel": 60,
        "flyMs": 700,
        "flyZoom": 3.0,
        "searchResults": 8,
        "symbolTotal": 40,
        "hitPad": 3.0,
        "minHitPx": 7.0,
        "edgeHitPx": 5.0,
        "dragPx": 4.0,
        "curveStep": 0.18,
        "curveSamples": 16,
        "arrowLen": 4.0,
        "arrowZoom": 2.2,
        "cooldownTicks": 400,
        "cooldownTicksReduced": 60,
        "docLinesPx": 9.0,
        "tipDocChars": 200,
        "hubTopN": 10,
        "fitPad": 48,
        "fitMaxZoom": 2.5,
        "fitLegendMinWidth": 700,
        "linkOpacity3d": 0.5,
        "linkWidth3dHighlight": 0.7,
        "linkWidth3dActive": 1.4,
        "particleWidth3d": 1.3,
        "depthFade": 0.3,
        "minGlyphPx": 2.5,
        "label3dPx": 9.0,
        "orbitSpeed": 0.6,
        "flyDistance3d": 320,
        "typeColors": dict(TYPE_COLORS),
        "groupColors": group_colors(graph or {"nodes": []}),
    }


def build_analytics(graph: dict, summary: dict | None = None) -> dict:
    """Side-panel analytics (attribution funnel + intel summary)."""
    stats = graph.get("stats", {}) or {}
    nodes = graph.get("nodes", []) or []
    total_symbols = sum(int(n.get("symbols", 0) or 0) for n in nodes if n.get("type") == "file")
    return {
        "attribution_funnel": {
            "total": stats.get("nodes", len(nodes)),
            "total_symbols": total_symbols,
            "god_nodes": len(summary.get("top_exposed", []) if summary else []),
        },
        "intel": summary or {},
    }


BUNDLE_RELATIONS = ("commands", "owns", "serves", "has_finding",
                      "targets", "runs", "observed_in",
                      "controls", "discovered", "opens")

BUNDLE_UNASSIGNED = "unassigned"
BUNDLE_COORD_DIGITS = 5
BUNDLE_INNER_RATIO = 0.55
BUNDLE_GROUP_GAP = 0.04


def _fibonacci_sphere(count: int) -> list[tuple[float, float, float]]:
    """Nearly uniform unit vectors on a golden-angle spiral, north to south."""
    if count <= 0:
        return []
    if count == 1:
        return [(0.0, -1.0, 0.0)]
    golden = math.pi * (3.0 - math.sqrt(5.0))
    out = []
    for i in range(count):
        y = 1.0 - 2.0 * (i + 0.5) / count
        ring = math.sqrt(max(0.0, 1.0 - y * y))
        theta = golden * i
        out.append((ring * math.cos(theta), y, ring * math.sin(theta)))
    return out


def _split_caps(labels: list[str], sizes: dict[str, int], points: list[int],
                lattice: list[tuple[float, float, float]],
                out: dict[str, list[int]]) -> None:
    """Bisect lattice points between runs of groups of matching size."""
    if len(labels) == 1:
        out[labels[0]] = points
        return
    total = sum(sizes[label] for label in labels)
    best, cut, running = total, 1, 0
    for i in range(1, len(labels)):
        running += sizes[labels[i - 1]]
        gap = abs(2 * running - total)
        if gap < best:
            best, cut = gap, i
    left_count = sum(sizes[label] for label in labels[:cut])
    spread = []
    for k in range(3):
        values = [lattice[pi][k] for pi in points]
        spread.append(max(values) - min(values))
    axis = max(range(3), key=lambda k: (spread[k], -k))
    ordered = sorted(points, key=lambda pi: (lattice[pi][axis], pi))
    _split_caps(labels[:cut], sizes, ordered[:left_count], lattice, out)
    _split_caps(labels[cut:], sizes, ordered[left_count:], lattice, out)


def _unit(vec) -> tuple[float, float, float]:
    """Normalize a 3D vector (zero vectors map to the south pole)."""
    norm = math.sqrt(sum(c * c for c in vec))
    if norm < 1e-12:
        return (0.0, -1.0, 0.0)
    return (vec[0] / norm, vec[1] / norm, vec[2] / norm)


def build_bundle_payload(graph: dict) -> dict:
    """Derive the circular/spherical bundle payload from a fused graph.

    Communities keep size order (largest first); ``misc`` nodes form a
    trailing unassigned group. Inside a group files are ordered by rank,
    so hubs sit at the center of their arc and cap. Edges are distinct
    directed file index pairs.
    """
    files = sorted(
        (n for n in graph.get("nodes", []) if n.get("type") == "file"),
        key=lambda n: str(n.get("id", "")),
    )
    if not files:
        return {"nodes": [], "groups": [], "edges": []}
    member_key: dict[str, str] = {}
    group_label: dict[str, str] = {}
    for node in files:
        label = str(node.get("community_label") or node.get("community") or "misc")
        key = BUNDLE_UNASSIGNED if label == "misc" else label
        member_key[node["id"]] = key
        group_label.setdefault(key, "unassigned" if key == BUNDLE_UNASSIGNED else label)
    ordered_keys = sorted(
        (k for k in group_label if k != BUNDLE_UNASSIGNED),
        key=lambda k: (-sum(1 for n in files if member_key[n["id"]] == k), k),
    )
    if any(member_key[n["id"]] == BUNDLE_UNASSIGNED for n in files):
        ordered_keys.append(BUNDLE_UNASSIGNED)
    members: dict[str, list[str]] = {key: [] for key in ordered_keys}
    for node in sorted(files, key=lambda n: (-float(n.get("rank", 0.0)), str(n["id"]))):
        members[member_key[node["id"]]].append(node["id"])
    total = sum(len(members[k]) for k in ordered_keys)
    usable = 2 * math.pi - BUNDLE_GROUP_GAP * len(ordered_keys)
    step = usable / max(1, total)
    angle = -math.pi / 2
    angles: dict[str, float] = {}
    arcs: dict[str, tuple[float, float]] = {}
    for key in ordered_keys:
        start = angle
        for nid in members[key]:
            angles[nid] = angle + step / 2
            angle += step
        arcs[key] = (start, angle)
        angle += BUNDLE_GROUP_GAP
    lattice = _fibonacci_sphere(total)
    regions: dict[str, list[int]] = {}
    _split_caps(ordered_keys, {k: len(members[k]) for k in ordered_keys},
                list(range(total)), lattice, regions)
    leaves: dict[str, tuple[float, float, float]] = {}
    hubs: dict[str, tuple[float, float, float]] = {}
    caps: dict[str, tuple[float, float, float]] = {}
    for key in ordered_keys:
        region = regions[key]
        center = _unit([sum(lattice[pi][k] for pi in region) for k in range(3)])
        caps[key] = center
        ordered_pts = sorted(
            region, key=lambda pi: (-sum(lattice[pi][k] * center[k] for k in range(3)), pi))
        for nid, pi in zip(members[key], ordered_pts, strict=True):
            leaves[nid] = lattice[pi]
        hubs[key] = (center[0] * BUNDLE_INNER_RATIO, center[1] * BUNDLE_INNER_RATIO,
                     center[2] * BUNDLE_INNER_RATIO)
    group_index = {key: i for i, key in enumerate(ordered_keys)}
    fallback = TYPE_COLORS["file"]
    groups = []
    for key in ordered_keys:
        start, end = arcs[key]
        mid = (start + end) / 2
        ratio = BUNDLE_INNER_RATIO
        name = group_label[key]
        groups.append({
            "k": key,
            "l": name,
            "c": fallback if key == BUNDLE_UNASSIGNED else _family_color(name),
            "n": len(members[key]),
            "a0": round(start, BUNDLE_COORD_DIGITS),
            "a1": round(end, BUNDLE_COORD_DIGITS),
            "h2": [round(ratio * math.cos(mid), BUNDLE_COORD_DIGITS),
                   round(ratio * math.sin(mid), BUNDLE_COORD_DIGITS)],
            "h3": [round(v, BUNDLE_COORD_DIGITS) for v in hubs[key]],
            "u": [round(v, BUNDLE_COORD_DIGITS) for v in caps[key]],
        })
    index = {node["id"]: i for i, node in enumerate(files)}
    nodes = []
    for node in files:
        nid = node["id"]
        key = member_key[nid]
        nodes.append({
            "id": nid,
            "f": str(node.get("file") or node.get("value") or nid),
            "l": str(node.get("label") or nid),
            "g": group_index[key],
            "c": str(node.get("color") or fallback),
            "ly": str(node.get("layer") or "unknown"),
            "lg": str(node.get("language") or "unknown"),
            "r": float(node.get("rank", 0.0)),
            "rp": int(node.get("rank_pos", 0)),
            "fd": int(node.get("findings", 0)),
            "d": str(node.get("doc") or ""),
            "a": round(angles[nid], BUNDLE_COORD_DIGITS),
            "p": [round(v, BUNDLE_COORD_DIGITS) for v in leaves[nid]],
        })
    pairs = sorted({
        (index[e["source"]], index[e["target"]])
        for e in graph.get("edges", [])
        if e.get("type") in BUNDLE_RELATIONS
        and e.get("source") in index and e.get("target") in index
        and e["source"] != e["target"]
    })
    return {"nodes": nodes, "groups": groups, "edges": [list(p) for p in pairs]}


def bundle_settings(graph: dict | None = None) -> dict:
    """Bundle page settings with ReadMenator sizes (exact values)."""
    return {
        "mode": "2d",
        "beta": 0.85,
        "samples": 20,
        "edgeAlpha": 0.30,
        "dimAlpha": 0.035,
        "labelAllMax": 140,
        "labelTopN": 24,
        "labelMax": 26,
        "nodeMin": 2.0,
        "nodeMax": 7.0,
        "hitPx": 9.0,
        "rotateSpeed": 0.12,
        "perspective": 3.0,
        "depthFade": 0.7,
        "particles": 3,
        "revealMs": 1400,
        "flowTopN": 8,
        "listMax": 40,
        "searchResults": 8,
        "tipDocChars": 200,
        "dragPx": 4.0,
        "flyMs": 700,
        "explorerHref": "/intel",
        "unassignedKey": BUNDLE_UNASSIGNED,
        "groupColors": group_colors(graph or {"nodes": []}),
    }


def assign_layout(graph: dict, mode: str = "force") -> dict:
    """Attach x/y/z for radial/spherical modes; force modes stay free.

    Accepts ReadMenator layout names (``force``, ``cluster``, ``radial``,
    ``dag``) plus legacy intel names (``force2d``, ``force3d``,
    ``circular``, ``spherical``). Force-family modes return without preset
    positions so the client physics (charge -300, distance 120, 400 ticks
    + fit-to-view) places every graph on screen.
    """
    nodes = graph.get("nodes", []) or []
    norm = (mode or "force").lower()
    if norm in ("force", "force2d", "force3d", "cluster", "dag"):
        for node in nodes:
            node.pop("x", None)
            node.pop("y", None)
            node.pop("z", None)
        return graph
    if norm == "circular":
        norm = "radial"
    groups: dict[str, list[dict]] = {}
    for node in nodes:
        if node.get("type") not in (None, "file"):
            continue
        groups.setdefault(str(node.get("community_label") or node.get("community", "?")), []).append(node)
    if norm == "radial":
        radius = 320.0
        kinds = sorted(groups)
        for idx, kind in enumerate(kinds):
            members = groups[kind]
            base = 2 * math.pi * idx / max(1, len(kinds))
            for j, node in enumerate(members):
                angle = base + 2 * math.pi * j / max(1, len(members))
                spread = radius * (0.55 + 0.45 * (kinds.index(kind) + 1) / len(kinds))
                node["x"] = round(spread * math.cos(angle), 1)
                node["y"] = round(spread * math.sin(angle), 1)
                node["z"] = 0
    else:
        radius = 300.0
        flat = [n for kind in sorted(groups) for n in groups[kind]]
        total = len(flat)
        for i, node in enumerate(flat):
            phi = math.acos(1 - 2 * (i + 0.5) / max(1, total))
            theta = math.pi * (1 + math.sqrt(5)) * i
            node["x"] = round(radius * math.sin(phi) * math.cos(theta), 1)
            node["y"] = round(radius * math.sin(phi) * math.sin(theta), 1)
            node["z"] = round(radius * math.cos(phi), 1)
    for node in nodes:
        if "x" in node:
            continue
        if node.get("type") == "community":
            members = groups.get(str(node.get("label", "")), [])
            if members:
                node["x"] = round(sum(m.get("x", 0) for m in members) / len(members), 1)
                node["y"] = round(sum(m.get("y", 0) for m in members) / len(members), 1)
                node["z"] = round(sum(m.get("z", 0) for m in members) / len(members), 1)
            else:
                node.update({"x": 0.0, "y": 0.0, "z": 0.0})
        else:
            node.update({"x": 0.0, "y": 0.0, "z": 0.0})
    c2 = next((n for n in nodes if n.get("kind") == "c2"), None)
    if c2 is not None:
        c2.update({"x": 0, "y": 0, "z": 0})
    return graph


def write_summary(graph: dict, sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Score host exposure and suggest intents for the autonomous planner."""
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    scores: dict[str, float] = {}
    for node in nodes:
        if node.get("kind") not in ("host", "host-owned"):
            continue
        score = 1.0 + node.get("degree", 0)
        score += 5.0 if node.get("kind") == "host-owned" else 0.0
        score += min(5.0, float(node.get("log_hits", 0)) / 10.0)
        scores[node["value"]] = round(score, 2)
    for edge in edges:
        target = next((n for n in nodes if n["id"] == edge.get("target")), None)
        if target is not None and target.get("kind", "").startswith("finding"):
            sev = SEV_RANK.get(str(target.get("severity", "info")), 4)
            src = next((n for n in nodes if n["id"] == edge.get("source")), None)
            if src is not None and src.get("value") in scores:
                scores[src["value"]] = round(scores[src["value"]] + (5 - sev), 2)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    hosts = [n for n in nodes if n.get("kind") in ("host", "host-owned")]
    with_services = set()
    with_findings = set()
    confirmed_finding_ids = set()
    for node in nodes:
        if (str(node.get("kind", "")).startswith("finding")
                and node.get("confirmation", "pending") == "confirmed"):
            confirmed_finding_ids.add(node["id"])
    confirmed_hosts = set()
    for edge in edges:
        if edge.get("type") in ("serves", "opens", "runs"):
            with_services.add(edge.get("source"))
        if edge.get("type") == "has_finding":
            with_findings.add(edge.get("source"))
            if edge.get("target") in confirmed_finding_ids:
                confirmed_hosts.add(edge.get("source"))
    host_ids = {n["id"] for n in hosts}
    owned = sorted(n["value"] for n in hosts
                   if n.get("kind") == "host-owned" or n.get("owned"))
    owned_confirmed = sorted(v for v in owned
                             if v in {n.get("value") for n in hosts
                                      if n["id"] in confirmed_hosts})
    funnel = [
        {"stage": "discovered", "hosts": len(hosts)},
        {"stage": "with services",
         "hosts": len([h for h in with_services if h in host_ids])},
        {"stage": "with findings",
         "hosts": len([h for h in with_findings if h in host_ids])},
        {"stage": "confirmed",
         "hosts": len([h for h in confirmed_hosts if h in host_ids])},
        {"stage": "owned",
         "hosts": len(owned_confirmed)},
    ]
    source_yield: dict[str, int] = {}
    for node in nodes:
        if not str(node.get("kind", "")).startswith("finding"):
            continue
        for src in node.get("sources", []) or []:
            source_yield[str(src)] = source_yield.get(str(src), 0) + 1
    summary = {"generated": time.time(),
               "hosts_scored": len(ranked),
               "top_exposed": [{"host": host, "score": score} for host, score in ranked[:10]],
               "suggested_intents": [
                   f"probe {host} (intel exposure {score})" for host, score in ranked[:5]],
               "funnel": funnel,
               "confirmed_hosts": sorted(n.get("value") for n in hosts
                                         if n["id"] in confirmed_hosts),
               "owned_hosts": owned,
               "source_yield": dict(sorted(source_yield.items(),
                                           key=lambda kv: -kv[1])),
               "stats": graph.get("stats", {})}
    try:
        dest = Path(str(sessions_dir)) / "intel_summary.json"
        dest.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    except OSError:
        pass
    return summary


__all__ = ["build_intel_graph", "assign_layout", "write_summary", "node_id",
           "NODE_COLORS", "EDGE_COLORS", "page_settings", "group_colors",
           "build_analytics", "build_bundle_payload", "bundle_settings"]
