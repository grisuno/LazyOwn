"""Shared kill-chain-phase to lookup-category mapping.

History- and catalog-driven selectors (``parquet``, ``bridge``) group their
lookups by coarse category rather than by the exact kill-chain phase, so a
``privesc`` phase also mines ``credential`` history and an ``exploit`` phase
also mines ``intrusion`` and ``brute_force``. The mapping lived privately in
the daemon; it is shared here so both runtimes resolve categories identically.
Unknown phases fall back to ``["other"]`` via :func:`categories_for`.
"""

from __future__ import annotations

PHASE_CATEGORIES: dict[str, list[str]] = {
    "recon": ["recon"],
    "enum": ["enum", "recon"],
    "exploit": ["exploit", "intrusion", "brute_force"],
    "privesc": ["privesc", "credential"],
    "lateral": ["lateral", "credential"],
    "report": ["other"],
}


def categories_for(phase: str) -> list[str]:
    """Return the lookup categories for a kill-chain phase.

    Args:
        phase: Canonical kill-chain phase name.

    Returns:
        The ordered categories to mine, or ``["other"]`` when the phase is
        unknown so a selector always has at least one category to try.
    """
    return PHASE_CATEGORIES.get(str(phase or "").strip().lower(), ["other"])


__all__ = ["PHASE_CATEGORIES", "categories_for"]
