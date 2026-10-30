# API (page 7 of 25)
Previous: [API_p6.md](API_p6.md)

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

## lazyc2.py
Depends on: `cli/auto_crypto.py`, `cli/palette.py`, `cli/palette_command.py`, `core/config.py`, `core/console.py`, `core/hardening.py`, `core/logging.py`, `core/parsers.py`, `core/reverse_shell_secret.py`, `core/session_secrets.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/extensions/users.py`, `lazyc2/security/cli_credentials.py`, `lazyc2/security/command_allowlist.py`, `lazyc2/security/constants.py`, `lazyc2/security/cors.py`, `lazyc2/security/csrf.py`, `lazyc2/security/html_sanitizer.py`, `lazyc2/security/https_redirect.py`, `lazyc2/security/services.py`, `lazyc2/security/trusted_proxy.py`, `lazyc2/security/validators.py`, `lazyown.py`, `modules/__init__.py`, `modules/attack_surface3d.py`, `modules/backdoor/server.c`, `modules/beacon_history.py`, `modules/beacon_recon.py`, `modules/c2_surfaces.py`, `modules/chain_approval.py`, `modules/collab_bp.py`, `modules/colors.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/dashboard_bp.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/event_engine.py`, `modules/intel_fusion.py`, `modules/kill_chain_viz.py`, `modules/killchain.py`, `modules/lazy_loop.py`, `modules/lazy_mentions.py`, `modules/lazy_rbac.py`, `modules/listener_manager.py`, `modules/live_surface.py`, `modules/llm_adapter.py`, `modules/llm_orchestrator.py`, `modules/logging_config.py`, `modules/loop_manager.py`, `modules/metrics.py`, `modules/security_sanitizers.py`, `modules/state_manager.py`, `modules/world_model.py`, `skills/daemon_health.py`, `skills/lazyown_facts.py`, `utils.py`
- `is_insecure_credential` (function) `lazyc2.py:242` `def is_insecure_credential(user, pwd)` -- Check for weak or default credentials
- `_JsonLogFormatter.format` (method) `lazyc2.py:482` `def format(self, record)`
- `ensure_sessions_dir` (function) `lazyc2.py:509` `def ensure_sessions_dir()` -- Ensure the sessions directory exists with safe permissions.
- `load_routes` (function) `lazyc2.py:520` `def load_routes()` -- Load dynamic routes from JSON file.
- `save_routes` (function) `lazyc2.py:530` `def save_routes(routes)` -- Save dynamic routes to JSON file with safe permissions.
- `validate_route_path` (function) `lazyc2.py:544` `def validate_route_path(route_path)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_route_path`.
- `validate_template_name` (function) `lazyc2.py:557` `def validate_template_name(template_name)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_template_name`.
- `is_safe_template_path` (function) `lazyc2.py:567` `def is_safe_template_path(template_path, template_name)` -- Verify ``template_path`` resolves inside ``app.template_folder``.
- `is_binary` (function) `lazyc2.py:607` `def is_binary(safe_filename)` -- Check whether a session file is binary based on its header bytes.
- `clean_expired_tokens` (function) `lazyc2.py:648` `def clean_expired_tokens()`
- `clean_json` (function) `lazyc2.py:656` `def clean_json(text)` -- Extract only the JSON content between ```json and ```, discarding everything else.
- `load_yaml_safely` (function) `lazyc2.py:684` `def load_yaml_safely(file_path)` -- Load a YAML file safely with error handling and default values.
- `Handler.on_any_event` (method) `lazyc2.py:768` `def on_any_event(event)`
- `get_karma_name` (function) `lazyc2.py:793` `def get_karma_name(elo)`
- `fromjson` (function) `lazyc2.py:810` `def fromjson(value)`
- `run_shell` (function) `lazyc2.py:814` `def run_shell()`
- `load_banners` (function) `lazyc2.py:824` `def load_banners()` -- Loads the banners from the JSON file.
- `load_mitre_data` (function) `lazyc2.py:844` `def load_mitre_data()`
- `load_event_config` (function) `lazyc2.py:850` `def load_event_config()`
- `load_notifications` (function) `lazyc2.py:858` `def load_notifications()`
- `implants_check` (function) `lazyc2.py:876` `def implants_check()`
- `extract_attack_vectors` (function) `lazyc2.py:893` `def extract_attack_vectors(nodes, edges)` -- Analyzes BloodHound nodes and edges to extract critical attack vectors for AD compromise.
- `process_bloodhound_zip` (function) `lazyc2.py:980` `def process_bloodhound_zip(zip_filepath)` -- Processes a BloodHound ZIP file to extract nodes and edges for graph visualization.
- `start_watching` (function) `lazyc2.py:1078` `def start_watching()`
- `load_tasks` (function) `lazyc2.py:1094` `def load_tasks()`
- `create_cves` (function) `lazyc2.py:1102` `def create_cves()`
- `load_cves` (function) `lazyc2.py:1108` `def load_cves()`
- `save_cves` (function) `lazyc2.py:1116` `def save_cves(cves)`
- `create_report` (function) `lazyc2.py:1121` `def create_report()`
- `save_tasks` (function) `lazyc2.py:1127` `def save_tasks(tasks)`
- `load_note` (function) `lazyc2.py:1132` `def load_note()`
- `aumentar_elo` (function) `lazyc2.py:1150` `def aumentar_elo(user_id, cantidad)`
- `save_note` (function) `lazyc2.py:1180` `def save_note(content)`
- `escape_js` (function) `lazyc2.py:1186` `def escape_js(s)`
- `markdown_to_html` (function) `lazyc2.py:1223` `def markdown_to_html(text)`
- `to_serializable` (function) `lazyc2.py:1231` `def to_serializable(obj)` -- Convert objects to serializable format.
- `make_serializable` (function) `lazyc2.py:1238` `def make_serializable(data)` -- Recursively convert data to serializable format.
- `datetime_now_iso` (function) `lazyc2.py:1256` `def datetime_now_iso()` -- Return the current UTC timestamp as an ISO-8601 string.
- `escape_js_string` (function) `lazyc2.py:1475` `def escape_js_string(value)` -- Escape special characters in a string for JavaScript.
- `check_auth` (function) `lazyc2.py:1487` `def check_auth(username, password)` -- Verify credentials.
- `authenticate` (function) `lazyc2.py:1502` `def authenticate()` -- Requests authentication.
- `requires_auth_or_session` (function) `lazyc2.py:1511` `def requires_auth_or_session(f)` -- Require Basic auth credentials or a valid Flask-Login session.
- `decorated` (function) `lazyc2.py:1521` `def decorated()`
- `requires_auth` (function) `lazyc2.py:1532` `def requires_auth(f)`
- `decorated` (function) `lazyc2.py:1534` `def decorated()`
- `csrf_protect` (function) `lazyc2.py:1543` `def csrf_protect(view)` -- Decorator that enforces the per-session CSRF token.
- `wrapper` (function) `lazyc2.py:1553` `def wrapper()`
- `aicmd_deepseek` (function) `lazyc2.py:1564` `def aicmd_deepseek(cmd)`
- `aicmd` (function) `lazyc2.py:1678` `def aicmd(cmd)`
- `search_database` (function) `lazyc2.py:1783` `def search_database(term, data_path)` -- Busca un término en un DataFrame, manejando listas, dicts y distintas estructuras.
- `execute_command` (function) `lazyc2.py:1838` `def execute_command(command)`
- `CustomDNSResolver.resolve` (method) `lazyc2.py:1868` `def resolve(self, request, handler)`
- `start_dns_server` (function) `lazyc2.py:1972` `def start_dns_server()` -- Start the C2 DNS server, gracefully degrading when binding is unsafe.
- `tcp_bridge` (function) `lazyc2.py:2012` `def tcp_bridge(local_port, remote_host, remote_port)` -- Establish a TCP bridge between a local port and a remote host.
- `handle_client` (function) `lazyc2.py:2036` `def handle_client(client_socket, remote_host, remote_port)` -- Handle communication between the client and the remote server.
- `decoy` (function) `lazyc2.py:2055` `def decoy()` -- Serve a decoy page to non-operator IPs when decoy mode is enabled.
- `encrypt_data` (function) `lazyc2.py:2112` `def encrypt_data(data)`
- `decrypt_data` (function) `lazyc2.py:2121` `def decrypt_data(encrypted_data, is_file)`
- `set_winsize` (function) `lazyc2.py:2134` `def set_winsize(fd, row, col, xpix, ypix)` -- Configura el tamaño de la terminal
- `read_and_forward_pty_output` (function) `lazyc2.py:2140` `def read_and_forward_pty_output()` -- Lectura continua del PTY y envío por WebSocket
- `get_discovered_hosts` (function) `lazyc2.py:2157` `def get_discovered_hosts()` -- Reads the sessions/hostsdiscovery.txt file and returns a list of discovered hosts.
- `get_local_ip_addresses` (function) `lazyc2.py:2207` `def get_local_ip_addresses()`
- `sanitize_json` (function) `lazyc2.py:2232` `def sanitize_json(data)` -- Elimina datos sensibles del diccionario JSON.
- `add_dynamic_data` (function) `lazyc2.py:2262` `def add_dynamic_data(data)` -- Agrega datos dinámicos al diccionario JSON si es necesario, basándose en el contenido del diccionario 'data'.
- `get_client_ip` (function) `lazyc2.py:2284` `def get_client_ip()` -- Get the client's IP address, handling proxies.
- `get_request_details` (function) `lazyc2.py:2293` `def get_request_details()` -- Collect comprehensive request details.
- `save_to_log` (function) `lazyc2.py:2328` `def save_to_log(data)` -- Append request data to the JSON log file with safe permissions.
- `parse_access_log_for_short_url` (function) `lazyc2.py:2350` `def parse_access_log_for_short_url(short_url)` -- Parse access.log for entries matching the given short URL.
- `parse_execution_log` (function) `lazyc2.py:2372` `def parse_execution_log(implante)` -- Parse execution log for the given implante, returning execution events.
- `load_implant_config` (function) `lazyc2.py:2398` `def load_implant_config(implante)` -- Load implant configuration from JSON file.
- `load_short_urls` (function) `lazyc2.py:2408` `def load_short_urls()` -- Load short URLs from JSON file, creating it if it doesn't exist.
- `save_short_urls` (function) `lazyc2.py:2428` `def save_short_urls(data)` -- Save short URLs to JSON file.
- `is_valid_url` (function) `lazyc2.py:2438` `def is_valid_url(url)` -- Validate if the input is a valid URL or existing local file path.
- `get_safe_file_path` (function) `lazyc2.py:2446` `def get_safe_file_path(user_path)` -- Construye de forma segura el path del archivo y verifica que está en el directorio permitido.
- `analyze_behavioral_data` (function) `lazyc2.py:2541` `def analyze_behavioral_data(behavioral_events)` -- Analyze behavioral events using the orchestrator LLM chain.
- `analyze_campaign_progress` (function) `lazyc2.py:2593` `def analyze_campaign_progress(campaign_id, events)` -- Analyze campaign progress using the orchestrator LLM chain.
- `require_mfa_socket` (function) `lazyc2.py:2737` `def require_mfa_socket(f)` -- Socket.IO-compatible MFA guard for command/control namespaces.
- `decorated` (function) `lazyc2.py:2745` `def decorated()`
- `User.__init__` (method) `lazyc2.py:3249` `def __init__(self, user_data)`
- `load_users` (function) `lazyc2.py:3271` `def load_users()`
- `save_users` (function) `lazyc2.py:3281` `def save_users(users)`
- `load_data` (function) `lazyc2.py:3292` `def load_data()`
- `load_user` (function) `lazyc2.py:3309` `def load_user(user_id)`
- `tojson_filter` (function) `lazyc2.py:3324` `def tojson_filter(value)` -- Custom tojson filter to handle non-serializable objects.
- `index` (function) `lazyc2.py:3331` `def index()`
- `send_command` (function) `lazyc2.py:3482` `def send_command(client_id)`
- `receive_result` (function) `lazyc2.py:3680` `def receive_result(client_id)`
- `issue_command` (function) `lazyc2.py:4239` `def issue_command()`
- `upload` (function) `lazyc2.py:4253` `def upload()`
- `download_file` (function) `lazyc2.py:4290` `def download_file()`
- `serve_file` (function) `lazyc2.py:4317` `def serve_file(file_path)` -- Serve a file from ``sessions/temp_uploads`` through :class:`SafeFileService`.
- `create_route` (function) `lazyc2.py:4419` `def create_route()` -- Register a new operator-supplied dynamic route bound to a template.
- `dynamic_route` (function) `lazyc2.py:4488` `def dynamic_route(route_path, data)` -- Handle dynamic routes based on stored route-to-template mappings.
- `sanitize_input` (function) `lazyc2.py:4495` `def sanitize_input(input_str)` -- Sanitize input to prevent XSS attacks.
- `is_valid_route_path` (function) `lazyc2.py:4505` `def is_valid_route_path(route_path)` -- Validate route path format.
- `is_valid_data` (function) `lazyc2.py:4512` `def is_valid_data(data)` -- Validate data parameter.
- `is_valid_template_name` (function) `lazyc2.py:4522` `def is_valid_template_name(template_name)` -- Validate template name.
- `log` (function) `lazyc2.py:4584` `def log(data)` -- Log request details to JSON file.
- `favicon` (function) `lazyc2.py:4602` `def favicon()` -- Serve the favicon.ico file.
- `palette_view` (function) `lazyc2.py:4615` `def palette_view()` -- Render the operator command palette browser.
- `palette_api` (function) `lazyc2.py:4643` `def palette_api()` -- JSON catalogue feed for the global Cmd+K / Ctrl+K overlay.
- `api_data` (function) `lazyc2.py:4664` `def api_data()`
- `create_short_url` (function) `lazyc2.py:4826` `def create_short_url()` -- Create multiple short URLs for a single original URL.
- `track_interaction` (function) `lazyc2.py:4854` `def track_interaction(short_url)` -- Serve tracking page and log behavioral data.
- `update_short_url` (function) `lazyc2.py:4879` `def update_short_url(short_url)`
- `redirect_to_file` (function) `lazyc2.py:4906` `def redirect_to_file(short_url)`
- `webserver_report` (function) `lazyc2.py:4934` `def webserver_report(filename)` -- Serve nmap HTML report assets from the sessions directory over HTTPS.
- `download_files` (function) `lazyc2.py:4954` `def download_files(filename)` -- Serve implant stage files by name, enforcing strict containment.
- `view_yaml` (function) `lazyc2.py:5006` `def view_yaml()`
- `run_command` (function) `lazyc2.py:5100` `def run_command()` -- Execute one shell command and return a sanitised, JSON-safe result.
- `get_output` (function) `lazyc2.py:5169` `def get_output()`
- `run_shellcode` (function) `lazyc2.py:5196` `def run_shellcode()`
- `get_results` (function) `lazyc2.py:5205` `def get_results()`
- `send_lcommand` (function) `lazyc2.py:5303` `def send_lcommand(ip, port)`
- `chatbot` (function) `lazyc2.py:5336` `def chatbot()`
- `vuln` (function) `lazyc2.py:5352` `def vuln()`
- `taskbot` (function) `lazyc2.py:5391` `def taskbot()`
- `search` (function) `lazyc2.py:5407` `def search()`
- `script` (function) `lazyc2.py:5423` `def script()`
- `redop` (function) `lazyc2.py:5439` `def redop()`
- `adversary` (function) `lazyc2.py:5458` `def adversary()`
- `generalbot` (function) `lazyc2.py:5474` `def generalbot()`
- `csv_to_html` (function) `lazyc2.py:5490` `def csv_to_html()`
- `search_results` (function) `lazyc2.py:5541` `def search_results()`
- `graph` (function) `lazyc2.py:5589` `def graph()`
- `task` (function) `lazyc2.py:5598` `def task(task_id)`
- `get_tasks` (function) `lazyc2.py:5613` `def get_tasks()`
- `tasks` (function) `lazyc2.py:5623` `def tasks()`
- `edit_task` (function) `lazyc2.py:5652` `def edit_task(task_id)`
- `cves` (function) `lazyc2.py:5686` `def cves()`
- `cve` (function) `lazyc2.py:5712` `def cve(cve_id)`
- `edit_cve` (function) `lazyc2.py:5727` `def edit_cve(cve_id)`
- `edit_notes` (function) `lazyc2.py:5761` `def edit_notes()`
- `get_notes` (function) `lazyc2.py:5779` `def get_notes()`
- `view_note` (function) `lazyc2.py:5789` `def view_note()`
- `push_notification` (function) `lazyc2.py:5799` `def push_notification()`
- `edit_event` (function) `lazyc2.py:5826` `def edit_event(event_name)`
- `get_event_config` (function) `lazyc2.py:5861` `def get_event_config()`
- `get_event_config_view` (function) `lazyc2.py:5868` `def get_event_config_view()`
- `aicmd_view` (function) `lazyc2.py:5903` `def aicmd_view()`
- `get_events` (function) `lazyc2.py:5928` `def get_events()`
- `list_tools` (function) `lazyc2.py:5960` `def list_tools()`
- `create_tool` (function) `lazyc2.py:5970` `def create_tool()`
- `view_tool` (function) `lazyc2.py:5997` `def view_tool(toolname)`
- `update_tool` (function) `lazyc2.py:6028` `def update_tool(toolname)`
- `delete_tool` (function) `lazyc2.py:6076` `def delete_tool(toolname)`
- `register` (function) `lazyc2.py:6111` `def register()`
- `login` (function) `lazyc2.py:6170` `def login()`
- `mfa_setup` (function) `lazyc2.py:6222` `def mfa_setup()`
- `mfa_qr` (function) `lazyc2.py:6296` `def mfa_qr(username)` -- Serve a locally-generated QR code SVG for MFA setup.
- `mfa_verify` (function) `lazyc2.py:6318` `def mfa_verify()`
- `admin_users` (function) `lazyc2.py:6371` `def admin_users()`
- `admin_set_role` (function) `lazyc2.py:6386` `def admin_set_role(user_id)`
- `admin_reset_mfa` (function) `lazyc2.py:6408` `def admin_reset_mfa(user_id)`
- `admin_delete_user` (function) `lazyc2.py:6420` `def admin_delete_user(user_id)`
- `admin_tenants` (function) `lazyc2.py:6438` `def admin_tenants()`
- `admin_create_tenant` (function) `lazyc2.py:6459` `def admin_create_tenant()`
- `admin_switch_tenant` (function) `lazyc2.py:6479` `def admin_switch_tenant(tenant_id)`
- `profile` (function) `lazyc2.py:6494` `def profile()`
- `logout` (function) `lazyc2.py:6518` `def logout()`
- `change_password` (function) `lazyc2.py:6534` `def change_password()` -- Force rotation of the initial one-time admin password.
- `aumentar_elo_route` (function) `lazyc2.py:6600` `def aumentar_elo_route(user_id)`
- `banners` (function) `lazyc2.py:6616` `def banners()`
- `mitre` (function) `lazyc2.py:6652` `def mitre()`
- `get_connected_clients` (function) `lazyc2.py:6697` `def get_connected_clients()`
- `lazybot` (function) `lazyc2.py:6708` `def lazybot()`
- `compliance_dashboard` (function) `lazyc2.py:6725` `def compliance_dashboard()`
- `compliance_report` (function) `lazyc2.py:6747` `def compliance_report()`
- `compliance_add_evidence` (function) `lazyc2.py:6777` `def compliance_add_evidence()`
- `compliance_verify_evidence` (function) `lazyc2.py:6813` `def compliance_verify_evidence()`
- `compliance_export` (function) `lazyc2.py:6827` `def compliance_export(format)`
- `lazyreport` (function) `lazyc2.py:6857` `def lazyreport()`
- `teamserver` (function) `lazyc2.py:6876` `def teamserver()`
- `report` (function) `lazyc2.py:6905` `def report()`
- `lazyreport_view` (function) `lazyc2.py:6912` `def lazyreport_view()`
- `killchain_view` (function) `lazyc2.py:6918` `def killchain_view()`
- `api_killchain` (function) `lazyc2.py:6948` `def api_killchain()` -- Return the unified kill-chain snapshot consumed by every surface.
- `api_beacon_results` (function) `lazyc2.py:6979` `def api_beacon_results(client_id)` -- Return the full ordered command/result history for one beacon.
- `api_loops_start` (function) `lazyc2.py:7010` `def api_loops_start()` -- Start one autonomous loop subprocess from the dashboard.
- `api_loops_list` (function) `lazyc2.py:7059` `def api_loops_list()` -- List every autonomous loop with refreshed live status.
- `api_loop_log` (function) `lazyc2.py:7071` `def api_loop_log(loop_id)` -- Return one chunk of a loop's output log.
- `api_loop_stop` (function) `lazyc2.py:7094` `def api_loop_stop(loop_id)` -- Stop one running loop by terminating its process group.
- `connect` (function) `lazyc2.py:7285` `def connect()`
- `listener` (function) `lazyc2.py:7291` `def listener()`
- `listener_connect` (function) `lazyc2.py:7298` `def listener_connect()`
- `listener_disconnect` (function) `lazyc2.py:7309` `def listener_disconnect()`
- `pty_input` (function) `lazyc2.py:7320` `def pty_input(data)`
- `resize` (function) `lazyc2.py:7335` `def resize(data)`
- `pty_connect` (function) `lazyc2.py:7349` `def pty_connect()`
- `handle_input` (function) `lazyc2.py:7381` `def handle_input(data)`
- `listener_command` (function) `lazyc2.py:7406` `def listener_command(msg)`
- `terminal` (function) `lazyc2.py:7420` `def terminal()`
- `terminal_connect` (function) `lazyc2.py:7430` `def terminal_connect()`
- `terminal_disconnect` (function) `lazyc2.py:7440` `def terminal_disconnect()`
- `terminal_input` (function) `lazyc2.py:7451` `def terminal_input(data)`
- `terminal_command` (function) `lazyc2.py:7465` `def terminal_command(data)`
- `terminal_resize` (function) `lazyc2.py:7481` `def terminal_resize(data)`
- `start_reverse_shell` (function) `lazyc2.py:7489` `def start_reverse_shell()`
- `start_bridge` (function) `lazyc2.py:7543` `def start_bridge()` -- Start a TCP bridge to a specified remote host and port.
- `page_not_found` (function) `lazyc2.py:7560` `def page_not_found(e)`
- `internal_server_error` (function) `lazyc2.py:7568` `def internal_server_error(e)`
- `get_config` (function) `lazyc2.py:7577` `def get_config()` -- Lee el archivo payload.json, lo manipula y lo expone como /config.json.
- `capture_image` (function) `lazyc2.py:7596` `def capture_image()`
- `capture_audio` (function) `lazyc2.py:7622` `def capture_audio()`
- `surface` (function) `lazyc2.py:7640` `def surface()`
- `surface_live` (function) `lazyc2.py:7646` `def surface_live()` -- Render the live attack-surface graph page.
- `api_surface_live` (function) `lazyc2.py:7661` `def api_surface_live()` -- Return the live attack-surface graph derived from the world model.
- `intel_view` (function) `lazyc2.py:7683` `def intel_view()` -- Render the fused sessions intel graph page (ReadMenator engine).
- `intel_bundle_view` (function) `lazyc2.py:7702` `def intel_bundle_view()` -- Render the circular/spherical bundle view of the intel graph.
- `attack3d_view` (function) `lazyc2.py:7717` `def attack3d_view()` -- Render the C2-centred attack-surface graph (ReadMenator engine).
- `attack_bundle_view` (function) `lazyc2.py:7736` `def attack_bundle_view()` -- Render the circular/spherical bundle view of the attack surface.
- `api_intel_graph` (function) `lazyc2.py:7751` `def api_intel_graph()` -- Return the fused C2-centred intel graph with precomputed layout.
- `broadcast_view` (function) `lazyc2.py:7807` `def broadcast_view()` -- Render the exploration timeline board for one loop task.
- `api_loop_broadcast_stream` (function) `lazyc2.py:7821` `def api_loop_broadcast_stream()` -- SSE live tail of one loop task's activity stream.
- `api_loop_broadcast` (function) `lazyc2.py:7879` `def api_loop_broadcast()` -- Return the paginated exploration timeline for one loop task.
- `api_guard_audit` (function) `lazyc2.py:7922` `def api_guard_audit()` -- Return guard history with pending approvals kept independent.
- `api_chain_approvals` (function) `lazyc2.py:7968` `def api_chain_approvals()` -- List confirm-step approval requests from the chain approval gate.
- `api_chain_approvals_decide` (function) `lazyc2.py:7996` `def api_chain_approvals_decide(request_id)` -- Approve or deny one pending chain approval request.
- `api_loop_graph` (function) `lazyc2.py:8037` `def api_loop_graph()` -- Return one loop task as ForceGraph-ready nodes/links plus context.
- `api_lazy_mentions` (function) `lazyc2.py:8068` `def api_lazy_mentions()` -- Search @ mention candidates with scroll pagination.
- `api_intel_bundle` (function) `lazyc2.py:8104` `def api_intel_bundle()` -- Return the circular/spherical bundle payload of the intel graph.
- `api_attack_graph` (function) `lazyc2.py:8137` `def api_attack_graph()` -- Return the fused C2-centred attack-surface graph.
- `api_attack_bundle` (function) `lazyc2.py:8189` `def api_attack_bundle()` -- Return the circular/spherical bundle payload of the attack surface.
- `get_data` (function) `lazyc2.py:8219` `def get_data()`
- `upload_zip_file` (function) `lazyc2.py:8228` `def upload_zip_file()` -- Handles the file upload, processes the BloodHound ZIP, and prepares data for visualization.
- `list_campaigns` (function) `lazyc2.py:8286` `def list_campaigns()`
- `create_campaign` (function) `lazyc2.py:8299` `def create_campaign()`
- `lazyphishingai` (function) `lazyc2.py:8377` `def lazyphishingai()`
- `track_pixel` (function) `lazyc2.py:8393` `def track_pixel(campaign_id, email)` -- Píxel de seguimiento para registrar aperturas.
- `campaign_report` (function) `lazyc2.py:8415` `def campaign_report(campaign_id)`
- `orchestrate_campaign` (function) `lazyc2.py:8497` `def orchestrate_campaign(campaign_id)`
- `create_multivector_campaign` (function) `lazyc2.py:8544` `def create_multivector_campaign()`
- `serve_landing_page` (function) `lazyc2.py:8696` `def serve_landing_page(campaign_id, short_url)`
- `health_check` (function) `lazyc2.py:8721` `def health_check()` -- Basic health and readiness endpoint.
- `metrics_exposition` (function) `lazyc2.py:8760` `def metrics_exposition()` -- Prometheus-compatible metrics endpoint.
- `api_dashboard` (function) `lazyc2.py:8767` `def api_dashboard()` -- Aggregated JSON dashboard: beacons, campaign, events, facts summary.
- `api_listeners` (function) `lazyc2.py:8837` `def api_listeners()` -- List all configured C2 listeners and their runtime status.
- `api_listeners_create` (function) `lazyc2.py:8844` `def api_listeners_create()` -- Create a new listener.
- `api_listeners_start` (function) `lazyc2.py:8860` `def api_listeners_start(listener_id)` -- Start an existing listener.
- `api_listeners_stop` (function) `lazyc2.py:8868` `def api_listeners_stop(listener_id)` -- Stop a running listener.
- `api_listeners_delete` (function) `lazyc2.py:8876` `def api_listeners_delete(listener_id)` -- Remove a listener configuration.


Next: [API_p8.md](API_p8.md)
