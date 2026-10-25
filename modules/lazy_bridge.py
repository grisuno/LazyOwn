"""Bidirectional LAZY <-> LazyOwn bridge.

LAZY runs standalone under sessions/lazy with its own tasks, assets,
experiment graphs, activity transcripts, traffic logs and guard audits.
This bridge syncs that universe with LazyOwn world_model, objectives,
evidence vault, traffic recorder, finding lifecycle and campaign DB in
both directions without touching LAZY runtime files.
"""

from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
LAZY_DIR = SESSIONS_DIR / "lazy"
SYNC_FILENAME = "lazy_bridge_sync.json"
C2_TASKS_FILENAME = "tasks.json"
C2_MAP_FILENAME = "lazy_bridge_c2_map.json"
C2_STATUS_MAP = {
    "queued": "New",
    "running": "Started",
    "paused": "Blocked",
    "done": "Done",
    "exhausted": "Review",
    "timeout": "Review",
    "failed": "Blocked",
}


def _data_dir() -> Path:
    """Resolve runtime data directory.

    Returns:
        LAZY_DIR holding tasks, assets and graphs.
    """
    return LAZY_DIR

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SERVICE_RE = re.compile(r"(\d+)/tcp\s+(\w+)\s+(\S+)\s+([^\n]*)")


def _read_json(path: Path, default):
    """Read json tolerating missing files.

    Args:
        path: File path.
        default: Default payload.

    Returns:
        Parsed payload or default.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default
    return data


def _read_jsonl(path: Path) -> list[dict]:
    """Read jsonl tolerating missing files.

    Args:
        path: File path.

    Returns:
        Row list.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            raw = json.loads(line)
        except ValueError:
            continue
        if isinstance(raw, dict):
            out.append(raw)
    return out


def lazy_tasks() -> dict:
    """Load LAZY task registry.

    Returns:
        Task map keyed by task id.
    """
    data = _read_json(_data_dir() / "tasks.json", {"tasks": {}})
    tasks = data.get("tasks", {}) if isinstance(data, dict) else {}
    return dict(tasks) if isinstance(tasks, dict) else {}


def lazy_assets() -> list[dict]:
    """Load LAZY asset nodes.

    Returns:
        Asset node list.
    """
    data = _read_json(_data_dir() / "assets.json", {"nodes": []})
    nodes = data.get("nodes", []) if isinstance(data, dict) else []
    return list(nodes) if isinstance(nodes, list) else []


def lazy_graph(task_id: str) -> dict:
    """Load experiment graph for a task.

    Args:
        task_id: LAZY task id.

    Returns:
        Graph dict with nodes, edges and anchors.
    """
    return _read_json(_data_dir() / f"exp_{task_id}.json",
                      {"nodes": [], "edges": [], "anchors": []})


def lazy_activity(task_id: str) -> list[dict]:
    """Load activity transcript for a task.

    Args:
        task_id: LAZY task id.

    Returns:
        Activity row list.
    """
    return _read_jsonl(_data_dir() / f"activity_{task_id}.jsonl")


def lazy_traffic(task_id: str) -> list[dict]:
    """Load traffic log for a task.

    Args:
        task_id: LAZY task id.

    Returns:
        Traffic row list.
    """
    return _read_jsonl(_data_dir() / f"traffic_{task_id}.jsonl")


def lazy_guard_audit(task_id: str) -> list[dict]:
    """Load guard audit for a task.

    Args:
        task_id: LAZY task id.

    Returns:
        Guard audit row list.
    """
    return _read_jsonl(_data_dir() / f"guard_audit_{task_id}.jsonl")


def bridge_status() -> dict:
    """Summarize LAZY universe and last sync cursor.

    Returns:
        Status dict with counts per task.
    """
    tasks = lazy_tasks()
    assets = lazy_assets()
    sync = _read_json(SESSIONS_DIR / SYNC_FILENAME, {})
    per_task = {}
    for task_id in tasks:
        per_task[task_id] = {"graph_nodes": len(lazy_graph(task_id).get("nodes", [])),
                             "activity": len(lazy_activity(task_id)),
                             "traffic": len(lazy_traffic(task_id)),
                             "guard": len(lazy_guard_audit(task_id)),
                             "status": tasks[task_id].get("status", "")}
    return {"lazy_dir": str(_data_dir()), "exists": _data_dir().exists(),
            "tasks": len(tasks), "assets": len(assets),
            "per_task": per_task, "last_sync": sync}


def _extract_hosts_from_graph(graph: dict) -> dict:
    """Derive host, service and vuln observations from graph facts.

    Args:
        graph: Experiment graph.

    Returns:
        Observation dict keyed by ip.
    """
    observations: dict[str, dict] = {}
    for node in graph.get("nodes", []):
        if not isinstance(node, dict):
            continue
        text = str(node.get("text", ""))
        for ip in IP_RE.findall(text):
            entry = observations.setdefault(ip, {"services": [], "facts": [], "open": False})
            entry["facts"].append(text[:1000])
            for match in SERVICE_RE.finditer(text):
                port, name, _state, _version = match.groups()
                if _state.lower() == "closed":
                    continue
                entry["services"].append({"port": port, "name": name})
                entry["open"] = True
    return observations


def pull_to_world_model() -> dict:
    """Sync LAZY graphs and assets into LazyOwn world model.

    Returns:
        Summary with hosts, services and facts synced.
    """
    from modules.world_model import get_world_model as _get_world_model

    tasks = lazy_tasks()
    assets = lazy_assets()
    hosts_synced: set[str] = set()
    services_synced = 0
    facts_synced = 0
    try:
        world = _get_world_model()
    except Exception:
        world = None
    for task_id in tasks:
        graph = lazy_graph(task_id)
        observations = _extract_hosts_from_graph(graph)
        for ip, observation in observations.items():
            hosts_synced.add(ip)
            facts_synced += len(observation["facts"])
            services_synced += len(observation["services"])
            if world is None:
                continue
            try:
                world.observe_host(ip, state="scanned")
                for service in observation["services"]:
                    world.observe_service(ip, service.get("name", ""),
                                          product="", version="",
                                          port=int(service.get("port", 0) or 0))
            except Exception:
                continue
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        if str(asset.get("kind")) == "ip":
            hosts_synced.add(str(asset.get("value", "")))
    summary = {"hosts": sorted(hosts_synced), "services": services_synced,
               "facts": facts_synced, "tasks": len(tasks), "assets": len(assets)}
    _record_sync("pull_world", summary)
    return summary


def pull_to_objectives() -> dict:
    """Inject open LAZY tasks as LazyOwn objectives without duplicates.

    Returns:
        Summary with injected count.
    """
    tasks = lazy_tasks()
    objectives_path = SESSIONS_DIR / "objectives.jsonl"
    try:
        existing = objectives_path.read_text(encoding="utf-8")
    except OSError:
        existing = ""
    injected = 0
    objectives_path.parent.mkdir(parents=True, exist_ok=True)
    with objectives_path.open("a", encoding="utf-8") as handle:
        for task_id, task in tasks.items():
            if not isinstance(task, dict):
                continue
            if str(task.get("status", "")) in ("done",):
                continue
            goal = str(task.get("goal", "")).strip()
            if not goal or goal in existing:
                continue
            record = {"id": f"lazy_{task_id}_{uuid.uuid4().hex[:6]}", "text": goal,
                      "priority": "high", "status": "pending", "source": f"lazy:{task_id}",
                      "context": {"lazy_task": task_id},
                      "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                      "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "notes": ""}
            handle.write(json.dumps(record) + "\n")
            injected += 1
    summary = {"injected": injected, "tasks": len(tasks)}
    _record_sync("pull_objectives", summary)
    return summary


def pull_findings_to_lifecycle() -> dict:
    """Confirm LAZY finding nodes in LazyOwn finding lifecycle.

    Returns:
        Summary with confirmed count.
    """
    from modules.finding_lifecycle import confirm as _confirm

    confirmed = 0
    for task_id in lazy_tasks():
        graph = lazy_graph(task_id)
        for node in graph.get("nodes", []):
            if not isinstance(node, dict):
                continue
            if str(node.get("kind")) != "finding":
                continue
            finding_id = f"lazy_{task_id}_{node.get('node_id', '')}"
            try:
                _confirm(finding_id, evidence=[str(node.get("text", ""))[:500]],
                         by=f"lazy:{task_id}")
                confirmed += 1
            except Exception:
                continue
    summary = {"confirmed": confirmed}
    _record_sync("pull_findings", summary)
    return summary


def _read_new_traffic(path: Path, offset: int) -> tuple[list[tuple[dict, int]], int]:
    """Read complete JSONL rows starting at a byte offset.

    Args:
        path: Traffic log file.
        offset: Last committed byte offset.

    Returns:
        Tuple of ``[(row, end_offset), ...]`` and the offset of the last
        complete line consumed. A partial trailing line is left for the
        next sync so a crashed writer cannot lose data.
    """
    try:
        if not path.is_file() or path.stat().st_size <= offset:
            return [], offset
        with path.open("rb") as handle:
            handle.seek(max(0, offset))
            chunk = handle.read()
    except OSError:
        return [], offset
    rows: list[tuple[dict, int]] = []
    line_start = max(0, offset)
    for line in chunk.splitlines(keepends=True):
        end = line_start + len(line)
        if not line.endswith(b"\n"):
            break
        try:
            raw = json.loads(line)
        except ValueError:
            line_start = end
            continue
        if isinstance(raw, dict):
            rows.append((raw, end))
        line_start = end
    return rows, line_start


def _notify(progress, text: str) -> None:
    """Call an optional progress callback without letting it break the sync."""
    if progress is None:
        return
    try:
        progress(text)
    except Exception:
        pass


def pull_traffic_to_recorder(progress=None) -> dict:
    """Mirror new LAZY traffic rows into the LazyOwn recorder index.

    The byte offset per task is persisted in ``lazy_bridge_sync.json`` so
    repeated syncs stay proportional to new activity instead of replaying
    the whole transcript (which used to stall the loop watchdog).

    Args:
        progress: Optional callback receiving short progress strings.

    Returns:
        Summary with mirrored count and byte offsets committed.
    """
    from modules.traffic_recorder import TrafficRecorder as _Recorder

    try:
        recorder = _Recorder(SESSIONS_DIR / "traffic")
    except Exception:
        return {"mirrored": 0, "error": "recorder unavailable"}
    state = _read_json(SESSIONS_DIR / SYNC_FILENAME, {})
    cursor = state.get("pull_traffic_offsets", {}) if isinstance(state, dict) else {}
    raw_offsets = cursor.get("summary", {}) if isinstance(cursor, dict) else {}
    offsets: dict[str, int] = {}
    if isinstance(raw_offsets, dict):
        for task_id, value in raw_offsets.items():
            try:
                offsets[str(task_id)] = max(0, int(value))
            except (TypeError, ValueError):
                continue
    tasks = lazy_tasks()
    mirrored = 0
    for task_id in tasks:
        path = _data_dir() / f"traffic_{task_id}.jsonl"
        start = offsets.get(task_id, 0)
        rows, next_offset = _read_new_traffic(path, start)
        if not rows:
            offsets[task_id] = next_offset
            continue
        _notify(progress, f"traffic {task_id}: {len(rows)} new row(s)")
        committed = start
        for row, end_offset in rows:
            command = str(row.get("command", ""))
            if not command:
                committed = end_offset
                continue
            output = str(row.get("output", ""))
            try:
                recorder.record(
                    "GET",
                    f"lazy://{task_id}/{mirrored}",
                    200,
                    command.encode()[:1000],
                    output.encode()[:4000],
                    task=task_id,
                )
            except Exception:
                break
            mirrored += 1
            committed = end_offset
            if mirrored % 50 == 0:
                _notify(progress, f"traffic mirrored={mirrored}")
        offsets[task_id] = committed
    summary = {"mirrored": mirrored}
    _record_sync("pull_traffic", summary)
    _record_sync("pull_traffic_offsets", offsets)
    return summary


def push_objective_to_lazy(goal: str, scope: list[str] | None = None) -> dict:
    """Export a LazyOwn objective as an LAZY-compatible task draft.

    Args:
        goal: Objective text.
        scope: Scope ip list.

    Returns:
        Draft task record written under sessions/lazy_drafts/.
    """
    drafts_dir = SESSIONS_DIR / "lazy_drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    task_id = f"t{uuid.uuid4().hex[:6]}"
    record = {"task_id": task_id, "goal": str(goal)[:500], "description": "",
              "status": "pending", "created": time.time(), "updated": time.time(),
              "constraints": [], "scope": [{"kind": "ip", "value": str(s),
                                            "reason": "lazyown push", "ts": time.time()}
                                           for s in (scope or [])][:10],
              "steer": {}, "killed": []}
    (drafts_dir / f"task_{task_id}.json").write_text(json.dumps(record, indent=2),
                                                     encoding="utf-8")
    _record_sync("push_task", {"task_id": task_id, "goal": goal})
    return record


def push_tasks_to_c2(only: list[str] | None = None) -> dict:
    """Mirror loop tasks into the lazyc2 Kanban board (sessions/tasks.json).

    One C2 card per loop task, upserted through a persisted id map so
    repeated syncs update the card instead of duplicating it. Statuses
    follow the C2 vocabulary (New/Started/Blocked/Review/Done).

    Args:
        only: Optional task id subset to sync.

    Returns:
        Dict with created/updated counts.
    """
    tasks = lazy_tasks()
    wanted = set(only or [])
    mapping = _read_json(SESSIONS_DIR / C2_MAP_FILENAME, {})
    if not isinstance(mapping, dict):
        mapping = {}
    board_path = SESSIONS_DIR / C2_TASKS_FILENAME
    board = _read_json(board_path, [])
    if not isinstance(board, list):
        board = []
    by_id = {int(card.get("id", 0)): card for card in board if isinstance(card, dict)}
    created = 0
    updated = 0
    for task_id in sorted(tasks):
        if wanted and task_id not in wanted:
            continue
        record = tasks[task_id] or {}
        try:
            c2_id = int(mapping.get(task_id, 0) or 0)
        except (TypeError, ValueError):
            c2_id = 0
        if c2_id <= 0:
            existing = [int(v or 0) for v in mapping.values()]
            c2_id = max([900000, *existing, *by_id.keys()]) + 1
            mapping[task_id] = c2_id
        status = C2_STATUS_MAP.get(str(record.get("status", "")).lower(), "New")
        title = f"[loop {task_id}] {str(record.get('goal', ''))[:120]}"
        description = (f"Autonomous loop task {task_id}\n\n"
                       f"Goal: {record.get('goal', '')}\n"
                       f"Status: {record.get('status', '')}\n"
                       f"Updated: {record.get('updated', '')}")
        card = by_id.get(c2_id)
        if card is None:
            by_id[c2_id] = {"id": c2_id, "title": title, "description": description,
                            "operator": "lazy_loop", "status": status}
            created += 1
        else:
            card["title"] = title
            card["description"] = description
            card["status"] = status
            updated += 1
    try:
        board_path.parent.mkdir(parents=True, exist_ok=True)
        board_path.write_text(json.dumps(list(by_id.values()), indent=2),
                              encoding="utf-8")
        (SESSIONS_DIR / C2_MAP_FILENAME).write_text(json.dumps(mapping, indent=2),
                                                    encoding="utf-8")
    except OSError:
        return {"created": 0, "updated": 0, "error": "board unwritable"}
    _record_sync("c2_tasks", {"created": created, "updated": updated})
    return {"created": created, "updated": updated}


def sync_all(progress=None) -> dict:
    """Run full bidirectional pull plus lifecycle, traffic and board mirror.

    Args:
        progress: Optional callback receiving one short string before each
            stage and during traffic mirroring so the loop watchdog sees
            progress on large stores.

    Returns:
        Combined sync summary.
    """
    _notify(progress, "sync: world model")
    world = pull_to_world_model()
    _notify(progress, "sync: objectives")
    objectives = pull_to_objectives()
    _notify(progress, "sync: findings")
    findings = pull_findings_to_lifecycle()
    _notify(progress, "sync: traffic")
    traffic = pull_traffic_to_recorder(progress=progress)
    _notify(progress, "sync: c2 board")
    c2_tasks = push_tasks_to_c2()
    _notify(progress, "sync: done")
    return {"world": world, "objectives": objectives,
            "findings": findings, "traffic": traffic, "c2_tasks": c2_tasks}


def _record_sync(action: str, summary: dict) -> None:
    """Record sync cursor best effort.

    Args:
        action: Sync action name.
        summary: Action summary.
    """
    try:
        current = _read_json(SESSIONS_DIR / SYNC_FILENAME, {})
        current[action] = {"at": time.time(), "summary": summary}
        (SESSIONS_DIR / SYNC_FILENAME).write_text(json.dumps(current, indent=2),
                                                  encoding="utf-8")
    except OSError:
        pass


__all__ = [
    "lazy_tasks", "lazy_assets", "lazy_graph", "lazy_activity",
    "lazy_traffic", "lazy_guard_audit", "bridge_status",
    "pull_to_world_model", "pull_to_objectives", "pull_findings_to_lifecycle",
    "pull_traffic_to_recorder", "push_objective_to_lazy", "push_tasks_to_c2",
    "sync_all",
]
