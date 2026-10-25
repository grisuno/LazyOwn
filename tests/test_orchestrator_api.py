"""Integration tests for the orchestrator REST API (``/api/v1/orchestrator``).

Builds a minimal Flask app with ``orchestrator_bp`` registered, a
sandboxed sessions configuration and a tenant API key. Covers status
awareness (world model, kill chain, verbs, triggers), verb and stage
toggling with catalog persistence, and trigger management.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from flask import Flask

from core.api_authz import ApiAuthzConfig, ApiKeyStore, create_api_token
from lazyc2.blueprints.orchestrator import orchestrator_bp


@pytest.fixture()
def orchestrator_client(tmp_path: Path, monkeypatch):
    """Flask test client with isolated orchestrator state and API key."""
    import modules.lazy_loop as loop

    sessions = tmp_path / "sessions"
    sessions.mkdir()
    monkeypatch.setattr(loop, "STORE_DIR", sessions)
    monkeypatch.setattr(loop, "_store_path", lambda name: sessions / name)

    store = ApiKeyStore(config=ApiAuthzConfig(api_keys_path=str(tmp_path / "api_keys.json")))
    token = create_api_token(store, tenant_id="test-tenant", label="pytest")

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.secret_key = "test-secret"
    app.config["SESSIONS_DIR"] = str(sessions)
    app.config["lazyown_api_key_store"] = store
    app.register_blueprint(orchestrator_bp)
    return app.test_client(), token, sessions


def _auth(token: str) -> dict[str, str]:
    return {"X-API-Key": token}


def test_status_requires_auth(orchestrator_client):
    """Given no API key, the status endpoint refuses with 401."""
    client, _, _ = orchestrator_client
    response = client.get("/api/v1/orchestrator/status")
    assert response.status_code == 401


def test_status_reports_layers(orchestrator_client):
    """Given the campaign layers, status returns every counter."""
    from modules.world_model import get_world_model

    client, token, _ = orchestrator_client
    get_world_model().add_host("10.10.11.5")
    body = client.get("/api/v1/orchestrator/status", headers=_auth(token)).get_json()
    assert "world" in body
    assert "verbs" in body
    assert "triggers" in body
    assert "stage_names" in body


def test_verb_toggle_round_trip(orchestrator_client, tmp_path, monkeypatch):
    """Given an operator toggle, the catalog YAML state flips."""
    import os

    from modules import verb_catalog
    from modules.verb_catalog import VerbCatalogConfig

    monkeypatch.setattr(
        verb_catalog,
        "_default_config",
        lambda: VerbCatalogConfig(catalog_path=tmp_path / "verbs.yaml"),
    )
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        verb_catalog.sync()
    finally:
        os.chdir(old_cwd)
    client, token, _ = orchestrator_client
    first = client.post(
        "/api/v1/orchestrator/verbs/toggle",
        json={"name": "lazynmap"},
        headers=_auth(token),
    )
    assert first.status_code == 200
    body = first.get_json()
    assert body["name"] == "lazynmap"
    assert isinstance(body["enabled"], bool)


def test_verb_toggle_unknown_command_rejected(orchestrator_client, tmp_path, monkeypatch):
    """Given a command outside the shell catalogue, the API returns 404."""
    from modules import verb_catalog
    from modules.verb_catalog import VerbCatalogConfig

    monkeypatch.setattr(
        verb_catalog,
        "_default_config",
        lambda: VerbCatalogConfig(catalog_path=tmp_path / "verbs.yaml"),
    )
    client, token, _ = orchestrator_client
    response = client.post(
        "/api/v1/orchestrator/verbs/toggle",
        json={"name": "not_a_real_command"},
        headers=_auth(token),
    )
    assert response.status_code == 404


def test_stage_toggle_round_trip(orchestrator_client, monkeypatch, tmp_path):
    """Given a stage name, the toggle flips its enabled flag."""
    import json as _json
    from pathlib import Path as _Path

    from modules import orchestrator_config
    from modules.orchestrator_config import stage_enabled

    isolated = tmp_path / "payload.json"

    def _load() -> dict:
        if isolated.is_file():
            return _json.loads(isolated.read_text(encoding="utf-8"))
        return {}

    def _write(payload: dict) -> None:
        isolated.write_text(_json.dumps(payload), encoding="utf-8")
        orchestrator_config._invalidate()

    monkeypatch.setattr(orchestrator_config, "_payload", _load)
    monkeypatch.setattr(orchestrator_config, "_save", _write)
    client, token, _ = orchestrator_client
    name = "scheduler"
    before = stage_enabled(name)
    response = client.post(
        "/api/v1/orchestrator/stages/toggle",
        json={"name": name},
        headers=_auth(token),
    )
    assert response.status_code == 200
    assert stage_enabled(name) != before


def test_stage_unknown_rejected(orchestrator_client):
    """Given an unknown stage, the API returns 404 without writing."""
    client, token, _ = orchestrator_client
    response = client.post(
        "/api/v1/orchestrator/stages/toggle",
        json={"name": "definitely-not-a-stage"},
        headers=_auth(token),
    )
    assert response.status_code == 404


def test_trigger_crud_round_trip(orchestrator_client):
    """Given a POST trigger then DELETE, the store rows change exactly once."""
    from modules.trigger_policy import export_store

    client, token, _ = orchestrator_client
    created = client.post(
        "/api/v1/orchestrator/triggers",
        json={"kind": "interval", "every_sec": 30},
        headers=_auth(token),
    )
    assert created.status_code == 200
    rows = export_store()
    assert any(row["kind"] == "interval" for row in rows)
    trigger_id = int(rows[-1]["id"])
    removed = client.delete(f"/api/v1/orchestrator/triggers/{trigger_id}", headers=_auth(token))
    assert removed.status_code == 200
    assert all(int(row["id"]) != trigger_id for row in export_store())


def test_trigger_unknown_kind_rejected(orchestrator_client):
    """Given an unknown trigger kind, the API returns 400."""
    client, token, _ = orchestrator_client
    response = client.post(
        "/api/v1/orchestrator/triggers",
        json={"kind": "nope", "every_sec": 0},
        headers=_auth(token),
    )
    assert response.status_code == 400
