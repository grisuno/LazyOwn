"""Intel-graph sink: rebuild the fused graph after meaningful outcomes."""

from __future__ import annotations

from pathlib import Path

from modules.intel_fusion import build_intel_graph, write_summary
from modules.outcome_bus import SESSIONS_DIR, OutcomeEvent

_KINDS = frozenset({"finding", "exploit", "emulation", "chain", "shell", "report"})


def apply(event: OutcomeEvent) -> bool:
    """Rebuild the intel graph and its summary.

    Args:
        event: Outcome that may change the graph.

    Returns:
        True when the graph was rebuilt.
    """
    if event.kind not in _KINDS:
        return False
    root = Path(str(event.metadata.get("sessions_dir") or SESSIONS_DIR))
    try:
        graph = build_intel_graph(root)
        write_summary(graph, root)
    except Exception:
        return False
    return True
