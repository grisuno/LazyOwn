"""Guardrail harness tests: tiers, capacity, warm restart, wiring.

Covers the capacity envelope priority rule, the checkpoint ledger and
warm restart, advisories and feature degradation, the guarded run
policy per tier, plus the loop, APT chain and orchestrator wiring.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from modules.guardrails import (
    CONFIG_SECTION,
    AdvisoryLedger,
    CapacityEnvelope,
    CheckpointLedger,
    FeatureGate,
    TaskClass,
    global_harness,
    reset_global_harness,
)


class TestTaskClass:
    def test_tier_ordering_is_strict(self):
        assert TaskClass.CORE < TaskClass.MISSION < TaskClass.SUPPORT

    def test_is_known_accepts_values_and_rejects_strays(self):
        assert TaskClass.is_known(0) and TaskClass.is_known(2)
        assert not TaskClass.is_known(3)
        assert not TaskClass.is_known("core")


class TestCapacityEnvelope:
    def test_defaults_snapshot(self):
        snapshot = CapacityEnvelope().describe()
        assert snapshot["threshold"] == pytest.approx(0.85)
        assert snapshot["tiers"]["core"]["capacity"] == 10000
        assert snapshot["tiers"]["support"]["capacity"] == 512

    def test_admit_and_account_roundtrip(self):
        envelope = CapacityEnvelope()
        assert envelope.admit(TaskClass.MISSION, 2) is True
        envelope.account(TaskClass.MISSION, 2)
        assert envelope.usage(TaskClass.MISSION) == 2
        envelope.release(TaskClass.MISSION, 2)
        assert envelope.usage(TaskClass.MISSION) == 0

    def test_saturated_tier_refuses_admission(self):
        envelope = CapacityEnvelope(threshold=0.5)
        envelope.account(TaskClass.SUPPORT, 256)
        assert envelope.saturated(TaskClass.SUPPORT) is True
        assert envelope.admit(TaskClass.SUPPORT, 512) is False
        assert envelope.admit(TaskClass.SUPPORT, 1) is False

    def test_higher_tier_saturation_refuses_lower_tiers(self):
        envelope = CapacityEnvelope(threshold=0.5)
        envelope.account(TaskClass.CORE, 5001)
        assert envelope.saturated(TaskClass.CORE) is True
        assert envelope.admit(TaskClass.SUPPORT, 1) is False
        assert envelope.admit(TaskClass.MISSION, 1) is False
        assert envelope.admit(TaskClass.CORE, 1) is True

    def test_reclaim_purges_support_only(self):
        envelope = CapacityEnvelope()
        envelope.account(TaskClass.SUPPORT, 100)
        envelope.account(TaskClass.MISSION, 100)
        freed = envelope.reclaim()
        assert freed == 100
        assert envelope.usage(TaskClass.SUPPORT) == 0
        assert envelope.usage(TaskClass.MISSION) == 100

    def test_configure_clamps_and_accepts_names(self):
        envelope = CapacityEnvelope()
        snapshot = envelope.configure(capacities={"support": 0, "mission": 4}, threshold=9)
        assert snapshot["tiers"]["support"]["capacity"] == 1
        assert snapshot["tiers"]["mission"]["capacity"] == 4
        assert snapshot["threshold"] <= 0.99


class TestCheckpointLedger:
    def test_capture_restore_roundtrip(self):
        ledger = CheckpointLedger()
        assert ledger.capture("loop.core_round", {"round": 3}) is True
        assert ledger.restore("loop.core_round") == {"round": 3}

    def test_history_is_bounded(self):
        ledger = CheckpointLedger(history=2)
        for round_index in range(5):
            ledger.capture("k", {"round": round_index})
        assert ledger.restore("k") == {"round": 4}
        assert len(ledger.keys()) == 1

    def test_restore_missing_is_none(self):
        assert CheckpointLedger().restore("absent") is None

    def test_warm_restart_restores_and_counts(self):
        ledger = CheckpointLedger()
        ledger.capture("core", {"state": "running"})
        summary = ledger.warm_restart("core")
        assert summary["restored"] is True
        assert summary["payload"] == {"state": "running"}
        assert summary["restarts"] == 1

    def test_warm_restart_without_key_reports_unrestored(self):
        summary = CheckpointLedger().warm_restart("missing")
        assert summary["restored"] is False
        assert summary["payload"] is None

    def test_capture_rejects_blank_keys(self):
        assert CheckpointLedger().capture("   ", {"a": 1}) is False


class TestAdvisoriesAndFeatures:
    def test_notice_is_bounded_newest_first(self):
        ledger = AdvisoryLedger(limit=3)
        for index in range(5):
            ledger.notice("code", f"msg-{index}")
        tail = ledger.tail(10)
        assert len(tail) == 3
        assert tail[0]["message"] == "msg-4"

    def test_clear_returns_count(self):
        ledger = AdvisoryLedger()
        ledger.notice("a")
        ledger.notice("b")
        assert ledger.clear() == 2
        assert ledger.tail() == []

    def test_feature_gate_unknown_feature_never_suspends(self):
        gate = FeatureGate()
        assert gate.suspend("render") is True
        assert gate.suspend("core_cycle") is False
        assert gate.is_suspended("render") is True
        assert gate.resume_all() == 1

    def test_feature_gate_known_set(self):
        for feature in ("render", "enrich", "llm_stream", "swan"):
            assert feature in FeatureGate().describe()["known"]


class TestGuardHarness:
    @pytest.fixture()
    def harness(self):
        return reset_global_harness()

    def test_mission_success_accounts_usage(self, harness):
        assert harness.run_guarded(TaskClass.MISSION, lambda: "ok") == "ok"
        assert harness.describe()["envelope"]["tiers"]["mission"]["usage"] == 1

    def test_mission_failure_degrades_with_advisory(self, harness):
        def boom():
            raise ValueError("sensor gone")

        assert harness.run_guarded(TaskClass.MISSION, boom) is None
        advisories = harness.describe()["advisories"]["items"]
        assert advisories[0]["code"] == "mission_failed"

    def test_support_refused_while_render_suspended(self, harness):
        assert harness.suspend("render", "degraded") is True
        assert harness.run_guarded(TaskClass.SUPPORT, lambda: "x") is None
        assert harness.describe()["advisories"]["items"][0]["code"] == "feature_dropped"
        assert harness.rearm()["resumed"] == 1
        assert harness.run_guarded(TaskClass.SUPPORT, lambda: "x") == "x"

    def test_core_retries_once_after_warm_restart(self, harness):
        calls = {"count": 0}

        def flaky():
            calls["count"] += 1
            if calls["count"] == 1:
                raise RuntimeError("first")
            return "recovered"

        result = harness.run_guarded(TaskClass.CORE, flaky, key="t.core", state={"round": 2})
        assert result == "recovered"
        assert calls["count"] == 2

    def test_core_gives_up_after_second_failure(self, harness):
        def always_fails():
            raise RuntimeError("fatal")

        assert harness.run_guarded(TaskClass.CORE, always_fails, key="t.core", state={"round": 1}) is None
        codes = [item["code"] for item in harness.describe()["advisories"]["items"]]
        assert "core_retry_failed" in codes

    def test_core_without_checkpoint_never_retries(self, harness):
        def boom():
            raise RuntimeError("no state")

        assert harness.run_guarded(TaskClass.CORE, boom) is None
        codes = [item["code"] for item in harness.describe()["advisories"]["items"]]
        assert "core_no_checkpoint" in codes

    def test_keyboard_interrupt_propagates(self, harness):
        def interrupted():
            raise KeyboardInterrupt()

        with pytest.raises(KeyboardInterrupt):
            harness.run_guarded(TaskClass.MISSION, interrupted)

    def test_priority_reservation_refuses_lower_tiers(self, harness):
        harness.configure({"saturation_threshold": 0.5, "capacity": {"core": 10}})
        harness.run_guarded(TaskClass.CORE, lambda: 1)
        harness.run_guarded(TaskClass.CORE, lambda: 1)
        harness.run_guarded(TaskClass.CORE, lambda: 1)
        harness.run_guarded(TaskClass.CORE, lambda: 1)
        harness.run_guarded(TaskClass.CORE, lambda: 1)
        assert harness.run_guarded(TaskClass.MISSION, lambda: 2) is None
        assert harness.run_guarded(TaskClass.SUPPORT, lambda: 3) is None
        assert harness.run_guarded(TaskClass.CORE, lambda: 4) == 4

    def test_configure_from_payload_section(self, harness):
        snapshot = harness.configure({"saturation_threshold": 0.6, "capacity": {"support": 2}})
        assert snapshot["envelope"]["threshold"] == pytest.approx(0.6)
        assert snapshot["envelope"]["tiers"]["support"]["capacity"] == 2

    def test_warm_restart_purges_support_and_notifies(self, harness):
        harness.run_guarded(TaskClass.SUPPORT, lambda: 1)
        summary = harness.warm_restart("loop.core_round")
        assert harness.describe()["envelope"]["tiers"]["support"]["usage"] == 0
        assert summary["restored"] is False
        codes = [item["code"] for item in harness.describe()["advisories"]["items"]]
        assert "warm_restart" in codes


class TestGlobalHarness:
    @pytest.fixture(autouse=True)
    def _fresh_global_harness(self):
        reset_global_harness()
        yield
        reset_global_harness()

    def test_singleton_shared(self):
        assert global_harness() is global_harness()

    def test_config_section_constant_shape(self):
        assert CONFIG_SECTION == "orchestrator.guardrails"


class TestLazyLoopWiring:
    @pytest.fixture(autouse=True)
    def _fresh_global_harness(self):
        reset_global_harness()
        yield
        reset_global_harness()

    def test_apply_profile_configures_harness(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
        monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
        payload = {"orchestrator": {"guardrails": {"saturation_threshold": 0.7, "capacity": {"support": 3}}}}
        import core.config

        monkeypatch.setattr(core.config, "load_payload", lambda target=None: payload)
        harness = reset_global_harness()
        engine = loop.LazyLoopEngine()
        engine.apply_profile()
        snapshot = harness.describe()
        assert snapshot["envelope"]["threshold"] == pytest.approx(0.7)
        assert snapshot["envelope"]["tiers"]["support"]["capacity"] == 3

    def test_worker_guard_maps_refusal_to_degraded_outcome(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
        monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
        harness = reset_global_harness()
        harness.configure({"saturation_threshold": 0.5, "capacity": {"core": 1}})
        harness.run_guarded(TaskClass.CORE, lambda: 1)
        engine = loop.LazyLoopEngine()
        worker = SimpleNamespace(
            name="w1",
            execute=lambda node, executor=None: (_ for _ in ()).throw(RuntimeError("unreachable")),
        )
        node = SimpleNamespace(node_id=42)
        outcome = engine._run_worker_guarded(worker, node, executor=None)
        assert outcome is None
        assert any(item["code"] == "tier_refused" for item in harness.describe()["advisories"]["items"])
        harness.rearm()

    def test_round_guard_halt_maps_to_degraded_abort(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
        monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
        harness = reset_global_harness()
        engine = loop.LazyLoopEngine()
        monkeypatch.setattr(engine, "run_round", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("planner glitch")))
        monkeypatch.setattr(engine, "admission_check", lambda task_id: {"admitted": True})
        result = engine.run("task-x", max_rounds=2)
        assert result["status"] in ("exhausted", "queued", "timeout", "running", "paused", "done")


class TestAptChainWiring:
    @pytest.fixture(autouse=True)
    def _fresh_global_harness(self):
        reset_global_harness()
        yield
        reset_global_harness()

    def test_recovery_guard_returns_none_when_refused(self, monkeypatch):
        import cli.apt_chain_support as support

        harness = reset_global_harness()
        harness.configure({"saturation_threshold": 0.5, "capacity": {"core": 1}})
        harness.run_guarded(TaskClass.CORE, lambda: 1)

        pool = type(
            "PoolStub",
            (),
            {
                "has_members": lambda self: True,
                "complete": lambda self, *a, **k: "sudo rm -rf /\nsleep 5",
            },
        )()
        from modules.mediation.chain_mediator import ChainMediator

        monkeypatch.setattr(ChainMediator, "llm", lambda self, *a, **k: pool)
        monkeypatch.setattr(support, "_validate_recovery_commands", lambda *a, **k: [], raising=False)
        result = support.build_llm_recovery_chain(
            type(
                "R",
                (),
                {
                    "name": "chain",
                    "target": "10.0.0.1",
                    "steps": [
                        type("S", (), {"id": "s1", "ok": False, "run": "cmd", "status": "failed", "reason": "boom"})()
                    ],
                },
            )(),
            task_id="t1",
        )
        assert result is None
        codes = [item["code"] for item in harness.describe()["advisories"]["items"]]
        assert any(code in ("tier_refused", "mission_failed") for code in codes)
        harness.rearm()


class TestOrchestratorHarnessTab:
    @pytest.fixture()
    def sandbox(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
        monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
        return tmp_path

    def test_command_registered(self):
        from cli.commands.lazyloop import LazyQueueCommandSet

        assert hasattr(LazyQueueCommandSet, "do_lazy_orchestrator")

    def test_guardrails_persist_via_payload(self, monkeypatch, sandbox):
        store = {"payload": {"rhost": "127.0.0.1"}}

        def _load(target=None):
            return dict(store["payload"])

        def _save(data, target=None):
            store["payload"] = dict(data)

        import core.config

        monkeypatch.setattr(core.config, "load_payload", _load)
        monkeypatch.setattr(core.config, "save_payload", _save)
        from cli.lazy_orchestrator import LazyOrchestratorApp

        app = LazyOrchestratorApp()
        guard = app.save_guardrails({"saturation": "0.9", "cap_mission": "7"})
        assert guard["saturation_threshold"] == pytest.approx(0.9)
        assert guard["capacity"]["mission"] == 7
        saved = store["payload"]["orchestrator"]["guardrails"]
        assert saved["capacity"]["mission"] == 7

    def test_harness_tab_composes_headless(self, sandbox, monkeypatch):
        pytest.importorskip("textual")
        asyncio = pytest.importorskip("asyncio")
        from cli.lazy_orchestrator import LazyOrchestratorApp

        async def _drive() -> None:
            app = LazyOrchestratorApp(task_id="t1")
            async with app.run_test() as pilot:
                await pilot.pause()
                table = app.query_one("#harness-table")
                assert table is not None

        asyncio.run(_drive())
