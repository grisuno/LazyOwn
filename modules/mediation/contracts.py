"""Mediation contracts: the abstractions every participant depends on.

These interfaces carry no peer imports, so any module can participate in
coordination without importing the concrete loop or chain implementations.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


class MediationDomains:
    """Domain keys used to route mediating requests."""

    INTEL = "loop.intel"
    FEEDBACK = "loop.feedback"
    TELEMETRY = "loop.telemetry"
    CHAIN = "chain"

    ALL: tuple[str, ...] = (INTEL, FEEDBACK, TELEMETRY, CHAIN)

    @classmethod
    def is_known(cls, domain: str) -> bool:
        """Check whether a domain key is registered in the default set.

        Args:
            domain: Domain key candidate.

        Returns:
            True when the domain belongs to the default coordination set.
        """
        return domain in cls.ALL


class ActivityLogPort(Protocol):
    """Read-port for task-scoped loop activity records.

    Implemented by ``modules.lazy_loop.ActivityLog``; registered on the
    intel mediator as a factory by the loop engine at construction time,
    which is what breaks callers from importing the loop god file
    directly.
    """

    def read(self, limit: int = 200) -> list[dict]:
        """Return the latest activity records oldest-first.

        Args:
            limit: Maximum records returned from the tail.

        Returns:
            Record dicts, oldest first.
        """
        ...


@runtime_checkable
class LlmCompletionPort(Protocol):
    """Request-port for LLM pool completion used by the chain pipeline."""

    def complete(
        self,
        prompt: str,
        max_tokens: int = 300,
        task_id: str = "",
    ) -> str:
        """Complete one prompt with the configured LLM pool.

        Args:
            prompt: User prompt text.
            max_tokens: Upper bound of generated tokens.
            task_id: Ledger id for usage accounting.

        Returns:
            Completion text, or an empty string when unavailable.
        """
        ...

    def has_members(self) -> bool:
        """Report whether any LLM member is configured."""
        ...


@runtime_checkable
class MediatorContract(Protocol):
    """Interface every specialised mediator implements."""

    domain: str

    def describe(self) -> dict[str, Any]:
        """Return introspection metadata for diagnostics."""
        ...


@runtime_checkable
class MediationHubContract(Protocol):
    """Interface the routing hub exposes to consumers."""

    def mediator_for(self, domain: str) -> MediatorContract | None:
        """Return the mediator registered for a domain key, or None."""
        ...


def resolve(domain: str) -> MediatorContract:
    """Return the default-hub mediator for a domain key.

    Args:
        domain: One of :class:`MediationDomains`.

    Returns:
        The mediator registered under that domain.

    Raises:
        KeyError: when the domain is unknown to the default hub.
    """
    from modules.mediation.hub import get_hub

    mediator = get_hub().mediator_for(domain)
    if mediator is None:
        raise KeyError(f"mediation: no mediator registered for domain '{domain}'")
    return mediator
