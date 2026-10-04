# cli/commands

*Community 0 | 176 files | cohesion 0.58*

## Definition

This community groups 176 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.58). Central symbols: `AESdecrypt`, `AESencrypt`, `AddonCatalog`, `AddonEntry`, `AiCommandSet`, `AntiForensicsCommandSet`, `AppLockerBypassCommandSet`, `AuditConfig`. Core file: `lazyown.py` (123 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: Este archivo contiene la.

## Files

### `cli/commands` (56 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/_base.py` | py | utility | 7 | yes |
| `cli/commands/_dormancy.py` | py | data_access | 2 | yes |

### `tests` (42 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_api_key_resolution.py` | py | testing | 9 | yes |
| `tests/test_autosuggest.py` | py | testing | 41 | yes |

### `modules` (31 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/bitm_engine.py` | py | utility | 18 | yes |
| `modules/bof_registry.py` | py | utility | 43 | yes |

### `cli` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/autosuggest.py` | py | utility | 27 | yes |
| `cli/banner_config.py` | py | infrastructure | 120 | yes |

### `.` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `banner.py` | py | utility | 3 | yes |
| `discord_c2.py` | py | infrastructure | 21 | no |

### `core` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/command_bridge.py` | py | utility | 9 | yes |
| `core/crypto.py` | py | utility | 7 | yes |

### `skills` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_control.py` | py | utility | 27 | yes |
| `skills/lazyown_claudemd.py` | py | utility | 8 | yes |

### `contrib/legacy` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |

### `scripts/devtools` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/command_audit.py` | py | infrastructure | 4 | yes |

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/phishing.py` | py | presentation | 7 | yes |

### `lazyc2/extensions` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/short_urls.py` | py | infrastructure | 5 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

*... and 156 more files in this community.*


## Key Symbols

- `image_to_bash` (function, `banner.py:25`) `def image_to_bash(image_path, image_res)`
- `list_png_files` (function, `banner.py:47`) `def list_png_files()`
- `main` (function, `banner.py:56`) `def main()`
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
- `refresh` (method, `cli/autosuggest.py:292`) `def refresh(self, context)` - Recompute the suggestion from the provider chain.
- `accept` (method, `cli/autosuggest.py:309`) `def accept(self)` - Return the active command string and clear the suggestion.
- `display_text` (method, `cli/autosuggest.py:317`) `def display_text(self)` - Return the ANSI-coloured ghost-text fragment for legacy callers.
- `_truncate` (method, `cli/autosuggest.py:335`) `def _truncate(value, max_len)` - Return ``value`` shortened to ``max_len`` characters with an ellipsis.
- `format_hint_line` (method, `cli/autosuggest.py:342`) `def format_hint_line(suggestion)` - Build the dim hint string surfaced after each command.
- `render_hint_line` (method, `cli/autosuggest.py:375`) `def render_hint_line(engine)` - Print one dim hint line for the engine's active suggestion.
- `_hint_console` (method, `cli/autosuggest.py:411`) `def _hint_console()` - Return a lazily-initialised :class:`rich.console.Console`.
- `build_default_engine` (method, `cli/autosuggest.py:427`) `def build_default_engine(advisor, chain, phase_priority)` - Wire the canonical provider chain used by the cmd2 shell.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 559
- Cross-boundary resolved imports (EXTRACTED): 436

## Connections

- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/registry.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/crypto.py.
- [EXTRACTED] depends_on community 0 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 6 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports modules/planner.py.
- [EXTRACTED] depends_on community 7 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/cloud_attacks.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/containers.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/misc_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/orchestration.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 9 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/payload_arsenal.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/banner_config.py` via `subprocess` (0 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/console.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)

## Open Questions

- Why do 6 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- Is the dangerous import `subprocess` in `cli/banner_config.py` still required, or can it be isolated?
- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.58?

## Sources

- `banner.py`
- `cli/autosuggest.py`
- `cli/banner_config.py`
- `cli/chain_mode.py`
- `cli/command_chain.py`
- `cli/commands/_base.py`
- `cli/commands/_dormancy.py`
- `cli/commands/ai.py`
- `cli/commands/anti_forensics.py`
- `cli/commands/applocker_bypass.py`
- `cli/commands/bitm.py`
- `cli/commands/bof_registry.py`
- `cli/commands/c2_profile.py`
- `cli/commands/caldera.py`
- `cli/commands/campaign.py`
- `cli/commands/catalog.py`
- `cli/commands/cicd.py`
- `cli/commands/cli_auth.py`
- `cli/commands/cloud.py`
- `cli/commands/collaboration.py`
- *... and 156 more*
