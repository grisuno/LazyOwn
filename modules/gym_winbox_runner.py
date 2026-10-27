"""Ordered WinBox gym matrix runner.

Ensures the lab VM is reachable, then reuses the generic gym matrix
engine (:mod:`modules.gym_matrix_runner`) with the WinBox catalogue
(:mod:`modules.winbox_gym`): one chain per indexed vector in severity
order, captures verified under ``sessions/ctf/``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from modules import ctf_capture, gym_matrix_runner, winbox_gym
from modules.chain_registry import get as get_chain

log = logging.getLogger(__name__)


def plan_matrix(
    target: str,
    sessions_dir: str | Path | None = None,
    only: list[str] | None = None,
    top_k: int = 0,
) -> list[dict]:
    """Build the ordered execution plan for the WinBox gym matrix.

    Args:
        target: Victim host IP (the lab VM).
        sessions_dir: Sessions directory override.
        only: Restrict to these vector ids.
        top_k: Cap the plan to the first N entries (0 keeps all).

    Returns:
        Ordered plan entries with ``vuln_id``, ``chain_name`` and
        metadata.

    Raises:
        ValueError: When no target is provided.
    """
    return gym_matrix_runner.plan_matrix(
        target,
        sessions_dir=sessions_dir,
        only=only,
        top_k=top_k,
        catalogue=winbox_gym,
    )


def run_matrix(
    target: str,
    *,
    executor=None,
    shell: Any = None,
    dry_run: bool = False,
    approver=None,
    on_step=None,
    sessions_dir: str | Path | None = None,
    only: list[str] | None = None,
    top_k: int = 0,
    lhost: str = "",
    lport: str = "",
    ensure_vm: bool = True,
) -> dict:
    """Execute every planned WinBox chain and verify its capture.

    Args:
        target: Victim host IP (the lab VM).
        executor: Optional execution primitive for chain steps.
        shell: Optional live shell for verb steps.
        dry_run: Resolve the plan without executing anything.
        approver: Callback for confirm steps.
        on_step: Per-step observer shared across chains.
        sessions_dir: Sessions directory override.
        only: Restrict to these vector ids.
        top_k: Cap the plan to the first N entries.
        lhost: Attacker host token.
        lport: Attacker port token.
        ensure_vm: Bring the lab VM up before running (skipped in
            dry-run mode and when the target is already bound).

    Returns:
        The matrix summary dict persisted to ``sessions/ctf/matrix_run.json``.
    """
    if not str(target or "").strip():
        raise ValueError("run_matrix requires the WinBox lab VM IP")
    vm_note: dict[str, Any] = {}
    if ensure_vm and not dry_run:
        vm_note = winbox_gym.ensure_lab_ready()
        if not vm_note.get("success"):
            return {
                "target": target,
                "dry_run": False,
                "runs": [],
                "stats": {"total": 0, "ok": 0, "failed": 0, "skipped": 0},
                "error": str(vm_note.get("message") or "WinBox lab VM unavailable"),
            }
    result = gym_matrix_runner.run_matrix(
        target,
        executor=executor,
        shell=shell,
        dry_run=dry_run,
        approver=approver,
        on_step=on_step,
        sessions_dir=sessions_dir,
        only=only,
        top_k=top_k,
        lhost=lhost,
        lport=lport,
        catalogue=winbox_gym,
    )
    if vm_note:
        result["vm"] = {"ip": vm_note.get("ip", ""), "message": vm_note.get("message", "")}
    return result


def report(sessions_dir: str | Path | None = None) -> dict:
    """Aggregate WinBox CTF captures for the report pipeline.

    Args:
        sessions_dir: Sessions directory override.

    Returns:
        The :func:`modules.ctf_capture.summary` mapping.
    """
    return ctf_capture.summary(sessions_dir=sessions_dir)


def chain_available(vuln_id: str) -> Any | None:
    """Return the resolved chain for one WinBox vector, or None.

    Args:
        vuln_id: Vector id from the WinBox index playbook.

    Returns:
        The chain object, or None.
    """
    return get_chain(str((winbox_gym.get(vuln_id) or {}).get("chain", "")), winbox_gym.CHAINS_DIR)


__all__ = ["chain_available", "plan_matrix", "report", "run_matrix"]
