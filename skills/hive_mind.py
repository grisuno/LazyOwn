#!/usr/bin/env python3
"""
skills/hive_mind.py — LazyOwn Borg Hive Mind
==============================================
Multi-agent cognitive architecture where Claude (MCP) is the Queen/Mainframe
and Groq/Ollama agents are satellite drones executing in parallel.

Architecture
------------
  HiveMemory      — Unified ChromaDB (semantic) + SQLite (episodic) + Parquet (long-term)
  QueenBrain      — Orchestrator: plan -> delegate -> synthesize (Claude is here via MCP)
  DronePool       — Parallel Groq/Ollama agents with specialised roles
  HiveBus         — In-memory message bus between queen and drones
  HiveMind        — Top-level coordinator, exposed as MCP tools

Memory layers
-------------
  working    — current task context (dict in memory, shared via bus)
  episodic   — SQLite FTS5: events, commands, outcomes per session
  semantic   — ChromaDB vectors: similarity search across all agents
  longterm   — Parquet: compressed historical knowledge

Drone roles
-----------
  recon      — host/port/service discovery
  exploit    — vulnerability analysis and exploitation
  analyze    — log/output analysis, pattern detection
  cred       — credential hunting and cracking
  lateral    — lateral movement and pivoting
  report     — synthesis and documentation
  generic    — any goal (default)

MCP tools added to lazyown_mcp.py
----------------------------------
  lazyown_hive_spawn     — spawn N drones for a goal (parallel)
  lazyown_hive_status    — hive-wide status + memory stats
  lazyown_hive_recall    — semantic recall from ChromaDB
  lazyown_hive_plan      — queen generates task decomposition
  lazyown_hive_result    — get aggregated drone results
  lazyown_hive_forget    — prune hive memory by topic/age

Usage
-----
  from hive_mind import get_hive
  hive = get_hive()
  run_ids = hive.queen.plan_and_dispatch("Enumerate AD on 10.10.11.78")
  status  = hive.status()
  result  = hive.collect(run_ids)

  python3 skills/hive_mind.py spawn "Enumerate SMB" --drones 3 --wait
  python3 skills/hive_mind.py status
  python3 skills/hive_mind.py recall "kerberos hash"
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import sys
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ── Paths ──────────────────────────────────────────────────────────────────────
# Mirror lazyown_mcp.py: respect LAZYOWN_DIR env override for consistency.

SKILLS_DIR   = Path(__file__).parent
LAZYOWN_DIR  = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
SESSIONS_DIR = LAZYOWN_DIR / "sessions"
PARQUETS_DIR = LAZYOWN_DIR / "parquets"
HIVE_DIR     = SESSIONS_DIR / "hive"
HIVE_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SKILLS_DIR))
sys.path.insert(0, str(LAZYOWN_DIR / "modules"))

log = logging.getLogger("hive_mind")

# ── Optional ChromaDB ──────────────────────────────────────────────────────────

try:
    import chromadb
    from chromadb.config import Settings as _ChromaSettings
    _CHROMA_OK = True
except ImportError:
    _CHROMA_OK = False

# ── Optional sentence-transformers (fully lazy — import + model deferred) ─────
# torch takes 10-15s to import. We must NOT import sentence_transformers at
# module level — it would block the MCP server startup handshake. Both the
# import and the model instantiation happen on the first call to _embed().

_EMBED_MODEL      = None   # populated lazily
_EMBED_MODEL_LOCK = threading.Lock()
_EMBED_CHECKED    = False  # True after first availability check
_EMBED_OK         = False  # set after first successful import


def _get_embed_model():
    """Return the embedding model. Imports sentence_transformers + loads model
    on first call. Thread-safe. Returns None if unavailable."""
    global _EMBED_MODEL, _EMBED_OK, _EMBED_CHECKED
    if _EMBED_MODEL is not None:
        return _EMBED_MODEL
    with _EMBED_MODEL_LOCK:
        if _EMBED_MODEL is not None:
            return _EMBED_MODEL
        if _EMBED_CHECKED:
            return None
        _EMBED_CHECKED = True
        try:
            from sentence_transformers import SentenceTransformer as _ST  # noqa: PLC0415
            _EMBED_MODEL = _ST("all-MiniLM-L6-v2")
            _EMBED_OK    = True
            log.info("sentence-transformers model loaded")
        except Exception as exc:
            log.debug("sentence-transformers unavailable: %s", exc)
    return _EMBED_MODEL

# ── Optional numpy ────────────────────────────────────────────────────────────

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 0 — Interfaces (I — Interface Segregation, O — Open/Closed)
# ─────────────────────────────────────────────────────────────────────────────


class IReadableMemory(ABC):
    """Read-only contract for memory stores."""

    @abstractmethod
    def recall(self, query: str, top_k: int = 10) -> List[Dict]:
        """Return top_k items matching query."""


class IWritableMemory(ABC):
    """Write-only contract for memory stores."""

    @abstractmethod
    def store(self, content: str, **meta: Any) -> str:
        """Persist content and return an opaque event_id."""


class IMemoryStore(IReadableMemory, IWritableMemory):
    """
    Combined readable + writable memory store.

    Concrete subclasses (EpisodicStore, SemanticStore, LongtermStore) all
    satisfy the Liskov Substitution Principle — they can replace each other
    in any context that expects IMemoryStore.
    """


class ICommandRunner(ABC):
    """Contract for executing a LazyOwn shell command and returning its output."""

    @abstractmethod
    def run(self, command: str, timeout: int) -> str:
        """Execute command within timeout seconds and return text output."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier for this runner."""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1A — EpisodicStore  (S — Single Responsibility: SQLite FTS5 only)
# ─────────────────────────────────────────────────────────────────────────────

class EpisodicStore(IMemoryStore):
    """
    SQLite-backed episodic memory with FTS5 full-text search.

    Responsible for: schema creation, insert, FTS keyword recall, forget.
    Nothing else.
    """

    _DDL_STMTS = [
        """CREATE TABLE IF NOT EXISTS hive_events (
            rowid       INTEGER PRIMARY KEY AUTOINCREMENT,
            id          TEXT NOT NULL UNIQUE,
            agent_id    TEXT NOT NULL,
            role        TEXT NOT NULL DEFAULT 'generic',
            event_type  TEXT NOT NULL DEFAULT 'observation',
            content     TEXT NOT NULL,
            meta_json   TEXT NOT NULL DEFAULT '{}',
            ts          REAL NOT NULL,
            session_tag TEXT NOT NULL DEFAULT ''
        )""",
        "CREATE VIRTUAL TABLE IF NOT EXISTS hive_fts USING fts5(content, tokenize='porter ascii')",
        """CREATE TRIGGER IF NOT EXISTS hive_ai AFTER INSERT ON hive_events BEGIN
            INSERT INTO hive_fts(rowid, content) VALUES (new.rowid, new.content);
        END""",
    ]

    def __init__(self, db_path: Optional[Path] = None) -> None:
        import sqlite3
        self._db_path = db_path or (HIVE_DIR / "hive_memory.db")
        self._lock    = threading.RLock()
        self._conn    = self._connect()

    def _connect(self):
        import sqlite3
        conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        for stmt in self._DDL_STMTS:
            try:
                conn.execute(stmt)
            except Exception:
                pass
        conn.commit()
        return conn

    # IWritableMemory ---------------------------------------------------------

    def store(
        self,
        content: str,
        agent_id: str = "queen",
        role: str = "generic",
        event_type: str = "observation",
        meta: Optional[Dict] = None,
        session_tag: str = "",
        **_ignored: Any,
    ) -> str:
        """Insert a row into hive_events and return event_id."""
        event_id  = uuid.uuid4().hex
        ts        = time.time()
        meta_json = json.dumps(meta or {}, ensure_ascii=False)

        with self._lock:
            try:
                self._conn.execute(
                    """INSERT OR IGNORE INTO hive_events
                       (id, agent_id, role, event_type, content, meta_json, ts, session_tag)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (event_id, agent_id, role, event_type, content[:8000],
                     meta_json, ts, session_tag),
                )
                self._conn.commit()
            except Exception as exc:
                log.error("SQLite store error: %s", exc)
        return event_id

    # IReadableMemory ---------------------------------------------------------

    def recall(
        self,
        query: str,
        top_k: int = 10,
        role: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[Dict]:
        """Keyword search via FTS5. Optionally filter by role or event_type."""
        with self._lock:
            try:
                extra_filters: List[str] = []
                params: List[Any] = [query]
                if role:
                    extra_filters.append("e.role = ?")
                    params.append(role)
                if event_type:
                    extra_filters.append("e.event_type = ?")
                    params.append(event_type)
                params.append(top_k)
                extra_where = ("AND " + " AND ".join(extra_filters)) if extra_filters else ""
                sql = f"""
                    SELECT e.id, e.agent_id, e.role, e.event_type,
                           e.content, e.meta_json, e.ts
                    FROM hive_events e
                    JOIN hive_fts f ON f.rowid = e.rowid
                    WHERE hive_fts MATCH ? {extra_where}
                    ORDER BY rank LIMIT ?
                """
                cur = self._conn.execute(sql, params)
                rows = cur.fetchall()
                return [
                    {
                        "id": r[0], "agent_id": r[1], "role": r[2],
                        "event_type": r[3], "content": r[4][:500],
                        "meta": json.loads(r[5]), "ts": r[6],
                    }
                    for r in rows
                ]
            except Exception as exc:
                log.error("Recall episodic error: %s", exc)
                return []

    # Additional helpers ------------------------------------------------------

    def stats(self) -> Dict[str, Any]:
        """Return row counts for status reporting."""
        with self._lock:
            total = self._conn.execute(
                "SELECT COUNT(*) FROM hive_events"
            ).fetchone()[0]
            agents = self._conn.execute(
                "SELECT COUNT(DISTINCT agent_id) FROM hive_events"
            ).fetchone()[0]
        return {"episodic_events": total, "unique_agents": agents}

    def forget(self, older_than_hours: float = 24.0, topic: str = "") -> int:
        """Delete old or topic-matching rows. Returns rows deleted."""
        cutoff = time.time() - older_than_hours * 3600
        with self._lock:
            if topic:
                cur = self._conn.execute(
                    "DELETE FROM hive_events WHERE ts < ? AND content LIKE ?",
                    (cutoff, f"%{topic}%"),
                )
            else:
                cur = self._conn.execute(
                    "DELETE FROM hive_events WHERE ts < ?", (cutoff,)
                )
            self._conn.commit()
            return cur.rowcount


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1B — SemanticStore  (S — Single Responsibility: ChromaDB only)
# ─────────────────────────────────────────────────────────────────────────────

class SemanticStore(IMemoryStore):
    """
    ChromaDB-backed vector similarity store.

    Falls back to the provided episodic_fallback when ChromaDB is unavailable.
    Responsible for: embedding, upsert into ChromaDB, similarity recall.
    Nothing else.
    """

    def __init__(
        self,
        chroma_dir: Optional[Path] = None,
        episodic_fallback: Optional[EpisodicStore] = None,
    ) -> None:
        self._episodic  = episodic_fallback
        self._collection = self._init_chroma(chroma_dir or (HIVE_DIR / "chroma"))

    def _init_chroma(self, chroma_dir: Path):
        if not _CHROMA_OK:
            return None
        try:
            client = chromadb.PersistentClient(path=str(chroma_dir))
            return client.get_or_create_collection(
                name="hive_memory",
                metadata={"hnsw:space": "cosine"},
            )
        except Exception as exc:
            log.warning("ChromaDB init failed: %s", exc)
            return None

    @property
    def available(self) -> bool:
        """True when ChromaDB is operational."""
        return self._collection is not None

    # IWritableMemory ---------------------------------------------------------

    def store(
        self,
        content: str,
        agent_id: str = "queen",
        role: str = "generic",
        event_type: str = "observation",
        meta: Optional[Dict] = None,
        session_tag: str = "",
        event_id: Optional[str] = None,
        **_ignored: Any,
    ) -> str:
        """Add a document to ChromaDB. Returns the event_id used."""
        eid = event_id or uuid.uuid4().hex
        if self._collection is None:
            if self._episodic is not None:
                return self._episodic.store(
                    content, agent_id=agent_id, role=role,
                    event_type=event_type, meta=meta, session_tag=session_tag,
                )
            return eid

        ts = time.time()
        try:
            embedding = self._embed(content)
            self._collection.add(
                ids=[eid],
                documents=[content[:2000]],
                embeddings=[embedding] if embedding else None,
                metadatas=[{
                    "agent_id":   agent_id,
                    "role":       role,
                    "event_type": event_type,
                    "ts":         str(ts),
                    "session":    session_tag,
                }],
            )
        except Exception as exc:
            log.debug("ChromaDB store error: %s", exc)
        return eid

    # IReadableMemory ---------------------------------------------------------

    def recall(
        self,
        query: str,
        top_k: int = 8,
        where: Optional[Dict] = None,
    ) -> List[Dict]:
        """Vector similarity search. Falls back to episodic FTS if unavailable."""
        if self._collection is None:
            if self._episodic is not None:
                return self._episodic.recall(query, top_k)
            return []
        try:
            embedding = self._embed(query)
            kw: Dict[str, Any] = {
                "n_results": top_k,
                "include": ["documents", "metadatas", "distances"],
            }
            if embedding:
                kw["query_embeddings"] = [embedding]
            else:
                kw["query_texts"] = [query]
            if where:
                kw["where"] = where
            res   = self._collection.query(**kw)
            docs  = res.get("documents",  [[]])[0]
            metas = res.get("metadatas",  [[]])[0]
            dists = res.get("distances",  [[]])[0]
            ids_  = res.get("ids",        [[]])[0]
            return [
                {
                    "id":         ids_[i],
                    "content":    docs[i],
                    "meta":       metas[i],
                    "similarity": round(1.0 - dists[i], 4),
                }
                for i in range(len(docs))
            ]
        except Exception as exc:
            log.debug("ChromaDB recall error: %s — falling back to FTS", exc)
            if self._episodic is not None:
                return self._episodic.recall(query, top_k)
            return []

    def count(self) -> int:
        """Return number of vectors stored."""
        if self._collection is None:
            return 0
        try:
            return self._collection.count()
        except Exception:
            return 0

    # Internal ----------------------------------------------------------------

    def _embed(self, text: str) -> Optional[List[float]]:
        model = _get_embed_model()
        if model is None:
            return None
        try:
            vec = model.encode(text[:512], show_progress_bar=False)
            if _NUMPY_OK:
                return vec.tolist()
            return list(vec)
        except Exception:
            return None


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1C — LongtermStore  (S — Single Responsibility: Parquet recall only)
# ─────────────────────────────────────────────────────────────────────────────

class LongtermStore(IMemoryStore):
    """
    Read-only keyword recall from Parquet knowledge files.

    store() is a no-op (Parquet files are managed by lazyown_parquet_db).
    Responsible for: delegating keyword search to lazyown_parquet_db.
    Nothing else.
    """

    def store(self, content: str, **_meta: Any) -> str:  # type: ignore[override]
        """Parquet store is read-only from here. Returns empty string."""
        return ""

    def recall(self, query: str, top_k: int = 10) -> List[Dict]:
        """Keyword search across Parquet knowledge files."""
        try:
            from lazyown_parquet_db import get_pdb
            pdb = get_pdb()
            if pdb is None:
                return []
            if hasattr(pdb, "query_knowledge"):
                rows = pdb.query_knowledge(keyword=query, limit=top_k)
            else:
                all_rows = pdb.query_session(limit=50)
                q_low = query.lower()
                rows = [
                    r for r in all_rows
                    if q_low in str(r.get("command", "")).lower()
                    or q_low in str(r.get("outcome", "")).lower()
                ][:top_k]
            return [
                {
                    "id":      r.get("id", ""),
                    "content": (
                        f"[{r.get('phase', r.get('category', '?'))}] "
                        f"{r.get('command', '?')} -> {r.get('outcome', '?')}"
                    ),
                    "meta":       {"phase": r.get("phase", r.get("category", "")), "source": "parquet"},
                    "similarity": None,
                }
                for r in rows
            ]
        except Exception as exc:
            log.debug("Parquet recall error: %s", exc)
            return []


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1D — HiveMemory  (D — Dependency Inversion: injects IMemoryStore list)
# ─────────────────────────────────────────────────────────────────────────────

def build_default_hive_memory(db_path: Optional[Path] = None) -> "HiveMemory":
    """
    Factory that creates HiveMemory with the default three-layer backend.

    Callers that need a custom configuration can construct each store
    explicitly and pass them to HiveMemory directly.
    """
    episodic  = EpisodicStore(db_path=db_path)
    semantic  = SemanticStore(episodic_fallback=episodic)
    longterm  = LongtermStore()
    return HiveMemory(stores=[episodic, semantic, longterm],
                      episodic=episodic, semantic=semantic, longterm=longterm)


class HiveMemory:
    """
    Unified three-layer memory shared across all hive agents.

    Composes EpisodicStore, SemanticStore, and LongtermStore.
    Handles cross-layer deduplication in recall().

    Dependency Inversion: concrete backends are injected via __init__.
    Open/Closed: add new backends by passing extra IMemoryStore instances.
    """

    def __init__(
        self,
        stores: List[IMemoryStore],
        episodic: Optional[EpisodicStore] = None,
        semantic: Optional[SemanticStore] = None,
        longterm: Optional[LongtermStore] = None,
    ) -> None:
        self._stores   = stores
        self._episodic = episodic
        self._semantic = semantic
        self._longterm = longterm

    # ── Write ─────────────────────────────────────────────────────────────────

    def store(
        self,
        content: str,
        agent_id: str = "queen",
        role: str = "generic",
        event_type: str = "observation",
        meta: Optional[Dict] = None,
        session_tag: str = "",
    ) -> str:
        """
        Store content in all writable layers.

        Returns the event_id from the first store (episodic).
        The same id is forwarded to semantic so ChromaDB and SQLite stay aligned.
        """
        event_id: Optional[str] = None
        kwargs = dict(
            agent_id=agent_id, role=role, event_type=event_type,
            meta=meta, session_tag=session_tag,
        )

        for store in self._stores:
            if isinstance(store, LongtermStore):
                continue  # Parquet is read-only
            if event_id is None:
                event_id = store.store(content, **kwargs)
            else:
                # Forward the same event_id so ChromaDB row aligns with SQLite row
                store.store(content, event_id=event_id, **kwargs)

        return event_id or uuid.uuid4().hex

    # ── Recall — episodic (FTS) ───────────────────────────────────────────────

    def recall_episodic(
        self,
        query: str,
        top_k: int = 10,
        role: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[Dict]:
        """Keyword search across hive episodic memory."""
        if self._episodic is None:
            return []
        return self._episodic.recall(query, top_k, role=role, event_type=event_type)

    # ── Recall — semantic (ChromaDB) ─────────────────────────────────────────

    def recall_semantic(
        self,
        query: str,
        top_k: int = 8,
        where: Optional[Dict] = None,
    ) -> List[Dict]:
        """Vector similarity search in ChromaDB."""
        if self._semantic is None:
            return self.recall_episodic(query, top_k)
        return self._semantic.recall(query, top_k, where=where)

    # ── Recall — long-term (Parquet) ─────────────────────────────────────────

    def recall_longterm(self, query: str, top_k: int = 10) -> List[Dict]:
        """Keyword search across Parquet knowledge files."""
        if self._longterm is None:
            return []
        return self._longterm.recall(query, top_k)

    # ── Unified recall (all layers) ──────────────────────────────────────────

    def recall(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Unified recall: semantic (ChromaDB) + episodic (SQLite) + longterm (Parquet).
        Deduplicates by content hash.
        """
        seen: set = set()
        results: List[Dict] = []

        for item in self.recall_semantic(query, top_k=top_k):
            key = hashlib.md5(item["content"][:200].encode()).hexdigest()
            if key not in seen:
                seen.add(key)
                item["layer"] = "semantic"
                results.append(item)

        for item in self.recall_longterm(query, top_k=top_k // 2 + 1):
            key = hashlib.md5(item["content"][:200].encode()).hexdigest()
            if key not in seen:
                seen.add(key)
                item["layer"] = "longterm"
                results.append(item)

        return results[:top_k]

    # ── Stats ─────────────────────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        """Return combined statistics from all layers."""
        result: Dict[str, Any] = {"chroma_enabled": _CHROMA_OK, "embed_enabled": _EMBED_OK}
        if self._episodic is not None:
            result.update(self._episodic.stats())
        result["chroma_vectors"] = self._semantic.count() if self._semantic else 0
        return result

    # ── Forget ────────────────────────────────────────────────────────────────

    def forget(self, older_than_hours: float = 24.0, topic: str = "") -> int:
        """Prune old or topic-matched entries. Returns number pruned."""
        if self._episodic is None:
            return 0
        return self._episodic.forget(older_than_hours=older_than_hours, topic=topic)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — HiveBus  (S — message passing only)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class HiveMessage:
    """A message on the hive bus."""
    msg_id:    str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    sender:    str = "queen"
    recipient: str = "*"          # "*" = broadcast
    kind:      str = "task"       # task | result | signal | heartbeat
    payload:   Dict = field(default_factory=dict)
    ts:        float = field(default_factory=time.time)


class HiveBus:
    """
    Simple thread-safe in-process message bus.
    Agents subscribe to their own mailbox (recipient == agent_id or "*").

    Single Responsibility: only message passing.
    """

    def __init__(self) -> None:
        self._lock    = threading.Lock()
        self._mailbox: Dict[str, List[HiveMessage]] = {}   # recipient -> [msgs]

    def publish(self, msg: HiveMessage) -> None:
        """Deliver msg to recipient mailbox (and to "*" broadcast)."""
        with self._lock:
            for recipient in (msg.recipient, "*"):
                self._mailbox.setdefault(recipient, []).append(msg)

    def receive(self, agent_id: str, max_msgs: int = 10) -> List[HiveMessage]:
        """Drain mailbox for agent_id (includes broadcast)."""
        with self._lock:
            direct    = self._mailbox.pop(agent_id, [])
            broadcast = self._mailbox.get("*", [])
            combined  = direct + broadcast
            return combined[:max_msgs]

    def ack_broadcast(self, agent_id: str, msg_id: str) -> None:
        """Mark a broadcast message as seen by agent_id (minimal bus — no-op)."""
        pass  # noqa: WPS420

    def pending_count(self, agent_id: str) -> int:
        """Count messages waiting for agent_id."""
        with self._lock:
            return len(self._mailbox.get(agent_id, [])) + len(self._mailbox.get("*", []))


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — DroneAgent  (satellite Groq/Ollama agent)
# ─────────────────────────────────────────────────────────────────────────────

# Role -> system prompt focus
_ROLE_FOCUS: Dict[str, str] = {
    "recon":             "You specialise in host discovery, port scanning, and service fingerprinting.",
    "exploit":           "You specialise in vulnerability analysis, CVE research, and exploitation.",
    "analyze":           "You specialise in log analysis, output parsing, and pattern detection.",
    "cred":              "You specialise in credential hunting, hash cracking, and auth bypass.",
    "lateral":           "You specialise in lateral movement, pivoting, and network traversal.",
    "report":            "You specialise in synthesising findings into structured, actionable reports.",
    "generic":           "You are a general-purpose red-team assistant.",
    # ── Specialised swarm roles ───────────────────────────────────────────────
    "stealth_specialist": (
        "You are the Stealth Specialist. Your primary concern is remaining undetected. "
        "Before recommending any command, query threat_model and reactive_suggest to "
        "estimate detection probability. If a technique carries high EDR/AV risk, "
        "propose a lower-noise alternative (LOLBas, living-off-the-land, AMSI bypass). "
        "Annotate every recommendation with its predicted log-source signature."
    ),
    "privesc_hunter": (
        "You are the Privilege Escalation Hunter. Your goal is to identify and exploit "
        "the fastest local privilege escalation path on the target. Check SUID binaries, "
        "sudo misconfigurations, writable cron jobs, service binary hijacking, and known "
        "kernel CVEs. Use linpeas/winpeas output analysis and GTFOBins lookups. "
        "Report the PoC command and required preconditions for each path found."
    ),
    "architect": (
        "You are the Architect. You maintain the engagement soul.md and the world model. "
        "After each phase, update the strategic picture: which hosts are owned, what "
        "credentials are available, and what the optimal next objective is. "
        "Generate a pivot graph narrative showing the highest-centrality nodes. "
        "Write lessons learned to hive memory after every significant finding."
    ),
}

# Role -> preferred tool subset
_ROLE_TOOLS: Dict[str, List[str]] = {
    "recon":   ["run_command", "facts_show", "bridge_suggest", "rag_query", "cve_lookup",
                "parquet_context", "memory_search", "session_status"],
    "exploit": ["run_command", "cve_lookup", "searchsploit", "bridge_suggest",
                "atomic_search", "parquet_context", "reactive_suggest", "rag_query"],
    "analyze": ["run_command", "rag_query", "memory_search", "reactive_suggest",
                "threat_model", "facts_show", "parquet_context"],
    "cred":    ["run_command", "bridge_suggest", "memory_search", "parquet_context",
                "reactive_suggest", "facts_show", "session_status"],
    "lateral": ["run_command", "bridge_suggest", "session_status", "c2_status",
                "c2_command", "reactive_suggest", "parquet_context"],
    "report":  ["run_command", "rag_query", "threat_model", "facts_show",
                "parquet_context", "task_list", "memory_search"],
    "generic": [],   # all tools
    # ── Specialised swarm roles ───────────────────────────────────────────────
    "stealth_specialist": [
        "run_command", "reactive_suggest", "threat_model", "rag_query",
        "bridge_suggest", "parquet_context", "memory_search",
    ],
    "privesc_hunter": [
        "run_command", "bridge_suggest", "atomic_search", "parquet_context",
        "reactive_suggest", "facts_show", "cve_lookup", "searchsploit",
    ],
    "architect": [
        "rag_query", "memory_search", "facts_show", "threat_model",
        "session_status", "hive_recall", "parquet_context", "task_list",
    ],
}

# Roles that require consensus approval before dispatch (high operational impact)
_HIGH_RISK_ROLES: frozenset = frozenset({"exploit", "lateral", "cred", "privesc_hunter"})


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3B — ConsensusProtocol  (S — voting logic only)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class ConsensusVote:
    """A single vote cast by a drone role during consensus evaluation."""
    voter_role:  str
    approved:    bool
    risk_score:  float   # estimated detection/operational risk in [0.0, 1.0]
    rationale:   str


class ConsensusProtocol:
    """
    Multi-drone voting gate for high-risk actions.

    Before a high-risk task (exploit, lateral, credential dump) is dispatched,
    the queen polls a panel of virtual voters — one per specialised role — and
    only proceeds when the weighted approval meets the required quorum.

    Voting model
    ------------
    - stealth_specialist : votes based on detection risk (approves if risk < threshold)
    - privesc_hunter     : votes based on whether current access level justifies the move
    - architect          : votes based on strategic alignment with current phase

    The detection risk estimate uses DetectionRiskAssessor when available,
    falling back to a static heuristic table.

    Design
    ------
    - Single Responsibility : voting logic only; no drone spawning
    - Open/Closed           : new voter roles added without modifying existing code
    - Dependency Inversion  : DetectionRiskAssessor injected, not constructed here
    """

    _DETECTION_RISK_BY_ROLE: Dict[str, float] = {
        "exploit":        0.82,
        "lateral":        0.75,
        "cred":           0.88,
        "privesc_hunter": 0.65,
    }
    _APPROVAL_QUORUM: float = 0.51   # fraction of weighted votes required

    def __init__(self, risk_assessor: Optional[Any] = None) -> None:
        self._risk_assessor = risk_assessor  # Optional DetectionRiskAssessor

    def evaluate(self, role: str, goal: str) -> Tuple[bool, List[ConsensusVote], str]:
        """
        Run the consensus vote for the given (role, goal) pair.

        Returns
        -------
        (approved: bool, votes: List[ConsensusVote], summary: str)
        """
        if role not in _HIGH_RISK_ROLES:
            return True, [], "role not subject to consensus review"

        detection_risk = self._estimate_detection_risk(role, goal)
        votes = [
            self._stealth_vote(detection_risk),
            self._privesc_hunter_vote(role, goal),
            self._architect_vote(role, goal),
        ]
        weighted_score = self._weighted_approval(votes)
        approved       = weighted_score >= self._APPROVAL_QUORUM
        summary        = (
            f"Consensus {'APPROVED' if approved else 'REJECTED'} "
            f"(weighted approval {weighted_score:.0%}, "
            f"detection_risk={detection_risk:.0%}). "
            + " | ".join(f"{v.voter_role}: {'YES' if v.approved else 'NO'}" for v in votes)
        )
        return approved, votes, summary

    # Voters ------------------------------------------------------------------

    def _stealth_vote(self, detection_risk: float) -> ConsensusVote:
        threshold = 0.70
        approved  = detection_risk < threshold
        return ConsensusVote(
            voter_role="stealth_specialist",
            approved=approved,
            risk_score=detection_risk,
            rationale=(
                f"Detection risk {detection_risk:.0%} is {'below' if approved else 'at or above'} "
                f"the {threshold:.0%} stealth threshold."
            ),
        )

    @staticmethod
    def _privesc_hunter_vote(role: str, goal: str) -> ConsensusVote:
        # Approves exploit/credential/lateral moves — these are its specialty
        approved = role in {"exploit", "lateral", "cred", "privesc_hunter"}
        return ConsensusVote(
            voter_role="privesc_hunter",
            approved=approved,
            risk_score=0.5,
            rationale=(
                "Exploitation path aligns with privilege escalation strategy."
                if approved
                else f"Role '{role}' is outside the privesc hunter's mandate."
            ),
        )

    @staticmethod
    def _architect_vote(role: str, goal: str) -> ConsensusVote:
        # Approves when the goal contains strategic keywords
        strategic_keywords = (
            "shell", "root", "admin", "system", "lateral", "cred",
            "pivot", "domain", "dc", "secretsdump", "hash",
        )
        goal_lower  = goal.lower()
        is_strategic = any(kw in goal_lower for kw in strategic_keywords)
        return ConsensusVote(
            voter_role="architect",
            approved=is_strategic,
            risk_score=0.4,
            rationale=(
                "Goal aligns with a defined strategic phase objective."
                if is_strategic
                else "Goal does not clearly advance the engagement phase."
            ),
        )

    def _estimate_detection_risk(self, role: str, goal: str) -> float:
        if self._risk_assessor is not None:
            try:
                return self._risk_assessor.assess_probability(goal, "", role)
            except Exception:
                pass
        return self._DETECTION_RISK_BY_ROLE.get(role, 0.50)

    @staticmethod
    def _weighted_approval(votes: List[ConsensusVote]) -> float:
        """
        Weight votes by role importance:
          stealth_specialist : 0.40 (detection risk is paramount)
          privesc_hunter     : 0.30 (operational expertise)
          architect          : 0.30 (strategic alignment)
        """
        weights = {
            "stealth_specialist": 0.40,
            "privesc_hunter":     0.30,
            "architect":          0.30,
        }
        total_weight  = 0.0
        approval_weight = 0.0
        for vote in votes:
            w = weights.get(vote.voter_role, 0.0)
            total_weight += w
            if vote.approved:
                approval_weight += w
        if total_weight == 0.0:
            return 0.0
        return approval_weight / total_weight


@dataclass
class DroneState:
    """Mutable state record for a single drone instance."""
    drone_id:   str
    role:       str
    goal:       str
    backend:    str      # groq | ollama
    status:     str = "queued"   # queued|running|completed|failed
    result:     str = ""
    error:      str = ""
    started:    float = 0.0
    finished:   float = 0.0
    iterations: int = 0
    tokens_in:  int = 0
    tokens_out: int = 0


class DroneAgent:
    """
    A satellite agent running on Groq or Ollama.
    Reports back to hive memory on completion.

    Dependency Inversion: accepts an optional ICommandRunner for testability.
    """

    def __init__(
        self,
        drone_id: str,
        role: str,
        goal: str,
        backend: str,
        memory: HiveMemory,
        bus: HiveBus,
        max_iterations: int = 10,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        runner: Optional[ICommandRunner] = None,
        on_state_change: Optional[Callable[["DroneState"], None]] = None,
    ) -> None:
        self.state    = DroneState(
            drone_id=drone_id, role=role, goal=goal, backend=backend,
        )
        self._memory           = memory
        self._bus              = bus
        self._max_it           = max_iterations
        self._api_key          = api_key
        self._model            = model
        self._runner           = runner
        self._on_state_change  = on_state_change
        self._thread: Optional[threading.Thread] = None

    def _persist(self) -> None:
        """Fire the on_state_change callback if registered."""
        if self._on_state_change is not None:
            try:
                self._on_state_change(self.state)
            except Exception as exc:
                log.debug("on_state_change callback error: %s", exc)

    def start(self) -> None:
        """Spawn the drone thread."""
        self._thread = threading.Thread(
            target=self._run,
            name=f"drone-{self.state.drone_id}-{self.state.role}",
            daemon=True,
        )
        self._thread.start()

    def join(self, timeout: Optional[float] = None) -> None:
        """Block until the drone thread finishes."""
        if self._thread:
            self._thread.join(timeout=timeout)

    def _run(self) -> None:
        s = self.state
        s.status  = "running"
        s.started = time.time()
        self._persist()  # persist: queued -> running

        self._memory.store(
            content=f"[DRONE STARTED] role={s.role} goal={s.goal[:200]}",
            agent_id=s.drone_id,
            role=s.role,
            event_type="lifecycle",
        )

        try:
            from lazyown_llm import LLMBridge
            from lazyown_groq_agents import REGISTRY

            key = (
                self._api_key
                or self._load_payload_key()
                or os.environ.get("GROQ_API_KEY", "")
            )
            bridge = LLMBridge(backend=s.backend, model=self._model, api_key=key)

            tool_names = _ROLE_TOOLS.get(s.role) or list(REGISTRY.keys())
            for name in tool_names:
                if name in REGISTRY:
                    desc, params, func = REGISTRY[name]
                    bridge.register_tool(name, desc, params, func)

            hive_ctx   = self._build_hive_context()
            sys_prompt = self._build_system_prompt(list(bridge._tools.keys()), hive_ctx)

            answer = bridge.ask(
                goal=s.goal,
                max_iterations=self._max_it,
                system_prompt=sys_prompt,
            )
            s.result  = answer
            s.status  = "completed"

        except Exception as exc:
            s.error  = str(exc)
            s.status = "failed"
            answer   = f"[FAILED] {exc}"

        finally:
            s.finished = time.time()
            self._persist()  # persist: running -> completed/failed

        self._memory.store(
            content=f"[DRONE RESULT] role={s.role} goal={s.goal[:100]}\n{answer[:2000]}",
            agent_id=s.drone_id,
            role=s.role,
            event_type="result",
            meta={"status": s.status, "duration_s": round(s.finished - s.started, 2)},
        )

        self._bus.publish(HiveMessage(
            sender=s.drone_id,
            recipient="queen",
            kind="result",
            payload={
                "drone_id": s.drone_id,
                "role":     s.role,
                "goal":     s.goal[:200],
                "status":   s.status,
                "result":   answer[:4000],
                "duration": round(s.finished - s.started, 2),
            },
        ))

    def _build_hive_context(self) -> str:
        """Pull relevant memories to seed this drone's context."""
        items = self._memory.recall(self.state.goal, top_k=5)
        if not items:
            return ""
        lines = ["=== Hive Memory Context ==="]
        for item in items:
            layer = item.get("layer", "?")
            lines.append(f"[{layer}] {item['content'][:300]}")
        return "\n".join(lines)

    def _build_system_prompt(self, tool_names: List[str], hive_ctx: str) -> str:
        role_focus = _ROLE_FOCUS.get(self.state.role, _ROLE_FOCUS["generic"])
        base = (
            f"You are a LazyOwn hive-mind drone. Role: {self.state.role.upper()}.\n"
            f"{role_focus}\n"
            "Rules:\n"
            "- Use ONLY real tool output — never fabricate results.\n"
            "- After each command, analyse the output with reactive_suggest.\n"
            "- Report ALL credentials, hostnames, and access levels you find.\n"
            "- Be concise and structured.\n"
            f"Available tools: {', '.join(tool_names)}.\n"
        )
        if hive_ctx:
            base += f"\n{hive_ctx}\n"
        return base

    @staticmethod
    def _load_payload_key() -> str:
        try:
            payload = json.loads((LAZYOWN_DIR / "payload.json").read_text())
            return payload.get("api_key", "") or payload.get("groq_api_key", "")
        except Exception:
            return ""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — QueenBrain  (S — orchestration only; D — all deps injected)
# ─────────────────────────────────────────────────────────────────────────────

_DECOMPOSITION_TEMPLATES: Dict[str, List[Dict]] = {
    "enum": [
        {"role": "recon",   "goal_suffix": "— host discovery and port scanning"},
        {"role": "analyze", "goal_suffix": "— service version fingerprinting"},
        {"role": "cred",    "goal_suffix": "— anonymous access and default credentials"},
    ],
    "exploit": [
        {"role": "recon",   "goal_suffix": "— confirm target services and versions"},
        {"role": "exploit", "goal_suffix": "— CVE research and exploit selection"},
        {"role": "analyze", "goal_suffix": "— post-exploit output analysis"},
    ],
    "ad": [
        {"role": "recon",   "goal_suffix": "— AD enumeration (users, groups, GPOs)"},
        {"role": "cred",    "goal_suffix": "— Kerberoasting and AS-REP roasting"},
        {"role": "lateral", "goal_suffix": "— lateral movement and privilege escalation"},
        {"role": "report",  "goal_suffix": "— synthesis of AD attack path"},
    ],
    "generic": [
        {"role": "recon",   "goal_suffix": ""},
        {"role": "analyze", "goal_suffix": ""},
        {"role": "report",  "goal_suffix": "— synthesis"},
    ],
}


def _classify_objective(goal: str) -> str:
    """Return one of 'ad', 'exploit', 'enum', 'generic' based on goal keywords."""
    g = goal.lower()
    if any(k in g for k in ("ad ", "active directory", "kerberos", "ldap", "domain")):
        return "ad"
    if any(k in g for k in ("exploit", "cve", "rce", "lfi", "sqli", "shell")):
        return "exploit"
    if any(k in g for k in ("enum", "scan", "nmap", "discover", "service")):
        return "enum"
    return "generic"


class QueenBrain:
    """
    The queen orchestrates the hive:
      1. plan(goal)          — decompose into drone tasks
      2. dispatch(tasks)     — spawn drones in parallel
      3. collect(ids)        — wait and aggregate results
      4. synthesize(results) — final summary written to hive memory

    Single Responsibility: orchestration only.
    Dependency Inversion: memory, bus, pool all injected.
    """

    def __init__(
        self,
        memory: HiveMemory,
        bus: HiveBus,
        pool: "DronePool",
        consensus: Optional["ConsensusProtocol"] = None,
    ) -> None:
        self._memory    = memory
        self._bus       = bus
        self._pool      = pool
        self._consensus = consensus or ConsensusProtocol()

    def plan(self, goal: str, n_drones: int = 0) -> List[Dict]:
        """
        Decompose a high-level goal into per-drone task specs.
        Returns list of {role, goal} dicts.
        """
        obj_type = _classify_objective(goal)
        template = _DECOMPOSITION_TEMPLATES.get(obj_type, _DECOMPOSITION_TEMPLATES["generic"])

        tasks = []
        for spec in template:
            suffix    = spec["goal_suffix"]
            task_goal = f"{goal} {suffix}".strip()
            tasks.append({"role": spec["role"], "goal": task_goal})

        while n_drones and len(tasks) < n_drones:
            tasks.append({"role": "generic", "goal": goal})

        return tasks

    def dispatch(
        self,
        tasks: List[Dict],
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> List[str]:
        """
        Spawn one drone per task in parallel.

        High-risk roles (exploit, lateral, cred, privesc_hunter) are gated
        through the ConsensusProtocol before dispatch.  Tasks that fail
        consensus are recorded in hive memory but not spawned.

        Returns list of drone_ids for approved and spawned drones.
        """
        drone_ids: List[str] = []
        blocked:   List[str] = []

        for task in tasks:
            role = task.get("role", "generic")
            goal = task["goal"]

            if role in _HIGH_RISK_ROLES:
                approved, votes, summary = self._consensus.evaluate(role, goal)
                self._memory.store(
                    content=f"[CONSENSUS] role={role} goal={goal[:100]}\n{summary}",
                    agent_id="queen",
                    event_type="consensus",
                    meta={
                        "role": role,
                        "approved": approved,
                        "votes": [
                            {
                                "voter": v.voter_role,
                                "approved": v.approved,
                                "risk": v.risk_score,
                                "rationale": v.rationale,
                            }
                            for v in votes
                        ],
                    },
                )
                if not approved:
                    log.warning("Consensus BLOCKED task role=%s: %s", role, summary)
                    blocked.append(goal[:80])
                    continue

            drone_id = self._pool.spawn(
                role=role,
                goal=goal,
                backend=backend,
                api_key=api_key,
                max_iterations=max_iterations,
            )
            drone_ids.append(drone_id)

        if tasks:
            self._memory.store(
                content=(
                    f"[QUEEN] Dispatched {len(drone_ids)}/{len(tasks)} drones"
                    f" (blocked={len(blocked)}) for: {tasks[0]['goal'][:120]}"
                ),
                agent_id="queen",
                event_type="dispatch",
                meta={
                    "drone_ids":  drone_ids,
                    "task_count": len(tasks),
                    "blocked":    blocked,
                },
            )
        return drone_ids

    def plan_and_dispatch(
        self,
        goal: str,
        n_drones: int = 0,
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> List[str]:
        """Convenience: plan + dispatch in one call."""
        tasks = self.plan(goal, n_drones=n_drones)
        return self.dispatch(tasks, backend=backend, api_key=api_key,
                             max_iterations=max_iterations)

    def collect(
        self,
        drone_ids: List[str],
        timeout: float = 300.0,
        poll_interval: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Wait for all drones to finish (up to timeout seconds).
        Returns aggregated results dict.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            states  = [self._pool.get_state(did) for did in drone_ids]
            pending = [s for s in states if s and s.status in ("queued", "running")]
            if not pending:
                break
            time.sleep(poll_interval)

        results = {}
        for did in drone_ids:
            s = self._pool.get_state(did)
            if s:
                results[did] = {
                    "role":     s.role,
                    "status":   s.status,
                    "result":   s.result[:3000] if s.result else s.error,
                    "duration": round(s.finished - s.started, 2) if s.finished else 0,
                }
        return results

    def synthesize(self, drone_ids: List[str], original_goal: str) -> str:
        """
        Read hive memory results for these drones and produce a synthesis summary.
        Written back to hive memory by the queen.
        """
        results  = self.collect(drone_ids, timeout=0)
        lines    = [f"# Hive Synthesis: {original_goal[:100]}", ""]
        total_ok = sum(1 for r in results.values() if r["status"] == "completed")
        lines.append(f"**Drones:** {len(drone_ids)} | **Completed:** {total_ok}")
        lines.append("")
        for did, r in results.items():
            lines.append(f"## Drone {did} [{r['role']}] — {r['status']} ({r['duration']}s)")
            lines.append(r["result"])
            lines.append("")

        summary = "\n".join(lines)
        self._memory.store(
            content=summary[:6000],
            agent_id="queen",
            event_type="synthesis",
            meta={"drone_ids": drone_ids, "goal": original_goal[:200]},
        )
        return summary

    def read_bus(self) -> List[HiveMessage]:
        """Drain queen's mailbox from drone result messages."""
        return self._bus.receive("queen")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5A — DroneStateStore  (S — drone persistence only)
# ─────────────────────────────────────────────────────────────────────────────


class DroneStateStore:
    """
    SQLite persistence layer for DroneState records.

    Responsible for: creating the drone_states table, upsert, load, and
    marking interrupted states on restart. Nothing else.

    Uses the same hive_memory.db as EpisodicStore but opens its own
    connection to avoid lock contention.

    On process restart, any drone whose status was 'queued' or 'running'
    is marked 'interrupted' so callers can re-queue them explicitly.
    """

    _DDL = """
    CREATE TABLE IF NOT EXISTS drone_states (
        drone_id    TEXT PRIMARY KEY,
        role        TEXT NOT NULL DEFAULT 'generic',
        goal        TEXT NOT NULL DEFAULT '',
        backend     TEXT NOT NULL DEFAULT 'groq',
        status      TEXT NOT NULL DEFAULT 'queued',
        result      TEXT NOT NULL DEFAULT '',
        error       TEXT NOT NULL DEFAULT '',
        started     REAL NOT NULL DEFAULT 0.0,
        finished    REAL NOT NULL DEFAULT 0.0,
        iterations  INTEGER NOT NULL DEFAULT 0,
        tokens_in   INTEGER NOT NULL DEFAULT 0,
        tokens_out  INTEGER NOT NULL DEFAULT 0,
        ts_updated  REAL NOT NULL DEFAULT 0.0
    )
    """

    def __init__(self, db_path: Optional[Path] = None) -> None:
        import sqlite3
        self._db_path = db_path or (HIVE_DIR / "hive_memory.db")
        self._lock    = threading.RLock()
        self._conn    = sqlite3.connect(
            str(self._db_path), check_same_thread=False
        )
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(self._DDL)
        self._conn.commit()

    def upsert(self, state: DroneState) -> None:
        """Insert or replace a drone state record. Called on every state change."""
        with self._lock:
            try:
                self._conn.execute(
                    """INSERT OR REPLACE INTO drone_states
                       (drone_id, role, goal, backend, status, result, error,
                        started, finished, iterations, tokens_in, tokens_out,
                        ts_updated)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        state.drone_id, state.role, state.goal[:2000],
                        state.backend, state.status,
                        state.result[:8000], state.error[:2000],
                        state.started, state.finished, state.iterations,
                        state.tokens_in, state.tokens_out, time.time(),
                    ),
                )
                self._conn.commit()
            except Exception as exc:
                log.warning("DroneStateStore.upsert error: %s", exc)

    def load_all(self, limit: int = 500) -> List[DroneState]:
        """Load all persisted drone states ordered by most recently updated."""
        with self._lock:
            try:
                cur = self._conn.execute(
                    """SELECT drone_id, role, goal, backend, status, result,
                              error, started, finished, iterations,
                              tokens_in, tokens_out
                       FROM drone_states
                       ORDER BY ts_updated DESC
                       LIMIT ?""",
                    (limit,),
                )
                rows = cur.fetchall()
            except Exception as exc:
                log.warning("DroneStateStore.load_all error: %s", exc)
                return []
        return [
            DroneState(
                drone_id=r[0], role=r[1], goal=r[2], backend=r[3],
                status=r[4], result=r[5], error=r[6],
                started=r[7], finished=r[8],
                iterations=r[9], tokens_in=r[10], tokens_out=r[11],
            )
            for r in rows
        ]

    def mark_interrupted(self) -> int:
        """
        Called on daemon startup: any drone that was queued/running when the
        process died is now in an unknown state. Mark them 'interrupted' so
        they are visible in status and can be re-queued explicitly.
        Returns number of records updated.
        """
        with self._lock:
            try:
                cur = self._conn.execute(
                    """UPDATE drone_states
                       SET status = 'interrupted', ts_updated = ?
                       WHERE status IN ('queued', 'running')""",
                    (time.time(),),
                )
                self._conn.commit()
                return cur.rowcount
            except Exception as exc:
                log.warning("DroneStateStore.mark_interrupted error: %s", exc)
                return 0

    def load_interrupted(self) -> List[DroneState]:
        """Return all drones currently in 'interrupted' state."""
        with self._lock:
            try:
                cur = self._conn.execute(
                    """SELECT drone_id, role, goal, backend, status, result,
                              error, started, finished, iterations,
                              tokens_in, tokens_out
                       FROM drone_states
                       WHERE status = 'interrupted'
                       ORDER BY ts_updated DESC""",
                )
                rows = cur.fetchall()
            except Exception as exc:
                log.warning("DroneStateStore.load_interrupted error: %s", exc)
                return []
        return [
            DroneState(
                drone_id=r[0], role=r[1], goal=r[2], backend=r[3],
                status=r[4], result=r[5], error=r[6],
                started=r[7], finished=r[8],
                iterations=r[9], tokens_in=r[10], tokens_out=r[11],
            )
            for r in rows
        ]

    def delete_older_than(self, days: float = 7.0) -> int:
        """Prune records older than N days. Returns count deleted."""
        cutoff = time.time() - days * 86400
        with self._lock:
            try:
                cur = self._conn.execute(
                    "DELETE FROM drone_states WHERE ts_updated < ?", (cutoff,)
                )
                self._conn.commit()
                return cur.rowcount
            except Exception as exc:
                log.warning("DroneStateStore.delete_older_than error: %s", exc)
                return 0


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — DronePool  (S — drone thread management only)
# ─────────────────────────────────────────────────────────────────────────────


class DronePool:
    """
    Registry of all spawned drones with their state and threads.

    Single Responsibility: spawn, track, and query drones.
    Dependency Inversion: accepts optional DroneStateStore for persistence.

    On construction, calls state_store.mark_interrupted() so any in-flight
    drones from a previous process are cleanly labelled. Then loads the full
    history into _history for status queries without re-running them.
    """

    def __init__(
        self,
        memory: HiveMemory,
        bus: HiveBus,
        state_store: Optional[DroneStateStore] = None,
    ) -> None:
        self._memory      = memory
        self._bus         = bus
        self._state_store = state_store
        self._drones: Dict[str, DroneAgent] = {}
        # Recovered states from previous runs (read-only, no live thread)
        self._history: Dict[str, DroneState] = {}
        self._lock = threading.Lock()

    def recover_from_store(self) -> int:
        """
        Load persisted drone states from a previous run.
        In-flight drones (queued/running) are marked 'interrupted'.
        Returns the number of interrupted drones found.
        """
        if self._state_store is None:
            return 0
        interrupted = self._state_store.mark_interrupted()
        all_states  = self._state_store.load_all()
        with self._lock:
            for state in all_states:
                if state.drone_id not in self._drones:
                    self._history[state.drone_id] = state
        if interrupted:
            log.info(
                "DronePool: %d drone(s) from previous run marked 'interrupted'",
                interrupted,
            )
        return interrupted

    def spawn(
        self,
        role: str,
        goal: str,
        backend: str = "groq",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_iterations: int = 10,
        runner: Optional[ICommandRunner] = None,
    ) -> str:
        """Create and start a DroneAgent. Returns drone_id."""
        drone_id = f"{role[:4]}-{uuid.uuid4().hex[:6]}"
        drone    = DroneAgent(
            drone_id=drone_id,
            role=role,
            goal=goal,
            backend=backend,
            memory=self._memory,
            bus=self._bus,
            max_iterations=max_iterations,
            api_key=api_key,
            model=model,
            runner=runner,
            on_state_change=self._state_store.upsert if self._state_store else None,
        )
        with self._lock:
            self._drones[drone_id] = drone
        # Persist initial 'queued' state before thread starts
        if self._state_store:
            self._state_store.upsert(drone.state)
        drone.start()
        return drone_id

    def requeue_interrupted(
        self,
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> List[str]:
        """
        Re-spawn all drones previously marked 'interrupted'.
        Returns list of new drone_ids.
        """
        if self._state_store is None:
            return []
        interrupted = self._state_store.load_interrupted()
        new_ids = []
        for state in interrupted:
            new_id = self.spawn(
                role=state.role,
                goal=state.goal,
                backend=backend or state.backend,
                api_key=api_key,
                max_iterations=max_iterations,
            )
            new_ids.append(new_id)
        log.info("DronePool: re-queued %d interrupted drone(s)", len(new_ids))
        return new_ids

    def get_state(self, drone_id: str) -> Optional[DroneState]:
        """Return the current state snapshot for a drone, or None if unknown."""
        with self._lock:
            d = self._drones.get(drone_id)
            if d is not None:
                return d.state
            # Fall back to persisted history (previous runs)
            return self._history.get(drone_id)

    def list_all(self, limit: int = 30) -> List[Dict]:
        """
        Return a sorted list of drone summary dicts (most recent first).
        Includes live drones and recovered history from previous runs.
        """
        with self._lock:
            live    = [(d.state, True)  for d in self._drones.values()]
            history = [(s,       False) for s in self._history.values()
                       if s.drone_id not in self._drones]
        combined = live + history
        combined.sort(key=lambda x: x[0].started, reverse=True)
        result = []
        for state, is_live in combined[:limit]:
            result.append({
                "drone_id": state.drone_id,
                "role":     state.role,
                "status":   state.status,
                "backend":  state.backend,
                "goal":     state.goal[:80],
                "live":     is_live,
                "duration": round(state.finished - state.started, 1)
                            if state.finished else None,
            })
        return result

    def active_count(self) -> int:
        """Return number of live drones currently in queued or running state."""
        with self._lock:
            return sum(
                1 for d in self._drones.values()
                if d.state.status in ("queued", "running")
            )


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — HiveMind  (top-level singleton)
# ─────────────────────────────────────────────────────────────────────────────


class HiveMind:
    """
    Top-level hive coordinator.
    Singleton — use get_hive() to obtain the instance.
    """

    def __init__(self) -> None:
        self.memory      = build_default_hive_memory()
        self.bus         = HiveBus()
        self.state_store = DroneStateStore()
        self._pool       = DronePool(self.memory, self.bus, self.state_store)
        self.queen       = QueenBrain(self.memory, self.bus, self._pool)
        # Recover drone states from any previous run
        self._pool.recover_from_store()

    # ── Convenience methods (called from MCP tools) ──────────────────────────

    def spawn(
        self,
        goal: str,
        role: str = "generic",
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> str:
        """Spawn a single drone. Returns drone_id."""
        return self._pool.spawn(
            role=role, goal=goal, backend=backend,
            api_key=api_key, max_iterations=max_iterations,
        )

    def spawn_hive(
        self,
        goal: str,
        n_drones: int = 0,
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> List[str]:
        """Queen plans and dispatches multiple drones in parallel."""
        return self.queen.plan_and_dispatch(
            goal=goal, n_drones=n_drones, backend=backend,
            api_key=api_key, max_iterations=max_iterations,
        )

    def status(self) -> Dict[str, Any]:
        """Return hive-wide status dict including historical drones from previous runs."""
        drone_list   = self._pool.list_all()
        mem_stats    = self.memory.stats()
        bus_msgs     = self.bus.pending_count("queen")
        interrupted  = (
            len(self._pool._history) if self._pool._history else 0
        )
        return {
            "active_drones":      self._pool.active_count(),
            "total_drones":       len(drone_list),
            "history_recovered":  interrupted,
            "drones":             drone_list,
            "memory":             mem_stats,
            "queen_mailbox":      bus_msgs,
        }

    def recall(self, query: str, top_k: int = 10) -> List[Dict]:
        """Unified recall from all memory layers."""
        return self.memory.recall(query, top_k=top_k)

    def drone_result(self, drone_id: str) -> Dict[str, Any]:
        """Return result dict for a specific drone."""
        s = self._pool.get_state(drone_id)
        if s is None:
            return {"error": f"Drone '{drone_id}' not found"}
        return {
            "drone_id": s.drone_id,
            "role":     s.role,
            "status":   s.status,
            "result":   s.result,
            "error":    s.error,
            "duration": round(s.finished - s.started, 2) if s.finished else None,
        }

    def collect_and_synthesize(self, drone_ids: List[str], goal: str) -> str:
        """Synthesize results from multiple drones."""
        return self.queen.synthesize(drone_ids, goal)

    def forget(self, older_than_hours: float = 24.0, topic: str = "") -> int:
        """Prune hive memory."""
        return self.memory.forget(older_than_hours=older_than_hours, topic=topic)


# ── Singleton ──────────────────────────────────────────────────────────────────

_hive_instance: Optional[HiveMind] = None
_hive_lock = threading.Lock()


def get_hive() -> HiveMind:
    """Return the process-wide HiveMind singleton, creating it if necessary."""
    global _hive_instance
    if _hive_instance is None:
        with _hive_lock:
            if _hive_instance is None:
                _hive_instance = HiveMind()
    return _hive_instance


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — MCP tool handlers (imported by lazyown_mcp.py)
# ─────────────────────────────────────────────────────────────────────────────


def mcp_hive_spawn(
    goal: str,
    role: str = "generic",
    n_drones: int = 1,
    backend: str = "groq",
    max_iterations: int = 10,
    api_key: str = "",
) -> str:
    """
    Spawn one or more hive drones for a goal.
    If n_drones > 1 or role == 'auto', queen plans and dispatches a full squad.
    """
    hive    = get_hive()
    eff_key = api_key or None

    if n_drones > 1 or role == "auto":
        ids = hive.spawn_hive(
            goal=goal, n_drones=n_drones, backend=backend,
            api_key=eff_key, max_iterations=max_iterations,
        )
        return json.dumps({
            "spawned":   len(ids),
            "drone_ids": ids,
            "message":   f"Hive squad dispatched: {len(ids)} drones in parallel",
        }, indent=2)
    else:
        drone_id = hive.spawn(
            goal=goal, role=role, backend=backend,
            api_key=eff_key, max_iterations=max_iterations,
        )
        return json.dumps({
            "drone_id": drone_id,
            "role":     role,
            "backend":  backend,
            "message":  f"Drone {drone_id} spawned for role={role}",
        }, indent=2)


def mcp_hive_status() -> str:
    """Return full hive status: active drones, memory stats, queen mailbox."""
    return json.dumps(get_hive().status(), indent=2)


def mcp_hive_recall(query: str, top_k: int = 10) -> str:
    """Semantic + episodic + longterm recall from hive memory."""
    results = get_hive().recall(query, top_k=top_k)
    if not results:
        return f"No hive memories found for: {query!r}"
    lines = [f"Hive recall ({len(results)} results) for: {query!r}", ""]
    for i, r in enumerate(results, 1):
        layer = r.get("layer", "?")
        sim   = r.get("similarity")
        sim_s = f"  sim={sim:.3f}" if sim is not None else ""
        lines.append(f"{i}. [{layer}]{sim_s}  {r['content'][:300]}")
    return "\n".join(lines)


def mcp_hive_plan(goal: str, n_drones: int = 0) -> str:
    """Queen generates task decomposition without spawning drones."""
    tasks = get_hive().queen.plan(goal, n_drones=n_drones)
    lines = [f"Hive plan for: {goal[:100]}", f"({len(tasks)} tasks)", ""]
    for i, t in enumerate(tasks, 1):
        lines.append(f"  {i}. [{t['role']:8s}] {t['goal'][:100]}")
    return "\n".join(lines)


def mcp_hive_result(drone_id: str) -> str:
    """Get result from a specific drone."""
    r = get_hive().drone_result(drone_id)
    return json.dumps(r, indent=2)


def mcp_hive_collect(drone_ids_csv: str, goal: str = "") -> str:
    """
    Wait for drones to finish and return synthesized result.
    drone_ids_csv: comma-separated drone IDs.
    """
    ids = [x.strip() for x in drone_ids_csv.split(",") if x.strip()]
    if not ids:
        return "No drone IDs provided."
    return get_hive().collect_and_synthesize(ids, goal or f"Collected from {len(ids)} drones")


def mcp_hive_forget(older_than_hours: float = 24.0, topic: str = "") -> str:
    """Prune hive memory. Removes entries older than N hours, optionally filtered by topic."""
    pruned = get_hive().forget(older_than_hours=older_than_hours, topic=topic)
    return f"Pruned {pruned} hive memory entries (older_than={older_than_hours}h, topic={topic!r})"


def mcp_hive_recover(
    backend: str = "groq",
    api_key: str = "",
    max_iterations: int = 10,
) -> str:
    """
    Re-queue all drones that were interrupted by a previous process crash/restart.
    Returns the list of new drone_ids that were re-spawned.
    """
    hive    = get_hive()
    eff_key = api_key or None
    new_ids = hive._pool.requeue_interrupted(
        backend=backend,
        api_key=eff_key,
        max_iterations=max_iterations,
    )
    if not new_ids:
        # Also report how many interrupted states exist in history
        interrupted = [
            s for s in hive._pool._history.values()
            if s.status == "interrupted"
        ]
        if not interrupted:
            return "No interrupted drones found — nothing to recover."
        return json.dumps({
            "recovered": 0,
            "message": (
                f"{len(interrupted)} interrupted drone(s) found but already loaded "
                "into history. Use mcp_hive_status to inspect them."
            ),
            "interrupted_ids": [s.drone_id for s in interrupted],
        }, indent=2)
    return json.dumps({
        "recovered":  len(new_ids),
        "new_ids":    new_ids,
        "message":    f"Re-spawned {len(new_ids)} interrupted drone(s)",
    }, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — CLI
# ─────────────────────────────────────────────────────────────────────────────


def _cli() -> None:  # noqa: C901
    import argparse

    parser = argparse.ArgumentParser(
        description="LazyOwn Hive Mind — multi-agent cognitive system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_sp = sub.add_parser("spawn", help="Spawn drones for a goal")
    p_sp.add_argument("goal",      help="High-level goal")
    p_sp.add_argument("--role",    default="auto", help="Drone role (auto = queen plans)")
    p_sp.add_argument("--drones",  type=int, default=0, help="Number of drones (0 = template)")
    p_sp.add_argument("--backend", default="groq", choices=["groq", "ollama"])
    p_sp.add_argument("--max-iter", type=int, default=10)
    p_sp.add_argument("--wait",    action="store_true", help="Block until all done")
    p_sp.add_argument("--timeout", type=float, default=300.0)

    sub.add_parser("status", help="Show hive status")

    p_rc = sub.add_parser("recall", help="Recall from hive memory")
    p_rc.add_argument("query")
    p_rc.add_argument("--top", type=int, default=10)

    p_pl = sub.add_parser("plan", help="Show queen's task decomposition")
    p_pl.add_argument("goal")
    p_pl.add_argument("--drones", type=int, default=0)

    p_rs = sub.add_parser("result", help="Get drone result")
    p_rs.add_argument("drone_id")

    p_fg = sub.add_parser("forget", help="Prune hive memory")
    p_fg.add_argument("--hours", type=float, default=24.0)
    p_fg.add_argument("--topic", default="")

    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)

    if args.cmd == "spawn":
        role = args.role if args.role != "auto" else "generic"
        n    = args.drones or (1 if role != "generic" else 0)
        print(mcp_hive_spawn(
            goal=args.goal, role=role,
            n_drones=n if args.role == "auto" else 1,
            backend=args.backend, max_iterations=args.max_iter,
        ))
        if args.wait:
            hive     = get_hive()
            deadline = time.time() + args.timeout
            while hive._pool.active_count() > 0 and time.time() < deadline:
                time.sleep(2.0)
            print(json.dumps(hive.status(), indent=2))

    elif args.cmd == "status":
        print(mcp_hive_status())

    elif args.cmd == "recall":
        print(mcp_hive_recall(args.query, top_k=args.top))

    elif args.cmd == "plan":
        print(mcp_hive_plan(args.goal, n_drones=args.drones))

    elif args.cmd == "result":
        print(mcp_hive_result(args.drone_id))

    elif args.cmd == "forget":
        print(mcp_hive_forget(older_than_hours=args.hours, topic=args.topic))

    else:
        parser.print_help()


if __name__ == "__main__":
    _cli()
