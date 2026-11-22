from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.lazy_loop import ActivityLog, ExplorationGraph, Guard, TrafficLog


class EngineTaskMixin:
    """Extracted LazyLoopEngine methods (verbatim lift + lazy imports).

    Each method injects its ``modules.lazy_loop`` module-level dependencies as a
    lazy import to avoid a circular import at load time. See
    modules/loop/README.md for the decomposition contract.
    """

    def create_task(self, goal: str, description: str = "") -> dict:
        """Create task, decompose goals, register scope, return summary."""
        from modules.lazy_loop import (
            ActivityLog,
            ExplorationGraph,
            _payload_scope_items,
            decompose_goals,
            extract_constraint_items,
            extract_scope_items,
        )
        task = self.store.create(goal, description)
        graph = ExplorationGraph(task.task_id)
        ActivityLog(task.task_id).emit("engine", "decompose", f"decomposing goal into verifiable goals: {goal[:160]}")
        for spec in decompose_goals(goal, description):
            graph.add_node("goal", spec["text"], state="pending", meta={"vulnclass": spec["vulnclass"]})
        added = 0
        for item in extract_scope_items(goal, description):
            try:
                self.store.add_scope(task.task_id, item["kind"], item["value"], item["reason"])
                try:
                    self.assets.insert(item["kind"], item["value"], task_id=task.task_id)
                except ValueError:
                    pass
                added += 1
            except (KeyError, ValueError):
                continue
        for item in _payload_scope_items():
            try:
                self.store.add_scope(task.task_id, item["kind"], item["value"], item["reason"])
                try:
                    self.assets.insert(item["kind"], item["value"], task_id=task.task_id)
                except ValueError:
                    pass
                added += 1
            except (KeyError, ValueError):
                continue
        for item in extract_constraint_items(goal, description):
            try:
                self.store.add_constraint(task.task_id, item["type"], item["text"])
            except (KeyError, ValueError):
                continue
        ActivityLog(task.task_id).emit(
            "engine", "task", f"created: {goal[:200]} (scope={added}, goals={len(graph.list('goal'))})"
        )
        self._sync_c2_board([task.task_id])
        return {"task_id": task.task_id, "goal": task.goal, "goals": len(graph.list("goal")), "scope": added}

    def spawn_task(self, goal: str, source_task_ids: list[str] | None = None, description: str = "") -> dict:
        """Create a task read-only inheriting assets and findings.

        Scope rules copy over verbatim and each source finding lands as
        a fact stamped with its origin, so the child reads everything
        without ever mutating the parents.
        """
        from modules.lazy_loop import ActivityLog, ExplorationGraph
        summary = self.create_task(goal, description)
        task_id = summary["task_id"]
        inherited = {"scope": 0, "facts": 0, "sources": []}
        for source_id in source_task_ids or []:
            source_id = (source_id or "").strip()
            record = self.store.get(source_id)
            if record is None:
                continue
            graph = ExplorationGraph(task_id)
            for item in record.get("scope", []) or []:
                try:
                    self.store.add_scope(
                        task_id, str(item.get("kind", "")), str(item.get("value", "")), f"inherited from {source_id}"
                    )
                    inherited["scope"] += 1
                except (KeyError, ValueError):
                    continue
            source_graph = ExplorationGraph(source_id)
            for finding in source_graph.list("finding"):
                node = graph.add_node(
                    "fact",
                    f"[{source_id} finding #{finding.node_id}] {finding.text[:400]}",
                    state="done",
                    meta={
                        "inherited_from": source_id,
                        "finding_id": finding.node_id,
                        "severity": str(finding.meta.get("severity", "")),
                        "summary": str(finding.meta.get("summary", ""))[:500],
                    },
                )
                inherited["facts"] += 1
                _ = node
            inherited["sources"].append(source_id)
        if inherited["sources"]:
            ActivityLog(task_id).emit(
                "engine",
                "spawn",
                f"spawned from {','.join(inherited['sources'])}: "
                f"{inherited['scope']} scope, {inherited['facts']} findings inherited read-only",
            )
        summary["inherited"] = inherited
        return summary

    def list_tasks(self) -> list[dict]:
        """Fleet view: every task with live intent/fact/finding counters.

        Cross-task parity with the orchestration list_tasks tool: one
        call yields the operator view of the whole campaign without
        touching each task's store by hand.
        """
        from modules.lazy_loop import ExplorationGraph
        out: list[dict] = []
        for record in self.store.list():
            task_id = str(record.get("task_id", ""))
            try:
                overview = ExplorationGraph(task_id).overview()
            except Exception:
                overview = {}
            pending = [i for i in overview.get("intents", []) if i.get("state") in ("open", "pending", "running")]
            out.append(
                {
                    "task_id": task_id,
                    "goal": str(record.get("goal", ""))[:200],
                    "status": str(record.get("status", "")),
                    "updated": float(record.get("updated", 0.0) or 0.0),
                    "intents_pending": len(pending),
                    "facts": int(overview.get("facts", 0) or 0),
                    "findings": int(overview.get("findings", 0) or 0),
                }
            )
        return out

    def pause_task(self, task_id: str, reason: str = "operator") -> bool:
        """Pause another task from here (cross-task control)."""
        from modules.lazy_loop import ActivityLog, RuntimeTracker
        if self.store.get(task_id) is None:
            raise KeyError(f"unknown task: {task_id}")
        if not self.store.pause(task_id):
            return False
        RuntimeTracker(self.store).abort(task_id, "paused", reason)
        ActivityLog(task_id).emit("engine", "pause", f"paused: {reason}")
        self._sync_c2_board([task_id])
        return True

    def resume_task(self, task_id: str) -> bool:
        """Resume a paused task from here (cross-task control)."""
        from modules.lazy_loop import ActivityLog
        if self.store.get(task_id) is None:
            raise KeyError(f"unknown task: {task_id}")
        if not self.store.resume(task_id):
            return False
        ActivityLog(task_id).emit("engine", "resume", "resumed by operator")
        self._sync_c2_board([task_id])
        return True

    def delete_task(self, task_id: str) -> dict:
        """Delete a task record plus every store file scoped to it.

        Matches file names carrying the task id as a full token so
        ``t0001`` never sweeps files of ``t00010``.

        Args:
            task_id: Task to remove.

        Returns:
            Dict with deleted flag and removed file names.
        """
        from modules.lazy_loop import STORE_DIR
        task_id = (task_id or "").strip()
        if not task_id:
            raise ValueError("task_id is required")
        if self.store.get(task_id) is None:
            return {"deleted": False, "removed": []}
        self.store.delete(task_id)
        removed: list[str] = []
        token = re.compile(rf"(^|[_-]){re.escape(task_id)}([_-]|\.)")
        try:
            entries = list(STORE_DIR.iterdir())
        except OSError:
            entries = []
        for path in entries:
            if not path.is_file() or not token.search(path.name):
                continue
            try:
                path.unlink()
                removed.append(path.name)
            except OSError:
                continue
        return {"deleted": True, "removed": removed}

    def task_graph(self, task_id: str) -> dict:
        """Graph overview of another task (get_task_graph parity)."""
        from modules.lazy_loop import ExplorationGraph
        if self.store.get(task_id) is None:
            raise KeyError(f"unknown task: {task_id}")
        return ExplorationGraph(task_id).overview()

    def task_findings(self, task_id: str) -> list[dict]:
        """Findings of another task with severity, status and report size."""
        from modules.lazy_loop import ExplorationGraph
        if self.store.get(task_id) is None:
            raise KeyError(f"unknown task: {task_id}")
        rows = []
        for node in ExplorationGraph(task_id).list("finding"):
            meta = node.meta or {}
            rows.append(
                {
                    "id": node.node_id,
                    "text": node.text[:200],
                    "severity": str(meta.get("severity", "")),
                    "status": str(meta.get("status", "")),
                    "evidence_version": int(meta.get("evidence_version", 0) or 0),
                    "report_chars": len(str(meta.get("report", "") or "")),
                }
            )
        return rows

    def task_traces(self, task_id: str, query: str = "", limit: int = 50) -> list[dict]:
        """Worker traces of another task, keyword-filtered when asked."""
        from modules.lazy_loop import ActivityLog
        if self.store.get(task_id) is None:
            raise KeyError(f"unknown task: {task_id}")
        activity = ActivityLog(task_id)
        if (query or "").strip():
            return activity.search_all(query, limit=max(1, int(limit or 50)))
        return activity.read(max(1, int(limit or 50)))

    def task_node_detail(self, task_id: str, node_id: int) -> dict:
        """Full node view of another task (get_task_node_detail parity)."""
        from modules.lazy_loop import ExplorationGraph
        if self.store.get(task_id) is None:
            raise KeyError(f"unknown task: {task_id}")
        return ExplorationGraph(task_id).node_detail(int(node_id))

    def _archive_discards(self, task_id: str, last_results: list[dict]) -> None:
        """Persist abandoned-route reasons into the findings ledger.

        Args:
            task_id: Engagement identifier.
            last_results: Worker outcomes from the final round.
        """
        from modules.lazy_loop import ActivityLog, ExplorationGraph, resolve_target
        try:
            from modules import orchestrator_config
            from modules.sinks.findings import ingest_discarded

            if not bool(orchestrator_config.sinks().get("findings", True)):
                return
            graph = ExplorationGraph(task_id)
            entries: list[dict] = []
            for row in last_results[:50]:
                state = str(row.get("state", "unknown"))
                if state in ("done",):
                    continue
                node = graph.get(int(row.get("intent_id", 0) or 0))
                entries.append(
                    {
                        "reason": f"intent #{row.get('intent_id', '?')} {str(node.text if node else row.get('worker', 'unknown'))[:120]} ended {state}",
                        "command": "",
                        "output": "",
                        "engagement_id": task_id,
                        "target": resolve_target(task_id, self.store, graph) if self.store else "",
                    }
                )
            if entries:
                ingest_discarded(task_id, entries)
        except Exception as exc:
            ActivityLog(task_id).emit("engine", "handoff", f"discard archive failed: {str(exc)[:120]}")

    def set_concurrency(self, limit: int) -> int:
        """Cap concurrently running tasks; 0 disables admission control.

        Args:
            limit: Max running tasks.

        Returns:
            The stored cap.
        """
        self.max_concurrent = max(0, int(limit or 0))
        return self.max_concurrent

    def drain_queue(self, max_tasks: int = 3, deadline_near: bool = False) -> list[dict]:
        """Run queued tasks while the concurrency cap allows.

        Draining is FIFO by default. When ``loop_triage_enabled`` is set the
        difficulty-triage scheduler orders the queue easy-first (salvaging
        partials first near a deadline) and abandons targets that hit the
        stop-loss limit without progress.

        Args:
            max_tasks: Max queued tasks promoted in one pass.
            deadline_near: When True, the triage scheduler prioritises
                salvageable partials.

        Returns:
            Per-task run summaries.
        """
        from modules.lazy_loop import ActivityLog
        results: list[dict] = []
        args = dict(self._run_defaults or {})
        previous = self._in_drain
        self._in_drain = True

        def order(items: list) -> list:
            if self.triage_enabled and self.triage is not None:
                return self.triage.order(items, deadline_near=deadline_near)
            return items

        try:
            for _ in range(max(1, int(max_tasks))):
                cap = int(self.max_concurrent or 0)
                if cap > 0 and self.store.active_count() >= cap:
                    break
                record = self.store.dequeue_next(order=order)
                if record is None:
                    break
                task_id = str(record.get("task_id", ""))
                if self.triage_enabled and self.triage is not None and self.triage.should_stop(record):
                    self.store.set_status(task_id, "exhausted")
                    ActivityLog(task_id).emit("engine", "stop-loss", "abandoned: attempts exhausted without progress")
                    continue
                ActivityLog(task_id).emit("engine", "admission", "dequeued: running now")
                results.append(self.run(task_id, **args))
        finally:
            self._in_drain = previous
        return results

    def admission_check(self, task_id: str) -> dict:
        """Return whether a task may run now, queueing it when capped.

        Args:
            task_id: Task requesting a slot.

        Returns:
            Dict with admitted flag; queued tasks carry active/cap counts.
        """
        from modules.lazy_loop import ActivityLog
        cap = int(self.max_concurrent or 0)
        if cap <= 0:
            return {"admitted": True}
        active = self.store.active_count(exclude=task_id)
        if active < cap:
            return {"admitted": True, "active": active, "cap": cap}
        self.store.enqueue(task_id)
        ActivityLog(task_id).emit("engine", "admission", f"queued: {active}/{cap} task(s) running")
        return {"admitted": False, "queued": True, "active": active, "cap": cap}

    def _parts(self, task_id: str) -> tuple[ExplorationGraph, ActivityLog, TrafficLog, Guard]:
        """Build per-task collaborators."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph, Guard, TrafficLog
        graph = ExplorationGraph(task_id)
        return graph, ActivityLog(task_id), TrafficLog(task_id), Guard(task_id)

    def update_finding_report(self, task_id: str, finding_id: int, report: str) -> int:
        """Write the narrative report of another task's finding."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph, FindingService
        if self.store.get(task_id) is None:
            raise KeyError(f"unknown task: {task_id}")
        graph = ExplorationGraph(task_id)
        version = FindingService(task_id, graph, ActivityLog(task_id), self.store).update_report(
            int(finding_id), report
        )
        if version:
            self._sync_c2_board([task_id])
        return version

    def _sync_c2_board(self, task_ids: list[str] | None = None) -> None:
        """Mirror loop task states into the C2 Kanban board (best effort)."""
        try:
            from modules.lazy_bridge import push_tasks_to_c2

            push_tasks_to_c2(task_ids)
        except Exception:
            pass

