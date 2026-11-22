from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.lazy_loop import ExplorationGraph, ExplorationNode


class EngineReportingMixin:
    """Extracted LazyLoopEngine methods (verbatim lift + lazy imports).

    Each method injects its ``modules.lazy_loop`` module-level dependencies as a
    lazy import to avoid a circular import at load time. See
    modules/loop/README.md for the decomposition contract.
    """

    def export_task_traffic(self, task_id: str) -> dict:
        """Export the task's proxy exchanges next to its archive.

        Args:
            task_id: Task whose exchanges are exported.

        Returns:
            Export summary (``exported`` 0 when the task has no traffic).
        """
        from modules import lazy_proxy as _proxy
        from modules.lazy_loop import _store_path

        controller = _proxy.get_proxy()
        recorder = controller.recorder()
        if recorder is None:
            from modules.traffic_recorder import TrafficRecorder

            recorder = TrafficRecorder(controller.traffic_dir)
        try:
            rows = recorder.query(task=task_id, limit=1)
        except Exception:
            rows = []
        if not rows:
            return {"exported": 0, "bodies": 0, "path": ""}
        target = _store_path(f"traffic_{task_id}.zip")
        try:
            return recorder.export_archive(target, task=task_id)
        except Exception as exc:
            return {"exported": 0, "bodies": 0, "path": "", "error": str(exc)[:200]}

    def export_evidence(self, task_id: str, dest: str | Path | None = None) -> dict:
        """Freeze every task artefact into a hash-manifested zip package.

        The package is the audit hand-off: task registry, exploration
        graph (goals, intents, facts, findings), activity trace, tool
        traffic, rendered report and the per-task traffic archive. Each
        file's SHA-256 is recorded in ``manifest.json`` so a reviewer can
        prove the package was not altered after export.

        Args:
            task_id: Task whose artefacts are frozen.
            dest: Optional destination zip path; defaults to
                ``sessions/lazy/evidence_<task_id>.zip``.

        Returns:
            Dict with the package path and the number of frozen files.
        """
        import zipfile

        from modules.lazy_loop import _now, _store_path

        record = self.store.get(task_id) or {}
        candidates: list[tuple[str, Path]] = []
        for name in (
            "tasks.json",
            f"exp_{task_id}.json",
            f"activity_{task_id}.jsonl",
            f"traffic_{task_id}.jsonl",
            f"traffic_{task_id}.zip",
        ):
            path = _store_path(name)
            if path.exists():
                candidates.append((name, path))
        for pattern in (f"report_{task_id}*.md", f"report_{task_id}*.json", f"archive*{task_id}*"):
            for path in sorted(_store_path(".").glob(pattern)):
                if path.is_file() and (path.name, path) not in candidates:
                    candidates.append((path.name, path))
        target = Path(dest) if dest else _store_path(f"evidence_{task_id}.zip")
        target.parent.mkdir(parents=True, exist_ok=True)
        manifest = {
            "version": 1,
            "task_id": task_id,
            "created": _now(),
            "status": str(record.get("status", "")),
            "goal": str(record.get("goal", ""))[:500],
            "files": [],
        }
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, path in sorted(candidates):
                data = path.read_bytes()
                manifest["files"].append(
                    {
                        "name": name,
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "bytes": len(data),
                    }
                )
                archive.writestr(name, data)
            archive.writestr("manifest.json", json.dumps(manifest, indent=2))
        return {"task_id": task_id, "path": str(target), "files": len(manifest["files"])}

    def export_findings_report(self, task_id: str, path: str = "", fmt: str = "md") -> dict:
        """Render the severity-ranked report to Markdown, JSON or CSV.

        Args:
            task_id: Task to render.
            path: Destination file (defaults under the lazy store).
            fmt: ``md`` (default), ``json`` or ``csv``.

        Returns:
            Dict with path, findings count and format.
        """
        from modules.lazy_loop import (
            BASE_DIR,
            ActivityLog,
            ExplorationGraph,
            FindingService,
            _store_path,
            resolve_target,
        )
        fmt = (fmt or "md").lower()
        graph = ExplorationGraph(task_id)
        activity = ActivityLog(task_id)
        ranked = FindingService(task_id, graph, activity, self.store).ranked()
        status = self.status(task_id)
        if fmt == "json":
            body = json.dumps(
                {
                    "task": task_id,
                    "findings": [
                        {
                            "id": n.node_id,
                            "severity": n.meta.get("severity"),
                            "status": n.meta.get("status"),
                            "text": n.text,
                            "retest": (n.meta.get("retest") or {}).get("verdict"),
                        }
                        for n in ranked
                    ],
                    "overview": status["overview"],
                },
                indent=2,
                ensure_ascii=False,
            )
            ext = "json"
        elif fmt == "csv":
            import csv as _csv
            import io as _io

            buffer = _io.StringIO()
            writer = _csv.writer(buffer)
            writer.writerow(["id", "severity", "status", "name", "summary", "poc", "assets", "retest"])
            for node in ranked:
                writer.writerow(
                    [
                        node.node_id,
                        node.meta.get("severity", ""),
                        node.meta.get("status", ""),
                        str(node.meta.get("name", ""))[:200],
                        str(node.meta.get("summary", ""))[:500],
                        str(node.meta.get("poc", ""))[:500],
                        ",".join(str(a) for a in graph.anchors_for(node.node_id)),
                        (node.meta.get("retest") or {}).get("verdict", ""),
                    ]
                )
            body = buffer.getvalue()
            ext = "csv"
        else:
            lines: list[str] = [
                f"# Lazy report — {task_id}",
                f"- goal: {(status.get('task') or {}).get('goal', '')[:200]}",
                f"- findings: {len(ranked)}",
                "",
                "## Findings (critical first)",
                "",
            ]
            for node in ranked:
                verdict = (node.meta.get("retest") or {}).get("verdict", "pending")
                lines.append(
                    f"### [{str(node.meta.get('severity', 'info')).upper()}] {node.meta.get('name', node.text[:80])}"
                )
                lines.append(f"{node.meta.get('summary', node.text)[:400]}")
                if node.meta.get("poc"):
                    lines.append(f"PoC: {str(node.meta['poc'])[:500]}")
                lines.append(f"status={node.meta.get('status', 'pending')} retest={verdict}")
                lines.append("")
            cov = status.get("coverage", {})
            lines.append(f"coverage: {cov.get('tested', 0)}/{cov.get('total', 0)} ({cov.get('pct', 0)}%)")
            runtime = status.get("runtime", {}) or {}
            lines.append(
                f"runtime: status={runtime.get('status', '')} "
                f"abort={runtime.get('abort_cause', '')} "
                f"workers={runtime.get('workers', 0)}"
            )
            budget = status.get("budget", {}) or {}
            lines.append(f"budget: used={budget.get('used', {})} limits={budget.get('limits', {})}")
            lines.append(f"intercept pending: {status.get('intercept_pending', 0)} (lazy_guard pending|approve|deny)")
            body = "\n".join(lines)
            ext = "md"
        target = Path(path) if path else _store_path(f"report_{task_id}.{ext}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        activity.emit("reporter", "report-export", f"{fmt} -> {target}")
        try:
            from modules.outcome_bus import record_event

            report_target = resolve_target(task_id, self.store, graph)
            record_event(
                kind="report",
                target=report_target,
                host=report_target,
                task_id=task_id,
                title=f"findings report {task_id}",
                description=f"{len(ranked)} finding(s) exported as {fmt}",
                success=True,
                source="lazy_loop",
                artifacts=[str(target)],
                sinks=["event_bus"],
                metadata={"sessions_dir": str(BASE_DIR / "sessions")},
            )
        except Exception:
            pass
        return {"path": str(target), "findings": len(ranked), "format": fmt}

    def status(self, task_id: str) -> dict:
        """Return full inspectable state for one task."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph, InterceptQueue, TodoStore
        record = self.store.get(task_id) or {}
        graph = ExplorationGraph(task_id)
        activity = ActivityLog(task_id)
        return {
            "task": record,
            "overview": graph.overview(),
            "coverage": self.assets.coverage_for(graph, record.get("scope", [])),
            "todos": TodoStore(task_id).as_list(),
            "recent": activity.read(10),
            "runtime": self.runtime.heartbeat(task_id),
            "budget": {
                "limits": self.budget.limits(task_id),
                "used": self.budget.usage(task_id),
                "check": self.budget.check(task_id),
            },
            "intercept_pending": len(InterceptQueue(task_id).pending()),
        }

    def graph_overview(self, task_id: str) -> dict:
        """Return planner-facing overview plus coverage and scope.

        Findings ride along in full (they are the highest-value, lowest
        volume product) so every round sees every confirmed vuln without
        an extra list call; host lists stay collapsed to a count.
        """
        from modules.lazy_loop import EXPLORATION_TERMINAL_STATES, ActivityLog, ColdCompactor, ExplorationGraph
        record = self.store.get(task_id) or {}
        graph = ExplorationGraph(task_id)
        overview = graph.overview()
        overview["coverage"] = self.assets.coverage_for(graph, record.get("scope", []))
        overview["scope"] = record.get("scope", [])
        overview["constraints"] = record.get("constraints", [])
        overview["runtime"] = self.runtime.heartbeat(task_id)
        overview["budget"] = {"limits": self.budget.limits(task_id), "used": self.budget.usage(task_id)}
        overview["finding_list"] = self._finding_list(graph)
        done_intents = [n for n in graph.list("intent") if n.state in EXPLORATION_TERMINAL_STATES]
        done_intents.sort(key=lambda n: n.updated, reverse=True)
        overview["done_intents_total"] = len(done_intents)
        overview["recent_done_intents"] = [
            {"id": n.node_id, "state": n.state, "text": n.text[:300]} for n in done_intents[:15]
        ]
        try:
            digest_view = ColdCompactor(graph, ActivityLog(task_id)).digest_overview()
            overview["cold_digests"] = digest_view.get("cold_digests", [])
            overview["cold_index"] = digest_view.get("cold_index", [])
            overview["covered_members"] = digest_view.get("covered_members", {})
        except Exception:
            overview["cold_digests"] = []
            overview["cold_index"] = []
            overview["covered_members"] = {}
        return overview

    def _finding_list(self, graph: ExplorationGraph) -> list[dict]:
        """Full finding rows: severity-first, assets readable."""
        from modules.lazy_loop import SEV_RANK
        rows = []
        for node in sorted(
            graph.list("finding"), key=lambda n: (SEV_RANK.get(str(n.meta.get("severity", "")), 5), n.node_id)
        ):
            from_intent = 0
            for parent_id in graph.parents(node.node_id):
                parent = graph.get(parent_id)
                if parent is not None and parent.kind == "intent":
                    from_intent = parent.node_id
                    break
            assets = []
            for asset_id in graph.anchors_for(node.node_id):
                asset = self.assets.get(int(asset_id))
                assets.append(asset.value[:200] if asset is not None else "")
            rows.append(
                {
                    "id": node.node_id,
                    "summary": str(node.meta.get("summary", "") or node.text)[:300],
                    "severity": str(node.meta.get("severity", "")),
                    "status": str(node.meta.get("status", "")),
                    "evidence": str(node.meta.get("poc", ""))[:300],
                    "from_intent": from_intent,
                    "assets": [a for a in assets if a],
                }
            )
        return rows

    def loop_graph(self, task_id: str) -> dict:
        """Return task graphs as ForceGraph-ready nodes/links.

        Exploration nodes keep their kind/state/priority; asset nodes
        ride along with their kind/value; exploration edges keep their
        kind and anchors become ``anchors`` links. The Intel/attack
        ForceGraph views and the broadcast board consume this shape
        directly, so the operator sees the same topology the planner
        ranks on.

        Args:
            task_id: Task to export.

        Returns:
            Dict with ``nodes`` and ``links`` lists.
        """
        from modules.lazy_loop import ExplorationGraph
        graph = ExplorationGraph(task_id)
        degree: dict[int, int] = {}
        for edge in graph.edges:
            degree[edge.src] = degree.get(edge.src, 0) + 1
            degree[edge.dst] = degree.get(edge.dst, 0) + 1
        anchor_count: dict[int, int] = {}
        for entry in graph.anchors:
            try:
                anchor_count[int(entry.get("node_id", 0))] = anchor_count.get(int(entry.get("node_id", 0)), 0) + 1
            except (TypeError, ValueError):
                continue
        nodes = []
        for node in graph.list():
            score = degree.get(node.node_id, 0) + anchor_count.get(node.node_id, 0)
            nodes.append(
                {
                    "id": f"e{node.node_id}",
                    "node_id": node.node_id,
                    "label": f"#{node.node_id} {node.text[:80]}",
                    "type": node.kind,
                    "kind": node.kind,
                    "state": node.state,
                    "priority": node.priority,
                    "val": 1 + score,
                    "degree": degree.get(node.node_id, 0),
                }
            )
        for asset in self.assets.list():
            linked = sum(1 for entry in graph.anchors if int(entry.get("asset_id", 0) or 0) == asset.asset_id)
            nodes.append(
                {
                    "id": f"a{asset.asset_id}",
                    "asset_id": asset.asset_id,
                    "label": f"{asset.kind} {asset.value[:80]}",
                    "type": "asset",
                    "kind": asset.kind,
                    "state": "tested" if asset.tested else "untested",
                    "val": 1 + linked,
                    "degree": linked,
                }
            )
        links = []
        for edge in graph.edges:
            links.append({"source": f"e{edge.src}", "target": f"e{edge.dst}", "type": edge.kind})
        for entry in graph.anchors:
            try:
                links.append(
                    {"source": f"e{int(entry['node_id'])}", "target": f"a{int(entry['asset_id'])}", "type": "anchors"}
                )
            except (KeyError, TypeError, ValueError):
                continue
        return {"nodes": nodes, "links": links}

    def graph_context(self, task_id: str, top: int = 8) -> dict:
        """Rank exploration topology to steer planner actions.

        Hubs are the most connected exploration nodes (attention
        concentrates there); islands are assets no intent anchored yet;
        suggested orders untested scoped assets by anchor-degree so the
        planner probes the best-connected surface first instead of id
        order. Mirrors the ForceGraph hub/island lenses.

        Args:
            task_id: Task to analyse.
            top: Max entries per section.

        Returns:
            Dict with ``hubs``, ``islands``, ``suggested`` and ``stats``.
        """
        from modules.lazy_loop import EXPLORATION_ACTIVE_STATES, ExplorationGraph
        record = self.store.get(task_id) or {}
        scope = record.get("scope", []) or []
        graph = ExplorationGraph(task_id)
        degree: dict[int, int] = {}
        for edge in graph.edges:
            degree[edge.src] = degree.get(edge.src, 0) + 1
            degree[edge.dst] = degree.get(edge.dst, 0) + 1
        for entry in graph.anchors:
            try:
                nid = int(entry.get("node_id", 0))
                degree[nid] = degree.get(nid, 0) + 1
            except (TypeError, ValueError):
                continue
        ranked = sorted(graph.list(), key=lambda n: (-degree.get(n.node_id, 0), n.node_id))
        hubs = [
            {
                "id": n.node_id,
                "kind": n.kind,
                "state": n.state,
                "degree": degree.get(n.node_id, 0),
                "text": n.text[:160],
            }
            for n in ranked[: max(1, top)]
            if degree.get(n.node_id, 0)
        ]
        anchored_assets = set()
        for entry in graph.anchors:
            try:
                anchored_assets.add(int(entry.get("asset_id", 0)))
            except (TypeError, ValueError):
                continue
        scoped_assets = self.assets.scoped(scope) if scope else self.assets.list()
        islands = [
            {"id": a.asset_id, "kind": a.kind, "value": a.value[:160]}
            for a in scoped_assets
            if a.asset_id not in anchored_assets
        ][: max(1, top)]
        untested = self.assets.untested_for(graph, scope, limit=50)
        asset_heat: dict[int, int] = {}
        for node in graph.list("intent"):
            if node.state in EXPLORATION_ACTIVE_STATES:
                for asset_id in graph.anchors_for(node.node_id):
                    asset_heat[asset_id] = asset_heat.get(asset_id, 0) + 2
        for node in graph.list("finding"):
            for asset_id in graph.anchors_for(node.node_id):
                asset_heat[asset_id] = asset_heat.get(asset_id, 0) + 3
        untested.sort(key=lambda a: (-asset_heat.get(a.asset_id, 0), a.asset_id))
        suggested = [
            {"id": a.asset_id, "kind": a.kind, "value": a.value[:160], "heat": asset_heat.get(a.asset_id, 0)}
            for a in untested[: max(1, top)]
        ]
        return {
            "hubs": hubs,
            "islands": islands,
            "suggested": suggested,
            "stats": {
                "nodes": len(graph.nodes),
                "edges": len(graph.edges),
                "anchors": len(graph.anchors),
                "assets": len(scoped_assets),
                "untested": len(untested),
            },
        }

    def broadcast(
        self,
        task_id: str,
        kinds: list[str] | None = None,
        query: str = "",
        order: str = "desc",
        page: int = 1,
        per_page: int = 20,
        states: list[str] | None = None,
    ) -> dict:
        """Paginated exploration timeline like the lazy broadcast board.

        Each row carries its id, upstream/downstream neighbours and
        anchored assets inline so expansion needs no extra request.
        Search matches text, source and ``#id`` / plain-id forms.

        Args:
            task_id: Task to read.
            kinds: Node kinds to keep (empty means all).
            query: Keyword or ``#41`` / ``41`` node-id filter.
            order: ``desc`` (newest first, live position) or ``asc``.
            page: 1-based page number.
            per_page: Rows per page (1..100).
            states: Node states to keep (empty means all).

        Returns:
            Dict with items, total, page, per_page, has_more and days.
        """
        from modules.lazy_loop import ExplorationGraph
        graph = ExplorationGraph(task_id)
        wanted = {k.strip() for k in (kinds or []) if k.strip()}
        wanted_states = {s.strip() for s in (states or []) if s.strip()}
        needle = (query or "").strip().lower()
        wanted_id = 0
        id_search = ""
        if needle.startswith("#"):
            id_search = needle[1:].strip()
        elif needle.isdigit():
            id_search = needle
        if id_search.isdigit():
            wanted_id = int(id_search)
        nodes = list(graph.nodes.values())
        if wanted:
            nodes = [n for n in nodes if n.kind in wanted]
        if wanted_states:
            nodes = [n for n in nodes if n.state in wanted_states]
        if wanted_id:
            nodes = [n for n in nodes if n.node_id == wanted_id]
        elif needle:
            scored = []
            for node in nodes:
                hay = f"{node.text} {node.kind} {node.state} {json.dumps(node.meta, ensure_ascii=False)}".lower()
                if needle in hay:
                    scored.append(node)
            nodes = scored
        reverse = order != "asc"
        nodes.sort(key=lambda n: (n.created, n.node_id), reverse=reverse)
        total = len(nodes)
        per_page = max(1, min(100, int(per_page or 20)))
        page = max(1, int(page or 1))
        start = (page - 1) * per_page
        window = nodes[start : start + per_page]
        items = [self._broadcast_row(graph, n) for n in window]
        days: dict[str, int] = {}
        for item in items:
            days[item["day"]] = days.get(item["day"], 0) + 1
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "has_more": start + per_page < total,
            "order": "asc" if order == "asc" else "desc",
            "days": days,
        }

    def _broadcast_row(self, graph: ExplorationGraph, node: ExplorationNode) -> dict:
        """Build one self-contained broadcast row for a node."""
        meta = dict(node.meta or {})
        source = str(
            meta.get("source", "") or meta.get("confidence", "") or ("cold-digest" if meta.get("cold_digest") else "")
        )
        payload = str(meta.get("evidence", "") or meta.get("poc", "") or meta.get("summary", ""))[:200]
        upstream = []
        for parent_id in graph.parents(node.node_id):
            parent = graph.get(parent_id)
            if parent is None:
                continue
            upstream.append(
                {"id": parent.node_id, "kind": parent.kind, "state": parent.state, "text": parent.text[:160]}
            )
        downstream = []
        for child_id in graph.children(node.node_id):
            child = graph.get(child_id)
            if child is None:
                continue
            downstream.append({"id": child.node_id, "kind": child.kind, "state": child.state, "text": child.text[:160]})
        anchored = []
        for asset_id in graph.anchors_for(node.node_id):
            asset = self.assets.get(int(asset_id))
            if asset is None:
                anchored.append({"id": int(asset_id), "kind": "", "value": ""})
                continue
            anchored.append({"id": asset.asset_id, "kind": asset.kind, "value": asset.value[:200]})
        try:
            day = time.strftime("%Y-%m-%d", time.localtime(float(node.created or 0)))
        except (ValueError, OSError, OverflowError):
            day = ""
        return {
            "id": node.node_id,
            "kind": node.kind,
            "state": node.state,
            "text": node.text[:500],
            "priority": node.priority,
            "created": node.created,
            "updated": node.updated,
            "day": day,
            "source": source[:80],
            "payload": payload,
            "upstream": upstream,
            "downstream": downstream,
            "assets": anchored,
            "delete_reason": str(meta.get("delete_reason", ""))[:500],
        }

    def broadcast_events(self, task_id: str, cursor: int = 0, batch: int = 500) -> dict:
        """Return activity records after a line cursor (SSE resume parity).

        The cursor is a 0-based line index over the task activity JSONL,
        which only ever appends, so an SSE client that reconnects with
        ``id``/``cursor`` resumes exactly where it stopped.

        Args:
            task_id: Task whose activity stream is read.
            cursor: Line index to resume from (0 = beginning).
            batch: Maximum records returned per call.

        Returns:
            Dict with ``items``, the next ``cursor`` and current ``total``.
        """
        from modules.lazy_loop import _store_path
        path = _store_path(f"activity_{task_id}.jsonl")
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return {"items": [], "cursor": max(0, int(cursor or 0)), "total": 0}
        total = len(lines)
        start = max(0, int(cursor or 0))
        window = lines[start : start + max(1, min(2000, int(batch or 500)))]
        items: list[dict] = []
        for line in window:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict):
                items.append(record)
        return {"items": items, "cursor": start + len(window), "total": total}

