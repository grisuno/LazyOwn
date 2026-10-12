"""Reusable development tools for the LazyOwn autonomous loop.

These are operator/developer harnesses, not framework runtime code:
they sandbox the store, fake the LLM/engine boundary and verify the
real user-facing paths (loop runner streaming, monitor TUI) without
network access. Run them directly with ``python -m modules.tools.<name>``
or import their ``run()`` from a test/session.
"""
