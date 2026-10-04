# tests

*Community 3 | 111 files | cohesion 0.54*

## Definition

This community groups 111 file(s) rooted at `tests` with dominant language py (cohesion 0.54). Central symbols: `ADCSCertipyWrapper`, `AESKeyManager`, `AIExploitChainer`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`. Core file: `lazyc2.py` (263 symbols). Documented purpose: Automatic encryption of sensitive session data on app open/close.  Before this module the operator had to manually run ``lazyenc.py encrypt`` and ``lazyenc.py d.

## Files

### `tests` (36 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 1 | yes |
| `tests/test_addon_creator.py` | py | testing | 86 | yes |

### `modules` (21 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/ai_exploit_chain.py` | py | utility | 11 | yes |

### `cli` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/auto_crypto.py` | py | utility | 12 | yes |
| `cli/dashboard_layout.py` | py | presentation | 3 | yes |

### `lazyc2/security` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `contrib/legacy` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |

### `lazyc2/extensions` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `lazyc2` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |

### `lazygui` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/__init__.py` | py | presentation | 0 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 263 | no |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

*... and 91 more files in this community.*


## Key Symbols

- `AutoCryptoConfig` (class, `cli/auto_crypto.py:48`) `class AutoCryptoConfig` - Centralised configuration for automatic session encryption.
- `AutoCryptoEngine` (class, `cli/auto_crypto.py:77`) `class AutoCryptoEngine` - Encrypt and decrypt sensitive session files with a derived key.
- `__init__` (method, `cli/auto_crypto.py:85`) `def __init__(self, config)`
- `enabled` (method, `cli/auto_crypto.py:90`) `def enabled(self)` - Whether the engine performs any I/O.
- `is_encrypted` (method, `cli/auto_crypto.py:95`) `def is_encrypted(self)` - Check whether session data appears encrypted.
- `encrypt_session` (method, `cli/auto_crypto.py:124`) `def encrypt_session(self)` - Encrypt all protected session files.
- `decrypt_session` (method, `cli/auto_crypto.py:174`) `def decrypt_session(self)` - Decrypt all protected session files.
- `_get_password` (method, `cli/auto_crypto.py:239`) `def _get_password(self)`
- `_load_or_create_salt` (method, `cli/auto_crypto.py:248`) `def _load_or_create_salt(self)`
- `_derive_key` (method, `cli/auto_crypto.py:279`) `def _derive_key(password, salt)`
- `build_password_provider_from_cli_login` (method, `cli/auto_crypto.py:285`) `def build_password_provider_from_cli_login()` - Return a password provider that reads the CLI login session.
- `_provider` (method, `cli/auto_crypto.py:298`) `def _provider()`
- `AutomationCommandSet` (class, `cli/commands/automation.py:17`) `class AutomationCommandSet(LazyOwnCommandSet)` - Automation & operator workflow commands.
- `do_cred_reuse` (method, `cli/commands/automation.py:24`) `def do_cred_reuse(self, line)` - Analyze captured credentials and suggest spray targets.
- `do_cred_mark_failed` (method, `cli/commands/automation.py:57`) `def do_cred_mark_failed(self, line)` - Mark a credential as failed against a host.
- `do_hooks_list` (method, `cli/commands/automation.py:78`) `def do_hooks_list(self, line)` - List all conditional hook rules.
- `do_hooks_enable` (method, `cli/commands/automation.py:101`) `def do_hooks_enable(self, line)` - Enable or disable a hook rule.
- `do_hooks_add` (method, `cli/commands/automation.py:129`) `def do_hooks_add(self, line)` - Add a new conditional hook rule (JSON string).
- `do_hooks_remove` (method, `cli/commands/automation.py:150`) `def do_hooks_remove(self, line)` - Remove a hook rule by name.
- `do_hooks_fire` (method, `cli/commands/automation.py:172`) `def do_hooks_fire(self, line)` - Manually fire a hook event for testing.
- `do_operators` (method, `cli/commands/automation.py:202`) `def do_operators(self, line)` - List all operator profiles.
- `do_operator_create` (method, `cli/commands/automation.py:229`) `def do_operator_create(self, line)` - Create a new operator profile.
- `do_operator_load` (method, `cli/commands/automation.py:264`) `def do_operator_load(self, line)` - Load effective config for an operator (team baseline + overrides).
- `do_operator_delete` (method, `cli/commands/automation.py:292`) `def do_operator_delete(self, line)` - Delete an operator profile.
- `do_hooks` (method, `cli/commands/automation.py:314`) `def do_hooks(self, line)` - Conditional hooks management — list, enable, disable, add, remove rules.
- `ExploitMigratedCommandSet` (class, `cli/commands/exploit_migrated.py:36`) `class ExploitMigratedCommandSet(LazyOwnCommandSet)`
- `do_cp` (method, `cli/commands/exploit_migrated.py:41`) `def do_cp(self, line)` - Copies a file from the ExploitDB directory to the sessions directory.
- `do_createcookie` (method, `cli/commands/exploit_migrated.py:82`) `def do_createcookie(self, line)` - Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value.
- `do_py3ttyup` (method, `cli/commands/exploit_migrated.py:128`) `def do_py3ttyup(self, line)` - Copies a Python reverse shell command to the clipboard.
- `do_pyautomate` (method, `cli/commands/exploit_migrated.py:166`) `def do_pyautomate(self, line)` - Automates the execution of pwntomate tools on XML configuration files.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 306
- Cross-boundary resolved imports (EXTRACTED): 288

## Connections

- [EXTRACTED] depends_on community 3 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/crypto.py.
- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 8 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/mcp_bridge.py imports modules/world_model.py.
- [EXTRACTED] depends_on community 3 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/dashboard_tui.py imports cli/commands/containers.py.
- [EXTRACTED] depends_on community 5 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/status_bar.py imports cli/reactive_hints.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [cycle] `lazyc2/blueprints/__init__.py` -> `lazyc2/blueprints/auth.py` -> `lazyc2.py` -> `lazyc2/blueprints/__init__.py`
- [cycle] `lazyc2.py` -> `lazyc2/extensions/users.py` -> `lazyc2.py`
- [cycle] `lazyc2.py` -> `lazyc2/extensions/users.py` -> `lazyc2.py`
- [cycle] `lazyc2.py` -> `lazyc2/extensions/users.py` -> `lazyc2.py`
- [cycle] `lazyc2.py` -> `lazyc2/extensions/users.py` -> `lazyc2.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazyproxy.py`)? What purpose do they serve?
- Can the cycle `lazyc2/blueprints/__init__.py` -> `lazyc2/blueprints/auth.py` -> `lazyc2.py` be broken with an interface?
- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 0.54?

## Sources

- `cli/auto_crypto.py`
- `cli/commands/automation.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/pwn.py`
- `cli/dashboard_layout.py`
- `cli/dashboard_tui.py`
- `cli/graph_advisor.py`
- `cli/killchain.py`
- `cli/noise_verbs.py`
- `cli/ops_commands.py`
- `cli/reactive_hints.py`
- `cli/reasoning_stream.py`
- `cli/recommendation.py`
- `cli/recommendation_signals.py`
- `cli/tips_engine.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazypwn.py`
- `contrib/legacy/lazyseo.py`
- *... and 91 more*
