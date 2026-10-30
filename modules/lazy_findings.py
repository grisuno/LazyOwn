"""Engagement findings ledger: state machine plus reproducible evidence.

Contract: one JSONL ledger per engagement records finding transitions
(hypothesis -> partial -> confirmed / discarded) with verbatim, re-executable
evidence. A finding can only reach ``confirmed`` when the row carries an
exact ``evidence.command`` plus ``evidence.output`` verbatim (or an
``artifact_ref`` into the evidence plane), enforced fail-closed here so no
caller can stamp an unverified exploit as confirmed. Evidence is redacted
through ``core.hardening.redact_text`` by default; redaction is an operator
decision because sealed credential stores remain the only home for secrets.

Standard library only. Sinks, CLI and the loop engine consume this module;
the validation-to-persistence path stays in one place so every caller shares
one audit surface.
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from core.hardening import redact_text

STATES: tuple[str, ...] = ("hypothesis", "partial", "confirmed", "discarded")

LEVELS: tuple[str, ...] = ("identified", "partial", "confirmed", "critical")

DEFAULT_MIN_EVIDENCE_OUTPUT = 16

DEFAULT_MAX_OUTPUT_CHARS = 4000

DEFAULT_MAX_TITLE_CHARS = 200

FINDINGS_DIRNAME = "findings"

ENGAGEMENT_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,80}$")

TECHNIQUE_PATTERN = re.compile(r"^T\d{4}(?:\.\d{3})?$")

TACTIC_PATTERN = re.compile(r"^TA\d{4}$")

CONFIRMED_REQUIRES_EVIDENCE = (
    "finding 'confirmed' requires reproducible evidence: 'command' plus verbatim "
    "'output' at or above the configured minimum, or 'artifact_ref'"
)

VERDICT_TO_TRANSITION: dict[str, str] = {
    "reproduced": "confirmed",
    "fixed": "discarded",
}


class FindingValidationError(ValueError):
    """A finding row failed fail-closed validation and nothing is persisted."""


@dataclass(frozen=True)
class LedgerLimits:
    """Numeric knobs of one ledger, injected by the caller.

    Attributes:
        min_evidence_output: Minimum verbatim ``evidence.output`` length that
            can support a ``confirmed`` state.
        max_output_chars: Cap applied to stored verbatim output and command.
        max_title_chars: Cap applied to the human title.
        redact_secrets: Mask credential-like material before persistence.
    """

    min_evidence_output: int = DEFAULT_MIN_EVIDENCE_OUTPUT
    max_output_chars: int = DEFAULT_MAX_OUTPUT_CHARS
    max_title_chars: int = DEFAULT_MAX_TITLE_CHARS
    redact_secrets: bool = True

    def clamped(self) -> LedgerLimits:
        """Return a copy with every knob forced into its valid range."""
        return replace(
            self,
            min_evidence_output=max(0, int(self.min_evidence_output)),
            max_output_chars=max(0, int(self.max_output_chars)),
            max_title_chars=max(1, int(self.max_title_chars)),
        )


def engagement_id_valid(value: str) -> bool:
    """Return True when the engagement id is safe as a path segment.

    Args:
        value: Engagement identifier supplied by any caller.

    Returns:
        True for ids carrying no traversal or separator characters.
    """
    return bool(ENGAGEMENT_PATTERN.fullmatch(str(value or "").strip()))


def technique_id_valid(value: str) -> bool:
    """Return True when a MITRE technique or tactic id is well formed.

    Args:
        value: Candidate ATT&CK id.

    Returns:
        True for ``T####``/``T####.###`` techniques and ``TA####`` tactics.
    """
    text = str(value or "").strip()
    return bool(TECHNIQUE_PATTERN.fullmatch(text) or TACTIC_PATTERN.fullmatch(text))


def severity_tier(severity: str) -> tuple[str, str]:
    """Map a severity to a starting state and evidence level.

    High/critical observables start partial until reproduced; lower
    severities stay identified hypotheses until retest decides.

    Args:
        severity: Severity string from the finding event.

    Returns:
        ``(state, level)`` pair from :data:`STATES` / :data:`LEVELS`.
    """
    text = str(severity or "").strip().lower()
    tier = {
        "critical": ("partial", "critical"),
        "high": ("partial", "confirmed"),
        "medium": ("partial", "partial"),
        "warning": ("partial", "partial"),
    }
    return tier.get(text, ("hypothesis", "identified"))


def level_for_state_uplift(level: str, state: str) -> str:
    """Return the evidence level after a state transition.

    Promotion to ``confirmed`` anchors the level at ``confirmed`` or above;
    other transitions keep a well-formed current level.

    Args:
        level: Current evidence level.
        state: New state after the transition.

    Returns:
        The adjusted evidence level.
    """
    if state == "confirmed" and level in ("identified", "partial"):
        return "confirmed"
    return level if level in LEVELS else "partial"


def evidence_reject_reason(
    state: str,
    evidence: Any,
    min_output: int = DEFAULT_MIN_EVIDENCE_OUTPUT,
) -> str:
    """Reason a ``confirmed`` state is rejected, or an empty string.

    Two evidence shapes validate: a ``command`` plus verbatim ``output`` at
    or above the minimum length, or an ``artifact_ref`` mapping with
    ``execution_id``/``name`` pointing at staged raw output.

    Args:
        state: Candidate row state.
        evidence: Evidence payload under validation.
        min_output: Minimum verbatim output length required.

    Returns:
        Rejection reason string, empty when the state is admissible.
    """
    if state != "confirmed":
        return ""
    if not isinstance(evidence, dict) or not evidence:
        return CONFIRMED_REQUIRES_EVIDENCE
    ref = evidence.get("artifact_ref")
    if isinstance(ref, dict) and ref.get("execution_id") and ref.get("name"):
        return ""
    command = evidence.get("command")
    output = evidence.get("output")
    if not isinstance(command, str) or not command.strip():
        return CONFIRMED_REQUIRES_EVIDENCE
    if not isinstance(output, str) or len(output.strip()) < max(0, int(min_output)):
        return CONFIRMED_REQUIRES_EVIDENCE
    return ""


def state_counts(rows: list[dict]) -> dict[str, int]:
    """Count the latest known state per finding reference.

    The ledger is append-only, so the newest transition per ``finding_ref``
    wins; rows are consumed in file order.

    Args:
        rows: Ledger rows in append order.

    Returns:
        Mapping of state name to finding count.
    """
    counts = {state: 0 for state in STATES}
    latest: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        ref = str(row.get("finding_ref", "") or "")
        state = str(row.get("state", "") or "")
        if ref and state in counts:
            latest[ref] = state
    for state in latest.values():
        counts[state] += 1
    return counts


def metadata_level(payload: dict[str, Any]) -> str:
    """Return the recorded evidence level of an event, sane default.

    Args:
        payload: Outcome event dict.

    Returns:
        Level string from :data:`LEVELS`.
    """
    candidate = str(((payload.get("metadata") or {}).get("level", "")) or "")
    return candidate if candidate in LEVELS else "partial"


def row_from_event(payload: dict[str, Any], limits: LedgerLimits | None = None) -> dict[str, Any] | None:
    """Map one outcome event to a ledger row, or None when unmappable.

    Accepted payloads are event dicts with finding-class kinds. Retest
    verdicts arrive as kind ``finding`` with ``metadata.verdict`` and append
    a transition row for the same ``finding_ref``; exploitation classes
    with success and evidence start at ``confirmed`` because the command
    and its verbatim output are already the artifact of record.

    Args:
        payload: Outcome event dict (``OutcomeEvent.to_dict`` shape).
        limits: Ledger limits controlling caps and redaction.

    Returns:
        Normalized row ready for append, or None for out-of-scope events.
    """
    bounds = (limits or LedgerLimits()).clamped()
    if not isinstance(payload, dict):
        return None
    kind = str(payload.get("kind", "") or "")
    metadata = dict(payload.get("metadata") or {})
    verdict = str(metadata.get("verdict", "") or "").strip().lower()
    if kind == "finding":
        if verdict:
            return _row_from_verdict(payload, verdict, bounds)
        row = _base_row(payload, bounds)
        row["state"], row["level"] = severity_tier(str(payload.get("severity", "")))
        row["phase"] = "act"
        row["reason"] = "reported"
        return row
    if kind in ("exploit", "chain", "emulation", "ctf_capture") and bool(payload.get("success")):
        row = _base_row(payload, bounds)
        gate_blocked = str(metadata.get("findings_gate", "") or "") == "blocked"
        if gate_blocked:
            row["state"] = "partial"
            row["level"] = metadata_level(payload)
            row["reason"] = "chain verdict insufficient_data: evidence does not clear the triage floor"
        elif evidence_supported(row["evidence"], bounds.min_evidence_output):
            row["state"] = "confirmed"
            row["level"] = "critical" if bool(payload.get("shell")) else "confirmed"
        else:
            row["state"] = "partial"
            row["level"] = "confirmed" if bool(payload.get("shell")) else "partial"
            row["reason"] = "foothold evidence"
        row["phase"] = "act"
        if metadata.get("reason", ""):
            row["reason"] = str(metadata["reason"])
        return row
    return None


def evidence_supported(evidence: Any, min_output: int) -> bool:
    """Return True when evidence backing allows the ``confirmed`` state.

    Args:
        evidence: Evidence payload (command/output/artifact_ref).

    Returns:
        True for artifact references or verbatim output at/above minimum.
    """
    decision = evidence_reject_reason("confirmed", evidence, min_output)
    return decision == ""


def _row_from_verdict(payload: dict[str, Any], verdict: str, bounds: LedgerLimits) -> dict[str, Any] | None:
    """Map a retest verdict to a transition row with faithful semantics.

    ``reproduced`` promotes the finding to ``confirmed`` only when the
    verdict drew on replay output; ``fixed`` demotes to ``discarded``;
    ``inconclusive`` stays ``partial`` with the blocking reason recorded.

    Args:
        payload: Outcome event dict carrying the retest metadata.
        verdict: Retest verdict string.
        bounds: Ledger limits.

    Returns:
        Transition row or None for unknown verdicts.
    """
    if verdict not in ("reproduced", "fixed", "inconclusive"):
        return None
    row = _base_row(payload, bounds)
    evidence = dict(row.get("evidence") or {})
    remeta = dict(payload.get("metadata") or {})
    if verdict == "reproduced":
        promoted = evidence_supported(evidence, bounds.min_evidence_output)
        if not promoted:
            replay_output = str(remeta.get("evidence_output", "") or "")
            replay_command = str(remeta.get("evidence_command", "") or "")
            if replay_command:
                evidence["command"] = replay_command or str(evidence.get("command", ""))
            if replay_output:
                evidence["output"] = replay_output
            promoted = evidence_supported(evidence, bounds.min_evidence_output)
        row["evidence"] = evidence
        if not promoted:
            row["state"] = "partial"
            row["reason"] = "retest marked reproduced but evidence is not reproducible"
        else:
            row["state"] = "confirmed"
            row["reason"] = "retest reproduced the issue with the stored PoC"
        row["level"] = level_for_state_uplift(metadata_level(payload), row["state"])
    elif verdict == "fixed":
        row["state"] = "discarded"
        row["level"] = metadata_level(payload)
        row["reason"] = "retest found the issue remediated or no longer present"
    else:
        row["state"] = "partial"
        row["level"] = metadata_level(payload)
        row["reason"] = "retest inconclusive: environment or evidence too thin to decide"
    row["phase"] = "act"
    return row


def _base_row(payload: dict[str, Any], bounds: LedgerLimits) -> dict[str, Any]:
    """Build one shared row skeleton from an outcome event.

    Args:
        payload: Outcome event dict.
        bounds: Ledger limits for title/evidence caps.

    Returns:
        Row skeleton with caps applied and a fresh ``recorded_at``.
    """
    metadata = dict(payload.get("metadata") or {})
    finding_ref = str(metadata.get("finding_ref", "") or metadata.get("finding_id", "") or "") or uuid.uuid4().hex
    artifacts = [str(item) for item in (payload.get("artifacts") or []) if item]
    evidence: dict[str, Any] = {
        "command": str(payload.get("command", "") or "")[: bounds.max_output_chars],
        "output": str(payload.get("output", "") or "")[: bounds.max_output_chars],
    }
    if artifacts:
        evidence["artifact_ref"] = {"execution_id": str(payload.get("task_id", "") or ""), "name": artifacts[0]}
    return {
        "id": uuid.uuid4().hex,
        "finding_ref": finding_ref,
        "engagement_id": str(payload.get("task_id", "") or ""),
        "title": str(payload.get("title", "") or "")[: bounds.max_title_chars],
        "state": "hypothesis",
        "level": "identified",
        "phase": "observe",
        "technique_id": str(payload.get("mitre_id", "") or ""),
        "target": str(payload.get("host_value", "") or payload.get("host", "") or ""),
        "severity": str(payload.get("severity", "") or ""),
        "evidence": evidence,
        "confidence": float(payload.get("confidence", 1.0) or 1.0),
        "metadata": metadata,
        "reason": "",
        "recorded_at": _now_iso(),
    }


def discard_row(
    reason: str,
    command: str = "",
    output: str = "",
    technique_id: str = "",
    engagement_id: str = "",
    target: str = "",
) -> dict[str, Any]:
    """Build a discarded-vector row so dead routes are recorded permanently.

    Ledger growth from abandoned hypotheses keeps future loops from
    repeating the same failed approach after a crash or context reset.

    Args:
        reason: Human reason the route was abandoned.
        command: Last command executed on the route, if any.
        output: Output of that command, if any.
        technique_id: ATT&CK id attempted, if any.
        engagement_id: Engagement identifier.
        target: Host the route targeted.

    Returns:
        Normalized discarded row ready for append.
    """
    return normalize_finding(
        {
            "id": uuid.uuid4().hex,
            "finding_ref": uuid.uuid4().hex,
            "engagement_id": engagement_id,
            "title": f"discarded vector: {str(reason)[:160]}",
            "state": "discarded",
            "level": "identified",
            "phase": "orient",
            "technique_id": technique_id,
            "target": target,
            "severity": "low",
            "evidence": {
                "command": str(command)[:DEFAULT_MAX_OUTPUT_CHARS],
                "output": str(output)[:DEFAULT_MAX_OUTPUT_CHARS],
            },
            "confidence": 0.0,
            "metadata": {},
            "reason": str(reason)[:300],
        }
    )


def normalize_finding(row: dict[str, Any], limits: LedgerLimits | None = None) -> dict[str, Any]:
    """Validate and normalize one row without persisting.

    Fail-closed: an invalid state, level, technique id, title or a
    ``confirmed`` state without reproducible evidence raises instead of
    returning a half-valid row. ``recorded_at`` is always assigned fresh
    and never trusted from callers.

    Args:
        row: Candidate row mapping.
        limits: Validation caps; module defaults when omitted.

    Returns:
        The normalized row.

    Raises:
        FindingValidationError: Any contract violation.
    """
    from collections.abc import Mapping

    bounds = (limits or LedgerLimits()).clamped()
    if not isinstance(row, Mapping):
        raise FindingValidationError("finding row must be a mapping")
    title = str(row.get("title", "") or "").strip()
    if not title:
        raise FindingValidationError("finding title is required")
    state = str(row.get("state", "") or "").strip()
    if state not in STATES:
        raise FindingValidationError(f"invalid finding state: {state!r}")
    level = str(row.get("level", "") or "").strip()
    if level not in LEVELS:
        raise FindingValidationError(f"invalid finding level: {level!r}")
    technique = str(row.get("technique_id", "") or "").strip()
    if technique and not technique_id_valid(technique):
        raise FindingValidationError(f"invalid ATT&CK id: {technique!r}")
    evidence = dict(row.get("evidence") or {})
    reject = evidence_reject_reason(state, evidence, bounds.min_evidence_output)
    if reject:
        raise FindingValidationError(reject)
    normalized = dict(row)
    normalized["title"] = title[: bounds.max_title_chars]
    normalized["state"] = state
    normalized["level"] = level_for_state_uplift(level, state)
    normalized["technique_id"] = technique
    normalized["recorded_at"] = _now_iso()
    if not str(normalized.get("id", "") or "").strip():
        normalized["id"] = uuid.uuid4().hex
    if not str(normalized.get("finding_ref", "") or "").strip():
        normalized["finding_ref"] = normalized["id"]
    return normalized


def build_handoff(rows: list[dict], status: str = "", rounds: int = 0) -> dict[str, Any]:
    """Shape the operator handoff from durable ledger rows.

    The handoff is the close-of-loop summary: state counts over the latest
    transitions, the confirmed findings with their reproducible evidence,
    the last discarded vectors (so the next run starts knowing what failed)
    and one explicit decision line for the operator.

    Args:
        rows: Latest ledger rows in append order.
        status: Final loop status.
        rounds: Completed round count.

    Returns:
        Handoff dict with states, confirmed, discarded and decision.
    """
    counts = state_counts(rows)
    latest: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        ref = str(row.get("finding_ref", "") or "")
        if ref:
            latest[ref] = row
    confirmed = [row for row in latest.values() if row.get("state") == "confirmed"]
    discarded = [
        str(row.get("reason", "") or row.get("title", ""))[:160]
        for row in latest.values()
        if row.get("state") == "discarded"
    ][-5:]
    if counts.get("confirmed", 0):
        decision = "confirmed findings present: review evidence and remediate"
    elif status in ("exhausted", "timeout", "failed", "handoff"):
        decision = "route exhausted without confirmed evidence: operator picks the next vector"
    else:
        decision = "engagement ended: review the ledger before re-running"
    return {
        "status": status,
        "rounds": rounds,
        "states": counts,
        "confirmed": [
            {
                "title": str(row.get("title", ""))[:160],
                "technique_id": str(row.get("technique_id", "") or ""),
                "evidence": dict(row.get("evidence") or {}),
            }
            for row in confirmed[-5:]
        ],
        "discarded_vectors": discarded,
        "next_decision": decision,
    }


def _now_iso() -> str:
    """Return a UTC ISO-8601 timestamp with ``Z`` suffix."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class FindingsLedger:
    """Append-only JSONL ledger of finding transitions for one engagement."""

    def __init__(
        self,
        engagement_id: str,
        base_dir: str | os.PathLike[str],
        limits: LedgerLimits | None = None,
        scrub: Callable[[str], str] | None = None,
    ) -> None:
        """Bind the ledger to one engagement path with injected limits.

        Args:
            engagement_id: Engagement identifier (safe path segment).
            base_dir: Root directory holding the ``findings`` folder.
            limits: Validation caps for this ledger.
            scrub: Redaction callable; defaults to ``redact_text``.

        Raises:
            FindingValidationError: Unknown engagement id.
        """
        clean = str(engagement_id or "").strip()
        if not engagement_id_valid(clean):
            raise FindingValidationError(f"invalid engagement id: {clean!r}")
        self.engagement_id = clean
        self.path = Path(base_dir)
        self.limits = (limits or LedgerLimits()).clamped()
        self._scrub = scrub or redact_text

    @property
    def file_path(self) -> Path:
        """Return the ledger JSONL file path."""
        return self.path / FINDINGS_DIRNAME / f"{self.engagement_id}.jsonl"

    def normalize(self, row: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize one row before persistence.

        Behaves like :func:`normalize_finding`; additionally applies the
        redaction scrub to title and string evidence so the store never
        holds masked-off secrets, then caps command/output lengths.

        Args:
            row: Candidate row mapping.

        Returns:
            The normalized row ready to append.

        Raises:
            FindingValidationError: Any contract violation.
        """
        record = dict(normalize_finding(row, self.limits))
        if self.limits.redact_secrets:
            record["title"] = self._scrub(str(record["title"]))
            record["evidence"] = {
                key: (self._scrub(str(value)) if isinstance(value, (str, bytes)) else value)
                for key, value in dict(record.get("evidence") or {}).items()
            }
        evidence = dict(record.get("evidence") or {})
        record["evidence"] = {
            "command": str(evidence.get("command", "") or "")[: self.limits.max_output_chars],
            "output": str(evidence.get("output", "") or "")[: self.limits.max_output_chars],
        }
        ref = evidence.get("artifact_ref")
        if isinstance(ref, dict):
            record["evidence"]["artifact_ref"] = ref
        return record

    def append(self, row: dict[str, Any]) -> dict[str, Any]:
        """Append one normalized row atomically and return it.

        A single ``O_APPEND`` write per row keeps concurrent producers from
        interleaving lines; nothing is stored when normalization fails.

        Args:
            row: Candidate row mapping.

        Returns:
            The persisted row.

        Raises:
            FindingValidationError: Invalid row; nothing is written.
        """
        record = self.normalize(row)
        path = self.file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
        handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            payload = json.dumps(record, ensure_ascii=False).encode("utf-8") + b"\n"
            os.write(handle, payload)
        finally:
            os.close(handle)
        return record

    def read(self, cursor: int = 0, limit: int | None = None) -> dict[str, Any]:
        """Read rows paginated by line index.

        Corrupt lines are skipped without failing the read; the ledger is
        best-effort outbound and strict inbound.

        Args:
            cursor: Zero-based index of the first row to return.
            limit: Maximum rows to return, None for all remaining.

        Returns:
            Mapping with ``findings``/``next_cursor``/``done``/``total``.
        """
        rows = self.rows()
        total = len(rows)
        start = max(0, int(cursor))
        stop = total if limit is None else min(total, start + max(0, int(limit)))
        return {
            "findings": rows[start:stop],
            "next_cursor": stop,
            "done": stop >= total,
            "total": total,
        }

    def rows(self) -> list[dict[str, Any]]:
        """Return every well-formed row in append order.

        Returns:
            Parsed rows; unreadable ledger content yields an empty list.
        """
        path = self.file_path
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return []
        rows: list[dict[str, Any]] = []
        for line in raw.splitlines():
            candidate = line.strip()
            if not candidate or not candidate.startswith("{"):
                continue
            try:
                parsed = json.loads(candidate)
            except ValueError:
                continue
            if isinstance(parsed, dict):
                rows.append(parsed)
        return rows

    def history(self, finding_ref: str) -> list[dict[str, Any]]:
        """Return every transition recorded for one finding reference.

        Args:
            finding_ref: Leaf identifier of the finding series.

        Returns:
            Rows for that reference in append order.
        """
        wanted = str(finding_ref or "")
        return [row for row in self.rows() if str(row.get("finding_ref", "")) == wanted]

    def latest_state(self, finding_ref: str) -> str:
        """Return the newest known state of one finding reference.

        Args:
            finding_ref: Leaf identifier of the finding series.

        Returns:
            State string, empty when the reference is unknown.
        """
        rows = self.history(finding_ref)
        return str(rows[-1].get("state", "")) if rows else ""


__all__ = [
    "CONFIRMED_REQUIRES_EVIDENCE",
    "DEFAULT_MAX_OUTPUT_CHARS",
    "DEFAULT_MAX_TITLE_CHARS",
    "DEFAULT_MIN_EVIDENCE_OUTPUT",
    "ENGAGEMENT_PATTERN",
    "FINDINGS_DIRNAME",
    "LEVELS",
    "STATES",
    "TACTIC_PATTERN",
    "TECHNIQUE_PATTERN",
    "FindingsLedger",
    "FindingValidationError",
    "LedgerLimits",
    "VERDICT_TO_TRANSITION",
    "build_handoff",
    "discard_row",
    "engagement_id_valid",
    "evidence_reject_reason",
    "evidence_supported",
    "level_for_state_uplift",
    "normalize_finding",
    "row_from_event",
    "severity_tier",
    "state_counts",
    "technique_id_valid",
]
