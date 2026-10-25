# `core.profiles`

> Source: [core/profiles.py:1](../../core/profiles.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Runtime profiles: ``light`` vs ``full`` installations.

The profile selects how much of the framework is expected to be present:

- ``full`` (default): every current behavior. Shell, C2, recon, analytics,
  and optional AI/LLM features that degrade gracefully when their packages
  are missing.
- ``light``: shell + C2 + recon core without the analytics and AI stack.
  The installer skips the heavy data/AI distributions and ``doctor`` does
  not require them.

Selection is explicit and never guessed: the ``LAZYOWN_PROFILE`` environment
variable wins, otherwise ``full`` applies. Anything else is a
`ValueError` so typos fail loudly instead of silently changing behavior.

## Contents

- **Functions:** [`active_profile`](#active_profile), [`is_light`](#is_light), [`specs_for_profile`](#specs_for_profile)
- **Constants:** [`PROFILE_LIGHT`](#profile_light), [`PROFILE_FULL`](#profile_full), [`PROFILE_ENV_VAR`](#profile_env_var), [`LIGHT_SKIPPED_IMPORTS`](#light_skipped_imports)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_core_profiles_py__is_light(["is_light"])
    n_core_profiles_py__active_profile(["active_profile"])
    n_core_profiles_py__specs_for_profile(["specs_for_profile"])
    n_core_profiles_py__is_light --> n_core_profiles_py__active_profile
    n_core_profiles_py__specs_for_profile --> n_core_profiles_py__is_light
```

## Functions

<a id="active_profile"></a>

### `active_profile`

`function` | [core/profiles.py:40](../../core/profiles.py#L40)

```python
def active_profile() -> str
```

Return the selected runtime profile.

**Returns:** `str` - ``"light"`` when ``LAZYOWN_PROFILE=light`` (case-insensitive,
surrounding whitespace ignored), otherwise ``"full"``.

**Raises**

- `ValueError`: When ``LAZYOWN_PROFILE`` is set to anything else.

*Called by:* [`is_light`](#is_light)

---

<a id="is_light"></a>

### `is_light`

`function` | [core/profiles.py:59](../../core/profiles.py#L59)

```python
def is_light() -> bool
```

Return ``True`` when the light profile is selected.

**Returns:** `bool`

*Calls:* [`active_profile`](#active_profile)

*Called by:* [`specs_for_profile`](#specs_for_profile)

---

<a id="specs_for_profile"></a>

### `specs_for_profile`

`function` | [core/profiles.py:64](../../core/profiles.py#L64)

```python
def specs_for_profile(specs: Sequence[_SpecT]) -> list[_SpecT]
```

Filter dependency specs down to the ones the active profile needs.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `specs` | `Sequence[_SpecT]` |  | [`cli.doctor.PackageSpec`](cli.doctor.py.md#packagespec) entries (or any objects with an ``import_name`` attribute). |

**Returns:** `list[_SpecT]` - Full list under the full profile; the list minus
[`LIGHT_SKIPPED_IMPORTS`](#light_skipped_imports) under the light profile.

*Calls:* [`is_light`](#is_light)

*Called by:* [`gather_report`](cli.doctor.py.md#gather_report)

---

## Constants

<a id="profile_light"></a>

### `PROFILE_LIGHT`

`constant` | [core/profiles.py:25](../../core/profiles.py#L25)

```python
PROFILE_LIGHT = 'light'
```

---

<a id="profile_full"></a>

### `PROFILE_FULL`

`constant` | [core/profiles.py:26](../../core/profiles.py#L26)

```python
PROFILE_FULL = 'full'
```

---

<a id="profile_env_var"></a>

### `PROFILE_ENV_VAR`

`constant` | [core/profiles.py:27](../../core/profiles.py#L27)

```python
PROFILE_ENV_VAR = 'LAZYOWN_PROFILE'
```

---

<a id="light_skipped_imports"></a>

### `LIGHT_SKIPPED_IMPORTS`

`constant` | [core/profiles.py:31](../../core/profiles.py#L31)

```python
LIGHT_SKIPPED_IMPORTS = frozenset({'pandas', 'pyarrow', 'networkx', 'groq'})
```

Import names ``doctor`` does not check under the light profile.

``pandas``/``pyarrow``/``networkx`` back reports, parquet bases, and graphs;
``groq`` backs the optional LLM provider. None of them is needed to run the
shell, the C2, or recon, so a light install is healthy without them.

---
