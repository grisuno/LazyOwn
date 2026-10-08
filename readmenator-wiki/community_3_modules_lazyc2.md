# modules: lazyc2

*Community 3 | 77 files | cohesion 0.53*

## Definition

This community groups 77 file(s) rooted at `tests` with dominant language py (cohesion 0.53). Central symbols: `AESKeyManager`, `AESdecrypt`, `AESencrypt`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`. Core file: `lazyc2.py` (263 symbols). Documented purpose: Automatic encryption of sensitive session data on app open/close.  Before this module the operator had to manually run ``lazyenc.py encrypt`` and ``lazyenc.py d.

## Files

### `tests` (27 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |

### `modules` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_history.py` | py | utility | 7 | yes |
| `modules/cli_auth.py` | py | utility | 18 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/campaign.py` | py | utility | 7 | yes |
| `cli/commands/cli_auth.py` | py | utility | 5 | yes |

### `lazyc2` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |

### `lazyc2/extensions` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `core` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/auto_crypto.py` | py | utility | 12 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 263 | no |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

*... and 57 more files in this community.*


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
- `CampaignCommandSet` (class, `cli/commands/campaign.py:36`) `class CampaignCommandSet(LazyOwnCommandSet)` - Export and import full campaign packages as portable archives.
- `do_campaign` (method, `cli/commands/campaign.py:43`) `def do_campaign(self, line)` - Export or import an entire campaign as a portable package.
- `_gather_campaign_manifest` (method, `cli/commands/campaign.py:92`) `def _gather_campaign_manifest(self, name)` - Build a manifest describing the current campaign state.
- `_campaign_export` (method, `cli/commands/campaign.py:134`) `def _campaign_export(self, name)` - Package the current campaign into a portable .zip archive.
- `_campaign_import` (method, `cli/commands/campaign.py:183`) `def _campaign_import(self, package_path)` - Restore a campaign from an exported .zip archive.
- `_campaign_list` (method, `cli/commands/campaign.py:308`) `def _campaign_list(self)` - List exported campaign packages.
- `_campaign_status` (method, `cli/commands/campaign.py:340`) `def _campaign_status(self)` - Print the live shared campaign state (no export, read-only).
- `CliAuthCommandSet` (class, `cli/commands/cli_auth.py:27`) `class CliAuthCommandSet(LazyOwnCommandSet)` - CLI operator authentication — login, logout, whoami.
- `do_login` (method, `cli/commands/cli_auth.py:34`) `def do_login(self, line)` - Authenticate against users.json (same users as lazyc2.py).
- `do_register` (method, `cli/commands/cli_auth.py:117`) `def do_register(self, line)` - Register a new operator account in users.json.
- `do_logout` (method, `cli/commands/cli_auth.py:191`) `def do_logout(self, line)` - Log out the current CLI operator and clear the remember-me token.
- `do_whoami` (method, `cli/commands/cli_auth.py:224`) `def do_whoami(self, line)` - Show the currently logged-in CLI operator.
- `DatabaseCommandSet` (class, `cli/commands/database.py:24`) `class DatabaseCommandSet(LazyOwnCommandSet)` - Database commands for campaign state management.
- `_get_db` (method, `cli/commands/database.py:30`) `def _get_db(self)`
- `_active_workspace` (method, `cli/commands/database.py:38`) `def _active_workspace(self)`
- `do_db_init` (method, `cli/commands/database.py:55`) `def do_db_init(self, line)` - Initialize the database (creates schema if not exists).
- `do_db_workspace` (method, `cli/commands/database.py:73`) `def do_db_workspace(self, line)` - Manage workspaces (list, create, switch, delete).
- `do_db_hosts` (method, `cli/commands/database.py:122`) `def do_db_hosts(self, line)` - List or add hosts in the active workspace.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 259
- Cross-boundary resolved imports (EXTRACTED): 182

## Connections

- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 8 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/phishing_wizard.py imports modules/phishing_orchestrator.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [cycle] `cli/engagement_hooks.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
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

- Why do 4 file(s) lack file-level docs (e.g. `lazyc2.py`)? What purpose do they serve?
- Can the cycle `cli/engagement_hooks.py` -> `modules/cli_auth.py` be broken with an interface?
- What would break if the most connected file in modules: lazyc2 changed?
- Should modules: lazyc2 be split, given cohesion 0.53?

## Sources

- `cli/auto_crypto.py`
- `cli/commands/campaign.py`
- `cli/commands/cli_auth.py`
- `cli/commands/database.py`
- `cli/commands/redteam_gym.py`
- `cli/engagement_hooks.py`
- `core/api_authz.py`
- `core/crypto.py`
- `core/protocols.py`
- `lazyc2.py`
- `lazyc2/__init__.py`
- `lazyc2/addon_creator.py`
- `lazyc2/app_factory.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/api.py`
- `lazyc2/blueprints/api_v1.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/session_auth.py`
- *... and 57 more*
