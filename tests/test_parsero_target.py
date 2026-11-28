"""Regression tests for the parsero target-selection bug fix.

Before the fix, ``do_parsero`` computed the explicit target from its
argument but then executed against ``self.params['rhost']``, so
``parsero <other-target>`` always scanned the configured target.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture()
def parsero_shell():
    """Return a command-set bound to a mock shell with a default rhost."""
    import cli.commands.scan as scan_mod
    from cli.commands.scan import ScanMigratedCommandSet

    cmdset = ScanMigratedCommandSet.__new__(ScanMigratedCommandSet)
    shell = MagicMock()
    shell.params = {"rhost": "10.10.10.1"}
    cmdset._resolve_shell = lambda: shell
    with patch.object(scan_mod, "is_binary_present", return_value=True):
        yield scan_mod, cmdset


def test_parsero_uses_explicit_target(parsero_shell):
    scan_mod, cmdset = parsero_shell
    captured = {}

    def fake_run(cmd, check, stdout, stderr):
        captured["cmd"] = cmd

    with patch.object(scan_mod.subprocess, "run", side_effect=fake_run):
        cmdset.do_parsero("10.10.10.99")
    assert captured["cmd"] == ["parsero", "-u", "10.10.10.99", "-sb"]


def test_parsero_falls_back_to_rhost(parsero_shell):
    scan_mod, cmdset = parsero_shell
    captured = {}

    def fake_run(cmd, check, stdout, stderr):
        captured["cmd"] = cmd

    with patch.object(scan_mod.subprocess, "run", side_effect=fake_run):
        cmdset.do_parsero("")
    assert captured["cmd"] == ["parsero", "-u", "10.10.10.1", "-sb"]


def test_parsero_rejects_invalid_target(parsero_shell):
    scan_mod, cmdset = parsero_shell

    with patch.object(scan_mod.subprocess, "run") as run:
        cmdset.do_parsero("bad;host")
    run.assert_not_called()
