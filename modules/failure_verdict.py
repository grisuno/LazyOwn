"""Failure verdict contract: classify one failed execution into an action.

Any runner (chain, retry, autonomous loop) captures the same evidence
for a failed attempt: command, exit code, output tail and a timeout
flag. This module turns that evidence into one typed verdict with an
engine action so every surface can share a single policy: never retry a
lockout, stop spraying after one, skip tool-less attempts outright, and
hand auth or permission walls to the adaptive fallback arbiter instead
of burning retries.

Pure stdlib, no I/O: the caller owns the evidence and the action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

_OUTPUT_TAIL_CHARS = 4000

_SCOPE_MARKERS = ("out of scope", "scope enforcement", "blocked by scope", "outside the scope")
_LOCKOUT_MARKERS = (
    "account locked",
    "account_lockout",
    "locked out",
    "status_account_locked",
    "kdc_err_client_revoked",
    "the account has been locked",
)
_AUTH_MARKERS = (
    "status_logon_failure",
    "logon failure",
    "authentication failed",
    "invalid credentials",
    "unauthorized",
    "krb5kdc_err_preauth_failed",
)
_PERMISSION_MARKERS = (
    "access denied",
    "access_denied",
    "status_access_denied",
    "permission denied",
    "permission_denied",
    "operation not permitted",
    "insufficient privilege",
    "error 5",
)
_TIMEOUT_MARKERS = ("timed out", "timeout")
_NETWORK_MARKERS = (
    "connection refused",
    "connection reset",
    "host unreachable",
    "no route to host",
    "network is unreachable",
    "network unreachable",
    "temporary failure in name resolution",
    "could not resolve host",
    "econnrefused",
    "broken pipe",
)
_TOOL_MISSING_MARKERS = (
    "command not found",
    "not recognized as an internal or external command",
    "not found in path",
    "executable file not found",
)

_EXIT_TOOL_MISSING = 127


class FailureClass(str, Enum):  # noqa: UP042 — repo pattern keeps str, Enum
    """Why one attempt failed, as far as captured evidence can say."""

    LOCKOUT = "lockout"
    SCOPE = "scope"
    AUTH = "auth"
    PERMISSION = "permission"
    TOOL_MISSING = "tool_missing"
    TIMEOUT = "timeout"
    NETWORK = "network"
    UNKNOWN = "unknown"


class FallbackAction(str, Enum):  # noqa: UP042 — repo pattern keeps str, Enum
    """Engine reaction requested for the verdict."""

    ABORT = "abort"
    FALLBACK = "fallback"
    SKIP = "skip"
    RETRY = "retry"


_CLASS_ACTIONS: dict[FailureClass, FallbackAction] = {
    FailureClass.LOCKOUT: FallbackAction.ABORT,
    FailureClass.SCOPE: FallbackAction.ABORT,
    FailureClass.AUTH: FallbackAction.FALLBACK,
    FailureClass.PERMISSION: FallbackAction.FALLBACK,
    FailureClass.TOOL_MISSING: FallbackAction.SKIP,
    FailureClass.TIMEOUT: FallbackAction.RETRY,
    FailureClass.NETWORK: FallbackAction.RETRY,
    FailureClass.UNKNOWN: FallbackAction.RETRY,
}

CLASS_ACTIONS: dict[FailureClass, FallbackAction] = dict(_CLASS_ACTIONS)

_EVOLUTION_ORDER: tuple[tuple[FailureClass, tuple[str, ...]], ...] = (
    (FailureClass.SCOPE, _SCOPE_MARKERS),
    (FailureClass.LOCKOUT, _LOCKOUT_MARKERS),
    (FailureClass.AUTH, _AUTH_MARKERS),
    (FailureClass.PERMISSION, _PERMISSION_MARKERS),
    (FailureClass.TOOL_MISSING, _TOOL_MISSING_MARKERS),
    (FailureClass.TIMEOUT, _TIMEOUT_MARKERS),
    (FailureClass.NETWORK, _NETWORK_MARKERS),
)


@dataclass(frozen=True)
class FailureVerdict:
    """One classified failure with the action its class requests."""

    failure_class: FailureClass
    action: FallbackAction
    reason: str = ""

    @property
    def is_hard_stop(self) -> bool:
        """Return True when the verdict forbids any further attempt."""
        return self.action == FallbackAction.ABORT

    @property
    def is_fallback_eligible(self) -> bool:
        """Return True when adaptive alternatives may replace the retry."""
        return self.action == FallbackAction.FALLBACK


def _marker_hit(markers: tuple[str, ...], haystack: str) -> str:
    """Return the first matching marker, or empty string when none hits."""
    for marker in markers:
        if marker in haystack:
            return marker
    return ""


def classify_failure(
    command: str,
    output: str = "",
    exit_code: int | None = None,
    timed_out: bool = False,
) -> FailureVerdict:
    """Classify one failed attempt into a verdict with an engine action.

    Args:
        command: The attempted command line (not parsed; kept empty-safe).
        output: Captured stdout/stderr or the error reason; the tail is
            enough and long inputs are truncated before matching.
        exit_code: Process exit status when the runner knows it.
        timed_out: True when the runner enforced a wall-clock timeout.

    Returns:
        A :class:`FailureVerdict`; unknown evidence still carries an
        action (retry) so a runner's default policy stays unchanged.
    """
    del command
    haystack = (output or "").lower()[-_OUTPUT_TAIL_CHARS:]
    for failure_class, markers in _EVOLUTION_ORDER:
        marker = _marker_hit(markers, haystack)
        if marker:
            return FailureVerdict(
                failure_class,
                _CLASS_ACTIONS[failure_class],
                f"marker {marker!r}",
            )
    if timed_out:
        return FailureVerdict(
            FailureClass.TIMEOUT,
            _CLASS_ACTIONS[FailureClass.TIMEOUT],
            "runner-enforced timeout",
        )
    if exit_code == _EXIT_TOOL_MISSING:
        return FailureVerdict(
            FailureClass.TOOL_MISSING,
            _CLASS_ACTIONS[FailureClass.TOOL_MISSING],
            f"exit code {_EXIT_TOOL_MISSING}",
        )
    return FailureVerdict(
        FailureClass.UNKNOWN,
        _CLASS_ACTIONS[FailureClass.UNKNOWN],
        "no classifying marker",
    )


def classify_outcome(outcome: object) -> FailureVerdict:
    """Classify one runner outcome object carrying the standard fields.

    Args:
        outcome: Anything exposing ``run``, ``status``, ``output``,
            ``reason`` and ``duration_ms`` (a chain ``StepOutcome``).

    Returns:
        The verdict only when the outcome actually failed; a successful
        or skipped outcome classifies as unknown-retry, which callers
        gate on :attr:`FailureVerdict.is_fallback_eligible` before use.
    """
    status = str(getattr(outcome, "status", "") or "")
    if status not in ("failed", "timeout"):
        return FailureVerdict(
            FailureClass.UNKNOWN,
            FallbackAction.RETRY,
            f"outcome status {status!r} is not a failure",
        )
    reason = str(getattr(outcome, "reason", "") or "")
    output = str(getattr(outcome, "output", "") or "") or reason
    timed_out = status == "timeout" or "timeout" in reason.lower()
    return classify_failure(
        str(getattr(outcome, "run", "") or ""),
        output=output,
        timed_out=timed_out,
    )


__all__ = [
    "CLASS_ACTIONS",
    "FailureClass",
    "FailureVerdict",
    "FallbackAction",
    "classify_failure",
    "classify_outcome",
]
