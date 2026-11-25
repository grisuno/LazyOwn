"""Tests for the SQLite event store and worker communication board."""

from __future__ import annotations

import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.loop.event_store import (  # noqa: E402
    MESSAGE_KINDS,
    EventStore,
    fleet_prompt_context,
    record_outcome,
)


def _tmp_dir() -> Path:
    return Path(tempfile.mkdtemp())


class EventStoreSpec(unittest.TestCase):
    def setUp(self):
        self.tmp = _tmp_dir()
        self.store = EventStore()

    def test_append_and_read_events(self):
        row_id = self.store.append_event(
            {"kind": "exploit", "host": "10.0.0.1", "task_id": "t1", "title": "shell", "severity": "high"}
        )
        self.assertGreater(row_id, 0)
        rows = self.store.events(task_id="t1")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["kind"], "exploit")
        self.assertEqual(rows[0]["payload"].get("title"), "shell")

    def test_foothold_and_message_filters(self):
        self.store.post_foothold("t1", "worker-1", "10.0.0.1", "SYSTEM shell")
        self.store.post_message("t2", "ss", "intel", "CVE-2021-41773 hot")
        self.assertEqual(len(self.store.footholds()), 1)
        self.assertEqual(len(self.store.messages(kind="intel")), 1)
        self.assertEqual(len(self.store.messages(task_id="t2")), 1)

    def test_message_kinds_validated(self):
        self.assertEqual(self.store.post_message("t1", "w", "bogus", "x"), 0)
        self.assertEqual(self.store.post_message("t1", "w", "note", "  "), 0)
        self.assertIn("foothold", MESSAGE_KINDS)

    def test_fleet_context_excludes_own_task(self):
        self.store.post_message("t1", "worker-1", "progress", "own task line")
        self.store.post_message("t2", "worker-2", "foothold", "10.0.0.9: root")
        text = fleet_prompt_context("t1", limit=5) or ""
        self.assertIn("worker-2", text)
        self.assertNotIn("own task line", text)

    def test_fleet_context_includes_all_when_no_task(self):
        self.store.post_message("t1", "worker-1", "progress", "own task line")
        text = fleet_prompt_context("", limit=5) or ""
        self.assertIn("own task line", text)

    def test_record_outcome_posts_foothold_on_shell(self):
        record_outcome(
            {
                "kind": "exploit",
                "host": "10.0.0.5",
                "task_id": "t9",
                "title": "rce",
                "success": True,
                "shell": True,
                "metadata": {"worker": "worker-3"},
            }
        )
        holds = self.store.footholds()
        self.assertEqual(len(holds), 1)
        self.assertIn("worker-3", holds[0]["worker"])

    def test_record_outcome_ignores_non_shell(self):
        record_outcome({"kind": "recon", "host": "h", "task_id": "t", "title": "scan", "success": True})
        self.assertEqual(len(self.store.footholds()), 0)

    def test_summary_and_prune(self):
        self.store.post_message("t1", "w", "note", "a")
        self.store.post_message("t1", "w", "note", "b")
        self.store.post_message("t1", "w", "intel", "c")
        self.store.append_event({"kind": "recon", "title": "x"})
        summary = self.store.summary("t1")
        self.assertEqual(summary["by_kind"].get("note"), 2)
        pruned = self.store.prune(max_events=0, max_messages=2)
        self.assertGreaterEqual(pruned["messages"], 1)
        self.assertEqual(len(self.store.messages()), 2)

    def test_thread_connections_are_independent(self):
        errors = []
        db_path = self.tmp / "loop_state.db"

        def _write():
            try:
                store = EventStore(db_path)
                store.post_message("tX", f"w-{threading.get_ident()}", "note", "hello")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=_write) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        self.assertEqual(len(EventStore(db_path).messages()), 4)


if __name__ == "__main__":
    unittest.main()
