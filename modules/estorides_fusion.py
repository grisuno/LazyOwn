"""Estorides intel fusion: merge OSINT graph entities into campaign graphs.

Reads an estorides export (``estorides_lazyown.json`` preferred, raw
``estorides_graph.json`` accepted) and merges it into the intel and
attack-surface graphs. When an IP or value already exists as a node, the
two records fuse: sources union plus ``estorides``, attributes merge,
edges re-anchor. New entities arrive tagged and capped so the graphs
stay readable.

Provenance stays explicit: every fused node carries ``estorides`` in its
sources and estorides edges keep their ``estorides:`` evidence prefix.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

LAZYOWN_EXPORT = "estorides_lazyown.json"
RAW_EXPORT = "estorides_graph.json"
LAN_LAZYOWN_EXPORTS = ("lan_lazyown.json", "lan_graph.json")
LAN_INVENTORY_EXPORTS = ("lan_inventory.json",)
LAN_STIX_EXPORTS = ("lan_stix.json",)
MAX_NEW_NODES = 300
MAX_LAN_NODES = 500

SKIP_ETYPES = frozenset({"source"})

RAW_TYPE_MAP = {
    "ipv4": "host", "ipv6": "host",
    "domain": "domain",
    "cve": "finding", "ghsa": "finding",
    "url": "url", "email": "email", "asn": "asn", "mac": "mac",
}

KNOWN_EDGE_TYPES = frozenset({
    "commands", "owns", "serves", "has_finding", "targets", "runs",
    "observed_in", "controls", "discovered", "opens",
    "member_of", "layered_as",
})


def estorides_checkout() -> Path | None:
    """Locate the estorides working copy.

    Resolution order, no hardcoded user paths: the ESTORIDES_DIR
    environment override first, then the lazyaddon install directory.
    """
    override = os.environ.get("ESTORIDES_DIR", "").strip()
    candidates = []
    if override:
        candidates.append(Path(override))
    candidates.append(BASE_DIR / "external" / ".exploit" / "estorides")
    for candidate in candidates:
        try:
            if (candidate / "estorides_cli.py").is_file():
                return candidate
        except OSError:
            continue
    return None


def find_export(sessions_dir: str | Path = SESSIONS_DIR) -> Path | None:
    """Find an estorides export, preferring the LazyOwn vocabulary file."""
    root = Path(str(sessions_dir))
    for name in (LAZYOWN_EXPORT, RAW_EXPORT):
        candidate = root / name
        if candidate.is_file():
            return candidate
    checkout = estorides_checkout()
    if checkout is not None:
        for name in (LAZYOWN_EXPORT, RAW_EXPORT):
            candidate = checkout / name
            if candidate.is_file():
                return candidate
    return None


def run_export(sessions_dir: str | Path = SESSIONS_DIR,
               cli_path: str | None = None,
               timeout_sec: float = 300.0) -> Path | None:
    """Run ``estorides_cli.py graph --export lazyown`` into sessions/.

    Never raises: failures return None and the caller keeps working with
    whatever export already exists.
    """
    checkout: Path | None = None
    if cli_path:
        candidate = Path(str(cli_path))
        if candidate.is_file() and candidate.name == "estorides_cli.py":
            checkout = candidate.parent
        elif (candidate / "estorides_cli.py").is_file():
            checkout = candidate
    if checkout is None:
        checkout = estorides_checkout()
    if checkout is None:
        return None
    dest = Path(str(sessions_dir)) / LAZYOWN_EXPORT
    try:
        subprocess.run(
            ["python3", "estorides_cli.py", "graph", "--export", "lazyown"],
            cwd=str(checkout), capture_output=True, text=True,
            timeout=timeout_sec, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    produced = checkout / LAZYOWN_EXPORT
    if produced.is_file():
        try:
            data = produced.read_bytes()
            dest.write_bytes(data)
            return dest
        except OSError:
            return produced
    return None


def _norm(value: object) -> str:
    """Normalize a fusion key (case/whitespace-insensitive)."""
    return str(value or "").strip().lower()


def load_export(path: str | Path) -> dict:
    """Load an export in either vocabulary into nodes/edges lists."""
    try:
        document = json.loads(Path(str(path)).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"nodes": [], "edges": []}
    if not isinstance(document, dict):
        return {"nodes": [], "edges": []}
    first = (document.get("nodes", []) or [{}])[0]
    if isinstance(first, dict) and "etype" in first and "kind" in first:
        return {"nodes": document.get("nodes", []), "edges": document.get("edges", [])}
    return _from_raw(document)


def _from_raw(document: dict) -> dict:
    """Translate a raw estorides export_json document to LazyOwn vocabulary."""
    nodes = []
    id_map: dict[str, tuple[str, str]] = {}
    for node in document.get("nodes", []) or []:
        if not isinstance(node, dict):
            continue
        etype = str(node.get("type", "unknown"))
        if etype in SKIP_ETYPES:
            continue
        value = str(node.get("value", node.get("id", "")))
        if not value:
            continue
        kind = RAW_TYPE_MAP.get(etype, "intel")
        nid = str(node.get("id", f"{etype}:{value}"))
        id_map[nid] = (kind, value)
        sources = node.get("sources", []) or []
        nodes.append({"kind": kind, "etype": etype, "value": value,
                      "label": value,
                      "sources": [str(s) for s in sources if s],
                      "attrs": {k: v for k, v in node.items()
                                if isinstance(v, (str, int, float, bool))}})
    edges = []
    for edge in document.get("edges", []) or []:
        if not isinstance(edge, dict):
            continue
        src = id_map.get(str(edge.get("source", "")))
        dst = id_map.get(str(edge.get("target", "")))
        if not src or not dst:
            continue
        relation = str(edge.get("relation", edge.get("type", "related")))
        edges.append({"source_kind": src[0], "source_value": src[1],
                      "target_kind": dst[0], "target_value": dst[1],
                      "type": relation if relation in KNOWN_EDGE_TYPES else "observed_in",
                      "evidence": f"estorides:{edge.get('relation', 'related')}"[:200]})
    return {"nodes": nodes, "edges": edges}


def community_for(kind: str, value: str) -> str:
    """Assign a campaign community to a fused entity."""
    if kind == "host" and value and "." in value:
        return f"net:{value}"
    return "intel"


def merge_estorides(nodes: dict[str, dict], edges: list[dict],
                    est: dict, cap: int = MAX_NEW_NODES) -> dict:
    """Fuse estorides entities into graph nodes/edges in place.

    Matching (kind, value) fuses records; new entities arrive with
    ``estorides`` provenance until ``cap``. Returns merge statistics.
    """
    stats = {"est_nodes": 0, "fused": 0, "added": 0, "edges": 0, "skipped": 0}
    key_to_id: dict[tuple[str, str], str] = {}
    for nid, node in nodes.items():
        if node.get("type") not in (None, "file"):
            continue
        key_to_id[(str(node.get("kind", "")), _norm(node.get("value")))] = nid
    est_nodes = [n for n in est.get("nodes", []) if isinstance(n, dict)]
    stats["est_nodes"] = len(est_nodes)
    est_id: dict[int, str] = {}
    for raw in est_nodes:
        kind = str(raw.get("kind", "intel"))
        value = str(raw.get("value", ""))
        if not value:
            stats["skipped"] += 1
            continue
        key = (kind, _norm(value))
        if key in key_to_id:
            nid = key_to_id[key]
            node = nodes[nid]
            for src in list(raw.get("sources", [])) + ["estorides"]:
                if src and src not in node.setdefault("sources", []):
                    node["sources"].append(src)
            attrs = raw.get("attrs", {}) or {}
            for field in ("os", "service", "version", "severity", "confidence"):
                if attrs.get(field) and not node.get(field):
                    node[field] = attrs[field]
            stats["fused"] += 1
            est_id[id(raw)] = nid
        elif stats["added"] < cap:
            nid = f"est:{kind}:{_norm(value)}"
            if nid in nodes:
                est_id[id(raw)] = nid
                continue
            community = community_for(kind, value)
            nodes[nid] = {"id": nid, "kind": kind, "value": value,
                          "label": str(raw.get("label", value)),
                          "meta": {}, "color": "#e0e0e0",
                          "familyColor": "#e0e0e0",
                          "community": community,
                          "sources": ["estorides"] + [s for s in raw.get("sources", [])
                                                     if s != "estorides"][:4]}
            attrs = raw.get("attrs", {}) or {}
            for field in ("os", "service", "version", "severity", "confidence"):
                if attrs.get(field):
                    nodes[nid][field] = attrs[field]
            key_to_id[key] = nid
            est_id[id(raw)] = nid
            stats["added"] += 1
        else:
            stats["skipped"] += 1
    for edge in est.get("edges", []) or []:
        if not isinstance(edge, dict):
            continue
        src = key_to_id.get((str(edge.get("source_kind", "intel")),
                             _norm(edge.get("source_value"))))
        dst = key_to_id.get((str(edge.get("target_kind", "intel")),
                             _norm(edge.get("target_value"))))
        if not src or not dst or src == dst:
            continue
        etype = str(edge.get("type", "observed_in"))
        if etype not in KNOWN_EDGE_TYPES:
            etype = "observed_in"
        if any(e["source"] == src and e["target"] == dst and e["type"] == etype
               for e in edges):
            continue
        color = {"member_of": "rgba(167,139,250,.22)",
                 "layered_as": "rgba(52,211,153,.16)"}.get(etype, "#808080")
        edges.append({"source": src, "target": dst, "type": etype,
                      "evidence": str(edge.get("evidence", "estorides"))[:200],
                      "color": color, "weight": 1.0})
        stats["edges"] += 1
    return stats


def find_lan_bundle(sessions_dir: str | Path = SESSIONS_DIR) -> Path | None:
    """Find a LAN bundle deliverable, preferring LazyOwn vocabulary."""
    roots: list[Path] = [Path(str(sessions_dir))]
    checkout = estorides_checkout()
    if checkout is not None:
        roots.append(checkout / "data" / "lan_output")
    for root in roots:
        if not root.is_dir():
            continue
        for name in LAN_LAZYOWN_EXPORTS + LAN_INVENTORY_EXPORTS:
            candidate = root / name
            if candidate.is_file():
                return candidate
        for name in LAN_LAZYOWN_EXPORTS + LAN_INVENTORY_EXPORTS:
            for suffixed in sorted(root.glob(f"lan_*{name[3:]}")):
                if suffixed.is_file():
                    return suffixed
    return None


def load_lan_bundle(path: str | Path) -> dict:
    """Load a LAN bundle file into nodes/edges lists. Never raises."""
    try:
        document = json.loads(Path(str(path)).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"nodes": [], "edges": []}
    if not isinstance(document, dict):
        return {"nodes": [], "edges": []}
    if isinstance(document.get("devices"), list):
        nodes: list[dict] = []
        edges: list[dict] = []
        for dev in document["devices"]:
            if not isinstance(dev, dict):
                continue
            sources = [str(s) for s in (dev.get("sources") or []) if s] or ["lan"]
            for ip in dev.get("ips", []) or []:
                nodes.append({"kind": "host",
                              "etype": "ipv6" if ":" in str(ip) else "ipv4",
                              "value": str(ip), "label": str(ip),
                              "sources": sources,
                              "attrs": {"device_id": str(dev.get("device_id", ""))}})
            if dev.get("mac"):
                nodes.append({"kind": "mac", "etype": "mac",
                              "value": str(dev["mac"]), "label": str(dev["mac"]),
                              "sources": sources,
                              "attrs": {"device_id": str(dev.get("device_id", ""))}})
            for host in dev.get("hostnames", []) or []:
                nodes.append({"kind": "domain", "etype": "domain",
                              "value": str(host), "label": str(host),
                              "sources": sources,
                              "attrs": {"device_id": str(dev.get("device_id", ""))}})
        return {"nodes": nodes, "edges": edges}
    return load_export(path)


def split_lan_targets(est: dict) -> tuple[dict, dict]:
    """Split a LAN payload into intel (all) and attack (hosts) views.

    The intel graph keeps everything known. The attack graph keeps only
    host nodes plus host-anchored edges so auto_loop queues actionable
    targets without MAC/hostname noise.
    """
    nodes = [n for n in est.get("nodes", []) if isinstance(n, dict)]
    edges = [e for e in est.get("edges", []) if isinstance(e, dict)]
    attack_nodes = [n for n in nodes if n.get("kind") == "host"]
    host_values = {str(n.get("value", "")).strip().lower() for n in attack_nodes}
    attack_edges = [e for e in edges
                    if str(e.get("source_value", "")).strip().lower() in host_values
                    or str(e.get("target_value", "")).strip().lower() in host_values]
    attack = {"nodes": attack_nodes, "edges": attack_edges}
    return ({"nodes": nodes, "edges": edges}, attack)


__all__ = [
    "LAN_INVENTORY_EXPORTS",
    "LAN_LAZYOWN_EXPORTS",
    "LAN_STIX_EXPORTS",
    "LAZYOWN_EXPORT",
    "MAX_LAN_NODES",
    "MAX_NEW_NODES",
    "community_for",
    "estorides_checkout",
    "find_export",
    "find_lan_bundle",
    "load_export",
    "load_lan_bundle",
    "merge_estorides",
    "run_export",
    "split_lan_targets",
]
