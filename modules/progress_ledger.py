"""Objective-progress ledger: qualitative strikes against goal stagnation.

Contract: one small JSON state per engagement tracks consecutive rounds
without objective progress. Generating hypotheses (new intents) is never
progress; real evidence is: new facts or findings persisted, a retest
verdict that reproduced the issue, a confirmed exploit-class outcome, or a
goal marked done. Reaching ``max_strikes`` (operator-configurable, default
3) tells the engine to stop burning rounds and hand the decision back to
the operator with the durable finding ledger as context.

State lives at ``sessions/findings/progress_<task>.json`` so a crash or a
resume continues the strike count instead of resetting silently.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, replace
from pathlib import Path

PROGRESS_DIRNAME = "findings"

ENGAGEMENT_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,80}$")

SIGNALS: tuple[str, ...] = ("facts", "findings", "reproduced", "exploit_success", "goals_done")

DEFAULT_MAX_STRIKES = 3

PROGRESS_REASON = ""

_STRIKE_REASONS: dict[str, str] = {
    "hypothesis_only": "round generated intents but persisted no objective evidence",
    "idle": "round produced no intents and no evidence",
}


class InvalidEngagement(ValueError):
    """The engagement id is not a safe path segment."""


@dataclass(frozen=True)
class StrikePolicy:
    """Numeric knobs of the strike rule, injected by the caller.

    Attributes:
        max_strikes: Consecutive no-progress rounds before handoff.
        handoff_on_strikes: Whether reaching the cap ends the loop.
    """

    max_strikes: int = DEFAULT_MAX_STRIKES
    handoff_on_strikes: bool = True

    def clamped(self) -> StrikePolicy:
        """Return a copy with the strike cap forced into range."""
        return replace(self, max_strikes=min(20, max(1, int(self.max_strikes))))


@dataclass(frozen=True)
class RoundSignals:
    """Objective evidence delta of one round.

    Attributes:
        facts: New fact count over the round.
        findings: New finding count over the round.
        reproduced: Retest verdicts that reproduced a finding.
        exploit_success: Successful exploit-class outcomes.
        goals_done: Goals newly marked done.
        new_intents: Intents created by the planner (hypotheses).
    """

    facts: int = 0
    findings: int = 0
    reproduced: int = 0
    exploit_success: int = 0
    goals_done: int = 0
    new_intents: int = 0

    @property
    def progress(self) -> bool:
        """Return True when any objective-evidence signal fired."""
        return any(getattr(self, name) > 0 for name in SIGNALS)


def _now_iso() -> str:
    """Return a UTC ISO-8601 timestamp with ``Z`` suffix."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _safe_state(value: object) -> int:
    """Coerce a stored counter safely."""
    try:
        return max(0, int(str(value or 0).strip() or 0))  # type: ignore[type-var, call-overload]
    except (TypeError, ValueError):
        return 0


class ProgressLedger:
    """Persisted strike counter for one engagement."""

    def __init__(
        self,
        engagement_id: str,
        base_dir: str | os.PathLike[str],
        policy: StrikePolicy | None = None,
    ) -> None:
        """Bind the ledger to one engagement.

        Args:
            engagement_id: Engagement/task id (safe path segment).
            base_dir: Root directory holding the ``findings`` folder.
            policy: Strike thresholds.

        Raises:
            InvalidEngagement: Unsafe engagement id.
        """
        clean = str(engagement_id or "").strip()
        if not ENGAGEMENT_PATTERN.fullmatch(clean):
            raise InvalidEngagement(f"invalid engagement id: {clean!r}")
        self.engagement_id = clean
        self.path = Path(base_dir)
        self.policy = (policy or StrikePolicy()).clamped()
        self._state: dict = {"strikes": 0, "log": [], "brief": {}, "updated_at": ""}

    @property
    def file_path(self) -> Path:
        """Return the persisted strike state path."""
        return self.path / PROGRESS_DIRNAME / f"progress_{self.engagement_id}.json"

    def load(self) -> ProgressLedger:
        """Load persisted state, keeping any file intact on parse failure.

        Returns:
            Self, for call chaining.
        """
        try:
            raw = self.file_path.read_text(encoding="utf-8", errors="replace")
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                self._state = {
                    "strikes": _safe_state(parsed.get("strikes")),
                    "log": [row for row in parsed.get("log", []) if isinstance(row, dict)][-20:],
                    "brief": dict(parsed.get("brief") or {}),
                    "updated_at": str(parsed.get("updated_at", "") or ""),
                }
        except (OSError, ValueError):
            pass
        return self

    def save(self) -> None:
        """Persist the strike state with owner-only permissions."""
        path = self.file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
        handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            os.write(handle, json.dumps(self._state, ensure_ascii=False).encode("utf-8"))
        finally:
            os.close(handle)

    @property
    def strikes(self) -> int:
        """Return the current consecutive no-progress strike count."""
        return int(self._state.get("strikes", 0))

    @property
    def log(self) -> list[dict]:
        """Return the recent strike/progress log rows."""
        return list(self._state.get("log", []))

    def signals_from_brief(self, brief: dict) -> RoundSignals:
        """Diff one graph/orchestrator brief against the stored previous one.

        The brief carries the objective counters (facts, findings, goals
        done) accumulated by the engine and the per-round hypothesis count;
        the diff yields positive evidence only when counters grew.

        Args:
            brief: Mapping with ``facts``/``findings``/``goals_done``/``new_intents``.

        Returns:
            RoundSignals delta of this round.
        """
        previous = dict(self._state.get("brief") or {})
        new_facts = max(0, _safe_state(brief.get("facts")) - _safe_state(previous.get("facts")))
        new_findings = max(0, _safe_state(brief.get("findings")) - _safe_state(previous.get("findings")))
        new_goals = max(0, _safe_state(brief.get("goals_done")) - _safe_state(previous.get("goals_done")))
        signals = RoundSignals(
            facts=new_facts,
            findings=new_findings,
            reproduced=_safe_state(brief.get("reproduced")),
            exploit_success=_safe_state(brief.get("exploit_success")),
            goals_done=new_goals,
            new_intents=_safe_state(brief.get("new_intents")),
        )
        self._state["brief"] = {
            "facts": _safe_state(brief.get("facts")),
            "findings": _safe_state(brief.get("findings")),
            "goals_done": _safe_state(brief.get("goals_done")),
        }
        return signals

    def observe(self, signals: RoundSignals, note: str = "") -> dict:
        """Record one round of signals and update the strike counter.

        Objective progress resets the strikes to zero; a hypothesis-only or
        idle round increments. The decision field tells the engine whether
        the cap was reached this round.

        Args:
            signals: Round evidence delta.
            note: Optional operator-visible context line.

        Returns:
            ``{"progress": bool, "strikes": int, "decision": str, "max_strikes": int}``
            where ``decision`` is ``"progress"``, ``"strike"`` or ``"handoff"``.
        """
        self._state["updated_at"] = _now_iso()
        row = {"ts": _now_iso(), "progress": signals.progress, "note": note[:160]}
        if signals.progress:
            self._state["strikes"] = 0
            row["reason"] = PROGRESS_REASON
            row["signals"] = {name: _safe_state(getattr(signals, name)) for name in SIGNALS}
            decision = "progress"
        else:
            reason = _STRIKE_REASONS["hypothesis_only"] if signals.new_intents else _STRIKE_REASONS["idle"]
            self._state["strikes"] = self.strikes + 1
            row["reason"] = reason
            row["signals"] = {"new_intents": signals.new_intents}
            decision = "strike"
        cap = self.policy.max_strikes
        if self.strikes >= cap and self.policy.handoff_on_strikes:
            decision = "handoff"
        self._state.setdefault("log", []).append(row)
        self._state["log"] = self._state["log"][-20:]
        self.save()
        return {
            "progress": signals.progress,
            "strikes": self.strikes,
            "decision": decision,
            "max_strikes": cap,
            "reason": str(row["reason"]),
        }

    def brief_for_discards(self) -> list[dict]:
        """Return durable rows for the finding-ledger discard recorder.

        Returns:
            Empty placeholder list; discarded vectors come from the
            engine's round results, not this counter state.
        """
        return []


__all__ = [
    "DEFAULT_MAX_STRIKES",
    "PROGRESS_DIRNAME",
    "SIGNALS",
    "InvalidEngagement",
    "ProgressLedger",
    "RoundSignals",
    "StrikePolicy",
]
