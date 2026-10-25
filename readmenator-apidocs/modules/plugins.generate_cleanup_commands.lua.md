# `plugins/generate_cleanup_commands.lua`

> Source: [plugins/generate_cleanup_commands.lua:1](../../plugins/generate_cleanup_commands.lua#L1) | language `lua` | coverage 50.0% | [API index](../index.md)

## Contents

- **Functions:** [`generate_cleanup_commands`](#generate_cleanup_commands)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_plugins_generate_cleanup_commands_lua__generate_cleanup_commands(["generate_cleanup_commands"])
    n_cli_ops_commands_py__LootEntry_value["ops_commands.LootEntry.value"]
    n_plugins_generate_cleanup_commands_lua__generate_cleanup_commands -.-> n_cli_ops_commands_py__LootEntry_value
```

## Functions

<a id="generate_cleanup_commands"></a>

### `generate_cleanup_commands`

`function` | [plugins/generate_cleanup_commands.lua:3](../../plugins/generate_cleanup_commands.lua#L3)

```lua
function generate_cleanup_commands(arg_string)
```

The main plugin function for generating cleanup commands NOW expects ONE string argument containing all key=value pairs

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `arg_string` |  |  |  |

*Calls:* [`LootEntry.value`](cli.ops_commands.py.md#lootentry-value)

---
