#!/usr/bin/env python3
"""
skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon
==================================================================
Cierra la brecha entre LazyOwn (orquestador asistido por Claude) y un sistema
OpenClaw/OpenHands completamente autónomo.

El daemon corre como proceso independiente y NO necesita a Claude Code para
operar entre objetivos. Claude sigue siendo la Reina Borg para inyectar
objetivos de alto nivel, pero el daemon los ejecuta sin intervención.

Arquitectura (4 roles asyncio concurrentes)
--------------------------------------------
  Role 1 — ObjectiveLoop    : Observa objectives.jsonl → cuando aparece uno
                              pending, lo toma, planifica y ejecuta.
  Role 2 — ExecutionEngine  : Loop de ejecución por pasos (equivalente al
                              auto_loop del MCP pero sin MCP). Usa la misma
                              cascada de selección de comandos:
                              reactive → parquet → bridge → LLM → fallback
  Role 3 — WorldModelWatcher: Observa world_model.json. Cuando cambia la fase
                              (recon→enum→exploit…) o aparecen nuevos hosts/
                              credenciales, inyecta objetivos derivados y
                              notifica a los drones del hive.
  Role 4 — DroneCoordinator : Puente hive-mind. Cuando recon descubre un host,
                              lanza drones exploit/analyze en paralelo.
                              Cuando un drone termina, escribe el resultado al
                              stream y actualiza el objetivo.

Streams de eventos (push, no polling)
--------------------------------------
  sessions/autonomous_events.jsonl  — cada acción, hallazgo, decisión
  sessions/autonomous_status.json   — estado en tiempo real del daemon

Gestión
--------
  python3 skills/autonomous_daemon.py start   # fork y detach
  python3 skills/autonomous_daemon.py stop    # terminar por PID
  python3 skills/autonomous_daemon.py run     # foreground (debug)
  python3 skills/autonomous_daemon.py status  # leer estado
  python3 skills/autonomous_daemon.py inject "Objetivo" [--priority high]

Integración MCP
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
import signal
import subprocess
import sys
import threading
import time
import uuid
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

# ── Archivos de estado ─────────────────────────────────────────────────────────

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

# ── Imports opcionales ────────────────────────────────────────────────────────

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
# SECCIÓN 1 — Event Stream (push de eventos en tiempo real)
# ─────────────────────────────────────────────────────────────────────────────

_stream_lock = threading.Lock()

_tasks_lock = threading.Lock()

def _update_task_status(title: str, new_status: str) -> bool:
    """Actualiza el status de la primera task cuyo título coincida. Thread-safe."""
    with _tasks_lock:
        try:
            if not TASKS_FILE.exists():
                return False
            tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
            changed = False
            for t in tasks:
                if t.get("title", "")[:80] == title[:80]:
                    t["status"] = new_status
                    changed = True
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
    Escribe directamente en sessions/tasks.json con el formato del C2 (lazyc2.py).
    Devuelve el id asignado. Thread-safe.
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
    """Escribe un evento al stream JSONL. Thread-safe."""
    event = {
        "id":        uuid.uuid4().hex[:8],
        "ts":        datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "type":      event_type,
        "severity":  severity,
        "payload":   payload,
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
# SECCIÓN 2 — Ejecución de comandos LazyOwn
# ─────────────────────────────────────────────────────────────────────────────

def _load_payload() -> Dict:
    try:
        return json.loads(PAYLOAD_FILE.read_text())
    except Exception:
        return {}


def _run_lazyown(command: str, timeout: int = STEP_TIMEOUT_S) -> str:
    """
    Ejecuta un comando LazyOwn usando PTY (igual que _run_lazyown_command del MCP).
    Intenta primero importar la función del MCP; si falla, replica la lógica con PTY.
    """
    # Opción 1: reusar la función del MCP directamente (evita duplicar lógica)
    try:
        from lazyown_mcp import _run_lazyown_command
        return _run_lazyown_command(command, timeout)
    except ImportError:
        pass

    # Opción 2: PTY propio (réplica de _run_lazyown_command sin dependencia del MCP)
    import fcntl, pty, select, struct, termios
    cmd_input = (command.strip() + "\nexit\n").encode()

    run_script = LAZYOWN_DIR / "run"
    argv = (["bash", str(run_script)] if run_script.is_file()
            else [sys.executable, "-W", "ignore", str(LAZYOWN_DIR / "lazyown.py")])

    env = os.environ.copy()
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

        import re
        raw = "".join(chunks)
        return re.sub(r"\x1b\[[0-9;]*[mGKH]", "", raw).strip()

    except Exception as exc:
        return f"[run error] {exc}"


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3 — StrategyEngine (selección de comando con cascada)
# ─────────────────────────────────────────────────────────────────────────────

# Mapa estático de categoría → comando fallback
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

# Fase → categorías que aplican en orden
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
    command:  str
    args:     str = ""
    source:   str = "fallback"   # reactive|parquet|bridge|llm|fallback
    reason:   str = ""
    mitre:    str = ""
    priority: int = 5


class StrategyEngine:
    """
    Decide el próximo comando para un (target, phase) dado.
    Cascada idéntica a lazyown_mcp.py auto_loop:
      1. Reactive engine (si hay decisión pendiente de alta prioridad)
      2. Parquet (comandos exitosos en sesiones anteriores)
      3. Bridge catalog (comandos del catálogo para la fase/servicios)
      4. LLM (Groq/Ollama si disponible)
      5. Fallback estático
    """

    def __init__(self) -> None:
        self._pdb        = _get_pdb() if _get_pdb else None
        self._dispatcher = _get_dispatcher() if _get_dispatcher else None
        self._reactive   = _ReactEngine() if _ReactEngine else None
        self._fail_counts: Dict[str, int] = {}
        self._reactive_pending: Optional[CommandDecision] = None

    def register_output(
        self,
        output: str,
        command: str,
        platform: str = "linux",
        success: bool = True,
    ) -> None:
        """Alimenta el reactive engine con el output del último comando."""
        if not success:
            key = command.split()[0] if command else command
            self._fail_counts[key] = self._fail_counts.get(key, 0) + 1

        if self._reactive is None:
            return
        try:
            decisions = self._reactive.analyse(
                output=output, command=command, platform=platform,
            )
            if decisions:
                top = decisions[0]
                if top.priority <= 2:
                    self._reactive_pending = CommandDecision(
                        command=top.command,
                        source="reactive",
                        reason=top.reason,
                        priority=top.priority,
                    )
        except Exception as exc:
            log.debug("reactive engine error: %s", exc)

    def next_command(
        self,
        target: str,
        phase: str,
        services: Optional[List[str]] = None,
    ) -> CommandDecision:
        categories = _PHASE_CATEGORIES.get(phase, ["other"])

        # 1. Reactive engine
        if self._reactive_pending:
            dec = self._reactive_pending
            self._reactive_pending = None
            return dec

        # 2. Parquet — comandos exitosos del pasado
        for cat in categories:
            cand = self._parquet_candidate(cat, target)
            if cand:
                return CommandDecision(command=cand, source="parquet",
                                       reason=f"past success in {cat}")

        # 3. Bridge catalog
        for cat in categories:
            cand = self._bridge_candidate(phase, services or [], cat)
            if cand:
                return cand

        # 4. LLM (skip para mantener el daemon sin API calls costosos por defecto)
        # (se puede habilitar con AUTO_USE_LLM=1)
        if os.environ.get("AUTO_USE_LLM", "0") == "1":
            cand = self._llm_candidate(target, phase)
            if cand:
                return cand

        # 5. Fallback estático
        cmd = _FALLBACK_MAP.get(categories[0], "list")
        return CommandDecision(command=cmd, source="fallback",
                               reason=f"static map for {categories[0]}")

    def _parquet_candidate(self, category: str, target: str) -> Optional[str]:
        if self._pdb is None:
            return None
        try:
            rows = self._pdb.query_session(
                phase=category, target=target, success_only=True, limit=30
            )
            freq: Dict[str, int] = {}
            for r in rows:
                cmd = (r.get("command") or "").strip().split()[0]
                if cmd and not cmd.startswith("/") and not cmd.startswith("echo"):
                    fail_n = self._fail_counts.get(cmd, 0)
                    if fail_n < MAX_FAILS_PER_CMD:
                        freq[cmd] = freq.get(cmd, 0) + 1
            return max(freq, key=lambda c: freq[c]) if freq else None
        except Exception:
            return None

    def _bridge_candidate(
        self, phase: str, services: List[str], tag: str = ""
    ) -> Optional[CommandDecision]:
        if self._dispatcher is None:
            return None
        try:
            result = self._dispatcher.suggest(
                phase=phase, services=services, tag_hint=tag, os_hint="any",
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

    def _llm_candidate(self, target: str, phase: str) -> Optional[CommandDecision]:
        try:
            from lazyown_llm import LLMBridge
            payload  = _load_payload()
            api_key  = payload.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
            if not api_key:
                return None
            bridge = LLMBridge(backend="groq", api_key=api_key)
            answer = bridge.ask(
                goal=(
                    f"Suggest ONE LazyOwn shell command for phase='{phase}' "
                    f"target='{target}'. Reply with ONLY the command name, "
                    "no explanation."
                ),
                max_iterations=1,
            )
            cmd = answer.strip().split()[0] if answer.strip() else None
            if cmd:
                return CommandDecision(command=cmd, source="llm",
                                       reason="LLM recommendation", priority=4)
        except Exception as exc:
            log.debug("LLM candidate error: %s", exc)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4 — ExecutionEngine (loop de pasos para un objetivo)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class StepResult:
    step:     int
    command:  str
    output:   str
    success:  bool
    source:   str
    findings: List[Dict] = field(default_factory=list)
    phase:    str = ""


async def _run_objective(
    objective_id: str,
    objective_text: str,
    target: str,
    max_steps: int,
    strategy: StrategyEngine,
    world_model: Any,           # WorldModel instance or None
    obs_parser: Any,            # ObsParser instance or None
    facts: Any,                 # FactStore instance or None
    loop: asyncio.AbstractEventLoop,
) -> List[StepResult]:
    """
    Ejecuta un objetivo autónomamente: selecciona comandos, los ejecuta,
    parsea el output, actualiza el world model, y emite eventos.
    Devuelve la lista de StepResult al completar.
    """
    log.info("▶  [%s] inicio: %s", objective_id, objective_text[:80])
    _emit("OBJECTIVE_START", {
        "id": objective_id, "text": objective_text[:200], "target": target,
    })

    results: List[StepResult] = []
    phase   = "recon"
    services: List[str] = []

    if world_model is not None:
        try:
            phase = world_model.get_phase().value
        except Exception:
            pass

    for step_n in range(1, max_steps + 1):
        # Seleccionar próximo comando
        decision = strategy.next_command(target, phase, services)
        # Sustituir placeholder de IP
        command  = decision.command.replace("{rhost}", target).replace("TARGET", target)
        full_cmd = f"set rhost {target}\n{command}"

        log.info("  step %d/%d [%s] %s", step_n, max_steps, decision.source, command)
        _emit("STEP_START", {
            "objective_id": objective_id,
            "step": step_n, "command": command,
            "source": decision.source, "reason": decision.reason,
        })

        # Ejecutar en executor para no bloquear el loop asyncio
        output = await loop.run_in_executor(
            None, _run_lazyown, full_cmd, STEP_TIMEOUT_S,
        )

        # Detectar éxito heurístico
        low = output.lower()
        failed = any(k in low for k in (
            "error", "failed", "no such", "command not found",
            "traceback", "refused", "timeout",
        )) and not any(k in low for k in ("found", "success", "open", "hash"))
        success = not failed

        # Parsear hallazgos
        findings: List[Dict] = []
        if obs_parser is not None:
            try:
                obs = obs_parser.parse(output, host=target, tool=command.split()[0])
                findings = [asdict(f) for f in obs.findings] if obs.findings else []
                # Actualizar world model y persistir a disco
                if world_model is not None:
                    world_model.update_from_findings(obs.findings)
                    try:
                        phase = world_model.get_phase().value
                    except Exception:
                        pass
                    # Guardar snapshot a world_model.json para que WorldModelWatcher lo vea
                    try:
                        wm_file = SESSIONS_DIR / "world_model.json"
                        wm_file.write_text(
                            json.dumps(world_model.snapshot(), indent=2, default=str),
                            encoding="utf-8",
                        )
                    except Exception as wm_err:
                        log.debug("world_model.json write error: %s", wm_err)
                # Extraer servicios descubiertos
                for f in obs.findings:
                    svc = getattr(f, "service", None)
                    if svc and svc not in services:
                        services.append(svc)
            except Exception as exc:
                log.debug("obs_parser error: %s", exc)

        # Actualizar facts
        if facts is not None and success:
            try:
                facts.ingest_text(output, source=command, target=target)
            except Exception:
                pass

        # Registrar en strategy engine para adaptar decisiones futuras
        strategy.register_output(
            output, command,
            platform=("windows" if world_model is None else
                      world_model.snapshot().get("hosts", {}).get(target, {}).get("os", "linux")),
            success=success,
        )

        sr = StepResult(
            step=step_n, command=command, output=output,
            success=success, source=decision.source,
            findings=findings, phase=phase,
        )
        results.append(sr)

        _emit("STEP_DONE", {
            "objective_id": objective_id,
            "step": step_n, "command": command,
            "success": success, "phase": phase,
            "findings_count": len(findings),
            "output_snippet": output[:300],
        }, severity="warning" if not success else "info")

        # Condición de parada: hallazgos de alto valor
        high_value = any(
            getattr(f, "type", "") in ("credential", "hash", "root_shell", "privesc")
            for f in (obs_parser.parse(output, host=target, tool=command).findings
                      if obs_parser else [])
        )
        if high_value:
            log.info("  ★  High-value finding — deteniendo loop temprano")
            _emit("HIGH_VALUE", {
                "objective_id": objective_id,
                "step": step_n, "command": command,
            }, severity="critical")
            break

        # Pausa entre pasos
        await asyncio.sleep(STEP_DELAY_S)

    _emit("OBJECTIVE_DONE", {
        "id": objective_id,
        "steps_run": len(results),
        "final_phase": phase,
        "findings_total": sum(len(r.findings) for r in results),
    })
    return results


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5 — DroneCoordinator (hive mind integration en tiempo real)
# ─────────────────────────────────────────────────────────────────────────────

class DroneCoordinator:
    """
    Observa los resultados del execution engine y lanza drones Groq/Ollama
    cuando detecta eventos que merecen análisis paralelo:
      - Nuevo host descubierto → drone recon
      - Servicio explotable detectado → drone exploit
      - Hash/credencial encontrada → drone cred
    """

    def __init__(self) -> None:
        self._hive   = _get_hive() if _get_hive else None
        self._seen_hosts: set = set()
        self._lock   = threading.Lock()

    def process_findings(
        self,
        findings: List[Dict],
        target: str,
        objective_id: str,
        payload_key: str = "",
    ) -> List[str]:
        """Lanza drones para hallazgos relevantes. Devuelve lista de drone_ids."""
        if self._hive is None:
            return []

        drone_ids: List[str] = []

        for f in findings:
            ftype   = f.get("type", "")
            value   = f.get("value", "")
            service = f.get("service", "")

            # Nuevo host/IP → drone recon (FindingType.IP = 'ip')
            if ftype in ("host", "ip") and value not in self._seen_hosts:
                with self._lock:
                    if value not in self._seen_hosts:
                        self._seen_hosts.add(value)
                goal = f"Enumerate new host {value} discovered during {objective_id}"
                did  = self._hive.spawn(goal=goal, role="recon",
                                        backend=HIVE_BACKEND,
                                        max_iterations=HIVE_MAX_ITER)
                drone_ids.append(did)
                _emit("DRONE_SPAWNED", {
                    "drone_id": did, "role": "recon",
                    "trigger": "new_host", "host": value,
                    "objective_id": objective_id,
                })
                log.info("  🤖 drone recon spawned for new host %s → %s", value, did)

            # Servicio explotable → drone exploit
            elif ftype in ("service_version", "cve") and service:
                fail_key = f"exploit:{service}:{target}"
                goal = (f"Exploit {service} on {target} "
                        f"(context: {objective_id}, finding: {value[:60]})")
                did  = self._hive.spawn(goal=goal, role="exploit",
                                        backend=HIVE_BACKEND,
                                        max_iterations=HIVE_MAX_ITER)
                drone_ids.append(did)
                _emit("DRONE_SPAWNED", {
                    "drone_id": did, "role": "exploit",
                    "trigger": ftype, "service": service, "value": str(value)[:80],
                    "objective_id": objective_id,
                })
                log.info("  🤖 drone exploit spawned for %s → %s", service, did)

            # Credencial/hash → drone cred
            elif ftype in ("credential", "hash"):
                goal = (f"Crack and use credential found on {target}: {str(value)[:80]} "
                        f"(context: {objective_id})")
                did  = self._hive.spawn(goal=goal, role="cred",
                                        backend=HIVE_BACKEND,
                                        max_iterations=HIVE_MAX_ITER)
                drone_ids.append(did)
                _emit("DRONE_SPAWNED", {
                    "drone_id": did, "role": "cred",
                    "trigger": ftype, "value": str(value)[:40],
                    "objective_id": objective_id,
                })
                log.info("  🤖 drone cred spawned → %s", did)

        return drone_ids


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 6 — Roles asyncio
# ─────────────────────────────────────────────────────────────────────────────

# Estado global del daemon
_daemon_stats: Dict[str, Any] = {
    "started_at":       None,
    "objectives_done":  0,
    "objectives_failed":0,
    "steps_run":        0,
    "drones_spawned":   0,
    "events_emitted":   0,
    "current_objective":None,
    "current_phase":    "idle",
    "last_objective_ts":None,
}
_should_stop = threading.Event()


def _write_status() -> None:
    try:
        STATUS_FILE.write_text(
            json.dumps({**_daemon_stats, "pid": os.getpid()},
                       indent=2, default=str)
        )
    except Exception:
        pass


# ── Role 1 — Objective Loop ───────────────────────────────────────────────────

async def objective_loop(
    max_steps: int,
    loop: asyncio.AbstractEventLoop,
) -> None:
    """
    Loop raíz autónomo: toma objetivos pending de objectives.jsonl y los ejecuta.
    Sin esperar input de Claude entre objetivos.
    """
    if _ObjectiveStore is None:
        log.error("ObjectiveStore no disponible — objective_loop deshabilitado")
        return

    store     = _ObjectiveStore()
    strategy  = StrategyEngine()
    coord     = DroneCoordinator()
    world_model = _WorldModel() if _WorldModel else None
    obs_parser  = _ObsParser()  if _ObsParser  else None
    facts       = _FactStore()  if _FactStore   else None
    blocked_counts: Dict[str, int] = {}   # objective_id → veces bloqueado

    log.info("objective_loop iniciado (poll=%.1fs, max_steps=%d)", OBJ_POLL_S, max_steps)

    while not _should_stop.is_set():
        await asyncio.sleep(OBJ_POLL_S)

        try:
            obj = store.next_pending()
        except Exception as exc:
            log.debug("next_pending error: %s", exc)
            continue

        if obj is None:
            continue

        # Extraer target del objetivo o del payload
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
            results = await _run_objective(
                objective_id=obj.id,
                objective_text=obj.text,
                target=target,
                max_steps=max_steps,
                strategy=strategy,
                world_model=world_model,
                obs_parser=obs_parser,
                facts=facts,
                loop=loop,
            )
        except Exception as exc:
            log.error("objective %s falló: %s", obj.id, exc)
            _emit("OBJECTIVE_ERROR", {"id": obj.id, "error": str(exc)}, severity="error")
            try:
                store.block(obj.id, reason=str(exc))
            except Exception:
                pass
            _update_task_status(obj.text, "Blocked")
            _daemon_stats["objectives_failed"] += 1
            _daemon_stats["current_objective"] = None
            _daemon_stats["current_phase"]     = "idle"
            _write_status()
            continue

        # Lanzar drones para todos los hallazgos acumulados
        all_findings = [f for r in results for f in r.findings]
        drone_ids = coord.process_findings(
            all_findings, target, obj.id,
            payload_key=payload.get("api_key", ""),
        )

        # Guardar resultado en hive memory
        if _get_hive:
            try:
                hive = _get_hive()
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

        # Marcar objetivo completado
        try:
            store.complete(obj.id)
        except Exception:
            pass
        _update_task_status(obj.text, "Done")

        _daemon_stats["objectives_done"] += 1
        _daemon_stats["steps_run"]       += len(results)
        _daemon_stats["drones_spawned"]  += len(drone_ids)
        _daemon_stats["current_objective"] = None
        _daemon_stats["current_phase"]     = "idle"
        _write_status()

        log.info("✓  [%s] completado — %d pasos, %d hallazgos, %d drones",
                 obj.id, len(results), len(all_findings), len(drone_ids))


# ── Role 2 — WorldModel Watcher ───────────────────────────────────────────────

async def world_model_watcher(loop: asyncio.AbstractEventLoop) -> None:
    """
    Observa world_model.json. Cuando cambia la fase o aparecen nuevos hosts,
    inyecta objetivos derivados automáticamente.
    """
    wm_file   = SESSIONS_DIR / "world_model.json"
    last_snap: Dict = {}

    if _ObjectiveStore is None:
        return

    store = _ObjectiveStore()
    log.info("world_model_watcher iniciado (poll=%.1fs)", WM_POLL_S)

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

        # Detectar nuevos hosts
        prev_hosts = set(last_snap.get("hosts", {}).keys())
        curr_hosts = set(snap.get("hosts", {}).keys())
        new_hosts  = curr_hosts - prev_hosts
        for host in new_hosts:
            text = f"Enumerate newly discovered host {host}"
            try:
                obj = store.inject(text=text, priority="high",
                                   source="world_model_watcher",
                                   context={"target": host})
                task_id = _inject_to_tasks_json(
                    title=text,
                    description=f"Auto-inyectado por WorldModelWatcher | objective_id={obj.id}",
                    operator="world_model_watcher",
                    status="New",
                )
                _emit("OBJECTIVE_AUTO_INJECTED", {
                    "text": text, "trigger": "new_host", "host": host, "task_id": task_id,
                })
                log.info("  🎯 nuevo objetivo auto-inyectado: %s (task_id=%d)", text, task_id)
            except Exception as exc:
                log.debug("inject error: %s", exc)

        # Detectar nuevas credenciales
        prev_creds = len(last_snap.get("credentials", []))
        curr_creds = len(snap.get("credentials", []))
        if curr_creds > prev_creds:
            new_count = curr_creds - prev_creds
            creds     = snap.get("credentials", [])[-new_count:]
            for cred in creds:
                cred_str = json.dumps(cred)[:80]
                text = f"Leverage new credential: {cred_str}"
                try:
                    obj = store.inject(text=text, priority="critical",
                                       source="world_model_watcher",
                                       context={"credential": cred})
                    task_id = _inject_to_tasks_json(
                        title=text,
                        description=f"Credencial detectada automáticamente | objective_id={obj.id}",
                        operator="world_model_watcher",
                        status="New",
                    )
                    _emit("OBJECTIVE_AUTO_INJECTED", {
                        "text": text, "trigger": "new_credential", "task_id": task_id,
                    }, severity="warning")
                    log.info("  🎯 credencial detectada → task_id=%d", task_id)
                except Exception:
                    pass

        # Detectar cambio de fase
        prev_phase = last_snap.get("phase", "")
        curr_phase = snap.get("phase", "")
        if curr_phase and curr_phase != prev_phase:
            _emit("PHASE_CHANGE", {
                "from": prev_phase, "to": curr_phase,
            })
            _daemon_stats["current_phase"] = curr_phase
            log.info("  📍 fase: %s → %s", prev_phase, curr_phase)

        last_snap = snap
        _write_status()


# ── Role 3 — Heartbeat ────────────────────────────────────────────────────────

async def heartbeat_loop() -> None:
    """Emite heartbeat y escribe status cada HEARTBEAT_S segundos."""
    while not _should_stop.is_set():
        await asyncio.sleep(HEARTBEAT_S)
        _daemon_stats["events_emitted"] += 1
        _emit("HEARTBEAT", {
            "pid":              os.getpid(),
            "objectives_done":  _daemon_stats["objectives_done"],
            "steps_run":        _daemon_stats["steps_run"],
            "drones_spawned":   _daemon_stats["drones_spawned"],
            "current_phase":    _daemon_stats["current_phase"],
            "current_objective":_daemon_stats["current_objective"],
        })
        _write_status()
        log.info("♥  heartbeat — done=%d steps=%d drones=%d",
                 _daemon_stats["objectives_done"],
                 _daemon_stats["steps_run"],
                 _daemon_stats["drones_spawned"])


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 7 — Main asyncio entrypoint
# ─────────────────────────────────────────────────────────────────────────────

async def _main_async(max_steps: int = MAX_STEPS_DEFAULT) -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    _daemon_stats["started_at"] = datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat()
    _write_status()

    loop = asyncio.get_event_loop()

    _emit("DAEMON_START", {
        "pid": os.getpid(),
        "max_steps": max_steps,
        "hive_backend": HIVE_BACKEND,
    })

    tasks = [
        asyncio.create_task(
            objective_loop(max_steps, loop), name="objective_loop"
        ),
        asyncio.create_task(
            world_model_watcher(loop), name="world_model_watcher"
        ),
        asyncio.create_task(
            heartbeat_loop(), name="heartbeat"
        ),
    ]

    log.info("LazyOwn autonomous daemon iniciado (pid=%d max_steps=%d)",
             os.getpid(), max_steps)

    ev_loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        ev_loop.add_signal_handler(
            sig, lambda: [_should_stop.set(), *[t.cancel() for t in tasks]]
        )

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        log.info("daemon detenido")
    finally:
        _emit("DAEMON_STOP", {"pid": os.getpid()})
        STATUS_FILE.write_text(
            json.dumps({"status": "stopped", "pid": os.getpid()}, indent=2)
        )
        _clear_pid()


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 8 — PID management + CLI
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
    _write_pid()
    try:
        asyncio.run(_main_async(max_steps))
    finally:
        _clear_pid()


def cmd_start(max_steps: int = MAX_STEPS_DEFAULT) -> None:
    running, pid = _is_running()
    if running:
        print(f"[auto] ya corriendo (pid={pid})")
        sys.exit(1)

    child = os.fork()
    if child > 0:
        print(f"[auto] iniciado en background (pid={child})")
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
    running, pid = _is_running()
    if not running:
        print("[auto] no está corriendo")
        sys.exit(1)
    os.kill(pid, signal.SIGTERM)
    print(f"[auto] SIGTERM enviado a pid={pid}")
    for _ in range(50):
        time.sleep(0.1)
        alive, _ = _is_running()
        if not alive:
            print("[auto] detenido")
            return
    print("[auto] sigue corriendo después de 5s — usa SIGKILL manualmente")


def cmd_status() -> None:
    running, pid = _is_running()
    state = "corriendo" if running else "detenido"
    print(f"[auto] {state}" + (f" (pid={pid})" if running else ""))
    if STATUS_FILE.exists():
        try:
            data = json.loads(STATUS_FILE.read_text())
            for k, v in data.items():
                print(f"  {k}: {v}")
        except Exception:
            print("  (status file ilegible)")
    else:
        print("  (sin status aún)")


def cmd_inject(text: str, priority: str = "high") -> None:
    if _ObjectiveStore is None:
        print("[auto] ObjectiveStore no disponible")
        sys.exit(1)
    store   = _ObjectiveStore()
    obj     = store.inject(text=text, priority=priority, source="cli")
    task_id = _inject_to_tasks_json(
        title=text,
        description=f"Inyectado por CLI | objective_id={obj.id}",
        operator="cli",
        status="New",
    )
    print(f"[auto] objetivo inyectado: [{obj.id}] {obj.text[:80]}")
    print(f"[auto] task.json id={task_id} — visible en /tasks del C2")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 9 — API pública para lazyown_mcp.py
# ─────────────────────────────────────────────────────────────────────────────

_daemon_thread: Optional[threading.Thread] = None
_daemon_loop:   Optional[asyncio.AbstractEventLoop] = None


def mcp_autonomous_start(
    max_steps: int = MAX_STEPS_DEFAULT,
    backend: str = HIVE_BACKEND,
) -> str:
    """Inicia el daemon autónomo en un thread de background (para llamada desde MCP)."""
    global _daemon_thread, _daemon_loop, HIVE_BACKEND

    if _daemon_thread and _daemon_thread.is_alive():
        return json.dumps({"status": "already_running",
                           "message": "El daemon autónomo ya está activo"})

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
            "Daemon autónomo activo. Inyecta objetivos con lazyown_autonomous_inject. "
            "Monitorea con lazyown_autonomous_status. "
            "Lee eventos en sessions/autonomous_events.jsonl"
        ),
    }, indent=2)


def mcp_autonomous_stop() -> str:
    """Detiene el daemon autónomo."""
    global _daemon_thread
    _should_stop.set()

    if _daemon_loop and _daemon_loop.is_running():
        for task in asyncio.all_tasks(_daemon_loop):
            task.cancel()

    if _daemon_thread:
        _daemon_thread.join(timeout=5.0)

    _emit("DAEMON_STOP_MCP", {"message": "Detenido via MCP"})
    return json.dumps({"status": "stopped", "message": "Daemon autónomo detenido"})


def mcp_autonomous_status() -> str:
    """Estado actual del daemon: objetivos, pasos, drones, fase."""
    alive = bool(_daemon_thread and _daemon_thread.is_alive())
    data  = {**_daemon_stats, "running": alive}
    if STATUS_FILE.exists():
        try:
            disk = json.loads(STATUS_FILE.read_text())
            data.update(disk)
        except Exception:
            pass
    return json.dumps(data, indent=2, default=str)


def mcp_autonomous_inject(text: str, priority: str = "high",
                           target: str = "") -> str:
    """Inyecta un objetivo en la cola del daemon autónomo y en sessions/tasks.json."""
    if _ObjectiveStore is None:
        return "[auto] ObjectiveStore no disponible"
    store = _ObjectiveStore()
    ctx   = {"target": target} if target else {}
    obj   = store.inject(text=text, priority=priority,
                         source="mcp_claude", context=ctx)

    # Escribir también en tasks.json (visible en el dashboard C2)
    task_id = _inject_to_tasks_json(
        title=text,
        description=(
            f"Objetivo autónomo — priority={priority}"
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
    """Lee los últimos N eventos del stream autonomous_events.jsonl."""
    if not EVENTS_FILE.exists():
        return "Sin eventos aún. Inicia el daemon con lazyown_autonomous_start."
    try:
        lines = EVENTS_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
        last  = lines[-last_n:]
        events = []
        for line in last:
            try:
                events.append(json.loads(line))
            except Exception:
                pass
        if not events:
            return "Sin eventos legibles."
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
# SECCIÓN 10 — CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

_COMMANDS = {
    "run":    lambda args: cmd_run(int(args.max_steps)),
    "start":  lambda args: cmd_start(int(args.max_steps)),
    "stop":   lambda _: cmd_stop(),
    "status": lambda _: cmd_status(),
    "inject": lambda args: cmd_inject(args.text, args.priority),
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
                       help="Pasos máximos por objetivo")

    sub.add_parser("stop")
    sub.add_parser("status")

    p_inj = sub.add_parser("inject", help="Inyectar objetivo")
    p_inj.add_argument("text", help="Texto del objetivo")
    p_inj.add_argument("--priority", default="high",
                       choices=["critical", "high", "medium", "low"])

    args = parser.parse_args()
    if args.cmd not in _COMMANDS:
        parser.print_help()
        sys.exit(1)
    _COMMANDS[args.cmd](args)
