"""Tests for Observer-style failure attribution and verb demotion.

The classifier must read a target's active refusal (WAF, 403/429, rate limit)
as ``blocked`` before any generic ``error``, so the planner treats a defence as
a strategy signal rather than a retryable failure. The ledger must tally per
verb, demote a verb only after repeated blocks with no later success, and clear
the demotion once the verb succeeds.
"""

from __future__ import annotations

from modules.outcome_attribution import (
    BLOCKED,
    ERROR,
    OK,
    AttributionLedger,
    classify,
    verb_of,
)


def test_classify_blocked_markers():
    assert classify("HTTP/1.1 403 Forbidden") == BLOCKED
    assert classify("Access denied by Cloudflare") == BLOCKED
    assert classify("429 Too Many Requests") == BLOCKED
    assert classify("Request blocked by mod_security") == BLOCKED


def test_classify_blocked_wins_over_error_flag():
    assert classify("403 Forbidden (WAF)", is_error=True) == BLOCKED


def test_classify_error_markers():
    assert classify("curl: (7) Connection refused") == ERROR
    assert classify("could not resolve host") == ERROR
    assert classify("anything", is_error=True) == ERROR


def test_classify_ok():
    assert classify("80/tcp open http") == OK
    assert classify("") == OK


def test_verb_of_basename():
    assert verb_of("/usr/bin/sqlmap -u http://t") == "sqlmap"
    assert verb_of("curl http://t") == "curl"
    assert verb_of("") == ""


def test_ledger_records_and_counts(tmp_path):
    ledger = AttributionLedger("t1", base_dir=tmp_path)
    ledger.record("curl http://t", BLOCKED)
    ledger.record("curl http://t", BLOCKED)
    counts = ledger.counts("curl")
    assert counts[BLOCKED] == 2 and counts[OK] == 0


def test_ledger_demotes_after_threshold(tmp_path):
    ledger = AttributionLedger("t1", base_dir=tmp_path)
    ledger.record("sqlmap -u http://t", BLOCKED)
    assert "sqlmap" not in ledger.blocked_verbs()
    ledger.record("sqlmap -u http://t", BLOCKED)
    assert "sqlmap" in ledger.blocked_verbs()


def test_ledger_success_clears_demotion(tmp_path):
    ledger = AttributionLedger("t1", base_dir=tmp_path)
    ledger.record("nmap t", BLOCKED)
    ledger.record("nmap t", BLOCKED)
    assert "nmap" in ledger.blocked_verbs()
    ledger.record("nmap t", OK)
    assert "nmap" not in ledger.blocked_verbs()


def test_ledger_ignores_unparseable_verb(tmp_path):
    ledger = AttributionLedger("t1", base_dir=tmp_path)
    assert ledger.record("", BLOCKED) == ""
    assert ledger.blocked_verbs() == set()


def test_ledger_task_isolation(tmp_path):
    a = AttributionLedger("a", base_dir=tmp_path)
    b = AttributionLedger("b", base_dir=tmp_path)
    a.record("curl t", BLOCKED)
    a.record("curl t", BLOCKED)
    assert "curl" in a.blocked_verbs()
    assert "curl" not in b.blocked_verbs()


def test_agentic_blocked_verbs_reads_ledger(tmp_path, monkeypatch):
    import modules.loop.worker_agentic as wa

    seed = AttributionLedger("task-x", base_dir=tmp_path)
    seed.record("sqlmap -u http://t", BLOCKED)
    seed.record("sqlmap -u http://t", BLOCKED)

    monkeypatch.setattr(
        "modules.outcome_attribution.AttributionLedger",
        lambda task_id="", base_dir=None: AttributionLedger(task_id, base_dir=tmp_path),
    )
    worker = type("W", (wa.WorkerAgenticMixin,), {})()
    worker.task_id = "task-x"
    assert "sqlmap" in worker._blocked_verbs()
