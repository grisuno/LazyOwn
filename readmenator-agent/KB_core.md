# Subsystem: core

## core/__init__.py
- Layer: utility
- Language: py
- Depends on: `core/config.py`, `core/console.py`, `core/credentials.py`, `core/crypto.py`, `core/dependencies.py`, `core/errors.py`, `core/http.py`, `core/network.py`, `core/parsers.py`, `core/payload_schema.py`, `core/process.py`, `core/validators.py`

## core/api_authz.py
- Layer: presentation
- Language: py
- Symbols:
  - `ApiAuthzConfig` (class, line 54) `class ApiAuthzConfig`
  - `ApiKey` (class, line 75) `class ApiKey`
  - `_hash_secret` (method, line 137) `def _hash_secret(secret)`
  - `_verify_secret` (method, line 142) `def _verify_secret(secret, stored_hash)`
  - `_generate_token_bytes` (method, line 147) `def _generate_token_bytes(nbytes)`
  - `ApiKeyStore` (class, line 161) `class ApiKeyStore`
  - `require_api_auth` (method, line 365) `def require_api_auth(store, permissions, require_tenant)`
  - `create_api_token` (method, line 440) `def create_api_token(store, tenant_id, label, permissions, expires_in_days)`
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
  - `_extract_key` (method, line 393) `def _extract_key(request_obj)`
  - `decorator` (method, line 405) `def decorator(f)`
  - `decorated` (method, line 407) `def decorated()`
- Imported by: `lazyc2/app_factory.py`, `lazyc2/blueprints/api.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `mutants/tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`, `tests/test_api_authz.py`

## core/command_bridge.py
- Layer: utility
- Language: py
- Symbols:
  - `CommandBridge` (class, line 13) `class CommandBridge`
  - `get_bridge` (method, line 130) `def get_bridge()`
  - `__init__` (method, line 16) `def __init__(self)`
  - `ready` (method, line 23) `def ready(self)`
  - `error` (method, line 28) `def error(self)`
  - `_ensure_shell` (method, line 32) `def _ensure_shell(self)`
  - `onecmd` (method, line 63) `def onecmd(self, command)`
  - `one_cmd` (method, line 93) `def one_cmd(self, command)`
  - `execute` (method, line 114) `def execute(self, command)`
- Depends on: `lazyown.py`
- Imported by: `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `mutants/tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`, `tests/test_core_command_bridge.py`

## core/config.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `_apply_env_overrides` (function, line 70) `def _apply_env_overrides(payload)`
  - `_coerce_env_value` (function, line 103) `def _coerce_env_value(raw, existing)`
  - `_mask_if_sensitive` (function, line 128) `def _mask_if_sensitive(key, value)`
  - `_log_config_change` (function, line 146) `def _log_config_change(key, old_value, new_value)`
  - `_collect_validation_warnings` (function, line 171) `def _collect_validation_warnings(payload)`
  - `Config` (class, line 195) `class Config`
  - `_migrate_keys` (method, line 238) `def _migrate_keys(config_dict)`
  - `resolve_aes_key` (method, line 250) `def resolve_aes_key(config_dict)`
  - `_load_raw_payload` (method, line 293) `def _load_raw_payload(path)`
  - `load_payload` (method, line 316) `def load_payload(path)`
  - `load_and_validate` (method, line 334) `def load_and_validate(path)`
  - `save_payload` (method, line 385) `def save_payload(payload, path)`
  - `__init__` (method, line 208) `def __init__(self, config_dict, sessions_dir)`
  - `__getattr__` (method, line 217) `def __getattr__(self, name)`
  - `__getitem__` (method, line 220) `def __getitem__(self, key)`
  - `as_params` (method, line 223) `def as_params(self)`
  - `overridden_keys` (method, line 233) `def overridden_keys(self)`
- Depends on: `core/logging.py`, `core/payload_schema.py`
- Imported by: `cli/aliases.py`, `cli/commands/bof_registry.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/mcp_bridge.py`, `cli/commands/misc_migrated.py`, `cli/commands/purple_team.py`, `cli/commands/recon_migrated.py`, `cli/commands/security.py`, `cli/commands/security.py`, `cli/commands/security.py`, `cli/commands/security.py`, `cli/commands/security.py`, `cli/engagement_hooks.py`, `core/__init__.py`, `core/credential_vault.py`, `core/prompt.py`, `lazyown.py`, `lazyown.py`, `lazyown.py`, `lazyown.py`, `lazyown.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/c2_profile_engine.py`, `modules/db.py`, `modules/db.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/reactive_engine.py`, `mutants/tests/test_aes_key_propagation.py`, `mutants/tests/test_cli_assign.py`, `mutants/tests/test_cli_command_sets.py`, `mutants/tests/test_cli_command_sets.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_improvements_spec.py`, `tests/test_aes_key_propagation.py`, `tests/test_cli_assign.py`, `tests/test_cli_command_sets.py`, `tests/test_cli_command_sets.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_improvements_spec.py`, `utils.py`

## core/console.py
- Layer: utility
- Language: py
- Symbols:
  - `_sanitize` (function, line 90) `def _sanitize(text)`
  - `print_error` (function, line 95) `def print_error(error)`
  - `print_msg` (function, line 100) `def print_msg(msg)`
  - `print_warn` (function, line 105) `def print_warn(warn)`
  - `print_succ` (function, line 110) `def print_succ(msg)`
- Imported by: `cli/autosuggest.py`, `cli/command_explorer.py`, `cli/commands/misc_migrated.py`, `cli/commands/misc_migrated.py`, `cli/commands/misc_migrated.py`, `cli/commands/misc_migrated.py`, `cli/commands/recon.py`, `cli/commands/security.py`, `cli/commands/security.py`, `cli/config_status.py`, `cli/contextual_help.py`, `cli/doctor.py`, `cli/exploit_advisor.py`, `cli/exploration_view.py`, `cli/ops_commands.py`, `cli/protips.py`, `cli/reactive_hints.py`, `cli/session_resumer.py`, `cli/splash.py`, `cli/surface_tui.py`, `cli/tips_engine.py`, `cli/toast_bus.py`, `cli/tutorial.py`, `cli/wizard.py`, `core/__init__.py`, `core/credentials.py`, `core/http.py`, `core/network.py`, `core/parsers.py`, `core/process.py`, `core/validators.py`, `key.py`, `lazy_sentinel4.py`, `lazyown.py`, `lazyown.py`, `modules/apt_playbooks.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/legacy/lazybinenc.py`, `modules/lilsplunky.py`, `modules/privesc_predictor.py`, `modules/rich_tui.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_exploration_and_addons.py`, `mutants/tests/test_toast_bus.py`, `mutants/tests/test_tui_splash.py`, `mutants/tests/test_tui_style.py`, `mutants/tests/test_tui_themes.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_exploration_and_addons.py`, `tests/test_scope_guard_integration.py`, `tests/test_toast_bus.py`, `tests/test_tui_splash.py`, `tests/test_tui_style.py`, `tests/test_tui_themes.py`, `utils.py`, `utils.py`

## core/credential_vault.py
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
- Imported by: `cli/commands/security.py`, `cli/commands/security.py`, `cli/commands/security.py`, `lazyown.py`, `lazyown.py`, `mutants/tests/test_credential_vault.py`, `tests/test_credential_vault.py`

## core/credentials.py
- Layer: utility
- Language: py
- Symbols:
  - `get_credentials` (function, line 17) `def get_credentials(file, ncred)`
  - `get_domain` (function, line 67) `def get_domain(url)`
  - `get_hash` (function, line 81) `def get_hash(dir)`
  - `get_users_dic` (function, line 115) `def get_users_dic(txt)`
  - `return_creds` (function, line 146) `def return_creds()`
  - `generate_emails` (function, line 160) `def generate_emails(full_name, domain)`
  - `crack_password` (function, line 183) `def crack_password(crypttext)`
  - `find_ea` (function, line 220) `def find_ea(keyword)`
  - `find_ps` (function, line 249) `def find_ps(keyword)`
  - `find_ss` (function, line 261) `def find_ss(keyword)`
  - `Spray` (function, line 273) `def Spray(domain, users, password, target_url, wait, verbose, more_verbose)`
  - `format_openssh_key` (function, line 341) `def format_openssh_key(raw_key)`
  - `format_rsa_key` (function, line 355) `def format_rsa_key(raw_key)`
- Depends on: `core/console.py`
- Imported by: `core/__init__.py`

## core/crypto.py
- Layer: utility
- Language: py
- Symbols:
  - `generate_salt` (function, line 24) `def generate_salt(length)`
  - `derive_key` (function, line 36) `def derive_key(password, salt)`
  - `xor_encrypt_decrypt` (function, line 67) `def xor_encrypt_decrypt(data, key)`
  - `generate_xor_key` (function, line 83) `def generate_xor_key(length)`
  - `AESencrypt` (function, line 98) `def AESencrypt(plaintext, key)`
  - `AESdecrypt` (function, line 123) `def AESdecrypt(data, key)`
  - `dropFile` (function, line 154) `def dropFile(key, ciphertext)`
- Imported by: `cli/auto_crypto.py`, `cli/commands/exfiltration.py`, `core/__init__.py`, `core/credential_vault.py`, `modules/db.py`, `modules/db.py`, `modules/phishing_orchestrator.py`, `modules/phishing_orchestrator.py`, `modules/phishing_orchestrator.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `utils.py`

## core/dependencies.py
- Layer: utility
- Language: py
- Symbols:
  - `MissingDependencyError` (class, line 37) `class MissingDependencyError(ImportError)`
  - `DependencySpec` (class, line 66) `class DependencySpec`
  - `_DeferredImport` (class, line 101) `class _DeferredImport`
  - `_spec_for` (method, line 157) `def _spec_for(import_name, pip_package, feature)`
  - `optional_import` (method, line 183) `def optional_import(import_name)`
  - `optional_attr` (method, line 209) `def optional_attr(import_name, attr)`
  - `DependencyStatus` (class, line 253) `class DependencyStatus`
  - `DependencyReport` (class, line 268) `class DependencyReport`
  - `probe_python_dependency` (method, line 288) `def probe_python_dependency(spec)`
  - `collect_dependency_report` (method, line 312) `def collect_dependency_report()`
  - `format_report` (method, line 323) `def format_report(report)`
  - `main` (method, line 368) `def main()`
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
- Imported by: `core/__init__.py`, `mutants/tests/test_dependencies.py`, `tests/test_dependencies.py`, `utils.py`

## core/errors.py
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
- Layer: utility
- Language: py
- Symbols:
  - `_validate_input` (function, line 41) `def _validate_input(command)`
  - `_validate_timeout` (function, line 75) `def _validate_timeout(timeout)`
  - `safe_run` (function, line 96) `def safe_run(command)`
  - `safe_run` (function, line 98) `def safe_run(command)`
  - `safe_run` (function, line 101) `def safe_run(command)`
  - `run_shell` (function, line 141) `def run_shell(cmd)`
- Depends on: `core/logging.py`
- Imported by: `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `mutants/tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`, `tests/test_core_executor.py`

## core/hardening.py
- Layer: utility
- Language: py
- Symbols:
  - `SecurityViolation` (class, line 45) `class SecurityViolation(PermissionError)`
  - `safe_subprocess_run` (method, line 49) `def safe_subprocess_run(argv)`
  - `safe_clipboard_copy` (method, line 87) `def safe_clipboard_copy(content)`
  - `build_sshpass_command` (method, line 126) `def build_sshpass_command(password, ssh_args)`
  - `set_sshpass_env` (method, line 155) `def set_sshpass_env(password)`
  - `escape_html_content` (method, line 174) `def escape_html_content(value)`
  - `safe_path_join` (method, line 186) `def safe_path_join(base_dir, user_path)`
  - `validate_network_cidr` (method, line 212) `def validate_network_cidr(cidr)`
  - `validate_port_spec` (method, line 224) `def validate_port_spec(ports)`
  - `validate_host` (method, line 240) `def validate_host(host)`
  - `require_encryption_key` (method, line 262) `def require_encryption_key(env_key, secret_file)`
  - `defused_xml_parse` (method, line 290) `def defused_xml_parse(source)`
  - `sanitize_filename` (method, line 312) `def sanitize_filename(filename, max_length)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/anti_forensics.py`, `cli/commands/anti_forensics.py`, `cli/commands/anti_forensics.py`, `cli/commands/anti_forensics.py`, `cli/commands/anti_forensics.py`, `cli/commands/cloud.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/exfiltration.py`, `cli/commands/lateral_migrated.py`, `cli/commands/misc_migrated.py`, `cli/commands/persist_migrated.py`, `cli/commands/persist_migrated.py`, `cli/commands/pivoting.py`, `lazyc2.py`, `modules/phishing_orchestrator.py`, `modules/websocket_beacon.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `mutants/tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`, `tests/test_security_hardening_v3.py`

## core/http.py
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
- Layer: utility
- Language: py
- Symbols:
  - `BudgetExceeded` (class, line 54) `class BudgetExceeded(RuntimeError)`
  - `LLMBackendLike` (class, line 58) `class LLMBackendLike(Protocol)`
  - `ModelPrice` (class, line 69) `class ModelPrice`
  - `BudgetConfig` (class, line 103) `class BudgetConfig`
  - `LedgerEntry` (class, line 132) `class LedgerEntry`
  - `_today_utc` (method, line 150) `def _today_utc(now)`
  - `_now_iso` (method, line 163) `def _now_iso(now)`
  - `BudgetLedger` (class, line 176) `class BudgetLedger`
  - `TokenEstimator` (class, line 268) `class TokenEstimator`
  - `BudgetGuard` (class, line 310) `class BudgetGuard`
  - `BudgetedBackend` (class, line 408) `class BudgetedBackend`
  - `default_model_prices` (method, line 442) `def default_model_prices()`
  - `default_sessions_dir` (method, line 461) `def default_sessions_dir()`
  - `_coerce_bool` (method, line 476) `def _coerce_bool(value, default)`
  - `_coerce_price_table` (method, line 496) `def _coerce_price_table(value)`
  - `_coerce_positive_float` (method, line 520) `def _coerce_positive_float(value, default)`
  - `_coerce_positive_int` (method, line 536) `def _coerce_positive_int(value, default)`
  - `load_budget_config` (method, line 552) `def load_budget_config(payload, sessions_dir)`
  - `read_budget_status` (method, line 585) `def read_budget_status(payload, sessions_dir)`
  - `format_budget_status` (method, line 616) `def format_budget_status(config, ledger)`
  - `_has_required_methods` (method, line 642) `def _has_required_methods(backend)`
  - `wrap_backend_with_budget` (method, line 657) `def wrap_backend_with_budget(backend, config, estimator, model, ledger)`
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
- Imported by: `cli/commands/ai.py`, `modules/llm_factory.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `mutants/tests/test_llm_budget.py`, `skills/lazyown_mcp.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`, `tests/test_llm_budget.py`

## core/logging.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `StructuredLogConfig` (class, line 41) `class StructuredLogConfig`
  - `_JsonLineFormatter` (class, line 70) `class _JsonLineFormatter(Formatter)`
  - `_ConsoleFormatter` (class, line 120) `class _ConsoleFormatter(Formatter)`
  - `StructuredLogger` (class, line 138) `class StructuredLogger(Logger)`
  - `_log_factory` (method, line 179) `def _log_factory(name, config)`
  - `get_logger` (method, line 230) `def get_logger(name)`
  - `install_json_handler` (method, line 250) `def install_json_handler(name, config)`
  - `reconfigure` (method, line 299) `def reconfigure(config)`
  - `__init__` (method, line 73) `def __init__(self, redacted_fields)`
  - `format` (method, line 77) `def format(self, record)`
  - `format` (method, line 131) `def format(self, record)`
  - `makeRecord` (method, line 147) `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)`
- Imported by: `cli/chain_mode.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/tips_engine.py`, `core/config.py`, `core/credential_vault.py`, `core/executor.py`, `core/hardening.py`, `core/safe_exec.py`, `core/scheduler.py`, `core/security.py`, `lazy_sentinel4.py`, `lazyc2.py`, `lazyc2.py`, `lazyc2.py`, `lazyc2/blueprints/api.py`, `lazyc2/blueprints/beacon.py`, `lazyc2/blueprints/phishing.py`, `lazyc2/extensions/short_urls.py`, `lazyc2/extensions/storage.py`, `lazygui/app.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/settings.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/agent_tool.py`, `modules/ai_model.py`, `modules/atomic_enricher.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/beacon_history.py`, `modules/bof_registry.py`, `modules/c2_profile.py`, `modules/c2_profile.py`, `modules/c2_profile_engine.py`, `modules/collab_bp.py`, `modules/command_executor.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/config_store.py`, `modules/credential_reuse.py`, `modules/cve_matcher.py`, `modules/cve_matcher.py`, `modules/db.py`, `modules/detection_feed.py`, `modules/detection_oracle.py`, `modules/engagement_hooks.py`, `modules/estorides_importer.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/hash_cracker.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/icmp_server.py`, `modules/integrations/misp_export.py`, `modules/integrations/misp_export.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/integrations/searchsploit.py`, `modules/integrations/searchsploit.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_rbac.py`, `modules/lazyownerweb.py`, `modules/legacy/lazydeepseekcli.py`, `modules/legacy/lazygptcli.py`, `modules/legacy/lazygptcli_unified.py`, `modules/legacy/lazyhoneypot.py`, `modules/legacy/lazyopenssh77enum2.py`, `modules/legacy/lazyphishingai.py`, `modules/legacy/lazysearch_bot.py`, `modules/legacy/lazysmbrelay.py`, `modules/legacy/lazyssh.py`, `modules/lesson_ingestor.py`, `modules/lilsplunky.py`, `modules/llm_client.py`, `modules/logging_config.py`, `modules/mcp_agent_bridge.py`, `modules/metrics.py`, `modules/module_registry.py`, `modules/moe_router.py`, `modules/moe_router.py`, `modules/obs_parser.py`, `modules/obs_parser.py`, `modules/operation.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/playbook_engine.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/rl_trainer.py`, `modules/session_rag.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`, `modules/state_manager.py`, `modules/sudo_tiocsti.py`, `modules/threat_model.py`, `modules/toposwarm_bridge.py`, `modules/toposwarm_bridge.py`, `modules/ttp_coverage.py`, `modules/unified_bridge.py`, `modules/unified_dashboard.py`, `modules/vuln_agent.py`, `modules/vulnbot.py`, `modules/world_model.py`, `modules/world_model.py`, `mutants/core/hardening.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `mutants/tests/test_structured_logging.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/autonomous_replay.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`, `tests/test_structured_logging.py`

## core/network.py
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

## core/parsers.py
- Layer: utility
- Language: py
- Symbols:
  - `strip_ansi` (function, line 21) `def strip_ansi(text)`
  - `clean_output` (function, line 40) `def clean_output(output)`
  - `clean_html` (function, line 52) `def clean_html(html_string)`
  - `clean_url` (function, line 64) `def clean_url(host)`
  - `htmlify` (function, line 79) `def htmlify(data)`
  - `de_htmlify` (function, line 91) `def de_htmlify(data)`
  - `is_exist` (function, line 106) `def is_exist(file)`
  - `get_xml` (function, line 121) `def get_xml(directory)`
  - `get_domain_from_xml` (function, line 137) `def get_domain_from_xml(xml_file)`
  - `extract_banners` (function, line 161) `def extract_banners(xml_file)`
  - `parse_nmap_csv` (function, line 191) `def parse_nmap_csv(csv_path)`
  - `manual_yaml_extraction` (function, line 211) `def manual_yaml_extraction(content)`
  - `fix_common_yaml_issues` (function, line 232) `def fix_common_yaml_issues(yaml_content)`
  - `aggressive_yaml_fix` (function, line 257) `def aggressive_yaml_fix(yaml_content)`
  - `create_synthetic_yaml` (function, line 283) `def create_synthetic_yaml(nmap_services)`
  - `parse_yaml_response` (function, line 306) `def parse_yaml_response(content)`
  - `load_adversary` (function, line 325) `def load_adversary()`
  - `load_knowledge_base` (function, line 338) `def load_knowledge_base(knowledge_file)`
  - `load_user_aliases` (function, line 354) `def load_user_aliases()`
  - `list_binaries` (function, line 368) `def list_binaries(directory)`
  - `select_binary` (function, line 383) `def select_binary(binaries)`
- Depends on: `core/console.py`, `skills/claude_md_orchestrator/parser.py`
- Imported by: `cli/banner_config.py`, `core/__init__.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `telegram_hermes.py`, `utils.py`

## core/payload_schema.py
- Layer: utility
- Language: py
- Symbols:
  - `FieldKind` (class, line 60) `class FieldKind(StrEnum)`
  - `Severity` (class, line 78) `class Severity(StrEnum)`
  - `FieldSpec` (class, line 87) `class FieldSpec`
  - `ValidationIssue` (class, line 129) `class ValidationIssue`
  - `_validate_string` (method, line 152) `def _validate_string(value)`
  - `_validate_int` (method, line 158) `def _validate_int(value)`
  - `_validate_port` (method, line 172) `def _validate_port(value)`
  - `_validate_bool` (method, line 182) `def _validate_bool(value)`
  - `_validate_ip` (method, line 199) `def _validate_ip(value)`
  - `_validate_hostname` (method, line 207) `def _validate_hostname(value)`
  - `_validate_url` (method, line 219) `def _validate_url(value)`
  - `_validate_path` (method, line 227) `def _validate_path(value)`
  - `_validate_interface` (method, line 233) `def _validate_interface(value)`
  - `_validate_hex` (method, line 241) `def _validate_hex(value)`
  - `_validate_os_id` (method, line 249) `def _validate_os_id(value)`
  - `_validate_json_blob` (method, line 255) `def _validate_json_blob(value)`
  - `_validate_opaque` (method, line 267) `def _validate_opaque(_value)`
  - `_coerce_int` (method, line 288) `def _coerce_int(raw)`
  - `_coerce_bool` (method, line 303) `def _coerce_bool(raw)`
  - `_spec` (method, line 322) `def _spec(name, kind, default, description)`
  - `field_for` (method, line 1113) `def field_for(key)`
  - `coerce_value` (method, line 1118) `def coerce_value(key, raw)`
  - `validate_value` (method, line 1141) `def validate_value(key, value)`
  - `validate_payload` (method, line 1215) `def validate_payload(payload)`
  - `format_issue` (method, line 1250) `def format_issue(issue)`
  - `default_payload` (method, line 1268) `def default_payload()`
  - `categories` (method, line 1276) `def categories()`
- Depends on: `cli/commands/enum.py`
- Imported by: `cli/assign.py`, `cli/wizard.py`, `core/__init__.py`, `core/config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_core_config.py`, `mutants/tests/test_payload_schema.py`, `skills/lazyown_mcp.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_core_config.py`, `tests/test_payload_schema.py`

## core/process.py
- Layer: business_logic
- Language: py
- Symbols:
  - `check_go_tool_installed` (function, line 32) `def check_go_tool_installed(tool_name)`
  - `is_binary_present` (function, line 52) `def is_binary_present(binary_name)`
  - `handle_multiple_rhosts` (function, line 66) `def handle_multiple_rhosts(func)`
  - `check_sudo` (function, line 95) `def check_sudo()`
  - `run` (function, line 106) `def run(command)`
  - `is_package_installed` (function, line 141) `def is_package_installed(package_name)`
  - `_print_run_command_status` (function, line 157) `def _print_run_command_status(command, elapsed, exit_code)`
  - `run_command` (function, line 181) `def run_command(command, timeout)`
  - `ensure_tmux_session` (function, line 250) `def ensure_tmux_session(session_name)`
  - `activate_server` (function, line 268) `def activate_server(httpd, url, lhost)`
  - `wrapper` (function, line 80) `def wrapper(self)`
  - `_drain_stderr` (function, line 217) `def _drain_stderr()`
- Depends on: `core/console.py`, `core/safe_subprocess.py`, `core/validators.py`
- Imported by: `core/__init__.py`, `modules/auto_purple.py`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `static/js/vis-network.min.js`, `utils.py`

## core/prompt.py
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
- Imported by: `key.py`, `modules/legacy/lazybinenc.py`, `static/js/quill-2.0.3.js`

## core/protocols.py
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
- Imported by: `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`

## core/safe_exec.py
- Layer: utility
- Language: py
- Symbols:
  - `CommandInjectionError` (class, line 42) `class CommandInjectionError(PermissionError)`
  - `UrlValidationError` (class, line 46) `class UrlValidationError(PermissionError)`
  - `safe_system` (method, line 50) `def safe_system(command)`
  - `safe_run_argv` (method, line 83) `def safe_run_argv(argv)`
  - `safe_run_shell` (method, line 123) `def safe_run_shell(command)`
  - `safe_clear_screen` (method, line 162) `def safe_clear_screen()`
  - `validate_url` (method, line 177) `def validate_url(url)`
  - `safe_git_clone` (method, line 204) `def safe_git_clone(repo_url, target_dir)`
  - `safe_ip_show` (method, line 238) `def safe_ip_show(interface)`
  - `safe_find_tool` (method, line 271) `def safe_find_tool(name)`
  - `safe_file_read` (method, line 287) `def safe_file_read(path)`
- Depends on: `core/logging.py`
- Imported by: `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`, `tests/test_security_hardening_v4.py`

## core/safe_subprocess.py
- Layer: business_logic
- Language: py
- Symbols:
  - `ShellNotAllowedError` (class, line 36) `class ShellNotAllowedError(PermissionError)`
  - `SafeRunResult` (class, line 41) `class SafeRunResult`
  - `SafeRunner` (class, line 57) `class SafeRunner`
  - `__init__` (method, line 67) `def __init__(self, audit_log_path)`
  - `run` (method, line 70) `def run(self, argv)`
  - `run_shell` (method, line 102) `def run_shell(self, command)`
  - `_audit` (method, line 172) `def _audit(self, record)`
- Imported by: `core/process.py`, `mutants/tests/test_safe_subprocess.py`, `mutants/tests/test_safe_subprocess_behavior.py`, `mutants/tests/test_security_hardening.py`, `tests/test_safe_subprocess.py`, `tests/test_safe_subprocess_behavior.py`, `tests/test_security_hardening.py`, `utils.py`

## core/scheduler.py
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
- Layer: utility
- Language: py
- Symbols:
  - `anti_debug` (function, line 18) `def anti_debug()`
  - `generate_certificates` (function, line 58) `def generate_certificates(output_dir)`
- Depends on: `core/logging.py`

## core/validators.py
- Layer: utility
- Language: py
- Symbols:
  - `check_rhost` (function, line 16) `def check_rhost(rhost)`
  - `check_lhost` (function, line 27) `def check_lhost(lhost)`
  - `check_lport` (function, line 38) `def check_lport(lport)`
  - `check_port` (function, line 48) `def check_port(port, name)`
- Depends on: `core/console.py`
- Imported by: `cli/commands/enum.py`, `core/__init__.py`, `core/process.py`, `modules/c2_builder.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `mutants/tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `tests/test_core.py`, `utils.py`
