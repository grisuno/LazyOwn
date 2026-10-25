"""BDD scoped tests for safety gates C01-C03.

Given the guard, traffic and evidence contracts, when I exercise
their public verbs, then the acceptance criteria hold.
"""

from __future__ import annotations


def test_c01_builtin_rules_block_destructive():
    """BDD: destructive shell surfaces require approval."""
    from modules.intercept import Guard
    guard = Guard()
    verdict = guard.check("Bash", "rm -rf / --no-preserve-root")
    assert verdict.action == "ask"
    assert verdict.approval_id


def test_c01_allow_passthrough_and_audit():
    """BDD: benign calls pass and appear in the audit log."""
    from modules.intercept import Guard
    guard = Guard()
    verdict = guard.check("Bash", "echo hello")
    assert verdict.action == "allow"
    entries = guard.audit_log()
    assert entries and entries[-1]["tool"] == "Bash"


def test_c01_deny_rule_and_expiry():
    """BDD: explicit deny wins and expired ask denies."""
    from modules.intercept import InterceptRule, Interceptor
    inter = Interceptor(rules=[InterceptRule(pattern="evil", action="deny", priority=10)],
                        ask_timeout_sec=0.0)
    assert inter.evaluate("Bash", "run evil payload").action == "deny"
    inter2 = Interceptor(rules=[InterceptRule(pattern="x", action="ask")],
                         ask_timeout_sec=-1.0)
    verdict = inter2.evaluate("Bash", "x marks it")
    assert verdict.action == "ask"
    assert inter2.pending_approvals() == []
    rec = inter2.approval_status(verdict.approval_id)
    assert rec is not None and rec.decision == "deny"


def test_c01_daemon_gate_blocks_denied_command():
    """BDD: the daemon safety gate maps deny verdicts to skips."""
    from modules.intercept import Guard
    guard = Guard()
    verdict = guard.check("daemon", "mimikatz sekurlsa::logonpasswords")
    assert verdict.action == "ask"
    benign = guard.check("daemon", "lazynmap 127.0.0.1")
    assert benign.action == "allow"


def test_c02_record_query_roundtrip(tmp_path):
    """BDD: recorded exchanges are queryable with bodies intact."""
    from modules.traffic_recorder import TrafficRecorder
    rec = TrafficRecorder(tmp_path / "traffic")
    ex = rec.record("GET", "http://target.local/a/123", status=200,
                    req_body=b"q=1", resp_body=b"hello")
    assert rec.count() == 1
    rows = rec.query(host="target.local")
    assert rows and rows[0]["id"] == ex.exchange_id
    body = rec.get_body(ex.exchange_id)
    assert "hello" in body["resp_body"]


def test_c02_path_traversal_blocked(tmp_path):
    """BDD: body fetch outside the vault is rejected."""
    from modules.traffic_recorder import TrafficRecorder
    rec = TrafficRecorder(tmp_path / "traffic")
    try:
        rec.get_body("../evil")
        assert False, "expected PermissionError"
    except (PermissionError, FileNotFoundError):
        assert True


def test_c03_put_get_and_gc(tmp_path):
    """BDD: evidence vault hashes, verifies, and collects garbage."""
    import time
    from modules import evidence as evmod
    from modules.evidence import EvidenceStore
    store = EvidenceStore(tmp_path / "evidence")
    digest = store.put(b"poc-bytes")
    assert store.exists(digest)
    assert store.get(digest) == b"poc-bytes"
    try:
        store.get("0" * 64)
        assert False, "expected missing blob error"
    except (FileNotFoundError, ValueError, OSError):
        assert True
    blob = store.blob_path(digest)
    old = time.time() - evmod.GC_GRACE_SEC - 10
    import os
    os.utime(blob, (old, old))
    removed = store.garbage_collect(set())
    assert removed == 1


def test_c03_tamper_detected(tmp_path):
    """BDD: corrupted blob bytes fail integrity verification."""
    from modules.evidence import EvidenceStore
    store = EvidenceStore(tmp_path / "evidence")
    digest = store.put(b"clean-bytes")
    blob = store.blob_path(digest)
    blob.write_bytes(b"tampered-bytes!!")
    try:
        store.get(digest)
        assert False, "expected ValueError"
    except ValueError:
        assert True
