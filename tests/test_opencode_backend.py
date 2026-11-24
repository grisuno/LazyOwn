"""Contract tests for the OpenCode Zen LLM backend.

OpenCode Zen is an OpenAI-compatible gateway wired into the canonical
``modules.llm_factory`` selection path. These tests pin its registration,
API-key resolution (config and environment), model selection, and the
operator-configurable base URL without issuing any network calls.
"""

import importlib

import pytest

factory = importlib.import_module("modules.llm_factory")
ai_model = importlib.import_module("modules.ai_model")


class _FakeOpenAIClient:
    """Minimal stand-in for the OpenAI SDK client used in build tests.

    Records the constructor arguments so the tests can assert the gateway
    base URL and key without importing the real SDK or issuing requests.
    """

    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url


@pytest.fixture
def fake_openai(monkeypatch):
    """Patch the lazy OpenAI importer to the local fake client."""
    monkeypatch.setattr(ai_model._LazyImporter, "_OPENAI_CLIENT", _FakeOpenAIClient, raising=False)
    return _FakeOpenAIClient


class TestOpenCodeRegistration:
    def test_backend_is_supported(self):
        assert factory.BACKEND_OPENCODE == "opencode"
        assert "opencode" in factory.SUPPORTED_BACKENDS

    def test_backend_is_cloud_gated(self):
        assert factory.BACKEND_OPENCODE in factory._CLOUD_BACKENDS

    def test_default_model_and_keys(self):
        assert factory.default_model_for("opencode") == factory.DEFAULT_OPENCODE_MODEL
        assert factory.model_config_key("opencode") == factory.CONFIG_KEY_MODEL_OPENCODE
        assert factory.api_key_config_key("opencode") == factory.CONFIG_KEY_OPENCODE_API_KEY
        assert factory.backend_requires_api_key("opencode") is True

    def test_model_class_exported(self):
        assert hasattr(ai_model, "OpenCodeModel")


class TestOpenCodeBuild:
    def test_builds_from_config_key(self, fake_openai):
        config = {
            "llm_backend": "opencode",
            "opencode_api_key": "sk-test-opencode",
            "llm_model_opencode": "qwen3-coder",
        }
        model = factory.get_llm_backend_raw(config, backend="opencode")
        assert type(model).__name__ == "OpenCodeModel"
        assert model.model == "qwen3-coder"
        assert model.base_url == factory.DEFAULT_OPENCODE_BASE_URL
        assert model.client.api_key == "sk-test-opencode"

    def test_base_url_override(self, fake_openai):
        config = {
            "opencode_api_key": "sk-test-opencode",
            "opencode_base_url": "https://gateway.example/zen/v1",
        }
        model = factory.get_llm_backend_raw(config, backend="opencode")
        assert model.base_url == "https://gateway.example/zen/v1"
        assert model.client.base_url == "https://gateway.example/zen/v1"

    def test_default_model_when_unset(self, fake_openai):
        config = {"opencode_api_key": "sk-test-opencode"}
        model = factory.get_llm_backend_raw(config, backend="opencode")
        assert model.model == factory.DEFAULT_OPENCODE_MODEL

    def test_env_var_fallback(self, fake_openai, monkeypatch):
        monkeypatch.setenv(factory.ENV_OPENCODE_API_KEY, "sk-env-opencode")
        model = factory.get_llm_backend_raw({}, backend="opencode")
        assert type(model).__name__ == "OpenCodeModel"

    def test_missing_key_raises(self, monkeypatch):
        monkeypatch.delenv(factory.ENV_OPENCODE_API_KEY, raising=False)
        with pytest.raises(factory.LLMBackendUnavailableError):
            factory.get_llm_backend_raw({"llm_backend": "opencode"}, backend="opencode")

    def test_placeholder_key_rejected(self, monkeypatch):
        monkeypatch.delenv(factory.ENV_OPENCODE_API_KEY, raising=False)
        with pytest.raises(factory.LLMBackendUnavailableError):
            factory.get_llm_backend_raw({"opencode_api_key": "your_api_key_here"}, backend="opencode")

    def test_model_identifier_for_budget(self):
        config = {"llm_model_opencode": "glm-5"}
        assert factory._resolve_model_identifier("opencode", config) == "glm-5"
