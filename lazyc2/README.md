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
| `blueprints/` | Flask blueprints registered from `lazyc2.py` (auth, operations, api, addons). |
| `extensions/` | Shared helpers for blueprints: decoy response, storage, short URLs. |

## Root modules

| File | Purpose |
|------|---------|
| `addon_creator.py` | LazyAddon creator contract: `AddonCreatorConfig`, `ParamSpec`, `AddonDraft`, `AddonValidator`, `AddonYamlRenderer`, `AddonStore`, `parse_addon_form`. Single source of truth for authoring `lazyaddons/*.yaml` from the `/addons` dashboard form. |

### LazyAddon creator contract spec

The guided form exposes every addon schema option: name, description,
author, version, enabled, target OS, trigger services, category,
module type, install type, tool block (name, repo_url, install_path,
install_command, execute_command), post-exploitation extras
(upload_file, remote_command, download_file, lazycommand), environment
variables, and dynamic parameter rows (name, type, required, default,
description).

Class contracts:

| Class | Responsibility |
|-------|----------------|
| `AddonCreatorConfig` | Every regex pattern, whitelist, length limit, option list, and the payload.json placeholder set |
| `ParamSpec` / `AddonDraft` | Value objects for one param and the full form state |
| `AddonValidator` | Pure validation returning field-specific `ValidationIssue` instances |
| `AddonYamlRenderer` | Canonical document matching the CLI loader schema plus `yaml.safe_dump` |
| `AddonStore` | Path-safe, atomic persistence inside the addons directory |
| `parse_addon_form` | Adapter from `request.form` (indexed `params-<i>-*` rows) to `AddonDraft` |

Security invariants:

- New addon names pass `^[a-z][a-z0-9_]{0,63}$` so path traversal
  through the generated filename is impossible by construction.
  Lookups of pre-existing files (view and delete) use the looser
  `filename_pattern` instead, so legacy addons such as `AdaptixC2.yaml`
  or `copy-fail-CVE-2026-31431.yaml` keep working while path separators
  and traversal sequences remain rejected.
- `AddonStore` re-checks realpath containment on every read, write,
  and delete, which also rejects symlink escapes planted inside the
  addons directory.
- Writes are atomic (temp file plus `os.replace`, chmod 0644); a
  crashed request never leaves a half-written addon or `.tmp` file.
- Command placeholders must be declared params or known payload.json
  keys; double-brace `{{x}}` tokens are rejected because the CLI
  replacement engine only honours single braces.
- Mutating routes enforce the CSRF policy: `_issue_csrf` binds the
  token to a stable random client id cookie (HttpOnly) so the Flask
  session re-signing caused by flash consumption never invalidates
  it; the token travels inside the form field; invalid tokens answer
  403 JSON.
- Every route runs `decoy_response()` like the rest of the dashboard.
- The list page links the view and delete actions by file stem
  (`filename`) rather than the YAML-declared name, because 15 shipped
  addons declare a name that differs from their filename.

Routes:

| Endpoint | Method | Behaviour |
|----------|--------|-----------|
| `/addons` | GET | List page; issues the CSRF cookie and token |
| `/addons/create` | GET/POST | Form; POST validates, saves atomically, redirects to the preview |
| `/addons/<name>/view` | GET | Canonical YAML preview |
| `/addons/<name>/delete` | POST | CSRF-protected delete |

Definition of Done gate:

1. `pytest tests/test_addon_creator.py` green (71 tests).
2. `python3 tests/run_mutation_addon_creator.py` reports
   `10 killed, 0 survived`.
3. `ruff check lazyc2/addon_creator.py lazyc2/blueprints/addons.py
   tests/test_addon_creator.py` clean under the repo ruff rules.

Wiring and boy scout notes:

- Registered in the `lazyc2.py` blueprint try block; the addons
  directory is exposed via `app.config["LAZYOWN_ADDONS_DIR"]` and the
  decoy `lhost` default via `app.config.setdefault("lhost", lhost)`.
- Nav entry in `templates/base.html` next to Tools.
- Fixed broken JavaScript in `templates/create_tool.html` while
  building this contract: undefined variables (`triggerSelect`,
  `customTriggerInput`, `description`), a malformed
  `"microsoft-ds"endif %}` option tag, a fetch that duplicated the
  form submission, and console spam. The event-config creation flow
  the page intended is preserved and now actually runs.

## lazyc2/blueprints

| File | Purpose |
|------|---------|
| `addons.py` | LazyAddon lifecycle under `/addons`: list, guided create form, YAML preview, delete. All mutating routes enforce the per-session CSRF token issued on the form page (`_issue_csrf` binds the token to a stable client id cookie so flash-message session re-signing never invalidates it). |
| `auth.py` | Login, logout, registration, MFA, profile, and admin user/tenant management. |
| `operations.py` | Tasks, CVEs, notes, and event management CRUD. |
| `api.py` | API and health-check endpoints. |
| `phishing.py` | Redirect blueprint for phishing campaigns. |

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
