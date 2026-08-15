"""Tests for ``core.api_authz`` — tenant-bound API authorization.

Covers ApiAuthzConfig, ApiKey, ApiKeyStore, require_api_auth decorator,
and create_api_token helper.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(REPO_ROOT))


class TestApiAuthzConfig:
    """Behaviour of the ApiAuthzConfig dataclass."""

    def test_defaults_are_secure_by_default(self):
        from core.api_authz import ApiAuthzConfig

        cfg = ApiAuthzConfig()
        assert cfg.token_header == "X-API-Key"
        assert cfg.require_tenant_scope is True
        assert cfg.default_token_bytes == 32

    def test_custom_overrides_preserve_typed_semantics(self):
        from core.api_authz import ApiAuthzConfig

        cfg = ApiAuthzConfig(
            api_keys_path="/tmp/keys.json",
            max_keys_per_tenant=5,
            default_token_bytes=64,
        )
        assert cfg.api_keys_path == "/tmp/keys.json"
        assert cfg.max_keys_per_tenant == 5
        assert cfg.default_token_bytes == 64


class TestApiKey:
    """Behaviour of the ApiKey data class."""

    def test_serialization_roundtrip_preserves_all_fields(self):
        from core.api_authz import ApiKey

        original = ApiKey(
            key_hash="abc123",
            tenant_id="acme",
            label="bot-01",
            permissions=frozenset({"api:read", "api:write"}),
            expires_at=time.time() + 86400,
        )
        data = original.to_dict()
        restored = ApiKey.from_dict(data)
        assert restored.key_hash == original.key_hash
        assert restored.tenant_id == original.tenant_id
        assert restored.permissions == original.permissions
        assert restored.label == original.label

    def test_detects_expiration_correctly(self):
        from core.api_authz import ApiKey

        expired = ApiKey(
            key_hash="h1", tenant_id="t1", label="k1",
            expires_at=time.time() - 1,
        )
        assert expired.is_expired() is True

        valid = ApiKey(
            key_hash="h2", tenant_id="t2", label="k2",
            expires_at=time.time() + 3600,
        )
        assert valid.is_expired() is False

        never = ApiKey(key_hash="h3", tenant_id="t3", label="k3")
        assert never.is_expired() is False

    def test_checks_permissions_with_set_operations(self):
        from core.api_authz import ApiKey

        key = ApiKey(
            key_hash="h1", tenant_id="t1", label="k1",
            permissions=frozenset({"read", "write"}),
        )
        assert key.has_permission("read") is True
        assert key.has_permission("admin") is False
        assert key.has_all_permissions(frozenset({"read", "write"})) is True
        assert key.has_all_permissions(frozenset({"read", "admin"})) is False


class TestApiKeyStore:
    """Behaviour of the ApiKeyStore persistence layer."""

    def _make_store(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore
        return ApiKeyStore(config=ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
        ))

    def test_creates_and_lists_keys_scoped_by_tenant(self, tmp_path):
        store = self._make_store(tmp_path)
        store.create_key("acme", "bot-01")
        store.create_key("acme", "bot-02")
        store.create_key("other", "bot-03")

        all_keys = store.list_keys()
        assert len(all_keys) == 3
        acme_keys = store.list_keys(tenant_id="acme")
        assert len(acme_keys) == 2

    def test_validates_a_known_key_and_returns_record(self, tmp_path):
        store = self._make_store(tmp_path)
        _, token = store.create_key("acme", "validator")
        result = store.validate_key(token)
        assert result is not None
        assert result.tenant_id == "acme"
        assert result.label == "validator"

    def test_rejects_unknown_key_returning_none(self, tmp_path):
        store = self._make_store(tmp_path)
        assert store.validate_key("nonexistent-key-12345") is None

    def test_rejects_empty_plaintext_key(self, tmp_path):
        store = self._make_store(tmp_path)
        assert store.validate_key("") is None

    def test_rejects_expired_key(self, tmp_path):
        from core.api_authz import _hash_secret

        store = self._make_store(tmp_path)
        plaintext = "this-key-is-expired"
        key_hash = _hash_secret(plaintext)
        with store._lock:
            records = store._read()
            records.append({
                "key_hash": key_hash,
                "tenant_id": "acme",
                "label": "expired-bot",
                "permissions": [],
                "created_at": time.time(),
                "expires_at": time.time() - 1,
            })
            store._write(records)
        assert store.validate_key(plaintext) is None

    def test_updates_last_used_on_successful_validation(self, tmp_path):
        from core.api_authz import _hash_secret

        store = self._make_store(tmp_path)
        _, token = store.create_key("acme", "stalker")
        store.validate_key(token)
        record = store.find_by_hash(_hash_secret(token))
        assert record is not None
        assert record.last_used_at is not None
        assert record.last_used_at > 0

    def test_revokes_key_preventing_future_validation(self, tmp_path):
        store = self._make_store(tmp_path)
        _, token = store.create_key("acme", "to-revoke")
        assert store.revoke_key("to-revoke", "acme") is True
        assert store.validate_key(token) is None

    def test_revocation_is_idempotent(self, tmp_path):
        store = self._make_store(tmp_path)
        assert store.revoke_key("never-existed", "acme") is False

    def test_enforces_max_keys_per_tenant_raises_value_error(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore

        cfg = ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
            max_keys_per_tenant=2,
        )
        store = ApiKeyStore(config=cfg)
        store.create_key("limited", "k1")
        store.create_key("limited", "k2")
        with pytest.raises(ValueError, match="maximum"):
            store.create_key("limited", "k3")

    def test_rotates_key_preserving_tenant_label_and_permissions(self, tmp_path):
        store = self._make_store(tmp_path)
        store.create_key("acme", "rotator", permissions=frozenset({"read"}))
        new_token = store.rotate_key("rotator", "acme")
        assert new_token is not None
        assert store.validate_key(new_token) is not None
        keys = store.list_keys(tenant_id="acme")
        assert len(keys) == 1
        assert keys[0].label == "rotator"

    def test_rotation_copies_permissions_from_the_rotated_key(self, tmp_path):
        store = self._make_store(tmp_path)
        store.create_key("acme", "worker", permissions=frozenset({"read"}))
        store.create_key("acme", "admin", permissions=frozenset({"admin"}))
        new_token = store.rotate_key("worker", "acme")
        assert new_token is not None
        rotated = store.validate_key(new_token)
        assert rotated is not None
        assert rotated.permissions == frozenset({"read"})
        assert "admin" not in rotated.permissions

    def test_old_key_stays_valid_during_rotation_grace(self, tmp_path):
        store = self._make_store(tmp_path)
        _, old_token = store.create_key("acme", "graceful", permissions=frozenset({"read"}))
        new_token = store.rotate_key("graceful", "acme")
        assert new_token is not None
        assert store.validate_key(old_token) is not None
        assert store.validate_key(new_token) is not None

    def test_old_key_rejected_after_rotation_grace_expires(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore

        store = ApiKeyStore(config=ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
            key_rotation_grace_seconds=0,
        ))
        _, old_token = store.create_key("acme", "short-grace", permissions=frozenset({"read"}))
        new_token = store.rotate_key("short-grace", "acme")
        assert new_token is not None
        assert store.validate_key(new_token) is not None
        assert store.validate_key(old_token) is None

    def test_retired_keys_are_pruned_after_grace_expires(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore

        store = ApiKeyStore(config=ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
            key_rotation_grace_seconds=0,
        ))
        store.create_key("acme", "k1")
        store.rotate_key("k1", "acme")
        records_before = store._read()
        assert any(r.get("retired_at") is not None for r in records_before)
        store.create_key("other", "k2")
        records_after = store._read()
        assert all(r.get("retired_at") is None for r in records_after)
        assert len([r for r in records_after if r.get("tenant_id") == "acme"]) == 1

    def test_rotation_does_not_grow_active_key_count(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore

        store = ApiKeyStore(config=ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
            max_keys_per_tenant=2,
            key_rotation_grace_seconds=0,
        ))
        store.create_key("acme", "k1")
        store.create_key("acme", "k2")
        store.rotate_key("k1", "acme")
        keys = store.list_keys(tenant_id="acme")
        assert len(keys) == 2
        assert {k.label for k in keys} == {"k1", "k2"}

    def test_never_stores_plaintext_token_on_disk(self, tmp_path):
        from core.api_authz import _hash_secret

        store = self._make_store(tmp_path)
        _, token = store.create_key("acme", "stealth")
        records = store._read()
        stored = records[0]
        assert "key_hash" in stored
        raw = json.dumps(records)
        assert token not in raw
        assert stored["key_hash"] == _hash_secret(token)


class TestRequireApiAuth:
    """Behaviour of the require_api_auth Flask decorator."""

    def _make_app(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore, require_api_auth

        store = ApiKeyStore(config=ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
        ))
        return store

    def _build_client(self, tmp_path, store=None):
        from flask import Flask, g, jsonify
        from core.api_authz import require_api_auth

        if store is None:
            store = self._make_app(tmp_path)
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/secure")
        @require_api_auth(store=store)
        def secure():
            return jsonify({"tenant": g.api_tenant_id, "ok": True})

        @app.route("/g-check")
        @require_api_auth(store=store)
        def g_check():
            return jsonify({
                "api_tenant_id": getattr(g, "api_tenant_id", None),
                "has_api_key_record": getattr(g, "api_key_record", None) is not None,
            })

        @app.route("/admin-only")
        @require_api_auth(store=store, permissions=frozenset({"api:admin"}))
        def admin_only():
            return jsonify({"ok": True})

        return app.test_client(), store

    def test_allows_valid_key_in_bearer_header(self, tmp_path):
        client, store = self._build_client(tmp_path)
        _, token = store.create_key("acme", "bearer-bot")
        resp = client.get("/secure", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json["tenant"] == "acme"

    def test_allows_valid_key_in_x_api_key_header(self, tmp_path):
        client, store = self._build_client(tmp_path)
        _, token = store.create_key("acme", "header-bot")
        resp = client.get("/secure", headers={"X-API-Key": token})
        assert resp.status_code == 200

    def test_allows_valid_key_in_query_param(self, tmp_path):
        client, store = self._build_client(tmp_path)
        _, token = store.create_key("acme", "query-bot")
        resp = client.get(f"/secure?api_key={token}")
        assert resp.status_code == 200

    def test_rejects_missing_key_with_401(self, tmp_path):
        client, store = self._build_client(tmp_path)
        resp = client.get("/secure")
        assert resp.status_code == 401

    def test_rejects_invalid_key_with_401(self, tmp_path):
        client, store = self._build_client(tmp_path)
        resp = client.get("/secure", headers={"X-API-Key": "fake-key-12345"})
        assert resp.status_code == 401

    def test_rejects_key_with_insufficient_permissions_with_403(self, tmp_path):
        client, store = self._build_client(tmp_path)
        _, token = store.create_key("acme", "reader", permissions=frozenset({"api:read"}))
        resp = client.get("/admin-only", headers={"X-API-Key": token})
        assert resp.status_code == 403

    def test_sets_g_variables_with_api_key_context_on_success(self, tmp_path):
        client, store = self._build_client(tmp_path)
        _, token = store.create_key("acme", "g-checker")
        resp = client.get("/g-check", headers={"X-API-Key": token})
        assert resp.status_code == 200
        assert resp.json["api_tenant_id"] == "acme"
        assert resp.json["has_api_key_record"] is True


class TestCreateApiToken:
    """Behaviour of the create_api_token convenience helper."""

    def _make_store(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore
        return ApiKeyStore(config=ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
        ))

    def test_returns_a_validatable_token(self, tmp_path):
        from core.api_authz import create_api_token

        store = self._make_store(tmp_path)
        token = create_api_token(store, "acme", "helper-bot")
        assert len(token) > 20
        assert store.validate_key(token) is not None

    def test_stores_permissions_on_the_key_record(self, tmp_path):
        from core.api_authz import create_api_token

        store = self._make_store(tmp_path)
        token = create_api_token(
            store, "acme", "power-bot",
            permissions=frozenset({"admin", "write"}),
        )
        record = store.validate_key(token)
        assert record is not None
        assert "admin" in record.permissions
        assert "write" in record.permissions

    def test_sets_expiration_when_days_are_provided(self, tmp_path):
        from core.api_authz import create_api_token

        store = self._make_store(tmp_path)
        token = create_api_token(store, "acme", "temporal", expires_in_days=7)
        record = store.validate_key(token)
        assert record is not None
        assert record.expires_at is not None
        assert record.expires_at > time.time()


class TestEdgeCases:
    """Edge-case and security boundary tests for api_authz."""

    def _make_store(self, tmp_path):
        from core.api_authz import ApiAuthzConfig, ApiKeyStore
        return ApiKeyStore(config=ApiAuthzConfig(
            api_keys_path=str(tmp_path / "api_keys.json"),
        ))

    def test_constant_time_comparison_rejects_wrong_secrets(self):
        from core.api_authz import _verify_secret
        import hashlib
        real = hashlib.sha256(b"realsecret").hexdigest()
        assert _verify_secret("realsecret", real) is True
        assert _verify_secret("wrong", real) is False

    def test_generates_50_unique_tokens_without_collision(self):
        from core.api_authz import _generate_token_bytes
        tokens = {_generate_token_bytes() for _ in range(50)}
        assert len(tokens) == 50

    def test_atomic_write_leaves_no_tmp_files(self, tmp_path):
        store = self._make_store(tmp_path)
        store.create_key("acme", "atomic")
        for sibling in store._path.parent.iterdir():
            assert not sibling.name.endswith(".tmp"), f"leftover tmp: {sibling}"
