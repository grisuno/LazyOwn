"""Auto-verb registry: loop-ready automation commands."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.auto_registry import (  # noqa: E402
    AUTO_VERBS,
    build_command,
    execute_shell_verb,
    is_shell_verb,
    missing_binary,
    propose_intents,
    steps_for,
    verb_available,
    verb_gap,
    verbs,
    verbs_for,
)


def test_registry_covers_auto_family() -> None:
    """Every auto_* shell verb is registered exactly once with metadata."""
    names = verbs()
    assert {"auto_pwn", "autopivot", "automsf", "autoblody",
            "auto_populate", "pyautomate"} <= set(names)
    assert len(names) == len(set(names))
    for entry in AUTO_VERBS:
        assert entry.verb and entry.phases and entry.keywords and entry.description


def test_build_command_binds_target() -> None:
    """Target binds for target verbs; populate needs none."""
    assert build_command("auto_pwn", "10.0.0.5") == "auto_pwn 10.0.0.5"
    assert build_command("auto_populate") == "auto_populate"
    assert build_command("autopivot", "10.0.0.5") == "autopivot 10.0.0.5"
    with pytest.raises(KeyError):
        build_command("nope", "10.0.0.5")


def test_is_shell_verb_matches_first_token() -> None:
    """Routing keys on the verb, never on trailing args."""
    assert is_shell_verb("auto_pwn 10.0.0.5")
    assert is_shell_verb("pyautomate")
    assert not is_shell_verb("nmap -sV 10.0.0.5")
    assert not is_shell_verb("")


def test_verbs_for_matches_keywords() -> None:
    """Goal/finding text selects the right automation."""
    assert [v.verb for v in verbs_for("gain initial access exploit")] == ["auto_pwn"]
    assert "autoblody" in [v.verb for v in verbs_for("AD kerberos privesc path")]
    assert "autopivot" in [v.verb for v in verbs_for("pivot to internal network")]
    assert verbs_for("just a port scan please") == []


def test_propose_and_translate_roundtrip() -> None:
    """Proposed intents translate back into runnable shell lines."""
    intents = propose_intents("gain initial access on 10.0.0.5", "10.0.0.5")
    assert intents and all(i.startswith("auto ") for i in intents)
    assert steps_for(intents[0], "") == [build_command("auto_pwn", "10.0.0.5")]
    assert steps_for("auto autoblody 10.0.0.5", "") == ["autoblody 10.0.0.5"]
    assert steps_for("auto nope 10.0.0.5", "") is None
    assert steps_for("nmap -sV 10.0.0.5", "10.0.0.5") is None


class _FakeShell:
    """Minimal shell double capturing onecmd input."""

    def __init__(self, output: str = "done") -> None:
        self.seen: list[str] = []
        self.output = output

    def onecmd_plus_hooks(self, command: str) -> None:
        """Record the command and echo canned output."""
        self.seen.append(command)
        print(self.output)


class _HangingShell:
    """Shell double that never returns."""

    def onecmd(self, command: str) -> None:
        """Block forever to exercise the executor timeout."""
        import threading

        threading.Event().wait()


def test_execute_shell_verb_captures_output() -> None:
    """Loop executor runs the verb and returns its transcript."""
    shell = _FakeShell("pwned")
    out = execute_shell_verb(shell, "auto_pwn 10.0.0.5", timeout_sec=5.0)
    assert "pwned" in out
    assert shell.seen == ["auto_pwn 10.0.0.5"]


def test_execute_shell_verb_rejects_non_verbs() -> None:
    """Bash stays on bash: non-verbs never reach the shell."""
    shell = _FakeShell()
    out = execute_shell_verb(shell, "nmap -sV 10.0.0.5", timeout_sec=5.0)
    assert out.startswith("execution failed")
    assert shell.seen == []


def test_execute_shell_verb_timeout_never_hangs() -> None:
    """A hanging automation reports TIMEOUT instead of wedging the loop."""
    out = execute_shell_verb(_HangingShell(), "auto_pwn 10.0.0.5", timeout_sec=0.2)
    assert "TIMEOUT" in out


def test_execute_shell_verb_without_shell() -> None:
    """Missing shell context degrades to a transcript, not an exception."""
    out = execute_shell_verb(None, "auto_pwn 10.0.0.5", timeout_sec=1.0)
    assert out.startswith("execution failed")


def test_verb_gap_flags_missing_tooling(monkeypatch) -> None:
    """Unavailable verbs report the gap; unconstrained verbs stay ready."""
    monkeypatch.setattr("modules.auto_registry.shutil.which", lambda name: None)
    assert verb_gap("automsf") == "missing tool(s): msfconsole"
    assert verb_gap("autopivot").startswith("no pivot tool installed")
    assert verb_available("autopivot") is False
    assert verb_available("auto_pwn") is True
    assert verb_available("exfil_auto") is True


def test_missing_binary_skips_builtins_paths_and_scripts(monkeypatch) -> None:
    """Only real standalone tools are checked against PATH."""
    monkeypatch.setattr("modules.auto_registry.shutil.which", lambda name: None)
    assert missing_binary("echo hello") == ""
    assert missing_binary("./setup.sh") == ""
    assert missing_binary("/opt/tool/run") == ""
    assert missing_binary("python3 -c 'print(1)'") == ""
    assert missing_binary("nmap -sV 10.0.0.5") == "nmap"


def test_propose_and_steps_skip_unavailable_verbs(monkeypatch) -> None:
    """The planner never dispatches work this host cannot execute."""
    monkeypatch.setattr("modules.auto_registry.shutil.which", lambda name: None)
    intents = propose_intents("gain initial access on 10.0.0.5", "10.0.0.5")
    assert intents == ["auto auto_pwn 10.0.0.5"]
    assert steps_for("auto autopivot 10.0.0.5", "") is None
    assert steps_for("pivot tunnel internal network", "10.0.0.5") is None
    assert steps_for("metasploit listener", "10.0.0.5") is None


def test_steps_for_uses_next_available_keyword_verb(monkeypatch) -> None:
    """Keyword matching falls through to the next verb when one is missing."""
    monkeypatch.setattr("modules.auto_registry.shutil.which", lambda name: None)
    assert steps_for("exploit with msf", "10.0.0.5") == ["auto_pwn 10.0.0.5"]


def test_cancel_running_commands_kills_streaming() -> None:
    """BDD: operator cancellation kills registered streaming processes."""
    import threading
    import time

    from modules.auto_registry import cancel_running_commands, execute_streaming

    result: dict = {}

    def _run() -> None:
        result["out"] = execute_streaming("sleep 30", timeout_sec=60)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    time.sleep(0.4)
    assert cancel_running_commands() >= 1
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert result.get("out") == ""
