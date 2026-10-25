# `cli.commands.lab`

> Source: [cli/commands/lab.py:1](../../cli/commands/lab.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Lab environment commands -- spin up vulnerable practice targets.

Provides on-demand CTF-style lab scenarios powered by Docker containers.
Operators can practice techniques against realistic targets without
risking production systems. The Docker lifecycle lives in
[`modules.lab_runtime`](modules.lab_runtime.py.md); this command set owns the operator UX.

## Contents

- **Classes:** [`LabCommandSet`](#labcommandset)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class LabCommandSet
    LabCommandSet : phase
    LabCommandSet : category
    LabCommandSet : do_lab()
    class LazyOwnCommandSet
    LazyOwnCommandSet <|-- LabCommandSet
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_commands_lab_py__LabCommandSet_do_lab(["LabCommandSet.do_lab"])
    n_core_console_py__print_error["console.print_error"]
    n_core_console_py__print_msg["console.print_msg"]
    n_cli_commands_lab_py__LabCommandSet_do_lab -.-> n_core_console_py__print_error
    n_cli_commands_lab_py__LabCommandSet_do_lab -.-> n_core_console_py__print_msg
```

## Classes

<a id="labcommandset"></a>

### `LabCommandSet`

`class` | [cli/commands/lab.py:27](../../cli/commands/lab.py#L27)

```python
class LabCommandSet(LazyOwnCommandSet)
```

Bases: [`LazyOwnCommandSet`](cli.commands._base.py.md#lazyowncommandset)

Manage local CTF lab environments via Docker.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`phase`](#labcommandset-phase) |  | `'lab'` |  |
| [`category`](#labcommandset-category) |  | `'12. Miscellaneous'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`do_lab`](#labcommandset-do_lab) | method | Manage local CTF practice labs. |

<a id="labcommandset-do_lab"></a>

#### `LabCommandSet.do_lab`

`method` | [cli/commands/lab.py:93](../../cli/commands/lab.py#L93)

Decorators: `@cmd2.with_category(miscellaneous_category)`

```python
def do_lab(self, line)
```

Manage local CTF practice labs.

Usage:
    lab list                     — show available scenarios
    lab start <scenario>         — spin up a vulnerable target
    lab stop <scenario>          — tear down a running scenario
    lab status                   — show running labs
    lab range start <profile>    — start a cyber range (ad-mini)
    lab range stop <profile>     — stop a cyber range
    lab range status             — range container status
    lab range verify <profile>   — fire a real exploit to prove it works

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

**Example**

```python
lab start metasploitable
    lab start wordpress
    lab list
    lab status
    lab stop metasploitable
    lab range start ad-mini

Requires Docker. Lab containers are isolated and safe for practice.
```

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg)

---
