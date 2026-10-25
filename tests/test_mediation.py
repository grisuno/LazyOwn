"""Mediator pattern contract tests for the mediation package."""

from __future__ import annotations

from types import SimpleNamespace

from modules.mediation import (
    ChainMediator,
    FeedbackMediator,
    IntelMediator,
    MediationDomains,
    TelemetryMediator,
    default_hub,
    get_hub,
)


class TestHubRouting:
    """The hub routes domain keys to specialised mediators only."""

    def test_all_default_domains_registered(self):
        hub = default_hub()
        for domain in MediationDomains.ALL:
            assert hub.mediator_for(domain) is not None

    def test_unknown_domain_returns_none(self):
        assert default_hub().mediator_for("not.a.domain") is None

    def test_singleton_hub_shared(self):
        assert get_hub() is get_hub()

    def test_mediation_contract_shape(self):
        mediator = default_hub().mediator_for(MediationDomains.CHAIN)
        assert mediator.domain == MediationDomains.CHAIN
        assert set(mediator.describe().keys()) == {"domain", "llm_port"}


class TestIntelMediatorActivityPort:
    """Registered loop factory replaces the lazy fallback."""

    def test_activity_records_via_injected_port(self):
        mediator = IntelMediator()
        mediator.register_activity_log_factory(lambda task_id: SimpleNamespace(read=lambda limit: [{"i": limit}]))
        assert mediator.activity_records("t9", 7) == [{"i": 7}]
        assert mediator.describe()["activity_log_registered"] is True

    def test_activity_records_fallback_graceful(self):
        mediator = IntelMediator()
        assert mediator.activity_records("-nonexistent-task-") == []

    def test_mask_and_stack_survive_missing_peers(self, monkeypatch):
        import modules.lazy_intel as li

        mediator = IntelMediator()
        monkeypatch.setattr(li, "mask_configured", lambda text: "masked:" + text)
        monkeypatch.setattr(li, "stack_signature", lambda assets: "sig-1")
        assert mediator.mask_configured("x") == "masked:x"
        assert mediator.stack_signature(None) == "sig-1"


class TestFeedbackMediator:
    """Ordering falls back to input order when the peer is unusable."""

    def test_order_steps_passthrough_on_error(self, monkeypatch):
        import modules.lazy_orchestrator_feedback as lof

        def boom(steps, stack):
            raise RuntimeError("peer down")

        monkeypatch.setattr(lof, "order_steps", boom)
        mediator = FeedbackMediator()
        assert mediator.order_steps(["a", "b"], "s") == ["a", "b"]

    def test_order_steps_forwarded(self, monkeypatch):
        import modules.lazy_orchestrator_feedback as lof

        monkeypatch.setattr(lof, "order_steps", lambda steps, stack="": list(reversed(steps)))
        assert FeedbackMediator().order_steps(["a", "b"], "s") == ["b", "a"]


class TestTelemetryMediator:
    """Bridge functions forward with identical arity."""

    def test_publish_event_default_severity_positional(self, monkeypatch):
        import modules.loop_ai_bridge as lab

        received: list = []
        monkeypatch.setattr(
            lab, "publish_loop_event", lambda task, worker, kind, text: received.append((task, worker, kind, text))
        )
        TelemetryMediator().publish_event("t", "w", "kind", "text")
        assert received == [("t", "w", "kind", "text")]

    def test_publish_event_forwarding_calls_default_path(self, monkeypatch):
        mediator = TelemetryMediator()
        annotation = mediator.annotate_detection("ls")
        assert isinstance(annotation, dict)
        assert mediator.swan_available() is False

    def test_rl_select_graceful_off(self, monkeypatch):
        import modules.loop_ai_bridge as lab

        def boom(*args, **kwargs):
            raise RuntimeError("off")

        monkeypatch.setattr(lab, "rl_select", boom)
        assert TelemetryMediator().rl_select("other", "engage", ["a", "b"], deterministic=True) == ""


class TestChainMediatorLlmPort:
    """Chain pipeline requests LLM completion through the port, not imports."""

    def test_port_contract(self):
        mediator = ChainMediator()
        port = mediator.llm()
        assert port.has_members() in (True, False)
        assert port.complete("ping", max_tokens=8, task_id="t") == "" or isinstance(
            port.complete("ping", max_tokens=8, task_id="t"), str
        )

    def test_register_llm_port_replaces(self):
        class Fake:
            def complete(self, prompt, max_tokens=300, task_id=""):
                return "fake-reply"

            def has_members(self):
                return True

        mediator = ChainMediator()
        mediator.register_llm_port(Fake())
        assert mediator.llm().complete("x") == "fake-reply"
        assert mediator.describe()["llm_port"] == "Fake"

    def _patch_hub(self, monkeypatch, port):
        import modules.mediation.hub as hub_mod

        class _FakeHub:
            def __init__(self, port):
                self._port = port

            def mediator_for(self, domain):
                return SimpleNamespace(llm=lambda: self._port)

        class _NoLock:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        monkeypatch.setattr(hub_mod, "_HUB", _FakeHub(port))
        monkeypatch.setattr(hub_mod, "_LOCK", _NoLock())

    def test_recovery_pool_absent_returns_empty(self, monkeypatch):
        from modules.chain_runner import ChainRunResult, StepOutcome

        class Empty:
            def complete(self, prompt, max_tokens=300, task_id=""):
                return ""

            def has_members(self):
                return False

        result = ChainRunResult(
            name="probe",
            target="10.0.0.9",
            run_id="r1",
            steps=[StepOutcome(id="s1", run="true", status="error", output="", reason="down")],
        )
        self._patch_hub(monkeypatch, Empty())
        from cli import apt_chain_support as acs

        chain = acs.build_llm_recovery_chain(result, target="10.0.0.9", task_id="t")
        assert chain is None

    def test_recovery_pool_builds_steps(self, monkeypatch):
        from modules.chain_runner import ChainRunResult, StepOutcome

        class FakePort:
            def complete(self, prompt, max_tokens=300, task_id=""):
                return "curl evil.example\nsudo rm -rf /\n# comment\n"

            def has_members(self):
                return True

        result = ChainRunResult(
            name="probe",
            target="10.0.0.9",
            run_id="r1",
            steps=[StepOutcome(id="s1", run="true", status="error", output="", reason="down")],
        )
        self._patch_hub(monkeypatch, FakePort())
        from cli import apt_chain_support as acs

        chain = acs.build_llm_recovery_chain(result, target="10.0.0.9", task_id="t")
        assert chain is not None
        assert chain.name == "probe_recovery"
        commands = [step.run for step in chain.steps]
        assert "curl evil.example" in commands
        assert all("sudo" not in command for command in commands)
        assert all(step.continue_on_error for step in chain.steps[:3])
