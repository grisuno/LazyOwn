"""Tests for modules/opsec_scorer.py"""

from __future__ import annotations

from modules.opsec_scorer import (
    COMMAND_NOISE,
    MITIGATIONS,
    PHASE_NOISE,
    OpsecScore,
    OpsecScorer,
    score_command,
)


class TestOpsecScorer:
    def test_score_high_noise_command(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        score = scorer.score("secretsdump", rhost="10.10.11.5")
        assert score.risk_level == "critical"
        assert score.noise_score >= 7
        assert score.command == "secretsdump"

    def test_score_low_noise_command(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        score = scorer.score("ping", rhost="10.10.11.5")
        assert score.risk_level in ("low", "medium")
        assert score.noise_score <= 4

    def test_score_unknown_command(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        score = scorer.score("totally_fake_command_xyz")
        assert score.command == "totally_fake_command_xyz"
        assert 0 <= score.noise_score <= 10

    def test_score_with_evasion(self):
        scorer = OpsecScorer({"sleep": "30", "rhost": "10.10.11.5"})
        assert scorer.evasion_active is True
        score = scorer.score("mimikatz", rhost="10.10.11.5")
        assert score.noise_score <= 10

    def test_score_batch(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        scores = scorer.score_batch(["ping", "lazynmap", "secretsdump"])
        assert len(scores) == 3
        assert scores["ping"].noise_score < scores["secretsdump"].noise_score

    def test_score_to_dict(self):
        score = OpsecScore(
            command="ping",
            noise_score=1,
            detection_risk="minimal",
            risk_level="low",
            confidence=0.85,
            detectable_by=["none"],
            mitigation=["standard OPSEC: monitor execution, have cleanup ready"],
            recommendation="Safe to proceed.",
        )
        d = score.to_dict()
        assert d["command"] == "ping"
        assert d["noise_score"] == 1
        assert d["risk_level"] == "low"

    def test_confidence_is_float(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        score = scorer.score("evil")
        assert isinstance(score.confidence, float)
        assert 0 <= score.confidence <= 1

    def test_mitigations_returned(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        score = scorer.score("secretsdump")
        assert len(score.mitigation) > 0

    def test_convenience_function(self):
        score = score_command("ping", {"rhost": "10.10.11.5"})
        assert isinstance(score, OpsecScore)
        assert score.command == "ping"

    def test_all_known_commands_have_mitigations(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        for cmd in COMMAND_NOISE:
            score = scorer.score(cmd)
            assert score.mitigation, f"{cmd} should have mitigations"
            assert score.detection_risk
            assert score.risk_level in ("low", "medium", "high", "critical")

    def test_suggest_mitigations(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        mitigations = scorer.suggest_mitigations("secretsdump")
        assert len(mitigations) > 0

    def test_target_sensitivity_dc(self):
        scorer = OpsecScorer({"rhost": "10.10.11.5"})
        score_dc = scorer.score("secretsdump", rhost="10.0.0.1")
        score_ws = scorer.score("secretsdump", rhost="10.0.0.2")
        assert isinstance(score_dc.noise_score, int)
        assert isinstance(score_ws.noise_score, int)
