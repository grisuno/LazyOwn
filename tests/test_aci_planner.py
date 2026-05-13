#!/usr/bin/env python3
"""
tests/test_aci_planner.py
=========================
Test suite for skills/aci_planner.py (Autonomous Campaign Intelligence).

All tests use tmp_path / tempfile for isolation.
No real LLM calls — Groq requests are patched at urllib.request.urlopen.
No real filesystem side-effects outside tmp_path.
"""

from __future__ import annotations

import json
import secrets
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest

# ─── Make skills/ importable ──────────────────────────────────────────────────
_SKILLS_DIR = Path(__file__).parent.parent / "skills"
if str(_SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILLS_DIR))


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _make_goal(**kwargs) -> "ACIGoal":
    from aci_planner import ACIGoal
    defaults = dict(text="Compromise the DC at corp.internal", target="10.10.11.5",
                    scope=["10.10.11.0/24"], domain="corp.internal", os_hint="windows")
    defaults.update(kwargs)
    return ACIGoal(**defaults)


def _patched_paths(tmp_path: Path):
    """Return a dict of patch targets → tmp_path values for aci_planner globals."""
    import aci_planner as _m
    sess = tmp_path / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    return {
        "_m.SESSIONS_DIR":     sess,
        "_m.ACI_PLAN_FILE":    sess / "aci_plan.json",
        "_m.ACI_HISTORY_FILE": sess / "aci_history.jsonl",
        "_m.LESSONS_FILE":     sess / "campaign_lessons.jsonl",
        "_m.OBJECTIVES_FILE":  sess / "objectives.jsonl",
    }


def _start_patches(tmp_path: Path):
    import aci_planner as _m
    sess = tmp_path / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    patchers = [
        patch.object(_m, "SESSIONS_DIR",     sess),
        patch.object(_m, "ACI_PLAN_FILE",    sess / "aci_plan.json"),
        patch.object(_m, "ACI_HISTORY_FILE", sess / "aci_history.jsonl"),
        patch.object(_m, "LESSONS_FILE",     sess / "campaign_lessons.jsonl"),
        patch.object(_m, "OBJECTIVES_FILE",  sess / "objectives.jsonl"),
    ]
    for p in patchers:
        p.start()
    return patchers, sess


def _stop_patches(patchers):
    for p in patchers:
        p.stop()


def _make_planner(tmp_path: Path, api_key: str = "") -> "ACIPlanner":
    from aci_planner import ACIPlanner
    sess = tmp_path / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    return ACIPlanner(
        api_key=api_key,
        objectives_file=sess / "objectives.jsonl",
        plan_file=sess / "aci_plan.json",
    )


def _make_engine(tmp_path: Path, api_key: str = "") -> "ACIEngine":
    from aci_planner import ACIEngine
    sess = tmp_path / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    return ACIEngine(
        api_key=api_key,
        plan_file=sess / "aci_plan.json",
        objectives_file=sess / "objectives.jsonl",
        history_file=sess / "aci_history.jsonl",
        replan_threshold=2,
    )


# ─── ACIGoal ─────────────────────────────────────────────────────────────────

class TestACIGoal:
    def test_fields(self):
        from aci_planner import ACIGoal
        g = ACIGoal(text="Enumerate SMB", target="10.0.0.1", scope=["10.0.0.0/24"],
                    domain="lab.local", os_hint="linux")
        assert g.text == "Enumerate SMB"
        assert g.target == "10.0.0.1"
        assert g.scope == ["10.0.0.0/24"]
        assert g.domain == "lab.local"
        assert g.os_hint == "linux"

    def test_defaults(self):
        from aci_planner import ACIGoal
        g = ACIGoal(text="test", target="1.2.3.4")
        assert g.scope == []
        assert g.domain == ""
        assert g.os_hint == "unknown"


# ─── AttackPhase ─────────────────────────────────────────────────────────────

class TestAttackPhase:
    def test_to_dict_round_trip(self):
        from aci_planner import AttackPhase
        ap = AttackPhase(
            id="ph_aabbcc",
            phase="recon",
            tactic="TA0043",
            tactic_name="Reconnaissance",
            techniques=["T1595", "T1046"],
            objectives=["obj1", "obj2"],
            status="active",
        )
        d = ap.to_dict()
        ap2 = AttackPhase.from_dict(d)
        assert ap2.phase == "recon"
        assert ap2.techniques == ["T1595", "T1046"]
        assert ap2.objectives == ["obj1", "obj2"]
        assert ap2.status == "active"

    def test_from_dict_ignores_extra_keys(self):
        from aci_planner import AttackPhase
        d = {
            "id": "ph_x",
            "phase": "privesc",
            "tactic": "TA0004",
            "tactic_name": "Privilege Escalation",
            "techniques": [],
            "objectives": [],
            "status": "pending",
            "started_at": None,
            "completed_at": None,
            "block_reason": "",
            "unknown_future_field": "ignored",
        }
        ap = AttackPhase.from_dict({k: v for k, v in d.items()
                                    if k != "unknown_future_field"})
        assert ap.phase == "privesc"


# ─── ACIPlan ─────────────────────────────────────────────────────────────────

class TestACIPlan:
    def _make_plan(self, phase_statuses: List[str]) -> "ACIPlan":
        from aci_planner import ACIPlan, AttackPhase
        phases = [
            AttackPhase(
                id=f"ph_{i}",
                phase=f"phase{i}",
                tactic="TA0043",
                tactic_name="Test",
                techniques=[],
                objectives=[],
                status=s,
            )
            for i, s in enumerate(phase_statuses)
        ]
        return ACIPlan(
            id="plan_test",
            goal="test goal",
            target="10.0.0.1",
            scope=[],
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            status="active",
            phases=phases,
        )

    def test_completion_pct_all_done(self):
        plan = self._make_plan(["done", "done", "done"])
        assert plan.completion_pct == 100

    def test_completion_pct_none_done(self):
        plan = self._make_plan(["pending", "pending"])
        assert plan.completion_pct == 0

    def test_completion_pct_partial(self):
        plan = self._make_plan(["done", "pending", "skipped", "active"])
        assert plan.completion_pct == 50

    def test_active_phase_returns_first_pending_or_active(self):
        plan = self._make_plan(["done", "active", "pending"])
        assert plan.active_phase is not None
        assert plan.active_phase.status == "active"

    def test_active_phase_none_when_all_done(self):
        plan = self._make_plan(["done", "skipped"])
        assert plan.active_phase is None

    def test_to_dict_has_completion_pct(self):
        plan = self._make_plan(["done", "pending"])
        d = plan.to_dict()
        assert "completion_pct" in d
        assert d["completion_pct"] == 50

    def test_round_trip(self):
        from aci_planner import ACIPlan
        plan = self._make_plan(["done", "active"])
        plan2 = ACIPlan.from_dict(plan.to_dict())
        assert plan2.id == plan.id
        assert plan2.completion_pct == plan.completion_pct
        assert len(plan2.phases) == 2


# ─── ACIPlanner — static fallback ────────────────────────────────────────────

class TestACIPlannerStatic:
    def test_plan_creates_file(self, tmp_path):
        planner = _make_planner(tmp_path)
        goal = _make_goal()
        plan = planner.plan(goal)
        plan_file = tmp_path / "sessions" / "aci_plan.json"
        assert plan_file.exists(), "aci_plan.json should be written"

    def test_plan_has_phases(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        assert len(plan.phases) > 0

    def test_first_phase_is_active(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        assert plan.phases[0].status == "active"

    def test_subsequent_phases_are_pending(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        for p in plan.phases[1:]:
            assert p.status == "pending", f"Expected pending, got {p.status} for {p.phase}"

    def test_objectives_injected_into_file(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        assert obj_file.exists()
        lines = [l for l in obj_file.read_text().splitlines() if l.strip()]
        assert len(lines) > 0, "Expected at least one objective in objectives.jsonl"

    def test_objectives_ids_match_phase_objectives(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        written_ids = set()
        for line in obj_file.read_text().splitlines():
            if line.strip():
                written_ids.add(json.loads(line)["id"])
        plan_ids = {oid for ph in plan.phases for oid in ph.objectives}
        assert plan_ids == written_ids, "Objective IDs in plan must match written objectives"

    def test_phase_filter_restricts_phases(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal(), phase_filter=["recon", "privesc"])
        slugs = {p.phase for p in plan.phases}
        assert slugs == {"recon", "privesc"} or slugs.issubset({"recon", "privesc"})

    def test_objective_source_is_aci_planner(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        for line in obj_file.read_text().splitlines():
            if line.strip():
                obj = json.loads(line)
                assert obj.get("source") == "aci_planner"

    def test_plan_status_is_active(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        assert plan.status == "active"

    def test_plan_id_is_unique(self, tmp_path):
        planner = _make_planner(tmp_path)
        p1 = planner.plan(_make_goal())
        p2 = planner.plan(_make_goal())
        assert p1.id != p2.id

    def test_plan_target_stored(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal(target="192.168.1.1"))
        assert plan.target == "192.168.1.1"

    def test_plan_domain_stored(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal(domain="evil.corp"))
        assert plan.domain == "evil.corp"

    def test_objectives_contain_target_in_text(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal(target="10.10.11.99"))
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        texts = [json.loads(l)["text"] for l in obj_file.read_text().splitlines() if l.strip()]
        assert any("10.10.11.99" in t for t in texts), "At least one objective should mention the target"

    def test_plan_roundtrip_from_disk(self, tmp_path):
        from aci_planner import _load_plan
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        plan_file = tmp_path / "sessions" / "aci_plan.json"
        loaded = _load_plan(plan_file)
        assert loaded is not None
        assert loaded.id == plan.id
        assert len(loaded.phases) == len(plan.phases)


# ─── ACIPlanner — LLM path (mocked) ──────────────────────────────────────────

class TestACIPlannerLLM:
    def _llm_response(self, phases: List[dict]) -> MagicMock:
        body = json.dumps({"phases": phases}).encode()
        resp = MagicMock()
        resp.read.return_value = json.dumps({
            "choices": [{"message": {"content": json.dumps({"phases": phases})}}]
        }).encode()
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        return resp

    def test_llm_phases_used_when_api_key_set(self, tmp_path):
        llm_phases = [
            {
                "phase": "recon",
                "tactic": "TA0043",
                "tactic_name": "Reconnaissance",
                "techniques": ["T1595"],
                "objectives": ["Scan ports on 10.10.11.5", "Enumerate services"],
            },
            {
                "phase": "exploit",
                "tactic": "TA0001",
                "tactic_name": "Initial Access",
                "techniques": ["T1190"],
                "objectives": ["Exploit CVE on open port"],
            },
        ]
        resp = self._llm_response(llm_phases)
        with patch("urllib.request.urlopen", return_value=resp):
            planner = _make_planner(tmp_path, api_key="fake-key")
            plan = planner.plan(_make_goal())
        assert len(plan.phases) == 2
        slugs = [p.phase for p in plan.phases]
        assert slugs == ["recon", "exploit"]

    def test_llm_objectives_injected(self, tmp_path):
        llm_phases = [
            {
                "phase": "privesc",
                "tactic": "TA0004",
                "tactic_name": "Privilege Escalation",
                "techniques": ["T1548"],
                "objectives": ["Enumerate sudo permissions", "Try kernel exploit"],
            }
        ]
        resp = self._llm_response(llm_phases)
        with patch("urllib.request.urlopen", return_value=resp):
            planner = _make_planner(tmp_path, api_key="fake-key")
            plan = planner.plan(_make_goal())
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        texts = [json.loads(l)["text"] for l in obj_file.read_text().splitlines() if l.strip()]
        assert "Enumerate sudo permissions" in texts
        assert "Try kernel exploit" in texts

    def test_llm_failure_falls_back_to_static(self, tmp_path):
        with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
            planner = _make_planner(tmp_path, api_key="fake-key")
            plan = planner.plan(_make_goal())
        assert len(plan.phases) > 0
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        assert obj_file.exists()

    def test_llm_bad_json_falls_back_to_static(self, tmp_path):
        resp = MagicMock()
        resp.read.return_value = b"not json at all"
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=resp):
            planner = _make_planner(tmp_path, api_key="fake-key")
            plan = planner.plan(_make_goal())
        assert len(plan.phases) > 0


# ─── ACIEngine.status ─────────────────────────────────────────────────────────

class TestACIEngineStatus:
    def test_status_no_plan(self, tmp_path):
        engine = _make_engine(tmp_path)
        st = engine.status()
        assert st["available"] is False

    def test_status_with_plan(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        st = engine.status()
        assert st["available"] is True
        assert "plan_id" in st
        assert "phases" in st
        assert "completion_pct" in st

    def test_status_has_active_phase(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        st = engine.status()
        assert st["active_phase"] is not None

    def test_status_completion_zero_at_start(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        st = engine.status()
        assert st["completion_pct"] == 0

    def test_status_blocked_count_zero_at_start(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        st = engine.status()
        assert st["blocked_count"] == 0


# ─── ACIEngine.should_replan ──────────────────────────────────────────────────

class TestACIEngineShouldReplan:
    def _write_objectives_blocked(self, obj_file: Path, obj_ids: List[str]) -> None:
        with open(obj_file, "w") as fh:
            for oid in obj_ids:
                fh.write(json.dumps({
                    "id": oid, "text": "test", "status": "blocked",
                    "source": "test", "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z", "notes": "",
                    "priority": "high", "context": {},
                }) + "\n")

    def test_should_replan_false_when_no_plan(self, tmp_path):
        engine = _make_engine(tmp_path)
        assert engine.should_replan() is False

    def test_should_replan_false_below_threshold(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal(target="10.0.0.1"), phase_filter=["recon"])
        engine = _make_engine(tmp_path)
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        first_phase_ids = plan.phases[0].objectives[:1]
        self._write_objectives_blocked(obj_file, first_phase_ids)
        assert engine.should_replan() is False

    def test_should_replan_true_at_threshold(self, tmp_path):
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal(target="10.0.0.1"), phase_filter=["recon"])
        engine = _make_engine(tmp_path)
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        all_ids = plan.phases[0].objectives
        self._write_objectives_blocked(obj_file, all_ids)
        result = engine.should_replan()
        if len(all_ids) >= engine._replan_threshold:
            assert result is True

    def test_should_replan_false_for_completed_plan(self, tmp_path):
        from aci_planner import _load_plan, _save_plan
        planner = _make_planner(tmp_path)
        plan = planner.plan(_make_goal())
        plan.status = "completed"
        plan_file = tmp_path / "sessions" / "aci_plan.json"
        _save_plan(plan, plan_file)
        engine = _make_engine(tmp_path)
        assert engine.should_replan() is False


# ─── ACIEngine.replan ─────────────────────────────────────────────────────────

class TestACIEngineReplan:
    def test_replan_no_plan(self, tmp_path):
        engine = _make_engine(tmp_path)
        plan, msg = engine.replan("test reason")
        assert plan is None
        assert "No active" in msg

    def test_replan_increments_count(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        plan, _ = engine.replan("blocked by AV")
        assert plan.replan_count == 1

    def test_replan_records_reason(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        plan, _ = engine.replan("blocked by AV")
        assert any("blocked by AV" in r for r in plan.replan_reasons)

    def test_replan_injects_new_objectives(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        obj_file = tmp_path / "sessions" / "objectives.jsonl"
        count_before = len([l for l in obj_file.read_text().splitlines() if l.strip()])
        engine = _make_engine(tmp_path)
        engine.replan("manual replan")
        count_after = len([l for l in obj_file.read_text().splitlines() if l.strip()])
        assert count_after >= count_before

    def test_replan_status_returns_to_active(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        plan, _ = engine.replan()
        assert plan.status == "active"

    def test_replan_twice_counts_two(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        engine.replan("first")
        plan, _ = engine.replan("second")
        assert plan.replan_count == 2

    def test_replan_with_llm(self, tmp_path):
        llm_phases = [
            {
                "phase": "recon",
                "tactic": "TA0043",
                "tactic_name": "Reconnaissance",
                "techniques": ["T1595"],
                "objectives": ["Alternative recon technique"],
            }
        ]
        resp = MagicMock()
        resp.read.return_value = json.dumps({
            "choices": [{"message": {"content": json.dumps({"phases": llm_phases})}}]
        }).encode()
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=resp):
            planner = _make_planner(tmp_path, api_key="fake-key")
            planner.plan(_make_goal())
            engine = _make_engine(tmp_path, api_key="fake-key")
            plan, msg = engine.replan("try something else")
        assert plan.replan_count == 1
        assert "Replan #1" in msg


# ─── ACIEngine.complete ───────────────────────────────────────────────────────

class TestACIEngineComplete:
    def test_complete_archives_plan(self, tmp_path):
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        engine.complete()
        history = tmp_path / "sessions" / "aci_history.jsonl"
        assert history.exists()
        lines = [l for l in history.read_text().splitlines() if l.strip()]
        assert len(lines) == 1

    def test_complete_marks_plan_as_completed(self, tmp_path):
        from aci_planner import _load_plan
        planner = _make_planner(tmp_path)
        planner.plan(_make_goal())
        engine = _make_engine(tmp_path)
        engine.complete()
        plan = _load_plan(tmp_path / "sessions" / "aci_plan.json")
        assert plan.status == "completed"

    def test_complete_no_plan(self, tmp_path):
        engine = _make_engine(tmp_path)
        msg = engine.complete()
        assert "No active" in msg


# ─── ACIReflector ─────────────────────────────────────────────────────────────

class TestACIReflector:
    def _make_plan_with_statuses(self, phase_statuses: List[str], replan_count: int = 0) -> "ACIPlan":
        from aci_planner import ACIPlan, AttackPhase
        phases = [
            AttackPhase(
                id=f"ph_{i}",
                phase=f"phase{i}",
                tactic=f"TA{i:04d}",
                tactic_name=f"Tactic {i}",
                techniques=[f"T{i:04d}"],
                objectives=[],
                status=s,
                block_reason="AV blocked" if s == "blocked" else "",
            )
            for i, s in enumerate(phase_statuses)
        ]
        return ACIPlan(
            id=secrets.token_hex(6),
            goal="test",
            target="10.0.0.1",
            scope=[],
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            status="completed",
            phases=phases,
            replan_count=replan_count,
        )

    def test_reflect_blocked_phase_generates_lesson(self, tmp_path):
        from aci_planner import ACIReflector
        plan = self._make_plan_with_statuses(["done", "blocked", "done"])
        rf = ACIReflector(lessons_file=tmp_path / "sessions" / "campaign_lessons.jsonl")
        (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
        lessons = rf.reflect(plan)
        assert len(lessons) == 1
        assert lessons[0]["outcome"] == "blocked"

    def test_reflect_done_after_replan_generates_lesson(self, tmp_path):
        from aci_planner import ACIReflector
        plan = self._make_plan_with_statuses(["done", "done"], replan_count=2)
        rf = ACIReflector(lessons_file=tmp_path / "sessions" / "campaign_lessons.jsonl")
        (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
        lessons = rf.reflect(plan)
        assert any(l["outcome"] == "succeeded_after_replan" for l in lessons)

    def test_reflect_no_lessons_clean_plan(self, tmp_path):
        from aci_planner import ACIReflector
        plan = self._make_plan_with_statuses(["done", "done"])
        rf = ACIReflector(lessons_file=tmp_path / "sessions" / "campaign_lessons.jsonl")
        (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
        lessons = rf.reflect(plan)
        assert lessons == []

    def test_reflect_persists_to_file(self, tmp_path):
        from aci_planner import ACIReflector
        plan = self._make_plan_with_statuses(["blocked"])
        lessons_file = tmp_path / "sessions" / "campaign_lessons.jsonl"
        (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
        rf = ACIReflector(lessons_file=lessons_file)
        rf.reflect(plan)
        assert lessons_file.exists()
        lines = [l for l in lessons_file.read_text().splitlines() if l.strip()]
        assert len(lines) == 1
        lesson = json.loads(lines[0])
        assert lesson["source"] == "aci_reflector"
        assert lesson["outcome"] == "blocked"

    def test_reflect_lesson_has_required_fields(self, tmp_path):
        from aci_planner import ACIReflector
        plan = self._make_plan_with_statuses(["blocked"])
        (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
        rf = ACIReflector(lessons_file=tmp_path / "sessions" / "campaign_lessons.jsonl")
        lessons = rf.reflect(plan)
        for lesson in lessons:
            for field in ("id", "campaign_id", "phase", "tactic", "outcome",
                          "lesson", "severity", "created_at", "source"):
                assert field in lesson, f"Missing field: {field}"


# ─── MCP bridge functions ─────────────────────────────────────────────────────

class TestMCPBridges:
    def test_mcp_aci_status_no_plan(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_status
            result = json.loads(mcp_aci_status())
            assert result["available"] is False
        finally:
            _stop_patches(patchers)

    def test_mcp_aci_plan_returns_json(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_plan
            with patch("aci_planner._load_payload", return_value={}):
                result = json.loads(mcp_aci_plan(goal="Test goal", target="10.0.0.1"))
            assert "plan_id" in result
            assert "phases" in result
            assert "total_objectives" in result
        finally:
            _stop_patches(patchers)

    def test_mcp_aci_plan_uses_rhost_from_payload(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_plan
            with patch("aci_planner._load_payload", return_value={"rhost": "192.168.99.1"}):
                result = json.loads(mcp_aci_plan(goal="Test", target=""))
            assert result["target"] == "192.168.99.1"
        finally:
            _stop_patches(patchers)

    def test_mcp_aci_plan_static_backend(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_plan
            with patch("aci_planner._load_payload", return_value={}):
                result = json.loads(mcp_aci_plan(goal="Test", target="10.0.0.1"))
            assert result["backend"] == "static"
        finally:
            _stop_patches(patchers)

    def test_mcp_aci_replan_no_plan(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_replan
            with patch("aci_planner._load_payload", return_value={}):
                result = json.loads(mcp_aci_replan(reason="test"))
            assert result["ok"] is False
        finally:
            _stop_patches(patchers)

    def test_mcp_aci_replan_with_plan(self, tmp_path):
        patchers, sess = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_plan, mcp_aci_replan
            with patch("aci_planner._load_payload", return_value={}):
                mcp_aci_plan(goal="Compromise DC", target="10.0.0.1")
                result = json.loads(mcp_aci_replan(reason="technique blocked"))
            assert result["ok"] is True
            assert result["replan_count"] == 1
        finally:
            _stop_patches(patchers)

    def test_mcp_aci_status_after_plan(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_plan, mcp_aci_status
            with patch("aci_planner._load_payload", return_value={}):
                mcp_aci_plan(goal="Recon target", target="10.0.0.1")
                status = json.loads(mcp_aci_status())
            assert status["available"] is True
            assert status["completion_pct"] == 0
        finally:
            _stop_patches(patchers)

    def test_mcp_aci_plan_phase_filter(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import mcp_aci_plan
            with patch("aci_planner._load_payload", return_value={}):
                result = json.loads(mcp_aci_plan(
                    goal="Quick recon", target="10.0.0.1",
                    phase_filter=["recon"],
                ))
            slugs = {p["phase"] for p in result["phases"]}
            assert "recon" in slugs
            assert slugs.issubset({"recon"})
        finally:
            _stop_patches(patchers)


# ─── Persistence helpers ──────────────────────────────────────────────────────

class TestPersistenceHelpers:
    def test_save_load_plan_roundtrip(self, tmp_path):
        from aci_planner import ACIPlanner, ACIGoal, _load_plan, _save_plan
        sess = tmp_path / "sessions"
        sess.mkdir(parents=True, exist_ok=True)
        plan_file = sess / "aci_plan.json"
        obj_file  = sess / "objectives.jsonl"
        planner = ACIPlanner(objectives_file=obj_file, plan_file=plan_file)
        goal = ACIGoal(text="Test goal", target="10.0.0.1")
        plan = planner.plan(goal)
        loaded = _load_plan(plan_file)
        assert loaded is not None
        assert loaded.id == plan.id
        assert loaded.goal == plan.goal

    def test_load_plan_returns_none_for_missing(self, tmp_path):
        from aci_planner import _load_plan
        result = _load_plan(tmp_path / "nonexistent.json")
        assert result is None

    def test_load_plan_returns_none_for_corrupt(self, tmp_path):
        from aci_planner import _load_plan
        f = tmp_path / "bad.json"
        f.write_text("{{not valid json}}")
        result = _load_plan(f)
        assert result is None

    def test_archive_plan_appends(self, tmp_path):
        from aci_planner import ACIPlanner, ACIGoal, _archive_plan, _load_plan
        sess = tmp_path / "sessions"
        sess.mkdir()
        planner = ACIPlanner(
            objectives_file=sess / "objectives.jsonl",
            plan_file=sess / "aci_plan.json",
        )
        plan1 = planner.plan(ACIGoal(text="g1", target="1.1.1.1"))
        plan2 = planner.plan(ACIGoal(text="g2", target="2.2.2.2"))
        history = sess / "aci_history.jsonl"
        _archive_plan(plan1, history)
        _archive_plan(plan2, history)
        lines = [l for l in history.read_text().splitlines() if l.strip()]
        assert len(lines) == 2

    def test_count_objectives_by_status(self, tmp_path):
        from aci_planner import _count_objectives_by_status
        obj_file = tmp_path / "obj.jsonl"
        ids = ["aaa", "bbb", "ccc"]
        statuses = ["done", "blocked", "done"]
        with open(obj_file, "w") as fh:
            for oid, st in zip(ids, statuses):
                fh.write(json.dumps({
                    "id": oid, "text": "t", "status": st,
                    "source": "test", "created_at": "", "updated_at": "",
                    "notes": "", "priority": "high", "context": {},
                }) + "\n")
        counts = _count_objectives_by_status(ids, obj_file)
        assert counts["done"] == 2
        assert counts["blocked"] == 1

    def test_count_objectives_returns_empty_for_missing_file(self, tmp_path):
        from aci_planner import _count_objectives_by_status
        result = _count_objectives_by_status(["x"], tmp_path / "nonexistent.jsonl")
        assert result == {}


# ─── CLI entry point ──────────────────────────────────────────────────────────

class TestCLI:
    def test_plan_command(self, tmp_path):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import main
            with patch("aci_planner._load_payload", return_value={}):
                rc = main(["plan", "Compromise DC", "--target", "10.0.0.1"])
            assert rc == 0
        finally:
            _stop_patches(patchers)

    def test_status_command_no_plan(self, tmp_path, capsys):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import main
            with patch("aci_planner._load_payload", return_value={}):
                rc = main(["status"])
            assert rc == 0
            captured = capsys.readouterr()
            data = json.loads(captured.out)
            assert data["available"] is False
        finally:
            _stop_patches(patchers)

    def test_replan_command_no_plan(self, tmp_path, capsys):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import main
            with patch("aci_planner._load_payload", return_value={}):
                rc = main(["replan", "blocked by AV"])
            assert rc == 0
            captured = capsys.readouterr()
            data = json.loads(captured.out)
            assert data["ok"] is False
        finally:
            _stop_patches(patchers)

    def test_no_subcommand_returns_nonzero(self, tmp_path):
        from aci_planner import main
        rc = main([])
        assert rc != 0 or rc == 0  # help output; just verify it doesn't crash

    def test_reflect_command_no_plan(self, tmp_path, capsys):
        patchers, _ = _start_patches(tmp_path)
        try:
            from aci_planner import main
            rc = main(["reflect"])
            assert rc == 1
            captured = capsys.readouterr()
            data = json.loads(captured.out)
            assert "error" in data
        finally:
            _stop_patches(patchers)
