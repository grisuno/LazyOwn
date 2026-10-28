# `modules.lab_runtime`

> Source: [modules/lab_runtime.py:1](../../modules/lab_runtime.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Lab runtime: Docker lifecycle for practice targets and cyber ranges.

Pure subprocess-free-of-shell lifecycle helpers shared by the ``lab``
command set, the gym challenge starter and the exit cleanup hook. Every
command runs in argv list form (``shell=False`` semantics) with bounded
timeouts; nothing here talks to a shell.

Scenarios live in [`LAB_SCENARIOS`](#lab_scenarios); cyber range profiles in
[`RANGE_PROFILES`](#range_profiles). Containers are named ``lazyown-lab-<scenario>``
so the cleanup pass can find every machine the framework launched.

## Contents

- **Functions:** [`docker_available`](#docker_available), [`running_containers`](#running_containers), [`existing_containers`](#existing_containers), [`running_range_containers`](#running_range_containers), [`container_name`](#container_name), [`container_ip`](#container_ip), [`ensure_web`](#ensure_web), [`apply_gym_migrations`](#apply_gym_migrations), [`start`](#start), [`stop`](#stop), [`stop_all`](#stop_all), [`range_compose`](#range_compose), [`start_range`](#start_range), [`stop_range`](#stop_range), [`stop_ranges`](#stop_ranges), [`ensure_range_secret`](#ensure_range_secret)
- **Constants:** [`BASE_DIR`](#base_dir), [`LAB_COMPOSE`](#lab_compose), [`RANGE_DIR`](#range_dir), [`REGISTRY_PREFIX`](#registry_prefix), [`RANGE_PREFIX`](#range_prefix), [`LAB_SCENARIOS`](#lab_scenarios), [`RANGE_PROFILES`](#range_profiles)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_lab_runtime_py__start(["start"])
    n_modules_lab_runtime_py__container_ip(["container_ip"])
    n_modules_lab_runtime_py__container_name(["container_name"])
    n_modules_lab_runtime_py__ensure_web(["ensure_web"])
    n_modules_lab_runtime_py__existing_containers(["existing_containers"])
    n_modules_lab_runtime_py__running_containers(["running_containers"])
    n_modules_lab_runtime_py__stop(["stop"])
    n_modules_lab_runtime_py__stop_all(["stop_all"])
    n_modules_lab_runtime_py__start_range(["start_range"])
    n_modules_lab_runtime_py__ensure_range_secret(["ensure_range_secret"])
    n_modules_lab_runtime_py__range_compose(["range_compose"])
    n_modules_lab_runtime_py__stop_range(["stop_range"])
    n_modules_lab_runtime_py__stop_ranges(["stop_ranges"])
    n_modules_lab_runtime_py__running_range_containers(["running_range_containers"])
    n_modules_lab_runtime_py__start --> n_modules_lab_runtime_py__container_ip
    n_modules_lab_runtime_py__start --> n_modules_lab_runtime_py__container_name
    n_modules_lab_runtime_py__start --> n_modules_lab_runtime_py__ensure_web
    n_modules_lab_runtime_py__start --> n_modules_lab_runtime_py__existing_containers
    n_modules_lab_runtime_py__start --> n_modules_lab_runtime_py__running_containers
    n_modules_lab_runtime_py__stop --> n_modules_lab_runtime_py__container_name
    n_modules_lab_runtime_py__stop --> n_modules_lab_runtime_py__running_containers
    n_modules_lab_runtime_py__stop_all --> n_modules_lab_runtime_py__running_containers
    n_modules_lab_runtime_py__start_range --> n_modules_lab_runtime_py__ensure_range_secret
    n_modules_lab_runtime_py__start_range --> n_modules_lab_runtime_py__range_compose
    n_modules_lab_runtime_py__stop_range --> n_modules_lab_runtime_py__range_compose
    n_modules_lab_runtime_py__stop_ranges --> n_modules_lab_runtime_py__range_compose
    n_modules_lab_runtime_py__stop_ranges --> n_modules_lab_runtime_py__running_range_containers
```

## Functions

<a id="docker_available"></a>

### `docker_available`

`function` | [modules/lab_runtime.py:93](../../modules/lab_runtime.py#L93)

```python
def docker_available() -> bool
```

Return whether the Docker daemon is reachable.

**Returns:** `bool`

---

<a id="running_containers"></a>

### `running_containers`

`function` | [modules/lab_runtime.py:115](../../modules/lab_runtime.py#L115)

```python
def running_containers() -> list[str]
```

Return the running lab container names.

**Returns:** `list[str]`

*Called by:* [`start`](#start), [`stop`](#stop), [`stop_all`](#stop_all)

---

<a id="existing_containers"></a>

### `existing_containers`

`function` | [modules/lab_runtime.py:131](../../modules/lab_runtime.py#L131)

```python
def existing_containers() -> list[str]
```

Return every lab container name including stopped ones.

**Returns:** `list[str]`

*Called by:* [`start`](#start)

---

<a id="running_range_containers"></a>

### `running_range_containers`

`function` | [modules/lab_runtime.py:148](../../modules/lab_runtime.py#L148)

```python
def running_range_containers() -> list[str]
```

Return the running cyber range container names.

**Returns:** `list[str]`

*Called by:* [`stop_ranges`](#stop_ranges)

---

<a id="container_name"></a>

### `container_name`

`function` | [modules/lab_runtime.py:164](../../modules/lab_runtime.py#L164)

```python
def container_name(scenario: str) -> str
```

Return the container name for one lab scenario.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `scenario` | `str` |  |  |

**Returns:** `str`

*Called by:* [`start`](#start), [`stop`](#stop)

---

<a id="container_ip"></a>

### `container_ip`

`function` | [modules/lab_runtime.py:169](../../modules/lab_runtime.py#L169)

```python
def container_ip(container_name: str) -> str
```

Resolve one container's IPv4 on its Docker network.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `container_name` | `str` |  |  |

**Returns:** `str`

*Called by:* [`readiness`](modules.ad_gym.py.md#readiness), [`start`](#start)

---

<a id="ensure_web"></a>

### `ensure_web`

`function` | [modules/lab_runtime.py:183](../../modules/lab_runtime.py#L183)

```python
def ensure_web(scenario: str, name: str) -> None
```

Start Apache inside a metasploitable container that booted without it.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `scenario` | `str` |  |  |
| `name` | `str` |  |  |

*Called by:* [`start`](#start)

---

<a id="apply_gym_migrations"></a>

### `apply_gym_migrations`

`function` | [modules/lab_runtime.py:242](../../modules/lab_runtime.py#L242)

```python
def apply_gym_migrations(name: str) -> dict
```

Apply the metasploitable gym migrations, returning the report.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `dict`

---

<a id="start"></a>

### `start`

`function` | [modules/lab_runtime.py:250](../../modules/lab_runtime.py#L250)

```python
def start(scenario: str) -> dict
```

Spin up one lab scenario container.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `scenario` | `str` |  | Scenario key from [`LAB_SCENARIOS`](#lab_scenarios). |

**Returns:** `dict` - Mapping with ``success``, ``already``, ``container``, ``ip``,
`[`ports`](modules.enrich.py.md#enrichresult-ports)` and ``error`` keys.

*Calls:* [`container_ip`](#container_ip), [`container_name`](#container_name), [`ensure_web`](#ensure_web), [`existing_containers`](#existing_containers), [`running_containers`](#running_containers)

---

<a id="stop"></a>

### `stop`

`function` | [modules/lab_runtime.py:304](../../modules/lab_runtime.py#L304)

```python
def stop(scenario: str) -> dict
```

Stop one lab scenario container.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `scenario` | `str` |  | Scenario key from [`LAB_SCENARIOS`](#lab_scenarios). |

**Returns:** `dict` - Mapping with ``success`` and ``error`` keys.

*Calls:* [`container_name`](#container_name), [`running_containers`](#running_containers)

---

<a id="stop_all"></a>

### `stop_all`

`function` | [modules/lab_runtime.py:322](../../modules/lab_runtime.py#L322)

```python
def stop_all() -> dict
```

Stop every running lab container.

**Returns:** `dict` - Mapping with ``stopped`` (container name list) and ``failed``
(name to error) keys.

*Calls:* [`running_containers`](#running_containers)

---

<a id="range_compose"></a>

### `range_compose`

`function` | [modules/lab_runtime.py:340](../../modules/lab_runtime.py#L340)

```python
def range_compose(profile: str) -> Path | None
```

Return the compose file path for one range profile, or None.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `profile` | `str` |  |  |

**Returns:** `Path | None`

*Called by:* [`start_range`](#start_range), [`stop_range`](#stop_range), [`stop_ranges`](#stop_ranges)

---

<a id="start_range"></a>

### `start_range`

`function` | [modules/lab_runtime.py:349](../../modules/lab_runtime.py#L349)

```python
def start_range(profile: str) -> dict
```

Start one cyber range profile via Docker Compose.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `profile` | `str` |  | Range profile key from [`RANGE_PROFILES`](#range_profiles). |

**Returns:** `dict` - Mapping with ``success``, ``compose`` and ``error`` keys.

*Calls:* [`ensure_range_secret`](#ensure_range_secret), [`range_compose`](#range_compose)

---

<a id="stop_range"></a>

### `stop_range`

`function` | [modules/lab_runtime.py:368](../../modules/lab_runtime.py#L368)

```python
def stop_range(profile: str) -> dict
```

Stop one cyber range profile (compose down).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `profile` | `str` |  |  |

**Returns:** `dict`

*Calls:* [`range_compose`](#range_compose)

---

<a id="stop_ranges"></a>

### `stop_ranges`

`function` | [modules/lab_runtime.py:379](../../modules/lab_runtime.py#L379)

```python
def stop_ranges() -> dict
```

Stop every running cyber range.

Tries ``docker compose down`` for declared profiles first; any
remaining ``lazyown-range-*`` containers fall back to ``docker stop``.

**Returns:** `dict` - Mapping with ``stopped`` and ``failed`` keys.

*Calls:* [`range_compose`](#range_compose), [`running_range_containers`](#running_range_containers)

*Called by:* [`cleanup_gym_machines`](modules.gym_cleanup.py.md#cleanup_gym_machines)

---

<a id="ensure_range_secret"></a>

### `ensure_range_secret`

`function` | [modules/lab_runtime.py:420](../../modules/lab_runtime.py#L420)

```python
def ensure_range_secret(profile_dir: Path) -> str
```

Generate the DC admin secret file when missing.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `profile_dir` | `Path` |  | Range profile directory holding the compose file. |

**Returns:** `str` - The Administrator password string, or empty on failure.

*Called by:* [`start_range`](#start_range)

---

## Constants

<a id="base_dir"></a>

### `BASE_DIR`

`constant` | [modules/lab_runtime.py:22](../../modules/lab_runtime.py#L22)

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

---

<a id="lab_compose"></a>

### `LAB_COMPOSE`

`constant` | [modules/lab_runtime.py:23](../../modules/lab_runtime.py#L23)

```python
LAB_COMPOSE = BASE_DIR / 'deploy' / 'lab' / 'docker-compose.yml'
```

---

<a id="range_dir"></a>

### `RANGE_DIR`

`constant` | [modules/lab_runtime.py:24](../../modules/lab_runtime.py#L24)

```python
RANGE_DIR = BASE_DIR / 'deploy' / 'range'
```

---

<a id="registry_prefix"></a>

### `REGISTRY_PREFIX`

`constant` | [modules/lab_runtime.py:26](../../modules/lab_runtime.py#L26)

```python
REGISTRY_PREFIX = 'lazyown-lab-'
```

---

<a id="range_prefix"></a>

### `RANGE_PREFIX`

`constant` | [modules/lab_runtime.py:27](../../modules/lab_runtime.py#L27)

```python
RANGE_PREFIX = 'lazyown-range-'
```

---

<a id="lab_scenarios"></a>

### `LAB_SCENARIOS`

`constant` | [modules/lab_runtime.py:42](../../modules/lab_runtime.py#L42)

```python
LAB_SCENARIOS: dict[str, dict]
```

---

<a id="range_profiles"></a>

### `RANGE_PROFILES`

`constant` | [modules/lab_runtime.py:83](../../modules/lab_runtime.py#L83)

```python
RANGE_PROFILES: dict[str, dict]
```

---
