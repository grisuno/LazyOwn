"""Graph-aware neighbour lookups for the operator command palette.

The graphify export at :file:`graphify-out/graph_lazyown.json` captures the
call graph of every ``do_*`` command together with its helper functions and
classes. This module reads that artefact once per process and exposes a tiny
read-only API so the palette CLI, the C2 web view and the MCP tool can all
attach the same "what does this command actually do" / "what other commands
work like this one" hints to a detail view.

Design constraints driving the shape of this module:

- Single Responsibility — :class:`GraphIndex` only loads and caches; pure
  functions like :func:`callees`, :func:`related_commands` and
  :func:`enrich_detail` translate it into palette-friendly shapes.
- Open/Closed — every threshold, edge label and limit lives on
  :class:`GraphLookupConfig`; new neighbour types mean adding a function, not
  editing existing call sites.
- Dependency Inversion — every public entry point accepts the parsed graph
  document, never reads it from disk on its own. Callers wire the loader
  through :func:`load_graph` so tests can inject fixtures.
- Sad path is a no-op. A missing or malformed graph file degrades to empty
  results so the palette stays usable on hosts that never ran graphify.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GRAPH_PATH = REPO_ROOT / "graphify-out" / "graph_lazyown.json"


class GraphIndexError(RuntimeError):
    """Raised when the graphify export is missing or malformed."""


@dataclass(frozen=True)
class GraphLookupConfig:
    """Centralised constants for graph-driven palette enrichment.

    Every literal that affects neighbour selection lives here so behaviour is
    tunable without touching call sites. ``frozen=True`` prevents accidental
    mutation by per-surface consumers.
    """

    do_command_prefix: str = "do_"
    callable_label_suffix: str = "()"
    file_label_suffix: str = ".py"
    callee_relations: tuple[str, ...] = ("calls", "uses")
    excluded_callee_labels: frozenset[str] = frozenset({".cmd()", "run()", "decode()"})
    callee_limit: int = 12
    related_limit: int = 6
    related_min_shared_helpers: int = 2
    accept_inferred_edges: bool = True


def _looks_like_command_label(label: str, *, prefix: str, suffix: str) -> bool:
    """Return ``True`` for graph labels that name a ``do_*`` command."""
    return label.startswith(prefix) and label.endswith(suffix)


def _command_name_from_label(label: str, *, suffix: str) -> str:
    """Strip the trailing ``()`` from a callable graph label."""
    return label[: -len(suffix)] if suffix and label.endswith(suffix) else label


@dataclass(frozen=True)
class GraphIndex:
    """Read-only adjacency view derived from the graphify document.

    Attributes:
        adjacency: ``{node_id: [(other_id, relation, confidence), ...]}``
            — symmetric, deduplicated edge list.
        node_labels: ``{node_id: label}`` for every node in the graph.
        command_to_node: ``{do_name_without_parens: node_id}`` resolver for
            command lookups.
    """

    adjacency: Mapping[str, tuple[tuple[str, str, str], ...]]
    node_labels: Mapping[str, str]
    command_to_node: Mapping[str, str]


def _build_adjacency(
    document: Mapping[str, Any],
    *,
    config: GraphLookupConfig,
) -> GraphIndex:
    """Translate a graphify JSON document into :class:`GraphIndex`."""
    nodes = document.get("nodes") or []
    edges = document.get("links") or document.get("edges") or []
    node_labels: dict[str, str] = {}
    command_to_node: dict[str, str] = {}
    for node in nodes:
        nid = node.get("id")
        label = node.get("label")
        if not isinstance(nid, str) or not isinstance(label, str):
            continue
        node_labels[nid] = label
        if _looks_like_command_label(
            label,
            prefix=config.do_command_prefix,
            suffix=config.callable_label_suffix,
        ):
            command_to_node[_command_name_from_label(label, suffix=config.callable_label_suffix)] = nid
    raw: dict[str, set[tuple[str, str, str]]] = defaultdict(set)
    for edge in edges:
        source = edge.get("source") or edge.get("_src")
        target = edge.get("target") or edge.get("_tgt")
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        relation = str(edge.get("relation") or "")
        confidence = str(edge.get("confidence") or "")
        raw[source].add((target, relation, confidence))
        raw[target].add((source, relation, confidence))
    adjacency = {node_id: tuple(sorted(neighbours)) for node_id, neighbours in raw.items()}
    return GraphIndex(adjacency=adjacency, node_labels=node_labels, command_to_node=command_to_node)


@lru_cache(maxsize=4)
def load_graph(path: str | None = None) -> GraphIndex:
    """Return the parsed graph index, cached per resolved path.

    Args:
        path: Override the default graph location. ``None`` uses
            :data:`DEFAULT_GRAPH_PATH`.

    Returns:
        A :class:`GraphIndex`. When the file is missing or invalid the
        function raises :class:`GraphIndexError`; callers that want graceful
        degradation should use :func:`safe_load_graph` instead.
    """
    target = Path(path) if path is not None else DEFAULT_GRAPH_PATH
    if not target.exists():
        raise GraphIndexError(f"Graph artefact not found at {target}. Run 'graphify' to regenerate it.")
    try:
        document = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GraphIndexError(f"Invalid JSON in {target}: {exc}") from exc
    return _build_adjacency(document, config=GraphLookupConfig())


def safe_load_graph(path: str | None = None) -> GraphIndex | None:
    """Best-effort variant of :func:`load_graph`.

    Returns ``None`` instead of raising so the palette stays usable on hosts
    that have never run graphify.
    """
    try:
        return load_graph(path)
    except GraphIndexError:
        return None


def _filter_neighbours(
    neighbours: Iterable[tuple[str, str, str]],
    *,
    config: GraphLookupConfig,
    accept_relations: Iterable[str],
) -> list[tuple[str, str, str]]:
    """Filter raw neighbour tuples by relation and confidence policy."""
    accepted = set(accept_relations)
    out: list[tuple[str, str, str]] = []
    for neighbour, relation, confidence in neighbours:
        if relation not in accepted:
            continue
        if confidence == "INFERRED" and not config.accept_inferred_edges:
            continue
        out.append((neighbour, relation, confidence))
    return out


def callees(
    graph: GraphIndex | None,
    command_name: str,
    *,
    config: GraphLookupConfig | None = None,
) -> list[str]:
    """Return helper-function labels invoked by ``command_name``.

    Args:
        graph: The loaded graph index (or ``None``; in which case the result
            is an empty list).
        command_name: A ``do_*`` command name with or without the ``do_``
            prefix.
        config: Optional override for the lookup config.

    Returns:
        At most :attr:`GraphLookupConfig.callee_limit` distinct labels,
        sorted alphabetically. Internal noise such as ``.cmd()`` is excluded.
    """
    cfg = config or GraphLookupConfig()
    if graph is None:
        return []
    name = command_name if command_name.startswith(cfg.do_command_prefix) else f"{cfg.do_command_prefix}{command_name}"
    node_id = graph.command_to_node.get(name)
    if node_id is None:
        return []
    neighbours = _filter_neighbours(
        graph.adjacency.get(node_id, ()),
        config=cfg,
        accept_relations=cfg.callee_relations,
    )
    seen: set[str] = set()
    out: list[str] = []
    for neighbour_id, _relation, _confidence in neighbours:
        label = graph.node_labels.get(neighbour_id, "")
        if not label or label in cfg.excluded_callee_labels:
            continue
        if label.endswith(cfg.file_label_suffix):
            continue
        if label in seen:
            continue
        seen.add(label)
        out.append(label)
    out.sort()
    return out[: cfg.callee_limit]


def related_commands(
    graph: GraphIndex | None,
    command_name: str,
    *,
    config: GraphLookupConfig | None = None,
) -> list[str]:
    """Return ``do_*`` commands that share helper functions with this one.

    Two commands are "related" when they call at least
    :attr:`GraphLookupConfig.related_min_shared_helpers` of the same helper
    nodes. This surfaces structurally similar commands without requiring an
    explicit ``runs_after`` annotation in the graph.

    Args:
        graph: The loaded graph index (or ``None``).
        command_name: A ``do_*`` command name with or without the ``do_``
            prefix.
        config: Optional override for the lookup config.

    Returns:
        At most :attr:`GraphLookupConfig.related_limit` command names,
        ordered by descending overlap then alphabetical.
    """
    cfg = config or GraphLookupConfig()
    if graph is None:
        return []
    name = command_name if command_name.startswith(cfg.do_command_prefix) else f"{cfg.do_command_prefix}{command_name}"
    node_id = graph.command_to_node.get(name)
    if node_id is None:
        return []
    own_helpers = {
        neighbour_id
        for neighbour_id, _relation, _confidence in _filter_neighbours(
            graph.adjacency.get(node_id, ()),
            config=cfg,
            accept_relations=cfg.callee_relations,
        )
        if not graph.node_labels.get(neighbour_id, "").endswith(cfg.file_label_suffix)
    }
    if not own_helpers:
        return []
    overlaps: list[tuple[int, str]] = []
    for other_name, other_id in graph.command_to_node.items():
        if other_id == node_id:
            continue
        other_helpers = {
            neighbour_id
            for neighbour_id, _relation, _confidence in _filter_neighbours(
                graph.adjacency.get(other_id, ()),
                config=cfg,
                accept_relations=cfg.callee_relations,
            )
            if not graph.node_labels.get(neighbour_id, "").endswith(cfg.file_label_suffix)
        }
        shared = len(own_helpers & other_helpers)
        if shared >= cfg.related_min_shared_helpers:
            overlaps.append((shared, other_name))
    overlaps.sort(key=lambda row: (-row[0], row[1]))
    return [other_name for _shared, other_name in overlaps[: cfg.related_limit]]


def enrich_detail(
    graph: GraphIndex | None,
    entry: Mapping[str, Any] | None,
    *,
    config: GraphLookupConfig | None = None,
) -> dict[str, Any] | None:
    """Attach ``calls`` and ``related`` lists to a palette detail entry.

    The returned dict is a shallow copy so the underlying command index is
    never mutated. ``None`` input passes through unchanged so callers can
    delegate the missing-target sad path to the renderer.
    """
    if entry is None:
        return None
    cfg = config or GraphLookupConfig()
    name = str(entry.get("name", ""))
    enriched = dict(entry)
    enriched["calls"] = callees(graph, name, config=cfg)
    enriched["related"] = related_commands(graph, name, config=cfg)
    return enriched


def enrich_commands(
    graph: GraphIndex | None,
    rows: Sequence[Mapping[str, Any]],
    *,
    config: GraphLookupConfig | None = None,
) -> list[dict[str, Any]]:
    """Enrich every entry of ``rows`` with neighbour data.

    Used by the C2 view and the Cmd+K overlay so the client-side renderer
    can show "calls" / "related" per row without round-tripping.
    """
    cfg = config or GraphLookupConfig()
    return [enrich_detail(graph, row, config=cfg) or {} for row in rows]


__all__ = [
    "DEFAULT_GRAPH_PATH",
    "GraphIndex",
    "GraphIndexError",
    "GraphLookupConfig",
    "callees",
    "enrich_commands",
    "enrich_detail",
    "load_graph",
    "related_commands",
    "safe_load_graph",
]
