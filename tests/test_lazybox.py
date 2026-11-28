"""Contract tests for LazyBox (gym + gamification intelligence).

Covers the aggregation contract (catalogue/intel/scoreboard), the
delegate passthroughs and the C2 blueprint routes over the factory app.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest


@pytest.fixture()
def _lazy_patched(tmp_path, monkeypatch):
    """Isolate every LazyBox I/O dependency under tmp_path."""
    import modules.lazy_loop as loop
    import modules.redteam_gym as rg

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(rg, "GYM_DIR", tmp_path / "gym")
    monkeypatch.setattr(rg, "GYM_LEADERBOARD", tmp_path / "gym" / "leaderboard.json")
    monkeypatch.setattr(rg, "GYM_CHALLENGES", tmp_path / "gym" / "challenges.json")
    monkeypatch.setattr("cli.engagement_hooks._load_state", lambda: _FakeState(), raising=False)
    from cli.engagement_hooks import get_karma_name

    _fake = _FakeState()
    monkeypatch.setattr(
        "modules.lazybox._operator_state",
        lambda: {
            "elo": _fake.elo,
            "karma_name": get_karma_name(_fake.elo),
            "badges": list(_fake.badges),
        },
    )
    return tmp_path


class _FakeState:
    def __init__(self) -> None:
        self.elo = 4200
        self.karma_name = "Hacker"
        self.commands_seen = set()
        self.phases_entered = ["recon"]
        self.total_commands = 42
        self.session_commands = 3
        self.session_start_ts = 0.0
        self.elo_session_delta = 15
        self.next_reward_at = 5
        self.badges = ["first_blood"]


class _FakeRegistry:
    last: dict[str, Any] = {}

    @staticmethod
    def get_active_runs(selector="", operator=""):
        _FakeRegistry.last = {"selector": selector, "operator": operator}
        if selector:
            return [
                {"run_id": "r7", "challenge_id": selector, "operator": "op1", "target": "10.0.0.9", "started_at": 1.0}
            ]
        return []


def test_catalogue_shape(_lazy_patched, monkeypatch):
    from modules import lazybox

    monkeypatch.setattr(
        lazybox,
        "_scenario_rows",
        lambda: [
            {
                "scenario": "metasploitable",
                "running": True,
                "description": "d",
                "difficulty": "easy",
                "container": "c",
                "ip": "10.0.0.5",
                "ports": {"ssh": 22},
                "node_id": "gym-metasploitable",
            },
            {
                "scenario": "ad-lab",
                "running": False,
                "description": "d",
                "difficulty": "medium",
                "container": "c2",
                "ip": "",
                "ports": {},
                "node_id": "gym-ad-lab",
            },
        ],
    )
    monkeypatch.setattr(
        lazybox,
        "_challenge_rows",
        lambda: [
            {"id": "first_blood_smb", "name": "First Blood", "active": True, "run_id": "r1", "elapsed": 5.0},
        ],
    )
    cat = lazybox.catalogue()
    assert cat["brand"] == "LazyBox"
    assert cat["totals"] == {
        "scenarios": 2,
        "scenarios_running": 1,
        "challenges": 1,
        "challenges_active": 1,
    }
    assert "scoreboard" in cat


def test_challenge_intel_crosses_engagement(_lazy_patched, monkeypatch):
    from modules import lazybox

    monkeypatch.setattr(
        "modules.redteam_gym.list_challenges",
        lambda: {
            "first_blood_smb": {
                "id": "first_blood_smb",
                "name": "First Blood",
                "difficulty": "easy",
                "phases": ["recon", "exploit"],
                "max_points": 1000,
                "elo_bonus": 150,
            },
        },
    )
    monkeypatch.setattr(
        "modules.redteam_gym.engagement_context",
        lambda target: {
            "phase": "exploit",
            "target": target,
            "hosts": ["10.0.0.9"],
            "host_states": {"10.0.0.9": "owned"},
            "live_shells": [{"target": "10.0.0.9"}],
            "ignored_hosts": [],
        },
    )
    monkeypatch.setattr("modules.gym_registry.get_active_runs", _FakeRegistry.get_active_runs)
    monkeypatch.setattr(
        lazybox, "_killchain_snapshot", lambda: {"current_phase": "exploit", "completed_phases": ["recon"]}
    )
    monkeypatch.setattr(
        "modules.redteam_gym.leaderboard",
        lambda: {
            "op1": {
                "attempts": [
                    {"challenge_id": "first_blood_smb", "success": True, "completed_at": 2.0, "total_points": 900},
                ]
            }
        },
    )

    intel = lazybox.challenge_intel("first_blood_smb")
    assert intel["success"] is True
    assert intel["definition"]["name"] == "First Blood"
    assert intel["run"]["run_id"] == "r7"
    assert intel["engagement"]["host_states"]["10.0.0.9"] == "owned"
    assert intel["killchain"]["current_phase"] == "exploit"
    assert intel["attempts"][0]["operator"] == "op1"

    assert lazybox.challenge_intel("ghost") == {"success": False, "error": "unknown challenge: ghost"}


def test_scoreboard_orders_and_attaches_operator(_lazy_patched):
    from cli.engagement_hooks import get_karma_name
    from modules import redteam_gym
    from modules.lazybox import scoreboard

    redteam_gym._save_leaderboard({"slow": {"total_points": 100}, "fast": {"total_points": 900}})
    board = scoreboard()
    names = [row["operator"] for row in board["leaderboard"]]
    assert names == ["fast", "slow"]
    assert board["operator"]["elo"] == 4200
    assert board["operator"]["karma_name"] == get_karma_name(4200)
    assert "first_blood" in board["operator"]["badges"]


def test_delegates_passthrough(_lazy_patched, monkeypatch):
    from modules import lazybox, redteam_gym

    seen: dict[str, Any] = {}
    monkeypatch.setattr(redteam_gym, "start_challenge", lambda cid, **kw: {"success": True, "id": cid})
    monkeypatch.setattr(redteam_gym, "submit_challenge", lambda **kw: {"success": True})
    monkeypatch.setattr(redteam_gym, "stop_challenges", lambda sel: {"success": True, "selector": sel})

    assert lazybox.start_challenge("first_blood_smb")["id"] == "first_blood_smb"
    assert lazybox.submit_challenge(techniques_used=["T1110"])["success"] is True
    assert lazybox.stop_challenges("r1")["selector"] == "r1"


def test_blueprint_routes_lazybox(_lazy_patched):
    from flask import Flask
    from flask_login import LoginManager

    from lazyc2.blueprints.lazybox import lazybox_bp

    repo_templates = str(Path(__file__).resolve().parent.parent / "templates")
    app = Flask(__name__, template_folder=repo_templates, static_folder=None)
    app.secret_key = "test"
    manager = LoginManager(app)
    manager.user_loader(lambda _user_id: None)
    manager.login_view = "login"

    @app.route("/login")
    def login():
        return "login", 200

    class _TestOperator:
        id = "1"
        username = "tester"
        is_authenticated = True
        is_active = True

        def get_id(self) -> str:
            return self.id

    @app.before_request
    def _auto_login():
        from flask_login import login_user

        login_user(_TestOperator())

    def _tolerant_url_for(endpoint, **values):
        from flask import url_for

        try:
            return url_for(endpoint, **values)
        except Exception:
            return "#"

    app.jinja_env.globals["url_for"] = _tolerant_url_for

    app.register_blueprint(lazybox_bp)
    app.config["TESTING"] = True
    client = app.test_client()
    rules = {str(r) for r in app.url_map.iter_rules()}
    assert "/lazybox" in rules
    assert "/api/lazybox/catalogue" in rules
    assert "/api/lazybox/intel/<challenge_id>" in rules
    assert "/api/lazybox/challenge/start" in rules

    page = client.get("/lazybox")
    assert page.status_code == 200
    assert b"LazyBox" in page.data

    cat = client.get("/api/lazybox/catalogue")
    assert cat.status_code == 200
    assert cat.get_json()["brand"] == "LazyBox"

    missing = client.get("/api/lazybox/intel/nope")
    assert missing.status_code == 404

    start = client.post("/api/lazybox/challenge/start", json={"challenge_id": "first_blood_smb"})
    assert start.status_code in (201, 409)

    stop = client.post("/api/lazybox/challenge/stop", json={"selector": "r1"})
    assert stop.status_code in (200, 409)
