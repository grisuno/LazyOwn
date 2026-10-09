# modules: wizard

*Community 4 | 54 files | cohesion 0.47*

## Definition

This community groups 54 file(s) rooted at `modules` with dominant language py (cohesion 0.47). Central symbols: `AIModel`, `ASTToolExtractor`, `AgentRunner`, `AgentTool`, `AiCommandSet`, `AnthropicModel`, `AuthError`, `BinarySpec`. Core file: `tests/test_payload_schema.py` (53 symbols). Documented purpose: Interactive command explorer by phase and goal for the LazyOwn shell.  Organizes the 727+ commands into user-friendly categories based on what the operator want.

## Files

### `core` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/__init__.py` | py | utility | 0 | yes |
| `core/console.py` | py | utility | 8 | yes |
| `core/credentials.py` | py | utility | 13 | yes |

### `modules` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 35 | yes |
| `modules/agent_tool.py` | py | utility | 4 | no |
| `modules/ai_model.py` | py | business_logic | 32 | yes |

### `tests` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_core_config.py` | py | testing | 19 | yes |
| `tests/test_dependencies.py` | py | testing | 35 | yes |

### `cli` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_explorer.py` | py | utility | 7 | yes |
| `cli/config_status.py` | py | infrastructure | 6 | yes |
| `cli/doctor.py` | py | utility | 21 | yes |

### `.` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `discord_c2.py` | py | utility | 21 | no |
| `slack_c2_bot.py` | py | utility | 16 | yes |
| `telegram_c2.py` | py | utility | 18 | no |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/ai.py` | py | utility | 6 | yes |
| `cli/commands/crystal_ball.py` | py | utility | 5 | yes |
| `cli/commands/help_ui.py` | py | presentation | 16 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |
| `contrib/legacy/lazyllmchat.py` | py | utility | 30 | no |

*... and 34 more files in this community.*


## Key Symbols

- `ExplorerConfig` (class, `cli/command_explorer.py:189`) `class ExplorerConfig` - Centralised constants for the command explorer.
- `_load_command_index` (method, `cli/command_explorer.py:195`) `def _load_command_index(path)` - Load the command index JSON. Returns empty dict on failure.
- `CommandExplorer` (class, `cli/command_explorer.py:207`) `class CommandExplorer` - Interactive command explorer organized by user goals.
- `__init__` (method, `cli/command_explorer.py:216`) `def __init__(self, aliases, params, config)`
- `render_goals_overview` (method, `cli/command_explorer.py:227`) `def render_goals_overview(self)` - Print the goals table showing all available categories.
- `render_goal_commands` (method, `cli/command_explorer.py:240`) `def render_goal_commands(self, goal_key)` - Print commands for a specific goal.
- `render_search` (method, `cli/command_explorer.py:260`) `def render_search(self, query)` - Search commands by keyword across all goals.
- `AiCommandSet` (class, `cli/commands/ai.py:70`) `class AiCommandSet(LazyOwnCommandSet)` - Pending phase module for the Artificial Intelligence commands.
- `do_ask` (method, `cli/commands/ai.py:77`) `def do_ask(self, line)` - Ask the AI a question with current session context pre-loaded.
- `do_groq` (method, `cli/commands/ai.py:146`) `def do_groq(self, line)` - Generate a single-line command through the Groq backend.
- `do_ai_playbook` (method, `cli/commands/ai.py:177`) `def do_ai_playbook(self, line)` - Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `do_ai_toggle` (method, `cli/commands/ai.py:284`) `def do_ai_toggle(self, _arg)` - Toggle the in-process AI assistant on or off.
- `do_llm_budget` (method, `cli/commands/ai.py:301`) `def do_llm_budget(self, line)` - Show the LLM daily cost budget, per call token cap, and current spend.
- `CrystalBallCommandSet` (class, `cli/commands/crystal_ball.py:20`) `class CrystalBallCommandSet(LazyOwnCommandSet)` - Crystal Ball — privesc vector prediction and ranking.
- `do_crystal_ball` (method, `cli/commands/crystal_ball.py:27`) `def do_crystal_ball(self, line)` - Analyze linpeas/winpeas output and rank privesc vectors with exact commands.
- `do_privesc_suggest` (method, `cli/commands/crystal_ball.py:110`) `def do_privesc_suggest(self, line)` - Quick alias for crystal_ball --auto.
- `_auto_detect_enum_file` (method, `cli/commands/crystal_ball.py:119`) `def _auto_detect_enum_file()` - Find linpeas or winpeas output in sessions/.
- `_safe_filename` (method, `cli/commands/crystal_ball.py:151`) `def _safe_filename(name)` - Sanitise a string for use as a filename component.
- `HelpUiCommandSet` (class, `cli/commands/help_ui.py:29`) `class HelpUiCommandSet(LazyOwnCommandSet)` - Help, tutorial and phase guidance.
- `do_wizard` (method, `cli/commands/help_ui.py:36`) `def do_wizard(self, line)` - Guided first-run setup wizard — configure rhost, lhost, domain, wordlists and more.
- `_save` (method, `cli/commands/help_ui.py:66`) `def _save(key, value)`
- `do_tutorial` (method, `cli/commands/help_ui.py:137`) `def do_tutorial(self, line)` - Interactive tutorial that walks you through the golden path.
- `do_help_phase` (method, `cli/commands/help_ui.py:160`) `def do_help_phase(self, line)` - List all commands for a given kill-chain phase.
- `do_help_status` (method, `cli/commands/help_ui.py:191`) `def do_help_status(self, line)` - Show which session requirements are met (rhost, creds, domain, OS).
- `do_ctx_help` (method, `cli/commands/help_ui.py:203`) `def do_ctx_help(self, line)` - Show contextual help for a command: description, phase, requirements, tips.
- `do_ctx` (method, `cli/commands/help_ui.py:223`) `def do_ctx(self, line)` - Print a single-line operator context: rhost, lhost, domain, phase, os, creds.
- `do_command_explorer` (method, `cli/commands/help_ui.py:235`) `def do_command_explorer(self, line)` - Interactive command explorer organized by goals and phases.
- `do_config_status` (method, `cli/commands/help_ui.py:267`) `def do_config_status(self, line)` - Show configuration status grouped by category with set/missing indicators.
- `do_tui_theme` (method, `cli/commands/help_ui.py:287`) `def do_tui_theme(self, line)` - Switch the TUI colour theme used by the splash and styled output.
- `do_doctor` (method, `cli/commands/help_ui.py:312`) `def do_doctor(self, line)` - Preflight environment health check — verify the install is ready.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 121
- Cross-boundary resolved imports (EXTRACTED): 143

## Connections

- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/command_explorer.py imports cli/palette.py.
- [EXTRACTED] depends_on community 4 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 4 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/recon.py imports modules/intelligence_engine.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/console.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `modules/ai_model.py` via `subprocess` (5 hops)
- [taint high] `cli/banner_config.py` -> `core/llm_budget.py` via `subprocess` (5 hops)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/commands/recon.py:609` `_run_single_search` `_s`: Result of allocator stored in `_s` is never checked against NULL.

## Open Questions

- Why do 6 file(s) lack file-level docs (e.g. `contrib/legacy/lazyllmchat.py`)? What purpose do they serve?
- What would break if the most connected file in modules: wizard changed?
- Should modules: wizard be split, given cohesion 0.47?

## Sources

- `cli/command_explorer.py`
- `cli/commands/ai.py`
- `cli/commands/crystal_ball.py`
- `cli/commands/help_ui.py`
- `cli/commands/recon.py`
- `cli/config_status.py`
- `cli/doctor.py`
- `cli/exploit_advisor.py`
- `cli/session_resumer.py`
- `cli/splash.py`
- `cli/tutorial.py`
- `cli/wizard.py`
- `cli/wizard_scope.py`
- `contrib/legacy/lazydeepseekcli.py`
- `contrib/legacy/lazyllmchat.py`
- `contrib/legacy/lazyphishingai.py`
- `core/__init__.py`
- `core/console.py`
- `core/credentials.py`
- `core/dependencies.py`
- *... and 34 more*
