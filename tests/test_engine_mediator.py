"""Engine mediator contract tests.

The loop must reach the three engines (autonomous exploit, reactive,
chain reasoning) only through the ``loop.engines`` mediator: these tests
lock the routing, the graceful degradation and the lazy-import
monkeypatch seam.
"""

from __future__ import annotations

from types import SimpleNamespace

from modules.mediation import MediationDomains, default_hub, get_hub
from modules.mediation.contracts import resolve
from modules.mediation.engine_mediator import EngineMediator


class TestRouting:
    """The hub routes the engine domain to the engine mediator."""

    def test_engine_domain_registered_in_default_hub(self):
        hub = default_hub()
        mediator = hub.mediator_for(MediationDomains.ENGINES)
        assert isinstance(mediator, EngineMediator)

    def test_resolve_returns_engine_mediator(self):
        assert isinstance(resolve(MediationDomains.ENGINES), EngineMediator)

    def test_domain_key_in_all_contract(self):
        assert "loop.engines" in MediationDomains.ALL

    def test_describe_shape(self):
        described = EngineMediator().describe()
        assert described["domain"] == "loop.engines"
        assert "exploit_retry" in described["ports"]
        assert "autonomous_exploit_engine" in described["engines"]


class TestRetryPort:
    """Credential reuse degrades to zero when the engine fails."""

    def test_retry_counts_queued_credentials(self, monkeypatch):
        import modules.autonomous_exploit_engine as aee

        captured = {}

        class FakeEngine:
            @staticmethod
            def get_instance():
                return SimpleNamespace(
                    retry_with_credentials=lambda target, credentials: captured.update(
                        {"target": target, "count": len(credentials)}
                    )
                )

        monkeypatch.setattr(aee, "AutonomousExploitEngine", FakeEngine)
        mediator = EngineMediator()
        assert mediator.retry_with_credentials("10.10.11.5", [{"user": "a", "password": "b"}]) == 1
        assert captured["target"] == "10.10.11.5"

    def test_retry_without_credentials_is_zero(self):
        assert EngineMediator().retry_with_credentials("10.10.11.5", []) == 0

    def test_retry_engine_import_failure_is_zero(self, monkeypatch):
        import modules.autonomous_exploit_engine as aee

        monkeypatch.setattr(aee, "AutonomousExploitEngine", None)
        assert EngineMediator().retry_with_credentials("10.10.11.5", [{"user": "a"}]) == 0


class TestReactionPort:
    """Reactive analysis returns decisions or degrades to empty."""

    def test_analyse_returns_engine_decisions(self, monkeypatch):
        import modules.reactive_engine as re_

        decision = SimpleNamespace(command="ls", reason="r", priority=1, mitre_tactic="t")
        monkeypatch.setattr(re_, "get_engine", lambda: SimpleNamespace(analyse=lambda **kw: [decision]))
        decisions = EngineMediator().analyse("output", "cmd", "linux")
        assert decisions == [decision]

    def test_analyse_engine_failure_is_empty(self, monkeypatch):
        import modules.reactive_engine as re_

        def boom():
            raise RuntimeError("engine down")

        monkeypatch.setattr(re_, "get_engine", boom)
        assert EngineMediator().analyse("output", "cmd", "linux") == []


class TestReasoningPort:
    """Chain strategy reasoning degrades to None."""

    def test_reason_without_target_is_none(self):
        assert EngineMediator().reason("") is None

    def test_reason_engine_failure_is_none(self, monkeypatch):
        import modules.ai_exploit_chain as aec

        def boom(*args, **kwargs):
            raise RuntimeError("chainer down")

        monkeypatch.setattr(aec, "AIExploitChainer", boom)
        assert EngineMediator().reason("10.10.11.5") is None


class TestLoopMediatedEdge:
    """The loop file no longer imports the engines at module scope."""

    def test_lazy_loop_module_has_no_direct_engine_import(self):
        import inspect

        import modules.lazy_loop as lazy_loop

        source = inspect.getsource(lazy_loop)
        assert "from modules.autonomous_exploit_engine import" not in source
        assert "from modules.reactive_engine import" not in source

    def test_shared_hub_serves_engine_domain(self):
        assert get_hub().mediator_for(MediationDomains.ENGINES) is not None
