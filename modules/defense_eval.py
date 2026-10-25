"""Detection rule replay over recorded attack and control logs.

Pure log replay: a deliberately small rule language (JSON, ``eq`` /
``neq`` / ``contains`` conditions) is evaluated against two datasets.
The ``target`` dataset holds attack traffic; the ``control`` dataset
holds benign traffic. A rule only passes when every target event
matches, no control event matches, and no referenced field was absent
or of an incompatible type. Nothing here touches the network, executes
commands or deploys rules to a SIEM.

Adapted from the ARTEX ``defenseeval`` engine (AGPL-3.0), which is in
turn inspired by the original ARTEX project.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any

ENGINE_VERSION = "lazyown-defense-eval/v1"

MAX_LOG_BYTES = 1 << 20
MAX_EVENTS = 2000
MAX_RULE_BYTES = 64 << 10
MAX_CONDITIONS = 16
MAX_FIELD_LENGTH = 128
MAX_RULE_VALUE_BYTES = 4096
MAX_EVENT_BYTES = 128 << 10

VERDICT_PASS = "pass"
VERDICT_FAIL = "fail"
VERDICT_INCONCLUSIVE = "inconclusive"

_ALLOWED_OPS = frozenset({"eq", "neq", "contains"})


class RuleEvaluationError(ValueError):
    """Raised when rule text or log data is invalid or oversized."""


@dataclass
class Condition:
    """One rule condition: field, operator and expected value."""

    field: str
    op: str
    value: Any


@dataclass
class Evaluation:
    """Outcome of applying the rule to one event."""

    dataset: str
    line: int
    outcome: str
    missing_fields: list[str] = field(default_factory=list)
    failed_fields: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "dataset": self.dataset,
            "line": self.line,
            "outcome": self.outcome,
            "missing_fields": list(self.missing_fields),
            "failed_fields": list(self.failed_fields),
        }


@dataclass
class DatasetSummary:
    """Per-dataset match counts."""

    total: int = 0
    matched: int = 0
    missed: int = 0
    inconclusive: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "total": self.total,
            "matched": self.matched,
            "missed": self.missed,
            "inconclusive": self.inconclusive,
        }


@dataclass
class RuleResult:
    """Verdict of one rule replay across target and control datasets."""

    rule: str = ""
    verdict: str = VERDICT_INCONCLUSIVE
    target: DatasetSummary = field(default_factory=DatasetSummary)
    control: DatasetSummary = field(default_factory=DatasetSummary)
    reasons: list[str] = field(default_factory=list)
    evaluations: list[Evaluation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "engine": ENGINE_VERSION,
            "verdict": self.verdict,
            "target": self.target.to_dict(),
            "control": self.control.to_dict(),
            "reasons": list(self.reasons),
            "evaluations": [item.to_dict() for item in self.evaluations],
        }


def parse_rule(rule_text: str) -> list[Condition]:
    """Parse the rule JSON document into a condition list.

    Args:
        rule_text: JSON document ``{"version": 1, "all": [...]}``.

    Returns:
        The ordered condition list.

    Raises:
        RuleEvaluationError: Malformed, oversized or unsupported rule.
    """
    raw = str(rule_text or "")
    if len(raw.encode("utf-8", errors="replace")) > MAX_RULE_BYTES:
        raise RuleEvaluationError(f"rule must be at most {MAX_RULE_BYTES} bytes")
    try:
        document = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuleEvaluationError(f"rule JSON: {exc}") from exc
    if not isinstance(document, dict) or set(document) != {"version", "all"}:
        raise RuleEvaluationError("rule needs exactly version and all fields")
    if document["version"] != 1:
        raise RuleEvaluationError(f"unsupported rule version: {document['version']!r}")
    all_conditions = document["all"]
    if not isinstance(all_conditions, list) or not all_conditions or len(all_conditions) > MAX_CONDITIONS:
        raise RuleEvaluationError(f"all needs 1-{MAX_CONDITIONS} conditions")
    conditions: list[Condition] = []
    for index, raw_condition in enumerate(all_conditions):
        if not isinstance(raw_condition, dict) or set(raw_condition) != {"field", "op", "value"}:
            raise RuleEvaluationError(f"condition {index + 1} needs exactly field, op and value")
        name = raw_condition["field"]
        op = raw_condition["op"]
        value = raw_condition["value"]
        if not isinstance(name, str) or not name or len(name) > MAX_FIELD_LENGTH:
            raise RuleEvaluationError(f"condition {index + 1}: invalid field name")
        if op not in _ALLOWED_OPS:
            raise RuleEvaluationError(f"condition {index + 1}: only eq, neq, contains operators are supported")
        if isinstance(value, str):
            if len(value.encode("utf-8", errors="replace")) > MAX_RULE_VALUE_BYTES:
                raise RuleEvaluationError(f"condition {index + 1}: value exceeds {MAX_RULE_VALUE_BYTES} bytes")
        elif isinstance(value, bool):
            if op == "contains":
                raise RuleEvaluationError(f"condition {index + 1}: contains value must be a string")
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            if op == "contains":
                raise RuleEvaluationError(f"condition {index + 1}: contains value must be a string")
        else:
            raise RuleEvaluationError(f"condition {index + 1}: value must be a string, number or boolean")
        conditions.append(Condition(field=name, op=op, value=value))
    return conditions


def _lookup(fields: dict[str, Any], field_name: str) -> tuple[Any, bool]:
    """Resolve one field: root dotted key first, then nested traversal."""
    if field_name in fields:
        return fields[field_name], True
    value: Any = fields
    for segment in field_name.split("."):
        if not isinstance(value, dict) or segment not in value:
            return None, False
        value = value[segment]
    return value, True


def _canonical_number(value: str) -> str:
    """Normalize a decimal literal so 1, 1.0 and 10e-1 compare equal."""
    text = str(value).strip()
    try:
        decimal = Decimal(text)
    except (InvalidOperation, ValueError) as exc:
        raise RuleEvaluationError(f"unparsable number: {value!r}") from exc
    if not decimal.is_finite():
        raise RuleEvaluationError(f"unbounded number: {value!r}")
    normalized = decimal.normalize()
    if normalized == normalized.to_integral_value():
        return str(normalized.quantize(Decimal(1)))
    return str(normalized)


def _compare(actual: Any, expected: Any, op: str) -> tuple[bool, bool]:
    """Compare one field value; returns (matched, evaluable)."""
    equal = False
    evaluable = False
    if isinstance(expected, str):
        if isinstance(actual, str):
            if op == "contains":
                equal = expected in actual
            else:
                equal = actual == expected
            evaluable = True
    elif isinstance(expected, bool):
        if isinstance(actual, bool):
            equal = actual == expected
            evaluable = True
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        if isinstance(actual, (int, float)) and not isinstance(actual, bool):
            try:
                left = _canonical_number(repr(actual))
                right = _canonical_number(repr(expected))
            except RuleEvaluationError:
                return False, False
            equal = left == right
            evaluable = True
    if op == "neq":
        equal = not equal
    return equal, evaluable


def _scalar_present(value: Any) -> bool:
    """Return whether one JSON value is a present scalar."""
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (bool, int, float)):
        return True
    if isinstance(value, list):
        return len(value) == 1 and _scalar_present(value[0])
    return False


def evaluate_event(conditions: list[Condition], fields: dict[str, Any]) -> Evaluation:
    """Apply every condition to one event.

    Args:
        conditions: Parsed rule conditions.
        fields: Normalized event field mapping.

    Returns:
        An :class:`Evaluation` for the event.
    """
    evaluation = Evaluation(dataset="", line=0, outcome="match")
    missing: dict[str, bool] = {}
    failed: dict[str, bool] = {}
    matched = True
    for condition in conditions:
        actual, found = _lookup(fields, condition.field)
        condition_match, evaluable = _compare(actual, condition.value, condition.op)
        if not found or not evaluable:
            if not missing.get(condition.field):
                missing[condition.field] = True
                evaluation.missing_fields.append(condition.field)
        elif not condition_match:
            if not failed.get(condition.field):
                failed[condition.field] = True
                evaluation.failed_fields.append(condition.field)
            matched = False
    if evaluation.missing_fields:
        evaluation.outcome = "inconclusive"
    elif not matched:
        evaluation.outcome = "no_match"
    evaluation.missing_fields.sort()
    evaluation.failed_fields.sort()
    return evaluation


def _parse_logs(text: str, dataset: str, max_events: int) -> list[dict[str, Any]]:
    """Parse one log dataset as JSON array or JSON lines.

    Args:
        text: Raw dataset text.
        dataset: Dataset name for error messages.
        max_events: Event count cap.

    Returns:
        List of field mappings.

    Raises:
        RuleEvaluationError: Unparsable, oversized or too-large dataset.
    """
    raw = str(text or "")
    if len(raw.encode("utf-8", errors="replace")) > MAX_LOG_BYTES:
        raise RuleEvaluationError(f"{dataset} logs must be at most {MAX_LOG_BYTES} bytes")
    events: list[dict[str, Any]] = []
    stripped = raw.strip()
    if stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise RuleEvaluationError(f"{dataset} logs JSON array: {exc}") from exc
        if not isinstance(parsed, list):
            raise RuleEvaluationError(f"{dataset} logs: expected a JSON array")
        for index, item in enumerate(parsed):
            if isinstance(item, dict):
                events.append(item)
            elif item is None or isinstance(item, (str, int, float, bool)):
                continue
            else:
                raise RuleEvaluationError(f"{dataset} logs item {index + 1}: unsupported type")
    else:
        for number, line in enumerate(stripped.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuleEvaluationError(f"{dataset} logs line {number}: {exc}") from exc
            if isinstance(parsed, dict):
                events.append(parsed)
            elif parsed is None or isinstance(parsed, (str, int, float, bool)):
                continue
            else:
                raise RuleEvaluationError(f"{dataset} logs line {number}: unsupported type")
    if len(events) > max_events:
        raise RuleEvaluationError(f"{dataset} logs exceed {max_events} events")
    return events


def evaluate_rule(rule_text: str, target_logs: str, control_logs: str) -> RuleResult:
    """Replay one rule against target and control datasets.

    A pass requires nonempty target and control sets, every target event
    matching, no control event matching and no unevaluable referenced
    field. This is log replay only: it never proves detection quality in
    a live SIEM.

    Args:
        rule_text: The JSON rule document.
        target_logs: Attack dataset (JSON array or JSON lines).
        control_logs: Benign dataset (JSON array or JSON lines).

    Returns:
        A :class:`RuleResult` with verdict, summaries and evaluations.

    Raises:
        RuleEvaluationError: Invalid rule or unparsable datasets.
    """
    conditions = parse_rule(rule_text)
    target = _parse_logs(target_logs, "target", MAX_EVENTS)
    control = _parse_logs(control_logs, "control", MAX_EVENTS - len(target))
    result = RuleResult(rule=str(rule_text))
    for dataset_name, events, summary in (
        ("target", target, result.target),
        ("control", control, result.control),
    ):
        for position, fields in enumerate(events, start=1):
            evaluation = evaluate_event(conditions, fields)
            evaluation.dataset = dataset_name
            evaluation.line = position
            summary.total += 1
            if evaluation.outcome == "match":
                summary.matched += 1
            elif evaluation.outcome == "no_match":
                summary.missed += 1
            else:
                summary.inconclusive += 1
            result.evaluations.append(evaluation)
    if result.target.total == 0:
        result.reasons.append("target dataset is empty; evaluation cannot complete")
    if result.control.total == 0:
        result.reasons.append("control dataset is empty; false-positive exposure cannot be assessed")
    if result.target.inconclusive + result.control.inconclusive > 0:
        result.reasons.append("some events reference absent or incompatible fields; outcome inconclusive")
    if result.target.missed > 0:
        result.reasons.append(f"{result.target.missed} target events did not match the rule")
    if result.control.matched > 0:
        result.reasons.append(f"{result.control.matched} control events matched the rule; false positives")
    if result.target.missed > 0 or result.control.matched > 0:
        result.verdict = VERDICT_FAIL
    if result.target.total == 0 or result.control.total == 0 or result.target.inconclusive + result.control.inconclusive > 0:
        result.verdict = VERDICT_INCONCLUSIVE
    if not result.reasons and result.target.missed == 0 and result.control.matched == 0:
        result.verdict = VERDICT_PASS
    return result


def metrics(result: RuleResult) -> dict[str, int]:
    """Return tp/fn/fp/tn metrics for one replay result.

    Args:
        result: A replay result from :func:`evaluate_rule`.

    Returns:
        Mapping with ``tp`` (target matches), ``fn`` (target misses),
        ``fp`` (control matches) and ``tn`` (control misses).
    """
    return {
        "tp": result.target.matched,
        "fn": result.target.missed,
        "fp": result.control.matched,
        "tn": result.control.missed,
    }


__all__ = [
    "ENGINE_VERSION",
    "MAX_CONDITIONS",
    "MAX_EVENTS",
    "RuleEvaluationError",
    "RuleResult",
    "VERDICT_FAIL",
    "VERDICT_INCONCLUSIVE",
    "VERDICT_PASS",
    "Condition",
    "DatasetSummary",
    "Evaluation",
    "evaluate_event",
    "evaluate_rule",
    "metrics",
    "parse_rule",
]
