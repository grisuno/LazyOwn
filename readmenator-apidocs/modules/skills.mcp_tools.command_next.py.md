# `skills.mcp_tools.command_next`

> Source: [skills/mcp_tools/command_next.py:1](../../skills/mcp_tools/command_next.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_command_next`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_command_next_py__handle(["handle"])
    n_cli_command_chain_py__CommandChain___init__["command_chain.CommandChain.__init__"]
    n_skills_mcp_tools_command_next_py__handle -.-> n_cli_command_chain_py__CommandChain___init__
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/command_next.py:45](../../skills/mcp_tools/command_next.py#L45)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_command_next MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`CommandChain.__init__`](cli.command_chain.py.md#commandchain-__init__)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/command_next.py:11](../../skills/mcp_tools/command_next.py#L11)

```python
TOOL
```

---
