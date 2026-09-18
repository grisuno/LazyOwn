# lazyc2/security

*Community 7 | 11 files | cohesion 0.63*

## Definition

This community groups 11 file(s) rooted at `lazyc2/security` with dominant language py (cohesion 0.63). Central symbols: `AESKeyManager`, `ApiAuthzConfig`, `ApiKey`, `ApiKeyStore`, `SafeFileService`, `SecretKeyManager`, `TestAESKeyManager`, `TestAESKeyValidator`. Core file: `tests/test_security_lazyc2.py` (58 symbols). Documented purpose: Tenant-bound API authorization for the LazyOwn C2 dashboard.  Provides API-key generation, storage, validation, and route-decorator enforcement that requires bo.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |
| `lazyc2/app_factory.py` | py | presentation | 9 | yes |
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/constants.py` | py | utility | 0 | yes |
| `lazyc2/security/html_sanitizer.py` | py | utility | 2 | yes |
| `lazyc2/security/services.py` | py | business_logic | 16 | yes |
| `lazyc2/security/validators.py` | py | utility | 8 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |
| `tests/test_html_sanitizer.py` | py | testing | 16 | yes |
| `tests/test_security_lazyc2.py` | py | testing | 58 | yes |

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

- Internal resolved imports (EXTRACTED): 33
- Cross-boundary resolved imports (EXTRACTED): 12

## Connections

- [EXTRACTED] depends_on community 7 <-> 4 (strength 0.9): Extracted import edge crosses communities: lazyc2/app_factory.py imports lazyc2/blueprints/__init__.py.

## Risks

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
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `lazyc2/security/__init__.py`)? What purpose do they serve?
- What would break if the most connected file in lazyc2/security changed?
- Should lazyc2/security be split, given cohesion 0.63?

## Sources

- `core/api_authz.py`
- `lazyc2/app_factory.py`
- `lazyc2/extensions/__init__.py`
- `lazyc2/security/__init__.py`
- `lazyc2/security/constants.py`
- `lazyc2/security/html_sanitizer.py`
- `lazyc2/security/services.py`
- `lazyc2/security/validators.py`
- `tests/test_api_authz.py`
- `tests/test_html_sanitizer.py`
- `tests/test_security_lazyc2.py`
