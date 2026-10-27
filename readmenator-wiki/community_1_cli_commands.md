# cli/commands

*Community 1 | 128 files | cohesion 0.50*

## Definition

This community groups 128 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.50). Central symbols: `AESdecrypt`, `AESencrypt`, `AddonHotReloader`, `AddonInfo`, `AddonRegistry`, `AddonUpdateResult`, `AliasResolver`, `AntiForensicsCommandSet`. Core file: `utils.py` (126 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: AGPL v3  Descripción: Este archivo contiene l.

## Files

### `cli/commands` (52 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/_base.py` | py | utility | 7 | yes |
| `cli/commands/_dormancy.py` | py | utility | 2 | yes |
| `cli/commands/anti_forensics.py` | py | utility | 7 | yes |

### `tests` (32 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_updater.py` | py | testing | 13 | yes |
| `tests/test_api_key_resolution.py` | py | testing | 9 | yes |
| `tests/test_backdoor_random.py` | py | testing | 5 | yes |

### `modules` (22 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/addon_updater.py` | py | utility | 10 | yes |
| `modules/bitm_engine.py` | py | utility | 18 | yes |
| `modules/categories.py` | py | utility | 0 | yes |

### `core` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/crypto.py` | py | utility | 7 | yes |
| `core/hardening.py` | py | utility | 34 | yes |
| `core/host_policy.py` | py | business_logic | 3 | yes |

### `cli` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/aliases.py` | py | utility | 8 | yes |
| `cli/cli_enhancements.py` | py | utility | 69 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazyhttpreverseshell.py` | py | utility | 10 | no |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `banner.py` | py | utility | 3 | yes |
| `utils.py` | py | utility | 126 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/core_smoke.py` | py | utility | 4 | yes |

*... and 108 more files in this community.*


## Key Symbols

- `image_to_bash` (function, `banner.py:26`) `def image_to_bash(image_path, image_res)`
- `list_png_files` (function, `banner.py:50`) `def list_png_files()`
- `main` (function, `banner.py:60`) `def main()`
- `_SafeFormatDict` (class, `cli/aliases.py:29`) `class _SafeFormatDict(dict)` - ``str.format_map`` source that returns ``""`` for missing/None values.
- `__missing__` (method, `cli/aliases.py:32`) `def __missing__(self, key)`
- `__getitem__` (method, `cli/aliases.py:35`) `def __getitem__(self, key)`
- `_substitute` (function, `cli/aliases.py:42`) `def _substitute(template, payload)` - Render ``template`` against ``payload`` placeholders.
- `template_placeholders` (function, `cli/aliases.py:56`) `def template_placeholders(template)` - Return the ``{name}`` placeholders referenced by ``template``.
- `empty_placeholders` (function, `cli/aliases.py:72`) `def empty_placeholders(template, context)` - Return placeholders whose rendered value against ``context`` is empty.
- `alias_with_trailing_args` (function, `cli/aliases.py:77`) `def alias_with_trailing_args(expanded, original)` - Append the operator's trailing arguments to an expanded alias.
- `load_aliases` (function, `cli/aliases.py:100`) `def load_aliases(payload, path, lazy)` - Return the cmd2 alias map.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 402
- Cross-boundary resolved imports (EXTRACTED): 365

## Connections

- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.
- [EXTRACTED] depends_on community 13 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 9 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 5 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 10 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/c2_session.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/campaign.py imports modules/world_model.py.
- [EXTRACTED] depends_on community 14 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/cloud_attacks.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `utils.py` -> `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `utils.py`
- [cycle] `utils.py` -> `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_security_hardening_v5.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.50?

## Sources

- `banner.py`
- `cli/aliases.py`
- `cli/cli_enhancements.py`
- `cli/commands/_base.py`
- `cli/commands/_dormancy.py`
- `cli/commands/anti_forensics.py`
- `cli/commands/applocker_bypass.py`
- `cli/commands/audit.py`
- `cli/commands/bitm.py`
- `cli/commands/campaign.py`
- `cli/commands/catalog.py`
- `cli/commands/cicd.py`
- `cli/commands/cloud.py`
- `cli/commands/command_and_control.py`
- `cli/commands/cred.py`
- `cli/commands/cred_migrated.py`
- `cli/commands/crystal_ball.py`
- `cli/commands/demo.py`
- `cli/commands/diagnostics.py`
- `cli/commands/dns_exfil.py`
- *... and 108 more*
