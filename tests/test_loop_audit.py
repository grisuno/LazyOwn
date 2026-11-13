"""Loop audit trail: timeline events, step context and rendering."""

from __future__ import annotations

import json

import pytest


@pytest.fixture()
def audit_dir(tmp_path, monkeypatch):
    """Point every audit path at a sandboxed directory."""
    from modules import loop_audit

    monkeypatch.setattr(loop_audit, "AUDIT_DIR", tmp_path)
    monkeypatch.setattr(loop_audit, "SESSIONS_DIR", tmp_path)
    return tmp_path


def test_record_appends_events(audit_dir):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9001", path=audit_dir / "audit_t9001.jsonl")
    audit.run_start(goal="own it", target="10.0.0.5", rounds=3, workers=2)
    event = audit.record("custom", note="x")
    audit.run_end(status="exhausted", rounds=3)
    rows = [json.loads(line) for line in (audit_dir / "audit_t9001.jsonl").read_text().splitlines()]
    assert rows[0]["kind"] == "run_start"
    assert rows[0]["goal"] == "own it"
    assert event["kind"] == "custom"
    assert rows[-1]["kind"] == "run_end"
    assert rows[-1]["status"] == "exhausted"


def test_record_command_carries_step_context(audit_dir):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9002", path=audit_dir / "audit_t9002.jsonl")
    with loop_audit.step_context(
        task_id="t9002",
        worker="w1",
        intent=7,
        judge_action="allow",
        judge_source="llm_judge",
        judge_reason="safe probe",
        detection_prob=0.12,
        step="probe smb",
    ):
        audit.record_command("nmap -p 445 10.0.0.5", "22/tcp open", 3.5)
    rows = [json.loads(line) for line in (audit_dir / "audit_t9002.jsonl").read_text().splitlines()]
    event = rows[-1]
    assert event["kind"] == "command"
    assert event["command"] == "nmap -p 445 10.0.0.5"
    assert event["module"] == "nmap"
    assert event["ok"] is True
    assert event["worker"] == "w1"
    assert event["intent"] == 7
    assert event["judge_action"] == "allow"
    assert event["judge_source"] == "llm_judge"
    assert event["judge_reason"] == "safe probe"
    assert event["detection_prob"] == 0.12
    assert event["step"] == "probe smb"


def test_record_command_detects_failure(audit_dir):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9003", path=audit_dir / "audit_t9003.jsonl")
    audit.record_command("curl http://down", "execution failed: connection refused", 1.0)
    rows = [json.loads(line) for line in (audit_dir / "audit_t9003.jsonl").read_text().splitlines()]
    assert rows[-1]["ok"] is False


def test_output_tail_bounded_and_ansi_stripped(audit_dir):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9004", path=audit_dir / "audit_t9004.jsonl")
    noise = "\x1b[31m" + "x" * 5000
    audit.record_command("long out", noise, 0.1)
    rows = [json.loads(line) for line in (audit_dir / "audit_t9004.jsonl").read_text().splitlines()]
    tail = rows[-1]["output_tail"]
    assert len(tail) <= loop_audit.AUDIT_OUTPUT_TAIL_LIMIT
    assert "\x1b" not in tail


def test_blocked_events(audit_dir):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9005", path=audit_dir / "audit_t9005.jsonl")
    audit.blocked("guard", "forbidden", command="rm -rf /", worker="w1", intent=3)
    rows = [json.loads(line) for line in (audit_dir / "audit_t9005.jsonl").read_text().splitlines()]
    assert rows[-1]["kind"] == "blocked"
    assert rows[-1]["source"] == "guard"


def test_registry_start_and_stop(audit_dir):
    from modules import loop_audit

    handle = loop_audit.start("t9006")
    assert loop_audit.audit_for("t9006") is handle
    loop_audit.stop("t9006")
    assert loop_audit.audit_for("t9006") is None
    assert loop_audit.audit_for("") is None


def test_timeline_merges_guard_and_activity(audit_dir, monkeypatch):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9007", path=audit_dir / "audit_t9007.jsonl")
    audit.run_start(goal="g", target="t", rounds=1, workers=1)
    audit.record_command("nmap t", "ok", 1.0)
    base = [json.loads(line) for line in (audit_dir / "audit_t9007.jsonl").read_text().splitlines()][0]["ts"]
    (audit_dir / "guard_audit_t9007.jsonl").write_text(
        json.dumps({"ts": base + 1.0, "tool": "Bash", "action": "deny", "reason": "rule", "command": "rm -rf /"}) + "\n"
    )
    (audit_dir / "activity_t9007.jsonl").write_text(
        json.dumps({"ts": base + 2.0, "worker": "planner", "kind": "engine", "text": "digest"}) + "\n"
        + json.dumps({"ts": base + 2.5, "worker": "w", "kind": "job", "text": "noise row"}) + "\n"
    )
    events = loop_audit.timeline("t9007", audit=audit)
    kinds = [event["kind"] for event in events]
    assert kinds[0] == "run_start"
    assert "guard_deny" in kinds
    assert "activity_engine" in kinds
    assert "activity_job" not in kinds
    rendered = loop_audit.render("t9007", audit=audit)
    assert "CMD " in rendered
    assert "GUARD_DENY" in rendered
    assert "ENG" in rendered


def test_render_shows_verdict_and_run_end(audit_dir):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9008", path=audit_dir / "audit_t9008.jsonl")
    audit.run_start(goal="own it", target="10.0.0.5", rounds=3, workers=2)
    audit.verdict({"verdict": "achieved", "status": "done", "coverage_pct": 80.0, "findings": 4, "confirmed": 2})
    audit.run_end(status="done", rounds=3, verdict={"verdict": "achieved", "findings": 4, "confirmed": 2})
    rendered = loop_audit.render("t9008", audit=audit)
    assert "VERDICT    achieved" in rendered
    assert "RUN  END" in rendered
    assert "status=done" in rendered


def test_list_runs_summarizes(audit_dir):
    from modules import loop_audit

    audit = loop_audit.LoopAudit("t9009", path=audit_dir / "audit_t9009.jsonl")
    audit.run_start(goal="g", target="t", rounds=1, workers=1)
    audit.record_command("nmap t", "ok", 1.0)
    audit.record_command("broken", "execution failed: x", 1.0)
    audit.run_end(status="done", rounds=1)
    runs = loop_audit.list_runs()
    match = [run for run in runs if run["task"] == "t9009"]
    assert match, "run missing from summary"
    summary = match[0]
    assert summary["commands"] == 2
    assert summary["ok"] == 1
    assert summary["failed"] == 1
    assert summary["status"] == "done"
    text = loop_audit.render_summary(runs)
    assert "t9009" in text
    assert "done" in text


def test_render_summary_empty(audit_dir):
    from modules import loop_audit

    assert "no loop audits" in loop_audit.render_summary([])


def test_cap_trims_oldest(audit_dir, monkeypatch):
    from modules import loop_audit

    monkeypatch.setattr(loop_audit, "AUDIT_MAX_RECORDS", 5)
    audit = loop_audit.LoopAudit("t9010", path=audit_dir / "audit_t9010.jsonl")
    for index in range(8):
        audit.record("tick", index=index)
    rows = [json.loads(line) for line in (audit_dir / "audit_t9010.jsonl").read_text().splitlines()]
    assert len(rows) == 5
    assert rows[0]["index"] == 3
    assert rows[-1]["index"] == 7
