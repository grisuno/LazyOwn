# Subsystem: security

## lazyc2/security/__init__.py
- Layer: utility
- Language: py
- Imported by: `mutants/tests/test_security_lazyc2.py`, `tests/test_security_lazyc2.py`

## lazyc2/security/command_allowlist.py
- Layer: utility
- Language: py
- Symbols:
  - `CommandRejectionReason` (class, line 36) `class CommandRejectionReason(StrEnum)`
  - `CommandDecision` (class, line 48) `class CommandDecision`
  - `CommandAllowlist` (class, line 70) `class CommandAllowlist`
  - `to_dict` (method, line 61) `def to_dict(self)`
  - `__init__` (method, line 82) `def __init__(self, allowed, audit_log_path)`
  - `allowed` (method, line 94) `def allowed(self)`
  - `check` (method, line 98) `def check(self, command)`
  - `_audit` (method, line 126) `def _audit(self, decision, command)`
- Depends on: `cli/commands/enum.py`
- Imported by: `lazyc2.py`, `mutants/tests/test_command_allowlist.py`, `mutants/tests/test_command_allowlist_behavior.py`, `tests/test_command_allowlist.py`, `tests/test_command_allowlist_behavior.py`

## lazyc2/security/constants.py
- Layer: utility
- Language: py
- Imported by: `lazyc2.py`, `lazyc2/security/html_sanitizer.py`, `lazyc2/security/services.py`, `lazyc2/security/validators.py`

## lazyc2/security/cors.py
- Layer: utility
- Language: py
- Symbols:
  - `CorsConfigError` (class, line 46) `class CorsConfigError(ValueError)`
  - `CorsPolicy` (class, line 50) `class CorsPolicy`
  - `_origin_matches` (method, line 199) `def _origin_matches(allowed, candidate)`
  - `_scheme_of` (method, line 223) `def _scheme_of(origin)`
  - `_host_of` (method, line 230) `def _host_of(origin)`
  - `__init__` (method, line 70) `def __init__(self, env, lhost, allowed_origins, c2_port, extra_socketio_ports)`
  - `env` (method, line 85) `def env(self)`
  - `resolve_origins` (method, line 89) `def resolve_origins(self)`
  - `origins_for_socketio` (method, line 110) `def origins_for_socketio(self)`
  - `is_allowed` (method, line 136) `def is_allowed(self, origin)`
  - `_socketio_ports` (method, line 157) `def _socketio_ports(self)`
  - `_collect_candidates` (method, line 166) `def _collect_candidates(self)`
  - `_clean` (method, line 175) `def _clean(candidates)`
  - `_dev_fallback_origins` (method, line 185) `def _dev_fallback_origins(self)`
  - `_dev_fallback` (method, line 195) `def _dev_fallback(self)`
- Imported by: `lazyc2.py`, `mutants/tests/test_cors_behavior.py`, `mutants/tests/test_cors_policy.py`, `mutants/tests/test_cors_socketio_regression.py`, `tests/test_cors_behavior.py`, `tests/test_cors_policy.py`, `tests/test_cors_socketio_regression.py`

## lazyc2/security/csrf.py
- Layer: utility
- Language: py
- Symbols:
  - `CSRFPolicy` (class, line 48) `class CSRFPolicy`
  - `__init__` (method, line 69) `def __init__(self, header, form_field, cookie_name, exempt_paths, secret)`
  - `header` (method, line 85) `def header(self)`
  - `cookie_name` (method, line 90) `def cookie_name(self)`
  - `issue` (method, line 94) `def issue(self, session_id)`
  - `rotate` (method, line 111) `def rotate(self, session_id)`
  - `forget` (method, line 126) `def forget(self, session_id)`
  - `validate` (method, line 130) `def validate(self, session_id, candidate)`
  - `is_exempt` (method, line 147) `def is_exempt(self, path)`
  - `extract_token` (method, line 163) `def extract_token(self, request)`
  - `check_request` (method, line 182) `def check_request(self, session_id, request)`
- Imported by: `lazyc2.py`, `lazyc2/blueprints/addons.py`, `mutants/tests/test_csrf_behavior.py`, `mutants/tests/test_csrf_policy.py`, `tests/test_csrf_behavior.py`, `tests/test_csrf_policy.py`

## lazyc2/security/html_sanitizer.py
- Layer: utility
- Language: py
- Symbols:
  - `_strip_dangerous_blocks` (function, line 62) `def _strip_dangerous_blocks(raw_html)`
  - `sanitize_html` (function, line 78) `def sanitize_html(raw_html, allowed_tags, allowed_attributes)`
- Depends on: `lazyc2/security/constants.py`
- Imported by: `lazyc2.py`, `mutants/tests/test_html_sanitizer.py`, `tests/test_html_sanitizer.py`

## lazyc2/security/https_redirect.py
- Layer: presentation
- Language: py
- Symbols:
  - `RedirectResponse` (class, line 29) `class RedirectResponse`
  - `HTTPSRedirect` (class, line 41) `class HTTPSRedirect`
  - `__init__` (method, line 51) `def __init__(self, env, enabled)`
  - `enabled` (method, line 56) `def enabled(self)`
  - `evaluate` (method, line 60) `def evaluate(self, request)`
- Imported by: `lazyc2.py`, `mutants/tests/test_https_redirect.py`, `tests/test_https_redirect.py`

## lazyc2/security/services.py
- Layer: business_logic
- Language: py
- Symbols:
  - `SecretKeyManager` (class, line 19) `class SecretKeyManager`
  - `SafeFileService` (class, line 56) `class SafeFileService`
  - `AESKeyManager` (class, line 152) `class AESKeyManager`
  - `UploadSizeValidator` (class, line 183) `class UploadSizeValidator`
  - `__init__` (method, line 30) `def __init__(self, sessions_dir)`
  - `get_or_create` (method, line 33) `def get_or_create(self)`
  - `__init__` (method, line 63) `def __init__(self, base_dir)`
  - `_resolve_safe` (method, line 68) `def _resolve_safe(self, relative_path)`
  - `read_bytes` (method, line 86) `def read_bytes(self, relative_path)`
  - `read_text` (method, line 102) `def read_text(self, relative_path, encoding)`
  - `write_bytes` (method, line 119) `def write_bytes(self, relative_path, data)`
  - `exists` (method, line 136) `def exists(self, relative_path)`
  - `__init__` (method, line 158) `def __init__(self, key_file)`
  - `get_or_generate` (method, line 161) `def get_or_generate(self)`
  - `__init__` (method, line 189) `def __init__(self, max_size_bytes)`
  - `validate` (method, line 192) `def validate(self, content_length)`
- Depends on: `lazyc2/security/constants.py`, `lazyc2/security/validators.py`
- Imported by: `lazyc2.py`, `lazyc2.py`, `lazyc2.py`, `lazyc2/app_factory.py`, `mutants/tests/test_security_lazyc2.py`, `tests/test_security_lazyc2.py`

## lazyc2/security/trusted_proxy.py
- Layer: utility
- Language: py
- Symbols:
  - `TrustedProxyResolver` (class, line 30) `class TrustedProxyResolver`
  - `__init__` (method, line 42) `def __init__(self, trusted_count, operator_allowlist)`
  - `trusted_count` (method, line 53) `def trusted_count(self)`
  - `client_ip` (method, line 57) `def client_ip(self, remote_addr, x_forwarded_for)`
  - `is_operator` (method, line 80) `def is_operator(self, ip)`
- Imported by: `lazyc2.py`, `mutants/tests/test_trusted_proxy.py`, `tests/test_trusted_proxy.py`

## lazyc2/security/validators.py
- Layer: utility
- Language: py
- Symbols:
  - `validate_route_path` (function, line 23) `def validate_route_path(route_path)`
  - `validate_template_name` (function, line 45) `def validate_template_name(template_name)`
  - `validate_yaml_filename` (function, line 67) `def validate_yaml_filename(filename)`
  - `validate_request_data` (function, line 85) `def validate_request_data(data)`
  - `validate_aes_key` (function, line 101) `def validate_aes_key(key)`
  - `validate_password_length` (function, line 117) `def validate_password_length(password)`
  - `validate_upload_size` (function, line 133) `def validate_upload_size(content_length)`
  - `validate_file_path_within_base` (function, line 149) `def validate_file_path_within_base(file_path, base_dir)`
- Depends on: `lazyc2/security/constants.py`
- Imported by: `lazyc2.py`, `lazyc2.py`, `lazyc2.py`, `lazyc2.py`, `lazyc2/security/services.py`, `mutants/tests/test_security_lazyc2.py`, `tests/test_security_lazyc2.py`
