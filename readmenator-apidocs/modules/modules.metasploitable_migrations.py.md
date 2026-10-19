# `modules.metasploitable_migrations`

> Source: [modules/metasploitable_migrations.py:1](../../modules/metasploitable_migrations.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Idempotent migrations for the Metasploitable 2 gym container.

The stock ``tleemcjr/metasploitable2`` image boots only a subset of the
services the gym matrix expects, and several exercises need small lab
adjustments (open X display, anonymous FTP, a deliberately vulnerable CGI
script, a PHP URL-include fixture and a populated mutillidae database).
Each migration below is idempotent: it first checks whether the fix is
already in place and only applies the change when it is not, so running
the migrations on every gym start is safe and cheap.

Execution goes through ``docker exec`` in argv form (no shell on the
operator side). Every step reports its own status; a failing step never
blocks the rest.

## Contents

- **Classes:** [`Migration`](#migration)
- **Functions:** [`build_migrations`](#build_migrations), [`apply_migrations`](#apply_migrations)
- **Constants:** [`DEFAULT_CONTAINER`](#default_container), [`DEFAULT_DOCKER_SUBNET`](#default_docker_subnet)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_metasploitable_migrations_py__build_migrations(["build_migrations"])
    n_modules_metasploitable_migrations_py__Migration(["Migration"])
    n_modules_metasploitable_migrations_py__apply_migrations(["apply_migrations"])
    n_modules_metasploitable_migrations_py__build_migrations --> n_modules_metasploitable_migrations_py__Migration
    n_modules_metasploitable_migrations_py__apply_migrations --> n_modules_metasploitable_migrations_py__build_migrations
```

## Classes

<a id="migration"></a>

### `Migration`

`class` `dataclass` | [modules/metasploitable_migrations.py:65](../../modules/metasploitable_migrations.py#L65)

Decorators: `@dataclass(frozen=True)`

```python
class Migration
```

One idempotent gym fix: a check script and an apply script.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`id`](#migration-id) | `str` |  | Stable migration identifier used in reports. |
| [`description`](#migration-description) | `str` |  | Human-readable summary. |
| [`check`](#migration-check) | `str` | `''` | Shell script run inside the container; exit 0 means the migration is already applied. |
| [`apply`](#migration-apply) | `str` | `''` | Shell script run inside the container when the check fails (or when there is no check). |
| [`payload`](#migration-payload) | `str` | `''` | Optional stdin content handed to the apply script (used by file-writing migrations with ``cat > path``). |

---

## Functions

<a id="build_migrations"></a>

### `build_migrations`

`function` | [modules/metasploitable_migrations.py:131](../../modules/metasploitable_migrations.py#L131)

```python
def build_migrations(subnet: str = DEFAULT_DOCKER_SUBNET) -> tuple[Migration, ...]
```

Return the ordered migration list with the docker subnet applied.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `subnet` | `str` | `DEFAULT_DOCKER_SUBNET` | IPv4 prefix of the lab docker network (hosts.allow entries use it as the trusted client list). |

**Returns:** `tuple[Migration, ...]` - Ordered tuple of [`Migration`](#migration) steps.

*Calls:* [`Migration`](#migration)

*Called by:* [`apply_migrations`](#apply_migrations)

---

<a id="apply_migrations"></a>

### `apply_migrations`

`function` | [modules/metasploitable_migrations.py:236](../../modules/metasploitable_migrations.py#L236)

```python
def apply_migrations(container: str = DEFAULT_CONTAINER, subnet: str = DEFAULT_DOCKER_SUBNET) -> dict[str, dict[str, Any]]
```

Run every migration on the gym container, skipping applied ones.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `container` | `str` | `DEFAULT_CONTAINER` | Gym container name. |
| `subnet` | `str` | `DEFAULT_DOCKER_SUBNET` | Docker subnet prefix handed to the hosts.allow entries. |

**Returns:** `dict[str, dict[str, Any]]` - Mapping of migration id to ``{"applied": bool, "skipped": bool,
"detail": str}``; ``applied`` reports the apply script's exit
status, ``skipped`` marks already-satisfied migrations.

*Calls:* [`build_migrations`](#build_migrations)

---

## Constants

<a id="default_container"></a>

### `DEFAULT_CONTAINER`

`constant` | [modules/metasploitable_migrations.py:23](../../modules/metasploitable_migrations.py#L23)

```python
DEFAULT_CONTAINER = 'lazyown-lab-metasploitable'
```

---

<a id="default_docker_subnet"></a>

### `DEFAULT_DOCKER_SUBNET`

`constant` | [modules/metasploitable_migrations.py:24](../../modules/metasploitable_migrations.py#L24)

```python
DEFAULT_DOCKER_SUBNET = '172.17.0.'
```

---
