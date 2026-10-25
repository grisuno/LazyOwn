"""Gym lifecycle: lab spin-up on start, teardown on stop and exit cleanup."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules import gym_registry, lab_runtime, redteam_gym  # noqa: E402


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Isolate world-model state, gym files and leaderboard."""
    import modules.outcome_bus as outcome_bus
    import modules.world_model as world_model

    shutil.copytree(gym_registry.GYMS_DIR, tmp_path / "gyms")
    monkeypatch.setattr(world_model, "_DEFAULT_PATH", tmp_path / "world_model.json")
    monkeypatch.setattr(world_model, "_default_wm", None)
    monkeypatch.setattr(gym_registry, "GYMS_DIR", tmp_path / "gyms")
    monkeypatch.setattr(gym_registry, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(redteam_gym, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(redteam_gym, "GYM_LEADERBOARD", tmp_path / "sessions" / "gym" / "leaderboard.json")
    monkeypatch.setattr(redteam_gym, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(outcome_bus, "record_event", lambda **kwargs: {})
    yield tmp_path
    monkeypatch.setattr(world_model, "_default_wm", None)


class _FakeDocker:
    """Scriptable docker argv recorder for lifecycle tests."""

    def __init__(self, responses: dict[tuple, object] | None = None) -> None:
        self.calls: list[list[str]] = []
        self.responses = responses or {}

    def __call__(self, *argv, **kwargs):
        self.calls.append([str(part) for part in argv])
        key = tuple(argv)
        if key in self.responses:
            return self.responses[key]
        return _result(0, "container-id-1234\n")


class _result:
    def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_start_spins_scenario_and_resolves_ip(sandbox, monkeypatch) -> None:
    """gym start auto-spins the scenario container and reports the IP."""
    docker = _FakeDocker()
    monkeypatch.setattr(lab_runtime, "_docker", docker)
    monkeypatch.setattr(lab_runtime, "docker_available", lambda: True)
    monkeypatch.setattr(lab_runtime, "running_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "existing_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "container_ip", lambda name: "172.17.0.2")
    monkeypatch.setattr(lab_runtime, "ensure_web", lambda *a, **k: None)
    monkeypatch.setattr(lab_runtime, "apply_gym_migrations", lambda name: {})
    print("DEBUG docker_avail:", lab_runtime.docker_available())
    import traceback
    try:
        from modules import lab_runtime as lr2
        print("DEBUG direct start:", lr2.start("metasploitable"))
    except Exception:
        traceback.print_exc()
    result = redteam_gym.start_challenge("metasploitable_full_chain")
    assert result["success"] is True
    lab = result.get("lab") or {}
    assert lab.get("success") is True
    assert lab.get("ip") == "172.17.0.2"
    assert result["next_steps"][0] == "assign rhost 172.17.0.2"
    run_cmd = [call for call in docker.calls if call[:2] == ["run", "-d"]]
    assert run_cmd, docker.calls
    assert "-i" in run_cmd[0]
    assert "docker" not in run_cmd[0]


def test_start_without_lab_flag_still_registers(sandbox, monkeypatch) -> None:
    """spin_lab=False keeps the old behaviour (no Docker touched)."""
    docker = _FakeDocker()
    monkeypatch.setattr(lab_runtime, "_docker", docker)
    result = redteam_gym.start_challenge("metasploitable_full_chain", spin_lab=False)
    assert result["success"] is True
    assert "lab" not in result
    assert docker.calls == []


def test_start_without_docker_degrades_gracefully(sandbox, monkeypatch) -> None:
    """No Docker never fails the run registration."""
    monkeypatch.setattr(lab_runtime, "docker_available", lambda: False)
    result = redteam_gym.start_challenge("metasploitable_full_chain")
    assert result["success"] is True
    assert "lab" not in result


def test_start_removes_stale_container_first(sandbox, monkeypatch) -> None:
    """A stopped container with the same name is removed before run."""
    docker = _FakeDocker()
    monkeypatch.setattr(lab_runtime, "_docker", docker)
    monkeypatch.setattr(lab_runtime, "docker_available", lambda: True)
    monkeypatch.setattr(lab_runtime, "running_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "existing_containers", lambda: ["lazyown-lab-metasploitable"])
    monkeypatch.setattr(lab_runtime, "container_ip", lambda name: "172.17.0.2")
    monkeypatch.setattr(lab_runtime, "ensure_web", lambda *a, **k: None)
    monkeypatch.setattr(lab_runtime, "apply_gym_migrations", lambda name: {})
    redteam_gym.start_challenge("metasploitable_full_chain")
    remove = [call for call in docker.calls if call[:2] == ["rm", "-f"]]
    assert remove == [["rm", "-f", "lazyown-lab-metasploitable"]]


def test_stop_teardowns_scenario_container(sandbox, monkeypatch) -> None:
    """gym stop stops the scenario container when no run remains."""
    docker = _FakeDocker()
    monkeypatch.setattr(lab_runtime, "_docker", docker)
    monkeypatch.setattr(lab_runtime, "docker_available", lambda: True)
    monkeypatch.setattr(lab_runtime, "running_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "existing_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "container_ip", lambda name: "172.17.0.2")
    monkeypatch.setattr(lab_runtime, "ensure_web", lambda *a, **k: None)
    monkeypatch.setattr(lab_runtime, "apply_gym_migrations", lambda name: {})
    redteam_gym.start_challenge("metasploitable_full_chain")
    monkeypatch.setattr(lab_runtime, "running_containers", lambda: ["lazyown-lab-metasploitable"])
    result = redteam_gym.stop_challenges()
    assert result.get("count") == 1
    labs = result.get("labs") or {}
    assert labs.get("metasploitable", {}).get("success") is True
    stop = [call for call in docker.calls if call[:1] == ["stop"]]
    assert ["stop", "lazyown-lab-metasploitable"] in stop


def test_stop_keeps_scenario_with_active_runs(sandbox, monkeypatch) -> None:
    """A scenario shared by a still-active run is not torn down."""
    docker = _FakeDocker()
    monkeypatch.setattr(lab_runtime, "_docker", docker)
    monkeypatch.setattr(lab_runtime, "docker_available", lambda: True)
    monkeypatch.setattr(lab_runtime, "running_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "existing_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "container_ip", lambda name: "172.17.0.2")
    monkeypatch.setattr(lab_runtime, "ensure_web", lambda *a, **k: None)
    monkeypatch.setattr(lab_runtime, "apply_gym_migrations", lambda name: {})
    redteam_gym.start_challenge("metasploitable_full_chain")
    redteam_gym.start_challenge("first_blood_smb")
    monkeypatch.setattr(lab_runtime, "running_containers", lambda: ["lazyown-lab-metasploitable"])
    result = redteam_gym.stop_challenges("gym0001")
    labs = result.get("labs") or {}
    assert labs == {}
    stop = [call for call in docker.calls if call[:1] == ["stop"]]
    assert stop == []


def test_cleanup_gym_machines_stops_all(tmp_path, monkeypatch, capsys) -> None:
    """Exit cleanup stops labs and ranges; payload flag disables it."""
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps({"rhost": "1.1.1.1"}), encoding="utf-8")

    import core.config as core_config

    monkeypatch.setattr(
        core_config,
        "load_payload",
        lambda *args, **kwargs: json.loads(payload.read_text(encoding="utf-8")),
    )

    import modules.gym_cleanup as gym_cleanup

    calls: list[list[str]] = []
    monkeypatch.setattr(lab_runtime, "_docker", lambda *argv, **k: (calls.append([str(part) for part in argv]), _result(0, "x\n"))[1])
    monkeypatch.setattr(lab_runtime, "running_containers", lambda: ["lazyown-lab-metasploitable"])
    monkeypatch.setattr(lab_runtime, "running_range_containers", lambda: ["lazyown-range-dc"])
    monkeypatch.setattr(lab_runtime, "range_compose", lambda profile: None)
    result = gym_cleanup.cleanup_gym_machines(verbose=True)
    assert result["enabled"] is True
    assert result["labs"]["stopped"] == ["lazyown-lab-metasploitable"]
    assert result["ranges"]["stopped"] == ["lazyown-range-dc"]
    output = capsys.readouterr().out
    assert "stopped 2 machine(s)" in output

    monkeypatch.setattr(lab_runtime, "running_containers", lambda: [])
    monkeypatch.setattr(lab_runtime, "running_range_containers", lambda: [])
    payload.write_text(json.dumps({"rhost": "1.1.1.1", "gym_cleanup_on_exit": False}), encoding="utf-8")
    result = gym_cleanup.cleanup_gym_machines(verbose=True)
    assert result["enabled"] is False
    assert "disabled" in capsys.readouterr().out
