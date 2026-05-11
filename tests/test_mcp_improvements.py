"""Tests for the high/medium/low impact MCP improvements.

Covers the pure-function helper module (skills.lazyown_mcp_helpers) and
the wiring inside skills.lazyown_mcp:
  - is_likely_credential / audit_tasks
  - evidence_freshness
  - build_target_context (host + port filters, provenance, freshness)
  - evidence_grep with scope filters
  - preflight_command (binary present, OS match, would_duplicate)
  - JobStore async submit + status
  - take_snapshot / diff_snapshot lifecycle
  - needs_confirmation gate

The MCP server itself is large and is exercised through small focused
integration tests for the new tool handlers (target_context, tasks_cleanup,
evidence_grep, session_diff) that monkey-patch SESSIONS_DIR onto a tmp_path.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "skills"))

from lazyown_mcp_helpers import (  # noqa: E402
    DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
    JobStore,
    audit_tasks,
    build_target_context,
    diff_snapshot,
    evidence_freshness,
    evidence_grep,
    is_likely_credential,
    needs_confirmation,
    parse_task_value,
    preflight_command,
    take_snapshot,
)

# ── is_likely_credential ─────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "value,expect_real,expect_reason",
    [
        ("12:09:08", False, "timestamp"),
        ("01:18:31,123", False, "timestamp"),
        ("23:59:59", False, "timestamp"),
        ("http://127.0.0.1", False, "url"),
        ("https://target.htb/admin", False, "url"),
        ("ftp://anon@host", False, "url"),
        ("127.0.0.1", False, "ip_address"),
        ("10.10.11.5:8080", False, "ip_address"),
        ("", False, "empty"),
        ("   ", False, "empty"),
        ("j.fleischman:J0elTHEM4n1990", True, "user_pass"),
        ("admin:admin", True, "user_pass"),
        (
            "aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0",
            True, "ntlm_pair",
        ),
        ("a1b2c3d4e5f67890", True, "hex_hash"),
        ("admin", True, "unknown"),
    ],
)
def test_is_likely_credential_classifies(value, expect_real, expect_reason):
    real, conf, reason = is_likely_credential(value)
    assert real is expect_real
    assert reason == expect_reason
    if expect_real:
        assert conf > 0
    else:
        assert conf == 0.0


def test_is_likely_credential_handles_non_string():
    assert is_likely_credential(None) == (False, 0.0, "non_string")
    assert is_likely_credential(42) == (False, 0.0, "non_string")


# ── parse_task_value ─────────────────────────────────────────────────────────

def test_parse_task_value_complete():
    title = (
        'Leverage new credential: {"value": "j.fleischman:J0elTHEM4n1990", '
        '"host": "127.0.0.1", "service": "smb", "confirmed": true}'
    )
    parsed = parse_task_value(title)
    assert parsed["value"] == "j.fleischman:J0elTHEM4n1990"
    assert parsed["host"] == "127.0.0.1"
    assert parsed["confirmed"] is True


def test_parse_task_value_truncated():
    title = 'Leverage new credential: {"value": "01:17:45", "host": "127.0.0.1", "service": "co'
    parsed = parse_task_value(title)
    assert parsed["value"] == "01:17:45"
    assert parsed["host"] == "127.0.0.1"


def test_parse_task_value_no_payload():
    assert parse_task_value("Recon target — no payload here") is None


# ── audit_tasks ──────────────────────────────────────────────────────────────

def test_audit_tasks_drops_timestamps_and_urls():
    tasks = [
        {"id": 0, "status": "Done", "title": "Recon 127.0.0.1"},
        {"id": 1, "status": "New", "title": (
            'Leverage new credential: {"value": "j.fleischman:J0elTHEM4n1990"}'
        )},
        {"id": 2, "status": "New", "title": (
            'Leverage new credential: {"value": "12:09:08", "host": "127.0.0.1"}'
        )},
        {"id": 3, "status": "New", "title": (
            'Leverage new credential: {"value": "http://127.0.0.1"}'
        )},
        {"id": 4, "status": "New", "title": "Enumerate newly discovered host 10.0.0.1"},
        {"id": 5, "status": "New", "title": "Enumerate newly discovered host 10.0.0.1"},
    ]
    result = audit_tasks(tasks)
    keep = [r for r in result if r.keep]
    drop = [r for r in result if not r.keep]
    keep_ids = {r.task_id for r in keep}
    drop_ids = {r.task_id for r in drop}
    assert 0 in keep_ids
    assert 1 in keep_ids
    assert 4 in keep_ids
    assert 2 in drop_ids
    assert 3 in drop_ids
    assert 5 in drop_ids
    reason_for_5 = next(r.reason for r in result if r.task_id == 5)
    assert reason_for_5 == "duplicate_title"


def test_audit_tasks_respects_min_confidence():
    tasks = [
        {"id": 9, "status": "New", "title": (
            'Leverage new credential: {"value": "admin"}'
        )},
    ]
    high_bar = audit_tasks(tasks, min_confidence=0.5)
    low_bar = audit_tasks(tasks, min_confidence=0.2)
    assert high_bar[0].keep is False
    assert low_bar[0].keep is True


# ── evidence_freshness ───────────────────────────────────────────────────────

def test_evidence_freshness_missing(tmp_path):
    fresh = evidence_freshness(tmp_path / "absent.txt")
    assert fresh["exists"] is False
    assert fresh["stale"] is False


def test_evidence_freshness_fresh(tmp_path):
    p = tmp_path / "scan.nmap"
    p.write_text("data")
    now = p.stat().st_mtime + 60
    fresh = evidence_freshness(p, now=now)
    assert fresh["exists"]
    assert fresh["age_seconds"] >= 60
    assert fresh["stale"] is False


def test_evidence_freshness_stale(tmp_path):
    p = tmp_path / "scan.nmap"
    p.write_text("data")
    far_future = p.stat().st_mtime + DEFAULT_FRESHNESS_THRESHOLD_SECONDS + 100
    fresh = evidence_freshness(p, now=far_future)
    assert fresh["stale"] is True
    assert fresh["age_seconds"] > DEFAULT_FRESHNESS_THRESHOLD_SECONDS


# ── build_target_context ─────────────────────────────────────────────────────

def _seed_sessions(tmp_path: Path) -> Path:
    s = tmp_path / "sessions"
    s.mkdir()
    (s / "scan_10.0.0.1.nmap").write_text(
        "Nmap scan report for 10.0.0.1\n"
        "22/tcp open  ssh OpenSSH 8.4p1\n"
        "80/tcp open  http nginx 1.18.0\n"
        "443/tcp open https nginx\n"
    )
    (s / "credentials.txt").write_text("admin:admin\n")
    return s


def test_build_target_context_filters_by_port(tmp_path):
    s = _seed_sessions(tmp_path)
    wm = {
        "current_phase": "enum",
        "credentials": [
            {"value": "admin:admin", "host": "10.0.0.1", "port": 80},
            {"value": "01:17:45", "host": "10.0.0.1", "port": 443},
        ],
        "vulnerabilities": [
            {"cve": "CVE-2024-9999", "host": "10.0.0.1", "severity": "high"},
        ],
        "hosts": {"10.0.0.1": {"state": "scanned"}},
    }
    ctx = build_target_context("10.0.0.1", port=80, sessions_dir=s, world_model=wm)
    assert ctx["host"] == "10.0.0.1"
    assert ctx["port"] == 80
    assert len(ctx["open_ports"]) == 1
    assert ctx["open_ports"][0]["port"] == 80
    assert any(c["value"] == "admin:admin" for c in ctx["credentials"])
    assert all(c.get("port") != 443 for c in ctx["credentials"])
    assert any(c["confidence"] >= 0.85 for c in ctx["credentials"])


def test_build_target_context_no_port_returns_all(tmp_path):
    s = _seed_sessions(tmp_path)
    ctx = build_target_context("10.0.0.1", port=None, sessions_dir=s, world_model={})
    assert len(ctx["open_ports"]) == 3


# ── evidence_grep ────────────────────────────────────────────────────────────

def test_evidence_grep_finds_in_loot_scope(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    (s / "credentials.txt").write_text("admin:admin\nuser:secret\n")
    (s / "scan_10.0.0.1.nmap").write_text("admin: ignore me\n")
    result = evidence_grep("admin", s, scope="loot")
    assert result["match_count"] >= 1
    assert all("credentials.txt" in m["path"] or "loot" in m["path"]
               for m in result["matches"])


def test_evidence_grep_invalid_regex(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    out = evidence_grep("(", s)
    assert "error" in out


def test_evidence_grep_truncates(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    (s / "credentials.txt").write_text("\n".join(f"admin{i}:pw" for i in range(50)))
    out = evidence_grep("admin", s, scope="loot", max_matches=5)
    assert out["truncated"] is True
    assert out["match_count"] == 5


# ── preflight_command ────────────────────────────────────────────────────────

def test_preflight_detects_duplicate(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    (s / "scan_10.0.0.1.nmap").write_text("x" * 200)
    pre = preflight_command(
        "lazynmap",
        payload={"rhost": "10.0.0.1", "os_id": 2},
        sessions_dir=s,
    )
    assert pre["base_command"] == "lazynmap"
    assert pre["would_duplicate"] is True
    assert any("scan_10.0.0.1.nmap" in d["path"] for d in pre["duplicate_artifacts"])


def test_preflight_flags_missing_payload_keys(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    pre = preflight_command(
        "gobuster",
        payload={"rhost": "10.0.0.1"},
        sessions_dir=s,
    )
    assert "dirwordlist" in pre["missing_payload_keys"]


def test_preflight_os_mismatch(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    pre = preflight_command(
        "evil-winrm",
        payload={"rhost": "10.0.0.1", "os_id": 1},
        sessions_dir=s,
    )
    assert pre["os_required"] == 2
    assert pre["os_match"] is False
    assert pre["ok"] is False


# ── JobStore ─────────────────────────────────────────────────────────────────

def test_jobstore_runs_command_and_reports_done():
    store = JobStore()

    def runner(cmd, timeout):
        return f"ran:{cmd}"

    jid = store.submit("hello", runner, timeout=5)
    deadline = time.time() + 2
    while time.time() < deadline:
        rec = store.status(jid)
        if rec and rec["state"] == "done":
            break
        time.sleep(0.05)
    rec = store.status(jid)
    assert rec is not None
    assert rec["state"] == "done"
    assert rec["stdout"] == "ran:hello"
    assert rec["exit_code"] == 0


def test_jobstore_captures_failure():
    store = JobStore()

    def runner(cmd, timeout):
        raise RuntimeError("boom")

    jid = store.submit("x", runner, timeout=1)
    deadline = time.time() + 2
    while time.time() < deadline:
        rec = store.status(jid)
        if rec and rec["state"] in ("done", "failed"):
            break
        time.sleep(0.05)
    rec = store.status(jid)
    assert rec["state"] == "failed"
    assert "boom" in rec["stderr"]


def test_jobstore_unknown_id():
    store = JobStore()
    assert store.status("nope") is None


def test_jobstore_list_orders_newest_first():
    store = JobStore()
    ids = []
    for i in range(3):
        ids.append(store.submit(f"c{i}", lambda c, t: c, timeout=1))
        time.sleep(0.01)
    listed = store.list(limit=10)
    assert [j["job_id"] for j in listed[:3]] == list(reversed(ids))


# ── snapshots / diff ─────────────────────────────────────────────────────────

def test_diff_first_run_reports_first_run(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    diff = diff_snapshot(s, payload={}, world_model={}, tasks=[])
    assert diff["first_run"] is True


def test_diff_picks_up_changes(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    (s / "a.txt").write_text("hello")
    take_snapshot(s, payload={"rhost": "10.0.0.1"}, world_model={"credentials": []}, tasks=[])
    (s / "b.txt").write_text("new file")
    (s / "a.txt").write_text("modified")
    wm = {"credentials": [{"value": "alice:pw"}]}
    tasks = [{"id": 99, "title": "t"}]
    diff = diff_snapshot(s, payload={}, world_model=wm, tasks=tasks)
    assert diff["first_run"] is False
    assert "b.txt" in diff["added_files"]
    assert "a.txt" in diff["modified_files"]
    assert "alice:pw" in diff["new_credentials"]
    assert 99 in diff["new_task_ids"]


# ── confirmation gate ────────────────────────────────────────────────────────

def test_confirmation_required_for_destructive_command():
    assert needs_confirmation(
        "lazyown_run_command", {"command": "rm -rf /tmp/foo"}
    ) is True
    assert needs_confirmation(
        "lazyown_run_command", {"command": "rm -rf /tmp/foo", "confirm": True}
    ) is False


def test_confirmation_skipped_for_benign():
    assert needs_confirmation("lazyown_run_command", {"command": "lazynmap"}) is False


def test_confirmation_required_for_destructive_tools():
    assert needs_confirmation("lazyown_c2_command", {}) is True
    assert needs_confirmation("lazyown_c2_command", {"confirm": True}) is False


# ── MCP handler integration smoke (target_context, tasks_cleanup) ────────────

def _fresh_mcp_module(tmp_path: Path):
    """Reload skills.lazyown_mcp pointing at an isolated SESSIONS_DIR."""
    import importlib

    sessions = tmp_path / "sessions"
    sessions.mkdir()
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps({"rhost": "10.0.0.1", "os_id": 2}))
    os.environ["LAZYOWN_DIR"] = str(tmp_path)
    sys.path.insert(0, str(_ROOT / "skills"))
    if "lazyown_mcp" in sys.modules:
        importlib.reload(sys.modules["lazyown_mcp"])
    import lazyown_mcp as mod
    return mod, sessions


def test_handler_target_context_via_helper(tmp_path):
    s = _seed_sessions(tmp_path)
    ctx = build_target_context("10.0.0.1", port=22, sessions_dir=s, world_model={})
    assert ctx["host"] == "10.0.0.1"
    assert any(p["service"] == "ssh" for p in ctx["open_ports"])


def test_handler_tasks_cleanup_dry_run(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    tasks = [
        {"id": 0, "status": "Done", "title": "Recon 127.0.0.1"},
        {"id": 1, "status": "New", "title": (
            'Leverage new credential: {"value": "12:09:08"}'
        )},
        {"id": 2, "status": "New", "title": (
            'Leverage new credential: {"value": "alice:pw1"}'
        )},
    ]
    (s / "tasks.json").write_text(json.dumps(tasks))
    audited = audit_tasks(tasks)
    keep_ids = {a.task_id for a in audited if a.keep}
    assert 1 not in keep_ids
    assert 2 in keep_ids


def test_evidence_grep_handler_ignores_binaries(tmp_path):
    s = tmp_path / "sessions"
    s.mkdir()
    (s / "image.png").write_bytes(b"\x89PNGfakeadminfake")
    (s / "credentials.txt").write_text("admin:admin\n")
    out = evidence_grep("admin", s, scope="loot")
    assert all(not m["path"].endswith(".png") for m in out["matches"])
