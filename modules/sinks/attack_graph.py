"""Attack-graph sink: rebuild the attack surface after meaningful outcomes."""

from __future__ import annotations

from pathlib import Path

from modules.attack_surface3d import build_attack_graph, refresh_summary
from modules.outcome_bus import SESSIONS_DIR, OutcomeEvent

_KINDS = frozenset({"finding", "exploit", "emulation", "chain", "shell", "report"})


def apply(event: OutcomeEvent) -> bool:
    """Rebuild the attack graph and its exposure summary.

    Args:
        event: Outcome that may change the graph.

    Returns:
        True when the graph was rebuilt.
    """
    if event.kind not in _KINDS:
        return False
    root = Path(str(event.metadata.get("sessions_dir") or SESSIONS_DIR))
    try:
        graph = build_attack_graph(root)
        refresh_summary(graph, root)
    except Exception:
        return False
    return True
