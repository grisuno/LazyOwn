"""Tests for the rescued LazyOwn LLM chat assistant module.

The assistant must load without a live backend, delegate backend
selection to :mod:`modules.llm_factory` (never instantiating a provider
directly), build grounded prompts, and degrade gracefully when no model
is reachable.
"""

import importlib.util
from pathlib import Path

import pytest

_MODULE_PATH = Path(__file__).resolve().parent.parent / "modules" / "lazyllmchat.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("lazyllmchat_under_test", _MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lazyllmchat = _load_module()


class TestPromptBuilder:
    def test_direct_query_includes_system_and_context(self):
        prompt = lazyllmchat.PromptBuilder.for_direct_query("enum smb", "ctx-block")
        assert lazyllmchat.PromptBuilder.SYSTEM in prompt
        assert "ctx-block" in prompt
        assert "enum smb" in prompt

    def test_command_analysis_includes_output(self):
        prompt = lazyllmchat.PromptBuilder.for_command_analysis(
            "lazynmap", "22/tcp open ssh", "ctx", history="prior"
        )
        assert "22/tcp open ssh" in prompt
        assert "prior" in prompt


class TestLLMEngineDelegation:
    def test_uses_factory_not_direct_provider(self, monkeypatch):
        calls = {}

        def fake_try(config=None, backend=None):
            calls["config_seen"] = True
            return None

        monkeypatch.setattr(lazyllmchat, "try_get_llm_backend", fake_try)
        monkeypatch.setattr(lazyllmchat, "load_payload", lambda: {"llm_backend": "opencode"})
        engine = lazyllmchat.LLMEngine()
        assert calls.get("config_seen") is True
        assert engine.is_ready() is False

    def test_ask_without_backend_returns_guidance(self):
        engine = lazyllmchat.LLMEngine.__new__(lazyllmchat.LLMEngine)
        engine.model = None
        engine.history = []
        engine.max_history = lazyllmchat.MAX_HISTORY_TURNS
        message = engine.ask("hello")
        assert "llm_backend" in message

    def test_ask_records_history_and_truncates(self, monkeypatch):
        class _Stub:
            def generate(self, prompt):
                return "answer"

        engine = lazyllmchat.LLMEngine.__new__(lazyllmchat.LLMEngine)
        engine.model = _Stub()
        engine.history = []
        engine.max_history = 2
        for _ in range(5):
            engine.ask("q")
        assert len(engine.history) == 2

    def test_ask_survives_backend_error(self):
        class _Boom:
            def generate(self, prompt):
                raise RuntimeError("down")

        engine = lazyllmchat.LLMEngine.__new__(lazyllmchat.LLMEngine)
        engine.model = _Boom()
        engine.history = []
        engine.max_history = lazyllmchat.MAX_HISTORY_TURNS
        assert "LLM error" in engine.ask("q")


class TestSessionContext:
    def test_missing_report_is_reported(self, tmp_path):
        provider = lazyllmchat.SessionContextProvider(session_path=str(tmp_path / "nope.csv"))
        assert "No session report" in provider.get_last_lines()

    def test_tail_returns_header_and_rows(self, tmp_path):
        report = tmp_path / "report.csv"
        report.write_text("header\nrow1\nrow2\nrow3\n", encoding="utf-8")
        provider = lazyllmchat.SessionContextProvider(session_path=str(report))
        text = provider.get_last_lines(count=2)
        assert "header" in text
        assert "row3" in text


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
