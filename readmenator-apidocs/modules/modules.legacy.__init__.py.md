# `modules.legacy`

> Source: [modules/legacy/__init__.py:1](../../modules/legacy/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Backward-compatibility shims for deprecated scripts.

Contract: the canonical location of these scripts is now
``contrib/legacy/``. Every module in this package is a symlink to its
counterpart there, so ``python3 modules/legacy/<name>.py``,
``run_script("modules/legacy/<name>.py")`` and
``from modules.legacy.<name> import ...`` keep working without any
caller change. New code must import from `[`contrib.legacy`](contrib.legacy.__init__.py.md)` directly
and must not add new modules here.
