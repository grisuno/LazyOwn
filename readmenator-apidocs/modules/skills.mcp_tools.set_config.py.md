# `skills.mcp_tools.set_config`

> Source: [skills/mcp_tools/set_config.py:1](../../skills/mcp_tools/set_config.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool `[`lazyown_set_config`](utils.py.md#lazyown_set_config)`: set one key in payload.json.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_set_config_py__handle(["handle"])
    n_core_payload_schema_py__coerce_value["payload_schema.coerce_value"]
    n_skills_mcp_tools_set_config_py__handle -.-> n_core_payload_schema_py__coerce_value
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/set_config.py:36](../../skills/mcp_tools/set_config.py#L36)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Coerce and persist one payload key, refusing to null an existing value.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`coerce_value`](core.payload_schema.py.md#coerce_value)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/set_config.py:12](../../skills/mcp_tools/set_config.py#L12)

```python
TOOL
```

---
