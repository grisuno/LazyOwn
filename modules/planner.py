"""Fact-based planner — decides the next ability to run.

The planner queries :class:`modules.world_model.WorldModel` for the
current facts, :class:`modules.obs_parser.ObsParser` for fresh
findings, and :class:`modules.playbook_engine.PlaybookEngine` for the
candidate abilities pulled from STIX2 + Atomic Red Team. It then
applies a deterministic ranking rule (no LLM dependency) to pick the
best next step.

Why this exists separately from ``PlaybookEngine``:
- ``PlaybookEngine.derive()`` produces a *batch* playbook at planning
  time. The planner picks a *single* next step at runtime.
- The planner respects observed facts (e.g. "smb signing disabled")
  and gates techniques that depend on them.

Ranking rule (transparent, no LLM):
    score = base + matched_fact_bonus - risk_penalty
where:
    base            : 100
    matched_fact    : +25 per required fact the world model satisfies
    confidence      : + author-rating (heuristic from technique description)
    risk_penalty    : -20 if technique is loud/destructive

If ``api_key`` is set, the planner can delegate re-ranking to the LLM
as a tie-breaker only.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger("planner")

_BASE_DIR = Path(__file__).parent.parent


@dataclass
class PlanCandidate:
    technique_id: str
    name: str
    tactic: str
    command: str
    description: str = ""
    score: float = 0.0
    matched_facts: list[str] = field(default_factory=list)
    missing_facts: list[str] = field(default_factory=list)
    risk: str = "low"


@dataclass
class PlanResult:
    target: str
    candidates: list[PlanCandidate]
    chosen: PlanCandidate | None
    rationale: str
    facts_observed: list[str] = field(default_factory=list)


def _gather_facts(world_model=None, obs_parser=None) -> list[str]:
    """Collect a flat list of fact-type strings from world model + obs parser."""
    facts: list[str] = []

    if world_model is not None:
        try:
            wm = world_model()
            snap = wm.snapshot() if hasattr(wm, "snapshot") else {}
        except Exception:
            snap = {}
        if isinstance(snap, dict):
            if snap.get("hosts"):
                facts.append("host.found")
            for h in snap.get("hosts", {}).values():
                if h.get("services"):
                    facts.append("service.found")
                if h.get("credentials"):
                    facts.append("credential.valid")
                if h.get("state") in ("exploited", "owned"):
                    facts.append("session.created")
                if h.get("vulnerabilities"):
                    facts.append("vulnerability.found")

    if obs_parser is not None:
        try:
            parser = obs_parser()
        except Exception:
            parser = None
        if parser is not None and hasattr(parser, "get_all_findings"):
            try:
                for f in parser.get_all_findings():
                    if f.type.value == "ip" and f.value and f.value not in facts:
                        facts.append("ip.discovered")
                    if f.type.value == "credential":
                        facts.append("credential.valid")
                    if f.type.value == "service_version":
                        facts.append("service.found")
                    if f.type.value == "hash":
                        facts.append("hash.found")
                    if f.type.value == "cve":
                        facts.append("vulnerability.found")
            except Exception:
                pass

    return sorted(set(facts))


_REQUIRED_FACTS = {
    "T1595.001": ["host.found"],
    "T1595.002": ["host.found"],
    "T1046":     ["host.found"],
    "T1018":     ["host.found", "service.found"],
    "T1016":     ["service.found"],
    "T1021.002": ["service.found", "credential.valid"],
    "T1021.001": ["service.found", "credential.valid"],
    "T1059.001": ["session.created"],
    "T1059.003": ["service.found"],
    "T1003.001": ["session.created"],
    "T1003.002": ["session.created"],
    "T1003.003": ["session.created"],
    "T1555":     ["session.created"],
    "T1547.001": ["session.created"],
    "T1543.003": ["session.created"],
    "T1136.001": ["session.created"],
    "T1110":     ["service.found"],
    "T1078":     ["credential.valid"],
    "T1562.001": ["session.created"],
    "T1087.002": ["session.created"],
    "T1087.001": ["session.created"],
    "T1083":     ["session.created"],
    "T1082":     ["session.created"],
    "T1012":     ["session.created"],
    "T1041":     ["file.found", "session.created"],
    "T1048":     ["file.found", "session.created"],
    "T1560":     ["file.found"],
}


_RISK_MAP = {
    "T1529": "high",
    "T1485": "high",
    "T1486": "high",
    "T1490": "high",
    "T1484": "high",
    "T1489": "high",
    "T1487": "high",
    "T1499": "high",
    "T1498": "high",
    "T1505": "medium",
    "T1543": "medium",
    "T1547": "medium",
    "T1546": "medium",
    "T1053": "medium",
}


def _risk_for(technique_id: str) -> str:
    for prefix, risk in _RISK_MAP.items():
        if technique_id.startswith(prefix):
            return risk
    return "low"


_RISK_PENALTY = {"low": 0, "medium": 20, "high": 40}


_FALLBACK_TECHNIQUES = [
    ("T1595.001", "IP Block Scan",             "reconnaissance",      "nmap -sn {target}/24",                "Discover live hosts on the target subnet"),
    ("T1046",     "Network Service Scan",      "discovery",           "nmap -sV -p- {target}",               "Enumerate open services and versions"),
    ("T1018",     "Remote System Discovery",   "discovery",           "net view /domain",                    "Discover remote systems"),
    ("T1016",     "System Network Config",     "discovery",           "ipconfig /all",                       "Read local network configuration"),
    ("T1110",     "Brute Force",               "credential-access",   "hydra -L users.txt -P pwds.txt {target} ssh", "Brute-force service credentials"),
    ("T1021.002", "SMB/Windows Admin Shares",  "lateral-movement",    "smbclient -L //{target} -U admin%pass", "Enumerate SMB shares with valid creds"),
    ("T1059.001", "PowerShell",                "execution",           "powershell -ep bypass -f shell.ps1",  "Execute PowerShell loader on session"),
    ("T1059.003", "Windows Command Shell",     "execution",           "cmd /c systeminfo",                   "Run cmd.exe on a session"),
    ("T1003.001", "LSASS Memory",              "credential-access",   "mimikatz sekurlsa::logonpasswords",   "Dump credentials from LSASS"),
    ("T1003.002", "Security Account Manager",  "credential-access",   "secretsdump.py LOCAL",                "Dump SAM via Impacket"),
    ("T1547.001", "Registry Run Keys",         "persistence",         "reg add HKCU\\...\\Run /v evil",      "Persist via registry Run key"),
    ("T1087.002", "Domain Account",            "discovery",           "net user /domain",                    "Enumerate domain accounts"),
    ("T1082",     "System Information",        "discovery",           "systeminfo",                          "Read system information"),
    ("T1562.001", "Disable or Modify Tools",   "defense-evasion",     "sc stop WinDefend",                   "Disable Windows Defender"),
    ("T1041",     "Exfil Over C2",             "exfiltration",        "powershell -c 'Invoke-WebRequest ...'","Send data over the C2 channel"),
]


def _score_step(step, facts: list[str]) -> PlanCandidate:
    tid = getattr(step, "technique_id", "") or ""
    name = getattr(step, "name", "") or ""
    tactic = getattr(step, "tactic", "") or ""
    cmd = getattr(step, "command", "") or ""
    desc = getattr(step, "description", "") or ""

    required = _REQUIRED_FACTS.get(tid, ["host.found"])
    matched = [f for f in required if f in facts]
    missing = [f for f in required if f not in facts]

    base = 100.0
    bonus = 25.0 * len(matched)
    penalty = _RISK_PENALTY.get(_risk_for(tid), 0)
    score = base + bonus - penalty

    if "host.found" in missing and "host.found" in facts:
        missing = [f for f in missing if f != "host.found"]

    if missing and "host.found" in missing and len(missing) == len(required):
        score = 0

    return PlanCandidate(
        technique_id=tid,
        name=name,
        tactic=tactic,
        command=cmd,
        description=desc,
        score=score,
        matched_facts=matched,
        missing_facts=missing,
        risk=_risk_for(tid),
    )


class Planner:
    """Fact-based next-ability selector.

    Args:
        world_model: Lazy-initialised callable returning a WorldModel.
        obs_parser:  Lazy-initialised callable returning an ObsParser.
        api_key:     Optional LLM key for tie-breaking only.
    """

    def __init__(
        self,
        world_model=None,
        obs_parser=None,
        api_key: str = "",
    ) -> None:
        self._wm_factory = world_model
        self._parser_factory = obs_parser
        self._api_key = api_key

    def _wm(self):
        if self._wm_factory is None:
            try:
                from modules.world_model import get_world_model as _gwm
                self._wm_factory = _gwm
            except Exception:
                pass
        if self._wm_factory is None:
            return None
        try:
            return self._wm_factory()
        except Exception:
            return None

    def _parser(self):
        if self._parser_factory is None:
            try:
                from modules.obs_parser import get_parser as _gp
                self._parser_factory = lambda: _gp()
            except Exception:
                pass
        if self._parser_factory is None:
            return None
        try:
            return self._parser_factory()
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def plan(self, target: str, max_candidates: int = 10) -> PlanResult:
        """Return a ranked list of next-step candidates for *target*.

        Args:
            target: The IP/hostname being engaged.
            max_candidates: How many candidates to return.

        Returns:
            :class:`PlanResult` with ranked candidates and the chosen one.
        """
        from modules.playbook_engine import PlaybookEngine

        facts = _gather_facts(self._wm, self._parser_factory)
        log.info("planner: %d facts observed: %s", len(facts), facts)

        candidates: list[PlanCandidate] = []
        engine = PlaybookEngine()
        try:
            playbook = engine.derive(target, phase=None, apt_name="LazyOwn_auto")
        except Exception as exc:
            log.warning("planner: derive failed: %s", exc)
            playbook = None

        if playbook is not None and playbook.steps:
            for step in playbook.steps:
                candidates.append(_score_step(step, facts))
        else:
            for tid, name, tactic, cmd, desc in _FALLBACK_TECHNIQUES:
                step = type("Step", (), {})()
                step.technique_id = tid
                step.name = name
                step.tactic = tactic
                step.command = cmd
                step.description = desc
                candidates.append(_score_step(step, facts))

        candidates = [c for c in candidates if c.score > 0]
        candidates.sort(key=lambda c: c.score, reverse=True)
        candidates = candidates[:max_candidates]

        chosen = candidates[0] if candidates else None
        rationale = self._build_rationale(chosen, facts, target)

        if self._api_key and len(candidates) > 1 and chosen is not None:
            top2 = candidates[:2]
            if abs(top2[0].score - top2[1].score) < 5:
                reordered = self._llm_tiebreak(target, facts, top2)
                if reordered:
                    candidates = reordered + candidates[2:]
                    chosen = candidates[0]
                    rationale += " (LLM tie-break applied)"

        return PlanResult(
            target=target,
            candidates=candidates,
            chosen=chosen,
            rationale=rationale,
            facts_observed=facts,
        )

    @staticmethod
    def _build_rationale(chosen: PlanCandidate | None, facts: list[str], target: str) -> str:
        if chosen is None:
            return (
                f"no candidates for {target} — run scan/atomic first to populate facts "
                f"(have: {', '.join(facts) or 'none'})"
            )
        matched_str = ", ".join(chosen.matched_facts) or "none"
        return (
            f"chose {chosen.technique_id} {chosen.name!r} for {target}: "
            f"score={chosen.score:.0f}, matched=[{matched_str}], "
            f"risk={chosen.risk}, observed {len(facts)} facts"
        )

    def _llm_tiebreak(
        self, target: str, facts: list[str], candidates: list[PlanCandidate]
    ) -> list[PlanCandidate] | None:
        try:
            from llm_client import LLMClient
            client = LLMClient(api_key=self._api_key)
            names = "\n".join(
                f"{i+1}. [{c.technique_id}] {c.name}: score={c.score}"
                for i, c in enumerate(candidates)
            )
            prompt = (
                f"target={target}\nfacts={','.join(facts)}\n\n"
                f"Two near-equal candidates:\n{names}\n\n"
                f"Reply with 1 or 2 to pick the better one."
            )
            raw = client.ask(prompt, provider="groq", temperature=0.0)
            m = re.search(r'\b([12])\b', raw)
            if m:
                idx = int(m.group(1)) - 1
                if 0 <= idx < len(candidates):
                    other = candidates[1 - idx]
                    return [candidates[idx], other] + candidates[2:]
        except Exception as exc:
            log.debug("LLM tiebreak skipped: %s", exc)
        return None

    def to_dict(self, result: PlanResult) -> dict:
        return {
            "target": result.target,
            "rationale": result.rationale,
            "facts_observed": result.facts_observed,
            "chosen": (
                {
                    "technique_id": result.chosen.technique_id,
                    "name": result.chosen.name,
                    "tactic": result.chosen.tactic,
                    "command": result.chosen.command,
                    "score": result.chosen.score,
                    "matched_facts": result.chosen.matched_facts,
                    "missing_facts": result.chosen.missing_facts,
                    "risk": result.chosen.risk,
                }
                if result.chosen
                else None
            ),
            "candidates": [
                {
                    "technique_id": c.technique_id,
                    "name": c.name,
                    "score": c.score,
                    "risk": c.risk,
                    "matched_facts": c.matched_facts,
                    "missing_facts": c.missing_facts,
                }
                for c in result.candidates
            ],
        }


def get_planner(api_key: str = "") -> Planner:
    return Planner(api_key=api_key)


__all__ = [
    "Planner",
    "PlanCandidate",
    "PlanResult",
    "get_planner",
]
