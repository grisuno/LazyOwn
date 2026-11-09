# `skills.mcp_tools.campaign_sitrep`

> Source: [skills/mcp_tools/campaign_sitrep.py:1](../../skills/mcp_tools/campaign_sitrep.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

MCP tool ``lazyown_campaign_sitrep`` (migrated from the call_tool dispatch chain).

## Contents

- **Functions:** [`handle`](#handle)
- **Constants:** [`TOOL`](#tool)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_skills_mcp_tools_campaign_sitrep_py__handle(["handle"])
    n_modules_killchain_py__KillChain_current_phase["killchain.KillChain.current_phase"]
    n_skills_lazyown_mcp_helpers_py__evidence_freshness["lazyown_mcp_helpers.evidence_freshness"]
    n_skills_lazyown_mcp_helpers_py__is_likely_credential["lazyown_mcp_helpers.is_likely_credential"]
    n_skills_mcp_tools_campaign_sitrep_py__handle -.-> n_modules_killchain_py__KillChain_current_phase
    n_skills_mcp_tools_campaign_sitrep_py__handle -.-> n_skills_lazyown_mcp_helpers_py__evidence_freshness
    n_skills_mcp_tools_campaign_sitrep_py__handle -.-> n_skills_lazyown_mcp_helpers_py__is_likely_credential
```

## Functions

<a id="handle"></a>

### `handle`

`function` | [skills/mcp_tools/campaign_sitrep.py:46](../../skills/mcp_tools/campaign_sitrep.py#L46)

```python
def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list
```

Handle the lazyown_campaign_sitrep MCP tool.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arguments` | `dict[str, Any]` |  |  |
| `tool_name` | `str` |  |  |
| `ctx` | `MCPContext` |  |  |

**Returns:** `list`

*Calls:* [`KillChain.current_phase`](modules.killchain.py.md#killchain-current_phase), [`evidence_freshness`](skills.lazyown_mcp_helpers.py.md#evidence_freshness), [`is_likely_credential`](skills.lazyown_mcp_helpers.py.md#is_likely_credential)

---

## Constants

<a id="tool"></a>

### `TOOL`

`constant` | [skills/mcp_tools/campaign_sitrep.py:13](../../skills/mcp_tools/campaign_sitrep.py#L13)

```python
TOOL
```

---
