"""SDD spec and BDD scenarios for the VulnBot orchestrator-governed CLI.

``modules/vulnbot.py`` (driven by ``modules/vuln_bot_cli.py`` and the
``vulnbot_groq`` addon) must never hard-fail on a missing, placeholder or
exhausted Groq key: the lazy_orchestrator failover chain
(:mod:`modules.llm_orchestrator`) serves the analysis when the primary
backend fails, and the knowledge base speaks the canonical list format
(:mod:`modules.llm_prompts.KnowledgeStore`) while still reading legacy
dict-shaped stores.

Behavioral contract (SDD):
1. A model that fails to load (missing/placeholder key) does not crash
   the bot; the orchestrator chain answers.
2. A primary backend error string (``Error from Groq: ...``, quota
   prose, blank) triggers the chain, not a leaked banner.
3. The knowledge base reads both list and dict formats; writes stay in
   the canonical list format; empty matches return empty text.
4. Console mode returns the notice-prefixed answer; web mode streams
   the chain answer when the primary stream fails.
"""

from __future__ import annotations

import json

import pytest

import modules.llm_orchestrator as orch
import modules.vulnbot as vulnbot


@pytest.fixture
def bot(tmp_path, monkeypatch):
    """VulnBotCLI instance with the heavy agent setup disabled."""
    monkeypatch.setattr(vulnbot.VulnBotCLI, "_setup_agent", lambda self, script_path: None)
    return vulnbot.VulnBotCLI(provider="groq", mode="console")


class TestKnowledgeBaseFormats:
    def test_list_format_matches(self, bot, tmp_path):
        """BDD: Given the canonical list-format knowledge base, When a
        prompt is matched, Then the stored responses are returned."""
        kb = tmp_path / "knowledge_base_vuln.json"
        kb.write_text(
            json.dumps([{"prompt": "nmap scan of 10.0.0.1", "response": "port 22 open"}]),
            encoding="utf-8",
        )
        bot.knowledge_base_file = str(kb)
        assert "port 22 open" in bot.get_relevant_knowledge("analyze the nmap scan")

    def test_legacy_dict_format_matches(self, bot, tmp_path):
        """BDD: Given a legacy dict-format knowledge base, When a prompt is
        matched, Then the stored responses are still served."""
        kb = tmp_path / "knowledge_base_vuln.json"
        kb.write_text(json.dumps({"nmap scan": "port 80 open"}), encoding="utf-8")
        bot.knowledge_base_file = str(kb)
        assert "port 80 open" in bot.get_relevant_knowledge("check this nmap scan output")

    def test_no_match_returns_empty_text(self, bot, tmp_path):
        """BDD: Given a knowledge base with no keyword match, When a prompt
        is matched, Then empty text is returned instead of a banner."""
        kb = tmp_path / "knowledge_base_vuln.json"
        kb.write_text(json.dumps([]), encoding="utf-8")
        bot.knowledge_base_file = str(kb)
        assert bot.get_relevant_knowledge("unrelated") == ""

    def test_corrupt_store_returns_empty_text(self, bot, tmp_path):
        """BDD: Given a corrupted knowledge base, When a prompt is matched,
        Then empty text is returned instead of raising."""
        kb = tmp_path / "knowledge_base_vuln.json"
        kb.write_text("{corrupt", encoding="utf-8")
        bot.knowledge_base_file = str(kb)
        assert bot.get_relevant_knowledge("anything") == ""

    def test_add_appends_canonical_list_format(self, bot, tmp_path):
        """BDD: Given any knowledge base shape, When a response is added,
        Then the store stays in the canonical list format."""
        kb = tmp_path / "knowledge_base_vuln.json"
        kb.write_text(json.dumps({"legacy": "old"}), encoding="utf-8")
        bot.knowledge_base_file = str(kb)
        bot.add_to_knowledge_base("new prompt", "new answer")
        records = json.loads(kb.read_text(encoding="utf-8"))
        assert isinstance(records, list)
        assert {"prompt": "new prompt", "response": "new answer"} in records

    def test_list_format_matches_by_prompt_text(self, bot, tmp_path):
        """BDD: Given a canonical store, When the prompt shares keywords,
        Then only matching records surface."""
        kb = tmp_path / "knowledge_base_vuln.json"
        kb.write_text(
            json.dumps(
                [
                    {"prompt": "smb enumeration on host", "response": "crackmapexec output"},
                    {"prompt": "kerberos user list", "response": "kerbrute output"},
                ]
            ),
            encoding="utf-8",
        )
        bot.knowledge_base_file = str(kb)
        got = bot.get_relevant_knowledge("run smb enumeration")
        assert "crackmapexec output" in got
        assert "kerbrute output" not in got


class TestGenerateFallback:
    def test_missing_model_served_by_chain(self, bot, tmp_path, monkeypatch):
        """BDD: Given a model that failed to load (no usable key), When the
        console analysis runs, Then the orchestrator chain answers."""
        bot.model = None
        served = orch.OrchestratorResult(
            text="chain plan",
            member="ollama-local",
            model="ollama:deepseek-r1:1.5b",
            backend="ollama",
            fallback_used=True,
            notice="[!] Primary model 'groq-cloud' failed: no key.",
        )
        monkeypatch.setattr(vulnbot, "complete_with_fallback", lambda *a, **k: served)
        target = tmp_path / "scan.nmap"
        target.write_text("Nmap scan report", encoding="utf-8")
        answer = bot.process_with_context(str(target))
        assert "chain plan" in answer

    def test_primary_error_banner_triggers_chain(self, bot, tmp_path, monkeypatch):
        """BDD: Given a primary backend returning an error banner, When the
        console analysis runs, Then the chain serves the answer."""
        class _DeadModel:
            def generate(self, prompt: str) -> str:
                return "Error from Groq: 401 invalid_api_key"

        bot.model = _DeadModel()
        served = orch.OrchestratorResult(
            text="fallback plan",
            member="pi-qwen",
            model="pi:local-model",
            backend="pi",
            fallback_used=True,
            notice="[!] Primary model 'groq-cloud' failed: 401.",
        )
        monkeypatch.setattr(vulnbot, "complete_with_fallback", lambda *a, **k: served)
        target = tmp_path / "scan.nmap"
        target.write_text("Nmap scan report", encoding="utf-8")
        answer = bot.process_with_context(str(target))
        assert "fallback plan" in answer
        assert answer.startswith("[!]")

    def test_primary_success_stays_primary(self, bot, tmp_path, monkeypatch):
        """BDD: Given a healthy primary backend, When the console analysis
        runs, Then the primary answer is returned and the chain is silent."""
        touched = []
        monkeypatch.setattr(
            vulnbot,
            "complete_with_fallback",
            lambda *a, **k: touched.append(1) or orch.OrchestratorResult(text="", backend="error"),
        )

        class _LiveModel:
            def generate(self, prompt: str) -> str:
                return "primary plan"

        bot.model = _LiveModel()
        target = tmp_path / "scan.nmap"
        target.write_text("Nmap scan report", encoding="utf-8")
        assert bot.process_with_context(str(target)) == "primary plan"
        assert touched == []

    def test_model_load_failure_returns_none_not_crash(self, bot, monkeypatch):
        """BDD: Given a placeholder Groq key, When the model is loaded,
        Then the load returns None instead of raising."""
        import modules.llm_factory as factory

        monkeypatch.setattr(factory, "load_payload", lambda *a, **k: {"api_key": "YOUR_API_KEY_HERE"})
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        assert bot._load_model() is None

    def test_missing_file_raises_read_error(self, bot, tmp_path):
        """BDD: Given a missing scan file, When the console analysis runs,
        Then the readable file error is raised as before."""
        with pytest.raises(FileNotFoundError):
            bot.process_with_context(str(tmp_path / "gone.nmap"))


class TestWebModeFallback:
    def test_stream_failure_serves_chain_answer(self, bot, tmp_path, monkeypatch):
        """BDD: Given web mode and a failing primary stream, When the web
        analysis runs, Then the chain answer streams instead."""
        bot.mode = "web"

        class _DeadStream:
            def stream_generate(self, prompt: str):
                raise RuntimeError("connection refused")
                yield ""

        bot.model = _DeadStream()
        served = orch.OrchestratorResult(
            text="web chain answer",
            member="ollama-local",
            model="ollama:m",
            backend="ollama",
            fallback_used=True,
            notice="[!] notice",
        )
        monkeypatch.setattr(vulnbot, "complete_with_fallback", lambda *a, **k: served)
        target = tmp_path / "scan.nmap"
        target.write_text("Nmap scan report", encoding="utf-8")
        body = "".join(bot._stream_with_fallback(bot.create_complex_prompt(target.read_text(encoding="utf-8"))))
        assert "web chain answer" in body

    def test_stream_error_banner_chunk_falls_back(self, bot, tmp_path, monkeypatch):
        """BDD: Given a stream yielding an error banner chunk, When the web
        analysis runs, Then the chain answer replaces the banner."""
        bot.mode = "web"

        class _BannerStream:
            def stream_generate(self, prompt: str):
                yield "Error from Groq: 401"

        bot.model = _BannerStream()
        served = orch.OrchestratorResult(
            text="banner-replaced answer",
            member="ollama-local",
            model="ollama:m",
            backend="ollama",
            fallback_used=True,
            notice="[!] notice",
        )
        monkeypatch.setattr(vulnbot, "complete_with_fallback", lambda *a, **k: served)
        target = tmp_path / "scan.nmap"
        target.write_text("Nmap scan report", encoding="utf-8")
        body = "".join(bot._stream_with_fallback(bot.create_complex_prompt(target.read_text(encoding="utf-8"))))
        assert "banner-replaced answer" in body
        assert "Error from Groq" not in body
