"""Decoy / honeypot page for unauthenticated visitors.

When a request comes from an IP that is not the operator's lhost the
C2 renders a decoy HTML page instead of the real interface. This module
is the single decoy contract: the monolith and every blueprint resolve
through :func:`decoy_response`, so mode precedence lives in exactly one
place (see :func:`modules.orchestrator_config.decoy_config`).
"""

from __future__ import annotations

import logging

from flask import abort, current_app, render_template, request


def decoy_response() -> str | None:
    """Serve a decoy page to non-operator IPs when decoy mode is enabled.

    Mode precedence (see :func:`modules.orchestrator_config.decoy_config`):
    module fallback ``page`` < YAML profile ``decoy.mode`` < payload
    ``orchestrator.decoy.mode`` < legacy payload ``c2_decoy_mode``.

    - ``"off"``: disabled; every request proceeds to normal handling.
    - ``"page"``: requests from IPs outside the operator allowlist
      receive a fake decoy page. This preserves the legacy honeypot look.
    - ``"deny"``: requests from non-operator IPs receive HTTP 403 instead
      of a misleading page. Use this when the decoy is not wanted.

    The operator allowlist is ``lhost``, ``127.0.0.1`` and the entries of
    the resolved ``operator_allowlist``.

    Returns:
        ``None`` when the request may proceed, otherwise the rendered
        decoy template (page mode). Deny mode aborts with 403.
    """
    try:
        from modules.orchestrator_config import decoy_config

        resolved = decoy_config()
    except Exception:
        return None
    mode = str(resolved.get("mode", "page") or "page").strip().lower()
    if mode == "off":
        return None
    client_ip = request.remote_addr
    lhost = current_app.config.get("lhost", "127.0.0.1")
    allowed_ips = {str(lhost), "127.0.0.1"}
    allowed_ips.update(
        ip.strip()
        for ip in str(resolved.get("operator_allowlist", "127.0.0.1") or "127.0.0.1")
        .replace("{lhost}", str(lhost))
        .split(",")
        if ip.strip()
    )
    if client_ip not in allowed_ips:
        logging.warning(
            "[decoy] Request from non-operator IP %s served decoy (%s mode)",
            client_ip,
            mode,
        )
        if mode == "deny":
            abort(403, description="Access denied")
        return render_template("decoy.html")
    return None
