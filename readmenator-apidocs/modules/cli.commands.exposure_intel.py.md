# `cli.commands.exposure_intel`

> Source: [cli/commands/exposure_intel.py:1](../../cli/commands/exposure_intel.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Target-aware exploit-intelligence exposure command set.

``lazyintel`` binds the discovered world-model services to a local exploit
feed with hard-evidence policy, prints the ranked exposure report and
publishes its outcome through the [`modules.outcome_bus`](modules.outcome_bus.py.md) fan-out so
the C2 surfaces, intel graph and reports stay current.

Subcommands:
    lazyintel [target]                  ranked exposure report
    lazyintel [target] --check          rendered read-only validation commands
    lazyintel --feed <path>             feed override for this run

## Contents

- **Classes:** [`LazyIntelCommandSet`](#lazyintelcommandset)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class LazyIntelCommandSet
    LazyIntelCommandSet : phase
    LazyIntelCommandSet : category
    LazyIntelCommandSet : do_lazyintel()
    class LazyOwnCommandSet
    LazyOwnCommandSet <|-- LazyIntelCommandSet
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel(["LazyIntelCommandSet.do_lazyintel"])
    n_core_console_py__print_error["console.print_error"]
    n_core_console_py__print_msg["console.print_msg"]
    n_core_console_py__print_succ["console.print_succ"]
    n_core_validators_py__check_rhost["validators.check_rhost"]
    n_modules_lazy_exposure_py__generate_report["lazy_exposure.generate_report"]
    n_modules_lazy_exposure_py__publish_report["lazy_exposure.publish_report"]
    n_modules_lazy_exposure_py__save_report["lazy_exposure.save_report"]
    n_modules_lazy_feedmatch_py__load_feed["lazy_feedmatch.load_feed"]
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_core_console_py__print_error
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_core_console_py__print_msg
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_core_console_py__print_succ
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_core_validators_py__check_rhost
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_modules_lazy_exposure_py__generate_report
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_modules_lazy_exposure_py__publish_report
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_modules_lazy_exposure_py__save_report
    n_cli_commands_exposure_intel_py__LazyIntelCommandSet_do_lazyintel -.-> n_modules_lazy_feedmatch_py__load_feed
```

## Classes

<a id="lazyintelcommandset"></a>

### `LazyIntelCommandSet`

`class` | [cli/commands/exposure_intel.py:32](../../cli/commands/exposure_intel.py#L32)

```python
class LazyIntelCommandSet(LazyOwnCommandSet)
```

Bases: [`LazyOwnCommandSet`](cli.commands._base.py.md#lazyowncommandset)

Expose lazy_intel to the operator.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`phase`](#lazyintelcommandset-phase) |  | `'recon'` |  |
| [`category`](#lazyintelcommandset-category) |  | `miscellaneous_category` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`do_lazyintel`](#lazyintelcommandset-do_lazyintel) | method | Rank discovered services against local exploit intelligence. |

<a id="lazyintelcommandset-do_lazyintel"></a>

#### `LazyIntelCommandSet.do_lazyintel`

`method` | [cli/commands/exposure_intel.py:39](../../cli/commands/exposure_intel.py#L39)

Decorators: `@cmd2.with_category(miscellaneous_category)`

```python
def do_lazyintel(self, line: str) -> None
```

Rank discovered services against local exploit intelligence.

Usage:
    lazyintel [target] [--check] [--feed <path>] [--json] [--quiet]

Without a target the current ``rhost`` is used. The feed defaults to
``sessions/intel/exploit_feed.json`` (or ``intel_feed`` from
``payload.json``) and cisa KEV dumps are accepted as-is.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` | `str` |  |  |

*Calls:* [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg), [`print_succ`](core.console.py.md#print_succ), [`check_rhost`](core.validators.py.md#check_rhost), [`generate_report`](modules.lazy_exposure.py.md#generate_report), [`publish_report`](modules.lazy_exposure.py.md#publish_report), [`save_report`](modules.lazy_exposure.py.md#save_report), [`load_feed`](modules.lazy_feedmatch.py.md#load_feed)

---
