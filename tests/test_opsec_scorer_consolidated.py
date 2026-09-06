"""Consolidated OPSEC scorer contract tests (SDD/TDD/BDD).

Covers the single-contract ``modules.opsec_scorer`` after merging the former
``opsec_scorer_v2`` module. Verifies:

- The shared noise-to-risk mapping is the single source of truth for both
  :class:`OpsecScorer` (advisory, string label) and :class:`OpsecScorerV2`
  (gated, enum label).
- V2 gating behaviour (allow / warn / confirm / block) and trend tracking.
- Backward-compatible V1 advisory scoring.
"""

from __future__ import annotations

from modules.opsec_scorer import (
    COMMAND_RISK_PROFILES,
    GateAction,
    OpsecContext,
    OpsecScore,
    OpsecScorer,
    OpsecScorerV2,
    RiskLevel,
    _risk_bucket,
    _risk_label,
    _risk_level,
)


class TestSharedRiskMapping:
    def test_risk_buckets_respect_thresholds(self):
        assert _risk_bucket(0) == 0
        assert _risk_bucket(2) == 0
        assert _risk_bucket(3) == 1
        assert _risk_bucket(4) == 1
        assert _risk_bucket(5) == 2
        assert _risk_bucket(7) == 2
        assert _risk_bucket(8) == 3
        assert _risk_bucket(10) == 3

    def test_risk_label_matches_bucket(self):
        assert _risk_label(1) == "low"
        assert _risk_label(3) == "medium"
        assert _risk_label(6) == "high"
        assert _risk_label(9) == "critical"

    def test_risk_level_matches_bucket(self):
        assert _risk_level(1) is RiskLevel.LOW
        assert _risk_level(3) is RiskLevel.MEDIUM
        assert _risk_level(6) is RiskLevel.HIGH
        assert _risk_level(9) is RiskLevel.CRITICAL

    def test_string_and_enum_labels_are_consistent(self):
        for noise in range(11):
            label = OpsecScorer._noise_to_risk(noise)
            level = OpsecScorerV2._noise_to_risk(noise)
            assert label == level.name.lower(), f"mismatch at noise {noise}"


class TestRiskLevelAndGate:
    def test_enum_values(self):
        assert RiskLevel.LOW == 1
        assert RiskLevel.MEDIUM == 2
        assert RiskLevel.HIGH == 3
        assert RiskLevel.CRITICAL == 4
        assert GateAction.ALLOW == 0
        assert GateAction.WARN == 1
        assert GateAction.CONFIRM == 2
        assert GateAction.BLOCK == 3

    def test_gate_mapping(self):
        scorer = OpsecScorerV2()
        assert scorer._risk_to_gate(RiskLevel.LOW) is GateAction.ALLOW
        assert scorer._risk_to_gate(RiskLevel.MEDIUM) is GateAction.ALLOW
        assert scorer._risk_to_gate(RiskLevel.HIGH) is GateAction.WARN
        assert scorer._risk_to_gate(RiskLevel.CRITICAL) is GateAction.CONFIRM


class TestOpsecScorerV2:
    def test_assess_returns_gated_score(self):
        scorer = OpsecScorerV2()
        score = scorer.assess("ping")
        assert score.command == "ping"
        assert isinstance(score.risk_level, RiskLevel)
        assert isinstance(score.gate_action, GateAction)
        assert score.risk_label == score.risk_level.name

    def test_mimikatz_is_high_critical(self):
        scorer = OpsecScorerV2(context=OpsecContext(
            killchain_phase="credential_access",
            target_environment="enterprise",
            edr_detected=True,
            siem_detected=True,
        ))
        score = scorer.assess("mimikatz")
        assert score.gate_action in (GateAction.WARN, GateAction.CONFIRM, GateAction.BLOCK)

    def test_ping_is_allow(self):
        scorer = OpsecScorerV2()
        allowed, score = scorer.should_allow("ping")
        assert allowed is True
        assert score.gate_action is GateAction.ALLOW

    def test_should_allow_returns_tuple(self):
        scorer = OpsecScorerV2()
        allowed, score = scorer.should_allow("nmap")
        assert isinstance(allowed, bool)
        assert score.command == "nmap"

    def test_trend_insufficient_data(self):
        scorer = OpsecScorerV2()
        assert scorer.get_trend() == {"trend": "insufficient_data", "sample_count": 0}

    def test_trend_after_scoring(self):
        scorer = OpsecScorerV2()
        for _ in range(4):
            scorer.assess("ping")
        trend = scorer.get_trend()
        assert trend["trend"] in ("stable", "improving", "escalating")
        assert trend["total_operations"] == 4

    def test_mitigations_generated(self):
        scorer = OpsecScorerV2(context=OpsecContext(edr_detected=True))
        score = scorer.assess("mimikatz")
        assert len(score.mitigations) > 0

    def test_alternatives_for_mimikatz(self):
        scorer = OpsecScorerV2()
        score = scorer.assess("mimikatz")
        assert len(score.alternative_commands) == 3

    def test_unknown_command_uses_default_profile(self):
        scorer = OpsecScorerV2()
        score = scorer.assess("totally_unknown_cmd")
        assert score.command == "totally_unknown_cmd"
        assert 0 <= score.noise_score <= 10


class TestBackwardCompatibility:
    def test_v1_score_returns_string_risk(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        score = scorer.score("secretsdump", rhost="10.10.11.5")
        assert isinstance(score, OpsecScore)
        assert score.risk_level in ("low", "medium", "high", "critical")

    def test_opsec_context_defaults(self):
        context = OpsecContext()
        assert context.killchain_phase == "recon"
        assert context.target_environment == "unknown"
        assert context.edr_detected is False
        assert context.siem_detected is False

    def test_risk_profiles_shared_table_intact(self):
        assert COMMAND_RISK_PROFILES["mimikatz"]["base_noise"] == 10
        assert COMMAND_RISK_PROFILES["ping"]["base_noise"] == 1
