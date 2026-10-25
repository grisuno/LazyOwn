"""Ordered Metasploitable 2 gym matrix runner.

Walks the indexed gym vulnerabilities in severity order, executes one
chain per vector, and stores the structured run plus its CTF capture
under ``sessions/ctf/<vuln_id>/`` and ``sessions/ctf/matrix_run.json``.
"""

from __future__ import annotations

import datetime
import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from modules import ctf_capture, metasploitable_gym
from modules.chain_registry import get as get_chain
from modules.chain_runner import ChainRunner

log = logging.getLogger(__name__)

MATRIX_ARTIFACT_NAME = "matrix_run.json"

SEVERITY_ORDER: dict[str, int] = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
}

MAX_MATRIX_OUTPUT_CHARS = 20_000


def plan_matrix(
    target: str,
    sessions_dir: str | Path | None = None,
    only: list[str] | None = None,
    top_k: int = 0,
) -> list[dict]:
    """Build the ordered execution plan for the gym matrix.

    Args:
        target: Victim host IP.
        sessions_dir: Sessions directory override.
        only: Restrict to these vulnerability ids.
        top_k: Cap the plan to the first N entries (0 keeps all).

    Returns:
        Ordered plan entries with ``vuln_id``, ``chain_name`` and
        metadata; entries without a chain carry ``chain_name: ""``.
    """
    if not str(target or "").strip():
        raise ValueError("plan_matrix requires a target host")
    wanted = {str(item).strip() for item in (only or []) if str(item).strip()}
    entries = metasploitable_gym.vulnerabilities()
    ordered = sorted(
        entries,
        key=lambda e: (
            SEVERITY_ORDER.get(str(e.get("severity", "medium")).lower(), 9),
            str(e.get("id", "")),
        ),
    )
    plan: list[dict] = []
    for entry in ordered:
        vuln_id = str(entry.get("id") or "")
        if not vuln_id:
            continue
        if wanted and vuln_id not in wanted:
            continue
        chain_name = str(entry.get("chain") or "")
        plan.append(
            {
                "vuln_id": vuln_id,
                "chain_name": chain_name if get_chain(chain_name) is not None else "",
                "cve": str(entry.get("cve") or ""),
                "severity": str(entry.get("severity") or "medium"),
                "port": str(entry.get("port") or ""),
                "service": str(entry.get("service") or ""),
                "mitre": str(entry.get("mitre") or ""),
            }
        )
    if top_k > 0:
        plan = plan[:top_k]
    return plan


def run_matrix(
    target: str,
    *,
    executor: Callable[[str], str] | None = None,
    shell: Any = None,
    dry_run: bool = False,
    approver: Callable[[str, str], bool] | None = None,
    on_step: Callable[[Any], None] | None = None,
    sessions_dir: str | Path | None = None,
    only: list[str] | None = None,
    top_k: int = 0,
    lhost: str = "",
    lport: str = "",
) -> dict:
    """Execute every planned chain and verify its CTF capture.

    Each vector runs in sequence; a capture is verified from the
    aggregate step outputs and one outcome is published per capture.

    Args:
        target: Victim host IP.
        executor: Optional execution primitive for chain steps.
        shell: Optional live shell for verb steps.
        dry_run: Resolve the plan without executing anything.
        approver: Callback for confirm steps.
        on_step: Per-step observer shared across chains.
        sessions_dir: Sessions directory override.
        only: Restrict to these vulnerability ids.
        top_k: Cap the plan to the first N entries.
        lhost: Attacker host token.
        lport: Attacker port token.

    Returns:
        The matrix summary dict persisted to
        ``sessions/ctf/matrix_run.json``.
    """
    plan = plan_matrix(target, sessions_dir=sessions_dir, only=only, top_k=top_k)
    runs: list[dict] = []
    for item in plan:
        vuln_id = item["vuln_id"]
        record_run: dict[str, Any] = dict(item)
        record_run["target"] = target
        if not item["chain_name"]:
            record_run["status"] = "unavailable_chain"
            record_run["capture"] = "skipped"
            runs.append(record_run)
            continue
        chain = get_chain(item["chain_name"])
        if chain is None:
            record_run["status"] = "unavailable_chain"
            record_run["capture"] = "skipped"
            runs.append(record_run)
            continue
        tokens = {
            "target": target,
            "exploit": str((metasploitable_gym.get(vuln_id) or {}).get("exploit") or ""),
            "vuln": vuln_id,
            "port": item["port"],
            "lhost": lhost,
            "lport": lport,
        }
        tokens = {key: value for key, value in tokens.items() if value}
        runner = ChainRunner(
            chain,
            tokens=tokens,
            shell=shell,
            executor=executor,
            dry_run=dry_run,
            approver=approver,
            on_step=on_step,
        )
        result = runner.run()
        outputs = "\n".join(step.output for step in result.steps if step.output)
        record_run["status"] = "ok" if result.ok else "failed"
        record_run["run_id"] = result.run_id
        record_run["chain_output"] = outputs[:MAX_MATRIX_OUTPUT_CHARS]
        if dry_run:
            record_run["capture"] = "dry-run"
        else:
            try:
                from modules.chain_facts import spool_chain_outputs

                record_run["spooled_facts"] = spool_chain_outputs(
                    result,
                    sessions_dir=sessions_dir,
                )
            except Exception as exc:
                log.debug("chain facts spool failed: %s", exc)
            try:
                capture = ctf_capture.capture(
                    vuln_id,
                    target,
                    output=record_run["chain_output"],
                    sessions_dir=sessions_dir,
                )
                record_run["capture"] = capture["status"]
            except ValueError as exc:
                record_run["capture"] = "skipped"
                record_run["capture_error"] = str(exc)
        runs.append(record_run)

    summary_result = {
        "target": target,
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "dry_run": bool(dry_run),
        "runs": runs,
        "stats": _stats(runs),
    }
    _persist(summary_result, sessions_dir)
    return summary_result


def _stats(runs: list[dict]) -> dict[str, int]:
    """Tally matrix run statuses.

    Args:
        runs: Per-vuln run records.

    Returns:
        Count per status plus total.
    """
    counts: dict[str, int] = {"total": len(runs)}
    for run in runs:
        status = str(run.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def _persist(summary_result: dict, sessions_dir: str | Path | None) -> None:
    """Write the matrix summary atomically under sessions/ctf.

    Args:
        summary_result: Matrix summary dict.
        sessions_dir: Sessions directory override.
    """
    root = ctf_capture.output_dir(sessions_dir)
    root.mkdir(parents=True, exist_ok=True)
    artifact = root / MATRIX_ARTIFACT_NAME
    tmp = artifact.with_suffix(".tmp")
    tmp.write_text(json.dumps(summary_result, indent=2), encoding="utf-8")
    tmp.replace(artifact)
    log.info("gym matrix artifact written: %s", artifact)


def load_matrix(sessions_dir: str | Path | None = None) -> dict:
    """Read the persisted matrix summary.

    Args:
        sessions_dir: Sessions directory override.

    Returns:
        Stored summary dict, or ``{"runs": []}`` when missing.
    """
    root = ctf_capture.output_dir(sessions_dir)
    artifact = root / MATRIX_ARTIFACT_NAME
    try:
        return json.loads(artifact.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"runs": []}
