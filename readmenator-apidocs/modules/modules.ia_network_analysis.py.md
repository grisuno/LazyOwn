# `modules.ia_network_analysis`

> Source: [modules/ia_network_analysis.py:1](../../modules/ia_network_analysis.py#L1) | language `py` | coverage 80.0% | [API index](../index.md)

ia_network_analysis.py

Autor: grisun0
Fecha de creación: 30/01/2025
Licencia: AGPL v3

Descripción: Bot de monitoreo de tráfico de red en tiempo real.
             Informa todo el tráfico (IPs, puertos, protocolos) y usa DeepSeek para detectar actividad sospechosa.

## Contents

- **Functions:** [`analyze_with_deepseek`](#analyze_with_deepseek), [`packet_callback`](#packet_callback), [`start_monitoring`](#start_monitoring), [`parse_args`](#parse_args)
- **Constants:** [`DEEPSEEK_API_URL`](#deepseek_api_url), [`DEEPSEEK_MODEL`](#deepseek_model)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_ia_network_analysis_py__packet_callback(["packet_callback"])
    n_modules_ia_network_analysis_py__analyze_with_deepseek(["analyze_with_deepseek"])
    n_modules_ia_network_analysis_py__start_monitoring(["start_monitoring"])
    n_modules_ia_network_analysis_py__packet_callback --> n_modules_ia_network_analysis_py__analyze_with_deepseek
    n_modules_ia_network_analysis_py__start_monitoring --> n_modules_ia_network_analysis_py__packet_callback
```

## Functions

<a id="analyze_with_deepseek"></a>

### `analyze_with_deepseek`

`function` | [modules/ia_network_analysis.py:39](../../modules/ia_network_analysis.py#L39)

```python
def analyze_with_deepseek(packet_info, mode='console')
```

Envía la información del paquete a DeepSeek para análisis avanzado.

Devuelve la respuesta del modelo en chunks.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `packet_info` |  |  |  |
| `mode` |  | `'console'` |  |

*Called by:* [`packet_callback`](#packet_callback)

---

<a id="packet_callback"></a>

### `packet_callback`

`function` | [modules/ia_network_analysis.py:91](../../modules/ia_network_analysis.py#L91)

```python
def packet_callback(packet, mode='console')
```

Callback para procesar cada paquete capturado.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `packet` |  |  |  |
| `mode` |  | `'console'` |  |

*Calls:* [`analyze_with_deepseek`](#analyze_with_deepseek)

*Called by:* [`start_monitoring`](#start_monitoring)

---

<a id="start_monitoring"></a>

### `start_monitoring`

`function` | [modules/ia_network_analysis.py:130](../../modules/ia_network_analysis.py#L130)

```python
def start_monitoring(interface=None, timeout=30, mode='console')
```

Inicia el monitoreo del tráfico de red.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `interface` |  | `None` |  |
| `timeout` |  | `30` |  |
| `mode` |  | `'console'` |  |

*Calls:* [`packet_callback`](#packet_callback)

---

<a id="parse_args"></a>

### `parse_args`

`function` | [modules/ia_network_analysis.py:154](../../modules/ia_network_analysis.py#L154)

```python
def parse_args()
```

---

## Constants

<a id="deepseek_api_url"></a>

### `DEEPSEEK_API_URL`

`constant` | [modules/ia_network_analysis.py:33](../../modules/ia_network_analysis.py#L33)

```python
DEEPSEEK_API_URL = 'http://localhost:11434/api/generate'
```

---

<a id="deepseek_model"></a>

### `DEEPSEEK_MODEL`

`constant` | [modules/ia_network_analysis.py:34](../../modules/ia_network_analysis.py#L34)

```python
DEEPSEEK_MODEL = 'deepseek-r1:1.5b'
```

---
