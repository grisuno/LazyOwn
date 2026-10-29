"""LazyShortener: URL shortener bridge for LazyOwn phishing delivery.

Calls keyless public shortener APIs (is.gd and v.gd) over HTTPS with a
validated URL, returning the short link written into lure emails when the
autonomous loop falls back to client-subject delivery. Single outbound
HTTP GET; no shell, no binaries, no secrets.

>>> from modules import lazyshortener
>>> bool(lazyshortener.PROVIDERS)
True
"""

from __future__ import annotations

from typing import Any

import requests

from core.safe_exec import UrlValidationError, validate_url

DEFAULT_TIMEOUT_SEC = 15.0
DEFAULT_PROVIDER = "isgd"

PROVIDERS: dict[str, str] = {
    "isgd": "https://is.gd/create.php",
    "vgd": "https://v.gd/create.php",
}


def providers() -> tuple[str, ...]:
    """Return every supported shortener provider key."""
    return tuple(PROVIDERS)


def shorten(url: str, provider: str = DEFAULT_PROVIDER, timeout: float = DEFAULT_TIMEOUT_SEC) -> dict[str, Any]:
    """Shorten one URL through a keyless public provider.

    Args:
        url: Absolute http/https URL to shorten.
        provider: One of :func:`providers` (default ``isgd``).
        timeout: HTTP timeout in seconds.

    Returns:
        Mapping with ``ok``, ``short_url``, ``provider`` and ``error``.
    """
    provider = str(provider or DEFAULT_PROVIDER).strip().lower() or DEFAULT_PROVIDER
    endpoint = PROVIDERS.get(provider)
    if endpoint is None:
        return {"ok": False, "short_url": "", "provider": provider, "error": f"unknown provider: {provider}"}
    try:
        validated = validate_url(url)
    except (ValueError, UrlValidationError) as exc:
        return {"ok": False, "short_url": "", "provider": provider, "error": f"url rejected: {exc}"}
    try:
        response = requests.get(
            endpoint,
            params={"format": "simple", "url": validated},
            timeout=timeout,
            headers={"User-Agent": "LazyOwn-LazyShortener/1.0"},
        )
        response.raise_for_status()
        short_url = response.text.strip()
        if not short_url.startswith("http"):
            return {"ok": False, "short_url": "", "provider": provider, "error": short_url[:200] or "empty response"}
    except requests.RequestException as exc:
        return {"ok": False, "short_url": "", "provider": provider, "error": f"request failed: {exc}"}
    return {"ok": True, "short_url": short_url, "provider": provider, "error": ""}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: lazyshortener.py <url> [provider]")
    else:
        print(shorten(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROVIDER))
