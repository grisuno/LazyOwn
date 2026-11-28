#!/usr/bin/env python3
"""Dispatch sweep: drive every indexed command through the real shell.

Boots ``LazyOwnShell``, stubs the executor and ``input`` so no side
effect can escape, then dispatches commands from
``cli/command_index.json`` with no arguments. A command that dispatches
into an uncaught ``AttributeError``/``NameError``/``TypeError`` (the
class of regression the unit suite misses) is reported by name.

Two modes:

- In-process (default): one shell dispatches every command from worker
  threads. Fast, but hung interactive commands accumulate runaway
  threads that degrade the remaining dispatches.
- Isolated (``--isolated``): one subprocess per command via
  ``--single``. A hung command is killed at the subprocess timeout with
  no effect on the next dispatch. Used by the CI gate.

Usage::

    python3 scripts/dispatch_sweep.py            # print report, exit 1 on crashes
    python3 scripts/dispatch_sweep.py --stdout   # JSON to stdout
    python3 scripts/dispatch_sweep.py --isolated # subprocess-per-command mode
    python3 scripts/dispatch_sweep.py --single groq
"""

from __future__ import annotations

import argparse
import io
import json
import os
import queue
import subprocess
import sys
import threading
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
os.environ.setdefault("NOBANNER", "1")
os.environ.setdefault("LAZYOWN_AUTO_CRYPTO", "0")

CRASH_MARKS = ("AttributeError", "NameError", "TypeError", "UnboundLocalError", "Traceback (most recent call last)")
_PER_COMMAND_TIMEOUT_SEC = 5.0
_ISOLATED_COMMAND_TIMEOUT_SEC = 20.0


class _FakeResult:
    def __init__(self) -> None:
        self.returncode = 0
        self.exit_code = 0
        self.stdout = ""
        self.stderr = ""
        self.pid = 12345

    @staticmethod
    def communicate(input=None, timeout=None):
        return "", ""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def poll(self):
        return 0

    def wait(self, timeout=None):
        return 0

    def kill(self):
        return None


class _StubExecutor:
    def __init__(self) -> None:
        self.commands: list[str] = []

    def run(self, command, env=None, **kwargs):
        self.commands.append(str(command))
        return _FakeResult()

    def run_passthrough(self, command, env=None, **kwargs):
        self.commands.append(str(command))
        return 0

    def run_tee(self, command, env=None, **kwargs):
        self.commands.append(str(command))
        return _FakeResult()

    def set_thread_timeout(self, *args, **kwargs):
        return None

    def clear_thread_timeout(self, *args, **kwargs):
        return None

    def set_thread_stdin_devnull(self, *args, **kwargs):
        return None

    def clear_thread_stdin_devnull(self, *args, **kwargs):
        return None

    def shutdown(self, *args, **kwargs):
        return None

    def last_exit_code(self):
        return 0


def _stub_environment() -> None:
    import builtins

    import utils

    utils.run_command = lambda command, **kwargs: f"[swept] {command}"

    def _eof_input(*args, **kwargs):
        raise EOFError(*args)

    builtins.input = _eof_input

    import modules.command_executor as executor_module

    executor_module.get_executor = lambda: _StubExecutor()

    import subprocess as _subprocess

    def _fake_run(*args, **kwargs):
        return _FakeResult()

    _subprocess.run = _fake_run
    _subprocess.call = lambda *args, **kwargs: 0
    _subprocess.check_output = lambda *args, **kwargs: b""
    _subprocess.check_call = lambda *args, **kwargs: 0
    _subprocess.getoutput = lambda *args, **kwargs: ""
    _subprocess.getstatusoutput = lambda *args, **kwargs: (0, "")
    _subprocess.Popen = _fake_run

    import os as _os

    def _no_exit(code=0):
        raise SystemExit(code)

    _os._exit = _no_exit
    _os.execvp = _no_exit
    _os.execv = _no_exit
    _os.execl = _no_exit
    _os.execle = _no_exit
    _os.execlp = _no_exit

    import time as _time

    _time.sleep = lambda *args, **kwargs: None

    import signal as _signal

    _signal.signal = lambda *args, **kwargs: None
    if hasattr(_signal, "pthread_sigmask"):
        _signal.pthread_sigmask = lambda *args, **kwargs: 0

    try:
        import curses as _curses

        for _fn in (
            "initscr",
            "nocbreak",
            "cbreak",
            "endwin",
            "noecho",
            "echo",
            "curs_set",
            "start_color",
            "keypad",
            "napms",
            "doupdate",
            "refresh",
            "raw",
            "noraw",
            "nonl",
            "nl",
            "meta",
            "use_env",
            "setupterm",
        ):
            if hasattr(_curses, _fn):
                setattr(_curses, _fn, lambda *args, **kwargs: None)
    except ImportError:
        pass

    try:
        import requests as _requests

        class _FakeResponse:
            status_code = 0
            content = b""
            text = ""

            @staticmethod
            def json():
                return {}

            def iter_content(self, *args, **kwargs):
                return iter([b""])

            @staticmethod
            def raise_for_status():
                return None

        _requests.Session.request = lambda *args, **kwargs: _FakeResponse()
    except ImportError:
        pass


def _classify(combined: str) -> tuple[str, str]:
    """Return the (verdict, error) pair for one dispatch output.

    Args:
        combined: Sentinel or captured output from the dispatch.

    Returns:
        Verdict string (``crash``/``usage``/``eof``/``ok``) plus the
        error tail for crashes.
    """
    if combined.startswith("__EXC__"):
        return "crash", combined[len("__EXC__") :]
    if combined in ("__EOF__", "__USAGE__"):
        return "usage", ""
    if combined and any(mark in combined for mark in CRASH_MARKS):
        return "crash", combined.strip()[-300:]
    if combined and combined.strip():
        return "usage", ""
    return "ok", ""


def _dispatch_single(command_name: str) -> dict:
    """Dispatch one command in-process and classify the outcome.

    Args:
        command_name: Command verb to dispatch (no ``do_`` prefix).

    Returns:
        Verdict dict with ``name``, ``verdict`` and ``error`` keys.
    """
    _stub_environment()
    import lazyown

    shell = lazyown.LazyOwnShell()
    out, err = io.StringIO(), io.StringIO()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            shell.onecmd(command_name)
    except SystemExit:
        combined = ""
    except Exception as exc:
        if isinstance(exc, EOFError):
            combined = "__EOF__"
        elif type(exc).__name__ == "Cmd2ArgparseError":
            combined = "__USAGE__"
        else:
            combined = f"__EXC__{type(exc).__name__}: {exc}"[:300]
    else:
        combined = out.getvalue() + err.getvalue()
    verdict, error = _classify(combined)
    return {"name": command_name, "verdict": verdict, "error": error}


def _sweep_isolated(names: list[str]) -> dict:
    """Dispatch every command in its own subprocess and merge verdicts.

    Args:
        names: Command verbs to sweep.

    Returns:
        Report dict with ``crashed`` (name + error tail), ``hung``,
        ``usage_error`` and ``ok_count`` lists.
    """
    crashed: list[dict[str, str]] = []
    hung: list[str] = []
    usage_error: list[str] = []
    ok = 0
    for name in names:
        try:
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "--single", name],
                capture_output=True,
                text=True,
                timeout=_ISOLATED_COMMAND_TIMEOUT_SEC,
                cwd=REPO_ROOT,
            )
        except subprocess.TimeoutExpired:
            hung.append(name)
            continue
        try:
            verdict = json.loads(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            hung.append(name)
            continue
        if verdict["verdict"] == "crash":
            crashed.append({"name": verdict["name"], "error": verdict["error"]})
        elif verdict["verdict"] == "ok":
            ok += 1
        else:
            usage_error.append(verdict["name"])
    return {
        "total": len(names),
        "crashed": crashed,
        "hung": hung,
        "usage_error": usage_error,
        "ok_count": ok,
    }


def _sweep_names(start: int = 0, limit: int | None = None, stride: int = 1) -> list[str]:
    """Return the sorted command names the sweep covers.

    YAML addon commands are excluded: they all share the single
    ``wrapper_yaml`` implementation (covered by the addon_args unit
    tests), and sweeping them would trigger archetype-A auto-installs.

    Args:
        start: Index of the first name (segmented runs).
        limit: Maximum number of names (``None`` = all).
        stride: Take every Nth name (sampling).

    Returns:
        The filtered, sorted command-name list.
    """
    index = json.loads((REPO_ROOT / "cli" / "command_index.json").read_text(encoding="utf-8"))
    names = sorted(
        {
            entry["name"].removeprefix("do_")
            for entry in index["commands"]
            if not entry.get("source_file", "").startswith("lazyaddons/")
        }
    )
    if stride > 1:
        names = names[start::stride]
    else:
        names = names[start:]
    if limit is not None:
        names = names[:limit]
    return names


def sweep(
    start: int = 0,
    limit: int | None = None,
    stride: int = 1,
    isolated: bool = False,
) -> dict:
    """Dispatch every indexed command once and classify the outcome.

    Args:
        start: Index of the first command to sweep (segmented runs).
        limit: Maximum number of commands to sweep (``None`` = all).
        stride: Sweep every Nth command (sampling).
        isolated: Run one subprocess per command instead of worker threads.

    Returns:
        Report dict with ``crashed`` (name + error tail), ``hung``,
        ``usage_error`` and ``ok_count`` lists.
    """
    names = _sweep_names(start=start, limit=limit, stride=stride)
    if isolated:
        return _sweep_isolated(names)

    _stub_environment()
    import lazyown

    shell = lazyown.LazyOwnShell()

    crashed: list[dict[str, str]] = []
    usage_error: list[str] = []
    ok: list[str] = []
    hung: list[str] = []

    def _dispatch(command_name: str, results: queue.Queue[tuple[str, str]]) -> None:
        out, err = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                shell.onecmd(command_name)
        except SystemExit:
            results.put((command_name, ""))
            return
        except Exception as exc:
            if isinstance(exc, EOFError):
                results.put((command_name, "__EOF__"))
                return
            if type(exc).__name__ == "Cmd2ArgparseError":
                results.put((command_name, "__USAGE__"))
                return
            results.put((command_name, f"__EXC__{type(exc).__name__}: {exc}"[:300]))
            return
        results.put((command_name, out.getvalue() + err.getvalue()))

    for name in names:
        results: queue.Queue[tuple[str, str]] = queue.Queue()
        worker = threading.Thread(target=_dispatch, args=(name, results), daemon=True)
        saved_stdout, saved_stderr = sys.stdout, sys.stderr
        worker.start()
        if os.environ.get("SWEEP_VERBOSE"):
            import time as _t

            sys.stderr.write(f"dispatching: {name} (t={_t.monotonic():.1f})\n")
            sys.stderr.flush()
        try:
            _name, combined = results.get(timeout=_PER_COMMAND_TIMEOUT_SEC)
        except queue.Empty:
            hung.append(name)
            if os.environ.get("SWEEP_VERBOSE"):
                sys.stderr.write(f"hung: {name}\n")
                sys.stderr.flush()
            continue
        finally:
            sys.stdout, sys.stderr = saved_stdout, saved_stderr
        verdict, error = _classify(combined)
        if verdict == "crash":
            crashed.append({"name": name, "error": error})
        elif verdict == "ok":
            ok.append(name)
        else:
            usage_error.append(name)
    return {
        "total": len(names),
        "crashed": crashed,
        "hung": hung,
        "usage_error": usage_error,
        "ok_count": len(ok),
    }


def main() -> int:
    """Run the sweep and exit 1 when any dispatch crashed.

    Returns:
        0 when every command dispatches crash-free, 1 otherwise.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--stdout", action="store_true", help="print the JSON report to stdout")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / "sessions" / "dispatch_sweep_report.json"),
        help="write the JSON report to this path",
    )
    parser.add_argument("--start", type=int, default=0, help="first command index (segmented runs)")
    parser.add_argument("--limit", type=int, default=None, help="maximum commands per segment")
    parser.add_argument("--stride", type=int, default=1, help="sweep every Nth command")
    parser.add_argument(
        "--isolated", action="store_true", help="run one subprocess per command (no thread accumulation)"
    )
    parser.add_argument("--single", default="", help="dispatch exactly one command and print its JSON verdict")
    parser.add_argument("--list-names", action="store_true", help="print the swept command names as JSON and exit")
    args = parser.parse_args()
    if args.list_names:
        sys.stdout.write(json.dumps(_sweep_names(start=0, stride=1)) + "\n")
        return 0
    if args.single:
        sys.stdout.write(json.dumps(_dispatch_single(args.single)) + "\n")
        return 0
    report = sweep(start=args.start, limit=args.limit, stride=args.stride, isolated=args.isolated)
    payload = json.dumps(report, indent=2)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(payload + "\n", encoding="utf-8")
    if args.stdout:
        sys.stdout.write(payload + "\n")
    else:
        sys.stdout.write(
            f"dispatch sweep: {report['total']} commands, "
            f"{len(report['crashed'])} crashed, {len(report.get('hung', []))} hung "
            f"(report: {report_path})\n"
        )
        for entry in report["crashed"][:40]:
            sys.stdout.write(f"  {entry['name']}: {entry['error'][:160]}\n")
        for name in report.get("hung", [])[:20]:
            sys.stdout.write(f"  hung: {name}\n")
    return 1 if report["crashed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
