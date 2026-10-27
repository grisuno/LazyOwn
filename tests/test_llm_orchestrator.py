"""SDD spec and BDD scenarios for the orchestrator-governed LLM failover chain.

``modules/llm_orchestrator.py`` is the single entry point every AI module
in the framework uses to reach a language model. The chain itself is owned
by ``lazy_orchestrator`` (the Models tab, persisted in
``sessions/lazy/llm_pool.json``): member priority acts as the weight that
decides the try order, the shared health registry parks failing members,
and the ``modules.llm_factory`` spec executor performs each leg.

Behavioral contract (SDD):
1. The first member of the priority-sorted chain is the primary.
2. A member fails when its executor raises, returns blank text, or
   returns an error banner (``[LLM error] ...``) or quota wording.
3. The chain walks members until one serves; it never raises.
4. When the primary fails and a fallback serves, the result carries a
   notice naming the primary, its error and the serving member.
5. When every member fails, the result backend is ``"error"`` and the
   notice names every attempted member with its error.
6. Unhealthy members (breaker cooldown) are skipped while any healthy
   member remains; when none is healthy they are attempted anyway.
7. Successful and failed attempts are recorded in the pool ledger.

BDD scenarios below follow the Given/When/Then discipline.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import modules.lazy_loop as loop
import modules.llm_orchestrator as orch

PROMPT = "suggest one probe"
SYSTEM = "You are a red team assistant."


class _StubHealth:
    """Health registry stub with injectable parked members."""

    def __init__(self, parked: tuple[str, ...] = ()) -> None:
        self.parked = set(parked)
        self.successes: list[str] = []
        self.failures: list[tuple[str, str]] = []

    def healthy(self, name: str) -> bool:
        return name not in self.parked

    def report_failure(self, name: str, error: str = "") -> None:
        self.failures.append((name, error))

    def report_success(self, name: str) -> None:
        self.successes.append(name)


def _scripted_executor(script: dict[str, object], calls: list[str] | None = None):
    def _execute(model_spec: str, prompt: str, max_tokens: int = 800) -> str:
        if calls is not None:
            calls.append(model_spec)
        outcome = script.get(model_spec, "")
        if isinstance(outcome, Exception):
            raise outcome
        return str(outcome)

    return _execute


def _member(name: str, model: str, priority: int) -> dict:
    return {"name": name, "model": model, "priority": priority}


@pytest.fixture
def isolated_pool(tmp_path, monkeypatch):
    """Point the LlmPool JSON store at a per-test directory."""
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


class TestChainOrder:
    def test_weights_sort_members_by_descending_priority(self):
        """BDD: Given an unsorted member list, When the chain is built,
        Then members are ordered by descending priority weight."""
        members = [
            _member("low", "groq:low-model", 1),
            _member("high", "groq:high-model", 9),
            _member("mid", "groq:mid-model", 5),
        ]
        ordered = orch.sort_members(members)
        assert [m["name"] for m in ordered] == ["high", "mid", "low"]

    def test_sort_members_never_mutates_input(self):
        """BDD: Given a member list, When sorted, Then the input list is untouched."""
        members = [_member("low", "groq:low", 1), _member("high", "groq:high", 9)]
        orch.sort_members(members)
        assert [m["name"] for m in members] == ["low", "high"]

    def test_pool_chain_reads_lazy_orchestrator_store(self, isolated_pool):
        """BDD: Given members added through the lazy_orchestrator pool,
        When the chain is requested, Then the persisted weights rule the order."""
        from modules.lazy_engine import LlmPool

        pool = LlmPool()
        pool.add_member("cloud", "groq:cloud-model", 7)
        pool.add_member("local", "ollama:local-model", 3)
        chain = orch.pool_chain()
        names = [m["name"] for m in chain]
        assert "cloud" in names and "local" in names
        assert names.index("cloud") < names.index("local")

    def test_pool_chain_self_heals_corrupt_store(self, isolated_pool):
        """BDD: Given a corrupted pool store, When the chain is requested,
        Then the seeded defaults answer instead of raising."""
        (isolated_pool / "llm_pool.json").write_text("{corrupt", encoding="utf-8")
        chain = orch.pool_chain()
        assert chain
        assert all("model" in member for member in chain)

    def test_pool_chain_returns_empty_when_pool_unreadable(self, monkeypatch):
        """BDD: Given the pool store exploding, When the chain is requested,
        Then an empty chain is returned instead of raising."""
        from modules import lazy_engine

        def _explode() -> None:
            raise RuntimeError("store gone")

        monkeypatch.setattr(lazy_engine, "LlmPool", _explode)
        assert orch.pool_chain() == []


class TestFailover:
    def test_primary_success_needs_no_fallback(self):
        """BDD: Given a healthy primary, When the chain completes,
        Then no fallback notice is produced and the answer is clean."""
        calls: list[str] = []
        executor = _scripted_executor({"groq:primary-model": "42"}, calls)
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("primary", "groq:primary-model", 9), _member("backup", "groq:backup", 1)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert result.text == "42"
        assert result.member == "primary"
        assert result.backend == "groq"
        assert result.fallback_used is False
        assert result.notice == ""
        assert result.model_name == "primary-model"
        assert calls == ["groq:primary-model"]

    def test_primary_failure_serves_fallback_with_notice(self):
        """BDD: Given a dead primary and a live fallback, When the chain
        completes, Then the answer is served and the notice names both."""
        calls: list[str] = []
        executor = _scripted_executor(
            {"groq:primary-model": RuntimeError("groq http 429"), "ollama:backup-model": "42"},
            calls,
        )
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("primary", "groq:primary-model", 9), _member("backup", "ollama:backup-model", 1)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert result.text == "42"
        assert result.member == "backup"
        assert result.backend == "ollama"
        assert result.fallback_used is True
        assert "Primary model 'primary'" in result.notice
        assert "groq:primary-model" in result.notice
        assert "groq http 429" in result.notice
        assert "served by 'backup'" in result.notice
        assert result.display_text.startswith("[!]")

    def test_all_members_fail_returns_error_result_without_raising(self):
        """BDD: Given every member dead, When the chain completes,
        Then an error result with the help message is returned, never an exception."""
        executor = _scripted_executor({"groq:a": RuntimeError("down"), "groq:b": ""}, [])
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("b", "groq:b", 1)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert not result.ok
        assert result.backend == "error"
        assert result.text == orch.HELP_MESSAGE
        assert "'a'" in result.notice and "'b'" in result.notice
        assert "down" in result.notice

    def test_error_banner_text_is_a_failure_not_content(self):
        """BDD: Given a leg replying with an error banner, When the chain
        completes, Then the banner is treated as a member failure."""
        calls: list[str] = []
        executor = _scripted_executor(
            {"groq:a": "[LLM error] GROQ_API_KEY not set.", "groq:b": "good"},
            calls,
        )
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("b", "groq:b", 1)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.text == "good"
        assert result.member == "b"
        assert result.fallback_used is True

    def test_blank_reply_is_a_failure(self):
        """BDD: Given a leg replying blank, When the chain completes,
        Then the next member serves the answer."""
        executor = _scripted_executor({"groq:a": "   ", "groq:b": "answer"})
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("b", "groq:b", 1)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.text == "answer"

    def test_quota_wording_reply_is_a_failure(self):
        """BDD: Given a leg replying quota exhaustion prose, When the chain
        completes, Then the reply never leaks as operator content."""
        executor = _scripted_executor({"groq:a": "You exceeded your current quota.", "groq:b": "plan"})
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("b", "groq:b", 1)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.text == "plan"

    def test_empty_prompt_short_circuits(self):
        """BDD: Given a blank prompt, When the chain is called,
        Then no member is contacted and an error result is returned."""
        calls: list[str] = []
        executor = _scripted_executor({"groq:a": "x"}, calls)
        result = orch.complete_with_fallback(
            "   ",
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert not result.ok
        assert calls == []

    def test_system_prompt_is_prepended_for_the_executor(self):
        """BDD: Given a system prompt, When the chain completes,
        Then the executor receives system and prompt combined."""
        seen: dict[str, str] = {}

        def executor(model_spec: str, prompt: str, max_tokens: int = 800) -> str:
            seen[model_spec] = prompt
            return "ok"

        orch.complete_with_fallback(
            PROMPT,
            system=SYSTEM,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert seen["groq:a"].startswith(SYSTEM)
        assert PROMPT in seen["groq:a"]

    def test_max_tokens_is_forwarded(self):
        """BDD: Given a token cap, When the chain completes,
        Then the executor receives the cap."""
        seen: list[int] = []

        def executor(model_spec: str, prompt: str, max_tokens: int = 800) -> str:
            seen.append(max_tokens)
            return "ok"

        orch.complete_with_fallback(
            PROMPT,
            max_tokens=123,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert seen == [123]

    def test_chain_uses_orchestrator_pool_when_no_override(self, isolated_pool):
        """BDD: Given a populated lazy_orchestrator pool and no override,
        When the chain completes, Then the pool members drive the walk."""
        from modules.lazy_engine import LlmPool

        LlmPool().add_member("served", "groq:served-model", 40)
        LlmPool().add_member("dead", "groq:dead-model", 50)
        calls: list[str] = []
        executor = _scripted_executor(
            {"groq:dead-model": RuntimeError("dead"), "groq:served-model": "from pool"},
            calls,
        )
        result = orch.complete_with_fallback(
            PROMPT,
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.text == "from pool"
        assert calls == ["groq:dead-model", "groq:served-model"]

    def test_dedupes_members_by_name(self):
        """BDD: Given a chain with a duplicated member, When the chain completes,
        Then the duplicate is attempted only once."""
        calls: list[str] = []
        executor = _scripted_executor({"groq:a": RuntimeError("down")}, calls)
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert calls == ["groq:a"]
        assert not result.ok


class TestHealth:
    def test_unhealthy_member_is_skipped_while_others_remain(self):
        """BDD: Given a parked primary and a healthy fallback, When the
        chain completes, Then the parked member is not contacted."""
        calls: list[str] = []
        executor = _scripted_executor({"groq:b": "from fallback"}, calls)
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("b", "groq:b", 1)],
            executor=executor,
            health=_StubHealth(parked=("a",)),
            record=False,
        )
        assert result.text == "from fallback"
        assert calls == ["groq:b"]
        assert result.fallback_used is True
        assert "a" in result.notice

    def test_all_unhealthy_members_still_get_attempted(self):
        """BDD: Given every member parked, When the chain completes,
        Then members are attempted anyway as the last resort."""
        calls: list[str] = []
        executor = _scripted_executor({"groq:a": "answer"}, calls)
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(parked=("a",)),
            record=False,
        )
        assert result.text == "answer"
        assert calls == ["groq:a"]

    def test_success_reports_health(self):
        """BDD: Given a serving member, When the chain completes,
        Then the health registry records the success."""
        health = _StubHealth()
        executor = _scripted_executor({"groq:a": "answer"})
        orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=health,
            record=False,
        )
        assert health.successes == ["a"]

    def test_failure_reports_health(self):
        """BDD: Given a failing member, When the chain completes,
        Then the health registry records the failure with its error."""
        health = _StubHealth()
        executor = _scripted_executor({"groq:a": RuntimeError("boom"), "groq:b": "answer"})
        orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("b", "groq:b", 1)],
            executor=executor,
            health=health,
            record=False,
        )
        assert ("a", "boom") in health.failures

    def test_default_health_comes_from_shared_registry(self, isolated_pool, monkeypatch):
        """BDD: Given no health override, When the chain completes,
        Then the shared modules.llm_pool registry is used."""
        import modules.llm_pool as pool_module

        seen: list[str] = []
        monkeypatch.setattr(pool_module, "shared_registry", lambda: _RecordingRegistry(seen))
        executor = _scripted_executor({"groq:a": "answer"})
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            record=False,
        )
        assert result.ok
        assert seen == ["a"]


class _RecordingRegistry:
    """Shared-registry stand-in that records report_success calls."""

    def __init__(self, seen: list[str]) -> None:
        self.seen = seen

    def healthy(self, name: str) -> bool:
        return True

    def report_failure(self, name: str, error: str = "") -> None:
        return None

    def report_success(self, name: str) -> None:
        self.seen.append(name)


class TestLedger:
    def test_success_is_recorded_in_the_pool_ledger(self, isolated_pool):
        """BDD: Given a serving member, When the chain completes,
        Then a success row lands in the llm_usage ledger."""
        from modules.lazy_engine import LlmPool

        executor = _scripted_executor({"groq:a": "answer"})
        orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
        )
        usage = LlmPool().usage()
        assert any(row.get("ok") and row.get("member") == "a" for row in usage.get("calls", []))

    def test_failure_is_recorded_in_the_pool_ledger(self, isolated_pool):
        """BDD: Given a failing member, When the chain completes,
        Then a failure row lands in the llm_usage ledger."""
        from modules.lazy_engine import LlmPool

        executor = _scripted_executor({"groq:a": RuntimeError("boom"), "groq:b": "answer"})
        orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9), _member("b", "groq:b", 1)],
            executor=executor,
            health=_StubHealth(),
        )
        usage = LlmPool().usage()
        assert any(not row.get("ok") and row.get("member") == "a" for row in usage.get("calls", []))


class TestBackendKind:
    @pytest.mark.parametrize(
        "spec,kind",
        [
            ("groq:llama-3.3-70b-versatile", "groq"),
            ("ollama:deepseek-r1:1.5b", "ollama"),
            ("pi:local-model", "pi"),
            ("llamacpp:local-model", "llamacpp"),
            ("toposwarm:router", "toposwarm"),
            ("bare-model", "auto"),
        ],
    )
    def test_backend_kind_parses_spec_prefix(self, spec, kind):
        """BDD: Given a model spec, When the backend kind is derived,
        Then the prefix or auto is returned."""
        assert orch.backend_kind(spec) == kind


class TestAdapterWiring:
    @pytest.fixture
    def cfg(self, tmp_path):
        from modules.llm_prompts import LlmPromptConfig

        return LlmPromptConfig(
            project_root=str(tmp_path),
            kb_dir=str(tmp_path / "kb"),
            payload_path=str(tmp_path / "payload.json"),
            event_config_path=str(tmp_path / "event_config.json"),
            sessions_dir=str(tmp_path / "sessions"),
        )

    @pytest.fixture
    def patched(self, cfg, monkeypatch):
        import modules.llm_adapter as adapter

        monkeypatch.setattr(adapter, "_CONFIG", cfg)
        return adapter

    def test_missing_client_serves_from_the_chain(self, patched, monkeypatch):
        """BDD: Given no Groq client and a live chain member, When a bot
        prompt is processed, Then the fallback answer plus notice is served."""
        result = orch.OrchestratorResult(
            text="nmap -sV target",
            member="ollama-local",
            model="ollama:deepseek-r1:1.5b",
            backend="ollama",
            fallback_used=True,
            notice="[!] Primary model 'groq-cloud' failed: no key.",
        )
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: result)
        answer = patched.process_prompt(None, "scan the host")
        assert "nmap -sV target" in answer
        assert answer.startswith("[!]")

    def test_missing_client_returns_legacy_error_when_chain_exhausted(self, patched, monkeypatch):
        """BDD: Given no Groq client and an exhausted chain, When a bot
        prompt is processed, Then the legacy configuration error is returned."""
        exhausted = orch.OrchestratorResult(text=orch.HELP_MESSAGE, backend="error")
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: exhausted)
        assert patched.process_prompt(None, "scan the host") == "Error: Groq API key not configured"

    def test_client_error_falls_back_to_the_chain(self, patched, monkeypatch):
        """BDD: Given a Groq client raising on every completion, When a bot
        prompt is processed, Then the chain serves the answer."""
        calls: list[str] = []
        result = orch.OrchestratorResult(
            text="fallback answer",
            member="pi-qwen",
            model="pi:local-model",
            backend="pi",
            fallback_used=True,
            notice="[!] Primary model 'groq-cloud' failed: quota.",
        )
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: result)
        dead = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **kwargs: (_ for _ in ()).throw(
                        RuntimeError("Error code: 429 - Rate limit reached: tokens per minute capped")
                    )
                )
            )
        )
        answer = patched.process_prompt(dead, "do the thing")
        assert "fallback answer" in answer
        assert answer.startswith("[!]")

    def test_client_success_stays_primary_without_chain_call(self, patched, monkeypatch):
        """BDD: Given a healthy Groq client, When a bot prompt is processed,
        Then the primary answer is returned and the chain is never contacted."""
        touched = []
        monkeypatch.setattr(
            patched,
            "complete_with_fallback",
            lambda *a, **k: touched.append(1) or orch.OrchestratorResult(text="", backend="error"),
        )
        client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **kwargs: SimpleNamespace(
                        choices=[SimpleNamespace(message=SimpleNamespace(content="primary answer"))]
                    )
                )
            )
        )
        got = patched.process_prompt(client, "goal")
        assert got == "primary answer"
        assert touched == []

    def test_client_401_error_string_falls_back_to_the_chain(self, patched, monkeypatch):
        """BDD: Given a Groq client answering with a 401 error string (the
        SDK returns errors as strings), When a bot prompt is processed,
        Then the chain serves the answer instead of the banner."""
        result = orch.OrchestratorResult(
            text="chain answer after 401",
            member="ollama-local",
            model="ollama:m",
            backend="ollama",
            fallback_used=True,
            notice="[!] Primary model 'groq-cloud' failed: 401.",
        )
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: result)
        banner = "Error code: 401 - {'error': {'code': 'invalid_api_key'}}"
        client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content=banner))]
                ))
            )
        )
        answer = patched.process_prompt(client, "goal")
        assert answer.startswith("[!]")
        assert "chain answer after 401" in answer

    def test_client_401_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch):
        """BDD: Given a Groq client answering with a 401 error string and an
        exhausted chain, When a bot prompt is processed, Then the legacy
        banner is returned unchanged."""
        exhausted = orch.OrchestratorResult(text=orch.HELP_MESSAGE, backend="error")
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: exhausted)
        banner = "Error code: 401 - {'error': {'code': 'invalid_api_key'}}"
        client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content=banner))]
                ))
            )
        )
        assert patched.process_prompt(client, "goal") == banner

    def test_fallback_answer_is_memorized_clean(self, patched, monkeypatch, tmp_path):
        """BDD: Given a fallback-served answer, When the bot prompt completes,
        Then the knowledge store keeps the clean answer without the notice."""
        result = orch.OrchestratorResult(
            text="clean answer",
            member="ollama-local",
            model="ollama:m",
            backend="ollama",
            fallback_used=True,
            notice="[!] notice text",
        )
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: result)
        patched.process_prompt(None, "memorize me")
        records = json.loads((tmp_path / "kb" / "knowledge_base.json").read_text())
        assert {"prompt": "memorize me", "response": "clean answer"} in records

    def test_ask_general_serves_from_the_chain_when_backend_missing(self, patched, monkeypatch):
        """BDD: Given no factory backend and a live chain, When ask_general
        runs, Then the chain answer plus notice is returned."""
        import modules.llm_factory as factory

        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: None)
        result = orch.OrchestratorResult(
            text="chain answer",
            member="ollama-local",
            model="ollama:m",
            backend="ollama",
            fallback_used=True,
            notice="[!] failover notice",
        )
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: result)
        assert patched.ask_general("question").startswith("[!]")
        assert "chain answer" in patched.ask_general("question")

    def test_ask_general_keeps_legacy_error_when_chain_exhausted(self, patched, monkeypatch):
        """BDD: Given no factory backend and an exhausted chain, When
        ask_general runs, Then the legacy backend error is returned."""
        import modules.llm_factory as factory

        monkeypatch.setattr(factory, "try_get_llm_backend", lambda *a, **k: None)
        exhausted = orch.OrchestratorResult(text=orch.HELP_MESSAGE, backend="error")
        monkeypatch.setattr(patched, "complete_with_fallback", lambda *a, **k: exhausted)
        assert patched.ask_general("question").startswith("Error:")


class TestC2Wiring:
    def test_analyze_functions_route_through_the_orchestrator(self):
        """BDD: Given lazyc2.py, When the phishing analyzers are checked,
        Then they call the orchestrator chain instead of a Groq client."""
        import pathlib

        root = pathlib.Path(__file__).resolve().parent.parent
        text = (root / "lazyc2.py").read_text(encoding="utf-8")
        assert "complete_with_fallback" in text
        assert 'model="llama3-70b-8192"' not in text

    def test_ai_fallback_call_routes_through_the_chain(self):
        """BDD: Given modules/ai_fallback.py, When call() is inspected,
        Then it delegates to the orchestrator chain as the first layer."""
        import pathlib

        root = pathlib.Path(__file__).resolve().parent.parent
        text = (root / "modules" / "ai_fallback.py").read_text(encoding="utf-8")
        assert "complete_with_fallback" in text


class TestErrorDetection:
    @pytest.mark.parametrize(
        "reply",
        [
            "Error code: 401 - {'error': {'message': 'Invalid API Key', 'code': 'invalid_api_key'}}",
            "Error from Groq: quota dead",
            "[LLM error] GROQ_API_KEY not set.",
            "Error from Ollama: connection refused",
            "Error streaming from llama.cpp: timeout",
            "",
            "   ",
        ],
    )
    def test_error_replies_detected(self, reply):
        """BDD: Given a backend error banner or quota prose, When the reply
        is inspected, Then it is treated as a failure, never as content."""
        assert orch.is_error_reply(reply)

    def test_real_answer_not_treated_as_error(self):
        """BDD: Given a legitimate model answer, When the reply is inspected,
        Then it is served as content."""
        assert not orch.is_error_reply("nmap -sV --script vulners.nmap 10.0.0.1")

    def test_pentest_prose_with_unauthorized_word_is_content(self):
        """BDD: Given a pentest answer mentioning unauthorized access, When
        the reply is inspected, Then it is served as content, never failed."""
        answer = "Never use these commands against unauthorized systems. Run nmap -sV target."
        assert not orch.is_error_reply(answer)

    def test_phishing_prose_with_credit_word_is_content(self):
        """BDD: Given a phishing-analysis answer mentioning credit cards, When
        the reply is inspected, Then it is served as content, never failed."""
        answer = "The simulated campaign harvested credit card submissions. Next vector: sms."
        assert not orch.is_error_reply(answer)

    def test_long_pentest_plan_is_served_not_failed_over(self):
        """BDD: Given an ollama leg answering a long pentest plan that mentions
        unauthorized access, When the chain completes, Then the plan is served."""
        answer = (
            "Structured plan for the NMAP output:\n"
            "1. Recon: nmap -sV target.\n"
            "2. Avoid acting against unauthorized systems; stay in the lab scope.\n"
            "3. Exploit the vsftpd 2.3.4 backdoor with msfconsole."
        )
        executor = _scripted_executor({"ollama:deepseek-r1:1.5b": answer}, [])
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("ollama-local", "ollama:deepseek-r1:1.5b", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert result.text == answer
        assert result.fallback_used is False

    def test_invalid_api_key_reply_is_a_failure(self):
        """BDD: Given a Groq invalid-api-key reply, When the chain completes,
        Then the walk moves to the next member."""
        executor = _scripted_executor(
            {
                "groq:primary-model": "Error code: 401 - {'error': {'code': 'invalid_api_key'}}",
                "ollama:backup-model": "plan",
            },
            [],
        )
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("primary", "groq:primary-model", 9), _member("backup", "ollama:backup-model", 1)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.text == "plan"
        assert result.backend == "ollama"


    def test_placeholder_groq_leg_refused_without_doomed_call(self, monkeypatch):
        """BDD: Given a placeholder env key and a groq member, When the
        chain completes, Then the leg is refused without a network call."""
        import modules.llm_factory as factory

        monkeypatch.setenv("GROQ_API_KEY", "YOUR_API_KEY_HERE")
        monkeypatch.setattr(factory, "load_payload", lambda *a, **k: {"api_key": "YOUR_API_KEY_HERE"})
        contacted = []
        real_complete = factory.complete

        def _spy(model_spec, prompt, max_tokens=800):
            contacted.append(model_spec)
            return real_complete(model_spec, prompt, max_tokens=max_tokens)

        monkeypatch.setattr(factory, "complete", _spy)
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=None,
            health=_StubHealth(),
            record=False,
        )
        assert not result.ok
        assert contacted == []
        assert "groq" in result.notice

    def test_placeholder_groq_leg_refused_even_with_payload_key(self, monkeypatch):
        """BDD: Given a real payload key under a placeholder env value, When
        the groq leg runs, Then the payload key is published and used."""
        import modules.llm_factory as factory

        monkeypatch.setenv("GROQ_API_KEY", "YOUR_API_KEY_HERE")
        monkeypatch.setattr(factory, "load_payload", lambda *a, **k: {"api_key": "gsk_real"})
        executor = _scripted_executor({"groq:a": "answer"})
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert orch.os.environ.get("GROQ_API_KEY") == "gsk_real"


class TestPlaceholderKeys:
    def test_placeholder_fragments_recognized(self):
        """BDD: Given the shipped placeholder key values, When inspected,
        Then they are recognized as placeholders."""
        for value in ("YOUR_API_KEY_HERE", "api_key", "your_api_key_here", "  ", ""):
            assert orch.is_placeholder_key(value), value

    def test_real_key_not_a_placeholder(self):
        """BDD: Given a real Groq key, When inspected, Then it is not a placeholder."""
        assert not orch.is_placeholder_key("gsk_realkey123")

    def test_factory_rejects_placeholder_payload_key(self):
        """BDD: Given the factory key resolver and a placeholder payload key,
        When resolved, Then None is returned so the leg fails over."""
        from modules.llm_factory import _resolve_api_key

        assert _resolve_api_key({"api_key": "YOUR_API_KEY_HERE"}) is None
        assert _resolve_api_key({"api_key": "api_key"}) is None
        assert _resolve_api_key({"api_key": "gsk_real"}) == "gsk_real"

    def test_factory_rejects_placeholder_env_key(self, monkeypatch):
        """BDD: Given the factory key resolver and a placeholder env key,
        When resolved, Then None is returned so the leg fails over."""
        from modules.llm_factory import _resolve_api_key

        monkeypatch.setenv("GROQ_API_KEY", "YOUR_API_KEY_HERE")
        assert _resolve_api_key({}) is None

    def test_placeholder_env_replaced_by_payload_key(self, monkeypatch):
        """BDD: Given a placeholder env key and a real payload key, When the
        chain completes, Then the environment receives the real key."""
        import modules.llm_factory as factory

        monkeypatch.setenv("GROQ_API_KEY", "YOUR_API_KEY_HERE")
        monkeypatch.setattr(factory, "load_payload", lambda *a, **k: {"api_key": "gsk_real"})
        executor = _scripted_executor({"groq:a": "answer"})
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert orch.os.environ.get("GROQ_API_KEY") == "gsk_real"

    def test_placeholder_env_survives_without_payload_key(self, monkeypatch):
        """BDD: Given a placeholder env key and no payload key, When the
        chain completes, Then the environment is left untouched."""
        import modules.llm_factory as factory

        monkeypatch.setenv("GROQ_API_KEY", "YOUR_API_KEY_HERE")
        monkeypatch.setattr(factory, "load_payload", lambda *a, **k: {"api_key": "YOUR_API_KEY_HERE"})
        executor = _scripted_executor({"groq:a": "answer"})
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert orch.os.environ.get("GROQ_API_KEY") == "YOUR_API_KEY_HERE"


class TestGroqEnvKey:
    def test_explicit_api_key_published_to_environment(self, monkeypatch):
        """BDD: Given an explicit Groq key and no environment key, When the
        chain completes, Then the key is published for the groq legs."""
        import modules.llm_factory as factory

        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        monkeypatch.setattr(factory, "load_payload", lambda *a, **k: {})
        executor = _scripted_executor({"groq:a": "answer"})
        result = orch.complete_with_fallback(
            PROMPT,
            api_key="gsk_test_key",
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert orch.os.environ.get("GROQ_API_KEY") == "gsk_test_key"

    def test_placeholder_payload_key_not_published(self, monkeypatch):
        """BDD: Given a placeholder payload key and no environment key, When
        the chain completes, Then the placeholder is never published."""
        import modules.llm_factory as factory

        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        monkeypatch.setattr(factory, "load_payload", lambda *a, **k: {"api_key": "api_key"})
        executor = _scripted_executor({"groq:a": "answer"})
        result = orch.complete_with_fallback(
            PROMPT,
            members=[_member("a", "groq:a", 9)],
            executor=executor,
            health=_StubHealth(),
            record=False,
        )
        assert result.ok
        assert orch.os.environ.get("GROQ_API_KEY") is None


class TestAiFallbackIntegration:
    def test_orchestrator_success_maps_to_ai_result(self, monkeypatch):
        """BDD: Given a chain-served answer, When ai_fallback.call runs,
        Then an AIResult with the serving backend and notice is returned."""
        import modules.ai_fallback as fallback

        result = orch.OrchestratorResult(
            text="answer",
            member="groq-cloud",
            model="groq:llama-3.3-70b-versatile",
            backend="groq",
            model_name="llama-3.3-70b-versatile",
            fallback_used=False,
            notice="",
        )
        monkeypatch.setattr(orch, "complete_with_fallback", lambda *a, **k: result)
        monkeypatch.setattr(fallback, "complete_with_fallback", lambda *a, **k: result)
        ai = fallback.call("prompt")
        assert ai.backend == "groq"
        assert ai.model == "llama-3.3-70b-versatile"
        assert ai.text == "answer"

    def test_orchestrator_success_after_failure_carries_notice(self, monkeypatch):
        """BDD: Given a chain-served answer after a primary failure, When
        ai_fallback.call runs, Then the notice prefixes the answer text."""
        import modules.ai_fallback as fallback

        result = orch.OrchestratorResult(
            text="answer",
            member="ollama-local",
            model="ollama:deepseek-r1:1.5b",
            backend="ollama",
            model_name="deepseek-r1:1.5b",
            fallback_used=True,
            notice="[!] Primary model 'groq-cloud' failed: quota.",
            attempts=[("groq-cloud", "quota")],
        )
        monkeypatch.setattr(fallback, "complete_with_fallback", lambda *a, **k: result)
        ai = fallback.call("prompt")
        assert ai.backend == "ollama"
        assert ai.text.startswith("[!]")
        assert "answer" in ai.text
        assert "quota" in ai.error

    def test_exhausted_chain_degrades_to_local_ollama(self, monkeypatch):
        """BDD: Given an exhausted chain and a live local Ollama, When
        ai_fallback.call runs, Then the local leg still answers."""
        import modules.ai_fallback as fallback

        exhausted = orch.OrchestratorResult(text=orch.HELP_MESSAGE, backend="error")
        monkeypatch.setattr(fallback, "complete_with_fallback", lambda *a, **k: exhausted)
        monkeypatch.setattr(fallback, "_ollama_available", lambda: True)
        monkeypatch.setattr(fallback, "_best_ollama_model", lambda: "llama3.2")
        monkeypatch.setattr(fallback, "_ollama_call", lambda *a, **k: "local answer")
        ai = fallback.call("prompt")
        assert ai.backend == "ollama"
        assert ai.text.endswith("local answer")

    def test_total_failure_returns_help_message(self, monkeypatch):
        """BDD: Given an exhausted chain and no local Ollama, When
        ai_fallback.call runs, Then the help message is returned."""
        import modules.ai_fallback as fallback

        exhausted = orch.OrchestratorResult(text=orch.HELP_MESSAGE, backend="error")
        monkeypatch.setattr(fallback, "complete_with_fallback", lambda *a, **k: exhausted)
        monkeypatch.setattr(fallback, "_ollama_available", lambda: False)
        ai = fallback.call("prompt")
        assert ai.backend == "error"
        assert "groq.com" in ai.text


def lazyc2_source() -> str:
    """Return the lazyc2.py source text for contract assertions."""
    import pathlib

    root = pathlib.Path(__file__).resolve().parent.parent
    return str(root / "lazyc2.py")


def test_orchestrator_module_exports_public_api():
    """BDD: Given modules/llm_orchestrator.py, When the public API is checked,
    Then the documented entry points exist."""
    for name in ("OrchestratorResult", "complete_with_fallback", "pool_chain", "sort_members", "HELP_MESSAGE"):
        assert hasattr(orch, name), f"llm_orchestrator missing {name}"
