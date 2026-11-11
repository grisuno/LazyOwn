# Symbols (page 8 of 51)
Previous: [SYMBOLS_p7.md](SYMBOLS_p7.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `_spec_for` | function | `core/dependencies.py:157` | `def _spec_for(import_name, pip_package, feature)` |
| `collect_dependency_report` | function | `core/dependencies.py:312` | `def collect_dependency_report()` |
| `format_report` | function | `core/dependencies.py:323` | `def format_report(report)` |
| `main` | function | `core/dependencies.py:368` | `def main()` |
| `missing` | method | `core/dependencies.py:278` | `def missing(self)` |
| `ok` | method | `core/dependencies.py:283` | `def ok(self)` |
| `optional_attr` | function | `core/dependencies.py:209` | `def optional_attr(import_name, attr)` |
| `optional_import` | function | `core/dependencies.py:183` | `def optional_import(import_name)` |
| `probe_python_dependency` | function | `core/dependencies.py:288` | `def probe_python_dependency(spec)` |
| `ErrorAdvice` | class | `core/error_advice.py:27` | `class ErrorAdvice` |
| `ErrorAdviceConfig` | class | `core/error_advice.py:16` | `class ErrorAdviceConfig` |
| `docs_url` | method | `core/error_advice.py:35` | `def docs_url(self, config)` |
| `get_advice` | function | `core/error_advice.py:74` | `def get_advice(key)` |
| `render_advice` | function | `core/error_advice.py:86` | `def render_advice(key, config)` |
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
| `SecurityViolation` | class | `core/hardening.py:133` | `class SecurityViolation(PermissionError)` |
| `_is_emoji_codepoint` | function | `core/hardening.py:714` | `def _is_emoji_codepoint(code)` |
| `_mask` | function | `core/hardening.py:853` | `def _mask(match)` |
| `_seal_key` | function | `core/hardening.py:756` | `def _seal_key(sessions_dir)` |
| `build_sshpass_command` | function | `core/hardening.py:250` | `def build_sshpass_command(password, ssh_args)` |
| `contains_emoji` | function | `core/hardening.py:722` | `def contains_emoji(text)` |
| `defused_xml_parse` | function | `core/hardening.py:412` | `def defused_xml_parse(source)` |
| `escape_html_content` | function | `core/hardening.py:298` | `def escape_html_content(value)` |
| `escape_powershell_single_quoted` | function | `core/hardening.py:112` | `def escape_powershell_single_quoted(value)` |
| `is_safe_dir_path` | function | `core/hardening.py:578` | `def is_safe_dir_path(raw)` |
| `is_safe_path_segment` | function | `core/hardening.py:557` | `def is_safe_path_segment(segment)` |
| `is_safe_yaml_name` | function | `core/hardening.py:604` | `def is_safe_yaml_name(name)` |
| `iter_emoji_spans` | function | `core/hardening.py:737` | `def iter_emoji_spans(text)` |
| `redact_text` | function | `core/hardening.py:842` | `def redact_text(text)` |
| `reject_option_injection` | function | `core/hardening.py:93` | `def reject_option_injection(argv)` |
| `require_encryption_key` | function | `core/hardening.py:384` | `def require_encryption_key(env_key, secret_file)` |
| `safe_clipboard_copy` | function | `core/hardening.py:211` | `def safe_clipboard_copy(content)` |
| `safe_join_under` | function | `core/hardening.py:623` | `def safe_join_under(base_dir, user_path)` |
| `safe_open_under` | function | `core/hardening.py:652` | `def safe_open_under(base_dir, user_path, mode)` |
| `safe_path_join` | function | `core/hardening.py:310` | `def safe_path_join(base_dir, user_path)` |
| `safe_subprocess_run` | function | `core/hardening.py:158` | `def safe_subprocess_run(argv)` |
| `sanitize_filename` | function | `core/hardening.py:434` | `def sanitize_filename(filename, max_length)` |
| `seal_secret` | function | `core/hardening.py:770` | `def seal_secret(plaintext)` |
| `set_sshpass_env` | function | `core/hardening.py:279` | `def set_sshpass_env(password)` |
| `store_secret_owner_only` | function | `core/hardening.py:679` | `def store_secret_owner_only(path, text)` |
| `terminal_env` | function | `core/hardening.py:137` | `def terminal_env(base)` |
| `tls_lab_fallback_context` | function | `core/hardening.py:506` | `def tls_lab_fallback_context()` |
| `tls_lab_unverified_allowed` | function | `core/hardening.py:479` | `def tls_lab_unverified_allowed(host)` |
| `tls_secure_context` | function | `core/hardening.py:454` | `def tls_secure_context(extra_ca)` |
| `unseal_secret` | function | `core/hardening.py:801` | `def unseal_secret(stored)` |
| `validate_host` | function | `core/hardening.py:364` | `def validate_host(host)` |
| `validate_network_cidr` | function | `core/hardening.py:336` | `def validate_network_cidr(cidr)` |
| `validate_port_spec` | function | `core/hardening.py:348` | `def validate_port_spec(ports)` |
| `validate_upstream_path` | function | `core/hardening.py:528` | `def validate_upstream_path(path)` |
| `is_engagement_target` | function | `core/host_policy.py:95` | `def is_engagement_target(value)` |
| `is_file_like` | function | `core/host_policy.py:77` | `def is_file_like(value)` |
| `is_valid_cidr` | function | `core/host_policy.py:36` | `def is_valid_cidr(value)` |
| `is_valid_host` | function | `core/host_policy.py:52` | `def is_valid_host(value)` |
| `rejects_shell_meta` | function | `core/host_policy.py:24` | `def rejects_shell_meta(value)` |
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
| `_coerce_bool` | function | `core/llm_budget.py:476` | `def _coerce_bool(value, default)` |
| `_coerce_positive_float` | function | `core/llm_budget.py:520` | `def _coerce_positive_float(value, default)` |
| `_coerce_positive_int` | function | `core/llm_budget.py:536` | `def _coerce_positive_int(value, default)` |
| `_coerce_price_table` | function | `core/llm_budget.py:496` | `def _coerce_price_table(value)` |
| `_empty_state` | method | `core/llm_budget.py:189` | `def _empty_state(self)` |
| `_has_required_methods` | function | `core/llm_budget.py:642` | `def _has_required_methods(backend)` |
| `_load` | method | `core/llm_budget.py:193` | `def _load(self)` |
| `_load_encoding` | method | `core/llm_budget.py:283` | `def _load_encoding(encoding_name)` |
| `_now_iso` | function | `core/llm_budget.py:163` | `def _now_iso(now)` |
| `_save` | method | `core/llm_budget.py:215` | `def _save(self, state)` |
| `_state` | method | `core/llm_budget.py:226` | `def _state(self)` |
| `_today_utc` | function | `core/llm_budget.py:150` | `def _today_utc(now)` |
| `calls_today` | method | `core/llm_budget.py:256` | `def calls_today(self)` |
| `complete` | method | `core/llm_budget.py:65` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `core/llm_budget.py:435` | `def complete(self, system, user, max_tokens, temperature)` |
| `count` | method | `core/llm_budget.py:292` | `def count(self, text)` |
| `default_model_prices` | function | `core/llm_budget.py:442` | `def default_model_prices()` |
| `default_sessions_dir` | function | `core/llm_budget.py:461` | `def default_sessions_dir()` |
| `estimate_and_check` | method | `core/llm_budget.py:356` | `def estimate_and_check(self, prompt, model, output_tokens)` |
| `estimate_cost` | method | `core/llm_budget.py:343` | `def estimate_cost(self, model, input_tokens, output_tokens)` |
| `format_budget_status` | function | `core/llm_budget.py:616` | `def format_budget_status(config, ledger)` |
| `from_mapping` | method | `core/llm_budget.py:81` | `def from_mapping(cls, data)` |
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
| `KeyPool` | class | `core/llm_key_pool.py:67` | `class KeyPool` |
| `__init__` | method | `core/llm_key_pool.py:76` | `def __init__(self, cooldown_sec)` |
| `_dedupe` | function | `core/llm_key_pool.py:55` | `def _dedupe(keys)` |
| `_is_real_key` | function | `core/llm_key_pool.py:39` | `def _is_real_key(value)` |
| `_pool_entries` | function | `core/llm_key_pool.py:179` | `def _pool_entries(raw)` |
| `available` | method | `core/llm_key_pool.py:163` | `def available(self, backend, now)` |
| `build_from_config` | function | `core/llm_key_pool.py:208` | `def build_from_config(config, pool)` |
| `get_key_pool` | function | `core/llm_key_pool.py:238` | `def get_key_pool()` |
| `has_pool` | method | `core/llm_key_pool.py:107` | `def has_pool(self, backend)` |
| `mark_exhausted` | method | `core/llm_key_pool.py:149` | `def mark_exhausted(self, backend, key, now)` |
| `next_key` | method | `core/llm_key_pool.py:117` | `def next_key(self, backend, now)` |
| `note_quota_error` | function | `core/llm_key_pool.py:274` | `def note_quota_error(backend, key)` |
| `refresh_from_config` | function | `core/llm_key_pool.py:243` | `def refresh_from_config(config)` |
| `reset` | method | `core/llm_key_pool.py:171` | `def reset(self)` |
| `resolve_pooled_key` | function | `core/llm_key_pool.py:249` | `def resolve_pooled_key(backend, config, fallback)` |
| `set_keys` | method | `core/llm_key_pool.py:88` | `def set_keys(self, backend, keys)` |
| `size` | method | `core/llm_key_pool.py:112` | `def size(self, backend)` |
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
| `_load_operator_specs` | function | `core/payload_schema.py:2186` | `def _load_operator_specs()` |
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
| `categories` | function | `core/payload_schema.py:2174` | `def categories()` |
| `coerce_value` | function | `core/payload_schema.py:2016` | `def coerce_value(key, raw)` |
| `default_payload` | function | `core/payload_schema.py:2166` | `def default_payload()` |
| `field_for` | function | `core/payload_schema.py:2011` | `def field_for(key)` |
| `format_issue` | function | `core/payload_schema.py:2148` | `def format_issue(issue)` |
| `register_specs` | function | `core/payload_schema.py:1970` | `def register_specs(specs)` |
| `unregister_specs` | function | `core/payload_schema.py:1993` | `def unregister_specs(keys)` |
| `validate_payload` | function | `core/payload_schema.py:2113` | `def validate_payload(payload)` |
| `validate_value` | function | `core/payload_schema.py:2039` | `def validate_value(key, value)` |
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
| `CommandInjectionError` | class | `core/safe_exec.py:49` | `class CommandInjectionError(PermissionError)` |
| `UrlValidationError` | class | `core/safe_exec.py:53` | `class UrlValidationError(PermissionError)` |
| `_communicate_group_managed` | function | `core/safe_exec.py:141` | `def _communicate_group_managed(process, timeout)` |
| `_kill_process_tree` | function | `core/safe_exec.py:111` | `def _kill_process_tree(process)` |
| `needs_shell` | function | `core/safe_exec.py:57` | `def needs_shell(command)` |
| `safe_clear_screen` | function | `core/safe_exec.py:285` | `def safe_clear_screen()` |
| `safe_file_read` | function | `core/safe_exec.py:414` | `def safe_file_read(path)` |
| `safe_find_tool` | function | `core/safe_exec.py:398` | `def safe_find_tool(name)` |
| `safe_git_clone` | function | `core/safe_exec.py:327` | `def safe_git_clone(repo_url, target_dir)` |
| `safe_ip_show` | function | `core/safe_exec.py:361` | `def safe_ip_show(interface)` |
| `safe_run_argv` | function | `core/safe_exec.py:174` | `def safe_run_argv(argv)` |
| `safe_run_shell` | function | `core/safe_exec.py:228` | `def safe_run_shell(command)` |
| `safe_system` | function | `core/safe_exec.py:74` | `def safe_system(command)` |
| `validate_url` | function | `core/safe_exec.py:300` | `def validate_url(url)` |
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
| `_mirror` | function | `core/session_secrets.py:115` | `def _mirror(config_obj, aes_hex, rat_key, session_magic)` |
| `_valid_session_token` | function | `core/session_secrets.py:106` | `def _valid_session_token(value, hex_len)` |
| `ensure_session_secrets` | function | `core/session_secrets.py:72` | `def ensure_session_secrets(config_obj, rotate, sessions_dir)` |
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
| `CustomDNSResolver` | class | `lazyc2.py:1867` | `class CustomDNSResolver(BaseResolver)` |
| `Handler` | class | `lazyc2.py:766` | `class Handler(FileSystemEventHandler)` |
| `User` | class | `lazyc2.py:3268` | `class User(UserMixin)` |
| `_JsonLogFormatter` | class | `lazyc2.py:479` | `class _JsonLogFormatter(Formatter)` |
| `_LazyShellProxy` | class | `lazyc2.py:2916` | `class _LazyShellProxy` |
| `__getattr__` | function | `lazyc2.py:2896` | `def __getattr__(name)` |
| `__getattr__` | method | `lazyc2.py:2928` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyc2.py:3269` | `def __init__(self, user_data)` |
| `__setattr__` | method | `lazyc2.py:2932` | `def __setattr__(self, name, value)` |
| `_add_security_headers` | function | `lazyc2.py:2759` | `def _add_security_headers(response)` |
| `_api_data_inner` | function | `lazyc2.py:4734` | `def _api_data_inner()` |
| `_append_beacon_record` | function | `lazyc2.py:1399` | `def _append_beacon_record(record)` |
| `_beacon_records_path` | function | `lazyc2.py:1291` | `def _beacon_records_path(client_id)` |
| `_beacon_signature_guard` | function | `lazyc2.py:3665` | `def _beacon_signature_guard()` |
| `_behavioral_risk_prompt` | function | `lazyc2.py:2521` | `def _behavioral_risk_prompt(event)` |
| `_bg_cred_reuse` | function | `lazyc2.py:4091` | `def _bg_cred_reuse(_ip)` |
| `_bootstrap_initial_admin` | function | `lazyc2.py:2996` | `def _bootstrap_initial_admin()` |
| `_build_privesc_command` | function | `lazyc2.py:3636` | `def _build_privesc_command(platform)` |
| `_campaign_adaptation_prompt` | function | `lazyc2.py:2574` | `def _campaign_adaptation_prompt(campaign_id, events)` |
| `_complete_mfa_login` | function | `lazyc2.py:6384` | `def _complete_mfa_login()` |
| `_current_aes_key` | function | `lazyc2.py:2093` | `def _current_aes_key()` |
| `_encrypt_command_for` | function | `lazyc2.py:3499` | `def _encrypt_command_for(client_id, command)` |
| `_enforce_https_redirect` | function | `lazyc2.py:2649` | `def _enforce_https_redirect()` |
| `_enforce_mfa_verified` | function | `lazyc2.py:2725` | `def _enforce_mfa_verified()` |
| `_enforce_password_rotation` | function | `lazyc2.py:2669` | `def _enforce_password_rotation()` |
| `_engage_publish` | function | `lazyc2.py:3863` | `def _engage_publish(_cid, _ip, _host, _user, _platform)` |
| `_enqueue_malleable_command` | function | `lazyc2.py:1371` | `def _enqueue_malleable_command(client_id, command)` |
| `_env_tag` | function | `lazyc2.py:230` | `def _env_tag()` |
| `_events` | function | `lazyc2.py:7901` | `def _events()` |
| `_extract_first_ip` | function | `lazyc2.py:3919` | `def _extract_first_ip(raw)` |
| `_generate_strong_credentials` | function | `lazyc2.py:3192` | `def _generate_strong_credentials()` |
| `_generic_loop_error` | function | `lazyc2.py:7044` | `def _generic_loop_error()` |
| `_get_rbac_user_obj` | function | `lazyc2.py:3281` | `def _get_rbac_user_obj(flask_user)` |
| `_group_tasks_for_display` | function | `lazyc2.py:5686` | `def _group_tasks_for_display(tasks)` |
| `_handle_404` | function | `lazyc2.py:2826` | `def _handle_404(_error)` |
| `_handle_405` | function | `lazyc2.py:2831` | `def _handle_405(_error)` |
| `_handle_exception` | function | `lazyc2.py:2836` | `def _handle_exception(error)` |
| `_ingest_beacon` | function | `lazyc2.py:4152` | `def _ingest_beacon(_ips, _host, _cmd, _out, _user)` |
| `_init_shell` | function | `lazyc2.py:2869` | `def _init_shell()` |
| `_is_unspecified_bind_literal` | function | `lazyc2.py:317` | `def _is_unspecified_bind_literal(address)` |
| `_is_valid_credential` | function | `lazyc2.py:3932` | `def _is_valid_credential(value)` |
| `_listen_address` | function | `lazyc2.py:290` | `def _listen_address()` |
| `_load_malleable_recon_state` | function | `lazyc2.py:1329` | `def _load_malleable_recon_state(client_id)` |
| `_load_or_create_secret_key` | function | `lazyc2.py:2779` | `def _load_or_create_secret_key()` |
| `_load_reverse_shell_password` | function | `lazyc2.py:5273` | `def _load_reverse_shell_password(secret_path)` |
| `_load_surface_intel` | function | `lazyc2.py:7179` | `def _load_surface_intel()` |

Next: [SYMBOLS_p9.md](SYMBOLS_p9.md)
