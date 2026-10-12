# `lazyc2.extensions`

> Source: [lazyc2/extensions/__init__.py:1](../../lazyc2/extensions/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Shared C2 extension modules.

Each module is a self-contained set of helpers that the monolithic
``lazyc2.py`` and/or individual Flask blueprints import. Call the
module-level ``configure()`` function during app initialisation to
set paths.
