"""Harness deterministic-mode contract tests."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from modules import harness


class HarnessFlagSpec(unittest.TestCase):
    """Environment and payload activation semantics."""

    def setUp(self):
        self._old_env = os.environ.pop(harness.HARNESS_ENV_FLAG, None)

    def tearDown(self):
        if self._old_env is not None:
            os.environ[harness.HARNESS_ENV_FLAG] = self._old_env
        else:
            os.environ.pop(harness.HARNESS_ENV_FLAG, None)

    def test_env_flag_enables(self):
        os.environ[harness.HARNESS_ENV_FLAG] = "1"
        self.assertTrue(harness.harness_enabled())
        self.assertFalse(harness.gate("plan_llm"))
        self.assertFalse(harness.gate("worker_agentic"))

    def test_env_flag_off_overrides_profile(self):
        os.environ[harness.HARNESS_ENV_FLAG] = "0"
        self.assertFalse(harness.harness_enabled())
        self.assertTrue(harness.gate("plan_llm"))

    def test_payload_section_enables(self):
        with patch("core.config.load_payload", return_value={"orchestrator": {"harness": True}}):
            self.assertTrue(harness.harness_enabled())

    def test_payload_section_disables(self):
        with patch("core.config.load_payload", return_value={"orchestrator": {"harness": False}}):
            self.assertFalse(harness.harness_enabled())


class HarnessProfileSpec(unittest.TestCase):
    """The orchestrator harness profile exists and carries the gates."""

    def test_profile_present(self):
        from modules.orchestrator_config import profiles

        self.assertIn("harness", profiles())

    def test_profile_flags(self):
        from modules.orchestrator_config import profile_config

        config = profile_config("harness")
        self.assertTrue(config.get("harness"))
        stages = config.get("stages") or {}
        self.assertFalse((stages.get("swan_ensemble") or {}).get("enabled", True))
        self.assertFalse((stages.get("llm_stream") or {}).get("enabled", True))
        self.assertEqual(config.get("chain"), "gym_ms2_foothold")


class GateSpec(unittest.TestCase):
    """lazy_loop consults the harness gates before LLM surfaces."""

    def _planner_returns_none_without_llm(self):
        from modules.lazy_loop import Planner

        planner = Planner.__new__(Planner)
        planner.store = None
        planner.task_id = "t0001"
        planner.graph = None
        planner.assets = None
        planner._denied = lambda text: False
        return planner

    def test_plan_llm_gate_blocked_under_harness(self):
        planner = self._planner_returns_none_without_llm()
        with patch.object(harness, "harness_enabled", return_value=True):
            self.assertEqual(planner._llm_candidates(set()), [])

    def test_worker_agentic_gate_blocked_under_harness(self):
        from modules.lazy_loop import Worker

        worker = Worker.__new__(Worker)
        worker.name = "worker-1"
        worker.graph = None
        worker.store = None
        called = []

        def _explode(*_args, **_kwargs):
            called.append(True)
            return True

        worker._agentic_try = _explode
        outcome: dict = {"state": ""}
        with patch.object(harness, "harness_enabled", return_value=True):
            blocked = not harness.gate("worker_agentic")
        self.assertTrue(blocked)
        self.assertEqual(called, [])

    def test_worker_llm_steps_gate_keeps_base_steps(self):
        from modules.lazy_loop import Worker

        worker = Worker.__new__(Worker)
        worker.store = None
        worker.task_id = "t0001"
        called = []

        def _llm_steps(_intent, _prior):
            called.append(True)
            return ["curl http://x"]

        worker._llm_steps = _llm_steps
        base = ["lazynmap 10.0.0.5"]
        with patch.object(harness, "harness_enabled", return_value=True):
            self.assertEqual(worker._with_llm_steps(None, base, ""), base)
        self.assertEqual(called, [])


class ChainDirectiveSpec(unittest.TestCase):
    """``auto chain <name> <target>`` translates into an apt_chain step."""

    def test_known_chain_resolves(self):
        from modules.auto_registry import steps_for

        resolved = steps_for("auto chain gym_ms2_foothold 172.17.0.2", "")
        self.assertEqual(resolved, ["apt_chain gym_ms2_foothold 172.17.0.2"])

    def test_unknown_chain_rejected(self):
        from modules.auto_registry import steps_for

        self.assertIsNone(steps_for("auto chain does_not_exist 172.17.0.2", ""))

    def test_target_token_fallback(self):
        from modules.auto_registry import steps_for

        resolved = steps_for("auto chain gym_ms2_foothold", "10.0.0.2")
        self.assertEqual(resolved, ["apt_chain gym_ms2_foothold 10.0.0.2"])


class ObjectiveDirectiveSpec(unittest.TestCase):
    """golden_path pushes chain-directive objectives."""

    def test_push_objective_text_carries_directive(self):
        from modules import golden_path

        with tempfile.TemporaryDirectory() as tmp:
            store_path = Path(tmp) / "objectives.jsonl"
            objs = golden_path.push_objectives(
                [{"target": "172.17.0.2", "cost": 1.0, "summary": "x[exploit]", "steps": []}],
                store_path=store_path,
            )
            self.assertTrue(objs)
            self.assertTrue(objs[0].text.startswith("auto chain gym_ms2_foothold 172.17.0.2"))


if __name__ == "__main__":
    unittest.main()
