# `cli.tui_theme`

> Source: [cli/tui_theme.py:1](../../cli/tui_theme.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Operator-facing ``tui_theme`` command logic.

The cmd2 `[`do_tui_theme`](cli.commands.help_ui.py.md#helpuicommandset-do_tui_theme)` method in ``lazyown.py`` delegates to
[`run`](#run) here. Keeping the logic out of the shell makes it
trivially testable: pass a payload dict, a payload-saver callable,
and a sys.argv-style argument list, get back a human-readable
result string and a side effect on the payload.

Usage from the shell:

    tui_theme                    # list all themes, mark current
    tui_theme gruvbox            # switch active theme
    tui_theme cycle              # next theme in deterministic order
    tui_theme prev               # previous theme
    tui_theme reset              # fall back to default

The command is intentionally idempotent and never raises -- any
invalid input is reported to the operator without mutating state.

## Contents

- **Functions:** [`run`](#run)

## Functions

<a id="run"></a>

### `run`

`function` | [cli/tui_theme.py:87](../../cli/tui_theme.py#L87)

```python
def run(args: Sequence[str], payload: MutableMapping[str, object], save: Callable[[MutableMapping[str, object]], None]) -> str
```

Execute the ``tui_theme`` command.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `args` | `Sequence[str]` |  | Argument list (excluding the verb itself). Empty list lists themes; one positional argument switches or moves the active theme; ``reset`` clears back to default. |
| `payload` | `MutableMapping[str, object]` |  | Live payload mapping. Mutated in place on theme changes; the operator's selection persists across shell restarts because `save` writes the JSON. |
| `save` | `Callable[[MutableMapping[str, object]], None]` |  | Callable invoked after every mutation so the on-disk ``payload.json`` matches the in-memory state. The shell binds this to the existing payload writer; tests pass a no-op recorder. |

**Returns:** `str` - Human-readable result string. Always a single block of text
suitable for direct printing.

---
