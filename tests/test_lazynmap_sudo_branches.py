"""LazyNmap sudo branches: unattended abort vs interactive prompt.

Regression pin for the live incident where an interactive ``nmap`` run
aborted because the script could not see a terminal (the CLI captures
output through pipes, so ``[ -t 1 ]`` is false). The branch must instead
key on ``LAZYOWN_AUTONOMOUS=1``, which only the loop sets.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "modules" / "lazynmap.sh"


def _fake_bin(tmp_path: Path) -> Path:
    """Build a PATH dir with a failing sudo and a silent gum."""
    fake = tmp_path / "bin"
    fake.mkdir(exist_ok=True)
    sudo = fake / "sudo"
    sudo.write_text("#!/bin/sh\nexit 1\n")
    sudo.chmod(0o755)
    gum = fake / "gum"
    gum.write_text("#!/bin/sh\nexit 0\n")
    gum.chmod(0o755)
    return fake


def _run_script(tmp_path: Path, extra_env: dict[str, str]) -> subprocess.CompletedProcess:
    fake = _fake_bin(tmp_path)
    env = {
        **os.environ,
        "PATH": f"{fake}:{os.environ.get('PATH', '')}",
        **extra_env,
    }
    return subprocess.run(
        ["bash", str(_SCRIPT), "-t", "127.0.0.1"],
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )


def test_autonomous_mode_aborts_without_passwordless_sudo(tmp_path):
    """Unattended runs refuse to prompt: exit 3 with a clear message."""
    proc = _run_script(tmp_path, {"LAZYOWN_AUTONOMOUS": "1"})
    assert proc.returncode == 3
    assert "unattended loop" in proc.stdout + proc.stderr


def test_interactive_mode_keeps_the_sudo_prompt_path(tmp_path):
    """Without the autonomous flag the script tries the password flow."""
    proc = _run_script(tmp_path, {"LAZYOWN_AUTONOMOUS": "0"})
    assert proc.returncode == 1
    assert "unattended loop" not in proc.stdout + proc.stderr
