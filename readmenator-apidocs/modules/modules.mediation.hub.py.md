# `modules.mediation.hub`

> Source: [modules/mediation/hub.py:1](../../modules/mediation/hub.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Thin routing hub for specialised mediators.

The hub owns no coordination logic: it is a registry keyed by domain so
callers request a mediator instead of importing its colleagues. Adding a
new domain never changes existing consumers.

## Contents

- **Classes:** [`MediationHub`](#mediationhub)
- **Functions:** [`default_hub`](#default_hub), [`get_hub`](#get_hub)

## Classes

<a id="mediationhub"></a>

### `MediationHub`

`class` | [modules/mediation/hub.py:19](../../modules/mediation/hub.py#L19)

```python
class MediationHub
```

Registry of specialised mediators keyed by domain.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#mediationhub-__init__) | constructor | Start with an empty registry. |
| [`register`](#mediationhub-register) | method | Register a mediator under its declared domain. |
| [`mediator_for`](#mediationhub-mediator_for) | method | Return the mediator registered for a domain key, or None. |
| [`snapshot`](#mediationhub-snapshot) | method | Return high-level metadata for every registered mediator. |

<a id="mediationhub-__init__"></a>

#### `MediationHub.__init__`

`constructor` | [modules/mediation/hub.py:22](../../modules/mediation/hub.py#L22)

```python
def __init__(self) -> None
```

Start with an empty registry.

<a id="mediationhub-register"></a>

#### `MediationHub.register`

`method` | [modules/mediation/hub.py:26](../../modules/mediation/hub.py#L26)

```python
def register(self, mediator: MediatorContract) -> None
```

Register a mediator under its declared domain.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `mediator` | `MediatorContract` |  | Specialised mediator whose ``domain`` attribute is the routing key. |

<a id="mediationhub-mediator_for"></a>

#### `MediationHub.mediator_for`

`method` | [modules/mediation/hub.py:35](../../modules/mediation/hub.py#L35)

```python
def mediator_for(self, domain: str) -> MediatorContract | None
```

Return the mediator registered for a domain key, or None.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `domain` | `str` |  | Routing key such as ``loop.intel`` or ``chain``. |

**Returns:** `MediatorContract | None` - The registered mediator, or None when absent.

<a id="mediationhub-snapshot"></a>

#### `MediationHub.snapshot`

`method` | [modules/mediation/hub.py:46](../../modules/mediation/hub.py#L46)

```python
def snapshot(self) -> dict[str, Any]
```

Return high-level metadata for every registered mediator.

**Returns:** `dict[str, Any]` - Mapping of domain key to the mediator's describe() document.

---

## Functions

<a id="default_hub"></a>

### `default_hub`

`function` | [modules/mediation/hub.py:73](../../modules/mediation/hub.py#L73)

```python
def default_hub() -> MediationHub
```

Return a fresh default-configured hub (test-safe, no singleton).

**Returns:** `MediationHub`

---

<a id="get_hub"></a>

### `get_hub`

`function` | [modules/mediation/hub.py:78](../../modules/mediation/hub.py#L78)

```python
def get_hub() -> MediationHub
```

Return the process-wide hub, building it on first use.

Thread-safe: concurrent first-touch callers race on construction and
the winner is shared.

**Returns:** `MediationHub` - The shared MediationHub instance or a retry-exhausted empty hub.

*Called by:* [`resolve`](modules.mediation.contracts.py.md#resolve)

---
