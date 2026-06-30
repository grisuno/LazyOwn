# LazyOwn Security Contracts

This document is the single source of truth for every security contract
implemented by the LazyOwn framework. Each section describes one contract:
its invariant, the file that owns it, the configuration keys it consumes,
and the tests that prove it.

Every contract follows the SDD + TDD + BDD methodology: the spec is
written in the module docstring first, the failing tests are written
next, and only then does the implementation land. Boy-scout mode is
on by default: any tech debt or security issue encountered while
implementing one of these contracts is fixed in the same change.

## Compat strategy

PROD fail-fast: when ``env == "PROD"`` and a required C2 key is missing
or invalid, the framework refuses to start the affected service.

DEV warn-and-default: when ``env != "PROD"`` missing keys print a clear
warning and a documented default is used so existing engagements keep
working.

AES key: lives in ``payload.json`` as ``aes_key`` (64 hex chars, 32
bytes). The resolved value is available as ``self.aes_key`` (bytes) and
``self.params['aes_key']`` (hex string) on every consumer. Lazyaddon
templates may use ``{{aes_key}}`` and ``{aes_key}`` for substitution.

## Contract index

| # | Module | Purpose | Test file | Config keys |
|---|--------|---------|-----------|-------------|
| 1 | `lazyc2/security/cors.py` | Origin allowlist for Socket.IO and HTTP | `tests/test_cors_policy.py`, `tests/test_cors_behavior.py` | `env`, `lhost`, `c2_allowed_origins` |
| 2 | `lazyc2/security/csrf.py` | Per-session CSRF token gate | `tests/test_csrf_policy.py`, `tests/test_csrf_behavior.py` | `c2_csrf_enabled`, `c2_csrf_exempt_paths` |
| 3 | `lazyc2/security/command_allowlist.py` | `/api/run` verb allowlist + audit | `tests/test_command_allowlist.py`, `tests/test_command_allowlist_behavior.py` | `c2_api_command_allowlist` |
| 4 | `lazyc2/security/https_redirect.py` | HTTP -> HTTPS redirect in PROD | `tests/test_https_redirect.py` | `env`, `c2_https_redirect` |
| 5 | `lazyc2/security/trusted_proxy.py` | `X-Forwarded-For` parser with operator allowlist | `tests/test_trusted_proxy.py` | `c2_trusted_proxy_count`, `c2_operator_ip_allowlist` |
| 6 | `lazyc2/security/html_sanitizer.py` | bleach-backed HTML cleaner | `tests/test_html_sanitizer.py` | n/a (constants in `lazyc2/security/constants.py`) |
| 7 | `core/safe_subprocess.py` | Default-deny shell runner | `tests/test_safe_subprocess.py`, `tests/test_safe_subprocess_behavior.py` | n/a |
| 8 | `core/config.py` (`resolve_aes_key`) | AES key resolver from payload / disk / random | `tests/test_aes_key_propagation.py` | `aes_key` |

Plus pre-existing contracts from the first security pass:

| # | Module | Purpose | Test file | Config keys |
|---|--------|---------|-----------|-------------|
| 9 | `lazyc2/security/services.py::SecretKeyManager` | Flask secret key persistence | `tests/test_security_lazyc2.py` | `LAZYOWN_SECRET_KEY` env |
| 10 | `lazyc2/security/services.py::SafeFileService` | Path-traversal-safe file I/O | `tests/test_security_lazyc2.py` | n/a |
| 11 | `lazyc2/security/services.py::AESKeyManager` | On-disk AES key generator | `tests/test_security_lazyc2.py` | n/a |
| 12 | `lazyc2/security/validators.py` | Pure validators (route, template, yaml, AES, password) | `tests/test_security_lazyc2.py` | n/a |

## Contract 1: CORS origin allowlist

**File:** `lazyc2/security/cors.py`
**Owns:** `CorsPolicy`
**Invariants:**

1. The wildcard `*` is never returned. CSV inputs drop `*` tokens.
2. `env == "PROD"` with empty allowlist raises `CorsConfigError`.
3. `env != "PROD"` with empty allowlist falls back to
   `http://{lhost}` + `https://{lhost}` (plus a `localhost` alias when
   the lhost is `127.0.0.1`).
4. `is_allowed(origin)` matches scheme + hostname (port-insensitive).
5. `origins_for_socketio()` returns the allowlist expanded with the
   configured `c2_port` and the common C2 ports (443, 5000, 5001, 8000,
   8080, 8443, 8888, 9000) so flask-socketio's exact-match check on the
   `Origin` header passes for the xterm.js terminal, beacon clients, and
   operator browser. This is what kept the websocket upgrade from being
   rejected with HTTP 400 after the wildcard was removed.

**Wire-up:** `lazyc2.py:2174` `socketio = SocketIO(..., cors_allowed_origins=_cors_policy.origins_for_socketio(), ...)`.

## Contract 2: CSRF token gate

**File:** `lazyc2/security/csrf.py`
**Owns:** `CSRFPolicy`, `csrf_protect` decorator in `lazyc2.py`
**Invariants:**

1. `issue(session_id)` returns a 32-byte URL-safe token, stable per session.
2. `validate(session_id, token)` is constant-time (`hmac.compare_digest`).
3. `is_exempt(path)` returns `True` for `/login`, `/logout`, `/register`,
   `/api/beacon/*`.
4. Safe methods (`GET`, `HEAD`, `OPTIONS`, `TRACE`) bypass the check.

**Wire-up:** `lazyc2.py:csrf_protect` applied to `/issue_command` and
`/api/run` mutating routes. Set `c2_csrf_enabled=false` in
`payload.json` to disable without code changes.

## Contract 3: Command allowlist (`/api/run`)

**File:** `lazyc2/security/command_allowlist.py`
**Owns:** `CommandAllowlist`, `CommandDecision`, `CommandRejectionReason`
**Invariants:**

1. First whitespace-delimited token is matched case-insensitively.
2. Shell metacharacters (`;`, `|`, `&`, `$`, `>`, `<`, backtick,
   newline, carriage return, backslash) are always rejected.
3. Empty / non-string input is rejected with reason `EMPTY`.
4. Every decision (allowed or denied) is appended to
   `sessions/api_command_audit.jsonl` as one JSON line.

**Wire-up:** `lazyc2.py:run_command` calls `_command_allowlist.check(command)`
before `shell.one_cmd`.

## Contract 4: HTTPS redirect

**File:** `lazyc2/security/https_redirect.py`
**Owns:** `HTTPSRedirect`, `RedirectResponse`
**Invariants:**

1. `is_secure=True` request always passes through.
2. `is_secure=False` + `env="PROD"` + `enabled=True` returns a 301
   redirect to the same URL with the scheme replaced by `https`.
3. Path, query string, and host header are preserved.

**Wire-up:** `lazyc2.py:_enforce_https_redirect` registered as
`@app.before_request` after `_metrics_before_request`.

## Contract 5: Trusted proxy resolver

**File:** `lazyc2/security/trusted_proxy.py`
**Owns:** `TrustedProxyResolver`
**Invariants:**

1. `trusted_count == 0` ignores `X-Forwarded-For` entirely.
2. `trusted_count > 0` parses right-to-left, skipping `trusted_count`
   hops, and returns the leftmost untrusted address.
3. `is_operator(ip)` does an exact-string comparison.

**Wire-up:** `_trusted_proxy_resolver` exposed as a module-level object
in `lazyc2.py` for the `decoy()` and operator-only route gates.

## Contract 6: HTML sanitizer

**File:** `lazyc2/security/html_sanitizer.py`
**Owns:** `sanitize_html`
**Invariants:**

1. `<script>`, `<iframe>`, `<object>`, `<embed>`, `<style>`, `<svg>`,
   `<math>`, `<form>`, `<input>`, `<button>`, `<textarea>`, `<select>`
   are removed entirely (tag + content).
2. `on*=` event handlers are stripped.
3. `javascript:` URIs in `href` and `src` are removed.
4. HTML comments are stripped.
5. Benign tags (`p`, `strong`, `em`, `ul`, `ol`, `li`, `a`, `code`,
   `pre`, `h1`..`h6`, `blockquote`) survive untouched.

**Wire-up:** `lazyc2.py:_sanitize_html` now delegates to
`lazyc2_sanitize_html`, which is the bleach-backed implementation.

## Contract 7: Safe subprocess runner

**File:** `core/safe_subprocess.py`
**Owns:** `SafeRunner`, `SafeRunResult`, `ShellNotAllowedError`
**Invariants:**

1. `run_shell(cmd, allow=False)` raises `ShellNotAllowedError`.
2. `run_shell(cmd, allow=True, reason="...")` requires a non-empty
   `reason`; an empty `reason` raises `ValueError`.
3. `run(argv)` is always allowed and never audits.
4. Every `run_shell` call is appended to the audit log (one JSON line)
   whether allowed or denied.

**Wire-up:** `utils.py:run` now delegates to `SafeRunner.run_shell`
with an explicit reason so existing CLI commands keep working.

## Contract 8: AES key resolution and propagation

**File:** `core/config.py` (`resolve_aes_key`, `Config`)
**Owns:** `self.aes_key` (bytes), `self.params['aes_key']` (hex string)
**Invariants:**

1. A 64-char hex `aes_key` in the payload decodes to 32 bytes.
2. An on-disk `sessions/key.aes` is loaded when the payload is empty.
3. Otherwise `os.urandom(32)` is generated and persisted with mode
   `0o600`.
4. Lazyaddon templates can use `{{aes_key}}` and `{aes_key}` for
   substitution; the existing addon substitution iterates over the
   whole payload so the key flows automatically.

**Wire-up:** `lazyaddons/beacon.yaml` now exports
`LAZYOWN_AES_KEY={{aes_key}}` so the Go beacon stub can use the same
key as the C2.

## Wire-up summary (boy-scout changes inside `lazyc2.py`)

- Replaced `cors_allowed_origins="*"` with `_cors_policy.origins_for_socketio()`.
- Replaced `ENV = "PROD"` with `ENV = _env_tag()`.
- Added `app.config['MAX_CONTENT_LENGTH']` driven by `c2_max_upload_size_mb`.
- Added `@app.before_request _enforce_https_redirect` for HTTPS upgrade.
- Replaced `_sanitize_html` regex with bleach-backed
  `lazyc2.security.html_sanitizer.sanitize_html`.
- Replaced the `/download` path resolution with `SafeFileService`.
- Replaced the hardcoded `reverse_shell_password = "..."` fallback in
  `/lazyos` with a payload-driven resolver that warns on legacy use.
- Gated `/api/run` with `CommandAllowlist` and `/issue_command`,
  `/api/run` with `@csrf_protect`.
- Replaced `/register` rate limit with `c2_register_limit` (was
  sharing `c2_login_limit`).
- Imported the new policy objects at module top of `lazyc2.py`.
