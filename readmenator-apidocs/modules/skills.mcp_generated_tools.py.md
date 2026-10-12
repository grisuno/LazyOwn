# `skills.mcp_generated_tools`

> Source: [skills/mcp_generated_tools.py:1](../../skills/mcp_generated_tools.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Auto-generated MCP tool handlers from command_index.json.

DO NOT EDIT BY HAND.  Re-generate with:
    python3 skills/mcp_tool_generator.py

This file is imported by lazyown_mcp.py to close the coverage gap between the 148 hand-written handlers and the 670+ CLI commands.

## Contents

- **Functions:** [`get_generated_tool_definitions`](#get_generated_tool_definitions), [`register_all_generated_handlers`](#register_all_generated_handlers)

## Functions

<a id="get_generated_tool_definitions"></a>

### `get_generated_tool_definitions`

`function` | [skills/mcp_generated_tools.py:659](../../skills/mcp_generated_tools.py#L659)

```python
def get_generated_tool_definitions() -> list
```

Return list[types.Tool] entries for all generated tools.

**Returns:** `list`

---

<a id="register_all_generated_handlers"></a>

### `register_all_generated_handlers`

`function` | [skills/mcp_generated_tools.py:684](../../skills/mcp_generated_tools.py#L684)

```python
def register_all_generated_handlers(register_handler_fn, make_text_fn, run_lazyown_cmd_fn) -> int
```

Register every generated handler via *register_handler_fn*.

Called by lazyown_mcp.py after its infrastructure is ready. Returns the count registered.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `register_handler_fn` |  |  |  |
| `make_text_fn` |  |  |  |
| `run_lazyown_cmd_fn` |  |  |  |

**Returns:** `int`

---
