# Symbols (page 7 of 35)
Previous: [SYMBOLS_p6.md](SYMBOLS_p6.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `__init__` | method | `core/errors.py:123` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:130` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:137` | `def __init__(self, message, error_code)` |
| `__str__` | method | `core/errors.py:74` | `def __str__(self)` |
| `to_dict` | method | `core/errors.py:66` | `def to_dict(self)` |
| `_validate_input` | function | `core/executor.py:41` | `def _validate_input(command)` |
| `_validate_timeout` | function | `core/executor.py:75` | `def _validate_timeout(timeout)` |
| `run_shell` | function | `core/executor.py:149` | `def run_shell(cmd)` |
| `safe_run` | function | `core/executor.py:96` | `def safe_run(command)` |
| `safe_run` | function | `core/executor.py:98` | `def safe_run(command)` |
| `safe_run` | function | `core/executor.py:101` | `def safe_run(command)` |
| `SecurityViolation` | class | `core/hardening.py:80` | `class SecurityViolation(PermissionError)` |
| `build_sshpass_command` | method | `core/hardening.py:189` | `def build_sshpass_command(password, ssh_args)` |
| `defused_xml_parse` | method | `core/hardening.py:353` | `def defused_xml_parse(source)` |
| `escape_html_content` | method | `core/hardening.py:237` | `def escape_html_content(value)` |
| `escape_powershell_single_quoted` | function | `core/hardening.py:59` | `def escape_powershell_single_quoted(value)` |
| `reject_option_injection` | function | `core/hardening.py:40` | `def reject_option_injection(argv)` |
| `require_encryption_key` | method | `core/hardening.py:325` | `def require_encryption_key(env_key, secret_file)` |
| `safe_clipboard_copy` | method | `core/hardening.py:150` | `def safe_clipboard_copy(content)` |
| `safe_path_join` | method | `core/hardening.py:249` | `def safe_path_join(base_dir, user_path)` |
| `safe_subprocess_run` | method | `core/hardening.py:105` | `def safe_subprocess_run(argv)` |
| `sanitize_filename` | method | `core/hardening.py:375` | `def sanitize_filename(filename, max_length)` |
| `set_sshpass_env` | method | `core/hardening.py:218` | `def set_sshpass_env(password)` |
| `terminal_env` | method | `core/hardening.py:84` | `def terminal_env(base)` |
| `validate_host` | method | `core/hardening.py:303` | `def validate_host(host)` |
| `validate_network_cidr` | method | `core/hardening.py:275` | `def validate_network_cidr(cidr)` |
| `validate_port_spec` | method | `core/hardening.py:287` | `def validate_port_spec(ports)` |
| `display_news` | function | `core/http.py:198` | `def display_news(titles, links, scores)` |
| `exploitalert` | function | `core/http.py:106` | `def exploitalert(content)` |
| `generate_http_req` | function | `core/http.py:18` | `def generate_http_req(host, port, uri, custom_header, cmd)` |
| `get_banner` | function | `core/http.py:50` | `def get_banner(host, port)` |
| `get_command` | function | `core/http.py:69` | `def get_command(url, lhost)` |
| `inject_payloads` | function | `core/http.py:211` | `def inject_payloads(urls, payload_url, request_timeout)` |
| `nvddb` | function | `core/http.py:143` | `def nvddb(content)` |
| `packetstormsecurity` | function | `core/http.py:125` | `def packetstormsecurity(content)` |
| `scrape_news` | function | `core/http.py:174` | `def scrape_news()` |
| `send_command` | function | `core/http.py:87` | `def send_command(cmd, url, lhost)` |
| `BudgetConfig` | class | `core/llm_budget.py:103` | `class BudgetConfig` |
| `BudgetExceeded` | class | `core/llm_budget.py:54` | `class BudgetExceeded(RuntimeError)` |
| `BudgetGuard` | class | `core/llm_budget.py:310` | `class BudgetGuard` |
| `BudgetLedger` | class | `core/llm_budget.py:176` | `class BudgetLedger` |
| `BudgetedBackend` | class | `core/llm_budget.py:408` | `class BudgetedBackend` |
| `LLMBackendLike` | class | `core/llm_budget.py:58` | `class LLMBackendLike(Protocol)` |
| `LedgerEntry` | class | `core/llm_budget.py:132` | `class LedgerEntry` |
| `ModelPrice` | class | `core/llm_budget.py:69` | `class ModelPrice` |
| `TokenEstimator` | class | `core/llm_budget.py:268` | `class TokenEstimator` |
| `__init__` | method | `core/llm_budget.py:278` | `def __init__(self, encoding_name)` |
| `__init__` | method | `core/llm_budget.py:319` | `def __init__(self, config, estimator, ledger)` |
| `__init__` | method | `core/llm_budget.py:417` | `def __init__(self, inner, guard, model)` |
| `_coerce_bool` | method | `core/llm_budget.py:476` | `def _coerce_bool(value, default)` |
| `_coerce_positive_float` | method | `core/llm_budget.py:520` | `def _coerce_positive_float(value, default)` |
| `_coerce_positive_int` | method | `core/llm_budget.py:536` | `def _coerce_positive_int(value, default)` |
| `_coerce_price_table` | method | `core/llm_budget.py:496` | `def _coerce_price_table(value)` |
| `_empty_state` | method | `core/llm_budget.py:189` | `def _empty_state(self)` |
| `_has_required_methods` | method | `core/llm_budget.py:642` | `def _has_required_methods(backend)` |
| `_load` | method | `core/llm_budget.py:193` | `def _load(self)` |
| `_load_encoding` | method | `core/llm_budget.py:283` | `def _load_encoding(encoding_name)` |
| `_now_iso` | method | `core/llm_budget.py:163` | `def _now_iso(now)` |
| `_save` | method | `core/llm_budget.py:215` | `def _save(self, state)` |
| `_state` | method | `core/llm_budget.py:226` | `def _state(self)` |
| `_today_utc` | method | `core/llm_budget.py:150` | `def _today_utc(now)` |
| `calls_today` | method | `core/llm_budget.py:256` | `def calls_today(self)` |
| `complete` | method | `core/llm_budget.py:65` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `core/llm_budget.py:435` | `def complete(self, system, user, max_tokens, temperature)` |
| `count` | method | `core/llm_budget.py:292` | `def count(self, text)` |
| `default_model_prices` | method | `core/llm_budget.py:442` | `def default_model_prices()` |
| `default_sessions_dir` | method | `core/llm_budget.py:461` | `def default_sessions_dir()` |
| `estimate_and_check` | method | `core/llm_budget.py:356` | `def estimate_and_check(self, prompt, model, output_tokens)` |
| `estimate_cost` | method | `core/llm_budget.py:343` | `def estimate_cost(self, model, input_tokens, output_tokens)` |
| `format_budget_status` | method | `core/llm_budget.py:616` | `def format_budget_status(config, ledger)` |
| `from_mapping` | method | `core/llm_budget.py:81` | `def from_mapping(cls, data)` |
| `generate` | method | `core/llm_budget.py:61` | `def generate(self, prompt)` |
| `generate` | method | `core/llm_budget.py:422` | `def generate(self, prompt)` |
| `load_budget_config` | method | `core/llm_budget.py:552` | `def load_budget_config(payload, sessions_dir)` |
| `price_for` | method | `core/llm_budget.py:329` | `def price_for(self, model)` |
| `read_budget_status` | method | `core/llm_budget.py:585` | `def read_budget_status(payload, sessions_dir)` |
| `record` | method | `core/llm_budget.py:232` | `def record(self, entry)` |
| `reset` | method | `core/llm_budget.py:261` | `def reset(self)` |
| `spent_today` | method | `core/llm_budget.py:251` | `def spent_today(self)` |
| `stream_generate` | method | `core/llm_budget.py:63` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `core/llm_budget.py:430` | `def stream_generate(self, prompt)` |
| `wrap_backend_with_budget` | method | `core/llm_budget.py:657` | `def wrap_backend_with_budget(backend, config, estimator, model, ledger)` |
| `StructuredLogConfig` | class | `core/logging.py:42` | `class StructuredLogConfig` |
| `StructuredLogger` | class | `core/logging.py:139` | `class StructuredLogger(Logger)` |
| `_ConsoleFormatter` | class | `core/logging.py:121` | `class _ConsoleFormatter(Formatter)` |
| `_JsonLineFormatter` | class | `core/logging.py:71` | `class _JsonLineFormatter(Formatter)` |
| `__init__` | method | `core/logging.py:74` | `def __init__(self, redacted_fields)` |
| `_log_factory` | method | `core/logging.py:180` | `def _log_factory(name, config)` |
| `format` | method | `core/logging.py:78` | `def format(self, record)` |
| `format` | method | `core/logging.py:132` | `def format(self, record)` |
| `get_logger` | method | `core/logging.py:231` | `def get_logger(name)` |
| `install_json_handler` | method | `core/logging.py:251` | `def install_json_handler(name, config)` |
| `makeRecord` | method | `core/logging.py:148` | `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)` |
| `reconfigure` | method | `core/logging.py:300` | `def reconfigure(config)` |
| `create_arp_packet` | function | `core/network.py:33` | `def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac)` |
| `get_banner` | function | `core/network.py:134` | `def get_banner(ip, port)` |
| `get_network_info` | function | `core/network.py:154` | `def get_network_info()` |
| `get_open_ports` | function | `core/network.py:105` | `def get_open_ports()` |
| `is_port_in_use` | function | `core/network.py:120` | `def is_port_in_use(port, host)` |
| `parse_ip_mac` | function | `core/network.py:18` | `def parse_ip_mac(input_string)` |
| `parse_proc_net_file` | function | `core/network.py:78` | `def parse_proc_net_file(file_path)` |
| `send_packet` | function | `core/network.py:66` | `def send_packet(packet, iface)` |
| `aggressive_yaml_fix` | function | `core/parsers.py:256` | `def aggressive_yaml_fix(yaml_content)` |
| `clean_html` | function | `core/parsers.py:52` | `def clean_html(html_string)` |
| `clean_output` | function | `core/parsers.py:40` | `def clean_output(output)` |
| `clean_url` | function | `core/parsers.py:64` | `def clean_url(host)` |
| `create_synthetic_yaml` | function | `core/parsers.py:282` | `def create_synthetic_yaml(nmap_services)` |
| `de_htmlify` | function | `core/parsers.py:91` | `def de_htmlify(data)` |
| `extract_banners` | function | `core/parsers.py:160` | `def extract_banners(xml_file)` |
| `fix_common_yaml_issues` | function | `core/parsers.py:231` | `def fix_common_yaml_issues(yaml_content)` |
| `get_domain_from_xml` | function | `core/parsers.py:136` | `def get_domain_from_xml(xml_file)` |
| `get_xml` | function | `core/parsers.py:120` | `def get_xml(directory)` |
| `htmlify` | function | `core/parsers.py:79` | `def htmlify(data)` |
| `is_exist` | function | `core/parsers.py:105` | `def is_exist(file)` |
| `list_binaries` | function | `core/parsers.py:368` | `def list_binaries(directory)` |
| `load_adversary` | function | `core/parsers.py:325` | `def load_adversary()` |
| `load_knowledge_base` | function | `core/parsers.py:338` | `def load_knowledge_base(knowledge_file)` |
| `load_user_aliases` | function | `core/parsers.py:354` | `def load_user_aliases()` |
| `manual_yaml_extraction` | function | `core/parsers.py:210` | `def manual_yaml_extraction(content)` |
| `parse_nmap_csv` | function | `core/parsers.py:190` | `def parse_nmap_csv(csv_path)` |
| `parse_yaml_response` | function | `core/parsers.py:305` | `def parse_yaml_response(content)` |
| `select_binary` | function | `core/parsers.py:383` | `def select_binary(binaries)` |
| `strip_ansi` | function | `core/parsers.py:21` | `def strip_ansi(text)` |
| `FieldKind` | class | `core/payload_schema.py:71` | `class FieldKind(StrEnum)` |
| `FieldSpec` | class | `core/payload_schema.py:98` | `class FieldSpec` |
| `Severity` | class | `core/payload_schema.py:89` | `class Severity(StrEnum)` |
| `ValidationIssue` | class | `core/payload_schema.py:140` | `class ValidationIssue` |
| `_coerce_bool` | method | `core/payload_schema.py:314` | `def _coerce_bool(raw)` |
| `_coerce_int` | method | `core/payload_schema.py:299` | `def _coerce_int(raw)` |
| `_spec` | method | `core/payload_schema.py:333` | `def _spec(name, kind, default, description)` |
| `_validate_bool` | method | `core/payload_schema.py:193` | `def _validate_bool(value)` |
| `_validate_hex` | method | `core/payload_schema.py:252` | `def _validate_hex(value)` |
| `_validate_hostname` | method | `core/payload_schema.py:218` | `def _validate_hostname(value)` |
| `_validate_int` | method | `core/payload_schema.py:169` | `def _validate_int(value)` |
| `_validate_interface` | method | `core/payload_schema.py:244` | `def _validate_interface(value)` |
| `_validate_ip` | method | `core/payload_schema.py:210` | `def _validate_ip(value)` |
| `_validate_json_blob` | method | `core/payload_schema.py:266` | `def _validate_json_blob(value)` |
| `_validate_opaque` | method | `core/payload_schema.py:278` | `def _validate_opaque(_value)` |
| `_validate_os_id` | method | `core/payload_schema.py:260` | `def _validate_os_id(value)` |
| `_validate_path` | method | `core/payload_schema.py:238` | `def _validate_path(value)` |
| `_validate_port` | method | `core/payload_schema.py:183` | `def _validate_port(value)` |
| `_validate_string` | method | `core/payload_schema.py:163` | `def _validate_string(value)` |
| `_validate_url` | method | `core/payload_schema.py:230` | `def _validate_url(value)` |
| `categories` | method | `core/payload_schema.py:1652` | `def categories()` |
| `coerce_value` | method | `core/payload_schema.py:1494` | `def coerce_value(key, raw)` |
| `default_payload` | method | `core/payload_schema.py:1644` | `def default_payload()` |
| `field_for` | method | `core/payload_schema.py:1489` | `def field_for(key)` |
| `format_issue` | method | `core/payload_schema.py:1626` | `def format_issue(issue)` |
| `validate_payload` | method | `core/payload_schema.py:1591` | `def validate_payload(payload)` |
| `validate_value` | method | `core/payload_schema.py:1517` | `def validate_value(key, value)` |
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
| `CommandInjectionError` | class | `core/safe_exec.py:44` | `class CommandInjectionError(PermissionError)` |
| `UrlValidationError` | class | `core/safe_exec.py:48` | `class UrlValidationError(PermissionError)` |
| `needs_shell` | method | `core/safe_exec.py:52` | `def needs_shell(command)` |
| `safe_clear_screen` | method | `core/safe_exec.py:192` | `def safe_clear_screen()` |
| `safe_file_read` | method | `core/safe_exec.py:321` | `def safe_file_read(path)` |
| `safe_find_tool` | method | `core/safe_exec.py:305` | `def safe_find_tool(name)` |
| `safe_git_clone` | method | `core/safe_exec.py:234` | `def safe_git_clone(repo_url, target_dir)` |
| `safe_ip_show` | method | `core/safe_exec.py:268` | `def safe_ip_show(interface)` |
| `safe_run_argv` | method | `core/safe_exec.py:106` | `def safe_run_argv(argv)` |
| `safe_run_shell` | method | `core/safe_exec.py:146` | `def safe_run_shell(command)` |
| `safe_system` | method | `core/safe_exec.py:69` | `def safe_system(command)` |
| `validate_url` | method | `core/safe_exec.py:207` | `def validate_url(url)` |
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
| `_wrapper` | method | `core/scheduler.py:241` | `def _wrapper()` |
| `_wrapper` | method | `core/scheduler.py:257` | `def _wrapper()` |
| `cancel_task` | method | `core/scheduler.py:192` | `def cancel_task(self, name)` |
| `get_scheduler` | method | `core/scheduler.py:285` | `def get_scheduler()` |
| `instance` | method | `core/scheduler.py:73` | `def instance(cls)` |
| `list_tasks` | method | `core/scheduler.py:205` | `def list_tasks(self)` |
| `schedule_once` | method | `core/scheduler.py:157` | `def schedule_once(self, name, delay_seconds, func)` |
| `schedule_task` | method | `core/scheduler.py:123` | `def schedule_task(self, name, interval_seconds, func)` |
| `start` | method | `core/scheduler.py:81` | `def start(self)` |
| `stop` | method | `core/scheduler.py:100` | `def stop(self)` |
| `anti_debug` | function | `core/security.py:18` | `def anti_debug()` |
| `generate_certificates` | function | `core/security.py:58` | `def generate_certificates(output_dir)` |
| `truncate_text` | function | `core/text_utils.py:10` | `def truncate_text(value, max_len, marker)` |
| `_is_valid_cidr` | function | `core/validators.py:44` | `def _is_valid_cidr(value)` |
| `_is_valid_host` | function | `core/validators.py:24` | `def _is_valid_host(value)` |
| `_rejects_shell_meta` | function | `core/validators.py:19` | `def _rejects_shell_meta(value)` |
| `check_lhost` | function | `core/validators.py:69` | `def check_lhost(lhost)` |
| `check_lport` | function | `core/validators.py:83` | `def check_lport(lport)` |
| `check_port` | function | `core/validators.py:93` | `def check_port(port, name)` |
| `check_rhost` | function | `core/validators.py:55` | `def check_rhost(rhost)` |
| `_probe` | function | `deploy/range/ad-mini/traffic-gen.py:21` | `def _probe(host, port)` |
| `main` | function | `deploy/range/ad-mini/traffic-gen.py:35` | `def main()` |
| `Config` | class | `discord_c2.py:86` | `class Config` |
| `SecureSessionManager` | class | `discord_c2.py:27` | `class SecureSessionManager` |
| `__getitem__` | method | `discord_c2.py:92` | `def __getitem__(self, key)` |
| `__init__` | method | `discord_c2.py:28` | `def __init__(self)` |
| `__init__` | method | `discord_c2.py:87` | `def __init__(self, config_dict)` |
| `add_cli` | method | `discord_c2.py:206` | `def add_cli(ctx, new_client_id)` |
| `addcli` | method | `discord_c2.py:278` | `def addcli(ctx, new_client_id)` |
| `c2` | method | `discord_c2.py:283` | `def c2(ctx)` |
| `check_lockout` | method | `discord_c2.py:40` | `def check_lockout(self, user_id)` |
| `check_rate_limit` | method | `discord_c2.py:49` | `def check_rate_limit(self, user_id)` |
| `clients` | method | `discord_c2.py:273` | `def clients(ctx)` |
| `create_session` | method | `discord_c2.py:62` | `def create_session(self, user_id, client_id)` |
| `download_c2` | method | `discord_c2.py:245` | `def download_c2(ctx, client_id, file_name)` |
| `exce_cmd` | method | `discord_c2.py:130` | `def exce_cmd(ctx)` |
| `handle_file` | method | `discord_c2.py:216` | `def handle_file(ctx)` |
| `load_payload` | method | `discord_c2.py:96` | `def load_payload()` |
| `on_ready` | method | `discord_c2.py:103` | `def on_ready()` |
| `register_failed_attempt` | method | `discord_c2.py:33` | `def register_failed_attempt(self, user_id)` |
| `send_connected_clients` | method | `discord_c2.py:256` | `def send_connected_clients(ctx)` |
| `start` | method | `discord_c2.py:108` | `def start(ctx)` |
| `validate_session` | method | `discord_c2.py:70` | `def validate_session(self, user_id)` |
| `ctrl_c` | function | `external/install_external.sh:13` | `` |
| `download` | function | `external/install_external.sh:18` | `` |
| `_jq` | function | `fast_run_as_r00t.sh:31` | `` |
| `check_deps` | function | `fast_run_as_r00t.sh:74` | `` |
| `check_sudo` | function | `fast_run_as_r00t.sh:83` | `` |
| `ensure_gum` | function | `fast_run_as_r00t.sh:63` | `` |
| `err_box` | function | `fast_run_as_r00t.sh:57` | `` |
| `log` | function | `fast_run_as_r00t.sh:55` | `` |
| `parse_args` | function | `fast_run_as_r00t.sh:92` | `` |
| `spin` | function | `fast_run_as_r00t.sh:56` | `` |
| `start_chown_watcher` | function | `fast_run_as_r00t.sh:141` | `` |
| `t_lazyown` | function | `fast_run_as_r00t.sh:117` | `` |
| `t_priv_user` | function | `fast_run_as_r00t.sh:130` | `` |
| `t_send` | function | `fast_run_as_r00t.sh:110` | `` |
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
| `Alert` | class | `lazy_sentinel4.py:271` | `class Alert` |
| `App` | class | `lazy_sentinel4.py:544` | `class App(Cmd)` |
| `Database` | class | `lazy_sentinel4.py:214` | `class Database` |
| `LazySentinel` | class | `lazy_sentinel4.py:340` | `class LazySentinel` |
| `LazySentinelHandler` | class | `lazy_sentinel4.py:302` | `class LazySentinelHandler(FileSystemEventHandler)` |
| `RAGManager` | class | `lazy_sentinel4.py:58` | `class RAGManager` |
| `__init__` | method | `lazy_sentinel4.py:61` | `def __init__(self, model_name, cache_size)` |
| `__init__` | method | `lazy_sentinel4.py:215` | `def __init__(self, db_path)` |
| `__init__` | method | `lazy_sentinel4.py:274` | `def __init__(self, alert_type, details, severity)` |
| `__init__` | method | `lazy_sentinel4.py:303` | `def __init__(self, lazysentinel)` |
| `__init__` | method | `lazy_sentinel4.py:341` | `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)` |
| `__init__` | method | `lazy_sentinel4.py:545` | `def __init__(self)` |
| `chunk_text` | method | `lazy_sentinel4.py:361` | `def chunk_text(self, text, chunk_size)` |
| `complete_rag_add` | method | `lazy_sentinel4.py:699` | `def complete_rag_add(self, text, line, begidx, endidx)` |
| `complete_rag_bulk_add` | method | `lazy_sentinel4.py:706` | `def complete_rag_bulk_add(self, text, line, begidx, endidx)` |
| `display_toastr` | method | `lazy_sentinel4.py:559` | `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)` |
| `do_debug` | method | `lazy_sentinel4.py:615` | `def do_debug(self, arg)` |
| `do_quit` | method | `lazy_sentinel4.py:611` | `def do_quit(self, arg)` |
| `do_rag_add` | method | `lazy_sentinel4.py:632` | `def do_rag_add(self, arg)` |
| `do_rag_bulk_add` | method | `lazy_sentinel4.py:659` | `def do_rag_bulk_add(self, arg)` |
| `do_rag_query` | method | `lazy_sentinel4.py:624` | `def do_rag_query(self, arg)` |
| `do_rag_search` | method | `lazy_sentinel4.py:678` | `def do_rag_search(self, arg)` |
| `do_rag_status` | method | `lazy_sentinel4.py:647` | `def do_rag_status(self, arg)` |
| `do_rag_toggle` | method | `lazy_sentinel4.py:654` | `def do_rag_toggle(self, arg)` |
| `execute` | method | `lazy_sentinel4.py:243` | `def execute(self, query, params)` |
| `get_cache_key` | method | `lazy_sentinel4.py:85` | `def get_cache_key(self, content)` |
| `get_knowledge_base_stats` | method | `lazy_sentinel4.py:191` | `def get_knowledge_base_stats(self)` |
| `initialize` | method | `lazy_sentinel4.py:219` | `def initialize(self)` |
| `initialize_cache_table` | method | `lazy_sentinel4.py:73` | `def initialize_cache_table(self)` |
| `insert` | method | `lazy_sentinel4.py:255` | `def insert(self, query, params)` |
| `invalidate_cache` | method | `lazy_sentinel4.py:177` | `def invalidate_cache(self, file_path)` |
| `is_text_file` | method | `lazy_sentinel4.py:306` | `def is_text_file(self, file_path)` |
| `load_existing_vectorstore` | method | `lazy_sentinel4.py:88` | `def load_existing_vectorstore(self)` |
| `ollama_llm` | method | `lazy_sentinel4.py:101` | `def ollama_llm(self, question, context)` |
| `on_created` | method | `lazy_sentinel4.py:316` | `def on_created(self, event)` |
| `on_modified` | method | `lazy_sentinel4.py:328` | `def on_modified(self, event)` |
| `parse_deepseek_response` | method | `lazy_sentinel4.py:378` | `def parse_deepseek_response(self, response_text)` |
| `postcmd` | method | `lazy_sentinel4.py:587` | `def postcmd(self, stop, line)` |
| `process_file` | method | `lazy_sentinel4.py:422` | `def process_file(self, file_path)` |
| `process_file_to_rag` | method | `lazy_sentinel4.py:115` | `def process_file_to_rag(self, file_path)` |
| `query_rag` | method | `lazy_sentinel4.py:155` | `def query_rag(self, question)` |
| `sanitize_content` | function | `lazy_sentinel4.py:47` | `def sanitize_content(text)` |
| `save_to_db` | method | `lazy_sentinel4.py:288` | `def save_to_db(self, db)` |
| `select_relevant_chunk` | method | `lazy_sentinel4.py:364` | `def select_relevant_chunk(self, file_content, chunks)` |
| `show_popup` | method | `lazy_sentinel4.py:404` | `def show_popup(self, file_name, relevant_info, commands, details)` |
| `stop` | method | `lazy_sentinel4.py:538` | `def stop(self)` |
| `to_dict` | method | `lazy_sentinel4.py:280` | `def to_dict(self)` |
| `CustomDNSResolver` | class | `lazyc2.py:1711` | `class CustomDNSResolver(BaseResolver)` |
| `Handler` | class | `lazyc2.py:711` | `class Handler(FileSystemEventHandler)` |
| `User` | class | `lazyc2.py:2874` | `class User(UserMixin)` |
| `_JsonLogFormatter` | class | `lazyc2.py:424` | `class _JsonLogFormatter(Formatter)` |
| `__init__` | method | `lazyc2.py:2875` | `def __init__(self, user_data)` |
| `_add_security_headers` | method | `lazyc2.py:2456` | `def _add_security_headers(response)` |
| `_api_data_inner` | method | `lazyc2.py:4239` | `def _api_data_inner()` |
| `_append_beacon_record` | method | `lazyc2.py:1243` | `def _append_beacon_record(record)` |
| `_beacon_records_path` | method | `lazyc2.py:1236` | `def _beacon_records_path(client_id)` |
| `_bg_cred_reuse` | method | `lazyc2.py:3623` | `def _bg_cred_reuse(_ip)` |
| `_bootstrap_initial_admin` | method | `lazyc2.py:2598` | `def _bootstrap_initial_admin()` |
| `_build_privesc_command` | method | `lazyc2.py:3220` | `def _build_privesc_command(platform)` |
| `_enforce_https_redirect` | method | `lazyc2.py:2413` | `def _enforce_https_redirect()` |
| `_enforce_password_rotation` | method | `lazyc2.py:2433` | `def _enforce_password_rotation()` |
| `_engage_publish` | method | `lazyc2.py:3407` | `def _engage_publish(_cid, _ip, _host, _user, _platform)` |
| `_env_tag` | function | `lazyc2.py:175` | `def _env_tag()` |
| `_extract_first_ip` | method | `lazyc2.py:3463` | `def _extract_first_ip(raw)` |
| `_get_rbac_user_obj` | method | `lazyc2.py:2887` | `def _get_rbac_user_obj(flask_user)` |
| `_handle_404` | method | `lazyc2.py:2520` | `def _handle_404(_error)` |
| `_handle_405` | method | `lazyc2.py:2525` | `def _handle_405(_error)` |
| `_handle_exception` | method | `lazyc2.py:2530` | `def _handle_exception(error)` |
| `_ingest_beacon` | method | `lazyc2.py:3656` | `def _ingest_beacon(_ips, _host, _cmd, _out, _user)` |
| `_is_unspecified_bind_literal` | function | `lazyc2.py:262` | `def _is_unspecified_bind_literal(address)` |
| `_is_valid_credential` | method | `lazyc2.py:3476` | `def _is_valid_credential(value)` |
| `_listen_address` | function | `lazyc2.py:235` | `def _listen_address()` |
| `_load_or_create_secret_key` | method | `lazyc2.py:2473` | `def _load_or_create_secret_key()` |
| `_log_dns_bind_failure` | method | `lazyc2.py:1777` | `def _log_dns_bind_failure(address, error_number)` |
| `_metrics_before_request` | method | `lazyc2.py:2407` | `def _metrics_before_request()` |
| `_normalise_platform` | method | `lazyc2.py:3505` | `def _normalise_platform(raw_platform)` |
| `_persist_bootstrap_password` | method | `lazyc2.py:2578` | `def _persist_bootstrap_password(prefix, password)` |
| `_probe_bind` | function | `lazyc2.py:314` | `def _probe_bind(address, port, sock_type)` |
| `_queue_beacon_cmd` | method | `lazyc2.py:3516` | `def _queue_beacon_cmd(action, ctx)` |
| `_read_beacon_records` | method | `lazyc2.py:1273` | `def _read_beacon_records(client_id)` |
| `_render_enhanced_report` | method | `lazyc2.py:6403` | `def _render_enhanced_report()` |
| `_render_legacy_report` | method | `lazyc2.py:6423` | `def _render_legacy_report()` |
| `_resolve_bind_address` | function | `lazyc2.py:359` | `def _resolve_bind_address(preferred, port, sock_type)` |
| `_resolve_reverse_shell_password` | method | `lazyc2.py:4712` | `def _resolve_reverse_shell_password()` |
| `_resolve_secure_template_path` | method | `lazyc2.py:3905` | `def _resolve_secure_template_path(template_name)` |
| `_resolve_within` | method | `lazyc2.py:612` | `def _resolve_within(allowed_base, name)` |
| `_sanitize_command_output` | method | `lazyc2.py:542` | `def _sanitize_command_output(value)` |
| `_sanitize_csv_field` | method | `lazyc2.py:1193` | `def _sanitize_csv_field(value, maxlen)` |
| `_sanitize_html` | method | `lazyc2.py:1156` | `def _sanitize_html(raw_html)` |
| `_secure_command_queue_path` | method | `lazyc2.py:1206` | `def _secure_command_queue_path(client_id)` |
| `_select_specific_bind_address` | function | `lazyc2.py:281` | `def _select_specific_bind_address(candidate)` |
| `_try_copy_privesc_tool` | method | `lazyc2.py:3200` | `def _try_copy_privesc_tool(platform)` |
| `add_dynamic_data` | method | `lazyc2.py:2087` | `def add_dynamic_data(data)` |
| `admin_create_tenant` | method | `lazyc2.py:5872` | `def admin_create_tenant()` |
| `admin_delete_user` | method | `lazyc2.py:5833` | `def admin_delete_user(user_id)` |
| `admin_reset_mfa` | method | `lazyc2.py:5821` | `def admin_reset_mfa(user_id)` |
| `admin_set_role` | method | `lazyc2.py:5799` | `def admin_set_role(user_id)` |
| `admin_switch_tenant` | method | `lazyc2.py:5891` | `def admin_switch_tenant(tenant_id)` |
| `admin_tenants` | method | `lazyc2.py:5851` | `def admin_tenants()` |
| `admin_users` | method | `lazyc2.py:5784` | `def admin_users()` |
| `adversary` | method | `lazyc2.py:4900` | `def adversary()` |
| `aicmd` | method | `lazyc2.py:1522` | `def aicmd(cmd)` |
| `aicmd_deepseek` | method | `lazyc2.py:1408` | `def aicmd_deepseek(cmd)` |
| `aicmd_view` | method | `lazyc2.py:5326` | `def aicmd_view()` |
| `analyze_behavioral_data` | method | `lazyc2.py:2341` | `def analyze_behavioral_data(behavioral_events)` |
| `analyze_campaign_progress` | method | `lazyc2.py:2369` | `def analyze_campaign_progress(campaign_id, events)` |
| `api_beacon_results` | method | `lazyc2.py:6388` | `def api_beacon_results(client_id)` |
| `api_dashboard` | method | `lazyc2.py:7427` | `def api_dashboard()` |
| `api_data` | method | `lazyc2.py:4216` | `def api_data()` |
| `api_killchain` | method | `lazyc2.py:6357` | `def api_killchain()` |
| `api_listeners` | method | `lazyc2.py:7497` | `def api_listeners()` |
| `api_listeners_create` | method | `lazyc2.py:7504` | `def api_listeners_create()` |
| `api_listeners_delete` | method | `lazyc2.py:7536` | `def api_listeners_delete(listener_id)` |
| `api_listeners_start` | method | `lazyc2.py:7520` | `def api_listeners_start(listener_id)` |
| `api_listeners_stop` | method | `lazyc2.py:7528` | `def api_listeners_stop(listener_id)` |
| `api_surface_live` | method | `lazyc2.py:6854` | `def api_surface_live()` |
| `aumentar_elo` | method | `lazyc2.py:1095` | `def aumentar_elo(user_id, cantidad)` |
| `aumentar_elo_route` | method | `lazyc2.py:6010` | `def aumentar_elo_route(user_id)` |
| `authenticate` | method | `lazyc2.py:1346` | `def authenticate()` |
| `banners` | method | `lazyc2.py:6026` | `def banners()` |
| `campaign_report` | method | `lazyc2.py:7075` | `def campaign_report(campaign_id)` |
| `capture_audio` | method | `lazyc2.py:6815` | `def capture_audio()` |
| `capture_image` | method | `lazyc2.py:6789` | `def capture_image()` |
| `change_password` | method | `lazyc2.py:5944` | `def change_password()` |
| `chatbot` | method | `lazyc2.py:4778` | `def chatbot()` |
| `check_auth` | method | `lazyc2.py:1331` | `def check_auth(username, password)` |
| `clean_expired_tokens` | method | `lazyc2.py:593` | `def clean_expired_tokens()` |
| `clean_json` | method | `lazyc2.py:601` | `def clean_json(text)` |
| `compliance_add_evidence` | method | `lazyc2.py:6186` | `def compliance_add_evidence()` |
| `compliance_dashboard` | method | `lazyc2.py:6135` | `def compliance_dashboard()` |
| `compliance_export` | method | `lazyc2.py:6236` | `def compliance_export(format)` |
| `compliance_report` | method | `lazyc2.py:6157` | `def compliance_report()` |
| `compliance_verify_evidence` | method | `lazyc2.py:6222` | `def compliance_verify_evidence()` |
| `connect` | method | `lazyc2.py:6488` | `def connect()` |
| `create_campaign` | method | `lazyc2.py:6959` | `def create_campaign()` |
| `create_cves` | method | `lazyc2.py:1047` | `def create_cves()` |
| `create_multivector_campaign` | method | `lazyc2.py:7204` | `def create_multivector_campaign()` |
| `create_report` | method | `lazyc2.py:1066` | `def create_report()` |
| `create_route` | method | `lazyc2.py:3972` | `def create_route()` |
| `create_short_url` | method | `lazyc2.py:4378` | `def create_short_url()` |
| `create_tool` | method | `lazyc2.py:5393` | `def create_tool()` |
| `csrf_protect` | method | `lazyc2.py:1387` | `def csrf_protect(view)` |
| `csv_to_html` | method | `lazyc2.py:4932` | `def csv_to_html()` |
| `cve` | method | `lazyc2.py:5135` | `def cve(cve_id)` |
| `cves` | method | `lazyc2.py:5109` | `def cves()` |
| `datetime_now_iso` | method | `lazyc2.py:1201` | `def datetime_now_iso()` |
| `decorated` | method | `lazyc2.py:1365` | `def decorated()` |
| `decorated` | method | `lazyc2.py:1378` | `def decorated()` |
| `decoy` | method | `lazyc2.py:1899` | `def decoy()` |
| `decrypt_data` | method | `lazyc2.py:1946` | `def decrypt_data(encrypted_data, is_file)` |
| `delete_tool` | method | `lazyc2.py:5499` | `def delete_tool(toolname)` |
| `download_file` | method | `lazyc2.py:3843` | `def download_file()` |
| `download_files` | method | `lazyc2.py:4506` | `def download_files(filename)` |
| `dynamic_route` | method | `lazyc2.py:4041` | `def dynamic_route(route_path, data)` |
| `edit_cve` | method | `lazyc2.py:5150` | `def edit_cve(cve_id)` |
| `edit_event` | method | `lazyc2.py:5249` | `def edit_event(event_name)` |
| `edit_notes` | method | `lazyc2.py:5184` | `def edit_notes()` |
| `edit_task` | method | `lazyc2.py:5075` | `def edit_task(task_id)` |
| `encrypt_data` | method | `lazyc2.py:1937` | `def encrypt_data(data)` |
| `ensure_sessions_dir` | method | `lazyc2.py:454` | `def ensure_sessions_dir()` |
| `escape_js` | method | `lazyc2.py:1131` | `def escape_js(s)` |
| `escape_js_string` | method | `lazyc2.py:1319` | `def escape_js_string(value)` |
| `execute_command` | method | `lazyc2.py:1682` | `def execute_command(command)` |
| `extract_attack_vectors` | method | `lazyc2.py:838` | `def extract_attack_vectors(nodes, edges)` |
| `favicon` | method | `lazyc2.py:4155` | `def favicon()` |
| `format` | method | `lazyc2.py:427` | `def format(self, record)` |
| `fromjson` | method | `lazyc2.py:755` | `def fromjson(value)` |
| `generalbot` | method | `lazyc2.py:4916` | `def generalbot()` |
| `get_client_ip` | method | `lazyc2.py:2109` | `def get_client_ip()` |
| `get_config` | method | `lazyc2.py:6770` | `def get_config()` |
| `get_connected_clients` | method | `lazyc2.py:6107` | `def get_connected_clients()` |
| `get_data` | method | `lazyc2.py:6879` | `def get_data()` |
| `get_discovered_hosts` | method | `lazyc2.py:1982` | `def get_discovered_hosts()` |
| `get_event_config` | method | `lazyc2.py:5284` | `def get_event_config()` |
| `get_event_config_view` | method | `lazyc2.py:5291` | `def get_event_config_view()` |
| `get_events` | method | `lazyc2.py:5351` | `def get_events()` |
| `get_karma_name` | method | `lazyc2.py:738` | `def get_karma_name(elo)` |
| `get_local_ip_addresses` | method | `lazyc2.py:2032` | `def get_local_ip_addresses()` |
| `get_notes` | method | `lazyc2.py:5202` | `def get_notes()` |
| `get_output` | method | `lazyc2.py:4669` | `def get_output()` |
| `get_request_details` | method | `lazyc2.py:2118` | `def get_request_details()` |
| `get_results` | method | `lazyc2.py:4705` | `def get_results()` |
| `get_safe_file_path` | method | `lazyc2.py:2271` | `def get_safe_file_path(user_path)` |
| `get_tasks` | method | `lazyc2.py:5055` | `def get_tasks()` |
| `graph` | method | `lazyc2.py:5031` | `def graph()` |
| `handle_client` | method | `lazyc2.py:1880` | `def handle_client(client_socket, remote_host, remote_port)` |
| `handle_input` | method | `lazyc2.py:6585` | `def handle_input(data)` |
| `health_check` | method | `lazyc2.py:7381` | `def health_check()` |
| `implants_check` | method | `lazyc2.py:821` | `def implants_check()` |
| `index` | method | `lazyc2.py:2957` | `def index()` |
| `internal_server_error` | method | `lazyc2.py:6761` | `def internal_server_error(e)` |
| `is_binary` | method | `lazyc2.py:552` | `def is_binary(safe_filename)` |
| `is_insecure_credential` | function | `lazyc2.py:187` | `def is_insecure_credential(user, pwd)` |
| `is_safe_template_path` | method | `lazyc2.py:512` | `def is_safe_template_path(template_path, template_name)` |
| `is_valid_data` | method | `lazyc2.py:4065` | `def is_valid_data(data)` |
| `is_valid_route_path` | method | `lazyc2.py:4058` | `def is_valid_route_path(route_path)` |
| `is_valid_template_name` | method | `lazyc2.py:4075` | `def is_valid_template_name(template_name)` |
| `is_valid_url` | method | `lazyc2.py:2263` | `def is_valid_url(url)` |
| `issue_command` | method | `lazyc2.py:3792` | `def issue_command()` |
| `killchain_view` | method | `lazyc2.py:6327` | `def killchain_view()` |
| `lazybot` | method | `lazyc2.py:6118` | `def lazybot()` |
| `lazyphishingai` | method | `lazyc2.py:7037` | `def lazyphishingai()` |
| `lazyreport` | method | `lazyc2.py:6266` | `def lazyreport()` |
| `lazyreport_view` | method | `lazyc2.py:6321` | `def lazyreport_view()` |
| `list_campaigns` | method | `lazyc2.py:6946` | `def list_campaigns()` |
| `list_tools` | method | `lazyc2.py:5383` | `def list_tools()` |
| `listener` | method | `lazyc2.py:6497` | `def listener()` |
| `listener_command` | method | `lazyc2.py:6609` | `def listener_command(msg)` |

Next: [SYMBOLS_p8.md](SYMBOLS_p8.md)
