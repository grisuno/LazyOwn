"""Detection-oracle dampening contract: benign alternatives quiet the score.

Every scenario states Given, When, Then. Sigma matching stays
deterministic; a declared benign twin lowers the derived probability
and explains itself in the recommendation without erasing the evidence.
"""

from __future__ import annotations

from modules.detection_oracle import DetectionOracle, _benign_alternative_matches


def test_benign_alternative_overlap_matches():
    """Given a declared twin sharing vocabulary, When matching, Then it counts as benign."""
    assert _benign_alternative_matches("mimikatz sekurlsa", "", ["red-team authorized"] ) is False
    assert (
        _benign_alternative_matches(
            "python loader_mimikatz.py",
            "--mode offline",
            ["mimikatz lab exercise"],
        )
        is True
    )


def test_no_overlap_never_dampens():
    """Given unrelated vocabulary, When matching, Then nothing counts as benign."""
    assert _benign_alternative_matches("mimikatz", "", ["tape backup device"]) is False
    assert _benign_alternative_matches("mimikatz", "", []) is False


def test_dampened_probability_keeps_sigma_evidence():
    """Given a matching twin, When assessing, Then probability drops and evidence stays."""
    oracle = DetectionOracle()
    base = oracle.assess("mimikatz", "sekurlsa::logonpasswords", "credential")
    with_twin = oracle.assess(
        "mimikatz",
        "sekurlsa::logonpasswords",
        "credential",
        benign_alternatives=["mimikatz lab exercise by authorized red team"],
    )
    assert with_twin.probability < base.probability
    assert with_twin.recommendation.startswith("benign alternative declared")
    assert with_twin.triggered_rules == base.triggered_rules


def test_probability_kwargs_route_through_assess():
    """Given alternatives at the probability level, When scoring, Then the dampening applies."""
    oracle = DetectionOracle()
    plain = oracle.probability("mimikatz", "sekurlsa::logonpasswords", "credential")
    dampened = oracle.probability(
        "mimikatz",
        "sekurlsa::logonpasswords",
        "credential",
        benign_alternatives=["mimikatz lab exercise by authorized red team"],
    )
    assert dampened < plain


def test_abs_signature_stays_compatible():
    """Given the abstract contract, When old callers use the legacy form, Then both signatures work."""
    from modules.detection_oracle import IDetectionOracle

    oracle = DetectionOracle()
    assert isinstance(oracle, IDetectionOracle)
    legacy = oracle.assess("defender scan", "run", "execution")
    assert 0.0 <= legacy.probability <= 1.0
