# cli

*Community 3 | 126 files | cohesion 0.55*

## Definition

This community groups 126 file(s) rooted at `tests` with dominant language py (cohesion 0.55). Central symbols: `A`, `AddonInfo`, `AddonRegistry`, `As`, `AuthError`, `AutoSuggestEngine`, `B`, `BUFFER`. Core file: `static/js/html2pdf.bundle.min.js` (738 symbols). Documented purpose: LazyOwn CLI infrastructure.  Tier 2 introduces a declarative, modular layer above ``lazyown.py``:  - ``cli/aliases.yaml`` and :func:`cli.aliases.load_aliases` p.

## Files

### `tests` (44 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_crypto.py` | py | testing | 22 | yes |
| `tests/test_autosuggest.py` | py | testing | 41 | yes |
| `tests/test_chain_mode.py` | py | testing | 28 | yes |

### `cli` (36 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/__init__.py` | py | utility | 0 | yes |
| `cli/assign.py` | py | utility | 1 | yes |

### `static/js` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/3d-force-graph-1.73.4.min.js` | js | utility | 176 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |

### `core` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/__init__.py` | py | utility | 0 | yes |
| `core/console.py` | py | utility | 11 | yes |

### `cli/commands` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/_dormancy.py` | py | utility | 2 | yes |

### `poc_tui` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |
| `poc_tui/app.py` | py | utility | 47 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/exp.c` | c | utility | 58 | yes |
| `modules/lazy_verify.py` | py | utility | 8 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `gyms/docker/php2shell/src` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `gyms/docker/php2shell/src/info.php` | php | utility | 0 | no |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/state.py` | py | utility | 0 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `static/hexabot` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/hexabot/hexabot-spinner.js` | js | utility | 24 | no |

*... and 106 more files in this community.*


## Key Symbols

- `apply_assign` (function, `cli/assign.py:42`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 606
- Cross-boundary resolved imports (EXTRACTED): 324

## Connections

- [EXTRACTED] depends_on community 3 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/command_chain.py imports cli/reactive_hints.py.
- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/commands/containers.py.
- [EXTRACTED] depends_on community 6 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/dependencies.py` via `subprocess` (5 hops)
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/commands/misc_migrated.py:333` `do_suggest_next` `_idx`: Result of allocator stored in `_idx` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `cli/commands/recon.py:603` `_run_single_search` `_s`: Result of allocator stored in `_s` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:371` `set_stable_table_and_set` `seq`: `seq` assigned at line 371 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:356` `set_stable_table_and_set` `table_seq`: `table_seq` assigned at line 356 but never read afterwards.

## Open Questions

- Why do 10 file(s) lack file-level docs (e.g. `gyms/docker/php2shell/src/info.php`)? What purpose do they serve?
- What would break if the most connected file in cli changed?
- Should cli be split, given cohesion 0.55?

## Sources

- `cli/__init__.py`
- `cli/assign.py`
- `cli/autosuggest.py`
- `cli/chain_mode.py`
- `cli/command_explorer.py`
- `cli/command_form.py`
- `cli/commands/__init__.py`
- `cli/commands/_dormancy.py`
- `cli/commands/help_ui.py`
- `cli/commands/misc_migrated.py`
- `cli/commands/orchestration.py`
- `cli/commands/recon.py`
- `cli/commands/session_ops.py`
- `cli/config_status.py`
- `cli/contextual_help.py`
- `cli/doctor.py`
- `cli/exploit_advisor.py`
- `cli/exploration_view.py`
- `cli/marketplace_config.py`
- `cli/noise_verbs.py`
- *... and 106 more*
