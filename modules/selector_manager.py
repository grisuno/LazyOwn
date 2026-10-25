"""Selector manager: deterministic priority cascade with provenance.

Every source in the auto-loop command cascade produces a ``Proposal``.
``select`` walks the ordered list, skips proposals whose base command is
blocked or malformed, and returns the winner together with the full
rejection trace so operators (and the digest) can see why a given source
lost. Deterministic: proposals are sorted by ``(priority, input order)``
and duplicate command strings collapse onto the best-priority instance.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

_UNKNOWN_SOURCE = "unknown"
_REJECTED_EMPTY = "empty command"


@dataclass
class Proposal:
    """One candidate command offered by a selection source."""

    command: str
    args: str = ""
    source: str = _UNKNOWN_SOURCE
    reason: str = ""
    priority: int = 100


@dataclass
class Selection:
    """The chosen proposal plus the reasons every other one lost."""

    command: str
    args: str
    source: str
    reason: str
    rejected: list[str] = field(default_factory=list)


def select(
    proposals: list[Proposal],
    is_blocked: Callable[[str], bool] | None = None,
) -> Selection | None:
    """Pick the first valid proposal; None when everything is filtered.

    Args:
        proposals: Candidates in any order; sorted by priority ascending.
        is_blocked: Optional veto predicate on the base command.

    Returns:
        Selection with command/args/source/reason and the rejection
        trace, or None when no proposal survived.
    """
    indexed = sorted(enumerate(proposals), key=lambda item: (item[1].priority, item[0]))
    seen: set[str] = set()
    rejected: list[str] = []
    for _index, proposal in indexed:
        base = proposal.command.strip().split()[0] if proposal.command.strip() else ""
        if not proposal.command.strip():
            rejected.append(f"{proposal.source}: {_REJECTED_EMPTY}")
            continue
        if proposal.command.strip() in seen:
            continue
        if is_blocked is not None and base and is_blocked(base):
            rejected.append(f"{proposal.source}: '{base}' blocked")
            continue
        seen.add(proposal.command.strip())
        return Selection(
            command=proposal.command.strip(),
            args=proposal.args,
            source=proposal.source,
            reason=proposal.reason,
            rejected=rejected,
        )
    return None
