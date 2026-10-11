# modules: lazy_sentinel4

*Community 3 | 64 files | cohesion 0.45*

## Definition

This community groups 64 file(s) rooted at `modules` with dominant language py (cohesion 0.45). Central symbols: `ACIEngine`, `ACIGoal`, `ACIPlan`, `ACIPlanner`, `ACIReflector`, `AIModel`, `ASTToolExtractor`, `AgentRunner`. Core file: `tests/test_aci_planner.py` (95 symbols). Documented purpose: Interactive command explorer by phase and goal for the LazyOwn shell.  Organizes the 727+ commands into user-friendly categories based on what the operator want.

## Files

### `modules` (19 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 35 | yes |
| `modules/agent_tool.py` | py | utility | 4 | no |
| `modules/ai_model.py` | py | business_logic | 32 | yes |

### `tests` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aci_planner.py` | py | testing | 95 | yes |
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_console_stdio.py` | py | testing | 14 | yes |

### `core` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/__init__.py` | py | utility | 0 | yes |
| `core/console.py` | py | utility | 11 | yes |
| `core/dependencies.py` | py | utility | 23 | yes |

### `cli` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_explorer.py` | py | utility | 7 | yes |
| `cli/config_status.py` | py | infrastructure | 6 | yes |
| `cli/doctor.py` | py | utility | 21 | yes |

### `.` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `discord_c2.py` | py | utility | 21 | no |
| `lazy_sentinel4.py` | py | utility | 47 | no |
| `slack_c2_bot.py` | py | utility | 16 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/ai.py` | py | utility | 8 | yes |
| `cli/commands/crystal_ball.py` | py | utility | 5 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |
| `contrib/legacy/lazyllmchat.py` | py | utility | 30 | no |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/aci_planner.py` | py | utility | 42 | yes |

*... and 44 more files in this community.*


## Key Symbols

- `ExplorerConfig` (class, `cli/command_explorer.py:189`) `class ExplorerConfig` - Centralised constants for the command explorer.
- `_load_command_index` (method, `cli/command_explorer.py:195`) `def _load_command_index(path)` - Load the command index JSON. Returns empty dict on failure.
- `CommandExplorer` (class, `cli/command_explorer.py:207`) `class CommandExplorer` - Interactive command explorer organized by user goals.
- `__init__` (method, `cli/command_explorer.py:216`) `def __init__(self, aliases, params, config)`
- `render_goals_overview` (method, `cli/command_explorer.py:227`) `def render_goals_overview(self)` - Print the goals table showing all available categories.
- `render_goal_commands` (method, `cli/command_explorer.py:240`) `def render_goal_commands(self, goal_key)` - Print commands for a specific goal.
- `render_search` (method, `cli/command_explorer.py:260`) `def render_search(self, query)` - Search commands by keyword across all goals.
- `AiCommandSet` (class, `cli/commands/ai.py:71`) `class AiCommandSet(LazyOwnCommandSet)` - Pending phase module for the Artificial Intelligence commands.
- `do_ask` (method, `cli/commands/ai.py:78`) `def do_ask(self, line)` - Ask the AI a question with current session context pre-loaded.
- `do_groq` (method, `cli/commands/ai.py:166`) `def do_groq(self, line)` - Generate a single-line command through the Groq backend.
- `do_poolcheck` (method, `cli/commands/ai.py:197`) `def do_poolcheck(self, line)` - Prove the LLM failover pool order with one live prompt.
- `_serve` (method, `cli/commands/ai.py:223`) `def _serve(member_id, backend_name, text)`
- `do_ai_playbook` (method, `cli/commands/ai.py:254`) `def do_ai_playbook(self, line)` - Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `do_ai_toggle` (method, `cli/commands/ai.py:361`) `def do_ai_toggle(self, _arg)` - Toggle the in-process AI assistant on or off.
- `do_llm_budget` (method, `cli/commands/ai.py:378`) `def do_llm_budget(self, line)` - Show the LLM daily cost budget, per call token cap, and current spend.
- `CrystalBallCommandSet` (class, `cli/commands/crystal_ball.py:20`) `class CrystalBallCommandSet(LazyOwnCommandSet)` - Crystal Ball — privesc vector prediction and ranking.
- `do_crystal_ball` (method, `cli/commands/crystal_ball.py:27`) `def do_crystal_ball(self, line)` - Analyze linpeas/winpeas output and rank privesc vectors with exact commands.
- `do_privesc_suggest` (method, `cli/commands/crystal_ball.py:110`) `def do_privesc_suggest(self, line)` - Quick alias for crystal_ball --auto.
- `_auto_detect_enum_file` (method, `cli/commands/crystal_ball.py:119`) `def _auto_detect_enum_file()` - Find linpeas or winpeas output in sessions/.
- `_safe_filename` (method, `cli/commands/crystal_ball.py:151`) `def _safe_filename(name)` - Sanitise a string for use as a filename component.
- `HelpUiCommandSet` (class, `cli/commands/help_ui.py:29`) `class HelpUiCommandSet(LazyOwnCommandSet)` - Help, tutorial and phase guidance.
- `do_wizard` (method, `cli/commands/help_ui.py:36`) `def do_wizard(self, line)` - Guided first-run setup wizard — configure rhost, lhost, domain, wordlists and more.
- `_save` (method, `cli/commands/help_ui.py:67`) `def _save(key, value)`
- `do_tutorial` (method, `cli/commands/help_ui.py:151`) `def do_tutorial(self, line)` - Interactive tutorial that walks you through the golden path.
- `do_help_phase` (method, `cli/commands/help_ui.py:175`) `def do_help_phase(self, line)` - List all commands for a given kill-chain phase.
- `do_help_status` (method, `cli/commands/help_ui.py:208`) `def do_help_status(self, line)` - Show which session requirements are met (rhost, creds, domain, OS).
- `do_ctx_help` (method, `cli/commands/help_ui.py:221`) `def do_ctx_help(self, line)` - Show contextual help for a command: description, phase, requirements, tips.
- `do_ctx` (method, `cli/commands/help_ui.py:242`) `def do_ctx(self, line)` - Print a single-line operator context: rhost, lhost, domain, phase, os, creds.
- `do_command_explorer` (method, `cli/commands/help_ui.py:254`) `def do_command_explorer(self, line)` - Interactive command explorer organized by goals and phases.
- `do_config_status` (method, `cli/commands/help_ui.py:287`) `def do_config_status(self, line)` - Show configuration status grouped by category with set/missing indicators.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 185
- Cross-boundary resolved imports (EXTRACTED): 151

## Connections

- [EXTRACTED] depends_on community 10 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/parsers.py.
- [EXTRACTED] depends_on community 3 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/command_explorer.py imports cli/palette.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 3 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_pool.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/console.py` via `subprocess` (5 hops)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [layer strict] `tests/test_help_ui_command_set.py` (testing) -> `cli/commands/help_ui.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/commands/recon.py:609` `_run_single_search` `_s`: Result of allocator stored in `_s` is never checked against NULL.

## Open Questions

- Why do 9 file(s) lack file-level docs (e.g. `contrib/legacy/lazyllmchat.py`)? What purpose do they serve?
- What would break if the most connected file in modules: lazy_sentinel4 changed?
- Should modules: lazy_sentinel4 be split, given cohesion 0.45?

## Sources

- `cli/command_explorer.py`
- `cli/commands/ai.py`
- `cli/commands/crystal_ball.py`
- `cli/commands/help_ui.py`
- `cli/commands/recon.py`
- `cli/config_status.py`
- `cli/doctor.py`
- `cli/exploit_advisor.py`
- `cli/splash.py`
- `cli/tutorial.py`
- `cli/wizard.py`
- `cli/wizard_scope.py`
- `contrib/legacy/lazydeepseekcli.py`
- `contrib/legacy/lazyllmchat.py`
- `contrib/legacy/lazyphishingai.py`
- `core/__init__.py`
- `core/console.py`
- `core/dependencies.py`
- `core/error_advice.py`
- `core/errors.py`
- *... and 44 more*
