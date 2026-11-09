# `skills.mcp_tools.cve_search`

> Source: [skills/mcp_tools/cve_search.py:1](../../skills/mcp_tools/cve_search.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_cve_search`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_cve_search_py__handle(["handle"])
    n_modules_cve_matcher_py__CVEMatcher___init__["cve_matcher.CVEMatcher.__init__"]
    n_modules_cve_matcher_py__CVEMatcher_search["cve_matcher.CVEMatcher.search"]
    n_skills_mcp_tools_cve_search_py__handle -.-> n_modules_cve_matcher_py__CVEMatcher___init__
    n_skills_mcp_tools_cve_search_py__handle -.-> n_modules_cve_matcher_py__CVEMatcher_search
```

## Functions

<a id="handle"></a>

### `handle`

`function` `async` | [skills/mcp_tools/cve_search.py:42](../../skills/mcp_tools/cve_search.py#L42)

```python
async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_cve_search MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`CVEMatcher.__init__`](modules.cve_matcher.py.md#cvematcher-__init__), [`CVEMatcher.search`](modules.cve_matcher.py.md#cvematcher-search)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/cve_search.py:12](../../skills/mcp_tools/cve_search.py#L12)

```python
TOOL
```

---
