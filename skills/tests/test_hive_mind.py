#!/usr/bin/env python3
"""
skills/tests/test_hive_mind.py — Tests for hive_mind.py (SOLID refactoring)

All file I/O uses tmp_path (pytest) or tempfile.TemporaryDirectory.
No external API calls. ChromaDB is mocked when not installed.
"""

from __future__ import annotations

import json
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest

# Make skills/ importable
_SKILLS_DIR = Path(__file__).parent.parent
if str(_SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILLS_DIR))


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_episodic(tmp_path: Path):
    """Return a fresh EpisodicStore backed by tmp_path."""
    from hive_mind import EpisodicStore
    return EpisodicStore(db_path=tmp_path / "test_hive.db")


def _make_semantic(tmp_path: Path, episodic=None):
    """Return a fresh SemanticStore (ChromaDB mocked or real if available)."""
    from hive_mind import SemanticStore, _CHROMA_OK
    return SemanticStore(
        chroma_dir=tmp_path / "chroma",
        episodic_fallback=episodic,
    )


def _make_hive_memory(tmp_path: Path):
    """Return a HiveMemory with real EpisodicStore and mocked SemanticStore."""
    from hive_mind import (
        EpisodicStore, SemanticStore, LongtermStore, HiveMemory
    )
    episodic = EpisodicStore(db_path=tmp_path / "hive_mem.db")
    semantic = SemanticStore(
        chroma_dir=tmp_path / "chroma",
        episodic_fallback=episodic,
    )
    longterm = LongtermStore()
    return HiveMemory(
        stores=[episodic, semantic, longterm],
        episodic=episodic,
        semantic=semantic,
        longterm=longterm,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 1. TestEpisodicStore
# ─────────────────────────────────────────────────────────────────────────────

class TestEpisodicStore:
    """Unit tests for EpisodicStore (SQLite FTS5)."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def test_store_returns_nonempty_id(self):
        """store() should return a non-empty string event_id."""
        store    = _make_episodic(self.tmp)
        event_id = store.store("hello world", agent_id="queen", role="generic")
        assert isinstance(event_id, str)
        assert len(event_id) > 0

    def test_recall_keyword_found(self):
        """Stored content can be retrieved by keyword."""
        store = _make_episodic(self.tmp)
        store.store("nmap discovered open port 445", agent_id="recon-01", role="recon")
        results = store.recall("nmap", top_k=5)
        assert len(results) >= 1
        assert any("nmap" in r["content"].lower() for r in results)

    def test_recall_keyword_not_found(self):
        """Recall with an unrelated keyword returns empty list."""
        store = _make_episodic(self.tmp)
        store.store("some unrelated text", agent_id="queen")
        results = store.recall("kerberoasting")
        assert results == []

    def test_recall_fts_multiple_hits(self):
        """Multiple stored entries with the same keyword are all returned."""
        store = _make_episodic(self.tmp)
        for i in range(3):
            store.store(f"SMB enumeration result {i}", agent_id=f"agent-{i}", role="recon")
        results = store.recall("SMB", top_k=10)
        assert len(results) >= 3

    def test_stats_counts_rows(self):
        """stats() returns correct episodic_events count."""
        store = _make_episodic(self.tmp)
        store.store("event one", agent_id="a1")
        store.store("event two", agent_id="a2")
        s = store.stats()
        assert s["episodic_events"] >= 2
        assert s["unique_agents"] >= 2

    def test_forget_old_events(self):
        """forget() removes rows older than the cutoff."""
        import sqlite3
        store = _make_episodic(self.tmp)
        store.store("old event", agent_id="test")
        # Manually push ts back 48 hours
        with store._lock:
            store._conn.execute(
                "UPDATE hive_events SET ts = ts - 172800"
            )
            store._conn.commit()
        pruned = store.forget(older_than_hours=24.0)
        assert pruned >= 1

    def test_forget_by_topic(self):
        """forget(topic=X) only removes rows whose content contains X."""
        store = _make_episodic(self.tmp)
        store.store("kerberos ticket found", agent_id="a")
        store.store("smb share discovered", agent_id="b")
        # Push all rows back 48h
        with store._lock:
            store._conn.execute("UPDATE hive_events SET ts = ts - 172800")
            store._conn.commit()
        pruned = store.forget(older_than_hours=1.0, topic="kerberos")
        assert pruned == 1
        remaining = store.recall("smb")
        assert len(remaining) >= 1


# ─────────────────────────────────────────────────────────────────────────────
# 2. TestSemanticStore
# ─────────────────────────────────────────────────────────────────────────────

class TestSemanticStore:
    """Unit tests for SemanticStore (ChromaDB, with fallback to episodic)."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def test_instantiation(self):
        """SemanticStore can be instantiated regardless of ChromaDB availability."""
        from hive_mind import SemanticStore
        store = SemanticStore(chroma_dir=self.tmp / "chroma")
        assert store is not None

    def test_store_returns_id(self):
        """store() returns a non-empty string."""
        from hive_mind import SemanticStore, EpisodicStore
        ep    = _make_episodic(self.tmp)
        store = SemanticStore(chroma_dir=self.tmp / "chroma", episodic_fallback=ep)
        eid   = store.store("test content", agent_id="queen")
        assert isinstance(eid, str)
        assert len(eid) > 0

    def test_fallback_to_episodic_when_chroma_unavailable(self):
        """When ChromaDB collection is None, recall() delegates to episodic store."""
        from hive_mind import SemanticStore, EpisodicStore
        ep    = _make_episodic(self.tmp)
        ep.store("lateral movement via psexec", agent_id="x")

        store             = SemanticStore(chroma_dir=self.tmp / "chroma", episodic_fallback=ep)
        store._collection = None  # Force unavailability

        results = store.recall("lateral", top_k=5)
        assert len(results) >= 1

    def test_recall_with_mock_chroma(self):
        """When ChromaDB is mocked, recall() returns parsed results."""
        from hive_mind import SemanticStore

        mock_col = MagicMock()
        mock_col.query.return_value = {
            "documents":  [["kerberos hash found"]],
            "metadatas":  [[{"agent_id": "a", "role": "cred", "event_type": "result", "ts": "0", "session": ""}]],
            "distances":  [[0.1]],
            "ids":        [["abc123"]],
        }

        store             = SemanticStore(chroma_dir=self.tmp / "chroma")
        store._collection = mock_col

        results = store.recall("kerberos", top_k=5)
        assert len(results) == 1
        assert results[0]["id"] == "abc123"
        assert results[0]["similarity"] == pytest.approx(0.9)

    def test_count_returns_zero_when_unavailable(self):
        """count() returns 0 when collection is None."""
        from hive_mind import SemanticStore
        store             = SemanticStore(chroma_dir=self.tmp / "chroma")
        store._collection = None
        assert store.count() == 0


# ─────────────────────────────────────────────────────────────────────────────
# 3. TestHiveMemory
# ─────────────────────────────────────────────────────────────────────────────

class TestHiveMemory:
    """Unit tests for HiveMemory (composition + deduplication)."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def test_store_and_recall(self):
        """store() followed by recall() returns the stored content."""
        mem = _make_hive_memory(self.tmp)
        mem.store("SMB shares enumerated on 10.10.11.78", agent_id="recon-01", role="recon")
        results = mem.recall("SMB", top_k=5)
        assert len(results) >= 1
        assert any("SMB" in r["content"] for r in results)

    def test_recall_deduplication(self):
        """The same content stored twice appears only once in unified recall."""
        from hive_mind import EpisodicStore, SemanticStore, LongtermStore, HiveMemory

        ep = _make_episodic(self.tmp)
        content = "duplicate content for testing deduplication"
        ep.store(content, agent_id="a")

        # Mock semantic to return the same content
        mock_sem = MagicMock(spec=SemanticStore)
        mock_sem.recall.return_value = [
            {"id": "x1", "content": content, "meta": {}, "similarity": 0.9}
        ]

        lt  = LongtermStore()
        mem = HiveMemory(
            stores=[ep, mock_sem, lt],
            episodic=ep,
            semantic=mock_sem,
            longterm=lt,
        )

        results = mem.recall("duplicate", top_k=10)
        # Deduplication should yield only one entry for this content
        matching = [r for r in results if "duplicate" in r["content"]]
        assert len(matching) == 1

    def test_stats_contains_expected_keys(self):
        """stats() returns dict with episodic_events and chroma_vectors."""
        mem = _make_hive_memory(self.tmp)
        s   = mem.stats()
        assert "episodic_events" in s
        assert "chroma_vectors" in s
        assert "chroma_enabled" in s

    def test_forget_delegates_to_episodic(self):
        """forget() removes episodic entries older than cutoff."""
        mem = _make_hive_memory(self.tmp)
        mem.store("old finding", agent_id="test")
        with mem._episodic._lock:
            mem._episodic._conn.execute("UPDATE hive_events SET ts = ts - 172800")
            mem._episodic._conn.commit()
        pruned = mem.forget(older_than_hours=24.0)
        assert pruned >= 1


# ─────────────────────────────────────────────────────────────────────────────
# 4. TestHiveBus
# ─────────────────────────────────────────────────────────────────────────────

class TestHiveBus:
    """Unit tests for HiveBus (message passing)."""

    def setup_method(self):
        from hive_mind import HiveBus
        self.bus = HiveBus()

    def test_publish_and_receive(self):
        """Published message arrives in recipient's mailbox."""
        from hive_mind import HiveMessage
        msg = HiveMessage(sender="drone-01", recipient="queen", kind="result",
                          payload={"data": "found hash"})
        self.bus.publish(msg)
        received = self.bus.receive("queen")
        assert len(received) >= 1
        ids = [m.msg_id for m in received]
        assert msg.msg_id in ids

    def test_broadcast_received_by_everyone(self):
        """Broadcast message (recipient='*') is included in any agent's receive()."""
        from hive_mind import HiveMessage
        msg = HiveMessage(sender="queen", recipient="*", kind="signal",
                          payload={"cmd": "stop"})
        self.bus.publish(msg)
        received = self.bus.receive("drone-42")
        assert any(m.msg_id == msg.msg_id for m in received)

    def test_pending_count_after_publish(self):
        """pending_count() reflects queued messages."""
        from hive_mind import HiveMessage
        self.bus.publish(
            HiveMessage(sender="q", recipient="drone-01", kind="task", payload={})
        )
        count = self.bus.pending_count("drone-01")
        assert count >= 1

    def test_receive_drains_direct_mailbox(self):
        """After receive(), direct messages are removed from the mailbox."""
        from hive_mind import HiveMessage
        msg = HiveMessage(sender="queen", recipient="drone-01", kind="task", payload={})
        self.bus.publish(msg)
        self.bus.receive("drone-01")  # drain
        # Direct messages should now be gone
        with self.bus._lock:
            assert "drone-01" not in self.bus._mailbox or len(self.bus._mailbox["drone-01"]) == 0


# ─────────────────────────────────────────────────────────────────────────────
# 5. TestDronePool
# ─────────────────────────────────────────────────────────────────────────────

class TestDronePool:
    """Unit tests for DronePool (thread management)."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def _make_pool(self):
        from hive_mind import DronePool
        mem = _make_hive_memory(self.tmp)
        from hive_mind import HiveBus
        bus = HiveBus()
        return DronePool(mem, bus)

    def test_spawn_returns_drone_id(self):
        """spawn() returns a non-empty string drone_id."""
        pool = self._make_pool()
        # Patch DroneAgent._run so no LLM is called
        with patch("hive_mind.DroneAgent._run", return_value=None):
            drone_id = pool.spawn(role="recon", goal="test goal", backend="groq")
        assert isinstance(drone_id, str)
        assert len(drone_id) > 0

    def test_get_state_returns_drone_state(self):
        """get_state() returns a DroneState for a known drone_id."""
        from hive_mind import DroneState
        pool = self._make_pool()
        with patch("hive_mind.DroneAgent._run", return_value=None):
            did = pool.spawn(role="analyze", goal="analyze logs", backend="groq")
        state = pool.get_state(did)
        assert state is not None
        assert isinstance(state, DroneState)
        assert state.drone_id == did

    def test_get_state_unknown_id_returns_none(self):
        """get_state() returns None for an unknown drone_id."""
        pool  = self._make_pool()
        state = pool.get_state("nonexistent-id")
        assert state is None

    def test_list_all_includes_spawned_drone(self):
        """list_all() includes the just-spawned drone."""
        pool = self._make_pool()
        with patch("hive_mind.DroneAgent._run", return_value=None):
            did = pool.spawn(role="exploit", goal="exploit target", backend="groq")
        items = pool.list_all()
        ids   = [d["drone_id"] for d in items]
        assert did in ids

    def test_active_count_decrements_when_done(self):
        """active_count() drops to 0 after the drone completes."""
        pool = self._make_pool()

        def _instant_run(self_inner):
            self_inner.state.status   = "running"
            self_inner.state.started  = time.time()
            time.sleep(0.05)
            self_inner.state.status   = "completed"
            self_inner.state.finished = time.time()

        with patch("hive_mind.DroneAgent._run", _instant_run):
            did = pool.spawn(role="recon", goal="quick test", backend="groq")

        # Wait up to 2 seconds for the thread to finish
        deadline = time.time() + 2.0
        while pool.active_count() > 0 and time.time() < deadline:
            time.sleep(0.05)

        assert pool.active_count() == 0


# ─────────────────────────────────────────────────────────────────────────────
# 6. TestQueenBrain
# ─────────────────────────────────────────────────────────────────────────────

class TestQueenBrain:
    """Unit tests for QueenBrain (orchestration)."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def _make_queen(self):
        from hive_mind import QueenBrain, HiveBus, DronePool
        mem  = _make_hive_memory(self.tmp)
        bus  = HiveBus()
        pool = DronePool(mem, bus)
        return QueenBrain(memory=mem, bus=bus, pool=pool), pool

    def test_plan_enum_returns_multiple_tasks(self):
        """plan() for an enum goal returns >= 2 tasks."""
        queen, _ = self._make_queen()
        tasks = queen.plan("Enumerate SMB and NFS shares")
        assert len(tasks) >= 2
        roles = [t["role"] for t in tasks]
        assert "recon" in roles

    def test_plan_exploit_goal(self):
        """plan() for an exploit goal includes an exploit role."""
        queen, _ = self._make_queen()
        tasks = queen.plan("Exploit CVE-2021-34527 on target")
        roles = [t["role"] for t in tasks]
        assert "exploit" in roles

    def test_plan_ad_goal(self):
        """plan() for Active Directory goal includes lateral role."""
        queen, _ = self._make_queen()
        tasks = queen.plan("Enumerate Active Directory domain users")
        roles = [t["role"] for t in tasks]
        assert "lateral" in roles

    def test_plan_generic_goal(self):
        """plan() for a generic goal returns tasks."""
        queen, _ = self._make_queen()
        tasks = queen.plan("Do something interesting")
        assert len(tasks) >= 1

    def test_plan_n_drones_pads_to_requested(self):
        """plan() with n_drones > template pads to the requested count."""
        queen, _ = self._make_queen()
        tasks = queen.plan("Simple goal", n_drones=10)
        assert len(tasks) >= 10

    def test_dispatch_returns_drone_ids(self):
        """dispatch() spawns drones and returns their IDs."""
        queen, _ = self._make_queen()
        tasks    = [{"role": "recon", "goal": "scan 10.10.11.1"}]
        with patch("hive_mind.DroneAgent._run", return_value=None):
            ids = queen.dispatch(tasks, backend="groq")
        assert len(ids) == 1
        assert isinstance(ids[0], str)

    def test_synthesize_structure(self):
        """synthesize() returns a string with expected headings."""
        queen, pool = self._make_queen()
        with patch("hive_mind.DroneAgent._run", return_value=None):
            did = pool.spawn(role="recon", goal="test", backend="groq")
        # Force state to completed
        pool.get_state(did).status   = "completed"
        pool.get_state(did).result   = "found port 445"
        pool.get_state(did).finished = time.time()

        summary = queen.synthesize([did], "Test goal")
        assert "Hive Synthesis" in summary
        assert "Drones:" in summary


# ─────────────────────────────────────────────────────────────────────────────
# 7. TestHiveMind  (integration)
# ─────────────────────────────────────────────────────────────────────────────

class TestHiveMind:
    """Integration tests for HiveMind (spawn + recall after store)."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def _make_hive(self):
        """Build a fresh HiveMind with isolated storage."""
        from hive_mind import HiveMind, build_default_hive_memory, HiveBus, DronePool, QueenBrain
        mem   = _make_hive_memory(self.tmp)
        bus   = HiveBus()
        pool  = DronePool(mem, bus)
        queen = QueenBrain(memory=mem, bus=bus, pool=pool)
        hive  = HiveMind.__new__(HiveMind)
        hive.memory = mem
        hive.bus    = bus
        hive._pool  = pool
        hive.queen  = queen
        return hive

    def test_spawn_single_drone(self):
        """spawn() creates a drone and returns its id."""
        hive = self._make_hive()
        with patch("hive_mind.DroneAgent._run", return_value=None):
            did = hive.spawn(goal="enumerate ports", role="recon", backend="groq")
        assert isinstance(did, str)
        assert len(did) > 0

    def test_recall_from_memory_after_store(self):
        """Storing data in memory makes it retrievable via hive.recall()."""
        hive = self._make_hive()
        hive.memory.store("found SMB vuln on 10.10.11.78", agent_id="test")
        results = hive.recall("SMB", top_k=5)
        assert len(results) >= 1

    def test_status_contains_expected_fields(self):
        """status() dict contains 'active_drones', 'memory', 'queen_mailbox'."""
        hive = self._make_hive()
        s    = hive.status()
        assert "active_drones" in s
        assert "memory" in s
        assert "queen_mailbox" in s

    def test_drone_result_unknown_id(self):
        """drone_result() for unknown id returns dict with 'error' key."""
        hive   = self._make_hive()
        result = hive.drone_result("no-such-id")
        assert "error" in result

    def test_forget_returns_int(self):
        """forget() returns an integer (count of pruned entries)."""
        hive = self._make_hive()
        n    = hive.forget(older_than_hours=0.0)
        assert isinstance(n, int)


# ─────────────────────────────────────────────────────────────────────────────
# 8. TestMCPHandlers
# ─────────────────────────────────────────────────────────────────────────────

class TestMCPHandlers:
    """Tests for MCP tool handler functions."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)
        # Patch the singleton so tests use isolated storage
        self._build_hive_and_patch()

    def teardown_method(self):
        self._patcher.stop()
        self._tmp.cleanup()

    def _build_hive_and_patch(self):
        from hive_mind import (
            HiveMind, HiveBus, DronePool, QueenBrain,
        )
        mem   = _make_hive_memory(self.tmp)
        bus   = HiveBus()
        pool  = DronePool(mem, bus)
        queen = QueenBrain(memory=mem, bus=bus, pool=pool)
        hive  = HiveMind.__new__(HiveMind)
        hive.memory = mem
        hive.bus    = bus
        hive._pool  = pool
        hive.queen  = queen
        import hive_mind as _hm
        self._patcher = patch.object(_hm, "_hive_instance", hive)
        self._patcher.start()

    def test_mcp_hive_plan_returns_parseable_string(self):
        """mcp_hive_plan() returns a string (text format, not JSON)."""
        from hive_mind import mcp_hive_plan
        result = mcp_hive_plan("Enumerate SMB shares on 10.10.11.78")
        assert isinstance(result, str)
        assert "Hive plan" in result
        assert len(result) > 0

    def test_mcp_hive_status_contains_fields(self):
        """mcp_hive_status() returns valid JSON with expected keys."""
        from hive_mind import mcp_hive_status
        raw  = mcp_hive_status()
        data = json.loads(raw)
        assert "active_drones" in data
        assert "memory" in data
        assert "queen_mailbox" in data

    def test_mcp_hive_recall_no_results(self):
        """mcp_hive_recall() returns a no-results string when memory is empty."""
        from hive_mind import mcp_hive_recall
        result = mcp_hive_recall("xyzzy_nothing_here", top_k=3)
        assert "No hive memories" in result

    def test_mcp_hive_forget_returns_pruned_count(self):
        """mcp_hive_forget() returns a message with 'Pruned' in it."""
        from hive_mind import mcp_hive_forget
        result = mcp_hive_forget(older_than_hours=0.0)
        assert "Pruned" in result

    def test_mcp_hive_spawn_single(self):
        """mcp_hive_spawn() for n_drones=1 returns JSON with drone_id."""
        from hive_mind import mcp_hive_spawn
        with patch("hive_mind.DroneAgent._run", return_value=None):
            raw  = mcp_hive_spawn(goal="test goal", role="recon", n_drones=1)
        data = json.loads(raw)
        assert "drone_id" in data

    def test_mcp_hive_result_unknown_drone(self):
        """mcp_hive_result() for unknown drone returns JSON with error key."""
        from hive_mind import mcp_hive_result
        raw  = mcp_hive_result("no-such-drone")
        data = json.loads(raw)
        assert "error" in data

    def test_mcp_hive_collect_no_ids(self):
        """mcp_hive_collect() with empty csv returns helpful message."""
        from hive_mind import mcp_hive_collect
        result = mcp_hive_collect("", goal="test")
        assert "No drone IDs" in result


# ─────────────────────────────────────────────────────────────────────────────
# 9. TestDroneStateStore
# ─────────────────────────────────────────────────────────────────────────────

class TestDroneStateStore:
    """Unit tests for DroneStateStore (drone persistence across restarts)."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def _make_store(self):
        from hive_mind import DroneStateStore
        return DroneStateStore(db_path=self.tmp / "test_drone_states.db")

    def _make_state(self, status: str = "queued") -> "DroneState":
        from hive_mind import DroneState
        return DroneState(
            drone_id=f"test-{uuid.uuid4().hex[:6]}",
            role="recon",
            goal="test enumeration",
            backend="groq",
            status=status,
            started=time.time(),
        )

    def test_upsert_and_load_all(self):
        """upsert() persists a DroneState; load_all() retrieves it."""
        store = self._make_store()
        state = self._make_state(status="completed")
        store.upsert(state)
        all_states = store.load_all()
        ids = [s.drone_id for s in all_states]
        assert state.drone_id in ids

    def test_upsert_updates_existing(self):
        """Calling upsert() twice with the same drone_id updates the record."""
        store = self._make_store()
        state = self._make_state(status="queued")
        store.upsert(state)
        state.status = "completed"
        state.result = "found open port 22"
        store.upsert(state)
        loaded = store.load_all()
        match  = next(s for s in loaded if s.drone_id == state.drone_id)
        assert match.status == "completed"
        assert match.result == "found open port 22"

    def test_mark_interrupted_targets_queued_and_running(self):
        """mark_interrupted() sets queued/running -> interrupted; completed stays."""
        store = self._make_store()
        s_queued    = self._make_state(status="queued")
        s_running   = self._make_state(status="running")
        s_completed = self._make_state(status="completed")
        for s in (s_queued, s_running, s_completed):
            store.upsert(s)
        n = store.mark_interrupted()
        assert n == 2
        loaded = {s.drone_id: s for s in store.load_all()}
        assert loaded[s_queued.drone_id].status    == "interrupted"
        assert loaded[s_running.drone_id].status   == "interrupted"
        assert loaded[s_completed.drone_id].status == "completed"

    def test_load_interrupted_returns_only_interrupted(self):
        """load_interrupted() returns only drones with status='interrupted'."""
        store = self._make_store()
        s_int   = self._make_state(status="queued")
        s_done  = self._make_state(status="completed")
        store.upsert(s_int)
        store.upsert(s_done)
        store.mark_interrupted()
        interrupted = store.load_interrupted()
        ids = [s.drone_id for s in interrupted]
        assert s_int.drone_id in ids
        assert s_done.drone_id not in ids

    def test_delete_older_than_removes_stale(self):
        """delete_older_than(0) removes all records."""
        store = self._make_store()
        for _ in range(3):
            store.upsert(self._make_state(status="completed"))
        n = store.delete_older_than(days=0.0)
        assert n == 3
        assert store.load_all() == []

    def test_load_all_empty_db(self):
        """load_all() on a fresh store returns an empty list."""
        store = self._make_store()
        assert store.load_all() == []


# ─────────────────────────────────────────────────────────────────────────────
# 10. TestDronePoolWithPersistence
# ─────────────────────────────────────────────────────────────────────────────

class TestDronePoolWithPersistence:
    """Tests for DronePool persistence: spawn persists, recover_from_store works."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)

    def teardown_method(self):
        self._tmp.cleanup()

    def _make_pool_with_store(self):
        from hive_mind import DronePool, DroneStateStore, HiveBus
        mem   = _make_hive_memory(self.tmp)
        bus   = HiveBus()
        store = DroneStateStore(db_path=self.tmp / "pool_states.db")
        pool  = DronePool(mem, bus, state_store=store)
        return pool, store

    def test_spawn_persists_initial_state(self):
        """spawn() writes the initial 'queued' state to DroneStateStore."""
        pool, store = self._make_pool_with_store()
        with patch("hive_mind.DroneAgent._run", return_value=None):
            did = pool.spawn(role="recon", goal="persist test", backend="groq")
        all_states = store.load_all()
        ids = [s.drone_id for s in all_states]
        assert did in ids

    def test_recover_from_store_marks_interrupted(self):
        """recover_from_store() marks in-flight drones as interrupted."""
        pool, store = self._make_pool_with_store()
        from hive_mind import DroneState
        # Simulate a drone that was queued in a previous run
        old_state = DroneState(
            drone_id="reco-abcdef", role="recon", goal="old goal",
            backend="groq", status="running",
        )
        store.upsert(old_state)
        # Fresh pool with same store — simulates a restart
        from hive_mind import DronePool, HiveBus
        mem2  = _make_hive_memory(self.tmp)
        bus2  = HiveBus()
        pool2 = DronePool(mem2, bus2, state_store=store)
        n     = pool2.recover_from_store()
        assert n == 1
        # The recovered state should appear in history
        recovered = pool2.get_state("reco-abcdef")
        assert recovered is not None
        assert recovered.status == "interrupted"

    def test_requeue_interrupted_respawns_drones(self):
        """requeue_interrupted() re-spawns all interrupted drones."""
        pool, store = self._make_pool_with_store()
        from hive_mind import DroneState
        # Plant an interrupted state
        interrupted = DroneState(
            drone_id="reco-zzz111", role="recon", goal="re-run me",
            backend="groq", status="interrupted",
        )
        store.upsert(interrupted)
        with patch("hive_mind.DroneAgent._run", return_value=None):
            new_ids = pool.requeue_interrupted(backend="groq")
        assert len(new_ids) == 1
        assert new_ids[0] != "reco-zzz111"   # new drone_id, same goal

    def test_list_all_includes_history(self):
        """list_all() merges live drones and persisted history."""
        pool, store = self._make_pool_with_store()
        from hive_mind import DroneState
        hist = DroneState(
            drone_id="hist-aaa000", role="report", goal="historical",
            backend="groq", status="completed",
        )
        store.upsert(hist)
        pool.recover_from_store()
        items = pool.list_all()
        ids   = [d["drone_id"] for d in items]
        assert "hist-aaa000" in ids

    def test_mcp_hive_recover_no_interrupted(self):
        """mcp_hive_recover() returns a helpful message when there is nothing to recover."""
        from hive_mind import mcp_hive_recover
        # Fresh hive — no interrupted drones
        result = mcp_hive_recover()
        assert "No interrupted" in result or "recovered" in result.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
