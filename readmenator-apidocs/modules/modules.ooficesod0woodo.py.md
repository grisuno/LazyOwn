# `modules.ooficesod0woodo`

> Source: [modules/ooficesod0woodo.py:1](../../modules/ooficesod0woodo.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

LibreOffice UNO remote command execution stager.

Connects to a StarOffice UNO socket bridge on the target and executes one
command through ``com.sun.star.system.SystemShellExecute``. Host, port and
command are CLI arguments so the PoC works as a reusable verb; defaults
preserve the original localhost:2002 behaviour.

## Contents

- **Functions:** [`main`](#main)

## Functions

<a id="main"></a>

### `main`

`function` | [modules/ooficesod0woodo.py:13](../../modules/ooficesod0woodo.py#L13)

```python
def main() -> None
```

Parse arguments, resolve the UNO bridge and execute the command.

**Raises**

- `SystemExit`: (raised in the body, not documented)

---
