"""Pre-loop bootstrap for an autonomous objective.

Single-responsibility contract extracted from the daemon ``_run_objective``
coroutine: everything that must happen once, before the per-step loop begins —
goal decomposition, task constraints, the global scope-deny gate, asynchronous
enrichment, the planner frontier (sole intent generator) and the intercept
guard.

The scope gate is the only early-abort: a denied target emits ``STEP_BLOCKED``
and returns a result flagged ``scope_denied`` without building the frontier or
guard, so the caller ends the objective with no steps. Every other concern
degrades independently and never raises.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

log = logging.getLogger("lazyown.daemon")


@dataclass
class ObjectiveBootstrap:
    """Result of bootstrapping one objective before its step loop.

    Attributes:
        goal_tracker: GoalTracker over the decomposed objective, or None.
        task_constraints: Loaded task constraints (deny wins), or None.
        frontier: Planner frontier used as the sole intent generator, or None.
        guard: Intercept guard for per-command checks, or None.
        scope_denied: Scope-deny reason; empty string when the target is in
            scope. A non-empty value means the caller must end the objective
            immediately with no steps.
    """

    goal_tracker: Any | None
    task_constraints: Any | None
    frontier: Any | None
    guard: Any | None
    scope_denied: str


def bootstrap_objective(
    objective_id: str,
    objective_text: str,
    target: str,
    world_model: Any,
    obs_parser: Any,
    planner: Any,
    emit: Callable[[str, dict[str, Any]], None],
    load_payload: Callable[[], dict],
) -> ObjectiveBootstrap:
    """Run every once-per-objective setup step before the loop.

    Args:
        objective_id: Owning objective identifier (for event correlation).
        objective_text: Natural-language objective to decompose into goals.
        target: Host under assessment (scope gate and enrichment input).
        world_model: World model, bound into the planner factory; may be None.
        obs_parser: Observation parser, bound into the planner factory.
        planner: Pre-built planner, or None to construct the default one.
        emit: Event emitter ``(name, payload) -> None``.
        load_payload: Callable returning the current ``payload.json`` as a dict.

    Returns:
        An ``ObjectiveBootstrap``. When ``scope_denied`` is non-empty the
        frontier and guard are None and the caller must stop immediately.
    """
    goal_tracker = None
    task_constraints = None
    try:
        from modules.goals import GoalTracker, decompose_rule_based, load_constraints

        goal_tracker = GoalTracker(decompose_rule_based(objective_text))
        task_constraints = load_constraints(load_payload())
        emit(
            "GOALS_DECOMPOSED",
            {"objective_id": objective_id, "goals": [g.text for g in goal_tracker.goals]},
        )
    except Exception as goals_exc:
        log.debug("round-0 goals error: %s", goals_exc)

    try:
        from modules.intercept import scope_blocked

        scope_hit = scope_blocked(target)
    except Exception:
        scope_hit = ""
    if scope_hit:
        log.info("[%s] scope denied: %s (%s)", objective_id, target, scope_hit)
        emit(
            "STEP_BLOCKED",
            {
                "objective_id": objective_id,
                "step": 0,
                "command": target,
                "reason": f"scope:{scope_hit}",
            },
        )
        return ObjectiveBootstrap(
            goal_tracker=goal_tracker,
            task_constraints=task_constraints,
            frontier=None,
            guard=None,
            scope_denied=scope_hit,
        )

    try:
        from modules.enrich import shared_engine

        shared_engine().submit(target)
    except Exception as enrich_exc:
        log.debug("enrich submit error: %s", enrich_exc)

    frontier = None
    try:
        from modules.planner import Frontier, TodoList

        if planner is None:
            from modules.planner import Planner

            planner = Planner(
                world_model=(lambda: world_model),
                obs_parser=(lambda: obs_parser),
            )
        frontier = Frontier(planner, todos=TodoList())
    except Exception:
        frontier = None

    try:
        from modules.intercept import Guard

        guard = Guard()
    except Exception:
        guard = None

    return ObjectiveBootstrap(
        goal_tracker=goal_tracker,
        task_constraints=task_constraints,
        frontier=frontier,
        guard=guard,
        scope_denied="",
    )
