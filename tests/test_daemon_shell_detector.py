"""Contract: the daemon shell detector agrees with the canonical detector.

The EngageOrchestrator decides ``SHELL_OBTAINED`` through
``_ShellDetector.detect_in_output``. For loop-to-loop and loop-to-daemon
consistency on Metasploitable path coverage, that decision MUST use the one
shared, precise detector (``atomic_exploit_bridge.shell_output_evidence``) that
the engine, ``auto_pwn`` and every gym already consume -- not a divergent
substring list that fabricates shells on benign ``uid=`` or ``root@`` banners.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))

import autonomous_daemon as daemon  # noqa: E402

from modules import atomic_exploit_bridge as aeb  # noqa: E402


class _Narrator:
    """Minimal narrator capturing narrate() calls."""

    def __init__(self) -> None:
        self.events: list[dict] = []

    def narrate(self, **kwargs: object) -> None:
        self.events.append(dict(kwargs))


def _detector() -> daemon._ShellDetector:
    return daemon._ShellDetector(_Narrator())


REAL_SHELL_OUTPUTS = (
    "uid=0(root) gid=0(root) groups=0(root)",
    "root@metasploitable:~# whoami\nroot",
    "meterpreter > getuid",
    "command shell session 1 opened (10.0.0.1:4444 -> 10.0.0.2:55111)",
    "sh-3.2# id",
    "NT AUTHORITY\\SYSTEM",
)

BENIGN_OUTPUTS = (
    "Contact: webmaster uid=www-data in logs",
    "From: root@localhost (Cron Daemon) subject nightly",
    "# whoami    (comment line in a config example)",
    "HTTP/1.1 200 OK\nServer: Apache/2.2.8 (Ubuntu)\n<html>home page</html>",
    "",
)


def test_real_shell_signals_detected():
    det = _detector()
    for out in REAL_SHELL_OUTPUTS:
        assert det.detect_in_output(out, target="10.0.0.2") is True, out


def test_benign_output_is_not_a_shell():
    det = _detector()
    for out in BENIGN_OUTPUTS:
        assert det.detect_in_output(out, target="10.0.0.2") is False, out


def test_matches_canonical_detector_exactly():
    det = _detector()
    for out in REAL_SHELL_OUTPUTS + BENIGN_OUTPUTS:
        assert det.detect_in_output(out, target="x") == aeb.shell_output_evidence(out), out


def test_narrates_on_positive_only():
    narrator = _Narrator()
    det = daemon._ShellDetector(narrator)
    det.detect_in_output("uid=0(root) gid=0(root)", target="10.0.0.2")
    assert any(e.get("kind") == "SHELL_OBTAINED" for e in narrator.events)
    narrator.events.clear()
    det.detect_in_output("just a banner root@localhost", target="10.0.0.2")
    assert not narrator.events
