"""Loop guardrails: command repair and bounded scanning retests."""

from __future__ import annotations

import modules.lazy_loop as loop


def _sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)


def test_repair_rejects_target_in_port_slot():
    """nmap -p <target> is rewritten to a valid targeted scan."""
    command, reason = loop.repair_worker_command("nmap -sV -p 172.17.0.2", "172.17.0.2")
    assert command == "nmap -sV 172.17.0.2"
    assert "port spec" in reason


def test_repair_strips_binary_path_for_shell_verb():
    """A path to a shell verb becomes the routable bare verb."""
    command, reason = loop.repair_worker_command("/usr/bin/lazynmap 172.17.0.2", "172.17.0.2")
    assert command == "lazynmap 172.17.0.2"
    assert "stripped binary path" in reason


def test_repair_keeps_valid_port_specs():
    """Valid ranges, lists and service names are not touched."""
    for raw in ("nmap -sV -p 80,443 172.17.0.2", "nmap -p- 172.17.0.2", "nmap -p http 172.17.0.2"):
        command, reason = loop.repair_worker_command(raw, "172.17.0.2")
        assert command == raw
        assert reason == ""


def test_repair_appends_missing_target():
    """A target-less network command gets the intent target."""
    command, _reason = loop.repair_worker_command("nmap -sV", "172.17.0.2")
    assert command == "nmap -sV 172.17.0.2"


def test_repair_drops_port_flag_without_value():
    """A dangling -p is dropped and the target is restored."""
    command, reason = loop.repair_worker_command("nmap -sV -p", "172.17.0.2")
    assert command == "nmap -sV 172.17.0.2"
    assert "port spec" in reason


def test_stall_thresholds_follow_command_timeout():
    """Long bounded commands do not trip the fixed 45s/120s watchdog."""
    from modules.lazy_runner import _stall_thresholds

    warn, dump = _stall_thresholds(300)
    assert warn >= 120
    assert dump > 300
    assert _stall_thresholds(60)[0] >= 45


def test_scan_commands_are_not_replayed(tmp_path, monkeypatch):
    """A finding whose PoC is a scan becomes terminal inconclusive without running."""
    _sandbox(tmp_path, monkeypatch)
    graph = loop.ExplorationGraph("t1")
    node = graph.add_node(
        "finding",
        "possible issue via nmap",
        state="pending",
        meta={"poc": "nmap -sV -p- 172.17.0.2"},
    )
    calls: list[str] = []
    retester = loop.Retester(graph, loop.ActivityLog("t1"), loop.TrafficLog("t1"))
    result = retester.retest(node.node_id, executor=lambda command: calls.append(command) or "open")
    assert result["verdict"] == "inconclusive"
    assert result["attempts"] == 0
    assert calls == []
    stored = graph.get(node.node_id)
    assert stored.state == "done"
    assert stored.meta["status"] == "inconclusive"
    assert stored.meta["retest_terminal"] is True
    assert graph.list("finding", "pending") == []
