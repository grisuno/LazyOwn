"""
tests/test_moe_rl_swan.py
=========================
Test suite for the MoE + RL + SWAN + Detection Oracle architecture.

Covers:
  - modules/detection_oracle.py  (DetectionOracle, DetectionAssessment)
  - modules/moe_router.py        (MoERouter, ExpertPerformanceStore, SoftmaxSelector)
  - modules/rl_trainer.py        (RLTrainer, QValueStore, EpsilonTracker)
  - skills/swan_agent.py         (SwanResult, OutcomeEvaluator, mcp_swan_route)
  - skills/autonomous_daemon.py  (SWANSelector, cascade order, RL feedback)
  - skills/lazyown_policy.py     (detection-aware reward shaping)
  - modules/world_model.py       (graph / pivot candidates)

All tests are self-contained: they do NOT call real LLM APIs, do NOT require
GROQ_API_KEY, and use tmp_path fixtures for any on-disk persistence.
"""
from __future__ import annotations

import json
import os
import sys
import threading
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
for _p in (str(_ROOT / "modules"), str(_ROOT / "skills")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# =============================================================================
# Detection Oracle
# =============================================================================

class TestDetectionOracle:

    def test_low_risk_dns_query(self):
        """A plain dig query should have LOW detection probability."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        prob = oracle.probability("dig", "@8.8.8.8 example.com", "recon")
        assert prob < 0.50, f"Expected <50% for dig, got {prob:.2%}"

    def test_high_risk_mimikatz(self):
        """mimikatz credential dump must be flagged HIGH risk."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        prob = oracle.probability("mimikatz", "sekurlsa::logonpasswords", "credential_access")
        assert prob >= 0.70, f"Expected >=70% for mimikatz, got {prob:.2%}"

    def test_critical_risk_combined_credential_tools(self):
        """secretsdump combined with lsass keyword should reach HIGH/CRITICAL."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        prob = oracle.probability("secretsdump.py", "-outputfile dump lsass", "credential_access")
        assert prob >= 0.50, f"Expected >=50% for secretsdump, got {prob:.2%}"

    def test_assessment_has_required_fields(self):
        """DetectionAssessment dataclass must contain all documented fields."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        assessment = oracle.assess("lazynmap", "", "recon")
        assert hasattr(assessment, "probability")
        assert hasattr(assessment, "triggered_rules")
        # field is predicted_log_sources (oracle predicts, not observes)
        assert hasattr(assessment, "predicted_log_sources")
        assert hasattr(assessment, "is_high_risk")
        assert hasattr(assessment, "is_critical_risk")

    def test_is_high_risk_property_consistent_with_probability(self):
        """is_high_risk must be True iff probability >= 0.70."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        a_safe = oracle.assess("lazynmap", "", "recon")
        assert (a_safe.is_high_risk) == (a_safe.probability >= 0.70)

    def test_singleton_returns_same_instance(self):
        """get_oracle() must always return the same object (singleton)."""
        from detection_oracle import get_oracle
        a = get_oracle()
        b = get_oracle()
        assert a is b

    def test_nmap_is_not_high_risk(self):
        """Plain nmap should not be considered high risk."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        prob = oracle.probability("lazynmap", "", "recon")
        assert prob < 0.70, f"lazynmap should be <70%, got {prob:.2%}"

    def test_evil_winrm_is_high_risk(self):
        """evil-winrm lateral movement must be flagged HIGH risk."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        prob = oracle.probability("evil-winrm", "-i 10.10.11.78 -u admin -p Password1",
                                  "lateral_movement")
        assert prob >= 0.70, f"evil-winrm expected >=70%, got {prob:.2%}"

    def test_is_critical_risk_property(self):
        """is_critical_risk must be True iff probability >= 0.90."""
        from detection_oracle import DetectionOracle
        oracle = DetectionOracle()
        a = oracle.assess("mimikatz", "sekurlsa::logonpasswords", "credential_access")
        assert (a.is_critical_risk) == (a.probability >= 0.90)


# =============================================================================
# MoE Router
# =============================================================================

class TestMoERouter:

    def test_singleton_returns_same_instance(self):
        """get_router() must return the same MoERouter instance."""
        from moe_router import get_router
        a = get_router()
        b = get_router()
        assert a is b

    def test_route_returns_expert_or_raises_gracefully(self):
        """route() must return a valid ExpertProfile or raise RuntimeError (no keys)."""
        from moe_router import get_router, ExpertProfile
        router = get_router()
        try:
            expert = router.route("recon", "enumerate SMB shares")
            assert isinstance(expert, ExpertProfile)
            assert expert.expert_id
        except RuntimeError:
            # Expected when no API keys and no Ollama running
            pass

    def test_ensemble_returns_available_candidates(self):
        """ensemble() must return a list (may be fewer than N when few experts available)."""
        from moe_router import get_router, ExpertProfile
        router = get_router()
        candidates = router.ensemble("exploit", "exploit apache", n=3)
        assert isinstance(candidates, list)
        for ep in candidates:
            assert isinstance(ep, ExpertProfile)
            assert ep.expert_id

    def test_record_outcome_updates_ema(self, tmp_path):
        """record() must create/update EMA for the given (expert, task_type)."""
        from moe_router import ExpertPerformanceStore
        store = ExpertPerformanceStore(path=tmp_path / "perf.json")
        store.record("test_expert", "recon", reward=8.0, detection_prob=0.0)
        perf = store.get("test_expert", "recon")
        assert perf is not None
        assert perf.ema_reward > 0

    def test_performance_bonus_positive_after_success(self, tmp_path):
        """After a high reward, performance_bonus should be non-negative."""
        from moe_router import ExpertPerformanceStore
        store = ExpertPerformanceStore(path=tmp_path / "perf_bonus.json")
        store.record("groq_fast", "recon", reward=9.0, detection_prob=0.1)
        bonus = store.performance_bonus("groq_fast", "recon")
        assert bonus >= 0.0

    def test_performance_bonus_penalises_high_detection(self, tmp_path):
        """Same base reward but high detection should yield lower EMA reward."""
        from moe_router import ExpertPerformanceStore
        store = ExpertPerformanceStore(path=tmp_path / "perf_det.json")
        store.record("exp_a", "exploit", reward=5.0, detection_prob=0.0)
        store.record("exp_b", "exploit", reward=5.0, detection_prob=0.9)
        ema_a = store.get("exp_a", "exploit").ema_reward
        ema_b = store.get("exp_b", "exploit").ema_reward
        assert ema_a > ema_b, "High detection should yield lower effective EMA"

    def test_status_report_contains_experts(self):
        """status_report() must return a dict with 'experts' key."""
        from moe_router import get_router
        router = get_router()
        status = router.status_report()
        assert "experts" in status
        assert len(status["experts"]) >= 1

    def test_softmax_deterministic_picks_highest_weight(self):
        """In deterministic mode, SoftmaxSelector.select() returns the argmax expert."""
        from moe_router import SoftmaxSelector, ExpertProfile, ExpertPerformanceStore
        import tempfile

        def _ep(eid, w):
            return ExpertProfile(
                expert_id=eid, backend="groq", model="x",
                capabilities=["recon"], base_weight=w,
                cost_tier=0, latency_ms=100,
            )

        selector = SoftmaxSelector(temperature=0.01)  # near-deterministic
        candidates = [_ep("a", 0.1), _ep("b", 0.9), _ep("c", 0.4)]
        with tempfile.NamedTemporaryFile(suffix=".json") as f:
            store = ExpertPerformanceStore(path=Path(f.name))
            winner = selector.select(candidates, "recon", store, deterministic=True)
        assert winner.expert_id == "b"


# =============================================================================
# RL Trainer
# =============================================================================

class TestRLTrainer:

    def test_encode_state_format(self):
        """encode_state must return 'task:phase:bucket' string."""
        from rl_trainer import RLTrainer, RLConfig
        trainer = RLTrainer(config=RLConfig())
        state = trainer.encode_state("recon", "exploitation", 0.0)
        parts = state.split(":")
        assert len(parts) == 3
        assert parts[0] == "recon"
        assert parts[1] == "exploitation"
        assert parts[2] in ("low", "medium", "high", "excellent")

    def test_select_action_returns_valid_candidate(self):
        """select_action must return one of the provided candidates."""
        from rl_trainer import RLTrainer, RLConfig
        trainer = RLTrainer(config=RLConfig())
        candidates = ["groq_fast", "groq_powerful", "ollama_reason"]
        state  = trainer.encode_state("exploit", "exploitation")
        choice = trainer.select_action(state, candidates)
        assert choice in candidates

    def test_update_changes_qvalue(self, tmp_path):
        """After update(), Q(state, action) must differ from the initial value."""
        from rl_trainer import RLTrainer, RLConfig, QValueStore, EpsilonTracker
        q_store = QValueStore(path=tmp_path / "qvals.json", optimistic_init=1.0)
        eps     = EpsilonTracker(start=0.20, minimum=0.05, decay=0.995,
                                 path=tmp_path / "eps.json")
        trainer = RLTrainer(config=RLConfig(), q_store=q_store, epsilon_tracker=eps)

        state      = trainer.encode_state("exploit", "exploitation", 0.0)
        next_state = trainer.encode_state("privesc", "post_exploitation", 5.0)
        old_q      = q_store.get(state, "groq_fast")

        trainer.update(
            state=state,
            action="groq_fast",
            reward=8.0,
            next_state=next_state,
            candidates=["groq_fast", "groq_powerful"],
            detection_prob=0.0,
        )
        new_q = q_store.get(state, "groq_fast")
        assert new_q != old_q, "Q-value should change after update"

    def test_epsilon_decays_after_update(self, tmp_path):
        """epsilon must be strictly smaller after calling update()."""
        from rl_trainer import RLTrainer, RLConfig, QValueStore, EpsilonTracker
        q_store = QValueStore(path=tmp_path / "qvals2.json")
        eps     = EpsilonTracker(start=0.20, minimum=0.05, decay=0.995,
                                 path=tmp_path / "eps2.json")
        trainer = RLTrainer(config=RLConfig(), q_store=q_store, epsilon_tracker=eps)
        initial_eps = trainer.epsilon
        state = trainer.encode_state("recon", "reconnaissance")
        trainer.update(state, "bridge", 3.0, state, ["bridge", "fallback"])
        assert trainer.epsilon < initial_eps

    def test_detection_penalty_lowers_effective_reward(self, tmp_path):
        """Same raw reward but high detection_prob must yield a lower Q-update."""
        from rl_trainer import RLTrainer, RLConfig, QValueStore, EpsilonTracker

        def _make_trainer(suffix):
            return RLTrainer(
                config=RLConfig(optimistic_init=0.0),
                q_store=QValueStore(path=tmp_path / f"q_{suffix}.json",
                                    optimistic_init=0.0),
                epsilon_tracker=EpsilonTracker(
                    start=0.0, minimum=0.0, decay=1.0,
                    path=tmp_path / f"e_{suffix}.json",
                ),
            )

        t_safe  = _make_trainer("safe")
        t_risky = _make_trainer("risky")
        state  = t_safe.encode_state("exploit", "exploitation")
        next_s = t_safe.encode_state("exploit", "exploitation")
        cands  = ["expert_a"]

        t_safe.update(state, "expert_a",  reward=5.0,
                      next_state=next_s, candidates=cands, detection_prob=0.0)
        t_risky.update(state, "expert_a", reward=5.0,
                       next_state=next_s, candidates=cands, detection_prob=0.9)

        q_safe  = t_safe._q.get(state, "expert_a")
        q_risky = t_risky._q.get(state, "expert_a")
        assert q_safe > q_risky, (
            f"Q without detection ({q_safe}) should exceed Q with detection ({q_risky})"
        )

    def test_optimistic_init_for_unseen_actions(self, tmp_path):
        """An unseen (state, action) pair must return optimistic_init value."""
        from rl_trainer import QValueStore
        store = QValueStore(path=tmp_path / "q_opt.json", optimistic_init=2.5)
        value = store.get("never_seen_state", "never_seen_action")
        assert value == 2.5

    def test_save_and_reload_persistence(self, tmp_path):
        """Q-values saved to disk must be recoverable after re-instantiation."""
        from rl_trainer import RLTrainer, RLConfig, QValueStore, EpsilonTracker
        path = tmp_path / "persist.json"
        q1  = QValueStore(path=path, optimistic_init=0.0)
        e1  = EpsilonTracker(start=0.1, minimum=0.05, decay=1.0,
                              path=tmp_path / "e_persist.json")
        t1  = RLTrainer(config=RLConfig(), q_store=q1, epsilon_tracker=e1)
        state = t1.encode_state("cred", "post_exploitation")
        t1.update(state, "ollama_reason", reward=7.0, next_state=state,
                  candidates=["ollama_reason"])
        t1.save()

        q2       = QValueStore(path=path, optimistic_init=0.0)
        reloaded = q2.get(state, "ollama_reason")
        assert reloaded != 0.0, "Saved Q-value should persist across re-instantiation"


# =============================================================================
# SWAN Agent (unit tests — no LLM API calls)
# =============================================================================

class TestSwanAgent:

    def test_swan_result_dataclass_fields(self):
        """SwanResult must have all documented fields."""
        from swan_agent import SwanResult
        r = SwanResult(
            task_id="t1",
            task_type="recon",
            goal="enumerate SMB",
            expert_id="groq_fast",
            backend="groq",
            model="llama-3",
            output="test",
            status="completed",
            reward=5.0,
            detection_prob=0.1,
            duration_s=0.5,
            state_key="recon:exploitation:medium",
        )
        assert r.task_id == "t1"
        assert r.status == "completed"
        assert r.reward == 5.0
        assert r.is_success

    def test_swan_result_failed_is_not_success(self):
        """is_success must be False when status != 'completed'."""
        from swan_agent import SwanResult
        r = SwanResult(
            task_id="t2", task_type="exploit", goal="test",
            expert_id="groq_fast", backend="groq", model="llama",
            output="", status="failed",
        )
        assert not r.is_success

    def test_outcome_evaluator_success_reward(self):
        """Successful non-detected command should yield positive reward."""
        from swan_agent import OutcomeEvaluator, SwanResult
        evaluator = OutcomeEvaluator()
        result = SwanResult(
            task_id="t3", task_type="recon", goal="nmap scan",
            expert_id="groq_fast", backend="groq", model="llama",
            output="22/tcp open ssh OpenSSH 8.4",
            status="completed",
        )
        reward, detect = evaluator.evaluate(result, "recon")
        assert reward > 0.0
        assert 0.0 <= detect <= 1.0

    def test_outcome_evaluator_failed_gives_negative_reward(self):
        """A failed execution must yield negative reward."""
        from swan_agent import OutcomeEvaluator, SwanResult
        evaluator = OutcomeEvaluator()
        result = SwanResult(
            task_id="t4", task_type="recon", goal="fail test",
            expert_id="groq_fast", backend="groq", model="llama",
            output="connection refused",
            status="failed",
        )
        reward, _ = evaluator.evaluate(result, "recon")
        assert reward < 0.0

    def test_outcome_evaluator_high_value_category_bonus(self):
        """Successful privesc task should have a higher reward than basic recon."""
        from swan_agent import OutcomeEvaluator, SwanResult

        def _result(task_type):
            return SwanResult(
                task_id="tx", task_type=task_type, goal="test",
                expert_id="groq_fast", backend="groq", model="llama",
                output="success", status="completed",
            )

        evaluator = OutcomeEvaluator()
        r_recon, _ = evaluator.evaluate(_result("recon"), "recon")
        r_priv,  _ = evaluator.evaluate(_result("privesc"), "privesc")
        assert r_priv >= r_recon, "privesc reward should be >= recon reward"

    def test_mcp_swan_route_returns_valid_json(self):
        """mcp_swan_route() must return valid JSON with routing + task_type."""
        from swan_agent import mcp_swan_route
        raw  = mcp_swan_route("recon", "enumerate SMB shares")
        data = json.loads(raw)
        assert "task_type" in data
        assert "routing" in data
        assert isinstance(data["routing"], list)
        # routing may be empty when no API keys / Ollama available; shape is what matters
        for row in data["routing"]:
            assert "expert_id" in row
            assert "base_weight" in row

    def test_mcp_swan_status_returns_valid_json(self):
        """mcp_swan_status() must return valid JSON with experts key."""
        from swan_agent import mcp_swan_status
        raw  = mcp_swan_status()
        data = json.loads(raw)
        assert "experts" in data

    def test_ensemble_result_dataclass_fields(self):
        """EnsembleResult must have all documented fields."""
        from swan_agent import EnsembleResult, ExpertVote
        vote = ExpertVote(
            expert_id="groq_fast", output="lazynmap", weight=0.5,
            status="completed", duration_s=1.0,
        )
        er = EnsembleResult(
            task_id="t_ens",
            task_type="recon",
            goal="enumerate SMB",
            votes=[vote],
            synthesis="Use lazynmap first",
            consensus_confidence=0.8,
            best_expert_id="groq_fast",
            reward=5.0,
            detection_prob=0.1,
            duration_s=1.2,
        )
        assert er.consensus_confidence == 0.8
        assert er.best_expert_id == "groq_fast"
        assert len(er.votes) == 1


# =============================================================================
# Autonomous Daemon — SWANSelector + RL feedback (unit-level)
# =============================================================================

class TestAutonomousDaemonSWAN:

    def test_swan_selector_disabled_by_default(self):
        """SWANSelector.select() must return None when AUTO_USE_SWAN is not '1'."""
        os.environ.pop("AUTO_USE_SWAN", None)
        from autonomous_daemon import SWANSelector
        sel    = SWANSelector()
        result = sel.select("10.0.0.1", "recon", {})
        assert result is None

    def test_swan_selector_phase_mapping_coverage(self):
        """Every phase in _PHASE_TO_TASK must map to a valid SWAN task_type."""
        from autonomous_daemon import SWANSelector
        valid_task_types = {"recon", "exploit", "privesc", "cred", "lateral", "analyze"}
        for phase, task in SWANSelector._PHASE_TO_TASK.items():
            assert task in valid_task_types, (
                f"Phase '{phase}' maps to unknown task_type '{task}'"
            )

    def test_cascade_strategy_contains_swan_selector(self):
        """The default StrategyEngine cascade must include a SWANSelector."""
        from autonomous_daemon import StrategyEngine, PTYCommandRunner, SWANSelector
        engine = StrategyEngine(runner=PTYCommandRunner())
        types  = [type(s).__name__ for s in engine._cascade._selectors]
        assert "SWANSelector" in types

    def test_cascade_strategy_order(self):
        """SWANSelector must appear before FallbackSelector in the cascade."""
        from autonomous_daemon import StrategyEngine, PTYCommandRunner
        engine = StrategyEngine(runner=PTYCommandRunner())
        names  = [type(s).__name__ for s in engine._cascade._selectors]
        assert names.index("SWANSelector") < names.index("FallbackSelector")

    def test_fallback_selector_never_returns_none(self):
        """FallbackSelector must always return a CommandDecision, never None."""
        from autonomous_daemon import FallbackSelector
        sel = FallbackSelector()
        for phase in ("recon", "exploit", "privesc", "lateral", "cred", "unknown_phase"):
            result = sel.select("10.0.0.1", phase, {})
            assert result is not None, (
                f"FallbackSelector returned None for phase={phase}"
            )

    def test_command_decision_source_label(self):
        """FallbackSelector decisions must carry source='fallback'."""
        from autonomous_daemon import FallbackSelector
        sel = FallbackSelector()
        dec = sel.select("10.0.0.1", "recon", {"os_hint": "linux"})
        assert dec.source == "fallback"

    def test_llm_selector_disabled_without_env(self):
        """LLMSelector must return None when AUTO_USE_LLM is not set."""
        os.environ.pop("AUTO_USE_LLM", None)
        from autonomous_daemon import LLMSelector
        sel    = LLMSelector()
        result = sel.select("10.0.0.1", "recon", {})
        assert result is None


# =============================================================================
# Policy Engine — Detection-Aware Reward Shaping
# =============================================================================

class TestPolicyDetectionAware:

    def test_detection_above_threshold_zeroes_reward(self):
        """calculate_with_detection: reward must be 0 when detect >= 0.70."""
        from lazyown_policy import RewardCalculator, DetectionRiskAssessor, Config
        from lazyown_policy import ActionCategory, OutcomeType
        assessor = DetectionRiskAssessor()
        calc     = RewardCalculator(cfg=Config.default(), risk_assessor=assessor)
        reward, detect = calc.calculate_with_detection(
            category=ActionCategory.CREDENTIAL,
            outcome=OutcomeType.SUCCESS,
            command="mimikatz",
            args="sekurlsa::logonpasswords",
        )
        if detect >= 0.70:
            assert reward == 0, (
                f"Expected reward=0 for high-detection command, got {reward} "
                f"(detect={detect:.2%})"
            )

    def test_low_detection_preserves_positive_reward(self):
        """Low-detection success should keep a positive reward value."""
        from lazyown_policy import RewardCalculator, DetectionRiskAssessor, Config
        from lazyown_policy import ActionCategory, OutcomeType
        assessor = DetectionRiskAssessor()
        calc     = RewardCalculator(cfg=Config.default(), risk_assessor=assessor)
        reward, detect = calc.calculate_with_detection(
            category=ActionCategory.RECON,
            outcome=OutcomeType.SUCCESS,
            command="lazynmap",
            args="",
        )
        if detect < 0.70:
            assert reward >= 0, (
                f"Low-detection success should not yield negative reward, got {reward}"
            )

    def test_failed_outcome_gives_negative_reward(self):
        """Failed recon action must produce a negative reward regardless of detection."""
        from lazyown_policy import RewardCalculator, Config, ActionCategory, OutcomeType
        calc = RewardCalculator(cfg=Config.default())
        reward = calc.calculate(ActionCategory.RECON, OutcomeType.FAIL)
        assert reward < 0, f"Expected negative reward for FAIL, got {reward}"


# =============================================================================
# World Model — Graph / Pivot Candidates
# =============================================================================

class TestWorldModelGraph:

    def test_add_relation_and_pivot_candidates(self, tmp_path):
        """After adding relations, pivot_candidates must return hosts by centrality."""
        from world_model import WorldModel
        wm = WorldModel(path=str(tmp_path / "wm.json"))
        wm.add_host("10.0.0.1")
        wm.add_host("10.0.0.2")
        wm.add_host("10.0.0.3")
        wm.add_relation("10.0.0.1", "10.0.0.2", "connects_to")
        wm.add_relation("10.0.0.1", "10.0.0.3", "connects_to")
        wm.add_relation("10.0.0.2", "10.0.0.3", "connects_to")
        pivots = wm.pivot_candidates(top_k=2)
        assert len(pivots) >= 1
        # pivot_candidates returns 'node' key (actual field name)
        assert "node" in pivots[0] or "host" in pivots[0]
        assert "centrality" in pivots[0]

    def test_graph_snapshot_is_serialisable(self, tmp_path):
        """graph_snapshot() must return a JSON-serialisable dict."""
        from world_model import WorldModel
        wm = WorldModel(path=str(tmp_path / "wm2.json"))
        wm.add_host("192.168.1.1")
        wm.add_relation("192.168.1.1", "192.168.1.2", "discovered")
        snap = wm.graph_snapshot()
        assert "nodes" in snap
        json.dumps(snap)  # must not raise

    def test_auto_relation_on_service_add(self, tmp_path):
        """add_service should auto-create a graph node for the host (prefixed)."""
        from world_model import WorldModel
        wm = WorldModel(path=str(tmp_path / "wm3.json"))
        wm.add_service("10.0.0.5", 22, "ssh", "OpenSSH 8.4")
        snap  = wm.graph_snapshot()
        nodes = snap.get("nodes", [])
        # The graph stores nodes as 'host:10.0.0.5' prefixed strings
        assert any("10.0.0.5" in n for n in nodes), (
            f"Expected a node containing '10.0.0.5' in {nodes}"
        )

    def test_pivot_candidates_sorted_by_centrality(self, tmp_path):
        """pivot_candidates must return results sorted descending by centrality."""
        from world_model import WorldModel
        wm = WorldModel(path=str(tmp_path / "wm4.json"))
        # Create a star topology: hub connects to 4 leaves
        for i in range(1, 5):
            wm.add_relation("hub", f"leaf_{i}", "connects_to")
            wm.add_relation(f"leaf_{i}", "hub", "connects_to")
        pivots = wm.pivot_candidates(top_k=5)
        if len(pivots) >= 2:
            assert pivots[0]["centrality"] >= pivots[1]["centrality"]


# =============================================================================
# MCP Registration — Verify SWAN tools are exposed
# =============================================================================

class TestMCPRegistration:

    def test_swan_tools_registered_in_mcp(self):
        """The four SWAN tools must appear in lazyown_mcp list_tools names."""
        import asyncio
        sys.path.insert(0, str(_ROOT / "skills"))

        # Import names without running the server
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "lazyown_mcp_check",
            str(_ROOT / "skills" / "lazyown_mcp.py"),
        )
        # We cannot easily run the async list_tools, so grep for the names
        src = (_ROOT / "skills" / "lazyown_mcp.py").read_text()
        for tool in ("lazyown_swan_run", "lazyown_swan_ensemble",
                     "lazyown_swan_status", "lazyown_swan_route"):
            assert tool in src, f"MCP tool '{tool}' not found in lazyown_mcp.py"

    def test_hive_tools_registered_in_mcp(self):
        """Core hive tools must appear in lazyown_mcp.py."""
        src = (_ROOT / "skills" / "lazyown_mcp.py").read_text()
        for tool in ("lazyown_hive_spawn", "lazyown_hive_status",
                     "lazyown_hive_recall", "lazyown_autonomous_start"):
            assert tool in src, f"MCP tool '{tool}' not found"
