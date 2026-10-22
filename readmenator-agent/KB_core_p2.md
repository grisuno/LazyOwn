# Subsystem: core (page 2 of 2)
Previous: [KB_core.md](KB_core.md)

## core/process.py
- Doc: Process and subprocess utilities for the LazyOwn framework.
- Layer: business_logic
- Language: py
- Symbols:
  - `check_go_tool_installed` (function, line 34) `def check_go_tool_installed(tool_name)`
  - `is_binary_present` (function, line 54) `def is_binary_present(binary_name)`
  - `handle_multiple_rhosts` (function, line 68) `def handle_multiple_rhosts(func)`
  - `check_sudo` (function, line 97) `def check_sudo()`
  - `run` (function, line 108) `def run(command)`
  - `is_package_installed` (function, line 143) `def is_package_installed(package_name)`
  - `_print_run_command_status` (function, line 159) `def _print_run_command_status(command, elapsed, exit_code)`
  - `run_command` (function, line 183) `def run_command(command, timeout)`
  - `ensure_tmux_session` (function, line 253) `def ensure_tmux_session(session_name)`
  - `activate_server` (function, line 271) `def activate_server(httpd, url, lhost)`
  - `wrapper` (function, line 82) `def wrapper(self)`
  - `_drain_stderr` (function, line 220) `def _drain_stderr()`
- Depends on: `core/console.py`, `core/hardening.py`, `core/safe_exec.py`, `core/safe_subprocess.py`, `core/validators.py`
- Imported by: `cli/commands/lazyops.py`, `cli/commands/misc_migrated.py`, `cli/commands/mobile_macos.py`, `core/__init__.py`, `modules/auto_purple.py`, `modules/lazy_loop.py`, `static/js/particles.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_lazy_runner.py`, `tests/test_shell_semantics.py`, `utils.py`

## core/profiles.py
- Doc: Runtime profiles: ``light`` vs ``full`` installations.
- Layer: utility
- Language: py
- Symbols:
  - `active_profile` (function, line 40) `def active_profile()`
  - `is_light` (function, line 59) `def is_light()`
  - `specs_for_profile` (function, line 64) `def specs_for_profile(specs)`
- Imported by: `cli/doctor.py`, `cli/wizard.py`, `tests/test_profiles.py`

## core/prompt.py
- Doc: Prompt builder for LazyOwn CLI and C2 dashboard banner.
- Layer: utility
- Language: py
- Symbols:
  - `_load_prompt_payload` (function, line 17) `def _load_prompt_payload()`
  - `get_git_info` (function, line 35) `def get_git_info()`
  - `get_venv_info` (function, line 60) `def get_venv_info()`
  - `get_kernel` (function, line 68) `def get_kernel()`
  - `get_terminal_size` (function, line 78) `def get_terminal_size()`
  - `get_local_ips` (function, line 87) `def get_local_ips()`
  - `copy2clip` (function, line 109) `def copy2clip(text)`
  - `getprompt` (function, line 127) `def getprompt()`
- Depends on: `core/config.py`
- Imported by: `contrib/legacy/lazybinenc.py`, `key.py`, `static/js/quill-2.0.3.js`

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

## core/reverse_shell_secret.py
- Doc: Reverse-shell fallback secret — sealed persistence contract.
- Layer: utility
- Language: py
- Symbols:
  - `seal_reverse_shell_password` (function, line 24) `def seal_reverse_shell_password(plaintext)`
  - `load_reverse_shell_password` (function, line 41) `def load_reverse_shell_password(secret_path)`
  - `generate_reverse_shell_password` (function, line 65) `def generate_reverse_shell_password()`
  - `is_configured_password_valid` (function, line 74) `def is_configured_password_valid(candidate, minimum_length)`
- Depends on: `core/hardening.py`
- Imported by: `lazyc2.py`, `tests/test_security_alerts_fix.py`

## core/safe_console.py
- Doc: Terminal-safe Rich console factory.
- Layer: utility
- Language: py
- Symbols:
  - `supports_unicode` (function, line 33) `def supports_unicode()`
  - `get_console` (function, line 42) `def get_console()`
  - `panel_box` (function, line 52) `def panel_box()`
  - `milestone_glyph` (function, line 57) `def milestone_glyph(state)`
  - `progress_bar` (function, line 67) `def progress_bar(ratio, width)`
- Depends on: `core/console.py`
- Imported by: `cli/autosuggest.py`, `cli/ops_commands.py`, `cli/tips_engine.py`, `modules/loop_progress.py`, `tests/test_safe_console.py`

## core/safe_exec.py
- Doc: Centralized safe command execution for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `CommandInjectionError` (class, line 44) `class CommandInjectionError(PermissionError)`
  - `UrlValidationError` (class, line 48) `class UrlValidationError(PermissionError)`
  - `needs_shell` (function, line 52) `def needs_shell(command)`
  - `safe_system` (function, line 69) `def safe_system(command)`
  - `safe_run_argv` (function, line 106) `def safe_run_argv(argv)`
  - `safe_run_shell` (function, line 146) `def safe_run_shell(command)`
  - `safe_clear_screen` (function, line 192) `def safe_clear_screen()`
  - `validate_url` (function, line 207) `def validate_url(url)`
  - `safe_git_clone` (function, line 234) `def safe_git_clone(repo_url, target_dir)`
  - `safe_ip_show` (function, line 268) `def safe_ip_show(interface)`
  - `safe_find_tool` (function, line 305) `def safe_find_tool(name)`
  - `safe_file_read` (function, line 321) `def safe_file_read(path)`
- Depends on: `core/logging.py`
- Imported by: `cli/banner_config.py`, `cli/commands/misc_migrated.py`, `cli/commands/pwn.py`, `cli/commands/shellsys.py`, `core/process.py`, `core/safe_subprocess.py`, `lazyc2/blueprints/api_v1.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/autonomous_exploit_engine.py`, `modules/chain_runner.py`, `modules/command_executor.py`, `modules/conditional_hooks.py`, `modules/dns_beacon.py`, `modules/metasploitable_migrations.py`, `modules/playbook_engine.py`, `modules/resource_script.py`, `modules/ttpscope_bridge.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_executor_kernel.py`, `tests/test_security_hardening_v4.py`, `tests/test_shell_semantics.py`

## core/safe_import.py
- Doc: Fail-closed import of attacker-supplied campaign packages.
- Layer: utility
- Language: py
- Symbols:
  - `is_safe_identifier` (function, line 20) `def is_safe_identifier(name)`
  - `filter_columns` (function, line 32) `def filter_columns(src_columns, dest_columns)`
  - `safe_extract_zip` (function, line 51) `def safe_extract_zip(archive, dest)`
  - `safe_copy_tree` (function, line 93) `def safe_copy_tree(src, dest)`
- Imported by: `cli/commands/campaign.py`, `tests/test_campaign_import_safety.py`

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
  - `get_scheduler` (function, line 285) `def get_scheduler()`
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
  - `_wrapper` (function, line 241) `def _wrapper()`
  - `_wrapper` (function, line 257) `def _wrapper()`
- Depends on: `core/logging.py`

## core/security.py
- Doc: Security helpers for LazyOwn — anti-debug, certificate generation.
- Layer: utility
- Language: py
- Symbols:
  - `anti_debug` (function, line 18) `def anti_debug()`
  - `generate_certificates` (function, line 58) `def generate_certificates(output_dir)`
- Depends on: `core/logging.py`

## core/terminal_guard.py
- Doc: Terminal state guard for interactive automation.
- Layer: utility
- Language: py
- Symbols:
  - `_tty_fd` (function, line 30) `def _tty_fd()`
  - `emit_restore_sequences` (function, line 41) `def emit_restore_sequences()`
  - `apply_stty_sane` (function, line 62) `def apply_stty_sane()`
  - `TerminalGuard` (class, line 73) `class TerminalGuard`
  - `__init__` (method, line 85) `def __init__(self)`
  - `__enter__` (method, line 91) `def __enter__(self)`
  - `__exit__` (method, line 104) `def __exit__(self)`
  - `restore` (method, line 108) `def restore(self)`
- Imported by: `modules/lazy_runner.py`, `tests/test_lazy_runner.py`

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
  - `check_rhost` (function, line 26) `def check_rhost(rhost)`
  - `check_lhost` (function, line 40) `def check_lhost(lhost)`
  - `check_lport` (function, line 54) `def check_lport(lport)`
  - `check_port` (function, line 64) `def check_port(port, name)`
  - `require_rhost` (function, line 77) `def require_rhost(params)`
  - `require_lhost` (function, line 94) `def require_lhost(params)`
  - `require_lport` (function, line 107) `def require_lport(params)`
  - `require_rport` (function, line 120) `def require_rport(params)`
- Depends on: `core/console.py`, `core/host_policy.py`
- Imported by: `cli/commands/_base.py`, `cli/commands/enum.py`, `cli/commands/mobile_macos.py`, `cli/commands/pwn.py`, `core/__init__.py`, `core/process.py`, `modules/c2_builder.py`, `tests/test_core.py`, `tests/test_host_policy.py`, `tests/test_input_fuzz.py`, `tests/test_require_guards.py`, `utils.py`

