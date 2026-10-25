# `core.autonomous`

> Source: [core/autonomous.py:1](../../core/autonomous.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Autonomous-run mode for the loop engine.

While the loop runs, interactive prompts have no operator in front of
them: `[`input`](core.llm_budget.py.md#modelprice-input)` calls from automation verbs must never steal the
keyboard from the shell. The context manager flips an environment flag
(so shell commands can detect unattended mode) and replaces
``builtins.input`` with a prompt-skipping stub that announces why the
default was taken.

## Contents

- **Functions:** [`is_autonomous`](#is_autonomous), [`autonomous_mode`](#autonomous_mode)
- **Constants:** [`AUTONOMOUS_ENV`](#autonomous_env)

## Functions

<a id="is_autonomous"></a>

### `is_autonomous`

`function` | [core/autonomous.py:21](../../core/autonomous.py#L21)

```python
def is_autonomous() -> bool
```

Return True while an autonomous loop run owns the process.

**Returns:** `bool`

*Called by:* [`ExploitMigratedCommandSet.do_autoblody`](cli.commands.exploit_migrated.py.md#exploitmigratedcommandset-do_autoblody), [`LazyOwnShell.cmd`](lazyown.py.md#lazyownshell-cmd)

---

<a id="autonomous_mode"></a>

### `autonomous_mode`

`function` `generator` | [core/autonomous.py:27](../../core/autonomous.py#L27)

Decorators: `@contextlib.contextmanager`

```python
def autonomous_mode() -> Iterator[None]
```

Suppress interactive prompts for the duration of a loop run.

**Returns:** `Iterator[None]`

**Yields:** Control with prompts answered by an empty string and
``LAZYOWN_AUTONOMOUS=1`` exported. Everything is restored on
exit, including when an exception unwinds the block.

*Called by:* [`run_loop`](modules.lazy_runner.py.md#run_loop)

---

## Constants

<a id="autonomous_env"></a>

### `AUTONOMOUS_ENV`

`constant` | [core/autonomous.py:18](../../core/autonomous.py#L18)

```python
AUTONOMOUS_ENV = 'LAZYOWN_AUTONOMOUS'
```

---
