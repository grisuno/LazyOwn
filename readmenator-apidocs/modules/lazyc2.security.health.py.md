# `lazyc2.security.health`

> Source: [lazyc2/security/health.py:1](../../lazyc2/security/health.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Health report assembly for the LazyOwn C2 web layer.

Contract: probes always run and their results always drive the aggregated
status and HTTP code, but the detailed `[`checks`](cli.doctor.py.md#doctorreport-checks)` (and ``daemon``) payloads
are only included when ``detailed`` is true (loopback caller or
authenticated operator). Building `[`checks`](cli.doctor.py.md#doctorreport-checks)` in a dedicated structure
guarantees a remote caller always receives a valid aggregated response
instead of a 500 when details are withheld.

## Contents

- **Functions:** [`gather_health`](#gather_health), [`build_health_report`](#build_health_report)

## Functions

<a id="gather_health"></a>

### `gather_health`

`function` | [lazyc2/security/health.py:20](../../lazyc2/security/health.py#L20)

```python
def gather_health(probes: Sequence[tuple[str, Callable[[], str]]], on_error: Callable[[str, BaseException], None] | None = None) -> dict[str, str]
```

Run every probe and collect per-check statuses.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `probes` | `Sequence[tuple[str, Callable[[], str]]]` |  | Sequence of ``(name, probe)`` pairs; ``probe`` returns the status string (``"ok"``, ``"stopped"``, ...) or raises. |
| `on_error` | `Callable[[str, BaseException], None] \| None` | `None` | Optional logging hook called with the check name and the raised exception. |

**Returns:** `dict[str, str]` - Mapping of check name to status string (``"error"`` on failure).

---

<a id="build_health_report"></a>

### `build_health_report`

`function` | [lazyc2/security/health.py:46](../../lazyc2/security/health.py#L46)

```python
def build_health_report(checks: Mapping[str, str], detailed: bool = False, daemon_status: Any = None) -> tuple[dict[str, Any], int]
```

Assemble the JSON payload and HTTP code for the health endpoint.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `checks` | `Mapping[str, str]` |  | Collected per-check statuses. |
| `detailed` | `bool` | `False` | Whether to include the `[`checks`](cli.doctor.py.md#doctorreport-checks)` map and ``daemon`` status in the response body. |
| `daemon_status` | `Any` | `None` | Optional daemon status payload (only embedded when ``detailed`` is true). |

**Returns:** `tuple[dict[str, Any], int]` - Tuple ``(payload, status_code)``; the code is 503 when any check
differs from ``"ok"``, else 200.

---
