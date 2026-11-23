"""Tests for parallelism knobs and orchestrator-config sections added to the loop."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules import orchestrator_config  # noqa: E402
from modules.loop_guardrails import TargetLimiter  # noqa: E402


class TargetLimiterSpec(unittest.TestCase):
    def test_grow_raises_cap(self):
        limiter = TargetLimiter(max_concurrent=2)
        self.assertEqual(limiter.grow_to(5), 5)
        self.assertEqual(limiter.max_concurrent, 5)

    def test_grow_never_shrinks(self):
        limiter = TargetLimiter(max_concurrent=4)
        self.assertEqual(limiter.grow_to(1), 4)
        self.assertEqual(limiter.max_concurrent, 4)

    def test_grow_permits_more_holders(self):
        import threading

        limiter = TargetLimiter(max_concurrent=1)
        ctx1 = limiter.slot("10.0.0.1")
        ctx1.__enter__()
        acquired = []

        def _hold():
            with limiter.slot("10.0.0.2"):
                acquired.append("second")

        limiter.grow_to(2)
        t = threading.Thread(target=_hold)
        t.start()
        t.join(timeout=2)
        ctx1.__exit__(None, None, None)
        self.assertEqual(acquired, ["second"])


class OrchestratorSectionsSpec(unittest.TestCase):
    def test_ss_cve_config_defaults(self):
        cfg = orchestrator_config.ss_cve_config()
        self.assertTrue(cfg["enabled"])
        self.assertFalse(cfg["llm_summary"])
        self.assertGreaterEqual(cfg["max_services"], 1)

    def test_worker_comms_config_defaults(self):
        cfg = orchestrator_config.worker_comms_config()
        self.assertTrue(cfg["enabled"])
        self.assertTrue(cfg["cross_task_only"])
        self.assertGreaterEqual(cfg["max_messages"], 1)

    def test_validate_accepts_new_sections(self):
        data = {
            "version": 1,
            "stages": {},
            "default_profile": "default",
            "profiles": {
                "default": {
                    "ss_cve": {"enabled": True, "max_services": 3},
                    "worker_comms": {"enabled": False},
                }
            },
        }
        self.assertEqual(orchestrator_config.validate_config(data), [])

    def test_validate_rejects_non_mapping_sections(self):
        data = {
            "version": 1,
            "stages": {},
            "default_profile": "default",
            "profiles": {"default": {"ss_cve": "on", "worker_comms": 5}},
        }
        errors = orchestrator_config.validate_config(data)
        self.assertEqual(len(errors), 2)

    def test_fallback_sinks_include_loop_state(self):
        self.assertTrue(orchestrator_config.FALLBACK_SINKS.get("loop_state"))


if __name__ == "__main__":
    unittest.main()


class DecoyConfigSpec(unittest.TestCase):
    def test_defaults(self):
        cfg = orchestrator_config.decoy_config()
        self.assertIn(cfg["mode"], orchestrator_config.DECOY_MODES)
        self.assertTrue(cfg["operator_allowlist"])

    def test_legacy_payload_key_wins(self, monkeypatch=None):
        import unittest.mock as mock

        with mock.patch.object(
            orchestrator_config,
            "_payload",
            return_value={"c2_decoy_mode": "off", "orchestrator": {"decoy": {"mode": "deny"}}},
        ):
            self.assertEqual(orchestrator_config.decoy_config()["mode"], "off")
        with mock.patch.object(
            orchestrator_config,
            "_payload",
            return_value={"orchestrator": {"decoy": {"mode": "deny"}}},
        ):
            self.assertEqual(orchestrator_config.decoy_config()["mode"], "deny")
        with mock.patch.object(
            orchestrator_config,
            "_payload",
            return_value={"c2_decoy_mode": "bogus", "orchestrator": {}},
        ):
            self.assertEqual(orchestrator_config.decoy_config()["mode"], "page")

    def test_validate_accepts_decoy_mapping(self):
        data = {
            "version": 1,
            "stages": {},
            "default_profile": "default",
            "profiles": {"default": {"decoy": {"mode": "deny"}}},
        }
        self.assertEqual(orchestrator_config.validate_config(data), [])
