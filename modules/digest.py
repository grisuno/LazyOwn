"""Operator digest generation for loop runs.

Digests compress a run into three blocks an operator actually reads:
what ran and how it ended (steps/outcomes), what the run knows
(findings, facts, assets) and what to do next (paths forward: leftover
blocks, pending creds, untested assets). Written as ``digest_<task>.md``
next to the archived graphs so the operator can hand it to the next
shift without reading an activity log.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

_DIGEST_NAME = "digest_{task_id}.md"
_MAX_STEPS_IN_DIGEST = 40


def build_engine_digest(
    task_id: str,
    status: str,
    rounds: int,
    findings: list[str],
    facts: list[str],
    blocks: list[str],
    reaction_backlog: list[str] | None = None,
) -> str:
    """Render the engine-loop markdown digest.

    Args:
        task_id: Task this digest describes.
        status: Terminal loop status.
        rounds: Round count executed.
        findings: Finding summaries.
        facts: Recent fact summaries.
        blocks: Blocked bases that burned attempts.
        reaction_backlog: Reactive decisions parked but unused.
    """
    lines: list[str] = [f"# digest {task_id}", ""]
    lines.append(f"- status: {status}")
    lines.append(f"- rounds: {int(rounds)}")
    lines.append(f"- findings: {len(findings)}")
    lines.append("")
    if findings:
        lines.append("## findings")
        for finding in findings[:12]:
            lines.append(f"- {str(finding)[:200]}")
        lines.append("")
    if facts:
        lines.append("## facts")
        for fact in facts[-8:]:
            lines.append(f"- {str(fact)[:200]}")
        lines.append("")
    if blocks:
        lines.append("## blocked")
        for block_name in blocks:
            lines.append(f"- {block_name}")
        lines.append("")
    if reaction_backlog:
        lines.append("## parked reactions")
        for reaction in reaction_backlog[:6]:
            lines.append(f"- {str(reaction)[:180]}")
        lines.append("")
    lines.append("## next shift")
    lines.append(f"- run `lazy_status {task_id}` / `lazy_overview` for the graph state")
    lines.append(f"- archive + evidence are already under sessions/")
    return "\n".join(lines)


def write_digest(task_id: str, body: str, root: Path | None = None) -> str:
    """Persist the digest beside the archives; returns the written path."""
    path = (root or Path(".")) / _DIGEST_NAME.format(task_id=task_id)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return str(path)
    except OSError:
        return ""


def worker_results_digest(rows: list[dict]) -> tuple[list[str], list[str]]:
    """Extract displayed step lines and blocked bases from result dicts."""
    shown: list[str] = []
    blocks: set[str] = set()
    for result in (rows or [])[:_MAX_STEPS_IN_DIGEST]:
        shown.append(
            f"- #{result.get('intent_id', 0)} {result.get('worker', 'worker')} -> "
            f"{result.get('state', result.get('outcome', '?'))}"
        )
        for skipped in result.get("skipped_tools", []) or []:
            blocks.add(str(skipped))
    return shown, sorted(blocks)
