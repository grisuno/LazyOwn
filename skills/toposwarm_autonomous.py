#!/usr/bin/env python3
"""
skills/toposwarm_autonomous.py
================================
TopoSwarm Autonomous Red Team Agent
====================================
Drives LazyOwn through a full pentest kill-chain using TopoSwarm as the
local AI router, with no dependency on Groq, Ollama, or Claude Code.

Architecture
------------
  payload.json  →  AutonomousAgent
                        │
                   phase loop (ReAct style)
                        │
                ┌───────┴───────┐
                ▼               ▼
         TopoSwarmBridge    ReactiveEngine
         route(goal)        analyse(output)
                │               │
                ▼               │
         LazyOwn PTY ───────────┘
         execute tool
                │
                ▼
         StateTracker
         (discoveries, creds, phase)
                │
                ▼
         next goal decided

Phase sequence
--------------
  0. INIT       — session init, set rhost/lhost from payload.json
  1. RECON      — port scan (lazynmap), web probe, fingerprint OS
  2. ENUM       — service-specific enum (SMB, LDAP, web dirs, etc.)
  3. VULN       — searchsploit + CVE analysis on discovered services
  4. EXPLOIT    — attempt exploitation of best candidate vuln
  5. POST       — credential dump, privesc, persistence
  6. LATERAL    — move to adjacent hosts if creds found
  7. REPORT     — generate final report + MISP export

Usage
-----
  python3 skills/toposwarm_autonomous.py [OPTIONS]

  Options:
    --rhost IP          Target IP (overrides payload.json)
    --lhost IP          Listener IP (overrides payload.json)
    --objective TEXT    High-level goal (default: "compromise the target")
    --max-steps N       Max actions per phase (default: 5)
    --max-phases N      Max phases to run (default: 7 = all)
    --no-model          Use keyword routing only (no GPU needed)
    --phase PHASE       Start from specific phase (0-7)
    --verbose           Print full tool output
    --json-out FILE     Write structured results to JSON file
    --effort low|med|high|max  How hard to try (default: high)

Author: Gris Iscomeback — GPL v3
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Paths ──────────────────────────────────────────────────────────────────────

_SKILLS_DIR   = Path(__file__).resolve().parent
_LAZYOWN_DIR  = _SKILLS_DIR.parent
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"
_MODULES_DIR  = _LAZYOWN_DIR / "modules"
_PAYLOAD_FILE = _LAZYOWN_DIR / "payload.json"

for _p in [str(_MODULES_DIR), str(_SKILLS_DIR)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Logging ────────────────────────────────────────────────────────────────────

_LOG_FILE = _SESSIONS_DIR / "toposwarm_autonomous.log"
_SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(_LOG_FILE), encoding="utf-8"),
    ],
)
log = logging.getLogger("toposwarm_auto")

# ANSI colours for terminal output
_R    = "\033[91m"
_G    = "\033[92m"
_Y    = "\033[93m"
_B    = "\033[94m"
_M    = "\033[95m"
_C    = "\033[96m"
_W    = "\033[97m"
_X    = "\033[0m"
_BOLD = "\033[1m"


# ── Phases ─────────────────────────────────────────────────────────────────────

PHASES = [
    (0, "INIT",    "Initialize session and configure target from payload.json"),
    (1, "RECON",   "Port scan, OS fingerprint, service detection on {rhost}"),
    (2, "ENUM",    "Enumerate discovered services on {rhost} in depth"),
    (3, "VULN",    "Search exploits and analyze CVEs for {rhost} services"),
    (4, "EXPLOIT", "Exploit best vulnerability found on {rhost}"),
    (5, "POST",    "Dump credentials, escalate privileges, establish persistence on {rhost}"),
    (6, "LATERAL", "Move laterally using captured credentials"),
    (7, "REPORT",  "Generate final pentest report and export findings"),
]

EFFORT_STEPS = {"low": 2, "med": 3, "medium": 3, "high": 5, "max": 8}


# ── State tracker ──────────────────────────────────────────────────────────────

@dataclass
class PentestState:
    """Tracks everything discovered during the autonomous run."""
    rhost:        str  = ""
    lhost:        str  = ""
    domain:       str  = ""
    target_os:    str  = "unknown"
    open_ports:   List[str] = field(default_factory=list)
    services:     List[str] = field(default_factory=list)
    credentials:  List[str] = field(default_factory=list)
    shells:       List[str] = field(default_factory=list)
    vulns:        List[str] = field(default_factory=list)
    findings:     List[str] = field(default_factory=list)
    phase_log:    Dict[str, List[str]] = field(default_factory=dict)
    start_time:   str  = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    phase:        int  = 0
    goal_achieved: bool = False

    def add_finding(self, phase_name: str, text: str) -> None:
        self.findings.append(f"[{phase_name}] {text}")
        self.phase_log.setdefault(phase_name, []).append(text)

    def summary(self) -> str:
        lines = [
            f"Target      : {self.rhost}  OS={self.target_os}",
            f"Open ports  : {', '.join(self.open_ports) or 'none yet'}",
            f"Services    : {', '.join(self.services[:8]) or 'none yet'}",
            f"Credentials : {len(self.credentials)} captured",
            f"Shells      : {len(self.shells)} active",
            f"Vulns       : {len(self.vulns)} identified",
        ]
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rhost": self.rhost, "lhost": self.lhost,
            "target_os": self.target_os,
            "open_ports": self.open_ports,
            "services": self.services,
            "credentials": self.credentials,
            "shells": self.shells,
            "vulns": self.vulns,
            "findings": self.findings,
            "start_time": self.start_time,
            "end_time": datetime.now(timezone.utc).isoformat(),
            "phases_completed": self.phase,
            "goal_achieved": self.goal_achieved,
        }


# ── Output parser ──────────────────────────────────────────────────────────────

def _parse_output(output: str, state: PentestState, phase_name: str) -> None:
    """Extract discovered information from tool output and update state."""
    low = output.lower()

    # Ports
    for m in re.finditer(r"(\d{1,5})/tcp\s+open\s+(\S+)", output, re.IGNORECASE):
        port_svc = f"{m.group(1)}/{m.group(2)}"
        if port_svc not in state.open_ports:
            state.open_ports.append(port_svc)
        if m.group(2) not in state.services:
            state.services.append(m.group(2))

    # OS
    for pat, os_name in [
        (r"windows", "windows"), (r"linux", "linux"), (r"ubuntu", "linux"),
        (r"debian", "linux"), (r"centos", "linux"), (r"freebsd", "bsd"),
    ]:
        if re.search(pat, low) and state.target_os == "unknown":
            state.target_os = os_name
            break

    # Credentials
    for m in re.finditer(
        r"(?:username|user|login)[:\s]+(\S+)[,\s]+(?:password|pass|pwd)[:\s]+(\S+)",
        low, re.IGNORECASE
    ):
        cred = f"{m.group(1)}:{m.group(2)}"
        if cred not in state.credentials:
            state.credentials.append(cred)
            state.add_finding(phase_name, f"Credential found: {cred}")

    # Shell / RCE
    for sig in ("shell", "command execution", "rce", "root@", "# ", "$ "):
        if sig in low:
            if not state.shells:
                state.add_finding(phase_name, f"Possible shell/RCE: {output[:80]}")
                state.shells.append(output[:80])
            break

    # Vulns / CVE
    for m in re.finditer(r"CVE-\d{4}-\d{4,}", output, re.IGNORECASE):
        if m.group(0) not in state.vulns:
            state.vulns.append(m.group(0))
            state.add_finding(phase_name, f"CVE: {m.group(0)}")


# ── Phase goals ────────────────────────────────────────────────────────────────

def _phase_goals(phase_idx: int, state: PentestState, effort: str) -> List[str]:
    """Return ordered list of NL goals to attempt in this phase."""
    rhost  = state.rhost
    domain = state.domain or rhost
    ports  = ", ".join(state.open_ports[:6]) or "unknown"
    svcs   = ", ".join(state.services[:6]) or "unknown services"
    creds  = state.credentials[0] if state.credentials else ""

    goals = {
        0: [
            "Initialize session and show situation report",
            f"Set target host to {rhost}",
            f"Set listener host to {state.lhost}",
        ],
        1: [
            f"Scan open ports on {rhost}",
            f"Run web fingerprint on {rhost}",
            f"Enumerate services on {rhost}",
        ],
        2: _enum_goals(state),
        3: [
            f"Search exploits for discovered services: {svcs} on {rhost}",
            f"Analyze vulnerabilities on {rhost}",
            f"CVE analysis for services: {svcs}",
        ],
        4: [
            f"Exploit the best vulnerability found on {rhost} with services: {svcs}",
            f"Run red team operation plan for {rhost}",
            f"Generate exploit script for {rhost} vulnerabilities: {state.vulns[:3]}",
        ],
        5: [
            f"Dump all credentials from {rhost}",
            f"Show captured credentials",
            f"Escalate privileges on {rhost}",
            f"Establish persistence on {rhost}",
        ],
        6: [
            f"Move laterally using credentials: {creds or 'captured creds'}",
            f"Spawn hive drones to enumerate adjacent hosts",
            f"Use captured credentials to expand access in {domain}",
        ],
        7: [
            "Generate full pentest report",
            "Show attack timeline",
            "Show campaign situation report",
            "Export findings to MISP",
        ],
    }
    g = goals.get(phase_idx, [f"Advance towards compromising {rhost}"])
    max_g = EFFORT_STEPS.get(effort, 5)
    return g[:max_g]


def _enum_goals(state: PentestState) -> List[str]:
    """Build enumeration goals based on discovered services."""
    goals = []
    svc_lower = [s.lower() for s in state.services]
    rhost = state.rhost

    if any(s in svc_lower for s in ("smb", "microsoft-ds", "netbios")):
        goals.append(f"Enumerate SMB shares on {rhost}")
    if any(s in svc_lower for s in ("http", "https", "www", "apache", "nginx")):
        goals.append(f"Enumerate web directories on {rhost}")
    if any(s in svc_lower for s in ("ldap", "msrpc", "kerberos")):
        goals.append(f"Enumerate Active Directory on {rhost}")
    if "ftp" in svc_lower:
        goals.append(f"Enumerate FTP on {rhost}")
    if not goals:
        goals.append(f"Enumerate all discovered services on {rhost}: {', '.join(state.services[:5])}")
    goals.append(f"What should I do after scanning {rhost}?")
    return goals


# ── Autonomous agent ───────────────────────────────────────────────────────────

class AutonomousAgent:
    def __init__(
        self,
        state:      PentestState,
        no_model:   bool = False,
        verbose:    bool = False,
        effort:     str  = "high",
        max_phases: int  = 8,
        json_out:   Optional[Path] = None,
    ) -> None:
        self.state      = state
        self.no_model   = no_model
        self.verbose    = verbose
        self.effort     = effort
        self.max_phases = max_phases
        self.json_out   = json_out

        # Lazy-import bridge
        try:
            from toposwarm_bridge import get_bridge
            self.bridge = get_bridge()
            if not no_model:
                self.bridge._try_load()
        except ImportError:
            log.error("toposwarm_bridge not found — ensure TOPOSWARM_DIR is set")
            sys.exit(1)

        # Optional reactive engine for signal parsing
        try:
            from reactive_engine import ReactiveEngine
            self.reactive = ReactiveEngine()
        except ImportError:
            self.reactive = None

    # ── Execution helpers ──────────────────────────────────────────────────────

    def _execute_goal(self, goal: str, phase_name: str) -> str:
        """Route a NL goal and execute it via the orchestrator."""
        routed = self.bridge.route(goal)
        log.info("  %s→%s %s%s  (conf=%.2f, %s)%s",
                 _C, _X, routed.tool_name, _X, routed.confidence, routed.backend, _X)

        output = self.bridge.execute_via_orchestrator(
            goal, no_model=self.no_model
        )

        if self.verbose:
            print(f"\n{_Y}{'─'*60}{_X}")
            print(output[:2000])
            print(f"{_Y}{'─'*60}{_X}\n")
        else:
            # Print first meaningful line
            first = next(
                (l.strip() for l in output.splitlines() if l.strip()
                 and not l.startswith("2026") and not l.startswith("INFO")),
                output[:120],
            )
            log.info("  └─ %s", first[:120])

        _parse_output(output, self.state, phase_name)

        # React to signals if reactive engine available
        if self.reactive:
            try:
                decisions = self.reactive.analyse(output)
                for d in (decisions or []):
                    if d.command:
                        log.info("  %s[reactive]%s %s → %s",
                                 _M, _X, d.reason[:60], d.command[:60])
            except Exception:
                pass

        return output

    # ── Phase runners ──────────────────────────────────────────────────────────

    def _run_phase(self, phase_idx: int) -> bool:
        """Run one phase. Returns True if we should continue to next phase."""
        _num, name, desc_tmpl = PHASES[phase_idx]
        desc = desc_tmpl.format(rhost=self.state.rhost)

        print(f"\n{_BOLD}{_B}{'═'*70}{_X}")
        print(f"{_BOLD}{_B}  PHASE {phase_idx}: {name}  —  {desc}{_X}")
        print(f"{_BOLD}{_B}{'═'*70}{_X}\n")

        goals = _phase_goals(phase_idx, self.state, self.effort)
        for i, goal in enumerate(goals, 1):
            log.info("%s[%s %d/%d]%s %s", _G, name, i, len(goals), _X, goal)
            try:
                self._execute_goal(goal, name)
            except KeyboardInterrupt:
                log.info("Interrupted — stopping phase %s", name)
                return False
            except Exception as exc:
                log.warning("Goal failed: %s — %s", goal[:60], exc)
            time.sleep(0.5)

        # Check for early completion signals
        if phase_idx >= 4 and self.state.shells:
            log.info("%s[!] Shell detected — goal achieved at phase %s!%s",
                     _G, name, _X)
            self.state.goal_achieved = True

        self.state.phase = phase_idx + 1
        self._save_state()
        return True

    # ── State persistence ──────────────────────────────────────────────────────

    def _save_state(self) -> None:
        state_file = _SESSIONS_DIR / f"toposwarm_state_{self.state.rhost}.json"
        try:
            state_file.write_text(
                json.dumps(self.state.to_dict(), indent=2, ensure_ascii=False)
            )
        except Exception:
            pass
        if self.json_out:
            try:
                self.json_out.write_text(
                    json.dumps(self.state.to_dict(), indent=2, ensure_ascii=False)
                )
            except Exception:
                pass

    # ── Main loop ──────────────────────────────────────────────────────────────

    def run(self, start_phase: int = 0) -> PentestState:
        print(f"\n{_BOLD}{_R}{'╔' + '═'*68 + '╗'}{_X}")
        print(f"{_BOLD}{_R}║  TopoSwarm Autonomous Red Team Agent{' '*31}║{_X}")
        print(f"{_BOLD}{_R}║  Target: {self.state.rhost:<58}║{_X}")
        print(f"{_BOLD}{_R}║  Model:  {'neural+keyword' if self.bridge.model_loaded else 'keyword-only':<56}║{_X}")
        print(f"{_BOLD}{_R}║  Effort: {self.effort:<58}║{_X}")
        print(f"{_BOLD}{_R}{'╚' + '═'*68 + '╝'}{_X}\n")

        log.info("Starting autonomous run — target=%s  phases=%d  effort=%s",
                 self.state.rhost, self.max_phases, self.effort)

        for phase_idx in range(start_phase, min(self.max_phases, len(PHASES))):
            ok = self._run_phase(phase_idx)
            if not ok:
                log.info("Stopping at phase %d on user interrupt", phase_idx)
                break
            if self.state.goal_achieved:
                log.info("%sGoal achieved at phase %d!%s", _G, phase_idx, _X)
                # Still run report phase if not already there
                if phase_idx < 7:
                    self._run_phase(7)
                break

        print(f"\n{_BOLD}{_G}{'═'*70}{_X}")
        print(f"{_BOLD}{_G}  AUTONOMOUS RUN COMPLETE{_X}")
        print(f"{_BOLD}{_G}{'═'*70}{_X}")
        print(self.state.summary())

        if self.state.credentials:
            print(f"\n{_Y}Credentials captured:{_X}")
            for c in self.state.credentials:
                print(f"  {_G}✓{_X} {c}")

        if self.state.vulns:
            print(f"\n{_Y}Vulnerabilities identified:{_X}")
            for v in self.state.vulns[:10]:
                print(f"  {_R}!{_X} {v}")

        self._save_state()
        log.info("State saved to sessions/toposwarm_state_%s.json", self.state.rhost)
        return self.state


# ── CLI ────────────────────────────────────────────────────────────────────────

def _load_payload() -> Dict[str, Any]:
    """Load payload.json from LazyOwn root."""
    if _PAYLOAD_FILE.exists():
        try:
            return json.loads(_PAYLOAD_FILE.read_text())
        except Exception:
            pass
    return {}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="TopoSwarm Autonomous Red Team Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--rhost",      type=str, default="",
                        help="Target IP (default: from payload.json)")
    parser.add_argument("--lhost",      type=str, default="",
                        help="Listener IP (default: from payload.json)")
    parser.add_argument("--domain",     type=str, default="",
                        help="Target domain")
    parser.add_argument("--objective",  type=str,
                        default="compromise the target and achieve domain admin or root",
                        help="High-level attack objective")
    parser.add_argument("--max-phases", type=int, default=8,
                        help="Max phases to run 0-7 (default: 8=all)")
    parser.add_argument("--phase",      type=int, default=0,
                        help="Start at phase N (0=INIT)")
    parser.add_argument("--effort",     type=str, default="high",
                        choices=["low", "med", "medium", "high", "max"],
                        help="Effort level — controls steps per phase")
    parser.add_argument("--no-model",   action="store_true",
                        help="Use keyword routing only (no GPU/model needed)")
    parser.add_argument("--verbose",    action="store_true",
                        help="Print full tool output")
    parser.add_argument("--json-out",   type=str, default="",
                        help="Write structured results to JSON file")

    args = parser.parse_args(argv)

    # Load payload.json defaults
    payload = _load_payload()
    rhost  = args.rhost  or payload.get("rhost", "")
    lhost  = args.lhost  or payload.get("lhost", "")
    domain = args.domain or payload.get("domain", "")

    if not rhost:
        log.error("No target: set rhost in payload.json or pass --rhost")
        return 1

    state = PentestState(rhost=rhost, lhost=lhost, domain=domain)

    agent = AutonomousAgent(
        state      = state,
        no_model   = args.no_model,
        verbose    = args.verbose,
        effort     = args.effort,
        max_phases = args.max_phases,
        json_out   = Path(args.json_out) if args.json_out else None,
    )

    try:
        agent.run(start_phase=args.phase)
    except KeyboardInterrupt:
        log.info("Run interrupted by user")
        agent._save_state()

    return 0 if state.goal_achieved else 2


if __name__ == "__main__":
    sys.exit(main())
