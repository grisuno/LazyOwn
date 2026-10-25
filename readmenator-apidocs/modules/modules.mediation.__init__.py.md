# `modules.mediation`

> Source: [modules/mediation/__init__.py:1](../../modules/mediation/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Mediation layer for LazyOwn cross-module coordination.

Colleagues never import each other directly: they depend on the
``contracts`` abstractions here and each specialised mediator owns
exactly one coordination concern. The hub routes requests by domain
key so callers stay ignorant of concrete peers.
