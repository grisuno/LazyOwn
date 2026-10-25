"""Deterministic harness gate for the LazyOwn loop.

When the harness is active the loop refuses every non-deterministic
decision path: planner LLM candidates, worker tool-calling agents,
worker LLM step suggestions, SWAN ensemble ensemble planning and LLM
streaming. Objectives and golden paths drive the loop instead.
"""

from __future__ import annotations

import logging
import os

log = logging.getLogger(__name__)

HARNESS_ENV_FLAG = "LAZYOWN_HARNESS"

GATE_NAMES: frozenset[str] = frozenset(
    {
        "plan_llm",
        "worker_agentic",
        "worker_llm_steps",
        "swan",
        "llm_stream",
        "recovery_llm",
    }
)


def harness_enabled() -> bool:
    """Return True when the deterministic harness is active.

    Sources (in order): the ``LAZYOWN_HARNESS`` environment flag, the
    ``orchestrator.harness`` payload key and the active orchestrator
    profile named ``harness``.

    Returns:
        True when the harness profile is engaged.
    """
    raw_env = os.getenv(HARNESS_ENV_FLAG, "").strip().lower()
    if raw_env in ("1", "true", "yes", "on"):
        return True
    if raw_env in ("0", "false", "no", "off"):
        return False
    try:
        from core.config import load_payload

        payload = load_payload() or {}
        section = payload.get("orchestrator") or {}
        if isinstance(section, dict):
            if section.get("harness") is True:
                return True
            if section.get("harness") is False:
                return False
    except Exception:
        pass
    try:
        from modules.orchestrator_config import active_profile

        return str(active_profile() or "").strip().lower() == "harness"
    except Exception:
        return False


def gate(name: str) -> bool:
    """Return whether one decision surface may remain stochastic.

    Args:
        name: Gate name from :data:`GATE_NAMES`.

    Returns:
        False whenever the harness is active (deterministic-only
        regime); True otherwise, regardless of the gate name.
    """
    return not harness_enabled()
