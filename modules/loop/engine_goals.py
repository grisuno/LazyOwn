from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.lazy_loop import ExplorationGraph, ExplorationNode


class EngineGoalsMixin:
    """Extracted LazyLoopEngine methods (verbatim lift + lazy imports).

    Each method injects its ``modules.lazy_loop`` module-level dependencies as a
    lazy import to avoid a circular import at load time. See
    modules/loop/README.md for the decomposition contract.
    """

    def add_intent(
        self,
        task_id: str,
        summary: str,
        asset_ids: list[int] | None = None,
        parent_ids: list[int] | None = None,
        priority: int | None = None,
    ) -> ExplorationNode:
        """Directly inject high-priority intent like the planner main-agent add_intent."""
        from modules.lazy_loop import DEFAULT_PRIORITY, ActivityLog, AssetGate, ExplorationGraph
        if priority is None:
            priority = DEFAULT_PRIORITY
        for asset_id in asset_ids or []:
            asset = self.assets.get(int(asset_id))
            if asset is not None:
                verdict = AssetGate(task_id).evaluate(asset.value)
                if not verdict["allowed"]:
                    raise ValueError(verdict["reason"])
        graph = ExplorationGraph(task_id)
        node = graph.add_node("intent", summary, priority=priority)
        for parent in parent_ids or []:
            graph.add_edge(parent, node.node_id, "derived_from")
        for asset_id in asset_ids or []:
            graph.anchor(node.node_id, int(asset_id))
        ActivityLog(task_id).emit("human", "intent", f"injected #{node.node_id}: {summary}", intent_id=node.node_id)
        self.store.set_status(task_id, "running")
        return node

    def set_goals(self, task_id: str, specs: list[dict]) -> list[ExplorationNode]:
        """Replace/append decomposed objectives like set_goals; wakes the task."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph
        graph = ExplorationGraph(task_id)
        created = []
        for spec in specs or []:
            text = str((spec or {}).get("text", "")).strip()
            if not text:
                continue
            node = graph.add_node(
                "goal", text[:300], state="pending", meta={"vulnclass": str((spec or {}).get("vulnclass", ""))[:80]}
            )
            created.append(node)
            ActivityLog(task_id).emit("planner", "goal", f"goal #{node.node_id}: {text[:160]}")
        if created:
            self.store.resume(task_id)
        return created

    def edit_goal(self, task_id: str, goal_id: int, text: str) -> bool:
        """Edit a goal node like the goals manager."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph, _now, scrub_secrets
        graph = ExplorationGraph(task_id)
        node = graph.get(int(goal_id))
        if node is None or node.kind != "goal" or not (text or "").strip():
            return False
        node.text = scrub_secrets(text.strip()[:300])
        node.updated = _now()
        graph._persist()
        ActivityLog(task_id).emit("planner", "goal", f"goal #{goal_id} edited")
        return True

    def delete_goal(self, task_id: str, goal_id: int) -> bool:
        """Delete a goal node; done tasks with no goals left stay done."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph
        graph = ExplorationGraph(task_id)
        node = graph.get(int(goal_id))
        if node is None or node.kind != "goal":
            return False
        del graph.nodes[int(goal_id)]
        graph._persist()
        ActivityLog(task_id).emit("planner", "goal", f"goal #{goal_id} deleted")
        return True

    def preview_delete_intent(self, task_id: str, intent_id: int) -> dict:
        """Estimate hard-delete cascade without mutating anything.

        Args:
            task_id: Task owning the intent.
            intent_id: Intent node id.

        Returns:
            Dict with intent_id, removable ids, shared (kept) ids.
        """
        from modules.lazy_loop import ExplorationGraph
        graph = ExplorationGraph(task_id)
        node = graph.get(int(intent_id))
        if node is None or node.kind != "intent":
            raise KeyError(f"unknown intent: {intent_id}")
        reachable = self._intent_subtree(graph, int(intent_id))
        removable, shared = self._split_exclusive(graph, reachable)
        return {
            "intent_id": int(intent_id),
            "removable": sorted(removable),
            "shared": sorted(shared),
            "cascade": len(removable),
        }

    def delete_intent(self, task_id: str, intent_id: int, mode: str = "soft", reason: str = "") -> dict:
        """Delete an intent in soft (fake) or hard (true) mode.

        Soft keeps the node and all outputs/lineage, marking it deleted
        with the reason. Hard physically removes the intent plus its
        exclusively-owned descendants, keeps shared nodes and goals,
        archives the usage snapshot by date and notifies the planner
        to replan without it.

        Args:
            task_id: Task owning the intent.
            intent_id: Intent node id.
            mode: ``soft`` (default) or ``hard``.
            reason: Operator reason (required).

        Returns:
            Dict with mode, intent_id, removed/shared ids and reason.
        """
        from modules.lazy_loop import (
            ActivityLog,
            EvidenceStore,
            ExplorationGraph,
            _load_json,
            _now,
            _save_json,
            _store_path,
        )
        reason = (reason or "").strip()
        if not reason:
            raise ValueError("a deletion reason is required")
        if mode not in ("soft", "hard"):
            raise ValueError("mode must be soft|hard")
        graph = ExplorationGraph(task_id)
        node = graph.get(int(intent_id))
        if node is None or node.kind != "intent":
            raise KeyError(f"unknown intent: {intent_id}")
        if node.state == "deleted":
            raise ValueError(f"intent #{intent_id} is already deleted")
        if node.state not in ("pending", "open", "running", "paused"):
            raise ValueError(f"intent #{intent_id} in state {node.state} cannot be deleted")
        activity = ActivityLog(task_id)
        summary = str(node.text or "")[:300]
        if mode == "soft":
            node.state = "deleted"
            node.updated = _now()
            node.meta["deleted"] = True
            node.meta["delete_mode"] = "soft"
            node.meta["delete_reason"] = reason[:500]
            node.meta["deleted_ts"] = _now()
            graph._persist()
            activity.emit(
                "human", "intent-delete", f"intent #{intent_id} soft-deleted: {reason[:200]}", intent_id=int(intent_id)
            )
            activity.emit(
                "planner",
                "cancelled",
                f"intent #{intent_id} by user deleted, content: {summary}, "
                f"reason: {reason[:200]}; deleted, replan without it",
                intent_id=int(intent_id),
            )
            return {
                "mode": "soft",
                "intent_id": int(intent_id),
                "removed": [],
                "shared": [],
                "reason": reason[:500],
                "summary": summary,
            }
        reachable = self._intent_subtree(graph, int(intent_id))
        removable, shared = self._split_exclusive(graph, reachable)
        graph.remove_nodes(removable)
        try:
            valid_findings = {n.node_id for n in graph.list("finding")}
            EvidenceStore(task_id).gc(valid_findings)
        except Exception:
            pass
        archive_path = _store_path(f"deleted_intents_{task_id}.json")
        archive = _load_json(archive_path, {"items": []})
        archive.setdefault("items", []).append(
            {
                "intent_id": int(intent_id),
                "mode": "hard",
                "reason": reason[:500],
                "summary": summary,
                "ts": _now(),
                "date": time.strftime("%Y-%m-%d", time.localtime(_now())),
                "removed": sorted(removable),
                "shared": sorted(shared),
                "usage": self.budget.usage(task_id),
            }
        )
        _save_json(archive_path, archive)
        activity.emit(
            "human",
            "intent-delete",
            f"intent #{intent_id} hard-deleted ({len(removable)} nodes): {reason[:200]}",
            intent_id=int(intent_id),
        )
        activity.emit(
            "planner",
            "cancelled",
            f"intent #{intent_id} by user deleted, content: {summary}, "
            f"reason: {reason[:200]}; deleted, replan without it",
            intent_id=int(intent_id),
        )
        return {
            "mode": "hard",
            "intent_id": int(intent_id),
            "removed": sorted(removable),
            "shared": sorted(shared),
            "reason": reason[:500],
            "summary": summary,
        }

    def _intent_subtree(self, graph: ExplorationGraph, intent_id: int) -> set[int]:
        """Return intent plus exclusive descendants along yields/derived_from/spawns."""
        seen = {int(intent_id)}
        queue = [int(intent_id)]
        allowed = {"yields", "derived_from", "spawns"}
        while queue:
            current = queue.pop()
            for edge in graph.edges:
                if edge.src != current or edge.kind not in allowed:
                    continue
                if edge.dst not in seen:
                    seen.add(edge.dst)
                    queue.append(edge.dst)
        return seen

    def _split_exclusive(self, graph: ExplorationGraph, reachable: set[int]) -> tuple[set[int], set[int]]:
        """Split reachable ids into exclusive (removable) vs shared (kept)."""
        removable: set[int] = set()
        shared: set[int] = set()
        for victim in reachable:
            node = graph.get(int(victim))
            if node is None:
                continue
            if node.kind == "goal":
                shared.add(int(victim))
                continue
            if node.meta.get("origin"):
                shared.add(int(victim))
                continue
            external = [src for src in graph.parents(int(victim)) if src not in reachable]
            if external:
                shared.add(int(victim))
                continue
            removable.add(int(victim))
        return removable, shared

    def add_hint(self, task_id: str, text: str) -> ExplorationNode:
        """Inject human steering hint read by the next planner round.

        Beyond the hint node, records an explicit planner trigger naming
        the new hint so the round is visibly fired by it instead of
        leaving the planner to discover the hint inside the overview.
        """
        from modules.lazy_loop import ActivityLog, ExplorationGraph
        graph = ExplorationGraph(task_id)
        node = graph.add_node("hint", text)
        activity = ActivityLog(task_id)
        activity.emit("human", "hint", text)
        activity.emit(
            "planner",
            "hint-trigger",
            f"human added 1 strategic hint: {text[:200]}; this round fires on new hint #{node.node_id}",
        )
        return node

