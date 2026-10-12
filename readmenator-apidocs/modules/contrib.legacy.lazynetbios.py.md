# `contrib.legacy.lazynetbios`

> Source: [contrib/legacy/lazynetbios.py:1](../../contrib/legacy/lazynetbios.py#L1) | language `py` | coverage 12.5% | [API index](../index.md)

main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: exploit netbios

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

## Contents

- **Functions:** [`check_sudo`](#check_sudo), [`signal_handler`](#signal_handler), [`scan_netbios`](#scan_netbios), [`check_arp`](#check_arp), [`check_netbios`](#check_netbios), [`send_nbns_spoof`](#send_nbns_spoof), [`generate_ip_range`](#generate_ip_range)

## Functions

<a id="check_sudo"></a>

### `check_sudo`

`function` | [contrib/legacy/lazynetbios.py:30](../../contrib/legacy/lazynetbios.py#L30)

```python
def check_sudo()
```

---

<a id="signal_handler"></a>

### `signal_handler`

`function` | [contrib/legacy/lazynetbios.py:38](../../contrib/legacy/lazynetbios.py#L38)

```python
def signal_handler(sig, frame)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sig` |  |  |  |
| `frame` |  |  |  |

---

<a id="scan_netbios"></a>

### `scan_netbios`

`function` | [contrib/legacy/lazynetbios.py:45](../../contrib/legacy/lazynetbios.py#L45)

```python
def scan_netbios(ip_range)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ip_range` |  |  |  |

---

<a id="check_arp"></a>

### `check_arp`

`function` | [contrib/legacy/lazynetbios.py:58](../../contrib/legacy/lazynetbios.py#L58)

```python
def check_arp(ip)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ip` |  |  |  |

---

<a id="check_netbios"></a>

### `check_netbios`

`function` | [contrib/legacy/lazynetbios.py:71](../../contrib/legacy/lazynetbios.py#L71)

```python
def check_netbios(ip)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ip` |  |  |  |

---

<a id="send_nbns_spoof"></a>

### `send_nbns_spoof`

`function` | [contrib/legacy/lazynetbios.py:90](../../contrib/legacy/lazynetbios.py#L90)

```python
def send_nbns_spoof(target_ip, target_name, spoof_ip, trans_id)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `target_ip` |  |  |  |
| `target_name` |  |  |  |
| `spoof_ip` |  |  |  |
| `trans_id` |  |  |  |

---

<a id="generate_ip_range"></a>

### `generate_ip_range`

`function` | [contrib/legacy/lazynetbios.py:115](../../contrib/legacy/lazynetbios.py#L115)

```python
def generate_ip_range(start_ip, end_ip)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `start_ip` |  |  |  |
| `end_ip` |  |  |  |

---
