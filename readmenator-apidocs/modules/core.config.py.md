# `core.config`

> Source: [core/config.py:1](../../core/config.py#L1) | language `py` | coverage 88.9% | [API index](../index.md)

Configuration loader and Config wrapper.

``payload.json`` is the single source of runtime configuration for the entire
LazyOwn framework. This module exposes:

- `[`PAYLOAD_PATH`](#payload_path)` constant pointing at ``payload.json`` in the current working
  directory.
- `[`load_payload`](#load_payload)` / `[`save_payload`](#save_payload)` for reading and writing it atomically.
- `[`Config`](#config)` — a thin attribute-style wrapper around the payload dictionary.
- `[`resolve_aes_key`](#resolve_aes_key)` — the AES key resolver used by `[`Config`](#config)` so the
  key is reachable from the shell, the C2, the MCP, and the lazyaddons
  templating.

Atomic writes go through ``*.tmp`` and ``os.replace`` so a crashed write never
leaves the operator with a corrupt payload file.

## Contents

- **Classes:** [`Config`](#config)
- **Functions:** [`resolve_aes_key`](#resolve_aes_key), [`load_payload`](#load_payload), [`load_and_validate`](#load_and_validate), [`save_payload`](#save_payload)
- **Constants:** [`PAYLOAD_FILENAME`](#payload_filename), [`PAYLOAD_PATH`](#payload_path), [`LAZYOWN_ENV_PREFIX`](#lazyown_env_prefix)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_core_config_py__Config___init__(["Config.__init__"])
    n_core_config_py__resolve_aes_key(["resolve_aes_key"])
    n_core_config_py__load_and_validate(["load_and_validate"])
    n_core_config_py__load_payload(["load_payload"])
    n_core_payload_schema_py__validate_payload["payload_schema.validate_payload"]
    n_core_config_py__Config___init__ --> n_core_config_py__resolve_aes_key
    n_core_config_py__load_and_validate --> n_core_config_py__load_payload
    n_core_config_py__load_and_validate -.-> n_core_payload_schema_py__validate_payload
```

## Classes

<a id="config"></a>

### `Config`

`class` | [core/config.py:206](../../core/config.py#L206)

```python
class Config
```

Attribute-style wrapper around a configuration dictionary.

Behavior is intentionally preserved from the legacy ``utils.Config``:
every key in the underlying dictionary becomes both an instance attribute
and is accessible via ``config[key]``. Missing keys via ``__getitem__``
return ``None`` rather than raising.

The instance also exposes ``aes_key`` (resolved bytes) and `[`as_params`](#config-as_params)`
(a snapshot of the underlying dictionary) so the LazyOwn shell can
substitute ``{{aes_key}}`` and other tokens in lazyaddons.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#config-__init__) | constructor |  |
| [`as_params`](#config-as_params) | method | Return a shallow copy of the underlying parameter dictionary. |
| [`overridden_keys`](#config-overridden_keys) | method | Return sorted list of keys that were overridden via ``LAZYOWN_*`` env vars. |

<a id="config-__init__"></a>

#### `Config.__init__`

`constructor` | [core/config.py:219](../../core/config.py#L219)

```python
def __init__(self, config_dict: dict[str, Any], sessions_dir: str | os.PathLike[str] | None = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `config_dict` | `dict[str, Any]` |  |  |
| `sessions_dir` | `str \| os.PathLike[str] \| None` | `None` |  |

*Calls:* [`resolve_aes_key`](#resolve_aes_key)

*Called by:* [`load_adversary`](utils.py.md#load_adversary)

<a id="config-as_params"></a>

#### `Config.as_params`

`method` | [core/config.py:234](../../core/config.py#L234)

```python
def as_params(self) -> dict[str, Any]
```

Return a shallow copy of the underlying parameter dictionary.

**Returns:** `dict[str, Any]` - A dict suitable for ``self.params`` on the cmd2 shell. The
``aes_key`` value is the hex string, matching the format
consumed by lazyaddon template substitution.

<a id="config-overridden_keys"></a>

#### `Config.overridden_keys`

`method` | [core/config.py:244](../../core/config.py#L244)

```python
def overridden_keys(self) -> list[str]
```

Return sorted list of keys that were overridden via ``LAZYOWN_*`` env vars.

**Returns:** `list[str]`

---

## Functions

<a id="resolve_aes_key"></a>

### `resolve_aes_key`

`function` | [core/config.py:261](../../core/config.py#L261)

```python
def resolve_aes_key(config_dict: dict[str, Any], *, sessions_dir: str | os.PathLike[str]) -> bytes
```

Return a 32-byte AES key derived from config, disk, or randomness.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `config_dict` | `dict[str, Any]` |  | The payload dictionary. Looks for an ``aes_key`` entry holding a 64-character hex string. |
| `sessions_dir` | `str \| os.PathLike[str]` |  | Directory holding ``key.aes``. Created if missing. |

**Returns:** `bytes` - Exactly 32 bytes suitable for AES-256.

**Raises**

- `ValueError`: when ``aes_key`` is present but not a 64-char hex.

*Called by:* [`Config.__init__`](#config-__init__), [`BeaconConfigBuilder.build`](modules.beacon_config_builder.py.md#beaconconfigbuilder-build)

---

<a id="load_payload"></a>

### `load_payload`

`function` | [core/config.py:327](../../core/config.py#L327)

```python
def load_payload(path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> dict[str, Any]
```

Load and return the JSON payload at ``path``.

If the payload does not exist but ``payload.example.json`` does, the
example file is copied to ``path`` automatically so a fresh clone never
leaves the operator without a starting configuration.

Environment variable overrides
(``LAZYOWN_<KEY>``) are applied on top of the file contents.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| os.PathLike[str]` | `PAYLOAD_FILENAME` |  |

**Returns:** `dict[str, Any]`

**Raises**

- `FileNotFoundError`: if neither the payload nor the example exists.
- `json.JSONDecodeError`: if the payload is not valid JSON.

*Called by:* [`load_aliases`](cli.aliases.py.md#load_aliases), [`BofMarketplaceCommandSet.do_bof_run`](cli.commands.bof_registry.py.md#bofmarketplacecommandset-do_bof_run), [`MiscMigratedCommandSet.do_config_banner`](cli.commands.misc_migrated.py.md#miscmigratedcommandset-do_config_banner), [`PurpleTeamCommandSet.do_purple_config`](cli.commands.purple_team.py.md#purpleteamcommandset-do_purple_config), [`SecurityCommandSet.do_opsec`](cli.commands.security.py.md#securitycommandset-do_opsec), [`SecurityCommandSet.do_rotate_aes`](cli.commands.security.py.md#securitycommandset-do_rotate_aes), [`SecurityCommandSet.do_seal_credentials`](cli.commands.security.py.md#securitycommandset-do_seal_credentials), [`SecurityCommandSet.do_unseal_credentials`](cli.commands.security.py.md#securitycommandset-do_unseal_credentials), [`load_and_validate`](#load_and_validate), [`get_defaults`](lazyc2.blueprints.api.py.md#get_defaults), [`set_default`](lazyc2.blueprints.api.py.md#set_default), [`LazyOwnShell.__init__`](lazyown.py.md#lazyownshell-__init__) and 13 more

---

<a id="load_and_validate"></a>

### `load_and_validate`

`function` | [core/config.py:345](../../core/config.py#L345)

```python
def load_and_validate(path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> dict[str, Any]
```

Load ``payload.json``, validate against the schema, and return a result dict.

Validation never raises: problems are collected in the ``warnings`` and
``errors`` lists of the result dict. The payload is returned in the
``payload`` key as loaded.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| os.PathLike[str]` | `PAYLOAD_FILENAME` | Filesystem location of the payload (defaults to ``payload.json`` in the current working directory). |

**Returns:** `dict[str, Any]` - A dict with keys:
- ``payload`` (``dict``): the loaded configuration dictionary.
- `[`valid`](modules.playbook_admin.py.md#playbookentry-valid)` (``bool``): ``True`` when no errors were found.
- ``warnings`` (``list[str]``): advisory issues (schema warnings,
  unresolved placeholders, default-looking values).
- ``errors`` (``list[str]``): blocking issues from schema
  validation.
- ``issues`` (``list[ValidationIssue]``): structured schema issues
  for programmatic consumers (preserves backward compat).

*Calls:* [`load_payload`](#load_payload), [`validate_payload`](core.payload_schema.py.md#validate_payload)

---

<a id="save_payload"></a>

### `save_payload`

`function` | [core/config.py:396](../../core/config.py#L396)

```python
def save_payload(payload: dict[str, Any], path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> None
```

Atomically write ``payload`` as pretty-printed JSON to ``path``.

Uses a sibling ``*.tmp`` file plus ``os.replace`` so a crash mid-write
cannot leave the operator with a half-written payload.

Configuration changes are audited to ``sessions/config_changes.jsonl``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `dict[str, Any]` |  |  |
| `path` | `str \| os.PathLike[str]` | `PAYLOAD_FILENAME` |  |

*Called by:* [`McpBridgeCommandSet.do_auto_populate`](cli.commands.mcp_bridge.py.md#mcpbridgecommandset-do_auto_populate), [`PurpleTeamCommandSet.do_purple_config`](cli.commands.purple_team.py.md#purpleteamcommandset-do_purple_config), [`SecurityCommandSet.do_rotate_aes`](cli.commands.security.py.md#securitycommandset-do_rotate_aes), [`SecurityCommandSet.do_seal_credentials`](cli.commands.security.py.md#securitycommandset-do_seal_credentials), [`SecurityCommandSet.do_unseal_credentials`](cli.commands.security.py.md#securitycommandset-do_unseal_credentials), [`OrchestratorAssetsMixin.save_config`](cli.orchestrator_assets_tabs.py.md#orchestratorassetsmixin-save_config), [`OrchestratorAssetsMixin.save_guardrails`](cli.orchestrator_assets_tabs.py.md#orchestratorassetsmixin-save_guardrails), [`set_default`](lazyc2.blueprints.api.py.md#set_default), [`LazyOwnShell.preloop`](lazyown.py.md#lazyownshell-preloop), [`set_full_cli`](modules.lazy_cli_bridge.py.md#set_full_cli), [`set_installer_enabled`](modules.lazy_installer.py.md#set_installer_enabled)

---

## Constants

<a id="payload_filename"></a>

### `PAYLOAD_FILENAME`

`constant` | [core/config.py:32](../../core/config.py#L32)

```python
PAYLOAD_FILENAME = 'payload.json'
```

---

<a id="payload_path"></a>

### `PAYLOAD_PATH`

`constant` | [core/config.py:33](../../core/config.py#L33)

```python
PAYLOAD_PATH = Path(PAYLOAD_FILENAME)
```

---

<a id="lazyown_env_prefix"></a>

### `LAZYOWN_ENV_PREFIX`

`constant` | [core/config.py:40](../../core/config.py#L40)

```python
LAZYOWN_ENV_PREFIX = 'LAZYOWN_'
```

---
