"""Parity contract tests for the self-contained Groq adapter family.

Guards the ``modules.llm_adapter`` Groq ``process_prompt_*`` implementation so
it preserves legacy call semantics (client-or-None handling, file-reading
variants, event/plan augmentation, knowledge persistence) without depending on
``modules.legacy.lazygptcli*``.
"""

from __future__ import annotations

import json
import os
from types import SimpleNamespace

import pytest

import modules.llm_adapter as adapter
from modules.llm_prompts import LlmPromptConfig

KB_BASENAME = "knowledge_base_vuln.json"


class _FakeCompletions:
    def __init__(self, content):
        self.content = content
        self.model = None
        self.messages = None
        self.max_tokens = None

    def create(self, model=None, messages=None, max_tokens=None):
        self.model = model
        self.messages = messages
        self.max_tokens = max_tokens
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))]
        )


class _FakeClient:
    def __init__(self, content="fake response"):
        self.completions = _FakeCompletions(content)
        self.chat = SimpleNamespace(completions=self.completions)


@pytest.fixture
def cfg(tmp_path):
    return LlmPromptConfig(
        project_root=str(tmp_path),
        kb_dir=str(tmp_path / "kb"),
        payload_path=str(tmp_path / "payload.json"),
        event_config_path=str(tmp_path / "event_config.json"),
        sessions_dir=str(tmp_path / "sessions"),
    )


@pytest.fixture
def patched(monkeypatch, cfg):
    monkeypatch.setattr(adapter, "_CONFIG", cfg)
    return cfg


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class TestMissingClient:
    @pytest.mark.parametrize(
        "name",
        [
            "process_prompt",
            "process_prompt_script",
            "process_prompt_adversary",
            "process_prompt_general",
            "process_prompt_search",
        ],
    )
    def test_direct_variants_report_missing_key(self, patched, name):
        fn = getattr(adapter, name)
        assert fn(None, "hello") == "Error: Groq API key not configured"

    @pytest.mark.parametrize("name", ["process_prompt_task", "process_prompt_vuln", "process_prompt_redop"])
    def test_file_variants_report_missing_key(self, patched, name, tmp_path):
        fn = getattr(adapter, name)
        path = tmp_path / "data.json"
        _write(path, json.dumps({"a": 1}))
        assert fn(None, str(path)) == "Error: Groq API key not configured"


class TestUninitializedClient:
    def test_complete_error_handled(self, patched):
        result = adapter.process_prompt(None, "query")
        assert result == "Error: Groq API key not configured"


class TestDirectPromptFlow:
    def test_sends_user_message_and_returns_content(self, patched):
        client = _FakeClient("the command")
        result = adapter.process_prompt(client, "scan this host")
        assert result == "the command"

    def test_completion_received_single_user_message(self, patched):
        client = _FakeClient("out")
        adapter.process_prompt(client, "goal")
        assert len(client.completions.messages) == 1
        assert client.completions.messages[0]["role"] == "user"
        assert "goal" in client.completions.messages[0]["content"]

    def test_default_max_tokens_applied(self, patched):
        client = _FakeClient("out")
        adapter.process_prompt(client, "goal")
        assert client.completions.max_tokens == adapter.DEFAULT_MAX_TOKENS


class TestKnowledgePersistence:
    def test_successful_response_is_remembered(self, patched, cfg):
        client = _FakeClient("good answer")
        adapter.process_prompt(client, "memorize me")
        path = cfg.knowledge_base_path("oneliner")
        assert path.endswith("knowledge_base.json")
        records = json.loads(open(path, encoding="utf-8").read())
        assert {"prompt": "memorize me", "response": "good answer"} in records

    def test_error_response_not_remembered(self, patched, cfg):
        client = _FakeClient("Error: upstream down")
        adapter.process_prompt(client, "do not memorize")
        path = cfg.knowledge_base_path("oneliner")
        assert not os.path.exists(path)


class TestFileReadingVariants:
    def test_task_reads_file_content(self, patched, tmp_path):
        path = tmp_path / "tasks.json"
        _write(path, json.dumps({"tasks": []}))
        client = _FakeClient("done 100%")
        result = adapter.process_prompt_task(client, str(path))
        assert result == "done 100%"

    def test_task_missing_file_returns_error(self, patched, tmp_path):
        result = adapter.process_prompt_task(_FakeClient(), str(tmp_path / "gone.json"))
        assert result == f"Error reading file: {tmp_path / 'gone.json'}"

    def test_redop_reads_file_content(self, patched, tmp_path):
        path = tmp_path / "op.json"
        _write(path, json.dumps({"status": "active"}))
        assert adapter.process_prompt_redop(_FakeClient("evaluated"), str(path)) == "evaluated"


class TestVulnAugmentation:
    def test_appends_event_tool_output(self, patched, cfg, tmp_path):
        _write(
            tmp_path / "event_config.json",
            json.dumps({"events": [{"name": "nmap", "tool_output": str(tmp_path / "tool.txt")}]}),
        )
        _write(tmp_path / "tool.txt", "port 445 open")
        target = tmp_path / "scan.nmap"
        _write(target, "Nmap scan report")
        client = _FakeClient("plan")
        adapter.process_prompt_vuln(client, str(target), event="nmap")
        content = client.completions.messages[0]["content"]
        assert "port 445 open" in content

    def test_appends_plan_history(self, patched, cfg, tmp_path):
        _write(tmp_path / "sessions" / "plan.txt", "phase 2 complete")
        target = tmp_path / "scan.nmap"
        _write(target, "Nmap output")
        client = _FakeClient("plan")
        adapter.process_prompt_vuln(client, str(target))
        content = client.completions.messages[0]["content"]
        assert "phase 2 complete" in content


class TestExports:
    def test_groq_family_exports_present(self):
        for name in (
            "process_prompt",
            "process_prompt_script",
            "process_prompt_adversary",
            "process_prompt_general",
            "process_prompt_search",
            "process_prompt_task",
            "process_prompt_vuln",
            "process_prompt_redop",
            "safe_groq_client",
        ):
            assert callable(getattr(adapter, name, None))

    def test_safe_groq_client_none_without_key(self):
        assert adapter.safe_groq_client(None) is None
        assert adapter.safe_groq_client("") is None


class _FakeBackend:
    def __init__(self, result="backend answer"):
        self.result = result
        self.system = None
        self.user = None

    def complete(self, system, user, **kwargs):
        self.system = system
        self.user = user
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class TestAskGeneral:
    def test_uses_configured_backend(self, patched, monkeypatch):
        import modules.llm_factory as factory

        backend = _FakeBackend("hello from ollama")
        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: backend)
        assert adapter.ask_general("some question") == "hello from ollama"

    def test_receives_system_and_rendered_user(self, patched, monkeypatch):
        import modules.llm_factory as factory
        from modules.llm_prompts import DEFAULT_SYSTEM_PROMPT

        backend = _FakeBackend("ok")
        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: backend)
        adapter.ask_general("MAGIC QUESTION")
        assert backend.system == DEFAULT_SYSTEM_PROMPT
        assert "MAGIC QUESTION" in backend.user

    def test_missing_backend_reports_error(self, patched, monkeypatch):
        import modules.llm_factory as factory

        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: None)
        result = adapter.ask_general("question")
        assert result.startswith("Error:")

    def test_backend_exception_reports_error(self, patched, monkeypatch):
        import modules.llm_factory as factory

        backend = _FakeBackend(RuntimeError("boom"))
        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: backend)
        assert adapter.ask_general("question").startswith("Error:")

    def test_backend_error_string_not_remembered(self, patched, cfg, monkeypatch):
        import modules.llm_factory as factory

        backend = _FakeBackend("Error from Groq: bad key")
        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: backend)
        result = adapter.ask_general("do not memorize")
        assert result.startswith("Error")
        assert not os.path.exists(cfg.knowledge_base_path("script"))

    def test_successful_answer_remembered(self, patched, cfg, monkeypatch):
        import json as jsonlib

        import modules.llm_factory as factory

        backend = _FakeBackend("good answer")
        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: backend)
        adapter.ask_general("memorize me")
        records = jsonlib.loads(open(cfg.knowledge_base_path("script"), encoding="utf-8").read())
        assert {"prompt": "memorize me", "response": "good answer"} in records

    def test_exported(self):
        assert callable(adapter.ask_general)
        assert "ask_general" in adapter.__all__
