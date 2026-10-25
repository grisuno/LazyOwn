# `cli.confirm`

> Source: [cli/confirm.py:1](../../cli/confirm.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Shared interactive confirmation helpers with safe non-TTY behaviour.

Every interactive prompt in the CLI should go through [`confirm`](#confirm) so
agent-driven sessions (stdin closed or non-interactive) degrade gracefully
instead of crashing with ``EOFError`` or hanging on a prompt that can never
be answered.

Behaviour matrix:

    - TTY stdin: prompt and wait for y/n.
    - Non-TTY stdin (pipe/EOF): return ``default`` immediately.
    - Empty answer: return ``default``.

## Contents

- **Functions:** [`confirm`](#confirm)

## Functions

<a id="confirm"></a>

### `confirm`

`function` | [cli/confirm.py:27](../../cli/confirm.py#L27)

```python
def confirm(question: str, default: bool = False, yes_values: frozenset[str] = frozenset({'y', 'yes', 's', 'si'})) -> bool
```

Ask a yes/no question, never raising on non-interactive stdin.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `question` | `str` |  | The question to show (a trailing `` [y/N] `` is appended). |
| `default` | `bool` | `False` | Answer returned when stdin is not a TTY or input is empty. |
| `yes_values` | `frozenset[str]` | `frozenset({'y', 'yes', 's', 'si'})` | Case-insensitive answers treated as yes. |

**Returns:** `bool` - True when the operator answered yes, False otherwise.

*Called by:* [`AiCommandSet.do_llm_budget`](cli.commands.ai.py.md#aicommandset-do_llm_budget), [`CloudCommandSet.do_cloud_iam`](cli.commands.cloud.py.md#cloudcommandset-do_cloud_iam)

---
