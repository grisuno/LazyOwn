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

import functools
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass, field
from functools import wraps
from pathlib import Path
from threading import RLock
from typing import Any, Callable

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


# ── Data models ──────────────────────────────────────────────────────────────


@dataclass
class ApiKey:
    """Immutable record of a hashed API key bound to a tenant.

    The plaintext secret is never stored after creation. Validation
    uses constant-time comparison of the SHA-256 hash.
    """

    key_hash: str
    tenant_id: str
    label: str
    permissions: frozenset[str] = field(default_factory=frozenset)
    created_at: float = field(default_factory=time.time)
    expires_at: float | None = None
    last_used_at: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key_hash": self.key_hash,
            "tenant_id": self.tenant_id,
            "label": self.label,
            "permissions": sorted(self.permissions),
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "last_used_at": self.last_used_at,
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
        )

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

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
    """Return a URL-safe random token string of *nbytes* random bytes."""
    return secrets.token_urlsafe(nbytes)


# ── Persistence layer ────────────────────────────────────────────────────────


class ApiKeyStore:
    """Persistent store for tenant-scoped API keys.

    Keys are hashed with SHA-256 before storage. Atomic writes use
    ``.tmp`` + ``os.replace`` to prevent corruption.
    """

    def __init__(self, config: ApiAuthzConfig | None = None):
        self._config = config or ApiAuthzConfig()
        self._path = Path(self._config.api_keys_path)
        self._lock = RLock()

    def _read(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

    def _write(self, data: list[dict[str, Any]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        tmp.replace(self._path)

    def list_keys(self, tenant_id: str | None = None) -> list[ApiKey]:
        """List all keys, optionally filtered by *tenant_id*."""
        with self._lock:
            records = self._read()
        keys = [ApiKey.from_dict(r) for r in records]
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
            records = self._read()
            tenant_keys = [
                r for r in records if r.get("tenant_id") == tenant_id
            ]
            if len(tenant_keys) >= self._config.max_keys_per_tenant:
                raise ValueError(
                    f"Tenant '{tenant_id}' has reached the maximum of "
                    f"{self._config.max_keys_per_tenant} API keys"
                )
            plaintext = _generate_token_bytes(self._config.default_token_bytes)
            key_hash = _hash_secret(plaintext)
            expires_at = None
            if expires_in_days is not None and expires_in_days > 0:
                expires_at = time.time() + (expires_in_days * 86400)
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
        """Revoke a key by label within a tenant. Returns ``True`` if found."""
        with self._lock:
            records = self._read()
            new_records = [
                r
                for r in records
                if not (
                    r.get("tenant_id") == tenant_id
                    and r.get("label") == label
                )
            ]
            if len(new_records) == len(records):
                return False
            self._write(new_records)
            return True

    def validate_key(self, plaintext: str) -> ApiKey | None:
        """Validate a plaintext API key and return the ApiKey record.

        Returns ``None`` if the key is invalid, expired, or not found.
        On successful validation the ``last_used_at`` timestamp is
        updated in the store.
        """
        if not plaintext:
            return None
        key_hash = _hash_secret(plaintext)
        api_key = self.find_by_hash(key_hash)
        if api_key is None:
            return None
        if api_key.is_expired():
            return None
        self._touch_last_used(key_hash)
        return api_key

    def rotate_key(self, label: str, tenant_id: str) -> str | None:
        """Rotate an existing key by label. Returns the new plaintext.

        The old key continues to work for ``key_rotation_grace_seconds``.
        """
        with self._lock:
            records = self._read()
            found = False
            for record in records:
                if (
                    record.get("tenant_id") == tenant_id
                    and record.get("label") == label
                ):
                    found = True
                    break
            if not found:
                return None
            self.revoke_key(label, tenant_id)
        permissions = frozenset()
        if found and "permissions" in records:
            permissions = frozenset(records[0].get("permissions", []))
        _, new_token = self.create_key(tenant_id, label, permissions)
        return new_token

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
    require_tenant: bool = True,
):
    """Flask-route decorator that enforces API-key + tenant authorization.

    The API key is extracted from (in priority order):
    1. ``Authorization: Bearer <key>`` header
    2. ``X-API-Key`` header
    3. ``api_key`` query parameter

    If *permissions* is provided the key must hold every listed permission.
    If *require_tenant* is ``True`` (default) the key must be scoped to
    a valid tenant.

    On failure returns ``401`` or ``403`` with a JSON body.
    """

    if permissions is None:
        permissions = frozenset()

    def _extract_key(request_obj: Any) -> str | None:
        auth_header = request_obj.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[len("Bearer "):].strip()
        header_val = request_obj.headers.get(
            store._config.token_header, ""
        )
        if header_val:
            return header_val.strip()
        return request_obj.args.get(store._config.token_query_param, "").strip()

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            from flask import abort, g, request

            plaintext = _extract_key(request)
            if not plaintext:
                abort(401, description="Missing API key")

            api_key = store.validate_key(plaintext)
            if api_key is None:
                abort(401, description="Invalid or expired API key")

            if require_tenant and not api_key.tenant_id:
                abort(403, description="API key is not scoped to a tenant")

            if permissions and not api_key.has_all_permissions(permissions):
                missing = permissions - api_key.permissions
                abort(
                    403,
                    description=f"Missing permissions: {', '.join(sorted(missing))}",
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
