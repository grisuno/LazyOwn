# API (page 7 of 23)
Previous: [API_p6.md](API_p6.md)

## core/prompt.py
Depends on: `core/config.py`
Imported by: `contrib/legacy/lazybinenc.py`, `key.py`, `static/js/quill-2.0.3.js`
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
Imported by: `cli/banner_config.py`, `cli/commands/misc_migrated.py`, `cli/commands/pwn.py`, `cli/commands/shellsys.py`, `core/process.py`, `core/safe_subprocess.py`, `lazyc2/blueprints/api_v1.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/autonomous_exploit_engine.py`, `modules/chain_runner.py`, `modules/command_executor.py`, `modules/conditional_hooks.py`, `modules/dns_beacon.py`, `modules/metasploitable_migrations.py`, `modules/playbook_engine.py`, `modules/resource_script.py`, `modules/ttpscope_bridge.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_executor_kernel.py`, `tests/test_security_hardening_v4.py`, `tests/test_shell_semantics.py`
- `needs_shell` (function) `core/safe_exec.py:52` `def needs_shell(command)` -- Return True when a command string needs a shell to be interpreted.
- `safe_system` (function) `core/safe_exec.py:69` `def safe_system(command)` -- Execute a fixed command string through the shell safely.
- `safe_run_argv` (function) `core/safe_exec.py:106` `def safe_run_argv(argv)` -- Execute a command via subprocess without shell interpretation.
- `safe_run_shell` (function) `core/safe_exec.py:146` `def safe_run_shell(command)` -- Execute a command through the shell, gated by policy.
- `safe_clear_screen` (function) `core/safe_exec.py:192` `def safe_clear_screen()` -- Clear the terminal screen without using os.system.
- `validate_url` (function) `core/safe_exec.py:207` `def validate_url(url)` -- Validate a URL string, rejecting shell metacharacters.
- `safe_git_clone` (function) `core/safe_exec.py:234` `def safe_git_clone(repo_url, target_dir)` -- Clone a git repository safely using subprocess list-form.
- `safe_ip_show` (function) `core/safe_exec.py:268` `def safe_ip_show(interface)` -- Parse IP addresses from ``ip show`` output in Python.
- `safe_find_tool` (function) `core/safe_exec.py:305` `def safe_find_tool(name)` -- Find a tool on PATH using shutil.which.
- `safe_file_read` (function) `core/safe_exec.py:321` `def safe_file_read(path)` -- Read a file safely with a size limit.

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
Depends on: `cli/auto_crypto.py`, `cli/palette.py`, `cli/palette_command.py`, `core/hardening.py`, `core/logging.py`, `core/parsers.py`, `core/reverse_shell_secret.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/extensions/users.py`, `lazyc2/security/command_allowlist.py`, `lazyc2/security/constants.py`, `lazyc2/security/cors.py`, `lazyc2/security/csrf.py`, `lazyc2/security/html_sanitizer.py`, `lazyc2/security/https_redirect.py`, `lazyc2/security/services.py`, `lazyc2/security/trusted_proxy.py`, `lazyc2/security/validators.py`, `lazyown.py`, `modules/attack_surface3d.py`, `modules/backdoor/server.c`, `modules/beacon_history.py`, `modules/c2_surfaces.py`, `modules/collab_bp.py`, `modules/colors.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/dashboard_bp.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/event_engine.py`, `modules/intel_fusion.py`, `modules/kill_chain_viz.py`, `modules/killchain.py`, `modules/lazy_loop.py`, `modules/lazy_mentions.py`, `modules/lazy_rbac.py`, `modules/listener_manager.py`, `modules/live_surface.py`, `modules/llm_adapter.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/security_sanitizers.py`, `modules/state_manager.py`, `modules/world_model.py`, `skills/daemon_health.py`, `skills/lazyown_facts.py`, `utils.py`
- `is_insecure_credential` (function) `lazyc2.py:204` `def is_insecure_credential(user, pwd)` -- Check for weak or default credentials
- `_JsonLogFormatter.format` (method) `lazyc2.py:444` `def format(self, record)`
- `ensure_sessions_dir` (function) `lazyc2.py:471` `def ensure_sessions_dir()` -- Ensure the sessions directory exists with safe permissions.
- `load_routes` (function) `lazyc2.py:482` `def load_routes()` -- Load dynamic routes from JSON file.
- `save_routes` (function) `lazyc2.py:492` `def save_routes(routes)` -- Save dynamic routes to JSON file with safe permissions.
- `validate_route_path` (function) `lazyc2.py:506` `def validate_route_path(route_path)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_route_path`.
- `validate_template_name` (function) `lazyc2.py:519` `def validate_template_name(template_name)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_template_name`.
- `is_safe_template_path` (function) `lazyc2.py:529` `def is_safe_template_path(template_path, template_name)` -- Verify ``template_path`` resolves inside ``app.template_folder``.
- `is_binary` (function) `lazyc2.py:569` `def is_binary(safe_filename)` -- Check whether a session file is binary based on its header bytes.
- `clean_expired_tokens` (function) `lazyc2.py:610` `def clean_expired_tokens()`
- `clean_json` (function) `lazyc2.py:618` `def clean_json(text)` -- Extract only the JSON content between ```json and ```, discarding everything else.
- `load_yaml_safely` (function) `lazyc2.py:646` `def load_yaml_safely(file_path)` -- Load a YAML file safely with error handling and default values.
- `Handler.on_any_event` (method) `lazyc2.py:730` `def on_any_event(event)`
- `get_karma_name` (function) `lazyc2.py:755` `def get_karma_name(elo)`
- `fromjson` (function) `lazyc2.py:772` `def fromjson(value)`
- `run_shell` (function) `lazyc2.py:776` `def run_shell()`
- `load_banners` (function) `lazyc2.py:786` `def load_banners()` -- Loads the banners from the JSON file.
- `load_mitre_data` (function) `lazyc2.py:806` `def load_mitre_data()`
- `load_event_config` (function) `lazyc2.py:812` `def load_event_config()`
- `load_notifications` (function) `lazyc2.py:820` `def load_notifications()`
- `implants_check` (function) `lazyc2.py:838` `def implants_check()`
- `extract_attack_vectors` (function) `lazyc2.py:855` `def extract_attack_vectors(nodes, edges)` -- Analyzes BloodHound nodes and edges to extract critical attack vectors for AD compromise.
- `process_bloodhound_zip` (function) `lazyc2.py:942` `def process_bloodhound_zip(zip_filepath)` -- Processes a BloodHound ZIP file to extract nodes and edges for graph visualization.
- `start_watching` (function) `lazyc2.py:1040` `def start_watching()`
- `load_tasks` (function) `lazyc2.py:1056` `def load_tasks()`
- `create_cves` (function) `lazyc2.py:1064` `def create_cves()`
- `load_cves` (function) `lazyc2.py:1070` `def load_cves()`
- `save_cves` (function) `lazyc2.py:1078` `def save_cves(cves)`
- `create_report` (function) `lazyc2.py:1083` `def create_report()`
- `save_tasks` (function) `lazyc2.py:1089` `def save_tasks(tasks)`
- `load_note` (function) `lazyc2.py:1094` `def load_note()`
- `aumentar_elo` (function) `lazyc2.py:1112` `def aumentar_elo(user_id, cantidad)`
- `save_note` (function) `lazyc2.py:1142` `def save_note(content)`
- `escape_js` (function) `lazyc2.py:1148` `def escape_js(s)`
- `markdown_to_html` (function) `lazyc2.py:1185` `def markdown_to_html(text)`
- `to_serializable` (function) `lazyc2.py:1193` `def to_serializable(obj)` -- Convert objects to serializable format.
- `make_serializable` (function) `lazyc2.py:1200` `def make_serializable(data)` -- Recursively convert data to serializable format.
- `datetime_now_iso` (function) `lazyc2.py:1218` `def datetime_now_iso()` -- Return the current UTC timestamp as an ISO-8601 string.
- `escape_js_string` (function) `lazyc2.py:1336` `def escape_js_string(value)` -- Escape special characters in a string for JavaScript.
- `check_auth` (function) `lazyc2.py:1348` `def check_auth(username, password)` -- Verify credentials.
- `authenticate` (function) `lazyc2.py:1363` `def authenticate()` -- Requests authentication.
- `requires_auth_or_session` (function) `lazyc2.py:1372` `def requires_auth_or_session(f)` -- Require Basic auth credentials or a valid Flask-Login session.
- `decorated` (function) `lazyc2.py:1382` `def decorated()`
- `requires_auth` (function) `lazyc2.py:1393` `def requires_auth(f)`
- `decorated` (function) `lazyc2.py:1395` `def decorated()`
- `csrf_protect` (function) `lazyc2.py:1404` `def csrf_protect(view)` -- Decorator that enforces the per-session CSRF token.
- `wrapper` (function) `lazyc2.py:1414` `def wrapper()`
- `aicmd_deepseek` (function) `lazyc2.py:1425` `def aicmd_deepseek(cmd)`
- `aicmd` (function) `lazyc2.py:1539` `def aicmd(cmd)`
- `search_database` (function) `lazyc2.py:1644` `def search_database(term, data_path)` -- Busca un término en un DataFrame, manejando listas, dicts y distintas estructuras.
- `execute_command` (function) `lazyc2.py:1699` `def execute_command(command)`
- `CustomDNSResolver.resolve` (method) `lazyc2.py:1729` `def resolve(self, request, handler)`
- `start_dns_server` (function) `lazyc2.py:1833` `def start_dns_server()` -- Start the C2 DNS server, gracefully degrading when binding is unsafe.
- `tcp_bridge` (function) `lazyc2.py:1873` `def tcp_bridge(local_port, remote_host, remote_port)` -- Establish a TCP bridge between a local port and a remote host.
- `handle_client` (function) `lazyc2.py:1897` `def handle_client(client_socket, remote_host, remote_port)` -- Handle communication between the client and the remote server.
- `decoy` (function) `lazyc2.py:1916` `def decoy()` -- Serve a decoy page to non-operator IPs when decoy mode is enabled.
- `encrypt_data` (function) `lazyc2.py:1954` `def encrypt_data(data)`
- `decrypt_data` (function) `lazyc2.py:1963` `def decrypt_data(encrypted_data, is_file)`
- `set_winsize` (function) `lazyc2.py:1976` `def set_winsize(fd, row, col, xpix, ypix)` -- Configura el tamaño de la terminal
- `read_and_forward_pty_output` (function) `lazyc2.py:1982` `def read_and_forward_pty_output()` -- Lectura continua del PTY y envío por WebSocket
- `get_discovered_hosts` (function) `lazyc2.py:1999` `def get_discovered_hosts()` -- Reads the sessions/hostsdiscovery.txt file and returns a list of discovered hosts.
- `get_local_ip_addresses` (function) `lazyc2.py:2049` `def get_local_ip_addresses()`
- `sanitize_json` (function) `lazyc2.py:2074` `def sanitize_json(data)` -- Elimina datos sensibles del diccionario JSON.
- `add_dynamic_data` (function) `lazyc2.py:2104` `def add_dynamic_data(data)` -- Agrega datos dinámicos al diccionario JSON si es necesario, basándose en el contenido del diccionario 'data'.
- `get_client_ip` (function) `lazyc2.py:2126` `def get_client_ip()` -- Get the client's IP address, handling proxies.
- `get_request_details` (function) `lazyc2.py:2135` `def get_request_details()` -- Collect comprehensive request details.
- `save_to_log` (function) `lazyc2.py:2170` `def save_to_log(data)` -- Append request data to the JSON log file with safe permissions.
- `parse_access_log_for_short_url` (function) `lazyc2.py:2192` `def parse_access_log_for_short_url(short_url)` -- Parse access.log for entries matching the given short URL.
- `parse_execution_log` (function) `lazyc2.py:2214` `def parse_execution_log(implante)` -- Parse execution log for the given implante, returning execution events.
- `load_implant_config` (function) `lazyc2.py:2240` `def load_implant_config(implante)` -- Load implant configuration from JSON file.
- `load_short_urls` (function) `lazyc2.py:2250` `def load_short_urls()` -- Load short URLs from JSON file, creating it if it doesn't exist.
- `save_short_urls` (function) `lazyc2.py:2270` `def save_short_urls(data)` -- Save short URLs to JSON file.
- `is_valid_url` (function) `lazyc2.py:2280` `def is_valid_url(url)` -- Validate if the input is a valid URL or existing local file path.
- `get_safe_file_path` (function) `lazyc2.py:2288` `def get_safe_file_path(user_path)` -- Construye de forma segura el path del archivo y verifica que está en el directorio permitido.
- `analyze_behavioral_data` (function) `lazyc2.py:2358` `def analyze_behavioral_data(behavioral_events)` -- Analyze behavioral events using Groq AI to generate risk scores.
- `analyze_campaign_progress` (function) `lazyc2.py:2386` `def analyze_campaign_progress(campaign_id, events)` -- Analyze campaign progress and suggest adaptations using Grok AI.
- `User.__init__` (method) `lazyc2.py:2974` `def __init__(self, user_data)`
- `load_users` (function) `lazyc2.py:2996` `def load_users()`
- `save_users` (function) `lazyc2.py:3006` `def save_users(users)`
- `load_data` (function) `lazyc2.py:3017` `def load_data()`
- `load_user` (function) `lazyc2.py:3034` `def load_user(user_id)`
- `tojson_filter` (function) `lazyc2.py:3049` `def tojson_filter(value)` -- Custom tojson filter to handle non-serializable objects.
- `index` (function) `lazyc2.py:3056` `def index()`
- `send_command` (function) `lazyc2.py:3207` `def send_command(client_id)`
- `receive_result` (function) `lazyc2.py:3352` `def receive_result(client_id)`
- `issue_command` (function) `lazyc2.py:3893` `def issue_command()`
- `upload` (function) `lazyc2.py:3907` `def upload()`
- `download_file` (function) `lazyc2.py:3944` `def download_file()`
- `serve_file` (function) `lazyc2.py:3971` `def serve_file(file_path)` -- Serve a file from ``sessions/temp_uploads`` through :class:`SafeFileService`.
- `create_route` (function) `lazyc2.py:4073` `def create_route()` -- Register a new operator-supplied dynamic route bound to a template.
- `dynamic_route` (function) `lazyc2.py:4142` `def dynamic_route(route_path, data)` -- Handle dynamic routes based on stored route-to-template mappings.
- `sanitize_input` (function) `lazyc2.py:4149` `def sanitize_input(input_str)` -- Sanitize input to prevent XSS attacks.
- `is_valid_route_path` (function) `lazyc2.py:4159` `def is_valid_route_path(route_path)` -- Validate route path format.
- `is_valid_data` (function) `lazyc2.py:4166` `def is_valid_data(data)` -- Validate data parameter.
- `is_valid_template_name` (function) `lazyc2.py:4176` `def is_valid_template_name(template_name)` -- Validate template name.
- `log` (function) `lazyc2.py:4238` `def log(data)` -- Log request details to JSON file.
- `favicon` (function) `lazyc2.py:4256` `def favicon()` -- Serve the favicon.ico file.
- `palette_view` (function) `lazyc2.py:4269` `def palette_view()` -- Render the operator command palette browser.
- `palette_api` (function) `lazyc2.py:4297` `def palette_api()` -- JSON catalogue feed for the global Cmd+K / Ctrl+K overlay.
- `api_data` (function) `lazyc2.py:4318` `def api_data()`
- `create_short_url` (function) `lazyc2.py:4480` `def create_short_url()` -- Create multiple short URLs for a single original URL.
- `track_interaction` (function) `lazyc2.py:4508` `def track_interaction(short_url)` -- Serve tracking page and log behavioral data.
- `update_short_url` (function) `lazyc2.py:4533` `def update_short_url(short_url)`
- `redirect_to_file` (function) `lazyc2.py:4560` `def redirect_to_file(short_url)`
- `webserver_report` (function) `lazyc2.py:4588` `def webserver_report(filename)` -- Serve nmap HTML report assets from the sessions directory over HTTPS.
- `download_files` (function) `lazyc2.py:4608` `def download_files(filename)` -- Serve implant stage files by name, enforcing strict containment.
- `view_yaml` (function) `lazyc2.py:4660` `def view_yaml()`
- `run_command` (function) `lazyc2.py:4754` `def run_command()` -- Execute one shell command and return a sanitised, JSON-safe result.
- `get_output` (function) `lazyc2.py:4823` `def get_output()`
- `run_shellcode` (function) `lazyc2.py:4850` `def run_shellcode()`
- `get_results` (function) `lazyc2.py:4859` `def get_results()`
- `send_lcommand` (function) `lazyc2.py:4957` `def send_lcommand(ip, port)`
- `chatbot` (function) `lazyc2.py:4990` `def chatbot()`
- `vuln` (function) `lazyc2.py:5006` `def vuln()`
- `taskbot` (function) `lazyc2.py:5045` `def taskbot()`
- `search` (function) `lazyc2.py:5061` `def search()`
- `script` (function) `lazyc2.py:5077` `def script()`
- `redop` (function) `lazyc2.py:5093` `def redop()`
- `adversary` (function) `lazyc2.py:5112` `def adversary()`
- `generalbot` (function) `lazyc2.py:5128` `def generalbot()`
- `csv_to_html` (function) `lazyc2.py:5144` `def csv_to_html()`
- `search_results` (function) `lazyc2.py:5195` `def search_results()`
- `graph` (function) `lazyc2.py:5243` `def graph()`
- `task` (function) `lazyc2.py:5252` `def task(task_id)`
- `get_tasks` (function) `lazyc2.py:5267` `def get_tasks()`
- `tasks` (function) `lazyc2.py:5277` `def tasks()`
- `edit_task` (function) `lazyc2.py:5306` `def edit_task(task_id)`
- `cves` (function) `lazyc2.py:5340` `def cves()`
- `cve` (function) `lazyc2.py:5366` `def cve(cve_id)`
- `edit_cve` (function) `lazyc2.py:5381` `def edit_cve(cve_id)`
- `edit_notes` (function) `lazyc2.py:5415` `def edit_notes()`
- `get_notes` (function) `lazyc2.py:5433` `def get_notes()`
- `view_note` (function) `lazyc2.py:5443` `def view_note()`
- `push_notification` (function) `lazyc2.py:5453` `def push_notification()`
- `edit_event` (function) `lazyc2.py:5480` `def edit_event(event_name)`
- `get_event_config` (function) `lazyc2.py:5515` `def get_event_config()`
- `get_event_config_view` (function) `lazyc2.py:5522` `def get_event_config_view()`
- `aicmd_view` (function) `lazyc2.py:5557` `def aicmd_view()`
- `get_events` (function) `lazyc2.py:5582` `def get_events()`
- `list_tools` (function) `lazyc2.py:5614` `def list_tools()`
- `create_tool` (function) `lazyc2.py:5624` `def create_tool()`
- `view_tool` (function) `lazyc2.py:5651` `def view_tool(toolname)`
- `update_tool` (function) `lazyc2.py:5682` `def update_tool(toolname)`
- `delete_tool` (function) `lazyc2.py:5730` `def delete_tool(toolname)`
- `register` (function) `lazyc2.py:5765` `def register()`
- `login` (function) `lazyc2.py:5824` `def login()`
- `mfa_setup` (function) `lazyc2.py:5871` `def mfa_setup()`
- `mfa_qr` (function) `lazyc2.py:5945` `def mfa_qr(username)` -- Serve a locally-generated QR code SVG for MFA setup.
- `mfa_verify` (function) `lazyc2.py:5967` `def mfa_verify()`
- `admin_users` (function) `lazyc2.py:6015` `def admin_users()`
- `admin_set_role` (function) `lazyc2.py:6030` `def admin_set_role(user_id)`
- `admin_reset_mfa` (function) `lazyc2.py:6052` `def admin_reset_mfa(user_id)`
- `admin_delete_user` (function) `lazyc2.py:6064` `def admin_delete_user(user_id)`
- `admin_tenants` (function) `lazyc2.py:6082` `def admin_tenants()`
- `admin_create_tenant` (function) `lazyc2.py:6103` `def admin_create_tenant()`
- `admin_switch_tenant` (function) `lazyc2.py:6123` `def admin_switch_tenant(tenant_id)`
- `profile` (function) `lazyc2.py:6138` `def profile()`
- `logout` (function) `lazyc2.py:6162` `def logout()`
- `change_password` (function) `lazyc2.py:6177` `def change_password()` -- Force rotation of the initial one-time admin password.
- `aumentar_elo_route` (function) `lazyc2.py:6243` `def aumentar_elo_route(user_id)`
- `banners` (function) `lazyc2.py:6259` `def banners()`
- `mitre` (function) `lazyc2.py:6295` `def mitre()`
- `get_connected_clients` (function) `lazyc2.py:6340` `def get_connected_clients()`
- `lazybot` (function) `lazyc2.py:6351` `def lazybot()`
- `compliance_dashboard` (function) `lazyc2.py:6368` `def compliance_dashboard()`
- `compliance_report` (function) `lazyc2.py:6390` `def compliance_report()`
- `compliance_add_evidence` (function) `lazyc2.py:6420` `def compliance_add_evidence()`
- `compliance_verify_evidence` (function) `lazyc2.py:6456` `def compliance_verify_evidence()`
- `compliance_export` (function) `lazyc2.py:6470` `def compliance_export(format)`
- `lazyreport` (function) `lazyc2.py:6500` `def lazyreport()`
- `teamserver` (function) `lazyc2.py:6519` `def teamserver()`
- `report` (function) `lazyc2.py:6548` `def report()`
- `lazyreport_view` (function) `lazyc2.py:6555` `def lazyreport_view()`
- `killchain_view` (function) `lazyc2.py:6561` `def killchain_view()`
- `api_killchain` (function) `lazyc2.py:6591` `def api_killchain()` -- Return the unified kill-chain snapshot consumed by every surface.
- `api_beacon_results` (function) `lazyc2.py:6622` `def api_beacon_results(client_id)` -- Return the full ordered command/result history for one beacon.
- `connect` (function) `lazyc2.py:6722` `def connect()`
- `listener` (function) `lazyc2.py:6731` `def listener()`
- `listener_connect` (function) `lazyc2.py:6740` `def listener_connect()`
- `listener_disconnect` (function) `lazyc2.py:6751` `def listener_disconnect()`
- `pty_input` (function) `lazyc2.py:6761` `def pty_input(data)`
- `resize` (function) `lazyc2.py:6775` `def resize(data)`
- `pty_connect` (function) `lazyc2.py:6788` `def pty_connect()`
- `handle_input` (function) `lazyc2.py:6819` `def handle_input(data)`
- `listener_command` (function) `lazyc2.py:6843` `def listener_command(msg)`
- `terminal` (function) `lazyc2.py:6857` `def terminal()`
- `terminal_connect` (function) `lazyc2.py:6866` `def terminal_connect()`
- `terminal_disconnect` (function) `lazyc2.py:6876` `def terminal_disconnect()`
- `terminal_input` (function) `lazyc2.py:6886` `def terminal_input(data)`
- `terminal_command` (function) `lazyc2.py:6899` `def terminal_command(data)`
- `terminal_resize` (function) `lazyc2.py:6914` `def terminal_resize(data)`
- `start_reverse_shell` (function) `lazyc2.py:6923` `def start_reverse_shell()`
- `start_bridge` (function) `lazyc2.py:6970` `def start_bridge()` -- Start a TCP bridge to a specified remote host and port.
- `page_not_found` (function) `lazyc2.py:6987` `def page_not_found(e)`
- `internal_server_error` (function) `lazyc2.py:6995` `def internal_server_error(e)`
- `get_config` (function) `lazyc2.py:7004` `def get_config()` -- Lee el archivo payload.json, lo manipula y lo expone como /config.json.
- `capture_image` (function) `lazyc2.py:7023` `def capture_image()`
- `capture_audio` (function) `lazyc2.py:7049` `def capture_audio()`
- `surface` (function) `lazyc2.py:7067` `def surface()`
- `surface_live` (function) `lazyc2.py:7073` `def surface_live()` -- Render the live attack-surface graph page.
- `api_surface_live` (function) `lazyc2.py:7088` `def api_surface_live()` -- Return the live attack-surface graph derived from the world model.
- `intel_view` (function) `lazyc2.py:7113` `def intel_view()` -- Render the fused sessions intel graph page (ReadMenator engine).
- `intel_bundle_view` (function) `lazyc2.py:7132` `def intel_bundle_view()` -- Render the circular/spherical bundle view of the intel graph.
- `attack3d_view` (function) `lazyc2.py:7147` `def attack3d_view()` -- Render the C2-centred attack-surface graph (ReadMenator engine).
- `attack_bundle_view` (function) `lazyc2.py:7166` `def attack_bundle_view()` -- Render the circular/spherical bundle view of the attack surface.
- `api_intel_graph` (function) `lazyc2.py:7181` `def api_intel_graph()` -- Return the fused C2-centred intel graph with precomputed layout.
- `broadcast_view` (function) `lazyc2.py:7237` `def broadcast_view()` -- Render the exploration timeline board for one loop task.
- `api_loop_broadcast_stream` (function) `lazyc2.py:7251` `def api_loop_broadcast_stream()` -- SSE live tail of one loop task's activity stream.
- `api_loop_broadcast` (function) `lazyc2.py:7309` `def api_loop_broadcast()` -- Return the paginated exploration timeline for one loop task.
- `api_guard_audit` (function) `lazyc2.py:7352` `def api_guard_audit()` -- Return guard history with pending approvals kept independent.
- `api_loop_graph` (function) `lazyc2.py:7398` `def api_loop_graph()` -- Return one loop task as ForceGraph-ready nodes/links plus context.
- `api_lazy_mentions` (function) `lazyc2.py:7429` `def api_lazy_mentions()` -- Search @ mention candidates with scroll pagination.
- `api_intel_bundle` (function) `lazyc2.py:7465` `def api_intel_bundle()` -- Return the circular/spherical bundle payload of the intel graph.
- `api_attack_graph` (function) `lazyc2.py:7498` `def api_attack_graph()` -- Return the fused C2-centred attack-surface graph.
- `api_attack_bundle` (function) `lazyc2.py:7550` `def api_attack_bundle()` -- Return the circular/spherical bundle payload of the attack surface.
- `get_data` (function) `lazyc2.py:7580` `def get_data()`
- `upload_zip_file` (function) `lazyc2.py:7589` `def upload_zip_file()` -- Handles the file upload, processes the BloodHound ZIP, and prepares data for visualization.
- `list_campaigns` (function) `lazyc2.py:7647` `def list_campaigns()`
- `create_campaign` (function) `lazyc2.py:7660` `def create_campaign()`
- `lazyphishingai` (function) `lazyc2.py:7738` `def lazyphishingai()`
- `track_pixel` (function) `lazyc2.py:7754` `def track_pixel(campaign_id, email)` -- Píxel de seguimiento para registrar aperturas.
- `campaign_report` (function) `lazyc2.py:7776` `def campaign_report(campaign_id)`
- `orchestrate_campaign` (function) `lazyc2.py:7858` `def orchestrate_campaign(campaign_id)`
- `create_multivector_campaign` (function) `lazyc2.py:7905` `def create_multivector_campaign()`
- `serve_landing_page` (function) `lazyc2.py:8057` `def serve_landing_page(campaign_id, short_url)`
- `health_check` (function) `lazyc2.py:8082` `def health_check()` -- Basic health and readiness endpoint.
- `metrics_exposition` (function) `lazyc2.py:8121` `def metrics_exposition()` -- Prometheus-compatible metrics endpoint.
- `api_dashboard` (function) `lazyc2.py:8128` `def api_dashboard()` -- Aggregated JSON dashboard: beacons, campaign, events, facts summary.
- `api_listeners` (function) `lazyc2.py:8198` `def api_listeners()` -- List all configured C2 listeners and their runtime status.
- `api_listeners_create` (function) `lazyc2.py:8205` `def api_listeners_create()` -- Create a new listener.
- `api_listeners_start` (function) `lazyc2.py:8221` `def api_listeners_start(listener_id)` -- Start an existing listener.
- `api_listeners_stop` (function) `lazyc2.py:8229` `def api_listeners_stop(listener_id)` -- Stop a running listener.
- `api_listeners_delete` (function) `lazyc2.py:8237` `def api_listeners_delete(listener_id)` -- Remove a listener configuration.

## lazyc2/addon_creator.py
Imported by: `lazyc2/blueprints/addons.py`, `tests/test_addon_creator.py`, `tests/test_placeholder_coverage.py`
- `ParamSpec.to_dict` (method) `lazyc2/addon_creator.py:363` `def to_dict(self)` -- Return the param as a schema-ordered mapping.
- `AddonValidationError.__init__` (method) `lazyc2/addon_creator.py:419` `def __init__(self, issues)`
- `AddonValidator.__init__` (method) `lazyc2/addon_creator.py:432` `def __init__(self, draft, config)` -- Store the draft and configuration used by every check.
- `AddonValidator.validate` (method) `lazyc2/addon_creator.py:446` `def validate(self)` -- Run every rule and return the collected issues.
- `AddonValidator.is_valid` (method) `lazyc2/addon_creator.py:460` `def is_valid(self)` -- Return True when the draft passes every rule.
- `AddonYamlRenderer.__init__` (method) `lazyc2/addon_creator.py:731` `def __init__(self, config)` -- Store the configuration used for defaults.
- `AddonYamlRenderer.render` (method) `lazyc2/addon_creator.py:739` `def render(self, draft)` -- Return the YAML document for the draft.
- `AddonYamlRenderer.to_document` (method) `lazyc2/addon_creator.py:757` `def to_document(self, draft)` -- Build the schema-ordered document mapping for the draft.
- `AddonStore.__init__` (method) `lazyc2/addon_creator.py:822` `def __init__(self, config, base_dir)` -- Configure the store.
- `AddonStore.resolve_path` (method) `lazyc2/addon_creator.py:837` `def resolve_path(self, name)` -- Return the safe absolute path for a newly created addon name.
- `AddonStore.resolve_existing_path` (method) `lazyc2/addon_creator.py:852` `def resolve_existing_path(self, name)` -- Return the safe absolute path for an existing addon file.
- `AddonStore.exists` (method) `lazyc2/addon_creator.py:896` `def exists(self, name)` -- Return True when an addon file already exists for the name.
- `AddonStore.save` (method) `lazyc2/addon_creator.py:907` `def save(self, name, yaml_text)` -- Persist the YAML document atomically.
- `AddonStore.load` (method) `lazyc2/addon_creator.py:961` `def load(self, name)` -- Return the parsed addon document for a name.
- `AddonStore.delete` (method) `lazyc2/addon_creator.py:984` `def delete(self, name)` -- Delete the addon file for a name.
- `AddonStore.list_all` (method) `lazyc2/addon_creator.py:1000` `def list_all(self)` -- Return summary dicts for every parseable addon.
- `parse_addon_form` (function) `lazyc2/addon_creator.py:1080` `def parse_addon_form(form)` -- Adapt raw form data into an AddonDraft.

## lazyc2/app_factory.py
Depends on: `core/api_authz.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/blueprints/orchestrator.py`, `lazyc2/extensions/__init__.py`, `lazyc2/security/services.py`, `modules/lazy_rbac.py`
- `create_app` (function) `lazyc2/app_factory.py:90` `def create_app()` -- Create and return a fully configured C2 Flask application.
- `_FactoryUser.__init__` (method) `lazyc2/app_factory.py:142` `def __init__(self, data)`

## lazyc2/blueprints/addons.py
Depends on: `core/logging.py`, `lazyc2/addon_creator.py`, `lazyc2/blueprints/session_auth.py`, `lazyc2/extensions/decoy.py`, `lazyc2/security/csrf.py`
Imported by: `lazyc2/blueprints/__init__.py`, `tests/test_addon_creator.py`, `tests/test_security_hardening_v5.py`
- `init_addons_bp` (function) `lazyc2/blueprints/addons.py:69` `def init_addons_bp(base_dir)` -- Configure the blueprint state before registration.
- `csrf_protect` (function) `lazyc2/blueprints/addons.py:96` `def csrf_protect(view)` -- Decorate a view so mutating requests must echo the CSRF token.
- `wrapper` (function) `lazyc2/blueprints/addons.py:110` `def wrapper()`
- `list_addons` (function) `lazyc2/blueprints/addons.py:263` `def list_addons()` -- Render the addon dashboard list page with a fresh CSRF token.
- `create_addon` (function) `lazyc2/blueprints/addons.py:277` `def create_addon()` -- Render the creation form and persist valid addon submissions.
- `view_addon` (function) `lazyc2/blueprints/addons.py:321` `def view_addon(name)` -- Render the persisted YAML document for an addon.
- `delete_addon` (function) `lazyc2/blueprints/addons.py:345` `def delete_addon(name)` -- Delete an addon file.


Next: [API_p8.md](API_p8.md)
