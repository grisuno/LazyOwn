"""TLS context policies for the LazyOwn framework.

One auditable home for client TLS: a verifying context with a TLS 1.2
floor by default, and a single gated fallback for lab self-signed hosts
that requires an explicit operator environment opt-in plus a
loopback/private target.
"""

from __future__ import annotations

import logging
import os
import ssl

log = logging.getLogger("core.tls")

TLS_MINIMUM_VERSION = ssl.TLSVersion.TLSv1_2
ENV_ALLOW_SELF_SIGNED_LAB = "LAZY_PROXY_ALLOW_SELF_SIGNED_LAB"
ENV_ALLOW_PRIVATE = "LAZY_PROXY_ALLOW_PRIVATE"
ENV_INSECURE_TLS = "LAZY_PROXY_INSECURE_TLS"
ENV_TRUST_CA = "LAZY_PROXY_TRUST_CA"


def tls_secure_context(extra_ca: str = "") -> ssl.SSLContext:
    """Build a verifying client TLS context with a TLS 1.2 floor.

    Args:
        extra_ca: Optional extra CA bundle path loaded for verification.

    Returns:
        Verifying SSLContext with hostname checking enabled.
    """
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.minimum_version = TLS_MINIMUM_VERSION
    bundle = (extra_ca or os.environ.get(ENV_TRUST_CA, "") or "").strip()
    if bundle:
        try:
            context.load_verify_locations(cafile=bundle)
        except OSError as exc:
            log.warning("trust bundle unreadable %r: %s", bundle, exc)
    return context


def tls_lab_unverified_allowed(host: str) -> bool:
    """Return True only when unverified lab TLS is explicitly opted in.

    Both conditions must hold: the host is a loopback/private literal (or
    localhost) and the operator set ``LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1``.
    Request data can never enable it alone.

    Args:
        host: Target hostname or IP literal.

    Returns:
        True when the operator opt-in covers this lab host.
    """
    import ipaddress as _ipaddress

    if os.environ.get(ENV_ALLOW_SELF_SIGNED_LAB, "") != "1":
        return False
    name = (host or "").strip().strip("[]").lower()
    if name == "localhost":
        return True
    try:
        addr = _ipaddress.ip_address(name)
    except ValueError:
        return False
    return bool(addr.is_loopback or addr.is_private or addr.is_link_local)


def tls_lab_fallback_context() -> ssl.SSLContext:
    """Build the gated unverified context for lab self-signed hosts.

    This is the single audited location allowed to disable verification.
    Callers must check :func:`tls_lab_unverified_allowed` first; the TLS
    1.2 floor still applies so only verification (not protocol version)
    is relaxed.

    Returns:
        Unverified SSLContext with TLS 1.2 floor.
    """
    log.warning("unverified TLS fallback engaged for lab target (self-signed)")
    fallback = ssl.create_default_context()
    fallback.check_hostname = False
    fallback.verify_mode = ssl.CERT_NONE
    fallback.minimum_version = TLS_MINIMUM_VERSION
    return fallback


__all__ = [
    "ENV_ALLOW_PRIVATE",
    "ENV_ALLOW_SELF_SIGNED_LAB",
    "ENV_INSECURE_TLS",
    "ENV_TRUST_CA",
    "TLS_MINIMUM_VERSION",
    "tls_lab_fallback_context",
    "tls_lab_unverified_allowed",
    "tls_secure_context",
]
