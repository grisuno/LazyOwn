"""BDD tests for hashing embeddings and hybrid episodic recall."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from modules.memory_embeddings import EmbeddingError, cosine, embed, semantic_top_k, as_floats
from modules.memory_store import MemoryEntry, MemoryStore, VectorSQLiteBackend


def _entry(tool: str, command: str, snippet: str = "ok") -> MemoryEntry:
    return MemoryEntry(
        session_id="s1",
        host="10.0.0.1",
        tool=tool,
        command=command,
        output_snippet=snippet,
        findings_json="[]",
        success=True,
        ts=time.time(),
    )


class TestHashingEmbedder:
    """Deterministic zero-dependency text vectors."""

    def test_identical_text_full_similarity(self):
        """Given the same text twice, Then cosine is 1.0."""
        story = "equal vectors share direction"
        blob = embed("nmap -sV target one")
        assert cosine(blob, embed("nmap -sV target one")) == pytest.approx(1.0, abs=1e-3), story

    def test_similar_text_scores_higher_than_unrelated(self):
        """Given related vs unrelated text, Then similarity ranks correctly."""
        story = "nmap text must beat random text against an nmap query"
        query = embed("nmap -sV scans ports")
        related = cosine(query, embed("nmap -sV -p 22 target"))
        unrelated = cosine(query, embed("yara rule malware sample"))
        assert related > unrelated >= 0.0, story

    def test_determinism_across_runs(self):
        """Given two embed calls, Then the BLOBs are identical."""
        story = "no model, no drift"
        assert embed("hydra -l a -p b") == embed("hydra -l a -p b")

    def test_empty_text_raises(self):
        """Given blank text, Then the embedder refuses."""
        story = "junk input must fail loudly"
        with pytest.raises(EmbeddingError):
            embed("   ")

    def test_unit_length(self):
        """Given any text, Then the vector is L2-normalised."""
        story = "cosine needs unit vectors"
        blob = embed("ssh root 10.0.0.9")
        assert sum(v * v for v in as_floats(blob)) == pytest.approx(1.0, abs=1e-2), story


class TestVectorSQLiteBackend:
    """Auto-embed on save plus semantic ranking."""

    def test_save_gets_embedding(self, tmp_path: Path):
        """Given a save, Then the row carries a non-null embedding."""
        story = "the dead BLOB column starts carrying data"
        backend = VectorSQLiteBackend(db_path=tmp_path / "lazymem.db")
        backend.save(_entry("nmap", "nmap -sV", "root"))
        entry = backend.all_entries(limit=5)[0]
        assert entry.embedding is not None, story

    def test_semantic_ranks_relevant_first(self, tmp_path: Path):
        """Given two entries, Then the semantic query surfaces the relevant one."""
        story = "vector search finds the right memory"
        backend = VectorSQLiteBackend(db_path=tmp_path / "lazymem.db")
        backend.save(_entry("nmap", "nmap -sV web 10.0.0.7", "port 80"))
        backend.save(_entry("yara", "yara_scan /tmp/x.bin", "clean"))
        hits = backend.search_semantic("web port scan", 2)
        assert hits and hits[0].tool == "nmap", story

    def test_keyword_query_still_works(self, tmp_path: Path):
        """Given an FTS5 query, Then keyword search keeps working on the new backend."""
        story = "no regression in FTS path"
        backend = VectorSQLiteBackend(db_path=tmp_path / "lazymem.db")
        backend.save(_entry("nmap", "nmap -sV tgt", "ports"))
        assert backend.search("nmap*", 5), story


class TestMemoryStoreHybrid:
    """recall_hybrid prefers FTS and falls back to vectors."""

    def test_fts_wins_when_present(self, tmp_path: Path):
        """Given matching keyword rows, Then FTS5 results are returned first."""
        story = "keyword precision takes priority"
        backend = VectorSQLiteBackend(db_path=tmp_path / "lazymem.db")
        backend.save(_entry("nmap", "nmap -sV tgt", "ports"))
        store = MemoryStore(backend)
        assert store.recall_hybrid("nmap*", 5), story

    def test_hybrid_fallback_after_miss(self, tmp_path: Path):
        """Given a keyword-miss query, Then semantic hits still surface."""
        story = "the fallback must not drop recall to zero"
        backend = VectorSQLiteBackend(db_path=tmp_path / "lazymem.db")
        backend.save(_entry("hydra", "hydra -l admin -p pass smb://x", "winshare"))
        store = MemoryStore(backend)
        hits = store.recall_hybrid("bruteforce winshare logins", 5)
        assert hits and hits[0].tool == "hydra", story
