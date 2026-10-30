"""Findings sink: append engagement finding transitions to the ledger.

One adapter from the outcome bus to ``modules.lazy_findings``. Every
finding-class outcome lands in the per-engagement JSONL ledger with its
evidence-backed state machine row; exploitation outcomes that carry a
command and verbatim output become ``confirmed`` rows because the artifact
of record is reproducible by construction.
"""

from __future__ import annotations

from pathlib import Path

from modules import lazy_findings
from modules.outcome_bus import OutcomeEvent

_BASE_DIR = Path(__file__).resolve().parent.parent.parent / "sessions"

LEDGER_MARKER = "findings_ledger"


def limits_for() -> lazy_findings.LedgerLimits:
    """Return the ledger limits resolved from operator configuration.

    Returns:
        LedgerLimits built from ``orchestrator_config.findings_config``.
    """
    try:
        from modules.orchestrator_config import findings_config

        settings = findings_config() or {}
    except Exception:
        settings = {}
    return lazy_findings.LedgerLimits(
        min_evidence_output=int(settings.get("min_evidence_output", 16) or 16),
        max_output_chars=int(settings.get("max_output_chars", 4000) or 4000),
        max_title_chars=int(settings.get("max_title_chars", 200) or 200),
        redact_secrets=bool(settings.get("redact_secrets", True)),
    )


def apply(event: OutcomeEvent) -> bool:
    """Append one ledger row for a finding-class outcome.

    Findings rows persist verbatim flow evidence; validation is fail
    closed, including the reproducibility gate for ``confirmed``. Logged
    rejections never raise out of a sink.

    Args:
        event: Outcome to translate into a ledger row.

    Returns:
        True when a row was appended or the event is out of scope; False
        when the row failed validation.
    """
    row = lazy_findings.row_from_event(event.to_dict(), limits_for())
    if row is None:
        return False
    engagement = str(row.get("engagement_id", "") or event.task_id or event.host_value or "")
    if not lazy_findings.engagement_id_valid(engagement):
        engagement = "default"
        row["engagement_id"] = engagement
    try:
        return bool(ledger_for(engagement).append(row))
    except Exception as exc:
        import logging

        logging.getLogger("sinks.findings").debug("findings sink rejected event: %s", exc)
        return False


def ledger_for(engagement_id: str) -> lazy_findings.FindingsLedger:
    """Return one ledger bound to the sessions findings directory.

    Args:
        engagement_id: Engagement/task id that owns the ledger.

    Returns:
        FindingsLedger for that engagement.
    """
    return lazy_findings.FindingsLedger(
        engagement_id,
        _BASE_DIR,
        limits_for(),
    )


def handoff(engagement_id: str, status: str = "", rounds: int = 0) -> dict:
    """Build the operator handoff from the durable ledger.

    Args:
        engagement_id: Engagement/task bound to the ledger.
        status: Final loop status.
        rounds: Completed rounds.

    Returns:
        Handoff dict (states, confirmed evidence, discarded, decision).
    """
    try:
        ledger = ledger_for(engagement_id)
        rows = ledger.rows()
    except Exception:
        rows = []
    return lazy_findings.build_handoff(rows, status=status, rounds=rounds)


def ingest_discarded(
    engagement_id: str,
    entries: list[dict],
) -> int:
    """Record discarded vector rows for one engagement.

    Args:
        engagement_id: Engagement/task bound to the ledger.
        entries: Discarded-route dicts from the progress ledger.

    Returns:
        Number of rows persisted.
    """
    written = 0
    try:
        ledger = ledger_for(engagement_id)
    except Exception:
        return 0
    for entry in entries:
        try:
            row = lazy_findings.discard_row(
                str(entry.get("reason", "")),
                command=str(entry.get("command", "")),
                output=str(entry.get("output", "")),
                technique_id=str(entry.get("technique_id", "")),
                engagement_id=str(engagement_id),
                target=str(entry.get("target", "")),
            )
            ledger.append(row)
            written += 1
        except Exception:
            continue
    return written


__all__ = ["LEDGER_MARKER", "apply", "handoff", "ingest_discarded", "ledger_for", "limits_for"]
