"""Orchestrator stage runners for defense validation and hunt verification.

Each runner is one pipeline stage managed by
:mod:`modules.orchestrator_config` (toggles, params, profiles) and
executed by the autonomous loop on terminal status. File-driven: stage
params in ``config/orchestrator.yaml`` or ``payload.json`` declare the
rule, dataset and output paths, with ``{task}`` replaced by the task id.
A missing configuration never aborts the loop; the stage records a skip
in the activity log instead.
"""

from __future__ import annotations

import glob as _glob
import json
import logging
import os
from pathlib import Path
from typing import Any

log = logging.getLogger("defense_stages")

STAGE_DEFENSE = "defense_validate"
STAGE_CLOSEDLOOP = "closedloop_tune"
STAGE_HUNT = "hunt_verify"


def _activity(task_id: str) -> Any:
    """Return the task activity log, or a no-op stub."""
    try:
        from modules.activity_log import ActivityLog

        return ActivityLog(task_id)
    except Exception:
        class _Stub:
            def emit(self, *args: Any, **kwargs: Any) -> None:
                """Swallow emissions when no activity log exists."""

        return _Stub()


def _params(stage: str) -> dict[str, Any]:
    """Return one stage's resolved parameters."""
    try:
        from modules.orchestrator_config import stage_params

        return stage_params(stage)
    except Exception:
        return {}


def _render(value: str, task_id: str) -> str:
    """Render the ``{task}`` placeholder in one path template."""
    return str(value or "").replace("{task}", str(task_id or ""))


def _read_text(path: str) -> str:
    """Return one file's text or an empty string when absent."""
    if not path or not os.path.isfile(path):
        return ""
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _load_dataset(stage: str, key: str, task_id: str) -> str:
    """Load one dataset by glob or single path from stage params."""
    template = _render(str(_params(stage).get(key, "")), task_id)
    if not template:
        return ""
    if os.path.isfile(template):
        return _read_text(template)
    chunks: list[str] = []
    for path in sorted(_glob.glob(template)):
        text = _read_text(path)
        if text.strip():
            chunks.append(text)
    return "\n".join(chunks)


def run_defense_validate(task_id: str) -> dict[str, Any]:
    """Replay the configured detection rule over attack and control logs.

    Args:
        task_id: Active loop task id (``{task}`` in paths).

    Returns:
        The persisted result mapping (empty when nothing configured).
    """
    params = _params(STAGE_DEFENSE)
    rule_path = _render(str(params.get("rule_path", "")), task_id)
    rule_text = _read_text(rule_path)
    if not rule_text:
        _activity(task_id).emit("defense_validate", "skip", "no rule_path configured")
        return {}
    target_logs = _load_dataset(STAGE_DEFENSE, "target_glob", task_id)
    control_logs = _load_dataset(STAGE_DEFENSE, "control_glob", task_id)
    try:
        from modules.defense_eval import evaluate_rule

        result = evaluate_rule(rule_text, target_logs, control_logs)
    except Exception as exc:
        _activity(task_id).emit("defense_validate", "error", str(exc)[:200])
        return {}
    output_path = _render(str(params.get("output", f"sessions/{task_id}/defense_eval.json")), task_id)
    written = _write_json(output_path, result.to_dict())
    _activity(task_id).emit(
        "defense_validate",
        "done",
        f"verdict={result.verdict} target={result.target.matched}/{result.target.total} "
        f"control={result.control.matched}/{result.control.total} out={written}",
    )
    return result.to_dict()


def run_closedloop_tune(task_id: str) -> dict[str, Any]:
    """Compare baseline vs candidate detection rules with suggestions.

    Args:
        task_id: Active loop task id (``{task}`` in paths).

    Returns:
        The persisted comparison mapping (empty when not configured).
    """
    params = _params(STAGE_CLOSEDLOOP)
    baseline = _read_text(_render(str(params.get("baseline_path", "")), task_id))
    candidate = _read_text(_render(str(params.get("candidate_path", "")), task_id))
    if not baseline or not candidate:
        _activity(task_id).emit("closedloop_tune", "skip", "baseline_path or candidate_path not configured")
        return {}
    target_logs = _load_dataset(STAGE_CLOSEDLOOP, "target_glob", task_id)
    control_logs = _load_dataset(STAGE_CLOSEDLOOP, "control_glob", task_id)
    try:
        from modules.closedloop import compare_rules

        comparison = compare_rules(baseline, candidate, target_logs, control_logs)
    except Exception as exc:
        _activity(task_id).emit("closedloop_tune", "error", str(exc)[:200])
        return {}
    output_path = _render(str(params.get("output", f"sessions/{task_id}/closedloop.json")), task_id)
    written = _write_json(output_path, comparison.to_dict())
    _activity(task_id).emit(
        "closedloop_tune",
        "done",
        f"verdict={comparison.verdict} suggestions={len(comparison.suggestions)} out={written}",
    )
    return comparison.to_dict()


def run_hunt_verify(task_id: str) -> dict[str, Any]:
    """Verify hunting observations against retained evidence per stage.

    Args:
        task_id: Active loop task id (``{task}`` in paths).

    Returns:
        The persisted verification mapping (empty when not configured).
    """
    params = _params(STAGE_HUNT)
    design_path = _render(str(params.get("design", "")), task_id)
    evidence_path = _render(str(params.get("evidence", "")), task_id)
    design_text = _read_text(design_path)
    evidence_text = _read_text(evidence_path)
    if not design_text or not evidence_text:
        _activity(task_id).emit("hunt_verify", "skip", "hunt design or evidence file missing")
        return {}
    try:
        from modules.hunt_verify import (
            EventRecord,
            Observation,
            StageSpec,
            verify_stages,
        )

        design = json.loads(design_text)
        evidence = json.loads(evidence_text)
        specs = [
            StageSpec(
                stage_id=str(item.get("stage_id", "") or ""),
                description=str(item.get("description", "") or ""),
                required_fields=[str(value) for value in item.get("required_fields", []) or []],
                event_kinds=[str(value) for value in item.get("event_kinds", []) or []],
                path_contains=[str(value) for value in item.get("path_contains", []) or []],
                depends_on=[str(value) for value in item.get("depends_on", []) or []],
                benign_alternatives=[str(value) for value in item.get("benign_alternatives", []) or []],
            )
            for item in (design.get("stages") or [])
            if isinstance(item, dict)
        ]
        observations = [
            Observation(
                stage_id=str(item.get("stage_id", "") or ""),
                kind=str(item.get("kind", "") or ""),
                summary=str(item.get("summary", "") or ""),
                evidence_refs=[str(value) for value in item.get("evidence_refs", []) or []],
                alternatives=[str(value) for value in item.get("alternatives", []) or []],
                next_steps=[str(value) for value in item.get("next_steps", []) or []],
            )
            for item in (evidence.get("observations") or [])
            if isinstance(item, dict)
        ]
        events = [
            EventRecord(
                ref=str(item.get("ref", "") or ""),
                fields=dict(item.get("fields") or {}),
                kind=str(item.get("kind", "") or ""),
                path=str(item.get("path", "") or ""),
                target=str(item.get("target", "") or ""),
                known_self=bool(item.get("known_self", False)),
            )
            for item in (evidence.get("events") or [])
            if isinstance(item, dict)
        ]
        verification = verify_stages(specs, observations, events, bool(evidence.get("scope_covered", False)))
    except Exception as exc:
        _activity(task_id).emit("hunt_verify", "error", str(exc)[:200])
        return {}
    output_path = _render(str(params.get("output", f"sessions/{task_id}/hunt_verification.json")), task_id)
    written = _write_json(output_path, verification.to_dict())
    _activity(task_id).emit(
        "hunt_verify",
        "done",
        f"status={verification.status} stages={len(verification.stages)} "
        f"chain_proven={verification.chain_proven} out={written}",
    )
    return verification.to_dict()


def _write_json(path: str, data: dict[str, Any]) -> str:
    """Persist one JSON document, returning the path or empty on failure."""
    try:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return str(target)
    except OSError as exc:
        log.warning("defense stage output failed: %s", exc)
        return ""


__all__ = [
    "STAGE_CLOSEDLOOP",
    "STAGE_DEFENSE",
    "STAGE_HUNT",
    "run_closedloop_tune",
    "run_defense_validate",
    "run_hunt_verify",
]
