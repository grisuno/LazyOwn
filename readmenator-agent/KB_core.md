# Subsystem: core (page 1 of 2)
Pages: [KB_core.md](KB_core.md), [KB_core_p2.md](KB_core_p2.md)

## core/__init__.py
- Doc: Core primitives for the LazyOwn framework.
- Layer: utility
- Language: py
- Depends on: `core/config.py`, `core/console.py`, `core/crypto.py`, `core/dependencies.py`, `core/errors.py`, `core/http.py`, `core/network.py`, `core/parsers.py`, `core/payload_schema.py`, `core/process.py`, `core/validators.py`
- Imported by: `tests/test_core_defaults.py`, `tests/test_llm_budget.py`, `tests/test_single_implementation.py`

## core/api_authz.py
- Doc: Tenant-bound API authorization for the LazyOwn C2 dashboard.
- Layer: presentation
- Language: py
- Symbols:
  - `ApiAuthzConfig` (class, line 54) `class ApiAuthzConfig`
  - `ApiKey` (class, line 75) `class ApiKey`
  - `_hash_secret` (function, line 137) `def _hash_secret(secret)`
  - `_verify_secret` (function, line 142) `def _verify_secret(secret, stored_hash)`
  - `_generate_token_bytes` (function, line 147) `def _generate_token_bytes(nbytes)`
  - `ApiKeyStore` (class, line 161) `class ApiKeyStore`
  - `require_api_auth` (function, line 365) `def require_api_auth(store, permissions, require_tenant)`
  - `create_api_token` (function, line 440) `def create_api_token(store, tenant_id, label, permissions, expires_in_days)`
  - `to_dict` (method, line 94) `def to_dict(self)`
  - `from_dict` (method, line 107) `def from_dict(cls, data)`
  - `is_expired` (method, line 119) `def is_expired(self)`
  - `is_retired` (method, line 124) `def is_retired(self)`
  - `has_permission` (method, line 127) `def has_permission(self, permission)`
  - `has_all_permissions` (method, line 130) `def has_all_permissions(self, permissions)`
  - `__init__` (method, line 170) `def __init__(self, config)`
  - `config` (method, line 176) `def config(self)`
  - `_read` (method, line 180) `def _read(self)`
  - `_write` (method, line 191) `def _write(self, data)`
  - `_grace_deadline` (method, line 197) `def _grace_deadline(self, retired_at)`
  - `_prune_retired` (method, line 201) `def _prune_retired(self, records)`
  - `list_keys` (method, line 217) `def list_keys(self, tenant_id)`
  - `find_by_hash` (method, line 229) `def find_by_hash(self, key_hash)`
  - `create_key` (method, line 238) `def create_key(self, tenant_id, label, permissions, expires_in_days)`
  - `revoke_key` (method, line 273) `def revoke_key(self, label, tenant_id)`
  - `validate_key` (method, line 287) `def validate_key(self, plaintext)`
  - `rotate_key` (method, line 309) `def rotate_key(self, label, tenant_id)`
  - `_prune_record` (method, line 343) `def _prune_record(self, key_hash)`
  - `_touch_last_used` (method, line 351) `def _touch_last_used(self, key_hash)`
  - `_extract_key` (function, line 393) `def _extract_key(request_obj)`
  - `decorator` (function, line 405) `def decorator(f)`
  - `decorated` (function, line 407) `def decorated()`
- Imported by: `lazyc2/app_factory.py`, `lazyc2/blueprints/api.py`, `tests/test_api_authz.py`, `tests/test_api_v1.py`, `tests/test_orchestrator_api.py`

## core/autonomous.py
- Doc: Autonomous-run mode for the loop engine.
- Layer: utility
- Language: py
- Symbols:
  - `is_autonomous` (function, line 21) `def is_autonomous()`
  - `autonomous_mode` (function, line 27) `def autonomous_mode()`
  - `_guarded_input` (function, line 39) `def _guarded_input(prompt)`
- Imported by: `cli/commands/exploit_migrated.py`, `cli/commands/mcp_bridge.py`, `lazyown.py`, `modules/lazy_runner.py`, `tests/test_lazy_runner.py`

## core/command_bridge.py
- Doc: Lightweight command execution bridge between C2 bots and the LazyOwn CLI shell.
- Layer: utility
- Language: py
- Symbols:
  - `CommandBridge` (class, line 15) `class CommandBridge`
  - `get_bridge` (function, line 126) `def get_bridge()`
  - `__init__` (method, line 18) `def __init__(self)`
  - `ready` (method, line 25) `def ready(self)`
  - `error` (method, line 30) `def error(self)`
  - `_ensure_shell` (method, line 34) `def _ensure_shell(self)`
  - `onecmd` (method, line 65) `def onecmd(self, command)`
  - `one_cmd` (method, line 89) `def one_cmd(self, command)`
  - `execute` (method, line 110) `def execute(self, command)`
- Depends on: `lazyown.py`
- Imported by: `tests/test_core_command_bridge.py`

## core/config.py
- Doc: Configuration loader and Config wrapper.
- Layer: infrastructure
- Language: py
- Symbols:
  - `_apply_env_overrides` (function, line 75) `def _apply_env_overrides(payload)`
  - `_coerce_env_value` (function, line 108) `def _coerce_env_value(raw, existing)`
  - `_mask_if_sensitive` (function, line 133) `def _mask_if_sensitive(key, value)`
  - `_log_config_change` (function, line 151) `def _log_config_change(key, old_value, new_value)`
  - `_calling_frame` (function, line 173) `def _calling_frame()`
  - `_collect_validation_warnings` (function, line 187) `def _collect_validation_warnings(payload)`
  - `Config` (class, line 211) `class Config`
  - `_migrate_keys` (function, line 254) `def _migrate_keys(config_dict)`
  - `resolve_aes_key` (function, line 266) `def resolve_aes_key(config_dict)`
  - `_load_raw_payload` (function, line 309) `def _load_raw_payload(path)`
  - `load_payload` (function, line 332) `def load_payload(path)`
  - `load_and_validate` (function, line 350) `def load_and_validate(path)`
  - `save_payload` (function, line 401) `def save_payload(payload, path)`
  - `_rat_key_is_valid` (function, line 455) `def _rat_key_is_valid(value)`
  - `ensure_rat_key` (function, line 468) `def ensure_rat_key(config_obj)`
  - `__init__` (method, line 224) `def __init__(self, config_dict, sessions_dir)`
  - `__getattr__` (method, line 233) `def __getattr__(self, name)`
  - `__getitem__` (method, line 236) `def __getitem__(self, key)`
  - `as_params` (method, line 239) `def as_params(self)`
  - `overridden_keys` (method, line 249) `def overridden_keys(self)`
- Depends on: `core/logging.py`, `core/payload_schema.py`
- Imported by: `cli/aliases.py`, `cli/commands/bof_registry.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/defaults.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/misc_migrated.py`, `cli/commands/params_ops.py`, `cli/commands/persist_migrated.py`, `cli/commands/purple_team.py`, `cli/commands/recon_migrated.py`, `cli/commands/security.py`, `cli/commands/session_ops.py`, `cli/commands/ux.py`, `cli/engagement_hooks.py`, `cli/orchestrator_assets_tabs.py`, `core/__init__.py`, `core/credential_vault.py`, `core/hardening.py`, `core/prompt.py`, `core/session_secrets.py`, `lazyc2.py`, `lazyc2/blueprints/api.py`, `lazyown.py`, `modules/atomic_exploit_bridge.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/c2_builder.py`, `modules/c2_profile_engine.py`, `modules/cli_auth.py`, `modules/config_store.py`, `modules/db.py`, `modules/gym_cleanup.py`, `modules/harness.py`, `modules/lazy_agent.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_installer.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_sandbox.py`, `modules/loop_ai_bridge.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/orchestrator_config.py`, `modules/reactive_engine.py`, `modules/redteam_gym.py`, `modules/sinks/beacon_dispatch.py`, `skills/lazyown_mcp.py`, `tests/test_aes_key_propagation.py`, `tests/test_audit_remediation.py`, `tests/test_cli_assign.py`, `tests/test_cli_command_sets.py`, `tests/test_core.py`, `tests/test_core_config.py`, `tests/test_guardrails.py`, `tests/test_gym_lifecycle.py`, `tests/test_improvements_spec.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_runner.py`, `tests/test_loop_supervision.py`, `tests/test_orchestrator_yaml.py`, `tests/test_session_secrets.py`, `utils.py`

## core/console.py
- Doc: ANSI color constants and console output helpers.
- Layer: utility
- Language: py
- Symbols:
  - `_sanitize` (function, line 93) `def _sanitize(text)`
  - `colors_enabled` (function, line 98) `def colors_enabled()`
  - `_paint` (function, line 114) `def _paint(code, text)`
  - `format_line` (function, line 121) `def format_line(prefix, message, glyph)`
  - `print_error` (function, line 137) `def print_error(error)`
  - `print_msg` (function, line 143) `def print_msg(msg)`
  - `print_warn` (function, line 149) `def print_warn(warn)`
  - `print_succ` (function, line 155) `def print_succ(msg)`
  - `ensure_blocking_stdio` (function, line 161) `def ensure_blocking_stdio()`
  - `write_stdout` (function, line 180) `def write_stdout(text)`
  - `_emit` (function, line 208) `def _emit(line)`
- Imported by: `cli/command_explorer.py`, `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/commands/orchestration.py`, `cli/commands/recon.py`, `cli/commands/security.py`, `cli/commands/ux.py`, `cli/config_status.py`, `cli/contextual_help.py`, `cli/doctor.py`, `cli/exploit_advisor.py`, `cli/exploration_view.py`, `cli/protips.py`, `cli/reactive_hints.py`, `cli/session_resumer.py`, `cli/splash.py`, `cli/surface_tui.py`, `cli/tips_engine.py`, `cli/toast_bus.py`, `cli/tutorial.py`, `cli/wizard.py`, `core/__init__.py`, `core/error_advice.py`, `core/http.py`, `core/network.py`, `core/process.py`, `core/safe_console.py`, `core/validators.py`, `key.py`, `lazy_sentinel4.py`, `lazyc2.py`, `lazyown.py`, `modules/apt_playbooks.py`, `modules/atomic_cli.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/lilsplunky.py`, `modules/privesc_predictor.py`, `modules/rich_tui.py`, `tests/test_console_stdio.py`, `tests/test_core.py`, `tests/test_exploration_and_addons.py`, `tests/test_lazy_parity.py`, `tests/test_loop_progress.py`, `tests/test_scope_guard_integration.py`, `tests/test_session_brief.py`, `tests/test_toast_bus.py`, `tests/test_tui_splash.py`, `tests/test_tui_style.py`, `tests/test_tui_themes.py`, `utils.py`

## core/credential_vault.py
- Doc: Credential vault — AES-256-GCM encryption for sensitive config values.
- Layer: utility
- Language: py
- Symbols:
  - `check_dangerous_defaults` (function, line 63) `def check_dangerous_defaults(payload)`
  - `_get_aes_key` (function, line 79) `def _get_aes_key(payload)`
  - `seal_value` (function, line 93) `def seal_value(plaintext, key)`
  - `unseal_value` (function, line 112) `def unseal_value(sealed, key)`
  - `seal_payload` (function, line 141) `def seal_payload(payload, key)`
  - `unseal_payload` (function, line 164) `def unseal_payload(payload, key)`
  - `rotate_aes_key` (function, line 186) `def rotate_aes_key(payload, current_key)`
  - `generate_secure_defaults` (function, line 215) `def generate_secure_defaults()`
- Depends on: `core/config.py`, `core/crypto.py`, `core/logging.py`
- Imported by: `cli/commands/security.py`, `core/hardening.py`, `lazyown.py`, `tests/test_credential_vault.py`

## core/crypto.py
- Doc: Symmetric primitives used by the framework.
- Layer: utility
- Language: py
- Symbols:
  - `generate_salt` (function, line 24) `def generate_salt(length)`
  - `derive_key` (function, line 36) `def derive_key(password, salt)`
  - `xor_encrypt_decrypt` (function, line 67) `def xor_encrypt_decrypt(data, key)`
  - `generate_xor_key` (function, line 83) `def generate_xor_key(length)`
  - `AESencrypt` (function, line 98) `def AESencrypt(plaintext, key)`
  - `AESdecrypt` (function, line 122) `def AESdecrypt(data, key)`
  - `dropFile` (function, line 154) `def dropFile(key, ciphertext)`
- Imported by: `cli/auto_crypto.py`, `cli/commands/exfiltration.py`, `core/__init__.py`, `core/credential_vault.py`, `modules/db.py`, `modules/lazy_loop.py`, `modules/phishing_orchestrator.py`, `modules/rootkit/rootkit.c`, `tests/test_core.py`, `tests/test_security_hardening_v5.py`, `utils.py`

## core/defaults.py
- Doc: Build-time default constants loaded from ``config/defaults.toml``.
- Layer: utility
- Language: py
- Symbols:
  - `load_defaults` (function, line 21) `def load_defaults(path)`
  - `clear_cache` (function, line 44) `def clear_cache()`
  - `get` (function, line 49) `def get(section, key, default)`
  - `default_lport` (function, line 63) `def default_lport()`
  - `default_rport` (function, line 72) `def default_rport()`
  - `rockyou_wordlist` (function, line 81) `def rockyou_wordlist()`
  - `common_wordlists` (function, line 90) `def common_wordlists()`
  - `sessions_dir` (function, line 100) `def sessions_dir()`
- Imported by: `cli/commands/cred_migrated.py`, `cli/commands/defaults.py`, `lazyc2/blueprints/api.py`, `lazyown.py`, `modules/autonomous_exploit_engine.py`, `modules/hash_cracker.py`, `tests/test_security_codeql_batch.py`

## core/dependencies.py
- Doc: Graceful optional-import handling for heavy third-party dependencies.
- Layer: utility
- Language: py
- Symbols:
  - `MissingDependencyError` (class, line 37) `class MissingDependencyError(ImportError)`
  - `DependencySpec` (class, line 66) `class DependencySpec`
  - `_DeferredImport` (class, line 101) `class _DeferredImport`
  - `_spec_for` (function, line 157) `def _spec_for(import_name, pip_package, feature)`
  - `optional_import` (function, line 183) `def optional_import(import_name)`
  - `optional_attr` (function, line 209) `def optional_attr(import_name, attr)`
  - `DependencyStatus` (class, line 253) `class DependencyStatus`
  - `DependencyReport` (class, line 268) `class DependencyReport`
  - `probe_python_dependency` (function, line 288) `def probe_python_dependency(spec)`
  - `collect_dependency_report` (function, line 312) `def collect_dependency_report()`
  - `format_report` (function, line 323) `def format_report(report)`
  - `main` (function, line 368) `def main()`
  - `__init__` (method, line 45) `def __init__(self, import_name, pip_package, feature)`
  - `__init__` (method, line 115) `def __init__(self, spec)`
  - `_raise` (method, line 123) `def _raise(self)`
  - `__getattr__` (method, line 132) `def __getattr__(self, _name)`
  - `__call__` (method, line 136) `def __call__(self)`
  - `__getitem__` (method, line 140) `def __getitem__(self, _key)`
  - `__iter__` (method, line 144) `def __iter__(self)`
  - `__len__` (method, line 148) `def __len__(self)`
  - `__bool__` (method, line 152) `def __bool__(self)`
  - `missing` (method, line 278) `def missing(self)`
  - `ok` (method, line 283) `def ok(self)`
- Imported by: `core/__init__.py`, `tests/test_dependencies.py`, `utils.py`

## core/error_advice.py
- Doc: Actionable error advice with fix command and documentation link.
- Layer: utility
- Language: py
- Symbols:
  - `ErrorAdviceConfig` (class, line 16) `class ErrorAdviceConfig`
  - `ErrorAdvice` (class, line 27) `class ErrorAdvice`
  - `get_advice` (function, line 74) `def get_advice(key)`
  - `render_advice` (function, line 86) `def render_advice(key, config)`
  - `docs_url` (method, line 35) `def docs_url(self, config)`
- Depends on: `core/console.py`

## core/errors.py
- Doc: Error taxonomy for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `ErrorCode` (class, line 10) `class ErrorCode(IntEnum)`
  - `LazyOwnError` (class, line 58) `class LazyOwnError(Exception)`
  - `ConfigError` (class, line 78) `class ConfigError(LazyOwnError)`
  - `TargetError` (class, line 85) `class TargetError(LazyOwnError)`
  - `AuthError` (class, line 92) `class AuthError(LazyOwnError)`
  - `ToolError` (class, line 99) `class ToolError(LazyOwnError)`
  - `PayloadError` (class, line 106) `class PayloadError(LazyOwnError)`
  - `DatabaseError` (class, line 113) `class DatabaseError(LazyOwnError)`
  - `NetworkError` (class, line 120) `class NetworkError(LazyOwnError)`
  - `PermissionError` (class, line 127) `class PermissionError(LazyOwnError)`
  - `ValidationError` (class, line 134) `class ValidationError(LazyOwnError)`
  - `__init__` (method, line 61) `def __init__(self, message, error_code)`
  - `to_dict` (method, line 66) `def to_dict(self)`
  - `__str__` (method, line 74) `def __str__(self)`
  - `__init__` (method, line 81) `def __init__(self, message, error_code)`
  - `__init__` (method, line 88) `def __init__(self, message, error_code)`
  - `__init__` (method, line 95) `def __init__(self, message, error_code)`
  - `__init__` (method, line 102) `def __init__(self, message, error_code)`
  - `__init__` (method, line 109) `def __init__(self, message, error_code)`
  - `__init__` (method, line 116) `def __init__(self, message, error_code)`
  - `__init__` (method, line 123) `def __init__(self, message, error_code)`
  - `__init__` (method, line 130) `def __init__(self, message, error_code)`
  - `__init__` (method, line 137) `def __init__(self, message, error_code)`
- Depends on: `cli/commands/enum.py`
- Imported by: `core/__init__.py`

## core/executor.py
- Doc: Centralised subprocess wrapper for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `_validate_input` (function, line 41) `def _validate_input(command)`
  - `_validate_timeout` (function, line 75) `def _validate_timeout(timeout)`
  - `safe_run` (function, line 96) `def safe_run(command)`
  - `safe_run` (function, line 98) `def safe_run(command)`
  - `safe_run` (function, line 101) `def safe_run(command)`
  - `run_shell` (function, line 149) `def run_shell(cmd)`
- Depends on: `core/logging.py`
- Imported by: `tests/test_core_executor.py`

## core/hardening.py
- Doc: Centralized security hardening utilities for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `reject_option_injection` (function, line 93) `def reject_option_injection(argv)`
  - `escape_powershell_single_quoted` (function, line 112) `def escape_powershell_single_quoted(value)`
  - `SecurityViolation` (class, line 133) `class SecurityViolation(PermissionError)`
  - `terminal_env` (function, line 137) `def terminal_env(base)`
  - `safe_subprocess_run` (function, line 158) `def safe_subprocess_run(argv)`
  - `safe_clipboard_copy` (function, line 211) `def safe_clipboard_copy(content)`
  - `build_sshpass_command` (function, line 250) `def build_sshpass_command(password, ssh_args)`
  - `set_sshpass_env` (function, line 279) `def set_sshpass_env(password)`
  - `escape_html_content` (function, line 298) `def escape_html_content(value)`
  - `safe_path_join` (function, line 310) `def safe_path_join(base_dir, user_path)`
  - `validate_network_cidr` (function, line 336) `def validate_network_cidr(cidr)`
  - `validate_port_spec` (function, line 348) `def validate_port_spec(ports)`
  - `validate_host` (function, line 364) `def validate_host(host)`
  - `require_encryption_key` (function, line 384) `def require_encryption_key(env_key, secret_file)`
  - `defused_xml_parse` (function, line 412) `def defused_xml_parse(source)`
  - `sanitize_filename` (function, line 434) `def sanitize_filename(filename, max_length)`
  - `tls_secure_context` (function, line 454) `def tls_secure_context(extra_ca)`
  - `tls_lab_unverified_allowed` (function, line 479) `def tls_lab_unverified_allowed(host)`
  - `tls_lab_fallback_context` (function, line 506) `def tls_lab_fallback_context()`
  - `validate_upstream_path` (function, line 528) `def validate_upstream_path(path)`
  - `is_safe_path_segment` (function, line 557) `def is_safe_path_segment(segment)`
  - `is_safe_dir_path` (function, line 578) `def is_safe_dir_path(raw)`
  - `is_safe_yaml_name` (function, line 604) `def is_safe_yaml_name(name)`
  - `safe_join_under` (function, line 623) `def safe_join_under(base_dir, user_path)`
  - `safe_open_under` (function, line 652) `def safe_open_under(base_dir, user_path, mode)`
  - `store_secret_owner_only` (function, line 679) `def store_secret_owner_only(path, text)`
  - `_is_emoji_codepoint` (function, line 714) `def _is_emoji_codepoint(code)`
  - `contains_emoji` (function, line 722) `def contains_emoji(text)`
  - `iter_emoji_spans` (function, line 737) `def iter_emoji_spans(text)`
  - `_seal_key` (function, line 756) `def _seal_key(sessions_dir)`
  - `seal_secret` (function, line 770) `def seal_secret(plaintext)`
  - `unseal_secret` (function, line 801) `def unseal_secret(stored)`
  - `redact_text` (function, line 842) `def redact_text(text)`
  - `_mask` (function, line 853) `def _mask(match)`
- Depends on: `core/config.py`, `core/credential_vault.py`, `core/host_policy.py`, `core/logging.py`
- Imported by: `cli/commands/anti_forensics.py`, `cli/commands/cloud.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/exfiltration.py`, `cli/commands/lateral_migrated.py`, `cli/commands/nethelpers.py`, `cli/commands/persist_migrated.py`, `cli/commands/pivoting.py`, `core/process.py`, `core/reverse_shell_secret.py`, `core/safe_subprocess.py`, `lazyc2.py`, `lazyown.py`, `modules/atomic_cli.py`, `modules/domain_dominance.py`, `modules/lazy_findings.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `modules/lazy_runner.py`, `modules/phishing_orchestrator.py`, `modules/sinks/beacon_dispatch.py`, `modules/websocket_beacon.py`, `modules/winbox_gym.py`, `modules/world_model.py`, `scripts/devtools/core_smoke.py`, `skills/claude_md_orchestrator/validators.py`, `tests/test_host_policy.py`, `tests/test_security_alerts_fix.py`, `tests/test_security_hardening_v3.py`, `tests/test_shell_semantics.py`, `tests/test_winbox_gym.py`

## core/host_policy.py
- Doc: Single source of truth for host and network shape validation.
- Layer: business_logic
- Language: py
- Symbols:
  - `rejects_shell_meta` (function, line 20) `def rejects_shell_meta(value)`
  - `is_valid_cidr` (function, line 32) `def is_valid_cidr(value)`
  - `is_valid_host` (function, line 48) `def is_valid_host(value)`
- Imported by: `core/hardening.py`, `core/validators.py`, `tests/test_host_policy.py`

## core/http.py
- Doc: HTTP and API utilities for the LazyOwn framework.
- Layer: presentation
- Language: py
- Symbols:
  - `generate_http_req` (function, line 18) `def generate_http_req(host, port, uri, custom_header, cmd)`
  - `get_banner` (function, line 50) `def get_banner(host, port)`
  - `get_command` (function, line 69) `def get_command(url, lhost)`
  - `send_command` (function, line 87) `def send_command(cmd, url, lhost)`
  - `exploitalert` (function, line 106) `def exploitalert(content)`
  - `packetstormsecurity` (function, line 125) `def packetstormsecurity(content)`
  - `nvddb` (function, line 143) `def nvddb(content)`
  - `scrape_news` (function, line 174) `def scrape_news()`
  - `display_news` (function, line 198) `def display_news(titles, links, scores)`
  - `inject_payloads` (function, line 211) `def inject_payloads(urls, payload_url, request_timeout)`
- Depends on: `core/console.py`
- Imported by: `core/__init__.py`

## core/llm_budget.py
- Doc: LLM budget cap and per call token counter.
- Layer: utility
- Language: py
- Symbols:
  - `BudgetExceeded` (class, line 54) `class BudgetExceeded(RuntimeError)`
  - `LLMBackendLike` (class, line 58) `class LLMBackendLike(Protocol)`
  - `ModelPrice` (class, line 69) `class ModelPrice`
  - `BudgetConfig` (class, line 103) `class BudgetConfig`
  - `LedgerEntry` (class, line 132) `class LedgerEntry`
  - `_today_utc` (function, line 150) `def _today_utc(now)`
  - `_now_iso` (function, line 163) `def _now_iso(now)`
  - `BudgetLedger` (class, line 176) `class BudgetLedger`
  - `TokenEstimator` (class, line 268) `class TokenEstimator`
  - `BudgetGuard` (class, line 310) `class BudgetGuard`
  - `BudgetedBackend` (class, line 408) `class BudgetedBackend`
  - `default_model_prices` (function, line 442) `def default_model_prices()`
  - `default_sessions_dir` (function, line 461) `def default_sessions_dir()`
  - `_coerce_bool` (function, line 476) `def _coerce_bool(value, default)`
  - `_coerce_price_table` (function, line 496) `def _coerce_price_table(value)`
  - `_coerce_positive_float` (function, line 520) `def _coerce_positive_float(value, default)`
  - `_coerce_positive_int` (function, line 536) `def _coerce_positive_int(value, default)`
  - `load_budget_config` (function, line 552) `def load_budget_config(payload, sessions_dir)`
  - `read_budget_status` (function, line 585) `def read_budget_status(payload, sessions_dir)`
  - `format_budget_status` (function, line 616) `def format_budget_status(config, ledger)`
  - `_has_required_methods` (function, line 642) `def _has_required_methods(backend)`
  - `wrap_backend_with_budget` (function, line 657) `def wrap_backend_with_budget(backend, config, estimator, model, ledger)`
  - `generate` (method, line 61) `def generate(self, prompt)`
  - `stream_generate` (method, line 63) `def stream_generate(self, prompt)`
  - `complete` (method, line 65) `def complete(self, system, user, max_tokens, temperature)`
  - `from_mapping` (method, line 81) `def from_mapping(cls, data)`
  - `_empty_state` (method, line 189) `def _empty_state(self)`
  - `_load` (method, line 193) `def _load(self)`
  - `_save` (method, line 215) `def _save(self, state)`
  - `_state` (method, line 226) `def _state(self)`
  - `record` (method, line 232) `def record(self, entry)`
  - `spent_today` (method, line 251) `def spent_today(self)`
  - `calls_today` (method, line 256) `def calls_today(self)`
  - `reset` (method, line 261) `def reset(self)`
  - `__init__` (method, line 278) `def __init__(self, encoding_name)`
  - `_load_encoding` (method, line 283) `def _load_encoding(encoding_name)`
  - `count` (method, line 292) `def count(self, text)`
  - `__init__` (method, line 319) `def __init__(self, config, estimator, ledger)`
  - `price_for` (method, line 329) `def price_for(self, model)`
  - `estimate_cost` (method, line 343) `def estimate_cost(self, model, input_tokens, output_tokens)`
  - `estimate_and_check` (method, line 356) `def estimate_and_check(self, prompt, model, output_tokens)`
  - `__init__` (method, line 417) `def __init__(self, inner, guard, model)`
  - `generate` (method, line 422) `def generate(self, prompt)`
  - `stream_generate` (method, line 430) `def stream_generate(self, prompt)`
  - `complete` (method, line 435) `def complete(self, system, user, max_tokens, temperature)`
- Imported by: `cli/commands/ai.py`, `modules/llm_factory.py`, `skills/lazyown_mcp.py`, `tests/test_llm_budget.py`

## core/logging.py
- Doc: Structured JSON-lines logging for the LazyOwn framework.
- Layer: infrastructure
- Language: py
- Symbols:
  - `StructuredLogConfig` (class, line 42) `class StructuredLogConfig`
  - `_JsonLineFormatter` (class, line 71) `class _JsonLineFormatter(Formatter)`
  - `_ConsoleFormatter` (class, line 121) `class _ConsoleFormatter(Formatter)`
  - `StructuredLogger` (class, line 139) `class StructuredLogger(Logger)`
  - `_log_factory` (function, line 180) `def _log_factory(name, config)`
  - `get_logger` (function, line 231) `def get_logger(name)`
  - `install_json_handler` (function, line 251) `def install_json_handler(name, config)`
  - `reconfigure` (function, line 300) `def reconfigure(config)`
  - `__init__` (method, line 74) `def __init__(self, redacted_fields)`
  - `format` (method, line 78) `def format(self, record)`
  - `format` (method, line 132) `def format(self, record)`
  - `makeRecord` (method, line 148) `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)`
- Imported by: `cli/auto_crypto.py`, `cli/chain_mode.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/session_resumer.py`, `cli/tips_engine.py`, `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazygptcli.py`, `contrib/legacy/lazygptcli_unified.py`, `contrib/legacy/lazyhoneypot.py`, `contrib/legacy/lazyopenssh77enum2.py`, `contrib/legacy/lazyphishingai.py`, `contrib/legacy/lazysearch_bot.py`, `contrib/legacy/lazysmbrelay.py`, `contrib/legacy/lazyssh.py`, `core/config.py`, `core/credential_vault.py`, `core/executor.py`, `core/hardening.py`, `core/param_registry.py`, `core/safe_exec.py`, `core/scheduler.py`, `core/security.py`, `core/session_secrets.py`, `lazy_sentinel4.py`, `lazyc2.py`, `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/api.py`, `lazyc2/blueprints/api_v1.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/beacon.py`, `lazyc2/blueprints/orchestrator.py`, `lazyc2/blueprints/phishing.py`, `lazyc2/extensions/short_urls.py`, `lazyc2/extensions/storage.py`, `lazyc2/security/cli_credentials.py`, `lazygui/app.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/settings.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazyown.py`, `modules/addon_updater.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/atomic_cli.py`, `modules/atomic_enricher.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/beacon_history.py`, `modules/beacon_recon.py`, `modules/bof_registry.py`, `modules/c2_agent.py`, `modules/c2_profile.py`, `modules/c2_profile_engine.py`, `modules/c2_surfaces.py`, `modules/chain_distill.py`, `modules/chain_facts.py`, `modules/chain_registry.py`, `modules/collab_bp.py`, `modules/command_executor.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/config_store.py`, `modules/credential_reuse.py`, `modules/ctf_capture.py`, `modules/cve_matcher.py`, `modules/db.py`, `modules/defense_stages.py`, `modules/detection_feed.py`, `modules/detection_oracle.py`, `modules/emulation_runner.py`, `modules/engagement_hooks.py`, `modules/estorides_importer.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/factsio.py`, `modules/golden_path.py`, `modules/gym_cleanup.py`, `modules/gym_matrix_runner.py`, `modules/gym_registry.py`, `modules/gym_winbox_runner.py`, `modules/harness.py`, `modules/hash_cracker.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/integrations/misp_export.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/integrations/searchsploit.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `modules/lazy_rbac.py`, `modules/lazyownerweb.py`, `modules/lesson_ingestor.py`, `modules/lilsplunky.py`, `modules/llm_adapter.py`, `modules/llm_client.py`, `modules/logging_config.py`, `modules/mcp_agent_bridge.py`, `modules/metasploitable_gym.py`, `modules/metrics.py`, `modules/module_registry.py`, `modules/moe_router.py`, `modules/obs_parser.py`, `modules/operation.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/session_rag.py`, `modules/sinks/findings.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`, `modules/state_manager.py`, `modules/sudo_tiocsti.py`, `modules/threat_model.py`, `modules/toposwarm_bridge.py`, `modules/trigger_policy.py`, `modules/ttp_coverage.py`, `modules/ttpscope_bridge.py`, `modules/unified_bridge.py`, `modules/unified_dashboard.py`, `modules/verb_catalog.py`, `modules/verb_manifest.py`, `modules/vulnbot.py`, `modules/winbox_gym.py`, `modules/world_model.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/autonomous_replay.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`, `tests/test_security_codeql_batch.py`, `tests/test_structured_logging.py`, `utils.py`

## core/network.py
- Doc: Network primitives for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `parse_ip_mac` (function, line 18) `def parse_ip_mac(input_string)`
  - `create_arp_packet` (function, line 33) `def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac)`
  - `send_packet` (function, line 66) `def send_packet(packet, iface)`
  - `parse_proc_net_file` (function, line 78) `def parse_proc_net_file(file_path)`
  - `get_open_ports` (function, line 105) `def get_open_ports()`
  - `is_port_in_use` (function, line 120) `def is_port_in_use(port, host)`
  - `get_banner` (function, line 134) `def get_banner(ip, port)`
  - `get_network_info` (function, line 154) `def get_network_info()`
- Depends on: `core/console.py`
- Imported by: `core/__init__.py`

## core/param_registry.py
- Doc: Operator-managed parameter registry.
- Layer: utility
- Language: py
- Symbols:
  - `OperatorParam` (class, line 114) `class OperatorParam`
  - `registry_path` (function, line 158) `def registry_path(root)`
  - `normalise_kind` (function, line 172) `def normalise_kind(kind)`
  - `effective_value` (function, line 187) `def effective_value(entry)`
  - `_entry_to_param` (function, line 204) `def _entry_to_param(name, entry)`
  - `load_entries` (function, line 226) `def load_entries(root)`
  - `list_params` (function, line 256) `def list_params(root, include_builtin, keyword)`
  - `create_param` (function, line 291) `def create_param(name, kind, default, description, category, root)`
  - `update_param` (function, line 341) `def update_param(name, default, description, kind, category, root)`
  - `delete_param` (function, line 387) `def delete_param(name, root)`
  - `param_value` (function, line 411) `def param_value(name, root)`
  - `operator_specs` (function, line 425) `def operator_specs(root)`
  - `apply_to_schema` (function, line 437) `def apply_to_schema(root)`
  - `sync_shell_params` (function, line 459) `def sync_shell_params(shell, root)`
  - `_write` (function, line 482) `def _write(entries, root)`
  - `as_entry` (method, line 133) `def as_entry(self)`
  - `to_spec` (method, line 142) `def to_spec(self)`
- Depends on: `core/logging.py`, `core/payload_schema.py`
- Imported by: `cli/commands/params_ops.py`, `cli/lazy_orchestrator.py`, `core/payload_schema.py`, `lazyc2/addon_creator.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_lazy_orchestrator.py`, `tests/test_param_registry.py`, `tests/test_php2shell_addon.py`

## core/parsers.py
- Doc: Shared text kernel for the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `strip_ansi` (function, line 15) `def strip_ansi(text)`
- Imported by: `cli/banner_config.py`, `core/__init__.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `telegram_hermes.py`, `tests/test_single_implementation.py`, `utils.py`

## core/payload_schema.py
- Doc: Declarative schema and validation for ``payload.json``.
- Layer: utility
- Language: py
- Symbols:
  - `FieldKind` (class, line 77) `class FieldKind(StrEnum)`
  - `Severity` (class, line 95) `class Severity(StrEnum)`
  - `FieldSpec` (class, line 104) `class FieldSpec`
  - `ValidationIssue` (class, line 146) `class ValidationIssue`
  - `_validate_string` (function, line 169) `def _validate_string(value)`
  - `_validate_int` (function, line 175) `def _validate_int(value)`
  - `_validate_port` (function, line 189) `def _validate_port(value)`
  - `_validate_bool` (function, line 199) `def _validate_bool(value)`
  - `_validate_ip` (function, line 216) `def _validate_ip(value)`
  - `_validate_hostname` (function, line 224) `def _validate_hostname(value)`
  - `_validate_url` (function, line 236) `def _validate_url(value)`
  - `_validate_path` (function, line 244) `def _validate_path(value)`
  - `_validate_interface` (function, line 250) `def _validate_interface(value)`
  - `_validate_hex` (function, line 258) `def _validate_hex(value)`
  - `_validate_os_id` (function, line 266) `def _validate_os_id(value)`
  - `_validate_json_blob` (function, line 272) `def _validate_json_blob(value)`
  - `_validate_opaque` (function, line 284) `def _validate_opaque(_value)`
  - `_coerce_int` (function, line 305) `def _coerce_int(raw)`
  - `_coerce_bool` (function, line 320) `def _coerce_bool(raw)`
  - `_spec` (function, line 339) `def _spec(name, kind, default, description)`
  - `register_specs` (function, line 1862) `def register_specs(specs)`
  - `unregister_specs` (function, line 1885) `def unregister_specs(keys)`
  - `field_for` (function, line 1903) `def field_for(key)`
  - `coerce_value` (function, line 1908) `def coerce_value(key, raw)`
  - `validate_value` (function, line 1931) `def validate_value(key, value)`
  - `validate_payload` (function, line 2005) `def validate_payload(payload)`
  - `format_issue` (function, line 2040) `def format_issue(issue)`
  - `default_payload` (function, line 2058) `def default_payload()`
  - `categories` (function, line 2066) `def categories()`
  - `_load_operator_specs` (function, line 2078) `def _load_operator_specs()`
- Depends on: `cli/commands/enum.py`, `core/param_registry.py`, `modules/llm_factory.py`
- Imported by: `cli/assign.py`, `cli/commands/params_ops.py`, `cli/commands/session_ops.py`, `cli/wizard.py`, `core/__init__.py`, `core/config.py`, `core/param_registry.py`, `scripts/devtools/core_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_audit_remediation.py`, `tests/test_core_config.py`, `tests/test_core_defaults.py`, `tests/test_infra_disposable.py`, `tests/test_param_registry.py`, `tests/test_payload_schema.py`, `tests/test_php2shell_addon.py`, `tests/test_placeholder_coverage.py`


Next: [KB_core_p2.md](KB_core_p2.md)
