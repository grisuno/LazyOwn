# `plugins/rundll32_sct_from_url.lua`

> Source: [plugins/rundll32_sct_from_url.lua:1](../../plugins/rundll32_sct_from_url.lua#L1) | language `lua` | coverage 40.0% | [API index](../index.md)

## Contents

- **Functions:** [`write_file`](#write_file), [`read_file`](#read_file), [`base64_encode`](#base64_encode), [`generate_sct`](#generate_sct)

## Functions

<a id="write_file"></a>

### `write_file`

`function` | [plugins/rundll32_sct_from_url.lua:4](../../plugins/rundll32_sct_from_url.lua#L4)

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

`function` | [plugins/rundll32_sct_from_url.lua:12](../../plugins/rundll32_sct_from_url.lua#L12)

```lua
local function read_file(path)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` |  |  |  |

---

<a id="base64_encode"></a>

### `base64_encode`

`function` | [plugins/rundll32_sct_from_url.lua:22](../../plugins/rundll32_sct_from_url.lua#L22)

```lua
local function base64_encode(data)
```

Base64 encode simple

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` |  |  |  |

---

<a id="generate_sct"></a>

### `generate_sct`

`function` | [plugins/rundll32_sct_from_url.lua:58](../../plugins/rundll32_sct_from_url.lua#L58)

```lua
local function generate_sct(lhost, xor_key, encoded_shellcode_b64)
```

Genera el archivo .sct (scriptlet) que ejecuta shellcode en memoria

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `lhost` |  |  |  |
| `xor_key` |  |  |  |
| `encoded_shellcode_b64` |  |  |  |

---
