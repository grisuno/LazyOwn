"""Routing-prior sink: learn from terminal outcomes."""

from __future__ import annotations

from modules.lazy_intel import record_routing_outcome
from modules.outcome_bus import OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Record one routing outcome for cross-task priors.

    Args:
        event: Outcome to learn from.

    Returns:
        True when the record was appended.
    """
    try:
        record_routing_outcome(
            event.task_id or "outcome_bus",
            int(event.intent_id or 0),
            event.command or f"{event.source} {event.title}",
            state="done" if (event.success or event.shell) else "blocked",
            facts=1 if event.kind in ("fact", "emulation", "chain") else 0,
            findings=1 if event.kind == "finding" else 0,
            stack=f"{event.source}:{event.mitre_id}".strip(":"),
        )
    except Exception:
        pass
    try:
        from modules.lazy_ledger import key_from_command as ledger_key_from_command
        from modules.lazy_ledger import record as ledger_record

        if event.command and event.kind in ("shell", "exploit", "chain", "emulation", "ctf_capture"):
            verb, target_text = ledger_key_from_command(event.command, event.host_value).split("|", 1)
            ledger_record(verb, target_text, ok=bool(event.success or event.shell))
    except Exception:
        return False
    return True
