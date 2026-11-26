"""Boot smoke gate: the real shell must start and dispatch commands.

In-process unit tests construct the shell with mocks and never drive
``LazyOwnShell.cmd`` (the central execution path). A name-binding
regression in ``lazyown.py`` (e.g. ``datetime`` bound as the module
instead of the class) crashed every command routed through ``cmd()``
while the whole test suite stayed green. This suite boots the real app
per command and asserts clean dispatch, so "the app does not even
start" can never ship again.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN = REPO_ROOT / "lazyown.py"

SAFE_COMMANDS: tuple[tuple[str, str], ...] = (
    ("display", "help"),
    ("display", "version"),
    ("display", "whoami"),
    ("display", "banner"),
    ("display", "sessions"),
    ("display", "payload"),
    ("display", "config"),
    ("display", "status"),
    ("display", "arsenal_show"),
    ("display", "bof_list"),
    ("display", "facts_show"),
    ("display", "chain list"),
    ("executor", "echo smoke_boot_probe"),
    ("credentials", "createcredentials smokeboot:probe123"),
)

_TRACEBACK_MARKS = ("AttributeError", "NameError", "TypeError", "KeyError", "Traceback (most recent call last)")


def _run_headless(command: str) -> dict:
    env = dict(os.environ)
    env["LAZYOWN_AUTO_CRYPTO"] = "0"
    result = subprocess.run(
        [sys.executable, str(LAZYOWN), "--headless", "--json-output", "-c", command],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=240,
        env=env,
    )
    for line in reversed(result.stdout.splitlines()):
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                break
    return {"success": False, "error": (result.stdout + result.stderr)[-500:], "exit_code": result.returncode}


@pytest.mark.parametrize("kind,command", SAFE_COMMANDS, ids=[c for _, c in SAFE_COMMANDS])
def test_headless_dispatch(kind: str, command: str) -> None:
    """A real boot must dispatch the command without a crash."""
    payload = _run_headless(command)
    assert payload.get("success") is True, f"[{command}] {payload.get('error')}"
    for mark in _TRACEBACK_MARKS:
        text = json.dumps(payload)
        assert mark not in text, f"[{command}] {mark} in payload"
