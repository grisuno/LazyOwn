"""Headless atomic_tests: numeric selection and autonomous-safe prompts.

Pins the operator contract: a technique with several atomics can be run
without the interactive chooser by passing the 1-based test number (a
trailing integer or ``--test``/``--index``), and an autonomous loop run
(``LAZYOWN_AUTONOMOUS=1``) never blocks on the chooser even with a tty
attached.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest


def _make_test(guid: str, name: str, command: str):
    """Return one atomic-test stand-in with a distinct command."""
    return SimpleNamespace(
        guid=guid,
        name=name,
        mitre_id="T1105",
        mitre_url="https://attack.mitre.org/techniques/T1105",
        platforms=["linux"],
        input_arguments={},
        prereq_command="",
        get_prereq_command="",
        command=command,
        cleanup_command="",
    )


@pytest.fixture()
def three_tests(monkeypatch):
    """Patch the resolver to return three distinct candidates."""
    import modules.atomic_cli as atomic_cli
    import modules.bof_delivery as bof_delivery

    tests = [
        _make_test("guid-one", "rsync push", "echo one"),
        _make_test("guid-two", "scp push", "echo two"),
        _make_test("guid-three", "sftp push", "echo three"),
    ]
    resolver = SimpleNamespace(
        available=True,
        ensure_repo=lambda: None,
        build_index=lambda: {"T1105": tests},
        resolve=lambda query, platform=None: list(tests),
    )
    monkeypatch.setattr(atomic_cli, "_resolver", lambda: resolver)
    queued: list = []
    monkeypatch.setattr(bof_delivery, "beacon_for_target", lambda target, **kwargs: "linux_beacon")
    monkeypatch.setattr(
        bof_delivery,
        "queue_to_beacon",
        lambda client_id, command, **kwargs: queued.append((client_id, command)) or True,
    )
    monkeypatch.setattr(
        bof_delivery,
        "wait_for_beacon",
        lambda client_id, **kwargs: {"client_id": client_id, "output": "ok"},
    )
    return atomic_cli, queued


def test_parse_accepts_numeric_and_flag_forms():
    """Trailing integer and --test/--index yield the 1-based index."""
    from modules.atomic_cli import parse_atomic_line

    assert parse_atomic_line("T1105 2")["test_index"] == 2
    assert parse_atomic_line("T1105 --test 3")["test_index"] == 3
    assert parse_atomic_line("T1105 --index=4")["test_index"] == 4
    assert parse_atomic_line("T1105 --platform linux 5")["test_index"] == 5
    assert parse_atomic_line("T1105 linux")["test_index"] == 0


def test_numeric_argument_selects_that_test(three_tests):
    """'T1105 2' runs the second listed atomic headless, no prompt."""
    atomic_cli, queued = three_tests
    result = atomic_cli.run_atomic_tests({"rhost": "172.17.0.2"}, "T1105 2", shell=None)
    assert result == 0
    assert queued == [("linux_beacon", "echo two")]


def test_out_of_range_index_is_usage_error(three_tests):
    """An index past the candidate count is a usage error, not a crash."""
    atomic_cli, queued = three_tests
    result = atomic_cli.run_atomic_tests({"rhost": "172.17.0.2"}, "T1105 9", shell=None)
    assert result == 2
    assert queued == []


def test_autonomous_mode_picks_first_without_prompt(three_tests, monkeypatch):
    """With a tty attached, autonomous mode never blocks on the chooser."""
    atomic_cli, queued = three_tests
    monkeypatch.setattr(atomic_cli.sys.stdin, "isatty", lambda: True)
    from core.autonomous import autonomous_mode

    with autonomous_mode():
        result = atomic_cli.run_atomic_tests({"rhost": "172.17.0.2"}, "T1105", shell=None)
    assert result == 0
    assert queued == [("linux_beacon", "echo one")]


def test_tty_without_autonomous_still_prompts(three_tests, monkeypatch):
    """A real interactive session keeps the chooser (no silent first-pick)."""
    atomic_cli, _queued = three_tests
    monkeypatch.setattr(atomic_cli.sys.stdin, "isatty", lambda: True)
    monkeypatch.delenv("LAZYOWN_AUTONOMOUS", raising=False)
    prompted: list = []

    def _fake_input(prompt=""):
        prompted.append(prompt)
        return "2"

    monkeypatch.setattr("builtins.input", _fake_input)
    result = atomic_cli.run_atomic_tests({"rhost": "172.17.0.2"}, "T1105", shell=None)
    assert result == 0
    assert prompted and "number of the test" in prompted[0]
