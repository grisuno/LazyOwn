# Subsystem: modules_tools

## modules/tools/__init__.py
- Doc: Reusable development tools for the LazyOwn autonomous loop.
- Layer: utility
- Language: py
- Imported by: `tests/test_lazy_runner.py`

## modules/tools/loop_smoke.py
- Doc: End-to-end smoke of the shared loop runner (no LLM, no network).
- Layer: utility
- Language: py
- Symbols:
  - `FakeShell` (class, line 22) `class FakeShell`
  - `FakeEngine` (class, line 31) `class FakeEngine`
  - `run` (function, line 77) `def run()`
  - `main` (function, line 114) `def main()`
  - `onecmd_plus_hooks` (method, line 25) `def onecmd_plus_hooks(self, command)`
  - `__init__` (method, line 36) `def __init__(self)`
  - `bind_shell` (method, line 44) `def bind_shell(self, shell)`
  - `set_concurrency` (method, line 48) `def set_concurrency(self, value)`
  - `create_task` (method, line 52) `def create_task(self, goal, description)`
  - `orchestrate` (method, line 56) `def orchestrate(self)`
- Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`

## modules/tools/monitor_smoke.py
- Doc: Headless smoke of the Textual worker monitor (``lazy_view``).
- Layer: utility
- Language: py
- Symbols:
  - `run` (function, line 20) `def run()`
  - `main` (function, line 59) `def main()`
  - `_drive` (function, line 40) `def _drive()`
- Depends on: `cli/lazy_monitor.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`
