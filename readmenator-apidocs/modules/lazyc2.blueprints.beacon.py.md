# `lazyc2.blueprints.beacon`

> Source: [lazyc2/blueprints/beacon.py:1](../../lazyc2/blueprints/beacon.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Beacon communication blueprint for the LazyOwn C2 server.

Handles implant polling, command delivery, result collection, file transfer,
and beacon lifecycle events. Integrates the conditional hooks engine so
operator-defined automation rules fire on beacon connection/disconnection.

Registered from ``lazyc2.py`` without a prefix so the existing malleable
routes (``/command``, ``/upload``, etc.) stay at their original paths.

## Contents

- **Functions:** [`init_beacon_bp`](#init_beacon_bp), [`send_command`](#send_command), [`receive_result`](#receive_result), [`issue_command`](#issue_command)

## Functions

<a id="init_beacon_bp"></a>

### `init_beacon_bp`

`function` | [lazyc2/blueprints/beacon.py:35](../../lazyc2/blueprints/beacon.py#L35)

```python
def init_beacon_bp(commands: dict[str, str], results: dict[str, Any], commands_history: dict[str, list[str]], connected_clients: set[str], encrypt_fn, decrypt_fn, config, sessions_dir: str = 'sessions', route_malleable: str = '') -> None
```

Wire the blueprint to the C2 monolith's shared state.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `commands` | `dict[str, str]` |  | Shared command queue dict. |
| `results` | `dict[str, Any]` |  | Shared results dict. |
| `commands_history` | `dict[str, list[str]]` |  | Shared command history dict. |
| `connected_clients` | `set[str]` |  | Shared connected clients set. |
| `encrypt_fn` |  |  | AES encrypt callable. |
| `decrypt_fn` |  |  | AES decrypt callable. |
| `config` |  |  | LazyOwn Config instance. |
| `sessions_dir` | `str` | `'sessions'` | Path to sessions directory. |
| `route_malleable` | `str` | `''` | Malleable C2 route prefix. |

---

<a id="send_command"></a>

### `send_command`

`function` | [lazyc2/blueprints/beacon.py:111](../../lazyc2/blueprints/beacon.py#L111)

Decorators: `@beacon_bp.route('/command/<client_id>', methods=['GET'])`

```python
def send_command(client_id: str)
```

Implant polls for the next encrypted command.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client_id` | `str` |  |  |

---

<a id="receive_result"></a>

### `receive_result`

`function` | [lazyc2/blueprints/beacon.py:131](../../lazyc2/blueprints/beacon.py#L131)

Decorators: `@beacon_bp.route('/command/<client_id>', methods=['POST'])`

```python
def receive_result(client_id: str)
```

Implant reports command output.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `client_id` | `str` |  |  |

---

<a id="issue_command"></a>

### `issue_command`

`function` | [lazyc2/blueprints/beacon.py:245](../../lazyc2/blueprints/beacon.py#L245)

Decorators: `@beacon_bp.route('/issue_command', methods=['POST'])`

```python
def issue_command()
```

Operator queues a command for a connected implant.

---
