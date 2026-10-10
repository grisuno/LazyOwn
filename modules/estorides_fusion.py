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
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

LAZYOWN_EXPORT = "estorides_lazyown.json"
RAW_EXPORT = "estorides_graph.json"
MAX_NEW_NODES = 300

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
    """Locate the estorides working copy (addon install or dev path)."""
    candidates = [
        BASE_DIR / "external" / ".exploit" / "estorides",
        Path.home() / "src_note" / "py" / "fucklantir" / "estorides" / "estorides",
    ]
    for candidate in candidates:
        if (candidate / "estorides_cli.py").is_file():
            return candidate
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


__all__ = [
    "LAZYOWN_EXPORT",
    "MAX_NEW_NODES",
    "community_for",
    "estorides_checkout",
    "find_export",
    "load_export",
    "merge_estorides",
    "run_export",
]
