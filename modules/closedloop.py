"""Closed-loop detection rule tuning: baseline vs candidate comparison.

Given a baseline rule and a candidate rule plus the same attack
(target) and benign (control) datasets, this module replays both, keeps
the per-rule metrics, computes the improvement delta and emits
deterministic tuning suggestions derived from the replay evidence. The
operator decides; nothing is deployed automatically.

Adapted from the ARTEX ``closedloop`` engine (AGPL-3.0).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from modules.defense_eval import (
    RuleResult,
    evaluate_rule,
    metrics,
)

VERDICT_IMPROVED = "improved"
VERDICT_REGRESSED = "regressed"
VERDICT_EQUIVALENT = "equivalent"
VERDICT_INCONCLUSIVE = "inconclusive"

_MAX_SUGGESTIONS = 12


@dataclass
class RuleMetrics:
    """Confusion-style metrics for one replayed rule."""

    tp: int = 0
    fn: int = 0
    fp: int = 0
    tn: int = 0
    inconclusive: int = 0
    verdict: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "tp": self.tp,
            "fn": self.fn,
            "fp": self.fp,
            "tn": self.tn,
            "inconclusive": self.inconclusive,
            "verdict": self.verdict,
        }


@dataclass
class Comparison:
    """Outcome of comparing a candidate rule against a baseline."""

    baseline: RuleMetrics = field(default_factory=RuleMetrics)
    candidate: RuleMetrics = field(default_factory=RuleMetrics)
    verdict: str = VERDICT_INCONCLUSIVE
    reasons: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    baseline_result: RuleResult | None = None
    candidate_result: RuleResult | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "baseline": self.baseline.to_dict(),
            "candidate": self.candidate.to_dict(),
            "verdict": self.verdict,
            "reasons": list(self.reasons),
            "suggestions": list(self.suggestions),
        }


def _metrics_for(result: RuleResult) -> RuleMetrics:
    """Convert one replay result into confusion-style metrics."""
    values = metrics(result)
    return RuleMetrics(
        tp=values["tp"],
        fn=values["fn"],
        fp=values["fp"],
        tn=values["tn"],
        inconclusive=result.target.inconclusive + result.control.inconclusive,
        verdict=result.verdict,
    )


def compare_rules(
    baseline_rule: str,
    candidate_rule: str,
    target_logs: str,
    control_logs: str,
) -> Comparison:
    """Replay baseline and candidate rules over identical datasets.

    Args:
        baseline_rule: Current rule JSON document.
        candidate_rule: Proposed rule JSON document.
        target_logs: Attack dataset (JSON array or JSON lines).
        control_logs: Benign dataset (JSON array or JSON lines).

    Returns:
        A :class:`Comparison` with metrics, verdict and suggestions.

    Raises:
        RuleEvaluationError: When either rule or dataset is invalid.
    """
    baseline_result = evaluate_rule(baseline_rule, target_logs, control_logs)
    candidate_result = evaluate_rule(candidate_rule, target_logs, control_logs)
    baseline = _metrics_for(baseline_result)
    candidate = _metrics_for(candidate_result)
    comparison = Comparison(baseline=baseline, candidate=candidate)
    comparison.baseline_result = baseline_result
    comparison.candidate_result = candidate_result
    if baseline.inconclusive or candidate.inconclusive:
        comparison.verdict = VERDICT_INCONCLUSIVE
        comparison.reasons.append("one or both replays were inconclusive; fix field availability first")
    elif baseline.verdict == "pass" and candidate.verdict == "pass":
        comparison.verdict = VERDICT_EQUIVALENT
        comparison.reasons.append("both rules pass the replay; prefer the candidate only for clarity")
    elif baseline.verdict == "pass" and candidate.verdict != "pass":
        comparison.verdict = VERDICT_REGRESSED
        comparison.reasons.append(f"candidate {candidate.verdict} where baseline passed")
    elif baseline.verdict == "fail" and candidate.verdict == "pass":
        comparison.verdict = VERDICT_IMPROVED
        comparison.reasons.append("candidate passes where baseline failed")
    else:
        comparison.verdict = VERDICT_EQUIVALENT
        comparison.reasons.append("both rules fail the replay; tune conditions further")
    comparison.suggestions = suggest_tuning(candidate_result, baseline_result)
    return comparison


def suggest_tuning(candidate: RuleResult, baseline: RuleResult | None = None) -> list[str]:
    """Return deterministic tuning suggestions from replay evidence.

    Args:
        candidate: Replay result for the candidate rule.
        baseline: Optional replay result for the baseline rule.

    Returns:
        Human-readable suggestions (empty when nothing to tune).
    """
    suggestions: list[str] = []
    missing: set[str] = set()
    failed: set[str] = set()
    for evaluation in candidate.evaluations:
        missing.update(evaluation.missing_fields)
        if evaluation.dataset == "target" and evaluation.outcome == "no_match":
            failed.update(evaluation.failed_fields)
    if candidate.target.missed > 0:
        if failed:
            suggestions.append(
                f"loosen or split conditions on: {', '.join(sorted(failed))}"
            )
        suggestions.append("review the unmatched target events for field value drift")
    if candidate.control.matched > 0:
        suggestions.append("narrow the rule; control (benign) events matched")
        if failed:
            suggestions.append(
                f"consider adding negated conditions on: {', '.join(sorted(failed))}"
            )
    if candidate.target.inconclusive + candidate.control.inconclusive > 0:
        suggestions.append(
            f"ensure referenced fields exist in every event: {', '.join(sorted(missing))}"
        )
    if candidate.verdict == "pass":
        if baseline is not None and baseline.verdict == "fail":
            suggestions.append("candidate fixes the baseline failure; keep the candidate")
        else:
            suggestions.append("candidate passes replay; no tuning needed")
    return suggestions[:_MAX_SUGGESTIONS]


__all__ = [
    "Comparison",
    "RuleMetrics",
    "VERDICT_EQUIVALENT",
    "VERDICT_IMPROVED",
    "VERDICT_INCONCLUSIVE",
    "VERDICT_REGRESSED",
    "compare_rules",
    "suggest_tuning",
]
