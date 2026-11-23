"""Listener management contracts for the C2 server.

Blueprint owning the multi-listener REST surface (`/api/listeners` CRUD).
The manager itself lives in :mod:`modules.listener_manager`; this package
owns the HTTP surface and reads the manager from the Flask app config.
"""

from lazyc2.listeners.blueprint import listeners_bp

__all__ = ["listeners_bp"]
