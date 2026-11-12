"""Reproducible decision ledger for the autonomous loop.

Every next-action choice the loop makes is recorded here as one bounded
JSONL row, so an operator can answer "why did the harness run this?" and
re-execute a campaign deterministically. The schema is a decision audit:
digests of the decision inputs (the engagement context, the model prompt, the
deterministic-relevant config) plus a model-versus-rule fallback flag make each
decision auditable without storing raw secrets.

A decision produced by a deterministic selector (:mod:`modules.selection`)
carries ``model_fallback=False`` and empty prompt/reply digests; one produced
by the LLM planner carries ``model_fallback=True`` with both digests set. The
``filtered`` list names every candidate the harness rejected and the reason,
so a silently dropped command is never invisible again.

The ledger is append-only and self-rotating, mirroring
``modules.lazy_loop.record_worker_traces`` so the two ledgers share one I/O
discipline. Nothing here imports the loop runtime, keeping the module free of
import cycles and usable from tests in isolation.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

_BASE_DIR = Path(__file__).resolve().parent.parent.parent
DECISIONS_FILE = _BASE_DIR / "sessions" / "decisions.jsonl"
DECISIONS_MAX_BYTES = 8 * 1024 * 1024
DECISIONS_KEEP_LINES = 20000
_DIGEST_WIDTH = 16
_DIRECTORY_MODE = 0o700
_CONFIG_KEYS = (
    "loop_planner_temperature",
    "loop_deterministic",
    "loop_guard_rules",
    "loop_wire_capture",
    "llm_backend",
    "llm_model_groq",
    "llm_model_ollama",
    "ollama_host",
)


def digest(text: str) -> str:
    """Return the stable short digest used to fingerprint a decision input.

    Args:
        text: Arbitrary input text (a prompt, a reply, a serialised context).

    Returns:
        The first :data:`_DIGEST_WIDTH` hex characters of the SHA-256 of
        ``text``; an empty string maps to an empty digest so absence is
        distinguishable from content.
    """
    payload = str(text or "")
    if not payload:
        return ""
    return hashlib.sha256(payload.encode("utf-8", errors="replace")).hexdigest()[:_DIGEST_WIDTH]


def _canonical(value: Any) -> Any:
    """Render a value into a deterministic, JSON-serialisable shape.

    Mappings sort by key and iterables of scalars sort by their string form,
    so two logically equal contexts that differ only in insertion order
    produce the same digest.

    Args:
        value: Any context fragment.

    Returns:
        A canonicalised structure safe to feed to ``json.dumps``.
    """
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (list, tuple, set, frozenset)):
        return sorted((_canonical(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def context_digest(ctx: Any) -> str:
    """Fingerprint a selection context independent of field ordering.

    The context's ``extra`` mapping is unordered by construction, so a naive
    repr would make equal states hash differently. This canonicalises every
    field first, which is what lets a caller memoise a decision by state.

    Args:
        ctx: A ``SelectionContext``-shaped object, or any object exposing the
            same attributes.

    Returns:
        The short digest of the canonical context, or an empty string when the
        object exposes no recognisable fields.
    """
    fields = ("target", "phase", "os_hint", "services", "has_creds", "exclude", "extra")
    snapshot: dict[str, Any] = {}
    for name in fields:
        if hasattr(ctx, name):
            snapshot[name] = _canonical(getattr(ctx, name))
    if not snapshot:
        return ""
    return digest(json.dumps(snapshot, sort_keys=True, ensure_ascii=False))


def config_digest(config: Mapping[str, Any] | None) -> str:
    """Fingerprint the config keys that change a decision's reproducibility.

    Only the keys in :data:`_CONFIG_KEYS` participate (planner temperature, the
    determinism and guard-rule flags, and model selection), so unrelated config
    churn does not invalidate a replay while a change that alters the decision
    correctly does.

    Args:
        config: A payload mapping, or ``None`` when unavailable.

    Returns:
        The short digest of the relevant config subset.
    """
    if not config:
        return ""
    subset = {key: config.get(key) for key in _CONFIG_KEYS if key in config}
    if not subset:
        return ""
    return digest(json.dumps(_canonical(subset), sort_keys=True, ensure_ascii=False))


def new_run_id() -> str:
    """Return a fresh identifier grouping all decisions of one loop run."""
    return "run_" + hashlib.sha256(f"{time.time_ns()}-{os.getpid()}".encode()).hexdigest()[:_DIGEST_WIDTH]


@dataclass(frozen=True)
class DecisionRecord:
    """One auditable next-action decision made by the loop.

    Attributes:
        run_id: Identifier shared by every decision in one loop run.
        step: The intent node id this decision advanced; stable per intent and
            combined with ``ts`` to order repeated decisions on one intent.
        source: Selector name, or ``"llm"`` for the model planner.
        model_fallback: True when the LLM produced the action rather than a
            deterministic selector.
        chosen: The command the harness committed to, empty when every
            candidate was rejected.
        reason: Short rationale carried from the selector or planner.
        ctx_digest: Fingerprint of the engagement context at decision time.
        config_digest: Fingerprint of the reproducibility-relevant config.
        prompt_digest: Fingerprint of the model prompt, empty for selectors.
        reply_digest: Fingerprint of the raw model reply, empty for selectors.
        candidates: Every command proposed before filtering.
        filtered: Rejected candidates as ``{"command", "reason"}`` rows.
        truncated: True when any recorded field was clipped for size.
        ts: UTC epoch seconds when the decision was captured.
    """

    run_id: str
    step: int
    source: str
    model_fallback: bool = False
    chosen: str = ""
    reason: str = ""
    ctx_digest: str = ""
    config_digest: str = ""
    prompt_digest: str = ""
    reply_digest: str = ""
    candidates: tuple[str, ...] = ()
    filtered: tuple[Mapping[str, str], ...] = ()
    truncated: bool = False
    ts: float = field(default_factory=time.time)


def _rotate(path: Path) -> None:
    """Trim the ledger to its tail when it outgrows the byte budget."""
    try:
        if path.exists() and path.stat().st_size > DECISIONS_MAX_BYTES:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            path.write_text("\n".join(lines[-DECISIONS_KEEP_LINES:]) + "\n", encoding="utf-8")
    except OSError:
        pass


def record(rec: DecisionRecord, path: Path | None = None) -> bool:
    """Append one decision to the ledger, rotating it when oversized.

    The write never raises: a decision ledger failure must not abort a live
    engagement, so an I/O error is swallowed and reported as ``False``.

    Args:
        rec: The decision to persist.
        path: Optional ledger path override for tests.

    Returns:
        True when the row was written, False on any I/O failure.
    """
    ledger = Path(path) if path else DECISIONS_FILE
    try:
        parent = ledger.parent
        parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(parent, _DIRECTORY_MODE)
        except OSError:
            pass
        _rotate(ledger)
        with ledger.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(rec), ensure_ascii=False, sort_keys=True) + "\n")
        return True
    except OSError:
        return False


def read_records(path: Path | None = None) -> list[dict[str, Any]]:
    """Return every decision row in order, for audit or deterministic replay.

    Args:
        path: Optional ledger path override for tests.

    Returns:
        The parsed rows; a corrupt line is skipped rather than aborting the
        read so a partially written tail never hides earlier history.
    """
    ledger = Path(path) if path else DECISIONS_FILE
    rows: list[dict[str, Any]] = []
    try:
        text = ledger.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return rows
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            rows.append(json.loads(stripped))
        except ValueError:
            continue
    return rows


def filtered_rows(items: Iterable[tuple[str, str]]) -> tuple[dict[str, str], ...]:
    """Shape ``(command, reason)`` pairs into ledger-ready rejection rows.

    Args:
        items: Rejected candidates with their reason.

    Returns:
        An immutable tuple of ``{"command", "reason"}`` mappings.
    """
    return tuple({"command": str(command)[:300], "reason": str(reason)[:160]} for command, reason in items)


__all__ = [
    "DECISIONS_FILE",
    "DecisionRecord",
    "config_digest",
    "context_digest",
    "digest",
    "filtered_rows",
    "new_run_id",
    "read_records",
    "record",
]
