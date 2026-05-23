"""Graph-aware advisor backed by the graphify knowledge graph.

This module turns the JSON file produced by ``/graphify`` over the LazyOwn
codebase (``graphify-out/graph_lazyown.json`` or any standard graphify
``graph.json``) into a fast, in-memory advisor that powers two new
user-experience features:

1. **Human operators** get graph-aware CLI commands — ``graph_search``,
   ``neighbors``, ``god_nodes``, ``suggest_next`` — and "did you mean ...?"
   recovery when they type an unknown ``do_*`` command. The advisor reads
   the recent ``LazyOwn_session_report.csv`` and recommends the next
   command by walking the graph outward from the most recent nodes.
2. **MCP agents** get four token-budget-aware tools so they can ask the
   knowledge graph for related commands, neighbours, suggestions, and a
   summary without re-reading the full report each turn.

Design (SOLID):

- ``GraphAdvisorConfig`` centralises every magic value (file paths,
  budgets, scoring weights, glyphs, token-budget caps).
- ``GraphLoader`` is the only piece touching the filesystem. It caches by
  ``(path, mtime)`` so repeated calls inside one process are free.
- ``GraphIndex`` provides O(1) lookups by id, label, and community.
- ``GraphScorer`` is a pure ranking primitive (Single Responsibility).
- ``GraphAdvisor`` is the orchestrator. It composes loader + index +
  scorer and exposes the small public surface used by the CLI, the MCP
  layer, the C2 web UI and the test suite.

The module has zero coupling to ``cmd2``, ``mcp.server``, ``flask`` or
``lazyown.py``. Every public method returns plain Python types so the
same advisor instance works equally well in any caller.
"""

from __future__ import annotations

import csv
import json
import os
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class GraphAdvisorConfig:
    """Centralised constants for the graph advisor.

    Every magic path, budget, weight or glyph lives here. Operators or
    tests can override any field by passing a fresh instance to
    :class:`GraphAdvisor`.
    """

    sessions_dir: str = "sessions"
    graphify_dir: str = "graphify-out"
    graph_candidates: tuple[str, ...] = (
        "graph.json",
        "graph_lazyown.json",
        "graph_focused.json",
    )
    transcript_filename: str = "LazyOwn_session_report.csv"
    transcript_command_column: str = "tool"
    fallback_transcript_columns: tuple[str, ...] = ("command", "tool", "name")

    default_search_limit: int = 10
    default_neighbor_depth: int = 1
    default_neighbor_limit: int = 25
    default_god_node_limit: int = 10
    default_suggestion_limit: int = 5
    default_recent_command_window: int = 12
    default_token_budget: int = 1500
    chars_per_token: int = 4

    stale_after_days: float = 7.0
    health_fresh: str = "fresh"
    health_stale: str = "stale"
    health_empty: str = "empty"

    score_exact: float = 1.0
    score_prefix: float = 0.9
    score_subsequence: float = 0.7
    score_substring: float = 0.6
    score_similarity_weight: float = 0.55
    score_similarity_floor: float = 0.4
    score_zero: float = 0.0

    suggestion_decay: float = 0.65
    suggestion_seed_self_weight: float = 0.0

    truncate_indicator: str = " …"


@dataclass(frozen=True)
class GraphNode:
    """Immutable view onto a node loaded from the graphify JSON."""

    id: str
    label: str
    community: int | None
    file_type: str
    source_file: str
    source_location: str
    extra: dict[str, Any] = field(default_factory=dict)

    def to_summary(self) -> dict[str, Any]:
        """Return a small, JSON-safe summary suitable for MCP responses."""
        return {
            "id": self.id,
            "label": self.label,
            "community": self.community,
            "file_type": self.file_type,
            "source_file": self.source_file,
            "source_location": self.source_location,
        }


@dataclass(frozen=True)
class GraphEdge:
    """Immutable view onto an edge loaded from the graphify JSON."""

    source: str
    target: str
    relation: str
    confidence: str
    weight: float
    confidence_score: float

    def to_summary(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "confidence": self.confidence,
            "confidence_score": self.confidence_score,
        }


@dataclass(frozen=True)
class ScoredNode:
    """Node plus its score and match position metadata."""

    node: GraphNode
    score: float
    matched_field: str


class GraphLoader:
    """Load a graphify JSON file with per-process ``(path, mtime)`` cache."""

    _cache: dict[str, tuple[float, dict[str, Any]]] = {}

    def __init__(self, config: GraphAdvisorConfig) -> None:
        self._cfg = config
        self._sticky_path: Path | None = None

    def resolve_path(self, override: str | os.PathLike[str] | None = None) -> Path | None:
        """Resolve which graphify JSON file to load.

        Honours an explicit override; otherwise returns the last path
        successfully loaded through this loader, falling back to a scan
        of :attr:`GraphAdvisorConfig.graph_candidates` inside
        :attr:`GraphAdvisorConfig.graphify_dir`. Returns ``None`` when no
        graph is available so callers can present a clear "graph
        missing" message instead of crashing.
        """
        if override is not None:
            path = Path(override)
            return path if path.exists() else None
        if self._sticky_path is not None and self._sticky_path.exists():
            return self._sticky_path
        graphify_dir = Path(self._cfg.graphify_dir)
        if not graphify_dir.exists():
            return None
        for candidate in self._cfg.graph_candidates:
            target = graphify_dir / candidate
            if target.exists():
                return target
        return None

    def load(self, override: str | os.PathLike[str] | None = None) -> dict[str, Any] | None:
        path = self.resolve_path(override)
        if path is None:
            return None
        try:
            mtime = path.stat().st_mtime
        except OSError:
            return None
        key = str(path.resolve())
        cached = GraphLoader._cache.get(key)
        if cached and cached[0] == mtime:
            self._sticky_path = path
            return cached[1]
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return None
        GraphLoader._cache[key] = (mtime, data)
        self._sticky_path = path
        return data

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()


class GraphIndex:
    """In-memory index over a graphify graph for O(1) lookups."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._raw = data
        self._nodes: dict[str, GraphNode] = {}
        self._adjacency: dict[str, list[str]] = {}
        self._edges: dict[tuple[str, str], list[GraphEdge]] = {}
        self._community_members: dict[int, list[str]] = {}
        self._degree: Counter[str] = Counter()
        self._build()

    def _build(self) -> None:
        for raw in self._raw.get("nodes", []):
            if not isinstance(raw, dict) or "id" not in raw:
                continue
            community_raw = raw.get("community")
            try:
                community = int(community_raw) if community_raw is not None else None
            except (TypeError, ValueError):
                community = None
            node = GraphNode(
                id=str(raw["id"]),
                label=str(raw.get("label") or raw["id"]),
                community=community,
                file_type=str(raw.get("file_type") or ""),
                source_file=str(raw.get("source_file") or ""),
                source_location=str(raw.get("source_location") or ""),
                extra=raw,
            )
            self._nodes[node.id] = node
            self._adjacency[node.id] = []
            if community is not None:
                self._community_members.setdefault(community, []).append(node.id)
        edges_raw = self._raw.get("links") or self._raw.get("edges") or []
        for raw in edges_raw:
            if not isinstance(raw, dict):
                continue
            source = str(raw.get("source") or "")
            target = str(raw.get("target") or "")
            if not source or not target:
                continue
            if source not in self._nodes or target not in self._nodes:
                continue
            try:
                weight = float(raw.get("weight") or 1.0)
            except (TypeError, ValueError):
                weight = 1.0
            try:
                confidence_score = float(raw.get("confidence_score") or 0.0)
            except (TypeError, ValueError):
                confidence_score = 0.0
            edge = GraphEdge(
                source=source,
                target=target,
                relation=str(raw.get("relation") or ""),
                confidence=str(raw.get("confidence") or ""),
                weight=weight,
                confidence_score=confidence_score,
            )
            self._edges.setdefault((source, target), []).append(edge)
            self._adjacency.setdefault(source, []).append(target)
            self._adjacency.setdefault(target, []).append(source)
            self._degree[source] += 1
            self._degree[target] += 1

    def nodes(self) -> list[GraphNode]:
        return list(self._nodes.values())

    def get(self, node_id: str) -> GraphNode | None:
        return self._nodes.get(node_id)

    def neighbors(self, node_id: str) -> list[str]:
        return list(self._adjacency.get(node_id, []))

    def edges_between(self, source: str, target: str) -> list[GraphEdge]:
        return list(self._edges.get((source, target), [])) + list(self._edges.get((target, source), []))

    def community_members(self, community_id: int) -> list[str]:
        return list(self._community_members.get(community_id, []))

    def degree(self, node_id: str) -> int:
        return int(self._degree.get(node_id, 0))

    def degree_ranked(self) -> list[tuple[str, int]]:
        return self._degree.most_common()


class GraphScorer:
    """Pure ranking primitive shared by search and suggest-next."""

    _TOKEN_RE = re.compile(r"[a-z0-9]+")

    def __init__(self, config: GraphAdvisorConfig) -> None:
        self._cfg = config

    def rank(self, nodes: Iterable[GraphNode], query: str) -> list[ScoredNode]:
        terms = self._tokens(query)
        if not terms:
            return [ScoredNode(node=node, score=self._cfg.score_exact, matched_field="all") for node in nodes]
        ranked: list[ScoredNode] = []
        for node in nodes:
            score, field_name = self._best_score(node, terms, query)
            if score > self._cfg.score_zero:
                ranked.append(ScoredNode(node=node, score=score, matched_field=field_name))
        ranked.sort(key=lambda s: (-s.score, s.node.id))
        return ranked

    def _best_score(self, node: GraphNode, terms: list[str], raw_query: str) -> tuple[float, str]:
        haystacks = (
            ("label", node.label.lower()),
            ("id", node.id.lower()),
            ("source_file", node.source_file.lower()),
        )
        query = raw_query.strip().lower()
        best = (self._cfg.score_zero, "")
        for field_name, value in haystacks:
            if not value:
                continue
            score = self._score(value, terms, query)
            if score > best[0]:
                best = (score, field_name)
        return best

    def _score(self, value: str, terms: list[str], query: str) -> float:
        if query and value == query:
            return self._cfg.score_exact
        if query and value.startswith(query):
            return self._cfg.score_prefix
        if terms and all(term in value for term in terms):
            return self._cfg.score_subsequence
        if query and query in value:
            return self._cfg.score_substring
        if query:
            similarity = SequenceMatcher(None, value, query).ratio()
            if similarity >= self._cfg.score_similarity_floor:
                return similarity * self._cfg.score_similarity_weight
        return self._cfg.score_zero

    def _tokens(self, query: str) -> list[str]:
        return [match.group(0) for match in self._TOKEN_RE.finditer((query or "").lower()) if len(match.group(0)) > 1]


class GraphAdvisor:
    """High-level facade over the graphify knowledge graph.

    All public methods return plain Python lists/dicts so callers can
    serialise to JSON (MCP), render Markdown (CLI) or template HTML (web
    UI) without further translation.
    """

    def __init__(
        self,
        config: GraphAdvisorConfig | None = None,
        loader: GraphLoader | None = None,
        index: GraphIndex | None = None,
        scorer: GraphScorer | None = None,
    ) -> None:
        self._cfg = config or GraphAdvisorConfig()
        self._loader = loader or GraphLoader(self._cfg)
        self._scorer = scorer or GraphScorer(self._cfg)
        self._index: GraphIndex | None = index

    @classmethod
    def from_path(
        cls, path: str | os.PathLike[str] | None = None, config: GraphAdvisorConfig | None = None
    ) -> GraphAdvisor:
        cfg = config or GraphAdvisorConfig()
        loader = GraphLoader(cfg)
        data = loader.load(path)
        index = GraphIndex(data) if data is not None else None
        return cls(config=cfg, loader=loader, index=index)

    def is_available(self) -> bool:
        return self._ensure_index() is not None

    def reload(self, path: str | os.PathLike[str] | None = None) -> bool:
        GraphLoader.clear_cache()
        data = self._loader.load(path)
        if data is None:
            self._index = None
            return False
        self._index = GraphIndex(data)
        return True

    def summary(self) -> dict[str, Any]:
        index = self._ensure_index()
        if index is None:
            return {"available": False, "reason": self._missing_reason()}
        nodes = index.nodes()
        edges_count = sum(1 for _ in self._iter_all_edges(index))
        communities: dict[int, int] = {}
        for node in nodes:
            if node.community is not None:
                communities[node.community] = communities.get(node.community, 0) + 1
        graph_path = self._loader.resolve_path()
        age_days = self._graph_age_days(graph_path)
        health, hint = self._classify_health(edges_count, age_days)
        payload: dict[str, Any] = {
            "available": True,
            "nodes": len(nodes),
            "edges": edges_count,
            "communities": len(communities),
            "community_sizes": dict(sorted(communities.items())),
            "graph_path": str(graph_path) if graph_path is not None else None,
            "age_days": round(age_days, 1) if age_days is not None else None,
            "health": health,
        }
        if hint:
            payload["hint"] = hint
        return payload

    def _graph_age_days(self, path: Path | None) -> float | None:
        if path is None:
            return None
        try:
            mtime = path.stat().st_mtime
        except OSError:
            return None
        return max(0.0, (time.time() - mtime) / 86400.0)

    def _classify_health(self, edges_count: int, age_days: float | None) -> tuple[str, str | None]:
        if edges_count == 0:
            return (
                self._cfg.health_empty,
                "graph has zero edges; run '/graphify .' to rebuild",
            )
        if age_days is not None and age_days >= self._cfg.stale_after_days:
            return (
                self._cfg.health_stale,
                f"graph is {age_days:.0f} days old; run '/graphify . --update' to refresh",
            )
        return self._cfg.health_fresh, None

    def search(self, query: str, limit: int | None = None) -> list[dict[str, Any]]:
        index = self._ensure_index()
        if index is None:
            return []
        bound = limit or self._cfg.default_search_limit
        ranked = self._scorer.rank(index.nodes(), query)
        return [
            {**scored.node.to_summary(), "score": round(scored.score, 3), "matched_field": scored.matched_field}
            for scored in ranked[:bound]
        ]

    def neighbors(self, node_query: str, depth: int | None = None, limit: int | None = None) -> dict[str, Any]:
        index = self._ensure_index()
        if index is None:
            return {"available": False, "reason": self._missing_reason()}
        node = self._resolve_query(node_query)
        if node is None:
            return {"available": True, "matched": None, "neighbors": []}
        depth_value = max(1, depth or self._cfg.default_neighbor_depth)
        limit_value = max(1, limit or self._cfg.default_neighbor_limit)
        visited = {node.id}
        frontier = {node.id}
        layers: list[list[dict[str, Any]]] = []
        for _ in range(depth_value):
            next_frontier: set[str] = set()
            layer: list[dict[str, Any]] = []
            for current in sorted(frontier):
                for neighbour_id in index.neighbors(current):
                    if neighbour_id in visited:
                        continue
                    neighbour = index.get(neighbour_id)
                    if neighbour is None:
                        continue
                    edges = [edge.to_summary() for edge in index.edges_between(current, neighbour_id)]
                    layer.append(
                        {
                            "from": current,
                            "node": neighbour.to_summary(),
                            "edges": edges,
                            "degree": index.degree(neighbour_id),
                        }
                    )
                    next_frontier.add(neighbour_id)
                    visited.add(neighbour_id)
                    if sum(len(layer_acc) for layer_acc in layers) + len(layer) >= limit_value:
                        break
                if sum(len(layer_acc) for layer_acc in layers) + len(layer) >= limit_value:
                    break
            if layer:
                layers.append(layer)
            frontier = next_frontier
            if not frontier:
                break
        return {
            "available": True,
            "matched": node.to_summary(),
            "depth": depth_value,
            "neighbors": [entry for layer in layers for entry in layer],
        }

    def god_nodes(self, limit: int | None = None) -> list[dict[str, Any]]:
        index = self._ensure_index()
        if index is None:
            return []
        bound = limit or self._cfg.default_god_node_limit
        ranked: list[dict[str, Any]] = []
        for node_id, degree in index.degree_ranked()[:bound]:
            node = index.get(node_id)
            if node is None:
                continue
            payload = node.to_summary()
            payload["degree"] = int(degree)
            ranked.append(payload)
        return ranked

    def suggest_next(
        self,
        recent_commands: Sequence[str] | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Suggest next commands by walking the graph outward from recent ones.

        ``recent_commands`` is a list of command identifiers — typically
        read from ``sessions/LazyOwn_session_report.csv``. The suggestion
        score is the weighted sum of inverse-distance contributions from
        every recent seed, with an exponential decay configured on
        :class:`GraphAdvisorConfig`. Nodes that *are* recent commands are
        deprioritised so the suggestion is always forward-looking.
        """
        index = self._ensure_index()
        if index is None:
            return []
        if recent_commands is None:
            recent_commands = self.read_recent_commands()
        seeds = self._seed_nodes(recent_commands)
        if not seeds:
            return []
        seed_ids = {node.id for node in seeds}
        scores: dict[str, float] = {}
        decay = self._cfg.suggestion_decay
        for seed in seeds:
            distances = self._bfs_distance(index, seed.id, max_hops=3)
            for other_id, distance in distances.items():
                if other_id in seed_ids and self._cfg.suggestion_seed_self_weight == 0.0:
                    continue
                contribution = decay**distance
                scores[other_id] = scores.get(other_id, 0.0) + contribution
        ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))
        bound = limit or self._cfg.default_suggestion_limit
        out: list[dict[str, Any]] = []
        for node_id, score in ranked:
            node = index.get(node_id)
            if node is None:
                continue
            payload = node.to_summary()
            payload["score"] = round(score, 3)
            out.append(payload)
            if len(out) >= bound:
                break
        return out

    def read_recent_commands(self, window: int | None = None) -> list[str]:
        """Read the last N executed commands from the session transcript."""
        bound = window or self._cfg.default_recent_command_window
        path = Path(self._cfg.sessions_dir) / self._cfg.transcript_filename
        if not path.exists():
            return []
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
        except (OSError, csv.Error):
            return []
        if not rows:
            return []
        columns = (self._cfg.transcript_command_column,) + self._cfg.fallback_transcript_columns
        chosen_column = next((c for c in columns if c in rows[0]), None)
        if chosen_column is None:
            return []
        commands: list[str] = []
        for row in rows[-bound:]:
            value = (row.get(chosen_column) or "").strip()
            if value:
                commands.append(value)
        return commands

    def did_you_mean(self, query: str, limit: int = 3) -> list[str]:
        results = self.search(query, limit=max(limit, 5))
        suggestions: list[str] = []
        seen: set[str] = set()
        for entry in results:
            label = str(entry.get("label") or entry.get("id") or "").strip()
            if not label or label in seen:
                continue
            seen.add(label)
            suggestions.append(label)
            if len(suggestions) >= limit:
                break
        return suggestions

    def truncate_to_budget(self, payload: dict[str, Any], budget_tokens: int | None = None) -> dict[str, Any]:
        """Trim list fields in-place so the JSON dump fits a token budget."""
        budget = budget_tokens or self._cfg.default_token_budget
        char_budget = budget * self._cfg.chars_per_token
        encoded = json.dumps(payload, ensure_ascii=False)
        if len(encoded) <= char_budget:
            return payload
        for key, value in list(payload.items()):
            if not isinstance(value, list) or not value:
                continue
            while len(value) > 1 and len(json.dumps(payload, ensure_ascii=False)) > char_budget:
                value.pop()
            payload[key] = value
            payload["truncated"] = True
            payload[f"{key}_remaining"] = max(0, len(value))
            if len(json.dumps(payload, ensure_ascii=False)) <= char_budget:
                break
        return payload

    def _seed_nodes(self, recent_commands: Sequence[str]) -> list[GraphNode]:
        index = self._ensure_index()
        if index is None or not recent_commands:
            return []
        seeds: list[GraphNode] = []
        seen: set[str] = set()
        for command in recent_commands:
            node = self._resolve_query(command)
            if node is None or node.id in seen:
                continue
            seeds.append(node)
            seen.add(node.id)
        return seeds

    def _resolve_query(self, query: str) -> GraphNode | None:
        index = self._ensure_index()
        if index is None or not query:
            return None
        direct = index.get(query)
        if direct is not None:
            return direct
        ranked = self._scorer.rank(index.nodes(), query)
        return ranked[0].node if ranked else None

    @staticmethod
    def _bfs_distance(index: GraphIndex, start: str, max_hops: int) -> dict[str, int]:
        distances = {start: 0}
        frontier = [start]
        for hop in range(1, max_hops + 1):
            next_frontier: list[str] = []
            for current in frontier:
                for neighbour_id in index.neighbors(current):
                    if neighbour_id not in distances:
                        distances[neighbour_id] = hop
                        next_frontier.append(neighbour_id)
            frontier = next_frontier
            if not frontier:
                break
        return distances

    @staticmethod
    def _iter_all_edges(index: GraphIndex) -> Iterable[GraphEdge]:
        seen: set[tuple[str, str]] = set()
        for node in index.nodes():
            for neighbour_id in index.neighbors(node.id):
                key = tuple(sorted((node.id, neighbour_id)))
                if key in seen:
                    continue
                seen.add(key)
                yield from index.edges_between(node.id, neighbour_id)

    def _ensure_index(self) -> GraphIndex | None:
        if self._index is not None:
            return self._index
        data = self._loader.load()
        if data is None:
            return None
        self._index = GraphIndex(data)
        return self._index

    def _missing_reason(self) -> str:
        resolved = self._loader.resolve_path()
        if resolved is None:
            return f"no graphify graph found in {self._cfg.graphify_dir}/. Run '/graphify .' to build one."
        return f"graphify graph at {resolved} failed to parse"


def format_search_table(results: Sequence[dict[str, Any]]) -> str:
    """Render search results as a fixed-width table for the cmd2 shell."""
    if not results:
        return "no matches"
    lines = ["label                              degree score  community  source_file"]
    for entry in results:
        label = (entry.get("label") or entry.get("id") or "")[:32].ljust(32)
        degree = str(entry.get("degree", "-")).rjust(6)
        score = str(entry.get("score", "-")).rjust(6)
        community = str(entry.get("community", "-")).rjust(9)
        source = entry.get("source_file") or ""
        lines.append(f"  {label} {degree} {score}  {community}  {source}")
    return "\n".join(lines)


def format_neighbors(result: dict[str, Any]) -> str:
    """Render a :py:meth:`GraphAdvisor.neighbors` result as plain text."""
    if not result.get("available"):
        return result.get("reason", "graph unavailable")
    matched = result.get("matched") or {}
    if not matched:
        return "no node matched"
    head = f"match: {matched.get('label')} (id={matched.get('id')}, community={matched.get('community')})"
    rows = []
    for entry in result.get("neighbors", []):
        node = entry.get("node") or {}
        relations = ", ".join(
            f"{edge.get('relation') or 'related'}:{edge.get('confidence') or '?'}" for edge in entry.get("edges", [])
        )
        rows.append(f"  {node.get('label')}  [{relations}]  deg={entry.get('degree')}  src={node.get('source_file')}")
    return "\n".join([head] + (rows or ["  (no neighbors)"]))


def format_god_nodes(results: Sequence[dict[str, Any]]) -> str:
    if not results:
        return "no god nodes"
    lines = ["rank  degree  label"]
    for rank, entry in enumerate(results, 1):
        label = entry.get("label") or entry.get("id") or ""
        lines.append(f"  {str(rank).rjust(4)}  {str(entry.get('degree', 0)).rjust(6)}  {label}")
    return "\n".join(lines)


def format_suggestions(results: Sequence[dict[str, Any]]) -> str:
    if not results:
        return "no suggestions (graph empty or no recent commands)"
    lines = ["score  community  label                            source_file"]
    for entry in results:
        label = (entry.get("label") or entry.get("id") or "")[:32].ljust(32)
        score = str(entry.get("score", 0)).rjust(5)
        community = str(entry.get("community", "-")).rjust(9)
        source = entry.get("source_file") or ""
        lines.append(f"  {score}  {community}  {label}  {source}")
    return "\n".join(lines)


__all__ = [
    "GraphAdvisor",
    "GraphAdvisorConfig",
    "GraphEdge",
    "GraphIndex",
    "GraphLoader",
    "GraphNode",
    "GraphScorer",
    "ScoredNode",
    "format_god_nodes",
    "format_neighbors",
    "format_search_table",
    "format_suggestions",
]
