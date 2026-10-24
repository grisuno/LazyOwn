"""Bridge chain run outputs into the FactStore.

Spools captured step outputs as tool-output text under
``sessions/chain_facts/<run_id>/`` and ingests them through
:class:`skills.lazyown_facts.FactStore` so credentials, shares, access
evidence and paths discovered inside a chain become queryable tokens for
the next chains and for the golden-path solver.
"""

from __future__ import annotations

import datetime
import logging
from collections.abc import Callable
from pathlib import Path

from modules.chain_runner import ChainRunResult

log = logging.getLogger(__name__)

FACTS_SPOOL_DIRNAME = "chain_facts"


def spool_chain_outputs(
    result: ChainRunResult,
    sessions_dir: str | Path | None = None,
    fact_store_factory: Callable[[], object] | None = None,
) -> int:
    """Persist one chain run's outputs and ingest them as facts.

    Args:
        result: Completed :class:`ChainRunResult` to bridge.
        sessions_dir: Sessions directory override; defaults to
            ``sessions/``.
        fact_store_factory: Optional factory returning an object with
            ``ingest_text`` and ``save``; used for tests to isolate I/O.

    Returns:
        Total number of facts deduplicated into the FactStore.
    """
    base = Path(sessions_dir) if sessions_dir else Path("sessions")
    outputs = [step for step in result.steps if step.output and step.output.strip()]
    if not outputs:
        return 0
    run_dir = base / FACTS_SPOOL_DIRNAME / (result.run_id or datetime.datetime.now(datetime.UTC).strftime("%Y%m%d%H%M%S"))
    run_dir.mkdir(parents=True, exist_ok=True)
    target_hint = result.target or result.variables.get("target", "") or ""
    ingested_total = 0
    try:
        store = fact_store_factory() if fact_store_factory else _default_store()
    except Exception as exc:
        log.debug("FactStore unavailable for chain spool: %s", exc)
        return 0
    for step in outputs:
        host_hint = _host_hint(step.output, step.phase or "", target_hint)
        path = run_dir / f"{target_hint or 'chain'}_{step.id}.txt"
        try:
            path.write_text(step.output, encoding="utf-8", errors="replace")
        except OSError as exc:
            log.debug("chain spool write failed for %s: %s", path, exc)
            continue
        try:
            ingested_total += int(store.ingest_text(path, host_hint=host_hint))
        except Exception as exc:
            log.debug("chain spool ingest failed for %s: %s", path, exc)
    try:
        store.save()
    except Exception as exc:
        log.debug("FactStore save failed after chain spool: %s", exc)
    return ingested_total


def _default_store():
    """Build the production FactStore instance.

    Returns:
        A :class:`skills.lazyown_facts.FactStore` bound to config.
    """
    from skills.lazyown_facts import FactStore

    return FactStore()


def _host_hint(output: str, phase: str, target_hint: str) -> str:
    """Guess the owning host for a spooled output blob.

    Args:
        output: Captured step output.
        phase: Declared step phase.
        target_hint: Chain-level target fallback.

    Returns:
        The most eligible IP hint for FactStore attribution.
    """
    import re

    candidates = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", (output or "")[:2000])
    for candidate in candidates:
        if candidate == target_hint:
            return candidate
    if candidates:
        return candidates[0]
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", target_hint or ""):
        return target_hint
    return ""
