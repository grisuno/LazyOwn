"""Global asset truth store joined to per-task exploration chains.

Ports the LAZY dual-graph contract. Asset nodes deduplicate by a
computed key. Exploration nodes form intent, fact, and finding chains.
Anchors join the two graphs in both directions for coverage queries.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class GraphConfig:
    """Centralized constants for graph behavior."""

    asset_types: frozenset = frozenset(
        {"root_domain", "subdomain", "ip", "service", "app", "endpoint"})
    node_kinds: frozenset = frozenset({"goal", "intent", "fact", "finding", "hint"})


CONFIG = GraphConfig()


def asset_key(asset_type: str, value: str, parent_key: str = "") -> str:
    """Compute the stable deduplication key for an asset."""
    return "|".join([str(asset_type or "").lower(),
                     str(value or "").lower(),
                     str(parent_key or "").lower()])


@dataclass
class AssetNode:
    """Single truth asset in the global graph."""

    node_id: str
    asset_type: str
    value: str
    parent_key: str = ""
    key: str = ""
    company: str = ""
    first_seen: float = 0.0
    last_seen: float = 0.0


@dataclass
class ExplorationNode:
    """Single step in a task exploration chain."""

    node_id: str
    task_id: str
    kind: str
    text: str
    parent_id: str = ""
    created_at: float = 0.0
    payload: dict = field(default_factory=dict)


@dataclass
class Anchor:
    """Join between an exploration node and an asset node."""

    exploration_id: str
    asset_key: str


class AssetGraph:
    """Thread-safe dual graph with bidirectional anchor lookup."""

    def __init__(self, config: GraphConfig = CONFIG) -> None:
        """Initialize empty graphs and anchor indexes."""
        self._config = config
        self._lock = threading.Lock()
        self._assets: dict[str, AssetNode] = {}
        self._nodes: dict[str, ExplorationNode] = {}
        self._by_exploration: dict[str, set[str]] = {}
        self._by_asset: dict[str, set[str]] = {}

    def upsert_asset(self, asset_type: str, value: str,
                     parent_key: str = "", company: str = "") -> AssetNode:
        """Insert or refresh an asset and return the canonical node."""
        normalized = str(asset_type or "").lower()
        if normalized not in self._config.asset_types:
            raise ValueError(f"Unsupported asset type: {asset_type}")
        key = asset_key(normalized, value, parent_key)
        now = time.time()
        with self._lock:
            existing = self._assets.get(key)
            if existing is not None:
                refreshed = AssetNode(
                    node_id=existing.node_id, asset_type=normalized,
                    value=str(value), parent_key=str(parent_key),
                    key=key, company=str(company or existing.company),
                    first_seen=existing.first_seen, last_seen=now)
                self._assets[key] = refreshed
                return refreshed
            node = AssetNode(node_id=uuid.uuid4().hex[:12],
                             asset_type=normalized, value=str(value),
                             parent_key=str(parent_key), key=key,
                             company=str(company),
                             first_seen=now, last_seen=now)
            self._assets[key] = node
            return node

    def add_node(self, task_id: str, kind: str, text: str,
                 parent_id: str = "", payload: dict | None = None) -> ExplorationNode:
        """Append an exploration node to a task chain."""
        normalized = str(kind or "").lower()
        if normalized not in self._config.node_kinds:
            raise ValueError(f"Unsupported node kind: {kind}")
        node = ExplorationNode(node_id=uuid.uuid4().hex[:12],
                               task_id=str(task_id), kind=normalized,
                               text=str(text), parent_id=str(parent_id or ""),
                               created_at=time.time(),
                               payload=dict(payload or {}))
        with self._lock:
            self._nodes[node.node_id] = node
        return node

    def add_fact(self, task_id: str, text: str, parent_id: str = "",
                 payload: dict | None = None) -> ExplorationNode:
        """Append a fact node to a task chain."""
        return self.add_node(task_id, "fact", text, parent_id, payload)

    def add_finding(self, task_id: str, text: str, parent_id: str = "",
                    payload: dict | None = None) -> ExplorationNode:
        """Append a finding node to a task chain."""
        return self.add_node(task_id, "finding", text, parent_id, payload)

    def anchor(self, exploration_id: str, key: str) -> Anchor:
        """Link an exploration node to an asset key."""
        with self._lock:
            if exploration_id not in self._nodes:
                raise KeyError(f"Unknown exploration node: {exploration_id}")
            if key not in self._assets:
                raise KeyError(f"Unknown asset key: {key}")
            link = Anchor(exploration_id=str(exploration_id), asset_key=str(key))
            self._by_exploration.setdefault(link.exploration_id, set()).add(key)
            self._by_asset.setdefault(key, set()).add(link.exploration_id)
            return link

    def assets_for_node(self, exploration_id: str) -> list[AssetNode]:
        """List assets anchored to one exploration node."""
        with self._lock:
            keys = self._by_exploration.get(str(exploration_id), set())
            return [self._assets[k] for k in keys if k in self._assets]

    def nodes_for_asset(self, key: str) -> list[ExplorationNode]:
        """List exploration nodes anchored to one asset."""
        with self._lock:
            ids = self._by_asset.get(str(key), set())
            return [self._nodes[i] for i in ids if i in self._nodes]

    def coverage(self, task_id: str) -> dict:
        """Report tested versus total assets for a task."""
        with self._lock:
            total = len(self._assets)
            tested_keys: set[str] = set()
            for node_id, node in self._nodes.items():
                if node.task_id == str(task_id):
                    tested_keys.update(self._by_exploration.get(node_id, set()))
            tested = len(tested_keys)
        ratio = (tested / total) if total else 0.0
        return {"task_id": str(task_id), "total": total,
                "tested": tested, "ratio": ratio}

    def mirror_to_campaign(self, db: object, world_model: object,
                           workspace_id: int) -> dict[str, int]:
        """Mirror graph assets into the campaign database and world model.

        Deduplicated graph nodes become db hosts/services and world model
        hosts, so the existing db_hosts/vuln_list/sitrep surfaces show
        them. Returns counts of mirrored hosts and services.
        """
        mirrored = {"hosts": 0, "services": 0}
        with self._lock:
            assets = list(self._assets.values())
        for asset in assets:
            try:
                if asset.asset_type in ("root_domain", "subdomain"):
                    host_id = db.host_add(int(workspace_id), asset.value,
                                          hostname=asset.value)
                    mirrored["hosts"] += 1
                    if world_model is not None:
                        world_model.add_host(asset.value)
                elif asset.asset_type == "ip":
                    host_id = db.host_add(int(workspace_id), asset.value)
                    mirrored["hosts"] += 1
                    if world_model is not None:
                        world_model.add_host(asset.value)
                elif asset.asset_type == "service":
                    host_id = db.host_add(int(workspace_id), asset.parent_key or asset.value)
                    try:
                        db.service_add(host_id, int(asset.value), name=asset.value)
                    except (ValueError, TypeError):
                        db.service_add(host_id, 0, name=asset.value)
                    mirrored["services"] += 1
                    if world_model is not None:
                        try:
                            world_model.add_service(asset.parent_key or asset.value,
                                                    int(asset.value), name=asset.value)
                        except (ValueError, TypeError):
                            pass
                else:
                    continue
            except Exception:
                continue
        return mirrored


def coverage_for(db: object, workspace_id: int, scope: list[str]) -> dict:
    """Report tested scope assets versus total scope from the campaign db.

    The scope is the explicit target list (never inferred). An address
    counts as tested when present in the workspace hosts.
    """
    wanted = [str(a).strip().lower() for a in (scope or []) if str(a).strip()]
    try:
        held = {str(h.get("address", "")).lower() for h in db.host_list(int(workspace_id))}
    except Exception:
        held = set()
    tested = sorted(a for a in wanted if a in held)
    total = len(wanted)
    return {"scope": sorted(wanted), "total": total, "tested": tested,
            "untested": sorted(a for a in wanted if a not in held),
            "ratio": (len(tested) / total) if total else 0.0}
