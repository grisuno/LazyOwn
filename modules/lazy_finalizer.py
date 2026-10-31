"""Evidence-gated finalization for the autonomous loop and apt_chain.

A task or chain run may report ``done`` while nothing was actually executed and
no evidence was captured: a worker self-report, an empty LLM turn, or a chain
whose steps all abstained. This module is the single gate that decides whether a
run may be promoted to a verified, user-facing conclusion. Natural-language or
status-level claims are only candidates until :func:`decide` confirms the run is
backed by real execution evidence.

The contract is pure (no I/O): the caller passes the evidence counts it already
has and receives a :class:`FinalizerDecision`. Both autonomous runtimes consume
it so ``achieved`` never rests on a bare status flag, mirroring the chain
runner's per-step ``evidence_observed`` verdict at task scope.
"""

from __future__ import annotations

from dataclasses import dataclass, field

STATUS_DONE = "done"

REASON_VERIFIED = "verified"
REASON_MISSING_EVIDENCE = "missing_execution_evidence"
REASON_PARTIAL = "partial_evidence"
REASON_UNFINISHED = "unfinished"
REASON_PENDING_APPROVALS = "pending_approvals"
REASON_PENDING_STEPS = "pending_plan_steps"

VERDICT_ACHIEVED = "achieved"
VERDICT_PARTIAL = "partial"
VERDICT_FAILED = "failed"


@dataclass(frozen=True)
class FinalizerDecision:
    """The single verdict on whether a run is a verified conclusion.

    Attributes:
        verdict: Evidence-adjusted outcome (``achieved``/``partial``/``failed``).
        finalizable: Whether the run may be promoted to a user-facing answer.
        evidence_verified: Whether real execution evidence backs the claim.
        completion_reason: Machine-readable reason for the decision.
        evidence_refs: Short human-readable evidence tokens that were counted.
        missing_checks: Evidence classes that were expected but absent.
        pending_approvals: Human-approval requests still undecided.
        pending_plan_steps: Plan steps still open when the run stopped.
    """

    verdict: str
    finalizable: bool
    evidence_verified: bool
    completion_reason: str
    evidence_refs: list[str] = field(default_factory=list)
    missing_checks: list[str] = field(default_factory=list)
    pending_approvals: list[str] = field(default_factory=list)
    pending_plan_steps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Return the decision as a JSON-serialisable dict for the verdict map."""
        return {
            "verdict": self.verdict,
            "finalizable": self.finalizable,
            "evidence_verified": self.evidence_verified,
            "completion_reason": self.completion_reason,
            "evidence_refs": list(self.evidence_refs),
            "missing_checks": list(self.missing_checks),
            "pending_approvals": list(self.pending_approvals),
            "pending_plan_steps": list(self.pending_plan_steps),
        }


def decide(
    status: str,
    candidate_verdict: str,
    facts: int,
    findings: int,
    confirmed: int,
    tested: int,
    pending_approvals: list[str] | None = None,
    pending_plan_steps: list[str] | None = None,
) -> FinalizerDecision:
    """Return the evidence-gated finalization decision for a run.

    A run is evidence-verified when it produced confirmed findings, or findings
    plus tested coverage, or facts plus tested coverage. A run that claims
    ``done`` with none of these is downgraded: the status is a self-report the
    evidence does not support, so the verdict cannot stay ``achieved``.

    Hard blocking rule (finalization contract): any undecided human approval
    or any still-open plan step prevents ``achieved`` regardless of evidence,
    because the run is not actually finished; the verdict degrades to
    ``partial`` with the blocking reason named.

    Args:
        status: Engine status of the run (``done`` is the only promotable one).
        candidate_verdict: The verdict the caller would assign before gating.
        facts: Count of non-cold facts recorded.
        findings: Count of findings recorded.
        confirmed: Count of confirmed or reproduced findings.
        tested: Count of assets with at least one completed probe.
        pending_approvals: Undecided approval request ids.
        pending_plan_steps: Open plan step identifiers.

    Returns:
        A :class:`FinalizerDecision` whose ``verdict`` never exceeds what the
        evidence and the pending-work state support.
    """
    approvals = [str(item) for item in (pending_approvals or []) if str(item).strip()]
    plan_steps = [str(item) for item in (pending_plan_steps or []) if str(item).strip()]
    refs: list[str] = []
    if confirmed > 0:
        refs.append(f"confirmed:{confirmed}")
    if findings > 0:
        refs.append(f"findings:{findings}")
    if facts > 0:
        refs.append(f"facts:{facts}")
    if tested > 0:
        refs.append(f"tested:{tested}")

    strong = confirmed > 0 or (findings > 0 and tested > 0) or (facts > 0 and tested > 0)
    weak = facts > 0 or findings > 0 or tested > 0
    evidence_verified = bool(strong)

    missing: list[str] = []
    if confirmed <= 0:
        missing.append("confirmed_findings")
    if tested <= 0:
        missing.append("tested_coverage")

    is_done = str(status or "").strip().lower() == STATUS_DONE

    if is_done and approvals:
        return FinalizerDecision(
            verdict=VERDICT_PARTIAL,
            finalizable=True,
            evidence_verified=evidence_verified,
            completion_reason=REASON_PENDING_APPROVALS,
            evidence_refs=refs,
            missing_checks=missing,
            pending_approvals=approvals,
            pending_plan_steps=plan_steps,
        )
    if is_done and plan_steps:
        return FinalizerDecision(
            verdict=VERDICT_PARTIAL,
            finalizable=True,
            evidence_verified=evidence_verified,
            completion_reason=REASON_PENDING_STEPS,
            evidence_refs=refs,
            missing_checks=missing,
            pending_approvals=approvals,
            pending_plan_steps=plan_steps,
        )
    if is_done and evidence_verified:
        return FinalizerDecision(
            verdict=candidate_verdict or VERDICT_ACHIEVED,
            finalizable=True,
            evidence_verified=True,
            completion_reason=REASON_VERIFIED,
            evidence_refs=refs,
            missing_checks=[],
        )
    if is_done and not evidence_verified:
        downgraded = VERDICT_PARTIAL if weak else VERDICT_FAILED
        return FinalizerDecision(
            verdict=downgraded,
            finalizable=weak,
            evidence_verified=False,
            completion_reason=REASON_MISSING_EVIDENCE,
            evidence_refs=refs,
            missing_checks=missing,
            pending_approvals=approvals,
            pending_plan_steps=plan_steps,
        )
    reason = REASON_PARTIAL if (strong or weak) else REASON_UNFINISHED
    return FinalizerDecision(
        verdict=candidate_verdict or (VERDICT_PARTIAL if weak else VERDICT_FAILED),
        finalizable=bool(weak),
        evidence_verified=evidence_verified,
        completion_reason=reason,
        evidence_refs=refs,
        missing_checks=missing,
        pending_approvals=approvals,
        pending_plan_steps=plan_steps,
    )


__all__ = [
    "FinalizerDecision",
    "REASON_MISSING_EVIDENCE",
    "REASON_PARTIAL",
    "REASON_PENDING_APPROVALS",
    "REASON_PENDING_STEPS",
    "REASON_UNFINISHED",
    "REASON_VERIFIED",
    "VERDICT_ACHIEVED",
    "VERDICT_FAILED",
    "VERDICT_PARTIAL",
    "decide",
]
