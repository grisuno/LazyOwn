# `skills.mcp_tools.evasion_generate`

> Source: [skills/mcp_tools/evasion_generate.py:1](../../skills/mcp_tools/evasion_generate.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_evasion_generate``: generate a C2 malleable profile.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_evasion_generate_py__handle(["handle"])
    n_modules_evasion_engine_py__EvasionEngine___init__["evasion_engine.EvasionEngine.__init__"]
    n_modules_evasion_engine_py__EvasionEngine_generate_profile["evasion_engine.EvasionEngine.generate_profile"]
    n_modules_evasion_engine_py__EvasionEngine_profile_to_json["evasion_engine.EvasionEngine.profile_to_json"]
    n_skills_mcp_tools_evasion_generate_py__handle -.-> n_modules_evasion_engine_py__EvasionEngine___init__
    n_skills_mcp_tools_evasion_generate_py__handle -.-> n_modules_evasion_engine_py__EvasionEngine_generate_profile
    n_skills_mcp_tools_evasion_generate_py__handle -.-> n_modules_evasion_engine_py__EvasionEngine_profile_to_json
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/evasion_generate.py:36](../../skills/mcp_tools/evasion_generate.py#L36)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Generate an evasion profile for the requested OS family as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`EvasionEngine.__init__`](modules.evasion_engine.py.md#evasionengine-__init__), [`EvasionEngine.generate_profile`](modules.evasion_engine.py.md#evasionengine-generate_profile), [`EvasionEngine.profile_to_json`](modules.evasion_engine.py.md#evasionengine-profile_to_json)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/evasion_generate.py:14](../../skills/mcp_tools/evasion_generate.py#L14)

```python
TOOL
```

---
