"""Triage doctrine: evidence floors, verdict algebra and signature dedup.

Deterministic pre-LLM classification of one finding so the model can
never invent proof. Rules:

- A classification may never fall below what the hard evidence sets
  (the floor table); the model can only raise, never lower beyond it.
- ``version_unknown`` stays immovable both ways: unknown versions read
  as needing validation with a capped score, never as confirmed.
- A model ``confirmed`` without any hard evidence demotes to ``likely``.
- One AI call per evidence signature: the sha1 covers the rule identity
  and the evidence-bearing fields, never the host, so fifty affected
  assets share one call and a re-probe re-asks without noise.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

CONFIRMED = "confirmed"
LIKELY = "likely"
NEEDS_VALIDATION = "needs_validation"
VERSION_UNKNOWN = "version_unknown"
LIKELY_FALSE_POSITIVE = "likely_false_positive"

_RANK = {
    LIKELY_FALSE_POSITIVE: 0,
    NEEDS_VALIDATION: 1,
    VERSION_UNKNOWN: 1,
    LIKELY: 2,
    CONFIRMED: 3,
}

_SIGNITURE_TTL_SEC = 86400.0 * 8
SIGNATURE_STORE_FILENAME = "triage_signatures.json"
_MAX_STORE_ENTRIES = 5000


def rank(verdict: str) -> int:
    """Return the comparison rank of a triage verdict."""
    return _RANK.get(str(verdict or "").lower(), _RANK[NEEDS_VALIDATION])


def hard_evidence(kind: str, facts: dict[str, Any]) -> str:
    """Classify one finding from its deterministic evidence floor.

    The floor table maps an outcome kind onto the strongest verdict its
    evidence already proves without any model. Nothing raises a verdict
    here above what the facts carry.

    Args:
        kind: Outcome kind (exploit, chain, emulation, nuclei, ...).
        facts: Evidence-bearing fields (success, shell, version, cve...).

    Returns:
        One of CONFIRMED, LIKELY, NEEDS_VALIDATION or VERSION_UNKNOWN.
    """
    kind = str(kind or "").lower()
    success = bool(facts.get("success"))
    shell = bool(facts.get("shell"))
    version = str(facts.get("version", "") or "").strip()
    if kind in ("exploit", "ctf_capture") and shell:
        return CONFIRMED
    if kind in ("exploit", "chain", "emulation", "ctf_capture") and success:
        return CONFIRMED
    if kind in ("nuclei", "template"):
        return CONFIRMED if success else NEEDS_VALIDATION
    if kind == "cve_match":
        if not version:
            return VERSION_UNKNOWN
        return NEEDS_VALIDATION
    if kind in ("recon", "discovery"):
        return NEEDS_VALIDATION
    return LIKELY if success else NEEDS_VALIDATION


def apply_rules(verdict: str, kind: str, facts: dict[str, Any]) -> str:
    """Constrain a (model or operator) verdict by the evidence floor.

    Args:
        verdict: Proposed verdict, lowercased by the caller or not.
        kind: Outcome kind feeding the floor.
        facts: Evidence-bearing fields.

    Returns:
        The constrained verdict, never below the floor: unbacked
        ``confirmed`` demotes to ``likely`` and ``version_unknown`` is
        immovable in both directions.
    """
    proposed = str(verdict or "").strip().lower() or LIKELY
    floor = hard_evidence(kind, facts)
    if proposed == VERSION_UNKNOWN:
        return VERSION_UNKNOWN
    if rank(proposed) < rank(floor):
        return floor
    if proposed == CONFIRMED and rank(floor) < rank(CONFIRMED):
        return LIKELY
    return proposed


_ASSET_FIELDS = ("host", "target", "ip", "port", "asset", "asset_id", "worker", "task_id")
_ASSET_CHARS = set("0123456789.:[]abcdef")


def signature_for(kind: str, fields: dict[str, Any]) -> str:
    """Return the evidence signature of one classification request.

    The signature covers the rule identity and evidence-bearing fields
    only: asset identifiers (hosts, ports, task ids) are dropped because
    two hosts carrying the same evidence ask the same question.

    Args:
        kind: Classification rule identity (floor table family).
        fields: Evidence fields about to steer the call.

    Returns:
        Hex digest string.
    """
    payload: dict[str, Any] = {"kind": str(kind or "").strip().lower()}
    for key in sorted(fields):
        if key in _ASSET_FIELDS:
            continue
        value = fields.get(key)
        if isinstance(value, str) and value:
            if all(char in _ASSET_CHARS for char in value):
                continue
        payload[key] = value
    blob = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha1(blob.encode("utf-8", "replace")).hexdigest()


class SignatureStore:
    """Bounded TTL store of already-answered evidence signatures."""

    def __init__(self, sessions_dir: str | Path | None = None, ttl: float = _SIGNITURE_TTL_SEC) -> None:
        """Bind the store file under sessions/lazy."""
        base = Path(str(sessions_dir or "sessions")) / "lazy"
        self._path = base / SIGNATURE_STORE_FILENAME
        self._ttl = float(ttl or _SIGNATURE_TTL_SEC)

    def fresh_signature(self, signature: str, now: float) -> str | None:
        """Return the previous signature row when it is inside the TTL window.

        Marks the signature seen afterwards, so callers reserve one
        answer per window in a single check-and-mark step.
        """
        if not signature:
            return None
        store = self._load()
        previous = store.get(signature)
        if isinstance(previous, (int, float)) and now - float(previous) < self._ttl:
            store[signature] = now
            self._save(store)
            return signature
        store[signature] = now
        self._save(store)
        return None

    def reset(self) -> None:
        """Drop every signature row."""
        self._save({})

    def _load(self) -> dict[str, float]:
        try:
            if self._path.is_file():
                raw = json.loads(self._path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    return {str(key): float(value) for key, value in raw.items() if isinstance(value, (int, float))}
        except Exception:
            pass
        return {}

    def _save(self, store: dict[str, float]) -> None:
        try:
            store = dict(sorted(store.items(), key=lambda row: -row[1])[:_MAX_STORE_ENTRIES])
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(store), encoding="utf-8")
        except Exception:
            pass


__all__ = [
    "CONFIRMED",
    "LIKELY",
    "NEEDS_VALIDATION",
    "VERSION_UNKNOWN",
    "LIKELY_FALSE_POSITIVE",
    "SignatureStore",
    "SIGNATURE_STORE_FILENAME",
    "apply_rules",
    "hard_evidence",
    "rank",
    "signature_for",
]
