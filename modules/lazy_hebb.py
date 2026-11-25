"""LazyHebb — zero-inference synaptic memory for the loop and the hive.

Inspired by the HebbMesh paper concepts (write-time semantic seeding,
hebbian co-activation, graph-level privacy firewall; Muñoz Jara 2026,
DOI 10.5281/zenodo.24514028), reimplemented LazyOwn-native over Python
``sqlite3`` with FTS5: zero embeddings, zero LLM calls, zero extra
dependencies. Retrieval is deterministic BM25 rank plus one-hop
spreading activation over a co-activation edge table; co-recalled
memories strengthen each other's edges (fire together, wire together).

One SQLite WAL file (``sessions/lazy/hebb.sqlite``). Private rows are
excluded from recall and from bridge pathfinding before any expansion
so private tags can never leak through public neighbours. Markdown
import/export with the ``| sem:`` line suffix is the durable,
versionable source of truth.
"""

from __future__ import annotations

import json
import re
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any

DB_FILENAME = "hebb.sqlite"
MAX_ROWS = 20_000
MAX_EDGES = 25_000
EDGE_PRUNE_BATCH = 2_500
HEBB_CONTEXT_MAX_CHARS = 700
CONTENT_MAX_CHARS = 600
SEM_TAGS_MAX_CHARS = 200
AGENT_MAX_CHARS = 64
PHASE_MAX_CHARS = 32
DEFAULT_TOP_K = 5
SEED_MULTIPLIER = 3
PROPAGATION_GAIN = 0.5
LEARNING_RATE = 0.08
EDGE_WEIGHT_CAP = 1.0
HUB_TOLL = 0.25
MAX_QUERY_TOKENS = 24
MAX_EDGE_FAN = 8
MAX_EXPORT_ROWS = 5_000
SEM_SUFFIX_RE = re.compile(r"\|\s*sem:\s*(?P<tags>.+?)\s*$", re.IGNORECASE)
TOKEN_RE = re.compile(r"[\w\.\-:/]+", re.UNICODE)
FTS_SAFE_RE = re.compile(r"[^\w\s]", re.UNICODE)
WHITESPACE_RE = re.compile(r"\s+")

SEM_SEED_MAP: tuple[tuple[tuple[str, ...], str], ...] = (
    (("psexec", "wmiexec", "smbexec", "atexec", "impacket"), "lateral,smb,exec"),
    (("ssh", "sshd", "keyfile", "authorized_keys"), "lateral,ssh,remote"),
    (("winrm", "evil-winrm", "5985", "5986"), "lateral,winrm,remote"),
    (("rdp", "3389", "freerdp"), "lateral,rdp,remote"),
    (("nmap", "masscan", "rustscan", "portscan"), "recon,discovery"),
    (("smb", "445", "139", "netexec", "crackmapexec"), "smb,recon"),
    (("ldap", "389", "636", "kerberos", "88", "kerberoast", "asreproast"), "ad,enum"),
    (("sqlmap", "sqli", "union select", "blind injection"), "web,sqli"),
    (("xss", "cross site script"), "web,xss"),
    (("ssrf", "server side request"), "web,ssrf"),
    (("lfi", "rfi", "traversal", "..%2f", "etc/passwd"), "web,fileread"),
    (("hydra", "spray", "bruteforce", "password spray"), "creds,spray"),
    (("hashdump", "lsass", "mimikatz", "ntds", "secretsdump"), "creds,dump"),
    (("hashcat", "john", "crack"), "creds,crack"),
    (("sudo", "suid", "gtfobins", "privesc", "privilege escalation"), "privesc"),
    (("kernel", "cve-", "exploit", "msfconsole", "metasploit"), "exploit,cve"),
    (("beacon", "c2", "listener", "reverse shell", "payload"), "c2,payload"),
    (("persistence", "cron", "scheduled task", "startup"), "persistence"),
    (("tunnel", "chisel", "proxychains", "socks", "pivot", "portfwd"), "pivot,tunnel"),
    (("flag", "proof", "loot", "capture"), "evidence,loot"),
)

_LOCK = threading.RLock()
_shared: LazyHebb | None = None
_shared_lock = threading.Lock()
_last_recall: dict[str, Any] = {"count": 0, "hops": 0, "ms": 0.0}

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS hebb_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL UNIQUE,
    agent_id TEXT NOT NULL DEFAULT '',
    phase TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL,
    sem_tags TEXT NOT NULL DEFAULT '',
    private INTEGER NOT NULL DEFAULT 0,
    ts REAL NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS hebb_fts USING fts5(
    content, sem_tags, tokenize='porter unicode61'
);
CREATE TRIGGER IF NOT EXISTS hebb_fts_ai AFTER INSERT ON hebb_memories BEGIN
    INSERT INTO hebb_fts(rowid, content, sem_tags) VALUES (new.id, new.content, new.sem_tags);
END;
CREATE TRIGGER IF NOT EXISTS hebb_fts_ad AFTER DELETE ON hebb_memories BEGIN
    DELETE FROM hebb_fts WHERE rowid = old.id;
END;
CREATE TABLE IF NOT EXISTS hebb_edges (
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL,
    w REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY (src, dst)
);
"""


def default_db_path() -> Path:
    """Return the default database path under sessions/lazy."""
    return Path("sessions") / "lazy" / DB_FILENAME


def parse_sem_tags(content: str) -> tuple[str, str]:
    """Split a ``| sem:`` suffix off content.

    Args:
        content: Raw text possibly ending with ``| sem: tag1, tag2``.

    Returns:
        Tuple ``(content_without_suffix, sem_tags_csv)``.
    """
    text = str(content or "").strip()
    match = SEM_SUFFIX_RE.search(text)
    if not match:
        return text, ""
    tags = WHITESPACE_RE.sub(" ", match.group("tags")).strip(", ")
    return text[: match.start()].rstrip(" |"), tags[:SEM_TAGS_MAX_CHARS]


def auto_seed_tags(content: str) -> str:
    """Derive semantic tags from content keywords without any model.

    Args:
        content: Raw memory text.

    Returns:
        Comma-separated tag list (may be empty).
    """
    text = str(content or "").lower()
    if not text:
        return ""
    found: list[str] = []
    for needles, tags in SEM_SEED_MAP:
        for needle in needles:
            if needle in text:
                found.append(tags)
                break
    ordered: list[str] = []
    for group in found:
        for tag in group.split(","):
            if tag not in ordered:
                ordered.append(tag)
    return ",".join(ordered[:8])


def _fts_query(intent: str) -> str:
    """Build a safe OR-of-quoted-tokens FTS5 MATCH expression."""
    tokens = TOKEN_RE.findall(str(intent or ""))[:MAX_QUERY_TOKENS]
    if not tokens:
        return ""
    return " OR ".join(f'"{token}"' for token in tokens)


class LazyHebb:
    """Zero-inference memory store: FTS5 recall + hebbian edges + firewall.

    Args:
        db_path: Database file path; defaults to ``sessions/lazy/hebb.sqlite``.
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._target = (Path(db_path) if db_path else default_db_path()).resolve()
        self._target.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()

    def _conn(self) -> sqlite3.Connection:
        """Return the per-thread connection with schema and WAL applied."""
        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(str(self._target), timeout=15.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=15000")
            conn.executescript(_SCHEMA_SQL)
            conn.commit()
            self._local.conn = conn
        return conn

    def store(
        self,
        content: str,
        agent_id: str = "engine",
        phase: str = "",
        sem_tags: str = "",
        private: bool = False,
        auto_seed: bool = True,
    ) -> str:
        """Persist one memory with write-time semantic seeding.

        Duplicate ``(agent_id, content)`` pairs are collapsed: the
        existing uid is returned and no new row is written.

        Args:
            content: Memory text (``| sem:`` suffix parsed when present).
            agent_id: Writer identity (worker, tool, operator).
            phase: Kill-chain phase label.
            sem_tags: Explicit tags; ``| sem:`` suffix wins over this.
            private: When True the row is firewalled from shared recall.
            auto_seed: Also append keyword-derived tags (no model).

        Returns:
            The memory uid (existing when duplicated), or an empty string
            on any error.
        """
        try:
            body, suffix_tags = parse_sem_tags(content)
            tags = (suffix_tags or str(sem_tags or "")).strip(", ")
            if auto_seed:
                extra = auto_seed_tags(body)
                for tag in extra.split(","):
                    if tag and tag not in tags:
                        tags = f"{tags},{tag}" if tags else tag
            with _LOCK:
                conn = self._conn()
                existing = conn.execute(
                    "SELECT uid FROM hebb_memories WHERE agent_id = ? AND content = ? LIMIT 1",
                    (str(agent_id or "")[:AGENT_MAX_CHARS], str(body or "")[:CONTENT_MAX_CHARS]),
                ).fetchone()
                if existing:
                    return str(existing[0])
                uid = uuid.uuid4().hex[:16]
                conn.execute(
                    "INSERT INTO hebb_memories (uid, agent_id, phase, content, sem_tags, private, ts)"
                    " VALUES (?,?,?,?,?,?,?)",
                    (
                        uid,
                        str(agent_id or "")[:AGENT_MAX_CHARS],
                        str(phase or "")[:PHASE_MAX_CHARS],
                        str(body or "")[:CONTENT_MAX_CHARS],
                        tags[:SEM_TAGS_MAX_CHARS],
                        1 if private else 0,
                        time.time(),
                    ),
                )
                conn.commit()
                self._prune_if_needed()
            return uid
        except Exception:
            return ""

    def spark(self, intent: str, top_k: int = DEFAULT_TOP_K, include_private: bool = False) -> list[dict[str, Any]]:
        """Recall memories for an intent without any inference step.

        BM25 FTS5 ranking seeds neurons, one hop over hebbian edges adds
        propagated activation, then k-WTA keeps the top winners. Edges
        among winners are strengthened (fire together, wire together).

        Args:
            intent: Free text goal/query.
            top_k: Max winners returned.
            include_private: Include firewalled rows (operator only).

        Returns:
            Winner mappings with ``content``, ``sem_tags``, ``phase``,
            ``agent_id``, ``ts``, ``score`` and ``hops``.
        """
        winners = self._spark_full(intent, top_k, include_private)
        return [{k: v for k, v in winner.items() if k != "id"} for winner in winners]

    def _spark_full(
        self, intent: str, top_k: int = DEFAULT_TOP_K, include_private: bool = False
    ) -> list[dict[str, Any]]:
        """Recall winners keeping internal row ids for graph operations."""
        try:
            query = _fts_query(intent)
            if not query:
                return []
            with _LOCK:
                rows = self._recall_rows(query, include_private)
                if not rows:
                    return []
                seeds = rows[: max(1, int(top_k)) * SEED_MULTIPLIER]
                winners = self._spread(seeds, top_k)
                self._strengthen([winner["id"] for winner in winners])
                self._conn().commit()
            return winners
        except Exception:
            return []

    def _recall_rows(self, query: str, include_private: bool) -> list[dict[str, Any]]:
        """Return BM25-ranked seed rows, preferring FTS5 with LIKE fallback."""
        conn = self._conn()
        firewall_clause = "" if include_private else " AND m.private = 0"
        try:
            sql = (
                "SELECT m.id, m.uid, m.agent_id, m.phase, m.content, m.sem_tags, m.private, m.ts"
                " FROM hebb_fts f JOIN hebb_memories m ON m.id = f.rowid"
                f" WHERE hebb_fts MATCH ?{firewall_clause} ORDER BY rank"
            )
            return [dict(row) for row in conn.execute(sql, (query,)).fetchall()]
        except Exception:
            tokens = FTS_SAFE_RE.sub(" ", query).split()[:MAX_QUERY_TOKENS]
            if not tokens:
                return []
            like_clause = " OR ".join("m.content LIKE ? OR m.sem_tags LIKE ?" for _ in tokens)
            params: list[Any] = []
            for token in tokens:
                params += [f"%{token}%"] * 2
            sql = (
                "SELECT m.id, m.uid, m.agent_id, m.phase, m.content, m.sem_tags, m.private, m.ts"
                f" FROM hebb_memories m WHERE ({like_clause}){firewall_clause}"
                " ORDER BY m.id DESC"
            )
            return [dict(row) for row in conn.execute(sql, params).fetchall()]

    def _spread(self, seeds: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        """One-hop spreading activation over hebbian edges (k-WTA winner list)."""
        conn = self._conn()
        base_max = float(len(seeds)) or 1.0
        scored: dict[int, dict[str, Any]] = {}
        for index, row in enumerate(seeds):
            row = dict(row)
            row["score"] = 1.0 - (index / base_max) * 0.5
            row["hops"] = 0
            scored[row["id"]] = row
        for row in seeds:
            seed = scored.get(row["id"])
            if seed is None:
                continue
            try:
                edges = conn.execute(
                    "SELECT CASE WHEN src = ? THEN dst ELSE src END AS peer, w FROM hebb_edges"
                    " WHERE src = ? OR dst = ? ORDER BY w DESC LIMIT ?",
                    (row["id"], row["id"], row["id"], MAX_EDGE_FAN),
                ).fetchall()
            except Exception:
                continue
            for peer, weight in edges:
                if peer in scored:
                    continue
                neighbour = self._load_row(peer)
                if neighbour is None:
                    continue
                scored[peer] = {
                    **neighbour,
                    "score": seed["score"] * PROPAGATION_GAIN * float(weight or 0.0),
                    "hops": 1,
                }
        winners = sorted(scored.values(), key=lambda item: (-item["score"], item["id"]))[: max(1, int(top_k))]
        return winners

    def _load_row(self, memory_id: int) -> dict[str, Any] | None:
        """Load one row by id, applying the private firewall."""
        try:
            row = (
                self._conn()
                .execute(
                    "SELECT id, uid, agent_id, phase, content, sem_tags, private, ts"
                    " FROM hebb_memories WHERE id = ? AND private = 0",
                    (memory_id,),
                )
                .fetchone()
            )
        except Exception:
            return None
        return dict(row) if row else None

    def _strengthen(self, winner_ids: list[int]) -> None:
        """Increment co-activation edge weights among the winners."""
        conn = self._conn()
        ids = sorted(set(int(i) for i in winner_ids))[: DEFAULT_TOP_K * 2]
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                src, dst = ids[i], ids[j]
                try:
                    conn.execute(
                        "INSERT INTO hebb_edges (src, dst, w) VALUES (?,?,?)"
                        " ON CONFLICT(src, dst) DO UPDATE SET w = MIN(?, w + ?)",
                        (src, dst, LEARNING_RATE, EDGE_WEIGHT_CAP, LEARNING_RATE),
                    )
                except Exception:
                    return
        self._prune_edges_if_needed(conn)

    def _prune_edges_if_needed(self, conn: sqlite3.Connection) -> None:
        """Enforce the edge cap, weakest first (memory does not bloat)."""
        try:
            count = int(conn.execute("SELECT COUNT(*) FROM hebb_edges").fetchone()[0])
            overflow = count - MAX_EDGES
            if overflow <= 0:
                return
            conn.execute(
                "DELETE FROM hebb_edges WHERE rowid IN ( SELECT rowid FROM hebb_edges ORDER BY w ASC LIMIT ?)",
                (max(overflow, EDGE_PRUNE_BATCH),),
            )
        except Exception:
            return

    def bridge(self, topic_a: str, topic_b: str, max_hops: int = 6) -> list[str]:
        """Find the shortest co-activation path between two intents.

        Dijkstra over the hebbian edge graph: strong edges cost less and
        a hub toll per degree keeps high-degree neurons from becoming
        oracles. Private nodes are excluded before pathfinding so no
        triangulation leak is possible.

        Args:
            topic_a: Start intent.
            topic_b: Target intent.
            max_hops: Max path length explored.

        Returns:
            Contents along the path, or an empty list when unreachable.
        """
        try:
            import heapq

            start = self._spark_full(topic_a, top_k=1)
            goal = self._spark_full(topic_b, top_k=1)
            if not start or not goal:
                return []
            start_id, goal_id = int(start[0]["id"]), int(goal[0]["id"])
            if start_id == goal_id:
                return [str(start[0]["content"])]
            adjacency, private_ids = self._adjacency()
            if start_id in private_ids or goal_id in private_ids:
                return []
            dist = {start_id: 0.0}
            hops = {start_id: 0}
            prev: dict[int, int] = {}
            heap: list[tuple[float, int, int]] = [(0.0, 0, start_id)]
            while heap:
                cost, depth, node = heapq.heappop(heap)
                if node == goal_id:
                    break
                if depth >= max_hops:
                    continue
                if cost > dist.get(node, float("inf")) + 1e-9:
                    continue
                for peer, weight in sorted(adjacency.get(node, []), key=lambda item: -item[1])[:MAX_EDGE_FAN]:
                    edge_cost = (
                        cost + (EDGE_WEIGHT_CAP - float(weight or 0.0)) + HUB_TOLL * len(adjacency.get(peer, []))
                    )
                    next_depth = depth + 1
                    if edge_cost < dist.get(peer, float("inf")) - 1e-9 or (
                        abs(edge_cost - dist.get(peer, float("inf"))) < 1e-9 and next_depth < hops.get(peer, 10**9)
                    ):
                        dist[peer] = edge_cost
                        hops[peer] = next_depth
                        prev[peer] = node
                        heapq.heappush(heap, (edge_cost, next_depth, peer))
            if goal_id not in dist:
                return []
            path = [goal_id]
            while path[-1] != start_id:
                parent = prev.get(path[-1])
                if parent is None:
                    return []
                path.append(parent)
            path.reverse()
            contents: list[str] = []
            for memory_id in path:
                row = self._load_row(memory_id)
                if row is None:
                    return []
                contents.append(str(row["content"]))
            return contents
        except Exception:
            return []

    def _adjacency(self) -> tuple[dict[int, list[tuple[int, float]]], set[int]]:
        """Load the undirected edge map plus the firewalled id set."""
        conn = self._conn()
        private_ids = {int(row[0]) for row in conn.execute("SELECT id FROM hebb_memories WHERE private = 1").fetchall()}
        adjacency: dict[int, list[tuple[int, float]]] = {}
        for src, dst, weight in conn.execute("SELECT src, dst, w FROM hebb_edges").fetchall():
            if int(src) in private_ids or int(dst) in private_ids:
                continue
            adjacency.setdefault(int(src), []).append((int(dst), float(weight or 0.0)))
            adjacency.setdefault(int(dst), []).append((int(src), float(weight or 0.0)))
        return adjacency, private_ids

    def stats(self) -> dict[str, Any]:
        """Return row, edge and firewall counters for dashboards."""
        try:
            conn = self._conn()
            memories = int(conn.execute("SELECT COUNT(*) FROM hebb_memories").fetchone()[0])
            private = int(conn.execute("SELECT COUNT(*) FROM hebb_memories WHERE private = 1").fetchone()[0])
            edges = int(conn.execute("SELECT COUNT(*) FROM hebb_edges").fetchone()[0])
            return {"memories": memories, "private": private, "edges": edges, "db": str(self._target)}
        except Exception:
            return {"memories": 0, "private": 0, "edges": 0, "db": str(self._target)}

    def forget(self, older_than_hours: float = 0.0, topic: str = "", include_private: bool = False) -> int:
        """Delete memories by age or topic. Returns the number pruned."""
        try:
            conn = self._conn()
            clauses: list[str] = []
            params: list[Any] = []
            if older_than_hours > 0:
                clauses.append("ts < ?")
                params.append(time.time() - float(older_than_hours) * 3600.0)
            if topic:
                clauses.append("(content LIKE ? OR sem_tags LIKE ?)")
                params += [f"%{topic}%", f"%{topic}%"]
            if not include_private:
                clauses.append("private = 0")
            if not clauses:
                return 0
            where = " AND ".join(clauses)
            ids = [row[0] for row in conn.execute(f"SELECT id FROM hebb_memories WHERE {where}", params)]
            if not ids:
                return 0
            cursor = conn.execute(f"DELETE FROM hebb_memories WHERE id IN ({','.join('?' * len(ids))})", ids)
            conn.execute(
                f"DELETE FROM hebb_edges WHERE src IN ({','.join('?' * len(ids))})"
                f" OR dst IN ({','.join('?' * len(ids))})",
                ids + ids,
            )
            conn.commit()
            return max(int(cursor.rowcount or 0), 0)
        except Exception:
            return 0

    def export_markdown(self, path: str | Path) -> int:
        """Write memories as ``| sem:``-suffixed Markdown lines.

        Args:
            path: Destination ``.md`` file.

        Returns:
            Number of rows exported.
        """
        try:
            rows = (
                self._conn()
                .execute(
                    "SELECT uid, agent_id, phase, content, sem_tags, private FROM hebb_memories"
                    " ORDER BY id ASC LIMIT ?",
                    (MAX_EXPORT_ROWS,),
                )
                .fetchall()
            )
            lines = ["# lazyhebb memory export", ""]
            for uid, agent_id, phase, content, sem_tags, private in rows:
                status = "P" if private else "V"
                suffix = f" | sem: {sem_tags}" if sem_tags else ""
                lines.append(f"- **{uid} `[{status}]` ({agent_id}/{phase or 'none'}):** {content}{suffix}")
            Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
            return len(rows)
        except Exception:
            return 0

    def import_markdown(self, path: str | Path) -> int:
        """Import ``| sem:``-suffixed Markdown bullet lines as memories.

        Args:
            path: Source ``.md`` file with ``- **code [V]:** text | sem: tags`` lines.

        Returns:
            Number of rows imported.
        """
        try:
            text = Path(path).read_text(encoding="utf-8", errors="replace")
        except Exception:
            return 0
        imported = 0
        for raw in text.splitlines():
            line = raw.strip()
            if not line.startswith("- "):
                continue
            body, suffix_tags = parse_sem_tags(line[2:])
            body = re.sub(r"^\*\*[^*]+\*\*\s*", "", body)
            if not body:
                continue
            if self.store(body, agent_id="import", sem_tags=suffix_tags):
                imported += 1
        return imported

    def _prune_if_needed(self) -> None:
        """Enforce the hard row cap, oldest first, edges included."""
        conn = self._conn()
        count = int(conn.execute("SELECT COUNT(*) FROM hebb_memories").fetchone()[0])
        overflow = count - MAX_ROWS
        if overflow > 0:
            stale = [
                row[0]
                for row in conn.execute("SELECT id FROM hebb_memories ORDER BY id ASC LIMIT ?", (overflow,)).fetchall()
            ]
            conn.execute(f"DELETE FROM hebb_memories WHERE id IN ({','.join('?' * len(stale))})", stale)
            conn.execute(
                f"DELETE FROM hebb_edges WHERE src IN ({','.join('?' * len(stale))})"
                f" OR dst IN ({','.join('?' * len(stale))})",
                stale + stale,
            )
            conn.commit()


def shared_hebb() -> LazyHebb:
    """Return the process-wide LazyHebb over the default path."""
    global _shared
    with _shared_lock:
        if _shared is None:
            _shared = LazyHebb()
        return _shared


def remember_outcome(event: dict[str, Any]) -> str:
    """Store a loop outcome as a memory (auto-seeded, never raises).

    Args:
        event: Outcome mapping with ``title``, ``host``/``target``,
            ``task_id``, ``kind`` and ``metadata``.

    Returns:
        The memory uid, or an empty string when nothing was stored.
    """
    try:
        metadata = event.get("metadata") or {}
        title = str(event.get("title", "") or "").strip()
        if not title:
            return ""
        host = str(event.get("host", "") or event.get("target", "") or "").strip()
        task = str(event.get("task_id", "") or "").strip()
        worker = str(metadata.get("worker", "") or event.get("source", "") or "engine").strip()
        content = f"{title} ({host}) task={task} worker={worker}" if host else title
        return shared_hebb().store(
            content=content,
            agent_id=worker[:AGENT_MAX_CHARS],
            phase=str(event.get("kind", "") or "")[:PHASE_MAX_CHARS],
        )
    except Exception:
        return ""


def last_recall() -> dict[str, Any]:
    """Return stats of the most recent :func:`hebb_prompt_context` call.

    Returns:
        Mapping with ``count`` (winners injected), ``hops`` (winners
        found via spreading activation) and ``ms`` (wall time).
    """
    return dict(_last_recall)


def hebb_prompt_context(intent: str, top_k: int = 5) -> str:
    """Render recall winners as a prompt-ready intel line.

    Args:
        intent: Current goal or plan text.
        top_k: Max memories rendered.

    Returns:
        One ``Hebb intel:`` line, or an empty string when silent. The
        caller fences the text as untrusted data before it reaches an LLM.
    """
    try:
        from modules.orchestrator_config import hebb_config

        config = hebb_config()
        if not config.get("enabled"):
            return ""
        limit = max(1, int(config.get("max_memories", top_k) or top_k))
        started = time.monotonic()
        winners = shared_hebb().spark(intent, top_k=limit)
        elapsed_ms = round((time.monotonic() - started) * 1000.0, 1)
        _last_recall["count"] = len(winners)
        _last_recall["hops"] = sum(1 for winner in winners if winner.get("hops"))
        _last_recall["ms"] = elapsed_ms
        if not winners:
            return ""
        parts = [
            f"[{w.get('phase') or 'none'}|{w.get('agent_id', '?')}] {str(w.get('content', ''))[:90]}"
            f" (sem: {str(w.get('sem_tags', ''))[:60]})"
            for w in winners
        ]
        rendered = "Hebb intel: " + " | ".join(parts)
        return rendered[:HEBB_CONTEXT_MAX_CHARS]
    except Exception:
        return ""


def hebb_stats_payload() -> str:
    """Return compact JSON stats for dashboards and MCP tools."""
    return json.dumps(shared_hebb().stats())
