"""Outcome sink adapters.

Each module exposes ``apply(event) -> bool`` and owns exactly one shared
surface. The outcome bus imports them lazily so a missing dependency
never blocks an engagement.
"""

__all__: list[str] = []
