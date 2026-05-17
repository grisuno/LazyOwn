#!/usr/bin/env python3
"""
skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
==================================================================
Bridges LazyOwn (Claude-assisted orchestrator) and a fully autonomous
OpenClaw/OpenHands-style system.

The daemon runs as an independent process and does NOT need Claude Code
to operate between objectives. Claude remains the Borg Queen for injecting
high-level objectives, but the daemon executes them without intervention.

Architecture (4 concurrent asyncio roles)
------------------------------------------
  Role 1 — ObjectiveLoop    : Watches objectives.jsonl. When a pending
                              objective appears, takes it, plans, executes.
  Role 2 — ExecutionEngine  : Per-step execution loop (equivalent to
                              auto_loop in MCP but without MCP). Uses the
                              same command selection cascade:
                              reactive -> parquet -> bridge -> LLM -> fallback
  Role 3 — WorldModelWatcher: Watches world_model.json. When the phase
                              changes (recon->enum->exploit...) or new
                              hosts/credentials appear, injects derived
                              objectives and notifies hive drones.
  Role 4 — DroneCoordinator : Hive-mind bridge. When recon discovers a
                              host, launches exploit/analyze drones in
                              parallel. When a drone finishes, writes the
                              result to the stream and updates the objective.

Event streams (push, no polling)
----------------------------------
  sessions/autonomous_events.jsonl  — every action, finding, decision
  sessions/autonomous_status.json   — real-time daemon state

Management
-----------
  python3 skills/autonomous_daemon.py start   # fork and detach
  python3 skills/autonomous_daemon.py stop    # terminate by PID
  python3 skills/autonomous_daemon.py run     # foreground (debug)
  python3 skills/autonomous_daemon.py status  # read state
  python3 skills/autonomous_daemon.py inject "Objective" [--priority high]

MCP integration
----------------
  lazyown_autonomous_start(max_steps_per_objective=10, backend="groq")
  lazyown_autonomous_stop()
  lazyown_autonomous_status()
  lazyown_autonomous_inject(text, priority)
"""

from __future__ import annotations

import asyncio
import datetime
import json
import logging
import os
import re
import signal
import subprocess
import sys
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Paths ──────────────────────────────────────────────────────────────────────

SKILLS_DIR   = Path(__file__).parent
LAZYOWN_DIR  = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
MODULES_DIR  = LAZYOWN_DIR / "modules"
SESSIONS_DIR = LAZYOWN_DIR / "sessions"
PAYLOAD_FILE = LAZYOWN_DIR / "payload.json"

for _p in (str(SKILLS_DIR), str(MODULES_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── State files ────────────────────────────────────────────────────────────────

PID_FILE    = SESSIONS_DIR / "autonomous_daemon.pid"
STATUS_FILE = SESSIONS_DIR / "autonomous_status.json"
EVENTS_FILE = SESSIONS_DIR / "autonomous_events.jsonl"
TASKS_FILE  = SESSIONS_DIR / "tasks.json"

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="[auto] %(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("autonomous_daemon")

# ── Config (env-overridable) ──────────────────────────────────────────────────

OBJ_POLL_S          = float(os.environ.get("AUTO_OBJ_POLL",      "5"))
WM_POLL_S           = float(os.environ.get("AUTO_WM_POLL",       "8"))
STEP_TIMEOUT_S      = int(os.environ.get("AUTO_STEP_TIMEOUT",    "60"))
STEP_DELAY_S        = float(os.environ.get("AUTO_STEP_DELAY",    "3"))
MAX_STEPS_DEFAULT   = int(os.environ.get("AUTO_MAX_STEPS",       "10"))
MAX_FAILS_PER_CMD   = int(os.environ.get("AUTO_MAX_FAILS",       "2"))
HIVE_BACKEND        = os.environ.get("AUTO_HIVE_BACKEND",        "groq")
HIVE_MAX_ITER       = int(os.environ.get("AUTO_HIVE_MAX_ITER",   "8"))
HEARTBEAT_S         = float(os.environ.get("AUTO_HEARTBEAT",     "30"))
BLOCKED_ESCALATE_N  = int(os.environ.get("AUTO_BLOCKED_ESCALATE","2"))

# ── Optional imports ──────────────────────────────────────────────────────────

def _try_import(module: str, attr: str = ""):
    try:
        m = __import__(module, fromlist=[attr] if attr else [])
        return getattr(m, attr) if attr else m
    except Exception as e:
        log.debug("optional import failed %s.%s: %s", module, attr, e)
        return None

_ObjectiveStore = _try_import("lazyown_objective", "ObjectiveStore")
_PolicyInteg    = _try_import("lazyown_policy",    "LazyOwnPolicyIntegration")
_FactStore      = _try_import("lazyown_facts",     "FactStore")
_get_pdb        = _try_import("lazyown_parquet_db","get_pdb")
_get_dispatcher = _try_import("lazyown_bridge",    "get_dispatcher") if _try_import("lazyown_bridge") else None
_get_hive       = _try_import("hive_mind",         "get_hive")

_WorldModel     = None
_ObsParser      = None
_ReactEngine    = None
try:
    from world_model import WorldModel as _WorldModel       # type: ignore[assignment]
    from obs_parser  import ObsParser  as _ObsParser        # type: ignore[assignment]
    from reactive_engine import get_engine as _ReactEngine  # type: ignore[assignment]
except Exception as _e:
    log.debug("world_model/obs_parser/reactive_engine not available: %s", _e)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — Event Stream (real-time push)
# ─────────────────────────────────────────────────────────────────────────────

_stream_lock = threading.Lock()
_tasks_lock  = threading.Lock()


def _update_task_status(title: str, new_status: str) -> bool:
    """Update the status of the first task whose title matches. Thread-safe."""
    with _tasks_lock:
        try:
            if not TASKS_FILE.exists():
                return False
            tasks   = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
            changed = False
            for t in tasks:
                if t.get("title", "")[:80] == title[:80]:
                    t["status"] = new_status
                    changed     = True
                    break
            if changed:
                TASKS_FILE.write_text(
                    json.dumps(tasks, indent=4, ensure_ascii=False), encoding="utf-8"
                )
            return changed
        except Exception as exc:
            log.debug("task status update error: %s", exc)
            return False


def _inject_to_tasks_json(
    title: str,
    description: str = "",
    operator: str = "autonomous_daemon",
    status: str = "New",
) -> int:
    """
    Write directly to sessions/tasks.json using the C2 format (lazyc2.py).
    Returns the assigned id. Thread-safe.
    """
    with _tasks_lock:
        try:
            SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
            if TASKS_FILE.exists():
                try:
                    tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
                    if not isinstance(tasks, list):
                        tasks = []
                except Exception:
                    tasks = []
            else:
                tasks = []

            new_id = len(tasks)
            tasks.append({
                "id":          new_id,
                "title":       title[:200],
                "description": description[:1000],
                "operator":    operator,
                "status":      status,
            })
            TASKS_FILE.write_text(
                json.dumps(tasks, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )
            return new_id
        except Exception as exc:
            log.warning("tasks.json write error: %s", exc)
            return -1


def _emit(event_type: str, payload: Dict[str, Any], severity: str = "info") -> None:
    """Write an event to the JSONL stream. Thread-safe."""
    event = {
        "id":       uuid.uuid4().hex[:8],
        "ts":       datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "type":     event_type,
        "severity": severity,
        "payload":  payload,
    }
    line = json.dumps(event, ensure_ascii=False, default=str)
    with _stream_lock:
        try:
            SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
            with EVENTS_FILE.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except Exception as exc:
            log.warning("emit error: %s", exc)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — ICommandRunner + concrete implementations
#             (S — Single Responsibility, D — Dependency Inversion)
# ─────────────────────────────────────────────────────────────────────────────

class ICommandRunner(ABC):
    """Contract for executing a LazyOwn shell command."""

    @abstractmethod
    def run(self, command: str, timeout: int) -> str:
        """Execute command within timeout seconds. Return text output."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier for this runner."""


class MCPCommandRunner(ICommandRunner):
    """
    Delegates to lazyown_mcp._run_lazyown_command when available.
    Single Responsibility: MCP import + delegation only.
    """

    @property
    def name(self) -> str:
        return "mcp"

    def run(self, command: str, timeout: int = STEP_TIMEOUT_S) -> str:
        """Try to import and call the MCP runner. Raises ImportError on failure."""
        from lazyown_mcp import _run_lazyown_command
        return _run_lazyown_command(command, timeout)


class PTYCommandRunner(ICommandRunner):
    """
    Full PTY-based command execution that mirrors _run_lazyown_command in the MCP
    but has no dependency on lazyown_mcp.
    Single Responsibility: PTY subprocess management only.
    """

    @property
    def name(self) -> str:
        return "pty"

    def run(self, command: str, timeout: int = STEP_TIMEOUT_S) -> str:
        """Execute command via PTY. Returns cleaned text output."""
        import fcntl
        import pty
        import re
        import select
        import struct
        import termios

        cmd_input   = (command.strip() + "\nexit\n").encode()
        run_script  = LAZYOWN_DIR / "run"
        argv = (
            ["bash", str(run_script)]
            if run_script.is_file()
            else [sys.executable, "-W", "ignore", str(LAZYOWN_DIR / "lazyown.py")]
        )

        env       = os.environ.copy()
        env["TERM"] = "xterm-256color"

        master_fd, slave_fd = pty.openpty()
        winsize = struct.pack("HHHH", 50, 220, 0, 0)
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsize)

        try:
            proc = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE,
                stdout=slave_fd,
                stderr=slave_fd,
                env=env,
                cwd=str(LAZYOWN_DIR),
                start_new_session=True,
            )
            os.close(slave_fd)
            try:
                proc.stdin.write(cmd_input)
                proc.stdin.close()
            except BrokenPipeError:
                pass

            chunks: list = []
            deadline = time.monotonic() + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    proc.kill()
                    os.close(master_fd)
                    return f"[timeout] {command} exceeded {timeout}s"
                r, _, _ = select.select([master_fd], [], [], min(remaining, 0.5))
                if r:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            chunks.append(data.decode("utf-8", errors="replace"))
                        else:
                            break
                    except OSError:
                        break
                if proc.poll() is not None and not r:
                    break

            proc.wait(timeout=2)
            try:
                os.close(master_fd)
            except OSError:
                pass

            raw = "".join(chunks)
            return re.sub(r"\x1b\[[0-9;]*[mGKH]", "", raw).strip()

        except Exception as exc:
            return f"[run error] {exc}"


class CommandRunnerChain(ICommandRunner):
    """
    Tries each runner in order and returns the first successful result.
    Falls back to the next runner on any exception.

    Chain of Responsibility pattern.
    Open/Closed: add new runners without modifying this class.
    """

    def __init__(self, runners: List[ICommandRunner]) -> None:
        if not runners:
            raise ValueError("CommandRunnerChain requires at least one runner")
        self._runners = runners

    @property
    def name(self) -> str:
        return "chain[" + ",".join(r.name for r in self._runners) + "]"

    def run(self, command: str, timeout: int = STEP_TIMEOUT_S) -> str:
        """Try each runner in sequence. Return first successful output."""
        last_exc: Optional[Exception] = None
        for runner in self._runners:
            try:
                return runner.run(command, timeout)
            except Exception as exc:
                log.debug("runner %s failed: %s", runner.name, exc)
                last_exc = exc
        raise RuntimeError(f"All runners failed. Last: {last_exc}") from last_exc


def _build_default_runner() -> ICommandRunner:
    """Return the default CommandRunnerChain (MCP -> PTY fallback)."""
    return CommandRunnerChain([MCPCommandRunner(), PTYCommandRunner()])


# Module-level runner instance used by StrategyEngine / ExecutionEngine
_default_runner: ICommandRunner = _build_default_runner()


def _run_lazyown(command: str, timeout: int = STEP_TIMEOUT_S) -> str:
    """
    Execute a LazyOwn command using the default runner chain.
    Preserved as a module-level function for backward compatibility.
    """
    return _default_runner.run(command, timeout)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — ICommandSelector + implementations
#             (S — Single Responsibility, Chain of Responsibility)
# ─────────────────────────────────────────────────────────────────────────────

# Static fallback maps: category -> command name, split by OS platform.
# The OS-specific maps are consulted first; _FALLBACK_MAP is the baseline.
_FALLBACK_MAP: Dict[str, str] = {
    "recon":       "lazynmap",
    "enum":        "enum_smb",
    "brute_force": "crackmapexec",
    "exploit":     "searchsploit",
    "intrusion":   "evil-winrm",
    "privesc":     "linpeas",
    "credential":  "secretsdump",
    "lateral":     "crackmapexec",
    "other":       "list",
}

_FALLBACK_MAP_LINUX: Dict[str, str] = {
    "privesc":    "linpeas",
    "intrusion":  "ssh",
    "credential": "secretsdump",
}

_FALLBACK_MAP_WINDOWS: Dict[str, str] = {
    "privesc":    "winpeas",
    "intrusion":  "evil-winrm",
    "credential": "secretsdump",
    "enum":       "enum_smb",
}

# Phase -> applicable categories in priority order
_PHASE_CATEGORIES: Dict[str, List[str]] = {
    "recon":   ["recon"],
    "enum":    ["enum", "recon"],
    "exploit": ["exploit", "intrusion", "brute_force"],
    "privesc": ["privesc", "credential"],
    "lateral": ["lateral", "credential"],
    "report":  ["other"],
}


@dataclass
class CommandDecision:
    """Result of a command selection."""
    command:  str
    args:     str = ""
    source:   str = "fallback"   # reactive|parquet|bridge|llm|fallback
    reason:   str = ""
    mitre:    str = ""
    priority: int = 5


class ICommandSelector(ABC):
    """Contract for command selection strategies."""

    @abstractmethod
    def select(
        self,
        target: str,
        phase: str,
        context: Dict,
    ) -> Optional[CommandDecision]:
        """Return a CommandDecision or None if this selector has no suggestion."""


class ReactiveSelector(ICommandSelector):
    """
    Returns a pending reactive engine decision if one is available.
    Single Responsibility: reactive engine integration only.
    """

    def __init__(self, reactive_engine: Any) -> None:
        self._engine  = reactive_engine
        self._pending: Optional[CommandDecision] = None

    def register_output(
        self,
        output: str,
        command: str,
        platform: str = "linux",
    ) -> None:
        """Feed reactive engine with last command output to generate new decisions."""
        if self._engine is None:
            return
        try:
            decisions = self._engine.analyse(
                output=output, command=command, platform=platform,
            )
            if decisions:
                top = decisions[0]
                if top.priority <= 2:
                    self._pending = CommandDecision(
                        command=top.command,
                        source="reactive",
                        reason=top.reason,
                        priority=top.priority,
                    )
        except Exception as exc:
            log.debug("reactive engine error: %s", exc)

    def select(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        """Pop and return the pending reactive decision if present."""
        if self._pending:
            dec           = self._pending
            self._pending = None
            return dec
        return None


class ParquetSelector(ICommandSelector):
    """
    Queries Parquet DB for commands that succeeded in past sessions.
    Single Responsibility: Parquet history lookup only.
    """

    def __init__(self, pdb: Any, fail_counts: Dict[str, int]) -> None:
        self._pdb         = pdb
        self._fail_counts = fail_counts

    def select(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        """Return the most-frequent successful command for this phase."""
        categories = _PHASE_CATEGORIES.get(phase, ["other"])
        for cat in categories:
            cand = self._parquet_candidate(cat, target)
            if cand:
                return CommandDecision(
                    command=cand,
                    source="parquet",
                    reason=f"past success in {cat}",
                )
        return None

    def _parquet_candidate(self, category: str, target: str) -> Optional[str]:
        if self._pdb is None:
            return None
        try:
            rows = self._pdb.query_session(
                phase=category, target=target, success_only=True, limit=30
            )
            blacklist = _get_campaign_blacklist()
            # Commands blacklisted under this category or globally
            blocked = set(blacklist.get(category, []) + blacklist.get("any", []))
            freq: Dict[str, int] = {}
            for r in rows:
                cmd = (r.get("command") or "").strip().split()[0]
                if not cmd or cmd.startswith("/") or cmd.startswith("echo"):
                    continue
                if self._fail_counts.get(cmd, 0) >= MAX_FAILS_PER_CMD:
                    continue
                if cmd in blocked:
                    continue
                freq[cmd] = freq.get(cmd, 0) + 1
            return max(freq, key=lambda c: freq[c]) if freq else None
        except Exception:
            return None


class BridgeSelector(ICommandSelector):
    """
    Queries the lazyown_bridge catalog for phase/service-appropriate commands.
    Single Responsibility: bridge catalog lookup only.
    """

    def __init__(self, dispatcher: Any, fail_counts: Dict[str, int]) -> None:
        self._dispatcher  = dispatcher
        self._fail_counts = fail_counts

    def select(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        """Return a bridge catalog suggestion for this phase."""
        categories = _PHASE_CATEGORIES.get(phase, ["other"])
        services   = context.get("services", [])
        os_hint    = context.get("os_hint", "any")
        for cat in categories:
            cand = self._bridge_candidate(phase, services, cat, os_hint=os_hint)
            if cand:
                return cand
        return None

    def _bridge_candidate(
        self, phase: str, services: List[str], tag: str = "", os_hint: str = "any"
    ) -> Optional[CommandDecision]:
        if self._dispatcher is None:
            return None
        try:
            result = self._dispatcher.suggest(
                phase=phase, services=services, tag_hint=tag, os_hint=os_hint,
            )
            if result is None:
                return None
            cmd_str, entry = result
            cmd_name = cmd_str.split()[0]
            if self._fail_counts.get(cmd_name, 0) >= MAX_FAILS_PER_CMD:
                return None
            return CommandDecision(
                command=cmd_str,
                source="bridge",
                reason=f"bridge catalog — {entry.description[:60]}",
                mitre=entry.mitre_tactic,
                priority=3,
            )
        except Exception:
            return None


def _get_phase_command_catalog(phase: str) -> str:
    """
    Return a compact string listing available LazyOwn commands for the given phase.
    Used to inject command context into LLM/SWAN prompts so they pick valid abstractions.
    """
    try:
        _disp = _get_dispatcher() if _get_dispatcher else None
        if _disp is None:
            return ""
        dispatcher = _disp()
        entries = dispatcher.list_phase(phase)
        if not entries:
            return ""
        names = [e.command for e in entries[:40]]          # cap at 40
        return ", ".join(names)
    except Exception:
        return ""


class LLMSelector(ICommandSelector):
    """
    Queries Groq/Ollama for a command suggestion.
    Only active when AUTO_USE_LLM=1.
    Single Responsibility: LLM command recommendation only.
    """

    def select(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        """Return an LLM-suggested command with catalog context, or None if disabled."""
        if os.environ.get("AUTO_USE_LLM", "0") != "1":
            return None
        return self._llm_candidate(target, phase, context)

    def _llm_candidate(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        try:
            from lazyown_llm import LLMBridge
            payload  = _load_payload()
            api_key  = payload.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
            if not api_key:
                return None
            bridge   = LLMBridge(backend="groq", api_key=api_key)
            catalog  = _get_phase_command_catalog(phase)
            services = context.get("services", [])
            os_hint  = context.get("os_hint", "unknown")
            has_creds = bool(payload.get("start_pass") or payload.get("start_user"))

            # Recent session history for context
            recent_cmds = _read_recent_csv_commands(limit=3)
            recent_line = (
                f"Recently executed: {', '.join(recent_cmds)}\n" if recent_cmds else ""
            )

            # World model context
            wm_line = ""
            wm_file = SESSIONS_DIR / "world_model.json"
            if wm_file.exists():
                try:
                    wm = json.loads(wm_file.read_text())
                    wm_hosts = list(wm.get("hosts", {}).keys())[:3]
                    wm_creds = len(wm.get("credentials", []))
                    wm_vulns = len(wm.get("vulnerabilities", []))
                    wm_line = (
                        f"World model: known_hosts={wm_hosts} creds={wm_creds} vulns={wm_vulns}\n"
                    )
                except Exception:
                    pass

            catalog_line = (
                f"Available LazyOwn commands for phase '{phase}': {catalog}\n"
                if catalog else ""
            )
            goal = (
                f"{catalog_line}"
                f"CRITICAL: These are HIGH-LEVEL ABSTRACTIONS. payload.json auto-injects rhost/domain/creds/wordlist. "
                f"Never write raw tool flags — just the command name.\n"
                f"Target: {target} | OS: {os_hint} | Services: {services[:5]} | Has-creds: {has_creds}\n"
                f"{recent_line}"
                f"{wm_line}"
                f"Suggest the BEST SINGLE command for phase='{phase}' that has NOT been recently executed. "
                f"Reply with ONLY the command name (one word). No explanation."
            )
            answer = bridge.ask(goal=goal, max_iterations=1)
            cmd = answer.strip().split()[0] if answer.strip() else None
            if cmd and len(cmd) < 50:
                return CommandDecision(
                    command=cmd, source="llm",
                    reason=f"LLM recommendation (catalog={bool(catalog)})", priority=4,
                )
        except Exception as exc:
            log.debug("LLM candidate error: %s", exc)
        return None


class SWANSelector(ICommandSelector):
    """
    SWAN (Scalable Weighted Adaptive Network) command selector.

    Routes the command-recommendation query to the best MoE expert via
    Q-learning-guided routing.  Only active when AUTO_USE_SWAN=1.

    Single Responsibility : MoE/RL expert routing only — no direct execution.
    Open/Closed           : Extend SwanOrchestrator subclasses; this selector
                            never changes to support new experts.
    Dependency Inversion  : depends on ICommandSelector interface; imports
                            swan_agent lazily so the daemon starts even without
                            GROQ_API_KEY present.
    """

    # Mapping from LazyOwn daemon phase names → SWAN task_type strings
    _PHASE_TO_TASK: Dict[str, str] = {
        "recon":          "recon",
        "enum":           "recon",
        "exploit":        "exploit",
        "postexp":        "privesc",
        "post_exploit":   "privesc",
        "cred":           "cred",
        "lateral":        "lateral",
        "privesc":        "privesc",
        "persist":        "lateral",
        "exfil":          "cred",
        "c2":             "analyze",
        "report":         "analyze",
    }

    def select(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        """Ask the best MoE expert for a command recommendation. Returns None if disabled."""
        if os.environ.get("AUTO_USE_SWAN", "0") != "1":
            return None
        return self._swan_candidate(target, phase, context)

    def _swan_candidate(
        self, target: str, phase: str, context: Dict
    ) -> Optional[CommandDecision]:
        try:
            from swan_agent import mcp_swan_run as _swan_run  # lazy import
            services  = context.get("services", [])
            os_hint   = context.get("os_hint", "unknown")
            task_type = self._PHASE_TO_TASK.get(phase, "analyze")
            catalog   = _get_phase_command_catalog(phase)
            catalog_line = (
                f"Available LazyOwn commands for phase '{phase}': {catalog}\n"
                if catalog else ""
            )
            goal = (
                f"{catalog_line}"
                f"IMPORTANT: These are HIGH-LEVEL ABSTRACTIONS — payload.json auto-injects all parameters. "
                f"Reply with ONLY the command name.\n"
                f"Suggest the best command for phase='{phase}' target='{target}' "
                f"os={os_hint} services={services[:5]}."
            )
            raw  = _swan_run(task_type, goal, phase=phase)
            data = json.loads(raw)
            output = data.get("output", "").strip()
            # Extract first word (command name) from the expert output
            cmd = output.split()[0] if output.split() else None
            if cmd and len(cmd) < 50 and "\n" not in cmd:
                return CommandDecision(
                    command=cmd,
                    source="swan",
                    reason=(
                        f"SWAN expert={data.get('expert_id','?')} "
                        f"detect={data.get('detection_pct',0):.0f}%"
                    ),
                    priority=3,
                )
        except Exception as exc:
            log.debug("SWANSelector error: %s", exc)
        return None


class FallbackSelector(ICommandSelector):
    """
    Static map fallback — always returns a CommandDecision, never None.
    Selects OS-appropriate commands when the OS is known.
    Single Responsibility: static fallback map only.
    """

    def select(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        """Return the static fallback command for this phase. Never returns None."""
        categories = _PHASE_CATEGORIES.get(phase, ["other"])
        category   = categories[0]
        os_hint    = context.get("os_hint", "unknown")

        os_map = (
            _FALLBACK_MAP_WINDOWS if os_hint == "windows"
            else _FALLBACK_MAP_LINUX if os_hint == "linux"
            else {}
        )
        cmd = os_map.get(category) or _FALLBACK_MAP.get(category, "list")

        return CommandDecision(
            command=cmd, source="fallback",
            reason=f"static map for {category} (os={os_hint})",
        )


class CredentialSpraySelector(ICommandSelector):
    """
    When credentials exist in payload.json and open services are known,
    generates credential-spray commands against those services.

    Only activates in exploit/lateral/privesc/cred phases.
    Tracks sprayed (command, target, user) tuples to avoid repeating.
    Single Responsibility: credential reuse selection only.
    """

    _SERVICE_COMMANDS: Dict[str, str] = {
        "ssh":    "lazyssh",
        "smb":    "crackmapexec",
        "winrm":  "evil-winrm",
        "ftp":    "lazyftp",
        "http":   "lazyburp",
        "https":  "lazyburp",
        "rdp":    "xfreerdp",
        "mssql":  "mssqlpwner",
        "mysql":  "mysqldump",
        "ldap":   "ldapdomaindump",
    }

    def __init__(self, fail_counts: Dict[str, int]) -> None:
        self._fail_counts = fail_counts
        self._sprayed: set = set()

    def select(self, target: str, phase: str, context: Dict) -> Optional[CommandDecision]:
        """Return a spray command when credentials + matching service are available."""
        if phase not in ("exploit", "lateral", "privesc", "cred"):
            return None
        payload = _load_payload()
        user    = payload.get("start_user", "")
        passwd  = payload.get("start_pass", "") or payload.get("hash", "")
        if not user or not passwd:
            return None
        services = context.get("services", [])
        for svc in services:
            cmd = self._SERVICE_COMMANDS.get(svc.lower())
            if cmd is None:
                continue
            if self._fail_counts.get(cmd, 0) >= MAX_FAILS_PER_CMD:
                continue
            spray_key = f"{cmd}:{target}:{user}"
            if spray_key in self._sprayed:
                continue
            self._sprayed.add(spray_key)
            return CommandDecision(
                command=cmd,
                source="cred_spray",
                reason=f"credential reuse — {user}@{target} via {svc}",
                priority=2,
            )
        return None


class CascadeStrategy:
    """
    Chains selectors in order and returns the first non-None result.

    Open/Closed: extend by adding selectors without modifying existing ones.
    """

    def __init__(self, selectors: List[ICommandSelector]) -> None:
        self._selectors = selectors

    def next_command(
        self,
        target: str,
        phase: str,
        context: Optional[Dict] = None,
    ) -> CommandDecision:
        """Try each selector in order. The FallbackSelector ensures a result."""
        ctx = context or {}
        for selector in self._selectors:
            result = selector.select(target, phase, ctx)
            if result is not None:
                return result
        # Should never reach here if FallbackSelector is last in the chain
        return CommandDecision(command="list", source="fallback", reason="emergency fallback")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — StrategyEngine  (D — injects runner + selectors)
# ─────────────────────────────────────────────────────────────────────────────


class StrategyEngine:
    """
    Decides the next command for a (target, phase) pair.

    Cascade identical to lazyown_mcp.py auto_loop:
      1. Reactive engine (if a high-priority decision is pending)
      2. Parquet (successful commands from previous sessions)
      3. Bridge catalog (commands for the phase/services)
      4. LLM (Groq/Ollama if AUTO_USE_LLM=1)
      5. Static fallback

    Dependency Inversion: runner and selectors are injected.
    """

    def __init__(
        self,
        runner: ICommandRunner,
        selectors: Optional[List[ICommandSelector]] = None,
    ) -> None:
        self._runner      = runner
        self._fail_counts: Dict[str, int] = {}
        self._reactive_sel: Optional[ReactiveSelector] = None

        if selectors is None:
            pdb        = _get_pdb() if _get_pdb else None
            dispatcher = _get_dispatcher() if _get_dispatcher else None
            reactive   = _ReactEngine() if _ReactEngine else None
            reactive_sel = ReactiveSelector(reactive)
            self._reactive_sel = reactive_sel
            selectors = [
                reactive_sel,
                CredentialSpraySelector(self._fail_counts),
                ParquetSelector(pdb, self._fail_counts),
                BridgeSelector(dispatcher, self._fail_counts),
                SWANSelector(),
                LLMSelector(),
                FallbackSelector(),
            ]

        self._cascade = CascadeStrategy(selectors)

    def register_output(
        self,
        output: str,
        command: str,
        platform: str = "linux",
        success: bool = True,
    ) -> None:
        """Feed the reactive selector with the last command output."""
        if not success:
            key = command.split()[0] if command else command
            self._fail_counts[key] = self._fail_counts.get(key, 0) + 1
        if self._reactive_sel is not None:
            self._reactive_sel.register_output(output, command, platform)

    def next_command(
        self,
        target: str,
        phase: str,
        services: Optional[List[str]] = None,
        os_hint: str = "unknown",
    ) -> CommandDecision:
        """Select the next command for target/phase using the cascade."""
        return self._cascade.next_command(
            target, phase, context={"services": services or [], "os_hint": os_hint}
        )


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — IObjectiveHandler + ExecutionEngine
#             (O — Open/Closed via protocol)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class StepResult:
    """Result of a single execution step."""
    step:     int
    command:  str
    output:   str
    success:  bool
    source:   str
    findings: List[Dict] = field(default_factory=list)
    phase:    str = ""


class IObjectiveHandler(ABC):
    """Contract for running an objective to completion."""

    @abstractmethod
    def handle(
        self,
        objective_id: str,
        objective_text: str,
        target: str,
        context: Dict,
    ) -> List[StepResult]:
        """Execute objective and return a list of step results."""


class ExecutionEngine(IObjectiveHandler):
    """
    Implements the per-objective execution loop.

    Selects commands, runs them, parses output, updates world model,
    emits events. Equivalent to the former _run_objective coroutine but
    encapsulated as a class to satisfy Open/Closed (subclass to override
    step logic without modifying this class).

    Dependency Inversion: strategy (which wraps runner) is injected.
    """

    def __init__(
        self,
        strategy: StrategyEngine,
        max_steps: int = MAX_STEPS_DEFAULT,
        world_model: Any = None,
        obs_parser: Any = None,
        facts: Any = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._strategy    = strategy
        self._max_steps   = max_steps
        self._world_model = world_model
        self._obs_parser  = obs_parser
        self._facts       = facts
        self._loop        = loop

    def handle(
        self,
        objective_id: str,
        objective_text: str,
        target: str,
        context: Optional[Dict] = None,  # type: ignore[override]
    ) -> List[StepResult]:
        """Synchronous entry point. Delegates to _run_sync."""
        return self._run_sync(objective_id, objective_text, target)

    async def run_async(
        self,
        objective_id: str,
        objective_text: str,
        target: str,
    ) -> List[StepResult]:
        """Asyncio entry point used by objective_loop."""
        loop = self._loop or asyncio.get_event_loop()
        return await _run_objective(
            objective_id=objective_id,
            objective_text=objective_text,
            target=target,
            max_steps=self._max_steps,
            strategy=self._strategy,
            world_model=self._world_model,
            obs_parser=self._obs_parser,
            facts=self._facts,
            loop=loop,
        )

    def _run_sync(
        self,
        objective_id: str,
        objective_text: str,
        target: str,
    ) -> List[StepResult]:
        """Run the async coroutine synchronously (for testing / non-async callers)."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    fut = pool.submit(
                        asyncio.run,
                        _run_objective(
                            objective_id=objective_id,
                            objective_text=objective_text,
                            target=target,
                            max_steps=self._max_steps,
                            strategy=self._strategy,
                            world_model=self._world_model,
                            obs_parser=self._obs_parser,
                            facts=self._facts,
                            loop=asyncio.new_event_loop(),
                        ),
                    )
                    return fut.result()
            else:
                return loop.run_until_complete(
                    _run_objective(
                        objective_id=objective_id,
                        objective_text=objective_text,
                        target=target,
                        max_steps=self._max_steps,
                        strategy=self._strategy,
                        world_model=self._world_model,
                        obs_parser=self._obs_parser,
                        facts=self._facts,
                        loop=loop,
                    )
                )
        except Exception as exc:
            log.error("ExecutionEngine._run_sync error: %s", exc)
            return []


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — _run_objective coroutine (kept as module-level for asyncio.gather)
# ─────────────────────────────────────────────────────────────────────────────

def _load_payload() -> Dict:
    """Load payload.json, returning empty dict on any error."""
    try:
        return json.loads(PAYLOAD_FILE.read_text())
    except Exception:
        return {}


def _read_recent_csv_commands(limit: int = 3) -> List[str]:
    """Return the last N command names from the session CSV log."""
    csv_path = SESSIONS_DIR / "LazyOwn_session_report.csv"
    if not csv_path.exists():
        return []
    try:
        lines = csv_path.read_text(encoding="utf-8", errors="replace").splitlines()
        cmds: List[str] = []
        for line in reversed(lines):
            parts = line.split(",")
            if len(parts) >= 2:
                cmd = parts[1].strip().strip('"').split()[0]
                if cmd and cmd not in cmds:
                    cmds.append(cmd)
            if len(cmds) >= limit:
                break
        return cmds
    except Exception:
        return []


def _load_campaign_blacklist() -> Dict[str, List[str]]:
    """Load per-context command blacklist from campaign_lessons.jsonl."""
    blacklist: Dict[str, List[str]] = {}
    lessons_file = SESSIONS_DIR / "campaign_lessons.jsonl"
    if not lessons_file.exists():
        return blacklist
    try:
        for line in lessons_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            lesson = json.loads(line)
            if lesson.get("outcome") != "failed":
                continue
            command = lesson.get("command", "").strip().split()[0]
            if not command:
                continue
            ctx = lesson.get("context", "any")
            if ctx not in blacklist:
                blacklist[ctx] = []
            if command not in blacklist[ctx]:
                blacklist[ctx].append(command)
    except Exception:
        pass
    return blacklist


_CAMPAIGN_BLACKLIST: Dict[str, List[str]] = {}
_BLACKLIST_LOADED: bool = False


def _get_campaign_blacklist() -> Dict[str, List[str]]:
    """Return cached campaign blacklist, reloading if the file changed."""
    global _CAMPAIGN_BLACKLIST, _BLACKLIST_LOADED
    lessons_file = SESSIONS_DIR / "campaign_lessons.jsonl"
    if not _BLACKLIST_LOADED or (lessons_file.exists() and lessons_file.stat().st_mtime > 0):
        _CAMPAIGN_BLACKLIST = _load_campaign_blacklist()
        _BLACKLIST_LOADED = True
    return _CAMPAIGN_BLACKLIST


def _compute_step_reward(
    output: str,
    command: str,
    phase: str,
    success: bool,
    findings: List[Dict],
    prev_cmds: List[str],
) -> float:
    """Compute multi-dimensional RL reward based on finding quality, novelty, and phase.

    Args:
        output:    Raw command output text.
        command:   Command string that was executed.
        phase:     Current engagement phase.
        success:   Basic success flag from keyword detection.
        findings:  Parsed ObsParser findings for this step.
        prev_cmds: Command names from previous steps (for novelty penalty).

    Returns:
        Reward scalar in the range [-2.0, 15.0].
    """
    if not success:
        return -2.0

    low = output.lower()

    # Finding-type priority (highest wins)
    score = 2.0
    for f in findings:
        ftype = f.get("type", "")
        if ftype in ("credential",):
            score = max(score, 10.0)
        elif ftype in ("root_shell", "privesc"):
            score = max(score, 9.0)
        elif ftype in ("hash",):
            score = max(score, 8.0)
        elif ftype in ("cve", "service_version"):
            score = max(score, 5.0)
        elif ftype in ("host", "ip", "open_port"):
            score = max(score, 3.5)

    # Keyword boost when obs_parser is absent
    if score < 5.0:
        if any(k in low for k in ("password", "passwd", "credentials found", "login successful")):
            score = max(score, 10.0)
        elif any(k in low for k in ("uid=0", "root shell", "nt authority", "system privilege")):
            score = max(score, 9.0)
        elif any(k in low for k in ("hash", "ntlm", "lm:", "aad3b435", "krb5tgs")):
            score = max(score, 8.0)
        elif any(k in low for k in ("open", "found", "200 ok", "login page")):
            score = max(score, 3.0)

    # Novelty penalty: repeated command earns less
    cmd_base = command.strip().split()[0] if command.strip() else ""
    repeat_count = prev_cmds.count(cmd_base)
    if repeat_count > 0:
        score = score * max(0.3, 1.0 - repeat_count * 0.2)

    # Phase multiplier: late-phase successes are worth more
    _phase_mult: Dict[str, float] = {
        "recon":   1.0,
        "enum":    1.2,
        "exploit": 1.5,
        "privesc": 1.8,
        "lateral": 1.6,
        "cred":    1.7,
        "exfil":   2.0,
    }
    score = score * _phase_mult.get(phase, 1.0)

    return round(min(score, 15.0), 2)


async def _detect_target_os(
    target: str,
    loop: asyncio.AbstractEventLoop,
) -> str:
    """
    Infer the target OS from ICMP TTL via a single ping probe.

    TTL heuristics (accounting for up to ~20 router hops consumed):
      TTL <= 64   -> Linux / Unix / macOS (default initial TTL = 64)
      TTL <= 128  -> Windows             (default initial TTL = 128)
      TTL > 128   -> Unknown / network device

    Returns one of: 'linux', 'windows', 'unknown'.
    An unreachable host returns 'unknown' — callers must treat unknown as a
    signal to skip OS-specific tooling rather than defaulting to any platform.
    """
    try:
        proc = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    ["ping", "-c", "1", "-W", "2", target],
                    capture_output=True,
                    text=True,
                ),
            ),
            timeout=6.0,
        )
        output = proc.stdout + proc.stderr
        match = re.search(r"ttl=(\d+)", output, re.IGNORECASE)
        if not match:
            log.debug("OS detection: no TTL in ping output for %s", target)
            return "unknown"
        ttl = int(match.group(1))
        if ttl <= 64:
            return "linux"
        if ttl <= 128:
            return "windows"
        return "unknown"
    except asyncio.TimeoutError:
        log.debug("OS detection: ping timed out for %s", target)
        return "unknown"
    except Exception as exc:
        log.debug("OS detection error for %s: %s", target, exc)
        return "unknown"


async def _run_objective(
    objective_id: str,
    objective_text: str,
    target: str,
    max_steps: int,
    strategy: StrategyEngine,
    world_model: Any,
    obs_parser: Any,
    facts: Any,
    loop: asyncio.AbstractEventLoop,
) -> List[StepResult]:
    """
    Execute an objective autonomously: select commands, run them,
    parse output, update world model, and emit events.
    Returns the list of StepResult on completion.
    """
    log.info("[%s] start: %s", objective_id, objective_text[:80])
    _emit("OBJECTIVE_START", {
        "id": objective_id, "text": objective_text[:200], "target": target,
    })

    results: List[StepResult] = []
    phase:   str              = "recon"
    services: List[str]       = []
    _consecutive_list: int    = 0
    _last_command: str        = ""
    _prev_cmds: List[str]     = []

    if world_model is not None:
        try:
            phase = world_model.get_phase().value
        except Exception:
            pass

    # ── OS detection (pre-recon) ──────────────────────────────────────────────
    # Probe the target with a single ICMP packet to infer the operating system
    # from TTL before any tool selection occurs.  This prevents dispatching
    # Windows-specific tooling (evil-winrm, secretsdump, etc.) against Linux
    # targets and vice-versa.  The probe runs in parallel with the first
    # objective log emission so it adds no meaningful latency to the loop.
    detected_os = await _detect_target_os(target, loop)
    log.info("[%s] OS detection: target=%s os=%s", objective_id, target, detected_os)
    _emit("OS_DETECTED", {
        "objective_id": objective_id,
        "target":       target,
        "os":           detected_os,
    })

    if world_model is not None and detected_os != "unknown":
        try:
            snapshot = world_model.snapshot()
            host_entry = snapshot.get("hosts", {}).get(target, {})
            if not host_entry.get("os_hint"):
                world_model.update_host(target, os_hint=detected_os)
        except Exception as wm_exc:
            log.debug("world_model OS update error: %s", wm_exc)

    # Persist the detected OS into payload.json so every fresh LazyOwn shell
    # process spawned by _run_lazyown_command inherits the correct os_id.
    # LazyOwn's do_ping uses os_id "1"=Windows, "2"=Linux, "4"=Unknown.
    _OS_ID_MAP = {"linux": "2", "windows": "1", "unknown": "4"}
    _detected_os_id = _OS_ID_MAP.get(detected_os, "4")
    if detected_os != "unknown":
        try:
            _pl = _load_payload()
            if _pl.get("os_id") != _detected_os_id:
                _pl["os_id"] = _detected_os_id
                PAYLOAD_FILE.write_text(
                    json.dumps(_pl, indent=2, ensure_ascii=False), encoding="utf-8"
                )
                log.info(
                    "[%s] payload.json os_id updated: %s (%s)",
                    objective_id, _detected_os_id, detected_os,
                )
        except Exception as _pe:
            log.debug("payload.json os_id update error: %s", _pe)

    # Write sessions/os.json in the same format that do_ping uses so that
    # run_lazynmap's OS-gate reads it and skips the redundant ping probe.
    try:
        _os_entry = [{
            "id":    _detected_os_id,
            "os":    detected_os.capitalize(),
            "ttl":   64 if detected_os == "linux" else (128 if detected_os == "windows" else "NULL"),
            "state": "active" if detected_os != "unknown" else "unknown",
        }]
        _os_json_path = SESSIONS_DIR / "os.json"
        _os_json_path.write_text(
            json.dumps(_os_entry, indent=4, ensure_ascii=False), encoding="utf-8"
        )
    except Exception as _oe:
        log.debug("sessions/os.json write error: %s", _oe)

    for step_n in range(1, max_steps + 1):
        decision = strategy.next_command(target, phase, services, os_hint=detected_os)
        command  = decision.command.replace("{rhost}", target).replace("TARGET", target)
        # Use 'assign' (the LazyOwn shell command) to set params including
        # rhost and os_id. Both _run_lazyown_command and PTYCommandRunner
        # accept multi-line input; each line is one shell command.
        full_cmd = f"assign rhost {target}\nassign os_id {_detected_os_id}\n{command}"

        log.info("  step %d/%d [%s] %s", step_n, max_steps, decision.source, command)

        # Pre-execution detection oracle: swap out critical-risk commands silently
        try:
            from detection_oracle import get_oracle as _pre_get_oracle
            _pre_assess = _pre_get_oracle().assess(
                command.split()[0], command, phase
            )
            if _pre_assess.is_critical_risk:
                log.info(
                    "  [oracle] %s critical-risk (%.0f%%) — requesting alternative",
                    command, _pre_assess.probability * 100,
                )
                _alt = strategy.next_command(target, phase, services, os_hint=detected_os)
                _alt_cmd = _alt.command.replace("{rhost}", target).replace("TARGET", target)
                if _alt_cmd and _alt_cmd != command:
                    decision = _alt
                    command  = _alt_cmd
                    full_cmd = (
                        f"assign rhost {target}\nassign os_id {_detected_os_id}\n{command}"
                    )
                    log.info("  [oracle] using %s instead", command)
        except Exception:
            pass

        _emit("STEP_START", {
            "objective_id": objective_id,
            "step":    step_n,
            "command": command,
            "source":  decision.source,
            "reason":  decision.reason,
        })

        output = await loop.run_in_executor(
            None, _run_lazyown, full_cmd, STEP_TIMEOUT_S,
        )

        low    = output.lower()
        failed = any(k in low for k in (
            "error", "failed", "no such", "command not found",
            "traceback", "refused", "timeout",
        )) and not any(k in low for k in ("found", "success", "open", "hash"))
        success = not failed

        findings: List[Dict] = []
        if obs_parser is not None:
            try:
                obs = obs_parser.parse(output, host=target, tool=command.split()[0])
                findings = [asdict(f) for f in obs.findings] if obs.findings else []
                if world_model is not None:
                    world_model.update_from_findings(obs.findings)
                    try:
                        phase = world_model.get_phase().value
                    except Exception:
                        pass
                    try:
                        wm_file = SESSIONS_DIR / "world_model.json"
                        wm_file.write_text(
                            json.dumps(world_model.snapshot(), indent=2, default=str),
                            encoding="utf-8",
                        )
                    except Exception as wm_err:
                        log.debug("world_model.json write error: %s", wm_err)
                for f in obs.findings:
                    svc = getattr(f, "service", None)
                    if svc and svc not in services:
                        services.append(svc)

                # ── Auto-inject discovered credentials into payload.json ──────
                # When ObsParser finds a CREDENTIAL (user:pass), write it back
                # so every subsequent command that needs auth has it available.
                try:
                    from modules.obs_parser import FindingType as _FT
                    cred_findings = obs.by_type(_FT.CREDENTIAL)
                    hash_findings = obs.by_type(_FT.HASH)
                    user_findings = obs.by_type(_FT.USERNAME)
                    domain_findings = obs.by_type(_FT.DOMAIN)
                    if cred_findings or hash_findings or user_findings or domain_findings:
                        _pl = _load_payload()
                        _changed = False
                        if cred_findings:
                            top = cred_findings[0]
                            parts = top.value.split(":", 1)
                            if len(parts) == 2 and not _pl.get("start_user"):
                                _pl["start_user"] = parts[0]
                                _pl["start_pass"] = parts[1]
                                _changed = True
                                log.info("[%s] AUTO-CRED: start_user=%s", objective_id, parts[0])
                                # also append to credentials file
                                try:
                                    _cred_file = SESSIONS_DIR / "credentials.txt"
                                    with _cred_file.open("a", encoding="utf-8") as _cf:
                                        _cf.write(f"{top.value}  # host={target} cmd={command}\n")
                                except Exception:
                                    pass
                                _emit("CREDENTIAL_FOUND", {
                                    "objective_id": objective_id,
                                    "user": parts[0],
                                    "host": target,
                                    "source": command,
                                })
                        if hash_findings and not _pl.get("hash"):
                            _pl["hash"] = hash_findings[0].value
                            _changed = True
                            log.info("[%s] AUTO-HASH: %s", objective_id, hash_findings[0].value[:30])
                        if user_findings and not _pl.get("start_user"):
                            _pl["start_user"] = user_findings[0].value
                            _changed = True
                        if domain_findings and not _pl.get("domain"):
                            _pl["domain"] = domain_findings[0].value
                            _changed = True
                            log.info("[%s] AUTO-DOMAIN: %s", objective_id, domain_findings[0].value)
                        if _changed:
                            PAYLOAD_FILE.write_text(
                                json.dumps(_pl, indent=2, ensure_ascii=False),
                                encoding="utf-8",
                            )
                except Exception as _cred_exc:
                    log.debug("credential auto-inject error: %s", _cred_exc)

                # ── nmap XML auto-populate ────────────────────────────────────
                # After any nmap-style command, parse the XML output and update
                # payload.json with domain, services, and additional hosts.
                if command.split()[0] in ("lazynmap", "nmap", "rustscan", "masscan"):
                    try:
                        import xml.etree.ElementTree as _ET
                        _xml_path = SESSIONS_DIR / f"scan_{target}.nmap.xml"
                        if _xml_path.exists():
                            _tree = _ET.parse(str(_xml_path))
                            _root = _tree.getroot()
                            _pl2 = _load_payload()
                            _ch2 = False
                            # Extract domain from hostnames
                            for _hn in _root.iter("hostname"):
                                _name = _hn.get("name", "")
                                if _name and "." in _name and not _pl2.get("domain"):
                                    _pl2["domain"] = _name
                                    _ch2 = True
                                    log.info("[%s] AUTO-DOMAIN(nmap): %s", objective_id, _name)
                                    break
                            # Extract open services
                            for _port in _root.iter("port"):
                                _state = _port.find("state")
                                if _state is not None and _state.get("state") == "open":
                                    _svc_el = _port.find("service")
                                    if _svc_el is not None:
                                        _svc_name = _svc_el.get("name", "")
                                        if _svc_name and _svc_name not in services:
                                            services.append(_svc_name)
                            # Extract OS match
                            for _osmatch in _root.iter("osmatch"):
                                _os_name = _osmatch.get("name", "").lower()
                                if _os_name and not _pl2.get("os_id"):
                                    _os_id = "2" if "windows" in _os_name else "1"
                                    _pl2["os_id"] = _os_id
                                    _ch2 = True
                                    break
                            if _ch2:
                                PAYLOAD_FILE.write_text(
                                    json.dumps(_pl2, indent=2, ensure_ascii=False),
                                    encoding="utf-8",
                                )
                    except Exception as _xml_exc:
                        log.debug("nmap XML auto-populate error: %s", _xml_exc)

            except Exception as exc:
                log.debug("obs_parser error: %s", exc)

        # ── Proactive phase advancement based on finding quality ──────────────
        # Advance immediately when evidence warrants it instead of waiting for
        # three repeated commands (the stuck-loop recovery is still the safety net).
        _phase_fwd = [
            "recon", "enum", "exploit", "postexp", "privesc",
            "lateral", "cred", "exfil", "c2", "report",
        ]
        _has_root    = any(f.get("type") == "root_shell" for f in findings)
        _has_cred    = any(f.get("type") in ("credential", "hash") for f in findings)
        _has_service = len(services) > 0
        try:
            _cur_idx = _phase_fwd.index(phase)
        except ValueError:
            _cur_idx = -1

        if _cur_idx >= 0:
            if _has_root and phase not in ("exfil", "c2", "report"):
                _jump = min(_cur_idx + 2, len(_phase_fwd) - 1)
                phase = _phase_fwd[_jump]
                log.info("[%s] PHASE JUMP→%s (root shell found)", objective_id, phase)
                _emit("PHASE_ADVANCE", {
                    "objective_id": objective_id, "reason": "root_shell", "phase": phase,
                })
            elif _has_cred and phase in ("recon", "enum"):
                phase = "exploit"
                log.info("[%s] PHASE→exploit (credential found)", objective_id, phase)
                _emit("PHASE_ADVANCE", {
                    "objective_id": objective_id, "reason": "credential_found", "phase": phase,
                })
            elif _has_service and phase == "recon" and len(services) >= 2:
                phase = "enum"
                log.info("[%s] PHASE→enum (%d services discovered)", objective_id, len(services))
                _emit("PHASE_ADVANCE", {
                    "objective_id": objective_id,
                    "reason": f"{len(services)}_services_found",
                    "phase": phase,
                })

        # ── Stuck-loop recovery ───────────────────────────────────────────────
        # Detect ANY repeated command (not just "list") — if the same command
        # runs 3x in a row with unknown/zero reward, escalate the phase.
        _cmd_base = command.strip().split()[0] if command.strip() else "list"
        if _cmd_base == _last_command:
            _consecutive_list += 1
        else:
            _consecutive_list = 0
            _last_command = _cmd_base

        if _consecutive_list >= 3:
            log.warning("[%s] stuck loop detected (%d× '%s') — escalating phase", objective_id, _consecutive_list, _last_command)
            _emit("STUCK_LOOP", {
                "objective_id": objective_id,
                "phase": phase,
                "repeated_command": _last_command,
                "consecutive_count": _consecutive_list,
            })
            # Try to advance phase via world_model, otherwise hard-advance
            _phase_order = ["recon", "enum", "exploit", "postexp", "persist", "privesc",
                            "cred", "lateral", "exfil", "c2", "report"]
            try:
                _cur_idx = _phase_order.index(phase)
                if _cur_idx + 1 < len(_phase_order):
                    phase = _phase_order[_cur_idx + 1]
                    log.info("[%s] phase advanced to %s (stuck recovery)", objective_id, phase)
                    _consecutive_list = 0
            except ValueError:
                pass
            # Reset fail counts to give new phase commands a fresh start
            strategy._fail_counts.clear()

        if facts is not None and success:
            try:
                facts.ingest_text(output, source=command, target=target)
            except Exception:
                pass

        # Determine platform for reactive engine: prefer world_model, then
        # the TTL-based detection result, and finally fall back to "linux"
        # (never hard-code "windows" as the unknown-platform default).
        if world_model is not None:
            try:
                wm_os = (
                    world_model.snapshot()
                    .get("hosts", {})
                    .get(target, {})
                    .get("os_hint", "")
                    or detected_os
                )
            except Exception:
                wm_os = detected_os
        else:
            wm_os = detected_os if detected_os != "unknown" else "linux"

        strategy.register_output(output, command, platform=wm_os, success=success)

        # ── RL feedback — update Q-table after every step ─────────────────────
        # The RLTrainer learns which sources (reactive/parquet/bridge/swan/llm)
        # produce successful outcomes per (phase, findings_quality) state.
        # This runs silently; failures never block execution.
        try:
            from rl_trainer import get_trainer as _get_rl_trainer
            _rl = _get_rl_trainer()
            _detect_prob = 0.0
            try:
                from detection_oracle import get_oracle as _get_oracle
                _detect_prob = _get_oracle().probability(command)
            except Exception:
                pass
            _reward_ema  = _compute_step_reward(
                output, command, phase, success, findings, _prev_cmds
            )
            _rl_state    = _rl.encode_state(phase, phase, _reward_ema)
            _rl_next     = _rl.encode_state(phase, phase, _reward_ema)
            _raw_reward  = _reward_ema
            _rl.update(
                state=_rl_state,
                action=decision.source,
                reward=_raw_reward,
                next_state=_rl_next,
                candidates=["reactive", "cred_spray", "parquet", "bridge", "swan", "llm", "fallback"],
                detection_prob=_detect_prob,
            )
            _rl.save()
        except Exception as _rl_exc:
            log.debug("RL update error: %s", _rl_exc)

        sr = StepResult(
            step=step_n, command=command, output=output,
            success=success, source=decision.source,
            findings=findings, phase=phase,
        )
        results.append(sr)
        _prev_cmds.append(command.strip().split()[0] if command.strip() else "")

        _emit("STEP_DONE", {
            "objective_id":   objective_id,
            "step":           step_n,
            "command":        command,
            "success":        success,
            "phase":          phase,
            "findings_count": len(findings),
            "output_snippet": output[:300],
        }, severity="warning" if not success else "info")

        high_value = any(
            getattr(f, "type", "") in ("credential", "hash", "root_shell", "privesc")
            for f in (
                obs_parser.parse(output, host=target, tool=command).findings
                if obs_parser else []
            )
        )
        if high_value:
            log.info("  High-value finding — stopping loop early")
            _emit("HIGH_VALUE", {
                "objective_id": objective_id,
                "step":         step_n,
                "command":      command,
            }, severity="critical")
            break

        await asyncio.sleep(STEP_DELAY_S)

    _emit("OBJECTIVE_DONE", {
        "id":             objective_id,
        "steps_run":      len(results),
        "final_phase":    phase,
        "findings_total": sum(len(r.findings) for r in results),
    })
    return results


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — DroneCoordinator
# ─────────────────────────────────────────────────────────────────────────────

class DroneCoordinator:
    """
    Watches ExecutionEngine results and launches hive drones when events
    worth parallel analysis are detected:
      - New host discovered  -> recon drone
      - Exploitable service  -> exploit drone
      - Hash/credential      -> cred drone
    """

    def __init__(self) -> None:
        self._hive        = _get_hive() if _get_hive else None
        self._seen_hosts: set = set()
        self._lock        = threading.Lock()

    def process_findings(
        self,
        findings: List[Dict],
        target: str,
        objective_id: str,
        payload_key: str = "",
    ) -> List[str]:
        """Launch drones for relevant findings. Returns list of drone_ids."""
        if self._hive is None:
            return []

        drone_ids: List[str] = []

        for f in findings:
            ftype   = f.get("type", "")
            value   = f.get("value", "")
            service = f.get("service", "")

            if ftype in ("host", "ip") and value not in self._seen_hosts:
                with self._lock:
                    if value not in self._seen_hosts:
                        self._seen_hosts.add(value)
                goal = f"Enumerate new host {value} discovered during {objective_id}"
                did  = self._hive.spawn(
                    goal=goal, role="recon",
                    backend=HIVE_BACKEND, max_iterations=HIVE_MAX_ITER,
                )
                drone_ids.append(did)
                _emit("DRONE_SPAWNED", {
                    "drone_id":     did,
                    "role":         "recon",
                    "trigger":      "new_host",
                    "host":         value,
                    "objective_id": objective_id,
                })

            elif ftype in ("service_version", "cve") and service:
                goal = (
                    f"Exploit {service} on {target} "
                    f"(context: {objective_id}, finding: {value[:60]})"
                )
                did  = self._hive.spawn(
                    goal=goal, role="exploit",
                    backend=HIVE_BACKEND, max_iterations=HIVE_MAX_ITER,
                )
                drone_ids.append(did)
                _emit("DRONE_SPAWNED", {
                    "drone_id":     did,
                    "role":         "exploit",
                    "trigger":      ftype,
                    "service":      service,
                    "value":        str(value)[:80],
                    "objective_id": objective_id,
                })

            elif ftype in ("credential", "hash"):
                goal = (
                    f"Crack and use credential found on {target}: {str(value)[:80]} "
                    f"(context: {objective_id})"
                )
                did  = self._hive.spawn(
                    goal=goal, role="cred",
                    backend=HIVE_BACKEND, max_iterations=HIVE_MAX_ITER,
                )
                drone_ids.append(did)
                _emit("DRONE_SPAWNED", {
                    "drone_id":     did,
                    "role":         "cred",
                    "trigger":      ftype,
                    "value":        str(value)[:40],
                    "objective_id": objective_id,
                })

        # ── Parallel per-service sweep when multiple open ports on same host ──
        # Group open-port/service_version findings by host, then spawn one
        # targeted exploit drone per service (cap: 3 per host per call).
        if self._hive is not None:
            _svc_findings = [
                f for f in findings
                if f.get("type") in ("open_port", "service_version")
            ]
            _host_svcs: Dict[str, List[Dict]] = {}
            for f in _svc_findings:
                _h = f.get("host", target) or target
                if _h not in _host_svcs:
                    _host_svcs[_h] = []
                _host_svcs[_h].append(f)

            for _h, _svcs in _host_svcs.items():
                if len(_svcs) < 2:
                    continue
                for _sf in _svcs[:3]:
                    _svc_name = _sf.get("service", "") or _sf.get("value", "")
                    if not _svc_name:
                        continue
                    _sweep_goal = (
                        f"Enumerate and exploit {_svc_name} on {_h} "
                        f"(parallel service sweep — context: {objective_id})"
                    )
                    _did = self._hive.spawn(
                        goal=_sweep_goal, role="exploit",
                        backend=HIVE_BACKEND, max_iterations=HIVE_MAX_ITER,
                    )
                    drone_ids.append(_did)
                    _emit("DRONE_SPAWNED", {
                        "drone_id":     _did,
                        "role":         "exploit",
                        "trigger":      "parallel_service_sweep",
                        "service":      _svc_name,
                        "host":         _h,
                        "objective_id": objective_id,
                    })

        return drone_ids


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7B — Engage Orchestrator (single-target kill-chain runner)
# ─────────────────────────────────────────────────────────────────────────────
#
# Public entry point: mcp_engage_target("10.10.11.5")
#
# Drives one host through the canonical kill-chain in a fixed, observable
# order: ping/os-detect -> nmap -> auto_populate -> enum -> exploit-search
# -> initial-access. Each phase has a primary tool, optional confirmation
# (gated by ApprovalGate), and a built-in fault recovery path that swaps
# the primary tool for the next bridge-catalog alternative when execution
# fails. Every action is narrated via EngagementNarrator so engagement.log
# stays human-readable and teammates connected to /collab/ see the same
# stream in real time.
#
# SOLID:
#   S — separate classes for the phase plan, the narrator, the shell detector,
#       the tool-switching fallback and the orchestrator. Each owns one job.
#   O — new phases plug in via PhaseStep(extension); the orchestrator iterates
#       the immutable plan tuple.
#   L — every phase step honours the same execute() contract.
#   I — the orchestrator depends on the small IApprovalGate / INarrator /
#       IBridgeCatalog protocols, not on concrete persistence.
#   D — narrator, gate, runner, bridge are all injected; defaults wire up
#       production implementations.
# ─────────────────────────────────────────────────────────────────────────────


_ENGAGE_PHASE_ORDER: Tuple[Tuple[str, str, str], ...] = (
    # (phase_id, primary_command, narrator_label)
    ("recon",          "ping",          "ping + OS detection"),
    ("recon",          "lazynmap",      "nmap full scan"),
    ("recon",          "auto_populate", "auto-populate payload.json"),
    ("enum",           "facts_show",    "enumerate services and facts"),
    ("enum",           "searchsploit",  "exploit candidate search"),
    ("exploit",        "lazymsfvenom",  "initial access — payload stage"),
)


_TOOL_FALLBACK_MAP: Dict[str, Tuple[str, ...]] = {
    "ping":          ("hostdiscover",),
    "lazynmap":      ("rustscan", "masscan", "nmap"),
    "auto_populate": ("facts_show",),
    "facts_show":    ("auto_populate",),
    "searchsploit":  ("nvddb", "exploitalert"),
    "lazymsfvenom":  ("generate_reverse_shell",),
}


@dataclass(frozen=True)
class EnginePhaseStep:
    """One step in the EngageOrchestrator plan.

    Attributes:
        phase: Canonical engagement phase tag (recon, enum, exploit, ...).
        primary: Preferred LazyOwn shell command for this step.
        label: Operator-facing short description used by the narrator.
        timeout_s: Per-step execution timeout. Defaults to STEP_TIMEOUT_S.
    """

    phase: str
    primary: str
    label: str
    timeout_s: int = STEP_TIMEOUT_S


@dataclass(frozen=True)
class EnginePhaseResult:
    """Result of one EnginePhaseStep execution."""

    step: EnginePhaseStep
    command_used: str
    output: str
    success: bool
    switched_from: str = ""
    skipped_reason: str = ""

    @property
    def did_switch(self) -> bool:
        """True when the orchestrator used a fallback tool."""
        return bool(self.switched_from)


class IToolFallbackResolver(ABC):
    """Contract for choosing a replacement tool after a failure."""

    @abstractmethod
    def next_tool(
        self,
        failed_command: str,
        phase: str,
        attempt: int,
    ) -> Optional[str]:
        """Return the next candidate command or None when exhausted."""


class StaticFallbackResolver(IToolFallbackResolver):
    """Resolver backed by the static :data:`_TOOL_FALLBACK_MAP`.

    Used when the bridge catalog is unavailable (eg the lazyown_bridge
    module failed to import). Picks the i-th alternative for the given
    primary command, returning None once the list is exhausted.
    """

    def next_tool(
        self,
        failed_command: str,
        phase: str,
        attempt: int,
    ) -> Optional[str]:
        primary = failed_command.strip().split()[0] if failed_command.strip() else ""
        alternatives = _TOOL_FALLBACK_MAP.get(primary, ())
        if attempt >= len(alternatives):
            return None
        return alternatives[attempt]


class BridgeFallbackResolver(IToolFallbackResolver):
    """Resolver that asks the bridge catalog for phase-appropriate alternatives.

    Falls back to the static map when the bridge cannot answer, so the
    orchestrator always converges instead of stalling. The internal
    candidate cache is keyed by (phase, primary) so repeated failures
    don't re-query the catalog.
    """

    def __init__(self, dispatcher: Any = None) -> None:
        self._dispatcher = dispatcher if dispatcher is not None else (
            _get_dispatcher() if _get_dispatcher else None
        )
        self._static = StaticFallbackResolver()
        self._cache: Dict[Tuple[str, str], List[str]] = {}

    def _candidates(self, primary: str, phase: str) -> List[str]:
        key = (phase, primary)
        if key in self._cache:
            return self._cache[key]
        ordered: List[str] = []
        if self._dispatcher is not None:
            try:
                catalog = self._dispatcher.list_phase(phase) or []
                for entry in catalog:
                    name = getattr(entry, "command", "")
                    if name and name != primary and name not in ordered:
                        ordered.append(name)
            except Exception:
                pass
        for fallback in _TOOL_FALLBACK_MAP.get(primary, ()):
            if fallback not in ordered and fallback != primary:
                ordered.append(fallback)
        self._cache[key] = ordered
        return ordered

    def next_tool(
        self,
        failed_command: str,
        phase: str,
        attempt: int,
    ) -> Optional[str]:
        primary = failed_command.strip().split()[0] if failed_command.strip() else ""
        candidates = self._candidates(primary, phase)
        if attempt >= len(candidates):
            # Last-resort: defer to static map even if catalog answered.
            return self._static.next_tool(failed_command, phase, attempt - len(candidates))
        return candidates[attempt]


class _ShellDetector:
    """Watches sessions/beacons.json for new beacons and emits SHELL_OBTAINED.

    Idempotent: only narrates each client_id once. The actual notification
    fabric (collab/telegram/discord) lives in engagement_hooks; this class
    is a thin watcher used by the orchestrator between phases. The lazyc2
    beacon hook publishes immediately on registration so this watcher only
    matters when beacons appear before EngageOrchestrator is the active
    process (e.g. during unattended sessions).
    """

    BEACONS_FILE: Path = SESSIONS_DIR / "beacons.json"

    def __init__(self, narrator: Any) -> None:
        self._narrator = narrator
        self._seen_ids: set = set()
        self._last_size: int = 0

    def poll(self, target: str = "") -> List[str]:
        """Return the newly-detected client_ids since the previous poll."""
        new_ids: List[str] = []
        try:
            if not self.BEACONS_FILE.exists():
                return new_ids
            current_size = self.BEACONS_FILE.stat().st_size
            if current_size == self._last_size and self._seen_ids:
                return new_ids
            self._last_size = current_size
            try:
                data = json.loads(self.BEACONS_FILE.read_text(encoding="utf-8"))
            except Exception:
                return new_ids
            beacons = data if isinstance(data, (list, dict)) else []
            iterable = beacons.values() if isinstance(beacons, dict) else beacons
            for entry in iterable:
                if not isinstance(entry, dict):
                    continue
                cid = str(entry.get("client_id") or entry.get("id") or "")
                if not cid or cid in self._seen_ids:
                    continue
                self._seen_ids.add(cid)
                new_ids.append(cid)
                try:
                    from engagement_hooks import publish_shell_obtained as _push
                    _push(
                        client_id=cid,
                        primary_ip=str(entry.get("ip") or target or ""),
                        hostname=str(entry.get("hostname", "")),
                        user=str(entry.get("user", "")),
                        platform=str(entry.get("platform", "")),
                        narrator=self._narrator,
                    )
                except Exception as exc:
                    log.debug("shell publish failed: %s", exc)
        except Exception as exc:
            log.debug("shell detector poll error: %s", exc)
        return new_ids

    def detect_in_output(self, output: str, target: str = "") -> bool:
        """Return True when a shell/root-shell signal appears in command output."""
        if not output:
            return False
        low = output.lower()
        markers = (
            "uid=0", "uid=", "root@", "# whoami", "nt authority\\system",
            "shell open", "meterpreter >", "successfully spawned a shell",
            "got shell", "reverse shell connection",
        )
        if any(m in low for m in markers):
            try:
                self._narrator.narrate(
                    kind="SHELL_OBTAINED",
                    target=target or "unknown",
                    message="shell indicator detected in command output",
                    payload={"output_snippet": output[-200:]},
                    severity="critical",
                )
            except Exception:
                pass
            return True
        return False


class EngageOrchestrator:
    """Single-target kill-chain orchestrator backing the ``engage`` verb.

    Public usage:
        orch = EngageOrchestrator(target="10.10.11.5")
        summary = orch.run()

    The orchestrator never raises. Every error path is logged through the
    narrator and reflected in the returned summary so the operator (or the
    MCP caller) sees the full timeline.
    """

    DEFAULT_MAX_SWITCHES_PER_STEP = 3

    def __init__(
        self,
        target: str,
        runner: Optional[ICommandRunner] = None,
        narrator: Any = None,
        approval_gate: Any = None,
        fallback_resolver: Optional[IToolFallbackResolver] = None,
        shell_detector: Optional[_ShellDetector] = None,
        plan: Optional[Tuple[EnginePhaseStep, ...]] = None,
        max_switches_per_step: int = DEFAULT_MAX_SWITCHES_PER_STEP,
    ) -> None:
        from engagement_hooks import EngagementNarrator as _Narrator
        from engagement_hooks import is_valid_target as _is_valid_target
        if not _is_valid_target(target):
            raise ValueError(f"invalid target: {target!r}")
        self._target = target
        self._runner = runner or _build_default_runner()
        self._narrator = narrator or _Narrator()
        if approval_gate is None:
            try:
                from lazyown_policy import ApprovalGate as _Gate
                approval_gate = _Gate()
            except Exception:
                approval_gate = None
        self._gate = approval_gate
        self._fallback = fallback_resolver or BridgeFallbackResolver()
        self._shell = shell_detector or _ShellDetector(self._narrator)
        self._plan = plan or tuple(
            EnginePhaseStep(phase=p, primary=c, label=l)
            for p, c, l in _ENGAGE_PHASE_ORDER
        )
        self._max_switches = max(0, int(max_switches_per_step))
        self._engagement_id = uuid.uuid4().hex[:8]

    @property
    def engagement_id(self) -> str:
        """Stable id for this engagement (correlates events in logs)."""
        return self._engagement_id

    def run(self) -> Dict[str, Any]:
        """Drive the full plan against the configured target.

        Returns a summary dict with the engagement_id, target, per-step
        results, switch counts, and the final shell-obtained flag.
        """
        self._narrator.narrate(
            kind="ENGAGE_START",
            target=self._target,
            message=f"engagement {self._engagement_id} started — kill-chain run",
            payload={"engagement_id": self._engagement_id, "plan": [s.primary for s in self._plan]},
        )
        # Mirror the engagement to the autonomous_status snapshot so the
        # existing autonomous_status MCP tool reflects current work.
        try:
            _daemon_stats["current_objective"] = f"engage {self._target}"
            _daemon_stats["current_phase"] = "recon"
            _write_status()
        except Exception:
            pass

        results: List[Dict[str, Any]] = []
        shell_obtained = False

        for step in self._plan:
            try:
                _daemon_stats["current_phase"] = step.phase
                _write_status()
            except Exception:
                pass

            result = self._run_step(step)
            results.append({
                "phase":          result.step.phase,
                "label":          result.step.label,
                "command":        result.command_used,
                "switched_from":  result.switched_from,
                "success":        result.success,
                "skipped_reason": result.skipped_reason,
                "output_tail":    (result.output or "")[-400:],
            })

            self._shell.poll(target=self._target)
            if self._shell.detect_in_output(result.output, target=self._target):
                shell_obtained = True
                break

        try:
            _daemon_stats["current_objective"] = None
            _daemon_stats["current_phase"] = "idle"
            _write_status()
        except Exception:
            pass

        self._narrator.narrate(
            kind="ENGAGE_DONE",
            target=self._target,
            message=(
                f"engagement {self._engagement_id} finished — "
                f"{len(results)} steps, shell={shell_obtained}"
            ),
            payload={
                "engagement_id":  self._engagement_id,
                "shell_obtained": shell_obtained,
                "steps":          len(results),
            },
            severity="critical" if shell_obtained else "info",
        )

        return {
            "engagement_id":  self._engagement_id,
            "target":         self._target,
            "shell_obtained": shell_obtained,
            "steps":          results,
        }

    def _run_step(self, step: EnginePhaseStep) -> EnginePhaseResult:
        """Execute one phase step with approval, fallback, and narration."""
        approval = self._consult_gate(step)
        if approval is not None and not approval.is_approved:
            self._narrator.narrate(
                kind="STEP_DENIED",
                target=self._target,
                message=f"{step.primary} denied at {step.phase} — {approval.rationale}",
                payload={
                    "phase":    step.phase,
                    "command":  step.primary,
                    "approval": approval.rationale,
                },
                severity="warning",
            )
            return EnginePhaseResult(
                step=step,
                command_used=step.primary,
                output="",
                success=False,
                skipped_reason=f"denied: {approval.rationale}",
            )

        command = step.primary
        switched_from = ""
        attempt = 0
        last_output = ""

        while True:
            self._narrator.narrate(
                kind="STEP_START",
                target=self._target,
                message=f"{step.label} via {command}",
                payload={
                    "engagement_id": self._engagement_id,
                    "phase":         step.phase,
                    "command":       command,
                    "attempt":       attempt,
                },
            )
            try:
                output = self._execute(command, step.timeout_s)
            except Exception as exc:
                output = f"[runner error] {exc}"
            last_output = output

            success = self._step_succeeded(command, output)
            if success:
                self._narrator.narrate(
                    kind="STEP_DONE",
                    target=self._target,
                    message=f"{command} succeeded ({len(output)} bytes)",
                    payload={
                        "phase":         step.phase,
                        "command":       command,
                        "switched_from": switched_from,
                        "output_size":   len(output),
                    },
                )
                return EnginePhaseResult(
                    step=step,
                    command_used=command,
                    output=output,
                    success=True,
                    switched_from=switched_from,
                )

            self._narrator.narrate(
                kind="STEP_FAILED",
                target=self._target,
                message=f"{command} failed — searching fallback",
                payload={
                    "phase":   step.phase,
                    "command": command,
                    "attempt": attempt,
                    "tail":    output[-200:],
                },
                severity="warning",
            )

            if attempt >= self._max_switches:
                self._narrator.narrate(
                    kind="STEP_EXHAUSTED",
                    target=self._target,
                    message=f"{step.phase} fallbacks exhausted after {attempt} switches",
                    payload={"phase": step.phase, "primary": step.primary},
                    severity="warning",
                )
                return EnginePhaseResult(
                    step=step,
                    command_used=command,
                    output=last_output,
                    success=False,
                    switched_from=switched_from,
                    skipped_reason="fallbacks exhausted",
                )

            next_cmd = self._fallback.next_tool(command, step.phase, attempt)
            if not next_cmd:
                self._narrator.narrate(
                    kind="STEP_EXHAUSTED",
                    target=self._target,
                    message=f"no fallback available for {command}",
                    payload={"phase": step.phase, "primary": step.primary},
                    severity="warning",
                )
                return EnginePhaseResult(
                    step=step,
                    command_used=command,
                    output=last_output,
                    success=False,
                    switched_from=switched_from,
                    skipped_reason="no fallback",
                )

            self._narrator.narrate(
                kind="SWITCH_TOOL",
                target=self._target,
                message=f"switching {command} -> {next_cmd}",
                payload={
                    "phase":     step.phase,
                    "from":      command,
                    "to":        next_cmd,
                    "attempt":   attempt,
                },
                severity="warning",
            )
            switched_from = command if not switched_from else switched_from
            command = next_cmd
            attempt += 1

    def _consult_gate(self, step: EnginePhaseStep):
        """Ask the ApprovalGate; return None if no gate is wired."""
        if self._gate is None:
            return None
        try:
            return self._gate.request(
                target=self._target,
                phase=step.phase,
                command=step.primary,
                reason=f"engage step: {step.label}",
            )
        except Exception as exc:
            log.debug("approval gate error: %s", exc)
            return None

    def _execute(self, command: str, timeout_s: int) -> str:
        """Run command via the shell, injecting target into payload first."""
        full_cmd = f"assign rhost {self._target}\n{command}"
        return self._runner.run(full_cmd, timeout=timeout_s)

    @staticmethod
    def _step_succeeded(command: str, output: str) -> bool:
        """Heuristic success check — same shape used by _run_objective."""
        if not output:
            return False
        low = output.lower()
        failure_markers = (
            "error", "failed", "no such", "command not found",
            "traceback", "refused", "timeout",
        )
        success_markers = (
            "found", "success", "open", "hash", "discovered",
            "credential", "uid=", "started", "listening",
        )
        if any(m in low for m in success_markers):
            return True
        if any(m in low for m in failure_markers):
            return False
        return len(output.strip()) > 0


def _engage_run_sync(target: str, max_switches_per_step: int = 3) -> Dict[str, Any]:
    """Synchronous helper used by all engage entry points."""
    orch = EngageOrchestrator(
        target=target,
        max_switches_per_step=max_switches_per_step,
    )
    return orch.run()


def mcp_engage_target(
    target: str,
    max_switches_per_step: int = 3,
    detach: bool = True,
) -> str:
    """Public MCP / CLI entry point for the engage verb.

    Args:
        target: IPv4 dotted-quad or hostname to engage.
        max_switches_per_step: Maximum number of fallback tools per phase.
        detach: When True (default) the orchestrator runs in a background
                thread and the call returns immediately with the engagement
                id; the operator polls progress via lazyown_engage_status.
                When False the call blocks until the kill-chain finishes
                and returns the full summary JSON.

    Returns:
        JSON string with ``engagement_id`` and ``status`` (started|done)
        plus the full result payload when detach is False.
    """
    try:
        from engagement_hooks import is_valid_target as _ivt
        if not _ivt(target):
            return json.dumps({
                "status":  "error",
                "message": f"invalid target: {target!r}",
            })
    except Exception:
        return json.dumps({
            "status":  "error",
            "message": "engagement_hooks module unavailable",
        })

    if not detach:
        try:
            summary = _engage_run_sync(target, max_switches_per_step)
            return json.dumps({"status": "done", **summary}, indent=2, default=str)
        except Exception as exc:
            return json.dumps({"status": "error", "message": str(exc)})

    engagement_id = uuid.uuid4().hex[:8]

    def _worker() -> None:
        try:
            _engage_run_sync(target, max_switches_per_step)
        except Exception as exc:
            log.error("engage worker error: %s", exc)
            _emit("ENGAGE_WORKER_ERROR", {
                "engagement_id": engagement_id,
                "target":        target,
                "error":         str(exc),
            }, severity="critical")

    thread = threading.Thread(
        target=_worker,
        name=f"engage-{engagement_id}",
        daemon=True,
    )
    thread.start()

    return json.dumps({
        "status":         "started",
        "engagement_id":  engagement_id,
        "target":         target,
        "message":        (
            "Engagement started in background. "
            "Poll progress with lazyown_engage_status or read sessions/engagement.log."
        ),
    }, indent=2)


def mcp_engage_status(last_n: int = 20) -> str:
    """Return the last N lines of sessions/engagement.log plus pending approvals."""
    try:
        from engagement_hooks import ENGAGEMENT_LOG, list_pending_approvals
    except Exception:
        return json.dumps({"status": "error", "message": "engagement_hooks unavailable"})
    lines: List[str] = []
    if ENGAGEMENT_LOG.exists():
        try:
            raw = ENGAGEMENT_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
            lines = raw[-max(1, int(last_n)) :]
        except Exception as exc:
            return json.dumps({"status": "error", "message": str(exc)})
    pending = list_pending_approvals()
    return json.dumps({
        "status":           "ok",
        "lines":            lines,
        "pending_approvals": pending,
        "log_path":         str(ENGAGEMENT_LOG),
    }, indent=2, default=str)


def mcp_engage_approve(approval_id: str, decision: str, operator: str = "") -> str:
    """Resolve a pending approval. decision must be 'approved' or 'denied'."""
    try:
        from engagement_hooks import resolve_approval
    except Exception:
        return json.dumps({"status": "error", "message": "engagement_hooks unavailable"})
    ok = resolve_approval(approval_id, decision, operator)
    if not ok:
        return json.dumps({
            "status":  "error",
            "message": "invalid approval_id or decision (use approved|denied)",
        })
    return json.dumps({
        "status":      "ok",
        "approval_id": approval_id,
        "decision":    decision,
        "operator":    operator or "system",
    }, indent=2)


def mcp_engage_list_pending() -> str:
    """List every pending approval awaiting an operator decision."""
    try:
        from engagement_hooks import list_pending_approvals
    except Exception:
        return json.dumps({"status": "error", "message": "engagement_hooks unavailable"})
    pending = list_pending_approvals()
    return json.dumps({
        "status":  "ok",
        "count":   len(pending),
        "pending": pending,
    }, indent=2, default=str)


def cmd_engage(target: str, max_switches_per_step: int = 3, detach: bool = False) -> None:
    """CLI helper bound to the `engage <ip>` daemon subcommand."""
    result = mcp_engage_target(
        target=target,
        max_switches_per_step=max_switches_per_step,
        detach=detach,
    )
    print(result)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — Asyncio roles
# ─────────────────────────────────────────────────────────────────────────────

_daemon_stats: Dict[str, Any] = {
    "started_at":        None,
    "objectives_done":   0,
    "objectives_failed": 0,
    "steps_run":         0,
    "drones_spawned":    0,
    "events_emitted":    0,
    "current_objective": None,
    "current_phase":     "idle",
    "last_objective_ts": None,
}
_should_stop = threading.Event()


def _write_status() -> None:
    """Persist current daemon stats to STATUS_FILE."""
    try:
        STATUS_FILE.write_text(
            json.dumps({**_daemon_stats, "pid": os.getpid()}, indent=2, default=str)
        )
    except Exception:
        pass


# ── Role 1 — Objective Loop ───────────────────────────────────────────────────

async def objective_loop(
    max_steps: int,
    loop: asyncio.AbstractEventLoop,
) -> None:
    """
    Root autonomous loop: takes pending objectives from objectives.jsonl
    and executes them without waiting for Claude input between objectives.
    """
    if _ObjectiveStore is None:
        log.error("ObjectiveStore not available — objective_loop disabled")
        return

    store    = _ObjectiveStore()
    runner   = _build_default_runner()
    strategy = StrategyEngine(runner=runner)
    coord    = DroneCoordinator()

    world_model = _WorldModel() if _WorldModel else None
    obs_parser  = _ObsParser()  if _ObsParser  else None
    facts       = _FactStore()  if _FactStore   else None
    blocked_counts: Dict[str, int] = {}

    engine = ExecutionEngine(
        strategy=strategy,
        max_steps=max_steps,
        world_model=world_model,
        obs_parser=obs_parser,
        facts=facts,
        loop=loop,
    )

    log.info("objective_loop started (poll=%.1fs, max_steps=%d)", OBJ_POLL_S, max_steps)

    while not _should_stop.is_set():
        await asyncio.sleep(OBJ_POLL_S)

        try:
            obj = store.next_pending()
        except Exception as exc:
            log.debug("next_pending error: %s", exc)
            continue

        if obj is None:
            continue

        payload = _load_payload()
        target  = (
            obj.context.get("target", "")
            or obj.context.get("rhost", "")
            or payload.get("rhost", "127.0.0.1")
        )

        _daemon_stats["current_objective"] = obj.id
        _daemon_stats["current_phase"]     = "running"
        _daemon_stats["last_objective_ts"] = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
        _write_status()

        try:
            store.start(obj.id)
        except Exception:
            pass
        _update_task_status(obj.text, "Started")

        try:
            results = await engine.run_async(
                objective_id=obj.id,
                objective_text=obj.text,
                target=target,
            )
        except Exception as exc:
            log.error("objective %s failed: %s", obj.id, exc)
            _emit("OBJECTIVE_ERROR", {"id": obj.id, "error": str(exc)}, severity="error")
            try:
                store.block(obj.id, reason=str(exc))
            except Exception:
                pass
            _update_task_status(obj.text, "Blocked")
            _daemon_stats["objectives_failed"] += 1
            _daemon_stats["current_objective"]  = None
            _daemon_stats["current_phase"]      = "idle"
            _write_status()
            continue

        all_findings = [f for r in results for f in r.findings]
        drone_ids    = coord.process_findings(
            all_findings, target, obj.id,
            payload_key=payload.get("api_key", ""),
        )

        if _get_hive:
            try:
                hive    = _get_hive()
                summary = (
                    f"[AUTONOMOUS] objective={obj.text[:100]} target={target} "
                    f"steps={len(results)} findings={len(all_findings)}"
                )
                hive.memory.store(
                    content=summary,
                    agent_id="autonomous_daemon",
                    role="generic",
                    event_type="objective_result",
                )
            except Exception as exc:
                log.debug("hive store error: %s", exc)

        try:
            store.complete(obj.id)
        except Exception:
            pass
        _update_task_status(obj.text, "Done")

        _daemon_stats["objectives_done"]  += 1
        _daemon_stats["steps_run"]        += len(results)
        _daemon_stats["drones_spawned"]   += len(drone_ids)
        _daemon_stats["current_objective"] = None
        _daemon_stats["current_phase"]     = "idle"
        _write_status()

        log.info("[%s] completed — %d steps, %d findings, %d drones",
                 obj.id, len(results), len(all_findings), len(drone_ids))


# ── Role 2 — WorldModel Watcher ───────────────────────────────────────────────

async def world_model_watcher(loop: asyncio.AbstractEventLoop) -> None:
    """
    Watch world_model.json. When the phase changes, new hosts appear,
    new service versions are found, or active beacons are detected,
    auto-inject derived objectives.
    """
    wm_file   = SESSIONS_DIR / "world_model.json"
    last_snap: Dict = {}
    _seen_service_versions: set = set()
    _seen_beacon_ips: set = set()

    if _ObjectiveStore is None:
        return

    store = _ObjectiveStore()
    log.info("world_model_watcher started (poll=%.1fs)", WM_POLL_S)

    while not _should_stop.is_set():
        await asyncio.sleep(WM_POLL_S)

        if not wm_file.exists():
            continue

        try:
            snap = json.loads(wm_file.read_text())
        except Exception:
            continue

        if snap == last_snap:
            continue

        prev_hosts = set(last_snap.get("hosts", {}).keys())
        curr_hosts = set(snap.get("hosts", {}).keys())
        new_hosts  = curr_hosts - prev_hosts
        for host in new_hosts:
            text = f"Enumerate newly discovered host {host}"
            try:
                obj = store.inject(
                    text=text, priority="high",
                    source="world_model_watcher",
                    context={"target": host},
                )
                task_id = _inject_to_tasks_json(
                    title=text,
                    description=f"Auto-injected by WorldModelWatcher | objective_id={obj.id}",
                    operator="world_model_watcher",
                    status="New",
                )
                _emit("OBJECTIVE_AUTO_INJECTED", {
                    "text": text, "trigger": "new_host", "host": host, "task_id": task_id,
                })
            except Exception as exc:
                log.debug("inject error: %s", exc)

        prev_creds = len(last_snap.get("credentials", []))
        curr_creds = len(snap.get("credentials", []))
        if curr_creds > prev_creds:
            new_count = curr_creds - prev_creds
            creds     = snap.get("credentials", [])[-new_count:]
            for cred in creds:
                cred_str = json.dumps(cred)[:80]
                text     = f"Leverage new credential: {cred_str}"
                try:
                    obj = store.inject(
                        text=text, priority="critical",
                        source="world_model_watcher",
                        context={"credential": cred},
                    )
                    task_id = _inject_to_tasks_json(
                        title=text,
                        description=f"Credential detected automatically | objective_id={obj.id}",
                        operator="world_model_watcher",
                        status="New",
                    )
                    _emit("OBJECTIVE_AUTO_INJECTED", {
                        "text": text, "trigger": "new_credential", "task_id": task_id,
                    }, severity="warning")
                except Exception:
                    pass

        prev_phase = last_snap.get("phase", "")
        curr_phase = snap.get("phase", "")
        if curr_phase and curr_phase != prev_phase:
            _emit("PHASE_CHANGE", {"from": prev_phase, "to": curr_phase})
            _daemon_stats["current_phase"] = curr_phase

        # ── Auto-CVE: inject CVE-search objectives for new service versions ──
        for host, hdata in snap.get("hosts", {}).items():
            for port, svc in hdata.get("services", {}).items():
                version  = svc.get("version", "")
                svc_name = svc.get("name", "")
                if not version or not svc_name:
                    continue
                ver_key = f"{host}:{port}:{svc_name}:{version}"
                if ver_key in _seen_service_versions:
                    continue
                _seen_service_versions.add(ver_key)
                text = f"Search CVEs for {svc_name} {version} on {host}:{port}"
                try:
                    obj = store.inject(
                        text=text, priority="medium",
                        source="world_model_watcher",
                        context={"target": host, "service": svc_name, "version": version},
                    )
                    _inject_to_tasks_json(
                        title=text,
                        description=f"Auto CVE search | objective_id={obj.id}",
                        operator="world_model_watcher",
                        status="New",
                    )
                    _emit("OBJECTIVE_AUTO_INJECTED", {
                        "text": text, "trigger": "new_service_version",
                        "host": host, "service": svc_name, "version": version,
                    })
                    log.info("WMWatcher: CVE objective injected for %s %s", svc_name, version)
                except Exception as exc:
                    log.debug("CVE inject error: %s", exc)

        # ── Beacon integration: inject post-exploit objectives for active beacons ──
        beacons_file = SESSIONS_DIR / "beacons.json"
        if beacons_file.exists():
            try:
                beacons = json.loads(beacons_file.read_text())
                if isinstance(beacons, list):
                    for beacon in beacons:
                        beacon_ip = (
                            beacon.get("ip", "")
                            or beacon.get("host", "")
                            or beacon.get("client_id", "")
                        )
                        if not beacon_ip or beacon_ip in _seen_beacon_ips:
                            continue
                        _seen_beacon_ips.add(beacon_ip)
                        text = f"Post-exploit active C2 beacon on {beacon_ip}"
                        try:
                            obj = store.inject(
                                text=text, priority="high",
                                source="beacon_watcher",
                                context={"target": beacon_ip},
                            )
                            _inject_to_tasks_json(
                                title=text,
                                description=f"Active beacon detected | objective_id={obj.id}",
                                operator="beacon_watcher",
                                status="New",
                            )
                            _emit("OBJECTIVE_AUTO_INJECTED", {
                                "text": text, "trigger": "active_beacon", "host": beacon_ip,
                            }, severity="warning")
                            log.info("WMWatcher: post-exploit objective for beacon %s", beacon_ip)
                        except Exception as exc:
                            log.debug("beacon inject error: %s", exc)
            except Exception as exc:
                log.debug("beacons.json read error: %s", exc)

        last_snap = snap


# ── Role 3 — Heartbeat ────────────────────────────────────────────────────────

async def heartbeat_loop() -> None:
    """Emit heartbeat and write status every HEARTBEAT_S seconds."""
    while not _should_stop.is_set():
        await asyncio.sleep(HEARTBEAT_S)
        _daemon_stats["events_emitted"] += 1
        _emit("HEARTBEAT", {
            "pid":               os.getpid(),
            "objectives_done":   _daemon_stats["objectives_done"],
            "steps_run":         _daemon_stats["steps_run"],
            "drones_spawned":    _daemon_stats["drones_spawned"],
            "current_phase":     _daemon_stats["current_phase"],
            "current_objective": _daemon_stats["current_objective"],
        })
        _write_status()
        log.info("heartbeat — done=%d steps=%d drones=%d",
                 _daemon_stats["objectives_done"],
                 _daemon_stats["steps_run"],
                 _daemon_stats["drones_spawned"])


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 — Main asyncio entry point
# ─────────────────────────────────────────────────────────────────────────────

async def _main_async(max_steps: int = MAX_STEPS_DEFAULT) -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    _daemon_stats["started_at"] = datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat()
    _write_status()

    loop = asyncio.get_event_loop()

    _emit("DAEMON_START", {
        "pid":         os.getpid(),
        "max_steps":   max_steps,
        "hive_backend": HIVE_BACKEND,
    })

    tasks = [
        asyncio.create_task(objective_loop(max_steps, loop),   name="objective_loop"),
        asyncio.create_task(world_model_watcher(loop),         name="world_model_watcher"),
        asyncio.create_task(heartbeat_loop(),                  name="heartbeat"),
    ]

    log.info("LazyOwn autonomous daemon started (pid=%d max_steps=%d)",
             os.getpid(), max_steps)

    ev_loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        ev_loop.add_signal_handler(
            sig, lambda: [_should_stop.set(), *[t.cancel() for t in tasks]]
        )

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        log.info("daemon stopped")
    finally:
        _emit("DAEMON_STOP", {"pid": os.getpid()})
        STATUS_FILE.write_text(
            json.dumps({"status": "stopped", "pid": os.getpid()}, indent=2)
        )
        _clear_pid()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 — PID management + CLI
# ─────────────────────────────────────────────────────────────────────────────

def _write_pid() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))


def _clear_pid() -> None:
    if PID_FILE.exists():
        PID_FILE.unlink()


def _read_pid() -> Optional[int]:
    try:
        return int(PID_FILE.read_text().strip())
    except Exception:
        return None


def _is_running() -> Tuple[bool, int]:
    pid = _read_pid()
    if pid is None:
        return False, 0
    try:
        os.kill(pid, 0)
        return True, pid
    except (ProcessLookupError, PermissionError):
        return False, 0


def cmd_run(max_steps: int = MAX_STEPS_DEFAULT) -> None:
    """Run daemon in foreground (debug mode)."""
    _write_pid()
    try:
        asyncio.run(_main_async(max_steps))
    finally:
        _clear_pid()


def cmd_start(max_steps: int = MAX_STEPS_DEFAULT) -> None:
    """Fork, detach, and run daemon in background."""
    running, pid = _is_running()
    if running:
        print(f"[auto] already running (pid={pid})")
        sys.exit(1)

    child = os.fork()
    if child > 0:
        print(f"[auto] started in background (pid={child})")
        sys.exit(0)

    os.setsid()
    grandchild = os.fork()
    if grandchild > 0:
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()
    with open(os.devnull, "r") as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    log_path = SESSIONS_DIR / "autonomous_daemon.log"
    with open(log_path, "a") as logf:
        os.dup2(logf.fileno(), sys.stdout.fileno())
        os.dup2(logf.fileno(), sys.stderr.fileno())

    _write_pid()
    asyncio.run(_main_async(max_steps))


def cmd_stop() -> None:
    """Send SIGTERM to the running daemon."""
    running, pid = _is_running()
    if not running:
        print("[auto] not running")
        sys.exit(1)
    os.kill(pid, signal.SIGTERM)
    print(f"[auto] SIGTERM sent to pid={pid}")
    for _ in range(50):
        time.sleep(0.1)
        alive, _ = _is_running()
        if not alive:
            print("[auto] stopped")
            return
    print("[auto] still running after 5s — use SIGKILL manually")


def cmd_status() -> None:
    """Print current daemon status to stdout."""
    running, pid = _is_running()
    state = "running" if running else "stopped"
    print(f"[auto] {state}" + (f" (pid={pid})" if running else ""))
    if STATUS_FILE.exists():
        try:
            data = json.loads(STATUS_FILE.read_text())
            for k, v in data.items():
                print(f"  {k}: {v}")
        except Exception:
            print("  (status file unreadable)")
    else:
        print("  (no status yet)")


def cmd_inject(text: str, priority: str = "high") -> None:
    """Inject an objective from the CLI."""
    if _ObjectiveStore is None:
        print("[auto] ObjectiveStore not available")
        sys.exit(1)
    store   = _ObjectiveStore()
    obj     = store.inject(text=text, priority=priority, source="cli")
    task_id = _inject_to_tasks_json(
        title=text,
        description=f"Injected by CLI | objective_id={obj.id}",
        operator="cli",
        status="New",
    )
    print(f"[auto] objective injected: [{obj.id}] {obj.text[:80]}")
    print(f"[auto] task.json id={task_id} — visible in /tasks on the C2")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 11 — Public API for lazyown_mcp.py
# ─────────────────────────────────────────────────────────────────────────────

_daemon_thread: Optional[threading.Thread] = None
_daemon_loop:   Optional[asyncio.AbstractEventLoop] = None


def mcp_autonomous_start(
    max_steps: int = MAX_STEPS_DEFAULT,
    backend: str = HIVE_BACKEND,
) -> str:
    """Start the autonomous daemon in a background thread (for MCP calls)."""
    global _daemon_thread, _daemon_loop, HIVE_BACKEND

    if _daemon_thread and _daemon_thread.is_alive():
        return json.dumps({"status": "already_running",
                           "message": "The autonomous daemon is already active"})

    HIVE_BACKEND = backend
    _should_stop.clear()
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    def _run():
        global _daemon_loop
        _daemon_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_daemon_loop)
        try:
            _daemon_loop.run_until_complete(_main_async(max_steps))
        finally:
            _daemon_loop.close()

    _daemon_thread = threading.Thread(target=_run, name="autonomous_daemon", daemon=True)
    _daemon_thread.start()

    _emit("DAEMON_START_MCP", {"max_steps": max_steps, "backend": backend})
    return json.dumps({
        "status":    "started",
        "max_steps": max_steps,
        "backend":   backend,
        "message":   (
            "Autonomous daemon active. Inject objectives with lazyown_autonomous_inject. "
            "Monitor with lazyown_autonomous_status. "
            "Read events in sessions/autonomous_events.jsonl"
        ),
    }, indent=2)


def mcp_autonomous_stop() -> str:
    """Stop the autonomous daemon."""
    global _daemon_thread
    _should_stop.set()

    if _daemon_loop and _daemon_loop.is_running():
        for task in asyncio.all_tasks(_daemon_loop):
            task.cancel()

    if _daemon_thread:
        _daemon_thread.join(timeout=5.0)

    _emit("DAEMON_STOP_MCP", {"message": "Stopped via MCP"})
    return json.dumps({"status": "stopped", "message": "Autonomous daemon stopped"})


def mcp_autonomous_status() -> str:
    """Current daemon state: objectives, steps, drones, phase."""
    alive = bool(_daemon_thread and _daemon_thread.is_alive())
    data  = {**_daemon_stats, "running": alive}
    if STATUS_FILE.exists():
        try:
            disk = json.loads(STATUS_FILE.read_text())
            data.update(disk)
        except Exception:
            pass
    return json.dumps(data, indent=2, default=str)


def mcp_autonomous_inject(
    text: str,
    priority: str = "high",
    target: str = "",
) -> str:
    """Inject an objective into the daemon queue and into sessions/tasks.json."""
    if _ObjectiveStore is None:
        return "[auto] ObjectiveStore not available"
    store = _ObjectiveStore()
    ctx   = {"target": target} if target else {}
    obj   = store.inject(text=text, priority=priority, source="mcp_claude", context=ctx)

    task_id = _inject_to_tasks_json(
        title=text,
        description=(
            f"Autonomous objective — priority={priority}"
            + (f" target={target}" if target else "")
            + f" | objective_id={obj.id}"
        ),
        operator="autonomous_daemon",
        status="New",
    )

    _emit("OBJECTIVE_INJECTED_MCP", {
        "id": obj.id, "text": text[:200], "priority": priority, "task_id": task_id,
    })
    return json.dumps({
        "id":       obj.id,
        "text":     obj.text,
        "priority": obj.priority,
        "status":   obj.status,
        "task_id":  task_id,
    }, indent=2)


def mcp_autonomous_events(last_n: int = 20) -> str:
    """Read the last N events from autonomous_events.jsonl."""
    if not EVENTS_FILE.exists():
        return "No events yet. Start the daemon with lazyown_autonomous_start."
    try:
        lines  = EVENTS_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
        last   = lines[-last_n:]
        events = []
        for line in last:
            try:
                events.append(json.loads(line))
            except Exception:
                pass
        if not events:
            return "No readable events."
        out = []
        for e in events:
            ts  = e.get("ts", "")[:19]
            typ = e.get("type", "?")
            pay = e.get("payload", {})
            out.append(f"[{ts}] {typ}: {json.dumps(pay, default=str)[:120]}")
        return "\n".join(out)
    except Exception as exc:
        return f"[events error] {exc}"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 12 — CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def _dispatch_pipeline(args: "argparse.Namespace") -> None:
    """Daemon-side pipeline subcommand handler.

    Lazy-imports modules.pipeline_engine so the daemon starts even when
    PyYAML is missing in non-pipeline workflows.
    """
    try:
        sys.path.insert(0, str(MODULES_DIR))
        from pipeline_engine import cmd_pipeline as _pl_cmd
    except Exception as exc:
        print(json.dumps({
            "status":  "error",
            "message": f"pipeline_engine import failed: {exc}",
        }))
        return
    _pl_cmd(
        action=args.action,
        name=getattr(args, "name", "") or "",
        target=getattr(args, "target", "") or "",
        background=bool(getattr(args, "background", False)),
    )


_COMMANDS = {
    "run":    lambda args: cmd_run(int(args.max_steps)),
    "start":  lambda args: cmd_start(int(args.max_steps)),
    "stop":   lambda _: cmd_stop(),
    "status": lambda _: cmd_status(),
    "inject": lambda args: cmd_inject(args.text, args.priority),
    "engage": lambda args: cmd_engage(
        target=args.target,
        max_switches_per_step=int(args.max_switches),
        detach=bool(args.background),
    ),
    "pipeline": _dispatch_pipeline,
}

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LazyOwn Autonomous Daemon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    for _cmd in ("run", "start"):
        p = sub.add_parser(_cmd)
        p.add_argument("--max-steps", default=MAX_STEPS_DEFAULT,
                       help="Maximum steps per objective")

    sub.add_parser("stop")
    sub.add_parser("status")

    p_inj = sub.add_parser("inject")
    p_inj.add_argument("text")
    p_inj.add_argument("--priority", default="high",
                       choices=["low", "medium", "high", "critical"])

    p_eng = sub.add_parser(
        "engage",
        help="Drive one target through the full kill-chain (ping->nmap->enum->exploit).",
    )
    p_eng.add_argument("target", help="Target IPv4 or hostname.")
    p_eng.add_argument(
        "--max-switches",
        default=3,
        dest="max_switches",
        help="Maximum fallback tools tried per phase before giving up.",
    )
    p_eng.add_argument(
        "--background",
        action="store_true",
        help="Run the engagement in a background thread and return immediately.",
    )

    p_pl = sub.add_parser(
        "pipeline",
        help="Run a declarative YAML pipeline (Pillar 3 composition layer).",
    )
    p_pl.add_argument(
        "action",
        choices=["list", "validate", "show", "run", "status"],
        help="Pipeline action.",
    )
    p_pl.add_argument("name", nargs="?", default="", help="Pipeline name.")
    p_pl.add_argument(
        "--target", default="", help="Optional target override for pipeline run.",
    )
    p_pl.add_argument(
        "--background", action="store_true",
        help="Detach the pipeline into a background worker thread.",
    )

    parsed = parser.parse_args()
    if parsed.cmd in _COMMANDS:
        _COMMANDS[parsed.cmd](parsed)
    else:
        parser.print_help()
