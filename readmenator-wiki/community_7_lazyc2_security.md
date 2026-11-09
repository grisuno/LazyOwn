# lazyc2/security

*Community 7 | 72 files | cohesion 0.52*

## Definition

This community groups 72 file(s) rooted at `tests` with dominant language py (cohesion 0.52). Central symbols: `AESKeyManager`, `ApiAuthzConfig`, `ApiKey`, `ApiKeyStore`, `BindAddressResolver`, `C2Server`, `CSRFPolicy`, `CheckpointSerializer`. Core file: `lazyc2.py` (313 symbols). Documented purpose: Tenant-bound API authorization for the LazyOwn C2 dashboard.  Provides API-key generation, storage, validation, and route-decorator enforcement that requires bo.

## Files

### `tests` (20 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |

### `lazyc2/security` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/cli_credentials.py` | py | utility | 3 | yes |

### `modules` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/c2_agent.py` | py | utility | 20 | yes |
| `modules/dashboard_bp.py` | py | presentation | 13 | yes |

### `skills/hermes-lazyown` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |

### `lazyc2/blueprints` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `lazyc2/extensions` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `lazyc2` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/app_factory.py` | py | presentation | 12 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 313 | no |

### `contrib/legacy` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

*... and 52 more files in this community.*


## Key Symbols

- `SamsungKnoxExploitServer` (class, `contrib/legacy/lazygalazy.py:8`) `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)`
- `do_GET` (method, `contrib/legacy/lazygalazy.py:11`) `def do_GET(self)`
- `apk_bytes` (method, `contrib/legacy/lazygalazy.py:33`) `def apk_bytes(self)`
- `launch_html` (method, `contrib/legacy/lazygalazy.py:36`) `def launch_html(self)`
- `exploit_js` (method, `contrib/legacy/lazygalazy.py:49`) `def exploit_js(self)`
- `rand_word` (method, `contrib/legacy/lazygalazy.py:93`) `def rand_word(self)`
- `main` (function, `contrib/legacy/lazygalazy.py:97`) `def main()`
- `encrypt` (function, `contrib/legacy/lazyhttpreverseshell.py:14`) `def encrypt(data)`
- `decrypt` (function, `contrib/legacy/lazyhttpreverseshell.py:17`) `def decrypt(data)`
- `compress` (function, `contrib/legacy/lazyhttpreverseshell.py:20`) `def compress(data)`
- `decompress` (function, `contrib/legacy/lazyhttpreverseshell.py:23`) `def decompress(data)`
- `reverse_http_shell_client` (function, `contrib/legacy/lazyhttpreverseshell.py:26`) `def reverse_http_shell_client(lhost, rhost, rport)`
- `reverse_http_shell_server` (function, `contrib/legacy/lazyhttpreverseshell.py:50`) `def reverse_http_shell_server(lhost, lport)`
- `RequestHandler` (class, `contrib/legacy/lazyhttpreverseshell.py:51`) `class RequestHandler(BaseHTTPRequestHandler)`
- `do_GET` (method, `contrib/legacy/lazyhttpreverseshell.py:52`) `def do_GET(self)`
- `do_POST` (method, `contrib/legacy/lazyhttpreverseshell.py:65`) `def do_POST(self)`
- `parse_arguments` (function, `contrib/legacy/lazyhttpreverseshell.py:88`) `def parse_arguments(args)`
- `ApiAuthzConfig` (class, `core/api_authz.py:54`) `class ApiAuthzConfig` - Configuration contract for the API authorization module.
- `ApiKey` (class, `core/api_authz.py:75`) `class ApiKey` - Immutable record of a hashed API key bound to a tenant.
- `to_dict` (method, `core/api_authz.py:94`) `def to_dict(self)`
- `from_dict` (method, `core/api_authz.py:107`) `def from_dict(cls, data)`
- `is_expired` (method, `core/api_authz.py:119`) `def is_expired(self)`
- `is_retired` (method, `core/api_authz.py:124`) `def is_retired(self)`
- `has_permission` (method, `core/api_authz.py:127`) `def has_permission(self, permission)`
- `has_all_permissions` (method, `core/api_authz.py:130`) `def has_all_permissions(self, permissions)`
- `_hash_secret` (function, `core/api_authz.py:137`) `def _hash_secret(secret)` - Return the SHA-256 hex digest of *secret*.
- `_verify_secret` (function, `core/api_authz.py:142`) `def _verify_secret(secret, stored_hash)` - Constant-time comparison of *secret* against *stored_hash*.
- `_generate_token_bytes` (function, `core/api_authz.py:147`) `def _generate_token_bytes(nbytes)` - Return a URL-safe random token string of *nbytes* random bytes.
- `ApiKeyStore` (class, `core/api_authz.py:161`) `class ApiKeyStore` - Persistent store for tenant-scoped API keys.
- `__init__` (method, `core/api_authz.py:170`) `def __init__(self, config)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 150
- Cross-boundary resolved imports (EXTRACTED): 147

## Connections

- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/c2_session.py imports modules/c2_agent.py.

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

- Why do 7 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- What would break if the most connected file in lazyc2/security changed?
- Should lazyc2/security be split, given cohesion 0.52?

## Sources

- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazyhttpreverseshell.py`
- `core/api_authz.py`
- `core/session_secrets.py`
- `lazyc2.py`
- `lazyc2/__init__.py`
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
- *... and 52 more*
