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
import re
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
    "cve": "#ff6b35",
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

# Normalized host score: every component is capped so the total stays
# within 0..100 and each earned point carries a label the operator can
# read ("why the score is N").
SCORE_CAP_TOTAL = 100
HEAT_POINTS = {"hot": 40.0, "warm": 20.0, "cold": 5.0}
HEAT_CAP = 50.0
FINDING_POINTS = {"critical": 25.0, "high": 25.0, "medium": 10.0, "low": 3.0}
FINDINGS_CAP = 25.0
OWNED_POINTS, OWNED_CAP = 10.0, 10.0
CONNECTIVITY_CAP = 10.0
ACTIVITY_CAP = 5.0
RECENCY_CAP = 10.0
RECENCY_NEW = 10.0
RECENCY_EXPOSURE = 5.0
GHOST_CAP = 15.0
LIFECYCLE_KINDS = ("host_new", "host_returned")
EXPOSURE_KINDS = ("port_opened", "port_closed", "service_changed", "os_changed")

_CVE_TEXT_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)

_CVE_CORRELATION_CACHE: dict[str, list[dict]] = {}
_CVE_CORRELATION_CAP_SERVICES = 40


def _service_cve_matches(service_name: str, version_text: str, svc: dict) -> list[dict]:
    """Heat-graded CVE candidates for one world-model service row.

    Correlation is cache-only (``allow_network=False``) so graph
    rebuilds stay fast and offline; a feed that was never downloaded
    degrades to no candidates instead of blocking the graph.

    Args:
        service_name: nmap service name (``ftp``, ``ssh``).
        version_text: Version/product text captured for the service.
        svc: Full service row (``version`` carries the full banner).

    Returns:
        List of ``{cve, heat, cvss, kev, epss, exploit, in_range,
        heat_rank}`` rows, hottest first.
    """
    banner = str(svc.get("version", "") or version_text or service_name or "")
    if not banner.strip():
        return []
    cache_key = banner.lower()
    if cache_key in _CVE_CORRELATION_CACHE:
        return _CVE_CORRELATION_CACHE[cache_key]
    if len(_CVE_CORRELATION_CACHE) > _CVE_CORRELATION_CAP_SERVICES:
        return []
    try:
        from modules import lazy_cve_feed
        from modules.lazy_heat import HEAT_RANK

        rows = lazy_cve_feed.correlate(banner, "", allow_network=False)
        graded = [
            {
                "cve": row["cve"],
                "heat": row.get("heat", "cold"),
                "cvss": row.get("cvss", 0.0),
                "kev": row.get("kev", False),
                "epss": row.get("epss"),
                "exploit": row.get("exploit", False),
                "in_range": row.get("in_range"),
                "heat_rank": HEAT_RANK.get(row.get("heat", "cold"), 0),
            }
            for row in rows
            if row.get("heat") != "cold" or row.get("kev")
        ]
        _CVE_CORRELATION_CACHE[cache_key] = graded[:8]
    except Exception:
        _CVE_CORRELATION_CACHE.pop(cache_key, None)
        return []
    return _CVE_CORRELATION_CACHE[cache_key]


def _extract_cve_id(vuln: dict) -> str:
    """Best CVE id from one world-model vulnerability row."""
    for source in (vuln.get("cve", ""), vuln.get("id", ""), vuln.get("title", "")):
        match = _CVE_TEXT_RE.search(str(source or ""))
        if match:
            return match.group(0).upper()
    return ""


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
    "cve": "testing",
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
    for line in lines[-max(1, limit) :]:
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                out.append(item)
        except ValueError:
            continue
    return out


def _host_mentions(text: str) -> list[str]:
    """Extract IPv4 literals from a blob of log text."""
    return re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text or "")


def _file_pagerank(
    ids: list[str], pairs: list[tuple[str, str]], alpha: float = 0.85, max_iter: int = 100, tol: float = 1e-6
) -> dict[str, float]:
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


def build_intel_graph(sessions_dir: str | Path = SESSIONS_DIR, est_cap: int = 300) -> dict:
    """Fuse all session artefacts into one C2-centred intel graph."""
    root = Path(str(sessions_dir))
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(kind: str, value: str, label: str = "", **extra) -> str:
        """Insert node or merge extra fields into the existing one."""
        nid = node_id(kind, value)
        if nid not in nodes:
            nodes[nid] = {
                "id": nid,
                "kind": kind,
                "value": value,
                "label": label or value,
                "color": NODE_COLORS.get(kind, "#e0e0e0"),
                "community": "misc",
                "sources": [],
            }
        nodes[nid].update(extra)
        community = nodes[nid].get("community", "misc")
        nodes[nid]["familyColor"] = _family_color(str(community))
        return nid

    def add_edge(src: str, dst: str, kind: str, evidence: str = "", weight: float = 1.0) -> None:
        """Append one provenance-tagged relation, deduped by (src, dst, kind)."""
        if src in nodes and dst in nodes:
            if any(e["source"] == src and e["target"] == dst and e["type"] == kind for e in edges):
                return
            edges.append(
                {
                    "source": src,
                    "target": dst,
                    "type": kind,
                    "evidence": (evidence or "")[:200],
                    "color": EDGE_COLORS.get(kind, "#808080"),
                    "weight": weight,
                }
            )

    def tag_source(nid: str, source: str) -> None:
        """Record a corroborating artefact on a node, deduped."""
        if nid in nodes and source not in nodes[nid]["sources"]:
            nodes[nid]["sources"].append(source)

    c2_id = add_node("c2", "lazyown", label="LazyOwn C2", degree_hint=0, community="core")

    from modules.world_model import read_state_dict

    world = read_state_dict(root / "world_model.json")
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
        hid = add_node(
            kind,
            ip,
            label=ip,
            os=str(host.get("os_hint", "") or "")[:80],
            state=str(host.get("state", "")),
            community=f"net:{ip}",
        )
        tag_source(hid, "world_model.json")
        add_edge(
            c2_id, hid, "owns" if ip in owned else "commands", evidence=f"world_model phase={world.get('phase', '')}"
        )
        services = host.get("services", {}) or {}
        items = services.items() if isinstance(services, dict) else []
        for port, svc in items:
            svc = svc if isinstance(svc, dict) else {"name": str(svc)}
            name = str(svc.get("name", "unknown"))
            svc_version = str(svc.get("version", "") or "")[:60]
            sid = add_node(
                "service",
                f"{ip}:{port}",
                label=f"{ip}:{port} {name}",
                port=str(port),
                service=name,
                version=svc_version,
                community=f"net:{ip}",
            )
            tag_source(sid, "world_model.json")
            add_edge(hid, sid, "serves", evidence=f"world_model services[{port}]={name}")
            for cve_row in _service_cve_matches(name, svc_version, svc):
                cid = add_node(
                    "cve",
                    cve_row["cve"],
                    label=cve_row["cve"],
                    cve=cve_row["cve"],
                    heat=cve_row.get("heat", "cold"),
                    cvss=cve_row.get("cvss", 0.0),
                    kev=cve_row.get("kev", False),
                    epss=cve_row.get("epss"),
                    exploit=cve_row.get("exploit", False),
                    heat_rank=cve_row.get("heat_rank", 0),
                    candidate=True,
                    in_range=cve_row.get("in_range"),
                    community=f"net:{ip}",
                )
                tag_source(cid, "lazy_cve_feed")
                add_edge(sid, cid, "matched", evidence=f"heat-correlated candidate on {name} {svc_version}")
    for vuln in world.get("vulnerabilities", []) or []:
        if not isinstance(vuln, dict):
            continue
        host_ip = str(vuln.get("host", "") or vuln.get("ip", "") or "")
        sev = str(vuln.get("severity", "info")).lower()
        fid = add_node(
            "finding-critical" if sev == "critical" else "finding",
            str(vuln.get("id", vuln.get("title", "")))[:120],
            label=str(vuln.get("title", "finding"))[:120],
            severity=sev,
            community=f"net:{host_ip}" if host_ip else "intel",
        )
        tag_source(fid, "world_model.json")
        if host_ip and node_id("host", host_ip) in nodes:
            add_edge(node_id("host", host_ip), fid, "has_finding", evidence="world_model vulnerabilities")
        elif host_ip and node_id("host-owned", host_ip) in nodes:
            add_edge(node_id("host-owned", host_ip), fid, "has_finding", evidence="world_model vulnerabilities")
        cve_id = _extract_cve_id(vuln)
        if cve_id:
            try:
                from modules.lazy_cve_feed import cve_intel as _cve_intel
                from modules.lazy_heat import HEAT_RANK

                intel = _cve_intel(cve_id, allow_network=False)
                cid = add_node(
                    "cve",
                    cve_id,
                    label=cve_id,
                    cve=cve_id,
                    heat=intel["heat"],
                    cvss=intel["cvss"],
                    kev=intel["kev"],
                    epss=intel["epss"],
                    exploit=intel["exploit"],
                    heat_rank=HEAT_RANK.get(intel["heat"], 0),
                    community=f"net:{host_ip}" if host_ip else "intel",
                )
                tag_source(cid, "lazy_cve_feed")
                if host_ip and (node_id("host", host_ip) in nodes or node_id("host-owned", host_ip) in nodes):
                    add_edge(
                        node_id("host", host_ip)
                        if node_id("host", host_ip) in nodes
                        else node_id("host-owned", host_ip),
                        cid,
                        "matched",
                        evidence="heat-correlated CVE",
                    )
            except Exception:
                pass

    lazy_dir = root / "lazy"
    tasks: dict = {}
    try:
        tasks = _load_json(lazy_dir / "tasks.json", {}).get("tasks", {}) or {}
    except Exception:
        tasks = {}
    for task_id, record in tasks.items():
        if not isinstance(record, dict):
            continue
        scoped = [str(s.get("value", "")) for s in record.get("scope", []) or [] if s.get("value")]
        task_community = f"net:{scoped[0]}" if scoped else "loop"
        tid = add_node(
            "task",
            task_id,
            label=f"{task_id}: {str(record.get('goal', ''))[:60]}",
            status=str(record.get("status", "")),
            goal=str(record.get("goal", ""))[:200],
            community=task_community,
        )
        tag_source(tid, "sessions/lazy/tasks.json")
        add_edge(c2_id, tid, "runs", evidence="lazy task registry")
        for scope in record.get("scope", []) or []:
            val = str(scope.get("value", ""))
            for kind in ("host", "host-owned"):
                if node_id(kind, val) in nodes:
                    add_edge(tid, node_id(kind, val), "targets", evidence=f"lazy scope {scope.get('kind')}:{val}")
        try:
            exp = _load_json(lazy_dir / f"exp_{task_id}.json", {})
            for node in exp.get("nodes", []) or []:
                if not isinstance(node, dict) or node.get("kind") != "finding":
                    continue
                meta = node.get("meta", {}) or {}
                sev = str(meta.get("severity", "info")).lower()
                fid = add_node(
                    "finding-critical" if sev == "critical" else "finding",
                    f"{task_id}#{node.get('node_id')}",
                    label=str(node.get("text", ""))[:120],
                    severity=sev,
                    status=str(meta.get("status", "")),
                    community=task_community,
                )
                tag_source(fid, f"sessions/lazy/exp_{task_id}.json")
                add_edge(tid, fid, "has_finding", evidence=f"lazy {task_id} finding #{node.get('node_id')}")
        except Exception:
            continue

    for row in _read_lines(root / "objectives.jsonl", 200):
        text = str(row.get("objective", "") or row.get("text", "") or "")[:160]
        if not text:
            continue
        oid = add_node("objective", text, label=text, status=str(row.get("status", "")), community="mission")
        tag_source(oid, "objectives.jsonl")
        add_edge(c2_id, oid, "targets", evidence="objectives queue")
        for ip in _host_mentions(text):
            for kind in ("host", "host-owned"):
                if node_id(kind, ip) in nodes:
                    add_edge(oid, node_id(kind, ip), "targets", evidence="objective mentions host")

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
            lid = add_node("host", ip, label=f"{ip} (log-only)", log_only=True, community=f"net:{ip}")
            nodes[lid]["log_hits"] = count
            tag_source(lid, "session logs")
            add_edge(
                c2_id, lid, "observed_in", evidence="mentioned in session logs", weight=min(3.0, 0.5 + count / 20.0)
            )

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
    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "stats": {
            "nodes": len(nodes),
            "edges": len(edges),
            "hosts": sum(1 for n in nodes.values() if n["kind"] in ("host", "host-owned")),
            "findings": sum(1 for n in nodes.values() if n["kind"].startswith("finding")),
            "communities": communities,
            "generated": time.time(),
        },
    }


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
    pairs = [(e["source"], e["target"]) for e in edges if e["source"] in nodes and e["target"] in nodes]
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
        language = str(node.get("os") or node.get("service") or node.get("severity") or node.get("status") or kind)
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
            nodes[hub_id] = {
                "id": hub_id,
                "kind": "community",
                "type": "community",
                "label": label,
                "value": label,
                "community": label,
                "community_label": label,
                "family": label,
                "language": "community",
                "layer": "unknown",
                "symbols": counts.get(label, 0),
                "degree": counts.get(label, 0),
                "findings": 0,
                "rank": 0.0,
                "rank_pos": 0,
                "doc": f"Community {label} · {counts.get(label, 0)} nodes",
                "symbol_list": [],
                "sources": [],
                "color": TYPE_COLORS["community"],
                "community_id": cid,
                "size": counts.get(label, 0),
                "familyColor": TYPE_COLORS["community"],
            }
        else:
            nodes[hub_id]["size"] = counts.get(label, 0)
    for node in list(nodes.values()):
        if node.get("type") != "file":
            continue
        cid = community_ids[str(node.get("community", "misc"))]
        hub_id = f"community:{cid}"
        node["community_id"] = cid
        edges.append(
            {
                "source": f"file:{node['id']}" if False else node["id"],
                "target": hub_id,
                "type": "member_of",
                "weight": 1,
                "color": EDGE_COLORS["member_of"],
                "evidence": "community",
            }
        )
        layer = str(node.get("layer", "unknown"))
        layer_id = f"layer:{layer}"
        if layer_id not in nodes:
            nodes[layer_id] = {
                "id": layer_id,
                "kind": "layer",
                "type": "layer",
                "label": layer,
                "value": layer,
                "community": "misc",
                "community_label": "",
                "family": layer,
                "language": "layer",
                "layer": layer,
                "symbols": 0,
                "degree": 0,
                "findings": 0,
                "rank": 0.0,
                "rank_pos": 0,
                "doc": f"Layer {layer}",
                "symbol_list": [],
                "sources": [],
                "color": TYPE_COLORS["layer"],
                "familyColor": TYPE_COLORS["layer"],
            }
        edges.append(
            {
                "source": node["id"],
                "target": layer_id,
                "type": "layered_as",
                "weight": 1,
                "color": EDGE_COLORS["layered_as"],
                "evidence": "layer",
            }
        )


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


BUNDLE_RELATIONS = (
    "commands",
    "owns",
    "serves",
    "has_finding",
    "targets",
    "runs",
    "observed_in",
    "controls",
    "discovered",
    "opens",
)

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


def _split_caps(
    labels: list[str],
    sizes: dict[str, int],
    points: list[int],
    lattice: list[tuple[float, float, float]],
    out: dict[str, list[int]],
) -> None:
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
    _split_caps(ordered_keys, {k: len(members[k]) for k in ordered_keys}, list(range(total)), lattice, regions)
    leaves: dict[str, tuple[float, float, float]] = {}
    hubs: dict[str, tuple[float, float, float]] = {}
    caps: dict[str, tuple[float, float, float]] = {}
    for key in ordered_keys:
        region = regions[key]
        center = _unit([sum(lattice[pi][k] for pi in region) for k in range(3)])
        caps[key] = center
        ordered_pts = sorted(region, key=lambda pi: (-sum(lattice[pi][k] * center[k] for k in range(3)), pi))
        for nid, pi in zip(members[key], ordered_pts, strict=True):
            leaves[nid] = lattice[pi]
        hubs[key] = (center[0] * BUNDLE_INNER_RATIO, center[1] * BUNDLE_INNER_RATIO, center[2] * BUNDLE_INNER_RATIO)
    group_index = {key: i for i, key in enumerate(ordered_keys)}
    fallback = TYPE_COLORS["file"]
    groups = []
    for key in ordered_keys:
        start, end = arcs[key]
        mid = (start + end) / 2
        ratio = BUNDLE_INNER_RATIO
        name = group_label[key]
        groups.append(
            {
                "k": key,
                "l": name,
                "c": fallback if key == BUNDLE_UNASSIGNED else _family_color(name),
                "n": len(members[key]),
                "a0": round(start, BUNDLE_COORD_DIGITS),
                "a1": round(end, BUNDLE_COORD_DIGITS),
                "h2": [
                    round(ratio * math.cos(mid), BUNDLE_COORD_DIGITS),
                    round(ratio * math.sin(mid), BUNDLE_COORD_DIGITS),
                ],
                "h3": [round(v, BUNDLE_COORD_DIGITS) for v in hubs[key]],
                "u": [round(v, BUNDLE_COORD_DIGITS) for v in caps[key]],
            }
        )
    index = {node["id"]: i for i, node in enumerate(files)}
    nodes = []
    for node in files:
        nid = node["id"]
        key = member_key[nid]
        nodes.append(
            {
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
            }
        )
    pairs = sorted(
        {
            (index[e["source"]], index[e["target"]])
            for e in graph.get("edges", [])
            if e.get("type") in BUNDLE_RELATIONS
            and e.get("source") in index
            and e.get("target") in index
            and e["source"] != e["target"]
        }
    )
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


def _score_lines(host_value: str, detail: list[dict]) -> tuple[float, list[dict]]:
    """Cap detail lines so their sum stays within the 100-point budget.

    Args:
        host_value: Host the lines belong to (for logging context only).
        detail: Ordered ``{"label", "points"}`` rows.

    Returns:
        ``(score, kept_lines)`` with the total bounded to ``SCORE_CAP_TOTAL``.
    """
    kept: list[dict] = []
    total = 0.0
    for line in detail:
        points = min(float(line.get("points", 0.0) or 0.0), SCORE_CAP_TOTAL - total)
        if points <= 0:
            continue
        kept.append({"label": str(line.get("label", ""))[:120], "points": round(points, 2)})
        total += points
        if total >= SCORE_CAP_TOTAL:
            break
    return round(min(total, SCORE_CAP_TOTAL), 2), kept


# -----------------------------------------------------------------------------
# Snapshot svg (docs/SCRIPTORIUM: static report rendering for /report)
# -----------------------------------------------------------------------------

SVG_NODE_CAP = 90
SVG_WIDTH = 1000
SVG_HEIGHT = 600
SVG_INNER_RADIUS = 160
SVG_OUTER_RADIUS = 260
SVG_LABEL_CHARS = 24
SVG_INNER_RING_MAX = 36
_SVG_CVE_RING = {"hot": "#ff1744", "warm": "#ffb300"}
_SVG_EDGE_DEFAULT = "rgba(148,163,184,.35)"


def _svg_text(value: object) -> str:
    """Escape untrusted text for an XML text node."""
    from xml.sax.saxutils import escape

    return escape(str(value or ""), {"'": "&apos;", '"': "&quot;"})


def _svg_attr(value: object) -> str:
    """Escape untrusted text for a double-quoted XML attribute."""
    return _svg_text(value).replace('"', "&quot;").replace("&#x27;", "&apos;")


def _svg_rank(node: dict) -> tuple:
    """Deterministic selection key: c2 hub first, then heat, degree, id."""
    kind = str(node.get("kind", ""))
    return (
        0 if kind == "c2" else 1,
        -int(node.get("heat_rank", 0) or 0),
        -float(node.get("degree", 0) or 0),
        str(node.get("id", "")),
    )


def svg_selection(graph: dict, cap_nodes: int = SVG_NODE_CAP) -> list[str]:
    """Return the node ids a bounded snapshot keeps, most important first.

    The lightest intel snapshot for static rendering: the c2 hub, then the
    hottest CVE matches, then the most connected nodes. Args: ``graph``
    intel payload, ``cap_nodes`` maximum selected ids.

    Returns:
        Selected node ids in placement order.
    """
    nodes = [n for n in (graph.get("nodes", []) or []) if isinstance(n, dict) and n.get("id")]
    cap = max(0, min(int(cap_nodes), len(nodes) or 0)) if cap_nodes >= 0 else 0
    if cap <= 0:
        return []
    ranked = sorted(nodes, key=_svg_rank)
    return [str(n["id"]) for n in ranked[:cap]]


def _svg_place(ids: list[str]) -> dict[str, tuple[float, float]]:
    """Assign deterministic coordinates: the c2 hub centred, the rest on rings."""
    positions: dict[str, tuple[float, float]] = {}
    cx, cy = SVG_WIDTH / 2, SVG_HEIGHT / 2
    rest = [nid for nid in ids if nid != "c2"]
    if "c2" in ids:
        positions["c2"] = (cx, cy)
    inner = rest[: SVG_INNER_RING_MAX]
    outer = rest[SVG_INNER_RING_MAX:]
    for group, radius in ((inner, SVG_INNER_RADIUS), (outer, SVG_OUTER_RADIUS)):
        count = len(group)
        for index, nid in enumerate(group):
            angle = 2.0 * math.pi * index / count if count else 0.0
            positions[nid] = (round(cx + radius * math.cos(angle), 1), round(cy + radius * math.sin(angle), 1))
    return positions


def _svg_host_of(node: dict) -> str:
    """Host value a node belongs to, via its community tag."""
    return str(node.get("community", "")).removeprefix("net:")


def relations_svg(graph: dict, cap_nodes: int = SVG_NODE_CAP) -> str:
    """Render a static svg snapshot of the intel graph for documents.

    Pure, bounded and XML-escaped: circles per selected node (fill by
    kind, ring by heat on CVE nodes), lines only between rendered nodes
    and a legend row. Scan-derived values never reach the markup raw, so
    the output is safe to embed with ``| safe``.

    Args:
        graph: Intel graph payload from :func:`build_intel_graph`.
        cap_nodes: Maximum rendered nodes.

    Returns:
        SVG markup, or "" when the graph has no renderable nodes.
    """
    nodes = [n for n in (graph.get("nodes", []) or []) if isinstance(n, dict) and n.get("id")]
    if not nodes:
        return ""
    selection = svg_selection(graph, cap_nodes)
    if not selection:
        return ""
    positions = _svg_place(selection)
    selected = {n["id"]: n for n in nodes if str(n["id"]) in positions}
    lines: list[str] = []
    for edge in graph.get("edges", []) or []:
        if not isinstance(edge, dict):
            continue
        src, dst = str(edge.get("source", "")), str(edge.get("target", ""))
        if src not in positions or dst not in positions:
            continue
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
        style = EDGE_COLORS.get(str(edge.get("type", "")), _SVG_EDGE_DEFAULT)
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{_svg_attr(style)}" stroke-width="1"/>'
        )
    dots: list[str] = []
    for nid, node in selected.items():
        cx, cy = positions[nid]
        kind = str(node.get("kind", ""))
        fill = _svg_attr(NODE_COLORS.get(kind, "#e0e0e0"))
        radius = 10 if kind == "c2" else 8
        ring = ""
        if kind == "cve":
            ring_color = _SVG_CVE_RING.get(str(node.get("heat", "")), "")
            if ring_color:
                ring = f' stroke="{_svg_attr(ring_color)}" stroke-width="2.5"'
        label = _svg_text(str(node.get("value", ""))[:SVG_LABEL_CHARS])
        host = _svg_host_of(node)
        title = _svg_text(f"{kind} {node.get('value', '')}" + (f" @ {host}" if host else ""))
        dots.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}"{ring} data-node-kind="{_svg_attr(kind)}">'
            f"<title>{title}</title></circle>"
        )
        dots.append(
            f'<text x="{cx}" y="{round(cy + radius + 12, 1)}" text-anchor="middle" font-size="9" fill="#cbd5e1">'
            f"{label}</text>"
        )
    kind_counts: dict[str, int] = {}
    for node in selected.values():
        kind = str(node.get("kind", ""))
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
    legend = "  ".join(f"{_svg_text(kind)}:{total}" for kind, total in sorted(kind_counts.items()))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" '
        f'width="{SVG_WIDTH}" height="{SVG_HEIGHT}" role="img" aria-label="campaign relation snapshot">'
        '<rect width="100%" height="100%" fill="#0f172a"/>'
        f"<text x=\"12\" y=\"20\" font-size=\"11\" fill=\"#e2e8f0\">relations snapshot ({legend})</text>"
        + "".join(lines)
        + "".join(dots)
        + "</svg>"
    )


def _recency_lines(sessions_dir: str | Path, host_value: str) -> list[dict]:
    """Recency points from the world change log (one line max)."""
    try:
        from modules.lazy_world_diff import recent_changes

        rows = recent_changes(sessions_dir, days=7, host=host_value)
    except Exception:
        return []
    if not rows:
        return []
    kinds = {str(row.get("kind", "")) for row in rows[:10]}
    if kinds & set(LIFECYCLE_KINDS):
        return [{"label": "host appeared or returned this week", "points": RECENCY_NEW}]
    if kinds & set(EXPOSURE_KINDS):
        return [{"label": "recent exposure change", "points": RECENCY_EXPOSURE}]
    return []


def _ghost_lines(sessions_dir: str | Path, host_value: str) -> list[dict]:
    """Ghost points for a host still answering without a name."""
    try:
        from modules.lazy_world_diff import load_ghosts

        record = (load_ghosts(sessions_dir).get("hosts", {}) or {}).get(host_value) or {}
    except Exception:
        return []
    if record.get("state") != "ghost":
        return []
    answers = ", ".join(str(a) for a in (record.get("answers", []) or [])[:3])
    label = "ghost host: name gone but it still answers"
    if answers:
        label += f" ({answers})"
    return [{"label": label, "points": GHOST_CAP}]


def write_summary(graph: dict, sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Score host exposure with a normalized, per-component breakdown.

    The score is bounded 0..100 with capped components, and every point
    carries a label so the planner and the operator can read why one
    host outranks another:

    - heat: hottest CVE candidate matched on the host (hot 40, warm 20,
      cold 5), capped at 50;
    - findings: severity-weighted findings attached to the host
      (critical/high 25, medium 10, low 3), capped at 25;
    - controlled: the C2 owns the host (10);
    - connectivity: capped node degree (10);
    - activity: recent log mentions (5);
    - recency: the host changed this week in the world change log (10);
    - ghost: the host answers on its last address without resolving (15).

    Args:
        graph: Intel graph from :func:`build_intel_graph`.
        sessions_dir: Sessions directory for ``intel_summary.json``.

    Returns:
        Summary dict; ``top_exposed`` rows gain ``score_detail``.
    """
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    node_by_id = {n["id"]: n for n in nodes}
    host_ids = {n["id"] for n in nodes if n.get("kind") in ("host", "host-owned") and not n.get("log_only")}
    details: dict[str, list[dict]] = {node_by_id[hid].get("value", ""): [] for hid in host_ids}
    heat_by_host: dict[str, float] = {}
    finding_points: dict[str, float] = {}
    with_services: set[str] = set()
    with_findings: set[str] = set()
    confirmed_finding_ids = set()
    for node in nodes:
        if str(node.get("kind", "")).startswith("finding") and node.get("confirmation", "pending") == "confirmed":
            confirmed_finding_ids.add(node["id"])
    for edge in edges:
        src = node_by_id.get(edge.get("source"))
        dst = node_by_id.get(edge.get("target"))
        if src is None or dst is None:
            continue
        edge_kind = edge.get("type")
        if edge_kind in ("serves", "opens", "runs"):
            with_services.add(edge.get("source", ""))
        if edge_kind == "has_finding":
            with_findings.add(edge.get("source", ""))
            if edge.get("target") in confirmed_finding_ids:
                pass
        if edge_kind == "matched" and str(dst.get("kind", "")) == "cve":
            ip = str(dst.get("community", "")).removeprefix("net:")
            if ip in details:
                heat_by_host[ip] = max(heat_by_host.get(ip, 0.0), HEAT_POINTS.get(str(dst.get("heat", "cold")), 0.0))
        if edge_kind == "has_finding" and str(dst.get("kind", "")).startswith("finding"):
            ip = str(src.get("value", ""))
            if ip in details:
                severity = str(dst.get("severity", "info")).lower()
                weight = FINDING_POINTS.get(severity, min(5.0, (4 - SEV_RANK.get(severity, 4)) * 2.0))
                heat = str(dst.get("heat", "") or "")
                if heat == "hot":
                    weight += 3.0
                elif heat == "warm":
                    weight += 1.0
                finding_points[ip] = min(FINDINGS_CAP, finding_points.get(ip, 0.0) + weight)
    for value, points in heat_by_host.items():
        cves = [
            n for n in nodes if n.get("kind") == "cve" and str(n.get("community", "")).removeprefix("net:") == value
        ]
        hottest = max(cves, key=lambda n: int(n.get("heat_rank", 0) or 0), default=None)
        label = "CVE heat " + str(hottest.get("value", "")) if hottest else "CVE heat"
        details[value].append({"label": label, "points": min(points, HEAT_CAP)})
    for value, points in finding_points.items():
        if points:
            details[value].append({"label": "findings and CVE heat", "points": round(points, 2)})
    for node in nodes:
        if node["id"] not in host_ids:
            continue
        value = node.get("value", "")
        degree = min(float(node.get("degree", 0) or 0), CONNECTIVITY_CAP)
        lines = details.setdefault(value, [])
        lines.append({"label": f"connectivity (degree {int(node.get('degree', 0) or 0)})", "points": round(degree, 2)})
        if node.get("kind") == "host-owned":
            lines.append({"label": "controlled by C2", "points": OWNED_POINTS})
        activity = min(ACTIVITY_CAP, float(node.get("log_hits", 0) or 0) / 10.0)
        if activity:
            lines.append({"label": "log activity", "points": round(activity, 2)})
        lines.extend(_recency_lines(sessions_dir, value))
        lines.extend(_ghost_lines(sessions_dir, value))
    scores: dict[str, float] = {}
    kept_details: dict[str, list[dict]] = {}
    for value, lines in details.items():
        if not value:
            continue
        score, kept = _score_lines(value, lines)
        if score > 0 or kept:
            scores[value] = score
            kept_details[value] = kept
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    hosts = [n for n in nodes if n.get("kind") in ("host", "host-owned")]
    confirmed_hosts = set()
    for edge in edges:
        if edge.get("type") == "has_finding" and edge.get("target") in confirmed_finding_ids:
            confirmed_hosts.add(edge.get("source"))
    host_id_values = {n["id"]: n.get("value") for n in hosts}
    owned = sorted(n.get("value", "") for n in hosts if n.get("kind") == "host-owned" or n.get("owned"))
    owned_confirmed = sorted(v for v in owned if v in {host_id_values.get(hid) for hid in confirmed_hosts})
    funnel = [
        {"stage": "discovered", "hosts": len(hosts)},
        {"stage": "with services", "hosts": len([v for v in with_services if v in host_id_values.values()])},
        {"stage": "with findings", "hosts": len([v for v in with_findings if v in host_id_values.values()])},
        {"stage": "confirmed", "hosts": len([v for v in owned_confirmed])},
        {"stage": "owned", "hosts": len(owned_confirmed)},
    ]
    source_yield: dict[str, int] = {}
    for node in nodes:
        if not str(node.get("kind", "")).startswith("finding"):
            continue
        for src in node.get("sources", []) or []:
            source_yield[str(src)] = source_yield.get(str(src), 0) + 1
    heat_counts = {"hot": 0, "warm": 0, "cold": 0}
    for node in nodes:
        heat = str(node.get("heat", ""))
        if node.get("kind") == "cve" and heat in heat_counts:
            heat_counts[heat] += 1
    recent_rows: list[dict] = []
    ghost_hosts: list[str] = []
    try:
        from modules.lazy_world_diff import recent_changes as _recent_changes

        recent_rows = _recent_changes(sessions_dir, days=7)[:10]
    except Exception:
        recent_rows = []
    try:
        from modules.lazy_world_diff import load_ghosts as _load_ghosts

        ghost_hosts = sorted(
            host
            for host, record in (_load_ghosts(sessions_dir).get("hosts", {}) or {}).items()
            if record.get("state") == "ghost"
        )
    except Exception:
        ghost_hosts = []
    summary = {
        "generated": time.time(),
        "hosts_scored": len(ranked),
        "top_exposed": [
            {"host": host, "score": score, "score_detail": kept_details.get(host, [])} for host, score in ranked[:10]
        ],
        "suggested_intents": [f"probe {host} (intel exposure {score})" for host, score in ranked[:5]],
        "funnel": funnel,
        "heat_counts": heat_counts,
        "recent_changes": recent_rows,
        "ghost_hosts": ghost_hosts,
        "confirmed_hosts": sorted(n.get("value") for n in hosts if n["id"] in confirmed_hosts),
        "owned_hosts": owned,
        "source_yield": dict(sorted(source_yield.items(), key=lambda kv: -kv[1])),
        "stats": graph.get("stats", {}),
    }
    try:
        dest = Path(str(sessions_dir)) / "intel_summary.json"
        dest.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    except OSError:
        pass
    return summary


__all__ = [
    "build_intel_graph",
    "assign_layout",
    "write_summary",
    "node_id",
    "NODE_COLORS",
    "EDGE_COLORS",
    "page_settings",
    "group_colors",
    "build_analytics",
    "build_bundle_payload",
    "bundle_settings",
    "svg_selection",
    "relations_svg",
]
