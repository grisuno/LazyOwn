# API (page 7 of 26)
Previous: [API_p6.md](API_p6.md)

## core/param_registry.py
Depends on: `core/logging.py`, `core/payload_schema.py`
Imported by: `cli/commands/params_ops.py`, `cli/lazy_orchestrator.py`, `core/payload_schema.py`, `lazyc2/addon_creator.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_orchestrator.py`, `tests/test_param_registry.py`, `tests/test_php2shell_addon.py`
- `OperatorParam.as_entry` (method) `core/param_registry.py:133` `def as_entry(self)` -- Return the YAML mapping stored in ``params/operator.yaml``.
- `OperatorParam.to_spec` (method) `core/param_registry.py:142` `def to_spec(self)` -- Return the payload schema spec for this parameter.
- `registry_path` (function) `core/param_registry.py:158` `def registry_path(root)` -- Return the operator registry file path.
- `normalise_kind` (function) `core/param_registry.py:172` `def normalise_kind(kind)` -- Return the canonical kind name for a user-supplied kind.
- `effective_value` (function) `core/param_registry.py:187` `def effective_value(entry)` -- Return the value a parameter contributes to the shell params.
- `load_entries` (function) `core/param_registry.py:226` `def load_entries(root)` -- Return every operator-declared parameter.
- `list_params` (function) `core/param_registry.py:256` `def list_params(root, include_builtin, keyword)` -- Return the parameters visible to the operator.
- `create_param` (function) `core/param_registry.py:291` `def create_param(name, kind, default, description, category, root)` -- Create an operator parameter and persist it in the registry.
- `update_param` (function) `core/param_registry.py:341` `def update_param(name, default, description, kind, category, root)` -- Update an operator parameter in place.
- `delete_param` (function) `core/param_registry.py:387` `def delete_param(name, root)` -- Delete an operator parameter from the registry.
- `param_value` (function) `core/param_registry.py:411` `def param_value(name, root)` -- Return the effective value of an operator parameter.
- `operator_specs` (function) `core/param_registry.py:425` `def operator_specs(root)` -- Return the payload schema specs of the operator parameters.
- `apply_to_schema` (function) `core/param_registry.py:437` `def apply_to_schema(root)` -- Register the operator parameters in the payload schema.
- `sync_shell_params` (function) `core/param_registry.py:459` `def sync_shell_params(shell, root)` -- Push the operator parameters into a live shell parameter dict.

## core/parsers.py
Imported by: `cli/banner_config.py`, `core/__init__.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `telegram_hermes.py`, `tests/test_single_implementation.py`, `utils.py`
- `strip_ansi` (function) `core/parsers.py:15` `def strip_ansi(text)` -- Remove ANSI escape sequences and readline markers from a string.

## core/payload_schema.py
Depends on: `cli/commands/enum.py`, `core/param_registry.py`, `modules/llm_factory.py`
Imported by: `cli/assign.py`, `cli/commands/params_ops.py`, `cli/commands/session_ops.py`, `cli/wizard.py`, `core/__init__.py`, `core/config.py`, `core/param_registry.py`, `scripts/devtools/core_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_audit_remediation.py`, `tests/test_core_config.py`, `tests/test_core_defaults.py`, `tests/test_infra_disposable.py`, `tests/test_param_registry.py`, `tests/test_payload_schema.py`, `tests/test_php2shell_addon.py`, `tests/test_placeholder_coverage.py`
- `register_specs` (function) `core/payload_schema.py:1862` `def register_specs(specs)` -- Register (or replace) field specs at runtime.
- `unregister_specs` (function) `core/payload_schema.py:1885` `def unregister_specs(keys)` -- Remove runtime-registered specs from the schema.
- `field_for` (function) `core/payload_schema.py:1903` `def field_for(key)` -- Return the :class:`FieldSpec` for ``key`` or ``None`` if it is unknown.
- `coerce_value` (function) `core/payload_schema.py:1908` `def coerce_value(key, raw)` -- Return ``raw`` coerced to the canonical type declared for ``key``.
- `validate_value` (function) `core/payload_schema.py:1931` `def validate_value(key, value)` -- Validate ``value`` against the schema entry for ``key``.
- `validate_payload` (function) `core/payload_schema.py:2005` `def validate_payload(payload)` -- Validate an entire payload dictionary and return all issues found.
- `format_issue` (function) `core/payload_schema.py:2040` `def format_issue(issue)` -- Render a :class:`ValidationIssue` as a single human-readable line.
- `default_payload` (function) `core/payload_schema.py:2058` `def default_payload()` -- Return a freshly built payload dict populated from the schema defaults.
- `categories` (function) `core/payload_schema.py:2066` `def categories()` -- Return schema entries grouped by :attr:`FieldSpec.category`.

## core/process.py
Depends on: `core/console.py`, `core/hardening.py`, `core/safe_exec.py`, `core/safe_subprocess.py`, `core/validators.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/misc_migrated.py`, `cli/commands/mobile_macos.py`, `core/__init__.py`, `modules/auto_purple.py`, `modules/lazy_loop.py`, `modules/lazy_verify.py`, `static/js/particles.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_lazy_runner.py`, `tests/test_shell_semantics.py`, `utils.py`
- `check_go_tool_installed` (function) `core/process.py:34` `def check_go_tool_installed(tool_name)` -- Check if a Go tool binary is installed and runnable.
- `is_binary_present` (function) `core/process.py:54` `def is_binary_present(binary_name)` -- Check whether binary is on ``PATH``.
- `handle_multiple_rhosts` (function) `core/process.py:68` `def handle_multiple_rhosts(func)` -- Decorator that iterates over a list of remote hosts.
- `wrapper` (function) `core/process.py:82` `def wrapper(self)`
- `check_sudo` (function) `core/process.py:97` `def check_sudo()` -- Re-launch the script with ``sudo`` if not already root.
- `run` (function) `core/process.py:108` `def run(command)` -- Execute a shell command via ``SafeRunner``.
- `is_package_installed` (function) `core/process.py:143` `def is_package_installed(package_name)` -- Check whether a Python package is importable.
- `run_command` (function) `core/process.py:183` `def run_command(command, timeout)` -- Run a command, streaming output in real time.
- `ensure_tmux_session` (function) `core/process.py:253` `def ensure_tmux_session(session_name)` -- Create a tmux session if it does not already exist.
- `activate_server` (function) `core/process.py:271` `def activate_server(httpd, url, lhost)` -- Start an HTTP server and print the serving URL.

## core/profiles.py
Imported by: `cli/doctor.py`, `cli/wizard.py`, `tests/test_profiles.py`
- `active_profile` (function) `core/profiles.py:40` `def active_profile()` -- Return the selected runtime profile.
- `is_light` (function) `core/profiles.py:59` `def is_light()` -- Return ``True`` when the light profile is selected.
- `specs_for_profile` (function) `core/profiles.py:64` `def specs_for_profile(specs)` -- Filter dependency specs down to the ones the active profile needs.

## core/prompt.py
Depends on: `core/config.py`
Imported by: `key.py`, `static/js/quill-2.0.3.js`
- `get_git_info` (function) `core/prompt.py:35` `def get_git_info()` -- Return current git branch and dirty-status for the prompt.
- `get_venv_info` (function) `core/prompt.py:60` `def get_venv_info()` -- Return the active virtualenv name, or empty string if none.
- `get_kernel` (function) `core/prompt.py:68` `def get_kernel()` -- Return the running kernel version (short form).
- `get_terminal_size` (function) `core/prompt.py:78` `def get_terminal_size()` -- Return ``(width, height)`` of the terminal, defaulting to 80x24.
- `get_local_ips` (function) `core/prompt.py:87` `def get_local_ips()` -- Return a comma-separated string of non-loopback IPv4 addresses.
- `copy2clip` (function) `core/prompt.py:109` `def copy2clip(text)` -- Copy ``text`` to the system clipboard via xclip.
- `getprompt` (function) `core/prompt.py:127` `def getprompt()` -- Build the coloured status line for the CLI header and C2 dashboard.

## core/protocols.py
Imported by: `tests/test_core.py`
- `Selector.suggest` (method) `core/protocols.py:27` `def suggest(self, target, phase, context)` -- Return ``{"command": str, "reasoning": str, "mitre": str}`` or ``None``.
- `LLMBackend.complete` (method) `core/protocols.py:40` `def complete(self, system, user, max_tokens, temperature)` -- Return the model completion as a string.
- `MemoryStore.put` (method) `core/protocols.py:54` `def put(self, key, value)`
- `MemoryStore.get` (method) `core/protocols.py:56` `def get(self, key, default)`
- `MemoryStore.search` (method) `core/protocols.py:58` `def search(self, query, k)`
- `BridgeCatalog.filter` (method) `core/protocols.py:65` `def filter(self, phase, os_id)` -- Return command entries matching ``phase`` and ``os_id``.
- `OutcomeEvaluator.evaluate` (method) `core/protocols.py:73` `def evaluate(self, command, output, target, phase)` -- Return a reward in ``[0.0, 1.0]``.

## core/reverse_shell_secret.py
Depends on: `core/hardening.py`
Imported by: `lazyc2.py`, `tests/test_security_alerts_fix.py`
- `seal_reverse_shell_password` (function) `core/reverse_shell_secret.py:24` `def seal_reverse_shell_password(plaintext)` -- Seal a fallback password for storage.
- `load_reverse_shell_password` (function) `core/reverse_shell_secret.py:41` `def load_reverse_shell_password(secret_path)` -- Load a persisted fallback password, unsealing vault values.
- `generate_reverse_shell_password` (function) `core/reverse_shell_secret.py:65` `def generate_reverse_shell_password()` -- Generate a fresh cryptographically random fallback password.
- `is_configured_password_valid` (function) `core/reverse_shell_secret.py:74` `def is_configured_password_valid(candidate, minimum_length)` -- Return True when an operator-configured password meets the floor.

## core/safe_console.py
Depends on: `core/console.py`
Imported by: `cli/autosuggest.py`, `cli/ops_commands.py`, `cli/tips_engine.py`, `modules/loop_progress.py`, `tests/test_safe_console.py`
- `supports_unicode` (function) `core/safe_console.py:33` `def supports_unicode()` -- Return True when stdout can encode box-drawing glyphs and emoji.
- `get_console` (function) `core/safe_console.py:42` `def get_console()` -- Build a Rich console with safe color/box defaults.
- `panel_box` (function) `core/safe_console.py:52` `def panel_box()` -- Return the ROUNDED box on UTF-8 sinks, ASCII otherwise.
- `milestone_glyph` (function) `core/safe_console.py:57` `def milestone_glyph(state)` -- Glyph for a milestone state: done / active / pending (or other).
- `progress_bar` (function) `core/safe_console.py:67` `def progress_bar(ratio, width)` -- Fixed-width fill bar, unicode blocks or ASCII hashes.

## core/safe_exec.py
Depends on: `core/logging.py`
Imported by: `cli/banner_config.py`, `cli/commands/misc_migrated.py`, `cli/commands/pwn.py`, `cli/commands/shellsys.py`, `core/process.py`, `core/safe_subprocess.py`, `lazyc2/blueprints/api_v1.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/autonomous_exploit_engine.py`, `modules/chain_runner.py`, `modules/command_executor.py`, `modules/conditional_hooks.py`, `modules/dns_beacon.py`, `modules/lazyshortener.py`, `modules/metasploitable_migrations.py`, `modules/playbook_engine.py`, `modules/resource_script.py`, `modules/ttpscope_bridge.py`, `modules/winbox_gym.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_executor_kernel.py`, `tests/test_group_kill.py`, `tests/test_security_hardening_v4.py`, `tests/test_shell_semantics.py`
- `needs_shell` (function) `core/safe_exec.py:57` `def needs_shell(command)` -- Return True when a command string needs a shell to be interpreted.
- `safe_system` (function) `core/safe_exec.py:74` `def safe_system(command)` -- Execute a fixed command string through the shell safely.
- `safe_run_argv` (function) `core/safe_exec.py:174` `def safe_run_argv(argv)` -- Execute a command via subprocess without shell interpretation.
- `safe_run_shell` (function) `core/safe_exec.py:228` `def safe_run_shell(command)` -- Execute a command through the shell, gated by policy.
- `safe_clear_screen` (function) `core/safe_exec.py:285` `def safe_clear_screen()` -- Clear the terminal screen without using os.system.
- `validate_url` (function) `core/safe_exec.py:300` `def validate_url(url)` -- Validate a URL string, rejecting shell metacharacters.
- `safe_git_clone` (function) `core/safe_exec.py:327` `def safe_git_clone(repo_url, target_dir)` -- Clone a git repository safely using subprocess list-form.
- `safe_ip_show` (function) `core/safe_exec.py:361` `def safe_ip_show(interface)` -- Parse IP addresses from ``ip show`` output in Python.
- `safe_find_tool` (function) `core/safe_exec.py:398` `def safe_find_tool(name)` -- Find a tool on PATH using shutil.which.
- `safe_file_read` (function) `core/safe_exec.py:414` `def safe_file_read(path)` -- Read a file safely with a size limit.

## core/safe_import.py
Imported by: `cli/commands/campaign.py`, `tests/test_campaign_import_safety.py`
- `is_safe_identifier` (function) `core/safe_import.py:20` `def is_safe_identifier(name)` -- Return True when ``name`` is a bare SQL identifier.
- `filter_columns` (function) `core/safe_import.py:32` `def filter_columns(src_columns, dest_columns)` -- Intersect source columns with destination columns, safely.
- `safe_extract_zip` (function) `core/safe_import.py:51` `def safe_extract_zip(archive, dest)` -- Extract a zip archive with ZipSlip protection.
- `safe_copy_tree` (function) `core/safe_import.py:93` `def safe_copy_tree(src, dest)` -- Copy a directory tree without symlink escape.

## core/safe_subprocess.py
Depends on: `core/hardening.py`, `core/safe_exec.py`
Imported by: `core/process.py`, `tests/test_safe_subprocess.py`, `tests/test_safe_subprocess_behavior.py`, `tests/test_security_hardening.py`, `tests/test_shell_semantics.py`, `utils.py`
- `SafeRunner.__init__` (method) `core/safe_subprocess.py:70` `def __init__(self, audit_log_path)`
- `SafeRunner.run` (method) `core/safe_subprocess.py:73` `def run(self, argv)` -- Execute ``argv`` without invoking a shell.
- `SafeRunner.run_shell` (method) `core/safe_subprocess.py:105` `def run_shell(self, command)` -- Execute ``command`` through the system shell, gated by policy.

## core/scheduler.py
Depends on: `core/logging.py`
- `TaskScheduler.__init__` (method) `core/scheduler.py:61` `def __init__(self)`
- `TaskScheduler.instance` (method) `core/scheduler.py:73` `def instance(cls)` -- Return the singleton ``TaskScheduler`` instance.
- `TaskScheduler.start` (method) `core/scheduler.py:81` `def start(self)` -- Start the scheduler background thread.
- `TaskScheduler.stop` (method) `core/scheduler.py:100` `def stop(self)` -- Stop the scheduler and cancel all pending tasks.
- `TaskScheduler.schedule_task` (method) `core/scheduler.py:123` `def schedule_task(self, name, interval_seconds, func)` -- Register a recurring task to run every ``interval_seconds``.
- `TaskScheduler.schedule_once` (method) `core/scheduler.py:157` `def schedule_once(self, name, delay_seconds, func)` -- Register a one-shot task to run after ``delay_seconds``.
- `TaskScheduler.cancel_task` (method) `core/scheduler.py:192` `def cancel_task(self, name)` -- Cancel a scheduled task by name.
- `TaskScheduler.list_tasks` (method) `core/scheduler.py:205` `def list_tasks(self)` -- Return metadata for all registered tasks.
- `get_scheduler` (function) `core/scheduler.py:285` `def get_scheduler()` -- Return the singleton ``TaskScheduler`` instance.

## core/security.py
Depends on: `core/logging.py`
- `anti_debug` (function) `core/security.py:18` `def anti_debug()` -- Check for debugger attachment and exit if found.
- `generate_certificates` (function) `core/security.py:58` `def generate_certificates(output_dir)` -- Generate a self-signed CA certificate and key pair.

## core/session_secrets.py
Depends on: `core/config.py`, `core/logging.py`
Imported by: `cli/commands/shellsys.py`, `lazyc2.py`, `modules/c2_agent.py`, `modules/c2_builder.py`, `tests/test_session_secrets.py`
- `rotate_session_secrets` (function) `core/session_secrets.py:38` `def rotate_session_secrets(config_obj, sessions_dir)` -- Generate and persist a fresh set of session secrets.
- `ensure_session_secrets` (function) `core/session_secrets.py:72` `def ensure_session_secrets(config_obj, rotate, sessions_dir)` -- Return valid session secrets, rotating them when required.

## core/terminal_guard.py
Imported by: `modules/lazy_runner.py`, `tests/test_lazy_runner.py`
- `emit_restore_sequences` (function) `core/terminal_guard.py:41` `def emit_restore_sequences()` -- Write the mode-reset sequences to the controlling terminal.
- `apply_stty_sane` (function) `core/terminal_guard.py:62` `def apply_stty_sane()` -- Best-effort ``stty sane`` fallback when termios restore fails.
- `TerminalGuard.__init__` (method) `core/terminal_guard.py:85` `def __init__(self)` -- Prepare an empty guard; the snapshot happens on ``__enter__``.
- `TerminalGuard.restore` (method) `core/terminal_guard.py:108` `def restore(self)` -- Restore saved termios, then reset extra terminal modes once.

## core/text_utils.py
Imported by: `cli/autosuggest.py`, `cli/graph_overlay.py`, `cli/palette_command.py`, `cli/palette_overlay.py`, `cli/reactive_hints.py`, `cli/reasoning_stream.py`, `cli/tips_engine.py`, `cli/toast_bus.py`
- `truncate_text` (function) `core/text_utils.py:10` `def truncate_text(value, max_len, marker)` -- Truncate value to max_len using marker.

## core/validators.py
Depends on: `core/console.py`, `core/host_policy.py`
Imported by: `cli/commands/_base.py`, `cli/commands/enum.py`, `cli/commands/mobile_macos.py`, `cli/commands/pwn.py`, `core/__init__.py`, `core/process.py`, `modules/c2_builder.py`, `tests/test_core.py`, `tests/test_host_policy.py`, `tests/test_input_fuzz.py`, `tests/test_require_guards.py`, `utils.py`
- `check_rhost` (function) `core/validators.py:26` `def check_rhost(rhost)` -- Return ``True`` if ``rhost`` is set, otherwise print an error and return ``False``.
- `check_lhost` (function) `core/validators.py:40` `def check_lhost(lhost)` -- Return ``True`` if ``lhost`` is set, otherwise print an error and return ``False``.
- `check_lport` (function) `core/validators.py:54` `def check_lport(lport)` -- Return ``True`` if ``lport`` is set, otherwise print an error and return ``False``.
- `check_port` (function) `core/validators.py:64` `def check_port(port, name)` -- Return ``True`` if ``port`` is a valid TCP/UDP port (1-65535).
- `require_rhost` (function) `core/validators.py:77` `def require_rhost(params)` -- Gate a command on a valid ``rhost`` looked up from ``params``.
- `require_lhost` (function) `core/validators.py:94` `def require_lhost(params)` -- Gate a command on a valid ``lhost`` looked up from ``params``.
- `require_lport` (function) `core/validators.py:107` `def require_lport(params)` -- Gate a command on a valid ``lport`` looked up from ``params``.
- `require_rport` (function) `core/validators.py:120` `def require_rport(params)` -- Gate a command on a valid ``rport`` looked up from ``params``.

## deploy/range/ad-mini/traffic-gen.py
- `main` (function) `deploy/range/ad-mini/traffic-gen.py:35` `def main()` -- Loop forever emitting fake background traffic.

## discord_c2.py
Depends on: `core/parsers.py`, `lazyown.py`, `modules/llm_adapter.py`
- `SecureSessionManager.__init__` (method) `discord_c2.py:28` `def __init__(self)`
- `SecureSessionManager.register_failed_attempt` (method) `discord_c2.py:33` `def register_failed_attempt(self, user_id)`
- `SecureSessionManager.check_lockout` (method) `discord_c2.py:40` `def check_lockout(self, user_id)`
- `SecureSessionManager.check_rate_limit` (method) `discord_c2.py:49` `def check_rate_limit(self, user_id)`
- `SecureSessionManager.create_session` (method) `discord_c2.py:62` `def create_session(self, user_id, client_id)`
- `SecureSessionManager.validate_session` (method) `discord_c2.py:70` `def validate_session(self, user_id)`
- `Config.__init__` (method) `discord_c2.py:87` `def __init__(self, config_dict)`
- `load_payload` (function) `discord_c2.py:96` `def load_payload()`
- `on_ready` (function) `discord_c2.py:103` `def on_ready()`
- `start` (function) `discord_c2.py:108` `def start(ctx)`
- `exce_cmd` (function) `discord_c2.py:130` `def exce_cmd(ctx)`
- `add_cli` (function) `discord_c2.py:206` `def add_cli(ctx, new_client_id)`
- `handle_file` (function) `discord_c2.py:216` `def handle_file(ctx)`
- `download_c2` (function) `discord_c2.py:245` `def download_c2(ctx, client_id, file_name)`
- `send_connected_clients` (function) `discord_c2.py:256` `def send_connected_clients(ctx)`
- `clients` (function) `discord_c2.py:273` `def clients(ctx)`
- `addcli` (function) `discord_c2.py:278` `def addcli(ctx, new_client_id)`
- `c2` (function) `discord_c2.py:283` `def c2(ctx)`

## external/install_external.sh
- `ctrl_c` (function) `external/install_external.sh:13`
- `download` (function) `external/install_external.sh:18`

## fast_run_as_r00t.sh
- `log` (function) `fast_run_as_r00t.sh:59` -- ── Pretty-print helpers ──────────────────────────────────────────────────────
- `spin` (function) `fast_run_as_r00t.sh:60`
- `err_box` (function) `fast_run_as_r00t.sh:61`
- `ensure_gum` (function) `fast_run_as_r00t.sh:67` -- ── Ensure gum is installed ───────────────────────────────────────────────────
- `check_deps` (function) `fast_run_as_r00t.sh:78` -- ── Dependency check ──────────────────────────────────────────────────────────
- `check_sudo` (function) `fast_run_as_r00t.sh:87` -- ── Re-exec as root if needed ─────────────────────────────────────────────────
- `parse_args` (function) `fast_run_as_r00t.sh:96` -- ── CLI argument parsing ──────────────────────────────────────────────────────
- `t_send` (function) `fast_run_as_r00t.sh:114` -- Send one or more commands to the active tmux pane
- `t_lazyown` (function) `fast_run_as_r00t.sh:121` -- Open a new pane (split v or h), start LazyOwn shell with optional run flags, then send any follow-up commands once...
- `t_priv_user` (function) `fast_run_as_r00t.sh:134` -- Open a new pane running a command as unprivileged user 1000 (with venv).
- `start_chown_watcher` (function) `fast_run_as_r00t.sh:145` -- ── Background chown watcher ────────────────────────────────────────────────── Re-chowns the project tree to the...
- `kill_stale_c2` (function) `fast_run_as_r00t.sh:166` -- ── Stale C2 cleanup ────────────────────────────────────────────────────────── A lazyc2.py left over from a previous...

## install.sh
- `usage` (function) `install.sh:49`
- `log` (function) `install.sh:88`
- `spin_run` (function) `install.sh:98`
- `ensure_gum` (function) `install.sh:128`
- `install_system_packages` (function) `install.sh:139`
- `install_external_tools` (function) `install.sh:150`
- `install_python_environment` (function) `install.sh:165`
- `install_ollama` (function) `install.sh:206`
- `install_external_storage` (function) `install.sh:218`
- `install_lazyownbt` (function) `install.sh:231`
- `download_file` (function) `install.sh:251`
- `install_encoder_module` (function) `install.sh:263`
- `generate_certificates` (function) `install.sh:274`
- `seed_payload_config` (function) `install.sh:281`
- `verify_installation` (function) `install.sh:294`
- `main` (function) `install.sh:310`

## key.py
Depends on: `core/console.py`, `core/prompt.py`
- `main` (function) `key.py:10` `def main()`

## lazy_sentinel4.py
Depends on: `cli/toast_bus.py`, `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `sanitize_content` (function) `lazy_sentinel4.py:45` `def sanitize_content(text)` -- Sanitize text to ensure it's safe for rendering.
- `RAGManager.__init__` (method) `lazy_sentinel4.py:59` `def __init__(self, model_name, cache_size)`
- `RAGManager.initialize_cache_table` (method) `lazy_sentinel4.py:71` `def initialize_cache_table(self)`
- `RAGManager.get_cache_key` (method) `lazy_sentinel4.py:83` `def get_cache_key(self, content)`
- `RAGManager.load_existing_vectorstore` (method) `lazy_sentinel4.py:86` `def load_existing_vectorstore(self)`
- `RAGManager.ollama_llm` (method) `lazy_sentinel4.py:99` `def ollama_llm(self, question, context)`
- `RAGManager.process_file_to_rag` (method) `lazy_sentinel4.py:113` `def process_file_to_rag(self, file_path)`
- `RAGManager.query_rag` (method) `lazy_sentinel4.py:153` `def query_rag(self, question)`
- `RAGManager.invalidate_cache` (method) `lazy_sentinel4.py:175` `def invalidate_cache(self, file_path)`
- `RAGManager.get_knowledge_base_stats` (method) `lazy_sentinel4.py:189` `def get_knowledge_base_stats(self)`
- `Database.__init__` (method) `lazy_sentinel4.py:213` `def __init__(self, db_path)`
- `Database.initialize` (method) `lazy_sentinel4.py:217` `def initialize(self)`
- `Database.execute` (method) `lazy_sentinel4.py:241` `def execute(self, query, params)`
- `Database.insert` (method) `lazy_sentinel4.py:253` `def insert(self, query, params)`
- `Alert.__init__` (method) `lazy_sentinel4.py:272` `def __init__(self, alert_type, details, severity)`
- `Alert.to_dict` (method) `lazy_sentinel4.py:278` `def to_dict(self)`
- `Alert.save_to_db` (method) `lazy_sentinel4.py:286` `def save_to_db(self, db)`
- `LazySentinelHandler.__init__` (method) `lazy_sentinel4.py:301` `def __init__(self, lazysentinel)`
- `LazySentinelHandler.is_text_file` (method) `lazy_sentinel4.py:304` `def is_text_file(self, file_path)`
- `LazySentinelHandler.on_created` (method) `lazy_sentinel4.py:314` `def on_created(self, event)`
- `LazySentinelHandler.on_modified` (method) `lazy_sentinel4.py:326` `def on_modified(self, event)`
- `LazySentinel.__init__` (method) `lazy_sentinel4.py:339` `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)`
- `LazySentinel.chunk_text` (method) `lazy_sentinel4.py:359` `def chunk_text(self, text, chunk_size)`
- `LazySentinel.select_relevant_chunk` (method) `lazy_sentinel4.py:362` `def select_relevant_chunk(self, file_content, chunks)`
- `LazySentinel.parse_deepseek_response` (method) `lazy_sentinel4.py:376` `def parse_deepseek_response(self, response_text)`
- `LazySentinel.show_popup` (method) `lazy_sentinel4.py:402` `def show_popup(self, file_name, relevant_info, commands, details)`
- `LazySentinel.process_file` (method) `lazy_sentinel4.py:420` `def process_file(self, file_path)`
- `LazySentinel.stop` (method) `lazy_sentinel4.py:536` `def stop(self)`
- `App.__init__` (method) `lazy_sentinel4.py:543` `def __init__(self)`
- `App.display_toastr` (method) `lazy_sentinel4.py:557` `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)` -- Display the sentinel popup through the shared toast bus panel.
- `App.postcmd` (method) `lazy_sentinel4.py:567` `def postcmd(self, stop, line)` -- Check the popup queue after each command and display toastr notifications.
- `App.do_quit` (method) `lazy_sentinel4.py:591` `def do_quit(self, arg)`
- `App.do_debug` (method) `lazy_sentinel4.py:595` `def do_debug(self, arg)`
- `App.do_rag_query` (method) `lazy_sentinel4.py:604` `def do_rag_query(self, arg)`
- `App.do_rag_add` (method) `lazy_sentinel4.py:612` `def do_rag_add(self, arg)`
- `App.do_rag_status` (method) `lazy_sentinel4.py:627` `def do_rag_status(self, arg)`
- `App.do_rag_toggle` (method) `lazy_sentinel4.py:634` `def do_rag_toggle(self, arg)`
- `App.do_rag_bulk_add` (method) `lazy_sentinel4.py:639` `def do_rag_bulk_add(self, arg)`
- `App.do_rag_search` (method) `lazy_sentinel4.py:658` `def do_rag_search(self, arg)`
- `App.complete_rag_add` (method) `lazy_sentinel4.py:679` `def complete_rag_add(self, text, line, begidx, endidx)`
- `App.complete_rag_bulk_add` (method) `lazy_sentinel4.py:686` `def complete_rag_bulk_add(self, text, line, begidx, endidx)`


Next: [API_p8.md](API_p8.md)
