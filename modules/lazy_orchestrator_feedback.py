"""Organic orchestrator training from loop usage.

Mirrors how the detection oracle learns: per-command outcomes already flow
online to MoE/Q-learning via ``loop_ai_bridge.record_step``; this module is
the batch counterpart of ``DetectionFeed.adjust_from_feedback``. It reads
the routing log written by :mod:`modules.lazy_intel` and produces two
artefacts under ``sessions/lazy/``:

- ``verb_priors.json`` — per-(phase, verb) success rates. The planner
  consults them through :func:`verb_prior` to rank candidate verbs, so
  verbs that historically work for a phase float up without any manual
  tuning. Cold verbs (fewer than ``MIN_ATTEMPTS`` samples) keep their
  default order instead of being punished for having no history.
- ``orchestrator_dataset.jsonl`` — instruction-tuning rows
  (instruction/input/output/reward/meta) exported by :func:`export_dataset`
  for TopoSwarm ``--finetune`` runs. Rows only exist when the operator
  actually ran the loop: usage writes the dataset, nobody hand-crafts it.

Stdlib only. Never raises; all entry points degrade gracefully.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STORE_DIR = REPO_ROOT / "sessions" / "lazy"
PRIORS_FILE = "verb_priors.json"
DATASET_FILE = "orchestrator_dataset.jsonl"

MIN_ATTEMPTS = 3

_PRIORS_LOCK = threading.Lock()
_PRIORS_CACHE: dict = {"at": 0.0, "mtime": 0, "priors": {}}
PRIORS_CACHE_TTL_SEC = 5.0


def _priors_path() -> Path:
    """Return priors path, ensuring the directory exists."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    return STORE_DIR / PRIORS_FILE


def _dataset_path() -> Path:
    """Return dataset path, ensuring the directory exists."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    return STORE_DIR / DATASET_FILE


def _reward_of(outcome: dict) -> float:
    """Score one outcome like the online trainer: 1 productive, 0 not."""
    state = str(outcome.get("state", "") or "")
    if state == "done" and (int(outcome.get("facts", 0) or 0) > 0 or int(outcome.get("findings", 0) or 0) > 0):
        return 1.0
    return 0.0


def adjust_from_usage(limit: int = 5000) -> dict:
    """Fold routing outcomes into per-(phase, stack, verb) success priors.

    Stacks fingerprint the target services, so repeat engagements against
    the same stack learn faster while unseen stacks fall back to global
    priors. Stored shape per phase is ``{"_global": {...}, "_stacks":
    {stack: {...}}}``; legacy flat files migrate on load.

    Args:
        limit: Max routing records scanned from the tail.

    Returns:
        Summary with verbs updated and outcomes seen.
    """
    from modules.lazy_intel import read_decisions

    summary = {"verbs": 0, "outcomes": 0}
    try:
        records = read_decisions(limit=limit)
    except Exception:
        return summary
    agg: dict[tuple[str, str, str], dict[str, int]] = {}
    for record in records:
        if record.get("kind") != "outcome":
            continue
        summary["outcomes"] += 1
        key = (
            str(record.get("phase", "") or "other"),
            str(record.get("stack", "") or ""),
            str(record.get("verb", "") or ""),
        )
        if not key[2]:
            continue
        bucket = agg.setdefault(key, {"success": 0, "total": 0})
        bucket["total"] += 1
        bucket["success"] += 1 if _reward_of(record) >= 1.0 else 0
    priors: dict[str, dict] = {}
    for (phase, stack, verb), bucket in agg.items():
        total = bucket["total"]
        entry = {
            "success": bucket["success"],
            "total": total,
            "rate": round(bucket["success"] / total, 3) if total else 0.0,
            "updated": time.time(),
        }
        phase_view = priors.setdefault(phase, {"_global": {}, "_stacks": {}})
        if stack:
            phase_view["_stacks"].setdefault(stack, {})[verb] = entry
        else:
            phase_view["_global"][verb] = entry
    try:
        _priors_path().write_text(json.dumps(priors, indent=2, ensure_ascii=False), encoding="utf-8")
        summary["verbs"] = sum(
            len(phase_view.get("_global", {})) + sum(len(v) for v in phase_view.get("_stacks", {}).values())
            for phase_view in priors.values()
        )
    except OSError:
        pass
    with _PRIORS_LOCK:
        _PRIORS_CACHE["priors"] = priors
        _PRIORS_CACHE["at"] = time.monotonic()
        try:
            _PRIORS_CACHE["mtime"] = _priors_path().stat().st_mtime_ns
        except OSError:
            _PRIORS_CACHE["mtime"] = 0
    return summary


def _normalize(priors: dict) -> dict:
    """Migrate legacy flat priors to the global/stacks shape."""
    if not isinstance(priors, dict):
        return {}
    normalized: dict = {}
    for phase, view in priors.items():
        if not isinstance(view, dict):
            continue
        if "_global" in view or "_stacks" in view:
            normalized[phase] = {"_global": dict(view.get("_global") or {}), "_stacks": dict(view.get("_stacks") or {})}
        else:
            normalized[phase] = {"_global": dict(view), "_stacks": {}}
    return normalized


def _load_priors() -> dict:
    """Return cached priors, reloading from disk when stale."""
    with _PRIORS_LOCK:
        cached = _PRIORS_CACHE["priors"]
        fresh = cached and (time.monotonic() - _PRIORS_CACHE["at"]) < PRIORS_CACHE_TTL_SEC
        if fresh:
            return cached
    priors: dict = {}
    try:
        priors = _normalize(json.loads(_priors_path().read_text(encoding="utf-8")))
    except (OSError, ValueError):
        priors = {}
    with _PRIORS_LOCK:
        _PRIORS_CACHE["priors"] = priors
        _PRIORS_CACHE["at"] = time.monotonic()
    return priors


def verb_prior(phase: str, verb: str, stack: str = "") -> dict | None:
    """Return the success prior for one (phase, stack, verb) triple.

    Stack-specific priors win when warm; otherwise the global pair
    applies. Cold pairs return None so default order is preserved.

    Args:
        phase: Kill-chain phase.
        verb: Shell verb.
        stack: Target stack fingerprint.

    Returns:
        Prior dict with success/total/rate, or None when cold.
    """
    view = _load_priors().get(str(phase or ""), {})
    if stack:
        entry = (view.get("_stacks", {}) or {}).get(str(stack), {}).get(str(verb or ""))
        if isinstance(entry, dict) and int(entry.get("total", 0) or 0) >= MIN_ATTEMPTS:
            return entry
    entry = (view.get("_global", {}) or {}).get(str(verb or ""))
    if not isinstance(entry, dict):
        return None
    if int(entry.get("total", 0) or 0) < MIN_ATTEMPTS:
        return None
    return entry


def rank_verbs(phase: str, verbs: list[str], stack: str = "") -> list[str]:
    """Order verbs by learned success rate, stable for cold verbs.

    Args:
        phase: Kill-chain phase the verbs serve.
        verbs: Candidate verb names in default order.
        stack: Target stack fingerprint for stack-specific priors.

    Returns:
        Verbs with warm priors first (rate desc), cold verbs untouched
        after them in their original relative order.
    """
    scored = []
    cold = []
    for position, verb in enumerate(verbs):
        prior = verb_prior(phase, verb, stack)
        if prior is None:
            cold.append((position, verb))
        else:
            scored.append((-float(prior.get("rate", 0.0) or 0.0), position, verb))
    scored.sort()
    return [verb for _, _, verb in scored] + [verb for _, verb in cold]


def order_steps(steps: list[str], stack: str = "") -> list[str]:
    """Reorder resolved step lines by stack-aware verb priors.

    Args:
        steps: Command lines in planner order.
        stack: Target stack fingerprint.

    Returns:
        Steps with warm-prior verbs first, order otherwise preserved.
    """
    try:
        from modules.lazy_cli_bridge import phase_for as _phase_for
    except Exception:
        _phase_for = lambda _v: "other"  # noqa: E731

    def _key(line: str) -> tuple:
        head = (line or "").strip().split()[0] if (line or "").strip() else ""
        prior = verb_prior(_phase_for(head), head, stack) if head else None
        if prior is None:
            return (1, 0.0)
        return (0, -float(prior.get("rate", 0.0) or 0.0))

    return sorted(list(steps or []), key=_key)


def export_dataset(out: str | Path | None = None, limit: int = 5000) -> dict:
    """Export instruction-tuning rows joined from decisions + outcomes.

    Each row pairs the operator-visible intent (instruction/input) with
    the command the loop chose (output) and the reward it earned, so a
    TopoSwarm ``--finetune`` run learns orchestration from real usage.

    Args:
        out: Destination path. Defaults to the store dataset file.
        limit: Max routing records scanned from the tail.

    Returns:
        Summary with rows written and destination.
    """
    from modules.lazy_intel import read_decisions

    dest = Path(out) if out else _dataset_path()
    summary = {"rows": 0, "dest": str(dest)}
    try:
        records = read_decisions(limit=limit)
    except Exception:
        return summary
    decisions: dict[tuple[str, int, str], dict] = {}
    for record in records:
        if record.get("kind") == "decision":
            decisions[(str(record.get("task", "")), int(record.get("intent", 0) or 0), str(record.get("command", "")))] = record
    rows = []
    for record in records:
        if record.get("kind") != "outcome":
            continue
        key = (str(record.get("task", "")), int(record.get("intent", 0) or 0), str(record.get("command", "")))
        decision = decisions.get(key, {})
        intent_text = str(decision.get("intent_text", "") or "")
        target = str(decision.get("target", "") or "")
        command = str(record.get("command", "") or "")
        if not command:
            continue
        phase = str(record.get("phase", "") or "other")
        rows.append(
            {
                "instruction": f"Choose the best Lazy shell command for kill-chain phase '{phase}'. Reply with ONLY the command line.",
                "input": f"intent: {intent_text[:300]} | target: {target[:100]}".strip(),
                "output": command[:500],
                "reward": _reward_of(record),
                "meta": {
                    "task": str(record.get("task", "")),
                    "phase": phase,
                    "verb": str(record.get("verb", "")),
                    "source": str(decision.get("source", "") or "unknown"),
                    "risk": str(record.get("risk", "") or "safe"),
                    "state": str(record.get("state", "")),
                },
            }
        )
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        summary["rows"] = len(rows)
    except OSError:
        pass
    return summary


__all__ = [
    "MIN_ATTEMPTS",
    "adjust_from_usage",
    "export_dataset",
    "order_steps",
    "rank_verbs",
    "verb_prior",
]
