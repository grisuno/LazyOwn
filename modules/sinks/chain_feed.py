"""Chain-feed sink: stream chain steps into the autonomous loop.

One adapter from the outcome bus to the loop task state. A running chain
publishes ``chain_step`` events; this sink appends a trace record to the
owning task's activity log and, for failures the chain cannot resolve
itself (the event carries ``metadata.steer``), plants a pending hint
node so the planner proposes an approach around the blocker on the next
wake. Failures already handled by the chain (``on_fail`` branches,
``continue_on_error`` steps, benign alternatives) never steer: the chain
keeps navigating them locally.
"""

from __future__ import annotations

import re

from modules.outcome_bus import OutcomeEvent

_TASK_ID_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")


def apply(event: OutcomeEvent) -> bool:
    """Append one chain-step trace record and steer unhandled failures.

    Args:
        event: Outcome carrying a ``chain_step`` payload with run id,
            chain name, step id, status and steer flag.

    Returns:
        True when the task was fed (trace written even when steering is
        skipped); False when the event is out of scope or the task state
        could not be reached.
    """
    if event.kind != "chain_step":
        return False
    task_id = str(event.task_id or "")
    if not task_id or not _TASK_ID_RE.fullmatch(task_id):
        return False
    metadata = dict(event.metadata or {})
    chain = str(metadata.get("chain", "") or "chain")
    step_id = str(metadata.get("step_id", "") or "step")
    status = str(metadata.get("status", "") or "")
    try:
        from modules.lazy_loop import ActivityLog, ExplorationGraph

        ActivityLog(task_id).emit(
            worker=f"chain-{chain}",
            kind="chain-step",
            text=f"chain {chain} step {step_id} [{status}] {event.command or event.description}",
        )
    except Exception:
        return False
    if not bool(metadata.get("steer")):
        return True
    steer_key = f"{metadata.get('run_id', '')}:{step_id}"
    reason = str(event.description or "failed").strip()
    hint_text = f"chain {chain} step {step_id} failed ({reason}); propose an approach around it"[:200]
    try:
        graph = ExplorationGraph(task_id)
        for node in graph.list("hint"):
            if str(node.meta.get("steer_chain", "")) == steer_key:
                return True
        graph.add_node(
            "hint",
            hint_text,
            state="pending",
            meta={
                "steer_chain": steer_key,
                "chain": chain,
                "step_id": step_id,
                "run_id": str(metadata.get("run_id", "") or ""),
                "target": event.target,
            },
        )
    except Exception:
        pass
    return True
