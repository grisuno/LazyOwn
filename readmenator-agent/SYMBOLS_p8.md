# Symbols (page 8 of 46)
Previous: [SYMBOLS_p7.md](SYMBOLS_p7.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `generate` | method | `core/llm_budget.py:61` | `def generate(self, prompt)` |
| `generate` | method | `core/llm_budget.py:422` | `def generate(self, prompt)` |
| `load_budget_config` | function | `core/llm_budget.py:552` | `def load_budget_config(payload, sessions_dir)` |
| `price_for` | method | `core/llm_budget.py:329` | `def price_for(self, model)` |
| `read_budget_status` | function | `core/llm_budget.py:585` | `def read_budget_status(payload, sessions_dir)` |
| `record` | method | `core/llm_budget.py:232` | `def record(self, entry)` |
| `reset` | method | `core/llm_budget.py:261` | `def reset(self)` |
| `spent_today` | method | `core/llm_budget.py:251` | `def spent_today(self)` |
| `stream_generate` | method | `core/llm_budget.py:63` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `core/llm_budget.py:430` | `def stream_generate(self, prompt)` |
| `wrap_backend_with_budget` | function | `core/llm_budget.py:657` | `def wrap_backend_with_budget(backend, config, estimator, model, ledger)` |
| `StructuredLogConfig` | class | `core/logging.py:42` | `class StructuredLogConfig` |
| `StructuredLogger` | class | `core/logging.py:139` | `class StructuredLogger(Logger)` |
| `_ConsoleFormatter` | class | `core/logging.py:121` | `class _ConsoleFormatter(Formatter)` |
| `_JsonLineFormatter` | class | `core/logging.py:71` | `class _JsonLineFormatter(Formatter)` |
| `__init__` | method | `core/logging.py:74` | `def __init__(self, redacted_fields)` |
| `_log_factory` | function | `core/logging.py:180` | `def _log_factory(name, config)` |
| `format` | method | `core/logging.py:78` | `def format(self, record)` |
| `format` | method | `core/logging.py:132` | `def format(self, record)` |
| `get_logger` | function | `core/logging.py:231` | `def get_logger(name)` |
| `install_json_handler` | function | `core/logging.py:251` | `def install_json_handler(name, config)` |
| `makeRecord` | method | `core/logging.py:148` | `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)` |
| `reconfigure` | function | `core/logging.py:300` | `def reconfigure(config)` |
| `create_arp_packet` | function | `core/network.py:33` | `def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac)` |
| `get_banner` | function | `core/network.py:134` | `def get_banner(ip, port)` |
| `get_network_info` | function | `core/network.py:154` | `def get_network_info()` |
| `get_open_ports` | function | `core/network.py:105` | `def get_open_ports()` |
| `is_port_in_use` | function | `core/network.py:120` | `def is_port_in_use(port, host)` |
| `parse_ip_mac` | function | `core/network.py:18` | `def parse_ip_mac(input_string)` |
| `parse_proc_net_file` | function | `core/network.py:78` | `def parse_proc_net_file(file_path)` |
| `send_packet` | function | `core/network.py:66` | `def send_packet(packet, iface)` |
| `OperatorParam` | class | `core/param_registry.py:114` | `class OperatorParam` |
| `_entry_to_param` | function | `core/param_registry.py:204` | `def _entry_to_param(name, entry)` |
| `_write` | function | `core/param_registry.py:482` | `def _write(entries, root)` |
| `apply_to_schema` | function | `core/param_registry.py:437` | `def apply_to_schema(root)` |
| `as_entry` | method | `core/param_registry.py:133` | `def as_entry(self)` |
| `create_param` | function | `core/param_registry.py:291` | `def create_param(name, kind, default, description, category, root)` |
| `delete_param` | function | `core/param_registry.py:387` | `def delete_param(name, root)` |
| `effective_value` | function | `core/param_registry.py:187` | `def effective_value(entry)` |
| `list_params` | function | `core/param_registry.py:256` | `def list_params(root, include_builtin, keyword)` |
| `load_entries` | function | `core/param_registry.py:226` | `def load_entries(root)` |
| `normalise_kind` | function | `core/param_registry.py:172` | `def normalise_kind(kind)` |
| `operator_specs` | function | `core/param_registry.py:425` | `def operator_specs(root)` |
| `param_value` | function | `core/param_registry.py:411` | `def param_value(name, root)` |
| `registry_path` | function | `core/param_registry.py:158` | `def registry_path(root)` |
| `sync_shell_params` | function | `core/param_registry.py:459` | `def sync_shell_params(shell, root)` |
| `to_spec` | method | `core/param_registry.py:142` | `def to_spec(self)` |
| `update_param` | function | `core/param_registry.py:341` | `def update_param(name, default, description, kind, category, root)` |
| `strip_ansi` | function | `core/parsers.py:15` | `def strip_ansi(text)` |
| `FieldKind` | class | `core/payload_schema.py:77` | `class FieldKind(StrEnum)` |
| `FieldSpec` | class | `core/payload_schema.py:104` | `class FieldSpec` |
| `Severity` | class | `core/payload_schema.py:95` | `class Severity(StrEnum)` |
| `ValidationIssue` | class | `core/payload_schema.py:146` | `class ValidationIssue` |
| `_coerce_bool` | function | `core/payload_schema.py:320` | `def _coerce_bool(raw)` |
| `_coerce_int` | function | `core/payload_schema.py:305` | `def _coerce_int(raw)` |
| `_load_operator_specs` | function | `core/payload_schema.py:2066` | `def _load_operator_specs()` |
| `_spec` | function | `core/payload_schema.py:339` | `def _spec(name, kind, default, description)` |
| `_validate_bool` | function | `core/payload_schema.py:199` | `def _validate_bool(value)` |
| `_validate_hex` | function | `core/payload_schema.py:258` | `def _validate_hex(value)` |
| `_validate_hostname` | function | `core/payload_schema.py:224` | `def _validate_hostname(value)` |
| `_validate_int` | function | `core/payload_schema.py:175` | `def _validate_int(value)` |
| `_validate_interface` | function | `core/payload_schema.py:250` | `def _validate_interface(value)` |
| `_validate_ip` | function | `core/payload_schema.py:216` | `def _validate_ip(value)` |
| `_validate_json_blob` | function | `core/payload_schema.py:272` | `def _validate_json_blob(value)` |
| `_validate_opaque` | function | `core/payload_schema.py:284` | `def _validate_opaque(_value)` |
| `_validate_os_id` | function | `core/payload_schema.py:266` | `def _validate_os_id(value)` |
| `_validate_path` | function | `core/payload_schema.py:244` | `def _validate_path(value)` |
| `_validate_port` | function | `core/payload_schema.py:189` | `def _validate_port(value)` |
| `_validate_string` | function | `core/payload_schema.py:169` | `def _validate_string(value)` |
| `_validate_url` | function | `core/payload_schema.py:236` | `def _validate_url(value)` |
| `categories` | function | `core/payload_schema.py:2054` | `def categories()` |
| `coerce_value` | function | `core/payload_schema.py:1896` | `def coerce_value(key, raw)` |
| `default_payload` | function | `core/payload_schema.py:2046` | `def default_payload()` |
| `field_for` | function | `core/payload_schema.py:1891` | `def field_for(key)` |
| `format_issue` | function | `core/payload_schema.py:2028` | `def format_issue(issue)` |
| `register_specs` | function | `core/payload_schema.py:1850` | `def register_specs(specs)` |
| `unregister_specs` | function | `core/payload_schema.py:1873` | `def unregister_specs(keys)` |
| `validate_payload` | function | `core/payload_schema.py:1993` | `def validate_payload(payload)` |
| `validate_value` | function | `core/payload_schema.py:1919` | `def validate_value(key, value)` |
| `_drain_stderr` | function | `core/process.py:220` | `def _drain_stderr()` |
| `_print_run_command_status` | function | `core/process.py:159` | `def _print_run_command_status(command, elapsed, exit_code)` |
| `activate_server` | function | `core/process.py:271` | `def activate_server(httpd, url, lhost)` |
| `check_go_tool_installed` | function | `core/process.py:34` | `def check_go_tool_installed(tool_name)` |
| `check_sudo` | function | `core/process.py:97` | `def check_sudo()` |
| `ensure_tmux_session` | function | `core/process.py:253` | `def ensure_tmux_session(session_name)` |
| `handle_multiple_rhosts` | function | `core/process.py:68` | `def handle_multiple_rhosts(func)` |
| `is_binary_present` | function | `core/process.py:54` | `def is_binary_present(binary_name)` |
| `is_package_installed` | function | `core/process.py:143` | `def is_package_installed(package_name)` |
| `run` | function | `core/process.py:108` | `def run(command)` |
| `run_command` | function | `core/process.py:183` | `def run_command(command, timeout)` |
| `wrapper` | function | `core/process.py:82` | `def wrapper(self)` |
| `active_profile` | function | `core/profiles.py:40` | `def active_profile()` |
| `is_light` | function | `core/profiles.py:59` | `def is_light()` |
| `specs_for_profile` | function | `core/profiles.py:64` | `def specs_for_profile(specs)` |
| `_load_prompt_payload` | function | `core/prompt.py:17` | `def _load_prompt_payload()` |
| `copy2clip` | function | `core/prompt.py:109` | `def copy2clip(text)` |
| `get_git_info` | function | `core/prompt.py:35` | `def get_git_info()` |
| `get_kernel` | function | `core/prompt.py:68` | `def get_kernel()` |
| `get_local_ips` | function | `core/prompt.py:87` | `def get_local_ips()` |
| `get_terminal_size` | function | `core/prompt.py:78` | `def get_terminal_size()` |
| `get_venv_info` | function | `core/prompt.py:60` | `def get_venv_info()` |
| `getprompt` | function | `core/prompt.py:127` | `def getprompt()` |
| `BridgeCatalog` | class | `core/protocols.py:62` | `class BridgeCatalog(Protocol)` |
| `LLMBackend` | class | `core/protocols.py:37` | `class LLMBackend(Protocol)` |
| `MemoryStore` | class | `core/protocols.py:51` | `class MemoryStore(Protocol)` |
| `OutcomeEvaluator` | class | `core/protocols.py:70` | `class OutcomeEvaluator(Protocol)` |
| `Selector` | class | `core/protocols.py:17` | `class Selector(Protocol)` |
| `complete` | method | `core/protocols.py:40` | `def complete(self, system, user, max_tokens, temperature)` |
| `evaluate` | method | `core/protocols.py:73` | `def evaluate(self, command, output, target, phase)` |
| `filter` | method | `core/protocols.py:65` | `def filter(self, phase, os_id)` |
| `get` | method | `core/protocols.py:56` | `def get(self, key, default)` |
| `put` | method | `core/protocols.py:54` | `def put(self, key, value)` |
| `search` | method | `core/protocols.py:58` | `def search(self, query, k)` |
| `suggest` | method | `core/protocols.py:27` | `def suggest(self, target, phase, context)` |
| `generate_reverse_shell_password` | function | `core/reverse_shell_secret.py:65` | `def generate_reverse_shell_password()` |
| `is_configured_password_valid` | function | `core/reverse_shell_secret.py:74` | `def is_configured_password_valid(candidate, minimum_length)` |
| `load_reverse_shell_password` | function | `core/reverse_shell_secret.py:41` | `def load_reverse_shell_password(secret_path)` |
| `seal_reverse_shell_password` | function | `core/reverse_shell_secret.py:24` | `def seal_reverse_shell_password(plaintext)` |
| `get_console` | function | `core/safe_console.py:42` | `def get_console()` |
| `milestone_glyph` | function | `core/safe_console.py:57` | `def milestone_glyph(state)` |
| `panel_box` | function | `core/safe_console.py:52` | `def panel_box()` |
| `progress_bar` | function | `core/safe_console.py:67` | `def progress_bar(ratio, width)` |
| `supports_unicode` | function | `core/safe_console.py:33` | `def supports_unicode()` |
| `CommandInjectionError` | class | `core/safe_exec.py:44` | `class CommandInjectionError(PermissionError)` |
| `UrlValidationError` | class | `core/safe_exec.py:48` | `class UrlValidationError(PermissionError)` |
| `needs_shell` | function | `core/safe_exec.py:52` | `def needs_shell(command)` |
| `safe_clear_screen` | function | `core/safe_exec.py:192` | `def safe_clear_screen()` |
| `safe_file_read` | function | `core/safe_exec.py:321` | `def safe_file_read(path)` |
| `safe_find_tool` | function | `core/safe_exec.py:305` | `def safe_find_tool(name)` |
| `safe_git_clone` | function | `core/safe_exec.py:234` | `def safe_git_clone(repo_url, target_dir)` |
| `safe_ip_show` | function | `core/safe_exec.py:268` | `def safe_ip_show(interface)` |
| `safe_run_argv` | function | `core/safe_exec.py:106` | `def safe_run_argv(argv)` |
| `safe_run_shell` | function | `core/safe_exec.py:146` | `def safe_run_shell(command)` |
| `safe_system` | function | `core/safe_exec.py:69` | `def safe_system(command)` |
| `validate_url` | function | `core/safe_exec.py:207` | `def validate_url(url)` |
| `filter_columns` | function | `core/safe_import.py:32` | `def filter_columns(src_columns, dest_columns)` |
| `is_safe_identifier` | function | `core/safe_import.py:20` | `def is_safe_identifier(name)` |
| `safe_copy_tree` | function | `core/safe_import.py:93` | `def safe_copy_tree(src, dest)` |
| `safe_extract_zip` | function | `core/safe_import.py:51` | `def safe_extract_zip(archive, dest)` |
| `SafeRunResult` | class | `core/safe_subprocess.py:44` | `class SafeRunResult` |
| `SafeRunner` | class | `core/safe_subprocess.py:60` | `class SafeRunner` |
| `ShellNotAllowedError` | class | `core/safe_subprocess.py:39` | `class ShellNotAllowedError(PermissionError)` |
| `__init__` | method | `core/safe_subprocess.py:70` | `def __init__(self, audit_log_path)` |
| `_audit` | method | `core/safe_subprocess.py:176` | `def _audit(self, record)` |
| `run` | method | `core/safe_subprocess.py:73` | `def run(self, argv)` |
| `run_shell` | method | `core/safe_subprocess.py:105` | `def run_shell(self, command)` |
| `TaskScheduler` | class | `core/scheduler.py:50` | `class TaskScheduler` |
| `_TaskInfo` | class | `core/scheduler.py:41` | `class _TaskInfo` |
| `__init__` | method | `core/scheduler.py:61` | `def __init__(self)` |
| `_cancel_internal` | method | `core/scheduler.py:224` | `def _cancel_internal(self, name)` |
| `_run_once_wrapper` | method | `core/scheduler.py:254` | `def _run_once_wrapper(self, name, func)` |
| `_run_stdlib_loop` | method | `core/scheduler.py:268` | `def _run_stdlib_loop(self)` |
| `_schedule_recurring_stdlib` | method | `core/scheduler.py:238` | `def _schedule_recurring_stdlib(self, info)` |
| `_wrapper` | function | `core/scheduler.py:241` | `def _wrapper()` |
| `_wrapper` | function | `core/scheduler.py:257` | `def _wrapper()` |
| `cancel_task` | method | `core/scheduler.py:192` | `def cancel_task(self, name)` |
| `get_scheduler` | function | `core/scheduler.py:285` | `def get_scheduler()` |
| `instance` | method | `core/scheduler.py:73` | `def instance(cls)` |
| `list_tasks` | method | `core/scheduler.py:205` | `def list_tasks(self)` |
| `schedule_once` | method | `core/scheduler.py:157` | `def schedule_once(self, name, delay_seconds, func)` |
| `schedule_task` | method | `core/scheduler.py:123` | `def schedule_task(self, name, interval_seconds, func)` |
| `start` | method | `core/scheduler.py:81` | `def start(self)` |
| `stop` | method | `core/scheduler.py:100` | `def stop(self)` |
| `anti_debug` | function | `core/security.py:18` | `def anti_debug()` |
| `generate_certificates` | function | `core/security.py:58` | `def generate_certificates(output_dir)` |
| `_mirror` | function | `core/session_secrets.py:113` | `def _mirror(config_obj, aes_hex, rat_key, session_magic)` |
| `_valid_session_token` | function | `core/session_secrets.py:104` | `def _valid_session_token(value, hex_len)` |
| `ensure_session_secrets` | function | `core/session_secrets.py:70` | `def ensure_session_secrets(config_obj, rotate, sessions_dir)` |
| `rotate_session_secrets` | function | `core/session_secrets.py:38` | `def rotate_session_secrets(config_obj, sessions_dir)` |
| `TerminalGuard` | class | `core/terminal_guard.py:73` | `class TerminalGuard` |
| `__enter__` | method | `core/terminal_guard.py:91` | `def __enter__(self)` |
| `__exit__` | method | `core/terminal_guard.py:104` | `def __exit__(self)` |
| `__init__` | method | `core/terminal_guard.py:85` | `def __init__(self)` |
| `_tty_fd` | function | `core/terminal_guard.py:30` | `def _tty_fd()` |
| `apply_stty_sane` | function | `core/terminal_guard.py:62` | `def apply_stty_sane()` |
| `emit_restore_sequences` | function | `core/terminal_guard.py:41` | `def emit_restore_sequences()` |
| `restore` | method | `core/terminal_guard.py:108` | `def restore(self)` |
| `truncate_text` | function | `core/text_utils.py:10` | `def truncate_text(value, max_len, marker)` |
| `check_lhost` | function | `core/validators.py:40` | `def check_lhost(lhost)` |
| `check_lport` | function | `core/validators.py:54` | `def check_lport(lport)` |
| `check_port` | function | `core/validators.py:64` | `def check_port(port, name)` |
| `check_rhost` | function | `core/validators.py:26` | `def check_rhost(rhost)` |
| `require_lhost` | function | `core/validators.py:94` | `def require_lhost(params)` |
| `require_lport` | function | `core/validators.py:107` | `def require_lport(params)` |
| `require_rhost` | function | `core/validators.py:77` | `def require_rhost(params)` |
| `require_rport` | function | `core/validators.py:120` | `def require_rport(params)` |
| `_probe` | function | `deploy/range/ad-mini/traffic-gen.py:21` | `def _probe(host, port)` |
| `main` | function | `deploy/range/ad-mini/traffic-gen.py:35` | `def main()` |
| `Config` | class | `discord_c2.py:86` | `class Config` |
| `SecureSessionManager` | class | `discord_c2.py:27` | `class SecureSessionManager` |
| `__getitem__` | method | `discord_c2.py:92` | `def __getitem__(self, key)` |
| `__init__` | method | `discord_c2.py:28` | `def __init__(self)` |
| `__init__` | method | `discord_c2.py:87` | `def __init__(self, config_dict)` |
| `add_cli` | function | `discord_c2.py:206` | `def add_cli(ctx, new_client_id)` |
| `addcli` | function | `discord_c2.py:278` | `def addcli(ctx, new_client_id)` |
| `c2` | function | `discord_c2.py:283` | `def c2(ctx)` |
| `check_lockout` | method | `discord_c2.py:40` | `def check_lockout(self, user_id)` |
| `check_rate_limit` | method | `discord_c2.py:49` | `def check_rate_limit(self, user_id)` |
| `clients` | function | `discord_c2.py:273` | `def clients(ctx)` |
| `create_session` | method | `discord_c2.py:62` | `def create_session(self, user_id, client_id)` |
| `download_c2` | function | `discord_c2.py:245` | `def download_c2(ctx, client_id, file_name)` |
| `exce_cmd` | function | `discord_c2.py:130` | `def exce_cmd(ctx)` |
| `handle_file` | function | `discord_c2.py:216` | `def handle_file(ctx)` |
| `load_payload` | function | `discord_c2.py:96` | `def load_payload()` |
| `on_ready` | function | `discord_c2.py:103` | `def on_ready()` |
| `register_failed_attempt` | method | `discord_c2.py:33` | `def register_failed_attempt(self, user_id)` |
| `send_connected_clients` | function | `discord_c2.py:256` | `def send_connected_clients(ctx)` |
| `start` | function | `discord_c2.py:108` | `def start(ctx)` |
| `validate_session` | method | `discord_c2.py:70` | `def validate_session(self, user_id)` |
| `ctrl_c` | function | `external/install_external.sh:13` | `` |
| `download` | function | `external/install_external.sh:18` | `` |
| `_jq` | function | `fast_run_as_r00t.sh:31` | `` |
| `check_deps` | function | `fast_run_as_r00t.sh:78` | `` |
| `check_sudo` | function | `fast_run_as_r00t.sh:87` | `` |
| `ensure_gum` | function | `fast_run_as_r00t.sh:67` | `` |
| `err_box` | function | `fast_run_as_r00t.sh:61` | `` |
| `kill_stale_c2` | function | `fast_run_as_r00t.sh:166` | `` |
| `log` | function | `fast_run_as_r00t.sh:59` | `` |
| `parse_args` | function | `fast_run_as_r00t.sh:96` | `` |
| `spin` | function | `fast_run_as_r00t.sh:60` | `` |
| `start_chown_watcher` | function | `fast_run_as_r00t.sh:145` | `` |
| `t_lazyown` | function | `fast_run_as_r00t.sh:121` | `` |
| `t_priv_user` | function | `fast_run_as_r00t.sh:134` | `` |
| `t_send` | function | `fast_run_as_r00t.sh:114` | `` |
| `download_file` | function | `install.sh:251` | `` |
| `ensure_gum` | function | `install.sh:128` | `` |
| `generate_certificates` | function | `install.sh:274` | `` |
| `install_encoder_module` | function | `install.sh:263` | `` |
| `install_external_storage` | function | `install.sh:218` | `` |
| `install_external_tools` | function | `install.sh:150` | `` |
| `install_lazyownbt` | function | `install.sh:231` | `` |
| `install_ollama` | function | `install.sh:206` | `` |
| `install_python_environment` | function | `install.sh:165` | `` |
| `install_system_packages` | function | `install.sh:139` | `` |
| `log` | function | `install.sh:88` | `` |
| `main` | function | `install.sh:310` | `` |
| `seed_payload_config` | function | `install.sh:281` | `` |
| `spin_run` | function | `install.sh:98` | `` |
| `usage` | function | `install.sh:49` | `` |
| `verify_installation` | function | `install.sh:294` | `` |
| `main` | function | `key.py:10` | `def main()` |
| `Alert` | class | `lazy_sentinel4.py:269` | `class Alert` |
| `App` | class | `lazy_sentinel4.py:542` | `class App(Cmd)` |
| `Database` | class | `lazy_sentinel4.py:212` | `class Database` |
| `LazySentinel` | class | `lazy_sentinel4.py:338` | `class LazySentinel` |
| `LazySentinelHandler` | class | `lazy_sentinel4.py:300` | `class LazySentinelHandler(FileSystemEventHandler)` |
| `RAGManager` | class | `lazy_sentinel4.py:56` | `class RAGManager` |
| `__init__` | method | `lazy_sentinel4.py:59` | `def __init__(self, model_name, cache_size)` |
| `__init__` | method | `lazy_sentinel4.py:213` | `def __init__(self, db_path)` |
| `__init__` | method | `lazy_sentinel4.py:272` | `def __init__(self, alert_type, details, severity)` |
| `__init__` | method | `lazy_sentinel4.py:301` | `def __init__(self, lazysentinel)` |
| `__init__` | method | `lazy_sentinel4.py:339` | `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)` |
| `__init__` | method | `lazy_sentinel4.py:543` | `def __init__(self)` |
| `chunk_text` | method | `lazy_sentinel4.py:359` | `def chunk_text(self, text, chunk_size)` |
| `complete_rag_add` | method | `lazy_sentinel4.py:679` | `def complete_rag_add(self, text, line, begidx, endidx)` |
| `complete_rag_bulk_add` | method | `lazy_sentinel4.py:686` | `def complete_rag_bulk_add(self, text, line, begidx, endidx)` |
| `display_toastr` | method | `lazy_sentinel4.py:557` | `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)` |
| `do_debug` | method | `lazy_sentinel4.py:595` | `def do_debug(self, arg)` |
| `do_quit` | method | `lazy_sentinel4.py:591` | `def do_quit(self, arg)` |
| `do_rag_add` | method | `lazy_sentinel4.py:612` | `def do_rag_add(self, arg)` |
| `do_rag_bulk_add` | method | `lazy_sentinel4.py:639` | `def do_rag_bulk_add(self, arg)` |
| `do_rag_query` | method | `lazy_sentinel4.py:604` | `def do_rag_query(self, arg)` |
| `do_rag_search` | method | `lazy_sentinel4.py:658` | `def do_rag_search(self, arg)` |
| `do_rag_status` | method | `lazy_sentinel4.py:627` | `def do_rag_status(self, arg)` |
| `do_rag_toggle` | method | `lazy_sentinel4.py:634` | `def do_rag_toggle(self, arg)` |
| `execute` | method | `lazy_sentinel4.py:241` | `def execute(self, query, params)` |
| `get_cache_key` | method | `lazy_sentinel4.py:83` | `def get_cache_key(self, content)` |
| `get_knowledge_base_stats` | method | `lazy_sentinel4.py:189` | `def get_knowledge_base_stats(self)` |
| `initialize` | method | `lazy_sentinel4.py:217` | `def initialize(self)` |
| `initialize_cache_table` | method | `lazy_sentinel4.py:71` | `def initialize_cache_table(self)` |
| `insert` | method | `lazy_sentinel4.py:253` | `def insert(self, query, params)` |
| `invalidate_cache` | method | `lazy_sentinel4.py:175` | `def invalidate_cache(self, file_path)` |
| `is_text_file` | method | `lazy_sentinel4.py:304` | `def is_text_file(self, file_path)` |
| `load_existing_vectorstore` | method | `lazy_sentinel4.py:86` | `def load_existing_vectorstore(self)` |
| `ollama_llm` | method | `lazy_sentinel4.py:99` | `def ollama_llm(self, question, context)` |
| `on_created` | method | `lazy_sentinel4.py:314` | `def on_created(self, event)` |
| `on_modified` | method | `lazy_sentinel4.py:326` | `def on_modified(self, event)` |
| `parse_deepseek_response` | method | `lazy_sentinel4.py:376` | `def parse_deepseek_response(self, response_text)` |
| `postcmd` | method | `lazy_sentinel4.py:567` | `def postcmd(self, stop, line)` |
| `process_file` | method | `lazy_sentinel4.py:420` | `def process_file(self, file_path)` |
| `process_file_to_rag` | method | `lazy_sentinel4.py:113` | `def process_file_to_rag(self, file_path)` |
| `query_rag` | method | `lazy_sentinel4.py:153` | `def query_rag(self, question)` |
| `sanitize_content` | function | `lazy_sentinel4.py:45` | `def sanitize_content(text)` |
| `save_to_db` | method | `lazy_sentinel4.py:286` | `def save_to_db(self, db)` |
| `select_relevant_chunk` | method | `lazy_sentinel4.py:362` | `def select_relevant_chunk(self, file_content, chunks)` |
| `show_popup` | method | `lazy_sentinel4.py:402` | `def show_popup(self, file_name, relevant_info, commands, details)` |
| `stop` | method | `lazy_sentinel4.py:536` | `def stop(self)` |
| `to_dict` | method | `lazy_sentinel4.py:278` | `def to_dict(self)` |
| `CustomDNSResolver` | class | `lazyc2.py:1855` | `class CustomDNSResolver(BaseResolver)` |
| `Handler` | class | `lazyc2.py:754` | `class Handler(FileSystemEventHandler)` |
| `User` | class | `lazyc2.py:3186` | `class User(UserMixin)` |
| `_JsonLogFormatter` | class | `lazyc2.py:467` | `class _JsonLogFormatter(Formatter)` |
| `_LazyShellProxy` | class | `lazyc2.py:2843` | `class _LazyShellProxy` |
| `__getattr__` | function | `lazyc2.py:2823` | `def __getattr__(name)` |
| `__getattr__` | method | `lazyc2.py:2855` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyc2.py:3187` | `def __init__(self, user_data)` |
| `__setattr__` | method | `lazyc2.py:2859` | `def __setattr__(self, name, value)` |
| `_add_security_headers` | function | `lazyc2.py:2686` | `def _add_security_headers(response)` |
| `_api_data_inner` | function | `lazyc2.py:4625` | `def _api_data_inner()` |
| `_append_beacon_record` | function | `lazyc2.py:1387` | `def _append_beacon_record(record)` |
| `_beacon_records_path` | function | `lazyc2.py:1279` | `def _beacon_records_path(client_id)` |
| `_beacon_signature_guard` | function | `lazyc2.py:3566` | `def _beacon_signature_guard()` |
| `_bg_cred_reuse` | function | `lazyc2.py:3982` | `def _bg_cred_reuse(_ip)` |
| `_bootstrap_initial_admin` | function | `lazyc2.py:2910` | `def _bootstrap_initial_admin()` |
| `_build_privesc_command` | function | `lazyc2.py:3537` | `def _build_privesc_command(platform)` |
| `_complete_mfa_login` | function | `lazyc2.py:6275` | `def _complete_mfa_login()` |
| `_current_aes_key` | function | `lazyc2.py:2081` | `def _current_aes_key()` |
| `_enforce_https_redirect` | function | `lazyc2.py:2576` | `def _enforce_https_redirect()` |
| `_enforce_mfa_verified` | function | `lazyc2.py:2652` | `def _enforce_mfa_verified()` |
| `_enforce_password_rotation` | function | `lazyc2.py:2596` | `def _enforce_password_rotation()` |
| `_engage_publish` | function | `lazyc2.py:3754` | `def _engage_publish(_cid, _ip, _host, _user, _platform)` |
| `_enqueue_malleable_command` | function | `lazyc2.py:1359` | `def _enqueue_malleable_command(client_id, command)` |
| `_env_tag` | function | `lazyc2.py:218` | `def _env_tag()` |
| `_events` | function | `lazyc2.py:7708` | `def _events()` |
| `_extract_first_ip` | function | `lazyc2.py:3810` | `def _extract_first_ip(raw)` |
| `_generic_loop_error` | function | `lazyc2.py:6935` | `def _generic_loop_error()` |
| `_get_rbac_user_obj` | function | `lazyc2.py:3199` | `def _get_rbac_user_obj(flask_user)` |
| `_group_tasks_for_display` | function | `lazyc2.py:5577` | `def _group_tasks_for_display(tasks)` |
| `_handle_404` | function | `lazyc2.py:2753` | `def _handle_404(_error)` |
| `_handle_405` | function | `lazyc2.py:2758` | `def _handle_405(_error)` |
| `_handle_exception` | function | `lazyc2.py:2763` | `def _handle_exception(error)` |
| `_ingest_beacon` | function | `lazyc2.py:4043` | `def _ingest_beacon(_ips, _host, _cmd, _out, _user)` |
| `_init_shell` | function | `lazyc2.py:2796` | `def _init_shell()` |
| `_is_unspecified_bind_literal` | function | `lazyc2.py:305` | `def _is_unspecified_bind_literal(address)` |
| `_is_valid_credential` | function | `lazyc2.py:3823` | `def _is_valid_credential(value)` |
| `_listen_address` | function | `lazyc2.py:278` | `def _listen_address()` |
| `_load_malleable_recon_state` | function | `lazyc2.py:1317` | `def _load_malleable_recon_state(client_id)` |
| `_load_or_create_secret_key` | function | `lazyc2.py:2706` | `def _load_or_create_secret_key()` |
| `_load_reverse_shell_password` | function | `lazyc2.py:5164` | `def _load_reverse_shell_password(secret_path)` |
| `_log_dns_bind_failure` | function | `lazyc2.py:1921` | `def _log_dns_bind_failure(address, error_number)` |
| `_malleable_recon_state_dir` | function | `lazyc2.py:1289` | `def _malleable_recon_state_dir(client_id)` |
| `_metrics_before_request` | function | `lazyc2.py:2570` | `def _metrics_before_request()` |
| `_mfa_challenge_pending` | function | `lazyc2.py:2634` | `def _mfa_challenge_pending()` |
| `_mfa_exempt_endpoint` | function | `lazyc2.py:2627` | `def _mfa_exempt_endpoint(endpoint)` |
| `_normalise_platform` | function | `lazyc2.py:3852` | `def _normalise_platform(raw_platform)` |
| `_normalize_task_title` | function | `lazyc2.py:5570` | `def _normalize_task_title(title)` |
| `_on_terminate` | function | `lazyc2.py:8794` | `def _on_terminate(signum, _frame)` |
| `_persist_bootstrap_password` | function | `lazyc2.py:2890` | `def _persist_bootstrap_password(prefix, password)` |
| `_probe_bind` | function | `lazyc2.py:357` | `def _probe_bind(address, port, sock_type)` |
| `_queue_beacon_cmd` | function | `lazyc2.py:3863` | `def _queue_beacon_cmd(action, ctx)` |
| `_read_beacon_records` | function | `lazyc2.py:1417` | `def _read_beacon_records(client_id)` |
| `_render_enhanced_report` | function | `lazyc2.py:7047` | `def _render_enhanced_report()` |
| `_render_legacy_report` | function | `lazyc2.py:7067` | `def _render_legacy_report()` |
| `_resolve_bind_address` | function | `lazyc2.py:402` | `def _resolve_bind_address(preferred, port, sock_type)` |
| `_resolve_reverse_shell_password` | function | `lazyc2.py:5178` | `def _resolve_reverse_shell_password()` |
| `_resolve_secure_template_path` | function | `lazyc2.py:4290` | `def _resolve_secure_template_path(template_name)` |
| `_resolve_within` | function | `lazyc2.py:655` | `def _resolve_within(allowed_base, name)` |
| `_sanitize_command_output` | function | `lazyc2.py:585` | `def _sanitize_command_output(value)` |
| `_sanitize_csv_field` | function | `lazyc2.py:1236` | `def _sanitize_csv_field(value, maxlen)` |
| `_sanitize_html` | function | `lazyc2.py:1199` | `def _sanitize_html(raw_html)` |
| `_save_malleable_recon_state` | function | `lazyc2.py:1338` | `def _save_malleable_recon_state(client_id, state)` |
| `_seal_reverse_shell_password` | function | `lazyc2.py:5150` | `def _seal_reverse_shell_password(plaintext)` |
| `_secure_command_queue_path` | function | `lazyc2.py:1249` | `def _secure_command_queue_path(client_id)` |
| `_select_specific_bind_address` | function | `lazyc2.py:324` | `def _select_specific_bind_address(candidate)` |
| `_target` | method | `lazyc2.py:2851` | `def _target(self)` |
| `_try_copy_privesc_tool` | function | `lazyc2.py:3517` | `def _try_copy_privesc_tool(platform)` |
| `add_dynamic_data` | function | `lazyc2.py:2250` | `def add_dynamic_data(data)` |
| `admin_create_tenant` | function | `lazyc2.py:6397` | `def admin_create_tenant()` |
| `admin_delete_user` | function | `lazyc2.py:6358` | `def admin_delete_user(user_id)` |
| `admin_reset_mfa` | function | `lazyc2.py:6346` | `def admin_reset_mfa(user_id)` |
| `admin_set_role` | function | `lazyc2.py:6324` | `def admin_set_role(user_id)` |
| `admin_switch_tenant` | function | `lazyc2.py:6417` | `def admin_switch_tenant(tenant_id)` |
| `admin_tenants` | function | `lazyc2.py:6376` | `def admin_tenants()` |
| `admin_users` | function | `lazyc2.py:6309` | `def admin_users()` |
| `adversary` | function | `lazyc2.py:5396` | `def adversary()` |
| `aicmd` | function | `lazyc2.py:1666` | `def aicmd(cmd)` |
| `aicmd_deepseek` | function | `lazyc2.py:1552` | `def aicmd_deepseek(cmd)` |
| `aicmd_view` | function | `lazyc2.py:5841` | `def aicmd_view()` |
| `analyze_behavioral_data` | function | `lazyc2.py:2504` | `def analyze_behavioral_data(behavioral_events)` |
| `analyze_campaign_progress` | function | `lazyc2.py:2532` | `def analyze_campaign_progress(campaign_id, events)` |
| `api_attack_bundle` | function | `lazyc2.py:7974` | `def api_attack_bundle()` |
| `api_attack_graph` | function | `lazyc2.py:7922` | `def api_attack_graph()` |
| `api_beacon_results` | function | `lazyc2.py:6917` | `def api_beacon_results(client_id)` |
| `api_dashboard` | function | `lazyc2.py:8552` | `def api_dashboard()` |
| `api_data` | function | `lazyc2.py:4602` | `def api_data()` |
| `api_guard_audit` | function | `lazyc2.py:7776` | `def api_guard_audit()` |
| `api_intel_bundle` | function | `lazyc2.py:7889` | `def api_intel_bundle()` |
| `api_intel_graph` | function | `lazyc2.py:7605` | `def api_intel_graph()` |
| `api_killchain` | function | `lazyc2.py:6886` | `def api_killchain()` |
| `api_lazy_mentions` | function | `lazyc2.py:7853` | `def api_lazy_mentions()` |
| `api_listeners` | function | `lazyc2.py:8622` | `def api_listeners()` |
| `api_listeners_create` | function | `lazyc2.py:8629` | `def api_listeners_create()` |
| `api_listeners_delete` | function | `lazyc2.py:8661` | `def api_listeners_delete(listener_id)` |
| `api_listeners_start` | function | `lazyc2.py:8645` | `def api_listeners_start(listener_id)` |
| `api_listeners_stop` | function | `lazyc2.py:8653` | `def api_listeners_stop(listener_id)` |
| `api_loop_broadcast` | function | `lazyc2.py:7733` | `def api_loop_broadcast()` |
| `api_loop_broadcast_stream` | function | `lazyc2.py:7675` | `def api_loop_broadcast_stream()` |
| `api_loop_graph` | function | `lazyc2.py:7822` | `def api_loop_graph()` |
| `api_loop_log` | function | `lazyc2.py:7008` | `def api_loop_log(loop_id)` |
| `api_loop_stop` | function | `lazyc2.py:7030` | `def api_loop_stop(loop_id)` |
| `api_loops_list` | function | `lazyc2.py:6996` | `def api_loops_list()` |
| `api_loops_start` | function | `lazyc2.py:6948` | `def api_loops_start()` |
| `api_surface_live` | function | `lazyc2.py:7515` | `def api_surface_live()` |
| `attack3d_view` | function | `lazyc2.py:7571` | `def attack3d_view()` |
| `attack_bundle_view` | function | `lazyc2.py:7590` | `def attack_bundle_view()` |
| `aumentar_elo` | function | `lazyc2.py:1138` | `def aumentar_elo(user_id, cantidad)` |
| `aumentar_elo_route` | function | `lazyc2.py:6538` | `def aumentar_elo_route(user_id)` |
| `authenticate` | function | `lazyc2.py:1490` | `def authenticate()` |
| `banners` | function | `lazyc2.py:6554` | `def banners()` |
| `broadcast_view` | function | `lazyc2.py:7661` | `def broadcast_view()` |
| `campaign_report` | function | `lazyc2.py:8200` | `def campaign_report(campaign_id)` |
| `capture_audio` | function | `lazyc2.py:7476` | `def capture_audio()` |
| `capture_image` | function | `lazyc2.py:7450` | `def capture_image()` |
| `change_password` | function | `lazyc2.py:6472` | `def change_password()` |
| `chatbot` | function | `lazyc2.py:5274` | `def chatbot()` |
| `check_auth` | function | `lazyc2.py:1475` | `def check_auth(username, password)` |
| `clean_expired_tokens` | function | `lazyc2.py:636` | `def clean_expired_tokens()` |
| `clean_json` | function | `lazyc2.py:644` | `def clean_json(text)` |
| `compliance_add_evidence` | function | `lazyc2.py:6715` | `def compliance_add_evidence()` |
| `compliance_dashboard` | function | `lazyc2.py:6663` | `def compliance_dashboard()` |
| `compliance_export` | function | `lazyc2.py:6765` | `def compliance_export(format)` |
| `compliance_report` | function | `lazyc2.py:6685` | `def compliance_report()` |
| `compliance_verify_evidence` | function | `lazyc2.py:6751` | `def compliance_verify_evidence()` |
| `connect` | function | `lazyc2.py:7139` | `def connect()` |
| `create_campaign` | function | `lazyc2.py:8084` | `def create_campaign()` |
| `create_cves` | function | `lazyc2.py:1090` | `def create_cves()` |
| `create_multivector_campaign` | function | `lazyc2.py:8329` | `def create_multivector_campaign()` |
| `create_report` | function | `lazyc2.py:1109` | `def create_report()` |
| `create_route` | function | `lazyc2.py:4357` | `def create_route()` |
| `create_short_url` | function | `lazyc2.py:4764` | `def create_short_url()` |
| `create_tool` | function | `lazyc2.py:5908` | `def create_tool()` |
| `csrf_protect` | function | `lazyc2.py:1531` | `def csrf_protect(view)` |
| `csv_to_html` | function | `lazyc2.py:5428` | `def csv_to_html()` |
| `cve` | function | `lazyc2.py:5650` | `def cve(cve_id)` |
| `cves` | function | `lazyc2.py:5624` | `def cves()` |
| `datetime_now_iso` | function | `lazyc2.py:1244` | `def datetime_now_iso()` |
| `decorated` | function | `lazyc2.py:1509` | `def decorated()` |
| `decorated` | function | `lazyc2.py:1522` | `def decorated()` |
| `decorated` | function | `lazyc2.py:2672` | `def decorated()` |
| `decoy` | function | `lazyc2.py:2043` | `def decoy()` |
| `decrypt_data` | function | `lazyc2.py:2109` | `def decrypt_data(encrypted_data, is_file)` |
| `delete_tool` | function | `lazyc2.py:6014` | `def delete_tool(toolname)` |
| `download_file` | function | `lazyc2.py:4228` | `def download_file()` |
| `download_files` | function | `lazyc2.py:4892` | `def download_files(filename)` |
| `dynamic_route` | function | `lazyc2.py:4426` | `def dynamic_route(route_path, data)` |
| `edit_cve` | function | `lazyc2.py:5665` | `def edit_cve(cve_id)` |
| `edit_event` | function | `lazyc2.py:5764` | `def edit_event(event_name)` |
| `edit_notes` | function | `lazyc2.py:5699` | `def edit_notes()` |
| `edit_task` | function | `lazyc2.py:5590` | `def edit_task(task_id)` |
| `encrypt_data` | function | `lazyc2.py:2100` | `def encrypt_data(data)` |
| `ensure_sessions_dir` | function | `lazyc2.py:497` | `def ensure_sessions_dir()` |
| `escape_js` | function | `lazyc2.py:1174` | `def escape_js(s)` |
| `escape_js_string` | function | `lazyc2.py:1463` | `def escape_js_string(value)` |
| `execute_command` | function | `lazyc2.py:1826` | `def execute_command(command)` |
| `extract_attack_vectors` | function | `lazyc2.py:881` | `def extract_attack_vectors(nodes, edges)` |
| `favicon` | function | `lazyc2.py:4540` | `def favicon()` |
| `format` | method | `lazyc2.py:470` | `def format(self, record)` |
| `fromjson` | function | `lazyc2.py:798` | `def fromjson(value)` |
| `generalbot` | function | `lazyc2.py:5412` | `def generalbot()` |
| `get_client_ip` | function | `lazyc2.py:2272` | `def get_client_ip()` |
| `get_config` | function | `lazyc2.py:7431` | `def get_config()` |
| `get_connected_clients` | function | `lazyc2.py:6635` | `def get_connected_clients()` |
| `get_data` | function | `lazyc2.py:8004` | `def get_data()` |
| `get_discovered_hosts` | function | `lazyc2.py:2145` | `def get_discovered_hosts()` |
| `get_event_config` | function | `lazyc2.py:5799` | `def get_event_config()` |
| `get_event_config_view` | function | `lazyc2.py:5806` | `def get_event_config_view()` |
| `get_events` | function | `lazyc2.py:5866` | `def get_events()` |
| `get_karma_name` | function | `lazyc2.py:781` | `def get_karma_name(elo)` |
| `get_local_ip_addresses` | function | `lazyc2.py:2195` | `def get_local_ip_addresses()` |
| `get_notes` | function | `lazyc2.py:5717` | `def get_notes()` |
| `get_output` | function | `lazyc2.py:5107` | `def get_output()` |
| `get_request_details` | function | `lazyc2.py:2281` | `def get_request_details()` |
| `get_results` | function | `lazyc2.py:5143` | `def get_results()` |
| `get_safe_file_path` | function | `lazyc2.py:2434` | `def get_safe_file_path(user_path)` |
| `get_tasks` | function | `lazyc2.py:5551` | `def get_tasks()` |
| `graph` | function | `lazyc2.py:5527` | `def graph()` |
| `handle_client` | function | `lazyc2.py:2024` | `def handle_client(client_socket, remote_host, remote_port)` |
| `handle_input` | function | `lazyc2.py:7241` | `def handle_input(data)` |
| `health_check` | function | `lazyc2.py:8506` | `def health_check()` |
| `implants_check` | function | `lazyc2.py:864` | `def implants_check()` |
| `index` | function | `lazyc2.py:3269` | `def index()` |
| `intel_bundle_view` | function | `lazyc2.py:7556` | `def intel_bundle_view()` |
| `intel_view` | function | `lazyc2.py:7537` | `def intel_view()` |
| `internal_server_error` | function | `lazyc2.py:7422` | `def internal_server_error(e)` |
| `is_binary` | function | `lazyc2.py:595` | `def is_binary(safe_filename)` |
| `is_insecure_credential` | function | `lazyc2.py:230` | `def is_insecure_credential(user, pwd)` |
| `is_safe_template_path` | function | `lazyc2.py:555` | `def is_safe_template_path(template_path, template_name)` |
| `is_valid_data` | function | `lazyc2.py:4450` | `def is_valid_data(data)` |
| `is_valid_route_path` | function | `lazyc2.py:4443` | `def is_valid_route_path(route_path)` |
| `is_valid_template_name` | function | `lazyc2.py:4460` | `def is_valid_template_name(template_name)` |
| `is_valid_url` | function | `lazyc2.py:2426` | `def is_valid_url(url)` |
| `issue_command` | function | `lazyc2.py:4177` | `def issue_command()` |
| `killchain_view` | function | `lazyc2.py:6856` | `def killchain_view()` |
| `lazybot` | function | `lazyc2.py:6646` | `def lazybot()` |
| `lazyphishingai` | function | `lazyc2.py:8162` | `def lazyphishingai()` |
| `lazyreport` | function | `lazyc2.py:6795` | `def lazyreport()` |
| `lazyreport_view` | function | `lazyc2.py:6850` | `def lazyreport_view()` |
| `list_campaigns` | function | `lazyc2.py:8071` | `def list_campaigns()` |
| `list_tools` | function | `lazyc2.py:5898` | `def list_tools()` |
| `listener` | function | `lazyc2.py:7148` | `def listener()` |
| `listener_command` | function | `lazyc2.py:7266` | `def listener_command(msg)` |
| `listener_connect` | function | `lazyc2.py:7158` | `def listener_connect()` |
| `listener_disconnect` | function | `lazyc2.py:7169` | `def listener_disconnect()` |

Next: [SYMBOLS_p9.md](SYMBOLS_p9.md)
