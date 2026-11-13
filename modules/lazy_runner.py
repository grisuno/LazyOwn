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
import json
import os
import queue
import re
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
DEFAULT_TARGET_CONCURRENCY = 3
_MAX_BATCH_TARGETS = 16
AUTO_PWN_MIN_TIMEOUT_SEC = 900.0
AUTONOMOUS_ENV = "LAZYOWN_AUTONOMOUS"
LOOP_WORKSPACE_ENV = "LAZYOWN_LOOP_WORKSPACE"
LOOP_RESULT_FILENAME = "result.json"
SUCCESS_LOOP_STATUSES = ("done", "pentest_proven")
EXIT_LOOP_ERROR = 1
EXIT_LOOP_TIMEOUT = 4


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
    budget: dict = field(default_factory=dict)
    budget_confirm: bool = False
    phishing_fallback: bool = False
    no_preflight: bool = False
    audit: object = field(default=None, compare=False)
    extra: dict = field(default_factory=dict)
    targets_file: str = ""
    max_concurrent: int = 0
    mode: str = ""

    def clamped(self) -> LoopRunConfig:
        """Clamp numeric knobs to the supported operating range."""
        self.rounds = max(1, min(MAX_ROUNDS, int(self.rounds or DEFAULT_ROUNDS)))
        self.workers = max(1, min(MAX_WORKERS, int(self.workers or DEFAULT_WORKERS)))
        self.timeout = max(0.0, float(self.timeout or 0.0))
        self.step_delay = max(0.0, float(self.step_delay or 0.0))
        self.verb_timeout = max(30.0, float(self.verb_timeout or DEFAULT_VERB_TIMEOUT_SEC))
        self.max_concurrent = max(0, int(self.max_concurrent or 0))
        known = str(self.mode or "").strip().lower()
        if known and known not in ENGAGEMENT_MODES:
            known = ""
        self.mode = known or self.mode
        return self


FLAG_VALUES = (
    "--target",
    "--task",
    "--profile",
    "--rounds",
    "--max-steps",
    "--workers",
    "--timeout",
    "--step-delay",
    "--budget",
    "--targets-from-file",
    "--max-concurrent",
    "--mode",
)
FLAG_TOGGLES = ("--no-bootstrap", "--view", "--plain", "--no-progress", "--budget-confirm", "--fallback-phish", "--no-preflight")
_BUDGET_KEYS = ("rounds", "toolcalls", "findings", "timeout_sec")
_BUDGET_MINIMUMS = {"rounds": 1, "toolcalls": 1, "findings": 1, "timeout_sec": 60.0}
ENGAGEMENT_MODES = ("pentest", "redteam", "ctf")
_MODE_HINT = "pentest stops the loop when exploitability is proven; redteam keeps compromising; ctf chases flags"


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
    targets_file = ""
    max_concurrent = 0
    no_bootstrap = False
    no_preflight = False
    progress = True
    view = False
    budget: dict[str, float] = {}
    budget_confirm = False
    phishing_fallback = False
    mode = ""
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
            elif token == "--targets-from-file":
                targets_file = value
            elif token == "--max-concurrent":
                max_concurrent = _to_int(value, 0)
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
            elif token == "--mode":
                known = str(value or "").strip().lower()
                if known not in ENGAGEMENT_MODES:
                    raise ValueError(f"--mode accepts {'/'.join(ENGAGEMENT_MODES)} ({_MODE_HINT})")
                mode = known
            elif token == "--budget":
                for chunk in str(value).split(","):
                    key, _, raw_value = chunk.strip().partition("=")
                    if key not in _BUDGET_KEYS or raw_value in ("", None):
                        raise ValueError(f"--budget accepts {'/'.join(_BUDGET_KEYS)}=N pairs (got {chunk!r})")
                    parsed = float(raw_value)
                    budget[key] = max(_BUDGET_MINIMUMS[key], parsed)
            idx += 2
            continue
        if token in FLAG_TOGGLES:
            if token == "--no-bootstrap":
                no_bootstrap = True
            elif token == "--no-preflight":
                no_preflight = True
            elif token == "--view":
                view = True
            elif token == "--budget-confirm":
                budget_confirm = True
            elif token == "--fallback-phish":
                phishing_fallback = True
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
        no_preflight=no_preflight,
        progress=progress,
        view=view,
        budget=budget,
        budget_confirm=budget_confirm,
        phishing_fallback=phishing_fallback,
        targets_file=targets_file,
        max_concurrent=max_concurrent,
        mode=mode,
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
    sandbox_task_id: str = "", sandbox_image: str = "", audit=None,
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

    When ``audit`` is provided, every dispatched command is recorded in
    the loop audit timeline with its duration and outcome.
    """

    def _resolve_alias(command: str) -> str:
        token = command.split()[0] if command.split() else ""
        aliases = getattr(shell, "aliases", None)
        if isinstance(aliases, dict) and aliases.get(token):
            rest = " ".join(command.split()[1:])
            return f"{aliases[token]} {rest}".strip()
        return command

    def _dispatch(command: str) -> str:
        text = str(command or "")
        if cancelled.get("flag"):
            return "execution failed: cancelled by operator"
        from utils import needs_sudo, sudo_available

        if needs_sudo(_resolve_alias(text)) and not sudo_available():
            stream(f"[skip] sudo unavailable in unattended mode: {text[:160]}")
            return f"skipped: sudo unavailable in unattended mode: {text[:160]}"
        stream(f">>> {text[:200]}")
        verb_timeout = config.verb_timeout
        if _resolve_alias(text).startswith("auto_pwn") and verb_timeout < AUTO_PWN_MIN_TIMEOUT_SEC:
            verb_timeout = AUTO_PWN_MIN_TIMEOUT_SEC
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
                        sandbox_task_id, text, timeout_sec=verb_timeout, image=sandbox_image
                    )
                except Exception as exc:
                    return f"execution failed: {exc}"
            try:
                return execute_shell_verb(shell, text, timeout_sec=verb_timeout, on_output=stream)
            except Exception as exc:
                return f"execution failed: {exc}"
        return execute_streaming(text, on_output=stream, timeout_sec=verb_timeout)

    def _executor(command: str) -> str:
        started = time.monotonic()
        try:
            outcome = _dispatch(command)
        except Exception as exc:
            outcome = f"execution failed: {exc}"
        if audit is not None:
            try:
                audit.record_command(command, outcome, time.monotonic() - started)
            except Exception:
                pass
        return outcome

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
    known = str(config.mode or "").strip().lower()
    if known in ENGAGEMENT_MODES:
        try:
            engine.engagement_mode = known
        except Exception:
            pass
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


def _start_browser_sync(params: dict) -> None:
    """Start the browser cookie sync receiver when payload asks for it."""
    if not bool((params or {}).get("browser_sync_enabled", True)):
        return
    try:
        port = int((params or {}).get("browser_sync_port", 8898) or 8898)
    except (TypeError, ValueError):
        port = 8898
    try:
        from modules import browser_sync

        status = browser_sync.start_receiver(port=port)
        if status.get("running"):
            inject = bool((params or {}).get("browser_sync_inject", True))
            print_msg(
                f"[*] browser sync {status['host']}:{status['port']} "
                f"cookies={status.get('cookies', 0)} inject={'on' if inject else 'off'}"
            )
    except Exception as exc:
        print_warn(f"browser sync autostart skipped: {exc}")


def _maybe_phishing_fallback(result: dict, config: LoopRunConfig, params: dict) -> dict:
    """Append the phishing handoff when the run ended without a foothold.

    Gated behind the explicit ``--fallback-phish`` operator flag. The
    fallback consults the live fact-store access token: when ANY session
    access already exists the handoff is skipped; otherwise
    :func:`modules.lazypoophish.run_fallback` stages the campaign (offline
    previews unless SMTP lives in ``payload.json``) and writes the
    handoff artefact. Never raises and never mutates ``result`` shape
    beyond the ``fallback`` key.

    Args:
        result: Final loop summary.
        config: Parsed loop invocation.
        params: Payload mapping.

    Returns:
        The same summary with a ``fallback`` key attached.
    """
    if not config.phishing_fallback or "fallback" in result:
        return result
    if result.get("cancelled") and not result.get("task_id"):
        return result
    target = str(config.target or "")
    if not target:
        return result
    try:
        from modules import lazypoophish

        if not lazypoophish.fallback_ready(target):
            result["fallback"] = {"ok": False, "skipped": "foothold already present"}
            return result
        summary = lazypoophish.run_fallback(target, params)
        result["fallback"] = summary
        if summary.get("ok"):
            print_msg(f"[*] phishing fallback staged: {summary.get('campaign_id', '')}")
            if summary.get("short_url"):
                print_msg(f"[*] short lure URL: {summary['short_url']}")
            print_msg(f"[*] handoff artefact: {summary.get('artifact', '')}")
        else:
            print_warn(f"[!] phishing fallback skipped: {summary.get('error', 'unknown error')}")
    except Exception as exc:
        print_warn(f"[!] phishing fallback unavailable: {exc}")
    return result


def loop_exit_code(result: dict) -> int:
    """Map one loop summary to an honest process exit code.

    A loop that only exhausted its rounds, timed out or stopped in a
    handoff is not a success: the dashboard marks loops on exit code, so
    this mapping keeps the finished/failed distinction truthful. The one
    promotion: when the independent verdict is ``achieved`` with
    verified evidence (a confirmed shell, captured credential), the run
    counts as success even if the engine merely exhausted its rounds.

    Args:
        result: Orchestrator summary.

    Returns:
        ``0`` when the run reached a success status or proven achieved
        evidence; ``4`` on timeout and ``1`` for every other ending.
    """
    if not isinstance(result, dict):
        return EXIT_LOOP_ERROR
    if result.get("error"):
        return EXIT_LOOP_ERROR
    if result.get("cancelled"):
        return EXIT_LOOP_ERROR
    if str(result.get("mode", "") or "") == "multi-target":
        return 0 if int(result.get("failed", 0) or 0) == 0 else EXIT_LOOP_ERROR
    status = str(result.get("status", "") or "")
    verdict = result.get("verdict") if isinstance(result.get("verdict"), dict) else {}
    if (
        str(verdict.get("verdict", "") or "") == "achieved"
        and bool(verdict.get("evidence_verified"))
        and status not in ("failed", "")
    ):
        return 0
    if status == "timeout":
        return EXIT_LOOP_TIMEOUT
    if status in SUCCESS_LOOP_STATUSES:
        verdict_text = str(verdict.get("verdict", "") or "")
        if verdict_text in ("", "achieved"):
            return 0
        return EXIT_LOOP_ERROR
    return EXIT_LOOP_ERROR


def autonomous_exit_gate(result: dict) -> None:
    """Convert a non-success loop ending into a non-zero process exit.

    Only active under the autonomous environment (C2-managed loop
    subprocesses): an interactive shell must survive a finished loop so
    the operator keeps working, while a dashboard loop must never look
    FINISHED when the goal was not achieved.

    Args:
        result: Orchestrator summary.

    Raises:
        SystemExit: When running autonomously and the outcome is not a
            success.
    """
    if os.environ.get(AUTONOMOUS_ENV, "") != "1":
        return
    code = loop_exit_code(result)
    if code == 0:
        return
    status = str(result.get("status", "") or "")
    print_warn(
        f"[loop] exit code {code}: loop ended without achieving the goal "
        f"(status={status or 'error'}) — inspect: loop_audit {result.get('task_id', '')}"
    )
    raise SystemExit(code)


def _loop_outcome(result: dict, goal: str = "") -> dict:
    """Project one loop summary into the durable outcome file payload."""
    verdict = result.get("verdict") if isinstance(result.get("verdict"), dict) else {}
    overview = result.get("overview") or {}
    return {
        "task_id": str(result.get("task_id", "") or ""),
        "status": str(result.get("status", "") or ("cancelled" if result.get("cancelled") else "")),
        "success": loop_exit_code(result) == 0,
        "verdict": str(verdict.get("verdict", "") or ""),
        "completion_reason": str(verdict.get("completion_reason", "") or ""),
        "evidence_verified": bool(verdict.get("evidence_verified")) if verdict else False,
        "rounds": int(result.get("rounds", 0) or 0),
        "facts": int(overview.get("facts", 0) or 0),
        "findings": int(overview.get("findings", 0) or 0),
        "goal": str(result.get("goal", "") or goal or ""),
        "error": str(result.get("error", "") or ""),
        "cancelled": bool(result.get("cancelled")),
        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def write_loop_result(config: LoopRunConfig, result: dict) -> None:
    """Persist the final loop outcome for the dashboard and the operator.

    The C2 loop manager cannot read the engine's internal status from a
    subprocess; it reads this file instead (workspace of the loop when
    running under the dashboard, ``sessions/loop_result_<task>.json``
    otherwise). Never raises.

    Args:
        config: Parsed run configuration.
        result: Orchestrator summary.
    """
    if not isinstance(result, dict) or not result:
        return
    outcome = _loop_outcome(result, goal=str(getattr(config, "goal", "") or ""))
    workspace = os.environ.get(LOOP_WORKSPACE_ENV, "")
    try:
        if workspace:
            path = Path(workspace) / LOOP_RESULT_FILENAME
        elif outcome.get("task_id"):
            path = Path(SESSIONS_DIR) / f"loop_result_{outcome['task_id']}.json"
        else:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, TypeError, ValueError):
        pass


def report_result(result: dict) -> None:
    """Print the final outcome of one loop run.

    Failed, cancelled or incomplete endings carry a retry offer so the
    operator can resume the exact task with user-varied flags, or arm
    the elevated ``--sudo`` mode when the failure was a sudo gate. The
    durable ledger handoff (states, confirmed evidence, discarded
    vectors, next decision) prints when present, and the independent
    goal verdict prints whenever the evaluator produced one, so a
    finished badge is never the only success claim.
    """
    if result.get("error"):
        print_error(f"lazy_loop failed: {result['error']}")
        task_id = str(result.get("task_id", "") or "")
        if task_id:
            print_warn(
                f"retry offer: retry loop {task_id} [--rounds N --target T] "
                "--sudo (elevated reruns prompt with a destructive-steps warning)"
            )
        return
    if result.get("cancelled"):
        print_warn(
            "lazy_loop cancelled by operator; partial state saved "
            f"({result.get('task_id') or 'no task'}). "
            "Inspect: lazy_status / lazy_trace"
        )
        task_id = str(result.get("task_id", "") or "")
        if task_id:
            print_warn(f"retry offer: retry loop {task_id} --sudo")
        return
    task_id = result.get("task_id", "")
    overview = result.get("overview", {}) or {}
    print_msg(
        f"[+] {task_id} [{result.get('status', '')}] rounds={result.get('rounds', 0)} "
        f"intents={len(overview.get('intents', []))} "
        f"facts={overview.get('facts', 0)} "
        f"findings={overview.get('findings', 0)}"
    )
    verdict = result.get("verdict") if isinstance(result.get("verdict"), dict) else {}
    if verdict:
        detail = str(verdict.get("completion_reason", "") or "")
        print_msg(
            f"[verdict] {verdict.get('verdict', '')} "
            f"coverage={verdict.get('coverage_pct', 0)}% "
            f"confirmed={verdict.get('confirmed', 0)}"
            + (f" ({detail})" if detail else "")
        )
        if verdict.get("path"):
            print_msg(f"[verdict] report: {verdict['path']}")
    _print_handoff(result.get("handoff") or {})
    if overview.get("findings"):
        print_warn(f"Findings present — inspect with: lazy_findings {task_id} / lazy_trace {task_id} list")
    if str(result.get("status", "")) in ("failed", "timeout", "exhausted", "handoff"):
        print_warn(
            "retry offer: retry loop "
            f"{task_id} [--sudo] (elevated reruns prompt with a destructive-steps warning)"
        )


def _print_handoff(handoff: dict) -> None:
    """Render the durable-ledger handoff block for the operator.

    Args:
        handoff: ``build_handoff`` result from the findings ledger.
    """
    if not isinstance(handoff, dict) or not handoff:
        return
    states = handoff.get("states") or {}
    if not any(states.values()):
        return
    print_msg(
        "[handoff] states: "
        + " ".join(f"{name}={count}" for name, count in states.items())
    )
    for item in handoff.get("confirmed") or []:
        technique = str(item.get("technique_id") or "")
        print_msg(f"[handoff] confirmed: {str(item.get('title', ''))[:120]}" + (f" [{technique}]" if technique else ""))
    for reason in handoff.get("discarded_vectors") or []:
        print_msg(f"[handoff] discarded: {str(reason)[:140]}")
    decision = str(handoff.get("next_decision", "") or "")
    if decision:
        print_msg(f"[handoff] next decision: {decision}")


def _bootstrap(scan_target: str, executor: Callable[[str], str]) -> None:
    """Ingest an existing nmap XML and stage the exposure report before round 1."""
    scan = Path(SESSIONS_DIR) / f"scan_{scan_target}.nmap.xml"
    if scan.exists():
        print_msg(f"[*] bootstrap: ingesting {scan.name} via auto_populate")
        started = time.monotonic()
        result = executor(f"auto_populate {scan_target}")
        if str(result).startswith("TIMEOUT"):
            print_warn(f"[!] bootstrap timed out after {int(time.monotonic() - started)}s; continuing")
        else:
            print_msg(f"[*] bootstrap done in {time.monotonic() - started:.1f}s")
    try:
        from modules.scan_brief import focus_summary, write_brief

        brief_path = write_brief(scan_target)
        if brief_path:
            from modules.scan_brief import load_brief

            print_msg(f"[*] bootstrap: scan brief staged at {brief_path} ({focus_summary(load_brief(brief_path))})")
    except Exception as exc:
        print_warn(f"[!] bootstrap scan brief skipped: {exc}")
    try:
        from modules.lazy_exposure import ensure_report

        path = ensure_report(scan_target)
        if path:
            print_msg(f"[*] bootstrap: exposure report staged at {path}")
    except Exception as exc:
        print_warn(f"[!] bootstrap intel report skipped: {exc}")


def _apply_budget(engine, task_id: str, budget: dict) -> None:
    """Persist per-task budget caps before orchestration begins."""
    if not task_id or not budget:
        return
    try:
        from modules.lazy_loop import Budget as _EngineBudget

        _EngineBudget(getattr(engine, "store", None)).set_limits(task_id, **budget)
        print_msg(f"[*] budget caps: {budget}")
    except Exception as exc:
        print_warn(f"[!] budget not applied: {exc}")


def _budget_declined(config: LoopRunConfig) -> bool:
    """Interactive confirm-gate for budget-constrained runs."""
    if not (config.budget and config.budget_confirm):
        return False
    if os.environ.get("LAZYOWN_AUTONOMOUS", "") == "1":
        return False
    try:
        reply = input(f"[*] budget caps {config.budget} will apply. Proceed? [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        reply = "n"
    if reply in ("y", "yes"):
        return False
    print_warn("budget run aborted at your request")
    return True


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
        audit=config.audit,
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


def _last_task_commands(task_id: str, limit: int = 5) -> list[str]:
    """Return the most recent commands the loop executed, oldest last.

    The stall dump must answer which command the loop was running when
    it froze, so the traffic ledger is the source of truth.

    Args:
        task_id: Task whose traffic ledger is read.
        limit: Maximum commands to include.

    Returns:
        Compact command strings (may be empty on any failure).
    """
    if not task_id:
        return []
    try:
        from modules.lazy_loop import TrafficLog

        rows = TrafficLog(task_id).read(limit=max(1, limit))
    except Exception:
        return []
    out: list[str] = []
    for row in rows:
        command = " ".join(str(row.get("command", "")).split())
        if not command:
            continue
        out.append(f"{command[:160]} ({row.get('kind', 'bash')})")
    return out


def _dump_thread_stacks(task_id: str = "", target=None) -> None:
    """Dump all thread stacks to stderr so a stuck loop is identifiable.

    When a task id is given the last executed commands are printed first,
    in plain English and without emojis, so the operator knows exactly
    which command was in flight (or timed out) before the stack dump.

    Args:
        task_id: Task whose recent commands precede the dump.
        target: Writable stream override (tests); defaults to the real
            stderr so redirected shells cannot swallow the dump.
    """
    import faulthandler
    import sys

    if target is None:
        target = getattr(sys, "__stderr__", None) or sys.stderr
    try:
        target.write("\n[stall] no loop activity; dumping all thread stacks:\n")
        for line in _last_task_commands(task_id):
            target.write(f"[stall] last command: {line}\n")
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
            _dump_thread_stacks(task_id)
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
        audit=config.audit,
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


def bind_target_authority(shell, targets: list[str]) -> dict:
    """Make the run's target(s) authoritative over payload rhost and scope.

    The loop binds a target to the task, but offensive verbs and the scope
    guard read ``rhost`` and ``scope`` from ``payload.json``. When those
    are stale, a run can act against a host the operator never named: a
    verb falls back to a stale ``rhost`` or the planner wanders onto a
    stale but still-in-scope host. This binds ``rhost`` to the primary
    target and replaces the authorized scope with exactly the run's
    targets, so the loop can only touch what was requested. Writes go
    through the shell's single payload writer; the enforcement posture is
    left untouched.

    Args:
        shell: The live LazyOwn shell whose params back the payload.
        targets: The validated run target(s); the first is the primary
            ``rhost`` and the full list becomes the authorized scope.

    Returns:
        A summary mapping (``bound``, ``rhost``, ``scope``, and the prior
        values) or ``{"bound": False}`` when there is nothing to bind.
    """
    clean: list[str] = []
    for item in targets or []:
        value = str(item or "").strip()
        if value and value not in clean:
            clean.append(value)
    params = getattr(shell, "params", None)
    if not clean or not isinstance(params, dict):
        return {"bound": False}
    primary = clean[0]
    previous_rhost = params.get("rhost")
    previous_scope = list(params.get("scope") or [])
    if str(previous_rhost or "") == primary and previous_scope == clean:
        return {"bound": False}
    params["rhost"] = primary
    try:
        if hasattr(shell, "_scope_save"):
            shell._scope_save(entries=list(clean))
        else:
            from core.config import save_payload

            params["scope"] = list(clean)
            save_payload(params)
    except Exception as exc:
        print_warn(f"[!] target authority bind failed: {exc}")
        return {"bound": False, "error": str(exc)}
    print_msg(
        f"[*] target authority: rhost={primary} scope={clean} "
        f"(was rhost={previous_rhost!r} scope={previous_scope or '[]'})"
    )
    return {
        "bound": True,
        "rhost": primary,
        "scope": list(clean),
        "previous_rhost": previous_rhost,
        "previous_scope": previous_scope,
    }


def load_targets_file(path: str) -> list[str]:
    """Read and validate one target per line from a scope file.

    Numeric dotted entries must parse as real IPs (``999.999.1.1`` is
    rejected even though the hostname regex would accept it); anything
    else goes through the shared host policy.

    Args:
        path: Plain-text file; blank lines and ``#`` comments skipped.

    Returns:
        Deduplicated valid hosts or CIDR blocks, capped at
        ``_MAX_BATCH_TARGETS``.

    Raises:
        ValueError: Missing file or no valid target inside.
    """
    import ipaddress

    from core.hardening import validate_host

    file_path = Path(str(path or "").strip())
    if not file_path.is_file():
        raise ValueError(f"targets file not found: {file_path}")
    targets: list[str] = []
    for raw_line in file_path.read_text(encoding="utf-8", errors="replace").splitlines():
        candidate = raw_line.strip()
        if not candidate or candidate.startswith("#"):
            continue
        host = candidate.split()[0]
        numeric = all(re.fullmatch(r"[\d.]+(?:/\d{1,2})?", token) for token in host.split("/"))
        valid = False
        if numeric and host[:1].isdigit():
            for parser in (ipaddress.ip_address, lambda value: ipaddress.ip_network(value, strict=False)):
                try:
                    parser(host)
                    valid = True
                    break
                except ValueError:
                    continue
        else:
            valid = validate_host(host)
        if not valid:
            print_warn(f"[!] targets file skipped invalid entry: {candidate[:60]}")
            continue
        if host not in targets:
            targets.append(host)
        if len(targets) >= _MAX_BATCH_TARGETS:
            print_warn(f"[!] targets file capped at {_MAX_BATCH_TARGETS} targets")
            break
    if not targets:
        raise ValueError(f"no valid targets in file: {file_path}")
    return targets


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
    if config.targets_file and not config.task_id:
        return _run_targets_file(shell, params, config)
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
    _start_browser_sync(params)
    print_msg(f"[*] orchestrator chain: {'/'.join(engine.ORCHESTRATOR_CHAIN)}")
    if _budget_declined(config):
        return {"task_id": config.task_id, "cancelled": True, "error": "budget declined"}
    if config.budget and not config.task_id:
        try:
            created = engine.create_task(config.goal or f"engage {config.target or 'target'}")
            config.task_id = str(created.get("task_id", ""))
            if config.target:
                engine.ensure_target(config.task_id, config.target, "loop target")
        except Exception as exc:
            print_warn(f"[!] pre-task budget failed: {exc}")
    if config.budget:
        _apply_budget(engine, config.task_id, config.budget)

    import signal as _signal

    previous_sigint = None
    if threading.current_thread() is threading.main_thread():
        try:
            previous_sigint = _signal.getsignal(_signal.SIGINT)
            _signal.signal(_signal.SIGINT, _signal.default_int_handler)
        except (ValueError, OSError, RuntimeError):
            previous_sigint = None
    result: dict = {}
    audit = None
    try:
        with TerminalGuard(), autonomous_mode():
            try:
                if config.view and _tty_available():
                    try:
                        from cli.lazy_monitor import run_monitor_session

                        result = run_monitor_session(engine, config, params)
                        result.setdefault("goal", config.goal)
                        report_result(result)
                    except Exception as exc:
                        print_warn(f"view unavailable ({exc}); falling back to the panel")
                if not result:
                    if not config.task_id:
                        created = engine.create_task(config.goal or f"engage {config.target or 'target'}")
                        config.task_id = str(created.get("task_id", ""))
                    else:
                        print_msg(f"[*] resuming task {config.task_id}")
                    try:
                        from modules import loop_audit

                        audit = loop_audit.start(config.task_id)
                        config.audit = audit
                    except Exception:
                        audit = None
                    if audit is not None:
                        try:
                            audit.run_start(
                                goal=config.goal,
                                target=config.target,
                                rounds=config.rounds,
                                workers=config.workers,
                                mode=str(config.mode or getattr(engine, "engagement_mode", "") or ""),
                                profile=str(config.profile or ""),
                            )
                        except Exception:
                            pass
                    preflight_failed = False
                    if config.target and not config.no_preflight:
                        failure = _preflight_gate(engine, config, audit)
                        if failure:
                            result = failure
                            preflight_failed = True
                            report_result(result)
                    if not result:
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
                        result = _maybe_phishing_fallback(result, config, params)
                        report_result(result)
                        if audit is not None and not preflight_failed:
                            try:
                                if result.get("verdict"):
                                    audit.verdict(result.get("verdict") or {})
                                audit.run_end(
                                    status=str(
                                        result.get("status", "")
                                        or ("cancelled" if result.get("cancelled") else "")
                                    ),
                                    rounds=int(result.get("rounds", 0) or 0),
                                    verdict=result.get("verdict") or {},
                                    error=str(result.get("error", "") or ""),
                                )
                            except Exception:
                                pass
            except (KeyboardInterrupt, SystemExit, EOFError):
                _abort_run(engine, config.task_id, "operator interrupt (Ctrl+C/Ctrl+D)")
                result = {"task_id": config.task_id, "cancelled": True, "overview": _overview(config.task_id)}
                report_result(result)
                if audit is not None:
                    try:
                        audit.run_end(status="cancelled", rounds=0, error="operator interrupt")
                    except Exception:
                        pass
    finally:
        if previous_sigint is not None:
            try:
                _signal.signal(_signal.SIGINT, previous_sigint)
            except (ValueError, OSError, RuntimeError):
                pass
    write_loop_result(config, result)
    autonomous_exit_gate(result)
    return result


def _preflight_gate(engine, config: LoopRunConfig, audit) -> dict:
    """Validate the target before spending a single round on it.

    Args:
        engine: The live loop engine (task store access).
        config: Parsed run configuration with the task already bound.
        audit: Active audit handle for the preflight event.

    Returns:
        A failed summary when the target is unreachable or its lab
        scenario is down; empty dict when the run may proceed.
    """
    from modules import loop_preflight

    outcome = loop_preflight.check_target(config.target)
    if audit is not None:
        try:
            audit.preflight(outcome)
        except Exception:
            pass
    if outcome.get("ok"):
        print_msg(f"[*] preflight: {outcome.get('reason', '')}")
        return {}
    hint = loop_preflight.recovery_hint(outcome)
    print_error(f"[preflight] refusing to run: {outcome.get('reason', '')}")
    if hint:
        print_warn(f"[preflight] {hint}")
    try:
        engine.store.set_status(config.task_id, "preflight_failed")
    except Exception:
        pass
    if audit is not None:
        try:
            audit.run_end(status="preflight_failed", rounds=0, error=outcome.get("reason", ""))
        except Exception:
            pass
    return {
        "task_id": config.task_id,
        "status": "preflight_failed",
        "error": str(outcome.get("reason", "")),
        "verdict": {},
        "rounds": 0,
        "overview": {},
        "goal": config.goal,
    }


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


def _run_targets_file(shell, params: dict, config: LoopRunConfig) -> dict:
    """Run one loop per target from a scope file with a concurrency cap.

    Each target gets its own task and worker pool; the semaphore shared
    through :class:`~modules.loop_guardrails.TargetLimiter` keeps at
    most ``--max-concurrent`` (default 3) targets active at once so the
    operator uplink is never saturated.
    """
    try:
        targets = load_targets_file(config.targets_file)
    except ValueError as exc:
        print_error(f"lazy_loop: {exc}")
        return {"error": str(exc)}
    from dataclasses import replace

    from modules.loop_guardrails import TargetLimiter

    max_concurrent = config.max_concurrent or DEFAULT_TARGET_CONCURRENCY
    limiter = TargetLimiter(max_concurrent=max_concurrent)
    print_msg(f"[*] multi-target run: {len(targets)} target(s), max {max_concurrent} concurrent")
    results: dict[str, dict] = {}
    lock = threading.Lock()

    def _work_one(target: str) -> None:
        single = replace(config, targets_file="", target=target, task_id="")

        def _limited() -> dict:
            with limiter.slot(target):
                return run_loop(shell, params, single)

        try:
            summary = _limited()
        except Exception as exc:
            summary = {"target": target, "error": str(exc)}
        with lock:
            results[target] = summary

    threads = [threading.Thread(target=_work_one, args=(target,), daemon=True) for target in targets]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    ok = sum(1 for summary in results.values() if summary.get("task_id") and not summary.get("error"))  # type: ignore[union-attr]
    return {
        "mode": "multi-target",
        "targets": targets,
        "ok": ok,
        "failed": len(results) - ok,
        "results": results,
    }


__all__ = [
    "AUTONOMOUS_ENV",
    "ENGAGEMENT_MODES",
    "LOOP_RESULT_FILENAME",
    "LoopRunConfig",
    "autonomous_exit_gate",
    "build_executor",
    "bind_target_authority",
    "load_targets_file",
    "loop_exit_code",
    "parse_loop_line",
    "report_result",
    "resolve_loop_defaults",
    "run_loop",
    "write_loop_result",
]
