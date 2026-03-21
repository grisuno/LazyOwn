#!/usr/bin/env python3
"""
modules/playbook_engine.py
===========================
Bridges MITRE ATT&CK (STIX2), Atomic Red Team, WorldModel, and LLMClient
into a closed autonomous execution cycle.

Workflow
--------
1.  derive(target, phase) -> Playbook
      - Resolve MITRE tactics for the current phase
      - Query STIX2 enterprise-attack store for techniques under those tactics
      - Filter by target platform (linux / windows / macos from WorldModel)
      - Match techniques to Atomic Red Team YAML test files
      - Ask LLM to select and rank the most relevant N tests (optional)
      - Return a Playbook ready for execution

2.  execute(playbook, executor) -> PlaybookResult
      - Run each PlaybookStep via the provided executor callable
      - Parse output with ObsParser -> update WorldModel
      - Record outcome per step
      - Return full PlaybookResult

3.  save(playbook, path) / load(path) -> Playbook
      - Persist / restore playbooks as YAML (compatible with existing format)

Design
------
- Single Responsibility : PlaybookEngine composes, not executes (executor is injected)
- Open/Closed           : new tactic mappings via PHASE_TACTIC_MAP extension
- Dependency Inversion  : depends on WorldModel and ObsParser protocols, not
                          concrete singletons (accepts instances or creates defaults)

Usage
-----
    from modules.playbook_engine import PlaybookEngine

    engine = PlaybookEngine()
    playbook = engine.derive("10.10.11.78", phase="scanning")
    result   = engine.execute(playbook, executor=lambda cmd, host: run(cmd))

    # Or via CLI:
    python3 modules/playbook_engine.py derive --target 10.10.11.78 --phase scanning
    python3 modules/playbook_engine.py run    --playbook playbooks/myplan.yaml --dry-run
"""
from __future__ import annotations

import glob
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

log = logging.getLogger("playbook_engine")

_BASE_DIR      = Path(__file__).parent.parent
_SESSIONS_DIR  = _BASE_DIR / "sessions"
_PLAYBOOK_DIR  = _BASE_DIR / "playbooks"
_ATOMIC_PATH   = _BASE_DIR / "external" / ".exploit" / "atomic-red-team"
_MITRE_PATH    = _BASE_DIR / "external" / ".exploit" / "mitre"
_ENTERPRISE_ATTACK_JSON = (
    _MITRE_PATH / "enterprise-attack" / "enterprise-attack-16.1.json"
)


# ---------------------------------------------------------------------------
# Phase -> MITRE tactic shortnames  (maps EngagementPhase to ATT&CK tactics)
# ---------------------------------------------------------------------------

PHASE_TACTIC_MAP: Dict[str, List[str]] = {
    "recon":             ["reconnaissance"],
    "scanning":          ["discovery"],
    "enumeration":       ["discovery", "credential-access"],
    "exploitation":      ["initial-access", "execution"],
    "post_exploitation": ["privilege-escalation", "lateral-movement",
                          "credential-access", "collection", "exfiltration"],
    "complete":          ["impact"],
}

# Default platform order when WorldModel has no os_hint
_DEFAULT_PLATFORM_ORDER = ["linux", "windows", "macos"]


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

@dataclass
class PlaybookStep:
    atomic_id:       str
    technique_id:    str       # e.g. T1059.001
    tactic:          str       # e.g. execution
    name:            str
    description:     str       = ""
    command:         str       = ""
    cleanup_command: str       = ""
    platform:        str       = "linux"
    mitre_url:       str       = ""
    llm_reasoning:   str       = ""

    def to_dict(self) -> dict:
        return {
            "atomic_id":       self.atomic_id,
            "technique_id":    self.technique_id,
            "tactic":          self.tactic,
            "name":            self.name,
            "description":     self.description,
            "command":         self.command,
            "cleanup_command": self.cleanup_command,
            "platform":        self.platform,
            "mitre_url":       self.mitre_url,
            "llm_reasoning":   self.llm_reasoning,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PlaybookStep":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Playbook:
    apt_name:     str
    description:  str
    target:       str
    phase:        str
    steps:        List[PlaybookStep] = field(default_factory=list)
    generated_at: str                = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "apt_name":     self.apt_name,
            "description":  self.description,
            "target":       self.target,
            "phase":        self.phase,
            "generated_at": self.generated_at,
            "steps":        [s.to_dict() for s in self.steps],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Playbook":
        steps = [PlaybookStep.from_dict(s) for s in d.get("steps", [])]
        return cls(
            apt_name     = d.get("apt_name", ""),
            description  = d.get("description", ""),
            target       = d.get("target", ""),
            phase        = d.get("phase", ""),
            generated_at = d.get("generated_at", ""),
            steps        = steps,
        )


@dataclass
class StepResult:
    step:     PlaybookStep
    output:   str
    success:  bool
    findings: list = field(default_factory=list)   # List[Finding] from obs_parser


@dataclass
class PlaybookResult:
    playbook:          Playbook
    results:           List[StepResult] = field(default_factory=list)
    total_steps:       int              = 0
    successful_steps:  int              = 0


# ---------------------------------------------------------------------------
# STIX2 loader (optional dependency)
# ---------------------------------------------------------------------------

class _StixLoader:
    """Loads the enterprise ATT&CK STIX2 bundle into a queryable in-memory store."""

    def __init__(self, json_path: Path = _ENTERPRISE_ATTACK_JSON) -> None:
        self._path  = json_path
        self._store = None

    def available(self) -> bool:
        return self._path.exists()

    def store(self):
        if self._store is None:
            if not self.available():
                return None
            try:
                from stix2 import MemoryStore, Filter  # noqa: F401
                with self._path.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                self._store = MemoryStore(stix_data=data)
                log.info("STIX2 store loaded from %s", self._path)
            except Exception as exc:
                log.warning("STIX2 load failed: %s", exc)
        return self._store

    def techniques_for_tactics(
        self, tactic_shortnames: List[str], platform: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Return ATT&CK techniques matching the given tactic shortnames."""
        store = self.store()
        if store is None:
            return []
        try:
            from stix2 import Filter
            techniques = store.query([Filter("type", "=", "attack-pattern")])
            results = []
            for t in techniques:
                phases = [p.get("phase_name", "") for p in t.get("kill_chain_phases", [])]
                if not any(phase in tactic_shortnames for phase in phases):
                    continue
                if platform:
                    platforms = [p.lower() for p in t.get("x_mitre_platforms", [])]
                    if platform.lower() not in platforms:
                        continue
                ext_refs = t.get("external_references", [])
                tid = next(
                    (r.get("external_id", "") for r in ext_refs
                     if r.get("source_name") == "mitre-attack"),
                    "",
                )
                results.append({
                    "id":          t.get("id", ""),
                    "technique_id": tid,
                    "name":        t.get("name", ""),
                    "description": t.get("description", "")[:300],
                    "tactics":     phases,
                    "platforms":   [p.lower() for p in t.get("x_mitre_platforms", [])],
                })
            return results
        except Exception as exc:
            log.warning("STIX2 query failed: %s", exc)
            return []


# ---------------------------------------------------------------------------
# Atomic Red Team index builder
# ---------------------------------------------------------------------------

class _AtomicIndex:
    """
    Indexes Atomic Red Team YAML files by technique ID.
    Returns concrete test definitions keyed by technique (T1059.001, etc.).
    """

    def __init__(self, atomics_path: Path = _ATOMIC_PATH / "atomics") -> None:
        self._path  = atomics_path
        self._index: Optional[Dict[str, List[dict]]] = None

    def available(self) -> bool:
        return self._path.exists()

    def build(self) -> Dict[str, List[dict]]:
        if self._index is not None:
            return self._index
        if not self.available():
            return {}
        index: Dict[str, List[dict]] = {}
        for yaml_file in glob.glob(str(self._path / "**" / "*.yaml"), recursive=True):
            try:
                with open(yaml_file, "r", encoding="utf-8", errors="replace") as fh:
                    data = yaml.safe_load(fh)
                if not data or "atomic_tests" not in data:
                    continue
                tid = data.get("attack_technique", "")
                if not tid:
                    continue
                for test in data["atomic_tests"]:
                    index.setdefault(tid, []).append({
                        "atomic_id":       test.get("auto_generated_guid", ""),
                        "name":            test.get("name", ""),
                        "description":     test.get("description", "")[:300],
                        "platforms":       test.get("supported_platforms", []),
                        "command":         test.get("executor", {}).get("command", ""),
                        "cleanup_command": test.get("executor", {}).get("cleanup_command", ""),
                        "technique_id":    tid,
                    })
            except Exception as exc:
                log.debug("Atomic parse error %s: %s", yaml_file, exc)
        self._index = index
        log.info("Atomic index built: %d techniques", len(index))
        return index

    def tests_for_technique(self, technique_id: str, platform: str = "linux") -> List[dict]:
        idx = self.build()
        candidates = idx.get(technique_id, [])
        return [t for t in candidates if platform.lower() in
                [p.lower() for p in t.get("platforms", [])]]


# ---------------------------------------------------------------------------
# LLM-based technique selector
# ---------------------------------------------------------------------------

class _TechniqueSelector:
    """
    Uses LLMClient to rank and select the most relevant techniques given
    WorldModel context. Falls back to returning the first N if LLM unavailable.
    """

    def select(
        self,
        candidates: List[dict],
        world_context: str,
        target: str,
        phase: str,
        api_key: str = "",
        top_n: int = 5,
    ) -> List[dict]:
        if not candidates:
            return []
        if len(candidates) <= top_n:
            return candidates
        if not api_key:
            return candidates[:top_n]
        try:
            from llm_client import LLMClient
            client = LLMClient(api_key=api_key)
            names = "\n".join(
                f"{i+1}. [{c['technique_id']}] {c['name']}: {c['description'][:80]}"
                for i, c in enumerate(candidates[:30])   # cap to avoid token overflow
            )
            prompt = (
                f"Target: {target}  Phase: {phase}\n\n"
                f"World model:\n{world_context}\n\n"
                f"Available ATT&CK techniques:\n{names}\n\n"
                f"Select the {top_n} most likely to succeed given the world model context. "
                f"Reply with a JSON array of indices (1-based), e.g. [2,5,1,3,4]."
            )
            raw = client.ask(
                prompt,
                provider="groq",
                system="You are an ATT&CK technique selector. Reply only with a JSON array of integers.",
                temperature=0.0,
            )
            import re
            m = re.search(r'\[[\d,\s]+\]', raw)
            if m:
                indices = json.loads(m.group())
                selected = []
                for idx in indices:
                    if 1 <= idx <= len(candidates):
                        selected.append(candidates[idx - 1])
                if selected:
                    log.info("LLM selected %d techniques for phase=%s", len(selected), phase)
                    return selected[:top_n]
        except Exception as exc:
            log.warning("LLM technique selection failed: %s", exc)
        return candidates[:top_n]


# ---------------------------------------------------------------------------
# PlaybookEngine
# ---------------------------------------------------------------------------

class PlaybookEngine:
    """
    Derives, executes, saves, and loads structured ATT&CK-grounded playbooks.

    Parameters
    ----------
    world_model  : WorldModel instance (created lazily if None)
    obs_parser   : ObsParser instance (created lazily if None)
    api_key      : Groq API key for LLM-based technique selection
    top_n        : maximum number of steps per generated playbook
    """

    def __init__(
        self,
        world_model=None,
        obs_parser=None,
        api_key: str = "",
        top_n: int = 5,
    ) -> None:
        self._wm       = world_model
        self._parser   = obs_parser
        self._api_key  = api_key or os.environ.get("GROQ_API_KEY", "")
        self._top_n    = top_n
        self._stix     = _StixLoader()
        self._atomic   = _AtomicIndex()
        self._selector = _TechniqueSelector()

    # ── Lazy accessors ────────────────────────────────────────────────────────

    def _world_model(self):
        if self._wm is None:
            try:
                sys.path.insert(0, str(Path(__file__).parent))
                from world_model import get_world_model
                self._wm = get_world_model()
            except Exception:
                pass
        return self._wm

    def _obs_parser(self):
        if self._parser is None:
            try:
                from obs_parser import get_parser
                self._parser = get_parser()
            except Exception:
                pass
        return self._parser

    # ── Public API ────────────────────────────────────────────────────────────

    def derive(
        self,
        target: str,
        phase: Optional[str] = None,
        platform: Optional[str] = None,
        apt_name: str = "LazyOwn_auto",
    ) -> Playbook:
        """
        Generate a Playbook for *target* at the given *phase*.

        If phase is None, derives it from the WorldModel.
        If platform is None, infers from WorldModel os_hint.
        """
        wm = self._world_model()

        # Resolve phase
        if phase is None:
            if wm is not None:
                phase = wm.get_phase().value
            else:
                phase = "scanning"

        # Resolve platform
        if platform is None and wm is not None:
            hosts = wm.snapshot().get("hosts", {})
            host_info = hosts.get(target, {})
            os_hint = host_info.get("os_hint", "").lower()
            if "windows" in os_hint:
                platform = "windows"
            elif "mac" in os_hint:
                platform = "macos"
            else:
                platform = "linux"
        platform = platform or "linux"

        # World model context string for LLM
        wm_context = wm.to_context_string() if wm is not None else "No world model available."

        # Tactics for this phase
        tactics = PHASE_TACTIC_MAP.get(phase, ["discovery"])
        log.info("Deriving playbook: target=%s phase=%s tactics=%s platform=%s",
                 target, phase, tactics, platform)

        # Query STIX2 for techniques
        if self._stix.available():
            techniques = self._stix.techniques_for_tactics(tactics, platform)
        else:
            log.warning("STIX2 data not available — run: git clone "
                        "https://github.com/mitre-attack/attack-stix-data.git "
                        "external/.exploit/mitre")
            techniques = []

        # LLM-ranked selection
        selected = self._selector.select(
            techniques, wm_context, target, phase,
            api_key=self._api_key, top_n=self._top_n * 2,
        )

        # Match to Atomic tests
        steps: List[PlaybookStep] = []
        for tech in selected:
            tid = tech.get("technique_id", "")
            if not tid:
                continue
            atomic_tests = self._atomic.tests_for_technique(tid, platform)
            if not atomic_tests:
                continue
            test = atomic_tests[0]   # pick first matching test
            tactic = tech.get("tactics", [""])[0]
            mitre_url = f"https://attack.mitre.org/techniques/{tid.replace('.', '/')}"
            steps.append(PlaybookStep(
                atomic_id       = test["atomic_id"],
                technique_id    = tid,
                tactic          = tactic,
                name            = test["name"],
                description     = test.get("description", tech.get("description", "")),
                command         = test.get("command", ""),
                cleanup_command = test.get("cleanup_command", ""),
                platform        = platform,
                mitre_url       = mitre_url,
            ))
            if len(steps) >= self._top_n:
                break

        if not steps:
            log.warning("No Atomic tests found for phase=%s platform=%s — playbook is empty",
                        phase, platform)

        return Playbook(
            apt_name    = apt_name,
            description = f"Auto-derived playbook for {target} at phase={phase} ({platform})",
            target      = target,
            phase       = phase,
            steps       = steps,
        )

    def execute(
        self,
        playbook: Playbook,
        executor: Callable[[str, str], str],
        dry_run: bool = False,
    ) -> PlaybookResult:
        """
        Execute a Playbook step by step.

        Parameters
        ----------
        playbook  : the Playbook to run
        executor  : callable(command: str, host: str) -> output: str
        dry_run   : if True, print commands without executing
        """
        result = PlaybookResult(playbook=playbook, total_steps=len(playbook.steps))
        parser = self._obs_parser()
        wm     = self._world_model()

        for step in playbook.steps:
            if not step.command.strip():
                log.debug("Skipping step %s — no command", step.technique_id)
                continue

            log.info("Executing step [%s] %s on %s",
                     step.technique_id, step.name, playbook.target)

            if dry_run:
                print(f"[DRY-RUN] [{step.technique_id}] {step.name}")
                print(f"  command: {step.command[:200]}")
                step_result = StepResult(step=step, output="[dry-run]", success=True)
            else:
                try:
                    output  = executor(step.command, playbook.target)
                    success = bool(output and len(output.strip()) > 5)
                except Exception as exc:
                    output  = f"[executor error] {exc}"
                    success = False

                # Parse observations and feed back to world model
                findings = []
                if parser is not None:
                    try:
                        obs      = parser.parse(output, host=playbook.target, tool=step.technique_id)
                        findings = obs.findings
                        success  = obs.success
                        if wm is not None:
                            wm.update_from_findings(findings)
                    except Exception as exc:
                        log.debug("ObsParser error: %s", exc)

                step_result = StepResult(
                    step=step, output=output, success=success, findings=findings
                )
                if success:
                    result.successful_steps += 1

            result.results.append(step_result)

        log.info("Playbook complete: %d/%d steps succeeded",
                 result.successful_steps, result.total_steps)
        return result

    # ── Persistence ───────────────────────────────────────────────────────────

    def save(self, playbook: Playbook, path: Optional[str | Path] = None) -> Path:
        """Persist playbook to YAML (compatible with existing playbooks/ format)."""
        if path is None:
            _PLAYBOOK_DIR.mkdir(parents=True, exist_ok=True)
            ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = _PLAYBOOK_DIR / f"{playbook.apt_name}_{ts}.yaml"
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(yaml.dump(playbook.to_dict(), allow_unicode=True, sort_keys=False),
                     encoding="utf-8")
        log.info("Playbook saved to %s", p)
        return p

    def load(self, path: str | Path) -> Playbook:
        """Load a playbook from YAML. Supports both new extended format and legacy format."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)

        # Legacy format: steps are {atomic_id: "..."} only
        steps_raw = data.get("steps", [])
        steps: List[PlaybookStep] = []
        for s in steps_raw:
            if isinstance(s, dict) and "technique_id" in s:
                steps.append(PlaybookStep.from_dict(s))
            elif isinstance(s, dict) and "atomic_id" in s:
                steps.append(PlaybookStep(
                    atomic_id    = s["atomic_id"],
                    technique_id = "",
                    tactic       = "",
                    name         = s.get("name", s["atomic_id"]),
                ))
        return Playbook(
            apt_name    = data.get("apt_name", ""),
            description = data.get("description", ""),
            target      = data.get("target", ""),
            phase       = data.get("phase", ""),
            steps       = steps,
        )

    def result_summary(self, result: PlaybookResult) -> str:
        """Return a human-readable / LLM-readable summary of a PlaybookResult."""
        lines = [
            f"Playbook: {result.playbook.apt_name}",
            f"Target:   {result.playbook.target}",
            f"Phase:    {result.playbook.phase}",
            f"Steps:    {result.successful_steps}/{result.total_steps} succeeded",
            "",
        ]
        for sr in result.results:
            status = "OK" if sr.success else "FAIL"
            lines.append(
                f"[{status}] [{sr.step.technique_id}] {sr.step.name[:60]}  "
                f"(tactic: {sr.step.tactic})"
            )
            if sr.findings:
                types = {}
                for f in sr.findings:
                    types[f.type] = types.get(f.type, 0) + 1
                lines.append(
                    "     findings: "
                    + ", ".join(f"{v}x {k}" for k, v in types.items())
                )
            if not sr.success and sr.output:
                lines.append(f"     output:   {sr.output[:120]}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_engine: Optional[PlaybookEngine] = None


def get_engine(api_key: str = "") -> PlaybookEngine:
    """Return (or create) the module-level singleton PlaybookEngine."""
    global _default_engine
    if _default_engine is None or (api_key and _default_engine._api_key != api_key):
        _default_engine = PlaybookEngine(api_key=api_key)
    return _default_engine


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    p = argparse.ArgumentParser(description="LazyOwn Playbook Engine")
    sub = p.add_subparsers(dest="cmd")

    # derive
    d = sub.add_parser("derive", help="Generate a playbook from ATT&CK + Atomic")
    d.add_argument("--target",   required=True)
    d.add_argument("--phase",    default=None)
    d.add_argument("--platform", default=None, choices=["linux", "windows", "macos"])
    d.add_argument("--top-n",    type=int, default=5)
    d.add_argument("--save",     action="store_true")

    # run
    r = sub.add_parser("run", help="Execute a playbook YAML")
    r.add_argument("--playbook", required=True)
    r.add_argument("--dry-run",  action="store_true")

    # show
    s = sub.add_parser("show", help="Show a playbook YAML in human-readable form")
    s.add_argument("--playbook", required=True)

    args = p.parse_args()

    sys.path.insert(0, str(_BASE_DIR / "modules"))
    engine = PlaybookEngine(api_key=os.environ.get("GROQ_API_KEY", ""), top_n=getattr(args, "top_n", 5))

    if args.cmd == "derive":
        pb = engine.derive(args.target, phase=args.phase, platform=args.platform)
        print(yaml.dump(pb.to_dict(), allow_unicode=True, sort_keys=False))
        if args.save:
            saved = engine.save(pb)
            print(f"Saved: {saved}")

    elif args.cmd == "run":
        pb = engine.load(args.playbook)

        def _local_executor(command: str, host: str) -> str:
            try:
                r = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=60
                )
                return (r.stdout + r.stderr).strip()
            except Exception as exc:
                return f"[error] {exc}"

        result = engine.execute(pb, executor=_local_executor, dry_run=args.dry_run)
        print(engine.result_summary(result))

    elif args.cmd == "show":
        pb = engine.load(args.playbook)
        print(f"Playbook: {pb.apt_name}  |  {pb.description}")
        print(f"Target: {pb.target}  Phase: {pb.phase}  Steps: {len(pb.steps)}")
        print()
        for i, s in enumerate(pb.steps, 1):
            print(f"  {i}. [{s.technique_id}] {s.name}  ({s.platform})")
            if s.mitre_url:
                print(f"     {s.mitre_url}")

    else:
        p.print_help()
