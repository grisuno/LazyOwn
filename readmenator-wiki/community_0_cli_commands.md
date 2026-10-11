# cli/commands

*Community 0 | 118 files | cohesion 0.56*

## Definition

This community groups 118 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.56). Central symbols: `AddonHotReloader`, `AddonInfo`, `AddonRegistry`, `AliasResolver`, `AntiForensicsCommandSet`, `AppLockerBypassCommandSet`, `AuditCommandSet`, `BitMCommandSet`. Core file: `utils.py` (121 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: Este archivo contiene la.

## Files

### `cli/commands` (47 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/_base.py` | py | utility | 7 | yes |
| `cli/commands/_dormancy.py` | py | utility | 2 | yes |
| `cli/commands/anti_forensics.py` | py | utility | 7 | yes |

### `tests` (28 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_api_key_resolution.py` | py | testing | 9 | yes |
| `tests/test_bdd_infra_range_report.py` | py | testing | 5 | yes |
| `tests/test_campaign_import_safety.py` | py | testing | 14 | yes |

### `modules` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/bitm_engine.py` | py | utility | 18 | yes |
| `modules/c2_builder.py` | py | infrastructure | 21 | yes |
| `modules/categories.py` | py | utility | 0 | yes |

### `cli` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/aliases.py` | py | utility | 7 | yes |
| `cli/cli_enhancements.py` | py | utility | 69 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/hardening.py` | py | utility | 16 | yes |
| `core/host_policy.py` | py | business_logic | 3 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazyhttpreverseshell.py` | py | utility | 10 | no |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `banner.py` | py | utility | 3 | yes |
| `utils.py` | py | utility | 121 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/core_smoke.py` | py | utility | 4 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 3 | yes |

*... and 98 more files in this community.*


## Key Symbols

- `image_to_bash` (function, `banner.py:26`) `def image_to_bash(image_path, image_res)`
- `list_png_files` (function, `banner.py:50`) `def list_png_files()`
- `main` (function, `banner.py:60`) `def main()`
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 374
- Cross-boundary resolved imports (EXTRACTED): 257

## Connections

- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 0 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/aliases.py imports core/config.py.
- [EXTRACTED] depends_on community 13 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/cli_auth.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 14 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/cloud_attacks.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/listener_manager.py.
- [EXTRACTED] depends_on community 9 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/host_policy.py` via `subprocess` (5 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_subprocess.py` via `subprocess` (5 hops)
- [taint high] `cli/banner_config.py` -> `modules/backdoor/server.c` via `subprocess` (5 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_security_hardening_v5.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_security_hardening_v5.py` (testing) -> `lazyc2/blueprints/api.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `banner.py:29` `image_to_bash` `img`: Result of allocator stored in `img` is never checked against NULL.

## Open Questions

- Why do 5 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.56?

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
- `cli/commands/command_and_control_migrated.py`
- `cli/commands/cred.py`
- `cli/commands/cred_migrated.py`
- `cli/commands/daemon_ctl.py`
- `cli/commands/demo.py`
- `cli/commands/diagnostics.py`
- *... and 98 more*
