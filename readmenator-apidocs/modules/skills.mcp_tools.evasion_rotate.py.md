# `skills.mcp_tools.evasion_rotate`

> Source: [skills/mcp_tools/evasion_rotate.py:1](../../skills/mcp_tools/evasion_rotate.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_evasion_rotate``: rotate to a fresh evasion profile.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_evasion_rotate_py__handle(["handle"])
    n_modules_evasion_engine_py__EvasionEngine___init__["evasion_engine.EvasionEngine.__init__"]
    n_modules_evasion_engine_py__EvasionEngine_profile_to_json["evasion_engine.EvasionEngine.profile_to_json"]
    n_modules_evasion_engine_py__EvasionEngine_rotate_profile["evasion_engine.EvasionEngine.rotate_profile"]
    n_skills_mcp_tools_evasion_rotate_py__handle -.-> n_modules_evasion_engine_py__EvasionEngine___init__
    n_skills_mcp_tools_evasion_rotate_py__handle -.-> n_modules_evasion_engine_py__EvasionEngine_profile_to_json
    n_skills_mcp_tools_evasion_rotate_py__handle -.-> n_modules_evasion_engine_py__EvasionEngine_rotate_profile
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/evasion_rotate.py:27](../../skills/mcp_tools/evasion_rotate.py#L27)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Rotate the active evasion profile and return it as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`EvasionEngine.__init__`](modules.evasion_engine.py.md#evasionengine-__init__), [`EvasionEngine.profile_to_json`](modules.evasion_engine.py.md#evasionengine-profile_to_json), [`EvasionEngine.rotate_profile`](modules.evasion_engine.py.md#evasionengine-rotate_profile)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/evasion_rotate.py:12](../../skills/mcp_tools/evasion_rotate.py#L12)

```python
TOOL
```

---
