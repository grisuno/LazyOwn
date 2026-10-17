"""Gym CLI lifecycle: start, status, stop by selector and stop-all."""

from __future__ import annotations

import pytest

from cli.commands.redteam_gym import RedTeamGymCommandSet


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Isolate world-model state, gym files and leaderboard."""
    import modules.gym_registry as registry
    import modules.outcome_bus as outcome_bus
    import modules.redteam_gym as gym
    import modules.world_model as world_model

    monkeypatch.setattr(world_model, "_DEFAULT_PATH", tmp_path / "world_model.json")
    monkeypatch.setattr(world_model, "_default_wm", None)
    import shutil

    shutil.copytree(registry.GYMS_DIR, tmp_path / "gyms")
    monkeypatch.setattr(registry, "GYMS_DIR", tmp_path / "gyms")
    monkeypatch.setattr(registry, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(gym, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(gym, "GYM_LEADERBOARD", tmp_path / "sessions" / "gym" / "leaderboard.json")
    monkeypatch.setattr(gym, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(outcome_bus, "record_event", lambda **kwargs: {})
    yield gym


def test_gym_stop_without_active_is_clean(sandbox, capsys):
    """gym stop with no argument reports no active gyms instead of failing."""
    RedTeamGymCommandSet().do_gym("stop")
    output = capsys.readouterr().out
    assert "No active gyms" in output


def test_gym_start_status_stop_lifecycle(sandbox, capsys):
    """A started gym is visible by id and can be stopped by id."""
    command = RedTeamGymCommandSet()
    command.do_gym("start first_blood_web --target 172.17.0.2")
    started = capsys.readouterr().out
    assert "Challenge started" in started
    assert "run gym" in started

    command.do_gym("status")
    listed = capsys.readouterr().out
    assert "Active gyms: 1" in listed
    assert "first_blood_web" in listed

    command.do_gym("status gym0001")
    detail = capsys.readouterr().out
    assert "Run ID:     gym0001" in detail
    assert "172.17.0.2" in detail

    command.do_gym("stop gym0001")
    stopped = capsys.readouterr().out
    assert "Stopped 1 gym(s)" in stopped

    command.do_gym("status")
    assert "No active gyms" in capsys.readouterr().out


def test_gym_stop_all_and_by_name(sandbox, capsys):
    """No argument stops every run; a display name stops only that gym."""
    command = RedTeamGymCommandSet()
    command.do_gym("start first_blood_web")
    command.do_gym("start first_implant")
    capsys.readouterr()

    command.do_gym("stop First Blood - Web")
    assert "Stopped 1 gym(s)" in capsys.readouterr().out
    command.do_gym("status")
    assert "Active gyms: 1" in capsys.readouterr().out

    command.do_gym("stop")
    assert "Stopped 1 gym(s)" in capsys.readouterr().out
    assert sandbox.get_active_challenges() == []


def test_gym_status_explains_live_shell_without_gym(sandbox, monkeypatch, capsys):
    """A live shell is reported as context, not as a gym run."""
    import modules.atomic_exploit_bridge as bridge

    monkeypatch.setitem(bridge._SESSIONS, ("172.17.0.2", "ms2_ingreslock"), object())
    RedTeamGymCommandSet().do_gym("status")
    output = capsys.readouterr().out
    assert "No active gyms" in output
    assert "Live shell sessions (not gym runs)" in output
    assert "does not create a gym run" in output


def test_gym_top_aliases_leaderboard(sandbox, capsys):
    """gym top is accepted as the leaderboard alias."""
    RedTeamGymCommandSet().do_gym("top")
    assert "Leaderboard is empty" in capsys.readouterr().out


def test_gym_status_filters_hosts_by_current_target(sandbox, monkeypatch, capsys):
    """Stale loopback hosts never appear as the current engagement state."""
    from modules import atomic_exploit_bridge as bridge
    from modules.world_model import HostState, get_world_model

    world = get_world_model()
    world.add_host("127.0.0.1")
    world.advance_host("127.0.0.1", HostState.OWNED)
    assert bridge.record_shell_outcome("172.17.0.2", via="ms2_ingreslock") is True
    monkeypatch.setattr("core.config.load_payload", lambda *args, **kwargs: {"rhost": "172.17.0.2"})

    RedTeamGymCommandSet().do_gym("status")
    output = capsys.readouterr().out
    assert "172.17.0.2 (exploited)" in output
    compromised = next(line for line in output.splitlines() if "compromised hosts" in line)
    assert "127.0.0.1" not in compromised
    assert "Ignored unrelated world-model host" in output
    assert "127.0.0.1" in output


def test_atomic_shell_marks_target_compromised(sandbox, monkeypatch, capsys):
    """A live atomic_shell session updates the target host state only."""
    import modules.atomic_exploit_bridge as bridge
    from cli.commands.command_and_control_migrated import CommandAndControlMigratedCommandSet
    from modules.world_model import get_world_model

    monkeypatch.setattr(
        bridge,
        "interactive_shell",
        lambda target, interactive=False: {"live": True, "repl": False, "via": "ms2_ingreslock"},
    )
    CommandAndControlMigratedCommandSet().do_atomic_shell("172.17.0.2 --interactive")
    snapshot = get_world_model().snapshot()
    assert snapshot["hosts"]["172.17.0.2"]["state"] == "exploited"
    assert "atomic_shell" in " ".join(snapshot["hosts"]["172.17.0.2"]["notes"])
    assert "Shell is live" in capsys.readouterr().out
