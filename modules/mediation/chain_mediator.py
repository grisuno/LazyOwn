"""Specialised mediator for the APT chain pipeline.

Owns the LLM completion dependency so chain code never imports the loop
god file directly. The ``modules.lazy_loop.LlmPool`` adapter lives here
and is resolved lazily at request time.
"""

from __future__ import annotations

from typing import Any


class LlmPoolPort:
    """Completion port backed by the loop LLM pool (resolved lazily)."""

    def complete(self, prompt: str, max_tokens: int = 300, task_id: str = "") -> str:
        """Complete one prompt through the LLM pool.

        Args:
            prompt: User prompt text.
            max_tokens: Upper bound of generated tokens.
            task_id: Ledger id for usage accounting.

        Returns:
            Completion text, or an empty string when the pool is absent.
        """
        try:
            from modules.lazy_loop import LlmPool

            return LlmPool().complete(prompt, max_tokens=max_tokens, task_id=task_id)
        except Exception:
            return ""

    def has_members(self) -> bool:
        """Report whether any LLM member is configured.

        Returns:
            True when the pool exposes at least one member.
        """
        try:
            from modules.lazy_loop import LlmPool

            return bool(LlmPool().members())
        except Exception:
            return False


class ChainMediator:
    """Mediate LLM completion and recovery planning for APT chains."""

    domain: str = "chain"

    def __init__(self) -> None:
        """Start with the default pool port."""
        self._llm_port = LlmPoolPort()

    def register_llm_port(self, port: Any) -> None:
        """Replace the completion port (injection point for tests/gyms).

        Args:
            port: Object satisfying :class:`LlmCompletionPort`.
        """
        self._llm_port = port

    def llm(self) -> LlmPoolPort:
        """Return the completion port for pipeline requests.

        Returns:
            The current LLM completion port.
        """
        return self._llm_port

    def describe(self) -> dict[str, Any]:
        """Return mediator metadata for diagnostics."""
        return {
            "domain": self.domain,
            "llm_port": type(self._llm_port).__name__,
        }
