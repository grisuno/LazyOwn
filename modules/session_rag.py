"""
session_rag.py — ChromaDB-backed RAG over sessions/ artefacts.

Incrementally indexes every text artefact in sessions/:
  *.log, *.txt, *.csv, *.xml, *.json, *.nmap, *.md

State tracked in sessions/rag_state.json (mtime per file) so only
new or changed files are re-indexed on each call.

ChromaDB is optional — if not installed the module degrades gracefully
to keyword search (Python in-memory fallback).

Install:
    pip install chromadb

Public API
----------
get_rag() -> SessionRAG          singleton
SessionRAG.index_new()           incremental re-index (fast, cron-safe)
SessionRAG.index_all()           full re-index from scratch
SessionRAG.query(text, n)        semantic / keyword search
SessionRAG.context_for_step(phase, target, n)  -> str for prompt injection
SessionRAG.stats()               -> dict
"""

from __future__ import annotations

import json
import os
import re
import time
import hashlib
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ChromaDB with graceful fallback
# ---------------------------------------------------------------------------
try:
    import chromadb
    from chromadb.config import Settings as _ChromaSettings
    _CHROMA_OK = True
except ImportError:
    _CHROMA_OK = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SESSIONS_DIR         = Path(__file__).parent.parent / "sessions"
RAG_STATE_FILE       = SESSIONS_DIR / "rag_state.json"
FALLBACK_INDEX_FILE  = SESSIONS_DIR / "keyword_fallback_index.json"
CHROMA_DIR           = SESSIONS_DIR / "chromadb"
COLLECTION_NAME      = "lazyown_sessions"
CHUNK_SIZE           = 400
CHUNK_OVERLAP        = 50
MAX_FALLBACK_DOCS    = 5000   # ring-buffer cap for keyword fallback

INDEXABLE_SUFFIXES = {
    ".log", ".txt", ".csv", ".xml", ".json",
    ".nmap", ".md", ".html",
}

# Files / patterns to skip (too large or binary)
SKIP_PATTERNS = re.compile(
    r"(\.png|\.jpg|\.gif|\.exe|\.bin|\.dll|rag_state\.json|chromadb)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
def _chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    if len(text) <= size:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


# ---------------------------------------------------------------------------
# Fallback in-memory keyword index
# ---------------------------------------------------------------------------
class _KeywordFallback:
    """
    Keyword search fallback when chromadb is not installed.

    Persists to FALLBACK_INDEX_FILE so the index survives process restarts.
    Uses a ring-buffer (MAX_FALLBACK_DOCS) to cap disk usage.
    """

    def __init__(self) -> None:
        self._docs: List[Dict[str, Any]] = []
        self._ids: set = set()    # for deduplication

    def load(self, path: Path) -> None:
        """Load index from disk (no-op if file absent or corrupt)."""
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text())
            self._docs = data.get("docs", [])
            self._ids  = {d["id"] for d in self._docs}
        except Exception:
            pass

    def save(self, path: Path) -> None:
        """Atomically persist index to disk."""
        try:
            SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps({"docs": self._docs}, separators=(",", ":")))
            os.replace(tmp, path)
        except Exception:
            pass

    def add(self, doc_id: str, text: str, meta: Dict[str, Any]) -> None:
        if doc_id in self._ids:
            return  # deduplication
        self._docs.append({"id": doc_id, "text": text, "meta": meta})
        self._ids.add(doc_id)
        # Ring-buffer: discard oldest entries when cap is exceeded
        if len(self._docs) > MAX_FALLBACK_DOCS:
            evicted = self._docs.pop(0)
            self._ids.discard(evicted["id"])

    def query(self, query_text: str, n: int = 5) -> List[Dict[str, Any]]:
        words = set(query_text.lower().split())
        scored: List[tuple[int, Dict[str, Any]]] = []
        for doc in self._docs:
            hits = sum(1 for w in words if w in doc["text"].lower())
            if hits:
                scored.append((hits, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:n]]

    def count(self) -> int:
        return len(self._docs)

    def reset(self) -> None:
        self._docs = []
        self._ids  = set()


# ---------------------------------------------------------------------------
# SessionRAG
# ---------------------------------------------------------------------------
@dataclass
class _RagState:
    mtimes: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "_RagState":
        if RAG_STATE_FILE.exists():
            try:
                data = json.loads(RAG_STATE_FILE.read_text())
                return cls(mtimes=data.get("mtimes", {}))
            except Exception:
                pass
        return cls()

    def save(self) -> None:
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        tmp = RAG_STATE_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps({"mtimes": self.mtimes}, indent=2))
        os.replace(tmp, RAG_STATE_FILE)


class SessionRAG:
    """Semantic search over sessions/ artefacts using ChromaDB or keyword fallback."""

    def __init__(self) -> None:
        self._state = _RagState.load()
        self._fallback = _KeywordFallback()
        self._collection: Optional[Any] = None
        self._client: Optional[Any] = None
        self._ready = False
        self._init_backend()

    # ------------------------------------------------------------------
    # Backend init
    # ------------------------------------------------------------------
    def _init_backend(self) -> None:
        if not _CHROMA_OK:
            log.info("session_rag: chromadb not installed — using keyword fallback")
            self._fallback.load(FALLBACK_INDEX_FILE)
            self._ready = True
            return
        try:
            CHROMA_DIR.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(
                path=str(CHROMA_DIR),
            )
            try:
                self._collection = self._client.get_collection(COLLECTION_NAME)
            except Exception:
                self._collection = self._client.create_collection(
                    name=COLLECTION_NAME,
                    metadata={"hnsw:space": "cosine"},
                )
            self._ready = True
            log.info("session_rag: ChromaDB backend ready at %s", CHROMA_DIR)
        except Exception as exc:
            log.warning("session_rag: ChromaDB init failed (%s) — using keyword fallback", exc)
            self._ready = True

    # ------------------------------------------------------------------
    # File discovery
    # ------------------------------------------------------------------
    def _iter_artefacts(self) -> List[Path]:
        files: List[Path] = []
        for p in SESSIONS_DIR.rglob("*"):
            if not p.is_file():
                continue
            if SKIP_PATTERNS.search(str(p)):
                continue
            if p.suffix.lower() not in INDEXABLE_SUFFIXES:
                continue
            if p.stat().st_size > 2_000_000:  # skip files > 2 MB
                continue
            files.append(p)
        return files

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------
    def _index_file(self, path: Path) -> int:
        """Index a single file; return number of chunks added."""
        try:
            text = path.read_text(errors="replace")
        except Exception:
            return 0
        if not text.strip():
            return 0

        rel = str(path.relative_to(SESSIONS_DIR))
        chunks = _chunk_text(text)
        added = 0
        for i, chunk in enumerate(chunks):
            doc_id = hashlib.md5(f"{rel}:{i}:{chunk[:40]}".encode()).hexdigest()
            meta = {
                "source":    rel,
                "chunk":     i,
                "mtime":     path.stat().st_mtime,
                "suffix":    path.suffix,
            }
            if self._collection is not None:
                try:
                    self._collection.add(
                        documents=[chunk],
                        ids=[doc_id],
                        metadatas=[meta],
                    )
                    added += 1
                except Exception:
                    pass  # duplicate id is fine
            else:
                self._fallback.add(doc_id, chunk, meta)
                added += 1
        return added

    def index_new(self) -> Dict[str, int]:
        """Incrementally index only new or changed files."""
        files = self._iter_artefacts()
        indexed_files = 0
        indexed_chunks = 0
        for path in files:
            rel = str(path.relative_to(SESSIONS_DIR))
            mtime = path.stat().st_mtime
            if self._state.mtimes.get(rel) == mtime:
                continue
            chunks = self._index_file(path)
            if chunks:
                indexed_files += 1
                indexed_chunks += chunks
                self._state.mtimes[rel] = mtime
        if indexed_files:
            self._state.save()
            if self._collection is None:   # keyword fallback — persist to disk
                self._fallback.save(FALLBACK_INDEX_FILE)
        return {"files": indexed_files, "chunks": indexed_chunks}

    def index_parquet_sources(self, force: bool = False) -> Dict[str, int]:
        """
        Index knowledge-base parquets (techniques_enriched, binarios, lolbas_index)
        into the RAG store.

        Each row is indexed as:  "<name>. <description_preview>  CMD: <command_preview>"
        so queries like "bypass amsi windows" or "suid privilege escalation" resolve
        to real Atomic Red Team commands and GTFOBins entries.

        State is tracked in rag_state.json under the key "parquets/<stem>".
        """
        try:
            import pandas as pd
        except ImportError:
            return {"files": 0, "chunks": 0, "error": "pandas not installed"}

        parquets_dir = SESSIONS_DIR.parent / "parquets"
        targets = [
            ("techniques_enriched", ["name", "description", "command", "mitre_id"]),
            ("techniques",          ["name", "description", "mitre_id"]),
            ("binarios",            ["name", "description", "type"]),
            ("lolbas_index",        ["Name", "Description", "Commands"]),
        ]

        indexed_files = 0
        indexed_chunks = 0

        for stem, cols in targets:
            path = parquets_dir / f"{stem}.parquet"
            if not path.exists():
                continue
            state_key = f"parquets/{stem}"
            mtime = path.stat().st_mtime
            if not force and self._state.mtimes.get(state_key) == mtime:
                continue

            try:
                df = pd.read_parquet(path)
            except Exception:
                continue

            file_chunks = 0
            for _, row in df.iterrows():
                parts = []
                for col in cols:
                    if col in row and row[col] and str(row[col]).strip():
                        val = str(row[col]).strip()
                        if col in ("command", "Commands"):
                            val = val[:200]
                        else:
                            val = val[:300]
                        parts.append(val)
                if not parts:
                    continue
                text    = " | ".join(parts)
                row_id  = str(row.get("id", row.get("Name", ""))) or hashlib.md5(
                    f"{stem}:{text[:40]}".encode()
                ).hexdigest()
                doc_id  = hashlib.md5(f"pq:{stem}:{row_id}".encode()).hexdigest()
                meta    = {"source": f"parquet/{stem}", "chunk": 0, "mtime": mtime}
                for chunk in _chunk_text(text):
                    if self._collection is not None:
                        try:
                            self._collection.add(
                                documents=[chunk],
                                ids=[doc_id],
                                metadatas=[meta],
                            )
                        except Exception:
                            pass
                    else:
                        self._fallback.add(doc_id, chunk, meta)
                    file_chunks += 1

            if file_chunks:
                indexed_files += 1
                indexed_chunks += file_chunks
                self._state.mtimes[state_key] = mtime

        if indexed_files:
            self._state.save()
            if self._collection is None:
                self._fallback.save(FALLBACK_INDEX_FILE)

        return {"files": indexed_files, "chunks": indexed_chunks}

    def index_all(self) -> Dict[str, int]:
        """Full re-index from scratch."""
        if self._collection is not None:
            try:
                self._client.delete_collection(COLLECTION_NAME)
                self._collection = self._client.create_collection(
                    name=COLLECTION_NAME,
                    metadata={"hnsw:space": "cosine"},
                )
            except Exception:
                pass
        else:
            self._fallback.reset()
            FALLBACK_INDEX_FILE.unlink(missing_ok=True)
        self._state = _RagState()
        return self.index_new()

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------
    def query(self, query_text: str, n: int = 5) -> List[Dict[str, Any]]:
        """Return top-n relevant chunks as dicts with keys: text, source, chunk, score."""
        if self._collection is not None:
            try:
                results = self._collection.query(
                    query_texts=[query_text],
                    n_results=min(n, max(self._collection.count(), 1)),
                )
                docs      = results.get("documents", [[]])[0]
                metas     = results.get("metadatas", [[]])[0]
                distances = results.get("distances", [[]])[0]
                out = []
                for doc, meta, dist in zip(docs, metas, distances):
                    out.append({
                        "text":   doc,
                        "source": meta.get("source", ""),
                        "chunk":  meta.get("chunk", 0),
                        "score":  round(1.0 - dist, 4),
                    })
                return out
            except Exception as exc:
                log.debug("session_rag: ChromaDB query failed (%s), using fallback", exc)

        # fallback
        hits = self._fallback.query(query_text, n)
        return [
            {
                "text":   h["text"],
                "source": h["meta"].get("source", ""),
                "chunk":  h["meta"].get("chunk", 0),
                "score":  None,
            }
            for h in hits
        ]

    def context_for_step(self, phase: str = "", target: str = "", cmd: str = "", n: int = 4) -> str:
        """
        Return a compact RAG context string suitable for injection into an LLM prompt.
        Queries with phase + target + command to retrieve the most relevant session artefacts.
        """
        query = f"phase:{phase} target:{target} command:{cmd} pentest reconnaissance exploitation"
        hits  = self.query(query, n)
        if not hits:
            return ""
        lines = ["[RAG context — relevant session artefacts]"]
        for h in hits:
            src   = h["source"]
            score = f" (score={h['score']:.3f})" if h["score"] is not None else ""
            lines.append(f"--- {src}{score} ---")
            lines.append(h["text"].strip()[:300])
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def stats(self) -> Dict[str, Any]:
        indexed = len(self._state.mtimes)
        if self._collection is not None:
            total_chunks = self._collection.count()
            backend = "chromadb"
        else:
            total_chunks = self._fallback.count()
            backend = "keyword_fallback"
        return {
            "backend":       backend,
            "indexed_files": indexed,
            "total_chunks":  total_chunks,
            "chroma_ok":     _CHROMA_OK,
            "state_file":    str(RAG_STATE_FILE),
        }


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------
_rag_instance: Optional[SessionRAG] = None


def get_rag() -> SessionRAG:
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = SessionRAG()
    return _rag_instance


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="LazyOwn Session RAG")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("index",   help="Incremental index")
    sub.add_parser("reindex", help="Full re-index from scratch")
    q_p = sub.add_parser("query",  help="Query the index")
    q_p.add_argument("text",  nargs="+")
    q_p.add_argument("-n",    type=int, default=5)
    sub.add_parser("stats",   help="Print stats")

    args = parser.parse_args()
    rag  = get_rag()

    if args.cmd == "index":
        r = rag.index_new()
        print(json.dumps(r, indent=2))
    elif args.cmd == "reindex":
        r = rag.index_all()
        print(json.dumps(r, indent=2))
    elif args.cmd == "query":
        hits = rag.query(" ".join(args.text), args.n)
        for h in hits:
            print(f"[{h['source']}]  score={h['score']}")
            print(h["text"][:200])
            print()
    elif args.cmd == "stats":
        print(json.dumps(rag.stats(), indent=2))
    else:
        parser.print_help()
