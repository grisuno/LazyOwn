"""LazyBox — gym catalogue, launch surface and gamification intelligence.

LazyBox is the branded dashboard contract that crosses the red-team
gym catalogue with the campaign intelligence layer:

- catalogue: docker scenarios (:mod:`modules.lab_runtime`), challenge
  definitions (:mod:`modules.redteam_gym`) and their active runs
  (:mod:`modules.gym_registry`), each with live status.
- intel: per-challenge world-model host states, kill-chain snapshot,
  live shells and the challenge attempt history from the leaderboard.
- scoreboard: gym leaderboard plus the operator ELO, karma tier and
  badges from :mod:`cli.engagement_hooks`.

Launch/submit/stop delegate to :mod:`modules.redteam_gym` so LazyBox
adds one aggregation layer, not a second scoring engine.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

BRAND = "LazyBox"

_GYM_NODE_PREFIX = "gym-"


def _challenge_rows() -> list[dict[str, Any]]:
    """Return challenge definitions enriched with active-run state."""
    from modules import gym_registry, redteam_gym

    definitions = redteam_gym.list_challenges()
    active: dict[str, list[dict[str, Any]]] = {}
    try:
        for run in gym_registry.get_active_runs(selector="", operator=""):
            cid = str(run.get("challenge_id", "") or "")
            if cid:
                active.setdefault(cid, []).append(run)
    except Exception:
        active = {}
    rows: list[dict[str, Any]] = []
    for cid, chal in sorted(definitions.items()):
        runs = active.get(cid, [])
        first = dict(runs[0]) if runs else {}
        rows.append(
            {
                **chal,
                "active": bool(runs),
                "run_id": str(first.get("run_id", "") or ""),
                "operator": str(first.get("operator", "") or ""),
                "target": str(first.get("target", "") or ""),
                "started_at": float(first.get("started_at", 0.0) or 0.0),
                "elapsed": max(0.0, time.time() - float(first.get("started_at", 0.0) or 0.0)) if runs else 0.0,
            }
        )
    return rows


def _scenario_rows() -> list[dict[str, Any]]:
    """Return docker gym scenarios with live container status."""
    try:
        from modules.lab_runtime import LAB_SCENARIOS, container_ip, container_name, running_containers

        running = set(running_containers())
    except Exception:
        return []
    rows: list[dict[str, Any]] = []
    for name, info in sorted(LAB_SCENARIOS.items()):
        name_full = container_name(name)
        live = name_full in running
        rows.append(
            {
                "scenario": name,
                "description": str(info.get("description", "")),
                "difficulty": str(info.get("difficulty", "")),
                "running": live,
                "container": name_full,
                "ip": container_ip(name_full) if live else "",
                "ports": dict(info.get("ports", {}) or {}),
                "node_id": f"{_GYM_NODE_PREFIX}{name}",
            }
        )
    return rows


def _operator_state() -> dict[str, Any]:
    """Return the CLI operator gamification state (fail-soft)."""
    try:
        from cli.engagement_hooks import get_state_snapshot

        return dict(get_state_snapshot() or {})
    except Exception:
        return {}


def scoreboard() -> dict[str, Any]:
    """Return the gym leaderboard plus operator ELO/karma/badges.

    Returns:
        Dict with ``leaderboard`` rows (sorted by points) and the
        ``operator`` snapshot from the CLI engagement engine.
    """
    from modules import redteam_gym

    board = redteam_gym.leaderboard()
    rows = sorted(
        (dict(operator=name, **stats) for name, stats in (board or {}).items()),
        key=lambda row: int(row.get("total_points", 0) or 0),
        reverse=True,
    )
    return {"leaderboard": rows, "operator": _operator_state()}


def challenge_intel(challenge_id: str) -> dict[str, Any]:
    """Cross campaign intelligence for one challenge.

    Args:
        challenge_id: Challenge definition id.

    Returns:
        Dict with the definition, the active run (if any), the
        engagement context (phase/hosts/live shells), the kill-chain
        snapshot and this challenge's attempt history.
    """
    from modules import gym_registry, redteam_gym

    definition = redteam_gym.list_challenges().get(challenge_id)
    if not definition:
        return {"success": False, "error": f"unknown challenge: {challenge_id}"}
    run: dict[str, Any] = {}
    target = ""
    try:
        runs = gym_registry.get_active_runs(selector=challenge_id, operator="")
        if runs:
            run = dict(runs[0])
            target = str(run.get("target", "") or "")
    except Exception:
        run = {}
    intel: dict[str, Any] = {
        "success": True,
        "brand": BRAND,
        "challenge_id": challenge_id,
        "definition": definition,
        "run": run,
        "engagement": redteam_gym.engagement_context(target),
        "killchain": _killchain_snapshot(),
        "attempts": _attempt_history(challenge_id),
    }
    return intel


def _killchain_snapshot() -> dict[str, Any]:
    """Return the unified kill-chain snapshot (fail-soft)."""
    try:
        from modules.killchain import KillChain

        return dict(KillChain.snapshot() or {})
    except Exception:
        return {}


def _attempt_history(challenge_id: str) -> list[dict[str, Any]]:
    """Return leaderboard attempts recorded for one challenge."""
    from modules import redteam_gym

    attempts: list[dict[str, Any]] = []
    for _operator, stats in sorted((redteam_gym.leaderboard() or {}).items()):
        for attempt in stats.get("attempts", []) or []:
            if str(attempt.get("challenge_id", "")) == challenge_id:
                attempts.append(dict(operator=_operator, **attempt))
    return sorted(attempts, key=lambda row: float(row.get("completed_at", 0.0) or 0.0), reverse=True)


def catalogue() -> dict[str, Any]:
    """Return the full LazyBox catalogue snapshot.

    Returns:
        Dict with ``brand``, live docker ``scenarios``, ``challenges``
        (with active-run state), the ``scoreboard`` and the challenge
        ``totals``.
    """
    scenarios = _scenario_rows()
    challenges = _challenge_rows()
    return {
        "brand": BRAND,
        "scenarios": scenarios,
        "challenges": challenges,
        "scoreboard": scoreboard(),
        "totals": {
            "scenarios": len(scenarios),
            "scenarios_running": sum(1 for row in scenarios if row["running"]),
            "challenges": len(challenges),
            "challenges_active": sum(1 for row in challenges if row["active"]),
        },
    }


def start_challenge(
    challenge_id: str,
    target: str = "",
    spin_lab: bool = True,
    notify: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Launch one gym challenge (delegates to redteam_gym)."""
    from modules import redteam_gym

    result = redteam_gym.start_challenge(challenge_id, target=target, spin_lab=spin_lab, notify=notify)
    return dict(result or {})


def submit_challenge(
    techniques_used: list[str] | None = None,
    success: bool = True,
    run_id: str = "",
) -> dict[str, Any]:
    """Submit one completed challenge (delegates to redteam_gym)."""
    from modules import redteam_gym

    result = redteam_gym.submit_challenge(techniques_used=techniques_used, success=success, run_id=run_id)
    return dict(result or {})


def stop_challenges(selector: str = "") -> dict[str, Any]:
    """Stop gym runs (delegates to redteam_gym)."""
    from modules import redteam_gym

    result = redteam_gym.stop_challenges(selector)
    return dict(result or {})


__all__ = [
    "BRAND",
    "catalogue",
    "challenge_intel",
    "scoreboard",
    "start_challenge",
    "stop_challenges",
    "submit_challenge",
]
