# `skills.lazyown_mcp_opencode`

> Source: [skills/lazyown_mcp_opencode.py:1](../../skills/lazyown_mcp_opencode.py#L1) | language `py` | coverage 75.0% | [API index](../index.md)

LazyOwn MCP OpenCode bridge.

Curated, short-named MCP server for autonomous OpenCode agents running on local
models (e.g. ollama/qwen3.8:27b). Local models mis-handle large tool catalogs and
re-namespace long names like ``lazyown_lazyown_campaign_sitrep``. This bridge
exposes only the essential LazyOwn tools under short, memorable names and proxies
every call back to the full ``lazyown_mcp`` server, which keeps the single source
of truth for logic, permissions and hooks.

Usage:
    python3 skills/lazyown_mcp_opencode.py

The stdio transport is used (default), matching OpenCode local MCP config.

## Contents

- **Functions:** [`list_tools`](#list_tools), [`call_tool`](#call_tool), [`main`](#main)
- **Constants:** [`CURATED_TOOLS`](#curated_tools), [`HARNESS_TOOLS`](#harness_tools)

## Functions

<a id="list_tools"></a>

### `list_tools`

`function` `async` | [skills/lazyown_mcp_opencode.py:181](../../skills/lazyown_mcp_opencode.py#L181)

Decorators: `@server.list_tools()`

```python
async def list_tools() -> list[types.Tool]
```

Expose the curated subset under short names, keeping original schemas.

**Returns:** `list[types.Tool]`

---

<a id="call_tool"></a>

### `call_tool`

`function` `async` | [skills/lazyown_mcp_opencode.py:201](../../skills/lazyown_mcp_opencode.py#L201)

Decorators: `@server.call_tool()`

```python
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]
```

Proxy the short name to the full LazyOwn MCP handler.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `arguments` | `dict[str, Any]` |  |  |

**Returns:** `list[types.TextContent]`

**Raises**

- `ValueError`: (raised in the body, not documented)

---

<a id="main"></a>

### `main`

`function` `async` | [skills/lazyown_mcp_opencode.py:211](../../skills/lazyown_mcp_opencode.py#L211)

```python
async def main() -> None
```

---

## Constants

<a id="curated_tools"></a>

### `CURATED_TOOLS`

`constant` | [skills/lazyown_mcp_opencode.py:38](../../skills/lazyown_mcp_opencode.py#L38)

```python
CURATED_TOOLS: dict[str, str]
```

---

<a id="harness_tools"></a>

### `HARNESS_TOOLS`

`constant` | [skills/lazyown_mcp_opencode.py:64](../../skills/lazyown_mcp_opencode.py#L64)

```python
HARNESS_TOOLS: dict[str, dict[str, str]]
```

---
