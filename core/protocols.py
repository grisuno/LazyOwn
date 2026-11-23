"""Stable structural interfaces (PEP 544 ``Protocol``) for high-level orchestration.

These protocols are the contract used by ``skills/autonomous_daemon.py``,
``skills/swan_agent.py`` and the MCP layer. New backends, selectors and memory
stores must implement these signatures so the orchestration layer never
depends on a concrete implementation (Dependency Inversion).

Type-only — no runtime side effects.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Selector(Protocol):
    """Suggests the next command for a given target/phase.

    Implementations include ``ReactiveSelector``, ``ParquetSelector``,
    ``BridgeSelector``, ``SWANSelector``, ``LLMSelector`` and
    ``FallbackSelector``.
    """

    name: str

    def suggest(
        self,
        target: str,
        phase: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Return ``{"command": str, "reasoning": str, "mitre": str}`` or ``None``."""


@runtime_checkable
class LLMBackend(Protocol):
    """Pluggable language model backend (Groq, Ollama, Claude, ...)."""

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> str:
        """Return the model completion as a string."""


@runtime_checkable
class MemoryStore(Protocol):
    """Persistent key/value store used by hive_mind, parquet_db and rag layers."""

    def put(self, key: str, value: Any) -> None: ...

    def get(self, key: str, default: Any = None) -> Any: ...

    def search(self, query: str, k: int = 5) -> list[dict[str, Any]]: ...


@runtime_checkable
class BridgeCatalog(Protocol):
    """Catalog of executable commands keyed by phase + OS."""

    def filter(self, phase: str, os_id: int) -> list[dict[str, Any]]:
        """Return command entries matching ``phase`` and ``os_id``."""


@runtime_checkable
class OutcomeEvaluator(Protocol):
    """Scores the outcome of an executed command for RL/MoE feedback."""

    def evaluate(
        self,
        command: str,
        output: str,
        target: str,
        phase: str,
    ) -> float:
        """Return a reward in ``[0.0, 1.0]``."""


@dataclass(frozen=True)
class C2Message:
    """One inbound operator message delivered over a C2 channel.

    Attributes:
        channel: Name of the channel the message arrived on.
        sender: Platform-side sender id (chat/user id).
        text: Raw message text.
    """

    channel: str
    sender: str
    text: str


@runtime_checkable
class C2Channel(Protocol):
    """Bidirectional operator channel into the C2 (telegram/discord/slack).

    Channels are transport-only: they deliver outbound text to the
    operator and poll inbound operator messages. Command execution is
    owned by an injected executor strategy, never by the channel.
    """

    name: str

    def send(self, text: str) -> bool:
        """Deliver one outbound message; return True on success."""

    def poll(self) -> list[C2Message]:
        """Return the new inbound messages since the last poll."""


__all__ = [
    "C2Channel",
    "C2Message",
    "Selector",
    "LLMBackend",
    "MemoryStore",
    "BridgeCatalog",
    "OutcomeEvaluator",
]
