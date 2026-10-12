"""Loop orchestrates every auto verb plus addon/tool triggers."""

from __future__ import annotations


def test_exfil_auto_registered_as_verb():
    from modules import auto_registry as _a

    assert "exfil_auto" in _a.verbs()
    assert _a.is_shell_verb("exfil_auto --method gofile") is True
    assert _a.is_routable_command("exfil_auto --method gofile") is True
    assert _a.steps_for("exfiltrate flags with exfil auto", "") == ["exfil_auto"]


def test_service_tokens_split_and_alias():
    from modules import auto_registry as _a

    tokens = _a.service_tokens("tcp/443 ssl/http")
    assert {"tcp", "443", "ssl", "http", "https"} <= tokens


def test_addon_hits_rank_specific_before_generic():
    from modules import auto_registry as _a

    hits = _a.addon_hits_for("tcp/80 http")
    names = [n for n, _s in hits]
    assert "commix2" in names
    assert "nuclei_templates" in names


def test_propose_addon_intents_shape_and_tool_collapse():
    from modules import auto_registry as _a

    intents = _a.propose_addon_intents(["tcp/80 http"], "10.0.0.1")
    assert intents
    assert all(i.startswith("lazy addon ") or i.startswith("auto pyautomate") for i in intents)
    assert len(intents) <= _a.ADDON_TRIGGER_CAP


def test_steps_for_lazy_addon_routes_to_command():
    from modules import auto_registry as _a

    assert _a.steps_for("lazy addon nuclei_templates 10.0.0.1", "") == [
        "lazy_addon run nuclei_templates --target 10.0.0.1"
    ]
    assert _a.is_routable_command("lazy_addon run nuclei_templates --target 10.0.0.1") is True


def test_worker_routes_verbs_via_bound_shell(tmp_path, monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    seen: list[str] = []

    class _Shell:
        def onecmd(self, command: str) -> None:
            seen.append(command)
            print(f"ran {command}")

    engine.bind_shell(_Shell())
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "auto pyautomate 127.0.0.1")
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
        shell=engine.shell,
    )
    assert worker._steps_for(intent) == ["pyautomate 127.0.0.1"]
    out = worker._run("pyautomate 127.0.0.1", None)
    assert "ran pyautomate 127.0.0.1" in out
    assert seen == ["pyautomate 127.0.0.1"]


def test_worker_without_shell_reports_honestly(tmp_path, monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
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
    out = worker._run("auto_pwn 127.0.0.1", None)
    assert out.startswith("execution failed:")


def test_execute_streaming_streams_and_captures():
    """BDD: bash output arrives line by line and is fully captured."""
    from modules.auto_registry import execute_streaming

    seen: list[str] = []
    output = execute_streaming("printf 'one\\ntwo\\n'", on_output=seen.append, timeout_sec=10)
    assert "one" in output and "two" in output
    assert seen == ["one", "two"]


def test_execute_streaming_timeout_reports():
    """BDD: a hung command is killed and reported as TIMEOUT."""
    from modules.auto_registry import execute_streaming

    output = execute_streaming("sleep 30", timeout_sec=1)
    assert output.startswith("TIMEOUT")


def test_execute_shell_verb_forwards_output():
    """BDD: shell verbs tee captured output to the live observer."""
    from modules.auto_registry import execute_shell_verb

    class _Shell:
        def onecmd_plus_hooks(self, command: str) -> None:
            print("colored line")

    seen: list[str] = []
    out = execute_shell_verb(_Shell(), "auto_pwn 10.0.0.5", timeout_sec=5.0, on_output=seen.append)
    assert "colored line" in out
    assert any("colored line" in chunk for chunk in seen)


def test_autonomous_mode_suppresses_and_restores_input(monkeypatch):
    """BDD: loop mode answers prompts with '' and restores input after."""
    import builtins

    from cli.commands.mcp_bridge import _autonomous_mode

    monkeypatch.setattr(builtins, "input", lambda prompt="": "typed")
    with _autonomous_mode():
        assert builtins.input("confirm?") == ""
    assert builtins.input("confirm?") == "typed"


def test_lazy_addon_command_registered():
    import ast
    from pathlib import Path

    source = (Path(__file__).resolve().parent.parent / "cli" / "commands" / "lazyops.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    methods = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert "do_lazy_addon" in methods


def test_worker_skips_missing_binary_and_records_gap(tmp_path, monkeypatch):
    """A probe whose binary is absent is skipped and explained as a fact."""
    import modules.auto_registry as registry
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(registry, "missing_binary", lambda command: "chisel")
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("probe surface")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
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
    outcome = worker.execute(intent, executor=lambda cmd: "should not run")
    assert outcome["skipped_tools"] == ["chisel"]
    assert outcome["state"] == "blocked"
    gaps = [n for n in graph.list("fact") if n.meta.get("capability_gap") == "chisel"]
    assert gaps


def test_service_trigger_fires_with_addon_hits(tmp_path, monkeypatch):
    """New service assets wake the orchestrator with matched addon names."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("recon surface")["task_id"]
    store = loop.TriggerStore(task_id)
    assert store.ensure_service_trigger() is True
    assert store.ensure_service_trigger() is False
    graph = loop.ExplorationGraph(task_id)
    activity = loop.ActivityLog(task_id)
    assert store.due(task_id, graph, activity, assets=engine.assets) == []
    engine.assets.insert("service", "tcp/80 http")
    fired = store.due(task_id, graph, activity, assets=engine.assets)
    assert fired and fired[0]["kind"] == "service"
    assert "tcp/80 http" in fired[0]["services"]
    assert any("commix2" in name for name in fired[0]["addons"])
    assert store.due(task_id, graph, activity, assets=engine.assets) == []
