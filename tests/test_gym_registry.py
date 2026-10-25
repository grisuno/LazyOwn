"""Gym YAML catalogue and persistent world-model run state."""

from __future__ import annotations

import json

import pytest

from modules import gym_registry
from modules.world_model import read_state_dict


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Isolate world-model state, gym files and leaderboard."""
    import shutil

    import modules.outcome_bus as outcome_bus
    import modules.redteam_gym as gym
    import modules.world_model as world_model

    shutil.copytree(gym_registry.GYMS_DIR, tmp_path / "gyms")
    monkeypatch.setattr(world_model, "_DEFAULT_PATH", tmp_path / "world_model.json")
    monkeypatch.setattr(world_model, "_default_wm", None)
    monkeypatch.setattr(gym_registry, "GYMS_DIR", tmp_path / "gyms")
    monkeypatch.setattr(gym_registry, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(gym, "GYM_DIR", tmp_path / "sessions" / "gym")
    monkeypatch.setattr(gym, "GYM_LEADERBOARD", tmp_path / "sessions" / "gym" / "leaderboard.json")
    monkeypatch.setattr(gym, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(outcome_bus, "record_event", lambda **kwargs: {})
    yield tmp_path
    monkeypatch.setattr(world_model, "_default_wm", None)


def _write_definition(directory, gym_id, **overrides):
    data = {
        "id": gym_id,
        "name": overrides.get("name", gym_id),
        "description": "demo",
        "scenario": "metasploitable",
        "chain": "",
        "objective": "root the target",
        "difficulty": overrides.get("difficulty", "easy"),
        "phases": ["enum", "exploit"],
        "required_techniques": [],
        "bonus_techniques": [],
        "max_points": 1000,
        "speed_bonus_max": 300,
        "stealth_bonus_max": 200,
        "technique_diversity_bonus": 200,
        "hints": ["try harder"],
        "success_check": "root",
        "elo_bonus": 100,
    }
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{gym_id}.yaml"
    import yaml

    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_shipped_catalogue_loads():
    """The repository ships a valid YAML gym catalogue."""
    definitions = gym_registry.load_definitions()
    assert {"first_blood_web", "first_implant", "vault_exfil"} <= set(definitions)
    assert definitions["first_blood_web"]["difficulty"] == "easy"
    assert definitions["first_implant"]["scenario"] == "ad-mini"


def test_definition_crud_is_confined(sandbox, tmp_path):
    """Create, update, delete and path confinement behave."""
    from modules import redteam_gym as gym

    directory = tmp_path / "gyms"
    path = gym_registry.create_definition("demo_gym", name="Demo", directory=directory)
    assert path.name == "demo_gym.yaml"
    assert gym_registry.definition_path("../../escape", directory).parent == directory.resolve()

    loaded = gym_registry.load_definitions(directory)
    assert loaded["demo_gym"]["name"] == "Demo"
    text = path.read_text(encoding="utf-8").replace("Demo", "Renamed")
    gym_registry.update_definition_yaml("demo_gym", text, directory=directory)
    assert gym_registry.load_definitions(directory)["demo_gym"]["name"] == "Renamed"
    assert gym_registry.delete_definition("demo_gym", directory=directory)["success"] is True
    assert not path.exists()

    assert gym.create_gym("demo_gym", name="Demo")["success"] is True
    assert gym.save_gym_yaml("demo_gym", text)["success"] is True
    assert gym.delete_gym("demo_gym")["success"] is True


def test_start_status_stop_all_persists(sandbox):
    """Runs survive reads and are stored in the world model."""
    from modules import redteam_gym as gym

    first = gym.start_challenge("first_blood_web", target="172.17.0.2")
    assert first["success"] is True
    assert first["run_id"].startswith("gym")
    second_attempt = gym.start_challenge("first_blood_web", target="172.17.0.2")
    assert second_attempt["already_active"] is True
    assert second_attempt["run_id"] == first["run_id"]
    assert len(gym.get_active_challenges()) == 1

    run = gym.get_active_challenge(first["run_id"])
    assert run and run["challenge_id"] == "first_blood_web" and run["target"] == "172.17.0.2"

    state = read_state_dict(sandbox / "world_model.json")
    assert state["gyms"]["active"][first["run_id"]]["challenge_id"] == "first_blood_web"

    stopped = gym.stop_challenges()
    assert stopped["count"] == 1
    assert gym.get_active_challenges() == []


def test_stop_by_id_and_name(sandbox):
    """Selectors accept run ids, challenge ids and display names."""
    from modules import redteam_gym as gym

    one = gym.start_challenge("first_blood_web")
    two = gym.start_challenge("first_implant")
    assert gym.stop_challenges("first_blood_web")["count"] == 1
    assert [run["run_id"] for run in gym.get_active_challenges()] == [two["run_id"]]
    assert gym.stop_challenges("first_implant")["count"] == 1
    assert gym.get_active_challenges() == []
    assert one["run_id"] != two["run_id"]


def test_submit_requires_disambiguation(sandbox):
    """Two active runs require an explicit run id to submit."""
    from modules import redteam_gym as gym

    one = gym.start_challenge("first_blood_web")
    gym.start_challenge("first_implant")
    ambiguous = gym.submit_challenge(techniques_used=[])
    assert ambiguous["success"] is False and "Multiple active gyms" in ambiguous["error"]

    submitted = gym.submit_challenge(techniques_used=["sqli_manual"], run_id=one["run_id"])
    assert submitted["success"] is True and submitted["completed"] is True
    assert submitted["elo_awarded"] > 0
    assert [run["challenge_id"] for run in gym.get_active_challenges()] == ["first_implant"]
    gym.stop_challenges()


def test_delete_refuses_active_definition(sandbox):
    """A definition with an active run cannot be deleted until it stops."""
    from modules import redteam_gym as gym

    gym.start_challenge("first_blood_web")
    refused = gym.delete_gym("first_blood_web")
    assert refused["success"] is False and "active runs" in refused["error"]
    gym.stop_challenges()
    assert gym.delete_gym("first_blood_web")["success"] is True


def test_legacy_active_files_are_imported_once(sandbox, monkeypatch):
    """Old per-operator active files appear until a write marks them migrated."""
    legacy = sandbox / "sessions" / "gym"
    legacy.mkdir(parents=True, exist_ok=True)
    (legacy / "active_old.json").write_text(
        json.dumps({"challenge_id": "first_blood_web", "username": "old", "started_at": 1.0}),
        encoding="utf-8",
    )
    monkeypatch.setattr(gym_registry, "GYM_DIR", legacy)
    runs = gym_registry.get_active_runs()
    assert len(runs) == 1 and runs[0]["operator"] == "old"
    assert gym_registry.stop_runs("first_blood_web")["count"] == 1
    assert gym_registry.get_active_runs() == []
