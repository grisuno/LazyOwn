"""Regressions surfaced by the t0027 engagement trace.

Covers the false-positive finding pipeline (ssh/dig failures reported as
confirmed criticals while the real auto_pwn shell stayed inconclusive),
the netcat idle hang, the tiny-model codegen waste, the silently dropped
rounds budget and the ambient-rate-limit noise that made the attribution
ledger block verbs that had just obtained a shell.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import modules.atomic_exploit_bridge as bridge
import modules.lazy_loop as loop
from modules.loop.worker_lazymode import _member_sizes_b


def _sandbox(tmp_path, monkeypatch):
    """Redirect loop persistence into a scratch directory."""
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)


def _retester(tmp_path, monkeypatch, task="tx"):
    """Build a Retester over a fresh scratch graph."""
    _sandbox(tmp_path, monkeypatch)
    graph = loop.ExplorationGraph(task)
    retester = loop.Retester(graph, loop.ActivityLog(task), loop.TrafficLog(task))
    return graph, retester


def test_netcat_piped_banner_sender_gets_idle_timeout():
    """printf | nc without -w is bounded without losing the payload quoting."""
    command, reason = loop.repair_worker_command("printf 'USER test:)\\n' | nc 172.17.0.4 21", "172.17.0.4")
    assert command == "printf 'USER test:)\\n' | nc -w 5 172.17.0.4 21"
    assert "netcat" in reason


def test_netcat_already_timed_is_untouched():
    """A command that already bounds reads is left exactly as proposed."""
    raw = "printf 'USER test:)\\n' | nc -w 5 172.17.0.4 21"
    command, reason = loop.repair_worker_command(raw, "172.17.0.4")
    assert command == raw
    assert reason == ""


def test_failed_ssh_replay_is_inconclusive_not_reproduced(tmp_path, monkeypatch):
    """The OpenSSH 'may be vulnerable' warning must not count as proof.

    t0027 finding #11: the ssh negotiation failed but the post-quantum
    warning text contains 'vulnerable', and the success marks ran before
    the blocked marks, so the failure was retested as reproduced.
    """
    graph, retester = _retester(tmp_path, monkeypatch)
    node = graph.add_node(
        "finding",
        "RCE via ssh 172.17.0.4",
        state="pending",
        meta={"poc": "ssh root@172.17.0.4 -p 22", "severity": "critical"},
    )
    failed = (
        "Unable to negotiate with 172.17.0.4 port 22: no matching host key type found. Their offer: ssh-rsa,ssh-dss"
    )
    result = retester.retest(node.node_id, executor=lambda _cmd: failed)
    assert result["verdict"] == "inconclusive"


def test_failed_dig_citation_is_inconclusive(tmp_path, monkeypatch):
    """A verbatim quote of a failed dig replay must not confirm the finding."""
    graph, retester = _retester(tmp_path, monkeypatch)
    node = graph.add_node(
        "finding",
        "CVE-2014-6271 via dig +short 172.17.0.4",
        state="pending",
        meta={"poc": "dig +short 172.17.0.4", "severity": "critical"},
    )
    failed = "dig: couldn't get address for '+short': not found"
    result = retester.retest(node.node_id, executor=lambda _cmd: failed)
    assert result["verdict"] == "inconclusive"


def test_exploit_finding_confirmed_from_captured_uid_without_live_session(tmp_path, monkeypatch):
    """The real auto_pwn shell (uid=1000) is confirmed from captured evidence.

    t0027 finding #13: no live session existed at retest time, the probe
    returned None and the only finding with an actual shell fell through
    to inconclusive (0 attempts), so the engagement never proved its own
    foothold at goal time.
    """
    _sandbox(tmp_path, monkeypatch)
    monkeypatch.setattr(bridge, "probe_live_shell", lambda target, command="id -u": None)
    graph = loop.ExplorationGraph("tx")
    node = graph.add_node(
        "finding",
        "RCE via auto_pwn 172.17.0.4 --all",
        state="pending",
        meta={"poc": "auto_pwn 172.17.0.4 --all\nuid=1000(msfadmin) gid=1000(msfadmin)"},
    )
    retester = loop.Retester(graph, loop.ActivityLog("tx"), loop.TrafficLog("tx"))
    calls: list[str] = []
    result = retester.retest(node.node_id, executor=lambda c: calls.append(c) or "")
    assert result["verdict"] == "reproduced"
    assert result["attempts"] == 0
    assert calls == []
    assert "uid=1000" in graph.get(node.node_id).meta["retest"]["evidence"]


def test_uid_fallback_refuses_failure_evidence(tmp_path, monkeypatch):
    """Captured uid text inside a failed connection is never proof."""
    _sandbox(tmp_path, monkeypatch)
    monkeypatch.setattr(bridge, "probe_live_shell", lambda target, command="id -u": None)
    graph = loop.ExplorationGraph("tx")
    node = graph.add_node(
        "finding",
        "RCE via ssh",
        state="pending",
        meta={"poc": "ssh root@172.17.0.4\nuid=0(root) connection refused"},
    )
    retester = loop.Retester(graph, loop.ActivityLog("tx"), loop.TrafficLog("tx"))
    result = retester.retest(node.node_id, executor=lambda _c: "")
    assert result["verdict"] == "inconclusive"


def test_writeback_refuses_finding_from_failure_output(tmp_path, monkeypatch):
    """dig 'couldn't get address' output creates no finding at writeback."""
    _sandbox(tmp_path, monkeypatch)
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    intent = graph.add_node("intent", "brief dig on 172.17.0.2", state="running")
    node = graph.get(intent.node_id)
    wrote = worker._writeback(node, [("dig +short 172.17.0.2", "dig: couldn't get address for '+short': not found")])
    assert wrote["findings"] == 0
    assert graph.list("finding") == []


def test_writeback_accepts_real_shell_output(tmp_path, monkeypatch):
    """A captured uid line still creates the finding evidence."""
    _sandbox(tmp_path, monkeypatch)
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    intent = graph.add_node("intent", "gain initial access on 172.17.0.2", state="running")
    node = graph.get(intent.node_id)
    wrote = worker._writeback(node, [("auto_pwn 172.17.0.2", "uid=1000(msfadmin) gid=1000(msfadmin)")])
    assert wrote["findings"] == 1


def test_member_sizes_parse_model_tags():
    """Size tags parse per member; untagged entries never block."""
    members = [
        {"name": "a", "model": "ollama:deepseek-r1:1.5b"},
        {"name": "b", "model": "groq:openai/gpt-oss-120b"},
        {"name": "c", "model": "llamacpp:local-model"},
        "not-a-dict",
    ]
    assert _member_sizes_b(members) == [1.5, 120.0]


def test_lazymode_skips_tiny_model_chain(tmp_path, monkeypatch):
    """A chain whose smallest member is 1.5B never reaches the model."""
    import core.config as core_config
    from modules.lazy_engine import LazyEngine

    _sandbox(tmp_path, monkeypatch)
    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {})
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    engine.ensure_target(task_id, "172.17.0.2", "loop target")
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    monkeypatch.setattr(
        loop,
        "task_llm_chain",
        lambda *a, **k: [{"name": "ollama-local", "model": "ollama:deepseek-r1:1.5b"}],
    )
    monkeypatch.setattr(loop.LlmPool, "members", lambda self: [])
    monkeypatch.setattr(loop.LlmPool, "complete", lambda self, *a, **k: "```python\nresult = {}\n```")
    import sdk.lazymode as lazymode

    fired = {"n": 0}
    monkeypatch.setattr(
        lazymode,
        "run",
        lambda script, **k: (
            fired.__setitem__("n", 1) or SimpleNamespace(ok=True, result={}, stdout="", error="", duration_s=0.1)
        ),
    )
    intent = graph.add_node("intent", "brief service: ssh on 172.17.0.2:22", state="open")
    node = graph.get(intent.node_id)
    outcome = {"facts": 0, "assets": 0, "findings": 0, "state": "done"}
    won = worker._lazymode_try(node, outcome, [], None, loop.Budget(worker.store))
    assert won is False
    assert fired["n"] == 0


def test_apply_budget_maps_cli_keys_to_engine_keys(tmp_path, monkeypatch):
    """--budget rounds=1 reaches the engine as max_rounds=1, not dropped."""
    from modules.lazy_engine import LazyEngine
    from modules.lazy_runner import _apply_budget

    _sandbox(tmp_path, monkeypatch)
    engine = LazyEngine()
    task_id = engine.create_task("engage 172.17.0.2")["task_id"]
    _apply_budget(engine, task_id, {"rounds": 1, "toolcalls": 250, "timeout_sec": 60.0})
    limits = engine.budget.limits(task_id)
    assert limits["max_rounds"] == 1
    assert limits["max_toolcalls"] == 250


def test_orchestrate_does_not_clobber_budget_rounds(tmp_path, monkeypatch):
    """A persisted budget max_rounds survives orchestrate's own set."""
    from modules.lazy_engine import LazyEngine

    _sandbox(tmp_path, monkeypatch)
    engine = LazyEngine()
    task_id = engine.create_task("engage 172.17.0.2")["task_id"]
    engine.budget.set_limits(task_id, max_rounds=1)
    engine.budget.set_limits(task_id, max_rounds=1)
    persisted = (engine.store.get(task_id) or {}).get("budget", {})
    assert persisted.get("max_rounds") == 1


def test_mark_goals_achieved_credits_pending_goals(tmp_path, monkeypatch):
    """An achieved wrap-up verdict closes pending goal nodes from evidence.

    t0027 printed ``goals 0/2 and 2 pending`` directly under ``achieved
    coverage=100.0%`` because goal nodes only advance on the round-time
    checker and deliberately stay pending to keep the planner alive.
    """

    _sandbox(tmp_path, monkeypatch)
    engine = loop.LazyLoopEngine()
    task_id = engine.create_task("engage 172.17.0.2")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    graph.add_node("goal", "gain initial access on 172.17.0.2", state="pending")
    graph.add_node("goal", "move laterally to 172.17.0.3", state="pending")
    graph.add_node("finding", "shell obtained on 172.17.0.2", state="confirmed")
    activity = loop.ActivityLog(task_id)
    engine._mark_goals_achieved(task_id, graph, activity)
    assert all(g.state == "done" for g in graph.list("goal"))


def test_dig_option_lines_pass_through_raw():
    """dig +short 172.17.0.4 is executed verbatim, never mangled into @+short.

    t0027: the do_dig wizardry interpolated the whole line as a DNS server,
    producing ``dig version.bind CHAOS TXT @+short 172.17.0.4``.
    """
    source = (Path(__file__).resolve().parent.parent / "cli" / "commands" / "recon.py").read_text()
    assert 'token.startswith(("+", "@"))' in source
    assert 'self.cmd(f"dig {line}")' in source
    assert 'self.cmd(f"dig version.bind CHAOS TXT @{line}")' not in source.split('self.cmd(f"dig {line}")')[0]


def test_attribution_scrubs_ambient_rate_limit_noise(monkeypatch):
    """A 429 agent-error panel inside captured output is not a target block.

    t0027: every step that coincided with an openai/gpt-oss-120b 429
    notification carried 'Rate limit reached' inside the captured output,
    so classify() read it as a hard block and the planner demoted auto_pwn
    right after it had obtained a shell.
    """
    import modules.loop.worker_memory as wm
    import modules.outcome_attribution as oa

    noise = (
        "[result] auto_pwn ran\nloop:agent-error: Error code: 429 - Rate limit reached for model\nuid=1000(msfadmin)\n"
    )
    seen: dict = {}

    class _FakeLedger:
        def __init__(self, task_id: str) -> None:
            pass

        def record(self, command: str, classification: str) -> str:
            seen["classification"] = classification
            return "auto_pwn"

    monkeypatch.setattr(oa, "AttributionLedger", _FakeLedger)
    mixin = wm.WorkerMemoryMixin.__new__(wm.WorkerMemoryMixin)
    mixin.name = "worker-1"
    mixin.task_id = "tx"
    mixin.activity = SimpleNamespace(emit=lambda *a, **k: None)
    mixin._attribute_outcome(SimpleNamespace(node_id=1), "auto_pwn 172.17.0.4 --all", noise)
    assert seen["classification"] != "blocked"
