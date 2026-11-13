"""Tests for the gym blueprint: auth gate, validation and route surface."""

from __future__ import annotations

import pytest
from flask import Flask
from flask_login import LoginManager

from lazyc2.blueprints.gym import GYM_NODE_PREFIX, _scenario_from_payload, gym_bp


@pytest.fixture()
def gym_app():
    app = Flask(__name__)
    app.secret_key = "test"
    manager = LoginManager(app)
    manager.user_loader(lambda _user_id: None)
    manager.login_view = "login"

    @app.route("/login")
    def login():
        return "login", 200

    app.register_blueprint(gym_bp)
    app.config["TESTING"] = True
    return app


def test_gym_node_prefix_is_namespaced():
    assert GYM_NODE_PREFIX == "gym-"


def test_scenario_payload_validation_rejects_bad_input():
    assert _scenario_from_payload(None) == ""
    assert _scenario_from_payload("metasploitable") == ""
    assert _scenario_from_payload({"scenario": ""}) == ""
    assert _scenario_from_payload({"scenario": "../etc"}) == ""
    assert _scenario_from_payload({"scenario": "metasploitable; rm"}) == ""
    assert _scenario_from_payload({"scenario": "metasploitable"}) == "metasploitable"
    assert _scenario_from_payload({"scenario": "AD-Lab"}) == "ad-lab"


def test_scenarios_requires_operator_session(gym_app):
    client = gym_app.test_client()
    response = client.get("/api/gym/scenarios")
    assert response.status_code in (301, 302)


def test_start_rejects_unknown_scenario_unauthenticated(gym_app):
    client = gym_app.test_client()
    response = client.post("/api/gym/start", json={"scenario": "nope"})
    assert response.status_code in (301, 302, 400)


def test_stop_all_is_routed(gym_app):
    client = gym_app.test_client()
    response = client.post("/api/gym/stop", json={"all": True})
    assert response.status_code in (301, 302)
