"""End-to-end tests for the CSRF token flow of the LazyOwn C2 dashboard.

Wires the real production primitives (:mod:`lazyc2.security.csrf_flow` plus
:class:`lazyc2.security.csrf.CSRFPolicy`) into a minimal Flask app with
flask-login and drives the full operator journey: authenticated session ->
token delivery -> rejected tokenless POST -> accepted echoed POST.
"""

from __future__ import annotations

from functools import wraps

import pytest
from flask import Flask, jsonify, request
from flask_login import LoginManager, current_user

from lazyc2.security.csrf import CSRFPolicy
from lazyc2.security.csrf_flow import (
    SESSION_KEY,
    ensure_session_key,
    make_csrf_protect,
    register_csrf_flow,
    token_cookie_name,
)

CLI_USER = "operator"
CLI_PASSWORD = "s3cret-password"


def _build_app(csrf_enabled=True):
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "unit-test-secret"
    login_manager = LoginManager(app)
    login_manager.user_loader(lambda user_id: type("U", (), {"id": user_id, "is_authenticated": True})() if user_id else None)

    policy = CSRFPolicy()
    enabled_fn = lambda: csrf_enabled  # noqa: E731
    basic_authenticated_fn = lambda: bool(  # noqa: E731
        request.authorization
        and request.authorization.username == CLI_USER
        and request.authorization.password == CLI_PASSWORD
    )
    csrf_protect = make_csrf_protect(policy, enabled_fn, basic_authenticated_fn)
    register_csrf_flow(app, policy, enabled_fn)

    @app.route("/")
    def index():
        from flask import render_template_string

        return render_template_string("<input type='hidden' name='xsrf_token' value='{{ csrf_token }}'>")

    def requires_auth_or_session(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            auth = request.authorization
            if auth and auth.username == CLI_USER and auth.password == CLI_PASSWORD:
                return view(*args, **kwargs)
            if current_user.is_authenticated:
                return view(*args, **kwargs)
            return jsonify({"error": "unauthenticated"}), 401

        return wrapper

    @app.route("/issue_command", methods=["POST"])
    @requires_auth_or_session
    @csrf_protect
    def issue_command():
        return jsonify({"status": "success", "command": request.form.get("command", "")}), 200

    return app


def _login(client):
    with client.session_transaction() as sess:
        sess["_user_id"] = "1"
        sess["_fresh"] = True


def _read_token_cookie(client):
    return client.get_cookie(token_cookie_name())


class TestDashboardFlow:
    def test_authenticated_post_without_token_is_403(self) -> None:
        app = _build_app()
        client = app.test_client()
        _login(client)
        client.get("/")
        response = client.post("/issue_command", data={"command": "whoami"})
        assert response.status_code == 403

    def test_authenticated_post_with_echoed_token_is_200(self) -> None:
        app = _build_app()
        client = app.test_client()
        _login(client)
        client.get("/")
        token_cookie = _read_token_cookie(client)
        assert token_cookie is not None and token_cookie.value
        response = client.post(
            "/issue_command",
            data={"command": "whoami"},
            headers={"X-XSRF-TOKEN": token_cookie.value},
        )
        assert response.status_code == 200

    def test_hidden_form_field_fallback_is_200(self) -> None:
        app = _build_app()
        client = app.test_client()
        _login(client)
        client.get("/")
        token_cookie = _read_token_cookie(client)
        response = client.post(
            "/issue_command",
            data={"command": "whoami", "xsrf_token": token_cookie.value},
        )
        assert response.status_code == 200

    def test_get_renders_token_into_template(self) -> None:
        app = _build_app()
        client = app.test_client()
        _login(client)
        html = client.get("/").get_data(as_text=True)
        assert "xsrf_token" in html
        assert len(html.split("value='")[1].split("'")[0]) >= 32

    def test_token_is_stable_across_requests(self) -> None:
        app = _build_app()
        client = app.test_client()
        _login(client)
        client.get("/")
        first = _read_token_cookie(client).value
        client.get("/")
        second = _read_token_cookie(client).value
        assert first == second

    def test_anonymous_visitor_gets_no_token_and_is_rejected(self) -> None:
        app = _build_app()
        client = app.test_client()
        client.get("/")
        assert _read_token_cookie(client) is None
        response = client.post("/issue_command", data={"command": "whoami"})
        assert response.status_code == 401

    def test_wrong_token_is_403(self) -> None:
        app = _build_app()
        client = app.test_client()
        _login(client)
        client.get("/")
        response = client.post(
            "/issue_command",
            data={"command": "whoami"},
            headers={"X-XSRF-TOKEN": "forged-token"},
        )
        assert response.status_code == 403


class TestCliChannel:
    def test_basic_auth_post_without_token_is_allowed(self) -> None:
        app = _build_app()
        client = app.test_client()
        response = client.post(
            "/issue_command",
            data={"command": "whoami"},
            auth=(CLI_USER, CLI_PASSWORD),
        )
        assert response.status_code == 200

    def test_basic_auth_with_wrong_password_is_rejected(self) -> None:
        app = _build_app()
        client = app.test_client()
        response = client.post(
            "/issue_command",
            data={"command": "whoami"},
            auth=(CLI_USER, "wrong"),
        )
        assert response.status_code == 401


class TestGateToggle:
    def test_disabled_gate_allows_tokenless_post(self) -> None:
        app = _build_app(csrf_enabled=False)
        client = app.test_client()
        _login(client)
        response = client.post("/issue_command", data={"command": "whoami"})
        assert response.status_code == 200
        assert _read_token_cookie(client) is None


class TestSessionKeyBinding:
    def test_ensure_session_key_is_stable(self) -> None:
        app = _build_app()
        with app.test_request_context():
            from flask import session as flask_session

            first = ensure_session_key(flask_session)
            second = ensure_session_key(flask_session)
            assert first == second
            assert flask_session[SESSION_KEY] == first

    def test_lazyc2_wires_the_real_flow(self) -> None:
        src = open("lazyc2.py", encoding="utf-8").read()
        assert "_register_csrf_flow(app, _csrf_policy, _csrf_enabled, secure_fn=_csrf_cookie_secure)" in src
        assert "def _csrf_cookie_secure()" in src
        assert "csrf_protect = _make_csrf_protect(_csrf_policy, _csrf_enabled, _basic_authenticated)" in src


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
