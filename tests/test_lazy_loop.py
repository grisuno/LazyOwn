"""Production loop fidelity tests: guard judge, findings, settlement, bridge."""

from __future__ import annotations

import json
import time


def _patched_engine(tmp_path, monkeypatch):
    """Return an engine whose stores live entirely under tmp_path."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_planner_queues_retest_after_world_change(tmp_path, monkeypatch):
    """BDD: a recent world change drives a re-test intent on the changed host."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("recon 10.0.0.5")["task_id"]
    engine.assets.insert("ip", "10.0.0.5", task_id=task_id)
    (tmp_path / "lazy_changes.jsonl").write_text(
        json.dumps({"kind": "port_opened", "ip": "10.0.0.5", "port": 443,
                    "before": None, "after": {"service": "https"}, "detected": time.time()}) + "\n",
        encoding="utf-8",
    )
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    summaries = [row[0] for row in planner._candidates()]
    assert any(summary.startswith("re-test 10.0.0.5 after port_opened") for summary in summaries)


def test_planner_queues_ghost_host_verification(tmp_path, monkeypatch):
    """BDD: an active ghost host drives a verification intent."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("verify ghosts")["task_id"]
    engine.assets.insert("ip", "old-name.local", task_id=task_id)
    (tmp_path / "lazy_ghosts.json").write_text(
        json.dumps({"hosts": {"old-name.local": {"state": "ghost", "since": time.time(),
                                                 "answers": ["10.0.0.5:443"], "cleared_at": None}}}),
        encoding="utf-8",
    )
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    summaries = [row[0] for row in planner._candidates()]
    assert any(summary.startswith("verify ghost host old-name.local") for summary in summaries)


def test_settlement_prompt_variants():
    """BDD: wrap-up wording depends on agent and stop reason."""
    from modules.lazy_engine import settlement_prompt

    worker = settlement_prompt("worker", "timeout")
    assert "Wall-clock" in worker
    assert "no new tool calls" in worker
    planner = settlement_prompt("planner", "max_turns")
    assert "Flush pending facts" in planner
    assert "prove_goal" in planner
    assert "handoff" in settlement_prompt("main", "max_turns")


def test_planner_proposes_chain_from_discovered_services(tmp_path, monkeypatch):
    """BDD: a matching service makes the planner queue a run-chain intent.

    Given an http service in the world model and an enabled web chain, When
    the planner builds candidates in the exploit phase, Then a
    'run chain apt_web_http' intent appears and _steps_for turns it into the
    routable 'apt_chain apt_web_http <target>' command.
    """
    import json

    import modules.chain_match as chain_match
    import modules.killchain as killchain
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain access on 10.0.0.9")["task_id"]
    engine.ensure_target(task_id, "10.0.0.9", "test")
    (tmp_path / "world_model.json").write_text(
        json.dumps({"hosts": {"10.0.0.9": {"services": [{"name": "http", "port": 8080}]}}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "modules.chain_registry.scan_all",
        lambda *a, **k: [
            {"name": "apt_web_http", "enabled": True, "valid": True, "tags": ["web", "http"], "platforms": ["linux"]},
        ],
    )
    monkeypatch.setattr(killchain.KillChain, "current_phase", staticmethod(lambda *a, **k: "exploit"))
    monkeypatch.setattr(loop.Planner, "_os_hint", staticmethod(lambda: "linux"))
    chain_match.reset_cache()

    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    summaries = [row[0] for row in planner._candidates()]
    assert "run chain apt_web_http" in summaries

    node = graph.add_node("intent", "run chain apt_web_http")
    worker = loop.Worker(
        "worker-1", task_id, engine.assets, graph,
        loop.ActivityLog(task_id), loop.TrafficLog(task_id), loop.Guard(task_id), engine.store,
    )
    assert worker._steps_for(node) == ["apt_chain apt_web_http 10.0.0.9"]


def test_failed_chain_step_steers_the_planner(tmp_path, monkeypatch):
    """BDD: an unresolvable chain-step failure becomes a planner intent.

    Given a chain step fails with steer set, When the chain_feed sink
    applies it and the planner builds candidates, Then a steered probe
    intent carrying the failure appears so the autonomous loop regains
    control of the stalled chain instead of dropping it.
    """
    import modules.lazy_loop as loop
    from modules.outcome_bus import OutcomeEvent
    from modules.sinks.chain_feed import apply as chain_feed_apply

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain access on 10.0.0.9")["task_id"]

    event = OutcomeEvent(
        kind="chain_step",
        task_id=task_id,
        target="10.0.0.9",
        description="smb login refused",
        metadata={"run_id": "r1", "chain": "demo", "step_id": "smb", "status": "failed", "steer": True},
    )
    assert chain_feed_apply(event) is True

    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    summaries = [row[0] for row in planner._candidates()]
    assert any(summary.startswith("steered probe:") and "smb" in summary for summary in summaries)


def test_terminal_hint_explains_disposition_to_operator():
    """BDD: terminal dispositions map to plain-language operator guidance."""
    from modules.lazy_engine import terminal_hint

    assert "redirect" in terminal_hint("repetition").lower()
    assert "not" in terminal_hint("timeout").lower()
    assert "budget" in terminal_hint("budget").lower()
    assert terminal_hint("", "exhausted").startswith("intent exhausted")
    assert terminal_hint("", "blocked").startswith("intent blocked")
    assert terminal_hint("unknown-reason", "") == ""


def test_intent_priority_claim_pause_resume(tmp_path, monkeypatch):
    """BDD: the frontier claims strictly by priority then id."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    low = engine.add_intent(task_id, "low probe", priority=3)
    high = engine.add_intent(task_id, "high probe", priority=9)
    graph = loop.ExplorationGraph(task_id)
    claimed = loop.Frontier(graph).claim_next()
    assert claimed is not None
    assert claimed.node_id == high.node_id
    assert engine.store.get(task_id) is not None
    assert engine.pause_intent(task_id, high.node_id) is True
    assert engine.resume_intent(task_id, high.node_id) is True
    assert loop.Frontier(graph).claim_next().node_id == high.node_id
    _ = low


def test_intent_soft_and_hard_delete(tmp_path, monkeypatch):
    """BDD: soft delete keeps outputs, hard delete cascades exclusives."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    soft = engine.add_intent(task_id, "remove me softly")
    hard = engine.add_intent(task_id, "remove me hard")
    graph = loop.ExplorationGraph(task_id)
    fact = graph.add_node("fact", "exclusive output", state="done")
    graph.add_edge(hard.node_id, fact.node_id, "yields")
    assert engine.delete_intent(task_id, soft.node_id, mode="soft",
                                reason="operator")["mode"] == "soft"
    graph.reload()
    assert graph.get(soft.node_id).state == "deleted"
    preview = engine.preview_delete_intent(task_id, hard.node_id)
    assert fact.node_id in preview["removable"]
    engine.delete_intent(task_id, hard.node_id, mode="hard", reason="operator")
    graph.reload()
    assert graph.get(hard.node_id) is None
    assert graph.get(fact.node_id) is None


def test_guard_judge_parse_and_fail_policy(tmp_path, monkeypatch):
    """BDD: judge JSON is strict and LLM outages apply the fail policy."""
    import modules.lazy_loop as loop

    parsed = loop.parse_judge_output('```json\n{"decision": "DENY", "comment": "wipes disk"}\n```')
    assert parsed == {"decision": "DENY", "comment": "wipes disk"}
    assert loop.parse_judge_output("nope") == {}
    assert loop.parse_judge_output('{"decision": "MAYBE", "comment": "x"}') == {}
    assert loop.parse_judge_output('{"decision": "ALLOW"}') == {}
    _patched_engine(tmp_path, monkeypatch)
    allow = loop.judge_command("rm -rf /", fail_action="allow")
    assert allow["decision"] == "ALLOW"
    assert allow["source"] == "fail_policy"
    deny = loop.judge_command("rm -rf /", fail_action="deny")
    assert deny["decision"] == "DENY"


def test_guard_judge_gates_when_enabled(tmp_path, monkeypatch):
    """BDD: with the judge on, unmatched commands follow the fail policy."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    (tmp_path / f"guard_rules_{task_id}.json").write_text(json.dumps({
        "rules": [],
        "judge": {"enabled": True, "fail_action": "deny"},
    }), encoding="utf-8")
    guard = loop.Guard(task_id)
    blocked = guard.check("Bash", "some ambiguous command", source="worker")
    assert blocked["action"] == "deny"
    assert blocked["source"] == "fail_policy"
    (tmp_path / f"guard_rules_{task_id}.json").write_text(json.dumps({"rules": []}),
                                                          encoding="utf-8")
    open_guard = loop.Guard(task_id)
    assert open_guard.check("Bash", "some ambiguous command")["action"] == "allow"


def test_guard_set_judge_persists_and_gates(tmp_path, monkeypatch):
    """BDD: lazy_guard judge on persists the config and gates immediately."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    guard = loop.Guard(task_id)
    assert guard.judge == {}
    config = guard.set_judge(True, fail_action="deny")
    assert config == {"enabled": True, "fail_action": "deny"}
    reloaded = loop.Guard(task_id)
    assert reloaded.judge == {"enabled": True, "fail_action": "deny"}
    assert reloaded.check("Bash", "ambiguous unmatched thing")["action"] == "deny"
    assert reloaded.set_judge(False, fail_action="allow") == {"enabled": False,
                                                              "fail_action": "allow"}
    assert loop.Guard(task_id).check("Bash", "ambiguous unmatched thing")["action"] == "allow"
    try:
        guard.set_judge(True, fail_action="bogus")
    except ValueError:
        pass
    else:
        raise AssertionError("bogus fail action must raise")


def test_finding_evidence_version_and_report(tmp_path, monkeypatch):
    """BDD: evidence binding and report writes bump the version."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    traffic = loop.TrafficLog(task_id)
    service = loop.FindingService(task_id, graph, loop.ActivityLog(task_id), engine.store)
    finding = service.report("sqli in login", summary="error-based", severity="high")
    assert finding.meta["evidence_version"] == 1
    assert traffic.bind(finding.node_id, "aaa111", graph, role="request") is True
    assert graph.get(finding.node_id).meta["evidence_version"] == 2
    assert service.update_report(finding.node_id, "full write-up") == 3
    assert graph.get(finding.node_id).meta["report"] == "full write-up"
    assert service.update_report(finding.node_id, "   ") == 0


def test_skills_match_inject_and_prompt_context(tmp_path, monkeypatch):
    """BDD: skills match by keyword, pin on the task and reach the prompt."""
    import modules.lazy_loop as loop
    import modules.lazy_skills as skills

    skill_dir = tmp_path / "skills" / "smb"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: smb-playbook\ndescription: SMB enumeration guide\n---\n"
        "# SMB\nEnumerate shares with smbclient and nxc.\n", encoding="utf-8")
    monkeypatch.setattr(skills, "SKILLS_DIR", tmp_path / "skills")
    skills._CACHE.clear()
    matches = skills.match_skills("enumerate smb shares")
    assert matches and matches[0]["name"] == "smb-playbook"
    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("enumerate smb shares")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    context = loop.build_prompt_context(task_id, graph, engine.assets, engine.store,
                                        budget=1500)
    assert "smb-playbook" in context
    state = engine.store.set_skills(task_id, ["smb-playbook"], auto=False)
    assert state["skills"] == ["smb-playbook"]
    assert state["skills_auto"] is False


def test_custom_tools_run_and_loop_wiring(tmp_path, monkeypatch):
    """BDD: custom tools execute and surface as planner/worker intents."""
    import modules.custom_tools as tools
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    entry = tools.add_tool("greet", "command", "printf hello-{arg}",
                           description="greet target smb")
    assert entry["kind"] == "command"
    assert "hello-10.0.0.5" in tools.run_tool("greet", "10.0.0.5")
    assert tools.match_tools("run greet on smb target")[0]["name"] == "greet"
    task_id = engine.create_task("greet smb target 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id),
                           engine.store)
    summaries = [row[0] for row in planner._candidates()]
    assert any(summary.startswith("custom tool greet") for summary in summaries)
    intent = graph.add_node("intent", "custom tool greet 127.0.0.1")
    worker = loop.Worker("worker-1", task_id, engine.assets, graph,
                         loop.ActivityLog(task_id), loop.TrafficLog(task_id),
                         loop.Guard(task_id), engine.store)
    assert worker._steps_for(intent) == ["custom tool greet 127.0.0.1"]
    assert "hello-127.0.0.1" in worker._run("custom tool greet 127.0.0.1", None)
    assert tools.remove_tool("greet") is True


def test_workspace_confined_io(tmp_path, monkeypatch):
    """BDD: workspace IO works inside the root and blocks traversal."""
    import modules.workspace as ws
    from modules.auto_registry import is_routable_command

    monkeypatch.setattr(ws, "WORKSPACE_ROOT", tmp_path / "ws")
    assert ws.write_text("notes/a.txt", "hello") == 5
    assert ws.read_text("notes/a.txt") == "hello"
    assert [entry["name"] for entry in ws.list_entries("notes")] == ["a.txt"]
    ws.make_dir("loot")
    assert any(entry["name"] == "loot" for entry in ws.list_entries())
    assert ws.remove("notes/a.txt") is True
    assert ws.remove("notes/a.txt") is False
    for bad in ("../escape.txt", "/etc/passwd"):
        try:
            ws.resolve(bad)
        except PermissionError:
            pass
        else:
            raise AssertionError(f"traversal allowed: {bad}")
    assert is_routable_command("lazy_workspace read notes/a.txt")


def test_selfupdate_check_and_apply(tmp_path, monkeypatch):
    """BDD: selfupdate fast-forwards a clean clone and refuses dirty ones."""
    import subprocess

    import modules.selfupdate as su

    def git(cwd, *args):
        return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                              text=True)

    origin = tmp_path / "origin.git"
    git(tmp_path, "init", "--bare", str(origin))
    work = tmp_path / "work"
    git(tmp_path, "clone", str(origin), str(work))
    git(work, "config", "user.email", "t@example.com")
    git(work, "config", "user.name", "tester")
    (work / "a.txt").write_text("one")
    git(work, "add", ".")
    git(work, "commit", "-m", "one")
    git(work, "branch", "-M", "dev")
    git(work, "push", "-u", "origin", "dev")
    other = tmp_path / "other"
    git(tmp_path, "clone", "-b", "dev", str(origin), str(other))
    git(other, "config", "user.email", "t@example.com")
    git(other, "config", "user.name", "tester")
    (other / "b.txt").write_text("two")
    git(other, "add", ".")
    git(other, "commit", "-m", "two")
    git(other, "push")
    monkeypatch.setattr(su, "BASE_DIR", work)
    info = su.check("dev")
    assert info["ok"] and info["behind"] == 1
    assert su.apply("dev", confirm=False)["applied"] is False
    assert su.apply("dev", confirm=True)["applied"] is True
    assert (work / "b.txt").exists()
    assert su.check("dev")["behind"] == 0
    (work / "a.txt").write_text("dirty")
    assert su.apply("dev", confirm=True)["applied"] is False


def test_c2_board_bridge_upserts(tmp_path, monkeypatch):
    """BDD: loop tasks mirror into the C2 Kanban board without duplicates."""
    import modules.lazy_bridge as bridge

    engine = _patched_engine(tmp_path, monkeypatch)
    monkeypatch.setattr(bridge, "LAZY_DIR", tmp_path)
    monkeypatch.setattr(bridge, "SESSIONS_DIR", tmp_path / "sessions")
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    board_file = tmp_path / "sessions" / "tasks.json"
    board = json.loads(board_file.read_text(encoding="utf-8"))
    assert len(board) == 1
    assert board[0]["status"] == "Started"
    assert board[0]["operator"] == "lazy_loop"
    assert task_id in board[0]["title"]
    engine.store.set_status(task_id, "done")
    out = bridge.push_tasks_to_c2()
    assert out["updated"] == 1
    board = json.loads(board_file.read_text(encoding="utf-8"))
    assert len(board) == 1
    assert board[0]["status"] == "Done"
    assert (tmp_path / "sessions" / "lazy_bridge_c2_map.json").exists()


def test_report_export_md_csv_and_terminal_trigger(tmp_path, monkeypatch):
    """BDD: reports render to md/csv and a terminal run writes one."""
    from pathlib import Path

    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    loop.FindingService(task_id, graph, loop.ActivityLog(task_id), engine.store).report(
        "rce in upload", summary="unauthenticated", severity="critical")
    md = engine.export_findings_report(task_id, fmt="md")
    assert md["findings"] == 1
    assert "rce in upload" in Path(md["path"]).read_text(encoding="utf-8")
    csv_out = tmp_path / "findings.csv"
    result = engine.export_findings_report(task_id, path=str(csv_out), fmt="csv")
    assert result["format"] == "csv"
    text = csv_out.read_text(encoding="utf-8")
    assert "critical" in text and "rce in upload" in text
    engine.run(task_id, max_rounds=1, workers=1, executor=lambda command: "ok\n")
    auto = [p for p in tmp_path.iterdir() if p.name.startswith(f"report_{task_id}")]
    assert auto


def test_trigger_task_create_fires_once(tmp_path, monkeypatch):
    """BDD: the task_create trigger reports new tasks exactly once."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    store = loop.TriggerStore("")
    store.add("task_create")
    engine.create_task("first task")
    graph = loop.ExplorationGraph("t0001")
    activity = loop.ActivityLog("t0001")
    first = store.due("", graph, activity, store=engine.store)
    assert any(hit["kind"] == "task_create" and "t0001" in hit["ids"] for hit in first)
    second = store.due("", graph, activity, store=engine.store)
    assert not any(hit["kind"] == "task_create" for hit in second)
    engine.create_task("second task")
    third = store.due("", graph, activity, store=engine.store)
    assert any(hit["kind"] == "task_create" and hit.get("ids") == ["t0002"]
               for hit in third)


def test_notifier_channels_slack_email_file(tmp_path, monkeypatch):
    """BDD: slack/email/file channels deliver with severity floors."""
    import smtplib
    import urllib.parse as urlparse

    import modules.lazy_loop as loop
    import modules.notify as notify_module

    engine = _patched_engine(tmp_path, monkeypatch)
    monkeypatch.setattr(notify_module, "url_allowed", lambda url: (True, "ok"))
    sent: list[tuple[str, bytes]] = []

    def fake_post(url, data, timeout=8):
        sent.append((url, data))

    monkeypatch.setattr(notify_module, "post_url_validated", fake_post)
    smtp_calls: list[tuple] = []

    class _Smtp:
        def __init__(self, host, port, timeout=10):
            smtp_calls.append(("connect", host, port))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def starttls(self):
            smtp_calls.append(("tls",))

        def login(self, user, password):
            smtp_calls.append(("login", user, password))

        def send_message(self, message):
            smtp_calls.append(("send", message["To"], message["Subject"]))

    monkeypatch.setattr(smtplib, "SMTP", _Smtp)
    notifier = loop.Notifier(engine.store)
    notifier.add_channel("slack", "https://hooks.example/T1", min_severity="medium")
    notifier.add_channel("email", "smtp.example:587", min_severity="high",
                         extra={"to": "ops@example.com", "from_addr": "lazy@example.com",
                                "user": "bot", "password": "secret"})
    file_target = tmp_path / "notify.jsonl"
    notifier.add_channel("file", str(file_target))
    low = notifier.emit("t0001", "finding_created", {"severity": "low", "name": "x"})
    assert low == 1
    assert file_target.exists()
    high = notifier.emit("t0001", "finding_created", {"severity": "high", "name": "y"})
    assert high == 3

    def _is_hooks_url(url: str) -> bool:
        try:
            parts = urlparse.urlsplit(url)
        except ValueError:
            return False
        if parts.username or parts.password:
            return False
        return parts.scheme == "https" and (parts.hostname or "").lower() == "hooks.example"

    assert any(_is_hooks_url(url) and b'"text"' in data for url, data in sent)
    assert _is_hooks_url("https://hooks.example/T1") is True
    assert _is_hooks_url("https://user:pass@hooks.example/T1") is False
    assert _is_hooks_url("https://hooks.example.evil.com/T1") is False
    assert _is_hooks_url("http://hooks.example/T1") is False
    assert any(call[0] == "send" and call[1] == "ops@example.com" for call in smtp_calls)
    assert notifier.remove_channel(1) is True
    assert len(notifier.channels()) == 2
    assert notifier.remove_channel(9) is False


def test_task_status_notification_on_terminal(tmp_path, monkeypatch):
    """BDD: terminal tasks fan out a task_status event to channels."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    target = tmp_path / "events.jsonl"
    loop.Notifier(engine.store).add_channel("file", str(target))
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    engine.run(task_id, max_rounds=1, workers=1,
               executor=lambda command: "80/tcp open http\n")
    assert "task_status" in target.read_text(encoding="utf-8")


def test_admission_queue_fifo_and_drain(tmp_path, monkeypatch):
    """BDD: capped engines queue tasks FIFO and drain them when slots free."""

    engine = _patched_engine(tmp_path, monkeypatch)
    running = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    second = engine.create_task("gain initial access on 127.0.0.2")["task_id"]
    third = engine.create_task("gain initial access on 127.0.0.3")["task_id"]
    engine.store.set_status(running, "running")
    engine.set_concurrency(1)
    stub = lambda command: "80/tcp open http\n"  # noqa: E731
    blocked = engine.run(second, max_rounds=1, workers=1, executor=stub)
    assert blocked["status"] == "queued"
    blocked_third = engine.run(third, max_rounds=1, workers=1, executor=stub)
    assert blocked_third["status"] == "queued"
    assert [task["task_id"] for task in engine.store.queue()] == [second, third]
    engine.store.set_status(running, "done")
    drained = engine.drain_queue(max_tasks=1)
    assert [item["task_id"] for item in drained] == [second]
    assert engine.store.get(second)["status"] != "queued"
    assert [task["task_id"] for task in engine.store.queue()] == [third]
    engine.set_concurrency(0)
    drained_rest = engine.drain_queue(max_tasks=2)
    assert [item["task_id"] for item in drained_rest] == [third]


def test_build_prompt_context_bounded_with_digests(tmp_path, monkeypatch):
    """BDD: prompt context caps size and surfaces digests over raw facts."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    for index in range(40):
        graph.add_node("fact", f"fact number {index} with some longer body text", state="done")
    digest = graph.add_node("fact", "cold digest: facts 0-10 summarized",
                            state="done", meta={"cold_digest": True, "members": list(range(10))})
    context = loop.build_prompt_context(task_id, graph, engine.assets, engine.store, budget=600)
    assert len(context) <= 600
    assert "Digests:" in context
    assert digest.text[:40] in context
    assert context.count("fact number") <= 8


def test_record_verdict_manual(tmp_path, monkeypatch):
    """BDD: an operator verdict is stored and fixed closes the finding."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    service = loop.FindingService(task_id, graph, loop.ActivityLog(task_id), engine.store)
    finding = service.report("weak tls", summary="tls 1.0")
    result = engine.record_verdict(task_id, finding.node_id, "fixed", note="patched")
    assert result["verdict"] == "fixed"
    graph.reload()
    stored = graph.get(finding.node_id)
    assert stored.meta["status"] == "fixed"
    assert stored.meta["retest"]["source"] == "operator"
    try:
        engine.record_verdict(task_id, finding.node_id, "bogus")
    except ValueError:
        pass
    else:
        raise AssertionError("bogus verdict must raise")


def test_broadcast_rows_and_worker_traces(tmp_path, monkeypatch):
    """BDD: the engine broadcast board and traces back the same graph."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = engine.add_intent(task_id, "probe host")
    fact = graph.add_node("fact", "open port 445", state="done")
    graph.add_edge(intent.node_id, fact.node_id, "yields")
    page = engine.broadcast(task_id)
    ids = {row["id"] for row in page["items"]}
    assert {intent.node_id, fact.node_id} <= ids
    filtered = engine.broadcast(task_id, query=f"#{fact.node_id}")
    assert filtered["total"] == 1
    kind_page = engine.broadcast(task_id, kinds=["fact"])
    assert all(row["kind"] == "fact" for row in kind_page["items"])
    log = loop.ActivityLog(task_id)
    log.emit("worker-1", "tool", "nmap scan open 445", intent_id=intent.node_id)
    log.emit("worker-1", "result", "smb signing disabled", intent_id=intent.node_id)
    hits = log.search_all("nmap")
    assert len(hits) == 1
    flow = log.trace(intent.node_id)
    kinds = [step["kind"] for step in flow["steps"]]
    assert "tool" in kinds and "result" in kinds


def test_bridge_reads_engine_store_fixture(tmp_path, monkeypatch):
    """BDD: the bridge reads one engine-shaped fixture without real sessions."""
    import modules.lazy_bridge as bridge

    (tmp_path / "tasks.json").write_text(json.dumps(
        {"tasks": {"t0001": {"status": "running", "goal": "engage"}}}), encoding="utf-8")
    (tmp_path / "assets.json").write_text(json.dumps(
        {"nodes": [{"asset_id": 1, "kind": "ip", "value": "127.0.0.1"}]}), encoding="utf-8")
    (tmp_path / "exp_t0001.json").write_text(json.dumps(
        {"nodes": [{"node_id": 1, "kind": "fact", "text": "open 80"}],
         "edges": [], "anchors": []}), encoding="utf-8")
    (tmp_path / "activity_t0001.jsonl").write_text(
        json.dumps({"worker": "planner", "kind": "intent", "text": "probe"}) + "\n",
        encoding="utf-8")
    (tmp_path / "traffic_t0001.jsonl").write_text(
        json.dumps({"kind": "bash", "command": "nmap -sV", "output": "80/tcp open http"}) + "\n",
        encoding="utf-8")
    (tmp_path / "guard_audit_t0001.jsonl").write_text(
        json.dumps({"tool": "Bash", "action": "allow"}) + "\n", encoding="utf-8")
    monkeypatch.setattr(bridge, "LAZY_DIR", tmp_path)
    monkeypatch.setattr(bridge, "SESSIONS_DIR", tmp_path)
    status = bridge.bridge_status()
    assert status["exists"] is True
    assert status["tasks"] == 1
    assert status["per_task"]["t0001"]["graph_nodes"] == 1
    graph = bridge.lazy_graph("t0001")
    assert any(node.get("kind") == "fact" for node in graph.get("nodes", []))
    assert len(bridge.lazy_activity("t0001")) == 1
    assert len(bridge.lazy_traffic("t0001")) == 1
    assert len(bridge.lazy_guard_audit("t0001")) == 1


def test_delete_task_sweeps_store_files(tmp_path, monkeypatch):
    """BDD: deleting a task removes its files and leaves siblings intact."""
    engine = _patched_engine(tmp_path, monkeypatch)
    first = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    second = engine.create_task("gain initial access on 127.0.0.2")["task_id"]
    result = engine.delete_task(first)
    assert result["deleted"] is True
    assert result["removed"]
    assert engine.store.get(first) is None
    assert engine.store.get(second) is not None
    assert engine.delete_task("t9999") == {"deleted": False, "removed": []}


def test_lazy_command_set_registered():
    import ast
    from pathlib import Path

    source = (Path(__file__).resolve().parent.parent / "cli" / "commands" / "lazyloop.py").read_text(
        encoding="utf-8")
    tree = ast.parse(source)
    methods = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    for name in ("do_lazy_sync", "do_lazy_intents", "do_lazy_delete",
                 "do_lazy_findings", "do_lazy_verdict", "do_lazy_mention",
                 "do_lazy_approve"):
        assert name in methods
    for name in ("do_lazy_status", "do_lazy_broadcast", "do_lazy_trace",
                 "do_lazy_hint", "do_lazy_steer", "do_lazy_kill",
                 "do_lazy_retest"):
        assert name not in methods
    assert "LazyQueueCommandSet" in source
    assert "LazyOwnCommandSet" in source


def test_mcp_lazy_handlers_registered():
    from pathlib import Path

    source = (Path(__file__).resolve().parent.parent / "skills" / "lazyown_mcp.py").read_text(
        encoding="utf-8")
    for name in ("lazyown_lazy_status", "lazyown_lazy_sync", "lazyown_lazy_board",
                 "lazyown_lazy_trace", "lazyown_lazy_hint", "lazyown_lazy_finding"):
        assert name in source


def test_mcp_lazy_tools_declared_for_every_handler():
    """BDD: every registered lazy handler is declared in list_tools."""
    import re
    from pathlib import Path

    source = (Path(__file__).resolve().parent.parent / "skills" / "lazyown_mcp.py").read_text(
        encoding="utf-8")
    handlers = set(re.findall(r'register_handler\("(lazyown_lazy_[a-z_]+)"\)', source))
    declared = set(re.findall(r'name="(lazyown_lazy_[a-z_]+)"', source))
    assert handlers, "no lazy handlers found"
    assert handlers <= declared, f"undeclared lazy tools: {sorted(handlers - declared)}"
