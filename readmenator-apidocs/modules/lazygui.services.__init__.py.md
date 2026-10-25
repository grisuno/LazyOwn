# `lazygui.services`

> Source: [lazygui/services/__init__.py:1](../../lazygui/services/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Service layer.

Defines the domain types the GUI consumes and the backend abstraction that
hides whether commands are issued to a local cmd2 console (PTY) or a remote
LazyOwn teamserver (HTTP/WebSocket).

The [`Backend`](lazygui.services.backend.py.md#backend) Protocol is the only contract the UI knows about. New
backend implementations only need to satisfy that contract to be plugged in.
