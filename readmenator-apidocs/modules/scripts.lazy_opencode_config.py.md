# `scripts.lazy_opencode_config`

> Source: [scripts/lazy_opencode_config.py:1](../../scripts/lazy_opencode_config.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Patch operator agent configs to use the Lazy llama.cpp server.

Shared by ``scripts/lazy_llamacpp_setup.sh`` and the
``lazyown_opencode_config`` MCP tool so interactive and agentic flows
apply byte-identical merges. Every write backs the file up first and
never touches an existing setup without an explicit call.

Targets:
- ``opencode``: ``~/.config/opencode/opencode.json`` gains the
  ``llamacpp`` provider plus the ``local-model`` entry.
- ``hermes``: ``~/.hermes/config.yaml`` gains the ``llamacpp``
  provider entry and points the default model at it.

## Contents

- **Functions:** [`patch_opencode`](#patch_opencode), [`patch_hermes`](#patch_hermes)

## Functions

<a id="patch_opencode"></a>

### `patch_opencode`

`function` | [scripts/lazy_opencode_config.py:46](../../scripts/lazy_opencode_config.py#L46)

```python
def patch_opencode(set_default: bool = False, host: str = LLAMACPP_HOST) -> dict
```

Merge the llamacpp provider into the opencode config.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `set_default` | `bool` | `False` | Also set the top-level model to llamacpp/local-model. |
| `host` | `str` | `LLAMACPP_HOST` | Server base URL (``.../v1``). |

**Returns:** `dict` - Summary with changed flag, backup path and path. Never raises.

---

<a id="patch_hermes"></a>

### `patch_hermes`

`function` | [scripts/lazy_opencode_config.py:93](../../scripts/lazy_opencode_config.py#L93)

```python
def patch_hermes(host: str = LLAMACPP_HOST) -> dict
```

Point the hermes config at the local llama.cpp server.

Surgical merge: only the llamacpp provider entry and the default
model pointer are ensured; every other key (and the operator's own
provider fields like ``name``/``transport``) is preserved. The file
is rewritten only when a required value actually differs.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `host` | `str` | `LLAMACPP_HOST` | Server base URL (``.../v1``). |

**Returns:** `dict` - Summary with changed flag, backup path and path. Never raises.

---
