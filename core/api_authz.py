"""Tenant-bound API authorization for the LazyOwn C2 dashboard.

Provides API-key generation, storage, validation, and route-decorator
enforcement that requires both a valid key AND tenant membership.
Keys are hashed at rest with ``hashlib.sha256``; only the plaintext
is returned once at creation time.

This module is self-contained and has zero dependencies beyond the
Python standard library. It integrates with Flask via decorators and
with the ``modules/lazy_rbac.py`` RBAC system for permission checks.

Contracts
---------
* ``ApiKeyStore``: persistence layer (atomic writes, no plaintext storage).
* ``require_api_auth``: Flask-route decorator that reads the API key from
  headers or query params, validates it, resolves the tenant, and enforces
  the required permissions.
* ``create_api_token``: convenience helper that stores the key and returns
  the one-time plaintext secret.

Usage::

    from core.api_authz import ApiAuthzConfig, ApiKeyStore, require_api_auth

    _store = ApiKeyStore(config=ApiAuthzConfig())

    @app.route("/api/secrets")
    @require_api_auth(store=_store, permissions={"api:read"})
    def secrets():
        return jsonify(...)

    token = create_api_token(store=_store, tenant_id="acme", label="bot-01")
    # → token only displayed ONCE
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from pathlib import Path
from threading import RLock
from typing import Any

# ── Config ───────────────────────────────────────────────────────────────────


@dataclass
class ApiAuthzConfig:
    """Configuration contract for the API authorization module.

    Every tunable value is defined here; no magic numbers exist elsewhere.
    """

    api_keys_path: str = "sessions/api_keys.json"
    token_header: str = "X-API-Key"
    token_query_param: str = "api_key"
    token_bearer_prefix: str = "Bearer "
    require_tenant_scope: bool = True
    default_token_bytes: int = 32
    max_keys_per_tenant: int = 100
    key_rotation_grace_seconds: int = 300
    seconds_per_day: int = 86400


# ── Data models ──────────────────────────────────────────────────────────────


@dataclass
class ApiKey:
    """Immutable record of a hashed API key bound to a tenant.

    The plaintext secret is never stored after creation. Validation
    uses constant-time comparison of the SHA-256 hash. ``retired_at``
    marks a rotated key: it stays valid for the configured grace
    window so live clients keep working during a rotation, then it is
    pruned from the store.
    """

    key_hash: str
    tenant_id: str
    label: str
    permissions: frozenset[str] = field(default_factory=frozenset)
    created_at: float = field(default_factory=time.time)
    expires_at: float | None = None
    last_used_at: float | None = None
    retired_at: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key_hash": self.key_hash,
            "tenant_id": self.tenant_id,
            "label": self.label,
            "permissions": sorted(self.permissions),
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "last_used_at": self.last_used_at,
            "retired_at": self.retired_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ApiKey:
        return cls(
            key_hash=data["key_hash"],
            tenant_id=data.get("tenant_id", "default"),
            label=data.get("label", ""),
            permissions=frozenset(data.get("permissions", [])),
            created_at=data.get("created_at", time.time()),
            expires_at=data.get("expires_at"),
            last_used_at=data.get("last_used_at"),
            retired_at=data.get("retired_at"),
        )

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def is_retired(self) -> bool:
        return self.retired_at is not None

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    def has_all_permissions(self, permissions: frozenset[str]) -> bool:
        return permissions.issubset(self.permissions)


# ── Hashing helpers ──────────────────────────────────────────────────────────


def _hash_secret(secret: str) -> str:
    """Return the SHA-256 hex digest of *secret*."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def _verify_secret(secret: str, stored_hash: str) -> bool:
    """Constant-time comparison of *secret* against *stored_hash*."""
    return hmac.compare_digest(_hash_secret(secret), stored_hash)


def _generate_token_bytes(nbytes: int = 32) -> str:
    """Return a URL-safe random token string of *nbytes* random bytes.

    Args:
        nbytes: Number of random bytes to encode. Defaults to
            :data:`ApiAuthzConfig.default_token_bytes` for backwards
            compatibility with direct callers.
    """
    return secrets.token_urlsafe(nbytes)


# ── Persistence layer ────────────────────────────────────────────────────────


class ApiKeyStore:
    """Persistent store for tenant-scoped API keys.

    Keys are hashed with SHA-256 before storage. Atomic writes use
    ``.tmp`` + ``os.replace`` to prevent corruption. Rotated keys are
    retired (not deleted) so they stay valid during the configured
    grace window, then pruned lazily.
    """

    def __init__(self, config: ApiAuthzConfig | None = None):
        self._config = config or ApiAuthzConfig()
        self._path = Path(self._config.api_keys_path)
        self._lock = RLock()

    @property
    def config(self) -> ApiAuthzConfig:
        """The configuration this store was built with."""
        return self._config

    def _read(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        return [record for record in data if isinstance(record, dict) and "key_hash" in record]

    def _write(self, data: list[dict[str, Any]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        tmp.replace(self._path)

    def _grace_deadline(self, retired_at: float) -> float:
        """Return the timestamp after which a retired key stops validating."""
        return retired_at + self._config.key_rotation_grace_seconds

    def _prune_retired(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Drop retired keys whose grace window has closed.

        Args:
            records: The record list to filter.

        Returns:
            The record list without expired retired entries.
        """
        now = time.time()
        return [
            record
            for record in records
            if not (record.get("retired_at") is not None and now > self._grace_deadline(record["retired_at"]))
        ]

    def list_keys(self, tenant_id: str | None = None) -> list[ApiKey]:
        """List all active keys, optionally filtered by *tenant_id*.

        Retired keys are excluded: the operator sees the live key set.
        """
        with self._lock:
            records = self._read()
        keys = [ApiKey.from_dict(record) for record in records if record.get("retired_at") is None]
        if tenant_id is not None:
            keys = [k for k in keys if k.tenant_id == tenant_id]
        return keys

    def find_by_hash(self, key_hash: str) -> ApiKey | None:
        """Look up a key record by its SHA-256 hash."""
        with self._lock:
            records = self._read()
        for record in records:
            if hmac.compare_digest(record["key_hash"], key_hash):
                return ApiKey.from_dict(record)
        return None

    def create_key(
        self,
        tenant_id: str,
        label: str,
        permissions: frozenset[str] | None = None,
        expires_in_days: int | None = None,
    ) -> tuple[ApiKey, str]:
        """Create a new API key and return ``(ApiKey, plaintext_secret)``.

        The plaintext secret is returned only once. The caller must
        display it to the operator immediately.
        """
        with self._lock:
            records = self._prune_retired(self._read())
            tenant_keys = [r for r in records if r.get("tenant_id") == tenant_id]
            if len(tenant_keys) >= self._config.max_keys_per_tenant:
                raise ValueError(
                    f"Tenant '{tenant_id}' has reached the maximum of {self._config.max_keys_per_tenant} API keys"
                )
            plaintext = _generate_token_bytes(self._config.default_token_bytes)
            key_hash = _hash_secret(plaintext)
            expires_at = None
            if expires_in_days is not None and expires_in_days > 0:
                expires_at = time.time() + (expires_in_days * self._config.seconds_per_day)
            api_key = ApiKey(
                key_hash=key_hash,
                tenant_id=tenant_id,
                label=label,
                permissions=permissions or frozenset(),
                expires_at=expires_at,
            )
            records.append(api_key.to_dict())
            self._write(records)
            return api_key, plaintext

    def revoke_key(self, label: str, tenant_id: str) -> bool:
        """Revoke every key with *label* within *tenant_id*.

        Both active and retired records are removed. Returns ``True``
        when at least one record was found.
        """
        with self._lock:
            records = self._read()
            new_records = [r for r in records if not (r.get("tenant_id") == tenant_id and r.get("label") == label)]
            if len(new_records) == len(records):
                return False
            self._write(new_records)
            return True

    def validate_key(self, plaintext: str) -> ApiKey | None:
        """Validate a plaintext API key and return the ApiKey record.

        Returns ``None`` if the key is invalid, expired, retired past its
        grace window, or not found. On successful validation the
        ``last_used_at`` timestamp is updated in the store.
        """
        if not plaintext:
            return None
        key_hash = _hash_secret(plaintext)
        api_key = self.find_by_hash(key_hash)
        if api_key is None:
            return None
        if api_key.is_expired():
            return None
        if api_key.retired_at is not None:
            if time.time() > self._grace_deadline(api_key.retired_at):
                self._prune_record(key_hash)
                return None
        self._touch_last_used(key_hash)
        return api_key

    def rotate_key(self, label: str, tenant_id: str) -> str | None:
        """Rotate an existing key by label. Returns the new plaintext.

        The old key keeps working for ``key_rotation_grace_seconds`` so
        clients can switch without an outage. Permissions and expiration
        are copied from the rotated key, never from another record.
        """
        with self._lock:
            records = self._prune_retired(self._read())
            active = [
                record
                for record in records
                if record.get("tenant_id") == tenant_id
                and record.get("label") == label
                and record.get("retired_at") is None
            ]
            if not active:
                return None
            source = active[0]
            plaintext = _generate_token_bytes(self._config.default_token_bytes)
            api_key = ApiKey(
                key_hash=_hash_secret(plaintext),
                tenant_id=tenant_id,
                label=label,
                permissions=frozenset(source.get("permissions", [])),
                expires_at=source.get("expires_at"),
            )
            now = time.time()
            for record in active:
                record["retired_at"] = now
            records.append(api_key.to_dict())
            self._write(records)
            return plaintext

    def _prune_record(self, key_hash: str) -> None:
        """Remove the retired record identified by *key_hash*."""
        with self._lock:
            records = self._read()
            kept = [record for record in records if not hmac.compare_digest(record.get("key_hash", ""), key_hash)]
            if len(kept) != len(records):
                self._write(kept)

    def _touch_last_used(self, key_hash: str) -> None:
        """Update ``last_used_at`` on the key record identified by *key_hash*."""
        with self._lock:
            records = self._read()
            for record in records:
                if hmac.compare_digest(record["key_hash"], key_hash):
                    record["last_used_at"] = time.time()
                    break
            self._write(records)


# ── Decorator ────────────────────────────────────────────────────────────────


def require_api_auth(
    store: ApiKeyStore,
    permissions: frozenset[str] | None = None,
    require_tenant: bool | None = None,
):
    """Flask-route decorator that enforces API-key + tenant authorization.

    The API key is extracted from (in priority order):
    1. ``Authorization: Bearer <key>`` header
    2. ``X-API-Key`` header
    3. ``api_key`` query parameter

    If *permissions* is provided the key must hold every listed permission.
    If *require_tenant* is ``True`` the key must be scoped to a valid
    tenant; when omitted it defaults to
    :data:`ApiAuthzConfig.require_tenant_scope` so the security posture
    lives in one place.

    On failure the decorated route returns a JSON body with ``401`` or
    ``403`` — never an HTML error page and never ``abort()``, so the
    contract holds even in apps with ``TRAP_HTTP_EXCEPTIONS`` enabled.
    """

    if permissions is None:
        permissions = frozenset()
    if require_tenant is None:
        require_tenant = store.config.require_tenant_scope

    def _extract_key(request_obj: Any) -> str | None:
        prefix = store.config.token_bearer_prefix
        auth_header = request_obj.headers.get("Authorization", "")
        if auth_header.startswith(prefix):
            bearer_token = auth_header[len(prefix) :].strip()
            if bearer_token:
                return bearer_token
        header_val = request_obj.headers.get(store.config.token_header, "")
        if header_val:
            return header_val.strip()
        return request_obj.args.get(store.config.token_query_param, "").strip()

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            from flask import g, jsonify, request

            plaintext = _extract_key(request)
            if not plaintext:
                return jsonify({"error": "Missing API key"}), 401

            api_key = store.validate_key(plaintext)
            if api_key is None:
                return jsonify({"error": "Invalid or expired API key"}), 401

            if require_tenant and not api_key.tenant_id:
                return jsonify({"error": "API key is not scoped to a tenant"}), 403

            if permissions and not api_key.has_all_permissions(permissions):
                missing = permissions - api_key.permissions
                return (
                    jsonify({"error": f"Missing permissions: {', '.join(sorted(missing))}"}),
                    403,
                )

            g.api_key_record = api_key
            g.api_tenant_id = api_key.tenant_id
            return f(*args, **kwargs)

        return decorated

    return decorator


# ── Convenience helpers ──────────────────────────────────────────────────────


def create_api_token(
    store: ApiKeyStore,
    tenant_id: str,
    label: str,
    permissions: frozenset[str] | None = None,
    expires_in_days: int | None = None,
) -> str:
    """Create an API key and return the one-time plaintext token.

    Args:
        store: The ApiKeyStore instance to persist the key.
        tenant_id: Tenant to which the key is bound.
        label: Human-readable label for the key.
        permissions: Optional set of permission strings.
        expires_in_days: If set, the key expires after this many days.

    Returns:
        The plaintext API token. Display once and store securely.
    """
    _, token = store.create_key(
        tenant_id=tenant_id,
        label=label,
        permissions=permissions or frozenset(),
        expires_in_days=expires_in_days,
    )
    return token
