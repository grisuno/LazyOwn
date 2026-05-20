"""LLM backend factory and selection utilities.

This module centralizes language model instantiation so that every caller
in the framework reads its provider, model name, host, and credentials
from a single source: ``payload.json``. The factory removes hardcoded
model strings duplicated across six callers and enforces the
Dependency Inversion Principle by returning the abstract :class:`AIModel`
type while keeping the concrete backend choice under operator control.

Adding a new backend means implementing :class:`AIModel` and registering
its identifier in :data:`SUPPORTED_BACKENDS`. No other module needs to
change.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Mapping

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_MODULE_DIR, os.pardir))
for _entry in (_PROJECT_ROOT, _MODULE_DIR):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

try:
    from modules.ai_model import AIModel, GroqModel, OllamaModel
except ModuleNotFoundError:
    from ai_model import AIModel, GroqModel, OllamaModel  # type: ignore[no-redef]

from core.protocols import LLMBackend

_REQUIRED_LLM_BACKEND_METHODS = ("complete",)
for _backend_class in (GroqModel, OllamaModel):
    for _method_name in _REQUIRED_LLM_BACKEND_METHODS:
        if not callable(getattr(_backend_class, _method_name, None)):
            raise RuntimeError(
                f"{_backend_class.__name__} does not implement "
                f"core.protocols.LLMBackend.{_method_name}()."
            )


BACKEND_GROQ = "groq"
BACKEND_OLLAMA = "ollama"
BACKEND_AUTO = "auto"

SUPPORTED_BACKENDS = (BACKEND_GROQ, BACKEND_OLLAMA, BACKEND_AUTO)

CONFIG_KEY_BACKEND = "llm_backend"
CONFIG_KEY_MODEL_GROQ = "llm_model_groq"
CONFIG_KEY_MODEL_OLLAMA = "llm_model_ollama"
CONFIG_KEY_OLLAMA_HOST = "ollama_host"
CONFIG_KEY_API_KEY = "api_key"
CONFIG_KEY_API_KEY_PLACEHOLDER = "api_key"

DEFAULT_BACKEND = BACKEND_AUTO
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_OLLAMA_MODEL = "deepseek-r1:1.5b"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"

ENV_GROQ_API_KEY = "GROQ_API_KEY"


class LLMBackendUnavailableError(RuntimeError):
    """Raised when no LLM backend can be instantiated from the current config."""


class LLMBackendNotSupportedError(ValueError):
    """Raised when the requested backend identifier is unknown."""


def load_payload(payload_path: str | None = None) -> dict[str, Any]:
    """Read ``payload.json`` from disk and return it as a dictionary.

    Args:
        payload_path: Optional explicit path. Defaults to the repository's
            ``payload.json`` resolved relative to this module's parent.

    Returns:
        The parsed payload mapping, or an empty dictionary if the file
        is missing or unreadable. Errors are swallowed so the factory
        can fall back to environment variables and defaults.
    """
    if payload_path is None:
        module_dir = os.path.dirname(os.path.abspath(__file__))
        payload_path = os.path.abspath(os.path.join(module_dir, "..", "payload.json"))
    if not os.path.exists(payload_path):
        return {}
    try:
        with open(payload_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


def _resolve_api_key(config: Mapping[str, Any]) -> str | None:
    """Return a usable Groq API key or ``None`` when no real key is set.

    The placeholder string in ``payload.json`` ("api_key") is treated as
    "unset" so the factory falls through to the next backend instead of
    sending a doomed request.

    Args:
        config: A mapping derived from ``payload.json``.

    Returns:
        The first non-placeholder API key found in the configuration or
        the ``GROQ_API_KEY`` environment variable, or ``None``.
    """
    candidate = config.get(CONFIG_KEY_API_KEY)
    if isinstance(candidate, str) and candidate and candidate != CONFIG_KEY_API_KEY_PLACEHOLDER:
        return candidate
    env_value = os.environ.get(ENV_GROQ_API_KEY)
    if env_value:
        return env_value
    return None


def _normalize_backend(backend: str | None) -> str:
    """Validate and normalize a backend identifier.

    Args:
        backend: Raw backend string read from config or call site.

    Returns:
        A lowercase identifier guaranteed to be in :data:`SUPPORTED_BACKENDS`.

    Raises:
        LLMBackendNotSupportedError: When ``backend`` is non-empty but
            not a recognized identifier.
    """
    if backend is None or backend == "":
        return DEFAULT_BACKEND
    candidate = backend.strip().lower()
    if candidate not in SUPPORTED_BACKENDS:
        raise LLMBackendNotSupportedError(
            f"Unsupported LLM backend '{backend}'. "
            f"Supported: {', '.join(SUPPORTED_BACKENDS)}"
        )
    return candidate


def _build_groq(config: Mapping[str, Any]) -> AIModel:
    """Instantiate a Groq backend or raise when no API key is available.

    Args:
        config: A mapping derived from ``payload.json``.

    Returns:
        A configured :class:`GroqModel` instance.

    Raises:
        LLMBackendUnavailableError: When no valid Groq API key is found.
    """
    api_key = _resolve_api_key(config)
    if not api_key:
        raise LLMBackendUnavailableError(
            "Groq backend selected but no API key is configured. "
            f"Set '{CONFIG_KEY_API_KEY}' in payload.json or export {ENV_GROQ_API_KEY}."
        )
    model_name = config.get(CONFIG_KEY_MODEL_GROQ) or DEFAULT_GROQ_MODEL
    return GroqModel(api_key=api_key, model=model_name)


def _build_ollama(config: Mapping[str, Any]) -> AIModel:
    """Instantiate an Ollama backend using configured model and host.

    Args:
        config: A mapping derived from ``payload.json``.

    Returns:
        A configured :class:`OllamaModel` instance.
    """
    model_name = config.get(CONFIG_KEY_MODEL_OLLAMA) or DEFAULT_OLLAMA_MODEL
    host = config.get(CONFIG_KEY_OLLAMA_HOST) or DEFAULT_OLLAMA_HOST
    return OllamaModel(model=model_name, host=host)


def get_llm_backend(
    config: Mapping[str, Any] | None = None,
    backend: str | None = None,
) -> AIModel:
    """Return a concrete :class:`AIModel` selected by configuration.

    The selection order is:

    1. Explicit ``backend`` argument when provided.
    2. ``llm_backend`` key from ``config`` (or loaded ``payload.json``).
    3. :data:`DEFAULT_BACKEND` (``"auto"``).

    When the resolved backend is ``"auto"`` the factory tries Groq first
    (if an API key is available) and falls back to Ollama. Any other
    explicit selection is honoured strictly: callers receive
    :class:`LLMBackendUnavailableError` rather than a silent fallback so
    they can decide whether to degrade or raise.

    Args:
        config: Optional pre-loaded payload mapping. When ``None`` the
            payload is read from disk.
        backend: Optional override for the backend identifier. Takes
            precedence over the configuration value.

    Returns:
        A configured :class:`AIModel` instance that also structurally
        satisfies :class:`core.protocols.LLMBackend`, ready for either
        ``generate`` or ``complete`` calls.

    Raises:
        LLMBackendNotSupportedError: When an unsupported identifier is
            requested.
        LLMBackendUnavailableError: When the requested backend cannot be
            constructed from the current environment (for example, Groq
            selected with no API key).
    """
    resolved_config: Mapping[str, Any] = config if config is not None else load_payload()
    raw_backend = backend if backend is not None else resolved_config.get(CONFIG_KEY_BACKEND)
    normalized = _normalize_backend(raw_backend)

    if normalized == BACKEND_GROQ:
        return _build_groq(resolved_config)
    if normalized == BACKEND_OLLAMA:
        return _build_ollama(resolved_config)

    if _resolve_api_key(resolved_config):
        try:
            return _build_groq(resolved_config)
        except LLMBackendUnavailableError:
            pass
    return _build_ollama(resolved_config)


def try_get_llm_backend(
    config: Mapping[str, Any] | None = None,
    backend: str | None = None,
) -> AIModel | None:
    """Return a backend or ``None`` if construction fails for any reason.

    Wraps :func:`get_llm_backend` so call sites that prefer to degrade
    gracefully (CLI assistants, opportunistic enrichers) can keep
    working when no LLM is reachable.

    Args:
        config: Optional pre-loaded payload mapping.
        backend: Optional explicit backend identifier.

    Returns:
        A configured :class:`AIModel`, or ``None`` when no backend is
        available.
    """
    try:
        return get_llm_backend(config=config, backend=backend)
    except (LLMBackendNotSupportedError, LLMBackendUnavailableError):
        return None


__all__ = [
    "BACKEND_AUTO",
    "BACKEND_GROQ",
    "BACKEND_OLLAMA",
    "CONFIG_KEY_API_KEY",
    "CONFIG_KEY_BACKEND",
    "CONFIG_KEY_MODEL_GROQ",
    "CONFIG_KEY_MODEL_OLLAMA",
    "CONFIG_KEY_OLLAMA_HOST",
    "DEFAULT_BACKEND",
    "DEFAULT_GROQ_MODEL",
    "DEFAULT_OLLAMA_HOST",
    "DEFAULT_OLLAMA_MODEL",
    "ENV_GROQ_API_KEY",
    "LLMBackendNotSupportedError",
    "LLMBackendUnavailableError",
    "SUPPORTED_BACKENDS",
    "get_llm_backend",
    "load_payload",
    "try_get_llm_backend",
]
