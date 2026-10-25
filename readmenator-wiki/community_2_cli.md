# cli

*Community 2 | 126 files | cohesion 0.55*

## Definition

This community groups 126 file(s) rooted at `tests` with dominant language py (cohesion 0.55). Central symbols: `AddonCatalog`, `AddonEntry`, `Alert`, `App`, `AuditConfig`, `AutoCryptoConfig`, `AutoCryptoEngine`, `AutoSuggestEngine`. Core file: `tests/test_command_palette.py` (238 symbols). Documented purpose: LazyOwn CLI infrastructure.  Tier 2 introduces a declarative, modular layer above ``lazyown.py``:  - ``cli/aliases.yaml`` and :func:`cli.aliases.load_aliases` p.

## Files

### `tests` (51 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_crypto.py` | py | testing | 22 | yes |
| `tests/test_autosuggest.py` | py | testing | 41 | yes |
| `tests/test_c2_agent.py` | py | testing | 20 | yes |

### `cli` (45 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/__init__.py` | py | utility | 0 | yes |
| `cli/auto_crypto.py` | py | utility | 13 | yes |
| `cli/autosuggest.py` | py | utility | 27 | yes |

### `skills/hermes-lazyown` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |

### `core` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/command_bridge.py` | py | utility | 9 | yes |
| `core/console.py` | py | utility | 11 | yes |

### `cli/commands` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/cli_auth.py` | py | utility | 5 | yes |

### `modules` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/cli_auth.py` | py | utility | 18 | yes |
| `modules/kill_chain_viz.py` | py | utility | 5 | yes |

### `poc_tui` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |
| `poc_tui/app.py` | py | utility | 47 | yes |

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

*... and 106 more files in this community.*


## Key Symbols

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
- `suggest` (method, `cli/autosuggest.py:162`) `def suggest(self, context)` - Return the first unseen adjacency, or phase fallback, or ``None``.
- `GraphProvider` (class, `cli/autosuggest.py:189`) `class GraphProvider` - Provider backed by the graphify knowledge-graph advisor.
- `__init__` (method, `cli/autosuggest.py:197`) `def __init__(self, advisor)` - Configure the provider.
- `suggest` (method, `cli/autosuggest.py:221`) `def suggest(self, context)` - Query the advisor and adapt the top result to a :class:`Suggestion`.
- `AutoSuggestEngine` (class, `cli/autosuggest.py:245`) `class AutoSuggestEngine` - Stateful holder for the active ghost-text suggestion.
- `__init__` (method, `cli/autosuggest.py:254`) `def __init__(self, provider)` - Store the provider and enabled flag.
- `enabled` (method, `cli/autosuggest.py:270`) `def enabled(self)` - Whether the engine refreshes suggestions on each command.
- `set_enabled` (method, `cli/autosuggest.py:274`) `def set_enabled(self, value)` - Toggle the engine without losing the provider chain.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 507
- Cross-boundary resolved imports (EXTRACTED): 330

## Connections

- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 2 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/commands/containers.py.
- [EXTRACTED] depends_on community 10 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `modules/cli_auth.py`
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/auto_crypto.py:272` `_load_or_create_salt` `fd`: Result of allocator stored in `fd` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `cli/commands/recon.py:609` `_run_single_search` `_s`: Result of allocator stored in `_s` is never checked against NULL.

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `lazy_sentinel4.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` be broken with an interface?
- What would break if the most connected file in cli changed?
- Should cli be split, given cohesion 0.55?

## Sources

- `cli/__init__.py`
- `cli/auto_crypto.py`
- `cli/autosuggest.py`
- `cli/chain_mode.py`
- `cli/command_chain.py`
- `cli/command_explorer.py`
- `cli/command_form.py`
- `cli/commands/__init__.py`
- `cli/commands/cli_auth.py`
- `cli/commands/help_ui.py`
- `cli/commands/orchestration.py`
- `cli/commands/recon.py`
- `cli/config_status.py`
- `cli/contextual_help.py`
- `cli/dashboard_layout.py`
- `cli/dashboard_tui.py`
- `cli/doctor.py`
- `cli/engagement_hooks.py`
- `cli/exploit_advisor.py`
- `cli/exploration.py`
- *... and 106 more*
