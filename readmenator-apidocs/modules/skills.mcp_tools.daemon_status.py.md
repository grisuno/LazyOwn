# `skills.mcp_tools.daemon_status`

> Source: [skills/mcp_tools/daemon_status.py:1](../../skills/mcp_tools/daemon_status.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_daemon_status`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/daemon_status.py:22](../../skills/mcp_tools/daemon_status.py#L22)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_daemon_status MCP tool.

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

`constant` | [skills/mcp_tools/daemon_status.py:11](../../skills/mcp_tools/daemon_status.py#L11)

```python
TOOL
```

---
