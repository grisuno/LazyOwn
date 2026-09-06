"""Behavioural tests for the resurrected ``ask``/``groq`` commands.

Pins the functional gap closure: ``do_ask`` answers through the configured
``llm_backend`` and ``do_groq`` through the explicit Groq backend, both
in-process via the canonical factory/adapter contracts. No subprocess, no
network, no shell is exercised.
"""

from __future__ import annotations

from types import SimpleNamespace

import cli.commands.ai as ai_module
from modules.llm_factory import LLMBackendUnavailableError


def _command_set(**attrs):
    instance = ai_module.AiCommandSet.__new__(ai_module.AiCommandSet)
    shell = SimpleNamespace(params={}, path="/tmp/lazyown-test", prompt="(test) > ")
    for key, value in attrs.items():
        setattr(shell, key, value)
    instance._resolve_shell = lambda: shell
    return instance


class TestDoAsk:
    def test_empty_question_prints_usage(self, monkeypatch):
        errors: list = []
        monkeypatch.setattr(ai_module, "print_error", errors.append)
        _command_set().do_ask("   ")
        assert errors and "Usage" in errors[0]

    def test_question_forwarded_with_session_context(self, monkeypatch):
        seen: list = []
        shown: list = []
        monkeypatch.setattr(ai_module, "ask_general", lambda prompt: seen.append(prompt) or "answer")
        monkeypatch.setattr(ai_module, "print_msg", shown.append)
        cmd = _command_set(params={"rhost": "10.0.0.9", "lhost": "10.0.0.1"})
        cmd.do_ask("best privesc path?")
        assert len(seen) == 1
        assert "Operator question: best privesc path?" in seen[0]
        assert "10.0.0.9" in seen[0]
        assert "answer" in shown

    def test_backend_error_surfaces_as_message(self, monkeypatch):
        shown: list = []
        monkeypatch.setattr(ai_module, "ask_general", lambda prompt: "Error: no backend")
        monkeypatch.setattr(ai_module, "print_msg", shown.append)
        _command_set().do_ask("hello")
        assert shown[-1] == "Error: no backend"


class TestDoGroq:
    def test_unavailable_backend_prints_actionable_error(self, monkeypatch):
        errors: list = []

        def _raise(**kwargs):
            raise LLMBackendUnavailableError("no key")

        monkeypatch.setattr(ai_module, "get_llm_backend", _raise)
        monkeypatch.setattr(ai_module, "print_error", errors.append)
        _command_set().do_groq("list files")
        assert errors
        assert "assign api_key" in errors[0]

    def test_success_completes_oneliner_and_prints(self, monkeypatch):
        calls: dict = {}
        shown: list = []
        seen_kwargs: dict = {}

        class _Backend:
            def complete(self, system, user, **kwargs):
                calls["system"] = system
                calls["user"] = user
                return "ls -la"

        def _factory(**kwargs):
            seen_kwargs.update(kwargs)
            return _Backend()

        monkeypatch.setattr(ai_module, "get_llm_backend", _factory)
        monkeypatch.setattr(ai_module, "print_msg", shown.append)
        cmd = _command_set(params={"llm_model_groq": "llama3-8b-8192"})
        cmd.do_groq("list files")
        assert seen_kwargs.get("backend") == "groq"
        assert "list files" in calls["user"]
        assert "ls -la" in shown
        assert any("llama3-8b-8192" in message for message in shown)

    def test_completion_failure_prints_error(self, monkeypatch):
        errors: list = []

        class _Backend:
            def complete(self, system, user, **kwargs):
                raise RuntimeError("down")

        monkeypatch.setattr(ai_module, "get_llm_backend", lambda **kwargs: _Backend())
        monkeypatch.setattr(ai_module, "print_error", errors.append)
        monkeypatch.setattr(ai_module, "print_msg", lambda message: None)
        _command_set().do_groq("list files")
        assert errors and "groq request failed" in errors[0]

    def test_empty_line_falls_back_to_shell_prompt(self, monkeypatch):
        calls: list = []

        class _Backend:
            def complete(self, system, user, **kwargs):
                calls.append(user)
                return "ok"

        monkeypatch.setattr(ai_module, "get_llm_backend", lambda **kwargs: _Backend())
        monkeypatch.setattr(ai_module, "print_msg", lambda message: None)
        cmd = _command_set(prompt="fallback goal")
        cmd.do_groq("")
        assert calls and "fallback goal" in calls[0]
