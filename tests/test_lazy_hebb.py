"""Tests for the LazyHebb zero-inference synaptic memory."""

from __future__ import annotations

import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules import lazy_hebb  # noqa: E402


def _tmp_db() -> str:
    return str(Path(tempfile.mkdtemp()) / "hebb.sqlite")


class LazyHebbSpec(unittest.TestCase):
    def setUp(self):
        self.hebb = lazy_hebb.LazyHebb(_tmp_db())

    def test_store_and_spark_roundtrip(self):
        uid = self.hebb.store("valid admin credential on 10.0.0.5", agent_id="worker-1", phase="lateral")
        self.assertTrue(uid)
        winners = self.hebb.spark("admin credential")
        self.assertEqual(len(winners), 1)
        self.assertIn("10.0.0.5", winners[0]["content"])
        self.assertEqual(winners[0]["agent_id"], "worker-1")

    def test_sem_suffix_indexed_for_semantic_recall(self):
        self.hebb.store("persist event id first | sem: dog, furry friend, pet")
        winners = self.hebb.spark("dog grooming")
        self.assertEqual(len(winners), 1)

    def test_auto_seed_tags_maps_keywords(self):
        tags = lazy_hebb.auto_seed_tags("psexec succeeded against host")
        self.assertIn("lateral", tags)
        self.assertIn("smb", tags)
        self.assertEqual(lazy_hebb.auto_seed_tags(""), "")

    def test_parse_sem_suffix(self):
        body, tags = lazy_hebb.parse_sem_tags("do the thing | sem: a, b, c")
        self.assertEqual(body, "do the thing")
        self.assertEqual(tags, "a, b, c")
        body, tags = lazy_hebb.parse_sem_tags("no suffix here")
        self.assertEqual(tags, "")

    def test_private_firewall_blocks_recall_and_bridge(self):
        self.hebb.store("public recon note alpha")
        self.hebb.store("operator zqx secret", private=True)
        self.assertEqual(len(self.hebb.spark("zqx secret")), 0)
        self.assertEqual(len(self.hebb.spark("zqx secret", include_private=True)), 1)
        self.assertEqual(len(self.hebb.spark("recon alpha")), 1)

    def test_fts_operator_abuse_is_safe(self):
        self.hebb.store("safe note")
        winners = self.hebb.spark('"; DROP TABLE hebb_memories; -- NOT (valid " unbalanced')
        self.assertIsInstance(winners, list)
        self.assertGreaterEqual(self.hebb.stats()["memories"], 1)

    def test_spreading_activation_recalls_neighbour(self):
        self.hebb.store("stripe webhook duplicate charge anchor")
        self.hebb.store("cloudflare waf rule tuned")
        for _ in range(3):
            self.hebb.spark("stripe webhook duplicate charge anchor cloudflare waf rule tuned")
        self.assertGreater(self.hebb.stats()["edges"], 0)
        path = self.hebb.bridge("stripe webhook", "cloudflare waf")
        self.assertEqual(len(path), 2)
        self.assertIn("duplicate charge", path[0])

    def test_bridge_unreachable_returns_empty(self):
        self.hebb.store("isolated topic alpha")
        self.hebb.store("unrelated topic omega")
        self.assertEqual(self.hebb.bridge("isolated topic alpha", "unrelated topic omega"), [])

    def test_spark_strengthen_then_recall_propagates(self):
        self.hebb.store("kerberoast service accounts target")
        self.hebb.store("impaired GetUserSPNs mitm")
        for _ in range(3):
            self.hebb.spark("kerberoast service accounts target impaired GetUserSPNs mitm")
        winners = self.hebb.spark("kerberoast", top_k=5)
        self.assertTrue(any(w["hops"] == 1 for w in winners))

    def test_forget_by_topic_and_age(self):
        self.hebb.store("stale note alpha", agent_id="x")
        self.hebb.store("aged note beta", agent_id="x")
        time.sleep(0.15)
        self.hebb.store("fresh note gamma", agent_id="x")
        self.assertEqual(self.hebb.forget(topic="alpha"), 1)
        self.assertEqual(self.hebb.forget(older_than_hours=0.00003), 1)
        self.assertEqual(self.hebb.stats()["memories"], 1)
        self.assertEqual(self.hebb.forget(topic="gamma"), 1)
        self.assertEqual(self.hebb.stats()["memories"], 0)

    def test_forget_private_needs_opt_in(self):
        self.hebb.store("private thing", private=True)
        self.assertEqual(self.hebb.forget(topic="private"), 0)
        self.assertEqual(self.hebb.forget(topic="private", include_private=True), 1)

    def test_row_cap_prunes_oldest(self):
        with mock.patch.object(lazy_hebb, "MAX_ROWS", 3):
            for index in range(5):
                self.hebb.store(f"memory number {index}")
            self.assertEqual(self.hebb.stats()["memories"], 3)

    def test_export_import_markdown_roundtrip(self):
        tmp = Path(tempfile.mkdtemp())
        target = tmp / "hebb.md"
        self.hebb.store("rule one about ssh keys | sem: ssh, lateral")
        self.hebb.store("rule two about kerberoast", private=True)
        self.assertEqual(self.hebb.export_markdown(target), 2)
        text = target.read_text()
        self.assertIn("| sem: ssh, lateral", text)
        self.assertIn("[P]", text)
        other = lazy_hebb.LazyHebb(_tmp_db())
        self.assertEqual(other.import_markdown(target), 2)
        self.assertEqual(len(other.spark("ssh keys")), 1)

    def test_stats_shape(self):
        stats = self.hebb.stats()
        self.assertIn("memories", stats)
        self.assertIn("edges", stats)
        self.assertIn("private", stats)

    def test_store_dedups_same_content_and_agent(self):
        first = self.hebb.store("unique payload note", agent_id="w1")
        second = self.hebb.store("unique payload note", agent_id="w1")
        self.assertEqual(first, second)
        self.assertEqual(self.hebb.stats()["memories"], 1)
        other_agent = self.hebb.store("unique payload note", agent_id="w2")
        self.assertNotEqual(first, other_agent)
        self.assertEqual(self.hebb.stats()["memories"], 2)

    def test_last_recall_stats_populated(self):
        self.hebb.store("remember the pivot host")
        with mock.patch.object(lazy_hebb, "shared_hebb", return_value=self.hebb):
            lazy_hebb.hebb_prompt_context("remember the pivot host")
            stats = lazy_hebb.last_recall()
            self.assertGreaterEqual(stats["count"], 1)
            self.assertGreaterEqual(stats["ms"], 0.0)
            lazy_hebb.hebb_prompt_context("zzz unmatched token qqq")
            self.assertEqual(lazy_hebb.last_recall()["count"], 0)

    def test_context_hard_char_cap(self):
        for index in range(12):
            self.hebb.store(f"distinct memory about ssh pivot {index} with enough text to be long")
        with mock.patch.object(lazy_hebb, "shared_hebb", return_value=self.hebb):
            ctx = lazy_hebb.hebb_prompt_context("ssh pivot", top_k=12)
        self.assertLessEqual(len(ctx), lazy_hebb.HEBB_CONTEXT_MAX_CHARS)

    def test_edge_cap_prunes_weakest(self):
        with mock.patch.object(lazy_hebb, "MAX_EDGES", 5), mock.patch.object(lazy_hebb, "EDGE_PRUNE_BATCH", 2):
            anchors = [self.hebb.store(f"edge anchor {index}") for index in range(8)]
            for index in range(len(anchors) - 1):
                for _ in range(2):
                    self.hebb.spark(f"edge anchor {index} edge anchor {index + 1}")
            self.assertLessEqual(self.hebb.stats()["edges"], 5 + 3)

    def test_remember_outcome_builds_content(self):
        uid = lazy_hebb.remember_outcome(
            {
                "kind": "exploit",
                "title": "root shell",
                "host": "10.0.0.9",
                "task_id": "t1",
                "metadata": {"worker": "worker-7"},
            }
        )
        self.assertTrue(uid)
        winners = lazy_hebb.shared_hebb().spark("root shell")
        self.assertIn("worker-7", winners[0]["content"])

    def test_hebb_prompt_context_renders_line(self):
        lazy_hebb.shared_hebb().store("valid creds admin on 10.0.0.5", phase="lateral", agent_id="w1")
        text = lazy_hebb.hebb_prompt_context("valid creds admin")
        self.assertTrue(text.startswith("Hebb intel:"))
        self.assertIn("10.0.0.5", text)

    def test_hebb_prompt_context_disabled_is_empty(self):
        with mock.patch("modules.orchestrator_config.hebb_config", return_value={"enabled": False}):
            self.assertEqual(lazy_hebb.hebb_prompt_context("anything"), "")


class HiveAdapterSpec(unittest.TestCase):
    def test_hebb_store_satisfies_hive_contract(self):
        from skills.hive_mind import HebbStore

        store = HebbStore(_tmp_db())
        event_id = store.store("pivot through dmz host", agent_id="queen", event_type="lateral")
        self.assertTrue(event_id)
        rows = store.recall("pivot dmz")
        self.assertEqual(rows[0]["layer"], "hebb")

    def test_default_hive_memory_uses_hebb_semantic_layer(self):
        import os

        from skills.hive_mind import HebbStore, build_default_hive_memory

        tmp = Path(tempfile.mkdtemp())
        old_cwd = os.getcwd()
        os.chdir(tmp)
        try:
            hive = build_default_hive_memory(db_path=tmp / "hive.sqlite")
        finally:
            os.chdir(old_cwd)
        self.assertIsInstance(hive._semantic, HebbStore)
        hive.store("lateral movement via psexec", agent_id="queen")
        rows = hive.recall_semantic("lateral psexec")
        self.assertTrue(rows)
        rows_all = hive.recall("lateral psexec")
        self.assertTrue(any(row.get("layer") in {"hebb", "semantic"} for row in rows_all))


if __name__ == "__main__":
    unittest.main()
