# cli

*Community 3 | 138 files | cohesion 0.58*

## Definition

This community groups 138 file(s) rooted at `tests` with dominant language py (cohesion 0.58). Central symbols: `AddonCatalog`, `AddonEntry`, `AddonHotReloader`, `AddonInfo`, `AddonRegistry`, `Alert`, `AliasResolver`, `App`. Core file: `tests/test_command_palette.py` (238 symbols). Documented purpose: LazyOwn CLI infrastructure.  Tier 2 introduces a declarative, modular layer above ``lazyown.py``:  - ``cli/aliases.yaml`` and :func:`cli.aliases.load_aliases` p.

## Files

### `tests` (63 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_crypto.py` | py | testing | 22 | yes |
| `tests/test_autosuggest.py` | py | testing | 41 | yes |
| `tests/test_c2_agent.py` | py | testing | 20 | yes |

### `cli` (50 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/__init__.py` | py | utility | 0 | yes |
| `cli/aliases.py` | py | utility | 8 | yes |
| `cli/auto_crypto.py` | py | utility | 13 | yes |

### `cli/commands` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/_dormancy.py` | py | utility | 2 | yes |
| `cli/commands/audit.py` | py | utility | 16 | yes |

### `core` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/command_bridge.py` | py | utility | 9 | yes |
| `core/console.py` | py | utility | 11 | yes |
| `core/error_advice.py` | py | utility | 5 | yes |

### `modules` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/cli_auth.py` | py | utility | 18 | yes |
| `modules/kill_chain_viz.py` | py | utility | 5 | yes |
| `modules/killchain.py` | py | utility | 25 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazy_sentinel4.py` | py | utility | 47 | no |
| `lazyown.py` | py | utility | 124 | yes |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/command_audit.py` | py | utility | 4 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/unified_orchestrator.py` | py | utility | 59 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/showdown-2.1.0.min.js` | js | utility | 5 | yes |

*... and 118 more files in this community.*


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
- `SuggestionContext` (class, `cli/autosuggest.py:50`) `class SuggestionContext` - Inputs available to every suggestion provider.
- `Suggestion` (class, `cli/autosuggest.py:71`) `class Suggestion` - One next-command suggestion with its rationale.
- `SuggestionProvider` (class, `cli/autosuggest.py:92`) `class SuggestionProvider(Protocol)` - Provider contract: examine context, return one suggestion or ``None``.
- `suggest` (method, `cli/autosuggest.py:95`) `def suggest(self, context)`
- `CompositeProvider` (class, `cli/autosuggest.py:98`) `class CompositeProvider` - Aggregator that returns the highest-scoring suggestion across providers.
- `__init__` (method, `cli/autosuggest.py:105`) `def __init__(self, providers)` - Store the provider chain.
- `suggest` (method, `cli/autosuggest.py:115`) `def suggest(self, context)` - Return the best suggestion across the chain, or ``None``.
- `KillChainProvider` (class, `cli/autosuggest.py:134`) `class KillChainProvider` - Provider backed by the static kill-chain adjacency map.
- `__init__` (method, `cli/autosuggest.py:143`) `def __init__(self, chain, phase_priority)` - Configure the provider.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 629
- Cross-boundary resolved imports (EXTRACTED): 357

## Connections

- [EXTRACTED] depends_on community 3 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.
- [EXTRACTED] depends_on community 3 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/crypto.py.
- [EXTRACTED] depends_on community 9 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/aliases.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `modules/cli_auth.py`
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/auto_crypto.py:272` `_load_or_create_salt` `fd`: Result of allocator stored in `fd` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `cli/commands/misc_migrated.py:333` `do_suggest_next` `_idx`: Result of allocator stored in `_idx` is never checked against NULL.

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `lazy_sentinel4.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` be broken with an interface?
- What would break if the most connected file in cli changed?
- Should cli be split, given cohesion 0.58?

## Sources

- `cli/__init__.py`
- `cli/aliases.py`
- `cli/auto_crypto.py`
- `cli/autosuggest.py`
- `cli/chain_mode.py`
- `cli/cli_enhancements.py`
- `cli/command_chain.py`
- `cli/command_explorer.py`
- `cli/command_form.py`
- `cli/commands/__init__.py`
- `cli/commands/_dormancy.py`
- `cli/commands/audit.py`
- `cli/commands/diagnostics.py`
- `cli/commands/help_ui.py`
- `cli/commands/misc_migrated.py`
- `cli/commands/orchestration.py`
- `cli/commands/recon.py`
- `cli/config_status.py`
- `cli/contextual_help.py`
- `cli/dashboard_layout.py`
- *... and 118 more*
