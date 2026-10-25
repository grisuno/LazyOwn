"""Hunt verification: verdict taxonomy, scope gate and dependency gating."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules.hunt_verify import (  # noqa: E402
    EventRecord,
    Observation,
    StageSpec,
    field_present,
    validate_specs,
    verify_stages,
)

SPECS = [
    StageSpec(stage_id="s1", required_fields=["user"], event_kinds=["auth"]),
    StageSpec(stage_id="s2", required_fields=["path"], path_contains=["/admin"], depends_on=["s1"]),
]


def _event(ref: str, fields: dict, kind: str = "auth", path: str = "") -> EventRecord:
    return EventRecord(ref=ref, fields=fields, kind=kind, path=path)


def test_observed_verdict_requires_fields() -> None:
    """An observed citation with required fields is evidence_observed."""
    events = [_event("e1", {"user": "root"}, kind="auth")]
    observations = [Observation(stage_id="s1", kind="observed", summary="su root", evidence_refs=["e1"])]
    result = verify_stages([SPECS[0]], observations, events, scope_covered=True)
    assert result.stages[0].status == "evidence_observed"
    assert result.status == "completed"
    assert result.chain_proven


def test_missing_fields_block_observed() -> None:
    """A required field absent from events blocks the observed verdict."""
    events = [_event("e1", {"user": ""}, kind="auth")]
    observations = [Observation(stage_id="s1", kind="observed", summary="su", evidence_refs=["e1"])]
    result = verify_stages([SPECS[0]], observations, events, scope_covered=True)
    assert result.stages[0].status == "insufficient_data"
    assert "user" in result.stages[0].missing_fields


def test_out_of_scope_ref_rejected() -> None:
    """Citing a reference outside the retained evidence rejects it."""
    observations = [Observation(stage_id="s1", kind="observed", summary="x", evidence_refs=["ghost"])]
    result = verify_stages([SPECS[0]], observations, [], scope_covered=True)
    assert result.stages[0].rejected_observations == 1
    assert result.stages[0].status == "insufficient_data"


def test_not_observed_requires_scope_covered() -> None:
    """Absence verdicts need confirmed coverage of the whole scope."""
    events = [_event("e1", {"user": "x"}, kind="web", path="/index")]
    observations = []
    result = verify_stages([SPECS[0]], observations, events, scope_covered=True)
    assert result.stages[0].status == "not_observed"
    result = verify_stages([SPECS[0]], observations, events, scope_covered=False)
    assert result.stages[0].status == "insufficient_data"


def test_stage_filters_exclude_events() -> None:
    """Events not matching the stage kind or path are not candidates."""
    events = [_event("e1", {"user": "x"}, kind="web", path="/index")]
    observations = [Observation(stage_id="s1", kind="observed", summary="x", evidence_refs=["e1"])]
    result = verify_stages([SPECS[0]], observations, events, scope_covered=True)
    assert result.stages[0].rejected_observations == 1


def test_inferred_requires_alternatives() -> None:
    """An inferred observation without benign alternatives is rejected."""
    events = [_event("e1", {"user": "x"}, kind="auth")]
    observations = [Observation(stage_id="s1", kind="inferred", summary="x", evidence_refs=["e1"], alternatives=[])]
    result = verify_stages([SPECS[0]], observations, events, scope_covered=True)
    assert result.stages[0].rejected_observations == 1
    observations = [
        Observation(stage_id="s1", kind="inferred", summary="x", evidence_refs=["e1"], alternatives=["admin login"])
    ]
    result = verify_stages([SPECS[0]], observations, events, scope_covered=True)
    assert result.stages[0].status == "inferred"


def test_dependency_gating_notes_unproven_chain() -> None:
    """A stage whose predecessor lacks observed evidence stays unproven."""
    events = [_event("e1", {"path": "/admin/x"}, kind="web", path="/admin/x")]
    observations = [Observation(stage_id="s2", kind="observed", summary="x", evidence_refs=["e1"])]
    result = verify_stages(SPECS, observations, events, scope_covered=True)
    s2 = [stage for stage in result.stages if stage.stage_id == "s2"][0]
    assert "attack chain is unproven" in " ".join(s2.reasons)


def test_known_self_refs_separated() -> None:
    """Self-recorded verification events are separated from evidence."""
    events = [_event("e1", {"user": "root"}, kind="auth"), EventRecord(ref="e2", fields={"user": "root"}, kind="auth", known_self=True)]
    observations = [Observation(stage_id="s1", kind="observed", summary="x", evidence_refs=["e1", "e2"])]
    result = verify_stages([SPECS[0]], observations, events, scope_covered=True)
    assert result.stages[0].known_self_refs == ["e2"]
    assert result.stages[0].evidence_refs == ["e1"]


def test_validate_specs_checks_dependencies() -> None:
    """Unknown or self dependencies are reported."""
    assert validate_specs([StageSpec(stage_id="a"), StageSpec(stage_id="b", depends_on=["a"])]) == []
    errors = validate_specs([StageSpec(stage_id="a", depends_on=["ghost"])])
    assert any("unknown dependency" in error for error in errors)
    errors = validate_specs([StageSpec(stage_id="a", depends_on=["a"])])
    assert any("cannot depend on itself" in error for error in errors)


def test_caps_enforced() -> None:
    """Count caps raise ValueError instead of silently truncating."""
    with pytest.raises(ValueError):
        verify_stages([SPECS[0]], [Observation(stage_id="s1", kind="observed", summary="x")] * 300, [], True)
    with pytest.raises(ValueError):
        verify_stages(SPECS, [], [_event(f"e{i}", {}) for i in range(9000)], True)


def test_field_present_helper() -> None:
    """Field presence handles dotted paths and empty scalars."""
    assert field_present({"a": {"b": "x"}}, "a.b")
    assert not field_present({"a": {"b": "  "}}, "a.b")
    assert not field_present({"a": 1}, "a.b")
