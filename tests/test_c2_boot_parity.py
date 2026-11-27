"""C2 boot-path parity contract tests.

The :func:`lazyc2.app_factory.create_app` factory is the canonical boot
path and must stay at security parity with the frozen ``lazyc2.py``
monolith: same blueprint surface, CSRF flow, CORS allowlist (never a
wildcard), CSP/security headers and a stable persisted secret key.
"""

import os
from pathlib import Path

import pytest

from lazyc2.app_factory import create_app
from lazyc2.blueprints import register_blueprints
from lazyc2.security.constants import CONTENT_SECURITY_POLICY

_EXPECTED_BLUEPRINTS = {
    "operations",
    "auth",
    "redirect",
    "api",
    "addons",
    "gym",
    "lazybox",
    "campaign",
    "loops",
    "listeners",
    "orchestrator",
    "api_v1",
}

_HEADER_PARITY = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}


@pytest.fixture(scope="module")
def app():
    """Build one factory app with a deterministic secret key.

    Blueprint objects are process singletons, so the app is built once
    per module. The ``LAZYOWN_SECRET_KEY`` environment variable is set
    only for the build and restored immediately: a lingering ``LAZYOWN_*``
    variable would leak into ``core.config`` env overrides for other
    tests.
    """
    sentinel_key = "LAZYOWN_SECRET_KEY"
    previous = os.environ.get(sentinel_key)
    os.environ[sentinel_key] = "parity-test-secret-key"
    try:
        from lazyc2.blueprints import reset_blueprint_registrations

        reset_blueprint_registrations()
        created = create_app()
    finally:
        if previous is None:
            os.environ.pop(sentinel_key, None)
        else:
            os.environ[sentinel_key] = previous
    return created


def test_all_blueprints_mounted(app):
    mounted = {rule.endpoint.split(".", 1)[0] for rule in app.url_map.iter_rules() if "." in rule.endpoint}
    missing = _EXPECTED_BLUEPRINTS - mounted
    assert not missing, f"boot path missing blueprints: {sorted(missing)}"


def test_security_headers_parity(app):
    with app.test_client() as client:
        response = client.get("/definitely-not-a-route")
    assert response.status_code == 404
    for header, value in _HEADER_PARITY.items():
        assert response.headers.get(header) == value, header


def test_csp_header_matches_shared_constant(app):
    with app.test_client() as client:
        response = client.get("/definitely-not-a-route")
    assert response.headers.get("Content-Security-Policy") == CONTENT_SECURITY_POLICY


def test_monolith_uses_shared_csp_constant():
    source = (Path(__file__).resolve().parents[1] / "lazyc2.py").read_text(encoding="utf-8")
    assert 'response.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY' in source


def test_secret_key_is_stable(app):
    assert app.secret_key == "parity-test-secret-key"


def test_secret_key_fails_closed(tmp_path, monkeypatch):
    import lazyc2.app_factory as factory

    monkeypatch.delenv("LAZYOWN_SECRET_KEY", raising=False)
    monkeypatch.setattr("lazyc2.security.services.SecretKeyManager.get_or_create", lambda self: "")
    with pytest.raises(RuntimeError):
        factory._load_or_create_secret_key(sessions_dir=str(tmp_path))


def test_socketio_cors_is_never_a_wildcard():
    source = (Path(__file__).resolve().parents[1] / "lazyc2" / "app_factory.py").read_text(encoding="utf-8")
    assert "cors_allowed_origins=cors_policy.origins_for_socketio()" in source
    assert 'cors_allowed_origins="*"' not in source

    from lazyc2.security.cors import CorsPolicy

    policy = CorsPolicy(env="DEV", lhost="127.0.0.1", allowed_origins="", c2_port=5000)
    assert "*" not in policy.origins_for_socketio()


def test_csrf_flow_is_wired(app):
    assert app.config["LAZYOWN_CSRF_POLICY"] is not None
    assert callable(app.config["LAZYOWN_CSRF_ENABLED_FN"])
    assert any("csrf" in getattr(fn, "__name__", "") for fn in app.before_request_funcs[None])


def test_register_blueprints_fails_closed_on_broken_blueprint(monkeypatch):
    monkeypatch.setattr("lazyc2.blueprints.init_loops_bp", lambda *args, **kwargs: None)

    class _BrokenApp:
        def register_blueprint(self, blueprint, **kwargs):
            raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        register_blueprints(_BrokenApp(), limiter=None)


def test_session_cookie_flags_follow_tls(app):
    secure = app.config["SESSION_COOKIE_SECURE"]
    assert app.config["REMEMBER_COOKIE_SECURE"] == secure
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
