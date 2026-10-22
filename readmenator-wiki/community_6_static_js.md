# static/js

*Community 6 | 43 files | cohesion 0.42*

## Definition

This community groups 43 file(s) rooted at `static/js` with dominant language py (cohesion 0.42). Central symbols: `A`, `AESdecrypt`, `AESencrypt`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

### `static/js` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |

### `tests` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_crypto.py` | py | testing | 22 | yes |
| `tests/test_cli_assign.py` | py | testing | 44 | yes |
| `tests/test_core.py` | py | testing | 47 | yes |

### `core` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/crypto.py` | py | utility | 7 | yes |
| `core/param_registry.py` | py | utility | 17 | yes |

### `cli` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/auto_crypto.py` | py | utility | 13 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/params_ops.py` | py | utility | 2 | yes |
| `cli/commands/session_ops.py` | py | utility | 37 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 39 | yes |
| `lazyc2/state.py` | py | utility | 0 | yes |

### `modules` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/exp.c` | c | utility | 58 | yes |
| `modules/search.py` | py | utility | 0 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazybinenc.py` | py | utility | 2 | no |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

*... and 23 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:42`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `AutoCryptoConfig` (class, `cli/auto_crypto.py:48`) `class AutoCryptoConfig` - Centralised configuration for automatic session encryption.
- `AutoCryptoEngine` (class, `cli/auto_crypto.py:77`) `class AutoCryptoEngine` - Encrypt and decrypt sensitive session files with a derived key.
- `__init__` (method, `cli/auto_crypto.py:85`) `def __init__(self, config)`
- `enabled` (method, `cli/auto_crypto.py:90`) `def enabled(self)` - Whether the engine performs any I/O.
- `is_encrypted` (method, `cli/auto_crypto.py:95`) `def is_encrypted(self)` - Check whether session data appears encrypted.
- `encrypt_session` (method, `cli/auto_crypto.py:124`) `def encrypt_session(self)` - Encrypt all protected session files.
- `decrypt_session` (method, `cli/auto_crypto.py:174`) `def decrypt_session(self)` - Decrypt all protected session files.
- `has_password` (method, `cli/auto_crypto.py:239`) `def has_password(self)` - Return True when the configured provider yields a password now.
- `_get_password` (method, `cli/auto_crypto.py:251`) `def _get_password(self)`
- `_load_or_create_salt` (method, `cli/auto_crypto.py:260`) `def _load_or_create_salt(self)`
- `_derive_key` (method, `cli/auto_crypto.py:291`) `def _derive_key(password, salt)`
- `build_password_provider_from_cli_login` (function, `cli/auto_crypto.py:297`) `def build_password_provider_from_cli_login()` - Return a password provider that reads the CLI login session.
- `_provider` (function, `cli/auto_crypto.py:310`) `def _provider()`
- `ParamCommandSet` (class, `cli/commands/params_ops.py:31`) `class ParamCommandSet(LazyOwnCommandSet)` - Create, inspect and delete the shared parameters.
- `do_param` (method, `cli/commands/params_ops.py:38`) `def do_param(self, line)` - Manage the shared parameter catalog used by addons and aliases.
- `_strip_shell_quotes` (function, `cli/commands/session_ops.py:72`) `def _strip_shell_quotes(value)` - Drop one pair of matching wrapping quotes kept by ``posix=False`` parsing.
- `SessionOpsCommandSet` (class, `cli/commands/session_ops.py:86`) `class SessionOpsCommandSet(LazyOwnCommandSet)` - Session and campaign operations.
- `do_note` (method, `cli/commands/session_ops.py:93`) `def do_note(self, line)` - Capture a quick operator note attached to the current target and phase.
- `do_l00t` (method, `cli/commands/session_ops.py:118`) `def do_l00t(self, line)` - Unified loot: show, search, reuse, graph, and mark credentials.
- `do_loot` (method, `cli/commands/session_ops.py:167`) `def do_loot(self, line)` - Alias for ``l00t`` — unified loot (show/search/reuse/graph/mark).
- `do_pivot` (method, `cli/commands/session_ops.py:175`) `def do_pivot(self, line)` - Record a newly discovered pivot target or show the pivot chain.
- `do_tasks` (method, `cli/commands/session_ops.py:200`) `def do_tasks(self, line)` - View and manage the task queue from sessions/tasks.json.
- `do_scans` (method, `cli/commands/session_ops.py:233`) `def do_scans(self, line)` - List nmap scan files in sessions/ with age, size, and open ports.
- `do_sitrep` (method, `cli/commands/session_ops.py:250`) `def do_sitrep(self, line)` - Print a unified operational situation report.
- `do_assign` (method, `cli/commands/session_ops.py:267`) `def do_assign(self, line)` - assign a parameter value, persist to payload.json and refresh aliases.
- `do_tenant` (method, `cli/commands/session_ops.py:332`) `def do_tenant(self, line)` - Manage multi-tenancy: list, switch, or create engagement tenants.
- `do_scope` (method, `cli/commands/session_ops.py:405`) `def do_scope(self, line)` - Manage the authorized engagement scope and the scope-guard posture.
- `do_show` (method, `cli/commands/session_ops.py:471`) `def do_show(self, line)` - Show params, modules, payloads, or active module options.
- `do_list` (method, `cli/commands/session_ops.py:547`) `def do_list(self, line)` - Lists all available scripts in the modules directory.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 300
- Cross-boundary resolved imports (EXTRACTED): 174

## Connections

- [EXTRACTED] depends_on community 6 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 6 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 7 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/param_registry.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/crypto.py` via `subprocess` (5 hops)
- [cycle] `core/payload_schema.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [dataflow UNCHECKED_ALLOC] `cli/auto_crypto.py:272` `_load_or_create_salt` `fd`: Result of allocator stored in `fd` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- Can the cycle `core/payload_schema.py` -> `core/param_registry.py` be broken with an interface?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.42?

## Sources

- `cli/assign.py`
- `cli/auto_crypto.py`
- `cli/commands/params_ops.py`
- `cli/commands/session_ops.py`
- `cli/session_resumer.py`
- `cli/show.py`
- `cli/style.py`
- `contrib/legacy/lazybinenc.py`
- `core/crypto.py`
- `core/param_registry.py`
- `core/payload_schema.py`
- `core/process.py`
- `core/prompt.py`
- `core/protocols.py`
- `key.py`
- `lazyc2/addon_creator.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/exp.c`
- `modules/rootkit/rootkit.c`
- *... and 23 more*
