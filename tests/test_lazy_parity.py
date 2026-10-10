"""LAZY parity proof tests: every ported subsystem must behave, not just exist.

Covers the gate (intercept allow/deny/ask), global scope deny, evidence
vault roundtrip, traffic exchange log, planner frontier + todos, goal
lifecycle, LLM failover pool, and the ephemeral sonner-style toast path.
Each test drives the real module used by the engage daemon and auto_loop.
"""

from __future__ import annotations

import io
import json
import os
import sys
import time
from pathlib import Path

from rich.console import Console

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from cli.themes import THEMES  # noqa: E402
from cli.toast_bus import ToastBus  # noqa: E402
from cli.toast_bus import ToastConfig  # noqa: E402
from cli.toast_bus import ToastFormatter  # noqa: E402
from cli.toast_bus import ToastReader  # noqa: E402
from cli.toast_bus import ToastState  # noqa: E402
from cli.toast_bus import build_default_bus  # noqa: E402
from cli.toast_bus import ephemeral_enabled  # noqa: E402
from cli.toast_bus import render_ephemeral_toasts  # noqa: E402
from evidence import EvidenceStore  # noqa: E402
from goals import GoalTracker  # noqa: E402
from goals import decompose_rule_based  # noqa: E402
from goals import load_constraints  # noqa: E402
from intercept import Guard  # noqa: E402
from intercept import Interceptor  # noqa: E402
from intercept import scope_blocked  # noqa: E402
from llm_pool import HealthRegistry  # noqa: E402
from llm_pool import LLMPool  # noqa: E402
from llm_pool import PoolExhausted  # noqa: E402
from llm_pool import PoolMember  # noqa: E402
from planner import Frontier  # noqa: E402
from planner import Planner  # noqa: E402
from planner import TodoList  # noqa: E402
from traffic_recorder import TrafficRecorder  # noqa: E402


def test_gate_allows_benign_command() -> None:
    """A recon scan passes the safety gate."""
    verdict = Guard().check("daemon", "lazynmap 127.0.0.1")
    assert verdict.action == "allow"


def test_gate_denies_destructive_command() -> None:
    """Filesystem wipes never reach execution."""
    verdict = Guard().check("run", "rm -rf / --no-preserve-root")
    assert verdict.action in ("deny", "ask")


def test_gate_ask_creates_decidable_approval() -> None:
    """Credential dumping parks as ask and resolves via decide."""
    interceptor = Interceptor(ask_timeout_sec=60.0)
    verdict = interceptor.evaluate("run", "mimikatz sekurlsa::logonpasswords")
    assert verdict.action == "ask"
    assert verdict.approval_id
    assert interceptor.decide(verdict.approval_id, "deny") is True
    pending = interceptor.pending_approvals()
    assert all(p.approval_id != verdict.approval_id for p in pending)


def test_gate_ask_expires_fail_closed() -> None:
    """Timed-out approvals leave the pending set (fail-closed)."""
    interceptor = Interceptor(ask_timeout_sec=0.01, timeout_action="deny")
    verdict = interceptor.evaluate("run", "mimikatz dump")
    assert verdict.action == "ask"
    time.sleep(0.05)
    assert interceptor.pending_approvals() == []


def test_scope_blocks_protected_suffixes() -> None:
    """Global deny list mirrors LAZY asset-intercept parity."""
    assert scope_blocked("target.gov") == ".gov"
    assert scope_blocked("host.mil") == ".mil"
    assert scope_blocked("127.0.0.1") == ""


def test_constraints_deny_wins() -> None:
    """Payload deny entries block matching commands."""
    constraints = load_constraints({"scope_deny": ["mimikatz"]})
    assert constraints.blocked("run mimikatz dump") == "mimikatz"
    assert constraints.blocked("lazynmap target") == ""


def test_evidence_roundtrip(tmp_path: Path) -> None:
    """Stored output comes back byte-identical under its hash."""
    store = EvidenceStore(tmp_path / "evidence")
    digest = store.put(b"proof output")
    assert store.exists(digest) is True
    assert store.get(digest) == b"proof output"


def test_evidence_rejects_tampered_blob(tmp_path: Path) -> None:
    """Flipping one byte fails the integrity check on read."""
    store = EvidenceStore(tmp_path / "evidence")
    digest = store.put(b"original")
    blob = store.blob_path(digest)
    blob.write_bytes(b"tampered")
    try:
        store.get(digest)
    except ValueError:
        return
    raise AssertionError("tampered blob must not verify")


def test_evidence_gc_drops_unreferenced(tmp_path: Path) -> None:
    """Blobs nobody references past the grace period are collected."""
    store = EvidenceStore(tmp_path / "evidence")
    digest = store.put(b"stale")
    blob = store.blob_path(digest)
    old = time.time() - 200000.0
    os.utime(blob, (old, old))
    assert store.garbage_collect(set()) == 1
    assert store.exists(digest) is False


def test_traffic_record_and_query(tmp_path: Path) -> None:
    """Each step exchange is queryable by host with its body."""
    recorder = TrafficRecorder(tmp_path / "traffic")
    exchange = recorder.record("TOOL", "http://127.0.0.1/lazynmap",
                               status=1, resp_body=b"open 22/tcp")
    rows = recorder.query(host="127.0.0.1")
    assert any(r["id"] == exchange.exchange_id for r in rows)
    assert "open 22/tcp" in recorder.get_body(exchange.exchange_id)["resp_body"]


def test_frontier_emits_then_dedupes() -> None:
    """Refill emits untried intents; pop marks them tried."""
    frontier = Frontier(Planner(), TodoList())
    first = frontier.refill("127.0.0.1")
    assert first
    claimed = frontier.pop()
    assert claimed is not None
    second_ids = {c.technique_id for c in frontier.refill("127.0.0.1")}
    assert claimed.technique_id not in second_ids


def test_todos_gate_lateral_on_creds() -> None:
    """Lateral techniques wait until the creds step is done."""
    todos = TodoList()
    todos.todo_add("creds")
    todos.todo_add("lateral", requires=["creds"])
    assert todos.blocks("lateral-movement") is True
    assert todos.todo_done("lateral") is False
    assert todos.todo_done("creds") is True
    assert todos.blocks("lateral-movement") is False
    assert todos.next_ready() is not None


def test_goals_decompose_and_prove() -> None:
    """Keyword objectives split into verifiable goals proven by evidence."""
    goals = decompose_rule_based("scan the target then exploit it")
    assert any("recon" in g.text for g in goals)
    tracker = GoalTracker(goals)
    assert tracker.prove_goal("recon: discover live hosts", evidence="abc123") is True
    assert tracker.goal_met() is False
    assert tracker.goal_met(opt_in=True) is True
    assert tracker.all_achieved() is True


def test_pool_fails_over_in_rank_order() -> None:
    """A dead head member falls through to the next rank."""
    seen: list[str] = []

    def _fail(prompt: str) -> str:
        seen.append("groq")
        raise RuntimeError("boom")

    def _ok(prompt: str) -> str:
        seen.append("ollama")
        return "answer"

    pool = LLMPool([
        PoolMember("groq", "groq", "groq", rank=10, complete=_fail),
        PoolMember("ollama", "ollama", "ollama", rank=1, complete=_ok),
    ], health=HealthRegistry())
    assert pool.complete("hi") == "answer"
    assert seen == ["groq", "ollama"]


def test_pool_skips_unhealthy_member() -> None:
    """Three strikes parks the member until backoff expires."""
    health = HealthRegistry()
    calls: list[str] = []

    def _flaky(prompt: str) -> str:
        calls.append("flaky")
        raise RuntimeError("down")

    pool = LLMPool([
        PoolMember("flaky", "flaky", "m", rank=10, complete=_flaky),
        PoolMember("steady", "steady", "m", rank=1, complete=lambda p: "ok"),
    ], health=health)
    assert pool.complete("a") == "ok"
    assert pool.complete("b") == "ok"
    assert pool.complete("c") == "ok"
    assert calls == ["flaky"] * 3
    before = list(calls)
    assert pool.complete("d") == "ok"
    assert calls == before


def test_pool_exhausted_when_all_fail() -> None:
    """Total outage raises instead of returning an empty string."""
    pool = LLMPool([
        PoolMember("a", "a", "m", rank=2, complete=lambda p: (_ for _ in ()).throw(RuntimeError("x"))),
        PoolMember("b", "b", "m", rank=1, complete=lambda p: (_ for _ in ()).throw(RuntimeError("y"))),
    ], health=HealthRegistry())
    try:
        pool.complete("hi")
    except PoolExhausted:
        return
    raise AssertionError("expected PoolExhausted")


def test_pool_session_key_format() -> None:
    """Sticky session headers carry conv, role and index."""
    pool = LLMPool([PoolMember("a", "a", "m", rank=1, complete=lambda p: "x")])
    assert pool.session_key("c1", role="worker", index=2) == "conv-c1-worker-2"


def test_ephemeral_toast_line_has_icon_and_duration() -> None:
    """Sonner-style lines reuse theme roles with per-level delays."""
    config = ToastConfig()
    formatter = ToastFormatter(config, THEMES["default"])
    from cli.toast_bus import ToastEvent as _ToastEvent

    line = formatter.format_ephemeral(_ToastEvent(
        source="events.jsonl", offset=0, event_type="STEP_DONE",
        severity="error", summary="boom", timestamp="t"))
    assert "STEP_DONE" in line.plain and "boom" in line.plain
    assert "✖" in line.plain
    error_delay = formatter.duration_for(_ToastEvent(
        source="e", offset=0, event_type="x", severity="error",
        summary="s", timestamp="t"))
    info_delay = formatter.duration_for(_ToastEvent(
        source="e", offset=0, event_type="x", severity="info",
        summary="s", timestamp="t"))
    assert error_delay > info_delay > 0


def test_ephemeral_render_consumes_cursor(tmp_path: Path) -> None:
    """Ephemeral render prints once; the shared cursor advances like render."""
    events_path = tmp_path / "events.jsonl"
    events_path.write_text(json.dumps({"type": "STEP_DONE", "severity": "info",
                                       "message": "hello"}) + "\n", encoding="utf-8")
    captured = Console(file=io.StringIO(), width=100)
    bus = build_default_bus(payload={"enable_toasts": True},
                            sessions_dir=str(tmp_path), console=captured)
    assert bus.render_ephemeral(enabled=True, duration=0) == 1
    assert "hello" in captured.file.getvalue()
    assert bus.render_ephemeral(enabled=True, duration=0) == 0


def test_ephemeral_flag_routing() -> None:
    """The payload flag selects panel vs sonner-style rendering."""
    assert ephemeral_enabled(None) is False
    assert ephemeral_enabled({"toast_ephemeral": True}) is True
    assert ephemeral_enabled({"toast_ephemeral": "off"}) is False


def test_render_ephemeral_helper(tmp_path: Path) -> None:
    """One-shot helper mirrors render_toasts semantics."""
    events_path = tmp_path / "events.jsonl"
    events_path.write_text(json.dumps({"type": "GOAL_PROVEN", "severity": "success",
                                       "message": "cred captured"}) + "\n", encoding="utf-8")
    captured = Console(file=io.StringIO(), width=100)
    count = render_ephemeral_toasts(payload={"enable_toasts": True},
                                    sessions_dir=str(tmp_path),
                                    console=captured, duration=0)
    assert count == 1


def _write_events(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")


def test_bus_render_still_counts_budget(tmp_path: Path) -> None:
    """The persistent panel path is untouched by the ephemeral addition."""
    config = ToastConfig(sessions_dir=str(tmp_path), max_per_tick_default=2)
    _write_events(tmp_path / "events.jsonl",
                   [{"type": "ev", "severity": "info", "summary": f"l{i}"} for i in range(4)])
    bus = ToastBus(config=config, state=ToastState(config, root=tmp_path),
                   reader=ToastReader(config, root=tmp_path),
                   formatter=ToastFormatter(config, THEMES["default"]),
                   console=Console(file=io.StringIO()))
    assert bus.render(enabled=True) == 2
