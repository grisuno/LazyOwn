"""Closed-loop tuning: baseline vs candidate comparison and suggestions."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules.closedloop import (  # noqa: E402
    VERDICT_EQUIVALENT,
    VERDICT_IMPROVED,
    VERDICT_INCONCLUSIVE,
    VERDICT_REGRESSED,
    compare_rules,
    suggest_tuning,
)

TARGET = '\n{"http": {"path": "/admin/panel", "status": 200}}\n'
CONTROL = '\n{"http": {"path": "/help", "status": 200}}\n'

BASELINE = '{"version": 1, "all": [{"field": "http.path", "op": "contains", "value": "/admin"}, {"field": "http.status", "op": "eq", "value": 200}]}'

CANDIDATE = '{"version": 1, "all": [{"field": "http.path", "op": "contains", "value": "p"}]}'


def test_candidate_with_false_positive_regresses() -> None:
    """A looser candidate matching control traffic is a regression."""
    comparison = compare_rules(BASELINE, CANDIDATE, TARGET, CONTROL)
    assert comparison.verdict == VERDICT_REGRESSED
    assert comparison.candidate.fp == 1
    assert any("narrow" in suggestion for suggestion in comparison.suggestions)


def test_both_pass_is_equivalent() -> None:
    """Two passing rules compare as equivalent with a preference note."""
    comparison = compare_rules(BASELINE, BASELINE, TARGET, CONTROL)
    assert comparison.verdict == VERDICT_EQUIVALENT
    assert "no tuning needed" in comparison.suggestions[-1]


def test_both_fail_is_equivalent_fail() -> None:
    """Two failing rules compare as equivalent with tuning suggestions."""
    comparison = compare_rules(BASELINE, CANDIDATE, CONTROL, TARGET)
    assert comparison.verdict == VERDICT_EQUIVALENT
    assert comparison.suggestions


def test_inconclusive_datasets() -> None:
    """Missing fields in the datasets mark the comparison inconclusive."""
    comparison = compare_rules(BASELINE, BASELINE, '{"other": 1}\n', '{"other": 1}\n')
    assert comparison.verdict == VERDICT_INCONCLUSIVE
    assert comparison.suggestions


def test_candidate_fixes_baseline_failure() -> None:
    """A candidate passing where the baseline fails is an improvement."""
    baseline = '{"version": 1, "all": [{"field": "http.path", "op": "contains", "value": "/missing"}]}'
    comparison = compare_rules(baseline, BASELINE, TARGET, CONTROL)
    assert comparison.verdict == VERDICT_IMPROVED
    assert "keep the candidate" in comparison.suggestions[-1]


def test_suggest_tuning_lists_missing_fields() -> None:
    """Suggestions surface the exact fields that made replay inconclusive."""
    result = compare_rules(BASELINE, BASELINE, '{"other": 1}\n', '{"other": 1}\n').candidate_result
    suggestions = suggest_tuning(result)
    assert any("http.path" in suggestion or "http.status" in suggestion for suggestion in suggestions)
