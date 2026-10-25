# `skills.mcp_lazy`

> Source: [skills/mcp_lazy.py:1](../../skills/mcp_lazy.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Single helper behind every lazy optional import of the MCP server.

Each ``_ensure_*`` wrapper in ``lazyown_mcp`` used to repeat the same
skeleton: return the cached flag when set, otherwise try the import,
bind names on success, store False on failure. Centralising the
skeleton here keeps one fail-closed policy (any import error disables
the feature instead of crashing the server) while every wrapper only
declares what to load.

## Contents

- **Functions:** [`ensure_optional`](#ensure_optional)

## Functions

<a id="ensure_optional"></a>

### `ensure_optional`

`function` | [skills/mcp_lazy.py:18](../../skills/mcp_lazy.py#L18)

```python
def ensure_optional(namespace: MutableMapping[str, Any], flag: str, loader: Loader) -> bool
```

Return the cached flag or run ``loader`` once to compute it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `namespace` | `MutableMapping[str, Any]` |  | Module globals holding the flag and bound names. |
| `flag` | `str` |  | Name of the availability flag inside ``namespace``. |
| `loader` | `Loader` |  | Receives ``namespace``; binds imported names into it and returns True on success, False when it installed a fallback stub instead. |

**Returns:** `bool` - True when the optional dependency is usable, False otherwise.
Any exception from ``loader`` fails closed to False.

---
