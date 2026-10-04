# cli

*Community 4 | 20 files | cohesion 0.45*

## Definition

This community groups 20 file(s) rooted at `cli` with dominant language py (cohesion 0.45). Central symbols: `CategorySpec`, `CommandFieldSet`, `CommandFormConfig`, `CommandFormState`, `CommandStat`, `CompletionPosition`, `ContainerCommandSet`, `ContainerEscapeTechniques`. Core file: `tests/test_command_palette.py` (237 symbols). Documented purpose: Textual form-mode launcher for LazyOwn commands.  The form turns any ``do_*`` command into a guided launcher: the operator picks a command name, sees the inferr.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/command_form.py` | py | data_access | 31 | yes |
| `cli/commands/containers.py` | py | infrastructure | 7 | yes |
| `cli/palette_command.py` | py | utility | 51 | yes |
| `cli/palette_graph.py` | py | utility | 13 | yes |
| `cli/palette_overlay.py` | py | utility | 24 | yes |
| `cli/palette_telemetry.py` | py | utility | 14 | yes |
| `cli/sessions_browser.py` | py | utility | 31 | yes |
| `cli/style.py` | py | utility | 4 | yes |
| `cli/themes.py` | py | utility | 3 | yes |
| `cli/timeline_browser.py` | py | utility | 25 | yes |
| `modules/lazyk8s.py` | py | utility | 32 | yes |
| `modules/search.py` | py | utility | 0 | yes |
| `static/js/showdown-2.1.0.min.js` | js | utility | 5 | yes |
| `tests/test_command_form.py` | py | testing | 13 | yes |
| `tests/test_command_palette.py` | py | testing | 237 | yes |
| `tests/test_palette_overlay.py` | py | testing | 10 | yes |
| `tests/test_sessions_browser.py` | py | testing | 8 | yes |
| `tests/test_themes.py` | py | testing | 6 | yes |
| `tests/test_timeline_browser.py` | py | testing | 8 | yes |
| `tests/test_tui_theme_command.py` | py | testing | 19 | yes |

## Key Symbols

- `FormField` (class, `cli/command_form.py:37`) `class FormField` - Single editable input in the form.
- `CommandFieldSet` (class, `cli/command_form.py:48`) `class CommandFieldSet` - Fields the form surfaces for a given command name.
- `CommandFormConfig` (class, `cli/command_form.py:56`) `class CommandFormConfig` - Centralised constants for the form-mode launcher.
- `CommandFormState` (class, `cli/command_form.py:116`) `class CommandFormState` - Pure data layer for the form.
- `__post_init__` (method, `cli/command_form.py:126`) `def __post_init__(self)`
- `fields` (method, `cli/command_form.py:131`) `def fields(self)` - Return the fields associated with :attr:`command_name`.
- `summary` (method, `cli/command_form.py:139`) `def summary(self)` - Return the command summary from the index, or an empty string.
- `set_value` (method, `cli/command_form.py:150`) `def set_value(self, identifier, value)` - Update the value of one field.
- `set_extra_args` (method, `cli/command_form.py:154`) `def set_extra_args(self, value)` - Replace the extra-args buffer.
- `build_command` (method, `cli/command_form.py:158`) `def build_command(self)` - Return the cmd-line preview string the operator sees.
- `overrides` (method, `cli/command_form.py:173`) `def overrides(self)` - Return ``[(payload_key, value), ...]`` for fields the operator changed.
- `verb_line` (method, `cli/command_form.py:188`) `def verb_line(self)` - Return ``"<verb> <extra_args>"`` ready for the shell.
- `is_valid` (method, `cli/command_form.py:195`) `def is_valid(self)` - Return ``True`` when the command name is known in the index.
- `_default_for` (method, `cli/command_form.py:200`) `def _default_for(self, field_spec)`
- `_payload_str` (method, `cli/command_form.py:205`) `def _payload_str(self, key)`
- `_iter_rows` (method, `cli/command_form.py:213`) `def _iter_rows(self)`
- `_normalise_command` (method, `cli/command_form.py:220`) `def _normalise_command(name)`
- `_verb` (method, `cli/command_form.py:229`) `def _verb(name)`
- `_load_index` (method, `cli/command_form.py:236`) `def _load_index()`
- `build_state` (method, `cli/command_form.py:247`) `def build_state(command_name, payload, index, config)` - Wire the canonical state used by :func:`launch_form`.
- `launch_form` (method, `cli/command_form.py:262`) `def launch_form(command_name, payload, state, runner)` - Open the form and return the populated state on submit.
- `_build_app` (method, `cli/command_form.py:298`) `def _build_app(state, theme)`
- `_CommandFormApp` (class, `cli/command_form.py:309`) `class _CommandFormApp(App)`
- `__init__` (method, `cli/command_form.py:325`) `def __init__(self)`
- `compose` (method, `cli/command_form.py:330`) `def compose(self)`
- `on_mount` (method, `cli/command_form.py:348`) `def on_mount(self)`
- `on_input_changed` (method, `cli/command_form.py:351`) `def on_input_changed(self, event)`
- `on_input_submitted` (method, `cli/command_form.py:360`) `def on_input_submitted(self, event)`
- `action_submit` (method, `cli/command_form.py:363`) `def action_submit(self)`
- `action_cancel` (method, `cli/command_form.py:366`) `def action_cancel(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 132
- Cross-boundary resolved imports (EXTRACTED): 40

## Connections

- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/palette.py.
- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/containers.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 3 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/dashboard_tui.py imports cli/commands/containers.py.
- [EXTRACTED] depends_on community 5 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/status_bar.py imports cli/themes.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in cli changed?
- Should cli be split, given cohesion 0.45?

## Sources

- `cli/command_form.py`
- `cli/commands/containers.py`
- `cli/palette_command.py`
- `cli/palette_graph.py`
- `cli/palette_overlay.py`
- `cli/palette_telemetry.py`
- `cli/sessions_browser.py`
- `cli/style.py`
- `cli/themes.py`
- `cli/timeline_browser.py`
- `modules/lazyk8s.py`
- `modules/search.py`
- `static/js/showdown-2.1.0.min.js`
- `tests/test_command_form.py`
- `tests/test_command_palette.py`
- `tests/test_palette_overlay.py`
- `tests/test_sessions_browser.py`
- `tests/test_themes.py`
- `tests/test_timeline_browser.py`
- `tests/test_tui_theme_command.py`
