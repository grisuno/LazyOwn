"""TDD tests for the CSRF policy contract.

Contract: ``lazyc2.security.csrf.CSRFPolicy`` issues per-session tokens that
must be echoed back by the client on every mutating request, except for
configured exemptions (login, logout, beacon endpoints).

Invariants under test:

1. ``issue(session_id)`` returns a 32-byte URL-safe token.
2. The token is bound to the session id: same session -> same token.
3. ``validate(session_id, token)`` returns ``True`` only on a constant-time
   match between the stored and the candidate token.
4. ``validate`` returns ``False`` on missing, empty, or wrong token.
5. ``validate`` returns ``False`` for an unknown session id.
6. The exempt path set is honoured: an exempt path on a session without a
   token still passes.
7. ``extract_header`` and ``extract_form`` parse tokens from request-shaped
   objects.
"""

from __future__ import annotations

import pytest

from lazyc2.security.csrf import CSRFPolicy


class _FakeRequest:
    def __init__(self, headers=None, form=None, path="/issue_command", method="POST"):
        self.headers = headers or {}
        self.form = form or {}
        self.path = path
        self.method = method


class TestTokenIssuance:
    """Verify the issuer contract."""

    def test_issue_returns_string(self) -> None:
        policy = CSRFPolicy()
        token = policy.issue("session-1")
        assert isinstance(token, str)
        assert len(token) >= 32

    def test_issue_is_deterministic_for_same_session(self) -> None:
        policy = CSRFPolicy()
        a = policy.issue("session-1")
        b = policy.issue("session-1")
        assert a == b

    def test_issue_is_unique_across_sessions(self) -> None:
        policy = CSRFPolicy()
        a = policy.issue("session-1")
        b = policy.issue("session-2")
        assert a != b


class TestTokenValidation:
    """Verify the validator contract."""

    def test_valid_token_passes(self) -> None:
        policy = CSRFPolicy()
        token = policy.issue("session-1")
        assert policy.validate("session-1", token) is True

    def test_missing_token_fails(self) -> None:
        policy = CSRFPolicy()
        policy.issue("session-1")
        assert policy.validate("session-1", "") is False
        assert policy.validate("session-1", None) is False

    def test_unknown_session_fails(self) -> None:
        policy = CSRFPolicy()
        token = policy.issue("session-1")
        assert policy.validate("session-other", token) is False

    def test_wrong_token_fails(self) -> None:
        policy = CSRFPolicy()
        policy.issue("session-1")
        assert policy.validate("session-1", "wrong-token") is False


class TestExemptions:
    """Verify that configured paths bypass the check."""

    def test_exempt_path_passes_without_token(self) -> None:
        policy = CSRFPolicy(exempt_paths=("/login", "/logout", "/api/beacon/poll"))
        assert policy.is_exempt("/login") is True
        assert policy.is_exempt("/logout") is True
        assert policy.is_exempt("/api/beacon/poll") is True

    def test_non_exempt_path_fails_check(self) -> None:
        policy = CSRFPolicy(exempt_paths=("/login",))
        assert policy.is_exempt("/issue_command") is False
        assert policy.is_exempt("/api/run") is False


class TestRequestExtraction:
    """Verify the request-shaped helper."""

    def test_extract_header(self) -> None:
        policy = CSRFPolicy()
        request = _FakeRequest(headers={"X-XSRF-TOKEN": "abc"})
        assert policy.extract_token(request) == "abc"

    def test_extract_form(self) -> None:
        policy = CSRFPolicy()
        request = _FakeRequest(headers={}, form={"xsrf_token": "def"})
        assert policy.extract_token(request) == "def"

    def test_extract_header_takes_precedence(self) -> None:
        policy = CSRFPolicy()
        request = _FakeRequest(
            headers={"X-XSRF-TOKEN": "header"},
            form={"xsrf_token": "form"},
        )
        assert policy.extract_token(request) == "header"

    def test_extract_returns_none_when_missing(self) -> None:
        policy = CSRFPolicy()
        request = _FakeRequest()
        assert policy.extract_token(request) is None


class TestCheckRequest:
    """Verify the full request check combining exemptions and validation."""

    def test_safe_methods_bypass(self) -> None:
        policy = CSRFPolicy()
        request = _FakeRequest(method="GET", path="/issue_command")
        assert policy.check_request("session-1", request) is True

    def test_mutating_without_token_fails(self) -> None:
        policy = CSRFPolicy()
        request = _FakeRequest(method="POST", path="/issue_command")
        assert policy.check_request("session-1", request) is False

    def test_mutating_with_valid_token_passes(self) -> None:
        policy = CSRFPolicy()
        token = policy.issue("session-1")
        request = _FakeRequest(
            method="POST",
            path="/issue_command",
            headers={"X-XSRF-TOKEN": token},
        )
        assert policy.check_request("session-1", request) is True

    def test_exempt_path_with_no_token_still_passes(self) -> None:
        policy = CSRFPolicy(exempt_paths=("/login",))
        request = _FakeRequest(method="POST", path="/login")
        assert policy.check_request("session-1", request) is True
