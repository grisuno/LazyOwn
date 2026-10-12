# `skills.lazyown_automapper`

> Source: [skills/lazyown_automapper.py:1](../../skills/lazyown_automapper.py#L1) | language `py` | coverage 77.8% | [API index](../index.md)

LazyOwn MCP Auto-Mapper ======================== Discovers LazyOwn extensions at startup and returns MCP Tool definitions + a runtime dispatch table.

Three source types are supported:

lazyaddons/*.yaml  (enabled: true)  → lazyown_addon_<name>
  tools/*.tool       (active: true)   → lazyown_tool_<name>
  plugins/*.yaml     (enabled: true)  → lazyown_plugin_<name>

All discovered tools are executed by running the LazyOwn shell command or,
for .tool files, by substituting the command template and running it via
subprocess.

Integration in lazyown_mcp.py
──────────────────────────────
    from lazyown_automapper import AutoMapper

    _automapper = AutoMapper(LAZYOWN_DIR)

    # list_tools():
    return STATIC_TOOLS + _automapper.mcp_tools()

    # call_tool():
    result = _automapper.dispatch(name, arguments, config)
    if result is not None:
        return result

Auto-regeneration of lazyown.md
───────────────────────────────
    _automapper.update_skills_md(skills_md_path)

    Appends / replaces the "## Auto-discovered tools" section of lazyown.md
    with a Markdown table of all dynamic tools found at startup.

## Contents

- **Classes:** [`AutoMapper`](#automapper)

## Classes

<a id="automapper"></a>

### `AutoMapper`

`class` | [skills/lazyown_automapper.py:332](../../skills/lazyown_automapper.py#L332)

```python
class AutoMapper
```

Discover and cache all dynamic MCP tools from lazyaddons/, tools/, plugins/.

Call .mcp_tools() to get the list of types.Tool objects.
Call .dispatch(name, arguments, config) → Optional[str] to execute.
Call .update_skills_md(path) to regenerate the auto-discovered section.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#automapper-__init__) | constructor |  |
| [`rescan`](#automapper-rescan) | method | Force a rescan of all source directories. |
| [`mcp_tools`](#automapper-mcp_tools) | method | Return list of mcp types.Tool objects for all discovered extensions. |
| [`dispatch`](#automapper-dispatch) | method | Execute a dynamic tool. |
| [`update_skills_md`](#automapper-update_skills_md) | method | Append / replace the auto-discovered section in skills/lazyown.md. |
| [`stats`](#automapper-stats) | method |  |
| [`list_specs`](#automapper-list_specs) | method | Return raw spec dicts (useful for debugging / reporting). |

<a id="automapper-__init__"></a>

#### `AutoMapper.__init__`

`constructor` | [skills/lazyown_automapper.py:341](../../skills/lazyown_automapper.py#L341)

```python
def __init__(self, lazyown_dir: Path) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `lazyown_dir` | `Path` |  |  |

<a id="automapper-rescan"></a>

#### `AutoMapper.rescan`

`method` | [skills/lazyown_automapper.py:364](../../skills/lazyown_automapper.py#L364)

```python
def rescan(self) -> None
```

Force a rescan of all source directories.

<a id="automapper-mcp_tools"></a>

#### `AutoMapper.mcp_tools`

`method` | [skills/lazyown_automapper.py:368](../../skills/lazyown_automapper.py#L368)

```python
def mcp_tools(self) -> list[Any]
```

Return list of mcp types.Tool objects for all discovered extensions.

**Returns:** `list[Any]`

<a id="automapper-dispatch"></a>

#### `AutoMapper.dispatch`

`method` | [skills/lazyown_automapper.py:389](../../skills/lazyown_automapper.py#L389)

```python
def dispatch(self, name: str, arguments: dict[str, Any], config: dict[str, Any], run_command_fn: Any = None) -> str | None
```

Execute a dynamic tool.

Returns the output string or None if name is not a known dynamic tool (caller should fall through to static dispatch).

run_command_fn: callable(cmd: str, timeout: int=30) → str
    When provided, addon/plugin calls go through the LazyOwn shell.
    .tool commands always run via subprocess.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `arguments` | `dict[str, Any]` |  |  |
| `config` | `dict[str, Any]` |  |  |
| `run_command_fn` | `Any` | `None` |  |

**Returns:** `str | None`

<a id="automapper-update_skills_md"></a>

#### `AutoMapper.update_skills_md`

`method` | [skills/lazyown_automapper.py:524](../../skills/lazyown_automapper.py#L524)

```python
def update_skills_md(self, skills_md_path: Path) -> None
```

Append / replace the auto-discovered section in skills/lazyown.md.

The section is delimited by HTML comments so it can be replaced cleanly.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `skills_md_path` | `Path` |  |  |

<a id="automapper-stats"></a>

#### `AutoMapper.stats`

`method` | [skills/lazyown_automapper.py:571](../../skills/lazyown_automapper.py#L571)

```python
def stats(self) -> str
```

**Returns:** `str`

<a id="automapper-list_specs"></a>

#### `AutoMapper.list_specs`

`method` | [skills/lazyown_automapper.py:581](../../skills/lazyown_automapper.py#L581)

```python
def list_specs(self) -> list[dict]
```

Return raw spec dicts (useful for debugging / reporting).

**Returns:** `list[dict]`

---
