"""Token-level streaming: factory, pool deltas, agent reassembly.

The stream stage is exercised with stubbed backends so no network is
touched; the agent test drives the real ``AgentRunner._stream_call``
with an OpenAI-compatible chunk script, including split tool calls.
"""

from __future__ import annotations

from types import SimpleNamespace


def _sandbox(tmp_path, monkeypatch) -> None:
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)


def test_stream_complete_collects_deltas_and_falls_back(monkeypatch):
    """Chunks flow to the sink; error chunks fall back to complete()."""
    import modules.llm_factory as factory

    class _Backend:
        model = "stub"

        def stream_generate(self, prompt):
            yield "hello "
            yield "world"

    monkeypatch.setattr(factory, "get_llm_backend", lambda backend=None: _Backend())
    deltas: list[str] = []
    text = factory.stream_complete("groq:stub", "prompt", on_delta=deltas.append)
    assert text == "hello world"
    assert deltas == ["hello ", "world"]

    class _Broken:
        model = "stub"

        def stream_generate(self, prompt):
            yield "Error streaming from Groq: boom"

    monkeypatch.setattr(factory, "get_llm_backend", lambda backend=None: _Broken())
    monkeypatch.setattr(factory, "complete", lambda model, prompt, max_tokens=800: "fallback")
    assert factory.stream_complete("groq:stub", "prompt") == "fallback"


def test_pool_forwards_deltas_when_stage_on(tmp_path, monkeypatch):
    """LlmPool routes through stream_complete and forwards every delta."""
    _sandbox(tmp_path, monkeypatch)
    import modules.lazy_loop as loop
    import modules.llm_factory as factory
    import modules.loop_ai_bridge as bridge

    monkeypatch.setattr(bridge, "stream_enabled", lambda: True)

    def _stream(model, prompt, max_tokens=800, on_delta=None):
        if on_delta is not None:
            on_delta("part-a")
            on_delta("part-b")
        return "part-apart-b"

    monkeypatch.setattr(factory, "stream_complete", _stream)
    monkeypatch.setattr(factory, "complete", lambda *args, **kwargs: "not-streamed")
    pool = loop.LlmPool()
    pool._health = None
    deltas: list[str] = []
    assert pool.complete("probe", on_delta=deltas.append) == "part-apart-b"
    assert deltas == ["part-a", "part-b"]


def test_pool_stays_unstreamed_when_stage_off(tmp_path, monkeypatch):
    """With the stage off the pool uses the plain completion path."""
    _sandbox(tmp_path, monkeypatch)
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    calls: list[str] = []

    def _stream(*args, **kwargs):
        calls.append("stream")
        return "streamed"

    def _plain(*args, **kwargs):
        calls.append("plain")
        return "plain"

    monkeypatch.setattr(factory, "stream_complete", _stream)
    monkeypatch.setattr(factory, "complete", _plain)
    pool = loop.LlmPool()
    pool._health = None
    assert pool.complete("probe", on_delta=lambda text: None) == "plain"
    assert calls and calls[0] == "plain"


def test_agent_streaming_reassembles_tool_calls_and_reports_deltas():
    """The agent stream call rebuilds split tool calls and emits deltas."""
    import modules.agent_runner as runner_module

    class _Delta:
        def __init__(self, content=None, reasoning=None, tool_calls=None):
            self.content = content
            self.reasoning_content = reasoning
            self.tool_calls = tool_calls

    class _Completions:
        def __init__(self):
            self.requests: list[dict] = []

        def create(self, **kwargs):
            self.requests.append(kwargs)
            assert kwargs.get("stream") is True
            return iter(
                [
                    SimpleNamespace(
                        choices=[
                            SimpleNamespace(
                                delta=_Delta(
                                    content="work",
                                    tool_calls=[
                                        SimpleNamespace(
                                            index=0,
                                            id="call_1",
                                            function=SimpleNamespace(name="run_command", arguments='{"command":'),
                                        )
                                    ],
                                )
                            )
                        ]
                    ),
                    SimpleNamespace(
                        choices=[
                            SimpleNamespace(
                                delta=_Delta(
                                    reasoning="weighing options",
                                    tool_calls=[
                                        SimpleNamespace(
                                            index=0,
                                            id=None,
                                            function=SimpleNamespace(name=None, arguments=' "id"}'),
                                        )
                                    ],
                                )
                            )
                        ]
                    ),
                ]
            )

    completions = _Completions()
    model = SimpleNamespace(client=SimpleNamespace(chat=SimpleNamespace(completions=completions)), model="groq:fake")
    runner = runner_module.AgentRunner(model, "system")
    events: list[tuple[str, str]] = []
    runner.stream_enabled = True
    runner.delta_sink = lambda kind, text: events.append((kind, text))
    runner.conversation_history.append({"role": "user", "content": "hello"})
    response = runner._call_model()
    message = response.choices[0].message
    assert message.content == "work"
    assert message.tool_calls[0].function.name == "run_command"
    assert message.tool_calls[0].function.arguments == '{"command": "id"}'
    assert message.tool_calls[0].id == "call_1"
    assert any(kind == "delta" for kind, _ in events)
    assert any(kind == "think" for kind, _ in events)
