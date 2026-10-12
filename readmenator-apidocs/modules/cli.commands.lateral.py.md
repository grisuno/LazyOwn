# `cli.commands.lateral`

> Source: [cli/commands/lateral.py:1](../../cli/commands/lateral.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Lateral Movement command set (pending).

Phase 08 — commands for lateral movement: tunneling, pivoting,
remote execution, and protocol-specific lateral movement tools.

Pending status: inherits from [`PendingCommandSet`](cli.commands._dormancy.py.md#pendingcommandset). Promote to
[`LazyOwnCommandSet`](cli.commands._base.py.md#lazyowncommandset) once originals are deleted from ``lazyown.py``.

## Contents

- **Classes:** [`LateralMovementCommandSet`](#lateralmovementcommandset)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class LateralMovementCommandSet
    LateralMovementCommandSet : phase
    LateralMovementCommandSet : category
    LateralMovementCommandSet : do_socat()
    LateralMovementCommandSet : do_chisel()
    LateralMovementCommandSet : do_set_proxychains()
    LateralMovementCommandSet : do_ngrok()
    LateralMovementCommandSet : do_ligolo()
    LateralMovementCommandSet : do_nc()
    LateralMovementCommandSet : do_wmiexec()
    LateralMovementCommandSet : do_ssh()
    class LazyOwnCommandSet
    LazyOwnCommandSet <|-- LateralMovementCommandSet
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_socat(["LateralMovementCommandSet.do_socat"])
    n_core_console_py__print_msg["console.print_msg"]
    n_core_validators_py__check_lhost["validators.check_lhost"]
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_chisel(["LateralMovementCommandSet.do_chisel"])
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_set_proxychains(["LateralMovementCommandSet.do_set_proxychains"])
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_ngrok(["LateralMovementCommandSet.do_ngrok"])
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_ligolo(["LateralMovementCommandSet.do_ligolo"])
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_nc(["LateralMovementCommandSet.do_nc"])
    n_core_validators_py__check_rhost["validators.check_rhost"]
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_wmiexec(["LateralMovementCommandSet.do_wmiexec"])
    n_core_console_py__print_error["console.print_error"]
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_ssh(["LateralMovementCommandSet.do_ssh"])
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_socat -.-> n_core_console_py__print_msg
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_socat -.-> n_core_validators_py__check_lhost
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_chisel -.-> n_core_console_py__print_msg
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_chisel -.-> n_core_validators_py__check_lhost
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_set_proxychains -.-> n_core_console_py__print_msg
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_set_proxychains -.-> n_core_validators_py__check_lhost
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_ngrok -.-> n_core_console_py__print_msg
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_ligolo -.-> n_core_validators_py__check_lhost
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_nc -.-> n_core_console_py__print_msg
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_nc -.-> n_core_validators_py__check_rhost
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_wmiexec -.-> n_core_console_py__print_error
    n_cli_commands_lateral_py__LateralMovementCommandSet_do_ssh -.-> n_core_validators_py__check_rhost
```

## Classes

<a id="lateralmovementcommandset"></a>

### `LateralMovementCommandSet`

`class` | [cli/commands/lateral.py:24](../../cli/commands/lateral.py#L24)

```python
class LateralMovementCommandSet(LazyOwnCommandSet)
```

Bases: [`LazyOwnCommandSet`](cli.commands._base.py.md#lazyowncommandset)

Lateral Movement phase commands (pending).

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`phase`](#lateralmovementcommandset-phase) |  | `'lateral'` |  |
| [`category`](#lateralmovementcommandset-category) |  | `'08. Lateral Movement'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`do_socat`](#lateralmovementcommandset-do_socat) | method | Run socat for port forwarding. |
| [`do_chisel`](#lateralmovementcommandset-do_chisel) | method | Run chisel for quick tunneling. |
| [`do_set_proxychains`](#lateralmovementcommandset-do_set_proxychains) | method | Configure proxychains for the current session. |
| [`do_ngrok`](#lateralmovementcommandset-do_ngrok) | method | Start ngrok tunnel. |
| [`do_ligolo`](#lateralmovementcommandset-do_ligolo) | method | Run Ligolo-ng for advanced pivoting. |
| [`do_nc`](#lateralmovementcommandset-do_nc) | method | Netcat listener or connect. |
| [`do_wmiexec`](#lateralmovementcommandset-do_wmiexec) | method | Execute commands via WMI. |
| [`do_ssh`](#lateralmovementcommandset-do_ssh) | method | SSH to a remote host (custom port). |

<a id="lateralmovementcommandset-do_socat"></a>

#### `LateralMovementCommandSet.do_socat`

`method` | [cli/commands/lateral.py:31](../../cli/commands/lateral.py#L31)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_socat(self, line)
```

Run socat for port forwarding.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_msg`](core.console.py.md#print_msg), [`check_lhost`](core.validators.py.md#check_lhost)

<a id="lateralmovementcommandset-do_chisel"></a>

#### `LateralMovementCommandSet.do_chisel`

`method` | [cli/commands/lateral.py:43](../../cli/commands/lateral.py#L43)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_chisel(self, line)
```

Run chisel for quick tunneling.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_msg`](core.console.py.md#print_msg), [`check_lhost`](core.validators.py.md#check_lhost)

<a id="lateralmovementcommandset-do_set_proxychains"></a>

#### `LateralMovementCommandSet.do_set_proxychains`

`method` | [cli/commands/lateral.py:59](../../cli/commands/lateral.py#L59)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_set_proxychains(self, line)
```

Configure proxychains for the current session.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_msg`](core.console.py.md#print_msg), [`check_lhost`](core.validators.py.md#check_lhost)

<a id="lateralmovementcommandset-do_ngrok"></a>

#### `LateralMovementCommandSet.do_ngrok`

`method` | [cli/commands/lateral.py:72](../../cli/commands/lateral.py#L72)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_ngrok(self, line)
```

Start ngrok tunnel.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_msg`](core.console.py.md#print_msg)

<a id="lateralmovementcommandset-do_ligolo"></a>

#### `LateralMovementCommandSet.do_ligolo`

`method` | [cli/commands/lateral.py:79](../../cli/commands/lateral.py#L79)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_ligolo(self, line)
```

Run Ligolo-ng for advanced pivoting.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`check_lhost`](core.validators.py.md#check_lhost)

<a id="lateralmovementcommandset-do_nc"></a>

#### `LateralMovementCommandSet.do_nc`

`method` | [cli/commands/lateral.py:91](../../cli/commands/lateral.py#L91)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_nc(self, line)
```

Netcat listener or connect.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_msg`](core.console.py.md#print_msg), [`check_rhost`](core.validators.py.md#check_rhost)

<a id="lateralmovementcommandset-do_wmiexec"></a>

#### `LateralMovementCommandSet.do_wmiexec`

`method` | [cli/commands/lateral.py:106](../../cli/commands/lateral.py#L106)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_wmiexec(self, line)
```

Execute commands via WMI.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error)

<a id="lateralmovementcommandset-do_ssh"></a>

#### `LateralMovementCommandSet.do_ssh`

`method` | [cli/commands/lateral.py:114](../../cli/commands/lateral.py#L114)

Decorators: `@cmd2.with_category(lateral_movement_category)`

```python
def do_ssh(self, line)
```

SSH to a remote host (custom port).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`check_rhost`](core.validators.py.md#check_rhost)

---
