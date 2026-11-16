"""Subprocess entry point that runs one lazymode Python script.

Invoked by :func:`sdk.lazymode.runner.run_python` as a separate process so
a runaway or crashing script cannot take down the caller. It builds a
:class:`sdk.facade.Lazy` bound to the operator payload, enforces the
operator scope posture, executes the user script with ``lazy`` in scope,
and emits a single JSON envelope after a unique sentinel so the parent can
recover the result even when a grandchild process writes to the inherited
stdout.

The script is operator-authored (or operator-approved) code that is meant
to drive the framework, not untrusted third-party input; the subprocess
boundary here is for isolation and resource bounding, not containment.
"""

from __future__ import annotations

import io
import json
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout
from typing import Any

ENVELOPE_SENTINEL = "__LAZYMODE_ENVELOPE__"
_RESULT_VARIABLE = "result"
_MAX_STDOUT_CHARS = 8000


def _bounded(text: str) -> str:
    """Return *text* capped so a chatty tool cannot flood the context.

    The script's ``result`` is the intended payload; captured stdout is a
    debugging tail, so only its head is kept with a truncation marker. This
    is what keeps code mode's context saving intact when a called command
    streams megabytes of output.

    Args:
        text: The captured stdout.

    Returns:
        The stdout unchanged when short, else its head plus a marker.
    """
    if len(text) <= _MAX_STDOUT_CHARS:
        return text
    dropped = len(text) - _MAX_STDOUT_CHARS
    return f"{text[:_MAX_STDOUT_CHARS]}\n... [{dropped} chars truncated]"


def _jsonable(value: Any) -> Any:
    """Return a JSON-serializable view of *value*.

    Args:
        value: The script's result object.

    Returns:
        The value unchanged when it already serializes, else its repr.
    """
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return repr(value)


def _emit(envelope: dict[str, Any]) -> None:
    """Write the result envelope to the real stdout after the sentinel.

    Args:
        envelope: The result mapping to serialize.
    """
    sys.__stdout__.write(f"\n{ENVELOPE_SENTINEL}\n")
    sys.__stdout__.write(json.dumps(envelope))
    sys.__stdout__.flush()


def main(argv: list[str]) -> int:
    """Run the lazymode script named in *argv* and emit its envelope.

    Args:
        argv: ``[script_path, payload_path, sessions_dir]``.

    Returns:
        Process exit code: 0 on success, 1 on script error.
    """
    script_path, payload_path, sessions_dir = argv[0], argv[1], argv[2]
    from core.config import load_payload
    from sdk.facade import Lazy
    from sdk.lazymode.runner import build_scope_check

    with open(script_path, encoding="utf-8") as handle:
        source = handle.read()

    payload = load_payload(payload_path)
    lazy = Lazy(
        payload_path=payload_path,
        sessions_dir=sessions_dir,
        scope_check=build_scope_check(payload),
    )
    namespace: dict[str, Any] = {"lazy": lazy, "__name__": "__lazymode__"}
    captured = io.StringIO()
    try:
        with redirect_stdout(captured), redirect_stderr(captured):
            exec(compile(source, "<lazymode>", "exec"), namespace)  # noqa: S102
        _emit(
            {
                "ok": True,
                "stdout": _bounded(captured.getvalue()),
                "result": _jsonable(namespace.get(_RESULT_VARIABLE)),
                "error": "",
            }
        )
        return 0
    except BaseException:
        _emit(
            {
                "ok": False,
                "stdout": _bounded(captured.getvalue()),
                "result": None,
                "error": traceback.format_exc(),
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
