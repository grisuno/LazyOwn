"""Tests for the reproducible loop mode that prefers heuristic steps.

Deterministic mode must make the heuristic, evidence-based steps win over the
LLM so an identical engagement state replays the same primary action, while
still falling back to the model when scope is missing and the heuristic only
produced a placeholder. Default mode must keep its LLM-augmented ordering.
"""

from __future__ import annotations

import types

import modules.loop.worker_agentic as wa
from modules.loop.worker_agentic import WorkerAgenticMixin, _is_placeholder_steps


class _Activity:
    """Record emitted activity lines for assertions."""

    def __init__(self):
        self.events = []

    def emit(self, *args, **kwargs):
        self.events.append((args, kwargs))


class _Worker(WorkerAgenticMixin):
    """Minimal host exposing only what ``_with_llm_steps`` touches."""

    def __init__(self, suggested):
        self.name = "worker-test"
        self.activity = _Activity()
        self._suggested = list(suggested)

    def _llm_steps(self, intent, prior_text=""):
        return list(self._suggested)


def _intent():
    return types.SimpleNamespace(node_id=1, text="probe http surface")


def test_is_placeholder_detects_no_target():
    assert _is_placeholder_steps([]) is True
    assert _is_placeholder_steps(["echo no-target: register scope"]) is True
    assert _is_placeholder_steps(["nmap -sV 10.0.0.1"]) is False


def test_default_mode_prefixes_llm(monkeypatch):
    monkeypatch.setattr(wa, "_loop_deterministic", lambda: False)
    worker = _Worker(["curl http://t/"])
    out = worker._with_llm_steps(_intent(), ["ping t", "nmap t"])
    assert out[0] == "curl http://t/"
    assert "ping t" in out and "nmap t" in out


def test_deterministic_mode_heuristic_wins_and_skips_model(monkeypatch):
    monkeypatch.setattr(wa, "_loop_deterministic", lambda: True)
    worker = _Worker(["curl http://attacker/"])
    out = worker._with_llm_steps(_intent(), ["ping t", "nmap -sV t"])
    assert out == ["ping t", "nmap -sV t"]
    assert any(args[1] == "deterministic" for args, _ in worker.activity.events)


def test_deterministic_mode_falls_back_to_model_on_placeholder(monkeypatch):
    monkeypatch.setattr(wa, "_loop_deterministic", lambda: True)
    worker = _Worker(["curl http://t/"])
    out = worker._with_llm_steps(_intent(), ["echo no-target: register scope first"])
    assert "curl http://t/" in out


def test_deterministic_fallback_orders_heuristic_first(monkeypatch):
    monkeypatch.setattr(wa, "_loop_deterministic", lambda: True)

    class _PlaceholderThenReal(_Worker):
        def _llm_steps(self, intent, prior_text=""):
            return ["curl http://t/"]

    worker = _PlaceholderThenReal(["curl http://t/"])
    out = worker._with_llm_steps(_intent(), ["echo no-target: x"])
    assert out[-1] == "curl http://t/" or out[0] == "echo no-target: x"


def test_loop_deterministic_reads_payload(monkeypatch):
    import core.config as config

    monkeypatch.setattr(config, "load_payload", lambda: {"loop_deterministic": True})
    assert wa._loop_deterministic() is True
    monkeypatch.setattr(config, "load_payload", lambda: {})
    assert wa._loop_deterministic() is False


def test_loop_deterministic_survives_error(monkeypatch):
    import core.config as config

    def _boom():
        raise RuntimeError("no payload")

    monkeypatch.setattr(config, "load_payload", _boom)
    assert wa._loop_deterministic() is False
