"""Tests for the loop_state outcome sink and ss CVE context builder."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules import ss_cve_context  # noqa: E402
from modules.loop.event_store import EventStore  # noqa: E402
from modules.outcome_bus import OutcomeEvent  # noqa: E402
from modules.sinks import loop_state as sink  # noqa: E402


def _tmp_dir() -> Path:
    return Path(tempfile.mkdtemp())


class LoopStateSinkSpec(unittest.TestCase):
    def setUp(self):
        self.tmp = _tmp_dir()
        self.store = EventStore(self.tmp / "state.db")
        self._orig_shared = sink.record_outcome
        import modules.loop.event_store as es

        self._orig_es_shared = es._shared
        es._shared = self.store
        self._es = es

    def tearDown(self):
        self._es._shared = self._orig_es_shared

    def test_sink_appends_event(self):
        event = OutcomeEvent(kind="recon", host="10.0.0.1", task_id="t1", title="scan", success=False)
        self.assertTrue(sink.apply(event))
        rows = self.store.events(task_id="t1")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["kind"], "recon")

    def test_sink_posts_foothold_on_shell_success(self):
        event = OutcomeEvent(
            kind="exploit",
            host="10.0.0.1",
            task_id="t1",
            title="rce",
            success=True,
            shell=True,
            metadata={"worker": "worker-2"},
        )
        self.assertTrue(sink.apply(event))
        holds = self.store.footholds()
        self.assertEqual(len(holds), 1)
        self.assertIn("worker-2", holds[0]["worker"])


class SsCveContextSpec(unittest.TestCase):
    def test_rows_from_results(self):
        from cli.exploit_advisor import ServiceInfo

        rows = ss_cve_context.rows_from_results([{"port": 22, "name": "ssh", "product": "OpenSSH", "version": "8.4"}])
        self.assertEqual(rows[0]["product"], "OpenSSH")
        svc = ServiceInfo(port=80, protocol="tcp", name="http", product="nginx", version="1.2")
        rows = ss_cve_context.rows_from_results([type("R", (), {"service": svc})()])
        self.assertEqual(rows[0]["port"], 80)

    def test_render_block_and_gate(self):
        payload = {
            "services": [
                {
                    "port": 22,
                    "product": "OpenSSH",
                    "version": "8.4",
                    "cves": [
                        {"cve": "CVE-2023-38408", "heat": "high", "kev": True, "exploit": False, "in_range": True}
                    ],
                }
            ]
        }
        block = ss_cve_context.render_block(payload)
        self.assertIn("CVE-2023-38408", block)
        self.assertIn("kev", block)
        self.assertEqual(ss_cve_context.render_block({"services": []}), "")

    def test_llm_summary_disabled_by_default(self):
        payload = {
            "services": [
                {
                    "port": 22,
                    "product": "x",
                    "version": "",
                    "cves": [{"cve": "CVE-1", "heat": "high", "kev": False, "exploit": False, "in_range": False}],
                }
            ]
        }
        self.assertEqual(ss_cve_context.llm_summary(payload, {"llm_summary": False}), "")

    def test_llm_summary_injectable(self):
        payload = {
            "services": [
                {
                    "port": 22,
                    "product": "x",
                    "version": "",
                    "cves": [{"cve": "CVE-1", "heat": "high", "kev": False, "exploit": False, "in_range": False}],
                }
            ]
        }
        seen = {}

        def fake_complete(prompt, max_tokens):
            seen["prompt"] = prompt
            return " 1. CVE-1 - hot - exploit it "

        text = ss_cve_context.llm_summary(payload, {"llm_summary": True}, complete_fn=fake_complete)
        self.assertIn("CVE-1", text)
        self.assertIn("UNTRUSTED", seen["prompt"])

    def test_save_context(self):
        tmp = _tmp_dir()
        path = ss_cve_context.save_context({"total_cves": 1}, "10.0.0.1", path=tmp / "ctx.json")
        self.assertTrue(path.exists())
        self.assertIn("total_cves", path.read_text())


if __name__ == "__main__":
    unittest.main()
