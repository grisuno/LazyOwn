"""Goal decomposition round-0 with constraints and proof.

Ports the LAZY ``agent/goals.go`` + ``agent/constraints.go`` contract:
round-0 splits a free-text objective into discrete verifiable goals,
records task constraints (allow/deny, highest priority), registers the
explicit asset scope, and proves goals from evidence. ``goal_met``
ends the whole task and is opt-in (default unbound, LAZY parity).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


MAX_DECOMPOSE_TURNS = 8


@dataclass
class GoalSpec:
    """One decomposed verifiable objective."""

    text: str
    vuln_class: str = ""
    state: str = "open"


@dataclass
class TaskConstraints:
    """Allow/deny constraints with deny-wins semantics (LAZY parity)."""

    allow: list[str] = field(default_factory=list)
    deny: list[str] = field(default_factory=list)

    def blocked(self, command: str) -> str:
        """Return the blocking constraint or empty string."""
        hay = str(command or "").lower()
        for rule in self.deny:
            if rule and str(rule).lower() in hay:
                return str(rule)
        return ""


_GOAL_SPLIT_RE = re.compile(r"[;.\n]+|\s+then\s+|\s+and then\s+", re.IGNORECASE)

_KEYWORD_GOALS = (
    ("scan", "recon: discover live hosts and open services"),
    ("enum", "enum: enumerate services and shares"),
    ("cred", "credential: capture valid credentials"),
    ("password", "credential: capture valid credentials"),
    ("hash", "credential: capture password hashes"),
    ("exploit", "exploit: gain initial access"),
    ("shell", "exploit: gain initial access"),
    ("access", "exploit: gain initial access"),
    ("lateral", "lateral: move laterally with captured creds"),
    ("privesc", "privesc: escalate privileges"),
    ("persist", "persist: establish persistence"),
    ("exfil", "exfil: collect and exfiltrate data"),
    ("report", "report: document findings with evidence"),
)


def decompose_rule_based(objective_text: str, max_goals: int = 8) -> list[GoalSpec]:
    """Split objective text into goal specs without an LLM (deterministic)."""
    raw = str(objective_text or "").strip()
    if not raw:
        return [GoalSpec(text="recon: discover live hosts and open services")]
    parts = [p.strip() for p in _GOAL_SPLIT_RE.split(raw) if p.strip()]
    goals: list[GoalSpec] = []
    for part in parts[:max(1, max_goals)]:
        low = part.lower()
        mapped = next((g for k, g in _KEYWORD_GOALS if k in low), "")
        goals.append(GoalSpec(text=mapped or f"task: {part[:120]}"))
    if not goals:
        goals.append(GoalSpec(text="recon: discover live hosts and open services"))
    seen: list[GoalSpec] = []
    for goal in goals:
        if goal.text not in {g.text for g in seen}:
            seen.append(goal)
    return seen[:max(1, max_goals)]


def load_constraints(payload: dict | None = None) -> TaskConstraints:
    """Build constraints from payload config (deny wins, LAZY parity)."""
    payload = payload or {}
    allow: list[str] = []
    deny: list[str] = []
    for key in ("task_allow", "allow_list", "scope_allow"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            allow.append(value.strip())
        elif isinstance(value, list):
            allow.extend(str(v) for v in value if str(v).strip())
    for key in ("task_deny", "deny_list", "scope_deny", "out_of_scope"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            deny.append(value.strip())
        elif isinstance(value, list):
            deny.extend(str(v) for v in value if str(v).strip())
    return TaskConstraints(allow=allow, deny=deny)


def constraint_block_text(constraints: TaskConstraints) -> str:
    """Render the constraint block injected at max priority (LAZY parity)."""
    lines = ["task_constraints (highest priority):"]
    if constraints.deny:
        lines.append("deny: " + "; ".join(constraints.deny))
    else:
        lines.append("deny: (none)")
    if constraints.allow:
        lines.append("allow: " + "; ".join(constraints.allow))
    else:
        lines.append("allow: (none — deny list still enforced)")
    return "\n".join(lines)


class GoalTracker:
    """Round-0 goals with prove_goal / goal_met semantics."""

    def __init__(self, goals: list[GoalSpec] | None = None) -> None:
        """Bind to an initial goal list."""
        self._goals: list[GoalSpec] = list(goals or [])

    @property
    def goals(self) -> list[GoalSpec]:
        """Return a copy of tracked goals."""
        return list(self._goals)

    def prove_goal(self, goal_text: str, evidence: str = "") -> bool:
        """Mark one goal achieved from evidence; return True when found."""
        needle = str(goal_text or "").strip().lower()
        for goal in self._goals:
            if goal.state != "open":
                continue
            if needle and (needle in goal.text.lower() or goal.text.lower() in needle):
                goal.state = "achieved"
                return True
        return False

    def goal_met(self, opt_in: bool = False) -> bool:
        """End the whole task; requires explicit opt-in (default unbound)."""
        if not opt_in:
            return False
        for goal in self._goals:
            goal.state = "achieved"
        return True

    def all_achieved(self) -> bool:
        """Return True when every goal is achieved."""
        return bool(self._goals) and all(g.state == "achieved" for g in self._goals)

    def open_goals(self) -> list[GoalSpec]:
        """Return goals still open."""
        return [g for g in self._goals if g.state == "open"]


__all__ = [
    "MAX_DECOMPOSE_TURNS", "GoalSpec", "TaskConstraints",
    "decompose_rule_based", "load_constraints", "constraint_block_text",
    "GoalTracker",
]
