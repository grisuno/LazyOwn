# `skills.mcp_tools.lolbas_list`

> Source: [skills/mcp_tools/lolbas_list.py:1](../../skills/mcp_tools/lolbas_list.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_lolbas_list``: list LOLBAS techniques from plugins.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/lolbas_list.py:34](../../skills/mcp_tools/lolbas_list.py#L34)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Return LOLBAS techniques discovered in plugin YAML files as JSON.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/lolbas_list.py:14](../../skills/mcp_tools/lolbas_list.py#L14)

```python
TOOL
```

---
