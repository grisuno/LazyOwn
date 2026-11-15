"""Traceability feeds the process: repeatedly gate-blocked verbs become vetoes.

The audit timeline records every command a gate blocked (guard deny, opsec,
approval, sudo), but nothing learned from it -- the planner could keep proposing
a verb the guard always denies, burning rounds. ``blocked_verbs`` distils the
timeline into the verbs blocked at or above a threshold so the loop can veto
them, closing the traceability-to-improvement gap.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import pytest  # noqa: E402

from modules import loop_audit  # noqa: E402


@pytest.fixture()
def audit(tmp_path, monkeypatch):
    monkeypatch.setattr(loop_audit, "AUDIT_DIR", tmp_path, raising=False)
    return tmp_path


def _write_run(task_id: str):
    a = loop_audit.start(task_id)
    a.blocked("opsec", "high detection", command="responder -I eth0")
    a.blocked("opsec", "high detection", command="responder -I eth0 -w")
    a.blocked("opsec", "high detection", command="responder -A")
    a.blocked("guard", "destructive", command="rm -rf /tmp/x")
    a.record("command", command="nmap -sV", success=True)
    loop_audit.stop(task_id)


def test_blocked_verbs_returns_repeat_offenders(audit):
    _write_run("t1")
    offenders = loop_audit.blocked_verbs("t1", min_count=3)
    assert offenders == ["responder"]


def test_blocked_verbs_threshold_respected(audit):
    _write_run("t1")
    assert loop_audit.blocked_verbs("t1", min_count=2) == ["responder"]
    assert loop_audit.blocked_verbs("t1", min_count=5) == []


def test_blocked_verbs_empty_for_unknown_task(audit):
    assert loop_audit.blocked_verbs("nope", min_count=1) == []


def test_blocked_verbs_ignores_executed_commands(audit):
    a = loop_audit.start("t2")
    a.record("command", command="nmap -sV", success=True)
    a.record("command", command="nmap -sC", success=True)
    a.record("command", command="nmap -p-", success=True)
    loop_audit.stop("t2")
    assert loop_audit.blocked_verbs("t2", min_count=1) == []
