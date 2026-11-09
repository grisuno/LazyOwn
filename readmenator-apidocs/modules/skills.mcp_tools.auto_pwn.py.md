# `skills.mcp_tools.auto_pwn`

> Source: [skills/mcp_tools/auto_pwn.py:1](../../skills/mcp_tools/auto_pwn.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_auto_pwn``: run the full autonomous exploitation chain.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_auto_pwn_py__handle(["handle"])
    n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine___init__["autonomous_exploit_engine.AutonomousExploitEngine.__init__"]
    n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_enable_stealth["autonomous_exploit_engine.AutonomousExploitEngine.enable_stealth"]
    n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_full_auto_pwn["autonomous_exploit_engine.AutonomousExploitEngine.full_auto_pwn"]
    n_skills_mcp_tools_auto_pwn_py__handle -.-> n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine___init__
    n_skills_mcp_tools_auto_pwn_py__handle -.-> n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_enable_stealth
    n_skills_mcp_tools_auto_pwn_py__handle -.-> n_modules_autonomous_exploit_engine_py__AutonomousExploitEngine_full_auto_pwn
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/auto_pwn.py:47](../../skills/mcp_tools/auto_pwn.py#L47)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Run the full auto-pwn chain and return results with a summary.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`AutonomousExploitEngine.__init__`](modules.autonomous_exploit_engine.py.md#autonomousexploitengine-__init__), [`AutonomousExploitEngine.enable_stealth`](modules.autonomous_exploit_engine.py.md#autonomousexploitengine-enable_stealth), [`AutonomousExploitEngine.full_auto_pwn`](modules.autonomous_exploit_engine.py.md#autonomousexploitengine-full_auto_pwn)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/auto_pwn.py:14](../../skills/mcp_tools/auto_pwn.py#L14)

```python
TOOL
```

---
