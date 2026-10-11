# lazyc2/security

*Community 7 | 53 files | cohesion 0.55*

## Definition

This community groups 53 file(s) rooted at `tests` with dominant language py (cohesion 0.55). Central symbols: `AESKeyManager`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`, `ApiAuthzConfig`. Core file: `lazyc2.py` (277 symbols). Documented purpose: Tenant-bound API authorization for the LazyOwn C2 dashboard.  Provides API-key generation, storage, validation, and route-decorator enforcement that requires bo.

## Files

### `tests` (16 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |
| `tests/test_command_allowlist.py` | py | testing | 14 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |
| `lazyc2/security/constants.py` | py | utility | 0 | yes |

### `lazyc2/blueprints` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `modules` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/compliance.py` | py | utility | 25 | yes |
| `modules/dashboard_bp.py` | py | presentation | 13 | yes |

### `lazyc2/extensions` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `lazyc2` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 277 | no |
| `pwntomate.py` | py | utility | 3 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |
| `static/js/socket.io-4.3.2.min.js` | js | utility | 15 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

*... and 33 more files in this community.*


## Key Symbols

- `ApiAuthzConfig` (class, `core/api_authz.py:54`) `class ApiAuthzConfig` - Configuration contract for the API authorization module.
- `ApiKey` (class, `core/api_authz.py:75`) `class ApiKey` - Immutable record of a hashed API key bound to a tenant.
- `to_dict` (method, `core/api_authz.py:94`) `def to_dict(self)`
- `from_dict` (method, `core/api_authz.py:107`) `def from_dict(cls, data)`
- `is_expired` (method, `core/api_authz.py:119`) `def is_expired(self)`
- `is_retired` (method, `core/api_authz.py:124`) `def is_retired(self)`
- `has_permission` (method, `core/api_authz.py:127`) `def has_permission(self, permission)`
- `has_all_permissions` (method, `core/api_authz.py:130`) `def has_all_permissions(self, permissions)`
- `_hash_secret` (method, `core/api_authz.py:137`) `def _hash_secret(secret)` - Return the SHA-256 hex digest of *secret*.
- `_verify_secret` (method, `core/api_authz.py:142`) `def _verify_secret(secret, stored_hash)` - Constant-time comparison of *secret* against *stored_hash*.
- `_generate_token_bytes` (method, `core/api_authz.py:147`) `def _generate_token_bytes(nbytes)` - Return a URL-safe random token string of *nbytes* random bytes.
- `ApiKeyStore` (class, `core/api_authz.py:161`) `class ApiKeyStore` - Persistent store for tenant-scoped API keys.
- `__init__` (method, `core/api_authz.py:170`) `def __init__(self, config)`
- `config` (method, `core/api_authz.py:176`) `def config(self)` - The configuration this store was built with.
- `_read` (method, `core/api_authz.py:180`) `def _read(self)`
- `_write` (method, `core/api_authz.py:191`) `def _write(self, data)`
- `_grace_deadline` (method, `core/api_authz.py:197`) `def _grace_deadline(self, retired_at)` - Return the timestamp after which a retired key stops validating.
- `_prune_retired` (method, `core/api_authz.py:201`) `def _prune_retired(self, records)` - Drop retired keys whose grace window has closed.
- `list_keys` (method, `core/api_authz.py:217`) `def list_keys(self, tenant_id)` - List all active keys, optionally filtered by *tenant_id*.
- `find_by_hash` (method, `core/api_authz.py:229`) `def find_by_hash(self, key_hash)` - Look up a key record by its SHA-256 hash.
- `create_key` (method, `core/api_authz.py:238`) `def create_key(self, tenant_id, label, permissions, expires_in_days)` - Create a new API key and return ``(ApiKey, plaintext_secret)``.
- `revoke_key` (method, `core/api_authz.py:273`) `def revoke_key(self, label, tenant_id)` - Revoke every key with *label* within *tenant_id*.
- `validate_key` (method, `core/api_authz.py:287`) `def validate_key(self, plaintext)` - Validate a plaintext API key and return the ApiKey record.
- `rotate_key` (method, `core/api_authz.py:309`) `def rotate_key(self, label, tenant_id)` - Rotate an existing key by label. Returns the new plaintext.
- `_prune_record` (method, `core/api_authz.py:343`) `def _prune_record(self, key_hash)` - Remove the retired record identified by *key_hash*.
- `_touch_last_used` (method, `core/api_authz.py:351`) `def _touch_last_used(self, key_hash)` - Update ``last_used_at`` on the key record identified by *key_hash*.
- `require_api_auth` (method, `core/api_authz.py:365`) `def require_api_auth(store, permissions, require_tenant)` - Flask-route decorator that enforces API-key + tenant authorization.
- `_extract_key` (method, `core/api_authz.py:393`) `def _extract_key(request_obj)`
- `decorator` (method, `core/api_authz.py:405`) `def decorator(f)`
- `decorated` (method, `core/api_authz.py:407`) `def decorated()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 119
- Cross-boundary resolved imports (EXTRACTED): 84

## Connections

- [EXTRACTED] depends_on community 0 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/listener_manager.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `lazyc2.py`)? What purpose do they serve?
- What would break if the most connected file in lazyc2/security changed?
- Should lazyc2/security be split, given cohesion 0.55?

## Sources

- `core/api_authz.py`
- `lazyc2.py`
- `lazyc2/__init__.py`
- `lazyc2/addon_creator.py`
- `lazyc2/app_factory.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/phishing.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/__init__.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/short_urls.py`
- `lazyc2/extensions/storage.py`
- `lazyc2/extensions/users.py`
- `lazyc2/models.py`
- `lazyc2/security/__init__.py`
- `lazyc2/security/command_allowlist.py`
- `lazyc2/security/constants.py`
- *... and 33 more*
