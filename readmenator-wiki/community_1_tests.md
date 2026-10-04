# tests

*Community 1 | 122 files | cohesion 0.50*

## Definition

This community groups 122 file(s) rooted at `tests` with dominant language py (cohesion 0.50). Central symbols: `AIModel`, `ASTToolExtractor`, `AddonHotReloader`, `AddonInfo`, `AddonRegistry`, `AgentRunner`, `AgentTool`, `AliasResolver`. Core file: `cli/cli_enhancements.py` (69 symbols). Documented purpose: LazyOwn CLI infrastructure.  Tier 2 introduces a declarative, modular layer above ``lazyown.py``:  - ``cli/aliases.yaml`` and :func:`cli.aliases.load_aliases` p.

## Files

### `tests` (35 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_bdd_infra_range_report.py` | py | testing | 5 | yes |
| `tests/test_beacon_config_builder.py` | py | testing | 16 | yes |

### `cli` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/__init__.py` | py | utility | 0 | yes |
| `cli/aliases.py` | py | utility | 7 | yes |
| `cli/cli_enhancements.py` | py | utility | 69 | yes |
| `cli/command_explorer.py` | py | utility | 7 | yes |

### `modules` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 35 | yes |
| `modules/ai_model.py` | py | business_logic | 32 | yes |
| `modules/apt_playbooks.py` | py | utility | 15 | yes |

### `core` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/__init__.py` | py | utility | 0 | yes |
| `core/config.py` | py | infrastructure | 17 | yes |
| `core/console.py` | py | utility | 8 | yes |

### `cli/commands` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/audit.py` | py | infrastructure | 13 | yes |
| `cli/commands/command_and_control_migrated.py` | py | utility | 26 | yes |
| `cli/commands/diagnostics.py` | py | infrastructure | 3 | yes |

### `contrib/legacy` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazybinenc.py` | py | utility | 2 | no |
| `contrib/legacy/lazyllmchat.py` | py | utility | 30 | no |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

*... and 102 more files in this community.*


## Key Symbols

- `_SafeFormatDict` (class, `cli/aliases.py:29`) `class _SafeFormatDict(dict)` - ``str.format_map`` source that returns ``""`` for missing/None values.
- `__missing__` (method, `cli/aliases.py:32`) `def __missing__(self, key)`
- `__getitem__` (method, `cli/aliases.py:35`) `def __getitem__(self, key)`
- `_substitute` (method, `cli/aliases.py:42`) `def _substitute(template, payload)` - Render ``template`` against ``payload`` placeholders.
- `template_placeholders` (method, `cli/aliases.py:56`) `def template_placeholders(template)` - Return the ``{name}`` placeholders referenced by ``template``.
- `empty_placeholders` (method, `cli/aliases.py:72`) `def empty_placeholders(template, context)` - Return placeholders whose rendered value against ``context`` is empty.
- `load_aliases` (method, `cli/aliases.py:77`) `def load_aliases(payload, path, lazy)` - Return the cmd2 alias map.
- `PayloadProvider` (class, `cli/cli_enhancements.py:40`) `class PayloadProvider(Protocol)` - Read-only view onto ``payload.json`` style configuration.
- `get` (method, `cli/cli_enhancements.py:43`) `def get(self, key, default)`
- `keys` (method, `cli/cli_enhancements.py:44`) `def keys(self)`
- `CommandLister` (class, `cli/cli_enhancements.py:47`) `class CommandLister(Protocol)` - Source of command metadata for indexing / fuzzy matching.
- `commands` (method, `cli/cli_enhancements.py:50`) `def commands(self)`
- `TerminalIO` (class, `cli/cli_enhancements.py:53`) `class TerminalIO(Protocol)` - Minimal duck-typed prompt/print pair so tests can fake it.
- `prompt` (method, `cli/cli_enhancements.py:56`) `def prompt(self, message, default)`
- `emit` (method, `cli/cli_enhancements.py:57`) `def emit(self, line)`
- `CommandInfo` (class, `cli/cli_enhancements.py:61`) `class CommandInfo` - Lightweight description of a shell command.
- `FuzzyMatch` (class, `cli/cli_enhancements.py:75`) `class FuzzyMatch` - A scored fuzzy match against a CommandInfo.
- `FuzzyCommandIndex` (class, `cli/cli_enhancements.py:83`) `class FuzzyCommandIndex` - Search a command catalogue with token-aware fuzzy matching.
- `__init__` (method, `cli/cli_enhancements.py:91`) `def __init__(self, source)`
- `search` (method, `cli/cli_enhancements.py:94`) `def search(self, query, limit)` - Return the top ``limit`` matches ordered by descending score.
- `_score` (method, `cli/cli_enhancements.py:109`) `def _score(info, q)`
- `CompletionResult` (class, `cli/cli_enhancements.py:138`) `class CompletionResult` - A single tab-completion suggestion.
- `PayloadAwareCompleter` (class, `cli/cli_enhancements.py:145`) `class PayloadAwareCompleter` - Suggest values from ``payload.json`` for context-sensitive arguments.
- `__init__` (method, `cli/cli_enhancements.py:164`) `def __init__(self, payload, addon_lister, plugin_lister, credential_lister)`
- `complete` (method, `cli/cli_enhancements.py:176`) `def complete(self, command, partial)` - Return suggestions for ``partial`` given the leading ``command``.
- `_suggest_payload_keys` (method, `cli/cli_enhancements.py:196`) `def _suggest_payload_keys(self, partial)`
- `_suggest_targets` (method, `cli/cli_enhancements.py:202`) `def _suggest_targets(self, partial)`
- `_suggest_wordlist_keys` (method, `cli/cli_enhancements.py:213`) `def _suggest_wordlist_keys(self, partial)`
- `_suggest_addons` (method, `cli/cli_enhancements.py:221`) `def _suggest_addons(self, partial)`
- `_suggest_plugins` (method, `cli/cli_enhancements.py:224`) `def _suggest_plugins(self, partial)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 376
- Cross-boundary resolved imports (EXTRACTED): 283

## Connections

- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/registry.py.
- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/palette.py.
- [EXTRACTED] depends_on community 8 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/mcp_bridge.py imports core/config.py.
- [EXTRACTED] depends_on community 1 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/session_resumer.py imports core/logging.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/console.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `modules/ai_model.py` via `subprocess` (5 hops)
- [cycle] `cli/engagement_hooks.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py`
- [layer strict] `tests/test_bdd_infra_range_report.py` (testing) -> `modules/c2_builder.py` (presentation)
- [layer strict] `tests/test_core_modules.py` (presentation) -> `modules/config_store.py` (data_access)
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- Can the cycle `cli/engagement_hooks.py` -> `modules/cli_auth.py` be broken with an interface?
- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 0.50?

## Sources

- `cli/__init__.py`
- `cli/aliases.py`
- `cli/cli_enhancements.py`
- `cli/command_explorer.py`
- `cli/commands/audit.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/commands/diagnostics.py`
- `cli/commands/exploitgym.py`
- `cli/commands/help_ui.py`
- `cli/commands/lab.py`
- `cli/commands/opsec_cleanup.py`
- `cli/commands/purple_team.py`
- `cli/commands/recon_migrated.py`
- `cli/commands/security.py`
- `cli/commands/ux.py`
- `cli/config_history.py`
- `cli/config_status.py`
- `cli/contextual_help.py`
- `cli/doctor.py`
- `cli/engagement_hooks.py`
- *... and 102 more*
