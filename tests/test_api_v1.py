"""Integration tests for the versioned C2 REST API (``/api/v1``).

Builds a minimal Flask app with ``api_v1_bp`` registered, an isolated
sessions dir and campaign database, and a tenant API key. Covers health,
targets, results, campaigns, and webhook CRUD plus auth enforcement.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from flask import Flask

from core.api_authz import ApiAuthzConfig, ApiKeyStore, create_api_token
from lazyc2.blueprints.api_v1 import api_v1_bp
from modules.beacon_history import BeaconHistoryConfig, append_record
from modules.db import LazyOwnDB


@pytest.fixture
def api_client(tmp_path: Path):
    """Flask test client with isolated sessions dir, db, and API key."""
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    store = ApiKeyStore(config=ApiAuthzConfig(api_keys_path=str(tmp_path / "api_keys.json")))
    token = create_api_token(store, tenant_id="test-tenant", label="pytest")

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.secret_key = "test-secret"
    app.config["SESSIONS_DIR"] = str(sessions)
    app.config["DB_PATH"] = str(sessions / "c2.db")
    app.config["lazyown_api_key_store"] = store
    app.register_blueprint(api_v1_bp)
    return app.test_client(), token, sessions


def _auth(token: str) -> dict[str, str]:
    return {"X-API-Key": token}


def test_health_is_public(api_client) -> None:
    client, _, _ = api_client
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.get_json()["status"] in {"healthy", "degraded", "unhealthy"}


def test_targets_requires_auth(api_client) -> None:
    client, _, _ = api_client
    assert client.get("/api/v1/targets").status_code == 401


def test_targets_empty_workspace(api_client) -> None:
    client, token, sessions = api_client
    LazyOwnDB(str(sessions / "c2.db"))
    response = client.get("/api/v1/targets", headers=_auth(token))
    assert response.status_code == 200
    assert response.get_json() == {"workspace": "default", "hosts": []}


def test_targets_lists_hosts_with_services(api_client) -> None:
    client, token, sessions = api_client
    db = LazyOwnDB(str(sessions / "c2.db"))
    workspace_id = db.default_workspace("default")
    host_id = db.host_add(workspace_id, address="10.10.11.5", hostname="lame", os="Linux")
    db.service_add(host_id, port=80, proto="tcp", name="http")
    body = client.get("/api/v1/targets", headers=_auth(token)).get_json()
    assert len(body["hosts"]) == 1
    assert body["hosts"][0]["address"] == "10.10.11.5"
    assert body["hosts"][0]["services"][0]["port"] == 80


def test_results_empty(api_client) -> None:
    client, token, _ = api_client
    body = client.get("/api/v1/results", headers=_auth(token)).get_json()
    assert body == {"clients": [], "latest": []}


def test_results_per_client(api_client) -> None:
    client, token, sessions = api_client
    config = BeaconHistoryConfig(base_dir=sessions.parent)
    assert append_record({"client_id": "beacon1", "output": "whoami"}, config) is True
    assert append_record({"client_id": "beacon1", "output": "id"}, config) is True
    body = client.get("/api/v1/results?client_id=beacon1", headers=_auth(token)).get_json()
    assert body["client_id"] == "beacon1"
    assert [r["output"] for r in body["records"]] == ["whoami", "id"]
    overview = client.get("/api/v1/results", headers=_auth(token)).get_json()
    assert overview["clients"] == ["beacon1"]
    assert overview["latest"][0]["record"]["output"] == "id"


def test_campaigns_empty_state(api_client) -> None:
    client, token, _ = api_client
    body = client.get("/api/v1/campaigns", headers=_auth(token)).get_json()
    assert body == {"phase": None, "pending_objectives": 0}


def test_campaigns_reads_state_files(api_client) -> None:
    client, token, sessions = api_client
    (sessions / "world_model.json").write_text(json.dumps({"phase": "exploitation"}), encoding="utf-8")
    (sessions / "objectives.jsonl").write_text('{"goal": "a"}\n{"goal": "b"}\n', encoding="utf-8")
    body = client.get("/api/v1/campaigns", headers=_auth(token)).get_json()
    assert body == {"phase": "exploitation", "pending_objectives": 2}


def test_webhook_crud(api_client) -> None:
    client, token, _ = api_client
    headers = _auth(token)
    assert client.get("/api/v1/webhooks", headers=headers).get_json() == {"webhooks": []}
    created = client.post(
        "/api/v1/webhooks", json={"url": "https://siem.local/hook", "events": ["results"]}, headers=headers
    )
    assert created.status_code == 201
    assert created.get_json()["index"] == 0
    listed = client.get("/api/v1/webhooks", headers=headers).get_json()
    assert listed["webhooks"][0]["url"] == "https://siem.local/hook"
    removed = client.delete("/api/v1/webhooks/0", headers=headers)
    assert removed.status_code == 200
    assert client.get("/api/v1/webhooks", headers=headers).get_json() == {"webhooks": []}
    assert client.delete("/api/v1/webhooks/0", headers=headers).status_code == 404


def test_webhook_rejects_bad_url(api_client) -> None:
    client, token, _ = api_client
    response = client.post("/api/v1/webhooks", json={"url": "ftp://evil.local/x"}, headers=_auth(token))
    assert response.status_code == 400
    response = client.post("/api/v1/webhooks", json={}, headers=_auth(token))
    assert response.status_code == 400


def test_mutating_endpoints_require_auth(api_client) -> None:
    client, _, _ = api_client
    assert client.post("/api/v1/webhooks", json={"url": "https://x.local/"}).status_code == 401
    assert client.delete("/api/v1/webhooks/0").status_code == 401
    assert client.get("/api/v1/results").status_code == 401
    assert client.get("/api/v1/campaigns").status_code == 401
