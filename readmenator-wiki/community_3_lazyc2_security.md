# lazyc2/security

*Community 3 | 63 files | cohesion 0.52*

## Definition

This community groups 63 file(s) rooted at `tests` with dominant language py (cohesion 0.52). Central symbols: `AESKeyManager`, `AESdecrypt`, `AESencrypt`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`. Core file: `lazyc2.py` (263 symbols). Documented purpose: Automatic encryption of sensitive session data on app open/close.  Before this module the operator had to manually run ``lazyenc.py encrypt`` and ``lazyenc.py d.

## Files

### `tests` (25 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `modules` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_history.py` | py | utility | 7 | yes |
| `modules/compliance.py` | py | utility | 25 | yes |

### `lazyc2/blueprints` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `core` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |
| `core/crypto.py` | py | utility | 7 | yes |

### `lazyc2/extensions` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/campaign.py` | py | utility | 7 | yes |
| `cli/commands/database.py` | py | data_access | 15 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |
| `lazyc2/app_factory.py` | py | presentation | 9 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 263 | no |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/auto_crypto.py` | py | utility | 12 | yes |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

*... and 43 more files in this community.*


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
- `DatabaseCommandSet` (class, `cli/commands/database.py:24`) `class DatabaseCommandSet(LazyOwnCommandSet)` - Database commands for campaign state management.
- `_get_db` (method, `cli/commands/database.py:30`) `def _get_db(self)`
- `_active_workspace` (method, `cli/commands/database.py:38`) `def _active_workspace(self)`
- `do_db_init` (method, `cli/commands/database.py:55`) `def do_db_init(self, line)` - Initialize the database (creates schema if not exists).
- `do_db_workspace` (method, `cli/commands/database.py:73`) `def do_db_workspace(self, line)` - Manage workspaces (list, create, switch, delete).
- `do_db_hosts` (method, `cli/commands/database.py:122`) `def do_db_hosts(self, line)` - List or add hosts in the active workspace.
- `do_db_services` (method, `cli/commands/database.py:183`) `def do_db_services(self, line)` - List all services in the active workspace.
- `do_db_vulns` (method, `cli/commands/database.py:211`) `def do_db_vulns(self, line)` - List or add vulnerabilities.
- `do_db_creds` (method, `cli/commands/database.py:265`) `def do_db_creds(self, line)` - List or add credentials.
- `do_db_loot` (method, `cli/commands/database.py:309`) `def do_db_loot(self, line)` - List or add loot items.
- `do_db_notes` (method, `cli/commands/database.py:349`) `def do_db_notes(self, line)` - List or add notes.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 138
- Cross-boundary resolved imports (EXTRACTED): 153

## Connections

- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 3 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/campaign.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/phishing_wizard.py imports modules/phishing_orchestrator.py.

## Risks

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
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `lazyc2.py`)? What purpose do they serve?
- What would break if the most connected file in lazyc2/security changed?
- Should lazyc2/security be split, given cohesion 0.52?

## Sources

- `cli/auto_crypto.py`
- `cli/commands/campaign.py`
- `cli/commands/database.py`
- `core/api_authz.py`
- `core/crypto.py`
- `core/protocols.py`
- `lazyc2.py`
- `lazyc2/addon_creator.py`
- `lazyc2/app_factory.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/api.py`
- `lazyc2/blueprints/api_v1.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/__init__.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/storage.py`
- `lazyc2/security/__init__.py`
- `lazyc2/security/command_allowlist.py`
- *... and 43 more*
