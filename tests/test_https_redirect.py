"""TDD tests for the HTTPS redirect contract.

Contract: ``lazyc2.security.https_redirect.HTTPSRedirect`` returns the
response a Flask ``before_request`` handler should produce to force the
client onto TLS in PROD, while leaving DEV traffic alone.

Invariants:

1. ``is_secure=True`` request: no redirect (None returned).
2. ``is_secure=False`` + ``env="PROD"``: a 301 redirect to the same URL
   with the scheme replaced by ``https``.
3. ``is_secure=False`` + ``env="DEV"``: no redirect.
4. The path and query string of the request are preserved in the redirect
   target.
5. The host header is preserved.
"""

from __future__ import annotations

import pytest

from lazyc2.security.https_redirect import HTTPSRedirect


class _FakeRequest:
    def __init__(self, is_secure: bool, host: str = "c2.example", path: str = "/", query_string: str = ""):
        self.is_secure = is_secure
        self.host = host
        self.path = path
        self.url = f"{'https' if is_secure else 'http'}://{host}{path}"
        if query_string:
            self.url += f"?{query_string}"
        self.query_string = query_string


class TestHTTPSRedirect:
    """Verify the redirect logic."""

    def test_secure_request_passes_through(self) -> None:
        policy = HTTPSRedirect(env="PROD", enabled=True)
        request = _FakeRequest(is_secure=True, path="/dashboard")
        assert policy.evaluate(request) is None

    def test_insecure_in_prod_redirects_to_https(self) -> None:
        policy = HTTPSRedirect(env="PROD", enabled=True)
        request = _FakeRequest(is_secure=False, host="c2.example", path="/dashboard")
        response = policy.evaluate(request)
        assert response is not None
        assert response.status_code == 301
        assert response.location == "https://c2.example/dashboard"

    def test_insecure_in_dev_passes_through(self) -> None:
        policy = HTTPSRedirect(env="DEV", enabled=True)
        request = _FakeRequest(is_secure=False, path="/dashboard")
        assert policy.evaluate(request) is None

    def test_insecure_when_disabled_passes_through(self) -> None:
        policy = HTTPSRedirect(env="PROD", enabled=False)
        request = _FakeRequest(is_secure=False, path="/dashboard")
        assert policy.evaluate(request) is None

    def test_query_string_preserved(self) -> None:
        policy = HTTPSRedirect(env="PROD", enabled=True)
        request = _FakeRequest(is_secure=False, path="/api/run", query_string="cmd=ping")
        response = policy.evaluate(request)
        assert response is not None
        assert response.location == "https://c2.example/api/run?cmd=ping"

    def test_root_path_preserved(self) -> None:
        policy = HTTPSRedirect(env="PROD", enabled=True)
        request = _FakeRequest(is_secure=False, path="/")
        response = policy.evaluate(request)
        assert response.location == "https://c2.example/"


class TestRedirectResponseShape:
    """Verify the dataclass returned to Flask."""

    def test_response_is_named_tuple_like(self) -> None:
        policy = HTTPSRedirect(env="PROD", enabled=True)
        request = _FakeRequest(is_secure=False, path="/x")
        response = policy.evaluate(request)
        assert response.status_code == 301
        assert isinstance(response.location, str)
