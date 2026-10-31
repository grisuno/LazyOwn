"""Evidence-gated finalization contract.

Ports the agent-finalizer idea (surveyed from external/cyberstrikeai, rebranded):
a run reported ``done`` is only ``achieved`` when real execution evidence backs
it; otherwise the verdict is downgraded with a ``missing_execution_evidence``
reason, the same philosophy apt_chain applies per step with ``evidence_observed``.
"""

from __future__ import annotations

from modules import lazy_finalizer as fin


def test_done_with_confirmed_findings_is_achieved_and_verified():
    """A done run with confirmed findings finalizes as verified achieved."""
    decision = fin.decide("done", "achieved", facts=3, findings=2, confirmed=1, tested=4)
    assert decision.verdict == fin.VERDICT_ACHIEVED
    assert decision.evidence_verified is True
    assert decision.finalizable is True
    assert decision.completion_reason == fin.REASON_VERIFIED


def test_done_without_any_evidence_is_downgraded_to_failed():
    """A bare done status with no evidence cannot claim achieved."""
    decision = fin.decide("done", "achieved", facts=0, findings=0, confirmed=0, tested=0)
    assert decision.verdict == fin.VERDICT_FAILED
    assert decision.evidence_verified is False
    assert decision.completion_reason == fin.REASON_MISSING_EVIDENCE
    assert "confirmed_findings" in decision.missing_checks
    assert "tested_coverage" in decision.missing_checks


def test_done_with_weak_evidence_downgrades_to_partial():
    """Done with facts but no confirmed/tested evidence becomes partial."""
    decision = fin.decide("done", "achieved", facts=2, findings=0, confirmed=0, tested=0)
    assert decision.verdict == fin.VERDICT_PARTIAL
    assert decision.evidence_verified is False
    assert decision.completion_reason == fin.REASON_MISSING_EVIDENCE
    assert decision.finalizable is True


def test_facts_plus_tested_is_strong_evidence():
    """Facts together with tested coverage count as verified evidence."""
    decision = fin.decide("done", "achieved", facts=1, findings=0, confirmed=0, tested=2)
    assert decision.evidence_verified is True
    assert decision.verdict == fin.VERDICT_ACHIEVED


def test_non_done_status_is_not_finalizable_without_evidence():
    """An unfinished run with no evidence is not finalizable."""
    decision = fin.decide("exhausted", "failed", facts=0, findings=0, confirmed=0, tested=0)
    assert decision.finalizable is False
    assert decision.completion_reason == fin.REASON_UNFINISHED


def test_decision_to_dict_round_trips_fields():
    """The decision serialises every field for the verdict map."""
    decision = fin.decide("done", "achieved", facts=0, findings=1, confirmed=0, tested=1)
    data = decision.to_dict()
    assert set(data) == {
        "verdict",
        "finalizable",
        "evidence_verified",
        "completion_reason",
        "evidence_refs",
        "missing_checks",
        "pending_approvals",
        "pending_plan_steps",
    }
    assert "findings:1" in data["evidence_refs"]


def test_pending_approvals_block_achieved():
    """Undecided human approvals prevent the achieved verdict."""
    decision = fin.decide(
        "done",
        "achieved",
        facts=2,
        findings=2,
        confirmed=1,
        tested=3,
        pending_approvals=["ap0123456789abcdef"],
    )
    assert decision.verdict == fin.VERDICT_PARTIAL
    assert decision.completion_reason == fin.REASON_PENDING_APPROVALS
    assert decision.pending_approvals == ["ap0123456789abcdef"]


def test_pending_plan_steps_block_achieved():
    """Still-open plan steps prevent the achieved verdict."""
    decision = fin.decide(
        "done",
        "achieved",
        facts=2,
        findings=2,
        confirmed=1,
        tested=3,
        pending_plan_steps=["confirm_shell"],
    )
    assert decision.verdict == fin.VERDICT_PARTIAL
    assert decision.completion_reason == fin.REASON_PENDING_STEPS
    assert decision.pending_plan_steps == ["confirm_shell"]


def test_pending_blocks_beat_evidence():
    """Pending work blocks even with strong evidence recorded."""
    decision = fin.decide(
        "done",
        "achieved",
        facts=5,
        findings=4,
        confirmed=2,
        tested=6,
        pending_approvals=["apf"],
        pending_plan_steps=["step2"],
    )
    assert decision.verdict == fin.VERDICT_PARTIAL
    assert decision.evidence_verified is True


def test_pending_state_survives_into_non_done_reasons():
    """Non-done runs still report the pending work they carry."""
    decision = fin.decide("timeout", "failed", facts=1, findings=1, confirmed=0, tested=1, pending_plan_steps=["x"])
    assert decision.pending_plan_steps == ["x"]
    assert decision.completion_reason == fin.REASON_PARTIAL
