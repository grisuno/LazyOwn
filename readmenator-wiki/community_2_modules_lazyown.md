# modules: lazyown

*Community 2 | 70 files | cohesion 0.36*

## Definition

This community groups 70 file(s) rooted at `modules` with dominant language py (cohesion 0.36). Central symbols: `AESdecrypt`, `AESencrypt`, `AgentBridgeWorker`, `AuditConfig`, `AutoCryptoConfig`, `AutoCryptoEngine`, `AutoRecommender`, `AutomationCommandSet`. Core file: `lazyown.py` (127 symbols). Documented purpose: Automatic encryption of sensitive session data on app open/close.  Before this module the operator had to manually run ``lazyenc.py encrypt`` and ``lazyenc.py d.

## Files

### `modules` (24 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_history.py` | py | utility | 7 | yes |
| `modules/c2_profile.py` | py | utility | 32 | yes |

### `tests` (20 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_api_v1.py` | py | testing | 13 | yes |
| `tests/test_auto_crypto.py` | py | testing | 13 | yes |

### `core` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/command_bridge.py` | py | utility | 9 | yes |
| `core/credential_vault.py` | py | utility | 8 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |
| `cli/commands/collaboration.py` | py | utility | 8 | yes |

### `contrib/legacy` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyhoneypot.py` | py | utility | 15 | yes |
| `contrib/legacy/lazyopenssh77enum2.py` | py | utility | 5 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/auto_crypto.py` | py | utility | 12 | yes |
| `cli/headless.py` | py | utility | 6 | yes |

### `lazyc2/blueprints` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/api_v1.py` | py | presentation | 12 | yes |
| `lazyc2/blueprints/beacon.py` | py | presentation | 7 | yes |

### `modules/integrations` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/nuclei_bridge.py` | py | utility | 29 | yes |
| `modules/integrations/nuclei_parser.py` | py | utility | 17 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown.py` | py | utility | 127 | yes |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/command_audit.py` | py | utility | 4 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/toposwarm_autonomous.py` | py | utility | 15 | yes |

*... and 50 more files in this community.*


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
- `CollaborationCommandSet` (class, `cli/commands/collaboration.py:20`) `class CollaborationCommandSet(LazyOwnCommandSet)` - Multi-operator collaboration commands for the CLI.
- `_get_collab` (method, `cli/commands/collaboration.py:26`) `def _get_collab(self)` - Lazy-load collaboration singletons from modules.collab_bp.
- `_resolve_target` (method, `cli/commands/collaboration.py:38`) `def _resolve_target(self, target)` - Resolve a target argument: explicit IP or rhost from payload.
- `do_lock_target` (method, `cli/commands/collaboration.py:48`) `def do_lock_target(self, line)` - Acquire an advisory lock on a target to prevent tool collisions.
- `do_unlock_target` (method, `cli/commands/collaboration.py:89`) `def do_unlock_target(self, line)` - Release an advisory lock on a target.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 277
- Cross-boundary resolved imports (EXTRACTED): 291

## Connections

- [EXTRACTED] depends_on community 2 <-> 10 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 9 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `modules/toposwarm_bridge.py` via `subprocess` (5 hops)
- [taint high] `cli/banner_config.py` -> `core/crypto.py` via `subprocess` (5 hops)
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [layer strict] `tests/test_api_v1.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `lazyc2/blueprints/api_v1.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `contrib/legacy/lazyssh.py`)? What purpose do they serve?
- Can the cycle `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` be broken with an interface?
- What would break if the most connected file in modules: lazyown changed?
- Should modules: lazyown be split, given cohesion 0.36?

## Sources

- `cli/auto_crypto.py`
- `cli/commands/automation.py`
- `cli/commands/collaboration.py`
- `cli/commands/estorides.py`
- `cli/commands/security.py`
- `cli/headless.py`
- `contrib/legacy/lazyhoneypot.py`
- `contrib/legacy/lazyopenssh77enum2.py`
- `contrib/legacy/lazysearch_bot.py`
- `contrib/legacy/lazyssh.py`
- `core/command_bridge.py`
- `core/credential_vault.py`
- `core/crypto.py`
- `core/executor.py`
- `core/logging.py`
- `core/safe_exec.py`
- `core/scheduler.py`
- `core/security.py`
- `lazyc2/blueprints/api_v1.py`
- `lazyc2/blueprints/beacon.py`
- *... and 50 more*
