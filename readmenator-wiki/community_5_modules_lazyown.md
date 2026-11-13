# modules: lazyown

*Community 5 | 104 files | cohesion 0.36*

## Definition

This community groups 104 file(s) rooted at `tests` with dominant language py (cohesion 0.36). Central symbols: `AESdecrypt`, `AESencrypt`, `AddonCreatorConfig`, `AddonDraft`, `AddonHotReloader`, `AddonStore`, `AddonValidationError`, `AddonValidator`. Core file: `lazyown.py` (125 symbols). Documented purpose: Declarative cmd2 alias loader.  Reads ``cli/aliases.yaml`` and substitutes ``{name}`` placeholders against a payload dict (typically loaded from ``payload.json`.

## Files

### `tests` (39 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |

### `modules` (19 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/askpass.py` | py | utility | 7 | yes |
| `modules/auto_purple.py` | py | utility | 40 | yes |

### `cli` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/aliases.py` | py | utility | 8 | yes |
| `cli/auto_crypto.py` | py | utility | 13 | yes |

### `cli/commands` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/audit.py` | py | utility | 16 | yes |
| `cli/commands/containers.py` | py | infrastructure | 7 | yes |

### `core` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |
| `core/command_bridge.py` | py | utility | 9 | yes |

### `skills/mcp_tools` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/create_param.py` | py | utility | 1 | yes |
| `skills/mcp_tools/delete_param.py` | py | utility | 1 | yes |

### `poc_tui` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |
| `poc_tui/app.py` | py | utility | 47 | yes |

### `lazyc2/blueprints` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/api.py` | py | presentation | 10 | yes |

### `modules/sinks` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/beacon_dispatch.py` | py | utility | 3 | yes |

### `scripts/devtools` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/command_audit.py` | py | utility | 4 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown.py` | py | utility | 125 | yes |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 39 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 6 | yes |

*... and 84 more files in this community.*


## Key Symbols

- `_SafeFormatDict` (class, `cli/aliases.py:29`) `class _SafeFormatDict(dict)` - ``str.format_map`` source that returns ``""`` for missing/None values.
- `__missing__` (method, `cli/aliases.py:32`) `def __missing__(self, key)`
- `__getitem__` (method, `cli/aliases.py:35`) `def __getitem__(self, key)`
- `_substitute` (function, `cli/aliases.py:42`) `def _substitute(template, payload)` - Render ``template`` against ``payload`` placeholders.
- `template_placeholders` (function, `cli/aliases.py:56`) `def template_placeholders(template)` - Return the ``{name}`` placeholders referenced by ``template``.
- `empty_placeholders` (function, `cli/aliases.py:72`) `def empty_placeholders(template, context)` - Return placeholders whose rendered value against ``context`` is empty.
- `alias_with_trailing_args` (function, `cli/aliases.py:77`) `def alias_with_trailing_args(expanded, original)` - Append the operator's trailing arguments to an expanded alias.
- `load_aliases` (function, `cli/aliases.py:100`) `def load_aliases(payload, path, lazy)` - Return the cmd2 alias map.
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
- `PayloadProvider` (class, `cli/cli_enhancements.py:40`) `class PayloadProvider(Protocol)` - Read-only view onto ``payload.json`` style configuration.
- `get` (method, `cli/cli_enhancements.py:43`) `def get(self, key, default)`
- `keys` (method, `cli/cli_enhancements.py:44`) `def keys(self)`
- `CommandLister` (class, `cli/cli_enhancements.py:47`) `class CommandLister(Protocol)` - Source of command metadata for indexing / fuzzy matching.
- `commands` (method, `cli/cli_enhancements.py:50`) `def commands(self)`
- `TerminalIO` (class, `cli/cli_enhancements.py:53`) `class TerminalIO(Protocol)` - Minimal duck-typed prompt/print pair so tests can fake it.
- `prompt` (method, `cli/cli_enhancements.py:56`) `def prompt(self, message, default)`
- `emit` (method, `cli/cli_enhancements.py:57`) `def emit(self, line)`
- `CommandInfo` (class, `cli/cli_enhancements.py:61`) `class CommandInfo` - Lightweight description of a shell command.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 508
- Cross-boundary resolved imports (EXTRACTED): 580

## Connections

- [EXTRACTED] depends_on community 4 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 5 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 1 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 10 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/param_registry.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `modules/harness.py` via `subprocess` (5 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `utils.py` -> `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `utils.py`

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `tests/test_gym_ms2_cli.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules: lazyown changed?
- Should modules: lazyown be split, given cohesion 0.36?

## Sources

- `cli/aliases.py`
- `cli/auto_crypto.py`
- `cli/cli_enhancements.py`
- `cli/commands/audit.py`
- `cli/commands/containers.py`
- `cli/commands/diagnostics.py`
- `cli/commands/lazyloop.py`
- `cli/commands/params_ops.py`
- `cli/commands/persist_migrated.py`
- `cli/commands/purple_team.py`
- `cli/commands/recon_migrated.py`
- `cli/commands/redteam_gym.py`
- `cli/commands/security.py`
- `cli/engagement_hooks.py`
- `cli/headless.py`
- `cli/lazy_orchestrator.py`
- `cli/orchestrator_assets_tabs.py`
- `cli/purple_tui.py`
- `cli/surface_tui.py`
- `cli/tui_forms.py`
- *... and 84 more*
