"""HTTP traffic recorder with file-tree storage and SQLite index.

Ports the LAZY ``traffic`` subsystem: every agent-driven HTTP exchange
is persisted to a human-browsable directory with a sidecar SQLite index
for paged queries. No redaction is applied; scoping is enforced by the
caller before recording.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import time
import urllib.parse
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

MAX_BODY_BYTES = CONFIG.max_body_bytes


def url_template(url: str) -> str:
    """Collapse numeric path segments so similar URLs group together."""
    try:
        parts = urllib.parse.urlparse(url)
        collapsed = "/".join(
            "N" if seg.isdigit() else seg for seg in parts.path.split("/"))
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
        with sqlite3.connect(str(self._db_path)) as conn:
            conn.executescript(INDEX_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        """Open a new index connection."""
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def record(self, method: str, url: str, status: int = 0,
               req_body: bytes = b"", resp_body: bytes = b"",
               content_type: str = "") -> Exchange:
        """Persist one exchange and return its descriptor."""
        safe_method = (method or "GET").upper()[:16]
        safe_url = str(url or "")[:4000]
        host = urllib.parse.urlparse(safe_url).hostname or ""
        digest = hashlib.sha256(
            f"{time.time_ns()}{safe_method}{safe_url}".encode()).hexdigest()[:16]
        exchange_id = f"{int(time.time())}-{digest}"
        req = bytes(req_body or b"")[:MAX_BODY_BYTES]
        resp = bytes(resp_body or b"")[:MAX_BODY_BYTES]
        body_path = self.base_dir / "bodies" / f"{exchange_id}.json"
        payload = {"req_head": f"{safe_method} {safe_url}",
                   "req_body": req.decode("utf-8", "replace"),
                   "resp_body": resp.decode("utf-8", "replace"),
                   "status": int(status)}
        body_path.write_text(json.dumps(payload), encoding="utf-8")
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO exchanges "
                    "(id, ts, host, method, url_template, url, status, "
                    "content_type, req_len, resp_len, path) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (exchange_id, int(time.time()), host, safe_method,
                     url_template(safe_url), safe_url, int(status),
                     str(content_type or "")[:128], len(req), len(resp),
                     str(body_path)))
        return Exchange(exchange_id=exchange_id, method=safe_method,
                        url=safe_url, status=int(status),
                        req_len=len(req), resp_len=len(resp))

    def query(self, host: str = "", status: int | None = None,
              limit: int = 50, offset: int = 0) -> list[dict]:
        """Page exchanges with optional host and status filters."""
        clauses: list[str] = []
        params: list[object] = []
        if host:
            clauses.append("host = ?")
            params.append(str(host))
        if status is not None:
            clauses.append("status = ?")
            params.append(int(status))
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = (f"SELECT * FROM exchanges {where} "
                 "ORDER BY ts DESC LIMIT ? OFFSET ?")
        params.extend([max(1, int(limit)), max(0, int(offset))])
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_body(self, exchange_id: str) -> dict:
        """Load the stored body document for one exchange."""
        safe_id = "".join(c for c in str(exchange_id)
                          if c.isalnum() or c in "-_")
        candidate = (self.base_dir / "bodies" / f"{safe_id}.json").resolve()
        allowed = (self.base_dir / "bodies").resolve()
        if allowed not in candidate.parents:
            raise PermissionError("Path traversal blocked.")
        return json.loads(candidate.read_text(encoding="utf-8"))

    def count(self) -> int:
        """Return the total number of recorded exchanges."""
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS n FROM exchanges").fetchone()
        return int(row["n"])
