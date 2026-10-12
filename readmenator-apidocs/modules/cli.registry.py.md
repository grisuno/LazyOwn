# `cli.registry`

> Source: [cli/registry.py:1](../../cli/registry.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

``cmd2.CommandSet`` discovery and registration for `[`cli.commands`](cli.commands.__init__.py.md)`.

Tier 2 introduces ``cli.commands.*`` modules where each module exposes one
or more ``CommandSet`` subclasses scoped to a kill-chain phase (recon,
enum, exploit, ...). This module discovers those CommandSets and registers
them on a live `cmd2.Cmd` instance.

The point: ``lazyown.py`` does not import every phase module — it calls
`register_command_sets(self)` at startup and the plumbing happens
declaratively. Adding a new phase is a single new file under
``cli/commands/`` plus a ``CommandSet`` subclass.

Migration coexistence
---------------------

During the staged migration the legacy `[`LazyOwnShell`](lazyown.py.md#lazyownshell)` still owns most
``do_*`` methods. The replacement phase modules subclass
[`cli.commands._dormancy.PendingCommandSet`](cli.commands._dormancy.py.md#pendingcommandset) so they are discovered
(and therefore testable) without colliding with the originals on the
shell. [`register_command_sets`](#register_command_sets) skips them; once a phase is fully
moved out of ``lazyown.py`` its set swaps its base class to
[`cli.commands._base.LazyOwnCommandSet`](cli.commands._base.py.md#lazyowncommandset) and joins the active
registry on the next shell start.

## Contents

- **Functions:** [`iter_command_sets`](#iter_command_sets), [`register_command_sets`](#register_command_sets)
- **Constants:** [`PACKAGE_NAME`](#package_name)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_registry_py__register_command_sets(["register_command_sets"])
    n_cli_registry_py__iter_command_sets(["iter_command_sets"])
    n_cli_commands__dormancy_py__is_pending["_dormancy.is_pending"]
    n_cli_registry_py__register_command_sets --> n_cli_registry_py__iter_command_sets
    n_cli_registry_py__iter_command_sets -.-> n_cli_commands__dormancy_py__is_pending
    n_cli_registry_py__register_command_sets -.-> n_cli_commands__dormancy_py__is_pending
```

## Functions

<a id="iter_command_sets"></a>

### `iter_command_sets`

`function` `generator` | [cli/registry.py:41](../../cli/registry.py#L41)

```python
def iter_command_sets(include_pending: bool = True) -> Iterable[type[CommandSet]]
```

Yield every ``CommandSet`` subclass found under ``cli.commands.*``.

Each module under `[`cli.commands`](cli.commands.__init__.py.md)` is imported and scanned for classes
that subclass ``cmd2.CommandSet``. Modules whose leaf name begins with
an underscore (``_base``, ``_dormancy``) are skipped because they hold
shared scaffolding rather than concrete command sets.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `include_pending` | `bool` | `True` | When ``True`` (default) pending sets are yielded so tests can validate their structure. When ``False`` the iterator filters them out — used by [`register_command_sets`](#register_command_sets) to avoid collisions with the legacy shell. |

**Returns:** `Iterable[type[CommandSet]]`

**Yields:** Each concrete ``CommandSet`` subclass declared in a discovered
module.

*Calls:* [`is_pending`](cli.commands._dormancy.py.md#is_pending)

*Called by:* [`register_command_sets`](#register_command_sets)

---

<a id="register_command_sets"></a>

### `register_command_sets`

`function` | [cli/registry.py:77](../../cli/registry.py#L77)

```python
def register_command_sets(shell) -> list[CommandSet]
```

Instantiate and register every active ``CommandSet`` on `[`shell`](lazyc2.state.py.md#shell)`.

Pending sets (subclasses of
[`cli.commands._dormancy.PendingCommandSet`](cli.commands._dormancy.py.md#pendingcommandset)) are skipped so they
can coexist with the legacy ``do_*`` methods on `[`LazyOwnShell`](lazyown.py.md#lazyownshell)`
during the incremental migration.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `shell` |  |  | A live `cmd2.Cmd` instance (typically `[`LazyOwnShell`](lazyown.py.md#lazyownshell)`). |

**Returns:** `list[CommandSet]` - The list of ``CommandSet`` instances that were successfully
registered. Errors during registration of an individual set are
reported via the shell's ``perror`` (or [`print`](modules.resource_script.py.md#scriptcontext-print) as a
fallback) and skipped — one failing set must not prevent the
shell from booting.

*Calls:* [`is_pending`](cli.commands._dormancy.py.md#is_pending), [`iter_command_sets`](#iter_command_sets)

---

## Constants

<a id="package_name"></a>

### `PACKAGE_NAME`

`constant` | [cli/registry.py:37](../../cli/registry.py#L37)

```python
PACKAGE_NAME = 'cli.commands'
```

---
