# `modules.sinks`

> Source: [modules/sinks/__init__.py:1](../../modules/sinks/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Outcome sink adapters.

Each module exposes ``apply(event) -> bool`` and owns exactly one shared
surface. The outcome bus imports them lazily so a missing dependency
never blocks an engagement.
