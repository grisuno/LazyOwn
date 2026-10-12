# `skills.hermes-lazyown.mcp_server`

> Source: [skills/hermes-lazyown/mcp_server.py:1](../../skills/hermes-lazyown/mcp_server.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

Hermes-native MCP server for LazyOwn.

Provides a compact, namespaced tool surface optimized for Hermes agent
context windows. Auto-detects Hermes sessions and adapts descriptions,
output compaction, and rule generation accordingly.

Usage:
    python3 skills/hermes-lazyown/mcp_server.py

This server does NOT replace skills/lazyown_mcp.py; it complements it
with a Hermes-optimized subset.

## Contents

- **Functions:** [`list_tools`](#list_tools), [`call_tool`](#call_tool), [`main`](#main)
- **Constants:** [`TOOLS`](#tools)

## Functions

<a id="list_tools"></a>

### `list_tools`

`function` `async` | [skills/hermes-lazyown/mcp_server.py:329](../../skills/hermes-lazyown/mcp_server.py#L329)

Decorators: `@server.list_tools()`

```python
async def list_tools() -> list[types.Tool]
```

**Returns:** `list[types.Tool]`

---

<a id="call_tool"></a>

### `call_tool`

`function` `async` | [skills/hermes-lazyown/mcp_server.py:334](../../skills/hermes-lazyown/mcp_server.py#L334)

Decorators: `@server.call_tool()`

```python
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]
```

Dispatch incoming tool calls to the appropriate handler.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `arguments` | `dict[str, Any]` |  |  |

**Returns:** `list[types.TextContent]`

---

<a id="main"></a>

### `main`

`function` `async` | [skills/hermes-lazyown/mcp_server.py:751](../../skills/hermes-lazyown/mcp_server.py#L751)

```python
async def main() -> None
```

---

## Constants

<a id="tools"></a>

### `TOOLS`

`constant` | [skills/hermes-lazyown/mcp_server.py:127](../../skills/hermes-lazyown/mcp_server.py#L127)

```python
TOOLS: list[types.Tool]
```

---
