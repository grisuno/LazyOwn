# Subsystem: core (page 2 of 2)
Previous: [KB_core.md](KB_core.md)

## core/protocols.py
- Doc: Stable structural interfaces (PEP 544 ``Protocol``) for high-level orchestration.
- Layer: utility
- Language: py
- Symbols:
  - `Selector` (class, line 17) `class Selector(Protocol)`
  - `LLMBackend` (class, line 37) `class LLMBackend(Protocol)`
  - `MemoryStore` (class, line 51) `class MemoryStore(Protocol)`
  - `BridgeCatalog` (class, line 62) `class BridgeCatalog(Protocol)`
  - `OutcomeEvaluator` (class, line 70) `class OutcomeEvaluator(Protocol)`
  - `suggest` (method, line 27) `def suggest(self, target, phase, context)`
  - `complete` (method, line 40) `def complete(self, system, user, max_tokens, temperature)`
  - `put` (method, line 54) `def put(self, key, value)`
  - `get` (method, line 56) `def get(self, key, default)`
  - `search` (method, line 58) `def search(self, query, k)`
  - `filter` (method, line 65) `def filter(self, phase, os_id)`
  - `evaluate` (method, line 73) `def evaluate(self, command, output, target, phase)`
- Imported by: `tests/test_core.py`

## core/safe_exec.py
- Doc: Centralized safe command execution for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `CommandInjectionError` (class, line 44) `class CommandInjectionError(PermissionError)`
  - `UrlValidationError` (class, line 48) `class UrlValidationError(PermissionError)`
  - `needs_shell` (method, line 52) `def needs_shell(command)`
  - `safe_system` (method, line 69) `def safe_system(command)`
  - `safe_run_argv` (method, line 106) `def safe_run_argv(argv)`
  - `safe_run_shell` (method, line 146) `def safe_run_shell(command)`
  - `safe_clear_screen` (method, line 192) `def safe_clear_screen()`
  - `validate_url` (method, line 207) `def validate_url(url)`
  - `safe_git_clone` (method, line 234) `def safe_git_clone(repo_url, target_dir)`
  - `safe_ip_show` (method, line 268) `def safe_ip_show(interface)`
  - `safe_find_tool` (method, line 305) `def safe_find_tool(name)`
  - `safe_file_read` (method, line 321) `def safe_file_read(path)`
- Depends on: `core/logging.py`
- Imported by: `cli/banner_config.py`, `cli/commands/misc_migrated.py`, `cli/commands/pwn.py`, `cli/commands/shellsys.py`, `core/process.py`, `core/safe_subprocess.py`, `lazyc2/blueprints/api_v1.py`, `lazyown.py`, `modules/autonomous_exploit_engine.py`, `modules/conditional_hooks.py`, `modules/dns_beacon.py`, `modules/playbook_engine.py`, `modules/resource_script.py`, `tests/test_security_hardening_v4.py`, `tests/test_shell_semantics.py`

## core/safe_subprocess.py
- Doc: Safe subprocess runner for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `ShellNotAllowedError` (class, line 39) `class ShellNotAllowedError(PermissionError)`
  - `SafeRunResult` (class, line 44) `class SafeRunResult`
  - `SafeRunner` (class, line 60) `class SafeRunner`
  - `__init__` (method, line 70) `def __init__(self, audit_log_path)`
  - `run` (method, line 73) `def run(self, argv)`
  - `run_shell` (method, line 105) `def run_shell(self, command)`
  - `_audit` (method, line 176) `def _audit(self, record)`
- Depends on: `core/hardening.py`, `core/safe_exec.py`
- Imported by: `core/process.py`, `tests/test_safe_subprocess.py`, `tests/test_safe_subprocess_behavior.py`, `tests/test_security_hardening.py`, `tests/test_shell_semantics.py`, `utils.py`

## core/scheduler.py
- Doc: Centralized task scheduler for the LazyOwn framework.
- Layer: infrastructure
- Language: py
- Symbols:
  - `_TaskInfo` (class, line 41) `class _TaskInfo`
  - `TaskScheduler` (class, line 50) `class TaskScheduler`
  - `get_scheduler` (method, line 285) `def get_scheduler()`
  - `__init__` (method, line 61) `def __init__(self)`
  - `instance` (method, line 73) `def instance(cls)`
  - `start` (method, line 81) `def start(self)`
  - `stop` (method, line 100) `def stop(self)`
  - `schedule_task` (method, line 123) `def schedule_task(self, name, interval_seconds, func)`
  - `schedule_once` (method, line 157) `def schedule_once(self, name, delay_seconds, func)`
  - `cancel_task` (method, line 192) `def cancel_task(self, name)`
  - `list_tasks` (method, line 205) `def list_tasks(self)`
  - `_cancel_internal` (method, line 224) `def _cancel_internal(self, name)`
  - `_schedule_recurring_stdlib` (method, line 238) `def _schedule_recurring_stdlib(self, info)`
  - `_run_once_wrapper` (method, line 254) `def _run_once_wrapper(self, name, func)`
  - `_run_stdlib_loop` (method, line 268) `def _run_stdlib_loop(self)`
  - `_wrapper` (method, line 241) `def _wrapper()`
  - `_wrapper` (method, line 257) `def _wrapper()`
- Depends on: `core/logging.py`

## core/security.py
- Doc: Security helpers for LazyOwn — anti-debug, certificate generation.
- Layer: utility
- Language: py
- Symbols:
  - `anti_debug` (function, line 18) `def anti_debug()`
  - `generate_certificates` (function, line 58) `def generate_certificates(output_dir)`
- Depends on: `core/logging.py`

## core/text_utils.py
- Doc: Shared text helpers for terminal surfaces.
- Layer: utility
- Language: py
- Symbols:
  - `truncate_text` (function, line 10) `def truncate_text(value, max_len, marker)`
- Imported by: `cli/autosuggest.py`, `cli/graph_overlay.py`, `cli/palette_command.py`, `cli/palette_overlay.py`, `cli/reactive_hints.py`, `cli/reasoning_stream.py`, `cli/tips_engine.py`, `cli/toast_bus.py`

## core/validators.py
- Doc: Input validators for runtime configuration values.
- Layer: utility
- Language: py
- Symbols:
  - `_rejects_shell_meta` (function, line 19) `def _rejects_shell_meta(value)`
  - `_is_valid_host` (function, line 24) `def _is_valid_host(value)`
  - `_is_valid_cidr` (function, line 44) `def _is_valid_cidr(value)`
  - `check_rhost` (function, line 55) `def check_rhost(rhost)`
  - `check_lhost` (function, line 69) `def check_lhost(lhost)`
  - `check_lport` (function, line 83) `def check_lport(lport)`
  - `check_port` (function, line 93) `def check_port(port, name)`
- Depends on: `core/console.py`
- Imported by: `cli/commands/enum.py`, `cli/commands/mobile_macos.py`, `cli/commands/pwn.py`, `core/__init__.py`, `core/process.py`, `modules/c2_builder.py`, `tests/test_core.py`, `tests/test_input_fuzz.py`, `utils.py`

