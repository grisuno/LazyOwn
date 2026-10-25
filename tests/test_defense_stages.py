"""Defense stages: orchestrator-managed runners and YAML stage visibility."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules import orchestrator_config  # noqa: E402
from modules.defense_eval import ENGINE_VERSION  # noqa: E402
from modules.defense_stages import (  # noqa: E402
    STAGE_CLOSEDLOOP,
    STAGE_DEFENSE,
    STAGE_HUNT,
    run_closedloop_tune,
    run_defense_validate,
    run_hunt_verify,
)

RULE = '{"version": 1, "all": [{"field": "http.path", "op": "contains", "value": "/admin"}]}'
TARGET = '{"http": {"path": "/admin/panel", "status": 200}}\n'
CONTROL = '{"http": {"path": "/index", "status": 200}}\n'


def test_new_stages_declared() -> None:
    """The purple stages are declared and default-enabled in the fallback table."""
    for stage in (STAGE_DEFENSE, STAGE_CLOSEDLOOP, STAGE_HUNT):
        assert stage in orchestrator_config.FALLBACK_STAGES
        assert orchestrator_config.FALLBACK_STAGES[stage]["enabled"] is True


def test_yaml_profiles_load(tmp_path: Path) -> None:
    """The shipped YAML stays valid and exposes the purple profile."""
    profiles = orchestrator_config.profiles()
    assert "purple" in profiles
    assert "harness" in profiles


def _set_stage_params(monkeypatch, stage: str, params: dict) -> None:
    monkeypatch.setattr(
        orchestrator_config,
        "stage_params",
        lambda name: params if name == stage else {},
    )


def test_defense_validate_writes_result(tmp_path: Path, monkeypatch) -> None:
    """The stage replays the rule and writes the verdict document."""
    rule_path = tmp_path / "rule.json"
    rule_path.write_text(RULE, encoding="utf-8")
    target = tmp_path / "traffic"
    target.mkdir()
    (target / "attack.jsonl").write_text(TARGET, encoding="utf-8")
    control = tmp_path / "benign.jsonl"
    control.write_text(CONTROL, encoding="utf-8")
    output = tmp_path / "defense_eval.json"
    _set_stage_params(
        monkeypatch,
        STAGE_DEFENSE,
        {
            "rule_path": str(rule_path),
            "target_glob": str(target / "*.jsonl"),
            "control_glob": str(control),
            "output": str(output),
        },
    )
    result = run_defense_validate("t1")
    assert result["verdict"] == "pass"
    assert output.is_file()
    assert json.loads(output.read_text(encoding="utf-8"))["engine"] == ENGINE_VERSION


def test_defense_validate_skips_without_rule(monkeypatch) -> None:
    """No configured rule is a silent skip, never an abort."""
    _set_stage_params(monkeypatch, STAGE_DEFENSE, {})
    assert run_defense_validate("t1") == {}


def test_closedloop_tune_writes_comparison(tmp_path: Path, monkeypatch) -> None:
    """The stage compares both rules and persists suggestions."""
    baseline = tmp_path / "baseline.json"
    candidate = tmp_path / "candidate.json"
    baseline.write_text('{"version": 1, "all": [{"field": "http.path", "op": "contains", "value": "/admin"}, {"field": "http.status", "op": "eq", "value": 200}]}', encoding="utf-8")
    candidate.write_text(RULE, encoding="utf-8")
    target = tmp_path / "traffic"
    target.mkdir()
    (target / "attack.jsonl").write_text(TARGET, encoding="utf-8")
    control = tmp_path / "benign.jsonl"
    control.write_text(CONTROL, encoding="utf-8")
    output = tmp_path / "closedloop.json"
    _set_stage_params(
        monkeypatch,
        STAGE_CLOSEDLOOP,
        {
            "baseline_path": str(baseline),
            "candidate_path": str(candidate),
            "target_glob": str(target / "*.jsonl"),
            "control_glob": str(control),
            "output": str(output),
        },
    )
    result = run_closedloop_tune("t1")
    assert result["verdict"] in ("improved", "regressed", "equivalent", "inconclusive")
    assert output.is_file()


def test_hunt_verify_writes_verification(tmp_path: Path, monkeypatch) -> None:
    """The stage verifies observations and persists stage assessments."""
    design = tmp_path / "hunt_design.json"
    design.write_text(
        json.dumps({"stages": [{"stage_id": "s1", "required_fields": ["user"], "event_kinds": ["auth"]}]}),
        encoding="utf-8",
    )
    evidence = tmp_path / "hunt_evidence.json"
    evidence.write_text(
        json.dumps(
            {
                "scope_covered": True,
                "events": [{"ref": "e1", "fields": {"user": "root"}, "kind": "auth"}],
                "observations": [{"stage_id": "s1", "kind": "observed", "summary": "su root", "evidence_refs": ["e1"]}],
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "hunt_verification.json"
    _set_stage_params(
        monkeypatch,
        STAGE_HUNT,
        {"design": str(design), "evidence": str(evidence), "output": str(output)},
    )
    result = run_hunt_verify("t1")
    assert result["status"] == "completed"
    assert result["chain_proven"] is True
    assert output.is_file()


def test_hunt_verify_skips_without_files(monkeypatch) -> None:
    """Missing design or evidence files skip the stage quietly."""
    _set_stage_params(monkeypatch, STAGE_HUNT, {"design": "/nonexistent", "evidence": "/nonexistent"})
    assert run_hunt_verify("t1") == {}
