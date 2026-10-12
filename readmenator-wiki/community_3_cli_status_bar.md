# cli: status_bar

*Community 3 | 101 files | cohesion 0.53*

## Definition

This community groups 101 file(s) rooted at `cli` with dominant language py (cohesion 0.53). Central symbols: `AESdecrypt`, `AESencrypt`, `AddonCatalog`, `AddonEntry`, `AuthError`, `AutoSuggestEngine`, `BackendAdapterSpec`, `BackendRegistry`. Core file: `tests/test_command_palette.py` (238 symbols). Documented purpose: LazyOwn CLI infrastructure.  Tier 2 introduces a declarative, modular layer above ``lazyown.py``:  - ``cli/aliases.yaml`` and :func:`cli.aliases.load_aliases` p.

## Files

### `cli` (38 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/__init__.py` | py | utility | 0 | yes |
| `cli/autosuggest.py` | py | utility | 27 | yes |
| `cli/chain_mode.py` | py | utility | 23 | yes |
| `cli/command_chain.py` | py | utility | 25 | yes |

### `tests` (37 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_autosuggest.py` | py | testing | 41 | yes |
| `tests/test_chain_mode.py` | py | testing | 28 | yes |
| `tests/test_command_chain.py` | py | testing | 24 | yes |

### `core` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/__init__.py` | py | utility | 0 | yes |
| `core/console.py` | py | utility | 11 | yes |
| `core/crypto.py` | py | utility | 7 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/containers.py` | py | infrastructure | 7 | yes |
| `cli/commands/help_ui.py` | py | presentation | 16 | yes |

### `poc_tui` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |
| `poc_tui/app.py` | py | utility | 47 | yes |
| `poc_tui/run.py` | py | utility | 1 | yes |

### `modules` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_purple.py` | py | utility | 40 | yes |
| `modules/lazyk8s.py` | py | utility | 32 | yes |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/unified_orchestrator.py` | py | utility | 59 | yes |

*... and 81 more files in this community.*


## Key Symbols

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
- `_truncate` (function, `cli/autosuggest.py:335`) `def _truncate(value, max_len)` - Return ``value`` shortened to ``max_len`` characters with an ellipsis.
- `format_hint_line` (function, `cli/autosuggest.py:342`) `def format_hint_line(suggestion)` - Build the dim hint string surfaced after each command.
- `render_hint_line` (function, `cli/autosuggest.py:375`) `def render_hint_line(engine)` - Print one dim hint line for the engine's active suggestion.
- `_hint_console` (function, `cli/autosuggest.py:411`) `def _hint_console()` - Return a lazily-initialised :class:`rich.console.Console`.
- `build_default_engine` (function, `cli/autosuggest.py:427`) `def build_default_engine(advisor, chain, phase_priority)` - Wire the canonical provider chain used by the cmd2 shell.
- `_ChainEscExit` (class, `cli/chain_mode.py:73`) `class _ChainEscExit(Exception)` - Internal signal: the operator pressed ESC at the chain prompt.
- `_read_line_unix` (function, `cli/chain_mode.py:77`) `def _read_line_unix(prompt)` - Read one line in raw TTY mode, honouring ESC, Ctrl+C and backspace.
- `_read_line_windows` (function, `cli/chain_mode.py:136`) `def _read_line_windows(prompt)` - Read one line on Windows, honouring ESC, Ctrl+C and backspace.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 335
- Cross-boundary resolved imports (EXTRACTED): 210

## Connections

- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 0 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/crypto.py.
- [EXTRACTED] depends_on community 3 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/assign.py.
- [EXTRACTED] depends_on community 3 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/ops_commands.py.
- [EXTRACTED] depends_on community 3 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/console.py` via `subprocess` (5 hops)
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/commands/recon.py:609` `_run_single_search` `_s`: Result of allocator stored in `_s` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `cli/lazynmap_post.py:244` `_emit_event` `fd`: Result of allocator stored in `fd` is never checked against NULL.

## Open Questions

- What would break if the most connected file in cli: status_bar changed?
- Should cli: status_bar be split, given cohesion 0.53?

## Sources

- `cli/__init__.py`
- `cli/autosuggest.py`
- `cli/chain_mode.py`
- `cli/command_chain.py`
- `cli/command_explorer.py`
- `cli/command_form.py`
- `cli/commands/__init__.py`
- `cli/commands/containers.py`
- `cli/commands/help_ui.py`
- `cli/commands/orchestration.py`
- `cli/commands/purple_team.py`
- `cli/commands/recon.py`
- `cli/config_status.py`
- `cli/contextual_help.py`
- `cli/doctor.py`
- `cli/exploit_advisor.py`
- `cli/exploration.py`
- `cli/exploration_view.py`
- `cli/graph_overlay.py`
- `cli/lazynmap_post.py`
- *... and 81 more*
