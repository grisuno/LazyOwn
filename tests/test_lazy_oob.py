"""Contract tests for the lazyoob OOB canary."""

from __future__ import annotations

import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

from modules import lazy_oob


class LazyOobCanarySpec(unittest.TestCase):
    """Canary lifecycle and hit recording contract."""

    def setUp(self):
        lazy_oob.reset()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        patcher = patch.object(lazy_oob, "HITS_PATH", Path(self._tmp.name) / "oob_hits.jsonl")
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(lazy_oob.reset)

    def test_start_picks_ephemeral_port(self):
        result = lazy_oob.start(host="127.0.0.1")
        self.assertTrue(result["ok"])
        self.assertGreater(result["port"], 0)
        self.assertIn("/oob/", result["url"])
        self.assertTrue(lazy_oob.is_running())

    def test_start_twice_reuses_listener(self):
        first = lazy_oob.start(host="127.0.0.1")
        second = lazy_oob.start(host="127.0.0.1")
        self.assertTrue(first["ok"])
        self.assertTrue(second["ok"])
        self.assertTrue(second["already"])
        self.assertEqual(first["port"], second["port"])

    def test_url_reuses_active_token(self):
        result = lazy_oob.start(host="127.0.0.1")
        self.assertIn(result["token"], lazy_oob.url())
        self.assertIn("custom-token", lazy_oob.url("custom-token"))

    def test_url_empty_when_not_running(self):
        self.assertEqual(lazy_oob.url(), "")

    def test_callback_recorded(self):
        result = lazy_oob.start(host="127.0.0.1")
        token = result["token"]
        urllib.request.urlopen(lazy_oob.url(token), timeout=5).read()
        rows = lazy_oob.hits(token)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["token"], token)
        self.assertEqual(rows[0]["method"], "GET")
        self.assertTrue(rows[0]["source"])

    def test_hit_mirrored_to_jsonl(self):
        result = lazy_oob.start(host="127.0.0.1")
        urllib.request.urlopen(lazy_oob.url(result["token"]), timeout=5).read()
        mirror = lazy_oob.HITS_PATH.read_text().strip().splitlines()
        self.assertEqual(len(mirror), 1)
        self.assertIn(result["token"], mirror[0])

    def test_hits_filter_by_token(self):
        first = lazy_oob.start(host="127.0.0.1")
        urllib.request.urlopen(lazy_oob.url(first["token"]), timeout=5).read()
        self.assertEqual(len(lazy_oob.hits(first["token"])), 1)
        self.assertEqual(lazy_oob.hits("unknown-token"), [])
        self.assertEqual(len(lazy_oob.hits()), 1)

    def test_stop_reports_and_clears(self):
        result = lazy_oob.start(host="127.0.0.1")
        urllib.request.urlopen(lazy_oob.url(result["token"]), timeout=5).read()
        stopped = lazy_oob.stop()
        self.assertTrue(stopped["ok"])
        self.assertEqual(stopped["hits"], 1)
        self.assertFalse(lazy_oob.is_running())
        self.assertEqual(lazy_oob.url(), "")

    def test_stop_without_start_is_guidance(self):
        stopped = lazy_oob.stop()
        self.assertTrue(stopped["ok"])
        self.assertEqual(stopped["hits"], 0)

    def test_start_bad_bind_fails_loud(self):
        result = lazy_oob.start(host="203.0.113.9", port=1)
        self.assertFalse(result["ok"])
        self.assertTrue(result["error"])


if __name__ == "__main__":
    unittest.main()
