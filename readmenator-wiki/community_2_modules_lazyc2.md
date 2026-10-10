# modules: lazyc2

*Community 2 | 89 files | cohesion 0.46*

## Definition

This community groups 89 file(s) rooted at `modules` with dominant language py (cohesion 0.46). Central symbols: `AESKeyManager`, `AgentBridgeWorker`, `ApiAuthzConfig`, `ApiKey`, `ApiKeyStore`, `AutoCryptoConfig`, `AutoCryptoEngine`, `AutoRecommender`. Core file: `lazyc2.py` (271 symbols). Documented purpose: Automatic encryption of sensitive session data on app open/close.  Before this module the operator had to manually run ``lazyenc.py encrypt`` and ``lazyenc.py d.

## Files

### `modules` (26 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_history.py` | py | utility | 7 | yes |
| `modules/c2_profile.py` | py | utility | 32 | yes |

### `tests` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_api_authz.py` | py | testing | 48 | yes |
| `tests/test_api_v1.py` | py | testing | 13 | yes |

### `contrib/legacy` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |

### `lazyc2/security` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/constants.py` | py | utility | 0 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |
| `core/executor.py` | py | utility | 6 | yes |

### `lazyc2/blueprints` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/api.py` | py | presentation | 8 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `lazyc2/extensions` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |

### `modules/integrations` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/nuclei_bridge.py` | py | utility | 29 | yes |

### `skills` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 271 | no |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/auto_crypto.py` | py | utility | 12 | yes |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/app_factory.py` | py | presentation | 9 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/xterm.js` | js | utility | 62 | no |

*... and 69 more files in this community.*


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
- `CampaignCommandSet` (class, `cli/commands/campaign.py:36`) `class CampaignCommandSet(LazyOwnCommandSet)` - Export and import full campaign packages as portable archives.
- `do_campaign` (method, `cli/commands/campaign.py:43`) `def do_campaign(self, line)` - Export or import an entire campaign as a portable package.
- `_gather_campaign_manifest` (method, `cli/commands/campaign.py:92`) `def _gather_campaign_manifest(self, name)` - Build a manifest describing the current campaign state.
- `_campaign_export` (method, `cli/commands/campaign.py:134`) `def _campaign_export(self, name)` - Package the current campaign into a portable .zip archive.
- `_campaign_import` (method, `cli/commands/campaign.py:183`) `def _campaign_import(self, package_path)` - Restore a campaign from an exported .zip archive.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 300
- Cross-boundary resolved imports (EXTRACTED): 227

## Connections

- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/crypto.py.
- [EXTRACTED] depends_on community 2 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 3 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 9 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)

## Open Questions

- Why do 7 file(s) lack file-level docs (e.g. `contrib/legacy/lazyproxy.py`)? What purpose do they serve?
- Can the cycle `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` be broken with an interface?
- What would break if the most connected file in modules: lazyc2 changed?
- Should modules: lazyc2 be split, given cohesion 0.46?

## Sources

- `cli/auto_crypto.py`
- `cli/commands/automation.py`
- `cli/commands/campaign.py`
- `cli/commands/collaboration.py`
- `cli/commands/estorides.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyhoneypot.py`
- `contrib/legacy/lazyopenssh77enum2.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazysearch_bot.py`
- `contrib/legacy/lazyseo.py`
- `contrib/legacy/lazyssh.py`
- `core/api_authz.py`
- `core/executor.py`
- `core/logging.py`
- `core/scheduler.py`
- `core/security.py`
- `lazyc2.py`
- `lazyc2/app_factory.py`
- *... and 69 more*
