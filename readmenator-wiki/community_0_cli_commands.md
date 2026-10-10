# cli/commands

*Community 0 | 161 files | cohesion 0.62*

## Definition

This community groups 161 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.62). Central symbols: `A`, `AESdecrypt`, `AESencrypt`, `AddonInfo`, `AddonRegistry`, `AntiForensicsCommandSet`, `AppLockerBypassCommandSet`, `As`. Core file: `static/js/html2pdf.bundle.min.js` (695 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: Este archivo contiene la.

## Files

### `cli/commands` (54 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/_base.py` | py | utility | 7 | yes |
| `cli/commands/_dormancy.py` | py | utility | 2 | yes |

### `tests` (39 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_api_key_resolution.py` | py | testing | 9 | yes |
| `tests/test_autosuggest.py` | py | testing | 41 | yes |

### `modules` (29 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_purple.py` | py | utility | 40 | yes |
| `modules/beacon_config_builder.py` | py | infrastructure | 14 | yes |

### `cli` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/aliases.py` | py | utility | 7 | yes |
| `cli/assign.py` | py | utility | 1 | yes |

### `static/js` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |

### `core` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/config.py` | py | infrastructure | 17 | yes |
| `core/credential_vault.py` | py | utility | 8 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `banner.py` | py | utility | 3 | yes |
| `utils.py` | py | utility | 121 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazysmbrelay.py` | py | utility | 7 | no |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/core_smoke.py` | py | utility | 4 | yes |

*... and 141 more files in this community.*


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
- `apply_assign` (function, `cli/assign.py:36`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
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
- `current` (method, `cli/autosuggest.py:284`) `def current(self)` - Return the suggestion last computed, or ``None`` when cleared.
- `clear` (method, `cli/autosuggest.py:288`) `def clear(self)` - Drop the active suggestion (called after accept or abort).

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 697
- Cross-boundary resolved imports (EXTRACTED): 387

## Connections

- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 0 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/crypto.py.
- [EXTRACTED] depends_on community 0 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/bof_registry.py imports modules/bof_registry.py.
- [EXTRACTED] depends_on community 11 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/cloud_attacks.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 9 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/dns_exfil.py imports modules/backdoor/server.c.
- [EXTRACTED] depends_on community 6 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/exploit_migrated.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/banner_config.py` via `subprocess` (0 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/console.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazysmbrelay.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- Is the dangerous import `subprocess` in `cli/banner_config.py` still required, or can it be isolated?
- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.62?

## Sources

- `banner.py`
- `cli/aliases.py`
- `cli/assign.py`
- `cli/autosuggest.py`
- `cli/banner_config.py`
- `cli/commands/__init__.py`
- `cli/commands/_base.py`
- `cli/commands/_dormancy.py`
- `cli/commands/anti_forensics.py`
- `cli/commands/applocker_bypass.py`
- `cli/commands/bitm.py`
- `cli/commands/bof_registry.py`
- `cli/commands/c2_profile.py`
- `cli/commands/catalog.py`
- `cli/commands/cicd.py`
- `cli/commands/cloud.py`
- `cli/commands/command_and_control.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/commands/cred.py`
- `cli/commands/cred_migrated.py`
- *... and 141 more*
