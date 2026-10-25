"""Non-interactive fuzzy matching reusing the picker's scorer.

The curses dropdown in :mod:`cli.fuzzy_picker` already ranks candidates
with :class:`MatchScorer`. Typo correction (did you mean) and headless
suggestion need the same ranking without a terminal UI. This module is
the thin pure adapter: build picker items, rank, return names.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from cli.fuzzy_picker import MatchScorer, PickerConfig, PickerItem


@dataclass(frozen=True)
class FuzzyMatchConfig:
    """Centralized knobs for fuzzy suggestion."""

    limit: int = 5
    min_score: float = 0.0


DEFAULT_FUZZY_CONFIG = FuzzyMatchConfig()


def suggest(
    query: str,
    candidates: Sequence[str],
    limit: int = DEFAULT_FUZZY_CONFIG.limit,
    config: PickerConfig | None = None,
) -> list[str]:
    """Return up to limit candidate names ranked by relevance to query.

    Args:
        query: Raw operator input, possibly a typo or prefix fragment.
        candidates: Command or phase names to rank.
        limit: Maximum names returned.
        config: Picker scoring constants. Defaults to PickerConfig().

    Returns:
        Ranked names, strongest first. Empty when nothing scores above zero.
    """
    cleaned = str(query or "").strip().lower()
    names = [str(c) for c in candidates if str(c).strip()]
    if not cleaned or not names:
        return []
    scorer = MatchScorer(config or PickerConfig())
    items = [PickerItem(text=name) for name in names]
    ranked = scorer.rank(items, cleaned)
    out = [s.item.text for s in ranked if s.score > DEFAULT_FUZZY_CONFIG.min_score]
    return out[: max(limit, 0)]


def did_you_mean(query: str, candidates: Sequence[str]) -> str | None:
    """Return the single best correction for query or None.

    Args:
        query: Raw operator input.
        candidates: Names to correct against.

    Returns:
        Best candidate name, or None when no candidate scores.
    """
    ranked = suggest(query, candidates, limit=1)
    return ranked[0] if ranked else None


__all__ = ["FuzzyMatchConfig", "DEFAULT_FUZZY_CONFIG", "suggest", "did_you_mean"]
