# `lazyc2.security.trusted_proxy`

> Source: [lazyc2/security/trusted_proxy.py:1](../../lazyc2/security/trusted_proxy.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Trusted proxy resolver for the LazyOwn C2 web layer.

Contract: this module decides what the real client IP is, taking the
``X-Forwarded-For`` chain into account only when the operator has
declared one or more trusted reverse proxies in front of the C2.

Invariants:

1. When ``trusted_count == 0`` the resolver ignores
   ``X-Forwarded-For`` entirely and returns ``remote_addr``.
2. When ``trusted_count > 0`` the chain is parsed right-to-left; the
   rightmost `[`trusted_count`](#trustedproxyresolver-trusted_count)` entries are considered proxy hops and
   discarded, and the leftmost remaining address is returned.
3. When the chain is shorter than `[`trusted_count`](#trustedproxyresolver-trusted_count)` the resolver falls
   back to ``remote_addr`` rather than trusting a spoofed header.
4. ``is_operator(ip)`` does an exact-string comparison against the
   configured allowlist.

Config keys owned:

- ``c2_trusted_proxy_count`` (int, default ``0``)
- ``c2_operator_ip_allowlist`` (CSV string, default ``"127.0.0.1,{lhost}"``)

## Contents

- **Classes:** [`TrustedProxyResolver`](#trustedproxyresolver)

## Classes

<a id="trustedproxyresolver"></a>

### `TrustedProxyResolver`

`class` | [lazyc2/security/trusted_proxy.py:30](../../lazyc2/security/trusted_proxy.py#L30)

```python
class TrustedProxyResolver
```

Resolve the real client IP from Flask's ``request`` data.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `trusted_count` |  |  | Number of trusted reverse proxies in front of the C2. Set to ``0`` to disable header parsing. |
| `operator_allowlist` |  |  | Iterable of operator IPs eligible for operator-only routes. |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#trustedproxyresolver-__init__) | constructor |  |
| [`trusted_count`](#trustedproxyresolver-trusted_count) | property | Return the configured number of trusted proxy hops. |
| [`client_ip`](#trustedproxyresolver-client_ip) | method | Return the resolved client IP. |
| [`is_operator`](#trustedproxyresolver-is_operator) | method | Return ``True`` when ``ip`` is in the operator allowlist. |

<a id="trustedproxyresolver-__init__"></a>

#### `TrustedProxyResolver.__init__`

`constructor` | [lazyc2/security/trusted_proxy.py:42](../../lazyc2/security/trusted_proxy.py#L42)

```python
def __init__(self, trusted_count: int, operator_allowlist: Iterable[str]) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `trusted_count` | `int` |  | Number of trusted reverse proxies in front of the C2. Set to ``0`` to disable header parsing. |
| `operator_allowlist` | `Iterable[str]` |  | Iterable of operator IPs eligible for operator-only routes. |

**Raises**

- `ValueError`: (raised in the body, not documented)

<a id="trustedproxyresolver-trusted_count"></a>

#### `TrustedProxyResolver.trusted_count`

`property` | [lazyc2/security/trusted_proxy.py:53](../../lazyc2/security/trusted_proxy.py#L53)

Decorators: `@property`

```python
def trusted_count(self) -> int
```

Return the configured number of trusted proxy hops.

**Returns:** `int`

<a id="trustedproxyresolver-client_ip"></a>

#### `TrustedProxyResolver.client_ip`

`method` | [lazyc2/security/trusted_proxy.py:57](../../lazyc2/security/trusted_proxy.py#L57)

```python
def client_ip(self, remote_addr: str | None, x_forwarded_for: str | None = None) -> str
```

Return the resolved client IP.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `remote_addr` | `str \| None` |  | Flask's ``request.remote_addr``. |
| `x_forwarded_for` | `str \| None` | `None` | The ``X-Forwarded-For`` header value or ``None`` if missing. |

**Returns:** `str` - The resolved IP string. Never empty.

<a id="trustedproxyresolver-is_operator"></a>

#### `TrustedProxyResolver.is_operator`

`method` | [lazyc2/security/trusted_proxy.py:80](../../lazyc2/security/trusted_proxy.py#L80)

```python
def is_operator(self, ip: str | None) -> bool
```

Return ``True`` when ``ip`` is in the operator allowlist.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ip` | `str \| None` |  | The IP string to test, typically the value returned by [`client_ip`](#trustedproxyresolver-client_ip). |

**Returns:** `bool` - ``True`` for an exact-string match against the allowlist.

---
