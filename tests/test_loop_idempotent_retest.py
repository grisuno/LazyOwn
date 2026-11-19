"""Idempotent retest + effect lock: exploitation verbs are verified, not replayed.

Bug 2.2: ``Retester.retest`` took the first PoC line and re-executed it. For a
shell finding the PoC head is ``auto_pwn``, so the retester re-exploited the
target and opened a duplicate session. The retest now verifies access-class
findings against a live session (idempotent ``id -u``) and never replays an
exploitation verb; the terminal fallback reuses a live session and claims a
``(target, vector)`` effect lock instead of double-exploiting.
"""

from __future__ import annotations

import modules.atomic_exploit_bridge as bridge
import modules.lazy_loop as loop


def _sandbox(tmp_path, monkeypatch):
    """Redirect loop persistence into a scratch directory."""
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)


def test_is_exploit_command_recognizes_access_verbs():
    """Access-establishing verbs are flagged; idempotent probes are not."""
    assert loop._is_exploit_command("auto_pwn 172.17.0.2")
    assert loop._is_exploit_command("/usr/bin/auto_pwn 172.17.0.2 --all")
    assert loop._is_exploit_command("atomic_shell 10.0.0.5")
    assert not loop._is_exploit_command("curl -sS -I http://172.17.0.2")
    assert not loop._is_exploit_command("nmap -sV 172.17.0.2")
    assert not loop._is_exploit_command("")


def test_exploit_target_prefers_command_then_text():
    """Target comes from the PoC argument, else an IPv4 in the finding text."""

    class _Node:
        text = "shell on 10.9.9.9 obtained"

    assert loop._exploit_target("auto_pwn 172.17.0.2 --all", _Node()) == "172.17.0.2"
    assert loop._exploit_target("auto_pwn --all", _Node()) == "10.9.9.9"


def test_session_verdict_passthrough_for_non_exploit(tmp_path, monkeypatch):
    """A non-exploit PoC is left to the ordinary replay path (returns None)."""
    _sandbox(tmp_path, monkeypatch)
    graph = loop.ExplorationGraph("tx")
    node = graph.add_node("finding", "sqli at /x", state="pending", meta={"poc": "curl -I http://x"})
    retester = loop.Retester(graph, loop.ActivityLog("tx"), loop.TrafficLog("tx"))
    assert retester._session_verdict(graph.get(node.node_id), "curl -I http://x") is None


def test_exploit_finding_not_replayed_without_session(tmp_path, monkeypatch):
    """auto_pwn PoC with no live session is inconclusive; executor never fires."""
    _sandbox(tmp_path, monkeypatch)
    monkeypatch.setattr(bridge, "probe_live_shell", lambda target, command="id -u": None)
    graph = loop.ExplorationGraph("tx")
    node = graph.add_node(
        "finding",
        "possible issue via auto_pwn: root shell",
        state="pending",
        meta={"poc": "auto_pwn 172.17.0.2"},
    )
    calls: list[str] = []
    retester = loop.Retester(graph, loop.ActivityLog("tx"), loop.TrafficLog("tx"))
    result = retester.retest(node.node_id, executor=lambda c: calls.append(c) or "uid=0(root)")
    assert result["verdict"] == "inconclusive"
    assert result["attempts"] == 0
    assert calls == []
    assert "re-exploitation suppressed" in graph.get(node.node_id).meta["retest"]["evidence"]


def test_exploit_finding_verified_via_live_session(tmp_path, monkeypatch):
    """A live shell verifies the finding via id -u, not by replaying auto_pwn."""
    _sandbox(tmp_path, monkeypatch)
    monkeypatch.setattr(
        bridge,
        "probe_live_shell",
        lambda target, command="id -u": {"output": "uid=0(root) gid=0(root)", "owner": "ms2_ingreslock"},
    )
    graph = loop.ExplorationGraph("tx")
    node = graph.add_node(
        "finding",
        "possible issue via auto_pwn: root shell",
        state="pending",
        meta={"poc": "auto_pwn 172.17.0.2"},
    )
    calls: list[str] = []
    retester = loop.Retester(graph, loop.ActivityLog("tx"), loop.TrafficLog("tx"))
    result = retester.retest(node.node_id, executor=lambda c: calls.append(c) or "x")
    assert result["verdict"] == "reproduced"
    assert calls == []
    stored = graph.get(node.node_id)
    assert stored.meta["vstate"] == "confirmed"
    assert "uid=0" in stored.meta["retest"]["evidence"]


def test_claim_effect_dedupes_by_target_vector():
    """A second claimant for the same host and vector is refused until release."""
    bridge.release_effect("9.9.9.9", "auto_pwn")
    bridge.release_effect("9.9.9.9", "atomic_shell")
    assert bridge.claim_effect("9.9.9.9", "auto_pwn") is True
    assert bridge.claim_effect("9.9.9.9", "auto_pwn") is False
    assert bridge.claim_effect("9.9.9.9", "atomic_shell") is True
    bridge.release_effect("9.9.9.9", "auto_pwn")
    assert bridge.claim_effect("9.9.9.9", "auto_pwn") is True
    bridge.release_effect("9.9.9.9", "auto_pwn")
    bridge.release_effect("9.9.9.9", "atomic_shell")


def test_claim_effect_fail_open_on_empty():
    """Empty target or vector grants the claim (fail-open)."""
    assert bridge.claim_effect("", "auto_pwn") is True
    assert bridge.claim_effect("x", "") is True


def test_probe_live_shell_no_session_returns_none():
    """No cached session for the target returns None so callers fall back."""
    assert bridge.probe_live_shell("203.0.113.199") is None
    assert bridge.probe_live_shell("") is None


def test_terminal_fallback_reuses_live_session(tmp_path, monkeypatch):
    """A cached live shell is reused; auto_pwn is never re-run."""
    _sandbox(tmp_path, monkeypatch)
    import modules.outcome_bus as ob

    events: list[dict] = []
    monkeypatch.setattr(ob, "record_event", lambda **kw: events.append(kw) or {"ok": True})
    monkeypatch.setattr(
        bridge,
        "probe_live_shell",
        lambda target, command="id -u": {"output": "uid=0(root)", "owner": "ms2_ingreslock"},
    )
    engine = loop.LazyLoopEngine()
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    calls: list[str] = []
    ok = engine._terminal_autopwn_fallback(task_id, lambda c: calls.append(c) or "x", loop.ActivityLog(task_id))
    assert ok is True
    assert calls == []
    assert events and events[-1]["source"] == "lazy_loop_fallback_reuse"
    assert events[-1]["metadata"]["reused"] is True


def test_terminal_fallback_skips_when_effect_locked(tmp_path, monkeypatch):
    """A held (target, auto_pwn) effect lock skips the duplicate terminal fallback."""
    _sandbox(tmp_path, monkeypatch)
    import modules.auto_registry as reg

    monkeypatch.setattr(reg, "verb_gap", lambda verb: False, raising=False)
    monkeypatch.setattr(reg, "verb_enabled", lambda verb: True, raising=False)
    monkeypatch.setattr(bridge, "probe_live_shell", lambda target, command="id -u": None)
    engine = loop.LazyLoopEngine()
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    assert bridge.claim_effect("172.17.0.2", "auto_pwn") is True
    calls: list[str] = []
    try:
        ok = engine._terminal_autopwn_fallback(
            task_id, lambda c: calls.append(c) or "uid=0(root)", loop.ActivityLog(task_id)
        )
    finally:
        bridge.release_effect("172.17.0.2", "auto_pwn")
    assert ok is False
    assert calls == []
