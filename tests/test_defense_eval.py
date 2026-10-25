"""Defense rule replay: target/control datasets, verdicts and metric counts."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules.defense_eval import (  # noqa: E402
    RuleEvaluationError,
    evaluate_rule,
    metrics,
    parse_rule,
)

RULE = '{"version": 1, "all": [{"field": "http.path", "op": "contains", "value": "/admin"}, {"field": "http.status", "op": "eq", "value": 200}]}'

TARGET = '\n{"http": {"path": "/admin/panel", "status": 200}}\n'
TARGET_PARTIAL = TARGET + '{"http": {"path": "/admin/panel", "status": 500}}\n'
CONTROL = '\n{"http": {"path": "/index", "status": 200}}\n{"http": {"path": "/about", "status": 200}}\n'


def test_parse_rule_accepts_and_rejects() -> None:
    """Valid rules parse; malformed ones raise."""
    assert len(parse_rule(RULE)) == 2
    with pytest.raises(RuleEvaluationError):
        parse_rule('{"version": 2, "all": [{"field": "a", "op": "eq", "value": 1}]}')
    with pytest.raises(RuleEvaluationError):
        parse_rule('{"version": 1, "all": [{"field": "a", "op": "like", "value": "x"}]}')
    with pytest.raises(RuleEvaluationError):
        parse_rule('{"version": 1, "all": []}')
    with pytest.raises(RuleEvaluationError):
        parse_rule('{"version": 1, "all": [{"field": "a", "op": "eq"}]}')
    with pytest.raises(RuleEvaluationError):
        parse_rule('{"version": 1, "all": [{"field": "a", "op": "eq", "value": None}]}')


def test_rule_pass_requires_control_clean() -> None:
    """Pass demands every target match and no control match."""
    result = evaluate_rule(RULE, TARGET, CONTROL)
    assert result.verdict == "pass"
    assert metrics(result) == {"tp": 1, "fn": 0, "fp": 0, "tn": 2}
    partial = evaluate_rule(RULE, TARGET_PARTIAL, CONTROL)
    assert partial.verdict == "fail"
    assert metrics(partial) == {"tp": 1, "fn": 1, "fp": 0, "tn": 2}
    assert partial.target.matched == 1
    assert partial.target.missed == 1


def test_control_match_is_fail() -> None:
    """Any control match flags a false positive and fails the rule."""
    control = '{"http": {"path": "/admin/help", "status": 200}}'
    result = evaluate_rule(RULE, TARGET, control)
    assert result.verdict == "fail"
    assert "control events matched the rule" in " ".join(result.reasons)


def test_missing_field_is_inconclusive() -> None:
    """Absent referenced fields downgrade to inconclusive."""
    logs = '{"other": 1}\n'
    result = evaluate_rule(RULE, logs, logs)
    assert result.verdict == "inconclusive"
    assert result.target.inconclusive == 1


def test_empty_datasets_are_inconclusive() -> None:
    """Empty target or control sets cannot conclude."""
    result = evaluate_rule(RULE, "", "")
    assert result.verdict == "inconclusive"
    result = evaluate_rule(RULE, TARGET, "")
    assert result.verdict == "inconclusive"


def test_number_canonicalization() -> None:
    """1, 1.0 and 10e-1 compare equal without float drift."""
    rule = '{"version": 1, "all": [{"field": "size", "op": "eq", "value": 1.0}]}'
    logs = '{"size": 10e-1}\n{"size": 1}\n'
    result = evaluate_rule(rule, logs, "")
    assert result.verdict == "inconclusive"
    assert result.target.matched == 2


def test_neq_operator() -> None:
    """neq inverts the equality comparison."""
    rule = '{"version": 1, "all": [{"field": "status", "op": "neq", "value": 404}]}'
    logs = '{"status": 200}\n'
    control = '{"status": 404}\n'
    result = evaluate_rule(rule, logs, control)
    assert result.target.matched == 1
    assert result.control.matched == 0
    assert result.verdict == "pass"


def test_json_array_datasets() -> None:
    """JSON arrays are accepted alongside JSON lines."""
    result = evaluate_rule(RULE, '[{"http": {"path": "/admin", "status": 200}}]', '[{"http": {"path": "/x", "status": 404}}]')
    assert result.verdict == "pass"


def test_malformed_logs_raise() -> None:
    """Bad JSON surfaces as RuleEvaluationError with the line number."""
    with pytest.raises(RuleEvaluationError):
        evaluate_rule(RULE, "{broken", "")


def test_oversized_rule_rejected() -> None:
    """Rules above the byte cap are rejected before parsing."""
    with pytest.raises(RuleEvaluationError):
        parse_rule('{"version": 1, "all": [{"field": "' + "a" * 70000 + '", "op": "eq", "value": 1}]}')
