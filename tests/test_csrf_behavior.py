"""BDD behavior scenarios for the CSRF contract."""

from __future__ import annotations

from lazyc2.security.csrf import CSRFPolicy


class _Request:
    def __init__(self, method: str, path: str, headers=None, form=None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.form = form or {}


def test_given_authenticated_post_without_token_then_rejected() -> None:
    """Given an authenticated operator POST without a token, the gate denies."""
    policy = CSRFPolicy()
    request = _Request(method="POST", path="/issue_command")
    assert policy.check_request("session-1", request) is False


def test_given_authenticated_post_with_valid_token_then_allowed() -> None:
    """Given a valid token echoed back, the gate allows the mutation."""
    policy = CSRFPolicy()
    token = policy.issue("session-1")
    request = _Request(
        method="POST",
        path="/issue_command",
        headers={"X-XSRF-TOKEN": token},
    )
    assert policy.check_request("session-1", request) is True


def test_given_login_path_without_token_then_allowed() -> None:
    """Given an exempt path (login), the gate allows without a token."""
    policy = CSRFPolicy()
    request = _Request(method="POST", path="/login")
    assert policy.check_request("session-1", request) is True


def test_given_get_request_then_always_allowed() -> None:
    """Given a safe HTTP method, the gate always allows regardless of token."""
    policy = CSRFPolicy()
    request = _Request(method="GET", path="/issue_command")
    assert policy.check_request("session-1", request) is True
