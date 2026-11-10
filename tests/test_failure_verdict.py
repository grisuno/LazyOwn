"""Failure verdict contract: classification, action hints and hard stops.

Every scenario states Given, When, Then.
"""

from __future__ import annotations

from modules.failure_verdict import (
    CLASS_ACTIONS,
    FailureClass,
    FallbackAction,
    classify_failure,
    classify_outcome,
)


def test_lockout_output_aborts():
    """Given an attempt whose output shows an account lockout, When
    classified, Then the verdict is lockout/abort and hard-stop."""
    verdict = classify_failure("netexec smb dc01", output="STATUS_ACCOUNT_LOCKED for user svc")
    assert verdict.failure_class == FailureClass.LOCKOUT
    assert verdict.action == FallbackAction.ABORT
    assert verdict.is_hard_stop
    assert not verdict.is_fallback_eligible


def test_out_of_scope_aborts_before_everything():
    """Given an output mixing scope and auth markers, When classified,
    Then scope wins and aborts: out-of-scope must never be retried."""
    verdict = classify_failure("nmap x", output="logon failure but 10.7.7.7 is out of scope")
    assert verdict.failure_class == FailureClass.SCOPE
    assert verdict.is_hard_stop


def test_auth_failure_is_fallback_eligible():
    """Given a logon failure, When classified, Then the verdict requests
    a fallback instead of another blind retry."""
    verdict = classify_failure(
        "python3 modules/atomic_exploit_bridge.py run --id ad_lab_passspray --rhost dc01",
        output="[-] STATUS_LOGON_FAILURE",
    )
    assert verdict.failure_class == FailureClass.AUTH
    assert verdict.is_fallback_eligible


def test_permission_wall_requests_fallback():
    """Given an access-denied wall, When classified, Then the verdict is
    permission with a fallback action."""
    verdict = classify_failure("secretsdump.py dc01", output="SMB SessionError: code 0xc0000022 (ACCESS_DENIED)")
    assert verdict.failure_class == FailureClass.PERMISSION
    assert verdict.action == FallbackAction.FALLBACK


def test_missing_tool_skips():
    """Given command-not-found evidence, When classified, Then the step
    is skipped rather than retried against nowhere."""
    verdict = classify_failure("nope --help", output="/bin/sh: 1: nope: command not found", exit_code=127)
    assert verdict.failure_class == FailureClass.TOOL_MISSING
    assert verdict.action == FallbackAction.SKIP


def test_timeout_with_clean_output_retries():
    """Given a runner timeout flag and no other marker, When classified,
    Then the verdict retries (transient), not aborts."""
    verdict = classify_failure("enum4linux -a dc01", output="", timed_out=True)
    assert verdict.failure_class == FailureClass.TIMEOUT
    assert verdict.action == FallbackAction.RETRY


def test_network_markers_retry():
    """Given connection-refused evidence, When classified, Then the
    verdict is a retryable network failure."""
    verdict = classify_failure("hydra ssh://dc01", output="ssh_connect: connection refused")
    assert verdict.failure_class == FailureClass.NETWORK
    assert verdict.action == FallbackAction.RETRY


def test_unknown_output_keeps_default_retry():
    """Given output with no classifying marker, When classified, Then
    the verdict stays unknown/retry so default policies never change."""
    verdict = classify_failure("whatever --flag", output="global variable check".capitalize())
    assert verdict.failure_class == FailureClass.UNKNOWN
    assert verdict.action == FallbackAction.RETRY


def test_success_and_skipped_outcomes_never_classify_as_fallback():
    """Given a non-failure outcome object, When classified, Then the
    verdict is never fallback-eligible (callers gate on it)."""

    class FakeOutcome:
        status = "ok"
        run = "x"
        output = "ACCESS_DENIED"
        reason = ""
        duration_ms = 1.0

    verdict = classify_outcome(FakeOutcome())
    assert not verdict.is_fallback_eligible


def test_failed_outcome_object_classifies_from_output():
    """Given a failed StepOutcome-shaped object, When classified, Then
    the verdict comes from its captured output."""

    class FakeOutcome:
        status = "failed"
        run = "run --id ad_lab_kerberoast"
        output = "account locked out for 10 minutes"
        reason = ""
        duration_ms = 2.0

    verdict = classify_outcome(FakeOutcome())
    assert verdict.failure_class == FailureClass.LOCKOUT
    assert verdict.is_hard_stop


def test_action_matrix_is_total():
    """Given the action matrix, When read, Then every class maps to one
    documented action and lockout/scope abort."""
    assert set(CLASS_ACTIONS) == set(FailureClass)
    assert CLASS_ACTIONS[FailureClass.LOCKOUT] == FallbackAction.ABORT
    assert CLASS_ACTIONS[FailureClass.SCOPE] == FallbackAction.ABORT


def test_lockout_marker_is_case_insensitive():
    """Given uppercase evidence, When classified, Then matching is
    case-insensitive."""
    verdict = classify_failure("cmd", output="The Account Has Been LOCKED OUT")
    assert verdict.failure_class == FailureClass.LOCKOUT
