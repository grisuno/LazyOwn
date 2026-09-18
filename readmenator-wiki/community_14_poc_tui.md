# poc_tui

*Community 14 | 4 files | cohesion 0.60*

## Definition

This community groups 4 file(s) rooted at `poc_tui` with dominant language py (cohesion 0.60). Central symbols: `DashboardPanel`, `LazyOwnTUI`, `OutputPanel`, `PluginBrowser`, `ShellBackend`, `TestLazyOwnTUIApp`, `TestShellBackend`, `__init__`. Core file: `poc_tui/test_app.py` (56 symbols). Documented purpose: Entry point: python3 -m poc_tui.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/__main__.py` | py | presentation | 0 | yes |
| `poc_tui/app.py` | py | presentation | 47 | yes |
| `poc_tui/run.py` | py | presentation | 1 | yes |
| `poc_tui/test_app.py` | py | testing | 56 | yes |

## Key Symbols

- `ShellBackend` (class, `poc_tui/app.py:44`) `class ShellBackend` - Run the real cmd2 LazyOwnShell in-process, capture all output.
- `__init__` (method, `poc_tui/app.py:47`) `def __init__(self, base_dir)`
- `import_shell_class` (method, `poc_tui/app.py:53`) `def import_shell_class(self)` - Import LazyOwnShell in the main thread (required for signal handlers).
- `start` (method, `poc_tui/app.py:71`) `def start(self)` - Instantiate LazyOwnShell (must be called from main thread).
- `run` (method, `poc_tui/app.py:83`) `def run(self, cmd)` - Execute a command and return its captured output.
- `get_commands` (method, `poc_tui/app.py:106`) `def get_commands(self)` - Return {command_name: help_text} from the live shell.
- `get_aliases` (method, `poc_tui/app.py:119`) `def get_aliases(self)`
- `stop` (method, `poc_tui/app.py:124`) `def stop(self)`
- `DashboardPanel` (class, `poc_tui/app.py:137`) `class DashboardPanel(Static)` - Left sidebar: live campaign state from payload.json.
- `__init__` (method, `poc_tui/app.py:140`) `def __init__(self, base_dir)`
- `compose` (method, `poc_tui/app.py:144`) `def compose(self)`
- `refresh_data` (method, `poc_tui/app.py:165`) `def refresh_data(self, backend, cmd_count)` - Pull latest state from the LIVE shell params (not stale disk file).
- `PluginBrowser` (class, `poc_tui/app.py:195`) `class PluginBrowser(Static)` - Right sidebar: command list from the real cmd2 shell.
- `__init__` (method, `poc_tui/app.py:198`) `def __init__(self)`
- `compose` (method, `poc_tui/app.py:201`) `def compose(self)`
- `update_commands` (method, `poc_tui/app.py:207`) `def update_commands(self, commands)`
- `_guess_category` (method, `poc_tui/app.py:223`) `def _guess_category(name, help_text)`
- `OutputPanel` (class, `poc_tui/app.py:240`) `class OutputPanel(VerticalScroll)` - Center: accumulative scrollable output log.
- `__init__` (method, `poc_tui/app.py:248`) `def __init__(self)`
- `compose` (method, `poc_tui/app.py:252`) `def compose(self)`
- `_log` (method, `poc_tui/app.py:255`) `def _log(self)`
- `write_renderable` (method, `poc_tui/app.py:258`) `def write_renderable(self, renderable)` - Write a Rich renderable (no markup parsing applied).
- `write_markup` (method, `poc_tui/app.py:263`) `def write_markup(self, text)` - Write a trusted internal string with Rich markup.
- `append_command` (method, `poc_tui/app.py:268`) `def append_command(self, cmd)`
- `append_result` (method, `poc_tui/app.py:273`) `def append_result(self, text, success)` - Write real shell output, converting ANSI — never markup-parsed.
- `append_error` (method, `poc_tui/app.py:283`) `def append_error(self, text)` - Write a TUI-side error message (plain, no markup from unsafe text).
- `append_system` (method, `poc_tui/app.py:287`) `def append_system(self, text)` - Write a TUI-side status message.
- `LazyOwnTUI` (class, `poc_tui/app.py:297`) `class LazyOwnTUI(App)` - Textual frontend for the real LazyOwn cmd2 shell.
- `__init__` (method, `poc_tui/app.py:394`) `def __init__(self, base_dir)`
- `compose` (method, `poc_tui/app.py:405`) `def compose(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 3
- Cross-boundary resolved imports (EXTRACTED): 3

## Connections

- [EXTRACTED] depends_on community 14 <-> 1 (strength 0.9): Extracted import edge crosses communities: poc_tui/app.py imports cli/commands/containers.py.

## Risks

- [layer strict] `poc_tui/test_app.py` (testing) -> `poc_tui/app.py` (presentation)

## Open Questions

- What would break if the most connected file in poc_tui changed?
- Should poc_tui be split, given cohesion 0.60?

## Sources

- `poc_tui/__main__.py`
- `poc_tui/app.py`
- `poc_tui/run.py`
- `poc_tui/test_app.py`
