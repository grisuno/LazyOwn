# Symbols (page 7 of 38)
Previous: [SYMBOLS_p6.md](SYMBOLS_p6.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_emit` | function | `core/console.py:208` | `def _emit(line)` |
| `_paint` | function | `core/console.py:114` | `def _paint(code, text)` |
| `_sanitize` | function | `core/console.py:93` | `def _sanitize(text)` |
| `colors_enabled` | function | `core/console.py:98` | `def colors_enabled()` |
| `ensure_blocking_stdio` | function | `core/console.py:161` | `def ensure_blocking_stdio()` |
| `format_line` | function | `core/console.py:121` | `def format_line(prefix, message, glyph)` |
| `print_error` | function | `core/console.py:137` | `def print_error(error)` |
| `print_msg` | function | `core/console.py:143` | `def print_msg(msg)` |
| `print_succ` | function | `core/console.py:155` | `def print_succ(msg)` |
| `print_warn` | function | `core/console.py:149` | `def print_warn(warn)` |
| `write_stdout` | function | `core/console.py:180` | `def write_stdout(text)` |
| `_get_aes_key` | function | `core/credential_vault.py:79` | `def _get_aes_key(payload)` |
| `check_dangerous_defaults` | function | `core/credential_vault.py:63` | `def check_dangerous_defaults(payload)` |
| `generate_secure_defaults` | function | `core/credential_vault.py:215` | `def generate_secure_defaults()` |
| `rotate_aes_key` | function | `core/credential_vault.py:186` | `def rotate_aes_key(payload, current_key)` |
| `seal_payload` | function | `core/credential_vault.py:141` | `def seal_payload(payload, key)` |
| `seal_value` | function | `core/credential_vault.py:93` | `def seal_value(plaintext, key)` |
| `unseal_payload` | function | `core/credential_vault.py:164` | `def unseal_payload(payload, key)` |
| `unseal_value` | function | `core/credential_vault.py:112` | `def unseal_value(sealed, key)` |
| `AESdecrypt` | function | `core/crypto.py:123` | `def AESdecrypt(data, key)` |
| `AESencrypt` | function | `core/crypto.py:98` | `def AESencrypt(plaintext, key)` |
| `derive_key` | function | `core/crypto.py:36` | `def derive_key(password, salt)` |
| `dropFile` | function | `core/crypto.py:154` | `def dropFile(key, ciphertext)` |
| `generate_salt` | function | `core/crypto.py:24` | `def generate_salt(length)` |
| `generate_xor_key` | function | `core/crypto.py:83` | `def generate_xor_key(length)` |
| `xor_encrypt_decrypt` | function | `core/crypto.py:67` | `def xor_encrypt_decrypt(data, key)` |
| `clear_cache` | function | `core/defaults.py:44` | `def clear_cache()` |
| `common_wordlists` | function | `core/defaults.py:90` | `def common_wordlists()` |
| `default_lport` | function | `core/defaults.py:63` | `def default_lport()` |
| `default_rport` | function | `core/defaults.py:72` | `def default_rport()` |
| `get` | function | `core/defaults.py:49` | `def get(section, key, default)` |
| `load_defaults` | function | `core/defaults.py:21` | `def load_defaults(path)` |
| `rockyou_wordlist` | function | `core/defaults.py:81` | `def rockyou_wordlist()` |
| `sessions_dir` | function | `core/defaults.py:100` | `def sessions_dir()` |
| `DependencyReport` | class | `core/dependencies.py:268` | `class DependencyReport` |
| `DependencySpec` | class | `core/dependencies.py:66` | `class DependencySpec` |
| `DependencyStatus` | class | `core/dependencies.py:253` | `class DependencyStatus` |
| `MissingDependencyError` | class | `core/dependencies.py:37` | `class MissingDependencyError(ImportError)` |
| `_DeferredImport` | class | `core/dependencies.py:101` | `class _DeferredImport` |
| `__bool__` | method | `core/dependencies.py:152` | `def __bool__(self)` |
| `__call__` | method | `core/dependencies.py:136` | `def __call__(self)` |
| `__getattr__` | method | `core/dependencies.py:132` | `def __getattr__(self, _name)` |
| `__getitem__` | method | `core/dependencies.py:140` | `def __getitem__(self, _key)` |
| `__init__` | method | `core/dependencies.py:45` | `def __init__(self, import_name, pip_package, feature)` |
| `__init__` | method | `core/dependencies.py:115` | `def __init__(self, spec)` |
| `__iter__` | method | `core/dependencies.py:144` | `def __iter__(self)` |
| `__len__` | method | `core/dependencies.py:148` | `def __len__(self)` |
| `_raise` | method | `core/dependencies.py:123` | `def _raise(self)` |
| `_spec_for` | method | `core/dependencies.py:157` | `def _spec_for(import_name, pip_package, feature)` |
| `collect_dependency_report` | method | `core/dependencies.py:312` | `def collect_dependency_report()` |
| `format_report` | method | `core/dependencies.py:323` | `def format_report(report)` |
| `main` | method | `core/dependencies.py:368` | `def main()` |
| `missing` | method | `core/dependencies.py:278` | `def missing(self)` |
| `ok` | method | `core/dependencies.py:283` | `def ok(self)` |
| `optional_attr` | method | `core/dependencies.py:209` | `def optional_attr(import_name, attr)` |
| `optional_import` | method | `core/dependencies.py:183` | `def optional_import(import_name)` |
| `probe_python_dependency` | method | `core/dependencies.py:288` | `def probe_python_dependency(spec)` |
| `ErrorAdvice` | class | `core/error_advice.py:27` | `class ErrorAdvice` |
| `ErrorAdviceConfig` | class | `core/error_advice.py:16` | `class ErrorAdviceConfig` |
| `docs_url` | method | `core/error_advice.py:35` | `def docs_url(self, config)` |
| `get_advice` | method | `core/error_advice.py:74` | `def get_advice(key)` |
| `render_advice` | method | `core/error_advice.py:86` | `def render_advice(key, config)` |
| `AuthError` | class | `core/errors.py:92` | `class AuthError(LazyOwnError)` |
| `ConfigError` | class | `core/errors.py:78` | `class ConfigError(LazyOwnError)` |
| `DatabaseError` | class | `core/errors.py:113` | `class DatabaseError(LazyOwnError)` |
| `ErrorCode` | class | `core/errors.py:10` | `class ErrorCode(IntEnum)` |
| `LazyOwnError` | class | `core/errors.py:58` | `class LazyOwnError(Exception)` |
| `NetworkError` | class | `core/errors.py:120` | `class NetworkError(LazyOwnError)` |
| `PayloadError` | class | `core/errors.py:106` | `class PayloadError(LazyOwnError)` |
| `PermissionError` | class | `core/errors.py:127` | `class PermissionError(LazyOwnError)` |
| `TargetError` | class | `core/errors.py:85` | `class TargetError(LazyOwnError)` |
| `ToolError` | class | `core/errors.py:99` | `class ToolError(LazyOwnError)` |
| `ValidationError` | class | `core/errors.py:134` | `class ValidationError(LazyOwnError)` |
| `__init__` | method | `core/errors.py:61` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:81` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:88` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:95` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:102` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:109` | `def __init__(self, message, error_code)` |
| `__init__` | method | `core/errors.py:116` | `def __init__(self, message, error_code)` |
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
| `SecurityViolation` | class | `core/hardening.py:82` | `class SecurityViolation(PermissionError)` |
| `build_sshpass_command` | method | `core/hardening.py:191` | `def build_sshpass_command(password, ssh_args)` |
| `defused_xml_parse` | method | `core/hardening.py:353` | `def defused_xml_parse(source)` |
| `escape_html_content` | method | `core/hardening.py:239` | `def escape_html_content(value)` |
| `escape_powershell_single_quoted` | function | `core/hardening.py:61` | `def escape_powershell_single_quoted(value)` |
| `reject_option_injection` | function | `core/hardening.py:42` | `def reject_option_injection(argv)` |
| `require_encryption_key` | method | `core/hardening.py:325` | `def require_encryption_key(env_key, secret_file)` |
| `safe_clipboard_copy` | method | `core/hardening.py:152` | `def safe_clipboard_copy(content)` |
| `safe_path_join` | method | `core/hardening.py:251` | `def safe_path_join(base_dir, user_path)` |
| `safe_subprocess_run` | method | `core/hardening.py:107` | `def safe_subprocess_run(argv)` |
| `sanitize_filename` | method | `core/hardening.py:375` | `def sanitize_filename(filename, max_length)` |
| `set_sshpass_env` | method | `core/hardening.py:220` | `def set_sshpass_env(password)` |
| `terminal_env` | method | `core/hardening.py:86` | `def terminal_env(base)` |
| `validate_host` | method | `core/hardening.py:305` | `def validate_host(host)` |
| `validate_network_cidr` | method | `core/hardening.py:277` | `def validate_network_cidr(cidr)` |
| `validate_port_spec` | method | `core/hardening.py:289` | `def validate_port_spec(ports)` |
| `is_valid_cidr` | function | `core/host_policy.py:32` | `def is_valid_cidr(value)` |
| `is_valid_host` | function | `core/host_policy.py:48` | `def is_valid_host(value)` |
| `rejects_shell_meta` | function | `core/host_policy.py:20` | `def rejects_shell_meta(value)` |
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
| `strip_ansi` | function | `core/parsers.py:15` | `def strip_ansi(text)` |
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
| `get_console` | function | `core/safe_console.py:42` | `def get_console()` |
| `milestone_glyph` | function | `core/safe_console.py:57` | `def milestone_glyph(state)` |
| `panel_box` | function | `core/safe_console.py:52` | `def panel_box()` |
| `progress_bar` | function | `core/safe_console.py:67` | `def progress_bar(ratio, width)` |
| `supports_unicode` | function | `core/safe_console.py:33` | `def supports_unicode()` |
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
| `check_lhost` | function | `core/validators.py:41` | `def check_lhost(lhost)` |
| `check_lport` | function | `core/validators.py:55` | `def check_lport(lport)` |
| `check_port` | function | `core/validators.py:65` | `def check_port(port, name)` |
| `check_rhost` | function | `core/validators.py:27` | `def check_rhost(rhost)` |
| `require_lhost` | function | `core/validators.py:95` | `def require_lhost(params)` |
| `require_lport` | function | `core/validators.py:108` | `def require_lport(params)` |
| `require_rhost` | function | `core/validators.py:78` | `def require_rhost(params)` |
| `require_rport` | function | `core/validators.py:121` | `def require_rport(params)` |
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
| `CustomDNSResolver` | class | `lazyc2.py:1710` | `class CustomDNSResolver(BaseResolver)` |
| `Handler` | class | `lazyc2.py:710` | `class Handler(FileSystemEventHandler)` |
| `User` | class | `lazyc2.py:2943` | `class User(UserMixin)` |
| `_JsonLogFormatter` | class | `lazyc2.py:423` | `class _JsonLogFormatter(Formatter)` |
| `_LazyShellProxy` | class | `lazyc2.py:2600` | `class _LazyShellProxy` |
| `__getattr__` | method | `lazyc2.py:2580` | `def __getattr__(name)` |
| `__getattr__` | method | `lazyc2.py:2612` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyc2.py:2944` | `def __init__(self, user_data)` |
| `__setattr__` | method | `lazyc2.py:2616` | `def __setattr__(self, name, value)` |
| `_add_security_headers` | method | `lazyc2.py:2455` | `def _add_security_headers(response)` |
| `_api_data_inner` | method | `lazyc2.py:4308` | `def _api_data_inner()` |
| `_append_beacon_record` | method | `lazyc2.py:1242` | `def _append_beacon_record(record)` |
| `_beacon_records_path` | method | `lazyc2.py:1235` | `def _beacon_records_path(client_id)` |
| `_bg_cred_reuse` | method | `lazyc2.py:3692` | `def _bg_cred_reuse(_ip)` |
| `_bootstrap_initial_admin` | method | `lazyc2.py:2667` | `def _bootstrap_initial_admin()` |
| `_build_privesc_command` | method | `lazyc2.py:3289` | `def _build_privesc_command(platform)` |
| `_enforce_https_redirect` | method | `lazyc2.py:2412` | `def _enforce_https_redirect()` |
| `_enforce_password_rotation` | method | `lazyc2.py:2432` | `def _enforce_password_rotation()` |
| `_engage_publish` | method | `lazyc2.py:3476` | `def _engage_publish(_cid, _ip, _host, _user, _platform)` |
| `_env_tag` | function | `lazyc2.py:174` | `def _env_tag()` |
| `_extract_first_ip` | method | `lazyc2.py:3532` | `def _extract_first_ip(raw)` |
| `_get_rbac_user_obj` | method | `lazyc2.py:2956` | `def _get_rbac_user_obj(flask_user)` |
| `_handle_404` | method | `lazyc2.py:2519` | `def _handle_404(_error)` |
| `_handle_405` | method | `lazyc2.py:2524` | `def _handle_405(_error)` |
| `_handle_exception` | method | `lazyc2.py:2529` | `def _handle_exception(error)` |
| `_ingest_beacon` | method | `lazyc2.py:3725` | `def _ingest_beacon(_ips, _host, _cmd, _out, _user)` |
| `_init_shell` | method | `lazyc2.py:2553` | `def _init_shell()` |
| `_is_unspecified_bind_literal` | function | `lazyc2.py:261` | `def _is_unspecified_bind_literal(address)` |
| `_is_valid_credential` | method | `lazyc2.py:3545` | `def _is_valid_credential(value)` |
| `_listen_address` | function | `lazyc2.py:234` | `def _listen_address()` |
| `_load_or_create_secret_key` | method | `lazyc2.py:2472` | `def _load_or_create_secret_key()` |
| `_log_dns_bind_failure` | method | `lazyc2.py:1776` | `def _log_dns_bind_failure(address, error_number)` |
| `_metrics_before_request` | method | `lazyc2.py:2406` | `def _metrics_before_request()` |
| `_normalise_platform` | method | `lazyc2.py:3574` | `def _normalise_platform(raw_platform)` |
| `_persist_bootstrap_password` | method | `lazyc2.py:2647` | `def _persist_bootstrap_password(prefix, password)` |
| `_probe_bind` | function | `lazyc2.py:313` | `def _probe_bind(address, port, sock_type)` |
| `_queue_beacon_cmd` | method | `lazyc2.py:3585` | `def _queue_beacon_cmd(action, ctx)` |
| `_read_beacon_records` | method | `lazyc2.py:1272` | `def _read_beacon_records(client_id)` |
| `_render_enhanced_report` | method | `lazyc2.py:6472` | `def _render_enhanced_report()` |
| `_render_legacy_report` | method | `lazyc2.py:6492` | `def _render_legacy_report()` |
| `_resolve_bind_address` | function | `lazyc2.py:358` | `def _resolve_bind_address(preferred, port, sock_type)` |
| `_resolve_reverse_shell_password` | method | `lazyc2.py:4781` | `def _resolve_reverse_shell_password()` |
| `_resolve_secure_template_path` | method | `lazyc2.py:3974` | `def _resolve_secure_template_path(template_name)` |
| `_resolve_within` | method | `lazyc2.py:611` | `def _resolve_within(allowed_base, name)` |
| `_sanitize_command_output` | method | `lazyc2.py:541` | `def _sanitize_command_output(value)` |
| `_sanitize_csv_field` | method | `lazyc2.py:1192` | `def _sanitize_csv_field(value, maxlen)` |
| `_sanitize_html` | method | `lazyc2.py:1155` | `def _sanitize_html(raw_html)` |
| `_secure_command_queue_path` | method | `lazyc2.py:1205` | `def _secure_command_queue_path(client_id)` |
| `_select_specific_bind_address` | function | `lazyc2.py:280` | `def _select_specific_bind_address(candidate)` |
| `_target` | method | `lazyc2.py:2608` | `def _target(self)` |
| `_try_copy_privesc_tool` | method | `lazyc2.py:3269` | `def _try_copy_privesc_tool(platform)` |
| `add_dynamic_data` | method | `lazyc2.py:2086` | `def add_dynamic_data(data)` |
| `admin_create_tenant` | method | `lazyc2.py:5941` | `def admin_create_tenant()` |
| `admin_delete_user` | method | `lazyc2.py:5902` | `def admin_delete_user(user_id)` |
| `admin_reset_mfa` | method | `lazyc2.py:5890` | `def admin_reset_mfa(user_id)` |
| `admin_set_role` | method | `lazyc2.py:5868` | `def admin_set_role(user_id)` |
| `admin_switch_tenant` | method | `lazyc2.py:5960` | `def admin_switch_tenant(tenant_id)` |
| `admin_tenants` | method | `lazyc2.py:5920` | `def admin_tenants()` |
| `admin_users` | method | `lazyc2.py:5853` | `def admin_users()` |
| `adversary` | method | `lazyc2.py:4969` | `def adversary()` |
| `aicmd` | method | `lazyc2.py:1521` | `def aicmd(cmd)` |
| `aicmd_deepseek` | method | `lazyc2.py:1407` | `def aicmd_deepseek(cmd)` |
| `aicmd_view` | method | `lazyc2.py:5395` | `def aicmd_view()` |
| `analyze_behavioral_data` | method | `lazyc2.py:2340` | `def analyze_behavioral_data(behavioral_events)` |
| `analyze_campaign_progress` | method | `lazyc2.py:2368` | `def analyze_campaign_progress(campaign_id, events)` |
| `api_attack_bundle` | method | `lazyc2.py:7157` | `def api_attack_bundle()` |
| `api_attack_graph` | method | `lazyc2.py:7105` | `def api_attack_graph()` |
| `api_beacon_results` | method | `lazyc2.py:6457` | `def api_beacon_results(client_id)` |
| `api_dashboard` | method | `lazyc2.py:7735` | `def api_dashboard()` |
| `api_data` | method | `lazyc2.py:4285` | `def api_data()` |
| `api_intel_bundle` | method | `lazyc2.py:7072` | `def api_intel_bundle()` |
| `api_intel_graph` | method | `lazyc2.py:7016` | `def api_intel_graph()` |
| `api_killchain` | method | `lazyc2.py:6426` | `def api_killchain()` |
| `api_listeners` | method | `lazyc2.py:7805` | `def api_listeners()` |
| `api_listeners_create` | method | `lazyc2.py:7812` | `def api_listeners_create()` |
| `api_listeners_delete` | method | `lazyc2.py:7844` | `def api_listeners_delete(listener_id)` |
| `api_listeners_start` | method | `lazyc2.py:7828` | `def api_listeners_start(listener_id)` |
| `api_listeners_stop` | method | `lazyc2.py:7836` | `def api_listeners_stop(listener_id)` |
| `api_surface_live` | method | `lazyc2.py:6923` | `def api_surface_live()` |
| `attack3d_view` | method | `lazyc2.py:6982` | `def attack3d_view()` |
| `attack_bundle_view` | method | `lazyc2.py:7001` | `def attack_bundle_view()` |
| `aumentar_elo` | method | `lazyc2.py:1094` | `def aumentar_elo(user_id, cantidad)` |
| `aumentar_elo_route` | method | `lazyc2.py:6079` | `def aumentar_elo_route(user_id)` |
| `authenticate` | method | `lazyc2.py:1345` | `def authenticate()` |
| `banners` | method | `lazyc2.py:6095` | `def banners()` |
| `campaign_report` | method | `lazyc2.py:7383` | `def campaign_report(campaign_id)` |
| `capture_audio` | method | `lazyc2.py:6884` | `def capture_audio()` |
| `capture_image` | method | `lazyc2.py:6858` | `def capture_image()` |

Next: [SYMBOLS_p8.md](SYMBOLS_p8.md)
