# `skills.mcp_tools.stealth`

> Source: [skills/mcp_tools/stealth.py:1](../../skills/mcp_tools/stealth.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_stealth``: toggle stealth mode for later operations.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_stealth_py__handle(["handle"])
    n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_get_instance["autonomous_exploit_engine.AutonomousExploitEngine.get_instance"]
    n_skills_mcp_tools_stealth_py__handle -.-> n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_get_instance
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/stealth.py:35](../../skills/mcp_tools/stealth.py#L35)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Set the stealth level on the exploit engine and persist it to config.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`AutonomousExploitEngine.get_instance`](modules.autonomous_exploit_engine.py.md#autonomousexploitengine-get_instance)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/stealth.py:14](../../skills/mcp_tools/stealth.py#L14)

```python
TOOL
```

---
