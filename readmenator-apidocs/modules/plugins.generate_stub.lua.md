# `plugins/generate_stub.lua`

> Source: [plugins/generate_stub.lua:1](../../plugins/generate_stub.lua#L1) | language `lua` | coverage 50.0% | [API index](../index.md)

## Contents

- **Functions:** [`write_file`](#write_file), [`read_file`](#read_file), [`xor_data`](#xor_data), [`xor_string`](#xor_string), [`generate_stub_ps1`](#generate_stub_ps1)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_plugins_generate_stub_lua__generate_stub_ps1(["generate_stub_ps1"])
    n_plugins_generate_stub_lua__xor_string(["xor_string"])
    n_plugins_generate_stub_lua__generate_stub_ps1 --> n_plugins_generate_stub_lua__xor_string
```

## Functions

<a id="write_file"></a>

### `write_file`

`function` | [plugins/generate_stub.lua:4](../../plugins/generate_stub.lua#L4)

```lua
local function write_file(path, content)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` |  |  |  |
| `content` |  |  |  |

---

<a id="read_file"></a>

### `read_file`

`function` | [plugins/generate_stub.lua:12](../../plugins/generate_stub.lua#L12)

```lua
local function read_file(path)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` |  |  |  |

---

<a id="xor_data"></a>

### `xor_data`

`function` | [plugins/generate_stub.lua:21](../../plugins/generate_stub.lua#L21)

```lua
local function xor_data(data, key)
```

Aplica XOR a datos binarios

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` |  |  |  |
| `key` |  |  |  |

---

<a id="xor_string"></a>

### `xor_string`

`function` | [plugins/generate_stub.lua:30](../../plugins/generate_stub.lua#L30)

```lua
local function xor_string(str, key)
```

Ofusca string para C# (bytes XOR)

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `str` |  |  |  |
| `key` |  |  |  |

*Called by:* [`generate_stub_ps1`](#generate_stub_ps1)

---

<a id="generate_stub_ps1"></a>

### `generate_stub_ps1`

`function` | [plugins/generate_stub.lua:43](../../plugins/generate_stub.lua#L43)

```lua
local function generate_stub_ps1(lhost, xor_key_hex)
```

=== Genera el script PowerShell con C# embebido (CORREGIDO) ===

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `lhost` |  |  |  |
| `xor_key_hex` |  |  |  |

*Calls:* [`xor_string`](#xor_string)

---
