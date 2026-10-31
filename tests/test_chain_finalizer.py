"""Chain finalization contract tests.

The apt_chain pipeline gates its terminal verdict through
``modules.lazy_finalizer``: a chain that finishes ``ok`` without captured
evidence, or with steps left open, is downgraded exactly like an
autonomous task, and the decision lands in ``ChainRunResult.finalization``.
"""

from __future__ import annotations

from modules.chain_registry import Chain, ChainStep
from modules.chain_runner import ChainRunner
from modules.lazy_finalizer import (
    REASON_PENDING_STEPS,
    REASON_VERIFIED,
    VERDICT_ACHIEVED,
    VERDICT_PARTIAL,
)


def _chain(steps: list[ChainStep], **kwargs) -> Chain:
    """Build a chain for a finalizer scenario."""
    return Chain(name="demo", defaults={"target": "127.0.0.1"}, steps=steps, **kwargs)


def test_chain_with_captured_evidence_is_verified():
    """Given a chain whose step captures evidence, When it finishes,
    Then the finalization is verified achieved."""
    executor = lambda command: "MINIO_ROOT_PASSWORD=leaked"  # noqa: E731
    chain = _chain([ChainStep(id="probe", run="verify", capture="evidence")])
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    final = result.finalization
    assert final["verdict"] == VERDICT_ACHIEVED
    assert final["completion_reason"] == REASON_VERIFIED
    assert final["evidence_verified"] is True
    assert "finalization" in result.to_dict()


def test_chain_ok_without_evidence_is_downgraded():
    """Given a chain that returns plain output and captures nothing, When
    it finishes ok, Then the verdict is downgraded to partial."""
    executor = lambda command: "ok"  # noqa: E731
    chain = _chain([ChainStep(id="probe", run="echo ok")])
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert result.finalization["verdict"] == VERDICT_PARTIAL


def test_chain_with_open_steps_reports_pending_reason():
    """Given a chain where one step fails, When the run stops, Then the
    finalization names the open step and blocks achieved."""

    def executor(command: str) -> str:
        if command == "fail":
            raise RuntimeError("step failed")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="bad", run="fail", continue_on_error=True),
            ChainStep(id="good", run="echo ok"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    final = result.finalization
    assert final["verdict"] == VERDICT_PARTIAL
    assert final["completion_reason"] == REASON_PENDING_STEPS
    assert "bad" in final["pending_plan_steps"]


def test_dry_run_has_no_finalization():
    """Given a dry run, When it finishes, Then no finalization is
    attached (nothing executed, nothing to verify)."""
    executor = lambda command: "never"  # noqa: E731
    chain = _chain([ChainStep(id="probe", run="echo hi")])
    result = ChainRunner(chain, executor=executor, dry_run=True).run()
    assert result.finalization == {}


def test_hunting_verdicts_count_as_confirmed(tmp_path):
    """Given steps with declared hunting evidence, When they verify,
    Then the observed verdicts count as confirmed evidence."""
    evidence = tmp_path / "hunt.jsonl"
    evidence.write_text('{"user": "root"}\n', encoding="utf-8")

    def executor(command: str) -> str:
        return "collected"

    chain = _chain(
        [
            ChainStep(
                id="hunt",
                run="collect",
                evidence=[str(evidence)],
                required_fields=["user"],
            )
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.chain_proven is True
    assert result.finalization["evidence_verified"] is True
