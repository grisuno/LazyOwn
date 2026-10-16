"""SDD regression tests for the CodeQL security batch.

Pins the fixed behavior so future changes cannot silently reintroduce
the flagged flaws: proxy SSRF guard, verified TLS by default, webhook
SSRF guard, encrypted channel secrets at rest, owner-only secret files,
traversal-proof yaml browsing, generic error responses, and a tightened
emoji pattern. Every test fails against the pre-fix code (verified by
mutation) and passes with the fix.
"""

from __future__ import annotations

import base64
import os
import stat
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_SERVER = None


def _server():
    """Load the C2 server file (lazyc2.py) explicitly.

    ``import lazyc2`` resolves to the ``lazyc2/`` package, not the
    server file, so the server module is loaded once from its path.
    """
    global _SERVER
    if _SERVER is None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("lazyc2_server", str(ROOT / "lazyc2.py"))
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _SERVER = module
    return _SERVER


class TestProxySsrfGuard:
    """CONTRACT: client-controlled proxy targets are validated server-side."""

    def test_allows_lab_targets_by_default(self):
        from modules.lazy_proxy import _validate_proxy_target

        assert _validate_proxy_target("127.0.0.1", 80, "http") == ("127.0.0.1", 80)
        assert _validate_proxy_target("localhost", 443, "https") == ("localhost", 443)
        assert _validate_proxy_target("10.0.0.9", 80, "http") == ("10.0.0.9", 80)

    def test_blocks_cloud_metadata(self):
        from modules.lazy_proxy import _validate_proxy_target

        for host in ("169.254.169.254", "169.254.169.253", "100.100.100.200", "fd00:ec2::254"):
            with pytest.raises(ValueError):
                _validate_proxy_target(host, 80, "http")
        for host in ("metadata.google.internal", "metadata.goog", "host.metadata.google.internal"):
            with pytest.raises(ValueError):
                _validate_proxy_target(host, 80, "http")

    def test_blocks_malformed_targets(self):
        from modules.lazy_proxy import _validate_proxy_target

        for host, port, scheme in (
            ("0.0.0.0", 80, "http"),
            ("224.0.0.1", 80, "http"),
            ("example.com", 0, "http"),
            ("example.com", 70000, "http"),
            ("example.com", 80, "ftp"),
            ("a@b", 80, "http"),
            ("has space", 80, "http"),
            ("", 80, "http"),
        ):
            with pytest.raises(ValueError):
                _validate_proxy_target(host, port, scheme)

    def test_blocks_private_when_operator_opts_out(self, monkeypatch):
        from modules.lazy_proxy import _validate_proxy_target

        monkeypatch.setenv("LAZY_PROXY_ALLOW_PRIVATE", "0")
        with pytest.raises(ValueError):
            _validate_proxy_target("10.0.0.9", 80, "http")
        with pytest.raises(ValueError):
            _validate_proxy_target("169.254.169.254", 80, "http")
        assert _validate_proxy_target("8.8.8.8", 443, "https") == ("8.8.8.8", 443)


class TestProxyTlsDefaults:
    """CONTRACT: upstream TLS verifies by default; insecure needs opt-in."""

    def test_verified_context_by_default(self, monkeypatch):
        import ssl

        from modules.lazy_proxy import _upstream_tls_context

        monkeypatch.delenv("LAZY_PROXY_INSECURE_TLS", raising=False)
        context = _upstream_tls_context("example.com")
        assert context.verify_mode == ssl.CERT_REQUIRED
        assert context.check_hostname is True
        assert context.minimum_version == ssl.TLSVersion.TLSv1_2

    def test_insecure_only_with_explicit_opt_in(self, monkeypatch):
        import ssl

        from modules.lazy_proxy import _upstream_tls_context

        monkeypatch.setenv("LAZY_PROXY_INSECURE_TLS", "1")
        context = _upstream_tls_context("example.com")
        assert context.verify_mode == ssl.CERT_NONE


class TestWebhookSsrfGuard:
    """CONTRACT: webhook delivery cannot be steered to metadata/loopback."""

    def test_blocks_metadata_and_userinfo_and_ftp(self):
        from modules.notify import url_allowed

        for url in (
            "http://169.254.169.254/latest/meta-data",
            "http://metadata.google.internal/",
            "http://[fd00:ec2::254]/",
            "http://user:pass@example.com/",
            "ftp://example.com/x",
        ):
            allowed, _ = url_allowed(url)
            assert allowed is False, url

    def test_loopback_needs_explicit_opt_in(self, monkeypatch):
        from modules.notify import url_allowed

        monkeypatch.delenv("LAZY_NOTIFY_ALLOW_LOCAL", raising=False)
        allowed, _ = url_allowed("http://127.0.0.1:8899/x")
        assert allowed is False
        monkeypatch.setenv("LAZY_NOTIFY_ALLOW_LOCAL", "1")
        allowed, _ = url_allowed("http://127.0.0.1:8899/x")
        assert allowed is True

    def test_allows_public_webhook(self):
        from modules.notify import url_allowed

        assert url_allowed("https://hooks.example/T1")[0] is True
        assert url_allowed("https://example.com/hook")[0] is True


class TestChannelSecrets:
    """CONTRACT: notifier passwords are scrubbed in transit, sealed at rest."""

    def test_scrub_masks_passwords_and_tokens(self):
        from modules.lazy_loop import scrub_secrets

        cleaned = scrub_secrets("login password= hunter2 api_key= sk-abc123XYZ bearer tok12345678 done")
        assert "hunter2" not in cleaned
        assert "sk-abc123XYZ" not in cleaned
        assert "tok12345678" not in cleaned

    def test_password_roundtrip_with_key(self, monkeypatch):
        from modules.lazy_loop import _decrypt_channel_secret, _encrypt_channel_secret

        monkeypatch.setenv("LAZYOWN_SECRET_KEY", "test-key-for-codeql-batch-0123456789")
        stored = _encrypt_channel_secret("secret")
        assert stored.startswith("enc:v1:")
        assert _decrypt_channel_secret(stored) == "secret"

    def test_password_roundtrip_without_key(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        monkeypatch.delenv("LAZYOWN_SECRET_KEY", raising=False)
        monkeypatch.setattr(loop, "BASE_DIR", tmp_path)
        assert loop._decrypt_channel_secret(loop._encrypt_channel_secret("secret")) == "secret"

    def test_channel_store_is_owner_only(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
        monkeypatch.delenv("LAZYOWN_SECRET_KEY", raising=False)
        loop.Notifier(None).add_channel("email", "smtp.example:587", extra={"to": "a@b.c", "password": "s3cret"})
        path = tmp_path / "notify_channels.json"
        assert path.exists()
        assert stat.S_IMODE(path.stat().st_mode) == 0o600


class TestReverseShellFallback:
    """CONTRACT: fallback token never reaches logs; owner-only file instead."""

    def test_secret_not_logged_and_file_restricted(self, tmp_path, monkeypatch, caplog):
        import logging

        lazyc2 = _server()

        monkeypatch.setattr(lazyc2, "SESSIONS_DIR", str(tmp_path))
        monkeypatch.setattr(lazyc2.config, "c2_reverse_shell_password", "")
        monkeypatch.setattr(lazyc2, "_REVERSE_SHELL_PASSWORD_CACHE", "")
        with caplog.at_level(logging.WARNING, logger="lazyc2"):
            value = lazyc2._resolve_reverse_shell_password()
        assert len(value) >= 32
        assert value not in caplog.text
        secret_file = tmp_path / ".reverse_shell_password"
        stored = secret_file.read_text().strip()
        assert stored, "sealed secret file must not be empty"
        assert stored != value, "secret file must be sealed, not plaintext"
        assert stat.S_IMODE(secret_file.stat().st_mode) == 0o600
        assert lazyc2._resolve_reverse_shell_password() == value


class TestViewYamlTraversal:
    """CONTRACT: yaml browsing stays inside the atomic base directory."""

    @staticmethod
    def _client(monkeypatch, tmp_path):
        lazyc2 = _server()

        monkeypatch.setattr(lazyc2, "check_auth", lambda u, p: True)
        monkeypatch.setattr(lazyc2, "atomic_framework_path", str(tmp_path))
        client = lazyc2.app.test_client()
        token = base64.b64encode(b"operator:any").decode("ascii")
        client.environ_base["HTTP_AUTHORIZATION"] = f"Basic {token}"
        return client

    def test_blocks_traversal_inputs(self, tmp_path, monkeypatch):
        client = self._client(monkeypatch, tmp_path)
        for evil in ("../..", "/etc", "a/../../b", "..%2f.."):
            response = client.post("/view_yaml", data={"directory": evil})
            assert response.status_code == 400, (evil, response.status_code)
        assert client.post("/view_yaml", data={"directory": ""}).status_code == 302

    def test_serves_valid_subdir_and_ignores_symlink_escape(self, tmp_path, monkeypatch):
        lazyc2 = _server()

        outside = tmp_path / "outside.yaml"
        outside.write_text("atomic_tests:\n  - {name: OUTSIDE-MARKER-9f8}\n")
        good = tmp_path / "T1059.001"
        good.mkdir()
        (good / "T1059.001.yaml").write_text(
            "atomic_tests:\n"
            "  - auto_generated_guid: abc\n"
            "    name: legit test\n"
            "    description: line1\n"
            "    supported_platforms: [windows]\n"
        )
        (good / "escape.yaml").symlink_to(outside)
        client = self._client(monkeypatch, tmp_path)
        response = client.post("/view_yaml", data={"directory": "T1059.001"})
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "legit test" in body
        assert "OUTSIDE-MARKER-9f8" not in body


def _login_and_call(monkeypatch, tmp_path, view, path):
    """Call a @login_required view as an authenticated operator."""
    import modules.lazy_loop as loop
    from flask_login import login_user

    lazyc2 = _server()

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(lazyc2.config, "c2_decoy_mode", "off")
    user = lazyc2.User({"id": 1, "username": "op", "password_hash": "x"})
    with lazyc2.app.test_request_context(path, environ_overrides={"REMOTE_ADDR": "127.0.0.1"}):
        login_user(user)
        return view()


class TestGenericErrorResponses:
    """CONTRACT: exception text never reaches HTTP clients (canary tests)."""

    def test_broadcast_hides_exception(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        lazyc2 = _server()

        monkeypatch.setattr(
            loop.LazyLoopEngine, "broadcast", lambda self, *a, **k: (_ for _ in ()).throw(RuntimeError("CANARY-BC-9f8"))
        )
        response, code = _login_and_call(monkeypatch, tmp_path, lazyc2.api_loop_broadcast, "/api/loop_broadcast?task=t")
        assert code == 404
        assert b"CANARY-BC-9f8" not in response.get_data()
        assert b"broadcast unavailable" in response.get_data()

    def test_loop_graph_hides_exception(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        lazyc2 = _server()

        monkeypatch.setattr(
            loop.LazyLoopEngine, "loop_graph", lambda self, *a, **k: (_ for _ in ()).throw(RuntimeError("CANARY-LG-9f8"))
        )
        response, code = _login_and_call(monkeypatch, tmp_path, lazyc2.api_loop_graph, "/api/loop_graph?task=t")
        assert code == 404
        assert b"CANARY-LG-9f8" not in response.get_data()

    def test_guard_lookup_hides_exception(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        lazyc2 = _server()

        monkeypatch.setattr(
            loop.Guard, "lookup", lambda self, *a, **k: (_ for _ in ()).throw(KeyError("CANARY-G-9f8"))
        )
        response, code = _login_and_call(
            monkeypatch, tmp_path, lazyc2.api_guard_audit, "/api/guard_audit?task=t&lookup=zzz"
        )
        assert code == 404
        assert b"CANARY-G-9f8" not in response.get_data()
        assert b"lookup not found" in response.get_data()

    def test_mentions_hide_exception(self, tmp_path, monkeypatch):
        import modules.lazy_mentions as mentions

        lazyc2 = _server()

        def _boom(*a, **k):
            raise mentions.InvalidCursor("CANARY-M-9f8")

        monkeypatch.setattr(mentions, "search_mentions_page", _boom)
        response, code = _login_and_call(monkeypatch, tmp_path, lazyc2.api_lazy_mentions, "/api/lazy_mentions")
        assert code == 400
        assert b"CANARY-M-9f8" not in response.get_data()

    def test_sse_stream_hides_exception(self, tmp_path, monkeypatch):
        import modules.lazy_loop as loop

        lazyc2 = _server()

        monkeypatch.setattr(
            loop.LazyLoopEngine,
            "broadcast_events",
            lambda self, *a, **k: (_ for _ in ()).throw(RuntimeError("CANARY-SSE-9f8")),
        )
        response = _login_and_call(
            monkeypatch, tmp_path, lazyc2.api_loop_broadcast_stream, "/api/loop_broadcast/stream?task=t&seconds=2"
        )
        data = "".join(response.response).encode("utf-8", "replace")
        assert b"CANARY-SSE-9f8" not in data
        assert b"event stream failed" in data

    def test_api_defaults_hide_exception(self, monkeypatch):
        import core.defaults as defaults
        from flask import Flask
        from lazyc2.blueprints import api as api_mod

        def _boom():
            raise ValueError("CANARY-D-9f8")

        monkeypatch.setattr(defaults, "load_defaults", _boom)
        app = Flask(__name__)
        app.register_blueprint(api_mod.api_bp)
        with app.test_request_context("/api/defaults"):
            response, code = api_mod.get_defaults()
        assert code == 500
        assert b"CANARY-D-9f8" not in response.get_data()


class TestEmojiPattern:
    """CONTRACT: emoji detection without an over-broad catch-all range."""

    def test_blocks_common_emoji_and_clean_text_passes(self):
        from skills.claude_md_orchestrator import validators

        assert validators.check_no_emoji("x='\U0001f600'", "s.py")
        assert not validators.check_no_emoji("value = 1", "s.py")

    def test_no_mega_range_in_source(self):
        source = (ROOT / "skills/claude_md_orchestrator/validators.py").read_text()
        assert "0001f300-\\U0001faff" not in source
