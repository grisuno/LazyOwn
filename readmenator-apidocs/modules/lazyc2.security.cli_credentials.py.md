# `lazyc2.security.cli_credentials`

> Source: [lazyc2/security/cli_credentials.py:1](../../lazyc2/security/cli_credentials.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

CLI boot credentials: owner-only credential file and RBAC registration.

The C2 boot block resolves one effective (user, password) pair and must
persist it for the operator and register it in the RBAC store, so a
fresh lab run is never locked out of its own C2. No Flask imports here
so tests import this module directly.

## Contents

- **Functions:** [`write_credentials_file`](#write_credentials_file), [`resolve_boot_credentials`](#resolve_boot_credentials), [`register_cli_user`](#register_cli_user)
- **Constants:** [`CREDENTIALS_FILE`](#credentials_file)

## Functions

<a id="write_credentials_file"></a>

### `write_credentials_file`

`function` | [lazyc2/security/cli_credentials.py:22](../../lazyc2/security/cli_credentials.py#L22)

```python
def write_credentials_file(username: str, password: str, path: str | Path = CREDENTIALS_FILE) -> Path
```

Persist the effective boot credentials owner-only.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `username` | `str` |  | Effective C2 username. |
| `password` | `str` |  | Effective C2 password. |
| `path` | `str \| Path` | `CREDENTIALS_FILE` | Destination (``.c2_credentials.txt`` by default). |

**Returns:** `Path` - The written file path.

**Raises**

- `OSError`: When the file cannot be written.

---

<a id="resolve_boot_credentials"></a>

### `resolve_boot_credentials`

`function` | [lazyc2/security/cli_credentials.py:47](../../lazyc2/security/cli_credentials.py#L47)

```python
def resolve_boot_credentials(user: str, password: str, rotate_on_boot: bool, generator, is_insecure) -> tuple[str, str, str]
```

Resolve the effective boot credentials.

Rotation wins over keeping: an explicit ``rotate_on_boot`` flag
regenerates the pair every run, then insecure pairs are regenerated,
and only strong pairs without the flag are kept as-is.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `user` | `str` |  | Incoming username. |
| `password` | `str` |  | Incoming password. |
| `rotate_on_boot` | `bool` |  | Force regeneration every boot (config flag). |
| `generator` |  |  | Callable returning a fresh ``(user, password)``. |
| `is_insecure` |  |  | Predicate ``(user, password) -> bool``. |

**Returns:** `tuple[str, str, str]` - ``(user, password, action)`` with ``action`` in
``{"kept", "rotated_insecure", "rotated_on_boot"}``.

---

<a id="register_cli_user"></a>

### `register_cli_user`

`function` | [lazyc2/security/cli_credentials.py:80](../../lazyc2/security/cli_credentials.py#L80)

```python
def register_cli_user(store, username: str, password: str, hash_password, create_role: str = 'admin') -> str
```

Register or update the boot CLI user in an RBAC store.

An existing account for the username gets its password refreshed;
a new username is created with ``create_role``. An unreadable store
is left untouched so corrupted operator state is never overwritten.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `store` |  |  | RBAC store exposing `[`find_by_username`](modules.lazy_rbac.py.md#rbacstore-find_by_username)`/``save``/ `[`create_user`](modules.lazy_rbac.py.md#rbacstore-create_user)`. |
| `username` | `str` |  | Effective boot username. |
| `password` | `str` |  | Effective boot password (plain). |
| `hash_password` |  |  | Callable turning a plain password into a hash. |
| `create_role` | `str` | `'admin'` | Role for accounts created here. |

**Returns:** `str` - ``"updated"``, ``"created"`` or ``"skipped_unreadable"``.

---

## Constants

<a id="credentials_file"></a>

### `CREDENTIALS_FILE`

`constant` | [lazyc2/security/cli_credentials.py:18](../../lazyc2/security/cli_credentials.py#L18)

```python
CREDENTIALS_FILE = '.c2_credentials.txt'
```

---
