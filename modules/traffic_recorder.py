"""HTTP traffic recorder with file-tree storage and SQLite index.

Ports the LAZY ``traffic`` subsystem: every agent-driven HTTP exchange
is persisted to a human-browsable directory with a sidecar SQLite index
for paged queries. No redaction is applied; scoping is enforced by the
caller before recording.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import threading
import time
import urllib.parse
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RecorderConfig:
    """Centralized constants for recorder behavior."""

    max_body_bytes: int = 2000000
    index_name: str = "index.sqlite"
    bodies_dir: str = "bodies"


CONFIG = RecorderConfig()

INDEX_SCHEMA = """
CREATE TABLE IF NOT EXISTS exchanges (
  id TEXT PRIMARY KEY,
  ts INTEGER,
  host TEXT,
  method TEXT,
  url_template TEXT,
  url TEXT,
  status INTEGER,
  content_type TEXT,
  req_len INTEGER,
  resp_len INTEGER,
  path TEXT
);
CREATE INDEX IF NOT EXISTS idx_ex_host ON exchanges(host);
CREATE INDEX IF NOT EXISTS idx_ex_ts ON exchanges(ts);
CREATE INDEX IF NOT EXISTS idx_ex_status ON exchanges(status);
"""

FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS bodies_fts USING fts5(
  exchange_id UNINDEXED,
  text,
  tokenize='trigram'
);
"""
"""Bodies index uses the trigram tokenizer so mid-token searches (API keys,
hashes, split words) match like a substring scan with index speed. Older
databases are migrated in place by :meth:`TrafficRecorder._ensure_fts`."""

FTS_TEXT_LIMIT = 262144

MAX_BODY_BYTES = CONFIG.max_body_bytes


def url_template(url: str) -> str:
    """Collapse numeric path segments so similar URLs group together."""
    try:
        parts = urllib.parse.urlparse(url)
        collapsed = "/".join("N" if seg.isdigit() else seg for seg in parts.path.split("/"))
        return f"{parts.scheme}://{parts.hostname or ''}{collapsed}"
    except Exception:
        return url


@dataclass
class Exchange:
    """Single recorded HTTP exchange."""

    exchange_id: str
    method: str
    url: str
    status: int
    req_len: int
    resp_len: int


class TrafficRecorder:
    """Append-only recorder backed by files plus SQLite index."""

    def __init__(self, base_dir: str | Path) -> None:
        """Create storage directories and initialize the index."""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        (self.base_dir / "bodies").mkdir(parents=True, exist_ok=True)
        self._db_path = self.base_dir / "index.sqlite"
        self._lock = threading.Lock()
        self._fts = False
        with sqlite3.connect(str(self._db_path)) as conn:
            conn.executescript(INDEX_SCHEMA)
            columns = {row[1] for row in conn.execute("PRAGMA table_info(exchanges)")}
            if "task" not in columns:
                conn.execute("ALTER TABLE exchanges ADD COLUMN task TEXT")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_ex_task ON exchanges(task)")
            try:
                conn.executescript(FTS_SCHEMA)
                self._migrate_fts(conn)
                self._fts = True
            except sqlite3.OperationalError:
                self._fts = False

    def _migrate_fts(self, conn: sqlite3.Connection) -> None:
        """Upgrade a pre-trigram ``bodies_fts`` table in place.

        Older sessions shipped the default ``unicode61`` tokenizer, which
        cannot find mid-token strings. The table is dropped and recreated
        with the trigram tokenizer; ``search_body`` backfills it lazily,
        so the migration stays cheap even on large stores.

        Args:
            conn: Open index connection (inside the ``__init__`` context).
        """
        row = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='bodies_fts'").fetchone()
        existing = str(row[0] or "") if row else ""
        if existing and "trigram" not in existing.lower():
            conn.execute("DROP TABLE IF EXISTS bodies_fts")
            conn.executescript(FTS_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        """Open a new index connection."""
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def record(
        self,
        method: str,
        url: str,
        status: int = 0,
        req_body: bytes = b"",
        resp_body: bytes = b"",
        content_type: str = "",
        req_headers: dict | None = None,
        resp_headers: dict | None = None,
        host: str = "",
        port: int = 0,
        scheme: str = "",
        task: str = "",
        note: str = "",
    ) -> Exchange:
        """Persist one exchange and return its descriptor.

        Args:
            method: HTTP method.
            url: Full request URL.
            status: Response status code (0 when the exchange failed).
            req_body: Request body bytes (truncated to the cap).
            resp_body: Response body bytes (truncated to the cap).
            content_type: Response content type.
            req_headers: Request header mapping.
            resp_headers: Response header mapping.
            host: Host override (MITM knows it before parsing the URL).
            port: Port override.
            scheme: Scheme override (https for MITM'd CONNECT tunnels).
            task: Optional task tag for loop ingestion.
            note: Optional failure note.

        Returns:
            Exchange descriptor.
        """
        safe_method = (method or "GET").upper()[:16]
        safe_url = str(url or "")[:4000]
        parsed = urllib.parse.urlparse(safe_url)
        resolved_host = str(host or parsed.hostname or "")[:255]
        resolved_port = int(port or parsed.port or (443 if scheme == "https" else 80))
        digest = hashlib.sha256(f"{time.time_ns()}{safe_method}{safe_url}".encode()).hexdigest()[:16]
        exchange_id = f"{int(time.time())}-{digest}"
        req = bytes(req_body or b"")[:MAX_BODY_BYTES]
        resp = bytes(resp_body or b"")[:MAX_BODY_BYTES]
        body_path = self.base_dir / "bodies" / f"{exchange_id}.json"
        payload = {
            "req_head": f"{safe_method} {safe_url}",
            "req_body": req.decode("utf-8", "replace"),
            "resp_body": resp.decode("utf-8", "replace"),
            "status": int(status),
            "scheme": str(scheme or parsed.scheme)[:16],
            "host": resolved_host,
            "port": resolved_port,
            "task": str(task or "")[:64],
            "note": str(note or "")[:300],
            "req_headers": dict(req_headers or {}),
            "resp_headers": dict(resp_headers or {}),
        }
        body_path.write_text(json.dumps(payload), encoding="utf-8")
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO exchanges "
                    "(id, ts, host, method, url_template, url, status, "
                    "content_type, req_len, resp_len, path, task) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        exchange_id,
                        int(time.time()),
                        resolved_host,
                        safe_method,
                        url_template(safe_url),
                        safe_url,
                        int(status),
                        str(content_type or "")[:128],
                        len(req),
                        len(resp),
                        str(body_path),
                        str(task or "")[:64],
                    ),
                )
        self._index_fts(exchange_id, req, resp)
        return Exchange(
            exchange_id=exchange_id,
            method=safe_method,
            url=safe_url,
            status=int(status),
            req_len=len(req),
            resp_len=len(resp),
        )

    def since(self, rowid: int = 0, limit: int = 200) -> list[dict]:
        """Page exchanges newer than a rowid watermark for loop ingestion.

        Args:
            rowid: Last ingested SQLite rowid (0 starts from the beginning).
            limit: Max rows per page.

        Returns:
            Row dicts including the ``rowid`` cursor.
        """
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT rowid, * FROM exchanges WHERE rowid > ? ORDER BY rowid LIMIT ?",
                (max(0, int(rowid)), max(1, int(limit))),
            ).fetchall()
        return [dict(r) for r in rows]

    def latest_rowid(self) -> int:
        """Return the current max rowid (0 when the index is empty)."""
        with self._connect() as conn:
            row = conn.execute("SELECT MAX(rowid) AS n FROM exchanges").fetchone()
        return int(row["n"] or 0)

    def query(
        self, host: str = "", status: int | None = None, limit: int = 50, offset: int = 0, task: str = ""
    ) -> list[dict]:
        """Page exchanges with optional host, status and task filters."""
        clauses: list[str] = []
        params: list[object] = []
        if host:
            clauses.append("host = ?")
            params.append(str(host))
        if status is not None:
            clauses.append("status = ?")
            params.append(int(status))
        if task:
            clauses.append("task = ?")
            params.append(str(task))
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = f"SELECT * FROM exchanges {where} ORDER BY ts DESC LIMIT ? OFFSET ?"
        params.extend([max(1, int(limit)), max(0, int(offset))])
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_body(self, exchange_id: str) -> dict:
        """Load the stored body document for one exchange."""
        safe_id = "".join(c for c in str(exchange_id) if c.isalnum() or c in "-_")
        candidate = (self.base_dir / "bodies" / f"{safe_id}.json").resolve()
        allowed = (self.base_dir / "bodies").resolve()
        if allowed not in candidate.parents:
            raise PermissionError("Path traversal blocked.")
        return json.loads(candidate.read_text(encoding="utf-8"))

    def read_body(self, exchange_id: str, part: str = "resp", offset: int = 0, length: int = 8192) -> dict:
        """Read one body in ranges like a blob store.

        Args:
            exchange_id: Exchange whose body is read.
            part: ``resp`` (default) or ``req``.
            offset: Byte offset.
            length: Max bytes (clamped to 1 MiB).

        Returns:
            Dict with data, offset, length, total and eof.

        Raises:
            ValueError: Unknown part.
            KeyError: Unknown exchange body.
        """
        if part not in ("req", "resp"):
            raise ValueError("part must be req|resp")
        document = self.get_body(exchange_id)
        blob = str(document.get(f"{part}_body", ""))
        start = max(0, int(offset or 0))
        size = max(1, min(1048576, int(length or 8192)))
        chunk = blob[start : start + size]
        return {
            "exchange_id": str(exchange_id),
            "part": part,
            "data": chunk,
            "offset": start,
            "length": len(chunk),
            "total": len(blob),
            "eof": start + len(chunk) >= len(blob),
        }

    def count(self) -> int:
        """Return the total number of recorded exchanges."""
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS n FROM exchanges").fetchone()
        return int(row["n"])

    def _index_fts(self, exchange_id: str, req: bytes, resp: bytes) -> None:
        """Index request and response text for full-text search.

        Failures are ignored: search falls back to a bounded LIKE scan
        when FTS5 is unavailable in the local sqlite build.
        """
        if not self._fts:
            return
        text = (
            bytes(req or b"")[:FTS_TEXT_LIMIT].decode("utf-8", "replace")
            + "\n"
            + bytes(resp or b"")[:FTS_TEXT_LIMIT].decode("utf-8", "replace")
        )
        try:
            with self._lock:
                with self._connect() as conn:
                    conn.execute("INSERT INTO bodies_fts(exchange_id, text) VALUES (?,?)", (exchange_id, text))
        except sqlite3.OperationalError:
            self._fts = False

    def backfill_fts(self, batch: int = 500) -> int:
        """Index stored bodies missing from the FTS table.

        Args:
            batch: Max bodies indexed per call.

        Returns:
            Number of newly indexed exchanges.
        """
        if not self._fts:
            return 0
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, path FROM exchanges WHERE id NOT IN "
                "(SELECT exchange_id FROM bodies_fts) ORDER BY rowid LIMIT ?",
                (max(1, int(batch)),),
            ).fetchall()
        indexed = 0
        for row in rows:
            try:
                payload = json.loads(Path(str(row["path"])).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            self._index_fts(
                str(row["id"]),
                str(payload.get("req_body", "")).encode()[:FTS_TEXT_LIMIT],
                str(payload.get("resp_body", "")).encode()[:FTS_TEXT_LIMIT],
            )
            indexed += 1
        return indexed

    @staticmethod
    def _fts_query(query: str) -> str:
        """Quote a user phrase so FTS5 metacharacters stay literal."""
        cleaned = re.sub(r'["*^:()\-]', " ", str(query or "")).strip()
        if not cleaned:
            return ""
        return f'"{cleaned}"'

    def search_body(self, query: str, limit: int = 20) -> list[dict]:
        """Full-text search request/response bodies.

        Uses the FTS5 index when available and falls back to a bounded
        LIKE scan over the most recent bodies otherwise.

        Args:
            query: Phrase to search for.
            limit: Max hits.

        Returns:
            Hits with exchange_id, url, status, host and a snippet.
        """
        needle = str(query or "").strip()
        if not needle:
            return []
        limit = max(1, int(limit))
        if self._fts and len(needle) < 3:
            return self._scan_bodies(needle, limit)
        if self._fts:
            self.backfill_fts()
            match = self._fts_query(needle)
            if match:
                try:
                    with self._connect() as conn:
                        rows = conn.execute(
                            "SELECT f.exchange_id AS exchange_id, "
                            "snippet(bodies_fts, 1, '[', ']', '...', 12) AS snippet, "
                            "e.url AS url, e.status AS status, e.host AS host "
                            "FROM bodies_fts f "
                            "LEFT JOIN exchanges e ON e.id = f.exchange_id "
                            "WHERE bodies_fts MATCH ? ORDER BY rank LIMIT ?",
                            (match, limit),
                        ).fetchall()
                    if rows:
                        return [dict(r) for r in rows]
                except sqlite3.OperationalError:
                    self._fts = False
        return self._scan_bodies(needle, limit)

    def _scan_bodies(self, needle: str, limit: int) -> list[dict]:
        """Bounded LIKE fallback over the most recent stored bodies."""
        lowered = needle.lower()
        hits: list[dict] = []
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, url, status, host, path FROM exchanges ORDER BY rowid DESC LIMIT 2000"
            ).fetchall()
        for row in rows:
            try:
                payload = json.loads(Path(str(row["path"])).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            blob = (str(payload.get("req_body", "")) + "\n" + str(payload.get("resp_body", ""))).lower()
            if lowered in blob:
                position = blob.find(lowered)
                hits.append(
                    {
                        "exchange_id": str(row["id"]),
                        "url": str(row["url"]),
                        "status": int(row["status"] or 0),
                        "host": str(row["host"]),
                        "snippet": blob[max(0, position - 40) : position + 80],
                    }
                )
                if len(hits) >= limit:
                    break
        return hits

    def export_archive(self, path: str | Path, limit: int = 0, task: str = "") -> dict:
        """Export the index plus bodies into a portable zip archive.

        Args:
            path: Destination zip path.
            limit: Max exchanges (0 exports all).
            task: Optional task filter for per-task archives.

        Returns:
            Dict with exported/bodies counts and the archive path.
        """
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            query = "SELECT * FROM exchanges"
            params: list[object] = []
            if task:
                query += " WHERE task = ?"
                params.append(str(task))
            query += " ORDER BY rowid"
            if limit and int(limit) > 0:
                query += f" LIMIT {int(limit)}"
            rows = [dict(r) for r in conn.execute(query, params).fetchall()]
        bodies_dir = (self.base_dir / "bodies").resolve()
        written = 0
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                "manifest.json", json.dumps({"version": 1, "created": time.time(), "exchanges": len(rows)})
            )
            archive.writestr("index.json", json.dumps(rows))
            for row in rows:
                body_path = Path(str(row.get("path", "")))
                try:
                    resolved = body_path.resolve()
                except OSError:
                    continue
                if bodies_dir not in resolved.parents or not resolved.exists():
                    continue
                archive.write(resolved, f"bodies/{resolved.name}")
                written += 1
        return {"exported": len(rows), "bodies": written, "path": str(target)}

    def import_archive(self, path: str | Path) -> dict:
        """Merge an archive exported by :meth:`export_archive`.

        Args:
            path: Source zip path.

        Returns:
            Dict with imported/bodies counts and the archive path.

        Raises:
            FileNotFoundError: Archive missing.
        """
        source = Path(path)
        if not source.exists():
            raise FileNotFoundError(f"archive not found: {source}")
        imported = 0
        bodies = 0
        with zipfile.ZipFile(source) as archive:
            names = set(archive.namelist())
            rows = json.loads(archive.read("index.json")) if "index.json" in names else []
            for row in rows:
                exchange_id = str(row.get("id", ""))
                if not exchange_id:
                    continue
                body_name = f"bodies/{exchange_id}.json"
                body_path = self.base_dir / "bodies" / f"{exchange_id}.json"
                if body_name in names:
                    body_path.write_bytes(archive.read(body_name))
                    bodies += 1
                with self._lock:
                    with self._connect() as conn:
                        conn.execute(
                            "INSERT OR REPLACE INTO exchanges "
                            "(id, ts, host, method, url_template, url, status, "
                            "content_type, req_len, resp_len, path, task) "
                            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                exchange_id,
                                int(row.get("ts", 0) or 0),
                                str(row.get("host", "")),
                                str(row.get("method", "")),
                                str(row.get("url_template", "")),
                                str(row.get("url", "")),
                                int(row.get("status", 0) or 0),
                                str(row.get("content_type", "")),
                                int(row.get("req_len", 0) or 0),
                                int(row.get("resp_len", 0) or 0),
                                str(body_path),
                                str(row.get("task", "")),
                            ),
                        )
                try:
                    payload = json.loads(body_path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    payload = {}
                self._index_fts(
                    exchange_id, str(payload.get("req_body", "")).encode(), str(payload.get("resp_body", "")).encode()
                )
                imported += 1
        return {"imported": imported, "bodies": bodies, "path": str(source)}

    def import_inbox(self, inbox_dir: str | Path | None = None) -> dict:
        """Import every zip dropped in the inbox, moving handled files away.

        Args:
            inbox_dir: Scan root (defaults to ``<base>/inbox``).

        Returns:
            Dict with imported count and handled file names.
        """
        root = Path(inbox_dir) if inbox_dir else (self.base_dir / "inbox")
        if not root.is_dir():
            return {"imported": 0, "files": []}
        done_dir = root / "imported"
        imported = 0
        handled: list[str] = []
        for archive in sorted(root.glob("*.zip")):
            try:
                summary = self.import_archive(archive)
            except Exception:
                continue
            imported += int(summary.get("imported", 0) or 0)
            try:
                done_dir.mkdir(parents=True, exist_ok=True)
                archive.replace(done_dir / archive.name)
                handled.append(archive.name)
            except OSError:
                try:
                    archive.unlink()
                    handled.append(archive.name)
                except OSError:
                    pass
        return {"imported": imported, "files": handled}

    def gc(self, older_than_sec: float = 0.0) -> dict:
        """Delete exchanges older than a cut-off with their bodies and index rows.

        Args:
            older_than_sec: Age threshold; 0 disables the sweep.

        Returns:
            Dict with removed count.
        """
        age = float(older_than_sec or 0.0)
        if age <= 0:
            return {"removed": 0, "reason": "positive age required"}
        cutoff = int(time.time() - age)
        with self._connect() as conn:
            rows = conn.execute("SELECT id, path FROM exchanges WHERE ts < ?", (cutoff,)).fetchall()
        removed = 0
        for row in rows:
            try:
                Path(str(row["path"])).unlink()
            except OSError:
                pass
            with self._lock:
                with self._connect() as conn:
                    conn.execute("DELETE FROM exchanges WHERE id = ?", (str(row["id"]),))
                    if self._fts:
                        try:
                            conn.execute("DELETE FROM bodies_fts WHERE exchange_id = ?", (str(row["id"]),))
                        except sqlite3.OperationalError:
                            self._fts = False
            removed += 1
        return {"removed": removed}
