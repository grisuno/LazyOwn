"""HTTP and API utilities for the LazyOwn framework.

Extracted from ``utils.py`` — HTTP request builders, exploit/PoC
scrapers, news feeds, and web interaction helpers.
"""

from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from core.console import print_error, print_msg


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
        resp = requests.get(url, timeout=5, verify=False)  # noqa: S501
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
            results.append({"title": title_el.get_text(strip=True), "link": link_el.get("href", "")})
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
            results.append({"title": title_el.get_text(strip=True), "link": title_el.get("href", "")})
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
                links.append(title_el.get("href", ""))
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
