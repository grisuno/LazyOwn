"""Contract tests for the lazycreds default-credential knowledge base."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from modules import lazy_creds


class LazyCredsKbSpec(unittest.TestCase):
    """Knowledge base load, search and export contract."""

    def test_kb_loads_rows(self):
        rows = lazy_creds.load()
        self.assertGreater(len(rows), 500)
        self.assertEqual(lazy_creds.count(), len(rows))
        first = rows[0]
        self.assertTrue(first.vendor)
        self.assertTrue(first.username)

    def test_search_matches_vendor_and_username(self):
        self.assertTrue(lazy_creds.search("apache"))
        self.assertTrue(lazy_creds.search("admin"))
        self.assertEqual(lazy_creds.search("no-vendor-like-this-xyz"), [])
        self.assertEqual(lazy_creds.search(""), [])

    def test_search_is_case_insensitive(self):
        lower = [r.username for r in lazy_creds.search("tomcat")]
        upper = [r.username for r in lazy_creds.search("TOMCAT")]
        self.assertEqual(lower, upper)

    def test_search_capped(self):
        rows = lazy_creds.search("a")
        self.assertLessEqual(len(rows), lazy_creds.MAX_OUTPUT_ROWS)

    def test_candidates_distinct_and_ranked(self):
        rows = lazy_creds.candidates(10)
        self.assertTrue(rows)
        pairs = [(row.username, row.password) for row in rows]
        self.assertEqual(len(pairs), len(set(pairs)))

    def test_as_lines_rendered(self):
        lines = lazy_creds.as_lines(lazy_creds.search("apache"))
        self.assertTrue(lines[0].strip())

    def test_export_pairs_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pairs.txt"
            result = lazy_creds.export_pairs(target, limit=25)
            self.assertEqual(result["error"], "")
            self.assertEqual(result["written"], 25)
            content = target.read_text().strip().splitlines()
            self.assertEqual(len(content), 25)
            self.assertIn(":", content[0])

    def test_export_rejects_bad_path(self):
        result = lazy_creds.export_pairs("/definitely/not/a/dir/pairs.txt")
        self.assertTrue(result["error"])


if __name__ == "__main__":
    unittest.main()
