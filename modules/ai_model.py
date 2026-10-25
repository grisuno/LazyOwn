"""Concrete language model backends for LazyOwn.

This module exposes the abstract :class:`AIModel` together with five
concrete implementations: :class:`GroqModel` (cloud),
:class:`OllamaModel` (local), :class:`OpenAIModel` (cloud),
:class:`AnthropicModel` (cloud), and :class:`DeepSeekModel` (cloud).
Every implementation honours both the historical
``generate``/``stream_generate`` interface used by the existing AI
agents and the :func:`complete` signature defined in
``core.protocols.LLMBackend``. Callers depending on the abstract type
remain decoupled from the concrete provider.

For provider selection driven by ``payload.json`` use
:func:`modules.llm_factory.get_llm_backend`. Do not instantiate the
concrete classes from new code unless a test explicitly requires it.
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Union

import requests

logger = logging.getLogger(__name__)

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_OLLAMA_MODEL = "deepseek-r1:1.5b"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"
DEFAULT_LLAMACPP_MODEL = "local-model"
DEFAULT_LLAMACPP_HOST = "http://127.0.0.1:8080"
DEFAULT_COMPLETE_MAX_TOKENS = 1024
DEFAULT_COMPLETE_TEMPERATURE = 0.2
HTTP_OK = 200
REQUEST_CONNECT_TIMEOUT_SEC = 10.0
REQUEST_READ_TIMEOUT_SEC = 180.0


class AIModel(ABC):
    """Abstract base class for language model backends.

    Concrete subclasses must implement :meth:`generate` and
    :meth:`stream_generate`. A default :meth:`complete` implementation
    is provided that combines ``system`` and ``user`` prompts into the
    historical single-prompt format so subclasses gain
    ``core.protocols.LLMBackend`` compatibility for free.
    """

    @abstractmethod
    def generate(self, prompt: str) -> Union[str, Generator[str, None, None]]:
        """Return a non-streaming completion for ``prompt``."""

    @abstractmethod
    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        """Yield streaming completion chunks for ``prompt``."""

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = DEFAULT_COMPLETE_MAX_TOKENS,
        temperature: float = DEFAULT_COMPLETE_TEMPERATURE,
    ) -> str:
        """Return a completion conforming to ``core.protocols.LLMBackend``.

        The default implementation concatenates ``system`` and ``user``
        with explicit role markers and delegates to :meth:`generate`.
        Backends that natively support role-aware chat formats may
        override this method for higher fidelity.

        Args:
            system: System prompt establishing persona, constraints,
                and output contract.
            user: User-turn prompt with the concrete task.
            max_tokens: Advisory cap accepted for protocol parity.
                Concrete backends honour it when their SDK supports it.
            temperature: Advisory sampling temperature accepted for
                protocol parity.

        Returns:
            The completion as a string.
        """
        del max_tokens, temperature
        composite = f"[SYSTEM]\n{system}\n\n[USER]\n{user}"
        result = self.generate(composite)
        if isinstance(result, str):
            return result
        return "".join(chunk for chunk in result if isinstance(chunk, str))


class _LazyImporter:
    """Deferred importer to avoid import errors when optional SDKs are unavailable."""

    _GROQ_CLIENT = None
    _OPENAI_CLIENT = None
    _ANTHROPIC_CLIENT = None

    @classmethod
    def groq(cls):
        if cls._GROQ_CLIENT is None:
            from groq import Groq as _Groq

            cls._GROQ_CLIENT = _Groq
        return cls._GROQ_CLIENT

    @classmethod
    def openai(cls):
        if cls._OPENAI_CLIENT is None:
            from openai import OpenAI as _OpenAI

            cls._OPENAI_CLIENT = _OpenAI
        return cls._OPENAI_CLIENT

    @classmethod
    def anthropic(cls):
        if cls._ANTHROPIC_CLIENT is None:
            from anthropic import Anthropic as _Anthropic

            cls._ANTHROPIC_CLIENT = _Anthropic
        return cls._ANTHROPIC_CLIENT


class GroqModel(AIModel):
    """Groq-hosted Llama backend.

    Uses the official ``groq`` SDK. Errors are returned as readable
    strings rather than raised so callers do not have to wrap every
    invocation in try/except blocks for surface-level failures.
    """

    def __init__(self, api_key: str, model: str = DEFAULT_GROQ_MODEL) -> None:
        self.client = _LazyImporter.groq()(api_key=api_key)
        self.model = model

    def _model_chain(self) -> tuple[str, ...]:
        """Return the configured model first, then known-good fallbacks."""
        try:
            from modules.llm_factory import groq_model_chain

            chain = groq_model_chain()
        except Exception:
            chain = ()
        out: list[str] = []
        for candidate in (self.model, *chain):
            if candidate and candidate not in out:
                out.append(candidate)
        return tuple(out)

    def generate(self, prompt: str) -> str:
        """Return a single completion for ``prompt``.

        Fails over to a known-good model id when the configured one is
        unavailable (Groq answers 404 model_not_found for retired ids).

        Args:
            prompt: The full prompt string sent to Groq.

        Returns:
            The model completion or a human-readable error string.
        """
        from modules.llm_factory import is_model_missing_error

        last_error = ""
        for model in self._model_chain():
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                )
                return chat_completion.choices[0].message.content.strip()
            except Exception as exc:
                last_error = f"Error from Groq: {exc}"
                if not is_model_missing_error(exc):
                    break
        return last_error

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        """Yield streamed completion chunks for ``prompt``.

        Fails over to a known-good model id when the configured one is
        unavailable, mirroring :meth:`generate`.

        Args:
            prompt: The full prompt string sent to Groq.

        Yields:
            Successive content fragments emitted by the Groq stream.
        """
        from modules.llm_factory import is_model_missing_error

        last_error = ""
        for model in self._model_chain():
            try:
                stream = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                    stream=True,
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
                return
            except Exception as exc:
                last_error = f"Error streaming from Groq: {exc}"
                if not is_model_missing_error(exc):
                    break
        yield last_error

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = DEFAULT_COMPLETE_MAX_TOKENS,
        temperature: float = DEFAULT_COMPLETE_TEMPERATURE,
    ) -> str:
        """Return a chat completion using native role separation.

        Overrides the default :meth:`AIModel.complete` to leverage
        Groq's chat schema and to honour ``max_tokens`` / ``temperature``
        directly.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            return f"Error from Groq: {exc}"


class OllamaModel(AIModel):
    """Ollama-hosted local backend.

    Communicates with a local Ollama daemon via its HTTP API. The model
    identifier and host are configurable so operators can point at any
    Ollama-compatible endpoint without code changes.
    """

    def __init__(
        self,
        model: str = DEFAULT_OLLAMA_MODEL,
        host: str = DEFAULT_OLLAMA_HOST,
    ) -> None:
        self.model = model
        self.host = host

    def generate(self, prompt: str) -> str:
        """Return a single completion for ``prompt``.

        Args:
            prompt: The full prompt string sent to Ollama.

        Returns:
            The model completion or a human-readable error string.
        """
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=(REQUEST_CONNECT_TIMEOUT_SEC, REQUEST_READ_TIMEOUT_SEC),
            )
            if response.status_code == HTTP_OK:
                return response.json().get("response", "").strip()
            return f"Error from Ollama: {response.status_code} - {response.text}"
        except Exception as exc:
            return f"Error connecting to Ollama: {exc}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        """Yield streamed completion chunks for ``prompt``.

        Args:
            prompt: The full prompt string sent to Ollama.

        Yields:
            Successive ``response`` fields from the Ollama stream.
        """
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": True},
                timeout=(REQUEST_CONNECT_TIMEOUT_SEC, REQUEST_READ_TIMEOUT_SEC),
                stream=True,
            )
            if response.status_code == HTTP_OK:
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                    except json.JSONDecodeError:
                        continue
                    if "response" in chunk:
                        yield chunk["response"]
            else:
                yield f"Error from Ollama: {response.status_code}"
        except Exception as exc:
            yield f"Error streaming from Ollama: {exc}"


class LlamaCppModel(AIModel):
    """llama.cpp server backend (OpenAI-compatible ``/v1`` API, keyless).

    Talks to a locally hosted ``llama-server`` (see the ``lazy_llamacpp``
    addon) over HTTP. Every request carries connect/read timeouts so a
    dead server fails fast into the pool failover instead of hanging the
    loop. When the ``openai`` SDK is importable, ``client`` exposes a
    tool-calling chat client against the same endpoint so the agentic
    path can use this leg.
    """

    def __init__(
        self,
        model: str = DEFAULT_LLAMACPP_MODEL,
        host: str = DEFAULT_LLAMACPP_HOST,
    ) -> None:
        self.model = model
        self.host = (host or DEFAULT_LLAMACPP_HOST).rstrip("/")
        self.client = None
        try:
            self.client = _LazyImporter.openai()(api_key="sk-no-key-required", base_url=f"{self.host}/v1")
            try:
                self.client.model = model
            except Exception:
                pass
        except Exception:
            self.client = None

    def _chat(self, messages: list, max_tokens: int, stream: bool):
        """POST one chat request; return the raw response.

        Thinking is disabled: loop turns are short tool decisions where a
        reasoning trace would burn the token budget and risk empty
        content, while multi-turn strategy already lives in the
        conversation, not in one block.
        """
        return requests.post(
            f"{self.host}/v1/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "stream": stream,
                "enable_thinking": False,
            },
            timeout=(REQUEST_CONNECT_TIMEOUT_SEC, REQUEST_READ_TIMEOUT_SEC),
            stream=stream,
        )

    def generate(self, prompt: str) -> str:
        """Return a single completion for ``prompt``.

        Args:
            prompt: The full prompt string sent to the server.

        Returns:
            The completion text or a human-readable error string.
        """
        try:
            response = self._chat([{"role": "user", "content": prompt}], DEFAULT_COMPLETE_MAX_TOKENS, False)
            if response.status_code == HTTP_OK:
                choices = response.json().get("choices", [])
                if choices:
                    return str(choices[0].get("message", {}).get("content", "") or "").strip()
                return "Error from llama.cpp: empty choices"
            return f"Error from llama.cpp: {response.status_code} - {response.text}"
        except Exception as exc:
            return f"Error connecting to llama.cpp: {exc}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        """Yield streamed completion deltas for ``prompt``.

        Args:
            prompt: The full prompt string sent to the server.

        Yields:
            Successive content deltas from the SSE stream.
        """
        try:
            response = self._chat([{"role": "user", "content": prompt}], DEFAULT_COMPLETE_MAX_TOKENS, True)
            if response.status_code != HTTP_OK:
                yield f"Error from llama.cpp: {response.status_code}"
                return
            for line in response.iter_lines():
                if not line or not line.startswith(b"data:"):
                    continue
                data = line[5:].strip()
                if data == b"[DONE]":
                    break
                try:
                    chunk = json.loads(data.decode("utf-8"))
                except json.JSONDecodeError:
                    continue
                for choice in chunk.get("choices", []):
                    delta = (choice.get("delta", {}) or {}).get("content", "")
                    if delta:
                        yield delta
        except Exception as exc:
            yield f"Error streaming from llama.cpp: {exc}"

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = DEFAULT_COMPLETE_MAX_TOKENS,
        temperature: float = DEFAULT_COMPLETE_TEMPERATURE,
    ) -> str:
        """Role-aware completion through the chat endpoint."""
        try:
            response = self._chat(
                [{"role": "system", "content": system}, {"role": "user", "content": user}], max_tokens, False
            )
            if response.status_code == HTTP_OK:
                choices = response.json().get("choices", [])
                if choices:
                    return str(choices[0].get("message", {}).get("content", "") or "").strip()
            return ""
        except Exception:
            return ""


class OpenAIModel(AIModel):
    """OpenAI-hosted backend (GPT-4o, GPT-4, etc.).

    Uses the ``openai`` SDK. Requires an OpenAI API key.
    """

    def __init__(self, api_key: str, model: str = DEFAULT_OPENAI_MODEL) -> None:
        self.client = _LazyImporter.openai()(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logger.warning("OpenAI generate error: %s", exc)
            return f"Error from OpenAI: {exc}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as exc:
            logger.warning("OpenAI stream error: %s", exc)
            yield f"Error streaming from OpenAI: {exc}"

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = DEFAULT_COMPLETE_MAX_TOKENS,
        temperature: float = DEFAULT_COMPLETE_TEMPERATURE,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logger.warning("OpenAI complete error: %s", exc)
            return f"Error from OpenAI: {exc}"


class AnthropicModel(AIModel):
    """Anthropic Claude backend.

    Uses the ``anthropic`` SDK. Requires an Anthropic API key.
    """

    def __init__(self, api_key: str, model: str = DEFAULT_ANTHROPIC_MODEL) -> None:
        self.client = _LazyImporter.anthropic()(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=DEFAULT_COMPLETE_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        except Exception as exc:
            logger.warning("Anthropic generate error: %s", exc)
            return f"Error from Anthropic: {exc}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=DEFAULT_COMPLETE_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                for text in stream.text_stream:
                    if text:
                        yield text
        except Exception as exc:
            logger.warning("Anthropic stream error: %s", exc)
            yield f"Error streaming from Anthropic: {exc}"

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = DEFAULT_COMPLETE_MAX_TOKENS,
        temperature: float = DEFAULT_COMPLETE_TEMPERATURE,
    ) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return response.content[0].text.strip()
        except Exception as exc:
            logger.warning("Anthropic complete error: %s", exc)
            return f"Error from Anthropic: {exc}"


class DeepSeekModel(AIModel):
    """DeepSeek cloud backend.

    Uses the OpenAI-compatible API at api.deepseek.com.
    Requires a DeepSeek API key.
    """

    def __init__(self, api_key: str, model: str = DEFAULT_DEEPSEEK_MODEL) -> None:
        self.client = _LazyImporter.openai()(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logger.warning("DeepSeek generate error: %s", exc)
            return f"Error from DeepSeek: {exc}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as exc:
            logger.warning("DeepSeek stream error: %s", exc)
            yield f"Error streaming from DeepSeek: {exc}"

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = DEFAULT_COMPLETE_MAX_TOKENS,
        temperature: float = DEFAULT_COMPLETE_TEMPERATURE,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logger.warning("DeepSeek complete error: %s", exc)
            return f"Error from DeepSeek: {exc}"


__all__ = [
    "AIModel",
    "AnthropicModel",
    "DEFAULT_ANTHROPIC_MODEL",
    "DEFAULT_COMPLETE_MAX_TOKENS",
    "DEFAULT_COMPLETE_TEMPERATURE",
    "DEFAULT_DEEPSEEK_MODEL",
    "DEFAULT_GROQ_MODEL",
    "DEFAULT_OLLAMA_HOST",
    "DEFAULT_OLLAMA_MODEL",
    "DEFAULT_OPENAI_MODEL",
    "DeepSeekModel",
    "GroqModel",
    "OllamaModel",
    "OpenAIModel",
]
