"""Contract tests for the wizard LLM provider setup step.

Covers provider answer parsing, secret masking, the interactive
``_ask_llm`` update flow (with scripted prompts), and the provider-aware
readiness summary. No real I/O or network is exercised.
"""

from __future__ import annotations

import cli.wizard as wizard
from modules.llm_factory import SUPPORTED_BACKENDS


def _scripted_prompt(answers):
    iterator = iter(answers)

    def _fake(message=""):
        return next(iterator)

    return _fake


class TestNormalizeProviderAnswer:
    def test_blank_returns_none(self):
        assert wizard._normalize_provider_answer("") is None
        assert wizard._normalize_provider_answer("   ") is None

    def test_name_case_insensitive(self):
        assert wizard._normalize_provider_answer("Ollama") == "ollama"
        assert wizard._normalize_provider_answer("GROQ") == "groq"

    def test_number_selects_backend(self):
        backends = list(SUPPORTED_BACKENDS)
        assert wizard._normalize_provider_answer("1") == backends[0]
        assert wizard._normalize_provider_answer(str(len(backends))) == backends[-1]

    def test_out_of_range_number_returns_none(self):
        assert wizard._normalize_provider_answer("0") is None
        assert wizard._normalize_provider_answer("99") is None

    def test_unknown_name_returns_none(self):
        assert wizard._normalize_provider_answer("watson") is None


class TestMaskSecret:
    def test_empty_returns_not_set(self):
        assert wizard._mask_secret(None) == "not set"
        assert wizard._mask_secret("") == "not set"

    def test_long_value_masked_with_tail(self):
        assert wizard._mask_secret("gsk_abcdef123456") == "********3456"

    def test_short_value_never_shown_clear(self):
        masked = wizard._mask_secret("abc")
        assert masked != "abc"
        assert masked.startswith("********")


class TestAskLlm:
    def test_blank_answers_keep_everything(self, monkeypatch):
        monkeypatch.setattr(wizard, "_prompt", _scripted_prompt(["", "", ""]))
        params = {"llm_backend": "auto", "api_key": "gsk_old"}
        assert wizard._ask_llm(params) == {}

    def test_provider_change_by_name(self, monkeypatch):
        monkeypatch.setattr(wizard, "_prompt", _scripted_prompt(["ollama", "", ""]))
        updates = wizard._ask_llm({"llm_backend": "groq"})
        assert updates == {"llm_backend": "ollama"}

    def test_provider_change_by_number(self, monkeypatch):
        backends = list(SUPPORTED_BACKENDS)
        monkeypatch.setattr(wizard, "_prompt", _scripted_prompt(["2", "", ""]))
        updates = wizard._ask_llm({"llm_backend": backends[0]})
        assert updates == {"llm_backend": backends[1]}

    def test_invalid_provider_keeps_current(self, monkeypatch):
        monkeypatch.setattr(wizard, "_prompt", _scripted_prompt(["watson", "", ""]))
        assert wizard._ask_llm({"llm_backend": "groq"}) == {}

    def test_model_override_stored_in_provider_slot(self, monkeypatch):
        monkeypatch.setattr(
            wizard, "_prompt", _scripted_prompt(["openai", "gpt-4o-mini", "sk-x"])
        )
        updates = wizard._ask_llm({})
        assert updates == {
            "llm_backend": "openai",
            "llm_model_openai": "gpt-4o-mini",
            "openai_api_key": "sk-x",
        }

    def test_ollama_skips_key_prompt(self, monkeypatch):
        consumed: list = []

        def _fake(message=""):
            consumed.append(message)
            return "ollama" if len(consumed) == 1 else ""

        monkeypatch.setattr(wizard, "_prompt", _fake)
        updates = wizard._ask_llm({})
        assert updates == {"llm_backend": "ollama"}
        assert len(consumed) == 2
        assert all("api_key" not in message for message in consumed)

    def test_key_kept_when_blank(self, monkeypatch):
        monkeypatch.setattr(wizard, "_prompt", _scripted_prompt(["", "", ""]))
        assert wizard._ask_llm({"llm_backend": "groq", "api_key": "gsk_old"}) == {}

    def test_existing_key_prompt_shows_mask(self, monkeypatch):
        seen: list = []

        def _fake(message=""):
            seen.append(message)
            return ""

        monkeypatch.setattr(wizard, "_prompt", _fake)
        wizard._ask_llm({"llm_backend": "groq", "api_key": "gsk_abcdef123456"})
        key_prompts = [message for message in seen if message.startswith("  api_key")]
        assert key_prompts
        assert "gsk_abcdef123456" not in key_prompts[0]
        assert "3456" in key_prompts[0]


class TestReadinessLlm:
    def _row(self, params, label="LLM backend"):
        rows = {item.label: item for item in wizard._build_readiness(params)}
        return rows[label]

    def test_cloud_with_key_ok(self):
        row = self._row({"llm_backend": "groq", "api_key": "gsk_x"})
        assert row.status == "ok"
        assert "groq" in row.value

    def test_cloud_without_key_missing(self):
        row = self._row({"llm_backend": "openai"})
        assert row.status == "missing"
        assert "openai_api_key" in row.hint

    def test_ollama_keyless_ok(self):
        row = self._row({"llm_backend": "ollama"})
        assert row.status == "ok"
        assert "keyless" in row.value

    def test_invalid_backend_missing_with_fix_hint(self):
        row = self._row({"llm_backend": "watson"})
        assert row.status == "missing"
        assert "llm_backend" in row.hint

    def test_model_shown_in_value(self):
        row = self._row({"llm_backend": "ollama", "llm_model_ollama": "llama3.2"})
        assert "llama3.2" in row.value

    def test_sensitive_values_masked(self):
        rows = wizard._build_readiness(
            {"rhost": "1.2.3.4", "llm_backend": "groq", "api_key": "gsk_secretvalue"}
        )
        assert "gsk_secretvalue" not in "\n".join(
            f"{item.label} {item.value}" for item in rows
        )
