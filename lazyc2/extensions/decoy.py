"""Decoy / honeypot page for unauthenticated visitors.

When a request comes from an IP that is not the operator's lhost the
C2 renders a decoy HTML page instead of the real interface.
"""

from __future__ import annotations

from flask import current_app, render_template, request


def decoy_response() -> str | None:
    """Return a decoy page when the client IP is not the operator host.

    Reads ``lhost`` from ``current_app.config`` and compares it
    against ``request.remote_addr``. Returns the rendered ``decoy.html``
    template when they differ, or ``None`` when the client is allowed.

    Returns:
        Rendered decoy template string or ``None``.
    """
    client_ip = request.remote_addr
    lhost = current_app.config.get("lhost", "127.0.0.1")
    if client_ip != lhost and client_ip != "127.0.0.1":
        return render_template("decoy.html")
    return None
