# `contrib.legacy.lazy_packet_image_sniffer`

> Source: [contrib/legacy/lazy_packet_image_sniffer.py:1](../../contrib/legacy/lazy_packet_image_sniffer.py#L1) | language `py` | coverage 0.0% | [API index](../index.md)

## Contents

- **Functions:** [`check_sudo`](#check_sudo), [`list_interfaces`](#list_interfaces), [`choose_interface`](#choose_interface), [`get_subnet_from_interface`](#get_subnet_from_interface), [`get_ip_addresses`](#get_ip_addresses), [`handle_packet`](#handle_packet), [`save_image`](#save_image), [`run`](#run), [`daemonize`](#daemonize)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_contrib_legacy_lazy_packet_image_sniffer_py__handle_packet(["handle_packet"])
    n_contrib_legacy_lazy_packet_image_sniffer_py__save_image(["save_image"])
    n_contrib_legacy_lazy_packet_image_sniffer_py__handle_packet --> n_contrib_legacy_lazy_packet_image_sniffer_py__save_image
```

## Functions

<a id="check_sudo"></a>

### `check_sudo`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:23](../../contrib/legacy/lazy_packet_image_sniffer.py#L23)

```python
def check_sudo()
```

---

<a id="list_interfaces"></a>

### `list_interfaces`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:31](../../contrib/legacy/lazy_packet_image_sniffer.py#L31)

```python
def list_interfaces()
```

---

<a id="choose_interface"></a>

### `choose_interface`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:49](../../contrib/legacy/lazy_packet_image_sniffer.py#L49)

```python
def choose_interface(interfaces)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `interfaces` |  |  |  |

---

<a id="get_subnet_from_interface"></a>

### `get_subnet_from_interface`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:61](../../contrib/legacy/lazy_packet_image_sniffer.py#L61)

```python
def get_subnet_from_interface(interface)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `interface` |  |  |  |

---

<a id="get_ip_addresses"></a>

### `get_ip_addresses`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:65](../../contrib/legacy/lazy_packet_image_sniffer.py#L65)

```python
def get_ip_addresses(interface)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `interface` |  |  |  |

---

<a id="handle_packet"></a>

### `handle_packet`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:111](../../contrib/legacy/lazy_packet_image_sniffer.py#L111)

```python
def handle_packet(packet)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `packet` |  |  |  |

*Calls:* [`save_image`](#save_image)

---

<a id="save_image"></a>

### `save_image`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:161](../../contrib/legacy/lazy_packet_image_sniffer.py#L161)

```python
def save_image(src_ip, end_idx)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `src_ip` |  |  |  |
| `end_idx` |  |  |  |

*Called by:* [`handle_packet`](#handle_packet)

---

<a id="run"></a>

### `run`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:187](../../contrib/legacy/lazy_packet_image_sniffer.py#L187)

```python
def run()
```

---

<a id="daemonize"></a>

### `daemonize`

`function` | [contrib/legacy/lazy_packet_image_sniffer.py:192](../../contrib/legacy/lazy_packet_image_sniffer.py#L192)

```python
def daemonize()
```

---
