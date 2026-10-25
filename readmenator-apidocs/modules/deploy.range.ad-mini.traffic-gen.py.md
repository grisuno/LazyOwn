# `deploy.range.ad-mini.traffic-gen`

> Source: [deploy/range/ad-mini/traffic-gen.py:1](../../deploy/range/ad-mini/traffic-gen.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Fake network traffic generator for the AD mini range.

Emits periodic SMB/Kerberos-like TCP probes plus fake user logons so junior
operators practice implant deployment and lateral movement against a noisy,
legal, fully local background. Targets resolve over the compose network,
so no fixed subnet is required.

## Contents

- **Functions:** [`main`](#main)
- **Constants:** [`TARGETS`](#targets), [`USERS`](#users), [`BASE_DELAY`](#base_delay), [`JITTER`](#jitter)

## Functions

<a id="main"></a>

### `main`

`function` | [deploy/range/ad-mini/traffic-gen.py:35](../../deploy/range/ad-mini/traffic-gen.py#L35)

```python
def main() -> None
```

Loop forever emitting fake background traffic.

---

## Constants

<a id="targets"></a>

### `TARGETS`

`constant` | [deploy/range/ad-mini/traffic-gen.py:15](../../deploy/range/ad-mini/traffic-gen.py#L15)

```python
TARGETS = [('dc', 445), ('dc', 389), ('ws01', 80)]
```

---

<a id="users"></a>

### `USERS`

`constant` | [deploy/range/ad-mini/traffic-gen.py:16](../../deploy/range/ad-mini/traffic-gen.py#L16)

```python
USERS = ['jdoe', 'asmith', 'svc_backup', 'helpdesk', 'mgarcia']
```

---

<a id="base_delay"></a>

### `BASE_DELAY`

`constant` | [deploy/range/ad-mini/traffic-gen.py:17](../../deploy/range/ad-mini/traffic-gen.py#L17)

```python
BASE_DELAY = 30
```

---

<a id="jitter"></a>

### `JITTER`

`constant` | [deploy/range/ad-mini/traffic-gen.py:18](../../deploy/range/ad-mini/traffic-gen.py#L18)

```python
JITTER = 15
```

---
