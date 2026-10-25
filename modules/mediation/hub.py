"""Thin routing hub for specialised mediators.

The hub owns no coordination logic: it is a registry keyed by domain so
callers request a mediator instead of importing its colleagues. Adding a
new domain never changes existing consumers.
"""

from __future__ import annotations

import threading
from typing import Any

from modules.mediation.contracts import MediationDomains, MediatorContract

_LOCK = threading.Lock()
_HUB: MediationHub | None = None


class MediationHub:
    """Registry of specialised mediators keyed by domain."""

    def __init__(self) -> None:
        """Start with an empty registry."""
        self._mediators: dict[str, MediatorContract] = {}

    def register(self, mediator: MediatorContract) -> None:
        """Register a mediator under its declared domain.

        Args:
            mediator: Specialised mediator whose ``domain`` attribute is
                the routing key.
        """
        self._mediators[str(getattr(mediator, "domain", ""))] = mediator

    def mediator_for(self, domain: str) -> MediatorContract | None:
        """Return the mediator registered for a domain key, or None.

        Args:
            domain: Routing key such as ``loop.intel`` or ``chain``.

        Returns:
            The registered mediator, or None when absent.
        """
        return self._mediators.get(str(domain))

    def snapshot(self) -> dict[str, Any]:
        """Return high-level metadata for every registered mediator.

        Returns:
            Mapping of domain key to the mediator's describe() document.
        """
        return {domain: mediator.describe() for domain, mediator in sorted(self._mediators.items())}


def _build_default() -> MediationHub:
    """Create a hub preloaded with the default specialised mediators."""
    from modules.mediation.chain_mediator import ChainMediator
    from modules.mediation.feedback_mediator import FeedbackMediator
    from modules.mediation.intel_mediator import IntelMediator
    from modules.mediation.telemetry_mediator import TelemetryMediator

    hub = MediationHub()
    hub.register(IntelMediator())
    hub.register(FeedbackMediator())
    hub.register(TelemetryMediator())
    hub.register(ChainMediator())
    for domain in MediationDomains.ALL:
        if hub.mediator_for(domain) is None:
            raise KeyError(f"mediation: default domain '{domain}' has no mediator")
    return hub


def default_hub() -> MediationHub:
    """Return a fresh default-configured hub (test-safe, no singleton)."""
    return _build_default()


def get_hub() -> MediationHub:
    """Return the process-wide hub, building it on first use.

    Thread-safe: concurrent first-touch callers race on construction and
    the winner is shared.

    Returns:
        The shared MediationHub instance or a retry-exhausted empty hub.
    """
    global _HUB
    with _LOCK:
        if _HUB is None:
            _HUB = _build_default()
        return _HUB
