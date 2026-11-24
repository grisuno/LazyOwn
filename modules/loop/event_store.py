"""SQLite event store for engine events and worker communication.

One contract over two tables in the shared WAL database
(``sessions/db/loop_state.db``):

* ``engine_events`` — append-only mirror of every OutcomeBus event; the
  durable spine of the engine from which projections can be rebuilt.
* ``worker_messages`` — communication channel between loop workers and
  tools: progress, footholds, notes and intel shared across tasks and
  workers. Workers publish here and read each other's entries through
  :func:`fleet_prompt_context` (injected into LLM prompt context) or the
  typed accessors (:meth:`EventStore.footholds`, :meth:`EventStore.messages`).
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
from pathlib import Path
from typing import Any

from modules.loop import state_db

MESSAGE_KINDS: tuple[str, ...] = ("progress", "foothold", "note", "intel")

EVENTS_TABLE_MAX_ROWS = 50_000
MESSAGES_TABLE_MAX_ROWS = 10_000
MESSAGE_BODY_MAX_CHARS = 600
DEFAULT_CONTEXT_MESSAGES = 6

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS engine_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    kind TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT '',
    host TEXT NOT NULL DEFAULT '',
    target TEXT NOT NULL DEFAULT '',
    task_id TEXT NOT NULL DEFAULT '',
    worker TEXT NOT NULL DEFAULT '',
    title TEXT NOT NULL DEFAULT '',
    digest TEXT NOT NULL DEFAULT '',
    payload TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_engine_events_task ON engine_events(task_id, id);
CREATE INDEX IF NOT EXISTS idx_engine_events_kind ON engine_events(kind, id);
CREATE TABLE IF NOT EXISTS worker_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    task_id TEXT NOT NULL DEFAULT '',
    worker TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL,
    body TEXT NOT NULL DEFAULT '',
    digest TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_worker_messages_task ON worker_messages(task_id, id);
CREATE INDEX IF NOT EXISTS idx_worker_messages_kind ON worker_messages(kind, id);
"""

_shared: EventStore | None = None
_shared_lock = threading.Lock()
_schema_applied: set[str] = set()
_write_lock = threading.RLock()


def _digest(*parts: str) -> str:
    """Return a short sha256 digest over the given parts."""
    return hashlib.sha256("\x1f".join(parts).encode("utf-8", "ignore")).hexdigest()[:16]


class EventStore:
    """Append-only engine event log plus worker message board.

    Args:
        db_path: Optional database path; defaults to the shared loop
            state database.
    """

    def __init__(self, db_path: str | Any | None = None) -> None:
        self._target = str(Path(db_path) if db_path else state_db.default_db_path())

    def _conn(self):
        """Return the per-thread connection for this store, schema applied."""
        with _write_lock:
            conn = state_db.thread_connection(self._target)
            if self._target not in _schema_applied:
                conn.executescript(_SCHEMA_SQL)
                conn.commit()
                _schema_applied.add(self._target)
            return conn

    def append_event(self, event: dict[str, Any]) -> int:
        """Insert one engine event row.

        Args:
            event: Mapping with ``kind`` plus optional ``severity``,
                ``host``, ``target``, ``task_id``, ``worker``, ``title``
                and any extra fields under ``metadata``.

        Returns:
            The inserted row id.
        """
        if not isinstance(event, dict):
            return 0
        kind = str(event.get("kind", "") or "unknown")[:64]
        metadata = event.get("metadata") or {}
        payload = {key: value for key, value in event.items() if key != "metadata"}
        payload["metadata"] = metadata
        conn = self._conn()
        with _write_lock:
            cursor = conn.execute(
                "INSERT INTO engine_events (ts, kind, severity, host, target, task_id, worker, title, digest, payload)"
                " VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    float(event.get("ts") or time.time()),
                    kind,
                    str(event.get("severity", "") or "")[:32],
                    str(event.get("host", "") or "")[:255],
                    str(event.get("target", "") or "")[:255],
                    str(event.get("task_id", "") or "")[:128],
                    str(event.get("worker", "") or "")[:64],
                    str(event.get("title", "") or "")[:200],
                    _digest(
                        kind,
                        str(event.get("host", "") or ""),
                        str(event.get("title", "") or ""),
                        str(event.get("task_id", "") or ""),
                    ),
                    json.dumps(payload, default=str)[:8000],
                ),
            )
            conn.commit()
        return int(cursor.lastrowid or 0)

    def events(self, task_id: str = "", kind: str = "", limit: int = 50) -> list[dict[str, Any]]:
        """Return recent engine events newest-first.

        Args:
            task_id: Filter by task; empty means all.
            kind: Filter by event kind; empty means all.
            limit: Max rows returned.

        Returns:
            List of event mappings with ``payload`` decoded.
        """
        sql = "SELECT * FROM engine_events"
        clauses: list[str] = []
        params: list[Any] = []
        if task_id:
            clauses.append("task_id = ?")
            params.append(task_id)
        if kind:
            clauses.append("kind = ?")
            params.append(kind)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(max(1, int(limit)))
        rows = self._conn().execute(sql, params).fetchall()
        results: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            try:
                item["payload"] = json.loads(item.get("payload") or "{}")
            except Exception:
                item["payload"] = {}
            results.append(item)
        return results

    def post_message(self, task_id: str, worker: str, kind: str, body: str) -> int:
        """Publish one worker message for other workers to read.

        Args:
            task_id: Owning task (may be empty for fleet-wide notes).
            worker: Publisher identity (worker name or tool name).
            kind: One of :data:`MESSAGE_KINDS`.
            body: Message text; truncated to :data:`MESSAGE_BODY_MAX_CHARS`.

        Returns:
            The inserted row id, or 0 for an unknown kind or empty body.
        """
        if kind not in MESSAGE_KINDS:
            return 0
        text = str(body or "").strip()[:MESSAGE_BODY_MAX_CHARS]
        if not text:
            return 0
        conn = self._conn()
        with _write_lock:
            cursor = conn.execute(
                "INSERT INTO worker_messages (ts, task_id, worker, kind, body, digest) VALUES (?,?,?,?,?,?)",
                (
                    time.time(),
                    str(task_id or "")[:128],
                    str(worker or "")[:64],
                    kind,
                    text,
                    _digest(kind, text),
                ),
            )
            conn.commit()
        return int(cursor.lastrowid or 0)

    def post_foothold(self, task_id: str, worker: str, host: str, summary: str) -> int:
        """Publish a foothold discovery so the rest of the fleet can use it.

        Args:
            task_id: Task that confirmed the foothold.
            worker: Worker or tool identity.
            host: Host where the foothold was obtained.
            summary: One-line description of the access.

        Returns:
            The inserted row id, or 0 when nothing was stored.
        """
        return self.post_message(task_id, worker, "foothold", f"{host}: {summary}" if host else summary)

    def messages(
        self,
        task_id: str = "",
        kind: str = "",
        since_id: int = 0,
        limit: int = 50,
        exclude_task: str = "",
    ) -> list[dict[str, Any]]:
        """Return recent worker messages newest-first.

        Args:
            task_id: Filter by task; empty means all tasks.
            kind: Filter by message kind; empty means all kinds.
            since_id: Only return rows with ``id > since_id``.
            limit: Max rows returned.
            exclude_task: Omit rows from this task (fleet-wide reads).

        Returns:
            List of message mappings.
        """
        sql = "SELECT * FROM worker_messages"
        clauses: list[str] = []
        params: list[Any] = []
        if task_id:
            clauses.append("task_id = ?")
            params.append(task_id)
        if kind:
            clauses.append("kind = ?")
            params.append(kind)
        if since_id > 0:
            clauses.append("id > ?")
            params.append(int(since_id))
        if exclude_task:
            clauses.append("task_id != ?")
            params.append(exclude_task)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(max(1, int(limit)))
        return [dict(row) for row in self._conn().execute(sql, params).fetchall()]

    def footholds(self, task_id: str = "", limit: int = 20) -> list[dict[str, Any]]:
        """Return recent foothold messages.

        Args:
            task_id: Filter by task; empty means all tasks.
            limit: Max rows returned.

        Returns:
            List of foothold message mappings.
        """
        return self.messages(task_id=task_id, kind="foothold", limit=limit)

    def summary(self, task_id: str = "") -> dict[str, Any]:
        """Return aggregate counters over both tables.

        Args:
            task_id: Optional task filter applied to both tables.

        Returns:
            Mapping with ``events``, ``messages`` and ``by_kind`` counts.
        """
        conn = self._conn()
        event_clause = " WHERE task_id = ?" if task_id else ""
        message_clause = " WHERE task_id = ?" if task_id else ""
        params: list[Any] = [task_id] if task_id else []
        events = int(conn.execute(f"SELECT COUNT(*) FROM engine_events{event_clause}", params).fetchone()[0])
        rows = conn.execute(
            f"SELECT kind, COUNT(*) FROM worker_messages{message_clause} GROUP BY kind",
            params,
        ).fetchall()
        by_kind = {str(row[0]): int(row[1]) for row in rows}
        messages = sum(by_kind.values())
        return {"events": events, "messages": messages, "by_kind": by_kind}

    def prune(
        self,
        max_events: int = EVENTS_TABLE_MAX_ROWS,
        max_messages: int = MESSAGES_TABLE_MAX_ROWS,
        max_age_sec: float = 0.0,
    ) -> dict[str, int]:
        """Apply retention limits to both tables.

        Args:
            max_events: Keep at most this many event rows.
            max_messages: Keep at most this many message rows.
            max_age_sec: When positive, also drop rows older than this.

        Returns:
            Mapping with deleted row counts per table.
        """
        conn = self._conn()
        deleted = {"events": 0, "messages": 0}
        cutoff = time.time() - max(0.0, float(max_age_sec)) if max_age_sec > 0 else 0.0
        with _write_lock:
            for table, cap, key in (
                ("engine_events", max_events, "events"),
                ("worker_messages", max_messages, "messages"),
            ):
                if cap > 0:
                    row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
                    overflow = int(row[0]) - int(cap)
                    if overflow > 0:
                        cursor = conn.execute(
                            f"DELETE FROM {table} WHERE id IN (SELECT id FROM {table} ORDER BY id ASC LIMIT ?)",
                            (overflow,),
                        )
                        deleted[key] = max(deleted[key], int(cursor.rowcount or 0))
                if cutoff:
                    cursor = conn.execute(f"DELETE FROM {table} WHERE ts < ?", (cutoff,))
                    deleted[key] = max(deleted[key], int(cursor.rowcount or 0))
            conn.commit()
        return deleted


def shared_store() -> EventStore:
    """Return the process-wide EventStore over the shared loop database."""
    global _shared
    with _shared_lock:
        if _shared is None:
            _shared = EventStore()
        return _shared


def fleet_prompt_context(task_id: str = "", limit: int = DEFAULT_CONTEXT_MESSAGES) -> str:
    """Render recent worker messages as a prompt-ready intel section.

    Rows from the same task come last so cross-task intel leads. The
    caller fences the returned text as untrusted data before it reaches
    an LLM.

    Args:
        task_id: Current task; its own messages are excluded.
        limit: Max lines rendered.

    Returns:
        One line per message, or an empty string when the board is empty.
    """
    try:
        store = shared_store()
        rows = store.messages(limit=max(1, int(limit)), exclude_task=str(task_id or ""))
        if not rows:
            rows = store.messages(task_id=str(task_id or ""), limit=max(1, int(limit)))
    except Exception:
        return ""
    lines = []
    for row in rows:
        lines.append(
            f"[{row.get('kind', 'note')}] {row.get('worker', '?')}@{row.get('task_id', '-')}#{row.get('id', 0)}: {row.get('body', '')}"
        )
    return "Fleet intel: " + " | ".join(lines)


def record_outcome(event: dict[str, Any]) -> int:
    """Persist one outcome payload as an engine event and foothold signal.

    Args:
        event: Outcome mapping (an ``OutcomeEvent.to_dict()`` shape or a
            plain mapping with ``kind``/``title``/``host`` fields).

    Returns:
        The inserted event row id.
    """
    store = shared_store()
    row_id = store.append_event(event)
    metadata = event.get("metadata") or {}
    if event.get("success") and (event.get("shell") or str(metadata.get("foothold", "")) == "1"):
        store.post_foothold(
            str(event.get("task_id", "") or ""),
            str(metadata.get("worker", "") or event.get("source", "") or "engine"),
            str(event.get("host", "") or event.get("target", "") or ""),
            str(event.get("title", "") or "shell access"),
        )
    return row_id
