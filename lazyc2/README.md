# lazyc2

Supplementary C2 layer components. This directory contains security validation
helpers and supporting code used by `lazyc2.py` but kept in a separate package
to maintain a clean separation of concerns.

The primary C2 server implementation lives in the root-level `lazyc2.py`.
This directory holds code that `lazyc2.py` imports — it is not a standalone
server.

## Subdirectories

| Directory | Contents |
|-----------|---------|
| `security/` | Input validation, path safety, CORS, CSRF, HTTPS, command allowlist, HTML sanitization, trusted-proxy parsing, and shell-runner policies used by C2 routes. |

## lazyc2/security

| File | Purpose |
|------|---------|
| `validators.py` | Pure stateless validators. `validate_route_path`, `validate_template_name`, `validate_yaml_filename`, `validate_request_data`, `validate_aes_key`, `validate_password_length`, `validate_upload_size`, `validate_file_path_within_base`. Called before any `render_template`, file-serving, or secret-handling operation. |
| `services.py` | Stateful services: `SecretKeyManager` (Flask secret key), `AESKeyManager` (on-disk AES key), `SafeFileService` (path-traversal-safe I/O), `UploadSizeValidator` (content-length gate). |
| `constants.py` | Centralised constants: regex patterns, length limits, file modes, AES key size, password minimum length. |
| `cors.py` | `CorsPolicy` — origin allowlist with PROD fail-fast semantics. Replaces the legacy `cors_allowed_origins="*"`. |
| `csrf.py` | `CSRFPolicy` — per-session token issuer/validator with `is_exempt(path)` for login, logout, register, and beacon endpoints. |
| `command_allowlist.py` | `CommandAllowlist` — gates `/api/run` so only whitelisted first tokens reach the shell. Always rejects shell metacharacters and audits every decision. |
| `https_redirect.py` | `HTTPSRedirect` — returns a 301 to the same URL with `https` scheme in PROD. Used by the `@app.before_request` handler in `lazyc2.py`. |
| `trusted_proxy.py` | `TrustedProxyResolver` — parses `X-Forwarded-For` right-to-left when `c2_trusted_proxy_count > 0`. |
| `html_sanitizer.py` | `sanitize_html` — bleach-backed replacement for the legacy regex `_sanitize_html`. |

## core

| File | Purpose |
|------|---------|
| `core/safe_subprocess.py` | `SafeRunner` — default-deny shell wrapper. `run_shell` requires `allow=True` and a non-empty `reason`; both denied and allowed attempts are audited. |
| `core/config.py` | `Config` and `resolve_aes_key` — the AES key resolver. The key is exposed as `self.aes_key` (bytes) and `self.params['aes_key']` (hex string); the latter feeds lazyaddon template substitution. |

## Path safety contract

Every route that renders a user-influenced template name must call:

```python
from lazyc2.security import validate_template_name, is_safe_template_path

if not validate_template_name(name):
    return error_response("invalid template name", 400)
if not is_safe_template_path(name):
    return error_response("path traversal denied", 400)
```

This is enforced in code review. Routes that bypass these checks are
rejected.

## CSRF and CORS contract

All mutating operator routes must be decorated with `@csrf_protect` (in
addition to `@requires_auth`). The CSRF policy is the module-level
`_csrf_policy` in `lazyc2.py`; the `c2_csrf_enabled` payload key
disables it without code changes for retro-compatibility.

The `CorsPolicy` is also module-level; `socketio` and Flask-CORS share
the same allowlist. Wildcard `*` is never accepted.

## AES key contract

The framework exposes a single 32-byte AES key on `self.aes_key` and as
`self.params['aes_key']` (hex string). The same value is persisted on
disk at `sessions/key.aes` and reused across boots. Any consumer
(beacon builder, payload obfuscator, addon) should read from
`self.aes_key` rather than touching the file directly. Lazyaddons can
reference the key in their YAML with `{{aes_key}}` or `{aes_key}` and
the framework substitutes the hex value before execution.

## Source of truth for the security contract

The full security contract — invariants, test files, and wire-up
locations — lives in `docs/SECURITY_CONTRACTS.md`. Update that file
whenever one of the contracts changes.
