"""Bridge from the technique planner to the loop intent frontier.

Consolidates the two planner surfaces into one pipeline: the
world-model technique planner (:mod:`modules.planner`) proposes ranked
``PlanCandidate`` steps; the loop engine planner owns the intent
frontier. The bridge converts the best technique candidates into
intent summaries so the technique planner FEEDS the loop frontier
instead of running beside it.
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)

MAX_BRIDGE_CANDIDATES = 4
BRIDGE_PRIORITY = 6
BRIDGE_SUMMARY_LIMIT = 200


def planner_bridge_enabled() -> bool:
    """Return whether the technique->intent bridge is enabled (default True)."""
    try:
        from modules import orchestrator_config as oc

        section = dict(oc.profile_config().get("planner") or {})
        section.update(oc._section().get("planner") or {})
    except Exception:
        return True
    return bool(section.get("bridge_enabled", True))


def technique_candidate_summary(candidate) -> str:
    """Render one PlanCandidate as an intent summary line."""
    technique_id = str(getattr(candidate, "technique_id", "") or "")
    name = str(getattr(candidate, "name", "") or "").strip()
    command = str(getattr(candidate, "command", "") or "").strip()
    head = f"{name} ({technique_id})" if technique_id else name
    if command:
        return f"technique step: {head} -> {command}"[:BRIDGE_SUMMARY_LIMIT]
    return f"technique step: {head}"[:BRIDGE_SUMMARY_LIMIT]


def technique_intents(target: str, max_candidates: int = MAX_BRIDGE_CANDIDATES) -> list[str]:
    """Run the technique planner for a target and return intent summaries.

    Args:
        target: IP/hostname the technique planner plans for.
        max_candidates: Upper bound on converted candidates.

    Returns:
        Deduplicated intent summary strings (possibly empty; never raises).
    """
    try:
        from modules.planner import get_planner

        result = get_planner().plan(target, max_candidates=max(1, int(max_candidates)))
    except Exception as exc:
        log.debug("technique planner bridge error: %s", exc)
        return []
    summaries: list[str] = []
    for candidate in getattr(result, "candidates", []) or []:
        summary = technique_candidate_summary(candidate)
        if summary and summary not in summaries:
            summaries.append(summary)
    return summaries[: max(1, int(max_candidates))]


def bridge_candidates_for_task(
    target: str, existing: set[str], max_candidates: int = MAX_BRIDGE_CANDIDATES
) -> list[tuple[str, list[int], int]]:
    """Return bridge candidate tuples the engine planner can consume.

    Args:
        target: Target the technique planner is queried with.
        existing: Intent texts already on the task graph (dedupe set).
        max_candidates: Upper bound on returned candidates.

    Returns:
        List of ``(summary, anchor_ids, priority)``; anchors stay empty
        because the technique planner does not know the asset graph.
    """
    if not planner_bridge_enabled():
        return []
    out: list[tuple[str, list[int], int]] = []
    for summary in technique_intents(target, max_candidates=max_candidates):
        if summary in existing:
            continue
        out.append((summary, [], BRIDGE_PRIORITY))
    return out
