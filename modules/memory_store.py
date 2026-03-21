"""
memory_store.py — Episodic memory for the LazyOwn auto_loop.

Stores (command, output, findings, host, tool, success) per session and
retrieves relevant past experiences via SQLite FTS5 keyword search.
Optionally uses numpy for cosine similarity when available.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

try:
    import numpy as np
    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False

_DB_PATH = Path(__file__).parent.parent / "sessions" / "memory.db"

_DDL_MAIN = """
CREATE TABLE IF NOT EXISTS memories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT    NOT NULL,
    host        TEXT    NOT NULL DEFAULT '',
    tool        TEXT    NOT NULL DEFAULT '',
    command     TEXT    NOT NULL DEFAULT '',
    output_snippet TEXT NOT NULL DEFAULT '',
    findings_json  TEXT NOT NULL DEFAULT '[]',
    success     INTEGER NOT NULL DEFAULT 0,
    ts          REAL    NOT NULL,
    embedding   BLOB,
    UNIQUE(session_id, command)
);
"""

_DDL_FTS = """
CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts
USING fts5(content, content_rowid=id);
"""

_DDL_TRIGGER_INSERT = """
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memory_fts(rowid, content)
    VALUES (
        new.id,
        new.host || ' ' || new.tool || ' ' || new.command || ' ' || new.output_snippet
    );
END;
"""

_DDL_TRIGGER_DELETE = """
CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, content)
    VALUES ('delete', old.id, old.host || ' ' || old.tool || ' ' || old.command || ' ' || old.output_snippet);
END;
"""

_DDL_TRIGGER_UPDATE = """
CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, content)
    VALUES ('delete', old.id, old.host || ' ' || old.tool || ' ' || old.command || ' ' || old.output_snippet);
    INSERT INTO memory_fts(rowid, content)
    VALUES (
        new.id,
        new.host || ' ' || new.tool || ' ' || new.command || ' ' || new.output_snippet
    );
END;
"""


@dataclass
class MemoryEntry:
    session_id: str
    host: str
    tool: str
    command: str
    output_snippet: str
    findings_json: str
    success: bool
    ts: float
    embedding: Optional[bytes] = field(default=None, repr=False)
    id: Optional[int] = field(default=None, repr=False)


class StorageBackend(ABC):
    @abstractmethod
    def save(self, entry: MemoryEntry) -> None: ...

    @abstractmethod
    def search(self, query: str, top_k: int) -> List[MemoryEntry]: ...

    @abstractmethod
    def by_host(self, host: str, top_k: int) -> List[MemoryEntry]: ...

    @abstractmethod
    def by_service(self, service: str, top_k: int) -> List[MemoryEntry]: ...

    @abstractmethod
    def all_entries(self, limit: int) -> List[MemoryEntry]: ...

    @abstractmethod
    def close(self) -> None: ...


def _row_to_entry(row) -> MemoryEntry:
    return MemoryEntry(
        id=row[0],
        session_id=row[1],
        host=row[2],
        tool=row[3],
        command=row[4],
        output_snippet=row[5],
        findings_json=row[6],
        success=bool(row[7]),
        ts=row[8],
        embedding=row[9],
    )


class SQLiteBackend(StorageBackend):
    def __init__(self, db_path: Path = _DB_PATH) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = self._connect()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        for stmt in (_DDL_MAIN, _DDL_FTS, _DDL_TRIGGER_INSERT,
                     _DDL_TRIGGER_DELETE, _DDL_TRIGGER_UPDATE):
            conn.execute(stmt)
        conn.commit()
        return conn

    def save(self, entry: MemoryEntry) -> None:
        with self._lock:
            try:
                self._conn.execute(
                    """
                    INSERT OR IGNORE INTO memories
                        (session_id, host, tool, command, output_snippet,
                         findings_json, success, ts, embedding)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        entry.session_id,
                        entry.host,
                        entry.tool,
                        entry.command,
                        entry.output_snippet,
                        entry.findings_json,
                        int(entry.success),
                        entry.ts,
                        entry.embedding,
                    ),
                )
                self._conn.commit()
            except sqlite3.Error:
                self._conn.rollback()
                raise

    def _fetch(self, sql: str, params: tuple) -> List[MemoryEntry]:
        with self._lock:
            cur = self._conn.execute(sql, params)
            return [_row_to_entry(r) for r in cur.fetchall()]

    def search(self, query: str, top_k: int) -> List[MemoryEntry]:
        sql = """
            SELECT m.id, m.session_id, m.host, m.tool, m.command,
                   m.output_snippet, m.findings_json, m.success, m.ts, m.embedding
            FROM memories m
            JOIN memory_fts f ON f.rowid = m.id
            WHERE memory_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """
        return self._fetch(sql, (query, top_k))

    def by_host(self, host: str, top_k: int) -> List[MemoryEntry]:
        sql = """
            SELECT id, session_id, host, tool, command, output_snippet,
                   findings_json, success, ts, embedding
            FROM memories
            WHERE host = ?
            ORDER BY ts DESC
            LIMIT ?
        """
        return self._fetch(sql, (host, top_k))

    def by_service(self, service: str, top_k: int) -> List[MemoryEntry]:
        pattern = f"%{service}%"
        sql = """
            SELECT id, session_id, host, tool, command, output_snippet,
                   findings_json, success, ts, embedding
            FROM memories
            WHERE command LIKE ? OR output_snippet LIKE ?
            ORDER BY ts DESC
            LIMIT ?
        """
        return self._fetch(sql, (pattern, pattern, top_k))

    def all_entries(self, limit: int) -> List[MemoryEntry]:
        sql = """
            SELECT id, session_id, host, tool, command, output_snippet,
                   findings_json, success, ts, embedding
            FROM memories
            ORDER BY ts DESC
            LIMIT ?
        """
        return self._fetch(sql, (limit,))

    def stats_raw(self) -> dict:
        with self._lock:
            total = self._conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            hosts = self._conn.execute(
                "SELECT COUNT(DISTINCT host) FROM memories"
            ).fetchone()[0]
            tools = self._conn.execute(
                "SELECT COUNT(DISTINCT tool) FROM memories"
            ).fetchone()[0]
        return {"total": total, "hosts": hosts, "tools": tools}

    def close(self) -> None:
        with self._lock:
            self._conn.close()


class MemoryStore:
    _MAX_OUTPUT = 2000

    def __init__(self, backend: StorageBackend) -> None:
        self._backend = backend

    def remember(
        self,
        session_id: str,
        host: str,
        tool: str,
        command: str,
        output: str,
        findings: object,
        success: bool,
    ) -> None:
        snippet = output[: self._MAX_OUTPUT]
        if isinstance(findings, str):
            findings_json = findings
        else:
            findings_json = json.dumps(findings, ensure_ascii=False)
        entry = MemoryEntry(
            session_id=session_id,
            host=host,
            tool=tool,
            command=command,
            output_snippet=snippet,
            findings_json=findings_json,
            success=success,
            ts=time.time(),
        )
        self._backend.save(entry)

    def recall(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        return self._backend.search(query, top_k)

    def recall_by_host(self, host: str, top_k: int = 10) -> List[MemoryEntry]:
        return self._backend.by_host(host, top_k)

    def recall_for_service(self, service_name: str, top_k: int = 5) -> List[MemoryEntry]:
        return self._backend.by_service(service_name, top_k)

    def stats(self) -> dict:
        if isinstance(self._backend, SQLiteBackend):
            return self._backend.stats_raw()
        entries = self._backend.all_entries(limit=100_000)
        hosts = len({e.host for e in entries})
        tools = len({e.tool for e in entries})
        return {"total": len(entries), "hosts": hosts, "tools": tools}

    def export_finetuning_dataset(self, path: Path) -> Path:
        path = Path(path)
        entries = self._backend.all_entries(limit=100_000)
        with path.open("w", encoding="utf-8") as fh:
            for e in entries:
                if not e.success:
                    continue
                record = {
                    "prompt": (
                        f"Host: {e.host} Tool: {e.tool} Command: {e.command}"
                    ),
                    "completion": (
                        f"Success: {e.success} Findings: {e.findings_json}"
                    ),
                }
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return path


_store_instance: Optional[MemoryStore] = None
_store_lock = threading.Lock()


def get_memory_store() -> MemoryStore:
    global _store_instance
    if _store_instance is None:
        with _store_lock:
            if _store_instance is None:
                _store_instance = MemoryStore(SQLiteBackend())
    return _store_instance


def remember(
    session_id: str,
    host: str,
    tool: str,
    command: str,
    output: str,
    findings: object,
    success: bool,
) -> None:
    get_memory_store().remember(session_id, host, tool, command, output, findings, success)


def recall(query: str, top_k: int = 5) -> List[MemoryEntry]:
    return get_memory_store().recall(query, top_k)


def _print_entries(entries: List[MemoryEntry]) -> None:
    if not entries:
        print("No results.")
        return
    for e in entries:
        ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.ts))
        print(
            f"[{ts_str}] host={e.host} tool={e.tool} success={e.success}\n"
            f"  cmd: {e.command}\n"
            f"  findings: {e.findings_json[:120]}\n"
        )


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Query the LazyOwn episodic memory store."
    )
    parser.add_argument("--query", "-q", help="FTS5 search query")
    parser.add_argument("--host", help="Filter by host")
    parser.add_argument("--service", help="Filter by service name in command/output")
    parser.add_argument("--top", "-n", type=int, default=5, help="Max results")
    parser.add_argument("--stats", action="store_true", help="Print store statistics")
    parser.add_argument("--export", metavar="PATH", help="Export fine-tuning JSONL to PATH")
    args = parser.parse_args()

    store = get_memory_store()

    if args.stats:
        s = store.stats()
        print(f"Total: {s['total']}  Hosts: {s['hosts']}  Tools: {s['tools']}")

    if args.query:
        results = store.recall(args.query, top_k=args.top)
        print(f"--- Results for query '{args.query}' ---")
        _print_entries(results)

    if args.host:
        results = store.recall_by_host(args.host, top_k=args.top)
        print(f"--- Results for host '{args.host}' ---")
        _print_entries(results)

    if args.service:
        results = store.recall_for_service(args.service, top_k=args.top)
        print(f"--- Results for service '{args.service}' ---")
        _print_entries(results)

    if args.export:
        out_path = store.export_finetuning_dataset(Path(args.export))
        print(f"Fine-tuning dataset written to: {out_path}")


if __name__ == "__main__":
    _cli()
