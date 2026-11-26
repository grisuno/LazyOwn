"""HTTP and API utilities for the LazyOwn framework.

Extracted from ``utils.py`` — HTTP request builders, exploit/PoC
scrapers, news feeds, and web interaction helpers.
"""

from __future__ import annotations

import ssl
from typing import Any

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, SSLError

from core.console import print_error, print_msg


class _LabTLSAdapter(requests.adapters.HTTPAdapter):
    """HTTPAdapter that negotiates TLS with the audited lab fallback context.

    Verification stays off only when the operator opted in via
    ``LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1``; the helper checks that gate
    before building this adapter.
    """

    def __init__(self, ssl_context: ssl.SSLContext) -> None:
        """Bind the adapter to a pre-built SSL context.

        Args:
            ssl_context: Context built by ``core.hardening`` helpers.
        """
        self._ssl_context = ssl_context
        super().__init__()

    def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
        """Initialise the urllib3 pool with the pinned SSL context.

        Args:
            *args: Positional poolmanager arguments.
            **kwargs: Keyword poolmanager arguments.
        """
        kwargs["ssl_context"] = self._ssl_context
        super().init_poolmanager(*args, **kwargs)


def lab_tolerant_request(method: str, url: str, **kwargs: Any) -> requests.Response:
    """Send *method* to *url* with certificate verification by default.

    On a certificate verification failure, retries once with the audited
    lab fallback context, only when the operator opt-in
    (``LAZY_PROXY_ALLOW_SELF_SIGNED_LAB=1``) covers the target host.

    Args:
        method: HTTP verb (``get``, ``post``, ...).
        url: Target URL.
        **kwargs: Forwarded to ``requests.Session.request``.

    Returns:
        The HTTP response.

    Raises:
        RequestException: When the request fails or TLS verification
            fails without operator opt-in.
    """
    session = requests.Session()
    kwargs.setdefault("timeout", 10)
    try:
        return session.request(method, url, **kwargs)
    except SSLError:
        from urllib.parse import urlparse

        from core.hardening import tls_lab_fallback_context, tls_lab_unverified_allowed

        host = urlparse(url).hostname or ""
        if not tls_lab_unverified_allowed(host):
            raise

        session.mount("https://", _LabTLSAdapter(tls_lab_fallback_context()))
        return session.request(method, url, **kwargs)
    finally:
        session.close()


def lab_tolerant_get(url: str, **kwargs: Any) -> requests.Response:
    """GET *url* with verification by default and a lab-gated TLS fallback.

    Args:
        url: Target URL.
        **kwargs: Forwarded to :func:`lab_tolerant_request`.

    Returns:
        The HTTP response.
    """
    return lab_tolerant_request("get", url, **kwargs)


def generate_http_req(
    host: str,
    port: int,
    uri: str,
    custom_header: dict[str, str] | None = None,
    cmd: str | None = None,
) -> str:
    """Build and send an HTTP GET request.

    Args:
        host: Target hostname or IP.
        port: Target port.
        uri: URI path.
        custom_header: Optional extra headers.
        cmd: Optional command to embed in the request.

    Returns:
        Response text or empty string.
    """
    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{host}:{port}{uri}"
    if cmd:
        url += f"?cmd={cmd}"
    headers = {"User-Agent": "Mozilla/5.0", **(custom_header or {})}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.text
    except RequestException as e:
        print_error(f"Request failed: {e}")
        return ""


def get_banner(host: str, port: int) -> str:
    """Fetch a banner by connecting via HTTP to the given host and port.

    Args:
        host: Target host.
        port: Target port.

    Returns:
        Response text or empty string.
    """
    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{host}:{port}/"
    try:
        resp = lab_tolerant_get(url, timeout=5)
        return resp.text[:500]
    except RequestException:
        return ""


def get_command(url: str, lhost: str) -> str | None:
    """Fetch a command payload from a remote URL.

    Args:
        url: Full URL to fetch.
        lhost: Local host address (unused, kept for signature compat).

    Returns:
        Response text or None on failure.
    """
    try:
        resp = requests.get(url, timeout=10)
        return resp.text
    except RequestException as e:
        print_error(str(e))
        return None


def send_command(cmd: str, url: str, lhost: str) -> str | None:
    """Send a command via HTTP POST.

    Args:
        cmd: Command string.
        url: Target URL.
        lhost: Local host.

    Returns:
        Response text or None.
    """
    try:
        resp = requests.post(url, data={"cmd": cmd, "lhost": lhost}, timeout=10)
        return resp.text
    except RequestException as e:
        print_error(str(e))
        return None


def exploitalert(content: str) -> list[dict[str, str]]:
    """Parse ExploitAlert search results HTML.

    Args:
        content: Raw HTML from ExploitAlert.

    Returns:
        List of ``{"title": …, "link": …}`` dicts.
    """
    results: list[dict[str, str]] = []
    soup = BeautifulSoup(content, "html.parser")
    for item in soup.select(".exploit-item"):
        title_el = item.select_one(".exploit-title")
        link_el = item.select_one("a")
        if title_el and link_el:
            results.append({"title": title_el.get_text(strip=True), "link": str(link_el.get("href", ""))})
    return results


def packetstormsecurity(content: str) -> list[dict[str, str]]:
    """Parse Packet Storm Security search results HTML.

    Args:
        content: Raw HTML from packetstormsecurity.com.

    Returns:
        List of ``{"title": …, "link": …}`` dicts.
    """
    results: list[dict[str, str]] = []
    soup = BeautifulSoup(content, "html.parser")
    for item in soup.select(".result"):
        title_el = item.select_one(".title a")
        if title_el:
            results.append({"title": title_el.get_text(strip=True), "link": str(title_el.get("href", ""))})
    return results


def nvddb(content: str) -> list[dict[str, Any]]:
    """Parse NVD JSON vulnerability feed.

    Args:
        content: Raw JSON string from the NVD API.

    Returns:
        List of CVE dicts.
    """
    import json

    results: list[dict[str, Any]] = []
    try:
        data = json.loads(content)
        for vuln in data.get("vulnerabilities", []):
            cve = vuln.get("cve", {})
            results.append(
                {
                    "id": cve.get("id", ""),
                    "description": cve.get("descriptions", [{}])[0].get("value", ""),
                    "severity": cve.get("metrics", {})
                    .get("cvssMetricV31", [{}])[0]
                    .get("cvssData", {})
                    .get("baseSeverity", ""),
                }
            )
    except (json.JSONDecodeError, KeyError, IndexError):
        pass
    return results


def scrape_news() -> tuple[list[str], list[str], list[str]]:
    """Scrape Hacker News top stories.

    Returns:
        ``(titles, links, scores)`` tuple.
    """
    titles: list[str] = []
    links: list[str] = []
    scores: list[str] = []
    try:
        resp = requests.get("https://news.ycombinator.com/", timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for row in soup.select(".athing"):
            title_el = row.select_one(".titleline a")
            if title_el:
                titles.append(title_el.get_text(strip=True))
                links.append(str(title_el.get("href", "")))
        for score_el in soup.select(".score"):
            scores.append(score_el.get_text(strip=True))
    except RequestException:
        pass
    return titles, links, scores


def display_news(titles: list[str], links: list[str], scores: list[str]) -> None:
    """Display scraped news in the console.

    Args:
        titles: News titles.
        links: News URLs.
        scores: News scores.
    """
    for i, (title, link, score) in enumerate(zip(titles, links, scores, strict=False), 1):
        print_msg(f"{i}. {title} ({score})")
        print_msg(f"   {link}")


def inject_payloads(urls: list[str], payload_url: str, request_timeout: int = 15) -> None:
    """Attempt to inject a payload URL into a list of target URLs.

    Args:
        urls: List of target URLs.
        payload_url: URL to inject.
        request_timeout: Timeout per request in seconds.
    """
    for url in urls:
        try:
            resp = requests.get(
                url.replace("INJECTHERE", payload_url),
                timeout=request_timeout,
            )
            print_msg(f"[{resp.status_code}] {url}")
        except RequestException as e:
            print_error(f"[!] {url}: {e}")


__all__ = [
    "display_news",
    "exploitalert",
    "generate_http_req",
    "get_banner",
    "get_command",
    "inject_payloads",
    "nvddb",
    "packetstormsecurity",
    "scrape_news",
    "send_command",
]
