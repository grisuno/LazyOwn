# `contrib.legacy`

> Source: [contrib/legacy/__init__.py:1](../../contrib/legacy/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Legacy module shims — deprecated scripts retained for compatibility.

Scripts in this directory are no longer maintained or imported by the
framework core. They may be invoked via `[`run_script`](lazyown.py.md#lazyownshell-run_script)` paths (which
should be updated to point here) or as standalone CLI tools.

New code must not add dependencies to modules in this directory.
