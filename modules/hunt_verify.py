"""Evidence verdict verification for hunting and chain stages.

Verifies that AI observations stand on in-scope, retained evidence
with the required fields present. The verdict taxonomy is deliberately
strict: ``evidence_observed`` means an observation cites in-scope
events whose required fields exist; it never means an exploit or
impact is proven. ``not_observed`` requires confirmed scope coverage
so a narrowed search cannot conclude absence. Dependency gating marks
any attack chain whose predecessor stages lack observed evidence.

Adapted from the ARTEX ``hunting`` verification engine (AGPL-3.0).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

STATUS_COMPLETED = "completed"
STATUS_INSUFFICIENT = "insufficient_data"

VERDICT_OBSERVED = "evidence_observed"
VERDICT_INFERRED = "inferred"
VERDICT_NOT_OBSERVED = "not_observed"
VERDICT_INSUFFICIENT = "insufficient_data"
_VERDICTS = frozenset({VERDICT_OBSERVED, VERDICT_INFERRED, VERDICT_NOT_OBSERVED, VERDICT_INSUFFICIENT})

KIND_OBSERVED = "observed"
KIND_INFERRED = "inferred"
KIND_INSUFFICIENT = "insufficient_data"
_KINDS = frozenset({KIND_OBSERVED, KIND_INFERRED, KIND_INSUFFICIENT})

MAX_STAGES = 8
MAX_OBSERVATIONS = 256
MAX_EVENTS = 8000
MAX_REFS_PER_OBSERVATION = 10
MAX_ALTERNATIVES = 8
MAX_NEXT_STEPS = 8
MAX_SUMMARY_CHARS = 4000

_IMPACT_NOTE = (
    "evidence_observed confirms in-scope activity with the required fields present; "
    "it never proves exploit success or impact by itself"
)


@dataclass
class EventRecord:
    """One retained, normalized evidence event."""

    ref: str
    fields: dict[str, Any] = field(default_factory=dict)
    kind: str = ""
    path: str = ""
    target: str = ""
    known_self: bool = False


@dataclass
class StageSpec:
    """One hunting stage: what happened, what to look for, what depends on it."""

    stage_id: str
    description: str = ""
    required_fields: list[str] = field(default_factory=list)
    event_kinds: list[str] = field(default_factory=list)
    path_contains: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    benign_alternatives: list[str] = field(default_factory=list)


@dataclass
class Observation:
    """One AI observation linked to a stage and evidence refs."""

    stage_id: str
    kind: str
    summary: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)


@dataclass
class StageAssessment:
    """Verified verdict for one stage."""

    stage_id: str
    status: str = VERDICT_INSUFFICIENT
    summary: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    known_self_refs: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    rejected_observations: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "stage_id": self.stage_id,
            "status": self.status,
            "summary": self.summary,
            "evidence_refs": list(self.evidence_refs),
            "known_self_refs": list(self.known_self_refs),
            "missing_fields": list(self.missing_fields),
            "reasons": list(self.reasons),
            "alternatives": list(self.alternatives),
            "next_steps": list(self.next_steps),
            "rejected_observations": self.rejected_observations,
        }


@dataclass
class Verification:
    """Whole-run verdict across stages."""

    status: str = STATUS_INSUFFICIENT
    stages: list[StageAssessment] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def chain_proven(self) -> bool:
        """Return whether every stage has observed evidence."""
        return bool(self.stages) and all(
            assessment.status == VERDICT_OBSERVED for assessment in self.stages
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "status": self.status,
            "stages": [stage.to_dict() for stage in self.stages],
            "warnings": list(self.warnings),
            "chain_proven": self.chain_proven,
        }


def _unique(values: list[str]) -> list[str]:
    """Return the list with empty entries and duplicates removed."""
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        value = str(value or "").strip()
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def field_present(fields: dict[str, Any], field_name: str) -> bool:
    """Return whether one required field exists with a present scalar value.

    Args:
        fields: Normalized event field mapping.
        field_name: Canonical name or exact dotted raw path.

    Returns:
        True when the field exists and holds a present scalar.
    """
    if field_name in fields:
        return _scalar_present(fields.get(field_name))
    value: Any = fields
    for segment in field_name.split("."):
        if not isinstance(value, dict) or segment not in value:
            return False
        value = value[segment]
    return _scalar_present(value)


def _field_present(event: EventRecord, field_name: str) -> bool:
    """Return whether one required field exists with a present scalar value."""
    return field_present(event.fields, field_name)


def _scalar_present(value: Any) -> bool:
    """Return whether one JSON value is a present scalar."""
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (bool, int, float)):
        return True
    if isinstance(value, list):
        return len(value) == 1 and _scalar_present(value[0])
    return False


def _stage_matches(spec: StageSpec, event: EventRecord) -> bool:
    """Return whether one event matches the stage's explicit filters."""
    if spec.event_kinds and not any(kind.lower() == (event.kind or "").lower() for kind in spec.event_kinds):
        return False
    if spec.path_contains and not any(marker in event.path for marker in spec.path_contains):
        return False
    return True


def validate_specs(specs: list[StageSpec]) -> list[str]:
    """Validate stage structure: caps, unique ids and known dependencies.

    Args:
        specs: Stage specifications.

    Returns:
        Human-readable errors; empty means the design is valid.
    """
    errors: list[str] = []
    if not specs:
        errors.append("at least one stage is required")
        return errors
    if len(specs) > MAX_STAGES:
        errors.append(f"at most {MAX_STAGES} stages are allowed")
    ids: set[str] = set()
    for spec in specs:
        if not spec.stage_id.strip():
            errors.append("every stage needs a non-empty id")
        elif spec.stage_id in ids:
            errors.append(f"duplicate stage id: {spec.stage_id!r}")
        ids.add(spec.stage_id)
        if len(spec.required_fields) > MAX_STAGES * 4:
            errors.append(f"stage {spec.stage_id}: too many required fields")
        if len(spec.depends_on) > MAX_STAGES:
            errors.append(f"stage {spec.stage_id}: too many dependencies")
    for spec in specs:
        for dependency in spec.depends_on:
            if dependency not in ids:
                errors.append(f"stage {spec.stage_id}: unknown dependency {dependency!r}")
        if spec.stage_id in spec.depends_on:
            errors.append(f"stage {spec.stage_id}: a stage cannot depend on itself")
    return errors


def verify_stages(
    specs: list[StageSpec],
    observations: list[Observation],
    events: list[EventRecord],
    scope_covered: bool = False,
) -> Verification:
    """Verify AI observations against retained events per stage.

    Args:
        specs: Stage specifications (max :data:`MAX_STAGES`).
        observations: AI observations to verify.
        events: Retained, normalized evidence events.
        scope_covered: True only when the collection provably covered
            the whole requested scope; ``not_observed`` verdicts require
            this.

    Returns:
        A :class:`Verification` with per-stage assessments.

    Raises:
        ValueError: When stage structure or counts exceed the caps.
    """
    errors = validate_specs(specs)
    if errors:
        raise ValueError("; ".join(errors))
    if len(observations) > MAX_OBSERVATIONS:
        raise ValueError(f"too many observations (max {MAX_OBSERVATIONS})")
    if len(events) > MAX_EVENTS:
        raise ValueError(f"too many events (max {MAX_EVENTS})")
    warnings: list[str] = []
    by_ref: dict[str, EventRecord] = {}
    integrity_issue = False
    for event in events:
        if not event.ref.strip():
            integrity_issue = True
            warnings.append("an event without an evidence reference was excluded")
            continue
        if event.ref in by_ref:
            integrity_issue = True
            warnings.append(f"duplicate evidence reference: {event.ref}")
            continue
        by_ref[event.ref] = event
    stage_ids = {spec.stage_id for spec in specs}
    by_stage: dict[str, list[Observation]] = {}
    for observation in observations:
        if observation.stage_id not in stage_ids:
            integrity_issue = True
            warnings.append(f"observation attached to unknown stage: {observation.stage_id}")
            continue
        by_stage.setdefault(observation.stage_id, []).append(observation)
    complete = scope_covered and not integrity_issue
    result = Verification(warnings=warnings)
    for spec in specs:
        assessment = _assess_stage(
            spec,
            by_stage.get(spec.stage_id, []),
            by_ref,
            complete,
            warnings,
        )
        result.stages.append(assessment)
        if assessment.rejected_observations > 0:
            integrity_issue = True
    states = {assessment.stage_id: assessment.status for assessment in result.stages}
    for spec, assessment in zip(specs, result.stages, strict=True):
        for dependency in spec.depends_on:
            if states.get(dependency) != VERDICT_OBSERVED:
                assessment.reasons.append(
                    f"predecessor stage {dependency} lacks observed evidence; the attack chain is unproven"
                )
    result.warnings = _unique([*warnings, _IMPACT_NOTE])
    insufficient = any(assessment.status == VERDICT_INSUFFICIENT for assessment in result.stages)
    result.status = STATUS_INSUFFICIENT if insufficient else STATUS_COMPLETED
    if integrity_issue:
        result.status = STATUS_INSUFFICIENT
    return result


def _assess_stage(
    spec: StageSpec,
    observations: list[Observation],
    events: dict[str, EventRecord],
    complete: bool,
    warnings: list[str],
) -> StageAssessment:
    """Assess one stage against its observations and the event set."""
    assessment = StageAssessment(
        stage_id=spec.stage_id,
        status=VERDICT_INSUFFICIENT,
        alternatives=list(spec.benign_alternatives),
    )
    observed = False
    inferred = False
    seen_keys: set[str] = set()
    for observation in observations:
        key = (
            observation.stage_id,
            observation.kind,
            observation.summary,
            tuple(sorted(observation.evidence_refs)),
        )
        if key in seen_keys:
            continue
        seen_keys.add(key)
        bad = len(observation.summary.strip()) < 1 or len(observation.summary) > MAX_SUMMARY_CHARS
        if len(observation.evidence_refs) > MAX_REFS_PER_OBSERVATION:
            bad = True
        if observation.kind not in _KINDS:
            bad = True
        if observation.kind == KIND_INFERRED and not observation.alternatives:
            bad = True
        if observation.kind != KIND_INSUFFICIENT and not observation.evidence_refs:
            bad = True
        missing: list[str] = []
        accepted: list[str] = []
        for ref in observation.evidence_refs:
            event = events.get(ref)
            if event is None:
                bad = True
                assessment.reasons.append(
                    "observation cites a reference outside the retained evidence"
                )
                continue
            if event.known_self:
                assessment.known_self_refs.append(ref)
                continue
            if not _stage_matches(spec, event):
                bad = True
                assessment.reasons.append("cited event does not match the stage's event kind or path conditions")
                continue
            for field_name in spec.required_fields:
                if not _field_present(event, field_name):
                    missing.append(field_name)
            accepted.append(ref)
        assessment.missing_fields.extend(missing)
        assessment.alternatives.extend(observation.alternatives)
        assessment.next_steps.extend(observation.next_steps)
        if bad:
            assessment.rejected_observations += 1
            continue
        assessment.evidence_refs.extend(accepted)
        if missing or not accepted:
            continue
        observed = observed or observation.kind == KIND_OBSERVED
        inferred = inferred or observation.kind == KIND_INFERRED
    candidates = 0
    available: dict[str, bool] = {}
    for event in events.values():
        if event.known_self:
            continue
        for field_name in spec.required_fields:
            available[field_name] = available.get(field_name, False) or _field_present(event, field_name)
        if _stage_matches(spec, event):
            candidates += 1
    for field_name in spec.required_fields:
        if not available.get(field_name):
            assessment.missing_fields.append(field_name)
    if assessment.rejected_observations > 0:
        assessment.reasons.append("resolve the integrity issues in the cited evidence before concluding")
    if assessment.missing_fields:
        assessment.reasons.append("required fields are absent from cited or collected events")
    if assessment.rejected_observations == 0 and not assessment.missing_fields:
        if observed:
            assessment.status = VERDICT_OBSERVED
            assessment.summary = (
                "in-scope activity with the required fields was observed; exploit success or impact is not confirmed"
            )
        elif inferred:
            assessment.status = VERDICT_INFERRED
            assessment.summary = "an AI hypothesis links real evidence; benign alternatives need review"
        elif complete and candidates == 0 and (spec.event_kinds or spec.path_contains):
            assessment.status = VERDICT_NOT_OBSERVED
            assessment.summary = (
                "the completed scope search observed no events matching this stage; absence of activity is not implied"
            )
        else:
            assessment.reasons.append("no verified observation or sufficient collection scope to conclude")
    if not complete:
        assessment.reasons.append("collection scope or limits leave gaps; absence cannot be confirmed")
    if assessment.known_self_refs:
        assessment.reasons.append("self-recorded verification events are separated from external evidence")
    assessment.evidence_refs = _unique(assessment.evidence_refs)
    assessment.known_self_refs = _unique(assessment.known_self_refs)
    assessment.missing_fields = sorted(set(assessment.missing_fields))
    assessment.reasons = _unique(assessment.reasons)
    assessment.alternatives = _unique(assessment.alternatives)
    assessment.next_steps = _unique(assessment.next_steps)
    if not assessment.summary:
        assessment.summary = "insufficient data or unverified evidence; this stage cannot be judged"
    return assessment


__all__ = [
    "EventRecord",
    "KIND_INFERRED",
    "KIND_INSUFFICIENT",
    "KIND_OBSERVED",
    "Observation",
    "StageAssessment",
    "StageSpec",
    "STATUS_COMPLETED",
    "STATUS_INSUFFICIENT",
    "VERDICT_INFERRED",
    "VERDICT_INSUFFICIENT",
    "VERDICT_NOT_OBSERVED",
    "VERDICT_OBSERVED",
    "Verification",
    "field_present",
    "validate_specs",
    "verify_stages",
]
