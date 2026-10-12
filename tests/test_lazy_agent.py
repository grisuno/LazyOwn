"""Agentic tool-calling: worker agent path, resume and main sessions.

The model is faked at the client boundary so these tests exercise the
real AgentRunner tool loop, the guard-enforced tool executors and the
conversation persistence without any network or API key.
"""

from __future__ import annotations

from types import SimpleNamespace


def _tool_call(tool_id: str, name: str, arguments: dict) -> object:
    import json

    return SimpleNamespace(id=tool_id, function=SimpleNamespace(name=name, arguments=json.dumps(arguments)))


def _message(content: str = "", tool_calls: list | None = None) -> object:
    return SimpleNamespace(content=content, tool_calls=tool_calls)


class _Completions:
    """Scripted OpenAI-compatible completions endpoint."""

    def __init__(self, script: list) -> None:
        self.script = list(script)
        self.requests: list[dict] = []

    def create(self, **kwargs) -> object:
        """Return the next scripted response, recording the request."""
        self.requests.append(kwargs)
        message = self.script.pop(0) if self.script else _message("stop")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def fake_model(script: list) -> object:
    """Build a raw backend shaped like GroqModel for AgentRunner."""
    completions = _Completions(script)
    return SimpleNamespace(client=SimpleNamespace(chat=SimpleNamespace(completions=completions)), model="groq:fake")


def _sandbox(tmp_path, monkeypatch) -> None:
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)


def _worker(loop, engine, task_id, graph):
    return loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )


def test_worker_agentic_tool_calling(tmp_path, monkeypatch):
    """BDD: the worker calls tools through the guard and persists facts."""
    _sandbox(tmp_path, monkeypatch)
    import modules.lazy_loop as loop
    from modules import lazy_agent
    from modules.lazy_engine import LazyEngine

    model = fake_model(
        [
            _message(tool_calls=[_tool_call("c1", "run_command", {"command": "nmap -sV 127.0.0.1"})]),
            _message(tool_calls=[_tool_call("c2", "record_fact", {"text": "22/tcp open ssh"})]),
            _message("done: ssh open"),
        ]
    )
    monkeypatch.setattr(lazy_agent, "resolve_agentic_model", lambda exclude=None: model)
    monkeypatch.setattr(lazy_agent, "tool_calling_enabled", lambda: True)
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "probe 127.0.0.1")
    ran: list[str] = []

    def _executor(command: str) -> str:
        ran.append(command)
        return "22/tcp open ssh\n80/tcp open http"

    worker = _worker(loop, engine, task_id, graph)
    outcome = worker.execute(intent, executor=_executor)
    assert ran == ["nmap -sV 127.0.0.1"]
    assert outcome["state"] in ("done", "exhausted")
    activity = loop.ActivityLog(task_id)
    kinds = [record.get("kind") for record in activity.for_intent(intent.node_id)]
    assert "agent" in kinds
    assert any(str(kind).startswith("agent-") for kind in kinds)
    assert "tool" in kinds
    facts = [node.text for node in graph.list("fact")]
    assert any("22/tcp open ssh" in text for text in facts)
    convo = lazy_agent.ConversationStore(task_id).intent_messages(intent.node_id)
    assert convo and any(message.get("role") == "tool" for message in convo)


def test_worker_agentic_resume_seeds_prior_turns(tmp_path, monkeypatch):
    _sandbox(tmp_path, monkeypatch)
    from modules import lazy_agent

    first = fake_model(
        [_message(tool_calls=[_tool_call("c1", "record_fact", {"text": "first observation"})]), _message("ok")]
    )
    runner = lazy_agent.run_worker_session(
        model=first,
        task_id="t0001",
        intent_id=7,
        system_prompt="sys",
        launch_prompt="go",
        tools=[
            {
                "name": "record_fact",
                "func": lambda text="": "ok",
                "description": "fact",
                "parameters": {"text": {"type": "string"}},
                "required": ["text"],
            }
        ],
    )
    assert runner["reply"] == "ok"

    second = fake_model([_message("continued")])
    lazy_agent.run_worker_session(
        model=second, task_id="t0001", intent_id=7, system_prompt="sys", launch_prompt="continue", tools=[]
    )
    messages = second.client.chat.completions.requests[0]["messages"]
    assert any(message.get("role") == "tool" for message in messages)
    assert "sys" == messages[0]["content"]


def test_main_session_persists_and_resumes(tmp_path, monkeypatch):
    _sandbox(tmp_path, monkeypatch)
    from modules import lazy_agent

    model = fake_model([_message("hello operator"), _message("still here")])
    lazy_agent.run_main_session(model, "sess1", "system", "hi", tools=[])
    lazy_agent.run_main_session(model, "sess1", "system", "more", tools=[])
    requests = model.client.chat.completions.requests
    contents = [message.get("content") for message in requests[1]["messages"]]
    assert "hello operator" in contents, contents
    sessions = lazy_agent.ConversationStore("").sessions()
    assert [row["session_id"] for row in sessions] == ["sess1"]


def test_model_keepalive_tick_while_waiting(tmp_path, monkeypatch):
    """A slow model call must announce that it is still being awaited."""
    import time as _time

    _sandbox(tmp_path, monkeypatch)
    from modules import lazy_agent

    monkeypatch.setattr(lazy_agent, "MODEL_KEEPALIVE_SEC", 0.1)
    events: list[tuple[str, str, str]] = []

    class _Completions:
        def create(self, **kwargs):
            _time.sleep(0.35)
            message = SimpleNamespace(content="done", tool_calls=None)
            return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    model = SimpleNamespace(client=SimpleNamespace(chat=SimpleNamespace(completions=_Completions())), model="groq:fake")
    lazy_agent.run_main_session(
        model, "s1", "system", "hi", tools=[], on_event=lambda kind, name, text: events.append((kind, name, text))
    )
    assert any("still waiting" in text for _kind, _name, text in events)


def test_tool_calling_flag_honors_payload(tmp_path, monkeypatch):
    _sandbox(tmp_path, monkeypatch)
    import core.config
    from modules import lazy_agent

    monkeypatch.setattr(core.config, "load_payload", lambda: {"agent_tool_calling": False})
    assert lazy_agent.tool_calling_enabled() is False


def test_external_opencode_degrades_without_binary(monkeypatch):
    import shutil as _shutil

    from modules import lazy_agent

    monkeypatch.setattr(_shutil, "which", lambda name: None)
    result = lazy_agent.run_external_opencode("probe")
    assert "not installed" in result["error"]


def test_lazy_agent_command_session_lifecycle(tmp_path, monkeypatch):
    _sandbox(tmp_path, monkeypatch)
    from cli.commands.lazyops import LazyCommandSet
    from modules.lazy_agent import ConversationStore

    command_set = LazyCommandSet()
    command_set.do_lazy_agent("new --title smoke")
    command_set.do_lazy_agent("list")
    assert ConversationStore("").sessions()
