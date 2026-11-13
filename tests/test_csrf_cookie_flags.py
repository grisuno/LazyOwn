"""Contract: CSRF cookie hardening (HttpOnly key, JS-readable token, Secure)."""

from __future__ import annotations

from flask import Flask
from flask_login import LoginManager

from lazyc2.security.csrf import CSRFPolicy
from lazyc2.security.csrf_flow import register_csrf_flow, token_cookie_name


def _app(secure_fn=None):
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "flags-test"
    login_manager = LoginManager(app)
    login_manager.user_loader(
        lambda user_id: type("U", (), {"id": user_id, "is_authenticated": True})() if user_id else None
    )
    policy = CSRFPolicy()
    register_csrf_flow(app, policy, lambda: True, secure_fn=secure_fn)

    @app.route("/")
    def index():
        return "ok"

    return app, policy


def _login(client):
    with client.session_transaction() as sess:
        sess["_user_id"] = "1"
        sess["_fresh"] = True


def _set_cookie_headers(response):
    return response.headers.getlist("Set-Cookie")


def test_key_cookie_httponly_token_cookie_readable() -> None:
    app, policy = _app()
    client = app.test_client()
    _login(client)
    resp = client.get("/")
    headers = _set_cookie_headers(resp)
    key_header = next(h for h in headers if h.startswith(policy.cookie_name + "="))
    token_header = next(h for h in headers if h.startswith(token_cookie_name() + "="))
    assert "HttpOnly" in key_header, "session-key cookie must be HttpOnly"
    assert "HttpOnly" not in token_header, "token cookie must stay JS-readable"
    assert "SameSite=Strict" in key_header and "SameSite=Strict" in token_header


def test_plain_http_no_secure_flag() -> None:
    app, policy = _app()
    client = app.test_client()
    _login(client)
    headers = _set_cookie_headers(client.get("/"))
    assert all("Secure" not in h for h in headers)


def test_secure_fn_adds_secure_flag() -> None:
    app, policy = _app(secure_fn=lambda: True)
    client = app.test_client()
    _login(client)
    headers = _set_cookie_headers(client.get("/"))
    key_header = next(h for h in headers if h.startswith(policy.cookie_name + "="))
    token_header = next(h for h in headers if h.startswith(token_cookie_name() + "="))
    assert "Secure" in key_header and "Secure" in token_header


def test_https_request_adds_secure_flag_without_fn() -> None:
    app, policy = _app()
    client = app.test_client()
    _login(client)
    headers = _set_cookie_headers(client.get("/", base_url="https://localhost"))
    key_header = next(h for h in headers if h.startswith(policy.cookie_name + "="))
    token_header = next(h for h in headers if h.startswith(token_cookie_name() + "="))
    assert "Secure" in key_header and "Secure" in token_header


def test_lazyc2_passes_secure_fn() -> None:
    src = open("lazyc2.py", encoding="utf-8").read()
    assert "_register_csrf_flow(app, _csrf_policy, _csrf_enabled, secure_fn=_csrf_cookie_secure)" in src
    assert "def _csrf_cookie_secure()" in src
