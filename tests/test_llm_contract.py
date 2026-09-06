"""LLM subsystem contract tests.

Encodes the single-source-of-truth contract for the LLM integration layer:

- ``modules.llm_factory`` is the canonical factory for every backend.
- ``modules.llm_client``, ``modules.llm_adapter``, ``modules.ai_model`` and
  ``modules.ai_fallback`` are the surviving support modules.
- ``modules.unified_llm_client`` is dead code and must not exist.

Any regressions that reintroduce a parallel LLM entry point or break the
factory surface are caught here.
"""

from __future__ import annotations

import importlib

import pytest

CANONICAL_BACKENDS = ("groq", "ollama", "openai", "anthropic", "deepseek", "auto")

LLM_FACTORY_PUBLIC = (
    "get_llm_backend",
    "get_llm_backend_raw",
    "try_get_llm_backend",
    "load_payload",
    "LLMBackendUnavailableError",
    "LLMBackendNotSupportedError",
    "SUPPORTED_BACKENDS",
)

LLM_CLIENT_PUBLIC = ("LLMClient", "get_client", "ask", "classify", "summarize")

AI_FALLBACK_PUBLIC = ("AIResult", "call")

AI_MODEL_PUBLIC = (
    "AIModel",
    "GroqModel",
    "OllamaModel",
    "OpenAIModel",
    "AnthropicModel",
    "DeepSeekModel",
)


def _import(name: str):
    return importlib.import_module(name)


class TestDeadModuleRemoved:
    def test_unified_llm_client_does_not_exist(self):
        with pytest.raises(ModuleNotFoundError):
            _import("modules.unified_llm_client")


class TestLlmFactoryContract:
    def test_factory_importable(self):
        _import("modules.llm_factory")

    def test_factory_exposes_public_api(self):
        factory = _import("modules.llm_factory")
        for name in LLM_FACTORY_PUBLIC:
            assert hasattr(factory, name), f"llm_factory missing {name}"

    def test_supported_backends_are_canonical(self):
        factory = _import("modules.llm_factory")
        assert tuple(factory.SUPPORTED_BACKENDS) == CANONICAL_BACKENDS

    def test_backend_constants_exposed(self):
        factory = _import("modules.llm_factory")
        assert factory.BACKEND_GROQ == "groq"
        assert factory.BACKEND_AUTO == "auto"
        assert factory.DEFAULT_BACKEND == "auto"

    def test_normalize_rejects_unknown_backend(self):
        factory = _import("modules.llm_factory")
        with pytest.raises(factory.LLMBackendNotSupportedError):
            factory._normalize_backend("nonsense_backend")

    def test_normalize_falls_back_to_auto_on_empty(self):
        factory = _import("modules.llm_factory")
        assert factory._normalize_backend(None) == "auto"
        assert factory._normalize_backend("") == "auto"


class TestSupportModulesContract:
    def test_llm_client_exposes_public_api(self):
        module = _import("modules.llm_client")
        for name in LLM_CLIENT_PUBLIC:
            assert hasattr(module, name), f"llm_client missing {name}"

    def test_llm_client_class_methods_present(self):
        module = _import("modules.llm_client")
        for method in ("ask", "classify", "summarize"):
            assert callable(getattr(module.LLMClient, method, None)), (
                f"LLMClient missing method {method}"
            )

    def test_ai_fallback_exposes_public_api(self):
        module = _import("modules.ai_fallback")
        for name in AI_FALLBACK_PUBLIC:
            assert hasattr(module, name), f"ai_fallback missing {name}"

    def test_ai_model_exposes_all_backends(self):
        module = _import("modules.ai_model")
        for name in AI_MODEL_PUBLIC:
            assert hasattr(module, name), f"ai_model missing {name}"

    def test_ai_fallback_reads_factory_constants(self):
        fallback = _import("modules.ai_fallback")
        factory = _import("modules.llm_factory")
        assert fallback._GROQ_MODEL == factory.DEFAULT_GROQ_MODEL
        assert fallback._OLLAMA_HOST == factory.DEFAULT_OLLAMA_HOST
