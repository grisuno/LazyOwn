# poc_tui

*Community 15 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `poc_tui` with dominant language py (cohesion 1.00). Central symbols: `PayloadConfig`, `PluginLoader`, `PluginSpec`, `_LuaAppProxy`, `__contains__`, `__getitem__`, `__init__`, `__post_init__`. Core file: `poc_tui/plugin_loader.py` (22 symbols). Documented purpose: Payload.json configuration manager for the TUI shell..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `poc_tui/config.py` | py | presentation | 11 | yes |
| `poc_tui/plugin_loader.py` | py | presentation | 22 | yes |

## Key Symbols

- `PayloadConfig` (class, `poc_tui/config.py:12`) `class PayloadConfig` - Read/write access to payload.json settings.
- `__post_init__` (method, `poc_tui/config.py:18`) `def __post_init__(self)`
- `reload` (method, `poc_tui/config.py:21`) `def reload(self)` - Re-read payload.json from disk.
- `save` (method, `poc_tui/config.py:28`) `def save(self)` - Persist current state back to payload.json.
- `get` (method, `poc_tui/config.py:35`) `def get(self, key, default)`
- `set` (method, `poc_tui/config.py:38`) `def set(self, key, value)`
- `keys` (method, `poc_tui/config.py:41`) `def keys(self)`
- `items` (method, `poc_tui/config.py:44`) `def items(self)`
- `__getitem__` (method, `poc_tui/config.py:47`) `def __getitem__(self, key)`
- `__setitem__` (method, `poc_tui/config.py:50`) `def __setitem__(self, key, value)`
- `__contains__` (method, `poc_tui/config.py:53`) `def __contains__(self, key)`
- `PluginSpec` (class, `poc_tui/plugin_loader.py:28`) `class PluginSpec` - Metadata for a single registered command.
- `_replace_placeholders` (method, `poc_tui/plugin_loader.py:40`) `def _replace_placeholders(command, params)` - Replace {key} tokens in a command string with values from params.
- `_subst` (method, `poc_tui/plugin_loader.py:43`) `def _subst(match)`
- `_validate_clone_url` (method, `poc_tui/plugin_loader.py:51`) `def _validate_clone_url(url)` - Validate a git clone URL, rejecting shell metacharacters.
- `PluginLoader` (class, `poc_tui/plugin_loader.py:73`) `class PluginLoader` - Load and register all plugin types into a command registry.
- `__init__` (method, `poc_tui/plugin_loader.py:80`) `def __init__(self, config, base_dir)`
- `_setup_lua` (method, `poc_tui/plugin_loader.py:94`) `def _setup_lua(self)`
- `_lua_register` (method, `poc_tui/plugin_loader.py:103`) `def _lua_register(self, name, func)` - Bridge: Lua calls register_command(name, fn) -> we wrap it.
- `wrapper` (method, `poc_tui/plugin_loader.py:106`) `def wrapper(arg)`
- `_list_files` (method, `poc_tui/plugin_loader.py:120`) `def _list_files(self, directory)`
- `load_all` (method, `poc_tui/plugin_loader.py:128`) `def load_all(self)` - Load yaml addons, lua plugins, and .tool files. Return specs.
- `_load_yaml_addons` (method, `poc_tui/plugin_loader.py:137`) `def _load_yaml_addons(self)`
- `_register_yaml_addon` (method, `poc_tui/plugin_loader.py:150`) `def _register_yaml_addon(self, data)`
- `wrapper` (method, `poc_tui/plugin_loader.py:161`) `def wrapper(arg)`
- `_load_lua_plugins` (method, `poc_tui/plugin_loader.py:212`) `def _load_lua_plugins(self)`
- `_load_tool_files` (method, `poc_tui/plugin_loader.py:237`) `def _load_tool_files(self)`
- `_register_tool` (method, `poc_tui/plugin_loader.py:250`) `def _register_tool(self, data)`
- `wrapper` (method, `poc_tui/plugin_loader.py:258`) `def wrapper(arg)`
- `_LuaAppProxy` (class, `poc_tui/plugin_loader.py:280`) `class _LuaAppProxy` - Minimal proxy exposed to Lua plugins as the global ``app`` object.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in poc_tui changed?
- Should poc_tui be split, given cohesion 1.00?

## Sources

- `poc_tui/config.py`
- `poc_tui/plugin_loader.py`
