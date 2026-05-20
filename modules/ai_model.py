"""Concrete language model backends for LazyOwn.

This module exposes the abstract :class:`AIModel` together with two
concrete implementations: :class:`GroqModel` (cloud) and
:class:`OllamaModel` (local). Every implementation honours both the
historical ``generate``/``stream_generate`` interface used by the
existing AI agents and the :func:`complete` signature defined in
``core.protocols.LLMBackend``. Callers depending on the abstract type
remain decoupled from the concrete provider.

For provider selection driven by ``payload.json`` use
:func:`modules.llm_factory.get_llm_backend`. Do not instantiate the
concrete classes from new code unless a test explicitly requires it.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Generator, Union

import requests
from groq import Groq


DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_OLLAMA_MODEL = "deepseek-r1:1.5b"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_COMPLETE_MAX_TOKENS = 1024
DEFAULT_COMPLETE_TEMPERATURE = 0.2
HTTP_OK = 200


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


class GroqModel(AIModel):
    """Groq-hosted Llama backend.

    Uses the official ``groq`` SDK. Errors are returned as readable
    strings rather than raised so callers do not have to wrap every
    invocation in try/except blocks for surface-level failures.
    """

    def __init__(self, api_key: str, model: str = DEFAULT_GROQ_MODEL) -> None:
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        """Return a single completion for ``prompt``.

        Args:
            prompt: The full prompt string sent to Groq.

        Returns:
            The model completion or a human-readable error string.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as exc:
            return f"Error from Groq: {exc}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        """Yield streamed completion chunks for ``prompt``.

        Args:
            prompt: The full prompt string sent to Groq.

        Yields:
            Successive content fragments emitted by the Groq stream.
        """
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
            yield f"Error streaming from Groq: {exc}"

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


__all__ = [
    "AIModel",
    "DEFAULT_COMPLETE_MAX_TOKENS",
    "DEFAULT_COMPLETE_TEMPERATURE",
    "DEFAULT_GROQ_MODEL",
    "DEFAULT_OLLAMA_HOST",
    "DEFAULT_OLLAMA_MODEL",
    "GroqModel",
    "OllamaModel",
]
