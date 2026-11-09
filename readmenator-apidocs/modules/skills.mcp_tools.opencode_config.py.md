# `skills.mcp_tools.opencode_config`

> Source: [skills/mcp_tools/opencode_config.py:1](../../skills/mcp_tools/opencode_config.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_opencode_config``: point opencode/hermes at llama.cpp.

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_opencode_config_py__handle(["handle"])
    n_scripts_lazy_opencode_config_py__patch_hermes["lazy_opencode_config.patch_hermes"]
    n_scripts_lazy_opencode_config_py__patch_opencode["lazy_opencode_config.patch_opencode"]
    n_skills_mcp_tools_opencode_config_py__handle -.-> n_scripts_lazy_opencode_config_py__patch_hermes
    n_skills_mcp_tools_opencode_config_py__handle -.-> n_scripts_lazy_opencode_config_py__patch_opencode
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/opencode_config.py:38](../../skills/mcp_tools/opencode_config.py#L38)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Patch opencode/hermes configs to the local llama.cpp server.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`patch_hermes`](scripts.lazy_opencode_config.py.md#patch_hermes), [`patch_opencode`](scripts.lazy_opencode_config.py.md#patch_opencode)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/opencode_config.py:12](../../skills/mcp_tools/opencode_config.py#L12)

```python
TOOL
```

---
