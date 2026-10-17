"""Kill-chain sink: advance the unified phase from proven outcomes."""

from __future__ import annotations

from modules.killchain import KillChain
from modules.outcome_bus import OutcomeEvent

_PROVEN_KINDS = frozenset({"exploit", "emulation", "chain"})


def apply(event: OutcomeEvent) -> bool:
    """Advance the kill-chain phase only when the outcome proves progress.

    A failed exploit, a dry-run emulation and a plain finding must never
    mark hosts as ``EXPLOITED``. Shell access is the strongest signal;
    otherwise an explicitly successful exploit/emulation/chain advances
    the phase. Report events only advance the reporting phase.

    Args:
        event: Outcome to classify.

    Returns:
        True when the phase was advanced or already ahead.
    """
    dry_run = bool(event.metadata.get("dry_run"))
    advance_host = event.host_value or ""
    if event.kind == "report":
        target = "report"
        advance_host = ""
    elif event.shell:
        target = "exploit"
    elif event.success and not dry_run and event.kind in _PROVEN_KINDS:
        target = "exploit"
    else:
        return False
    try:
        KillChain().advance_phase(target, host=advance_host)
    except Exception:
        return False
    return True
