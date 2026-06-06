#!/usr/bin/env python3
"""
Autonomous Campaign Intelligence (ACI) Planner
===============================================
Decomposes a natural-language engagement goal into a MITRE ATT&CK-aligned
tactical plan, injects each phase as objectives into the ObjectiveStore,
monitors execution, and replans when too many objectives are blocked.

Architecture (SOLID)
--------------------
- ACIGoal          dataclass — immutable goal descriptor
- AttackPhase      dataclass — one tactical phase with ATT&CK metadata
- ACIPlan          dataclass — full mutable plan persisted to sessions/
- ACIPlanner       — decomposes goals (LLM-backed with static fallback)
- ACIEngine        — monitors plan state, decides when to replan
- ACIReflector     — generates campaign_lessons from plan outcomes
- mcp_aci_plan     — MCP bridge: plan a goal
- mcp_aci_status   — MCP bridge: live plan status
- mcp_aci_replan   — MCP bridge: force adaptive replan

Persistence
-----------
sessions/aci_plan.json   — current active plan (one plan at a time)
sessions/aci_history.jsonl — archived completed/abandoned plans
sessions/campaign_lessons.jsonl — lessons appended by ACIReflector

Usage (CLI)
-----------
    python3 skills/aci_planner.py plan  "Compromise the DC at corp.internal" --target 10.10.11.5
    python3 skills/aci_planner.py status
    python3 skills/aci_planner.py replan "Kerberoasting blocked, try AS-REP"

Usage (MCP)
-----------
    mcp_aci_plan(goal="...", target="10.10.11.5", scope=["10.10.11.0/24"])
    mcp_aci_status()
    mcp_aci_replan(reason="...")
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import os
import secrets
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ─── Paths ───────────────────────────────────────────────────────────────────

BASE_DIR         = Path(__file__).parent.parent
SESSIONS_DIR     = BASE_DIR / "sessions"
ACI_PLAN_FILE    = SESSIONS_DIR / "aci_plan.json"
ACI_HISTORY_FILE = SESSIONS_DIR / "aci_history.jsonl"
LESSONS_FILE     = SESSIONS_DIR / "campaign_lessons.jsonl"
OBJECTIVES_FILE  = SESSIONS_DIR / "objectives.jsonl"

log = logging.getLogger("aci_planner")

# ─── Constants ───────────────────────────────────────────────────────────────

REPLAN_THRESHOLD        = 3    # blocked objectives in current phase → trigger replan
MAX_OBJECTIVES_PER_PHASE = 5
GROQ_API_URL            = "https://api.groq.com/openai/v1/chat/completions"
GROQ_DEFAULT_MODEL      = "llama-3.3-70b-versatile"

# MITRE ATT&CK tactic reference used in static fallback
MITRE_KILL_CHAIN: List[Dict] = [
    {"tactic": "TA0043", "tactic_name": "Reconnaissance",      "phase": "recon",    "techniques": ["T1595", "T1046", "T1592"]},
    {"tactic": "TA0042", "tactic_name": "Resource Development", "phase": "setup",    "techniques": ["T1587", "T1583"]},
    {"tactic": "TA0001", "tactic_name": "Initial Access",       "phase": "exploit",  "techniques": ["T1190", "T1566", "T1133"]},
    {"tactic": "TA0002", "tactic_name": "Execution",            "phase": "exec",     "techniques": ["T1059", "T1203"]},
    {"tactic": "TA0004", "tactic_name": "Privilege Escalation", "phase": "privesc",  "techniques": ["T1548", "T1134", "T1055"]},
    {"tactic": "TA0006", "tactic_name": "Credential Access",    "phase": "cred",     "techniques": ["T1003", "T1558", "T1552"]},
    {"tactic": "TA0008", "tactic_name": "Lateral Movement",     "phase": "lateral",  "techniques": ["T1021", "T1550", "T1570"]},
    {"tactic": "TA0010", "tactic_name": "Exfiltration",         "phase": "exfil",    "techniques": ["T1048", "T1041"]},
    {"tactic": "TA0040", "tactic_name": "Impact",               "phase": "impact",   "techniques": []},
]

# Phase → default objective templates (used when LLM is unavailable)
PHASE_OBJECTIVE_TEMPLATES: Dict[str, List[str]] = {
    "recon":   [
        "Run full port scan against {target} and record open services",
        "Identify OS version and service banners on {target}",
        "Enumerate DNS records for {domain}",
    ],
    "setup":   [
        "Prepare listener on lport and verify C2 connectivity",
    ],
    "exploit": [
        "Identify exploitable vulnerabilities in discovered services on {target}",
        "Attempt initial access using discovered attack surface on {target}",
    ],
    "exec":    [
        "Establish stable shell on {target} and verify execution context",
    ],
    "privesc": [
        "Enumerate local privilege escalation vectors on {target}",
        "Escalate to root/SYSTEM on {target}",
    ],
    "cred":    [
        "Dump credential material from {target} (hashes, tickets, cleartext)",
        "Attempt lateral movement with captured credentials",
    ],
    "lateral": [
        "Identify adjacent hosts reachable from {target}",
        "Pivot to highest-value asset in scope",
    ],
    "exfil":   [
        "Document all captured flags, credentials, and evidence from {target}",
    ],
    "impact":  [
        "Generate final engagement report with risk ratings for {target}",
    ],
}

# ─── Data model ──────────────────────────────────────────────────────────────


@dataclass
class ACIGoal:
    """Immutable descriptor for a natural-language engagement goal."""

    text: str
    target: str
    scope: List[str] = field(default_factory=list)
    domain: str = ""
    os_hint: str = "unknown"


@dataclass
class AttackPhase:
    """One tactical phase inside an ACIPlan."""

    id: str
    phase: str
    tactic: str
    tactic_name: str
    techniques: List[str]
    objectives: List[str]          # objective IDs injected into ObjectiveStore
    status: str = "pending"        # pending / active / done / blocked / skipped
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    block_reason: str = ""

    def to_dict(self) -> dict:
        """Serialize to dict for JSON persistence."""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "AttackPhase":
        """Deserialize from dict."""
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ACIPlan:
    """Full tactical plan for one engagement goal."""

    id: str
    goal: str
    target: str
    scope: List[str]
    created_at: str
    updated_at: str
    status: str                    # draft / active / replanning / completed / abandoned
    phases: List[AttackPhase]
    replan_count: int = 0
    replan_reasons: List[str] = field(default_factory=list)
    domain: str = ""
    os_hint: str = "unknown"

    @property
    def active_phase(self) -> Optional[AttackPhase]:
        """Return the first phase that is active or pending."""
        for ph in self.phases:
            if ph.status in ("active", "pending"):
                return ph
        return None

    @property
    def completion_pct(self) -> int:
        """Percentage of phases that are done or skipped."""
        if not self.phases:
            return 0
        done = sum(1 for p in self.phases if p.status in ("done", "skipped"))
        return int(done / len(self.phases) * 100)

    def to_dict(self) -> dict:
        """Serialize to dict for JSON persistence."""
        d = asdict(self)
        d["completion_pct"] = self.completion_pct
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ACIPlan":
        """Deserialize from dict."""
        phases = [AttackPhase.from_dict(p) for p in d.get("phases", [])]
        fields = {k: v for k, v in d.items()
                  if k in cls.__dataclass_fields__ and k != "phases"}
        return cls(phases=phases, **fields)


# ─── Persistence helpers ──────────────────────────────────────────────────────


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _save_plan(plan: ACIPlan, plan_file: Optional[Path] = None) -> None:
    """Atomically write plan to aci_plan.json."""
    if plan_file is None:
        plan_file = ACI_PLAN_FILE
    plan_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = plan_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(plan.to_dict(), indent=2))
    tmp.replace(plan_file)


def _load_plan(plan_file: Optional[Path] = None) -> Optional[ACIPlan]:
    """Load active plan from aci_plan.json, return None if absent/corrupt."""
    if plan_file is None:
        plan_file = ACI_PLAN_FILE
    if not plan_file.exists():
        return None
    try:
        return ACIPlan.from_dict(json.loads(plan_file.read_text()))
    except Exception as exc:
        log.warning("Failed to load ACI plan: %s", exc)
        return None


def _archive_plan(plan: ACIPlan, history_file: Optional[Path] = None) -> None:
    """Append plan to aci_history.jsonl."""
    if history_file is None:
        history_file = ACI_HISTORY_FILE
    history_file.parent.mkdir(parents=True, exist_ok=True)
    with open(history_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(plan.to_dict()) + "\n")


def _load_payload() -> dict:
    """Read payload.json for api_key, target context."""
    payload_file = BASE_DIR / "payload.json"
    try:
        return json.loads(payload_file.read_text())
    except Exception:
        return {}


def _load_world_model() -> dict:
    """Read sessions/world_model.json for live engagement context."""
    wm_file = SESSIONS_DIR / "world_model.json"
    try:
        return json.loads(wm_file.read_text())
    except Exception:
        return {}


def _count_objectives_by_status(obj_ids: List[str], objectives_file: Path = OBJECTIVES_FILE) -> Dict[str, int]:
    """Count objectives in a list by their current status."""
    if not objectives_file.exists():
        return {}
    counts: Dict[str, int] = {}
    try:
        for line in objectives_file.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("id") in obj_ids:
                st = obj.get("status", "pending")
                counts[st] = counts.get(st, 0) + 1
    except Exception as exc:
        log.warning("Failed reading objectives: %s", exc)
    return counts


# ─── LLM helpers ─────────────────────────────────────────────────────────────

_DECOMPOSE_SYSTEM = """\
You are an expert red team planner.
Given a penetration test engagement goal, decompose it into tactical ATT&CK-aligned phases.
Return ONLY valid JSON — no markdown, no prose — in this exact schema:

{
  "phases": [
    {
      "phase": "<slug: recon|enum|exploit|exec|privesc|cred|lateral|exfil|impact>",
      "tactic": "<MITRE tactic ID e.g. TA0043>",
      "tactic_name": "<MITRE tactic name>",
      "techniques": ["<T-ID>", ...],
      "objectives": [
        "<one concrete objective sentence for this target>",
        ...
      ]
    }
  ]
}

Rules:
- Include only phases relevant to the stated goal.
- Each phase has 1-4 objective sentences, specific to the target and goal.
- Objectives must be actionable commands or actions an operator can perform.
- Never include phases that are obviously out of scope for the goal.
- Never exceed 8 phases total.
"""


def _llm_decompose(goal: ACIGoal, api_key: str) -> Optional[List[dict]]:
    """Call Groq to decompose goal into phases. Returns raw phase dicts or None."""
    if not api_key:
        return None
    prompt = (
        f"Goal: {goal.text}\n"
        f"Target: {goal.target}\n"
        f"Scope: {', '.join(goal.scope) or 'single host'}\n"
        f"Domain: {goal.domain or 'none'}\n"
        f"OS hint: {goal.os_hint}\n"
    )
    body = json.dumps({
        "model": GROQ_DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": _DECOMPOSE_SYSTEM},
            {"role": "user",   "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 2048,
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(
        GROQ_API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        ctx = __import__("ssl").create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = json.loads(resp.read())
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return parsed.get("phases", [])
    except Exception as exc:
        log.warning("LLM decompose failed: %s", exc)
        return None


_REPLAN_SYSTEM = """\
You are an expert red team planner adapting to obstacles.
Given the current plan state and the reason for replanning, generate replacement objectives
for the blocked/remaining phases. Return ONLY valid JSON:

{
  "phases": [
    {
      "phase": "<same slug as original>",
      "tactic": "<MITRE tactic ID>",
      "tactic_name": "<name>",
      "techniques": ["<T-ID>", ...],
      "objectives": ["<new objective>", ...]
    }
  ]
}

Only include phases that are still pending/blocked (not already completed).
Prefer alternative techniques if the original approach was blocked.
"""


def _llm_replan(plan: ACIPlan, reason: str, api_key: str) -> Optional[List[dict]]:
    """Call Groq to generate replacement objectives for remaining phases."""
    if not api_key:
        return None
    remaining = [p for p in plan.phases if p.status not in ("done", "skipped")]
    if not remaining:
        return None
    context = (
        f"Original goal: {plan.goal}\n"
        f"Target: {plan.target}\n"
        f"Replan reason: {reason}\n"
        f"Blocked/pending phases: {[p.phase for p in remaining]}\n"
        f"Replan count so far: {plan.replan_count}\n"
    )
    body = json.dumps({
        "model": GROQ_DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": _REPLAN_SYSTEM},
            {"role": "user",   "content": context},
        ],
        "temperature": 0.15,
        "max_tokens": 2048,
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(
        GROQ_API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        ctx = __import__("ssl").create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = json.loads(resp.read())
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return parsed.get("phases", [])
    except Exception as exc:
        log.warning("LLM replan failed: %s", exc)
        return None


# ─── ACIPlanner ───────────────────────────────────────────────────────────────


class ACIPlanner:
    """Decomposes a high-level engagement goal into an ACIPlan.

    Uses the Groq LLM when an api_key is available; falls back to
    the static MITRE kill-chain template otherwise.

    Args:
        api_key: Groq API key. If empty, static fallback is used.
        objectives_file: Path override for ObjectiveStore (tests).
        plan_file: Path override for ACI plan JSON (tests).
    """

    def __init__(
        self,
        api_key: str = "",
        objectives_file: Optional[Path] = None,
        plan_file: Optional[Path] = None,
    ) -> None:
        self._api_key = api_key
        self._objectives_file = objectives_file if objectives_file is not None else OBJECTIVES_FILE
        self._plan_file = plan_file if plan_file is not None else ACI_PLAN_FILE

    def plan(self, goal: ACIGoal, phase_filter: Optional[List[str]] = None) -> ACIPlan:
        """Decompose *goal* into an ACIPlan, inject objectives, persist.

        Args:
            goal: ACIGoal descriptor.
            phase_filter: If provided, only include these phase slugs.

        Returns:
            A new ACIPlan with status 'active'.
        """
        raw_phases = _llm_decompose(goal, self._api_key)
        if raw_phases:
            phases = self._build_phases_from_llm(raw_phases, goal, phase_filter)
        else:
            phases = self._build_phases_static(goal, phase_filter)

        plan = ACIPlan(
            id=secrets.token_hex(6),
            goal=goal.text,
            target=goal.target,
            scope=list(goal.scope),
            domain=goal.domain,
            os_hint=goal.os_hint,
            created_at=_now_iso(),
            updated_at=_now_iso(),
            status="active",
            phases=phases,
        )
        if plan.phases:
            plan.phases[0].status = "active"
            plan.phases[0].started_at = _now_iso()

        self._inject_all_objectives(plan)
        _save_plan(plan, self._plan_file)
        return plan

    # ── internal builders ────────────────────────────────────────────────────

    def _build_phases_from_llm(
        self,
        raw: List[dict],
        goal: ACIGoal,
        phase_filter: Optional[List[str]],
    ) -> List[AttackPhase]:
        phases = []
        for r in raw:
            slug = r.get("phase", "")
            if phase_filter and slug not in phase_filter:
                continue
            texts = r.get("objectives", [])[:MAX_OBJECTIVES_PER_PHASE]
            ap = AttackPhase(
                id=f"ph_{secrets.token_hex(3)}",
                phase=slug,
                tactic=r.get("tactic", ""),
                tactic_name=r.get("tactic_name", ""),
                techniques=r.get("techniques", []),
                objectives=[],
                status="pending",
            )
            object.__setattr__(ap, "_obj_texts", texts)
            phases.append(ap)
        return phases

    def _build_phases_static(
        self,
        goal: ACIGoal,
        phase_filter: Optional[List[str]],
    ) -> List[AttackPhase]:
        phases = []
        for entry in MITRE_KILL_CHAIN:
            slug = entry["phase"]
            if phase_filter and slug not in phase_filter:
                continue
            templates = PHASE_OBJECTIVE_TEMPLATES.get(slug, [])
            obj_texts = [
                t.format(target=goal.target, domain=goal.domain or goal.target)
                for t in templates[:MAX_OBJECTIVES_PER_PHASE]
            ]
            ap = AttackPhase(
                id=f"ph_{secrets.token_hex(3)}",
                phase=slug,
                tactic=entry["tactic"],
                tactic_name=entry["tactic_name"],
                techniques=list(entry["techniques"]),
                objectives=[],
                status="pending",
            )
            object.__setattr__(ap, "_obj_texts", obj_texts)
            phases.append(ap)
        return phases

    def _inject_all_objectives(self, plan: ACIPlan) -> None:
        """Inject objectives for every phase into the ObjectiveStore."""
        self._objectives_file.parent.mkdir(parents=True, exist_ok=True)
        for phase in plan.phases:
            texts: List[str] = getattr(phase, "_obj_texts", [])
            for text in texts:
                obj_id = self._write_objective(text, phase.phase, plan.target)
                phase.objectives.append(obj_id)

    def _write_objective(self, text: str, phase: str, target: str) -> str:
        """Append one objective to objectives.jsonl and return its id."""
        obj_id = secrets.token_hex(4)
        record = {
            "id": obj_id,
            "text": text,
            "priority": "high",
            "status": "pending",
            "source": "aci_planner",
            "context": {"phase": phase, "target": target},
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "notes": "",
        }
        with open(self._objectives_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
        return obj_id


# ─── ACIEngine ────────────────────────────────────────────────────────────────


class ACIEngine:
    """Monitors ACIPlan execution and triggers replanning when stalled.

    Args:
        api_key: Groq API key for LLM-backed replan.
        plan_file: Path override (tests).
        objectives_file: Path override (tests).
        history_file: Path override (tests).
        replan_threshold: Blocked-objective count that triggers replan.
    """

    def __init__(
        self,
        api_key: str = "",
        plan_file: Optional[Path] = None,
        objectives_file: Optional[Path] = None,
        history_file: Optional[Path] = None,
        replan_threshold: int = REPLAN_THRESHOLD,
    ) -> None:
        self._api_key = api_key
        self._plan_file = plan_file if plan_file is not None else ACI_PLAN_FILE
        self._objectives_file = objectives_file if objectives_file is not None else OBJECTIVES_FILE
        self._history_file = history_file if history_file is not None else ACI_HISTORY_FILE
        self._replan_threshold = replan_threshold

    def status(self) -> dict:
        """Return a structured status dict for the active plan.

        Returns:
            Dict with keys: plan_id, goal, target, status, phases, completion_pct,
            active_phase, blocked_count, replan_count, should_replan.
        """
        plan = _load_plan(self._plan_file)
        if plan is None:
            return {"available": False, "reason": "No active ACI plan found."}

        self._sync_phase_statuses(plan)
        _save_plan(plan, self._plan_file)

        ap = plan.active_phase
        blocked = self._count_blocked(plan)
        return {
            "available": True,
            "plan_id": plan.id,
            "goal": plan.goal,
            "target": plan.target,
            "scope": plan.scope,
            "status": plan.status,
            "phases": [
                {
                    "phase": p.phase,
                    "tactic": p.tactic_name,
                    "status": p.status,
                    "objectives_count": len(p.objectives),
                    "techniques": p.techniques[:3],
                }
                for p in plan.phases
            ],
            "completion_pct": plan.completion_pct,
            "active_phase": ap.phase if ap else None,
            "blocked_count": blocked,
            "replan_count": plan.replan_count,
            "should_replan": self.should_replan(plan),
        }

    def should_replan(self, plan: Optional[ACIPlan] = None) -> bool:
        """Return True when the plan is stalled and a replan is warranted.

        Args:
            plan: Pre-loaded plan (avoids re-reading disk in tight loops).
        """
        if plan is None:
            plan = _load_plan(self._plan_file)
        if plan is None or plan.status in ("completed", "abandoned"):
            return False
        blocked = self._count_blocked(plan)
        return blocked >= self._replan_threshold

    def replan(self, reason: str = "") -> Tuple[Optional[ACIPlan], str]:
        """Generate a new set of objectives for blocked/remaining phases.

        Args:
            reason: Human-readable explanation of why we're replanning.

        Returns:
            (updated_plan, message) — plan is None if no active plan exists.
        """
        plan = _load_plan(self._plan_file)
        if plan is None:
            return None, "No active ACI plan to replan."

        plan.status = "replanning"
        plan.replan_count += 1
        plan.replan_reasons.append(f"[{_now_iso()}] {reason or 'manual trigger'}")
        plan.updated_at = _now_iso()
        _save_plan(plan, self._plan_file)

        planner = ACIPlanner(
            api_key=self._api_key,
            objectives_file=self._objectives_file,
            plan_file=self._plan_file,
        )
        remaining = [p for p in plan.phases if p.status not in ("done", "skipped")]

        raw_phases = _llm_replan(plan, reason, self._api_key)
        if raw_phases:
            for rp in raw_phases:
                slug = rp.get("phase", "")
                for existing in remaining:
                    if existing.phase == slug:
                        existing.objectives.clear()
                        texts = rp.get("objectives", [])[:MAX_OBJECTIVES_PER_PHASE]
                        object.__setattr__(existing, "_obj_texts", texts)
                        existing.status = "pending"
                        existing.block_reason = ""
        else:
            goal = ACIGoal(
                text=plan.goal,
                target=plan.target,
                scope=plan.scope,
                domain=plan.domain,
                os_hint=plan.os_hint,
            )
            new_phases = planner._build_phases_static(
                goal,
                phase_filter=[p.phase for p in remaining],
            )
            for new_ph in new_phases:
                for existing in remaining:
                    if existing.phase == new_ph.phase:
                        existing.objectives.clear()
                        texts = getattr(new_ph, "_obj_texts", [])
                        object.__setattr__(existing, "_obj_texts", texts)
                        existing.status = "pending"
                        existing.block_reason = ""

        planner._inject_all_objectives(plan)

        plan.status = "active"
        if plan.phases:
            first_pending = next((p for p in plan.phases if p.status == "pending"), None)
            if first_pending:
                first_pending.status = "active"
                first_pending.started_at = _now_iso()

        _save_plan(plan, self._plan_file)
        return plan, f"Replan #{plan.replan_count} complete. Reason: {reason or 'manual trigger'}"

    def complete(self) -> str:
        """Mark the active plan as completed and archive it."""
        plan = _load_plan(self._plan_file)
        if plan is None:
            return "No active ACI plan."
        plan.status = "completed"
        plan.updated_at = _now_iso()
        _save_plan(plan, self._plan_file)
        _archive_plan(plan, self._history_file)
        return f"Plan {plan.id} completed and archived."

    # ── private helpers ──────────────────────────────────────────────────────

    def _sync_phase_statuses(self, plan: ACIPlan) -> None:
        """Update each phase status based on current objective completion."""
        for phase in plan.phases:
            if not phase.objectives:
                continue
            counts = _count_objectives_by_status(phase.objectives, self._objectives_file)
            total = len(phase.objectives)
            done_ct = counts.get("done", 0)
            blocked_ct = counts.get("blocked", 0)
            skipped_ct = counts.get("skipped", 0)

            if done_ct + skipped_ct >= total:
                if phase.status not in ("done", "skipped"):
                    phase.status = "done"
                    phase.completed_at = _now_iso()
            elif blocked_ct >= total and total > 0:
                phase.status = "blocked"
                phase.block_reason = f"All {total} objectives blocked"

    def _count_blocked(self, plan: ACIPlan) -> int:
        """Count total blocked objectives across all non-done phases."""
        blocked = 0
        for phase in plan.phases:
            if phase.status in ("done", "skipped"):
                continue
            counts = _count_objectives_by_status(phase.objectives, self._objectives_file)
            blocked += counts.get("blocked", 0)
        return blocked


# ─── ACIReflector ─────────────────────────────────────────────────────────────


class ACIReflector:
    """Generates campaign lessons from completed or replanned ACIPlan outcomes.

    Lessons are appended to sessions/campaign_lessons.jsonl in the same
    format used by EpisodeReflectionEngine in lazyown_campaign.py.

    Args:
        lessons_file: Path override (tests).
    """

    def __init__(self, lessons_file: Optional[Path] = None) -> None:
        self._lessons_file = lessons_file if lessons_file is not None else LESSONS_FILE

    def reflect(self, plan: ACIPlan) -> List[dict]:
        """Analyse *plan* and generate lessons.

        Args:
            plan: A completed or replanned ACIPlan.

        Returns:
            List of lesson dicts appended to campaign_lessons.jsonl.
        """
        lessons = []
        for phase in plan.phases:
            if phase.status == "blocked":
                lesson = {
                    "id": secrets.token_hex(4),
                    "campaign_id": plan.id,
                    "phase": phase.phase,
                    "tactic": phase.tactic,
                    "techniques_tried": phase.techniques,
                    "outcome": "blocked",
                    "lesson": (
                        f"Phase '{phase.phase}' ({phase.tactic_name}) was blocked "
                        f"on target {plan.target}. "
                        f"Reason: {phase.block_reason or 'unknown'}. "
                        "Consider alternative techniques next engagement."
                    ),
                    "severity": "medium",
                    "created_at": _now_iso(),
                    "source": "aci_reflector",
                }
                lessons.append(lesson)
            elif phase.status == "done" and plan.replan_count > 0:
                lesson = {
                    "id": secrets.token_hex(4),
                    "campaign_id": plan.id,
                    "phase": phase.phase,
                    "tactic": phase.tactic,
                    "techniques_tried": phase.techniques,
                    "outcome": "succeeded_after_replan",
                    "lesson": (
                        f"Phase '{phase.phase}' succeeded after {plan.replan_count} replan(s) "
                        f"on {plan.target}. "
                        "Document the alternative technique that worked."
                    ),
                    "severity": "info",
                    "created_at": _now_iso(),
                    "source": "aci_reflector",
                }
                lessons.append(lesson)

        self._persist_lessons(lessons)
        return lessons

    def _persist_lessons(self, lessons: List[dict]) -> None:
        """Append lessons to campaign_lessons.jsonl."""
        if not lessons:
            return
        self._lessons_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._lessons_file, "a", encoding="utf-8") as fh:
            for lesson in lessons:
                fh.write(json.dumps(lesson) + "\n")


# ─── MCP bridge functions ─────────────────────────────────────────────────────


def mcp_aci_plan(
    goal: str,
    target: str,
    scope: Optional[List[str]] = None,
    domain: str = "",
    os_hint: str = "unknown",
    phase_filter: Optional[List[str]] = None,
) -> str:
    """Plan an engagement goal and return a JSON summary.

    Args:
        goal: Natural-language engagement goal.
        target: Primary target IP or hostname.
        scope: List of CIDR ranges or IPs in scope.
        domain: Target domain (optional).
        os_hint: Target OS hint: 'linux', 'windows', or 'unknown'.
        phase_filter: Only include these phase slugs (e.g. ['recon','exploit']).

    Returns:
        JSON string with plan summary.
    """
    payload = _load_payload()
    api_key = (
        os.environ.get("GROQ_API_KEY", "")
        or payload.get("api_key", "")
    )
    aci_goal = ACIGoal(
        text=goal,
        target=target or payload.get("rhost", ""),
        scope=scope or [],
        domain=domain or payload.get("domain", ""),
        os_hint=os_hint,
    )
    planner = ACIPlanner(api_key=api_key, objectives_file=OBJECTIVES_FILE, plan_file=ACI_PLAN_FILE)
    plan = planner.plan(aci_goal, phase_filter=phase_filter)
    summary = {
        "plan_id": plan.id,
        "goal": plan.goal,
        "target": plan.target,
        "phases": [
            {
                "phase": p.phase,
                "tactic": p.tactic_name,
                "techniques": p.techniques[:3],
                "objectives_count": len(p.objectives),
                "status": p.status,
            }
            for p in plan.phases
        ],
        "total_phases": len(plan.phases),
        "total_objectives": sum(len(p.objectives) for p in plan.phases),
        "backend": "llm" if api_key else "static",
        "message": (
            f"Plan {plan.id} created with {len(plan.phases)} phases and "
            f"{sum(len(p.objectives) for p in plan.phases)} objectives injected. "
            f"Run lazyown_auto_loop() to start execution."
        ),
    }
    return json.dumps(summary, indent=2)


def mcp_aci_status() -> str:
    """Return live status of the active ACI plan as JSON.

    Returns:
        JSON string with plan status, phase breakdown, and replan recommendation.
    """
    payload = _load_payload()
    api_key = os.environ.get("GROQ_API_KEY", "") or payload.get("api_key", "")
    engine = ACIEngine(
        api_key=api_key,
        plan_file=ACI_PLAN_FILE,
        objectives_file=OBJECTIVES_FILE,
        history_file=ACI_HISTORY_FILE,
    )
    return json.dumps(engine.status(), indent=2)


def mcp_aci_replan(reason: str = "") -> str:
    """Force adaptive replanning of the active ACI plan.

    Args:
        reason: Why replanning is needed (e.g. 'Kerberoasting blocked').

    Returns:
        JSON string with replan result summary.
    """
    payload = _load_payload()
    api_key = os.environ.get("GROQ_API_KEY", "") or payload.get("api_key", "")
    engine = ACIEngine(
        api_key=api_key,
        plan_file=ACI_PLAN_FILE,
        objectives_file=OBJECTIVES_FILE,
        history_file=ACI_HISTORY_FILE,
    )
    plan, message = engine.replan(reason)
    if plan is None:
        return json.dumps({"ok": False, "message": message})
    reflector = ACIReflector(lessons_file=LESSONS_FILE)
    lessons = reflector.reflect(plan)
    return json.dumps({
        "ok": True,
        "plan_id": plan.id,
        "replan_count": plan.replan_count,
        "message": message,
        "lessons_generated": len(lessons),
        "phases_remaining": sum(1 for p in plan.phases if p.status not in ("done", "skipped")),
    }, indent=2)


# ─── CLI entry point ──────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Autonomous Campaign Intelligence (ACI) Planner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("plan", help="Decompose a goal into a tactical plan")
    sp.add_argument("goal", help="Natural-language engagement goal")
    sp.add_argument("--target", default="", help="Primary target IP/hostname")
    sp.add_argument("--scope", nargs="*", default=[], help="CIDR ranges in scope")
    sp.add_argument("--domain", default="", help="Target domain")
    sp.add_argument("--os", dest="os_hint", default="unknown", help="OS hint: linux|windows|unknown")
    sp.add_argument("--phases", nargs="*", default=None, help="Only include these phase slugs")

    sub.add_parser("status", help="Show active plan status")

    rp = sub.add_parser("replan", help="Force adaptive replan of active plan")
    rp.add_argument("reason", nargs="?", default="", help="Reason for replanning")

    sub.add_parser("reflect", help="Generate lessons from active plan outcomes")

    return p


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for CLI usage."""
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "plan":
        print(mcp_aci_plan(
            goal=args.goal,
            target=args.target,
            scope=args.scope,
            domain=args.domain,
            os_hint=args.os_hint,
            phase_filter=args.phases,
        ))
        return 0

    if args.cmd == "status":
        print(mcp_aci_status())
        return 0

    if args.cmd == "replan":
        print(mcp_aci_replan(reason=args.reason))
        return 0

    if args.cmd == "reflect":
        plan = _load_plan(ACI_PLAN_FILE)
        if plan is None:
            print(json.dumps({"error": "No active ACI plan."}))
            return 1
        reflector = ACIReflector()
        lessons = reflector.reflect(plan)
        print(json.dumps({"lessons": lessons}, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
