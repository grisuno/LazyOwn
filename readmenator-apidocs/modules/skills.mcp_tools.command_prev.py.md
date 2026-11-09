# `skills.mcp_tools.command_prev`

> Source: [skills/mcp_tools/command_prev.py:1](../../skills/mcp_tools/command_prev.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_command_prev`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_command_prev_py__handle(["handle"])
    n_cli_command_chain_py__CommandChain___init__["command_chain.CommandChain.__init__"]
    n_cli_command_chain_py__CommandChain_prev["command_chain.CommandChain.prev"]
    n_skills_mcp_tools_command_prev_py__handle -.-> n_cli_command_chain_py__CommandChain___init__
    n_skills_mcp_tools_command_prev_py__handle -.-> n_cli_command_chain_py__CommandChain_prev
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/command_prev.py:31](../../skills/mcp_tools/command_prev.py#L31)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_command_prev MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`CommandChain.__init__`](cli.command_chain.py.md#commandchain-__init__), [`CommandChain.prev`](cli.command_chain.py.md#commandchain-prev)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/command_prev.py:11](../../skills/mcp_tools/command_prev.py#L11)

```python
TOOL
```

---
