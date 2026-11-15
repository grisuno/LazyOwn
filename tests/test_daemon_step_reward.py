"""Contract: the daemon step reward grants the shell tier via the canonical detector.

The daemon's RL reward used its own loose keyword list (``"uid=0"``,
``"root shell"``) to decide a shell, diverging from the one precise detector the
engine and every gym use. A landed session is the strongest signal, so the
reward must reach the shell tier exactly when
``atomic_exploit_bridge.shell_output_evidence`` says a shell is present -- and
not on a benign ``root@`` banner.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))

import autonomous_daemon as daemon  # noqa: E402

SHELL_TIER = 9.0


def _reward(output: str, phase: str = "exploit") -> float:
    return daemon._compute_step_reward(output, "run exploit", phase, True, [], [])


def test_real_shell_reaches_shell_tier():
    reward = _reward("uid=0(root) gid=0(root) groups=0(root)")
    assert reward >= SHELL_TIER


def test_msf_session_banner_reaches_shell_tier():
    reward = _reward("command shell session 1 opened (10.0.0.1 -> 10.0.0.2)")
    assert reward >= SHELL_TIER


def test_benign_banner_below_shell_tier():
    reward = _reward("From: root@localhost (Cron Daemon)\nSubject: nightly")
    assert reward < SHELL_TIER


def test_failed_step_is_penalized():
    assert daemon._compute_step_reward("whatever", "cmd", "exploit", False, [], []) == -2.0
