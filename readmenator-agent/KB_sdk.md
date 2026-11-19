# Subsystem: sdk

## sdk/__init__.py
- Doc: The LazyOwn programmatic SDK.
- Language: py
- Depends on: `sdk/errors.py`, `sdk/facade.py`
- Imported by: `skills/mcp_tools/get_config.py`, `skills/mcp_tools/read_session_file.py`, `skills/mcp_tools/set_config.py`, `tests/test_sdk_facade.py`

## sdk/errors.py
- Doc: Typed errors for the LazyOwn programmatic SDK.
- Language: py
- Symbols:
  - `SdkError` (class, line 13) `class SdkError(Exception)`
  - `ScopeBlocked` (class, line 17) `class ScopeBlocked(PermissionError, SdkError)`
  - `ConfigValidationError` (class, line 27) `class ConfigValidationError(ValueError, SdkError)`
  - `SessionPathError` (class, line 31) `class SessionPathError(PermissionError, SdkError)`
- Imported by: `sdk/__init__.py`, `sdk/facade.py`, `sdk/lazymode/runner.py`, `tests/test_lazymode_runner.py`

## sdk/facade.py
- Doc: The LazyOwn programmatic facade (``Lazy``).
- Language: py
- Symbols:
  - `_safe_session_name` (function, line 51) `def _safe_session_name(name, sessions_dir)`
  - `ConfigApi` (class, line 89) `class ConfigApi`
  - `SessionsApi` (class, line 145) `class SessionsApi`
  - `ReconApi` (class, line 198) `class ReconApi`
  - `Lazy` (class, line 270) `class Lazy`
  - `__init__` (method, line 97) `def __init__(self, payload_path)`
  - `all` (method, line 105) `def all(self)`
  - `get` (method, line 109) `def get(self, key, default)`
  - `set` (method, line 121) `def set(self, key, value)`
  - `__init__` (method, line 148) `def __init__(self, sessions_dir)`
  - `list` (method, line 156) `def list(self, pattern)`
  - `path` (method, line 169) `def path(self, name)`
  - `read` (method, line 180) `def read(self, name, max_bytes)`
  - `__init__` (method, line 201) `def __init__(self, sessions_dir, run, scope_check)`
  - `nmap` (method, line 218) `def nmap(self, target, flags, timeout)`
  - `ports` (method, line 250) `def ports(self, target)`
  - `__init__` (method, line 279) `def __init__(self, payload_path, sessions_dir, scope_check, command_runner)`
  - `sh` (method, line 304) `def sh(self, command, timeout)`
  - `search_exploits` (method, line 321) `def search_exploits(self, query, timeout)`
- Depends on: `core/config.py`, `core/payload_schema.py`, `core/process.py`, `modules/nmap_fingerprint.py`, `modules/scan_brief.py`, `sdk/errors.py`
- Imported by: `sdk/__init__.py`, `sdk/lazymode/_bootstrap.py`, `sdk/lazymode/index.py`, `sdk/lazymode/runner.py`
