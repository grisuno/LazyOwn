"""Health report assembly for the LazyOwn C2 web layer.

Contract: probes always run and their results always drive the aggregated
status and HTTP code, but the detailed ``checks`` (and ``daemon``) payloads
are only included when ``detailed`` is true (loopback caller or
authenticated operator). Building ``checks`` in a dedicated structure
guarantees a remote caller always receives a valid aggregated response
instead of a 500 when details are withheld.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping, Sequence
from typing import Any

logger = logging.getLogger(__name__)


def gather_health(
    probes: Sequence[tuple[str, Callable[[], str]]],
    on_error: Callable[[str, BaseException], None] | None = None,
) -> dict[str, str]:
    """Run every probe and collect per-check statuses.

    Args:
        probes: Sequence of ``(name, probe)`` pairs; ``probe`` returns the
            status string (``"ok"``, ``"stopped"``, ...) or raises.
        on_error: Optional logging hook called with the check name and the
            raised exception.

    Returns:
        Mapping of check name to status string (``"error"`` on failure).
    """
    checks: dict[str, str] = {}
    for name, probe in probes:
        try:
            checks[name] = probe() or "ok"
        except Exception as exc:
            if on_error is not None:
                on_error(name, exc)
            checks[name] = "error"
    return checks


def build_health_report(
    checks: Mapping[str, str],
    detailed: bool = False,
    daemon_status: Any = None,
) -> tuple[dict[str, Any], int]:
    """Assemble the JSON payload and HTTP code for the health endpoint.

    Args:
        checks: Collected per-check statuses.
        detailed: Whether to include the ``checks`` map and ``daemon``
            status in the response body.
        daemon_status: Optional daemon status payload (only embedded when
            ``detailed`` is true).

    Returns:
        Tuple ``(payload, status_code)``; the code is 503 when any check
        differs from ``"ok"``, else 200.
    """
    any_error = any(value != "ok" for value in checks.values())
    report: dict[str, Any] = {"status": "unhealthy" if any_error else "healthy"}
    if detailed:
        report["checks"] = dict(checks)
        if daemon_status is not None:
            report["daemon"] = daemon_status
    return report, (503 if any_error else 200)


__all__ = ["build_health_report", "gather_health"]
