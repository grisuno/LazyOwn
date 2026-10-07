# cli

*Community 2 | 89 files | cohesion 0.56*

## Definition

This community groups 89 file(s) rooted at `cli` with dominant language py (cohesion 0.56). Central symbols: `AddonCatalog`, `AddonEntry`, `AddonHotReloader`, `AliasResolver`, `AptPlaybook`, `AptPlaybookEngine`, `AtomicTestRef`, `AuditCommandSet`. Core file: `tests/test_command_palette.py` (237 symbols). Documented purpose: LazyOwn CLI infrastructure.  Tier 2 introduces a declarative, modular layer above ``lazyown.py``:  - ``cli/aliases.yaml`` and :func:`cli.aliases.load_aliases` p.

## Files

### `cli` (39 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/__init__.py` | py | utility | 0 | yes |
| `cli/chain_mode.py` | py | utility | 23 | yes |
| `cli/cli_enhancements.py` | py | utility | 69 | yes |
| `cli/command_chain.py` | py | utility | 25 | yes |

### `tests` (36 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_chain_mode.py` | py | testing | 28 | yes |
| `tests/test_cli_enhancements.py` | py | testing | 50 | yes |
| `tests/test_command_chain.py` | py | testing | 24 | yes |

### `poc_tui` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | utility | 0 | yes |
| `poc_tui/app.py` | py | utility | 47 | yes |
| `poc_tui/run.py` | py | utility | 1 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/apt_playbooks.py` | py | utility | 15 | yes |
| `modules/lazyk8s.py` | py | utility | 32 | yes |
| `modules/search.py` | py | utility | 0 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/audit.py` | py | utility | 13 | yes |
| `cli/commands/containers.py` | py | infrastructure | 7 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/command_bridge.py` | py | utility | 9 | yes |
| `core/text_utils.py` | py | utility | 1 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown.py` | py | utility | 123 | yes |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/command_audit.py` | py | utility | 4 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/showdown-2.1.0.min.js` | js | utility | 5 | yes |

*... and 69 more files in this community.*


## Key Symbols

- `_ChainEscExit` (class, `cli/chain_mode.py:73`) `class _ChainEscExit(Exception)` - Internal signal: the operator pressed ESC at the chain prompt.
- `_read_line_unix` (method, `cli/chain_mode.py:77`) `def _read_line_unix(prompt)` - Read one line in raw TTY mode, honouring ESC, Ctrl+C and backspace.
- `_read_line_windows` (method, `cli/chain_mode.py:136`) `def _read_line_windows(prompt)` - Read one line on Windows, honouring ESC, Ctrl+C and backspace.
- `ChainSuggestion` (class, `cli/chain_mode.py:183`) `class ChainSuggestion` - A single next-step proposal, normalised from any resolver output.
- `from_step` (method, `cli/chain_mode.py:191`) `def from_step(cls, step)` - Build a suggestion from a duck-typed resolver step object.
- `ChainOutcome` (class, `cli/chain_mode.py:212`) `class ChainOutcome` - Result of one chain prompt round.
- `ChainModeConfig` (class, `cli/chain_mode.py:231`) `class ChainModeConfig` - Centralised configuration for the chain prompt engine.
- `ChainModeStore` (class, `cli/chain_mode.py:242`) `class ChainModeStore` - Atomic persistence of the chain-mode toggle in the sessions dir.
- `__init__` (method, `cli/chain_mode.py:250`) `def __init__(self, sessions_dir)` - Store the sessions directory that owns the state file.
- `load` (method, `cli/chain_mode.py:258`) `def load(self)` - Return the persisted enabled flag, or ``None`` when unset.
- `save` (method, `cli/chain_mode.py:275`) `def save(self, enabled)` - Persist the enabled flag atomically.
- `ChainPromptEngine` (class, `cli/chain_mode.py:298`) `class ChainPromptEngine` - Coordinate one interactive chain prompt round per executed command.
- `__init__` (method, `cli/chain_mode.py:301`) `def __init__(self, config, resolver)` - Wire the engine with its config, resolver and I/O functions.
- `enabled` (method, `cli/chain_mode.py:335`) `def enabled(self)` - Whether the chain prompt loop is currently active.
- `steps_run` (method, `cli/chain_mode.py:340`) `def steps_run(self)` - Number of commands executed through the chain this activation.
- `set_enabled` (method, `cli/chain_mode.py:344`) `def set_enabled(self, value, persist)` - Toggle chain mode and optionally persist the choice.
- `step` (method, `cli/chain_mode.py:358`) `def step(self, last_cmd, phase)` - Run one chain prompt round for the command that just executed.
- `_prompt_loop` (method, `cli/chain_mode.py:389`) `def _prompt_loop(self, suggestions)` - Read and interpret operator input, re-prompting on invalid picks.
- `_prompt_line` (method, `cli/chain_mode.py:428`) `def _prompt_line(self)` - Read one chain-prompt line with ESC/Ctrl+C support on real TTYs.
- `_suggest` (method, `cli/chain_mode.py:450`) `def _suggest(self, verb, phase)`
- `_render_menu` (method, `cli/chain_mode.py:468`) `def _render_menu(self, verb, suggestions)`
- `_run` (method, `cli/chain_mode.py:485`) `def _run(self, command)`
- `_disable` (method, `cli/chain_mode.py:491`) `def _disable(self, reason)`
- `PayloadProvider` (class, `cli/cli_enhancements.py:40`) `class PayloadProvider(Protocol)` - Read-only view onto ``payload.json`` style configuration.
- `get` (method, `cli/cli_enhancements.py:43`) `def get(self, key, default)`
- `keys` (method, `cli/cli_enhancements.py:44`) `def keys(self)`
- `CommandLister` (class, `cli/cli_enhancements.py:47`) `class CommandLister(Protocol)` - Source of command metadata for indexing / fuzzy matching.
- `commands` (method, `cli/cli_enhancements.py:50`) `def commands(self)`
- `TerminalIO` (class, `cli/cli_enhancements.py:53`) `class TerminalIO(Protocol)` - Minimal duck-typed prompt/print pair so tests can fake it.
- `prompt` (method, `cli/cli_enhancements.py:56`) `def prompt(self, message, default)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 323
- Cross-boundary resolved imports (EXTRACTED): 170

## Connections

- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/command_explorer.py imports cli/palette.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/lazynmap_post.py:244` `_emit_event` `fd`: Result of allocator stored in `fd` is never checked against NULL.

## Open Questions

- What would break if the most connected file in cli changed?
- Should cli be split, given cohesion 0.56?

## Sources

- `cli/__init__.py`
- `cli/chain_mode.py`
- `cli/cli_enhancements.py`
- `cli/command_chain.py`
- `cli/command_form.py`
- `cli/commands/audit.py`
- `cli/commands/containers.py`
- `cli/contextual_help.py`
- `cli/dashboard_layout.py`
- `cli/dashboard_tui.py`
- `cli/exploration.py`
- `cli/exploration_view.py`
- `cli/graph_advisor.py`
- `cli/graph_overlay.py`
- `cli/headless.py`
- `cli/lazynmap_post.py`
- `cli/noise_verbs.py`
- `cli/palette.py`
- `cli/palette_command.py`
- `cli/palette_graph.py`
- *... and 69 more*
