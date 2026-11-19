# Subsystem: lazymode

## sdk/lazymode/__init__.py
- Doc: lazymode: programmatic (code-mode) execution over the LazyOwn SDK.
- Language: py
- Depends on: `sdk/lazymode/index.py`, `sdk/lazymode/runner.py`
- Imported by: `modules/lazymode_playbook.py`, `skills/mcp_tools/lazymode_exec.py`, `skills/mcp_tools/lazymode_search.py`, `tests/test_lazymode_runner.py`

## sdk/lazymode/_bootstrap.py
- Doc: Subprocess entry point that runs one lazymode Python script.
- Language: py
- Symbols:
  - `_bounded` (function, line 30) `def _bounded(text)`
  - `_jsonable` (function, line 50) `def _jsonable(value)`
  - `_emit` (function, line 66) `def _emit(envelope)`
  - `main` (function, line 77) `def main(argv)`
- Depends on: `core/config.py`, `sdk/facade.py`, `sdk/lazymode/runner.py`
- Imported by: `sdk/lazymode/runner.py`

## sdk/lazymode/index.py
- Doc: Discoverable index of the lazymode SDK surface.
- Language: py
- Symbols:
  - `_entry` (function, line 21) `def _entry(path, member)`
  - `build_index` (function, line 40) `def build_index()`
  - `search` (function, line 66) `def search(query, limit)`
  - `score` (function, line 82) `def score(entry)`
- Depends on: `sdk/facade.py`
- Imported by: `sdk/lazymode/__init__.py`

## sdk/lazymode/runner.py
- Doc: The lazymode code runners (hybrid: Python subprocess + Lua in-process).
- Language: py
- Symbols:
  - `_bounded` (function, line 51) `def _bounded(text)`
  - `LazymodeResult` (class, line 69) `class LazymodeResult`
  - `build_scope_check` (function, line 93) `def build_scope_check(payload)`
  - `_cpu_seconds_for` (function, line 123) `def _cpu_seconds_for(timeout)`
  - `_set_limits` (function, line 140) `def _set_limits(cpu_seconds)`
  - `_parse_envelope` (function, line 161) `def _parse_envelope(stdout)`
  - `run_python` (function, line 180) `def run_python(script)`
  - `run_lua` (function, line 251) `def run_lua(script)`
  - `run` (function, line 300) `def run(script, lang)`
  - `to_dict` (method, line 88) `def to_dict(self)`
  - `_check` (function, line 115) `def _check(command, target)`
- Depends on: `cli/scope_guard.py`, `core/config.py`, `core/dependencies.py`, `sdk/errors.py`, `sdk/facade.py`, `sdk/lazymode/_bootstrap.py`
- Imported by: `sdk/lazymode/__init__.py`, `sdk/lazymode/_bootstrap.py`, `tests/test_lazymode_runner.py`
