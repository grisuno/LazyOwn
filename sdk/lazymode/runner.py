"""The lazymode code runners (hybrid: Python subprocess + Lua in-process).

Code mode (programmatic tool calling) turns many separate tool round-trips
into one script that drives the framework through the :class:`sdk.facade.Lazy`
surface and returns only what matters, keeping intermediate output out of
the model context. Two backends share one result contract:

- ``run_python`` runs the script in a separate process with CPU, memory
  and wall-clock bounds, so a crash or a runaway loop never affects the
  caller. It reuses :mod:`sdk.lazymode._bootstrap`.
- ``run_lua`` runs the script in a lupa Lua runtime in-process, reusing
  the Lua substrate LazyOwn already ships for its plugin system. It is
  faster to start and lighter, at the cost of weaker isolation.

Both build the scope check from the operator payload so a script cannot
drive an offensive operation against an out-of-scope target when the
operator posture is ``enforce``.
"""

from __future__ import annotations

import json
import os
import resource
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from cli.scope_guard import ScopeGuard
from core.dependencies import optional_attr
from sdk.errors import ScopeBlocked
from sdk.lazymode._bootstrap import ENVELOPE_SENTINEL

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BOOTSTRAP_PATH = Path(__file__).resolve().parent / "_bootstrap.py"
_DEFAULT_PAYLOAD_PATH = _REPO_ROOT / "payload.json"
_DEFAULT_SESSIONS_DIR = _REPO_ROOT / "sessions"

_DEFAULT_WALL_TIMEOUT = 300.0
_DEFAULT_CPU_SECONDS = 120
_CPU_TIMEOUT_FACTOR = 2
_DEFAULT_MEMORY_BYTES = 2 * 1024 * 1024 * 1024
_MAX_STDOUT_CHARS = 8000
_LUA_LOG_GLOBAL = "log"
_LUA_FACADE_GLOBAL = "lazy"


def _bounded(text: str) -> str:
    """Return *text* capped to keep code mode's context saving intact.

    Args:
        text: The captured output.

    Returns:
        The text unchanged when short, else its head plus a marker.
    """
    if len(text) <= _MAX_STDOUT_CHARS:
        return text
    dropped = len(text) - _MAX_STDOUT_CHARS
    return f"{text[:_MAX_STDOUT_CHARS]}\n... [{dropped} chars truncated]"


LuaRuntime = optional_attr("lupa", "LuaRuntime")


@dataclass(frozen=True)
class LazymodeResult:
    """Outcome of one lazymode script execution.

    Attributes:
        backend: The runner used, ``python`` or ``lua``.
        ok: Whether the script completed without raising.
        result: The script's declared result value, JSON-safe.
        stdout: Captured script output.
        error: Traceback or error text, empty on success.
        duration_s: Wall-clock runtime in seconds.
    """

    backend: str
    ok: bool
    result: Any
    stdout: str
    error: str
    duration_s: float

    def to_dict(self) -> dict[str, Any]:
        """Return the result as a plain dict for JSON serialization."""
        return asdict(self)


def build_scope_check(payload: dict[str, Any]):
    """Return a scope check callback built from the operator payload.

    The callback reuses :class:`cli.scope_guard.ScopeGuard` so lazymode
    honours the exact same posture as the interactive shell. Every SDK
    offensive helper is treated as offensive; the guard still allows a
    command with no resolvable target, keeping the posture fail-open.

    Args:
        payload: The loaded ``payload.json`` mapping.

    Returns:
        A ``callable(command, target)`` that raises
        :class:`sdk.errors.ScopeBlocked` when the guard blocks the target.
    """
    guard = ScopeGuard(
        scope_entries=payload.get("scope", []),
        mode=payload.get("scope_enforcement", "warn"),
        is_offensive=lambda command: True,
        deny_entries=payload.get("scope_deny"),
    )

    def _check(command: str, target: str) -> None:
        decision = guard.evaluate(command, target)
        if not decision.allowed:
            raise ScopeBlocked(decision.reason)

    return _check


def _cpu_seconds_for(timeout: float) -> int:
    """Return the CPU-second rlimit matched to a wall-clock *timeout*.

    The CPU limit must leave headroom for legitimate CPU-heavy, possibly
    multi-threaded work (for example an msfconsole-backed exploit spec) up
    to the requested wall-clock budget; the wall-clock timeout remains the
    real bound. A fixed low CPU cap would kill such work with SIGXCPU.

    Args:
        timeout: The requested wall-clock timeout in seconds.

    Returns:
        The CPU-second soft limit to apply.
    """
    return max(_DEFAULT_CPU_SECONDS, int(timeout) * _CPU_TIMEOUT_FACTOR)


def _set_limits(cpu_seconds: int) -> None:
    """Apply CPU and address-space rlimits to the current process.

    Runs in the forked child before the interpreter starts so a runaway
    script is bounded. Any platform that rejects a limit is tolerated.

    Args:
        cpu_seconds: The CPU-second soft limit to request.
    """
    for which, soft in (
        (resource.RLIMIT_CPU, cpu_seconds),
        (resource.RLIMIT_AS, _DEFAULT_MEMORY_BYTES),
    ):
        try:
            _, hard = resource.getrlimit(which)
            ceiling = soft if hard == resource.RLIM_INFINITY else min(soft, hard)
            resource.setrlimit(which, (ceiling, hard))
        except (ValueError, OSError):
            continue


def _parse_envelope(stdout: str) -> dict[str, Any] | None:
    """Extract the JSON result envelope emitted after the sentinel.

    Args:
        stdout: The subprocess combined stdout.

    Returns:
        The parsed envelope, or None when no envelope was emitted.
    """
    marker = f"\n{ENVELOPE_SENTINEL}\n"
    index = stdout.rfind(marker)
    if index == -1:
        return None
    try:
        return json.loads(stdout[index + len(marker) :])
    except (ValueError, TypeError):
        return None


def run_python(
    script: str,
    *,
    payload_path: str | os.PathLike[str] | None = None,
    sessions_dir: str | os.PathLike[str] | None = None,
    timeout: float = _DEFAULT_WALL_TIMEOUT,
) -> LazymodeResult:
    """Run a lazymode Python script in a bounded subprocess.

    Args:
        script: The Python source to execute with ``lazy`` in scope.
        payload_path: Override for the payload path handed to the SDK.
        sessions_dir: Override for the sessions directory.
        timeout: Wall-clock timeout in seconds.

    Returns:
        The :class:`LazymodeResult` for the execution.
    """
    payload_path = str(payload_path or _DEFAULT_PAYLOAD_PATH)
    sessions_dir = str(sessions_dir or _DEFAULT_SESSIONS_DIR)
    started = time.monotonic()
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as handle:
        handle.write(script)
        script_path = handle.name
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(_REPO_ROOT), str(_REPO_ROOT / "modules"), env.get("PYTHONPATH", "")])
    try:
        completed = subprocess.run(
            [sys.executable, str(_BOOTSTRAP_PATH), script_path, payload_path, sessions_dir],
            cwd=str(_REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=lambda: _set_limits(_cpu_seconds_for(timeout)),
        )
    except subprocess.TimeoutExpired:
        return LazymodeResult("python", False, None, "", f"timeout after {timeout}s", time.monotonic() - started)
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass
    envelope = _parse_envelope(completed.stdout)
    if envelope is None:
        return LazymodeResult(
            "python",
            False,
            None,
            completed.stdout,
            completed.stderr or "no result envelope emitted",
            time.monotonic() - started,
        )
    return LazymodeResult(
        "python",
        bool(envelope.get("ok")),
        envelope.get("result"),
        envelope.get("stdout", ""),
        envelope.get("error", ""),
        time.monotonic() - started,
    )


def run_lua(
    script: str,
    *,
    payload_path: str | os.PathLike[str] | None = None,
    sessions_dir: str | os.PathLike[str] | None = None,
) -> LazymodeResult:
    """Run a lazymode Lua script in-process against the SDK facade.

    The Lua chunk reaches the framework through the ``lazy`` global (dot
    syntax, e.g. ``lazy.sh("id")``, because the Python methods are already
    bound) and may append progress with ``log(message)``. A top-level
    ``return`` becomes the script result.

    Args:
        script: The Lua source to execute.
        payload_path: Override for the payload path handed to the SDK.
        sessions_dir: Override for the sessions directory.

    Returns:
        The :class:`LazymodeResult` for the execution.
    """
    started = time.monotonic()
    if LuaRuntime is None:
        return LazymodeResult("lua", False, None, "", "lupa not installed", 0.0)
    from core.config import load_payload
    from sdk.facade import Lazy

    payload_file = str(payload_path or _DEFAULT_PAYLOAD_PATH)
    payload = load_payload(payload_file)
    lazy = Lazy(
        payload_path=payload_file,
        sessions_dir=str(sessions_dir or _DEFAULT_SESSIONS_DIR),
        scope_check=build_scope_check(payload),
    )
    logs: list[str] = []
    runtime = LuaRuntime(unpack_returned_tuples=True)
    runtime.globals()[_LUA_FACADE_GLOBAL] = lazy
    runtime.globals()[_LUA_LOG_GLOBAL] = lambda message: logs.append(str(message))
    try:
        value = runtime.execute(script)
        return LazymodeResult("lua", True, value, _bounded("\n".join(logs)), "", time.monotonic() - started)
    except BaseException as exc:
        return LazymodeResult(
            "lua", False, None, _bounded("\n".join(logs)), f"{type(exc).__name__}: {exc}", time.monotonic() - started
        )


def run(script: str, lang: str = "python", **kwargs: Any) -> LazymodeResult:
    """Run a lazymode script with the backend selected by *lang*.

    Args:
        script: The script source.
        lang: ``python`` (bounded subprocess) or ``lua`` (in-process).
        **kwargs: Forwarded to the selected runner.

    Returns:
        The :class:`LazymodeResult` for the execution.

    Raises:
        ValueError: When *lang* names no known backend.
    """
    normalized = (lang or "python").strip().lower()
    if normalized == "python":
        return run_python(script, **kwargs)
    if normalized == "lua":
        return run_lua(script, **kwargs)
    raise ValueError(f"unknown lazymode backend: {lang!r}")
