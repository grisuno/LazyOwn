"""Single execution path for ``lazy_loop`` and ``auto_loop``.

Both commands are the same engine by contract; this module owns the one
runner so their behavior cannot drift again. Command sets only parse
arguments into a :class:`LoopRunConfig` — everything operational lives
here: terminal safety, autonomous prompt suppression, live worker
streaming, the Rich milestone panel, cancellation and the final
summary.
"""

from __future__ import annotations

import contextlib
import io
import queue
import shlex
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from core.autonomous import autonomous_mode
from core.terminal_guard import TerminalGuard
from utils import print_error, print_msg, print_warn

SESSIONS_DIR = "sessions"
HEARTBEAT_SEC = 15.0
DEFAULT_VERB_TIMEOUT_SEC = 300.0
DEFAULT_ROUNDS = 6
DEFAULT_WORKERS = 2
MAX_WORKERS = 5
MAX_ROUNDS = 50
POLL_SEC = 0.5
WORKER_JOIN_SEC = 5.0
TRANSCRIPT_DRAIN_CAP = 500
STALL_WARN_SEC = 45.0
STALL_DUMP_SEC = 120.0


class ThreadStdoutRouter(io.TextIOBase):
    """stdout proxy: main thread keeps the real stream, workers spool.

    A plain ``redirect_stdout`` is process-global: a cancelled
    orchestrator thread that outlives the command keeps ``sys.stdout``
    pointed at an abandoned queue, leaving the shell apparently hung.
    This router only captures non-main threads, so restoring the real
    stream from the main thread always leaves a working shell.
    """

    def __init__(self, main_stream, spool: queue.Queue) -> None:
        """Bind the real stream and the worker spool queue."""
        super().__init__()
        self._main_stream = main_stream
        self._spool = spool

    def write(self, data: str) -> int:
        """Route main-thread writes to the terminal, worker writes to spool."""
        text = str(data)
        if threading.current_thread() is threading.main_thread():
            try:
                return self._main_stream.write(text)
            except Exception:
                return len(text)
        self._spool.put(text)
        return len(text)

    def flush(self) -> None:
        """Flush the real stream; the spool needs no flushing."""
        try:
            self._main_stream.flush()
        except Exception:
            pass

    @property
    def encoding(self) -> str:
        """Report the real stream encoding."""
        return str(getattr(self._main_stream, "encoding", "utf-8") or "utf-8")

    def isatty(self) -> bool:
        """Report whether the real stream is a terminal."""
        probe = getattr(self._main_stream, "isatty", None)
        try:
            return bool(probe()) if callable(probe) else False
        except Exception:
            return False


@dataclass
class LoopRunConfig:
    """Everything one loop invocation needs, parsed by the command sets."""

    goal: str = ""
    task_id: str = ""
    target: str = ""
    rounds: int = DEFAULT_ROUNDS
    workers: int = DEFAULT_WORKERS
    timeout: float = 0.0
    step_delay: float = 0.0
    sandbox: str = ""
    no_bootstrap: bool = False
    progress: bool = True
    view: bool = False
    verb_timeout: float = DEFAULT_VERB_TIMEOUT_SEC
    profile: str = ""
    rounds_set: bool = True
    workers_set: bool = True
    extra: dict = field(default_factory=dict)

    def clamped(self) -> LoopRunConfig:
        """Clamp numeric knobs to the supported operating range."""
        self.rounds = max(1, min(MAX_ROUNDS, int(self.rounds or DEFAULT_ROUNDS)))
        self.workers = max(1, min(MAX_WORKERS, int(self.workers or DEFAULT_WORKERS)))
        self.timeout = max(0.0, float(self.timeout or 0.0))
        self.step_delay = max(0.0, float(self.step_delay or 0.0))
        self.verb_timeout = max(30.0, float(self.verb_timeout or DEFAULT_VERB_TIMEOUT_SEC))
        return self


FLAG_VALUES = ("--target", "--task", "--profile", "--rounds", "--max-steps", "--workers", "--timeout", "--step-delay")
FLAG_TOGGLES = ("--no-bootstrap", "--view", "--plain", "--no-progress")


def _to_int(raw: str, default: int) -> int:
    """Parse an integer flag value, falling back to the default."""
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError):
        return default


def _to_float(raw: str, default: float) -> float:
    """Parse a float flag value, falling back to the default."""
    try:
        return float(str(raw).strip())
    except (TypeError, ValueError):
        return default


def parse_loop_line(line: str) -> LoopRunConfig:
    """Parse one loop command line into a :class:`LoopRunConfig`.

    Shared by ``lazy_loop`` and ``auto_loop`` so both accept the exact
    same flags and defaults.

    Args:
        line: Raw command line after the verb.

    Returns:
        Parsed configuration.

    Raises:
        ValueError: Empty line, unknown flag value or unbalanced quotes.
    """
    raw = (line or "").strip()
    if not raw:
        raise ValueError("usage")
    parts = shlex.split(raw)
    target = ""
    task_id = ""
    profile = ""
    rounds = DEFAULT_ROUNDS
    workers = DEFAULT_WORKERS
    rounds_set = False
    workers_set = False
    timeout = 0.0
    step_delay = 0.0
    sandbox = ""
    no_bootstrap = False
    progress = True
    view = False
    goal_parts: list[str] = []
    idx = 0
    while idx < len(parts):
        token = parts[idx]
        if token == "--sandbox":
            nxt = parts[idx + 1] if idx + 1 < len(parts) else ""
            if nxt and not nxt.startswith("--"):
                sandbox = nxt
                idx += 2
            else:
                sandbox = "default"
                idx += 1
            continue
        if token in FLAG_VALUES:
            if idx + 1 >= len(parts):
                raise ValueError(f"missing value for {token}")
            value = parts[idx + 1]
            if token == "--target":
                target = value
            elif token == "--task":
                task_id = value
            elif token == "--profile":
                profile = value
            elif token in ("--rounds", "--max-steps"):
                rounds = _to_int(value, DEFAULT_ROUNDS)
                rounds_set = True
            elif token == "--workers":
                workers = _to_int(value, DEFAULT_WORKERS)
                workers_set = True
            elif token == "--timeout":
                timeout = _to_float(value, 0.0)
            elif token == "--step-delay":
                step_delay = _to_float(value, 0.0)
            idx += 2
            continue
        if token in FLAG_TOGGLES:
            if token == "--no-bootstrap":
                no_bootstrap = True
            elif token == "--view":
                view = True
            else:
                progress = False
            idx += 1
            continue
        if token.startswith("--"):
            raise ValueError(f"unknown flag: {token}")
        goal_parts.append(token)
        idx += 1
    return LoopRunConfig(
        goal=" ".join(goal_parts),
        task_id=task_id,
        target=target,
        profile=profile,
        rounds=rounds,
        workers=workers,
        rounds_set=rounds_set,
        workers_set=workers_set,
        timeout=timeout,
        step_delay=step_delay,
        sandbox=sandbox,
        no_bootstrap=no_bootstrap,
        progress=progress,
        view=view,
    )


def resolve_loop_defaults(config: LoopRunConfig) -> LoopRunConfig:
    """Fill unset rounds and workers from the selected orchestrator profile.

    Args:
        config: Parsed invocation; explicit flags stay untouched.

    Returns:
        The same configuration with profile defaults applied.
    """
    from modules import orchestrator_config

    name = config.profile or orchestrator_config.active_profile()
    try:
        profile = orchestrator_config.profile_config(name)
    except Exception:
        profile = orchestrator_config.profile_config()
        name = orchestrator_config.active_profile()
    limits = dict(profile.get("limits") or {})
    config.profile = name
    if not config.rounds_set:
        try:
            config.rounds = int(limits.get("rounds", config.rounds) or config.rounds)
        except (TypeError, ValueError):
            pass
    if not config.workers_set:
        try:
            config.workers = int(limits.get("workers", config.workers) or config.workers)
        except (TypeError, ValueError):
            pass
    try:
        config.verb_timeout = float(limits.get("verb_timeout_sec", config.verb_timeout) or config.verb_timeout)
    except (TypeError, ValueError):
        pass
    return config


def build_executor(
    shell, config: LoopRunConfig, stream: Callable[[str], None], cancelled: dict,
    sandbox_task_id: str = "", sandbox_image: str = "",
) -> Callable[[str], str]:
    """Build the worker executor: shell verbs, custom tools, safe bash.

    Every branch is stdin-detached: shell verbs cannot prompt (input is
    suppressed by the autonomous context), custom tools run through the
    streaming runner, and raw bash goes through ``execute_streaming``
    with ``stdin=DEVNULL`` and its own process group so Ctrl+C and time
    limits always kill the child, never the operator's terminal.

    When ``sandbox_task_id`` is set, routable shell verbs run inside the
    per-task Docker container (``modules.lazy_sandbox``) instead of the
    operator host; custom tools and raw bash stay local.
    """

    def _resolve_alias(command: str) -> str:
        token = command.split()[0] if command.split() else ""
        aliases = getattr(shell, "aliases", None)
        if isinstance(aliases, dict) and aliases.get(token):
            rest = " ".join(command.split()[1:])
            return f"{aliases[token]} {rest}".strip()
        return command

    def _executor(command: str) -> str:
        text = str(command or "")
        if cancelled.get("flag"):
            return "execution failed: cancelled by operator"
        from utils import needs_sudo, sudo_available

        if needs_sudo(_resolve_alias(text)) and not sudo_available():
            stream(f"[skip] sudo unavailable in unattended mode: {text[:160]}")
            return f"skipped: sudo unavailable in unattended mode: {text[:160]}"
        stream(f">>> {text[:200]}")
        if text.startswith("custom tool "):
            try:
                from modules.custom_tools import run_tool

                parts = text.split(maxsplit=4)
                name = parts[2] if len(parts) > 2 else ""
                arg = " ".join(parts[3:]).strip() if len(parts) > 3 else ""
                return str(run_tool(name, arg, on_output=stream) or "")
            except Exception as exc:
                return f"execution failed: {exc}"
        try:
            from modules.auto_registry import (
                execute_shell_verb,
                execute_streaming,
                is_routable_command,
            )
        except Exception as exc:
            return f"execution failed: {exc}"
        if shell is not None and is_routable_command(text):
            if sandbox_task_id:
                try:
                    from modules.lazy_sandbox import exec_command as _sandbox_exec

                    stream(f"[sandbox] {text[:200]}")
                    return _sandbox_exec(
                        sandbox_task_id, text, timeout_sec=config.verb_timeout, image=sandbox_image
                    )
                except Exception as exc:
                    return f"execution failed: {exc}"
            try:
                return execute_shell_verb(shell, text, timeout_sec=config.verb_timeout, on_output=stream)
            except Exception as exc:
                return f"execution failed: {exc}"
        return execute_streaming(text, on_output=stream, timeout_sec=config.verb_timeout)

    return _executor


def _abort_run(engine, task_id: str, reason: str) -> None:
    """Cancel streaming children, abort the runtime and pause the task."""
    try:
        from modules.auto_registry import cancel_running_commands

        cancel_running_commands()
    except Exception:
        pass
    if task_id:
        try:
            engine.runtime.abort(task_id, "user", reason)
        except Exception:
            pass
        try:
            engine.store.pause(task_id)
        except Exception:
            pass


def _prepare_engine(engine, shell, config: LoopRunConfig, params: dict) -> None:
    """Bind shell and apply payload-driven tuning to the engine."""
    try:
        engine.bind_shell(shell)
    except Exception:
        pass
    if config.step_delay:
        engine.debounce_sec = max(float(getattr(engine, "debounce_sec", 0.0) or 0.0), config.step_delay)
    try:
        engine.set_concurrency(int((params or {}).get("max_concurrent", 0) or 0))
    except (TypeError, ValueError):
        pass


def _start_proxy(engine, params: dict) -> None:
    """Start the recording proxy when payload asks for it (fail-soft)."""
    if not bool((params or {}).get("proxy_autostart", True)):
        return
    port_raw = (params or {}).get("proxy_port", 0)
    try:
        proxy_port = int(port_raw or 0)
    except (TypeError, ValueError):
        proxy_port = 0
    try:
        engine.proxy_gc_days = max(0, int((params or {}).get("proxy_gc_days", 30) or 30))
    except (TypeError, ValueError):
        pass
    try:
        status = engine.proxy_start(port=proxy_port, upstream=str((params or {}).get("proxy_upstream", "") or ""))
        trust = status.get("trust") or {}
        print_msg(
            f"[*] recorder proxy {status['host']}:{status['port']} "
            f"CA={'trusted' if trust.get('installed') else 'pending'} "
            f"exchanges={status['exchanges']}"
        )
    except Exception as exc:
        print_warn(f"proxy autostart skipped: {exc}")


def report_result(result: dict) -> None:
    """Print the final outcome of one loop run."""
    if result.get("error"):
        print_error(f"lazy_loop failed: {result['error']}")
        return
    if result.get("cancelled"):
        print_warn(
            "lazy_loop cancelled by operator; partial state saved "
            f"({result.get('task_id') or 'no task'}). "
            "Inspect: lazy_status / lazy_trace"
        )
        return
    task_id = result.get("task_id", "")
    overview = result.get("overview", {}) or {}
    print_msg(
        f"[+] {task_id} [{result.get('status', '')}] rounds={result.get('rounds', 0)} "
        f"intents={len(overview.get('intents', []))} "
        f"facts={overview.get('facts', 0)} "
        f"findings={overview.get('findings', 0)}"
    )
    if overview.get("findings"):
        print_warn(f"Findings present — inspect with: lazy_findings {task_id} / lazy_trace {task_id} list")


def _bootstrap(scan_target: str, executor: Callable[[str], str]) -> None:
    """Ingest an existing nmap XML through ``auto_populate`` before round 1."""
    scan = Path(SESSIONS_DIR) / f"scan_{scan_target}.nmap.xml"
    if not scan.exists():
        return
    print_msg(f"[*] bootstrap: ingesting {scan.name} via auto_populate")
    started = time.monotonic()
    result = executor(f"auto_populate {scan_target}")
    if str(result).startswith("TIMEOUT"):
        print_warn(f"[!] bootstrap timed out after {int(time.monotonic() - started)}s; continuing")
    else:
        print_msg(f"[*] bootstrap done in {time.monotonic() - started:.1f}s")


def _run_with_progress(engine, config: LoopRunConfig) -> dict:
    """Run orchestration behind the Rich milestone panel.

    Bootstrap (``auto_populate`` over an existing nmap XML) runs inside
    the same streamed thread as the orchestrator, so its transcript is
    visible in the panel instead of disappearing behind the redirect.
    """
    from modules.loop_progress import LoopProgress

    transcript: queue.Queue = queue.Queue()
    live_sink: dict = {"emit": None}
    cancelled = {"flag": False}
    outcome: dict = {}
    task_id = config.task_id

    def stream(text: str) -> None:
        sink = live_sink.get("emit")
        if sink is None:
            print(text, end="" if str(text).endswith("\n") else "\n", flush=True)
            return
        try:
            sink(text if str(text).endswith("\n") else str(text) + "\n")
        except Exception:
            pass

    import sys as _sys

    real_stdout = _sys.stdout if _sys.stdout is not None else _sys.stderr
    router = ThreadStdoutRouter(real_stdout, transcript)
    if config.sandbox:
        record = engine.store.get(task_id) if task_id else None
        if record is None:
            task_id = engine.create_task(config.goal or f"engage {config.target or 'target'}")["task_id"]
            if config.target:
                engine.ensure_target(task_id, config.target, "loop target")
            config.task_id = task_id
            stream(f"[*] sandbox task {task_id} bound to container\n")
    sandbox_image = "" if config.sandbox in ("", "default") else config.sandbox
    executor = build_executor(
        engine.shell, config, stream, cancelled,
        sandbox_task_id=task_id if config.sandbox else "",
        sandbox_image=sandbox_image,
    )
    progress = LoopProgress(goal=config.goal, target=config.target)
    progress.start()
    live_sink["emit"] = transcript.put
    progress.emit(
        f"[*] task {task_id} running (rounds<={config.rounds}, "
        f"workers={config.workers}) — tool calls stream below; "
        "audit: lazy_view / lazy_trace; Ctrl+C cancels"
    )

    def _run() -> None:
        try:
            if config.target and not config.no_bootstrap:
                _bootstrap(config.target, executor)
            outcome["result"] = engine.orchestrate(
                goal=config.goal,
                task_id=task_id,
                target=config.target,
                max_rounds=config.rounds,
                workers=config.workers,
                timeout_sec=config.timeout,
                executor=executor,
            )
        except BaseException as exc:  # noqa: BLE001 - reported by caller
            outcome["error"] = exc

    worker = threading.Thread(target=_run, daemon=True)
    try:
        with contextlib.redirect_stdout(router):
            worker.start()
            try:
                _poll_progress(engine, config, progress, transcript, worker)
            except (KeyboardInterrupt, SystemExit, EOFError):
                cancelled["flag"] = True
                progress.emit("operator interrupt received; cancelling running commands...")
                _abort_run(engine, task_id, "operator interrupt (Ctrl+C/Ctrl+D)")
                worker.join(timeout=WORKER_JOIN_SEC)
                if worker.is_alive():
                    progress.emit(
                        "[!] orchestrator thread still winding down in the background; "
                        "state is saved and the shell stays responsive — "
                        f"inspect with: lazy_status {task_id}"
                    )
    finally:
        progress.stop()
    if "error" in outcome:
        return {
            "task_id": task_id,
            "error": str(outcome["error"]),
            "cancelled": cancelled["flag"],
            "overview": _overview(task_id),
        }
    if "result" not in outcome:
        return {
            "task_id": task_id,
            "cancelled": cancelled["flag"],
            "error": "" if cancelled["flag"] else "orchestrator produced no result",
            "overview": _overview(task_id),
        }
    result = outcome["result"]
    result["cancelled"] = cancelled["flag"]
    return result


def _overview(task_id: str) -> dict:
    """Best-effort graph overview for partial results."""
    try:
        from modules.lazy_loop import ExplorationGraph

        return ExplorationGraph(task_id).overview()
    except Exception:
        return {}


def _format_activity(record: dict) -> str:
    """One compact English line per activity record for the operator.

    Tool results are skipped because the raw output is already streamed
    by the executor; everything else (claims, planner wakes, LLM calls
    and retries, guard decisions, approvals, enrich, retest, compaction,
    traffic, triggers) is surfaced so any runaway loop is visible.
    """
    kind = str(record.get("kind", "event"))
    worker = str(record.get("worker", "engine"))
    text = " ".join(str(record.get("text", "")).split())
    return f"[{kind}] {worker}: {text[:220]}"


def _dump_thread_stacks() -> None:
    """Dump all thread stacks to stderr so a stuck loop is identifiable."""
    import faulthandler
    import sys

    target = getattr(sys, "__stderr__", None) or sys.stderr
    try:
        target.write("\n[stall] no loop activity; dumping all thread stacks:\n")
        target.flush()
        faulthandler.dump_traceback(file=target, all_threads=True)
        target.flush()
    except Exception:
        pass


def _stall_thresholds(verb_timeout: float) -> tuple[float, float]:
    """Return warning and dump thresholds for a command timeout.

    A legitimate nmap run can exceed the fixed 45s/120s defaults. Tie the
    thresholds to the configured verb timeout so a long-but-bounded tool
    run never looks like a dead loop; the executor still kills the child
    at ``verb_timeout``.
    """
    timeout = max(30.0, float(verb_timeout or 300.0))
    warn_after = max(STALL_WARN_SEC, min(180.0, timeout * 0.5))
    dump_after = max(STALL_DUMP_SEC, timeout + 30.0)
    return warn_after, dump_after


def _poll_progress(engine, config: LoopRunConfig, progress, transcript, worker: threading.Thread) -> None:
    """Drain live output into the panel until the orchestrator finishes.

    Two streams feed the operator: the executor transcript (tool calls
    and raw output) and the task activity log (every engine step). A
    stall watchdog warns and dumps thread stacks when neither moves.
    """
    import modules.lazy_loop as _loop
    from modules.jsonl_tail import JsonlTail
    from modules.lazy_loop import ActivityLog, ExplorationGraph
    from modules.loop_progress import snapshot_from_overview

    task_id = config.task_id
    graph = ExplorationGraph(task_id)
    activity = ActivityLog(task_id)
    tail = JsonlTail(_loop._store_path(f"activity_{task_id}.jsonl"))
    started = time.monotonic()
    last_beat = started
    last_event = started
    last_stall_dump = 0.0
    last_stall_warn = 0.0
    last_line = ""
    pending_line = ""
    warn_after, dump_after = _stall_thresholds(float(getattr(config, "verb_timeout", 300.0) or 300.0))
    while worker.is_alive():
        for _ in range(TRANSCRIPT_DRAIN_CAP):
            try:
                chunk = transcript.get_nowait()
            except queue.Empty:
                break
            pending_line += str(chunk)
            while "\n" in pending_line:
                line, pending_line = pending_line.split("\n", 1)
                progress.emit(line)
                last_line = line
                last_event = time.monotonic()
        for record in tail.read_new(limit=200):
            line = _format_activity(record)
            progress.emit(line)
            last_line = line
            last_event = time.monotonic()
        try:
            graph.reload()
            overview = graph.overview()
        except Exception:
            overview = {}
        try:
            record = engine.store.get(task_id) or {}
        except Exception:
            record = {}
        entries = []
        try:
            entries = activity.read(limit=60) or []
        except Exception:
            entries = []
        tools = sum(1 for e in entries if e.get("kind") == "tool")
        results = sum(1 for e in entries if e.get("kind") == "result")
        last = str(entries[-1].get("text", "") if entries else "")
        now = time.monotonic()
        snap = snapshot_from_overview(overview, record, activity_tail=last, elapsed_sec=now - started)
        snap.tool_calls = tools
        snap.results = results
        progress.refresh(snap)
        idle = now - last_event
        if idle >= warn_after and now - last_stall_warn >= warn_after:
            last_stall_warn = now
            progress.emit(
                f"[stall] no loop activity for {int(idle)}s; last step: "
                f"{last_line[:160] or 'none'} (Ctrl+C cancels and saves state)"
            )
        if idle >= dump_after and now - last_stall_dump >= dump_after:
            last_stall_dump = now
            progress.emit(f"[stall] still idle after {int(idle)}s; dumping all thread stacks to stderr")
            _dump_thread_stacks()
        if now - last_beat >= HEARTBEAT_SEC:
            last_beat = now
            progress.emit(
                f"[hb] {int(now - started)}s alive: tools={tools} results={results} idle={int(idle)}s "
                f"last={last[:80] or 'idle'}"
            )
        worker.join(timeout=POLL_SEC)
    while True:
        try:
            chunk = transcript.get_nowait()
        except queue.Empty:
            break
        pending_line += str(chunk)
    while "\n" in pending_line:
        line, pending_line = pending_line.split("\n", 1)
        progress.emit(line)
    if pending_line.strip():
        progress.emit(pending_line)
    for record in tail.read_new(limit=2000):
        progress.emit(_format_activity(record))


def _terminal_stream():
    """Return a stream writer bound to the *real* stdout.

    Shell verbs run with ``stdout`` redirected into their capture
    buffer; observers that print through ``sys.stdout`` would write into
    that buffer instead of the terminal. ``sys.__stdout__`` bypasses the
    redirect, so live output stays visible without feedback loops.
    """
    import sys

    target = getattr(sys, "__stdout__", None) or sys.stderr

    def _write(text: str) -> None:
        try:
            target.write(text if str(text).endswith("\n") else str(text) + "\n")
            target.flush()
        except Exception:
            pass

    return _write


def _run_plain(engine, config: LoopRunConfig) -> dict:
    """Run orchestration without the live panel (plain transcript)."""
    cancelled = {"flag": False}
    if config.sandbox:
        record = engine.store.get(config.task_id) if config.task_id else None
        if record is None:
            config.task_id = engine.create_task(config.goal or f"engage {config.target or 'target'}")["task_id"]
            if config.target:
                engine.ensure_target(config.task_id, config.target, "loop target")
    sandbox_image = "" if config.sandbox in ("", "default") else config.sandbox
    executor = build_executor(
        engine.shell, config, _terminal_stream(), cancelled,
        sandbox_task_id=config.task_id if config.sandbox else "",
        sandbox_image=sandbox_image,
    )
    try:
        if config.target and not config.no_bootstrap:
            _bootstrap(config.target, executor)
        result = engine.orchestrate(
            goal=config.goal,
            task_id=config.task_id,
            target=config.target,
            max_rounds=config.rounds,
            workers=config.workers,
            timeout_sec=config.timeout,
            executor=executor,
        )
        result["cancelled"] = False
        return result
    except (KeyboardInterrupt, SystemExit, EOFError):
        cancelled["flag"] = True
        _abort_run(engine, config.task_id, "operator interrupt (Ctrl+C/Ctrl+D)")
        return {"task_id": config.task_id, "cancelled": True, "overview": _overview(config.task_id)}


def run_loop(shell, params: dict, config: LoopRunConfig) -> dict:
    """Execute one complete loop run and return its summary.

    Args:
        shell: Live LazyOwn shell (workers route verbs through it).
        params: Payload mapping (proxy/concurrency/verb timeout).
        config: Parsed command invocation.

    Returns:
        Orchestrator summary with ``cancelled``/``error`` keys added.
    """
    resolve_loop_defaults(config)
    config.clamped()
    raw_verb_timeout = (params or {}).get("verb_timeout", 0)
    try:
        if raw_verb_timeout:
            config.verb_timeout = max(30.0, float(raw_verb_timeout))
    except (TypeError, ValueError):
        pass
    if not config.goal and config.target:
        config.goal = f"gain initial access on {config.target}"
    try:
        from modules.lazy_engine import LazyEngine
    except Exception as exc:
        print_error(f"lazy_loop: engine unavailable ({exc})")
        return {"task_id": config.task_id, "error": str(exc)}

    engine = LazyEngine()
    try:
        engine.apply_profile(config.profile)
    except Exception:
        pass
    _prepare_engine(engine, shell, config, params)
    _start_proxy(engine, params)
    print_msg(f"[*] orchestrator chain: {'/'.join(engine.ORCHESTRATOR_CHAIN)}")

    import signal as _signal

    previous_sigint = None
    if threading.current_thread() is threading.main_thread():
        try:
            previous_sigint = _signal.getsignal(_signal.SIGINT)
            _signal.signal(_signal.SIGINT, _signal.default_int_handler)
        except (ValueError, OSError, RuntimeError):
            previous_sigint = None
    try:
        with TerminalGuard(), autonomous_mode():
            try:
                if config.view and _tty_available():
                    try:
                        from cli.lazy_monitor import run_monitor_session

                        result = run_monitor_session(engine, config, params)
                        report_result(result)
                        return result
                    except Exception as exc:
                        print_warn(f"view unavailable ({exc}); falling back to the panel")
                if not config.task_id:
                    created = engine.create_task(config.goal or f"engage {config.target or 'target'}")
                    config.task_id = str(created.get("task_id", ""))
                else:
                    print_msg(f"[*] resuming task {config.task_id}")
                print_msg(
                    f"[*] orchestrator: rounds<={config.rounds} "
                    f"workers={config.workers} — auto-invokes "
                    f"{'/'.join(engine.ORCHESTRATOR_CHAIN)}"
                )
                if config.progress and config.task_id:
                    result = _run_with_progress(engine, config)
                    result.setdefault("goal", config.goal)
                else:
                    result = _run_plain(engine, config)
                report_result(result)
                return result
            except (KeyboardInterrupt, SystemExit, EOFError):
                _abort_run(engine, config.task_id, "operator interrupt (Ctrl+C/Ctrl+D)")
                result = {"task_id": config.task_id, "cancelled": True, "overview": _overview(config.task_id)}
                report_result(result)
                return result
    finally:
        if previous_sigint is not None:
            try:
                _signal.signal(_signal.SIGINT, previous_sigint)
            except (ValueError, OSError, RuntimeError):
                pass


def _tty_available() -> bool:
    """Return True when a real terminal is attached to this process."""
    import sys

    for stream in (sys.stdin, sys.stdout):
        try:
            if stream is not None and stream.isatty():
                return True
        except Exception:
            continue
    return False


__all__ = [
    "LoopRunConfig",
    "build_executor",
    "parse_loop_line",
    "report_result",
    "resolve_loop_defaults",
    "run_loop",
]
