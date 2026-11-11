"""Read-only side questions against the loop's immutable decision checkpoints.

It lets an operator interrogate a frozen checkpoint of the autonomous loop
without owning an agent session or a tool executor, so asking a question can
never mutate the run it asks about.

The checkpoints are the rows already written to ``sessions/decisions.jsonl`` by
:mod:`modules.loop.decision_log`; each is immutable once written. Every
checkpoint is addressed by a content-derived ordinal rather than its position in
the file: a persisted ordinal, not an array offset, so restart, pagination and
failed requests cannot shift it, and a rotation or a partial read never
re-points an identifier at a different decision.

Answers are appended to a separate ``sessions/sidequests.jsonl`` ledger, keeping
the side channel auditable yet fully isolated from loop state. Nothing here
writes to the loop, and the module imports no loop runtime, so it stays
cycle-free.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

_BASE_DIR = Path(__file__).resolve().parent.parent
_SIDEQUEST_FILE = _BASE_DIR / "sessions" / "sidequests.jsonl"
_DIRECTORY_MODE = 0o700
_ORDINAL_WIDTH = 16
_DEFAULT_LIMIT = 20
_SIDEQUEST_TEMPERATURE = 0.0
_ANSWER_MAX_TOKENS = 400


def checkpoint_id(row: dict[str, Any]) -> str:
    """Return a stable, position-independent ordinal for one decision row.

    The id is the digest of the fields that identify the decision (run, step,
    context, chosen action and timestamp), so it survives ledger rotation and
    pagination: the same decision always resolves to the same id, and no two
    distinct decisions collide in practice.

    Args:
        row: One decision ledger row.

    Returns:
        The checkpoint ordinal, or an empty string for an empty row.
    """
    if not row:
        return ""
    material = "|".join(
        str(row.get(key, ""))
        for key in ("run_id", "step", "source", "ctx_digest", "chosen", "ts")
    )
    return hashlib.sha256(material.encode("utf-8", errors="replace")).hexdigest()[:_ORDINAL_WIDTH]


def list_checkpoints(run_id: str = "", limit: int = _DEFAULT_LIMIT) -> list[dict[str, Any]]:
    """Return recent decision checkpoints, newest last, each with its ordinal.

    Args:
        run_id: When set, only checkpoints from that loop run are returned.
        limit: Maximum number of checkpoints to return.

    Returns:
        The checkpoints as summary dicts carrying their ``checkpoint_id`` and
        the fields an operator needs to choose one; an empty list when the
        ledger is absent.
    """
    try:
        from modules.loop import decision_log

        rows = decision_log.read_records()
    except Exception:
        return []
    if run_id:
        rows = [row for row in rows if str(row.get("run_id", "")) == str(run_id)]
    rows = rows[-max(1, int(limit)):]
    out: list[dict[str, Any]] = []
    for row in rows:
        out.append(
            {
                "checkpoint_id": checkpoint_id(row),
                "run_id": str(row.get("run_id", "")),
                "step": int(row.get("step", 0) or 0),
                "source": str(row.get("source", "")),
                "model_fallback": bool(row.get("model_fallback", False)),
                "chosen": str(row.get("chosen", "")),
                "reason": str(row.get("reason", "")),
                "ts": float(row.get("ts", 0.0) or 0.0),
            }
        )
    return out


def get_checkpoint(ordinal: str) -> dict[str, Any] | None:
    """Return the full frozen decision row for a checkpoint ordinal.

    Args:
        ordinal: The checkpoint id from :func:`list_checkpoints`.

    Returns:
        The decision row, or None when no checkpoint matches.
    """
    want = str(ordinal or "").strip()
    if not want:
        return None
    try:
        from modules.loop import decision_log

        rows = decision_log.read_records()
    except Exception:
        return None
    for row in rows:
        if checkpoint_id(row) == want:
            return row
    return None


def _render_context(row: dict[str, Any]) -> str:
    """Render a frozen checkpoint into a compact prompt context block."""
    candidates = row.get("candidates") or []
    filtered = row.get("filtered") or []
    lines = [
        f"source: {row.get('source', '')} (model_fallback={bool(row.get('model_fallback', False))})",
        f"chosen action: {row.get('chosen', '') or '(none)'}",
        f"reason: {row.get('reason', '')}",
        f"context digest: {row.get('ctx_digest', '')}",
        f"config digest: {row.get('config_digest', '')}",
    ]
    if candidates:
        lines.append("candidates: " + " | ".join(str(c) for c in candidates[:8]))
    if filtered:
        rejects = ", ".join(f"{f.get('command', '')}=>{f.get('reason', '')}" for f in filtered[:8])
        lines.append(f"rejected: {rejects}")
    return "\n".join(lines)


def ask(ordinal: str, question: str, temperature: float = _SIDEQUEST_TEMPERATURE) -> dict[str, Any]:
    """Answer a question about one frozen checkpoint, read-only.

    The checkpoint is never mutated and the loop is never touched: the function
    only reads the ledger, renders the frozen decision into context, queries the
    model, and appends the exchange to the side-question ledger.

    Args:
        ordinal: The checkpoint id to interrogate.
        question: The operator's question.
        temperature: Sampling temperature; greedy by default for a reproducible
            answer.

    Returns:
        A result dict with ``ok``, and either ``answer`` and ``checkpoint_id``
        or an ``error`` describing why no answer was produced.
    """
    text = str(question or "").strip()
    if not text:
        return {"ok": False, "error": "empty question"}
    row = get_checkpoint(ordinal)
    if row is None:
        return {"ok": False, "error": f"unknown checkpoint: {ordinal}"}
    prompt = (
        "You are auditing one frozen decision made by an autonomous red-team "
        "loop. Answer the operator's question using only the checkpoint below. "
        "Do not propose new commands to run; this is a read-only review.\n\n"
        f"Checkpoint:\n{_render_context(row)}\n\n"
        f"Question: {text[:600]}"
    )
    try:
        from modules.llm_factory import complete as _complete

        try:
            answer = str(_complete("auto", prompt, max_tokens=_ANSWER_MAX_TOKENS, temperature=temperature) or "").strip()
        except TypeError:
            answer = str(_complete("auto", prompt, max_tokens=_ANSWER_MAX_TOKENS) or "").strip()
    except Exception as exc:
        return {"ok": False, "error": f"model unavailable: {exc}"}
    if not answer:
        return {"ok": False, "error": "model returned no answer"}
    _record_sidequest(str(checkpoint_id(row)), text, answer)
    return {"ok": True, "checkpoint_id": checkpoint_id(row), "answer": answer}


def _record_sidequest(ordinal: str, question: str, answer: str) -> None:
    """Append one side-question exchange to its isolated ledger."""
    entry = {
        "ts": time.time(),
        "checkpoint_id": ordinal,
        "question": question[:600],
        "answer": answer[:4000],
    }
    try:
        _SIDEQUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(_SIDEQUEST_FILE.parent, _DIRECTORY_MODE)
        except OSError:
            pass
        with _SIDEQUEST_FILE.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        return


__all__ = ["ask", "checkpoint_id", "get_checkpoint", "list_checkpoints"]
