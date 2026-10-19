# `scripts.mcp_call`

> Source: [scripts/mcp_call.py:1](../../scripts/mcp_call.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Call one LazyOwn MCP tool over stdio and print its text content.

Reusable hermes-style client used by operators, agents and tests:

    python3 scripts/mcp_call.py lazyown_campaign_sitrep '{"format":"json"}'
    python3 scripts/mcp_call.py lazyown_run_command         '{"command":"list","timeout":60}' --timeout 120

The MCP server is spawned from the repository that ships this script. The
interpreter is resolved portably: the first project virtualenv found
(``env``, ``venv``, ``.venv``) wins, otherwise the running interpreter is
reused. No user-specific absolute paths are ever written here. Parent
environment variables (``AUTO_USE_LLM``, ``AUTO_USE_SWAN``, credentials)
flow to the server subprocess unchanged, so the caller controls engine
toggles from the outside.

Exit codes: 0 tool answer printed, 1 tool answered with isError, 2 usage
error, 3 the ``mcp`` package is missing, 4 timeout or transport failure,
5 server-side exception relayed.

## Contents

- **Functions:** [`main`](#main)
- **Constants:** [`REPO_ROOT`](#repo_root), [`SERVER_RELATIVE_PATH`](#server_relative_path)

## Functions

<a id="main"></a>

### `main`

`function` | [scripts/mcp_call.py:173](../../scripts/mcp_call.py#L173)

```python
def main(argv: list[str] | None = None) -> int
```

Parse the CLI, execute one MCP tool and print its answer.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `argv` | `list[str] \| None` | `None` | Optional argv override for embedding callers. |

**Returns:** `int` - Process exit code using the documented exit-code contract.

**Raises**

- `SystemExit`: Only via the caller wiring; this function returns codes.

---

## Constants

<a id="repo_root"></a>

### `REPO_ROOT`

`constant` | [scripts/mcp_call.py:32](../../scripts/mcp_call.py#L32)

```python
REPO_ROOT = Path(__file__).resolve().parents[1]
```

---

<a id="server_relative_path"></a>

### `SERVER_RELATIVE_PATH`

`constant` | [scripts/mcp_call.py:33](../../scripts/mcp_call.py#L33)

```python
SERVER_RELATIVE_PATH = Path('skills') / 'lazyown_mcp.py'
```

---
