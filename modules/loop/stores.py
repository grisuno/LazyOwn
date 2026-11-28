"""Task stores and operator notification for the LazyOwn loop.

One contract per family, extracted from the ``modules/lazy_loop`` god
module: the task registry (``TaskStore``), the goal-breakdown stores
(``TodoStore`` / ``TaskTemplate`` / ``TaskCategory``), the operator
interaction queues (``InterceptQueue`` / ``CompanyScope``), the tool
favourites registry (``ToolCatalog``) and the finding event fan-out
(``Notifier``).

The private store helpers (``_store_path``, ``_load_json``, ...) resolve
through :mod:`modules.lazy_loop` at call time so the loop's test seams
(monkeypatched ``STORE_DIR`` / ``_store_path``) keep working verbatim.
"""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import asdict, dataclass, field
from pathlib import Path

from modules.loop.channel_secrets import _decrypt_channel_secret, _encrypt_channel_secret

_LOG = logging.getLogger("modules.lazy_loop")
INTERCEPT_TIMEOUT_SEC = 30.0
SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4, "": 5}
TASK_STATUSES = ("queued", "running", "paused", "done", "failed", "timeout", "exhausted", "handoff")
CONSTRAINT_TYPES = ("allow", "deny")
CONSTRAINT_SCOPES = ("planner", "worker", "both")


def _now() -> float:
    from modules.lazy_loop import _now as _impl

    return _impl()


def _store_path(name: str) -> Path:
    from modules.lazy_loop import _store_path as _impl

    return _impl(name)


def _load_json(path: Path, default: dict) -> dict:
    from modules.lazy_loop import _load_json as _impl

    return _impl(path, default)


def _save_json(path: Path, payload: dict) -> None:
    from modules.lazy_loop import _save_json as _impl

    _impl(path, payload)


def _restrict_file(path: Path) -> None:
    from modules.lazy_loop import _restrict_file as _impl

    _impl(path)


@dataclass
class LazyTask:
    """Lifecycle record for one autonomous engagement."""

    task_id: str
    goal: str
    description: str = ""
    status: str = "running"
    created: float = field(default_factory=_now)
    updated: float = field(default_factory=_now)


class TodoStore:
    """Per-task shared planner scratchpad for serial exploit chains."""

    def __init__(self, task_id: str) -> None:
        """Load persisted todos."""
        self.task_id = task_id
        self._path = _store_path(f"todos_{task_id}.json")
        raw = _load_json(self._path, {"items": []})
        self.items: list[dict] = raw.get("items", [])

    def _persist(self) -> None:
        """Persist todo list."""
        _save_json(self._path, {"items": self.items})

    def add(self, text: str) -> dict:
        """Append a serial step and return it."""
        item = {"id": len(self.items) + 1, "text": text.strip(), "state": "pending", "ts": _now()}
        self.items.append(item)
        self._persist()
        return item

    def complete(self, item_id: int) -> bool:
        """Mark step done."""
        for item in self.items:
            if int(item.get("id", 0)) == int(item_id):
                item["state"] = "done"
                self._persist()
                return True
        return False

    def next_pending(self) -> dict | None:
        """Return first pending step."""
        for item in self.items:
            if item.get("state") == "pending":
                return item
        return None

    def as_list(self) -> list[dict]:
        """Return all steps."""
        return list(self.items)


class TaskStore:
    """Registry of tasks, goals, constraints, hints, scope, findings."""

    def __init__(self) -> None:
        """Load task registry."""
        self._path = _store_path("tasks.json")
        self._raw = _load_json(self._path, {"seq": 0, "tasks": {}})

    def _persist(self) -> None:
        """Persist registry."""
        _save_json(self._path, self._raw)

    def create(self, goal: str, description: str = "") -> LazyTask:
        """Create task record and return it."""
        seq = int(self._raw.get("seq", 0)) + 1
        self._raw["seq"] = seq
        task_id = f"t{seq:04d}"
        task = LazyTask(task_id=task_id, goal=goal.strip(), description=description.strip())
        tasks = self._raw.setdefault("tasks", {})
        tasks[task_id] = {**asdict(task), "constraints": [], "scope": [], "steer": {}, "killed": []}
        self._persist()
        return task

    def get(self, task_id: str) -> dict | None:
        """Return raw task record or None."""
        return self._raw.get("tasks", {}).get(task_id)

    def list(self) -> list[dict]:
        """Return all task records."""
        return sorted(self._raw.get("tasks", {}).values(), key=lambda t: t.get("task_id", ""))

    def set_status(self, task_id: str, status: str) -> bool:
        """Update task status through the transition FSM."""
        from modules.loop.task_fsm import InvalidTaskTransition, require_transition

        record = self.get(task_id)
        if record is None:
            return False
        if status not in TASK_STATUSES:
            raise ValueError(f"unknown status: {status}")
        current = str(record.get("status", "running"))
        try:
            require_transition(current, status)
        except InvalidTaskTransition:
            raise
        record["status"] = status
        record["updated"] = _now()
        self._persist()
        return True

    def pause(self, task_id: str) -> bool:
        """Pause planner and workers like the planner Engine.Pause."""
        from modules.loop.task_fsm import InvalidTaskTransition

        try:
            return self.set_status(task_id, "paused")
        except InvalidTaskTransition:
            return False

    def resume(self, task_id: str) -> bool:
        """Resume a paused task back to running like the planner resumeTask."""
        record = self.get(task_id)
        if record is None:
            return False
        if record.get("status") not in ("paused", "queued", "exhausted"):
            return True
        return self.set_status(task_id, "running")

    def delete(self, task_id: str) -> bool:
        """Remove task record; per-task graph files are cleaned by caller."""
        tasks = self._raw.get("tasks", {})
        if task_id not in tasks:
            return False
        del tasks[task_id]
        self._persist()
        return True

    def active_count(self, exclude: str = "") -> int:
        """Return how many tasks are currently running."""
        return sum(1 for task in self.list() if task.get("status") == "running" and task.get("task_id") != exclude)

    def queue(self) -> list[dict]:
        """Return queued tasks in FIFO arrival order."""
        items = [task for task in self.list() if task.get("status") == "queued"]
        return sorted(items, key=lambda task: (float(task.get("queued_at", 0.0) or 0.0), str(task.get("task_id", ""))))

    def enqueue(self, task_id: str) -> bool:
        """Mark a task queued with its arrival stamp."""
        from modules.loop.task_fsm import InvalidTaskTransition

        record = self.get(task_id)
        if record is None:
            return False
        record["queued_at"] = _now()
        try:
            return self.set_status(task_id, "queued")
        except InvalidTaskTransition:
            return False

    def dequeue_next(self, order=None) -> dict | None:
        """Pop one queued task, mark it running and return it.

        Args:
            order: Optional callable taking the FIFO-ordered queue and
                returning it reordered; the first element is dequeued. When
                None the oldest queued task is popped (FIFO).

        Returns:
            The dequeued task record, or None when the queue is empty.

        Raises:
            InvalidTaskTransition: When the stored status drifted away
                from the queued state between listing and dequeuing.
        """
        items = self.queue()
        if not items:
            return None
        if order is not None:
            try:
                reordered = list(order(items))
                if reordered:
                    items = reordered
            except Exception:
                _LOG.debug("queue order callback failed, keeping FIFO order")
        record = items[0]
        self.set_status(record["task_id"], "running")
        record["status"] = "running"
        record["updated"] = _now()
        self._persist()
        return record

    def _refresh(self) -> None:
        """Reload the registry so concurrent store instances stay coherent."""
        self._raw = _load_json(self._path, {"seq": 0, "tasks": {}})

    def set_llm_chain(self, task_id: str, members: list[dict], active: int = 0) -> dict:
        """Bind a per-task LLM chain with a failover cursor.

        Args:
            task_id: Task to bind.
            members: Chain specs (name/model/priority dicts).
            active: Starting member index.

        Returns:
            Persisted chain state.

        Raises:
            KeyError: Unknown task.
        """
        self._refresh()
        record = self.get(task_id)
        if record is None:
            raise KeyError(f"unknown task: {task_id}")
        state = {
            "members": [dict(member) for member in members],
            "active": max(0, int(active)),
            "revision": int((record.get("llm") or {}).get("revision", 0)) + 1,
        }
        record["llm"] = state
        record["updated"] = _now()
        self._persist()
        return dict(state)

    def llm_state(self, task_id: str) -> dict:
        """Return the task LLM chain state (empty when unbound)."""
        self._refresh()
        record = self.get(task_id) or {}
        return dict(record.get("llm") or {})

    def advance_llm(self, task_id: str) -> dict:
        """Advance the per-task active member after quota exhaustion.

        Args:
            task_id: Task whose chain rotates.

        Returns:
            Updated chain state (empty when unbound).
        """
        self._refresh()
        state = self.llm_state(task_id)
        members = state.get("members") or []
        if not members:
            return {}
        state["active"] = (int(state.get("active", 0)) + 1) % len(members)
        state["revision"] = int(state.get("revision", 1)) + 1
        record = self.get(task_id)
        if record is None:
            return {}
        record["llm"] = state
        record["updated"] = _now()
        self._persist()
        return dict(state)

    def set_skills(self, task_id: str, names: list[str], auto: bool | None = None) -> dict:
        """Pin skills for prompt injection and optionally toggle auto-match.

        Args:
            task_id: Task to update.
            names: Skill names pinned on the record.
            auto: Optional new value for keyword auto-matching.

        Returns:
            Dict with the pinned skills and auto flag.

        Raises:
            KeyError: Unknown task.
        """
        self._refresh()
        record = self.get(task_id)
        if record is None:
            raise KeyError(f"unknown task: {task_id}")
        record["skills"] = [str(name)[:120] for name in names]
        if auto is not None:
            record["skills_auto"] = bool(auto)
        record["updated"] = _now()
        self._persist()
        return {"skills": list(record["skills"]), "skills_auto": bool(record.get("skills_auto", True))}

    def set_deadline(self, task_id: str, timeout_sec: float) -> bool:
        """Stamp absolute deadline like the planner deadline coordinator."""
        record = self.get(task_id)
        if record is None:
            return False
        record["deadline"] = _now() + max(0.0, float(timeout_sec)) if timeout_sec else 0.0
        record["updated"] = _now()
        self._persist()
        return True

    def expired(self, task_id: str) -> bool:
        """Report whether task deadline passed."""
        record = self.get(task_id) or {}
        deadline = float(record.get("deadline", 0.0) or 0.0)
        return bool(deadline) and _now() >= deadline

    def add_constraint(self, task_id: str, ctype: str, text: str, scope: str = "both") -> dict:
        """Register allow/deny operation constraint like the planner set_constraints.

        Scope selects where the constraint injects: planner, worker or
        both (default). Reads take effect immediately each round.
        """
        if ctype not in CONSTRAINT_TYPES:
            raise ValueError(f"type must be one of {CONSTRAINT_TYPES}")
        if scope not in CONSTRAINT_SCOPES:
            raise ValueError(f"scope must be one of {CONSTRAINT_SCOPES}")
        record = self.get(task_id)
        if record is None:
            raise KeyError(f"unknown task: {task_id}")
        item = {"type": ctype, "text": text.strip(), "scope": scope, "ts": _now()}
        record.setdefault("constraints", []).append(item)
        record["updated"] = _now()
        self._persist()
        return item

    def add_scope(self, task_id: str, kind: str, value: str, reason: str = "") -> dict:
        """Register authorized asset scope like the planner add_task_scope."""
        record = self.get(task_id)
        if record is None:
            raise KeyError(f"unknown task: {task_id}")
        item = {"kind": kind.strip(), "value": value.strip(), "reason": reason.strip(), "ts": _now()}
        record.setdefault("scope", []).append(item)
        record["updated"] = _now()
        self._persist()
        return item

    def steer(self, task_id: str, intent_id: int, message: str) -> bool:
        """Attach mid-run correction to a running intent like steer_work."""
        record = self.get(task_id)
        if record is None:
            return False
        record.setdefault("steer", {})[str(int(intent_id))] = {"msg": message, "ts": _now()}
        self._persist()
        return True

    def kill(self, task_id: str, intent_id: int) -> bool:
        """Flag a running intent for termination like kill_work."""
        record = self.get(task_id)
        if record is None:
            return False
        killed = record.setdefault("killed", [])
        if int(intent_id) not in killed:
            killed.append(int(intent_id))
        self._persist()
        return True

    def steer_for(self, task_id: str, intent_id: int) -> str:
        """Return pending steer message for intent if any."""
        record = self.get(task_id) or {}
        return str((record.get("steer", {}).get(str(int(intent_id)), {}) or {}).get("msg", ""))

    def clear_steer(self, task_id: str, intent_id: int) -> bool:
        """Drop the pending steer message for an intent after delivery."""
        record = self.get(task_id)
        if record is None:
            return False
        steer = record.get("steer", {}) or {}
        key = str(int(intent_id))
        if key in steer:
            steer.pop(key, None)
            self._persist()
            return True
        return False

    def killed(self, task_id: str, intent_id: int) -> bool:
        """Report whether intent was flagged for termination."""
        record = self.get(task_id) or {}
        return int(intent_id) in (record.get("killed", []) or [])


class TaskTemplate:
    """Named goal templates like task_templates: list/add/use/remove."""

    def __init__(self) -> None:
        """Bind template table."""
        self._path = _store_path("task_templates.json")

    def _load(self) -> dict:
        """Load template payload."""
        return _load_json(self._path, {"items": []})

    def list(self) -> list[dict]:
        """Return all templates."""
        return list(self._load().get("items", []))

    def add(self, name: str, goal: str) -> dict:
        """Register a template; names are unique (overwrite on clash)."""
        payload = self._load()
        items = [i for i in payload.get("items", []) if i.get("name") != name]
        item = {"name": name[:120], "goal": goal[:500], "ts": _now()}
        items.append(item)
        payload["items"] = items
        _save_json(self._path, payload)
        return item

    def remove(self, name: str) -> bool:
        """Delete a template by name."""
        payload = self._load()
        before = len(payload.get("items", []))
        payload["items"] = [i for i in payload["items"] if i.get("name") != name]
        if len(payload["items"]) != before:
            _save_json(self._path, payload)
            return True
        return False

    def get(self, name: str) -> dict | None:
        """Return one template by name or None."""
        for item in self.list():
            if item.get("name") == name:
                return item
        return None


class TaskCategory:
    """Per-task labels like task_categories: set/list."""

    def __init__(self, store=None) -> None:
        """Bind optional task store."""
        self._store = store
        self._path = _store_path("task_categories.json")

    def set(self, task_id: str, category: str) -> dict:
        """Label a task; returns the mapping."""
        payload = _load_json(self._path, {"map": {}})
        payload.setdefault("map", {})[task_id] = category[:80]
        _save_json(self._path, payload)
        return {"task_id": task_id, "category": category[:80]}

    def get(self, task_id: str) -> str:
        """Return the category for a task or empty string."""
        return str(_load_json(self._path, {"map": {}}).get("map", {}).get(task_id, ""))

    def list(self, category: str = "") -> list[dict]:
        """Return task->category rows, optionally filtered."""
        rows = [{"task_id": k, "category": v} for k, v in _load_json(self._path, {"map": {}}).get("map", {}).items()]
        if category:
            rows = [r for r in rows if r["category"] == category]
        return sorted(rows, key=lambda r: r["task_id"])


class CompanyScope:
    """Company asset-range registry like db/companies + company_scope."""

    def __init__(self) -> None:
        """Load company table."""
        self._path = _store_path("companies.json")

    def _load(self) -> dict:
        """Load company payload."""
        return _load_json(self._path, {"seq": 0, "items": []})

    def add(self, name: str, scope: str = "") -> dict:
        """Register a company with an optional scope pattern."""
        payload = self._load()
        payload["seq"] = int(payload.get("seq", 0)) + 1
        item = {"id": payload["seq"], "name": name[:200], "scope": (scope or "")[:300], "ts": _now()}
        payload.setdefault("items", []).append(item)
        _save_json(self._path, payload)
        return item

    def list(self) -> list[dict]:
        """Return companies with asset counts."""
        return list(self._load().get("items", []))

    def match(self, value: str) -> list[dict]:
        """Return companies whose scope substring hits the value."""
        lowered = (value or "").lower()
        return [c for c in self.list() if c.get("scope") and c["scope"].lower() in lowered]


class ToolCatalog:
    """Per-agent tool bindings like agent/toolcatalog (DB-overridable)."""

    def __init__(self) -> None:
        """Load binding table."""
        self._path = _store_path("tool_catalog.json")

    def _load(self) -> dict:
        """Load catalog payload."""
        return _load_json(
            self._path,
            {
                "bindings": {
                    "planner": ["graph", "facts", "findings", "node", "intent", "goal"],
                    "worker": ["bash", "fact", "finding", "trace", "node"],
                    "reporter": ["finding", "traffic", "evidence"],
                }
            },
        )

    def bindings(self, agent: str = "") -> dict:
        """Return bindings for one agent or the whole table."""
        table = self._load().get("bindings", {})
        return {agent: table.get(agent, [])} if agent else dict(table)

    def bind(self, agent: str, tool: str) -> list[str]:
        """Opt a tool into an agent lane."""
        payload = self._load()
        tools = payload.setdefault("bindings", {}).setdefault(agent, [])
        if tool not in tools:
            tools.append(tool)
        _save_json(self._path, payload)
        return list(tools)

    def unbind(self, agent: str, tool: str) -> list[str]:
        """Remove a tool from an agent lane."""
        payload = self._load()
        tools = payload.setdefault("bindings", {}).setdefault(agent, [])
        if tool in tools:
            tools.remove(tool)
        _save_json(self._path, payload)
        return list(tools)


class InterceptQueue:
    """Pending ask-queue with decide + timeout, priority ordered."""

    _EVENTS: dict[str, threading.Event] = {}
    _EVENTS_LOCK = threading.Lock()

    @classmethod
    def _event_for(cls, path: str, item_id: int) -> threading.Event:
        """Process-wide decision event for one pending intercept row.

        Approvals may be decided from a different queue instance (the
        operator command or the monitor TUI) than the worker thread that
        waits; keying by store path plus row id lets both sides meet on
        the same event.
        """
        key = f"{path}:{int(item_id)}"
        with cls._EVENTS_LOCK:
            event = cls._EVENTS.get(key)
            if event is None:
                event = threading.Event()
                cls._EVENTS[key] = event
            return event

    @classmethod
    def _drop_event(cls, path: str, item_id: int) -> None:
        """Forget a settled row's wake-up event."""
        with cls._EVENTS_LOCK:
            cls._EVENTS.pop(f"{path}:{int(item_id)}", None)

    def __init__(self, task_id: str = "") -> None:
        """Bind queue to task."""
        self.task_id = task_id
        suffix = f"_{task_id}" if task_id else ""
        self._path = _store_path(f"intercept{suffix}.json")

    def _load(self) -> dict:
        """Load queue payload."""
        return _load_json(self._path, {"seq": 0, "items": []})

    def _save(self, payload: dict) -> None:
        """Persist queue payload."""
        _save_json(self._path, payload)

    def request(self, tool: str, command: str, reason: str = "", tool_use_id: str = "") -> dict:
        """Enqueue one ask decision and return pending entry."""
        payload = self._load()
        seq = int(payload.get("seq", 0)) + 1
        payload["seq"] = seq
        item = {
            "id": seq,
            "tool": tool,
            "command": command[:2000],
            "reason": reason[:500],
            "state": "pending",
            "ts": _now(),
            "tool_use_id": str(tool_use_id or "")[:32],
        }
        payload.setdefault("items", []).append(item)
        self._save(payload)
        return item

    def pending(self) -> list[dict]:
        """Return pending entries ordered by id."""
        return sorted([i for i in self._load().get("items", []) if i.get("state") == "pending"], key=lambda i: i["id"])

    def history(self, page: int = 1, per_page: int = 20, states: list[str] | None = None, query: str = "") -> dict:
        """Paginated intercept history; pending stays fully visible.

        Pending requests are never hidden by history pagination: the
        response always carries the full pending list alongside the
        requested history page (lazy 0.3.12 #133 parity). History rows
        filter by decision state and keyword (lazy #139 parity).

        Args:
            page: 1-based history page number.
            per_page: History rows per page (1..100).
            states: Decision states to keep (empty means all).
            query: Keyword over tool/command/reason/tool_use_id.

        Returns:
            Dict with history items, total, page, per_page, has_more
            plus the complete pending list and its count.
        """
        payload = self._load()
        items = list(payload.get("items", []))
        pending = sorted([i for i in items if i.get("state") == "pending"], key=lambda i: i["id"])
        wanted = {s.strip() for s in (states or []) if s.strip()}
        history = [i for i in items if i.get("state") != "pending"]
        if wanted:
            history = [i for i in history if str(i.get("state", "")) in wanted]
        needle = (query or "").strip().lower()
        if needle:
            scored = []
            for item in history:
                hay = (
                    f"{item.get('tool', '')} {item.get('command', '')} "
                    f"{item.get('reason', '')} {item.get('tool_use_id', '')}"
                ).lower()
                if needle in hay:
                    scored.append(item)
            history = scored
        history.sort(key=lambda i: int(i.get("id", 0)), reverse=True)
        total = len(history)
        per_page = max(1, min(100, int(per_page or 20)))
        page = max(1, int(page or 1))
        start = (page - 1) * per_page
        window = history[start : start + per_page]
        return {
            "items": window,
            "total": total,
            "page": page,
            "per_page": per_page,
            "has_more": start + per_page < total,
            "pending": pending,
            "pending_count": len(pending),
        }

    def decide(self, item_id: int, verdict: str) -> bool:
        """Approve or deny one pending entry and wake its waiter."""
        if verdict not in ("approved", "denied"):
            raise ValueError("verdict must be approved|denied")
        payload = self._load()
        for item in payload.get("items", []):
            if int(item.get("id", 0)) == int(item_id) and item.get("state") == "pending":
                item["state"] = verdict
                item["decided"] = _now()
                self._save(payload)
                self._event_for(str(self._path), item_id).set()
                return True
        return False

    def wait(self, item_id: int, timeout_sec: float = INTERCEPT_TIMEOUT_SEC) -> str:
        """Block until decided or timeout; timeout denies safely.

        In-process decisions wake the waiter immediately through the
        shared event registry; a 0.2 s file poll stays as the fallback
        for decisions made by another process (monitor TUI, second
        shell), which cannot signal this process's events.
        """
        event = self._event_for(str(self._path), item_id)
        deadline = _now() + max(0.0, float(timeout_sec))
        while _now() < deadline:
            for item in self._load().get("items", []):
                if int(item.get("id", 0)) == int(item_id):
                    if item.get("state") in ("approved", "denied"):
                        self._drop_event(str(self._path), item_id)
                        return str(item["state"])
            event.wait(timeout=min(0.2, max(0.0, deadline - _now())))
        payload = self._load()
        for item in payload.get("items", []):
            if int(item.get("id", 0)) == int(item_id) and item.get("state") == "pending":
                item["state"] = "denied"
                item["decided"] = _now()
                item["reason"] = (item.get("reason", "") + " [timeout->deny]")[:500]
                self._save(payload)
                break
        self._drop_event(str(self._path), item_id)
        return "denied"


class Notifier:
    """Finding event fan-out like notify/ (log + webhook, stateless)."""

    def __init__(self, store=None) -> None:
        """Bind optional channel config from task store."""
        self._store = store

    def channels(self) -> list[dict]:
        """Return configured channels (empty = log only)."""
        try:
            raw = _load_json(_store_path("notify_channels.json"), {"channels": []})
            return list(raw.get("channels", []))
        except Exception:
            return []

    def add_channel(self, kind: str, target: str, min_severity: str = "", extra: dict | None = None) -> dict:
        """Register a channel: log|webhook|file|slack|email with severity floor.

        Args:
            kind: Channel type.
            target: URL, file path, ``smtp-host:port`` or log label.
            min_severity: Skip events below this severity.
            extra: Optional email/slack fields (to, from_addr, user,
                password, tls).

        Returns:
            Stored channel dict.

        Raises:
            ValueError: Unknown channel kind.
        """
        if kind not in ("log", "webhook", "file", "slack", "email"):
            raise ValueError("kind must be log|webhook|file|slack|email")
        if kind in ("webhook", "slack"):
            try:
                from modules.notify import url_allowed as _allowed

                ok, _reason = _allowed(str(target or ""))
                if not ok:
                    raise ValueError(f"webhook target denied: {_reason}")
            except ValueError:
                raise
            except Exception:
                pass
        if kind == "email":
            _target = str(target or "")
            _host = _target.rpartition(":")[0] or _target
            if not _host or len(_host) > 253 or any(ch.isspace() for ch in _host):
                raise ValueError("invalid smtp target")
        payload = _load_json(_store_path("notify_channels.json"), {"channels": []})
        item = {"kind": kind, "target": target[:500], "min_severity": min_severity or ""}
        for key in ("to", "from_addr", "user", "password", "tls"):
            value = (extra or {}).get(key)
            if value not in (None, ""):
                if key == "password":
                    item[key] = _encrypt_channel_secret(str(value))
                else:
                    item[key] = value
        payload.setdefault("channels", []).append(item)
        _save_json(_store_path("notify_channels.json"), payload)
        return item

    def remove_channel(self, index: int) -> bool:
        """Remove one channel by its 1-based list position."""
        payload = _load_json(_store_path("notify_channels.json"), {"channels": []})
        channels = payload.get("channels", [])
        position = int(index) - 1
        if position < 0 or position >= len(channels):
            return False
        channels.pop(position)
        payload["channels"] = channels
        _save_json(_store_path("notify_channels.json"), payload)
        return True

    @staticmethod
    def _send_email(channel: dict, line: str, event: str) -> bool:
        """Deliver one notification over SMTP; False on missing target."""
        import smtplib
        from email.message import EmailMessage

        to_addr = str(channel.get("to") or "")
        if not to_addr or "@" not in to_addr or len(to_addr) > 320:
            return False
        target = str(channel.get("target", ""))
        host, _, port_text = target.rpartition(":")
        if not host:
            host, port_text = target, "25"
        host = host.strip()
        if not host or len(host) > 253 or any(ch.isspace() for ch in host):
            return False
        try:
            port = int(port_text or 25)
        except ValueError:
            port = 25
        if not 1 <= port <= 65535:
            return False
        message = EmailMessage()
        message["Subject"] = f"[LazyOwn] {event}"
        message["From"] = str(channel.get("from_addr") or channel.get("user") or "lazyown@localhost")
        message["To"] = to_addr
        message.set_content(line)
        with smtplib.SMTP(host, port, timeout=10) as smtp:
            if channel.get("tls", True):
                try:
                    smtp.starttls()
                except smtplib.SMTPException:
                    pass
            user = str(channel.get("user") or "")
            if user:
                smtp.login(user, _decrypt_channel_secret(str(channel.get("password") or "")))
            smtp.send_message(message)
        return True

    def emit(self, task_id: str, event: str, data: dict) -> int:
        """Fan out finding/status/task events; returns deliveries.

        Channels: log (always), webhook, slack (text payload), file and
        email (SMTP with optional STARTTLS/login).
        """
        sev = str((data or {}).get("severity", "") or "")
        try:
            from modules.notify import mask_secrets as _mask

            safe_data = {k: (_mask(str(v)) if isinstance(v, str) else v) for k, v in (data or {}).items()}
        except Exception:
            safe_data = dict(data or {})
        line = json.dumps({"ts": _now(), "task": task_id, "event": event, **safe_data}, ensure_ascii=False)
        notify_path = _store_path("notify.log")
        with notify_path.open("a") as handle:
            handle.write(line + "\n")
        _restrict_file(notify_path)
        delivered = 0
        for channel in self.channels():
            floor = str(channel.get("min_severity", "") or "")
            if floor and SEV_RANK.get(sev, 5) > SEV_RANK.get(floor, 5):
                continue
            kind = channel.get("kind")
            try:
                if kind in ("webhook", "slack") and channel.get("target"):
                    try:
                        from modules import notify as _notify

                        ok, _reason = _notify.url_allowed(str(channel["target"]))
                    except Exception:
                        ok, _reason = True, "ok"
                    if not ok:
                        continue
                    payload = json.dumps({"text": line}).encode() if kind == "slack" else line.encode()
                    try:
                        _notify.post_url_validated(str(channel["target"]), payload, timeout=8)
                    except ValueError:
                        continue
                elif kind == "email":
                    if not self._send_email(channel, line, event):
                        continue
                elif kind == "file" and channel.get("target"):
                    dest = Path(str(channel["target"]))
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with dest.open("a") as handle:
                        handle.write(line + "\n")
                delivered += 1
            except Exception:
                continue
        return delivered


