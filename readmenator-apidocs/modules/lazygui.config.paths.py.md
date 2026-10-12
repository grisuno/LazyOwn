# `lazygui.config.paths`

> Source: [lazygui/config/paths.py:1](../../lazygui/config/paths.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Filesystem layout resolver.

The application stores user-specific data under the platform-appropriate
config directory and reads project-relative resources from the repository
root. All path resolution flows through [`AppPaths`](#apppaths) so tests can swap
locations and so nothing downstream embeds an absolute path.

## Contents

- **Classes:** [`AppPaths`](#apppaths)

## Classes

<a id="apppaths"></a>

### `AppPaths`

`class` `dataclass` | [lazygui/config/paths.py:19](../../lazygui/config/paths.py#L19)

Decorators: `@dataclass(frozen=True, slots=True)`

```python
class AppPaths
```

Resolved filesystem locations for runtime artefacts.

The constructor derives every path from the supplied [`AppConstants`](lazygui.config.constants.py.md#appconstants)
and the current environment, so a test can override `[`home_dir`](#apppaths-home_dir)` or the
`[`project_root`](#apppaths-project_root)` without monkey-patching the rest of the application.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`constants`](#apppaths-constants) | `AppConstants` |  |  |
| [`project_root`](#apppaths-project_root) | `Path` | `field(default_factory=lambda: _detect_project_root())` |  |
| [`home_dir`](#apppaths-home_dir) | `Path` | `field(default_factory=Path.home)` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`config_dir`](#apppaths-config_dir) | property | User config directory respecting ``XDG_CONFIG_HOME`` when set. |
| [`settings_file`](#apppaths-settings_file) | property | Absolute path of the persisted settings JSON file. |
| [`layout_file`](#apppaths-layout_file) | property | Absolute path of the persisted Qt layout binary blob. |
| [`project_run_script`](#apppaths-project_run_script) | property | Absolute path to the ``run`` shell launcher in the repository. |
| [`lazyc2_script`](#apppaths-lazyc2_script) | property | Absolute path to the Flask backend ``lazyc2.py``. |
| [`c2_credentials_path`](#apppaths-c2_credentials_path) | property | Absolute path to the C2 auto-generated credentials file. |
| [`sessions_dir`](#apppaths-sessions_dir) | property | Absolute path to the sessions directory. |
| [`ensure_config_dir`](#apppaths-ensure_config_dir) | method | Create the config directory if missing and return it. |

<a id="apppaths-config_dir"></a>

#### `AppPaths.config_dir`

`property` | [lazygui/config/paths.py:32](../../lazygui/config/paths.py#L32)

Decorators: `@property`

```python
def config_dir(self) -> Path
```

User config directory respecting ``XDG_CONFIG_HOME`` when set.

**Returns:** `Path`

<a id="apppaths-settings_file"></a>

#### `AppPaths.settings_file`

`property` | [lazygui/config/paths.py:39](../../lazygui/config/paths.py#L39)

Decorators: `@property`

```python
def settings_file(self) -> Path
```

Absolute path of the persisted settings JSON file.

**Returns:** `Path`

<a id="apppaths-layout_file"></a>

#### `AppPaths.layout_file`

`property` | [lazygui/config/paths.py:44](../../lazygui/config/paths.py#L44)

Decorators: `@property`

```python
def layout_file(self) -> Path
```

Absolute path of the persisted Qt layout binary blob.

**Returns:** `Path`

<a id="apppaths-project_run_script"></a>

#### `AppPaths.project_run_script`

`property` | [lazygui/config/paths.py:49](../../lazygui/config/paths.py#L49)

Decorators: `@property`

```python
def project_run_script(self) -> Path
```

Absolute path to the ``run`` shell launcher in the repository.

**Returns:** `Path`

<a id="apppaths-lazyc2_script"></a>

#### `AppPaths.lazyc2_script`

`property` | [lazygui/config/paths.py:54](../../lazygui/config/paths.py#L54)

Decorators: `@property`

```python
def lazyc2_script(self) -> Path
```

Absolute path to the Flask backend ``lazyc2.py``.

**Returns:** `Path`

<a id="apppaths-c2_credentials_path"></a>

#### `AppPaths.c2_credentials_path`

`property` | [lazygui/config/paths.py:59](../../lazygui/config/paths.py#L59)

Decorators: `@property`

```python
def c2_credentials_path(self) -> Path
```

Absolute path to the C2 auto-generated credentials file.

``lazyc2.py`` writes ``.c2_credentials.txt`` at startup when it
generates strong credentials. The operator console reads this file
to auto-discover the username and password.

**Returns:** `Path`

<a id="apppaths-sessions_dir"></a>

#### `AppPaths.sessions_dir`

`property` | [lazygui/config/paths.py:69](../../lazygui/config/paths.py#L69)

Decorators: `@property`

```python
def sessions_dir(self) -> Path
```

Absolute path to the sessions directory.

**Returns:** `Path`

<a id="apppaths-ensure_config_dir"></a>

#### `AppPaths.ensure_config_dir`

`method` | [lazygui/config/paths.py:73](../../lazygui/config/paths.py#L73)

```python
def ensure_config_dir(self) -> Path
```

Create the config directory if missing and return it.

**Returns:** `Path`

*Called by:* [`Application.__init__`](lazygui.app.py.md#application-__init__), [`AppSettings.save`](lazygui.config.settings.py.md#appsettings-save)

---
