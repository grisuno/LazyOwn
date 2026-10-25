# `modules.hive_invoke`

> Source: [modules/hive_invoke.py:1](../../modules/hive_invoke.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

modules/hive_invoke.py ======================= Invokes Claude Code CLI with the LazyOwn MCP server and forwards an operator prompt for autonomous or hive-mind execution.

Claude Code will have access to the lazyown MCP server (configured in
~/.claude.json) and will use its tools to fulfil the request.

Usage (via hive addon)
----------------------
  hive enumerate all SMB shares on 10.10.11.78
  hive spawn 3 drones to perform AD enumeration
  hive start autonomous mode targeting 10.10.11.78
  hive what hosts and credentials have been captured so far
  hive -i enumerate Active Directory on 10.10.11.78  (interactive mode)

Usage (direct)
--------------
  python3 modules/hive_invoke.py [OPTIONS] <prompt words ...>

Options
-------
  -i, --interactive     Open Claude Code in interactive REPL mode so the
                        operator can follow up after the initial response.
                        Default: non-interactive print mode (-p).
  -e, --effort LEVEL    Effort level passed to Claude: low | medium | high | max
                        Default: high.
  -h, --help            Show this help message and exit.

Exit codes
----------
  0   Claude executed successfully.
  1   Missing prompt or claude binary not found.
  2   Claude returned a non-zero exit code.

## Contents

- **Functions:** [`main`](#main)

## Functions

<a id="main"></a>

### `main`

`function` | [modules/hive_invoke.py:255](../../modules/hive_invoke.py#L255)

```python
def main(argv: list[str] | None = None) -> int
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `argv` | `list[str] \| None` | `None` |  |

**Returns:** `int`

---
